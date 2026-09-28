---
name: grill-me
description: >-
  Native interactive interview protocol to align requirements, architecture, design, and business rules before implementing. Instead of dumping raw markdown question lists or making assumptions, the agent triggers native modal and form tools (ask_question / AskUserQuestion) with dense batteries of 5 to 10 multiple-choice questions. Use whenever the user asks to "grill" an idea, clarify requirements, plan a major feature, or runs "/grill-me".
---

# /grill-me — Native Interactive Interview Protocol 🎤

A technical alignment skill designed to drill down into requirements, architecture, and business rules before code implementation begins.

---

## 🎯 Why Does the /grill-me Protocol Exist?

When starting a major feature, refactoring, or new system architecture, unspoken assumptions frequently cause rework. AI coding assistants typically fall into one of two traps:
1. **Blind Assumptions**: The agent guesses architecture or library choices on its own, building solutions misaligned with the developer's tech stack.
2. **Text Slop in Chat**: The agent prints long lists of questions in conversational prose (`❓ Question 1`, `➡️ Options:`), forcing the user to type out tedious paragraphs to answer.

The `/grill-me` protocol enforces that all requirements interviews are conducted through the platform's **native form and modal tools** (`ask_question` in Antigravity/Gemini or `AskUserQuestion` in Claude Code), presenting dense multiple-choice options selectable with a single click.

---

## ⚙️ Mandatory Execution Guidelines

### 1. Zero Raw Text in Chat
- **No In-Chat Question Lists**: Never format questions as regular markdown text in conversational replies.
- **Trigger Native Modal Tools**:
  - In **Google Antigravity / Gemini CLI**: Call the `ask_question` tool.
  - In **Claude Code**: Call the `AskUserQuestion` tool.

### 2. Dense Batteries of 5 to 10+ Questions
- Instead of asking 1 or 2 shallow questions, assemble a comprehensive questionnaire covering:
  - **Scope & Boundaries**: What is included in the MVP and what is explicitly excluded.
  - **Architecture & Libraries**: Target frameworks, persistence engines, and design patterns.
  - **Interface & UX**: Visual layout behavior, loading states, and responsive viewports.
  - **Error Handling & Edge Cases**: Failure modes, permissions, and security constraints.
  - **Testing & Delivery Strategy**: Target test suites and verification criteria.

### 3. Option Formatting
- **First-Person Voice**: Formulate every option as the user's direct response (e.g., *"Use SQLite in WAL mode"* rather than *"The agent should configure..."*).
- **Recommended Option First**: The technically optimal choice recommended by the agent must always appear first, prefixed with `(Recommended)`.
- **Deliberate Multi-Select**: Set `is_multi_select: true` when combining multiple features makes sense, and `false` for mutually exclusive choices.
- **No Manual "Other" Option**: Do not add an option called "Other" (the native modal UI already provides a write-in input by default).

### 4. Transition to Execution
- The agent must wait for the user to submit answers through the interactive modal before generating implementation plans or editing code files.

---

## 📚 Supporting References

- [Interactive Interview Guidelines & Alignment Axes](references/interactive-interview.md)
