import sys
import json
from pathlib import Path

_MCP_JSON_TEMPLATE = {
    "mcpServers": {
        "standup": {
            "command": "uvx",
            "args": ["standup-mcp"],
            "env": {
                "NOTION_TOKEN": "YOUR_NOTION_TOKEN_HERE",
                "NOTION_DATABASE_ID": "YOUR_NOTION_PAGE_ID_HERE",
                "COHERE_API_KEY": "YOUR_COHERE_API_KEY_HERE",
            },
        }
    }
}


def _init():
    target = Path.cwd() / ".mcp.json"

    if target.exists():
        print(f"[standup-mcp] .mcp.json already exists at {target}")
        print("Edit it to add your credentials if you haven't already.")
        return

    target.write_text(json.dumps(_MCP_JSON_TEMPLATE, indent=2) + "\n")
    print(f"[standup-mcp] Created {target}\n")
    print("Next steps:")
    print("  1. Open .mcp.json and replace the placeholder values:")
    print("       NOTION_TOKEN       — your Notion integration secret")
    print("       NOTION_DATABASE_ID — the ID of your Notion page")
    print("       COHERE_API_KEY     — your Cohere API key")
    print()
    print("  2. Restart your AI agent / Claude Code session.")
    print()
    print("  3. Tell your agent:")
    print('       "log my standup — today I worked on jwt API and dashboard"')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        _init()
    else:
        from standup_mcp.server import mcp
        mcp.run()
