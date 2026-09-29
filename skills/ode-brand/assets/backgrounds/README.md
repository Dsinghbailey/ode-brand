# Ode brand grounds — generated, not committed

These are pre-rendered 16:9 PNGs of the `--grad-*` grounds from `../tokens.css`, for
media that can't use a live CSS background (e.g. `.pptx` slide covers/dividers).
They are generated, so they aren't committed. Regenerate them whenever the
`--grad-*` tokens change:

```bash
cd ..            # into ode-brand/assets
npm i puppeteer
node gen-backgrounds.mjs
```

This writes `cover.png` (`--grad-hero`), `divider.png` (`--grad-divider`), and
`brand.png` (`--grad-brand`). Ode's grounds are near-solid warm darks (Bistre→Cola),
not mesh gradients. If these PNGs are absent, `ode-slides` falls back to a solid
Bistre ground for cover/divider/closing slides — legible and on-brand, just flatter.
