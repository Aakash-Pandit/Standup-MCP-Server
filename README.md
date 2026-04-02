# standup-mcp

An MCP server that logs your daily standups to Notion using natural language.

Tell your AI agent:
> "log my standup — today I worked on jwt API and dashboard"

It extracts the tasks (via Cohere) and appends them as a dated bullet list to your Notion page.

---

## Quick start

### 1. Install &amp; add `.mcp.json` to your repo

Pick one — run this once inside your project directory:

**Using `uvx` (no install needed):**
```bash
uvx standup-mcp init
```

**Using `pip`:**
```bash
pip install standup-mcp
standup-mcp init
```

This creates a `.mcp.json` file:

```json
{
  "mcpServers": {
    "standup": {
      "command": "uvx",
      "args": ["standup-mcp"],
      "env": {
        "NOTION_TOKEN": "YOUR_NOTION_TOKEN_HERE",
        "NOTION_DATABASE_ID": "YOUR_NOTION_PAGE_ID_HERE",
        "COHERE_API_KEY": "YOUR_COHERE_API_KEY_HERE"
      }
    }
  }
}
```

### 3. Fill in your credentials

| Key | Where to get it |
|-----|----------------|
| `NOTION_TOKEN` | [Create a Notion integration](https://www.notion.so/my-integrations) → copy the **Internal Integration Secret** |
| `NOTION_DATABASE_ID` | Open your Notion page in the browser → copy the ID from the URL (`notion.so/<workspace>/<PAGE_ID>?...`) |
| `COHERE_API_KEY` | [Cohere dashboard](https://dashboard.cohere.com/api-keys) |

> Make sure your Notion integration has access to the target page (share the page with your integration).

### 4. Restart your AI agent / Claude Code session

The MCP server is picked up automatically from `.mcp.json`.

### 5. Log a standup

Just tell your agent:

```
log my standup — today I worked on jwt API and dashboard
```

The server will parse the message, extract individual tasks, and append them to your Notion page under today's date.

---

## How it works

1. Your agent calls the `log_standup` MCP tool with your natural language message.
2. Cohere extracts individual tasks via tool use.
3. The tasks are appended to your Notion page as a dated bullet list.

---

## Requirements

- Python 3.10+
- `uv` (for `uvx`) or `pip`
