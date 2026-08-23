# Anti-slop checklist ("does this look like the model spat it out?")

Run this against any UI, page, or component you produce or review — including your own output — before showing it. Each item is a *tell*: harmless once, damning in aggregate. The underlying failure is the same every time: filling space instead of communicating something.

## Typography
- [ ] More than **three** font sizes on the surface? Consolidate to three (display, body, small).
- [ ] Bold/black weights used as the default for headings and labels? Pull back to regular/medium; go as light as legibility allows.
- [ ] Tiny all-caps eyebrows/kickers with wide letter-spacing above every heading? Delete unless the eyebrow carries real information (a category, a date).
- [ ] Line length, line height, and contrast: is body text comfortably readable? Are "supporting" texts visually subordinate (lower contrast, smaller) instead of competing?

## Layout & components
- [ ] Cards everywhere (a grid of 6–20 near-identical cards)? Ask what each card *communicates*. Prefer a list, a table, one featured item + supporting items, or prose.
- [ ] Colored accent border / side-swoop on cards? Remove.
- [ ] Numbered markers (01 / 02 / 03) where order isn't meaningful? Remove. Keep only for real sequences.
- [ ] Badges, pills, chips with icons stuck onto headings? Remove unless the pill is an actual status.
- [ ] Icons next to everything? Keep icons only where they aid scanning or replace a word.
- [ ] Widgets for widgets' sake — stat blocks, mini-charts, "trusted by" rows with no real logos, decorative dividers?
- [ ] Both light and dark mode shipped as a first feature? Cut it unless the product genuinely needs it; if you keep dark mode, design it (never a plain color inversion, never pure black).

## Color & effects
- [ ] Purple / violet gradients, glows, blurred blobs, glassmorphism by default? Choose a palette *for this subject*.
- [ ] Gradient text? Almost always undermines trust.
- [ ] Contrast errors: light gray text on white, gray on colored backgrounds, colored text on gradients?
- [ ] Is the visual energy appropriate for the domain? Finance/health/legal need calm and precision; consumer/creative can be louder — but "louder" still needs one deliberate signature, not noise everywhere.

## Landing-page tells (from the critique episodes)
- [ ] Accelerator badge ("Backed by YC") larger or more prominent than your own logo/name; two names for one product; about page linking to a launch post.
- [ ] Two equal-weight CTAs (or "book a demo" as the *only* first ask); email field hidden behind a button; a "try it" that dead-ends in a login wall; a hand cursor on something that doesn't drag.
- [ ] Testimonials with no company name, Title Cased Every Word, or cartoonized/edited headshots — reads fake and taints adjacent numbers.
- [ ] Generic template hero (badge, two blue buttons, headline, small far-away screenshot) with nothing that says what this specific product is.
- [ ] Logo/name/tagline that contradicts each other (a company named Blue with a green logo, "win the war" copy on a playful brand, a broken-TV logo for a TV product).
- [ ] Moving grid or looping video behind body text; scroll hijack; "scroll to explore"; auto-advancing carousel; a fast logo ticker; content locked in tabs.
- [ ] Double spaces, spaces before periods, no max-width on text, mixed Title/Sentence case, hovers that don't work, boxes-in-boxes screenshots with inconsistent shadows and borders.

## Content & comprehension
- [ ] Can a stranger say what this is, who it's for, and what they get within five seconds, above the fold?
- [ ] Is the strongest evidence (how it works, a demo/animation, real social proof, accreditation) buried below the fold? Bring it up.
- [ ] Too much text? Cut by half, then cut again. Then check whether the remaining words are specific (what it does) rather than clever.
- [ ] Copy tells: "Seamlessly", "Empower", "Unlock", "Supercharge", "Effortlessly", "Elevate", "Streamline", "Revolutionize", "Next-generation". Replace with plain verbs and specifics.
- [ ] Section headers that are generic ("Features", "Why us", "Benefits") instead of claims.
- [ ] Every element earns its place: a label labels, an example demonstrates, nothing quietly does double duty.
- [ ] Coined nouns or invented concepts nobody would search for ("Artisans", "progressive discovery") in place of the user's own words.
- [ ] Negative-first or clever headline without a literal sub-headline.

## Motion
- [ ] Scattered hover-lift, fade-in-on-scroll, and shimmer on everything? Cut. Choose one orchestrated moment (page-load, a hero interaction, a state transition) that serves the subject.
- [ ] Reduced-motion respected?

## Fit and finish (the "what else don't they pay attention to?" test)
- [ ] Alignment: do edges, baselines, and gutters line up? Any awkward gaps between sections?
- [ ] Text overflow, clipped labels, wrapped buttons at common viewport widths?
- [ ] Focus states visible; tap targets ≥ 44px; keyboard navigable?
- [ ] Empty, loading, and error states designed (with direction, not mood)?
- [ ] Do the visuals *agree* with the message? (No "tipping coin" logo on a product about safety.)

## The one-line test
Take everything off that you can. If it still communicates and still feels good, it was decoration. Put back only what you miss.
