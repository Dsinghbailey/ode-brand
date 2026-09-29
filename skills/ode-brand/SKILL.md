---
name: ode-brand
description: |
  The Ode with Anthropic brand foundation — palette, typography, logo usage,
  voice, and the brand asset files (fonts, logos, color tokens). Use this
  whenever an artifact needs to be on-brand, or when another skill needs the raw
  assets: "what are our brand colors", "use the Ode palette", "which logo goes on
  a dark background", "make this on-brand", or when building an Ode doc, deck, or
  app UI. This is the shared layer the ode-pdf and ode-slides skills build on.
  (Ode is the new name for the team formerly branded Fractional AI.)
license: UNLICENSED
compatibility: claude-code
tags:
  Function: [Brand & Design]
---

# Ode with Anthropic — Brand Foundation

This skill is the single source of truth for the Ode with Anthropic visual brand.
It holds the brand rules **and** the asset files. The doc, slide, and app-UI
skills all draw from here, so the brand stays consistent across every medium.

The authority is the **Ode Brand Hub** (the internal Notion "Ode with Anthropic –
Brand Hub" and the design-guideline / logo / verbal-identity PDFs it links). The
load-bearing rules are distilled below and in `reference/`. When a downstream
stylesheet or theme conflicts with these rules, the Brand Hub wins.

> **Assets bundled.** The **logo files** (SVG + high-res transparent PNG, all
> lockups) and the **fonts** — ABC Diatype Regular, ABC Diatype Semi Mono, and
> Styrene A Medium, each as `.otf` + `.woff2` — are committed under `assets/`. The
> `ode-pdf` engine embeds all three into the PDF (verified: the rendered PDF
> contains `ABCDiatype-Regular`, `ABCDiatypeSemiMono-Regular`, and
> `StyreneAWeb-Medium`, with no Helvetica/Arial fallback). One caveat, stated
> plainly: **`.pptx` decks render the real font only where ABC Diatype is
> installed/embedded — Google Slides substitutes it, because it isn't a Google
> Font** (a Google platform limit, not ours; use `ode-pdf` when exact fidelity is
> required). Fonts are provided as single weights (Diatype Regular, Styrene Medium);
> heavier weights are synthesized. The Ode design system is still evolving; prefer
> the tokens here and flag anything you had to invent.

## When to use this skill

- Any time you produce or polish an Ode-branded artifact and need the correct
  color, type, or logo.
- When a consumer skill (`ode-pdf`, `ode-slides`, a future app-UI skill) needs the
  raw assets — point those skills at the files under `assets/`.
- Quick brand lookups ("what's our accent color", "which font for headers").

## The assets (under `assets/`)

| File | What it is |
|---|---|
| `tokens.css` | `@font-face` + `:root` CSS variables. Every CSS-based medium imports this. |
| `tokens.json` | The same tokens, machine-readable, for programmatic consumers (pptx, app UIs). |
| `fonts/` | ABC Diatype Regular, ABC Diatype Semi Mono, and Styrene A Medium — each as `.otf` (desktop/embedding) and `.woff2` (web/PDF engine), wired into `tokens.css` `@font-face`. See `fonts/README.md`. |
| `logos/` | Every lockup as **SVG** (vector, used by `ode-pdf`) **and** transparent high-res **PNG** (used by `ode-slides`): `logo`, `lockup`, `mark`, `wordmark`, each in `-light` (Bone) and `-dark` (Cola). See `logos/README.md`. |
| `backgrounds/` | Pre-rendered 16:9 brand grounds for media without live CSS (e.g. slides). Generate with `gen-backgrounds.mjs`. |
| `gen-backgrounds.mjs` | Regenerates the background PNGs from the `--grad-*` tokens; run only when they change. |

**Never hardcode a hex value or font name** in a downstream artifact. Reference a
`tokens.css` variable (`var(--tomato)`) or read `tokens.json`. If a value you need
is missing, add it to the token files (sourced from the Brand Hub), don't inline a
raw value.

## Color — warm, editorial, restrained

The brand reads as light mode (Bone `#FBFBF8`) or dark mode (Bistre `#201D1C`);
either also serves as the primary text color over the opposite ground. It is a
warm, earthy, editorial palette — restrained by default, with color used
deliberately.

| Token | Hex | Role |
|---|---|---|
| Bistre | `#201D1C` | Foundation dark / primary text |
| Bone | `#FBFBF8` | Foundation light |
| Cola | `#3C2E2A` | Warm secondary dark (grounds, panels) |
| Dove | `#625855` | Warm gray, muted / secondary text |
| Slate | `#D9D9D9` | Light gray, dividers, fills |
| Tomato | `#CD3E1D` | Primary accent (links, emphasis, one strong hit) |
| Blue Gray | `#728FA8` | Secondary, supporting UI |
| Teal | `#5EA6B1` | Expressive accent (listed as "Pale Gray" in the hub) |
| Tea | `#E8EBD7` | Pale green tint (soft panels) |
| Lilac | `#F4DCEA` | Pale pink tint (soft panels) |

Shades at 100/80/60/40/20% of Bistre and the accents may be used for sub-elements;
the `--bistre-*` opacity ramp in `tokens.css` is the workhorse for text hierarchy
and hairlines. Tomato is a loud red-orange — treat it as the single accent that
earns attention on a unit, not a fill. Full detail in
`reference/brand-guidelines.md`.

## Typography

- **ABC Diatype** for display **and** body (the Brand Hub uses one family across
  the hierarchy). **ABC Diatype Semi Mono** (`--font-mono`) is the accent/texture
  face for eyebrows, labels, and figures. **Styrene** (`--font-secondary`) is the
  secondary typeface.
- **Helvetica Neue is the sanctioned fallback** — the Brand Hub names it explicitly
  for Google/where the licensed fonts aren't available. Keep the fallback stack
  (`'ABC Diatype', 'Helvetica Neue', Arial, sans-serif`); don't strip it.
- Display and headings carry slight negative letter-spacing (about -2%); numerals
  use tabular figures.
- The marketing type scale (H1 56/64, H2 40/48, etc.) is in `tokens.json`; dense
  print sets its own smaller sizes. Match families, weights, and tracking rather
  than fixed point sizes.

## Logo

Ode has several lockups (all under `logos/`, see `logos/README.md`):

- **Full lockup with "with Anthropic" endorsement** (`logo-{light,dark}`): the
  default brand signature — use this unless told otherwise.
- **Lockup, no endorsement** (`lockup-{light,dark}`): mark + "Ode" only. Use
  sparingly, or when the un-endorsed lockup is explicitly requested.
- **Graphic mark / symbol** (`mark-{light,dark}`): the symbol alone (favicons,
  small corners, LinkedIn avatar). Use sparingly.
- **Wordmark** (`wordmark-{light,dark}`): the "Ode" name alone. Rarely needed.

Light logo on dark/gradient grounds, dark logo on light grounds. SVG for
vector/web/print; PNG for raster contexts (pptx). Keep clear space; never recolor,
stretch, or place a dark logo on a dark ground.

## Voice (external prose)

Ode's voice stays constant; tone shifts by context. Four attributes: **Ambitious,
Exacting, Kinetic, Grounded**. On top of that sit the writing-hygiene rules (US
English, no em-dashes, titles that label rather than pitch, no AI-writing tells).
The full rules, boilerplates, and approved headlines are in `reference/voice.md`.

## Design principles (polish)

Beyond color and type, the layout itself carries the brand. `reference/
design-principles.md` holds the cross-cutting rules that make any artifact read as
premium: whitespace as a feature, one idea per unit, hierarchy through scale not
decoration, a single alignment grid, restraint with color and rules, and vertical
rhythm. Every consumer skill (PDF, slides, app UI) should apply these.

## Handing off to consumer skills

When `ode-pdf` or `ode-slides` runs, it pulls these assets into its build
workspace (fonts, logos, tokens) rather than restyling from scratch. Those skills
locate this one as a sibling at `../ode-brand/`. If you add a new medium, consume
`assets/tokens.{css,json}` and the fonts/logos here — don't fork the palette.
