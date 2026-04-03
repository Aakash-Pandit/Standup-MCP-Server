# standup-mcp

> A Model Context Protocol (MCP) server that logs your daily standups to Notion using natural language.

Tell your AI agent:
```
log my standup — today I worked on jwt API and dashboard
```

It parses your message, extracts individual tasks via Cohere, and appends them as a dated bullet list to your Notion page — no forms, no templates, just plain English.

---

## How it works

```
You (natural language)
        ↓
   Claude Code
        ↓
  log_standup tool  ←── MCP server (this repo)
        ↓
  Cohere API  (extracts tasks)
        ↓
  Notion API  (appends to your page)
```

---

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) or [pipx](https://pipx.pypa.io/stable/installation/) installed
- A Notion account with a page to log standups to
- A Cohere account for natural language parsing

---

## Setup

### Step 1 — Get your Notion token

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration** → give it a name → click **Save**
3. Copy the **Internal Integration Secret** → this is your `NOTION_TOKEN`

### Step 2 — Get your Notion page ID

1. Open your Notion standup page in the browser
2. Copy the ID from the URL:
   ```
   https://www.notion.so/myworkspace/Daily-Standup-abc123def456...
                                                    ^^^^^^^^^^^^^^^^
                                                    this is your NOTION_DATABASE_ID
   ```
3. Share the page with your integration:
   - Open the page → click **...** (top right) → **Connections** → select your integration

### Step 3 — Get your Cohere API key

1. Go to [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
2. Click **New API key** → copy it → this is your `COHERE_API_KEY`

### Step 4 — Install the package

Install directly from GitHub (no PyPI needed):

```bash
# using uv (recommended)
uv tool install git+https://github.com/Aakash-Pandit/standup-mcp-server

# using pipx
pipx install git+https://github.com/Aakash-Pandit/standup-mcp-server
```

### Step 5 — Run the setup wizard

Navigate to your project and run:

```bash
cd your-project
standup-mcp init
```

The wizard will:
- Prompt for your three credentials
- Save them to `~/.zshrc` (not in `.mcp.json` — keeps tokens off the repo)
- Apply them to your current session automatically
- Create `.mcp.json` in your project with no credentials inside

```
[standup-mcp] Setup wizard
========================================

  NOTION_TOKEN — your Notion integration secret
  Get it at: notion.so/my-integrations → New integration → copy the secret
  > secret_xxxxxxxxxxxxxxxxxxxx

  NOTION_DATABASE_ID — your Notion page ID
  Open your Notion page in browser → copy the ID from the URL
  > abc123xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  COHERE_API_KEY — your Cohere API key
  Get it at: dashboard.cohere.com/api-keys
  > xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  Written to /Users/you/.zshrc

[standup-mcp] Created .mcp.json

All done! Next step:
  Restart your Claude Code session, then tell your agent:
  "log my standup — today I worked on X and Y"
```

> If `.mcp.json` already exists with other MCP servers configured, `init` safely merges the `standup` entry without modifying anything else.

### Step 6 — Restart Claude Code

Close and reopen your Claude Code session. Verify the server loaded:

```
/mcp
```

You should see `standup` listed with a connected status.

### Step 7 — Log your standup

Tell your agent in plain English:

```
log my standup — today I worked on jwt API and dashboard
```

It will append to your Notion page:

```
📅 2026-04-03
• jwt API
• dashboard
```

---

## Credentials summary

| Key | Where to get it |
|-----|----------------|
| `NOTION_TOKEN` | [notion.so/my-integrations](https://www.notion.so/my-integrations) → New integration → Internal Integration Secret |
| `NOTION_DATABASE_ID` | Your Notion page URL → the long ID after the workspace name |
| `COHERE_API_KEY` | [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys) |

Tokens are stored in `~/.zshrc` — never in `.mcp.json` or the repo.

---

## Troubleshooting

**`standup` shows as failed in `/mcp list`**

Credentials are likely missing or incorrect. Re-run the wizard:
```bash
standup-mcp init
```
Then restart Claude Code.

**Notion page not updating**

Your integration doesn't have access to the page:
- Open the Notion page → **...** → **Connections** → add your integration

**`standup-mcp: command not found`**

The package isn't installed. Run:
```bash
uv tool install git+https://github.com/Aakash-Pandit/standup-mcp-server
```

**Claude starts working on my repo instead of logging standup**

The MCP server isn't connected. Check `/mcp` — if `standup` isn't listed, re-run `standup-mcp init` and restart the session.

---

## Stack

| Layer | Tool |
|-------|------|
| MCP framework | [FastMCP](https://github.com/jlowin/fastmcp) |
| NLP / task extraction | [Cohere](https://cohere.com) |
| Storage | [Notion](https://notion.so) |
| Runtime | Python 3.10+ |
