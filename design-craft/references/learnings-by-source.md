# Learnings by source

Distilled from 20 YC videos: the full "Design Review" playlist (website/app critiques with Garry Tan, Katie Dill, Karri Saarinen, Ryo Lu, Jorn van Dijk, David Siegel, Vlad Magdalin, Zack Onisko, Zain Ali, Pete Koomen, Raphael Schaad, Steven Haney, Ev Boufar) plus Garry Tan's "Design for Startups" lecture and Pete Koomen's "AI horseless carriages" talk. Paraphrased in our own words; not transcripts.

## Table of contents

1. Karri Saarinen (Linear) — products that stand out
2. Steven Haney (Paper) — design in the agent era
3. Ev Boufar (YC Head of Design) — designing with AI
4. Cross-source synthesis (all sources)
5. Garry Tan — Design for Startups (foundations lecture)
6. Pete Koomen — AI horseless carriages / better AI apps
7. Katie Dill (Stripe) — why design matters + site reviews
8. Raphael Schaad — founders' design game + AI interfaces of the future
9. Karri Saarinen — brand design review (Linear v1 vs today)
10. Ryo Lu (Cursor) — vibe-coded sites
11. Jorn van Dijk (Framer) — why sites don't convert
12. Website critique episodes (Webflow, Instacart, Garry Tan on AI sites, Pete Koomen on conversion, Zack Onisko first-impression test, Glide dev-tools, Glide mobile apps)
13. YC's own homepage redesign (Aaron + Ev)

---

## 1. Karri Saarinen (Linear) — products that stand out

**Why design, and what it is**
- Design is "finding things that fit and feel good." Applied to products *and* companies.
- Every touchpoint is the brand: the sales rep, the onboarding email, the error state — not just logo and colors. Brand is what the person *feels* across the experience, and consistency over time is what makes a brand trustworthy (Airbnb lesson: predictable behavior builds trust; volatility destroys it).
- Design's value is partly usability and partly emotional — it amplifies everything else you do (customers, hires, even investors respond emotionally).
- Design compounds. Small quality decisions early accumulate; skipping them creates a big-redesign debt years later that annoys customers when everything changes.
- Even a 3–5 person startup benefits from a designer because early leverage is huge.

**Trust and visual craft (Coinbase lesson)**
- A functional product built on off-the-shelf UI kits reads as "a hack project" — in a trust-sensitive domain (money, health, identity) that costs conversions. Fix visuals first, structure second, brand third.
- In abstract or scary domains, use concrete, human, grounding imagery (people, landscapes) to make it feel real.
- Details signal care: a logo with a coin "tipping over" feels unstable when the product is about safety. Every visual should agree with the message.

**Quality without slowness — Linear's operating model**
- "Quality" ≠ perfection. It's a direction: the customer must have a great experience; rough beta is fine if you *come back and finish it.*
- Small teams (1 designer + 1–3 engineers), no big committee. Design-by-committee produces features that are "for nothing" because everyone added a bit.
- You can spec a solution, but you can't spec quality of execution — that lives with the people building it, so give the engineer + designer ownership to change the design when it turns out not to work.
- Process: feature flags → internal dogfood (rough is fine) → beta with specific customers → **final polish pass before GA**: check animations, details, "does it feel good, are we missing something." Polish once, at the end, deliberately.
- Light timeline pressure is useful because it forces scoping down, which forces prioritizing the right things. Track progress, don't punish missed dates.

**People and hiring**
- The people you hire are the biggest lever on product quality. Look for people who have built something whole on their own (first engineer, side project, open source), because it forces "should I do it this way or that way?" thinking.
- Interview by asking "what are you proud of, and why did you do it that way?" repeatedly; you're testing whether they *notice* good vs bad and pay attention to user/business problems, not just tech.
- Founders' test: "if we disappeared, would the team know what to do?"

**Differentiation**
- To be an outlier you must be *known* for one thing you do far better than anyone else. Decide it deliberately; it can't be what everyone else does. Most competitors have no brand at all — nobody can say what they're "about."

**Designers as founders / designer mindset**
- A designer's job is solving the company's problems *through* design, not filling Figma files. Design feedback is often really "this doesn't solve my problem" — the problem is misaligned or unclear. Learn from sales (they talk to customers), from leadership (what they want).
- Designer superpower: broader view — sensing what fits, visualizing outcomes, reasoning back to inputs (people, brand, product).

**AI and design**
- AI raises the floor (decent design becomes accessible) and raises the ceiling (best keeps getting better). Getting to *average* is easy; beyond that still needs the accumulated judgment.
- Danger: when something is easy to make, you stop thinking about it. Difficulty forces "is this worth doing? are we approaching it wrong?" — a clarifying friction. Outsourcing output too much means losing understanding of your own product.
- The real website problem is not the design, it's the narrative: what is this for, who is it for. AI doesn't solve that for you.
- Roles shift toward IC-lead/curator: responsible for the AI's output — "is this good, does it fit, does it work."
- Product AI advice: solve specific, bottom-up problems (e.g. issue triage) rather than broad "ask anything" chat.

## 2. Steven Haney (Paper) — design in the agent era

**Why design (again)**
- Every great company of the last 10–20 years has exceptional design; you can't name a counterexample. If you want to be one, put the care in.
- Using whatever the model spits out makes you look like one of a million projects and "less like you care." It's tempting under time pressure — resist.
- Sloppy design triggers "what else don't they pay attention to?" — especially deadly for finance, health, anything requiring trust.
- Mediocre presentation also hurts hiring: talent is attracted by craft.

**The AI-tells list (the "insecure designer" look)** — models over-fill space
- Too-heavy font weights (bold/black everywhere). Pull weights back as light as they can go.
- Too many font sizes (5–8). Consolidate to **three**.
- Little colored side-swoop / accent border on every card.
- Cards everywhere; 20 cards on one page.
- Purple + gradients; glows.
- Tiny all-caps kickers/eyebrows with extra letter-spacing.
- Badges/pills with icons; icons everywhere.
- Meaningless numbered markers (01/02/03) that anchor corners but communicate nothing.
- Light/dark mode as a launch "feature" — free from the model, rarely worth building; bad dark modes that just invert colors.
- Too much text; too much going on; contrast mistakes.
- Generic stock hero shapes and layouts identical to every other vibe-coded site.
- Widgets for widgets' sake — decoration that doesn't help the user understand anything.
- Trend-encoding: "Linear made this style great, then it got encoded into the models." In isolation none of these are bad; overused they read as unintentional.

**Fixes that immediately read as "designed"**
- Three type sizes, regular weight or lighter, check contrast/readability, delete decorative numbers/icons/badges → suddenly "cleaner and more approachable."
- "A lot of design is deleting." Overbuild, then pull back. Chanel rule: remove one accessory.
- Supporting elements should look supporting (lower contrast), not compete with content.
- Get the real value proposition (and the strongest evidence, e.g. "how it works", social proof like a YC badge) **above the fold**. Many sites get *more* trustworthy the further you scroll — that's backwards.
- Comprehension is a big part of design: can the reader tell what this is and what they get?
- Keep the energy that makes a site unique; only pull back what undermines trust. Sometimes an over-clean rewrite loses the excitement — that's where a human re-injects it.
- Design's baseline is always moving; average = invisible.

**Agent-native workflow**
- Code as the source of truth for the design system. Teams maintaining two copies (design tool + code) can't keep them in sync — it's intractable. Summon components from the codebase as needed.
- Ask agents for **many variations** (3, 20, hundreds overnight), then curate and branch: "I like the list from this one, the featured-card layout from that one." Curation is a new design process.
- Give the agent an expert's guardrails: Paper's "secret sauce" is literally senior designers distilling typography/contrast rules into model instructions.
- Best tool for the job: sometimes prompting, sometimes dragging/direct manipulation. Deleting an element by hand and watching layout snap into place beats describing it in prose.
- Prompt simply; iterate; the model isn't done when it first returns — check text overflow, alignment, contrast, then correct.
- Model choice: use the highest-taste model for real design work; fast models for demos make more mistakes. Different models for taste vs precision/batch tasks.
- Start from what users actually see (grab the live site), edit, then push back into the codebase; the agent matches existing conventions. The handoff disappears.
- Humans still make the decisions: design in an org is stakeholders, requirements, problem space — the pixels are the output. Models get better at tactics (letter-spacing, weights); taste and narrative stay human.
- Paper still has humans read every line of core-product code because a design tool needs precision and 120fps; "quality software takes time." Competitors with every feature don't win if nobody cares about them.

**Company/product lessons**
- Do the thing you'd do anyway (founder-market fit). Values-aligned marketing (a shader library, a font) instead of ads.
- Bottleneck-first: identify what the business needs next and do the simplest thing that unblocks it.
- Talk to a designer every single day for the first year; everyone talks to users.
- Radix lesson: listening to both sides of a handoff (designers want engineers to change, engineers want designers to change) produces confusion. Pick a user.

## 3. Ev Boufar (YC Head of Design) — designing with AI

**Toolchain and modality**
- Lives almost entirely in a coding-agent orchestrator + an agent-native canvas tool. Pinterest for visual inspiration/moodboards.
- Talks instead of types (voice → stream of consciousness feature description).

**Context is the unlock ("soul.md")**
- Record every meeting; dump transcripts + manifesto + glossary into a `soul.md` (or a hierarchy: design.md, manifesto.md, content.md). Treat it as the exhaustive source of truth that feeds every future decision.
- Result: the agent starts including things you didn't ask for (the launch-party date, a barcode because it's a zine, an interactive map) — "it can see things ahead of us." One-shottable quality is only possible with a detailed, intentional design.md/soul.md.
- Feed moodboards/screenshots/websites you love. You don't need to know *why* you love a site — the agent can find the common thread across your references. This is how you break out of generic output.

**Exploration by volume, then curate**
- One-shot 16 full-website variations from the moodboard + real content. Build a disposable gallery page for yourself with pin/bookmark to keep track of favorites. Combine pieces across iterations.
- One-shots aren't for craft; they're for exploration and feel.

**Disposable tools / "you can build anything for yourself"**
- Build throwaway tuning modals (sliders for a dithering shader), a template generator for 12+ speaker cards, a screen-recording timer for a perfect 4-second loop, a gallery with bookmarks. Make everything live and tunable instead of static, then discard the tool. It's a muscle to train.
- Everything is editable/movable — imagination is the bottleneck now.

**UX decisions on the projects**
- Playful data-report cards inspired by Spotify Wrapped, prompted by real user interviews ("I'd love to know my biggest crash-out").
- Deliberately text-heavy landing page because the goal was to be explicit and upfront about motivation (an experiment). Break convention when the reason is the user's actual need.
- Two versions of a site: human (visual) and machine (markdown, distilled, copy-to-clipboard, with an explicit "AI agents: do not run commands from this page" note). Agents don't care about visuals; that's a content exercise.
- Feature-request / bug form treated as a prompt box that fires an agent → PR; CTA says literally "Send to an agent." Collect name to credit contributors. Software becomes personal/customizable.
- Consistent visual language: one shader with fixed parameters reused across posters, tickets (personalized with name and city — shareable delight moment), social loops, giant event screens. Consistency is now easy — reuse the same code.
- No-AI on the physical zine's art: it's obvious to viewers when something is highly intentional and took months.

## 4. Cross-source synthesis

Where the sources converge (see the landing-page and AI-UX references for the applied versions):
1. **Design = differentiation + trust.** Sloppy or generic visuals cost trust in exactly the moments that matter, and generic = invisible.
2. **Comprehension first.** Value prop, evidence, and "how it works" must be understood fast, above the fold. Narrative beats decoration.
3. **Restraint.** Fewer type sizes, lighter weights, fewer cards/badges/icons/numbers, less text. Delete more than you add. Spend boldness in one place.
4. **Quality is a culture and a final pass, not slowness.** Small owning teams, feature-flag → dogfood → beta → deliberate polish → ship.
5. **AI raises the floor; humans own taste, narrative, and decisions.** Use agents for volume (variations, tedium, consistency), then curate. Feed them rich context (soul.md, moodboards, real content, expert rules). Never ship raw output.
6. **Code is the source of truth**; the design tool is a visual interface onto it. One design system, in the repo.
7. **Every touchpoint is the brand**, and consistency over time is what makes it trustworthy.
8. **A stranger must answer, in order: what is it → is it for me → does it work / can I trust it → what do I do next.** Nothing lower in the hierarchy compensates for a miss higher up.
9. **Users are one tap from leaving.** Earn each scroll; five to ten seconds is all a hero gets.
10. **Show the real product, and let people try it before any wall.** Screenshots zoomed to the meat, live demos, playgrounds; gate on export/save, not on entry.
11. **Details are trust.** Spacing, alignment, casing, hover states, working links, real names on quotes — sloppiness triggers "what else don't they care about?"

---

## 5. Garry Tan — Design for Startups (foundations lecture; transcript ends ~40 min in)
- Design is making things *for other people* that work well and delight; remove any word from that and it breaks. It's how it works, not merely how it looks. Form follows function; empathy (Carnegie, PG's "what is the user thinking and feeling") is the founder skill.
- Good design is as little design as possible (Rams). Novelty is often the opposite of functionality; at the interaction level, steal what works (established patterns) and watch for modality mismatches (mobile carousel dots on a desktop site). Party metaphor: no line, someone greets you, takes your coat, shows you where things are.
- Product design = problem statement → personas (specific humans, their device and comfort with tech) → PRD → P0–P3 priorities → bug database. If you don't prioritize you can't cut, and then you never ship. Scope / quality / time triangle. Devil is in the P2/P3 tail.
- Interaction design: people treat computers as people (Nass, Reeves, Fogg); a UI is a conversation. Use direct command language and active voice; one obvious high-contrast CTA; startups can't afford big-company passive voice. Reduce cognitive load (dropping "confirm password" lifted signup conversion ~50%); chop complex flows into wizards.
- Visual design: avoid ornament and chart-junk (Tufte); remove anything removable without loss of meaning (even colons in forms). Three tools: **contrast** (weight, color, size — if everything is bold nothing is), **closeness** (proximity = relatedness), and a **grid**, which together yield visual hierarchy. Squint test: the eye goes to the highest contrast thing. Layout order: padding/margin first → a line if needed → a box last (boxes are loud). Whitespace is fine.
- Feedback loops: usability-test wireframes before code; customer support is user research — the long tail of "once in a blue moon" cases adds up to a broken product; the founder answering support creates evangelists ("100 people who love it").

## 6. Pete Koomen — AI horseless carriages / how to design better AI apps
- The failure: bolting AI onto software designed for humans to do work in ("how do we slot AI into Gmail?"). Ask instead how the tool would be designed from scratch to offload the repetitive work.
- Gmail draft example: a generic, hidden system prompt produces text nobody would write, and the prompt is as long as the output — more work than doing it yourself. Two failures: not in my voice; not less effort.
- The system prompt is English, so stop treating it as a black box: let the user see and edit it; better, auto-generate it from their history and refine it via feedback ("I'd have phrased it this way"), with a break-glass edit. Most people never touch it, but it's custom to them.
- Prompts are code non-programmers can write; every profession gets a "Cursor moment" when the domain expert can teach the agent their workflow. Developers shift to building tools (label, archive, draft, call APIs) — agents that act, not chatbots. Liability mindset nerfs products; dev tools won by handing over the full power.
- Practical pattern: sit next to the user, watch the workflow, write the prompt together, iterate.

## 7. Katie Dill (Stripe) — why design matters, and how she reviews
- Trust-heavy, novel products (a stranger's home, moving money) succeed because thoughtful details make the new thing approachable: "if they cared this much about the interface, they'll take care of my money." That logic applies against any competitor.
- The founder's mindset sets the culture: if design happens only "when it moves the numbers", it happens only then. Care about the user and about intentionality in every detail; hire that mindset.
- "The gravitational pull is to mediocrity." Quality is micro-decisions every day plus the courage to hold a ship a week when it would leave a mark on the first impression. Balance with betas and bite-sized releases; never craft without feedback.
- Product-quality order: functional (utility) → usable → craft & beauty. Beauty is material, not nice-to-have — but pointless without the first two.
- Pre-flight mindset: inspect as if something *is* wrong and you must find it. Question every word and pixel. Technical founders can apply edge-case thinking to design.
- You can't un-know your product: sit users down, think-aloud, repeatedly. Develop taste by observing what you love and hate and writing down why; taste is harder to teach than a domain.
- Org: designers embedded in product teams with shared goals; product, brand, and website under one roof so billboard → site → product is one story.
- "Walk the store": 17 essential journeys, each scored red/yellow/green quarterly with friction logs; a company goal to keep them green; a bugs@ alias anyone can use; regressions happen as the product grows ("redid the dining room, now the kitchen looks worse").
- Micro-behavior matters: don't flag an email invalid while the user is still typing. One redesigned onboarding email (hierarchy + one clear CTA) lifted product conversion ~20%.
- Site reviews: first impression = how the brand wants you to feel, on purpose. Scroll-hijacking, "scroll to explore", long story videos before information — people leave; if you have to tell them how to use the site, it's wrong. Every pixel must add value; a video thumbnail must carry value unplayed; portray the actual customer (a 21-year-old sample vs an older-man photo); mixed Title/Sentence case, stray shadows, cut-off decorative lines, a logo that reads as a broken TV — all erode trust. Ask users how they'd describe you → headline. Map the whole journey (ad → landing → CTA → signup): the problem is often the step before. B2B can be joyful; stop when fun erodes legibility. Don't bold the negatives — skimmers read the bold. Bring "why trust us" onto the page; people scroll more than they click.

## 8. Raphael Schaad — founders' design game; AI interfaces of the future
- Desirable × viable × feasible = design × business × tech; design is the "make something people want" circle. Designers now control the means of production; be fluent in the medium (code).
- Design = how it looks + how it works + **how it's built** (framework, latency, loading states are design). "Like" isn't a design word — it works or it doesn't; users judge. Good design lasts, is repairable, gets better with age (adaptive UI, muscle memory, shortcuts).
- Level up: learn by doing; surround yourself with well-designed objects and refuse bad ones; read *Grid Systems*, *Elements of Typographic Style*, *Design of Everyday Things* (mental models).
- Process: users → paper sketch (unconstrained but bounded) → straight to high fidelity in code to *feel* it → put in front of users. Respect platform norms (focus/blur, dropdown behavior), then push — familiar yet novel.
- AI era: nouns (buttons, fields) → verbs (autocomplete, summarize, send an agent); time and real data become part of the design; static mockups break down. Voice: latency is the interface, expose it (ms), pair multimodal cues, handle interruptions. Agents: canvas as a new document type; color-code node types with a legend; different fidelity per zoom level; templates that show branching. Blank prompt boxes need example prompts as one-click buttons and contextual suggestions; show sources inline per claim/cell so results can be trusted; keep the human in the loop (editable columns). Long generations: persistent step-by-step logs, honest ETA, low-fidelity early results you can interact with, or "we'll notify you". Prefer incremental/diff edits and module-level prompting; show what the model respected vs ignored from the prompt; guided prompt builders for jargon. Adaptive UI: content in → UI out; keep hotkeys stable when labels change; be explicit about focus. Ladder of abstraction: autocomplete → adaptive options → best-guess draft already there → autopilot. Trade fidelity for immediacy (blurred preview + real audio before a 12-minute render).

## 9. Karri Saarinen — brand design review (Linear v1 → today)
- Be authentic to your stage. Stripe's and Linear's first sites weren't polished; a very polished site on a month-old product sets the wrong expectation. Own being small.
- Linear v1 (2019, ~2 days of work): "issue tracking" — the specific term the ICP uses — instead of "work platform". The ambitious pitch is for investors; the specific one is for the site; you are *filtering out* the wrong people. One page: faded product screenshot for curiosity, "fast", command menu, integrations, a real team, an email box. Later versions add depth in sub-pages but keep the homepage simple.
- Homepage = front page for people who don't know you: enough to decide if it's interesting, not so much you're overwhelmed. Pyramid: one clear thing, then expand as you scroll; deeper pages for features, customer stories, security.
- Nice effects signal care, but movement in the hero can steal attention from the copy; a floating prompt box reads as a cookie banner and gets ignored — put it in the page.
- Generic builders: group templates by audience and blow up one example so people see how it works.
- Enterprise: website conversion is low because enterprises don't convert via websites — you need sales/events; still let people try, give the demo agent guided prompts (a blank "what do you want to talk about?" stalls), and know that demo mistakes scare buyers. Use the buyer's language. Don't overclaim ("most admired companies in the world"). If it's voice, say voice in the hero. Enterprise buyers need materials (security page, stories) — deep pages you link from email, not the front page.
- Unreal Milk: memorable, first-principles, hand-drawn font/illustrations create an organic feel to counter unease about lab food — but no CTA and unclear what it is / where to buy; add "join the cause" mailing list; the bottle's plain logo misses the site's playfulness — brand must be consistent across touchpoints.
- Type: sites are text, so typeface is a big brand decision; small sizes need a standard readable face; headlines can carry a unique one; choose the world the brand lives in (serif/retro vs geometric-modern vs futuristic).
- Differentiation: find your lane; the first ICP cares about one thing (startups → speed, no complexity); ask customers why they picked you and put those reasons on the page. If your wedge is existing open-source users, say "hosted X — here's how the platform expands it".
- Dropback: chaotic because everything is crammed above the fold with a moving grid behind text; people do scroll — keep the top simple and bigger, push info down or into targeted pages via nav; yellow buttons need contrast; feature-based vs use-case/customer-based pages depending on audience; non-technical buyers want trust and faces like theirs more than a fancy site.

## 10. Ryo Lu (Cursor head of design) — vibe-coded sites
- Motion timing: don't animate CTAs before people can read; motion is attention theft — spend it at the right moment. Broken hovers and snapping tickers scream "vibe coded".
- A cute headline needs a literal sub-headline; talk to the target more, not vaguer. Style drift between sections; default AI icon packs and tight Helvetica read as slop. Fix: decide core tokens deliberately (or go safe with system fonts — a decision beats randomness), avoid massive shadows and purple gradients/buttons; with robust tokens + components, AI composes well.
- Six words describing the product and everything else about signup = not enough; add words. Don't ask for money before explaining. Your logo should be bigger than the YC badge — the badge isn't the thing. Two names for one product = confusion; pick one.
- Per scroll one main CTA; priority = message → CTA → proof. Invented concepts ("progressive discovery") that nobody searches for → describe the problem in the user's words ("I have too many MCPs"), old world vs new world. Show all integrations with quick filters instead of a fast ticker. Excel-looking charts, moving-while-reading, unnecessary lines: bad. Headlines must be explicit; subheads are only read if the headline intrigues.
- Negative-first headline is uninformative; say the positive thing. Marketing → product → pricing must feel like one site. Don't cartoonize people's photos; standardize headshots with a filter. Own about page, not a link to your launch post.
- Structure fine, details missing (raw markdown look, misclipped video, misaligned images, inconsistent shadows/borders — boxes in boxes). Don't describe yourself as "Cursor for X + ChatGPT + Superhuman" — own it. Above the fold: zero obvious detail bugs.
- Product UI while the AI works: show every state (tool calls, what's running, what needs confirmation) in a controlled focus area — no wall of text, no random spinner quips, no two spinners, no mystery toggle without tooltip. Let people play before sign-in and constrain the first demo to succeed. Disjointed radii/hover states/iframes = raw AI UI.
- The standard template (badge, two blue buttons, headline, screenshot) is fine for many; break it when you need identity — but simple and plain, with product and message as the hero and "punch points" as you scroll, is respectable.

## 11. Jorn van Dijk (Framer CEO) — why sites don't convert
- Too much motion; two CTAs get lost among brand-orange — try black or one large CTA. "Book a demo" is a dramatic ask on a first visit: convince first; the CTA should be "show me the product / 2-minute walkthrough".
- Vague generic illustrations don't anchor anything; show screenshots or a video; concrete feature names land — put them higher. Tabs: assume no one clicks; tie tabs to scroll if you must; slow the logo ticker and make logos clickable to context.
- Animation is hard; its #1 use is drawing attention and making the point overly obvious; simplify — a new visitor won't watch four loops. Ask someone experienced to review your first animation. Product shots should show the actual product, not a metaphor.
- Claims like "high quality" require proof, and honesty about the real value prop (speed/ease vs premium). Sample outputs must be great by everyone's standard.
- Sign-up walls block the aha; let people generate first and gate on export/share; put the prompt bar on the front page; you're competing with free.
- Distinct style + hook headline + modern logos work; a try-it box followed by a signup wall is a missed chance to show blurred results; notification-like popping cards feel stressful; a dated changelog signals momentum; brand disconnects (people product with no people; "war" metaphor vs a playful name) confuse.
- If the copy says enterprise scale, the visuals must too (many agents, not one consumer phone). Pulsing "click to answer" is animation done right; steer demos toward the buyer's problem.
- Swirly script + random fonts, double spaces, spaces before periods → "not detail-oriented"; set a max-width; funnel text to the button; unexplained name/joke; same widget must behave the same everywhere; testimonials without company names, Title-Cased Every Word, feel fake and taint the numbers next to them. Exercise: blank page, only what explains what it is, test on 20 strangers, then expand. Multiple pages are allowed.

## 12. Website critique episodes — consolidated
- **Order of questions** (every host): what is it? → is it for me? → does it work / is it credible? → what do I do next. Answer above the fold, in that order.
- **Headline-skim test**: read only the H1/H2s down the page; the story must survive. Competing value props in H1 vs H2 (developers vs product teams) confuse.
- **Value over features**: "rent it faster, make more money" beats "image enhancement"; turn features into pains solved ("never do X by hand again").
- **User's words**: ask customers "how would you describe us?" and put the phrase in the H1. Jargon can be right when it self-selects the ICP — test with them, not with outsiders. Don't be clever if clever = confusing.
- **One primary CTA**; secondary as a link; repeat it (same text, color) down the page and in the footer; sticky if long. Button words set expectations ("open" ≠ "sign up"). Embedding the email field beats a "book a meeting" button. Address the objection on the button ("no credit card"). Social login cuts friction.
- **Funnel**: map every step from landing to the aha; measure drop-off; cut until the aha is step two. Two questions: does the page convince me? does the signup talk me out of it? Everything behind tabs/sliders/carousels is unseen; auto-advancing carousels fight the reader; lay it down the page.
- **Show the product**: before/after slider, live demo, "feat of strength" for AI (type a little, magic output), example prompts as one-click buttons, sandbox before account, screenshots zoomed to the meat with the rest blurred, text overlays and slower pacing at key beats; a headline→full patent demo strains belief — show enough steps. Screenshots on a white site bleed into the page — change background contrast; alternate section backgrounds; label interactive demos ("edit me").
- **Trust**: faces + names + companies + press logos read as real; a founder story/about page; live chat with the founders behind it is an unfair advantage; case study with a known logo; counts (approvals, users) in high-stakes domains. Fake-feeling testimonials (no company, odd casing) poison the numbers next to them.
- **Motion**: a spotlight, not weather. Put it on the one thing to read first; wrapping sentences in motion are unread; sideways/fast tickers, moving grids behind text, multiple simultaneous animations, glows, and scroll-hijack are the common sins. Calm reads as established. Animate CTAs in when the reader reaches the decision point.
- **Fit and finish**: line-height, section gaps, alignment, contrast (light gray on dark), max-width, tap targets, casing, hovers — small misses break the "enterprise" illusion. Heavy pages die on mobile before the five seconds start.
- **Specificity of audience**: write for the ICP, not "anyone who might need our tech"; persona landing pages convert; say the location if you're local; say the sub-segment (US C-corps) in the primary message; the "biggest clue" (construction footage) shouldn't be below the fold.
- **Differentiation must be explicit**: "why us vs the dozen others"; the buried mechanic (group buying) should have been the headline. Nobody wants generic "workflow" software — lead with a specific use case, then reveal breadth; "how it works" early.
- **Dev tools**: repo + stars + contributor velocity, a playground to try now, syntax-highlighted real-text code at least as big as body copy and hand-wrapped, annotate code line by line, bento feature grids, pricing turns a project into a product; early-stage: product and code first; later: testimonials, pricing, contact sales; details before benefits for a skeptical technical audience; acknowledge how you differ from prior attempts.
- **Enterprise vs self-serve**: enterprise sites aren't conversion machines; give buyers materials in deep pages; still let people try; guide the demo agent.
- **Mobile apps**: platform standards (native nav, tab bar, disclosure indicators, no wrapping tab labels), design for context of use (walking, driving, one hand), thumb targets ~60px, animate shape changes, forgiving live search, get to the aha immediately then show state (available vs busy), one primary CTA color, don't repeat your logo on the main screen, confirm cart adds, no upsell/gamification before the first successful transaction, cut onboarding questions, drop users into the first real action, taps must respond instantly, and if it's mostly content it's a website not an app.
- **First-impression test**: five seconds, close it, "what does it do?" If the answer is a color, the hero failed. One headline, one byline, one CTA; two equal columns means neither wins; the real headline is often one scroll below — promote it.

## 13. YC's own homepage redesign (Aaron + Ev)
- Old site failed the headline-skim test, didn't quantify claims, listed what YC *doesn't* do instead of the positive, and looked like a B2B SaaS template.
- New: don't sell the program, make people dream. Storytelling from the brand's roots ("formidable", a footnote nod to PG); the hero as a header for the next section; before/after founder photos so a builder thinks "this could be me"; kept 13-year-old copy for continuity; founders' words instead of self-praise; partner photos from their own batch (transformation, playfulness); event photos animated carefully so faces stay stable; the final CTA addresses the #1 objection ("it's never too early").
- Aesthetic: minimal hero after trying pictures/animation; airy, floating, no borders/dividers; remove every unnecessary element; deliberately no hero CTA because inspiration, not 0.1% conversion, is the goal.
- Process: mood boards → Figma felt constraining → new repo, iterate live with a coding agent as a co-worker ("here's the info for this section, display it creatively" → keep the kernel); interactions/animation only when they communicate better; most of the time went to storytelling and interactions because the tools removed the grunt work; kept the brand background color for continuity.
