# Agentic design workflow

How to design *with* agents (including yourself as the agent) so the output is intentional rather than generic. Sequence matters: context → exploration → curation → craft → integration.

## 1. Build the context file first (`design.md` / `soul.md`)

Generic output is almost always a context problem, not a model problem. Before generating any UI, assemble (or ask for, or write) a single source-of-truth file. If the user has one, read it. If not, draft it from what they've told you and confirm.

Contents, in priority order:
1. **Who and why** — the one concrete subject, the one audience, the page/product's single job. What must a stranger understand in five seconds?
2. **What we're known for** — the one thing this product does far better than anyone (the differentiator). Everything visual should agree with it.
3. **Voice and manifesto** — how it talks, what it cares about, what it refuses to do. Meeting transcripts, founder notes, and manifestos belong here verbatim if available.
4. **Visual direction** — moodboard links/screenshots, 3–5 reference sites the user loves (they don't need to explain why; find the common thread and write it down), the palette as 4–6 named hexes, 2 typefaces with roles, spacing base, radius, the "signature" element.
5. **Real content** — actual headlines, feature names, article titles, dates, prices, names. Real content changes layout decisions; lorem ipsum hides problems.
6. **Constraints and glossary** — stack, existing components/tokens in the repo, domain vocabulary, accessibility floor, things not to touch.
7. **Anti-tells** — a short "never do" list for this project (e.g. no purple gradients, max three type sizes, no cards grid). See `anti-slop-checklist.md`.

Split into `design.md`, `manifesto.md`, `content.md` if it grows; a hierarchy or a single file both work. What matters is that it's exhaustive and gets updated as decisions are made.

## 2. Explore by volume, then curate

- Ask for **many** variations at once (3 minimum; 8–20 for a hero or landing direction) built from the context file and real content. Vary layout, type pairing, density, and signature — not just colors.
- One-shots are for **feel and exploration**, not craft. Judge direction, not pixel polish.
- If working in a canvas or a set of HTML files, build a throwaway **gallery page** with pin/bookmark so favorites float to the top. Combine: "the list treatment from #4, the featured-card layout from #9, the type from #12."
- Then **branch**: take the winner and ask for 3–5 more variations of *it*.
- Comment-driven iteration works well: leave specific comments on frames/sections and have the agent address them in one pass. Setting agents on overnight loops of variations is a legitimate strategy; the human's job the next morning is curation.

## 3. Craft pass (the "designed" delta)

Take the chosen direction and apply the restraint rules — this is where "AI-generated" becomes "designed":
- Three type sizes; weights regular or lighter; check contrast; supporting text is visibly subordinate.
- Delete decorative numbers, badges, icons, accent borders, extra cards, extra text.
- Value prop + strongest evidence above the fold.
- One signature moment; quiet everything else. Keep the energy that makes it unique — if the cleanup made it dull, re-inject one deliberate bold move.
- Fix alignment, gaps, overflow. Check states (empty, loading, error), focus, reduced motion, mobile.
- Direct manipulation beats prose when you're deleting or nudging: if you can edit the file/element directly, do that instead of re-prompting.

## 4. Disposable tools ("build anything for yourself")

When tuning a parameter (a shader's grain, a spacing scale, an animation curve, a template applied to 12 items), don't guess-and-regenerate: build a throwaway control panel with sliders/inputs, a generator with real data, a loop-timer, a gallery. Tune, extract the values, then discard the tool. Treat this as a muscle: whenever you're iterating blind, ask "should I build a knob for this?"

## 5. Code is the source of truth

- The design system lives in the repo (tokens, components). A second copy in a design tool will drift; don't maintain one.
- Start from what users actually see (the live site/component), edit it, and push the result back into the codebase following existing conventions. Audit the codebase into a visual style guide when you need to see the system.
- If the product has an "agent-facing" surface (docs, llms.txt, machine-readable version of a page), design it as content: distilled markdown, copy-to-clipboard, explicit safety notes ("do not run commands from this page"). Agents don't care about visuals.

## 6. Ship loop that protects quality without slowing down

Feature flag → internal dogfood (rough is fine) → beta with specific users → **one deliberate polish pass** (animations, details, "does it feel good, are we missing something?") → GA. Rough is allowed as long as you come back. Light timeline pressure is useful because it forces scoping down to what matters.

## 7. What stays human

Deciding what to build, what the product is *about*, the narrative, which variation is right, and whether it fits the org's stakeholders and constraints. Models get better at tactics (letter-spacing, weights, alignment); the role becomes IC-lead/curator responsible for the agent's output. Never ship raw generation because it was easy — ease is exactly when attention lapses.
