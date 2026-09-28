# MCP Setup Guide for Memory & Obsidian 🔌

This guide explains how to connect your AI coding agent (Claude Code, Antigravity, Cursor, etc.) to Obsidian vaults and persistent memory engines.

For platform-specific vault paths, data directories, and CLI behavior, see the [Cross-Platform Setup Guide](cross-platform-setup.md).

---

## 1. Connecting to Obsidian via MCP

Choose the connection method that matches your agent and operating system:

### Option A: Direct Filesystem Bridge via `@bitbonsai/mcpvault` (Recommended — Zero Plugins Required)
[`@bitbonsai/mcpvault`](https://www.npmjs.com/package/@bitbonsai/mcpvault) connects directly to your vault folder on disk. It requires no community plugins, no API keys, and works even when Obsidian is closed:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "@bitbonsai/mcpvault",
        "/absolute/path/to/your/Obsidian/Vault"
      ]
    }
  }
}
```

### Option B: Official Obsidian CLI (No MCP server required)

If your agent can run shell commands, the official CLI can search and edit the vault through the Obsidian desktop app:

```shell
obsidian search query="architecture decisions"
obsidian daily
```

The CLI requires the Obsidian 1.12.7+ installer, command-line interface enabled in Settings, and the Obsidian app running. Registration differs by operating system; follow the [official CLI setup guide](https://obsidian.md/help/cli).

### Option C: REST API Bridge via `mcp-obsidian-local` (For Obsidian Local REST API Plugin)
If you already use the popular **Local REST API** community plugin inside Obsidian:
1. Open Obsidian → **Settings** → **Community plugins** → install and enable **Local REST API**.
2. Copy your generated **API Key**.
3. Configure [`mcp-obsidian-local`](https://www.npmjs.com/package/mcp-obsidian-local) in your agent configuration:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-obsidian-local"
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

[`ai-memory`](https://github.com/akitaonrails/ai-memory) is a high-performance local daemon developed by Fabio Akita for cross-session continuity, SQLite FTS5 full-text indexing, and automated multi-agent handoffs.

### Architecture & Capabilities:
1. Runs locally in the background, listening on default port `49374`.
2. Exposes HTTP endpoints and stdio MCP bridging.
3. Enables sub-10ms full-text search across hundreds of historical sessions without token re-reading overhead.

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

To install and compile the `ai-memory` daemon, follow the official setup instructions at [github.com/akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory).

---

## 3. Direct Filesystem Access (Zero MCP Mode)

If you prefer not to run MCP servers, agents can manipulate vault files directly if the vault folder is mounted or symlinked in the project workspace:
- Place notes under `docs/notes/` or create a directory symlink to your vault root.
- The agent reads, creates, and edits standard Markdown notes with zero external protocol dependencies.
