# Ode fonts

These are **licensed commercial Dinamo typefaces** (see the `Dinamo Licensing
Terms.pdf` in the brand Drive). They are committed here for internal Ode use; keep
them out of any public mirror of this repo (add to `.gitignore` if it ever goes
public).

## Bundled (wired into `../tokens.css`)

| File | Typeface | Used for |
|---|---|---|
| `ABCDiatype-Regular.otf` / `.woff2` | ABC Diatype Regular | display + body (`--font-display`, `--font-body`) |
| `ABCDiatypeSemiMono-Regular.otf` / `.woff2` | ABC Diatype Semi Mono | eyebrows, labels, figures (`--font-mono`) |
| `StyreneA-Medium.otf` / `StyreneA-Medium-Web.woff2` | Styrene A Medium | secondary face (`--font-secondary`) |

All three embed into `ode-pdf` output (verified with `pdffonts`: `ABCDiatype-Regular`,
`ABCDiatypeSemiMono-Regular`, `StyreneAWeb-Medium` — no Helvetica/Arial).
`StyreneA-Medium-Web.css` is Dinamo's own `@font-face` snippet, kept for reference;
our `../tokens.css` is the source of truth.

`.woff2` is what the HTML→PDF Chromium engine loads and **embeds** into the PDF
(`ode-pdf` output contains `ABCDiatype-Regular`, verified with `pdffonts` — no
Helvetica/Arial fallback). `.otf` is the desktop file: install it (open the `.otf`)
so PowerPoint / Keynote / Google Docs render the real face, and for PowerPoint font
embedding.

## Weight coverage

Only single cuts are provided per family: **ABC Diatype Regular** and **Styrene A
Medium**. The renderer synthesizes heavier heading weights of ABC Diatype from
Regular; Styrene A is mapped across the weight range to its Medium cut in
`../tokens.css`. If more licensed weights arrive
([Styrene folder](https://drive.google.com/drive/folders/1nnQkW-FwpcFbNBdN-iSVcTTGMsMoJ9md);
Diatype folders in the Dinamo root), add each with its own `@font-face` and the
correct `font-weight`.

Drive source: <https://drive.google.com/drive/folders/16VhZLOOWLTZfJXutKvzAajA9RTo8kFqE>
