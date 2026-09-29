# Ode with Anthropic brand — full reference

Distilled from the Ode Brand Hub (Notion "Ode with Anthropic – Brand Hub" plus the
linked design-guideline, logo, and verbal-identity PDFs). Load this when SKILL.md's
summary isn't enough — fine-grained color, type, and logo detail.

## Color system

### The two foundations
The brand is warm and monochrome-first. Every layout starts as either:
- **Light mode** — Bone `#FBFBF8` ground, Bistre text.
- **Dark mode** — Bistre `#201D1C` (or warm Cola `#3C2E2A`) ground, Bone text.

Pick one foundation per surface, then add brand color with intent.

### Brand color, exact values
| Name | Hex | RGB | Role |
|---|---|---|---|
| Bone | `#FBFBF8` | 251, 251, 248 | Foundation light |
| Bistre | `#201D1C` | 32, 29, 28 | Foundation dark, primary text |
| Cola | `#3C2E2A` | 60, 46, 42 | Warm secondary dark, grounds/panels |
| Dove | `#625855` | 98, 88, 85 | Warm gray, muted / secondary text |
| Slate | `#D9D9D9` | 217, 217, 217 | Light gray, dividers, fills |
| Tomato | `#CD3E1D` | 205, 62, 29 | Primary accent, emphasis, links |
| Blue Gray | `#728FA8` | 114, 143, 168 | Secondary, supporting UI |
| Teal | `#5EA6B1` | 94, 166, 177 | Expressive accent (labeled "Pale Gray" in the hub) |
| Tea | `#E8EBD7` | 232, 235, 215 | Pale green tint, soft panels |
| Lilac | `#F4DCEA` | 244, 220, 234 | Pale pink tint, soft panels |

> Note on names: the Brand Hub color table labels `#5EA6B1` "Pale Gray" even though
> it reads teal, and `#D9D9D9` "Slate." The token names here follow how the colors
> actually read (`--teal`, `--slate`) so downstream use isn't confusing; the hex
> values are authoritative and unchanged.

### Do / don't (from the hub)
- Use only the approved palette. **Do not** adjust hue, saturation, or brightness of
  a brand color, and **do not** introduce unapproved colors.
- Tomato is a loud red-orange. Use it as the single accent that earns attention on a
  unit (a rule, a key figure, a link) — not as a large fill.
- Tea and Lilac are soft tints for panels/cards/highlights, not text colors.
- Dove is the muted/secondary text color on Bone; the `--bistre-*` opacity ramp
  covers the rest of the text hierarchy and hairlines.

### Shades
Use 100/80/60/40/20% of Bistre and the accents for sub-elements (hairlines, fills,
muted text). Bistre at reduced opacity is the workhorse for text hierarchy and
rules — see the `--bistre-*` ramp in `tokens.css`.

## Grounds (not gradients)

Ode's identity is flat and editorial: the Brand Hub defines **no mesh gradients**.
Covers, dividers, and hero panels use solid warm-dark grounds (Bistre, or Cola for
a warmer feel) with a single restrained accent, rather than sweeping color washes.
The `--grad-*` tokens in `tokens.css` are therefore near-solid Bistre→Cola blends
with, at most, a faint Tomato/Teal hotspot — deliberately understated. The rendered
PNGs in `assets/backgrounds/` come from these tokens via `gen-backgrounds.mjs`.
Keep dark grounds dark enough to carry Bone/white text.

## Typography

- **ABC Diatype** (Dinamo) is the primary typeface, used for display **and** body —
  the hub uses one family across the whole hierarchy (display, headers, body).
- **ABC Diatype Semi Mono** is the accent/texture face: eyebrows, all-caps labels,
  tabular figures, code-like detail. Exposed as `--font-mono`.
- **Styrene** is the secondary typeface (`--font-secondary`).
- **Fallback: Helvetica Neue.** The hub names it explicitly as what to use on Google
  and anywhere the licensed fonts aren't available. Keep the fallback stack
  (`'ABC Diatype', 'Helvetica Neue', Arial, sans-serif`) in the font variables.
- **Tracking**: display/headings ≈ -2%; body ≈ -1%. All-caps labels/eyebrows use
  positive tracking.
- **Numerals**: tabular (`font-variant-numeric: tabular-nums` /
  `font-feature-settings: 'tnum'`).

### Marketing type scale (reference)
H1 56/64 · H2 40/48 · H3 36/42 · H4 28/36 · Subhead 24/32 · Body 16/22. These are
marketing sizes; dense print and slide media set their own smaller scales while
matching family/weight/tracking.

### Fonts
All three faces are **bundled** in `assets/fonts/` as `.otf` + `.woff2` and wired
into the `@font-face` rules: ABC Diatype Regular (display/body), ABC Diatype Semi
Mono (accent/labels), and Styrene A Medium (secondary). `ode-pdf` embeds all three
into the PDF (verified with `pdffonts`: the output contains `ABCDiatype-Regular`,
`ABCDiatypeSemiMono-Regular`, `StyreneAWeb-Medium`, and no Helvetica/Arial). These
are licensed commercial fonts (Dinamo EULA) — see `assets/fonts/README.md`. Only
single weights are provided (Diatype Regular, Styrene Medium); heavier weights are
synthesized. Helvetica Neue stays in the stack only as a last-resort safety net,
never the intended face.

## Logo

Ode's lockups, in order of default preference:

- **Full lockup, "with Anthropic" endorsement** (`logo-{light,dark}`): the default
  signature — the logo mark + "Ode" + the "with Anthropic" endorsement. Use by
  default.
- **Lockup, no endorsement** (`lockup-{light,dark}`): mark + "Ode" only. Use
  sparingly, or when the un-endorsed lockup is explicitly requested.
- **Graphic mark / symbol** (`mark-{light,dark}`, plus a full-color variant): the
  symbol alone — favicons, small corners, the LinkedIn/social avatar.
- **Wordmark** (`wordmark-{light,dark}`): the "Ode" name alone. Rarely needed.

Rules:
- Light logo on dark/ground surfaces, dark logo on light. Never dark-on-dark.
- SVG for vector contexts (web, print, the HTML→PDF engine); PNG for raster
  contexts (pptx, raster app assets).
- Maintain clear space; never recolor, stretch, or restyle the logo.
- Over photographs or busy grounds, use the light logo and confirm legibility.
- The logo files are **bundled** in `assets/logos/` — every lockup as SVG (used by
  `ode-pdf`) and transparent high-res PNG (used by `ode-slides`). See
  `assets/logos/README.md`.

## Putting it together
- Start monochrome (one foundation), then add brand color deliberately (usually a
  single Tomato hit per unit).
- Pull every value from `tokens.css` / `tokens.json`. Add to the tokens rather than
  inlining a new value.
- When in doubt, the Ode Brand Hub is the final authority; this file is a faithful
  distillation, not a substitute. The design system is still evolving — flag
  anything you had to invent.
