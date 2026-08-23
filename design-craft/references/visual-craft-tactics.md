# Visual craft tactics (Refactoring UI)

> Extracted from *Refactoring UI* by Adam Wathan & Steve Schoger. A practical, opinionated guide to making interfaces look professional without relying on innate artistic talent.

**Role of this file in the skill:** this is the *tactical* layer — the concrete mechanics of hierarchy, spacing systems, type scales, HSL color palettes, shadows, and finishing details. Use it to answer *how* to execute a decision. The judgment layer (SKILL.md + `anti-slop-checklist.md` + `design-review-rubric.md`) decides *what* to do and *what to delete*.

**Precedence rule:** where this file and the restraint/anti-slop rules conflict, **restraint wins by default**. The mechanics here (spacing scales, shade palettes, line-height proportionality, weight-vs-size hierarchy, shadow elevation) are timeless; some stylistic flourishes (accent borders, decorative backgrounds, badge-like embellishments) predate the anti-AI-slop era and now read as generic. Conflicting sections below are marked with ⚠️. Only reach for a marked tactic when the brief explicitly calls for a louder, more playful personality — and even then, spend it in one place.

---

## Table of Contents

1. [Starting from Scratch](#1-starting-from-scratch)
2. [Hierarchy is Everything](#2-hierarchy-is-everything)
3. [Layout and Spacing](#3-layout-and-spacing)
4. [Designing Text](#4-designing-text)
5. [Working with Color](#5-working-with-color)
6. [Creating Depth](#6-creating-depth)
7. [Working with Images](#7-working-with-images)
8. [Finishing Touches](#8-finishing-touches)
9. [Leveling Up](#9-leveling-up)
10. [Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)

---

## 1. Starting from Scratch

### 1.1 Start with a Feature, Not a Layout

- **Do not start by designing the shell** (navigation bar, sidebar, logo placement). An "app" is a collection of features — you don't have the information to design the navigation until you've designed several features first.
- **Start with a piece of actual functionality.** If building a flight booking service, start with the search form (departure city, destination city, dates, search button). The shell comes later.
- Google's homepage is proof you might not even need a shell — just the core feature.

### 1.2 Detail Comes Later

- In the earliest stages, **don't get hung up on typefaces, shadows, or icons.** That stuff matters eventually, not right now.
- **Design with a thick Sharpie on paper** to make it physically impossible to obsess over details. This forces you to explore layout ideas quickly.
- **Hold the color.** Design in grayscale first. This forces you to use spacing, contrast, and size to create hierarchy. Color is then an enhancement, not a crutch.
- **Don't over-invest in wireframes.** Sketches and wireframes are disposable. Use them to explore ideas, then leave them behind when you've decided.

### 1.3 Don't Design Too Much

- **Don't design every feature before moving to implementation.** Figuring out every edge case in the abstract is extremely hard (2000 contacts? overlapping calendar events? error messages?).
- **Work in short cycles:**
  1. Design a simple version of the next feature.
  2. Make it real (build it).
  3. Iterate on the working design until problems are solved.
  4. Jump back to design mode for the next feature.
- **Be a pessimist.** Don't imply functionality you aren't ready to build. If attachments in comments will take too long, ship comments without attachments first.
- **Design the smallest useful version you can ship.** If part of a feature is a "nice-to-have," design it later.

### 1.4 Choose a Personality

Every design communicates a personality through concrete factors:

| Factor | Elegant/Formal | Playful/Fun | Neutral/Plain |
|--------|---------------|-------------|---------------|
| **Font** | Serif typeface | Rounded sans-serif | Neutral sans-serif |
| **Color** | Gold (sophisticated) | Pink (fun) | Blue (safe, familiar) |
| **Border radius** | None (serious) | Large (playful) | Small (neutral) |
| **Language** | "Your account has been created" | "You're in! Welcome aboard!" | Somewhere in between |

- **Stay consistent.** Mixing square corners with rounded corners in the same interface almost always looks worse than committing to one or the other.
- **Look at sites used by your target audience** to calibrate the right personality. Don't borrow too much from direct competitors.

### 1.5 Limit Your Choices

- **Designing without constraints is torture.** Having millions of colors and thousands of fonts leads to paralysis — there's always more than one "right" choice.
- **Define systems in advance:**
  - Don't reach for the color picker every time — choose from a predefined set of 8-10 shades.
  - Don't tweak font sizes 1px at a time — define a restrictive type scale.
- **Design by process of elimination.** With a constrained set (e.g., icon sizes: 12px, 16px, 24px, 32px), guess the middle value, compare with neighbors, and eliminate obviously bad choices.
- **Systematize everything:** font size, font weight, line height, color, margin, padding, width, height, box shadows, border radius, border width, opacity.
- Introduce new systems as you encounter new decisions. Avoid making the same minor decision twice.

---

## 2. Hierarchy is Everything

### 2.1 Not All Elements Are Equal

- **Visual hierarchy** is the most effective tool for making something feel "designed." It's about how important elements appear in relation to one another.
- When everything competes for attention, the interface feels noisy and chaotic.
- **De-emphasize secondary and tertiary information** and highlight the most important elements. This immediately improves the design even without changing colors, fonts, or layout.

### 2.2 Size Isn't Everything

- **Don't rely solely on font size for hierarchy.** This leads to primary content that's too large and secondary content that's too small.
- **Use font weight and color instead:**
  - Make primary elements **bolder** (600-700 weight) at a reasonable font size.
  - Use a **softer color** for supporting text instead of making it tiny.
- **Three-color system for text:**
  - **Dark color** for primary content (article headlines)
  - **Grey** for secondary content (publish dates)
  - **Lighter grey** for tertiary content (copyright notices)
- **Two font weights for UI:**
  - **Normal** (400 or 500) for most text
  - **Heavy** (600 or 700) for emphasized text
- **Never use font weights below 400 for UI work.** They work for large headings but are too hard to read at small sizes. To de-emphasize text, use a lighter color or smaller size instead.

### 2.3 Don't Use Grey Text on Colored Backgrounds

- Grey on white works because it **reduces contrast**. On colored backgrounds, grey text looks bad.
- **Don't just reduce opacity** of white text — it looks dull, washed out, and sometimes disabled. On images/patterns, the background shows through.
- **Hand-pick a new color** based on the background: same hue, adjusted saturation and lightness until it looks right.

### 2.4 Emphasize by De-emphasizing

- When the main element won't stand out despite styling, **de-emphasize the competing elements** instead of further emphasizing the target.
- Example: If an active nav item doesn't pop, give the inactive items a softer color so they recede.
- For sidebars competing with main content: **remove the sidebar's background color** — let the content sit on the page background directly.

### 2.5 Labels Are a Last Resort

- Displaying data as "label: value" gives every piece of data equal emphasis, destroying hierarchy.
- **You might not need a label at all:**
  - Format is enough: `janedoe@example.com` (email), `(555) 765-4321` (phone), `$19.99` (price).
  - Context is enough: "Customer Support" under a person's name in an employee directory.
- **Combine labels and values:** Instead of "In stock: 12", write "12 left in stock." Instead of "Bedrooms: 3", write "3 bedrooms."
- **When you need labels, treat them as secondary.** De-emphasize: make them smaller, lower contrast, lighter font weight, or all three. The data itself is the focus.
- **When to emphasize labels:** On information-dense pages (e.g., product specs) where users scan for labels like "depth" rather than values like "7.6mm."

### 2.6 Separate Visual Hierarchy from Document Hierarchy

- Don't let semantic HTML elements (h1, h2, h3) dictate visual styling.
- **Section titles often act like labels,** not headings — they should be small and supportive, not attention-grabbing.
- Pick elements for semantic purposes and **style them however you need** to create the best visual hierarchy.

### 2.7 Balance Weight and Contrast

- Bold text feels emphasized because it covers **more surface area** (more pixels for text vs. background).
- **Icons feel heavy** (especially solid ones) next to text. You can't change icon weight, so **lower their contrast** by giving them a softer color.
- **Reducing contrast counterbalances heavy elements.** Increasing weight emphasizes low-contrast elements.
- Example: If a thin 1px border is too subtle in a soft color but darkening it feels harsh, **increase the border width** instead.

### 2.8 Semantics Are Secondary (Button Hierarchy)

- Don't design actions based purely on semantics. Every action sits in a **pyramid of importance:**
  - **Primary actions:** Obvious. Solid, high-contrast background colors.
  - **Secondary actions:** Clear but not prominent. Outline styles or lower-contrast backgrounds.
  - **Tertiary actions:** Discoverable but unobtrusive. Styled like links.
- **Destructive actions are not automatically primary.** A "Delete" button might deserve secondary/tertiary treatment on the main page, with big-red-bold styling only in the confirmation modal where it IS the primary action.

---

## 3. Layout and Spacing

### 3.1 Start with Too Much White Space

- **White space should be removed, not added.** The default approach of adding minimum padding results in designs that only avoid looking bad, not designs that look great.
- **Start by giving way too much space, then remove it** until you're happy. What feels like "a little too much" in isolation usually becomes "just enough" in a complete UI.
- **Dense UIs have their place** (dashboards with lots of data), but this should be a deliberate decision, not the default.

### 3.2 Establish a Spacing and Sizing System

- **A linear scale won't work.** "Make everything a multiple of 4px" doesn't help you choose between 120px and 125px. At small sizes, a couple of pixels is a 33% difference (12px to 16px). At large sizes, it's imperceivable (500px to 520px = 4%).
- **No two values in your scale should be closer than about 25% apart.**
- **Use a base value of 16px** (divides nicely, matches default browser font size), then build a scale using factors and multiples:
  - Tightly packed at the small end, progressively more spread apart at the large end.
  - Example practical scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 640, 768

### 3.3 You Don't Have to Fill the Whole Screen

- **If you only need 600px, use 600px.** Spreading things out makes interfaces harder to interpret. Extra space around the edges never hurt.
- Individual sections don't need to be full-width just because the nav is full-width.
- **Shrink the canvas:** If designing a small interface on a large canvas is hard, start with ~400px (mobile-first). Adjust for larger screens afterward — you'll change less than you think.
- **Think in columns:** If a narrow element (like a form) feels unbalanced in a wide UI, split it into columns (e.g., form + supporting text in a separate column).

### 3.4 Grids Are Overrated

- **Not all elements should be fluid.** A sidebar shouldn't scale proportionally with the screen — it should have a fixed width optimized for its contents, with the main area flexing to fill remaining space.
- **Don't shrink elements until you need to.** Instead of giving a login card a percentage width, give it a max-width (e.g., 500px). Only let it shrink when the screen is smaller than that.
- **Don't be a slave to the 12-column grid.** Give components the space they need without compromise until actually necessary.

### 3.5 Relative Sizing Doesn't Scale

- **Elements should scale independently across screen sizes.** If body copy is 18px and headlines are 45px (2.5x) on desktop, that ratio won't work on mobile — 2.5x of 14px is 35px, way too big.
- A better mobile headline might be 20-24px (1.5-1.7x body) — a completely different relationship.
- **Rule: Large elements shrink faster than small elements.** The difference between small and large should be less extreme at small screen sizes.
- **Component properties should scale independently too.** A large button shouldn't just be a zoomed-in small button — padding should be more generous at large sizes and disproportionately tighter at small sizes. Fine-tune things independently for each context.

### 3.6 Avoid Ambiguous Spacing

- When elements lack visible separators (borders, backgrounds), spacing determines which elements belong together.
- **If the margin below a label equals the margin below an input, the form group won't feel connected.** Fix: Increase space between form groups.
- **The rule: More space around a group than within it.** Always ensure the inter-group spacing exceeds intra-group spacing.
- This applies to: form groups, section headings in articles, bulleted lists, horizontal components.

---

## 4. Designing Text

### 4.1 Establish a Type Scale

- Most UIs use way too many font sizes. Every pixel from 10px to 24px used somewhere = inconsistency + slow workflow.
- **Modular scales** (e.g., 4:5 ratio, golden ratio) sound appealing but produce fractional values and often too-limiting jumps for UI work.
- **Hand-crafted scales are more practical for UI design.** Example:
  - 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
- Constrained enough to speed decision-making, not so limited you feel stuck.
- **Avoid em units for type scales.** Nested elements compute unexpected sizes (e.g., 1.25em inside 0.875em = 17.5px, not in your scale). Use **px or rem** only.
- **Reconciliation with restraint rules:** the full scale is the *system-wide vocabulary*; any single surface/page should still draw only **three** of those sizes (display / body / small), per `foundations-and-systems.md`. The scale exists so those three are always consistent picks, not so every page uses seven sizes.

### 4.2 Use Good Fonts

- **Play it safe:** Use a neutral sans-serif (Helvetica, system font stack: `-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue`).
- **Filter by weight count:** Ignore typefaces with fewer than 5 weights. On Google Fonts, filter by 10+ styles (including italics) — this eliminates 85% of options, leaving <50 quality sans-serifs.
- **Optimize for legibility:** Avoid condensed typefaces with short x-heights for main UI text. Fonts for small sizes have wider letter-spacing and taller lowercase letters.
- **Trust popularity:** Sort font directories by popularity to surface well-crafted options.
- **Steal from great sites:** Inspect favorite sites to discover their typefaces.

### 4.3 Keep Line Length in Check

- **Optimal line length: 45-75 characters per line.** Use 20-35em width to achieve this.
- Going wider than 75 characters is risky territory.
- **If mixing paragraph text with large components,** still limit paragraph width even if the overall content area is wider. Different widths in the same content area almost always look more polished.

### 4.4 Baseline, Not Center

- When mixing font sizes on a single line, **align by baseline**, not vertical center.
- Center-aligned mixed sizes create awkward offset baselines.
- Baseline alignment leverages an alignment reference your eyes already perceive, producing a simpler, cleaner look.

### 4.5 Line-Height is Proportional

- A line-height of ~1.5 is a starting point, not a universal rule. **Adjust based on context:**
- **Line-height and paragraph width are proportional:** Narrow content → 1.5 line-height. Wide content → up to 2.0 line-height. (Longer eye travel = more need for spacing to find the next line.)
- **Line-height and font size are inversely proportional:** Small text → taller line-height (1.5+). Large headlines → shorter line-height (1.0 is fine). Large text doesn't need extra help finding the next line.

### 4.6 Not Every Link Needs a Color

- In blocks of non-link text, links should visually pop. But in a **link-heavy interface** (nav, lists), brightly colored links are overbearing.
- **Emphasize most links subtly:** Heavier font weight or darker color.
- **Ancillary links** (not on the main path) can have no special styling by default — add underline or color change only on hover.

### 4.7 Align with Readability in Mind

- **Default to left-alignment** (for LTR languages).
- **Center-alignment** works for headlines and short independent blocks (2-3 lines max). If one centered block is too long, rewrite it shorter.
- **Right-align numbers** in tables so decimals line up for easy comparison.
- **Hyphenate justified text** to avoid awkward word gaps. Justified text works best for print-mimicking contexts (online magazines).

### 4.8 Use Letter-Spacing Effectively

- Generally trust the typeface designer's built-in letter-spacing.
- **Tighten headlines:** Fonts with wider letter-spacing (like Open Sans) can benefit from decreased letter-spacing when used as headlines, mimicking the condensed look of purpose-built headline fonts. Don't do the reverse — headline fonts don't work well at small sizes even with increased spacing.
- **Increase letter-spacing for ALL-CAPS text.** Uppercase letters are all the same height, lacking the visual diversity of lowercase (ascenders, descenders), making default spacing harder to read.

---

## 5. Working with Color

### 5.1 Ditch Hex for HSL

- Hex and RGB make visually similar colors look nothing alike in code.
- **HSL (Hue, Saturation, Lightness)** represents colors by attributes the human eye intuitively perceives:
  - **Hue:** Position on the color wheel (0°=red, 120°=green, 240°=blue).
  - **Saturation:** 0% = grey, 100% = vibrant.
  - **Lightness:** 0% = black, 50% = pure color, 100% = white.
- **HSL vs HSB:** They're different. HSB 100% brightness at 100% saturation ≠ white. Browsers only understand HSL. Use HSL for web.

### 5.2 You Need More Colors Than You Think

- **Five hex codes are useless for building real interfaces.** You need a comprehensive palette.
- **Three categories of colors:**
  1. **Greys (8-10 shades):** Text, backgrounds, panels, form controls. Start from a very dark grey (not true black — it looks unnatural) up to white.
  2. **Primary colors (5-10 shades each):** For primary actions, active navigation. Ultra-light shades for tinted backgrounds (alerts), darker shades for text.
  3. **Accent colors (5-10 shades each):** Semantic states (red=destructive, yellow=warning, green=positive), feature highlights (teal, pink), categories (graph lines, calendar events, tags).
- **Total: ~10 colors with 5-10 shades each** for a complex UI.

### 5.3 Define Your Shades Up Front

- **Never use CSS preprocessor functions** (lighten/darken) to create shades on the fly. You'll end up with 35 slightly different blues.
- **Process for building a shade palette:**
  1. **Choose the base color (shade 500):** Pick a shade that works as a button background.
  2. **Find the edges:** Pick the darkest shade (900, for text) and lightest shade (100, for tinted backgrounds). Use an alert component as a test case.
  3. **Fill in the gaps:** Pick 700 and 300 (midpoints), then 800, 600, 400, 200. Nine shades total (100-900).
- **For greys:** Pick darkest (for darkest text) and lightest (for subtle off-white background), then fill in gaps.
- **Trust your eyes, not the numbers.** Tweak saturation/lightness after testing in real designs. But avoid adding new shades frequently.

### 5.4 Don't Let Lightness Kill Your Saturation

- At extreme lightness values (near 0% or 100%), saturation's impact weakens. Light/dark shades can look washed out.
- **Increase saturation as lightness moves away from 50%** to maintain color intensity.
- **Perceived brightness varies by hue:** Yellow appears much lighter than blue at the same HSL lightness. Three brightness peaks (yellow ~60°, cyan ~180°, magenta ~300°) and three troughs (red ~0°, green ~120°, blue ~240°).
- **Rotate hue to adjust perceived brightness without losing intensity:**
  - To lighten: rotate toward nearest bright hue (60°, 180°, or 300°).
  - To darken: rotate toward nearest dark hue (0°, 120°, or 240°).
  - Example: Yellow's darker shades become warmer/richer by rotating toward orange.
  - **Limit hue rotation to 20-30°** or it looks like a different color entirely.

### 5.5 Greys Don't Have to Be Grey

- True grey (0% saturation) feels lifeless. In practice, "greys" are often saturated.
- **Color temperature in greys:**
  - **Cool greys:** Saturate with blue.
  - **Warm greys:** Saturate with yellow or orange.
- **Increase saturation for lighter and darker grey shades** to maintain consistent temperature (otherwise those shades look washed out near the extremes).

### 5.6 Accessible Doesn't Have to Mean Ugly

- **WCAG recommends:** 4.5:1 contrast ratio for normal text (<~18px), 3:1 for larger text.
- **Flip the contrast:** Instead of light text on dark colored backgrounds (requires very dark colors, creating unwanted visual weight), use **dark colored text on a light colored background.** The color supports the text without dominating.
- **Rotate hue for accessible colored text on colored backgrounds:** When adjusting only lightness gets you too close to white, rotate hue toward a brighter hue (cyan, magenta, yellow) to increase contrast while maintaining color.

### 5.7 Don't Rely on Color Alone

- Color-blind users can't distinguish red from green. **Always pair color with another indicator:**
  - Add icons (up/down arrows for positive/negative changes).
  - Use contrast differences instead of purely different hues (light vs. dark is easier for color-blind users than two distinct colors).
- **Color should support what the design already communicates — never be the only signal.**

---

## 6. Creating Depth

### 6.1 Emulate a Light Source

- **Light comes from above.** This is the fundamental rule for creating raised/inset effects.
- **Raised elements:**
  - Top edge = slightly lighter (inset box shadow or top border, facing the light).
  - Small dark box shadow below (element blocks light from reaching area beneath).
  - Don't use semi-transparent white for the top highlight — it sucks saturation. Hand-pick a lighter color.
  - Keep blur radius small (couple pixels) — these shadows should have sharp edges.
- **Inset elements (wells, inputs, checkboxes):**
  - Bottom lip = slightly lighter (facing upward toward light).
  - Small dark inset box shadow at the top (area above blocks light from reaching top of element).
- **Don't get carried away.** Borrow visual cues from reality to add depth, but don't aim for photo-realistic.

### 6.2 Use Shadows to Convey Elevation

- Shadows position elements on a virtual z-axis, creating a sense of depth:
  - **Small shadows (tight blur):** Buttons — noticed but don't dominate.
  - **Medium shadows:** Dropdowns — sit above surrounding UI.
  - **Large shadows (high blur):** Modals — capture full attention.
- **Define a fixed elevation system.** Five shadow levels is usually enough:
  1. Smallest (subtle elements).
  2. Small (buttons).
  3. Medium (dropdowns, cards).
  4. Large (sticky headers, floating elements).
  5. Largest (modals, dialogs).
- **Combine shadows with interaction:**
  - Add a shadow on click/drag to make elements feel like they pop forward.
  - Switch to a smaller shadow on button press to simulate pressing into the page.
- **Don't think about the shadow itself — think about where the element sits on the z-axis** and assign accordingly.

### 6.3 Shadows Can Have Two Parts

- Many well-crafted shadows use **two layered shadows:**
  1. **Larger, softer shadow:** Large vertical offset, big blur radius. Simulates the shadow from a direct light source.
  2. **Tighter, darker shadow:** Smaller offset, smaller blur radius. Simulates the area underneath where even ambient light can't reach.
- This gives more control — the large shadow stays subtle while the close shadow stays defined.
- **At higher elevations, the tight ambient shadow should become more subtle** (almost invisible at the highest elevation), because objects further from a surface lose their ambient shadow.

### 6.4 Even Flat Designs Can Have Depth

- **Depth with color:** Lighter elements feel closer (raised); darker elements feel further away (inset). Use shades of the same color relative to the background.
- **Solid shadows** (short vertical offset, no blur radius) give a flat-aesthetic-compatible sense of depth to cards and buttons.

### 6.5 Overlap Elements to Create Layers

- **Offset elements across boundaries** (e.g., a card crossing the transition between two different backgrounds) to create a layered feel.
- Make elements taller than their parent to overlap on both sides.
- Works for small components too (carousel controls overlapping the content).
- **For overlapping images:** Add an "invisible border" (matching the background color) to prevent ugly clashing between images.

---

## 7. Working with Images

### 7.1 Use Good Photos

- **Bad photos ruin a design** even if everything else is perfect.
- Options: Hire a professional photographer or use high-quality stock photography (Unsplash, etc.).
- **Never design with placeholder images** expecting to swap in smartphone photos later.

### 7.2 Text Needs Consistent Contrast

- When placing text on background images, the image's dynamic range (light and dark areas) causes inconsistent readability.
- **Solutions:**
  1. **Semi-transparent overlay:** Black overlay helps light text; white overlay helps dark text.
  2. **Lower image contrast:** Reduce the dynamic range, then adjust brightness to compensate.
  3. **Colorize the image:** Lower contrast → desaturate → add a solid fill with "multiply" blend mode. Also helps match brand colors.
  4. **Text shadow (as a glow):** Large blur radius, no offset — increases contrast only where needed. Combine with slight overall contrast reduction.

### 7.3 Everything Has an Intended Size

- **Don't scale up small icons.** Icons drawn at 16-24px look chunky at 3-4x. Instead, **enclose small icons in a shape with a background color** to fill the space while keeping the icon at its intended size.
- **Don't scale down screenshots.** A full screenshot shrunk 70% makes 16px text into 4px. Instead:
  - Take the screenshot at a smaller screen size (tablet layout).
  - Use a partial screenshot.
  - Draw a simplified version of the UI (details removed, small text replaced with lines).
- **Don't scale down icons either.** A 128px logo shrunk to 16px favicon = mush. Redraw a simplified version at the target size.

### 7.4 Beware User-Uploaded Content

- **Control shape and size:** Center images in fixed containers, crop anything that doesn't fit. Use `background-size: cover` in CSS.
- **Prevent background bleed:** When a user image's background matches your UI background, the image loses its shape. Use a **subtle inner box shadow** (not a border — borders clash with image colors). A semi-transparent inner border also works.

---

## 8. Finishing Touches

### 8.1 Supercharge the Defaults

- Don't always add new elements — enhance what's already there:
  - **Bulleted lists:** Replace bullets with icons (checkmarks, arrows, or content-specific icons like padlocks for security features).
  - **Testimonials:** Make quote marks larger and colored as visual elements.
  - **Links:** Custom underlines (thick, colorful, partially overlapping text), or just a changed color + font weight.
  - **Form controls:** Custom checkboxes and radio buttons using brand colors for selected states.

### 8.2 ⚠️ Add Color with Accent Borders — superseded by anti-slop rules

> **Default: don't.** Colored accent borders on cards and headings are now a primary "AI-generated" tell (see `anti-slop-checklist.md`). The two legitimate survivors are *functional* uses: the side of an **active navigation item** and the side of an **alert/status message**, where the border carries state, not decoration. Skip the rest of this section unless the brief demands it.

- A simple colored rectangle/border adds visual flair without graphic design skills:
  - Top of a card
  - Side of active navigation items
  - Along the side of alert messages
  - Short accent underneath a headline
  - Across the top of the entire layout

### 8.3 ⚠️ Decorate Your Backgrounds — apply with restraint

> Background color *changes* to distinguish sections remain valid. But gradients, blurred blobs, and repeating patterns are on the anti-slop list — glows and purple-ish gradients especially. If you decorate a background, it counts as the design's *one* bold move.

- **Change the background color** to emphasize panels or distinguish page sections. Slight gradients add energy (keep hues within ~30° of each other).
- **Subtle repeating patterns** (e.g., from Hero Patterns). Keep contrast between pattern and background low for readability. Can repeat along a single edge instead of the entire background.
- **Individual graphics:** Simple geometric shapes, small chunks of a pattern, or a simplified illustration (like a world map). Keep contrast low.

### 8.4 Don't Overlook Empty States

- **Empty states should be a priority, not an afterthought.** The first experience a user has with a new feature is likely an empty screen.
- Include an image or illustration to grab attention. Emphasize the call-to-action to encourage the next step.
- **Hide supporting UI** (tabs, filters) that does nothing until the user creates content.
- Use empty states as an opportunity to be interesting and exciting.

### 8.5 Use Fewer Borders

- Borders aren't the only way to create separation. Too many borders = busy and cluttered.
- **Alternatives:**
  1. **Box shadows:** Outline elements more subtly (works best when element color differs from background).
  2. **Different background colors:** Adjacent elements with slightly different backgrounds create natural distinction. If you have both a border AND different backgrounds, try removing the border.
  3. **Extra spacing:** Simply increase the gap between elements — no new UI needed.

### 8.6 Think Outside the Box

- Don't be constrained by preconceived notions of how components "should" look:
  - **Dropdowns:** Don't just list links. Break into sections, use multiple columns, add supporting text, colorful icons.
  - **Tables:** Combine related columns for hierarchy. Add images, color to enrich data. (Only keep separate columns when sorting is needed.)
  - **Radio buttons:** Instead of boring circles + labels, use selectable cards with descriptions and visual styling.
- **Constraints are powerful, but freedom leads to the next level.**

---

## 9. Leveling Up

### 9.1 Look for Decisions You Wouldn't Have Made

- When you see a design you like, ask: "Did the designer do anything I never would have thought to do?"
  - Inverted background color on a datepicker
  - Button positioned inside a text input
  - Two different font colors in one headline
- **Collecting unintuitive decisions** builds your repertoire of design ideas.

### 9.2 Rebuild Your Favorite Interfaces

- **Recreate designs from scratch without peeking at dev tools.** When your version looks different, you'll discover tricks organically:
  - "Reduce line height for headings"
  - "Add letter-spacing to uppercase text"
  - "Combine multiple shadows"
- Studying inspiring work with a careful eye teaches design tricks for years.

---

## 10. Quick Reference Cheat Sheet

### Design Systems to Define Up Front

| System | Recommendation |
|--------|---------------|
| **Spacing/sizing scale** | Base 16px, non-linear (e.g., 4, 8, 12, 16, 24, 32, 48, 64, 96, 128...) |
| **Type scale** | Hand-crafted: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72 |
| **Font weights** | Two: normal (400-500) and bold (600-700) |
| **Text colors** | Three: dark (primary), grey (secondary), light grey (tertiary) |
| **Color palette** | 8-10 shades per color (greys, primary, accents) |
| **Shadow/elevation** | 5 levels, smallest to largest |
| **Border radius** | Consistent choice across the UI |

### Key Numbers

| Property | Value |
|----------|-------|
| Line length | 45-75 characters (20-35em) |
| Line-height (body) | 1.5 (narrow) to 2.0 (wide content) |
| Line-height (headings) | 1.0 to 1.25 |
| Color shades per hue | 5-10 (9 is ideal) |
| Shadow levels | 5 |
| Grey shades | 8-10 |
| WCAG contrast (normal text) | 4.5:1 minimum |
| WCAG contrast (large text) | 3:1 minimum |
| Hue rotation limit | 20-30° max |
| Gradient hue range | 30° max between two hues |
| Scale adjacency | ≥25% difference between values |

### Anti-Patterns to Avoid

1. Starting with the layout shell before designing features
2. Designing in full color from the start (design in grayscale first)
3. Using only font size for hierarchy
4. Grey text on colored backgrounds
5. Label: value format for all data display
6. Letting HTML semantics dictate visual styling
7. Making all elements fluid/percentage-based (use fixed widths where appropriate)
8. Scaling all elements proportionally across screen sizes
9. Equal spacing everywhere (use more space between groups, less within)
10. Using em units in type scales
11. Using CSS lighten/darken for color shades
12. Using hex instead of HSL
13. Relying on color alone to convey meaning
14. Adding borders to separate everything
15. Scaling icons/screenshots beyond their intended size
16. Designing with placeholder images
17. Ignoring empty states

### Quick Decision Framework

```
Need emphasis?     → Bold weight or darker color (not bigger size)
Need de-emphasis?  → Softer color or smaller size (not lighter weight below 400)
Colored background → Hand-pick text color (same hue, adjusted S/L), not grey
Need separation?   → Try spacing first, then background color, then shadow, then border (last resort)
Choosing a value?  → Use your predefined system, pick by elimination
Stuck on a detail? → It doesn't matter yet — move on, refine later
```

---

*This document is a comprehensive reference for LLMs and developers building user interfaces. Apply these principles systematically to produce professional, polished designs without relying on innate artistic talent.*
