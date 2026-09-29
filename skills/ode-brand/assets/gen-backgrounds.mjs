/*
 * gen-backgrounds.mjs — render the brand grounds to PNG.
 *
 * Ode's grounds are near-solid warm darks (Bistre→Cola), not mesh
 * gradients — see the --grad-* tokens. Produces full-bleed 16:9
 * background images that downstream media
 * (slides, app hero panels) can drop in where a live CSS gradient is
 * not available. Run from this directory with puppeteer installed:
 *
 *   npm i puppeteer && node gen-backgrounds.mjs
 *
 * Outputs into ./backgrounds:
 *   cover.png     -- the --grad-hero mesh (cover slides / hero panels)
 *   divider.png   -- the --grad-warm diagonal (section dividers)
 *   brand.png     -- the --grad-brand sweep (alt accent panels)
 *
 * Regenerate only when the brand gradients in tokens.css change.
 */
import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';
import { mkdirSync, readFileSync } from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(__dirname, 'backgrounds');
mkdirSync(out, { recursive: true });

const W = 1920, H = 1080; // 16:9

// Single source of truth: read the brand gradients straight from tokens.css so
// the rendered PNGs can never drift from the --grad-* tokens.
const css = readFileSync(path.join(__dirname, 'tokens.css'), 'utf8');
function grad(name) {
  const m = css.match(new RegExp('--' + name + ':\\s*([\\s\\S]*?);'));
  if (!m) throw new Error('tokens.css missing --' + name);
  return m[1].replace(/\s+/g, ' ').trim();
}
const grads = {
  cover: grad('grad-hero'),
  divider: grad('grad-divider'),
  brand: grad('grad-brand'),
};

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });

for (const [name, bg] of Object.entries(grads)) {
  const html = `<!doctype html><html><head><style>
    html,body{margin:0;padding:0}
    .bg{width:${W}px;height:${H}px;background:${bg};}
  </style></head><body><div class="bg"></div></body></html>`;
  await page.setContent(html, { waitUntil: 'load' });
  await page.screenshot({ path: path.join(out, `${name}.png`), clip: { x: 0, y: 0, width: W, height: H } });
  console.log(`wrote backgrounds/${name}.png`);
}

await browser.close();
