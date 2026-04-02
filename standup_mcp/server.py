import os
import json
from datetime import datetime

import cohere
from fastmcp import FastMCP
from notion_client import Client

mcp = FastMCP("standup-bot")

_REQUIRED_ENV = ["NOTION_TOKEN", "NOTION_DATABASE_ID", "COHERE_API_KEY"]


def _check_env():
    missing = [k for k in _REQUIRED_ENV if not os.getenv(k)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Run `standup-mcp init` to set them up."
        )


def _notion():
    return Client(auth=os.environ["NOTION_TOKEN"])


def _cohere():
    return cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])


def _append_to_notion(tasks: list[str]) -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"📅 {today}"}}]
            },
        }
    ] + [
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": task}}]
            },
        }
        for task in tasks
    ]
    return _notion().blocks.children.append(block_id=os.environ["NOTION_DATABASE_ID"], children=blocks)


@mcp.tool()
def add_task_to_notion(tasks: list[str]) -> str:
    """
    Add today's standup tasks to the Notion page.
    Call this after extracting the list of tasks from the user's message.

    Args:
        tasks: List of task strings, e.g. ["jwt API", "dashboard"]
    """
    _append_to_notion(tasks)
    return f"Added {len(tasks)} task(s) to Notion: {', '.join(tasks)}"


@mcp.tool()
def log_standup(message: str) -> str:
    """
    Parse a natural language standup message and add the tasks to Notion.
    Example input: "today I worked on jwt API and dashboard"

    Args:
        message: Natural language standup update from the user
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task_to_notion",
                "description": "Add extracted tasks to Notion page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tasks": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of individual tasks extracted from the message",
                        }
                    },
                    "required": ["tasks"],
                },
            },
        }
    ]

    _check_env()
    response = _cohere().chat(
        model="command-a-03-2025",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a standup assistant. Extract individual tasks from the user's "
                    "message and call add_task_to_notion with the list. "
                    "For example: 'today I worked on jwt API and dashboard' → tasks=['jwt API', 'dashboard']"
                ),
            },
            {"role": "user", "content": message},
        ],
        tools=tools,
    )

    for tool_call in response.message.tool_calls or []:
        if tool_call.function.name == "add_task_to_notion":
            args = json.loads(tool_call.function.arguments)
            return add_task_to_notion(args["tasks"])

    return "Could not extract tasks from the message."


def main():
    mcp.run()
