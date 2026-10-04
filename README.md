<h1 align="center">Welcome to Skillpper 🐿️ </h1>

<p align="center">
<img src="./logo.png" alt="Skillpper mascot" width="150">
</p>

<p align="center">
 <em> Practical skills for developers and their AI coding agents 🤓 </em>
</p>

---

Skillpper is a community collection of reusable instructions for everyday development work: designing interfaces, researching technical topics, and sharing workflows that work. Each skill gives your agent a focused process, useful references, and clear expectations for the result.

Browse the collection, install the skills that fit your work, and contribute what you learn along the way.

## Skills

This index is generated from the `name` and `description` in each root-level skill's `SKILL.md`. Descriptions keep their original language.

<!-- SKILLS:START -->

| Skill | Description |
| --- | --- |
| [ai-memory-obsidian](./ai-memory-obsidian/SKILL.md) | Portable workflows for persistent memory and Obsidian across macOS, Linux, and Windows. Use when the user asks to recall or save past context, record decisions, create vault notes, or configure ai-memory, Obsidian CLI, or an Obsidian MCP bridge. |
| [design-craft](./design-craft/SKILL.md) | Opinionated product-design skill for building, reviewing, polishing, and iterating on landing pages, apps, dashboards, AI products, design systems, and brand touchpoints. UX and comprehension first, then restraint (three type sizes, delete decoration), then foundations, then tactical craft — hierarchy, spacing systems, type scales, HSL palettes, shadows, finishing touches. Distilled from 20 YC Design Review videos (Linear, Stripe, Cursor, Framer) plus the Refactoring UI book. Use whenever the user asks to design, redesign, critique, or polish anything user-facing: "make it look better/more professional/trustworthy", de-slop the AI/vibe-coded look, fix a landing or pricing page, improve conversion, design an AI feature or agent UI, set up tokens or a design system, review a URL/screenshot/mockup. Also trigger for tactical UI questions — spacing feels off, visual hierarchy, choosing colors, typography, empty states, Tailwind/CSS styling — even without the word "design". Not for pure backend/DevOps work. |
| [skillpper-saver](./skillpper-saver/SKILL.md) | Aggressive token, context, and cost optimization mode for AI coding agents (Claude Code, Antigravity, Cursor, etc.). Prevents marathon sessions, eliminates redundant file re-reading, prioritizes text extraction over screenshots in browser automation, and manages context windows with surgical cutoff triggers. Use when the user requests token savings, context optimization, quota conservation, or when starting extensive refactoring, browsing, or debugging tasks. |
| [study-quiz](./study-quiz/SKILL.md) | Use ao pedir quiz, teste, prova, simulado, questões de múltipla escolha, mini-desafio, gabarito, “me testa sobre X”, “gera um quiz de X” ou uma avaliação sobre um assunto, em um nível ou numa faixa de níveis. Use também quando o usuário responder um quiz gerado aqui e quiser a correção. Não use para palestras, slides, design, flashcards, resumo ou plano de estudo. |
| [technical-talk-research](./technical-talk-research/SKILL.md) | Pesquisa e estrutura palestras técnicas em PT-BR com fontes atuais e verificáveis. Use ao pedir referências para uma explicação técnica, levantamento de artigos ou posts recentes, curadoria de fontes, roteiro ou slides de palestra, ou revisão da bibliografia de uma apresentação. Pesquisa somente no catálogo de fontes aprovado, mantém rastreabilidade de cada afirmação técnica e exige um slide final de Referências bibliográficas. Cria apresentações exclusivamente pelo MCP da Gamma, usando o template \`nkhgcucv1lw00wc\`. |

<!-- SKILLS:END -->

We also have a bunch of recomendation of third-party skills you can use on your daily workflow, [check it out!](RECOMENDATIONS.md)

### Suggest a recommendation

Open a pull request adding a row to this table with the project name, original repository, author, a short description of its use case, and official installation instructions. Include an example of how you used it in the pull request so maintainers can assess the recommendation.

This list is curated manually and stays separate from the automatically generated index of this repository's own skills.

## How to install

### 1. Check the prerequisites

Install [Node.js](https://nodejs.org/en/download) with npm, and use an agent supported by the [Skills CLI](https://github.com/vercel-labs/skills), such as Claude Code, Codex, or Cursor.

```bash
node --version
npm --version
```

### 2. Choose your skills

Open a terminal in the project where you want to use the skills. Preview the available skills:

```bash
npx skills add kipperdev/skillpper --list
```

Then launch the interactive installer:

```bash
npx skills add kipperdev/skillpper
```

Follow the prompts to select your skills, target agents, and installation scope. Project installation makes the skills available in that project; global installation makes them available across your projects.

To install just one skill:

```bash
npx skills add kipperdev/skillpper --skill design-craft
```

To install it globally for Codex:

```bash
npx skills add kipperdev/skillpper --skill design-craft --agent codex --global
```

### 3. Put a skill to work

Start a new session in your agent and ask for a task that matches the skill. For example:

> Use design-craft to review this landing page and suggest the three most useful improvements.

Read the skill's `SKILL.md` for its workflow and prerequisites. Some skills require additional tools or services; `technical-talk-research`, for example, requires Gamma MCP and its specified template to create presentations.

## How to contribute

New skills, improvements to existing workflows, clearer documentation, and bug reports are welcome. A useful skill solves a concrete problem and helps another developer repeat your process.

### 1. Fork and clone the repository

[Create a fork](https://github.com/kipperdev/skillpper/fork), then clone your fork and create a branch (replace `YOUR-USERNAME` with your GitHub username):

```bash
git clone https://github.com/YOUR-USERNAME/skillpper.git
cd skillpper
git switch -c add/my-skill
```

### 2. Add or improve a skill

Create one folder per skill at the repository root. Use a lowercase, hyphen-separated name:

```text
my-skill/
├── SKILL.md           # Required: metadata and instructions
├── references/        # Optional: supporting documentation
├── scripts/           # Optional: helpers used by the skill
└── assets/            # Optional: templates or other resources
```

Start `SKILL.md` with YAML frontmatter. The `name` must match the folder name, and both fields must be non-empty strings:

```markdown
---
name: my-skill
description: >-
  Explain what the skill does and when an agent should use it.
---

# My Skill

## When to use

Describe the problem this skill solves and any required tools or setup.

## Workflow

1. Gather the context needed for the task.
2. Follow concrete, repeatable steps.
3. Verify the result against clear success criteria.

## Expected output

Describe what the user should receive and include an example.
```

Keep instructions focused, link supporting files with relative paths, and document dependencies. Use examples that another developer can try without access to your private environment. Include only material you have permission to share, and credit sources where appropriate.

### 3. Try it locally

From your clone, install your working copy for your agent:

```bash
npx skills add . --skill my-skill
```

Try a realistic task and check that the skill produces the expected result. For an existing skill, check that your changes still support its original use case.

You can also validate the metadata and preview the generated index with Python 3.10 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r scripts/requirements.txt
python scripts/update_skills_index.py
python scripts/update_skills_index.py --check
python -m unittest discover -s tests
```

Edit skill descriptions in their `SKILL.md` files. The table above is generated automatically; you do not need to maintain its rows by hand.

### 4. Open a pull request

```bash
git add my-skill/
git commit -m "feat: add my-skill"
git push -u origin add/my-skill
```

Open a pull request from your branch to this repository's default branch. Explain the problem your skill solves, include an example prompt, and describe how you tested it. For improvements, explain what changes for the user. GitHub Actions validates the metadata and index generator; the README index is refreshed after merge.

For ideas or problems that do not need a pull request yet, [open an issue](https://github.com/kipperdev/skillpper/issues).

## How the index stays up to date

The [skills index workflow](.github/workflows/update-skills-index.yml) discovers root-level `*/SKILL.md` files and generates an alphabetical table from their YAML metadata. Adding, renaming, removing, or changing a skill updates the index on the next relevant push to the default branch. Everything outside the index markers stays untouched.

Pull requests run validation without pushing changes. On the default branch, the workflow commits `README.md` only when the generated index has changed. Maintainers can also run it from **Actions → Update skills index → Run workflow**, selecting the default branch.

The update job requests `contents: write` for the built-in `GITHUB_TOKEN`; no personal access token is required. Repository or organization policies and branch rules must allow that bot to push to the default branch. If direct pushes are blocked, generate the index locally and include the README change in a pull request.
