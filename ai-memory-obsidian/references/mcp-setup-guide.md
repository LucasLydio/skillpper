# MCP Setup Guide for Memory & Obsidian 🔌

This guide explains how to connect your AI coding agent (Claude Code, Antigravity, Cursor, etc.) to Obsidian vaults and persistent memory engines.

---

## 1. Connecting via Obsidian Local REST API MCP

The most accessible method to grant agents vault access is the community **Local REST API** plugin paired with an Obsidian MCP server.

### Step 1: Inside Obsidian
1. Open Obsidian and navigate to **Settings** → **Community plugins**.
2. Install and enable the **Local REST API** plugin.
3. Retrieve your **API Key** from the plugin settings page.

### Step 2: Agent Configuration
Add the server entry to your `claude.json`, `.gemini/settings.json`, or relevant agent configuration file:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-obsidian"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "YOUR_API_KEY_HERE",
        "OBSIDIAN_BASE_URL": "https://127.0.0.1:27124"
      }
    }
  }
}
```

---

## 2. Local Memory Engine with `ai-memory`

`ai-memory` is a high-performance local daemon providing SQLite FTS5 full-text indexing, periodic memory retention, and cross-agent handoff management.

### Architecture:
1. Runs locally in the background, listening on default port `49374`.
2. Exposes HTTP endpoints and stdio MCP bridging.
3. Enables sub-10ms queries across hundreds of historical sessions without token re-reading overhead.

### Stdio Bridge Configuration:
```json
{
  "mcpServers": {
    "ai-memory": {
      "command": "ai-memory",
      "args": ["mcp-bridge"]
    }
  }
}
```

---

## 3. Direct Filesystem Access (Zero MCP Mode)

If you do not run MCP servers, agents can manipulate vault files directly if the vault folder is mounted or symlinked in the project workspace:
- Place notes under `docs/notes/` or create a directory symlink to your vault root.
- The agent reads, creates, and edits standard Markdown notes with zero external protocol dependencies.
