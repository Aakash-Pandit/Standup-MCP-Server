import os
import shutil
import sys
import json
from pathlib import Path


def _prompt(label: str, hint: str) -> str:
    print(f"\n  {label}")
    print(f"  {hint}")
    while True:
        value = input("  > ").strip()
        if value:
            return value
        print("  (cannot be empty, please try again)")


def _env_already_set() -> list[str]:
    keys = ["NOTION_TOKEN", "NOTION_DATABASE_ID", "COHERE_API_KEY"]
    return [k for k in keys if os.getenv(k)]


def _write_to_zshrc(notion_token: str, notion_db_id: str, cohere_key: str):
    zshrc = Path.home() / ".zshrc"
    block = (
        "\n# standup-mcp\n"
        f'export NOTION_TOKEN="{notion_token}"\n'
        f'export NOTION_DATABASE_ID="{notion_db_id}"\n'
        f'export COHERE_API_KEY="{cohere_key}"\n'
    )

    existing = zshrc.read_text() if zshrc.exists() else ""

    if "# standup-mcp" in existing:
        # Replace existing block
        lines = existing.splitlines(keepends=True)
        new_lines = []
        skip = False
        for line in lines:
            if line.strip() == "# standup-mcp":
                skip = True
                new_lines.append(block)
                continue
            if skip and line.startswith("export ") and any(
                k in line for k in ["NOTION_TOKEN", "NOTION_DATABASE_ID", "COHERE_API_KEY"]
            ):
                continue
            skip = False
            new_lines.append(line)
        zshrc.write_text("".join(new_lines))
    else:
        with zshrc.open("a") as f:
            f.write(block)

    print(f"\n  Written to {zshrc}")


def _init():
    target = Path.cwd() / ".mcp.json"

    print("\n[standup-mcp] Setup wizard")
    print("=" * 40)

    already_set = _env_already_set()
    if already_set:
        print(f"\n  Found existing env vars: {', '.join(already_set)}")
        print("  Press Enter to keep them, or type a new value to replace.")

    print("\n  Tokens will be saved to ~/.zshrc (not in .mcp.json).")
    print("  This keeps your credentials secure and works across all projects.\n")

    notion_token = _prompt(
        "NOTION_TOKEN — your Notion integration secret",
        "Get it at: notion.so/my-integrations → New integration → copy the secret",
    )
    notion_db_id = _prompt(
        "NOTION_DATABASE_ID — your Notion page ID",
        "Open your Notion page in browser → copy the ID from the URL (notion.so/<workspace>/<ID>)",
    )
    cohere_key = _prompt(
        "COHERE_API_KEY — your Cohere API key",
        "Get it at: dashboard.cohere.com/api-keys",
    )

    _write_to_zshrc(notion_token, notion_db_id, cohere_key)

    # Apply to current process immediately
    os.environ["NOTION_TOKEN"] = notion_token
    os.environ["NOTION_DATABASE_ID"] = notion_db_id
    os.environ["COHERE_API_KEY"] = cohere_key

    # Write .mcp.json without any credentials
    binary = shutil.which("standup-mcp")
    if binary:
        command, args = binary, []
    else:
        command, args = "uvx", ["standup-mcp"]

    config = {"command": command, "args": args}

    if target.exists():
        existing = json.loads(target.read_text())
        servers = existing.setdefault("mcpServers", {})
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
