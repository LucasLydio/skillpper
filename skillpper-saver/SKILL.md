---
name: skillpper-saver
description: >-
  Aggressive token, context, and cost optimization mode for AI coding agents (Claude Code, Antigravity, Cursor, etc.). Prevents marathon sessions, eliminates redundant file re-reading, prioritizes text extraction over screenshots in browser automation, and manages context windows with surgical cutoff triggers. Use when the user requests token savings, context optimization, quota conservation, or when starting extensive refactoring, browsing, or debugging tasks.
---

# Skillpper Saver 🐿️⚡

A governance and aggressive optimization skill designed to reduce token consumption, operating costs, and context window bloating for AI coding agents.

Based on empirical development metrics: the primary drivers of runaway token consumption are not high-end models themselves, but rather **marathon sessions** (threads running for tens of hours), **repetitive re-reading of identical files**, **unnecessary screenshots during web automation**, and **dumping massive terminal logs** directly into the context window.

---

## 🎯 When to Use

Activate this skill when:
- The user asks to "save tokens", "reduce cost", "run in saver mode", "skillpper saver", "muri saver", or `/saver`.
- The developer operates under strict API budgets or session window rate limits (e.g., 5-hour rolling quotas or weekly caps).
- The task requires deep exploration of large codebases, complex debugging, or multi-step browser QA.

---

## ⚙️ Universal Execution Rules

### 1. Direct Responses Without Slop
- **Zero Preamble**: Never repeat the user's prompt or provide conversational filler ("Sure thing!", "I would be happy to help with that...").
- **Concise Summaries**: Limit completion responses to 1–2 actionable sentences highlighting what was changed or the immediate next step.
- **No Code Mirroring**: Never restate large blocks of unchanged code. Only display concise git diffs or edited segments.

### 2. Surgical File Reading
- **Grep/Glob First**: Never read entire files to find a single declaration or symbol. Locate the exact line range first using targeted search.
- **Partial Reads**: For files exceeding 100 lines, use line slicing (`StartLine`/`EndLine` or `offset`/`limit`) instead of loading the entire content.
- **Never Re-read**: Never re-read a file already loaded in the current session unless it was modified externally or by an edit tool. Trust what is already present in context.

### 3. Browser Automation (Rule: Text > Screenshots)
- **Text Extraction First**: To verify navigation, clicks, or loaded content, always extract DOM text (rendered HTML, page headings, or accessibility tree).
- **Strict Visual Criteria**: Only take screenshots when the task is inherently visual (e.g., layout reviews, CSS styling checks, responsive viewports). Screenshots persist indefinitely in conversational history and are never evicted by prompt caching, inflating every subsequent turn.

### 4. Surgical Log & Error Handling
- **Immediate Truncation**: If a terminal command, build tool, or test runner produces more than 50 lines of output, extract only the first 5 lines, the core error message, and the immediate stack trace.
- **Massive Logs**: Never paste multi-hundred-line outputs into the chat. Pipe them to a local file (e.g., `scratch/error.log`) and inspect using grep.

### 5. Session Management & Handoffs (Highest Cost Lever)
- **Prevent Marathon Sessions**: Continuing a single conversation across dozens of turns forces the agent to re-send the entire cumulative history on every new prompt.
- **Cutoff Triggers**: After reaching a clear milestone (feature completed, bug resolved) or exceeding 15–20 tool calls, proactively suggest `/clear` or `/compact` along with a 1-line resume command (Handoff).
- **Idle Inactivity**: If a session remains inactive for over 1 hour, the LLM prompt cache has expired. Summarize and start a fresh session.

---

## 🧭 Workflow by Task Type

| Task Type | Recommended Economy Practice | Reference |
| :--- | :--- | :--- |
| **Backend & APIs** | Targeted Grep by route/controller signature; run only the specific test for the touched endpoint. | [Tools Guide](references/automation-and-tools.md) |
| **Frontend & UI** | Reuse existing styling tokens; capture screenshots only after finishing an entire component block. | [Tools Guide](references/automation-and-tools.md) |
| **Browser & QA** | Extract text via DOM/Accessibility Tree; prohibit screenshots for step verification. | [Tools Guide](references/automation-and-tools.md) |
| **Architecture & Refactoring** | Record decisions in atomic local notes and terminate sessions before accumulating stale context. | [Session Guide](references/session-management.md) |

---

## 📚 Supporting References

- [Universal Optimization Rules](references/universal-rules.md)
- [Session Management & Handoff Protocol](references/session-management.md)
- [Automation, Browser & Tool Best Practices](references/automation-and-tools.md)
