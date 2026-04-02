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


def _prompt(label: str, hint: str) -> str:
    print(f"\n  {label}")
    print(f"  {hint}")
    while True:
        value = input("  > ").strip()
        if value:
            return value
        print("  (cannot be empty, please try again)")


def _init():
    target = Path.cwd() / ".mcp.json"

    print("\n[standup-mcp] Setup wizard")
    print("=" * 40)

    notion_token = _prompt(
        "NOTION_TOKEN — your Notion integration secret",
        "Get it at: notion.so/my-integrations → New integration → copy the secret",
    )
    notion_db_id = _prompt(
        "NOTION_DATABASE_ID — your Notion database ID",
        "Open your Notion database in browser → copy the ID from the URL (notion.so/<ID>?v=...)",
    )
    cohere_key = _prompt(
        "COHERE_API_KEY — your Cohere API key",
        "Get it at: dashboard.cohere.com/api-keys",
    )

    config = {
        "command": "uvx",
        "args": ["standup-mcp"],
        "env": {
            "NOTION_TOKEN": notion_token,
            "NOTION_DATABASE_ID": notion_db_id,
            "COHERE_API_KEY": cohere_key,
        },
    }

    if target.exists():
        existing = json.loads(target.read_text())
        servers = existing.setdefault("mcpServers", {})
        if "standup" in servers:
            print(f"\n  'standup' already present in {target} — updating credentials.")
        servers["standup"] = config
        target.write_text(json.dumps(existing, indent=2) + "\n")
        print(f"\n[standup-mcp] Updated {target}")
    else:
        target.write_text(json.dumps({"mcpServers": {"standup": config}}, indent=2) + "\n")
        print(f"\n[standup-mcp] Created {target}")

    print("\nAll done! Next step:")
    print("  Restart your Claude Code session, then tell your agent:")
    print('  "log my standup — today I worked on X and Y"\n')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        _init()
    else:
        from standup_mcp.server import mcp
        mcp.run()
