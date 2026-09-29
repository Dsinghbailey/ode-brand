# Deck API reference

`ode_deck.py` exposes one class, `Deck`. Construct it, call slide-type methods in
the order you want slides to appear, then `save()`. All color and type come from
the brand tokens — you don't pass colors or fonts.

```python
from ode_deck import Deck
d = Deck(brand_dir="brand")   # folder with tokens.json, logos/, backgrounds/
...
d.save("deck.pptx")
```

Canvas is 16:9 (13.333 × 7.5 in). Slides render in both PowerPoint and Google
Slides (import the .pptx into Slides).

## Slide types

### `add_cover(title, subtitle=None, eyebrow=None, date=None)`
Full-bleed warm-dark ground (`backgrounds/cover.png`, or a solid Bistre fallback)
cover with the light logo, an optional uppercase eyebrow, a large ABC Diatype
title, an optional subtitle, and a footer with "Prepared by Ode with Anthropic" and
the date.

### `add_section(number, title, synopsis=None)`
Warm-dark divider (`backgrounds/divider.png`) with a giant ghosted numeral, a
"Section NN" label, the title, and an optional synopsis.

### `add_content(title, bullets=None, eyebrow=None, body=None)`
Light (Bone) content slide: optional tomato eyebrow with accent tick, a Bistre
title, an optional lead `body` paragraph, and an optional `bullets` list (square
markers, generous row spacing, measure capped for readability). The text fallback.
**Prefer `add_cards` / `add_bars` when the content has structure** — a plain bullet
list is the least visual option.

### `add_cards(title, cards, eyebrow=None)`
A grid of accent-topped cards — the scannable, visual alternative to bullets.
`cards` is a list of dicts: `{"num": "EUR 200M", "title": "New sectors", "body":
"..."}` (`num` optional). Lays out one row for ≤3 cards, 2×2 for 4, three columns
for 5–6. Accent color cycles tomato → blue-gray → teal. Great for a set of levers,
workstreams, or differentiators.

### `add_bars(title, items, eyebrow=None, note=None)`
A horizontal bar chart, bars scaled to the largest value — the right way to show a
value or EV breakdown. `items` is a list of `(label, number, value_text)`, e.g.
`("New sectors", 200, "EUR 200M")`. Pass them pre-sorted for a ranking. Optional
`note` prints a caption under the chart.

### `add_roadmap(title, phases, eyebrow=None)`
A horizontal phased timeline: a track with nodes and a column per phase. `phases`
is a list of `{"name", "when", "body"}`. Best with 3–5 phases; keep `name` to one
or two words. The delivery-plan slide.

### `add_stats(stats, title=None, eyebrow=None)`
A row of up to four number-led stats between two rules. `stats` is a list of
`(value, label)` tuples, e.g. `[("40%", "A metric"), ("3x", "A multiplier")]`.
Caps at four columns (more would crowd). **With five or more figures**, pick the
four that carry the story and put the rest in a following `add_statement` (e.g. a
total), or split across two stat slides. Don't try to force five into the row.

### `add_two_column(title, left_title, left_body, right_title, right_body)`
Two accent-barred columns (tomato left, teal right) under a title — good for
comparisons ("what changes / what stays").

### `add_statement(text, label=None)`
A marquee statement, centered between top and bottom rules, with an optional tomato
uppercase label. The deck equivalent of the document `.thesis`.

### `add_closing(title, subtitle=None)`
Full-bleed warm-dark ground (`backgrounds/brand.png`) closing slide with the light
logo, a title, and an optional subtitle.

### `save(path)`
Writes the `.pptx` and returns the path.

## Extending

To add a slide type, write a new method on `Deck` that composes the low-level
helpers, reading brand colors from `self.BISTRE / BONE / WHITE / TOMATO / BLUEGRAY /
TEAL` and fonts from `self.DISPLAY` (ABC Diatype) / `self.BODY` (ABC Diatype):

- `self._slide()` — add a blank slide.
- `self._bg_solid(slide, color)` / `self._bg_image(slide, name, fallback)` —
  background fill or a full-bleed PNG from `brand/backgrounds/<name>.png`.
- `self._logo(slide, "light"|"dark", left, top, height)`.
- `self._text(slide, left, top, w, h, runs, align, anchor)` — `runs` is a list of
  paragraphs; each paragraph is a list of `(text, opts)`. `opts` keys: `font`,
  `size` (pt), `color` (an RGBColor like `self.TOMATO`), `bold`, `italic`, `caps`,
  `tracking` (letter-spacing in 1/100 pt, for caps labels), `space_after` (pt),
  `line_spacing`.
- `self._rule(...)` / `self._accent_bar(...)` — hairline rule / colored bar.

Use `Inches(...)` and `Pt(...)` from `pptx.util`.

## Brand-fidelity notes

- **Fonts.** The deck's runs **and its theme** are set to ABC Diatype (so typed-in
  text is on-brand too); `_retheme_fonts()` rewrites the theme's major/minor Latin
  font on save. python-pptx cannot embed font files, and **ABC Diatype is a
  commercial Dinamo font, NOT a Google Font**, so the real face shows only where the
  font is present: install `brand/fonts/ABCDiatype-Regular.otf` for PowerPoint /
  Keynote (or embed via File > Options/Preferences > Save > Embed fonts, PowerPoint
  2021/2024/365). **Google Slides substitutes it regardless** — a Google platform
  limit. For guaranteed ABC Diatype fidelity use `ode-pdf` (it embeds the font). See
  the SKILL "Fonts and fidelity" and `../ode-brand/assets/fonts/README.md`.
- **Grounds.** Covers/dividers/closings use pre-rendered brand background PNGs
  rather than live gradients (python-pptx gradient support is limited). Ode's
  grounds are near-solid warm darks (Bistre→Cola), not mesh gradients. Regenerate
  them with `gen-backgrounds.mjs` in `ode-brand` if the `--grad-*` tokens change; if
  the PNGs are absent, cover/section/closing slides fall back to a solid Bistre
  ground.
- **Letter-spacing** on uppercase labels is set via the `spc` XML attribute (no
  python-pptx API); other tracking is left at the font default.
- **Editing after generation.** The output is fully editable; expect a human to
  fine-tune spacing in PowerPoint/Slides. If you need a fixed, print-perfect
  artifact, use `ode-pdf` (HTML→PDF) instead.

## Reviewing a deck

`lint_deck.py` (run automatically by `review.sh`) is a renderer-free check: shapes
off the 16:9 canvas, off-palette colors, non-brand fonts. It does **not** see text
overflowing its own box or contrast problems on the dark grounds — those need a
render. `review.sh` produces per-slide PNGs via LibreOffice when it is installed;
otherwise open the deck in PowerPoint/Google Slides. Build → review → fix until each
slide holds up.

## Slide polish

Apply the shared `../ode-brand/reference/design-principles.md` (whitespace, one idea
per unit, hierarchy, alignment, restraint). Slide-specific specifics:

- **One message per slide.** The title states the takeaway as a label; the body
  supports it. If a slide makes two points, split it.
- **Don't crowd the canvas.** 3–5 short bullets max per `add_content`; trailing
  whitespace at the bottom reads as confident, not empty. Long paragraphs belong in
  the PDF, not on a slide.
- **Contrast follows the ground.** Light text only on the dark-ground slides
  (cover/section/closing); Bistre text on the Bone content slides. The helper
  enforces this — don't override it.
- **One component per slide.** Stats *or* bullets *or* two columns, not all stacked.
  Reach for the slide type that fits the one idea.
- **Consistent entry points.** Content titles start at the same top position across
  slides; let the helper place them rather than nudging per slide.
- **Keep numbers to four.** See `add_stats` above for the 5+ case.
