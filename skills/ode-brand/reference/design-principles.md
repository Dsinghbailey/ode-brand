# Ode with Anthropic — design principles (polish)

Cross-cutting layout principles that make any Ode artifact (PDF, deck, app UI) read
as considered and premium rather than busy. These are medium-agnostic; each
consumer skill adds its own specifics (see `ode-pdf/reference/authoring.md` and
`ode-slides/reference/deck-api.md`). When a layout feels off, it is almost always
one of the items below.

## 1. Whitespace is a feature, not leftover space

- **Don't fill to the edges.** A page or slide that sits around 70–80% full reads
  as more premium than one packed to the margin. Trailing whitespace at the bottom
  is intentional, not a gap to fill.
- **Prefer splitting over cramming.** If content is tight, move a block to a second
  page/slide or cut it. Shrinking type or padding to force a fit is the last
  resort, and usually visible.
- **Give marquee elements room.** Covers, dividers, big stats, and pull quotes earn
  their weight from the space around them. Crowding them kills the effect.
- **Generous, consistent outer margins.** Keep the page/slide padding uniform; do
  not let one element creep into the margin to buy space.

## 2. One idea per unit

- One page or slide carries one idea; one section carries one argument. If you are
  describing two unrelated things, that is two units.
- Lead with the conclusion in the first line (the lede or the title-as-label), then
  support it. The reader should get the point before the detail.

## 3. Visual hierarchy through scale and weight, not decoration

- Establish a clear order: eyebrow → title → lede → body → caption. Each step is
  visibly different in size or weight, and you only use the steps the design
  already defines. Do not invent new sizes.
- Make the most important thing the largest or boldest thing on the unit, and make
  sure there is exactly one of those.
- Never use color or bold to create emphasis that hierarchy should carry. Bold is
  for the occasional load-bearing phrase, not for scanning.

## 4. Alignment and a single grid

- Everything hangs off the same left edge unless it is deliberately centered
  (centering is for display covers/dividers, not body content).
- Align like with like across columns: card tops, stat baselines, and multi-column
  rows should sit on shared baselines. Ragged columns read as broken.
- Numerals are tabular so figures line up in columns and stat strips.

## 5. Restraint with color and rules

- Monochrome-first: start from one ground (Bone light or Bistre dark) and add brand
  color with intent. Tomato is the default accent; Blue Gray and Teal are secondary
  and expressive; Tea and Lilac are soft tints, not accents. See [[ode-brand]]
  tokens.
- One accent doing one job per unit. Color used everywhere stops meaning anything.
- Don't stack hairline rules. A rule separates groups that space alone cannot;
  if a subhead already introduces a list, the list doesn't also need a top rule.
- Reserve the dark grounds for the brand moments (covers, dividers, hero panels),
  not for ordinary content backgrounds. Ode uses solid warm-dark grounds, not
  sweeping gradients.

## 6. Vertical rhythm and grouping

- Use consistent spacing between components rather than hand-tuned one-off gaps.
  Related items sit closer together; unrelated groups are separated by more space
  (proximity groups; space separates).
- Don't let a heading sit alone at the bottom of a page/slide (orphan) or a single
  trailing line spill to the next (widow). Keep a heading with its content.

## 7. Type discipline

- One primary family: ABC Diatype across display and body. Semi Mono is for
  eyebrows/labels/figures and Styrene is the secondary face; no unapproved typeface.
- Display and headings carry tight tracking; uppercase labels carry open tracking.
- Don't center long text; left-align body. Keep line length readable (roughly
  60–80 characters); very wide measures tire the eye.

## The quick polish pass

Before calling an artifact done, scan for:
- Is anything crammed edge-to-edge that should breathe? (whitespace)
- Is there one clear focal point per unit? (hierarchy)
- Do columns and left edges line up? (alignment)
- More than one accent color fighting for attention, or stacked rules? (restraint)
- A lone heading at a page/slide boundary? (widows/orphans)
- Consistent spacing, or random gaps? (rhythm)

Fixing these is usually the difference between "fine" and "polished."
