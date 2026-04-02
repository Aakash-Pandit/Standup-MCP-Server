# standup-mcp

An MCP server that logs your daily standups to Notion using natural language.

Tell your AI agent:
> "log my standup — today I worked on jwt API and dashboard"

It extracts the tasks (via Cohere) and appends them as a dated bullet list to your Notion page.

---

## Prerequisites

Before starting, make sure you have:

- Python 3.10+
- `uv` installed — [install uv](https://docs.astral.sh/uv/getting-started/installation/)
- A [Notion account](https://notion.so) with a page to log standups to
- A [Cohere account](https://cohere.com) for natural language parsing

---

## Step-by-step setup

### Step 1 — Get your Notion token

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Give it a name (e.g. "Standup MCP") and click **Save**
4. Copy the **Internal Integration Secret** — this is your `NOTION_TOKEN`

### Step 2 — Get your Notion database ID

1. Open your Notion page in the browser
2. Look at the URL: `https://www.notion.so/<workspace>/<PAGE_ID>?v=...`
3. Copy the `PAGE_ID` part — this is your `NOTION_DATABASE_ID`
4. **Important:** Share the page with your integration:
   - Open the Notion page
   - Click **...** (top right) → **Connections** → select your integration

### Step 3 — Get your Cohere API key

1. Go to [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
2. Click **New API key**
3. Copy the key — this is your `COHERE_API_KEY`

### Step 4 — Install the package

Install globally so Claude Code can run it as an MCP server:

```bash
uv tool install standup-mcp
```

Or with `pipx`:

```bash
pipx install standup-mcp
```

### Step 5 — Run the setup wizard

Navigate to your project directory and run:

```bash
cd your-project
standup-mcp init
```

The wizard will prompt you for each token:

```
[standup-mcp] Setup wizard
========================================

  NOTION_TOKEN — your Notion integration secret
  Get it at: notion.so/my-integrations → New integration → copy the secret
  > secret_xxxxxxxxxxxx

  NOTION_DATABASE_ID — your Notion database ID
  Open your Notion database in browser → copy the ID from the URL
  > abc123xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  COHERE_API_KEY — your Cohere API key
  Get it at: dashboard.cohere.com/api-keys
  > xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[standup-mcp] Created .mcp.json

All done! Next step:
  Restart your Claude Code session, then tell your agent:
  "log my standup — today I worked on X and Y"
```

This creates (or updates) `.mcp.json` in your project with the correct config and your credentials filled in.

> If `.mcp.json` already exists with other MCP servers, `init` will safely merge the `standup` entry without touching the rest.

### Step 6 — Restart Claude Code

Close and reopen your Claude Code session (or run `/mcp` to verify the server loaded).

You should see `standup` listed as a connected MCP server.

### Step 7 — Log your standup

Just tell your agent:

```
log my standup — today I worked on jwt API and dashboard
```

The server will parse your message, extract individual tasks, and append them to your Notion page under today's date like this:

```
📅 2026-04-02
• jwt API
• dashboard
```

---

## Troubleshooting

**MCP server shows as "failed" in `/mcp list`**

This usually means the credentials in `.mcp.json` are wrong or missing. Re-run the wizard to fix them:

```bash
standup-mcp init
```

Then restart Claude Code.

**Notion page not updating**

Make sure your Notion integration has been granted access to the target page:
- Open the page in Notion → click **...** → **Connections** → add your integration

**`standup-mcp: command not found`**

The package isn't installed globally. Run:

```bash
uv tool install standup-mcp
```

---

## How it works

1. Your agent calls the `log_standup` MCP tool with your natural language message
2. Cohere extracts individual tasks via tool use
3. Tasks are appended to your Notion page as a dated bullet list

---

## Requirements

- Python 3.10+
- `uv` or `pipx` for global installation
