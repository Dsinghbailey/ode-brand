# Ode logos

All lockups are **bundled** here, each as vector **SVG** and transparent, high-res
**PNG** (RGBA), in `-light` (Bone `#FBFBF8`, for dark grounds) and `-dark` (Cola
`#3C2E2A`, for light grounds):

| Base name | What it is |
|---|---|
| `logo-{light,dark}` | Full lockup **with the "with Anthropic" endorsement** — the default signature. |
| `lockup-{light,dark}` | Lockup **without** endorsement (mark + "Ode"). |
| `mark-{light,dark}` | Graphic mark / symbol only. |
| `wordmark-{light,dark}` | "Ode" wordmark only. |

- **`ode-pdf`** uses the **SVG** (scales cleanly, embeds in the PDF).
- **`ode-slides`** uses the **PNG** (python-pptx can't place SVG). The helper only
  references the light logo, but both are provided.
- Light logo on dark/ground surfaces, dark on light. Never dark-on-dark.

## Provenance / regenerating

The **SVGs were pulled from the brand Google Drive** (byte-exact to the originals).
The **PNGs were rasterized from those SVGs** at 4× the viewBox with transparent
background (identical artwork to the Drive raster exports, generated locally for
reliability rather than round-tripped). To regenerate the PNGs after an SVG change:

```bash
cd <somewhere> && npm i sharp
node -e '
const sharp=require("sharp"),fs=require("fs"),path=require("path");
const dir="<abs path to this logos/ dir>", S=4;
for (const f of fs.readdirSync(dir).filter(f=>f.endsWith(".svg"))) {
  const svg=fs.readFileSync(path.join(dir,f),"utf8");
  const w=Math.round(parseFloat(svg.match(/viewBox="0 0 ([\d.]+)/)[1])*S);
  sharp(Buffer.from(svg),{density:72*S}).resize({width:w}).png()
    .toFile(path.join(dir,f.replace(/\.svg$/,".png")));
}'
```

Drive (other formats — EPS, extra PNG resolutions): <https://drive.google.com/drive/folders/1Sd6R4HEFbrRPVgQNuwemwrOmu0mbrpkZ>
