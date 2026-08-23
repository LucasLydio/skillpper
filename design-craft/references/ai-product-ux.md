# AI product UX

For designing products where a model or agent does work — chat is only one of many surfaces and usually not the right one. Distilled from Pete Koomen, Raphael Schaad, Ryo Lu, Steven Haney, and Karri Saarinen.

## Start from the work, not the model

- Don't ask "how do we slot AI into this app?" Ask "if this tool were designed from scratch to take the repetitive work off the user, what would it be?" Bolting a chatbot onto software designed for humans to do work in is the horseless carriage.
- Solve specific, bottom-up problems (triage this issue, draft this reply in my voice, reorder before I run out) rather than "ask anything". Users don't want generic workflow software; they want a named problem gone.
- Two tests for any AI feature: does the output sound like *me* / fit my context, and is it *less* work than doing it myself? A prompt as long as the output fails the second.

## Nouns → verbs

Interfaces used to be nouns (buttons, fields, sidebars). AI features are verbs (summarize, autocomplete, send an agent, generate). Verbs have duration, uncertainty, and side effects, so:
- Design time explicitly: what the user sees at 0s, 2s, 30s, 10 minutes.
- Design with real data; static mockups break for verbs.
- Design the ladder of abstraction and pick a rung deliberately: autocomplete → adaptive suggestions per item → best-guess draft already waiting → autopilot with review. Move users up the ladder as trust is earned.

## Latency, states, and waiting

- Latency *is* the interface (voice especially). Show it if the audience is technical; make it feel natural if not.
- Show every meaningful state while the agent works: what's running, what tool it's calling, what needs confirmation — in one controllable focus area, not a wall of logs, not a spinner with jokes, never two spinners.
- Trade fidelity for immediacy: low-res preview, blurred frames with real audio, partial results streaming in (flight-search prior art), so the human can steer before the expensive render.
- Long jobs: honest ETA, persistent step log, "we'll notify you". Interruptions handled gracefully; taps and voice input acknowledged instantly with a visual cue.
- Prefer incremental/diff edits over full regeneration; module-level prompting; keep the rest stable when one part changes.

## Prompts and inputs

- A blank prompt box is a blank canvas problem. Offer example prompts as one-click buttons; infer contextual suggestions from what's on screen; offer pill/lego builders for jargon users may not know ("glassmorphic").
- Sometimes prompting is the wrong input: dragging, selecting, deleting, or a knob is faster. Best tool for the job.
- Show what the model respected vs ignored from the prompt so people learn to prompt and the system learns what to improve.
- The system prompt is English: let users see and edit it, or better auto-generate it from their history and refine via feedback, with a break-glass edit. Never a black box that speaks in a corporate voice on the user's behalf.

## Trust and verification

- Show sources inline per claim or per cell (Perplexity-style footnotes) so results can be checked at the point of use.
- Keep the human in the loop where it matters: editable columns, review before send, agents propose PRs and humans merge.
- A demo that gets a detail wrong (mispronounces a compliance standard) costs more than no demo. Constrain first demos to succeed; steer them toward the buyer's actual problem.

## Adaptive UI

- Content in → UI out (suggested replies that change per email). The cost is predictability: keep hotkeys/positions stable even when labels change; be explicit about focus so a hotkey never fires while typing.
- Prefer showing only the relevant actions over a hundred toolbar buttons — but earn it with consistency.

## Agent-era product patterns worth reusing

- Canvas as a document type for branching workflows: color-code node types with a legend; different fidelity per zoom level; templates that show branching, not just linear recipes; inline instruction text.
- Feedback/feature-request boxes as prompt boxes that fire an agent → PR; CTA says what happens ("Send to an agent"); credit contributors.
- Human and machine versions of a surface (a markdown/llms.txt page): distilled, copyable, with explicit safety notes; visuals don't matter, content does.
- Dev-mode vs production-mode: expose internals (latency, tool calls, thinking) for builders; hide them for end users.

## Design-tooling implications for the team

- Code is the source of truth; the design tool is a visual interface onto it. Agents read HTML/CSS natively — a design system in the repo composes well with agents; a second copy drifts.
- Give agents an expert's guardrails (typography, contrast, anti-tells) — that's the "secret sauce", not a special model.
- Explore by volume, curate by hand, polish once. Never ship raw generation because it was easy.
