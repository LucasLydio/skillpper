---
name: ai-memory-obsidian
description: >-
  Portable workflows for persistent memory and Obsidian across macOS, Linux, and Windows. Use when the user asks to recall or save past context, record decisions, create vault notes, or configure ai-memory, Obsidian CLI, or an Obsidian MCP bridge.
---

# AI Memory & Obsidian 🧠📚

A skill providing **long-term persistent memory** and documentation governance for AI coding agents (Claude Code, Antigravity, Cursor, and others) using local **Obsidian** vaults and memory engines such as **ai-memory**.

This skill supports macOS, Linux, and Windows. Choose native paths and agent configuration for the user's environment; see the [Cross-Platform Setup Guide](references/cross-platform-setup.md).

---

## ⚡ Quick Install

```bash
npx skills add https://github.com/kipperdev/skillpper --skill ai-memory-obsidian
```

---

## 🎯 Why Persistent Memory?

By default, AI coding agents are amnesic: every `/clear` or fresh session discards past conversational history, architectural trade-offs, and domain knowledge.

This skill equips agents with a systematic protocol to:
1. **Check Memory First**: Search local vault notes before re-reading dozens of repository files or asking the developer to restate previous decisions.
2. **Document Decisions Automatically**: Log Architectural Decision Records (ADRs) and atomic notes in standardized Markdown.
3. **Execute Frictionless Handoffs**: Wrap up sessions with structured state snapshots and 1-line resume commands.

---

## ⚙️ Integration Modes (MCP & Local Vault)

Agents can connect to Obsidian through three interfaces:

1. **MCPVault filesystem bridge**:
   - Reads and writes the vault directory through MCP using `@bitbonsai/mcpvault`; Obsidian does not need to be running.
2. **Official Obsidian CLI**:
   - Controls the desktop app through shell commands. It requires Obsidian 1.12.7+ and the app running.
3. **Local REST API bridge**:
   - Uses the Obsidian Local REST API community plugin with a compatible MCP server.

These options work across macOS, Linux, and Windows when configured with the native vault path and the chosen agent's supported MCP or shell setup. See the [Cross-Platform Setup Guide](references/cross-platform-setup.md).

The **`ai-memory` daemon** provides a separate persistent memory interface:
   - A background local service indexing agent sessions, tool observations, and handoffs in SQLite/FTS5.
   - Enables full-text queries via CLI or MCP (`memory_query`, `memory_status`).

*(See comprehensive setup instructions in the [MCP Setup Guide](references/mcp-setup-guide.md)).*

---

## 📋 Execution Protocol

### 1. Task Inception (The "Memory First" Rule)
- When a task refers to past context ("as we discussed", "resume where we left off", "according to our decision"):
  - Search configured memory tools first (for example, `memory_query` or the Obsidian MCP search/read tools).
  - Provide a concise 1-line confirmation to the developer:
    `🧠 Memory consulted: Found records in [[Architecture-Decision-JWT]] and [[Session-2026-09-25]].`
  - If no memory integration is configured, continue from available context and offer setup only when it would help; do not assume a vault path.

### 2. Active Development (Capturing Decisions)
- When a significant technical decision is finalized (library choice, naming convention, schema design):
  - Draft or write an ADR in `decisions/ADR-YYYY-MM-DD-<slug>.md`.
  - Use standard ADR statuses (`accepted`, `proposed`, `superseded`).
  - If no vault is configured, keep the decision in the project's existing documentation or ask whether the user wants to configure a vault.

### 3. Session Wrap-up (Handoff & Daily Note)
- When reaching logical milestones or session limits:
  - Generate an end-of-session note in `sessions/Session-YYYY-MM-DD-<id>.md` or append to `dailies/Daily-YYYY-MM-DD.md`.
  - Provide a 1-line resume command for the user to paste into the next session.
  - Use automatic ai-memory handoff when the agent already provides it; avoid duplicating the same handoff in a vault note.

---

## 🛡️ Markdown & Obsidian Integrity Rules

1. **HTML/JSX Encapsulation**: Obsidian renders HTML directly in its DOM. NEVER leave raw HTML tags or unclosed JSX elements in markdown bodies (always enclose in ````html ... ```` or ````jsx ... ````). Unbalanced tags corrupt the editor's visual hierarchy.
2. **Clean Wikilinks**: Prefer standard `[[Note-Name]]` internal links to keep the Obsidian knowledge graph interconnected.
3. **Additive History**: Session logs and daily entries are strictly additive. Never summarize by destructively overwriting previous notes.

---

## 📚 Supporting References

- [MCP Setup Guide (Obsidian & ai-memory)](references/mcp-setup-guide.md)
- [Note Templates (ADRs, Sessions, and Dailies)](references/note-templates.md)
- [Cross-Session Handoff Protocol](references/handoff-protocol.md)
- [Cross-Platform Setup Guide](references/cross-platform-setup.md)
