---
name: ode-slides
description: |
  Generate an on-brand Ode with Anthropic slide deck as an editable .pptx that
  opens in both PowerPoint and Google Slides. Builds 16:9 slides with the Ode
  palette, fonts, logos, and warm-dark ground backgrounds via a brand-themed
  python-pptx helper. Use when the user says "make an Ode deck / slides /
  presentation", "build a pitch deck", "turn this into slides", or wants an
  editable branded presentation. Builds on the ode-brand foundation. For
  print-quality PDFs use ode-pdf instead. (Ode is the new name for the team
  formerly branded Fractional AI.)
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

# Ode with Anthropic — Slide Decks (.pptx)

Produce an editable, on-brand slide deck. Slides are authored in Python with a
brand-themed `python-pptx` helper and saved as a 16:9 `.pptx` that opens cleanly in
**PowerPoint and Google Slides** (import the .pptx into Google Slides).

This skill builds on **`ode-brand`**, which supplies the palette, fonts, PNG logos,
and ground backgrounds. For print-quality PDF documents (proposals, reports), use
**`ode-pdf`** instead.

## When to use

- "Make an Ode deck / pitch deck / presentation / slides."
- "Turn this content into slides."
- Any editable, brand-consistent presentation.

## Why editable .pptx (and the fidelity tradeoff)

This skill generates native `.pptx` rather than a rendered deck, so the output is
editable in PowerPoint or Google Slides. That keeps slides editable but means less
pixel control than the HTML/PDF engine: grounds come in as pre-rendered background
images, and font rendering depends on the opener (see "Fonts and fidelity" below —
ABC Diatype is commercial and not a Google Font, so Google Slides substitutes it and
PowerPoint needs it installed/embedded). If the goal is a fixed, brand-perfect
artifact rather than an editable file, prefer `ode-pdf`, which embeds the real font.

## Prerequisites

- **Required:** Python 3 with `python-pptx` (`pip install python-pptx`).
- **Optional, for visual review:** a slide renderer. `review.sh` tries, in order,
  **LibreOffice → Keynote → PowerPoint** to render the deck to per-slide PNGs (the
  docs-parity visual loop). On a typical Mac, Keynote is preinstalled, so this works
  with no install. If none is available, the build and linter still run and
  `review.sh` reports LINT-ONLY with an install hint
  (`brew install --cask libreoffice`). First use of Keynote/PowerPoint may prompt a
  one-time macOS automation-permission dialog.
- **For the ground covers/dividers:** the brand background PNGs must exist in
  `ode-brand/assets/backgrounds/`. If they don't yet, generate them once (needs Node
  + Puppeteer):
  ```bash
  cd <ode-brand-dir>/assets && npm i puppeteer && node gen-backgrounds.mjs
  ```
  Without them, cover/divider/closing slides fall back to a solid Bistre ground.
- **Fonts and logos are bundled** in `../ode-brand/assets/` and copied into the
  workspace `brand/` by the scaffold (logo PNGs, ground backgrounds, and the ABC
  Diatype `.otf`/`.woff2`). The deck and its theme are set to ABC Diatype. Rendering
  the real face depends on the opener — see "Fonts and fidelity" below.

## Workflow

### 1. Scaffold a build workspace

```bash
bash <skill-dir>/assets/scaffold.sh <target-dir>
cd <target-dir> && pip install python-pptx
```

This copies the deck helper (`ode_deck.py`), a starter `build_deck.py`, and the
brand assets into `<target-dir>/brand/` (tokens, PNG logos, ground backgrounds) — so
the workspace is self-contained.

### 2. Author the deck

Edit `build_deck.py` (the scaffold created this starter — edit it in place; if you
overwrite it wholesale, Read it once first). Construct a `Deck(brand_dir="brand")`
and call slide-type methods in order. **Read `reference/deck-api.md`** for every
slide type, its arguments, and the slide-polish section; and
**`../ode-brand/reference/design-principles.md`** for the polish bar (one idea per
slide, whitespace, restraint, contrast). The available types:

- `add_cover(title, subtitle, eyebrow, date)` — full-bleed warm-dark ground cover.
- `add_section(number, title, synopsis)` — warm-dark section divider.
- `add_cards(title, cards, eyebrow)` — grid of accent-topped cards (levers,
  workstreams) — the scannable, visual alternative to bullets.
- `add_bars(title, items, eyebrow, note)` — horizontal bar chart for a value / EV
  breakdown, bars scaled to the max.
- `add_roadmap(title, phases, eyebrow)` — horizontal phased timeline (delivery plan).
- `add_stats(stats, title)` — a row of up to four number-led stats.
- `add_two_column(title, left_title, left_body, right_title, right_body)` — a
  from/to comparison.
- `add_content(title, bullets, eyebrow, body)` — light text slide; the fallback when
  content has no structure. Prefer cards/bars/roadmap for impact.
- `add_statement(text, label)` — a marquee statement framed by rules.
- `add_closing(title, subtitle)` — warm-dark closing slide.

For content slides, reach for a **visual** type (cards, bars, roadmap, stats) before
a plain bullet list — a wall of bullets is the least engaging option and the most
common reason a deck reads as flat.

Keep content on-brand: the helper already enforces palette and type, so don't
override colors with raw values. Prose follows the Ode voice
(`../ode-brand/reference/voice.md`): US English, no em-dashes, titles label rather
than pitch. If you need a slide type the helper doesn't have, add a method to
`ode_deck.py` using the existing ones as a pattern (and reading the brand tokens),
rather than hand-placing off-brand shapes.

### 3. Build and review (self-correction loop)

```bash
python build_deck.py            # writes deck.pptx
bash review.sh deck.pptx        # lint, then render to PNGs if a renderer is present
```

`review.sh` is the slides equivalent of the PDF skill's screenshot loop. It always
runs `lint_deck.py` (a renderer-free check: shapes off the 16:9 canvas, off-palette
colors, non-brand fonts — exits non-zero on findings). Then it renders the deck to
`review/slide-*.png` via the first available of **LibreOffice → Keynote →
PowerPoint** so you can **look at every slide** for what a linter can't see: text
overflowing its box, contrast on the dark grounds, awkward wrapping. It ends with a
banner stating the **review level**:

- **`REVIEW LEVEL: VISUAL`** — slides were rendered; open every `review/slide-*.png`
  and actually look before calling it done. (A local renderer substitutes fonts, so
  type is approximate; layout is accurate.)
- **`REVIEW LEVEL: LINT-ONLY`** — no renderer was available; the deck passed
  structural checks but **was not seen**.

**Always tell the user which level you reached.** If you only got LINT-ONLY, say so
plainly: the deck is structurally sound but you have not visually verified polish —
recommend they open it in Google Slides / PowerPoint, or install a renderer
(`brew install --cask libreoffice`) and re-run. Don't imply a deck looks good when
you only linted it.

Fix linter findings before shipping, and iterate build → review until each slide
holds up.

## Fonts and fidelity

Colors, grounds, logos, and layout are baked into the file and render identically
everywhere. **Font rendering is the one thing that depends on the opener** — and
this is a genuine, unavoidable limitation, so state it to the user plainly rather
than implying the deck is pixel-perfect everywhere. `.pptx` references fonts by name
(python-pptx cannot embed font files), and **ABC Diatype is a commercial font, not a
Google Font**. Both the text runs and the deck's theme are set to ABC Diatype (so
even newly-typed text requests it), but whether the real face actually shows depends
on the opener:

- **PowerPoint / Keynote (desktop) — real face if the font is installed.** The
  scaffold bundles `brand/fonts/ABCDiatype-Regular.otf`; install it (open the
  `.otf`) and the deck renders in true ABC Diatype. You can also embed it into the
  file via PowerPoint > Preferences/Options > Save > "Embed fonts in the file"
  (2021/2024/365) so the deck travels self-contained. Without either, PowerPoint
  substitutes a system sans-serif.
- **Google Slides — substitutes, and there's no fix.** Google Slides only renders
  Google Fonts, so it swaps ABC Diatype for a sans-serif on import regardless of
  bundling or embedding. This is a Google platform limitation.

**For guaranteed ABC Diatype fidelity, use `ode-pdf`** — that engine embeds the real
font into the PDF, so it's correct on every machine and in every viewer. Reserve
`.pptx` for when the deck genuinely must stay editable, and tell the user up front
which opener will show the true face.

## Sharing to Google Slides

The local `.pptx` is always the guaranteed deliverable. It opens in Google Slides
directly (Drive > open with Google Slides, or Slides > File > Import slides),
converting to a native, editable deck (fonts substitute per "Fonts and fidelity").

Uploading to Drive is an optional convenience, never a requirement: **only if** a
Google Drive tool is connected in the session, you may offer to upload the `.pptx`
so the user gets a link instead of a local file (it lands in their authenticated
account). If no Drive tool is connected, hand off the local file and tell them how
to import it. There is no native Google Slides API generation here; the `.pptx` is
the artifact either way.

## Scope boundaries

- The helper owns brand styling; author content, not raw formatting. Extend the
  helper for new slide types rather than placing one-off off-brand shapes.
- A genuine brand change belongs in `ode-brand/assets/tokens.json` (it propagates to
  every medium), not as a local override here.
- Don't hand-edit colors to off-palette values. If a needed color isn't in the
  tokens, add it to the brand foundation.
