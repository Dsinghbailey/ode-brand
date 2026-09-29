# Component catalog

Every component is defined in `components.css`. Build pages from these; don't
invent ad-hoc styles. All color/type/gradient comes from `tokens.css`
(`var(--tomato)`, `var(--font-display)`, etc.). Class names below are the contract.

## Page containers

- `.page` — fixed 8.5×11in, padded, `overflow: hidden`, page-break-after. One per
  physical page. Content cannot leak across a boundary; it clips.
- `.page--bleed` — zero padding, for full-bleed cover/divider/back pages.

## Full-bleed brand pages

- `.cover` — hero mesh-gradient cover. Children: `.cover__logo` (use
  `logo-light.svg`), `.cover__body` > `.cover__eyebrow` + `.cover__title` +
  `.cover__subtitle`, and `.cover__meta` with `.cover__meta-block` >
  `.cover__meta-label` + `.cover__meta-value`.
- `.divider` — section-divider gradient page. `.divider__numeral` (giant ghosted
  number), `.divider__top` > `.divider__logo` + `.divider__eyebrow`,
  `.divider__bottom` > `.divider__title` + `.divider__synopsis`. Optional
  `.divider__contents` list (`.divider__contents-row` with `.num`).
  Reused for the back/closing page.

## Runners (header / footer on content pages)

```html
<div class="runner runner--top">
  <img class="runner__logo" src="logos/logo-dark.svg" alt="" />
  <div class="runner__rule"></div>
  <div class="runner__meta">01 Section Name <span class="sep">·</span> <span class="runner__page"></span></div>
</div>
<!-- ...content... -->
<div class="runner runner--bottom">
  <div class="runner__rule"></div>
  <div class="runner__meta">Ode with Anthropic <span class="sep">·</span> <span class="runner__page"></span></div>
</div>
```

Leave `.runner__page` empty — `paginate.js` fills it. The section label ("01
Section Name") is authored by hand.

## Headers

- `.section__header` (`--compact` for tighter) — `.eyebrow` + `.section__title`
  (+ optional `.section__lede`). `.section__title--md` is the 22pt smaller title.
- `.subhead` with `.subhead__num` — sub-section header with a tomato numbered chip.
- `.eyebrow` — uppercase tracked label with a leading rule; tomato by default.
- `.h-eyebrow` — muted uppercase mini-label.

## Prose

- `.prose` wrapping `<p>` — body text. `.prose p.lede` for a leading paragraph.

## Cards and grids

- `.three-up` (3-col), `.two-up` (2-col), `.four-up` (2×2) — grid wrappers.
  Modifiers `.three-up--tall` and `.three-up--fit` adjust card height/density.
- `.card` — `.card__num`, `.card__title`, `.card__body`. Variants: `.card--dark`,
  and top-accent `.card--accent-tomato` / `--accent-bluegray` / `--accent-teal`.
- `.feat` (inside `.four-up`/`.two-up`) — `.feat__label`, `.feat__title`,
  `.feat__body`. Variants `.feat--teal` / `--bluegray`.

## Number-led displays

- `.stat-strip` (+ `.stat-strip--3`) of `.stat` — `.stat__value` (with `.unit`
  span), `.stat__label`, optional `.stat__caption`.
- `.hero-stat` — gradient panel; `.hero-stat__label`, `__value`, `__caption`.
  Backers variant `.hero-stat--backers` with a `.backers-row` of `.backer-logo`.
- `.numlist` (+ `.numlist--compact`) of `.numlist__item` — `.numlist__num` +
  `.numlist__body` (`.numlist__title` + `.numlist__text`).
- `.pattern` row — huge `.pattern__num` + `.pattern__title` + `.pattern__body`.

## Set-apart statements

- `.thesis` (+ `.thesis--compact`) — `.thesis__label` + `.thesis__text`, framed by
  hairlines. The canonical marquee statement. Not a quotation.
- `.pq` (+ `.pq--tomato` / `--bluegray`) — pull quote with quote glyphs;
  `.pq__text` + `.pq__attrib`. Use for actual attributed quotations.
- `.callout` (+ `--teal` / `--bluegray`) — bordered note box; `.callout__label` +
  `.callout__body`. The home for sidebar content (alternatives, precedent, notes).

## Roadmap and deltas

- `.roadmap` — horizontal phase timeline with gradient track. `.roadmap__track`
  (+ `__nodes`/`__node`), `.roadmap__phases` of `.roadmap__phase`
  (`__label`, `__name`, `__duration`, `__body`). Optional `.roadmap__alpha` marker.
  Keep `__name` to **one or two short words** ("Discover", "Automate"). The name
  row reserves two lines so a wrap won't stagger the columns, but long names still
  look cramped; put the longer phrase in `__body` or a `.phase-grid__label` below.
- `.delta-cards` — two teal-accented `.delta-card` (`__label` + `__body`), e.g.
  "what changes / what stays."
- `.traits-box` — compact 2×2 highlight; `.traits-box__grid` of `.traits-box__item`
  with `.traits-box__num`.

## Tables

- `table.t` — borderless, horizontal rules, tabular numerals. First column is
  display-weight. `.pill--ok` (green "aligned") and `.pill--note` (teal) chips.
  `.t--num-narrow` for a narrow first column.

## Lists and structure

- `ol.prose-list` with `.prose-list__num` — flat numbered list, tomato numerals.
- `.decision-grid` (+ `--bare`) — 3-up threshold grid inside a callout.
- `.arch-list` (+ `--3`, `--3-2`, `--sm`) — bulleted component list under a
  diagram; `.arch-list__item` with `strong` lead-in.
- `.phase-block` — `.phase-grid` (2-col workstreams/deliverables with
  `.phase-grid__label` + `ul.phase-grid__list`) plus a `.phase-exit` gate box
  (`.phase-exit__label` + `.phase-exit__list`, optional `--two-col`).

## Team

- `.team-list` of `.team-row` — `.team-row__photo` (img or `--placeholder`) +
  `.team-row__body` (`.team-row__heading` > `.team-row__name` / `__sep` /
  `__role` / `__badge`, then `.team-row__blurb`). `.team-row--split` for two
  half-rows side by side.

## Diagrams and images

- `img.arch-diagram` — full-width bordered diagram. `--portrait` for a centered,
  height-capped portrait image. Drop source images in the workspace `assets/`
  folder and reference them relatively.

## Table of contents

- `.toc` of `.toc__entry` (`--major` / `--sub`) — anchor (`href="#id"`) wrapping
  `.toc__num` + `.toc__title` + `.toc__dots` + `.toc__page`. Leave `.toc__page`
  empty; `paginate.js` fills it from the page the anchor targets.

## Utility

- `.spacer-sm` / `-md` / `-lg`, `.col-2` (two-column text), `.no-break`
  (avoid breaking inside).

## Adjacent-sibling rule collapse

When a `.subhead` directly precedes a `.numlist`, `.pattern`, `.feat`,
`.arch-list`, or `table.t`, the following component's top rule is suppressed so
hairlines don't stack. If you add a new bordered component meant to follow a
subhead, add it to that selector block at the bottom of `components.css`.
