// Tests for the public reach: scripts/site/apply_metrics.py (baked in at
// build time) and site/assets/metrics.js (refreshed in the browser).
// Node's own runner, no dependencies: `node --test scripts/site/`.
//
// Each test fills site/ with apply_release.py (the fixture release), then
// with apply_metrics.py from a given metrics JSON, and either reads the
// slots it wrote or runs metrics.js in a VM against them with a fake fetch.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import vm from 'node:vm';

const ROOT = new URL('../../', import.meta.url).pathname;
const JS = readFileSync(join(ROOT, 'site/assets/metrics.js'), 'utf8');
const PYTHON = process.env.PYTHON || 'python3';
const API = 'https://api.github.com/repos/MAECLY/coverly-roms';

// Both pages, filled with the fixture release and then `metrics` (or with
// apply_metrics.py not run at all when `metrics` is null).
function built(metrics) {
  const dir = mkdtempSync(join(tmpdir(), 'cr-metrics-'));
  const out = join(dir, 'site');
  execFileSync(PYTHON, ['-I', join(ROOT, 'scripts/site/apply_release.py'),
    '--release-json', join(ROOT, 'scripts/site/fixtures/release.json'),
    '--repo', 'MAECLY/coverly-roms', '--site', join(ROOT, 'site'), '--out', out], { stdio: 'pipe' });
  if (metrics) {
    writeFileSync(join(dir, 'm.json'), JSON.stringify(metrics));
    execFileSync(PYTHON, ['-I', join(ROOT, 'scripts/site/apply_metrics.py'),
      '--metrics-json', join(dir, 'm.json'), '--out', out], { stdio: 'pipe' });
  }
  const pages = {
    es: readFileSync(join(out, 'index.html'), 'utf8'),
    en: readFileSync(join(out, 'en/index.html'), 'utf8'),
  };
  rmSync(dir, { recursive: true });
  return pages;
}

// The data-metric elements of a page: { name: { text, hidden } }.
function slots(html) {
  const out = {};
  for (const m of html.matchAll(/<(\w+)\b([^>]*)\sdata-metric="(\w+)"([^>]*)>(.*?)<\/\1>/g)) {
    out[m[3]] = { text: m[5], hidden: /\shidden\b/.test(m[4]) };
  }
  return out;
}

test('apply_metrics: known numbers above zero are written, localized', () => {
  const { es, en } = built({ downloads: 1234567, stars: 1 });
  assert.deepEqual(slots(es), {
    downloads: { text: '1.234.567 descargas', hidden: false },
    stars: { text: '1 estrella', hidden: false },
  });
  assert.deepEqual(slots(en), {
    downloads: { text: '1,234,567 downloads', hidden: false },
    stars: { text: '1 star', hidden: false },
  });
  const small = built({ downloads: 1234, stars: 2 });
  assert.equal(slots(small.es).downloads.text, '1.234 descargas', 'es groups four digits too');
  assert.equal(slots(small.en).stars.text, '2 stars');
  assert.equal(slots(built({ downloads: 1 }).es).downloads.text, '1 descarga');
});

test('apply_metrics: zero, missing or not a whole number stays empty and hidden', () => {
  const empty = { text: '', hidden: true };
  for (const metrics of [{}, { downloads: 0, stars: 0 }, { downloads: -3, stars: '5' }, { downloads: 2.5, stars: true }]) {
    const { es, en } = built(metrics);
    assert.deepEqual(slots(es), { downloads: empty, stars: empty }, JSON.stringify(metrics));
    assert.deepEqual(slots(en), { downloads: empty, stars: empty }, JSON.stringify(metrics));
  }
  const some = built({ downloads: 42 });
  assert.deepEqual(slots(some.en), { downloads: { text: '42 downloads', hidden: false }, stars: empty });
});

test('apply_metrics: a slot it cannot read fails the build', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cr-metrics-bad-'));
  writeFileSync(join(dir, 'm.json'), '{"downloads": 5}');
  for (const html of [
    '<html lang="es"><li data-metric="views" hidden></li></html>',
    '<html lang="es"><li data-metric="downloads" hidden>12</li></html>',
    '<html lang="es"><li data-metric="downloads"></li></html>',
    '<html><li data-metric="downloads" hidden></li></html>',
  ]) {
    writeFileSync(join(dir, 'index.html'), html);
    const run = spawnSync(PYTHON, ['-I', join(ROOT, 'scripts/site/apply_metrics.py'),
      '--metrics-json', join(dir, 'm.json'), '--out', dir], { encoding: 'utf8' });
    assert.equal(run.status, 1, html);
  }
  rmSync(dir, { recursive: true });
});

// metrics.js in a VM: a stand-in DOM made of the page's data-metric slots,
// a fake fetch answering `answer(url)` and a sessionStorage.
async function run(html, answer, store = {}) {
  const els = [];
  for (const m of html.matchAll(/<(\w+)\b([^>]*)\sdata-metric="(\w+)"([^>]*)>(.*?)<\/\1>/g)) {
    els.push({ name: m[3], textContent: m[5], hidden: /\shidden\b/.test(m[4]),
      getAttribute(k) { return k === 'data-metric' ? this.name : null; } });
  }
  const calls = [];
  const ctx = {
    document: {
      documentElement: { lang: /<html lang="(\w+)"/.exec(html)[1] },
      querySelectorAll: (sel) => (sel === '[data-metric]' ? els : []),
    },
    sessionStorage: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = v; },
    },
    AbortController, setTimeout, clearTimeout, Date, JSON, Promise, Array,
    fetch: async (url) => {
      calls.push(url);
      const a = answer(url);
      if (a instanceof Error) throw a;
      return { ok: a.status === 200, status: a.status, json: async () => a.body };
    },
  };
  ctx.window = ctx;
  vm.runInNewContext(JS, ctx);
  await new Promise((r) => setTimeout(r, 30));
  const by = Object.fromEntries(els.map((e) => [e.name, { text: e.textContent, hidden: e.hidden }]));
  return { by, calls, store };
}

// `n` releases, the first with two assets adding up to `total` downloads.
function releases(n, total) {
  return Array.from({ length: n }, (_, i) => ({
    tag_name: `v0.${i}.0`,
    assets: i ? [{ download_count: 0 }] : [{ download_count: total - Math.min(total, 1) }, { download_count: Math.min(total, 1) }],
  }));
}
const ok = (body) => ({ status: 200, body });
// GitHub with `total` downloads spread over `pages` pages of releases.
function github({ total = 1234, stars = 7, pages = 1 } = {}) {
  return (url) => {
    if (url === API) return ok({ stargazers_count: stars });
    const page = +/[&]page=(\d+)/.exec(url)[1];
    return ok(releases(page < pages ? 100 : 3, page === 1 ? total : 0));
  };
}

test('metrics.js: fills and shows known numbers above zero, in each language', async () => {
  const { es, en } = built(null);
  const a = await run(es, github());
  assert.deepEqual(a.by, { downloads: { text: '1.234 descargas', hidden: false }, stars: { text: '7 estrellas', hidden: false } });
  assert.deepEqual(a.calls.sort(), [API, `${API}/releases?per_page=100&page=1`]);
  const b = await run(en, github({ total: 1, stars: 1 }));
  assert.deepEqual(b.by, { downloads: { text: '1 download', hidden: false }, stars: { text: '1 star', hidden: false } });
});

test('metrics.js: follows every page of releases', async () => {
  const { en } = built(null);
  const { by, calls } = await run(en, github({ total: 5000, pages: 3 }));
  assert.equal(by.downloads.text, '5,000 downloads');
  assert.equal(calls.filter((u) => u.includes('/releases')).length, 3);
});

test('metrics.js: zero hides the slot, even a built one', async () => {
  const { en } = built({ downloads: 42, stars: 3 });
  const { by } = await run(en, github({ total: 0, stars: 0 }));
  assert.deepEqual(by, { downloads: { text: '42 downloads', hidden: true }, stars: { text: '3 stars', hidden: true } });
});

test('metrics.js: an API error, a rate limit or a bad answer leaves the built page', async () => {
  const { es } = built({ downloads: 42, stars: 3 });
  const before = { downloads: { text: '42 descargas', hidden: false }, stars: { text: '3 estrellas', hidden: false } };
  const answers = [
    () => ({ status: 403 }),
    () => ({ status: 500 }),
    () => new TypeError('offline'),
    (url) => (url === API ? ok({}) : ok({ message: 'not a list' })),
    (url) => (url === API ? ok({ stargazers_count: -1 }) : ok([{ assets: [{ download_count: 'x' }] }])),
  ];
  for (const answer of answers) {
    const { by, store } = await run(es, answer);
    assert.deepEqual(by, before);
    assert.deepEqual(store, {}, 'a failure is not cached');
  }
  const blank = await run(built(null).es, () => ({ status: 403 }));
  assert.deepEqual(blank.by, { downloads: { text: '', hidden: true }, stars: { text: '', hidden: true } }, 'no number is made up');
});

test('metrics.js: a full answer is cached for the tab for 10 minutes', async () => {
  const { en } = built(null);
  const first = await run(en, github({ total: 99, stars: 2 }));
  assert.deepEqual(JSON.parse(first.store['cr-metrics']).m, { downloads: 99, stars: 2 });
  const second = await run(en, () => new Error('must not fetch'), first.store);
  assert.equal(second.calls.length, 0);
  assert.equal(second.by.downloads.text, '99 downloads');
  const stale = { 'cr-metrics': JSON.stringify({ t: Date.now() - 11 * 60 * 1000, m: { downloads: 99, stars: 2 } }) };
  const third = await run(en, github({ total: 120, stars: 2 }), stale);
  assert.equal(third.by.downloads.text, '120 downloads');
});
