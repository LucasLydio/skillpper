---
name: ai-memory-obsidian
description: >-
  Long-term persistent memory and continuous documentation for AI agents using Obsidian and ai-memory. Enables agents to record architectural decision records (ADRs), session digests, daily logs, and atomic notes in local vaults via MCP servers (Obsidian Local REST API / CLI or ai-memory). Use when the user requests saving or recalling past session context, managing cross-agent state, capturing durable project decisions, or creating structured notes in an Obsidian vault.
---

# AI Memory & Obsidian 🧠📚

A skill providing **long-term persistent memory** and documentation governance for AI coding agents (Claude Code, Antigravity, Cursor, and others) using local **Obsidian** vaults and memory engines such as **ai-memory**.

---

## ⚡ Quick Install

```bash
npx skills add kipperdev/skillpper --skill ai-memory-obsidian
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

Agents connect to Obsidian vaults through two primary interfaces:

1. **Obsidian Local REST API / Obsidian CLI (Direct Vault Access)**:
   - Reads, searches, and appends notes directly in your vault filesystem via Obsidian MCP tools (`@bitbonsai/mcpvault` or `mcp-obsidian-local`).
   - Ideal for developers already using Obsidian as a personal or team knowledge base.
2. **`ai-memory` Daemon (Semantic & FTS5 Search)**:
   - A background local service indexing agent sessions, tool observations, and handoffs in SQLite/FTS5.
   - Enables millisecond full-text queries via CLI or MCP (`memory_query`, `memory_status`).

*(See comprehensive setup instructions in the [MCP Setup Guide](references/mcp-setup-guide.md)).*

---

## 📋 Execution Protocol

### 1. Task Inception (The "Memory First" Rule)
- When a task refers to past context ("as we discussed", "resume where we left off", "according to our decision"):
  - Search the vault first (`search_notes`, `read_note`, or `ai-memory search`).
  - Provide a concise 1-line confirmation to the developer:
    `🧠 Memory consulted: Found records in [[Architecture-Decision-JWT]] and [[Session-2026-09-25]].`
  - If no prior records exist, proceed with standard cold analysis without delaying execution.

### 2. Active Development (Capturing Decisions)
- When a significant technical decision is finalized (library choice, naming convention, schema design):
  - Draft or write an ADR in `decisions/ADR-YYYY-MM-DD-<slug>.md`.
  - Use standard ADR statuses (`accepted`, `proposed`, `superseded`).

### 3. Session Wrap-up (Handoff & Daily Note)
- When reaching logical milestones or session limits:
  - Generate an end-of-session note in `sessions/Session-YYYY-MM-DD-<id>.md` or append to `dailies/Daily-YYYY-MM-DD.md`.
  - Provide a 1-line resume command for the user to paste into the next session.

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
