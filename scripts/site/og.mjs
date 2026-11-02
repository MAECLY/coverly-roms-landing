#!/usr/bin/env node
/**
 * Render the landing's Open Graph cards, 1200x630: site/assets/og.png (es)
 * and og-en.png (en) for the homes, og-features(-en).png and
 * og-roadmap(-en).png for the other pages, each with that page's H1.
 * `node scripts/site/og.mjs features roadmap` renders only those cards.
 *
 * The card: the Lean-To app icon (design/icon/app.svg, inlined as-is) on the
 * left; on the right the wordmark (COVERLY in Archivo Display 800 plus the
 * Manila ROMs tag, brand.md section 3), the headline, one line of copy, and the
 * shelf rule with the site's host along the bottom. Colours are the light
 * semantic palette from brand.md section 4.3.
 *
 * Text needs the brand font, which ships only as a woff2 (site/assets/fonts),
 * so the card is laid out as HTML and screenshotted with headless Chrome or
 * Chromium instead of resvg (which reads TTF/OTF only). The browser is found
 * through $CHROME, then the usual install paths and PATH names.
 *
 * Run: make site-og   (or: node scripts/site/og.mjs)
 */
import { execFileSync } from 'node:child_process';
import {
  existsSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const W = 1200;
const H = 630;

const COPY = {
  es: {
    lang: 'es',
    out: 'og.png',
    h1: 'Cada ROM, con su portada.',
    p: 'Mira qué juegos de tu tarjeta SD no tienen portada y añádelas de una vez. Primero la simulación, después deshacer.',
  },
  en: {
    lang: 'en',
    out: 'og-en.png',
    h1: 'Every ROM gets its cover.',
    p: 'See which games on your SD card have no cover art and fill them in one go. Dry run first, undo after.',
  },
  'features-es': {
    lang: 'es',
    out: 'og-features.png',
    h1: 'Todo lo que hace Coverly ROMs.',
    p: 'Portadas, 131 sistemas, comprimidos y discos, duplicados, seis vistas y la terminal, con la versión de cada cosa.',
  },
  'features-en': {
    lang: 'en',
    out: 'og-features-en.png',
    h1: 'Everything Coverly ROMs does.',
    p: 'Covers, 131 systems, archives and discs, duplicates, six views and the command line, with the version of each.',
  },
  'roadmap-es': {
    lang: 'es',
    out: 'og-roadmap.png',
    h1: 'Lo que ya está y lo que viene.',
    p: 'Cada versión con su fecha, y lo que viene en orden y con su estado.',
  },
  'roadmap-en': {
    lang: 'en',
    out: 'og-roadmap-en.png',
    h1: "What's done and what's next.",
    p: 'Each version with its date, and what comes next in order and with its status.',
  },
};
// `og.mjs features` renders only the cards whose key starts with a word given.
const only = process.argv.slice(2);
const cards = Object.keys(COPY).filter(
  (k) => !only.length || only.some((w) => k.startsWith(w)),
);

// Light palette, brand.md 4.3.
const C = {
  bg: '#F2F3EF',
  text: '#1B1E1B',
  muted: '#535A52',
  border: '#D3D7CF',
  primary: '#0E5E6F',
  manila: '#E6C171',
  manilaFg: '#2A2111',
};

const icon = readFileSync(join(REPO, 'design', 'icon', 'app.svg'), 'utf8')
  .replace(/<title>[^<]*<\/title>\n?/, '')
  .replace('<svg ', '<svg class="icon" aria-hidden="true" ');
const font = readFileSync(
  join(REPO, 'site', 'assets', 'fonts', 'archivo-variable.woff2'),
).toString('base64');

const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function page(key) {
  const t = COPY[key];
  return `<!DOCTYPE html>
<html lang="${t.lang}">
<head>
<meta charset="utf-8">
<style>
@font-face { font-family: 'Archivo Display'; font-weight: 600 800; font-stretch: 75% 112%; font-display: block;
  src: url(data:font/woff2;base64,${font}) format('woff2'); }
* { box-sizing: border-box; margin: 0; }
html, body { width: ${W}px; height: ${H}px; overflow: hidden; background: ${C.bg}; }
body { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; color: ${C.text}; }
.card { position: relative; width: ${W}px; height: ${H}px; }
/* app.svg is a 1024 canvas with a 100 px gutter: 440 px shows a 354 px tile. */
.icon { position: absolute; left: 36px; top: 74px; width: 440px; height: 440px; }
.copy { position: absolute; left: 520px; right: 72px; top: 110px; }
.wordmark { display: flex; align-items: center; gap: 14px; font: 800 52px/1 'Archivo Display'; letter-spacing: -0.01em; }
.tag { font: 800 30px/1 'Archivo Display'; letter-spacing: 0; background: ${C.manila}; color: ${C.manilaFg};
  border-radius: 5px; padding: 7px 0.3em 6px; }
h1 { margin-top: 56px; font: 800 66px/1.02 'Archivo Display'; letter-spacing: -0.01em; }
p { margin-top: 24px; font-size: 25px; line-height: 1.4; color: ${C.muted}; }
.shelf { position: absolute; left: 72px; right: 72px; bottom: 64px; height: 1px; background: ${C.border}; }
.shelf::before { content: ''; position: absolute; left: 0; top: -1px; width: 96px; height: 3px; background: ${C.primary}; }
.host { position: absolute; right: 72px; bottom: 30px; font: 500 20px/1 ui-monospace, 'SF Mono', Menlo, monospace; color: ${C.muted}; }
/* The site sets its headings at wdth 75 (after the font shorthands). */
h1, .wordmark, .tag { font-stretch: 75%; }
</style>
</head>
<body>
<div class="card">
${icon}
<div class="copy">
<div class="wordmark"><span>COVERLY</span><span class="tag">ROMs</span></div>
<h1>${esc(t.h1)}</h1>
<p>${esc(t.p)}</p>
</div>
<div class="shelf"></div>
<span class="host">coverly-roms.maecly.com</span>
</div>
</body>
</html>
`;
}

// ------------------------------------------------------------------ browser

function findChrome() {
  const candidates = [
    process.env.CHROME,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ].filter(Boolean);
  for (const c of candidates) if (existsSync(c)) return c;
  for (const name of [
    'google-chrome',
    'google-chrome-stable',
    'chromium',
    'chromium-browser',
  ]) {
    try {
      return execFileSync('which', [name], { encoding: 'utf8' }).trim();
    } catch {
      /* next */
    }
  }
  console.error(
    'No Chrome or Chromium found. Install one, or point $CHROME at its binary.',
  );
  process.exit(1);
}

/** Width and height from a PNG's IHDR. */
function pngSize(buf) {
  return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
}

const chrome = findChrome();
const dir = mkdtempSync(join(tmpdir(), 'coverly-og-'));
try {
  for (const lang of cards) {
    const html = join(dir, `${lang}.html`);
    const shot = join(dir, `${lang}.png`);
    writeFileSync(html, page(lang));
    execFileSync(
      chrome,
      [
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        '--no-first-run',
        '--no-default-browser-check',
        `--user-data-dir=${join(dir, 'profile')}`,
        '--force-device-scale-factor=1',
        '--force-color-profile=srgb',
        `--window-size=${W},${H}`,
        '--virtual-time-budget=3000',
        `--screenshot=${shot}`,
        pathToFileURL(html).href,
      ],
      { stdio: 'ignore' },
    );
    const png = readFileSync(shot);
    const [w, h] = pngSize(png);
    if (w !== W || h !== H)
      throw new Error(`${lang}: expected ${W}x${H}, got ${w}x${h}`);
    const out = join(REPO, 'site', 'assets', COPY[lang].out);
    writeFileSync(out, png);
    console.log('  wrote', out.slice(REPO.length + 1));
  }
} finally {
  rmSync(dir, { recursive: true, force: true });
}
