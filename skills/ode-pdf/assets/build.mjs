/*
 * build.mjs — render a Ode designed document to PDF via headless Chrome.
 *
 * Usage:  node build.mjs [source.html]   (default: doc.html)
 * Output: output-<basename>.pdf  (e.g. doc.html -> output-doc.pdf)
 *
 * Pages are Letter (8.5x11in), full-bleed, printBackground on. If the document
 * loads paginate.js, build.mjs waits for the data-paginated flag before printing
 * so page numbers are stamped first.
 */
import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const sourceArg = process.argv[2] || 'doc.html';
const sourceName = sourceArg.endsWith('.html') ? sourceArg : `${sourceArg}.html`;
const baseName = path.basename(sourceName, '.html');
const outputName = `output-${baseName}.pdf`;

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
const fileUrl = 'file://' + path.join(__dirname, sourceName);

await page.goto(fileUrl, { waitUntil: ['networkidle0', 'load'] });
await page.evaluateHandle('document.fonts.ready');

// If the document self-numbers (loads paginate.js), wait until it has stamped
// every page/TOC number before printing. Documents without it build unchanged.
const selfNumbers = await page.evaluate(() => !!document.querySelector('script[src*="paginate"]'));
if (selfNumbers) {
  await page.waitForFunction(
    () => document.documentElement.getAttribute('data-paginated') === 'true',
    { timeout: 5000 },
  );
}

await page.pdf({
  path: path.join(__dirname, outputName),
  width: '8.5in',
  height: '11in',
  printBackground: true,
  preferCSSPageSize: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});

await browser.close();
console.log(`PDF rendered to ${outputName}`);
