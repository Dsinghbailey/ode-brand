---
name: ode-pdf
description: |
  Generate a polished, on-brand Ode with Anthropic PDF: proposals, reports, memos,
  one-pagers, leave-behinds. Authors HTML pages with the Ode design-system
  component library and renders them to a Letter-size PDF via a headless-Chrome
  (Puppeteer) pipeline. Use when the user says "make an Ode-branded PDF /
  proposal / report / memo", "build a designed document", "turn this into a
  designed PDF", or wants a print-quality branded document. Builds on the
  ode-brand foundation. Output is a fixed PDF, not editable Word/Google Docs; for
  editable slide decks use ode-slides. (Ode is the new name for the team formerly
  branded Fractional AI.)
license: UNLICENSED
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
tags:
  Function: [Brand & Design]
---

# Ode with Anthropic — Designed PDFs (HTML → PDF)

Produce a print-quality, on-brand PDF. Content is authored as a sequence of
fixed-height HTML pages styled with the Ode component library; a headless Chrome
render turns them into a Letter (8.5×11in), full-bleed PDF with correct fonts,
colors, and self-computed page numbers.

This skill builds on **`ode-brand`** (the sibling foundation skill), which supplies
the fonts, logos, and color/type tokens. Output is **PDF**. For editable
PowerPoint / Google Slides, use **`ode-slides`**.

## When to use

- "Make an Ode-branded PDF / proposal / report / memo / one-pager."
- "Turn this content into a designed document."
- Any print-quality, brand-consistent document deliverable.

Not this skill: editable decks (`ode-slides`), web/app UIs (a future app-UI skill),
or quick brand lookups (`ode-brand`).

## Prerequisites

- Node.js on PATH (the render engine uses Puppeteer, which downloads Chromium on
  first `npm install`).
- `pdftoppm` (poppler) for screenshotting rendered pages during review. On macOS:
  `brew install poppler`.
- **Brand fonts and logos are bundled** in `../ode-brand/assets/` and copied into
  the workspace by the scaffold. The engine **embeds ABC Diatype into the PDF**
  (`.woff2`), so the output is in the real brand face on any machine — verified with
  `pdffonts` (the PDF contains `ABCDiatype-Regular`, no Helvetica/Arial). No font
  install is needed to produce an on-brand PDF.

## Workflow

### 1. Scaffold a build workspace

Pick a working directory (in the user's project, or a fresh folder). Run the
bundled scaffold, which copies the render engine here plus the brand assets from
`../ode-brand/`:

```bash
bash <skill-dir>/assets/scaffold.sh <target-dir> <doc-name>
cd <target-dir> && npm install
```

`<skill-dir>` is this skill's directory. The workspace ends up with `tokens.css`,
`components.css`, `build.mjs`, `watch.mjs`, `paginate.js`, `package.json`, `fonts/`,
`logos/`, an `assets/` folder for per-doc images, and a starter `<doc-name>.html`.
`npm install` is needed once per workspace. (If the brand fonts/logos aren't
present, the scaffold prints a note and continues; the doc still builds.)

### 2. Author the document

Edit `<doc-name>.html` (the scaffold created this starter — edit it in place; if you
author by overwriting it wholesale, Read it once first). Each physical PDF page is
one `<section class="page">` (or `.page--bleed` for full-bleed cover/divider pages).
Build the content from the component library — do not invent ad-hoc styles or inline
hex values.

- **Read `../ode-brand/reference/design-principles.md`** for the polish bar
  (whitespace as a feature, one idea per page, hierarchy, alignment, restraint).
  This is what separates a passable doc from a premium one.
- **Read `reference/components.md`** for the full component catalog (cover, divider,
  section header, cards, stat strips, roadmaps, callouts, tables, TOC, team rows,
  and more) with the markup for each.
- **Read `reference/authoring.md`** for page structure, the runner header/footer
  pattern, the self-numbering rules, handling content that doesn't fit, and the
  edit→render→screenshot iteration loop.
- Pull every color/font from the tokens (`var(--tomato)` etc.). If a value you need
  isn't a token, add it to `tokens.css` (sourced from the Brand Hub), don't hardcode
  it.
- Prose follows the Ode voice (`../ode-brand/reference/voice.md`): US English, no
  em-dashes, titles label rather than pitch, no AI-writing tells.

### 3. Render

```bash
cd <target-dir> && node build.mjs <doc-name>.html
```

Produces `output-<doc-name>.pdf`. For continuous rebuilds during editing, run
`node watch.mjs <doc-name>.html` in a spare terminal and wait for each
`[watch] ... done` before reopening the PDF.

### 4. Screenshot and review — always

Rendering is not the same as reviewing. After any visual change, rasterize the pages
and **look at them**:

```bash
pdftoppm -png -r 140 output-<doc-name>.pdf /tmp/page
```

Read the PNGs. Check every page for: content overflowing under the runners, clipped
or missing content, off-brand color or type, broken alignment, widowed headings, and
redundant stacked hairlines. Fix in CSS when an issue affects more than one place;
use per-element inline overrides only as a last resort. Repeat until every page meets
the bar. The detailed loop is in `reference/authoring.md`.

## Scope boundaries

- Author content and components; keep the engine files (`build.mjs`, `paginate.js`,
  `package.json`) untouched unless the user asks to change build behavior.
- Never hand-type page numbers — `paginate.js` computes them. A contents entry
  rendering as `??` means a TOC anchor's target `id` is missing; fix the anchor,
  don't paper over it. See `reference/authoring.md`.
- Don't edit the shared brand foundation casually. A genuine brand fix belongs in
  `ode-brand/assets/tokens.css` (it propagates to every medium), not in a one-off
  override here.
- If a build errors, surface the error verbatim and stop; don't silently skip it.
