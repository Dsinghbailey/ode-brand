/*
 * watch.mjs — rebuild the PDF on every edit to the source, CSS, or assets.
 *
 * Usage: node watch.mjs [source.html]   (default: doc.html)
 * Leave running in a terminal during edits. Wait for "done" before opening the
 * output PDF. Debounced via chokidar awaitWriteFinish so partial writes are safe.
 */
import chokidar from 'chokidar';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const sourceArg = process.argv[2] || 'doc.html';
const sourceName = sourceArg.endsWith('.html') ? sourceArg : `${sourceArg}.html`;

let building = false;
let queued = false;

function build(reason) {
  if (building) { queued = true; return; }
  building = true;
  const started = Date.now();
  process.stdout.write(`\n[watch] rebuild ${sourceName} (${reason}) ... `);
  const child = spawn(process.execPath, [path.join(__dirname, 'build.mjs'), sourceName], {
    cwd: __dirname,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let err = '';
  child.stderr.on('data', d => { err += d.toString(); });
  child.on('close', code => {
    const ms = Date.now() - started;
    if (code === 0) {
      process.stdout.write(`done in ${ms}ms\n`);
    } else {
      process.stdout.write(`failed (exit ${code}) in ${ms}ms\n`);
      if (err) process.stderr.write(err);
    }
    building = false;
    if (queued) { queued = false; build('queued'); }
  });
}

const watchPaths = [
  path.join(__dirname, sourceName),
  path.join(__dirname, 'tokens.css'),
  path.join(__dirname, 'components.css'),
  path.join(__dirname, 'paginate.js'),
  path.join(__dirname, 'assets'),
];

const watcher = chokidar.watch(watchPaths, {
  ignoreInitial: true,
  awaitWriteFinish: { stabilityThreshold: 120, pollInterval: 40 },
});

watcher.on('all', (event, file) => {
  const rel = path.relative(__dirname, file);
  build(`${event} ${rel}`);
});

console.log(`[watch] watching ${sourceName}, tokens.css, components.css, paginate.js, assets/`);
console.log('[watch] running initial build...');
build('initial');
