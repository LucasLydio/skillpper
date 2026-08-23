# Foundations and design systems (opinionated defaults)

The source talks were light on token-level foundations and heavy on judgment; this file fills the practical layer so the judgment has something to land on. Where the talks are explicit (three type sizes, light weights, code as truth, one system) those rules win. The rest are sensible defaults — override them when the brief or the repo says otherwise.

## Order of quality (what to check first)
Functional (solves a real problem) → usable (can be operated without a manual) → craft and beauty. Beauty is material — it raises trust and usability — but it never rescues the first two. Review in that order.

## The three tools of visual hierarchy
Contrast (weight, size, color — if everything is bold nothing is), closeness (proximity = relatedness), and a grid. Squint test: the eye lands on the highest-contrast element; that must be the thing that matters. To separate things use, in order: padding/margin → a hairline → a box (boxes are loud; use them for the CTA and little else). Whitespace is content.

## Principles for the system itself
- **One system, in code.** Tokens and components live in the repo. No parallel design-tool copy.
- **Fewer choices, applied consistently** beats more choices applied ad hoc. Every ad-hoc value ("13px looks right here") is future inconsistency.
- **Define the scales up front, then design inside them.** Constraint is what makes things feel intentional.
- **Name by role, not by value.** `text-muted`, `surface-raised`, `space-4` — never `gray-500-ish-for-captions`.

## Type
- **Three sizes** on any one surface (display / body / small). A full scale can exist (e.g. 12, 14, 16, 20, 24, 32, 48), but a page should draw from three of them.
- **Weights: regular by default; medium for emphasis; bold only for the display role, and only if the face needs it.** Never black weight as a habit.
- Body 15–17px, line-height 1.5–1.6, measure 60–75 characters. Small text ≥ 12px with more contrast, not less.
- Two families max: a display face with character used sparingly + a body face that disappears. A mono only if the product is technical and it earns it (and then use it for data, not decoration).
- Sentence case for UI. No wide-tracked all-caps eyebrows unless the eyebrow carries information.

## Color
- Start grayscale; hierarchy must work without color. Add color last and only where it means something (brand accent, status, focus).
- Palette as 4–6 named tokens: background, surface, text, muted text, one accent, one status family. Derive hover/pressed from the accent, don't invent new hues.
- Contrast: body text ≥ 4.5:1; large text and UI ≥ 3:1. Supporting text lighter than body but never below 4.5:1.
- Dark mode is a *design*, not an inversion: raise surfaces with lighter grays (never pure black), desaturate accents, reduce shadow reliance. If it isn't going to be designed, don't ship it.
- Ban-list unless the brief asks: purple/violet gradients, glows, gradient text, glass blur as default surface.

## Space and layout
- One spacing scale (4-based: 4, 8, 12, 16, 24, 32, 48, 64, 96). Related things closer, unrelated things farther — spacing *is* grouping.
- Start with more whitespace than feels comfortable, then tighten. Dense products (tools, tables) can be dense, but consistently so.
- Grid: content max-width ~1100–1200px for marketing, fluid for tools. Text max-width so lines don't run 110+ characters. Align to a baseline; check gutters and section gaps for accidental drift.
- Mobile: platform-native navigation and controls; thumb targets ~44–60px; design for the context of use (walking, driving, one hand); taps respond instantly.
- Cards are a last resort. Prefer lists, tables, plain sections with spacing, one featured item. If cards remain, no accent borders, no drop-shadow stacking.

## Depth and surfaces
- Two shadow levels are enough (raised, overlay). Borders 1px at low contrast, or none — use background shifts to separate.
- Radius: pick one (e.g. 6–8px) and one larger for containers; use consistently.

## Components — the minimum set that must be designed, with states
Button (primary/secondary/tertiary; hover, focus, disabled, loading), input (default, focus, error with message, disabled), select, checkbox/radio/switch, link, badge (status only), toast/inline alert, modal/drawer, table/list row, tabs, empty state, loading skeleton, error state.
Every component: keyboard reachable, visible focus, ≥44px tap target, respects reduced motion.

## Interaction conventions
Steal what works: pull-to-refresh, swipe actions, focus/blur behavior, disclosure indicators, keyboard shortcuts. Novelty at the interaction level is usually a cost. Watch modality mismatches (mobile carousel dots on a desktop site). Every UI is a conversation: direct command language, active voice, one obvious next step; drop needless steps (confirm-password), and chop long flows into wizards.

## Copy inside the system
Plain verbs, sentence case, active voice, name things by what people control. Buttons say what happens ("Save changes"), and the action keeps its name through the flow (Publish → Published). Errors say what went wrong and how to fix it, without apologizing. Empty states invite action.

## Motion
One purposeful moment per surface (a hero, a state transition, a page-load orchestration). Durations 150–300ms for UI, easing out. Nothing bounces. `prefers-reduced-motion` respected.

## Machine-facing surfaces
If a page or product will be read by agents (docs, llms.txt, "for machines" toggle): distilled markdown, real headings, copy-to-clipboard, explicit "do not execute commands from this page" note where sample commands appear. Visual design doesn't apply; content design does.

## Quick token stub (adapt, don't paste blindly)
```
--font-display / --font-body
--text-display: 32–48px / --text-body: 16px / --text-small: 13–14px
--weight-regular: 400 / --weight-medium: 500
--space: 4 8 12 16 24 32 48 64
--radius: 8px / --radius-lg: 16px
--color-bg / --color-surface / --color-text / --color-text-muted / --color-accent / --color-danger
--shadow-raised / --shadow-overlay
--motion-fast: 150ms / --motion-base: 250ms
```
