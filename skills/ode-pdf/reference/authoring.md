# Authoring a Ode document

How the document is structured, numbered, and iterated. Read alongside
`components.md` (the component markup).

## One section per page

The document is one HTML file. Each physical PDF page is a top-level
`<section class="page">`. Page geometry is fixed (8.5×11in via `@page`, per-section
fixed height with `overflow: hidden`), so content **cannot silently leak across a
page boundary** — it clips at the edge instead. That makes the layout
deterministic: what you place on a page stays on that page.

If you genuinely need natural flow across pages, that is the one place to break
the convention — but prefer splitting content into explicit pages.

## Page numbers are generated, not authored

`paginate.js` computes every number at load time from each page's DOM position.
`build.mjs` waits for the `data-paginated` flag before printing, so a normal build
already has correct numbers.

- Leave `.runner__page` slots **empty** — the script stamps the page's 1-based
  ordinal (zero-padded).
- Leave `.toc__page` slots **empty** — the script fills each from the page its
  TOC anchor (`href="#id"`) points to.
- A contents page rendering as `??` means the anchor's target `id` is missing or
  misspelled. Fix the `id`; never hand-type the number.

What is **not** generated, and is authored by hand: the TOC section identifiers
(`.toc__num`, e.g. "01" or "3.1") and the runner section labels (e.g.
"01 First Section"). Adding or removing a page shifts page numbers automatically,
but you must update these hand-authored section labels yourself.

## Adding a page

Copy an existing content page's `<section class="page">`, keep the runner blocks
(with empty `.runner__page` slots), update the hand-authored section label, and
add a TOC entry whose `href` points to the new page's `id` if it should appear in
contents. Page numbers re-flow on the next build.

## When content doesn't fit a page

In order of preference:

1. **Tighten.** Drop a redundant paragraph, trim a callout, or use a `--compact`
   modifier (`.section__header--compact`, `.thesis--compact`,
   `.numlist--compact`).
2. **Split across pages.** Put a logical break, even mid-point in a numbered list.
   Label the continuation (e.g. a callout "Operating precedent (cont.)") so the
   reader knows it carries over.
3. **Shrink type — last resort.** `.section__title--md` (22pt), or an inline
   `style="font-size: …"` on the specific block. Never globally reduce body type
   below 10pt.

### When content overflows under a runner
Caused by content exceeding the fixed `.page` height. Fix in order: tighten a
paragraph/callout → reduce the component's vertical padding/gap → lower the local
font-size of the offending block → move the block to a continuation page.

## The iteration loop

Rendering is not reviewing. After every visual change:

1. **Edit** the HTML and/or `components.css`. If running `watch.mjs`, wait for
   `[watch] ... done`; otherwise run `node build.mjs <doc>.html`.
2. **Rasterize the affected pages** and actually look at them:
   ```bash
   pdftoppm -png -r 140 -f 4 -l 6 output-<doc>.pdf /tmp/page
   ```
   `-f N -l M` selects pages N–M; `-r 140` is good for layout review, bump to 180
   to inspect type.
3. **Read every screenshot.** Check for: content overflow into runners, clipped or
   missing content, off-brand color or type, broken alignment, widow/orphan
   headings, redundant stacked hairlines.
4. **Fix in CSS first** when an issue affects more than one place. Reach for
   per-page inline `style="..."` only as a last resort.
5. Repeat until every page meets the bar.

> The `pdftoppm` filename suffix is the rendered page index, not the printed
> runner number. After inserting/removing pages, `page-16.png` may show a runner
> that reads "14". Cross-check both.

## Where to put a brand fix vs a doc fix

- A value or rule that should hold across **all** Ode media → fix it in
  `../ode-brand/assets/tokens.css` (and `tokens.json`). It propagates.
- A layout concern specific to **this document** → fix it in the workspace
  `components.css` or the page HTML.
- A new reusable component → add it to `components.css` and document it in
  `components.md`, not as a one-off inline style.

## Gotchas

- **`mix-blend-mode: multiply`** prints correctly in Chromium (used to drop white
  backgrounds from signature PNGs onto the page). If a signature shows as a white
  box, that rule was lost.
- **`:has()`** is used in the rule-collapse block and is supported by the
  Puppeteer Chromium. Don't replace it with JS.
- **ABC Diatype is bundled and embeds into the PDF.** The `@font-face` rules in
  `tokens.css` load the `.woff2` from `fonts/` (Regular + Semi Mono); `build.mjs`
  waits on `document.fonts.ready` and Chromium embeds the face into the output.
  Confirm with `pdffonts output-<doc>.pdf` — you should see `ABCDiatype-Regular`
  (embedded) and **no** Helvetica/Arial. If you see a fallback, the `fonts/` copies
  or the `@font-face` paths are wrong. These are licensed commercial fonts — see
  `../ode-brand/assets/fonts/README.md`.
- **`pdftoppm` prints `Syntax Warning: Bad bounding box in Type 3 glyph` lines** —
  expected and harmless. Chromium embeds the fonts as Type 3 glyph outlines; the
  pages rasterize correctly. Don't chase these warnings.

## Design polish

The shared `../ode-brand/reference/design-principles.md` carries the
cross-cutting rules (whitespace as a feature, one idea per page, hierarchy,
alignment, restraint, vertical rhythm) — read it. PDF-specific specifics:

- **Aim for ~70–80% page fill.** A content page packed to the runner reads as
  dense; trailing whitespace at the bottom is fine and looks intentional. If a
  page is overfull, split it (see "When content doesn't fit") rather than shrinking
  type or padding.
- **One section per page where you can.** Let dividers and covers breathe; don't
  append stray content to a divider page.
- **No orphaned headings.** A `.subhead` or `.section__header` must not sit at the
  bottom of a page with its content pushed to the next. Move the heading down with
  its body.
- **Lean on the spacers and `--compact` modifiers** (`.spacer-md`,
  `.section__header--compact`, `.thesis--compact`, `.numlist--compact`) for
  consistent rhythm instead of hand-tuning gaps per page.
- **Let the rule-collapse do its job.** Don't add a manual rule above a list that
  already follows a `.subhead`; stacked hairlines read as clutter.
- **Keep one accent per page.** Card top-accents, eyebrows, and callout borders all
  pull color; if a page has three accent colors competing, pick one.
- **Tables and stat strips breathe.** Don't fill every column; 3–4 stats land
  better than 5–6 crammed. Numbers are tabular and right-weighted.
