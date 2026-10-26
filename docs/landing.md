# Landing page

The public page at **https://coverly-roms.maecly.com** is the static site in
`site/` of this repository (`MAECLY/coverly-roms-landing`); the app lives in
[`MAECLY/coverly-roms`](https://github.com/MAECLY/coverly-roms). Spanish at
`/` (also `x-default`), English at `/en/`, plus `404.html`, `robots.txt`,
`sitemap.xml`, `llms.txt`, `agents.txt` and the web manifests. Plain HTML,
one stylesheet, five small scripts (`theme.js` for the colour mode and OS
hint, `motion.js` for the reveals, step clips, terminal and the third-party
request counter, `shelf.js` for the showcase choreography, `release.js` for
the latest release and the copy buttons, `metrics.js` for the public
reach) and the decorative art under
`site/assets/art/`. No framework and no dependencies: the build is a Python
script that fills the release markers. The only other server the page talks
to is `api.github.com`, for the latest release and the public reach (the
CSP allows nothing else).

It follows the conventions of the Pluryprint and Versorium landings: the same
section order, bilingual setup, SEO and agent files, and release-filled
download section.

## How it follows the releases

Nothing in `site/` names a version, a date, a download link or a file size.
Those places carry `{{release.*}}` markers inside `<!-- release:begin -->` …
`<!-- release:end -->` blocks, next to `<!-- norelease:begin -->` blocks with
the "not published yet" state.

`scripts/site/apply_release.py` copies `site/` to an output folder and:

- with `--release-json` (the `GET /repos/MAECLY/coverly-roms/releases/latest`
  record), keeps the release blocks and fills every marker; it refuses a
  draft or pre-release, a tag that is not `v<SemVer>`, and any missing,
  ambiguous, empty or misplaced download (the app bundles are matched by
  pattern, like the app repository's `release_tools.py build_artifacts()`, so the
  `Coverly.ROMs_<v>_…` prefix that `release.yml` stages is not hardcoded);
- with `--no-release`, keeps the norelease blocks and drops every marker.

## How it deploys

Vercel (project `coverly-roms-landing`) builds and serves the page through
its Git integration: every push to `main` deploys production, pull requests
get preview deployments. `vercel.json` sets the build:

- `installCommand: true` (nothing to install) and
  `buildCommand: bash scripts/site/vercel_build.sh`, which runs
  `check_site.py`, asks the GitHub API for the latest release of
  `MAECLY/coverly-roms` (with `GITHUB_TOKEN`, when the project defines it,
  only to raise the rate limit), fills `site/` into `target/site` with
  `apply_release.py`, and uses `--no-release` only when the API answers
  404; any other API error fails the build, so a deploy never links a file
  that is not there;
- `outputDirectory: target/site`, `trailingSlash: true`;
- the security headers on every path (`X-Content-Type-Options`,
  `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy`; Vercel adds
  HSTS itself) and long cache lifetimes for the fonts and art.

Publishing a release changes no file here, so the app repository's
[`landing-redeploy.yml`](https://github.com/MAECLY/coverly-roms/blob/main/.github/workflows/landing-redeploy.yml)
POSTs a Vercel deploy hook for `main` (its `VERCEL_DEPLOY_HOOK_URL` secret)
when a release is published. Until that build is live, and if it ever
fails, `site/assets/release.js` reads the same API record in the browser and
swaps the version, date, notes link and every `a[data-asset]` download for
the newer release (only when every file exists in it; any error leaves the
built page alone). `release.test.mjs` runs it against both filled pages.

## Public reach

The hero's facts line shows the total downloads ("43 descargas" / "43
downloads": the `download_count` of every asset of every release of
`MAECLY/coverly-roms`), and the footer's "Código fuente" link is followed by
the GitHub stars. Both are public numbers from the GitHub API; repository
views are not (they need an admin token) and are never shown.

In `site/` each one is an empty, hidden slot (`data-metric="downloads"`,
`data-metric="stars"`). After `apply_release.py`, `vercel_build.sh` runs
`scripts/site/fetch_metrics.py` (every page of releases, plus the repository
record) and `scripts/site/apply_metrics.py`, which writes the label in the
page's language (`1.234 descargas`, `1,234 downloads`, `1 estrella`) and
unhides the slot only for a number that is known and above zero. An API
error, a rate limit or a 0 leaves the slot hidden, and never fails the
build. In the browser, `site/assets/metrics.js` asks the same API (cached
for the tab for 10 minutes, like `release.js`) and refreshes the numbers;
any error leaves the built page alone. `metrics.test.mjs` covers both, and
the `metrics` gate of `check_site.py` keeps every slot empty and hidden in
`site/`.

## Brand tokens

`design/tokens.json` is a copy of the app's, the source of truth for the
brand. `scripts/brand/build_tokens.mjs` (the app's generator, trimmed to the
landing) writes `site/assets/tokens.css` from it; `--check` fails when the
CSS is stale or a contrast pair misses its WCAG target. `make sync-tokens`
fetches the app's `main` copy and regenerates;
`.github/workflows/sync-tokens.yml` does the same weekly (or by hand) and
opens a pull request when anything changed.

## Local preview and checks

```bash
make site                                            # before the first release
make site RELEASE=scripts/site/fixtures/release.json # with a (fake) release
make site SITE_PORT=8111                             # another port (default 8080)
make build                                           # what Vercel builds, into target/site
make check                                           # every gate, both states
```

`make check` runs `build_tokens.mjs --check`, `gen_covers.mjs --check`,
`node --test` on `scripts/site/*.test.mjs` and `check_site.py`, which builds
both states and checks: required files, `tokens.css` against a fresh build of
`design/tokens.json`, `vercel.json` (output folder, build command, security
headers), action pins in this repository's workflows, internal links and
`#fragments`, Spanish/English structural parity, FAQ JSON-LD against the
visible FAQ, CSP and head tags, sized/described/lazy images, size budgets,
visible word count, WCAG contrast of the token pairs, the motion contract (see
Motion), the art and the live-release layer. `.github/workflows/check.yml`
runs the same on every push and pull request.

## Motion

The page is one long library shelf, "The Living Shelf"
([landing-showcase-spec.md](landing-showcase-spec.md) is the design record;
[landing-motion-research.md](landing-motion-research.md) the research behind
it). It opens on the app icon's pose, a cover leaning at 12° against an empty
slot, and closes with that cover seated. The motion only ever enacts the slot
grammar: **dashed = not yet, solid = done, Buckram spine = Coverly did it,
Manila tab = you can still undo it.**

Rules, the same as on the Pluryprint and Versorium landings:

- **The HTML is the finished page.** Motion only plays towards it. Text,
  headings and screenshots are never faded or slid in; only decorative SVG
  (`svg.art`) and the steps' camera get a starting pose.
- **Two gates.** `theme.js` sets `html.anim` in `<head>` unless the visitor
  asked for reduced motion or turned on Save-Data. `motion.js` adds
  `html.motion` once its setup worked. Any error, or reduced motion switched
  on mid-visit, runs `halt()`, which also dispatches `cr-halt`; `shelf.js`
  listens and runs its own `stop()`s. Every `stop()` puts its piece in the
  frame the HTML already shows: halting means finishing.
- **One loud moment.** The hero plays once; nothing else moves while it
  does. Everything else is a quiet beat, scrolled or clicked.
- **Scroll-linked parts** sit inside `@supports (animation-timeline:
  view())`, declared after the `animation` shorthand, with `fill-mode:
  both`. Without support (Firefox 154, Safari before 26) they show finished;
  the closing shelf instead plays the same frames once by the clock
  (`.landed`).
- **Off screen, paused.** `shelf.js`'s one `IntersectionObserver` marks
  `svg.art` that leaves the screen with `[data-off]`, which pauses its
  animations.
- **Reduced motion is a finished still life**, not a stripped copy: every
  animation, transition and view transition stops, the replay buttons go,
  and the #seguro demo still answers clicks with instant swaps (150 ms
  opacity at most).
- Easing comes from `design/tokens.json`: `--cr-ease-ink` for every apply,
  fill, register and undo, `--cr-ease-spring` only for tag drops,
  `--cr-ease-standard` for the rest. The landing adds `--lp-ease-swing` (the
  accession tag) and `--lp-dur-hero`.

What moves:

| Where | What | Trigger |
| --- | --- | --- |
| Header | The Lean-To mark tips upright and back on hover or focus. A row of 24 mini slots under the bar fills with the reading progress. | Hover/focus; scroll (CSS) |
| Hero, "The Lean-To" | Inline SVG (a wide scene ≥ 1024 px, a 64 px strip between the H1 and the copy below). The shelf rule draws, the two gaps' dashes march, a riso ghost proof appears in each (simulate), the layers register while the photo-corners fold away and the Manila tabs drop (apply), the Buckram spines draw and the tally reads 6/7 (commit), and the leaning cover rocks 12° → 9° → 12° without seating. The H1's keyword stands on a slot underline that turns solid. 2.3 s. ↻ Replay stays in place, `aria-disabled` while it plays. | 40% of the art on screen, at once if it already is; a load slower than 4 s shows the end frame |
| Section heads | Each H2's shelf rule draws out from its Buckram cap | Scroll (CSS) |
| #como (greyboard-dark band) | From 1024 px the four shots share one pinned desk: each step's text wipes its shot down over the last (`clip-path`, never a cross-fade, which would double-expose two busy screenshots). Each screenshot's camera moves in on the spot that matters (`--cx`/`--cy` sit on the mark, so the mark stays put and inside the frame); a slot rail fills step by step; the callouts and the stamp draw | Scroll (CSS) |
| Step 3 and 4 clips | See **Step clips** below | 60% of the step's text (pinned) or 50% of the figure |
| #seguro | The visitor runs the round trip: Simular → Aplicar → Deshacer, with a polite live region; the card ends exactly as it began. The five pictograms draw. | Click (also under reduced motion); scroll (CSS) |
| #formatos | One gallery row develops once (grounds, covers, spines); hovering a layout row lifts its run. The terminal types each command and prints one output line; the cursor is a dashed slot that blinks three times. | `[data-reveal]`; hover; 45% on screen |
| #comparar | The Coverly column's highlight wipes down row by row and its checks draw | Scroll (CSS) |
| #descargar | No release: a waiting slot whose dashes march once and whose `v0.1.0` accession tag swings and settles. Release: the OS cards fill like slots and the detected one's tag drops in. | Scroll (CSS) / `[data-reveal]` |
| FAQ | The marker is a mini slot: dashed closed, solid Buckram open | Open |
| Closing | A shelf across the viewport (25 slots, 7 on phones) with the hero's cover at its centre, leaning. The covers wipe on left to right, their spines just after; two slots (one on phones) stay dashed and pulse once, with `152` over them (Coverly never guesses); the leaning cover tips upright into its slot, its Manila tab drops and the CTA's Buckram spine draws under the button. | Scroll (CSS, pixel ranges on the shelf's own view timeline so the end is reached on any viewport); without scroll timelines `.landed` at 50% of the section, 1.6 s |
| Footer | The "requests to other servers" count sits in a dashed mini slot that stays empty | Static |
| Colour mode, ES/EN | The new mode spreads from the click; ES/EN cross-fade, the hero shelf rule held still (`view-transition-name: shelf`) | Click or key |

The art: `assets/art/covers.svg` (40 generative covers and a 7-glyph stroke
font, from `scripts/site/gen_covers.mjs`, deterministic, invented titles as
seeds, one muted ink per cover as the brand's landing exception allows),
`kit.svg` (slot parts and pictograms), `grain.svg` and `weave.svg`. Every
symbol is `currentColor`; the page colours each `<use>` with a class
(`.ink-0`…`.ink-5`, generated light and dark). The hero inlines its covers
so the first paint needs no request. Serve the site over http to preview it:
external `<use>` does not work from `file://`.

The gates in `check_site.py`:

- **motion**: the gates, `halt()` and `cr-halt` in both scripts, the
  reduced-motion matchMedia in `shelf.js`; a reduced-motion block that stops
  animations, transitions, view transitions and the replay buttons;
  keyframes and transitions only move transform, opacity, visibility,
  clip-path, stroke-dashoffset, background size, box-shadow and colours (the FAQ's height is the one
  exception, since it answers a click); `animation-timeline` only inside
  `@supports`; every other animation behind `html.anim`, `html.motion` or
  `prefers-reduced-motion: no-preference`; motion never hides text or
  images; no `<video>` or `autoplay`.
- **art**: every inline `svg.art` is `aria-hidden="true"
  focusable="false"`, has a `viewBox` and `width`/`height` (CLS 0), and holds
  no `text`, `image`, `img`, `script` or `foreignObject`; the files under
  `assets/art/` reference nothing outside themselves.
- **links**: a `#fragment` into an `.svg` must name an `id` in that file.
- **files**: `gen_covers.mjs --check` (the sprite and the ink block are not
  stale).

Budgets (raw / gzip bytes):

| What | Budget |
| --- | --- |
| Each page (`index.html`, `en/index.html`) | 66,500 / 15,600 |
| Stylesheets (`tokens.css` + `site.css`) | 83,500 / 18,800 |
| All scripts under `assets/` (recursive) | 26,000 / 8,400 |
| `motion.js` alone | 9,500 |
| `shelf.js` alone | 5,000 |
| `release.js` alone | 6,500 |
| Art (`assets/art/*.svg`) | 24,000 / 7,000 |
| `covers.svg` alone | 18,000 |
| Fonts | 128,000 |
| Visible words, each locale | 1,850 |

**Before merging a motion change, check it in a browser** (Chrome DevTools,
the release-filled copy on a local port):

- 1440×900 and 390×844, light and dark, reduced motion on and off, both
  locales.
- With reduced motion: `document.getAnimations().length === 0`, the
  finished still life, and the #seguro demo still works.
- Without JS: the same finished page; the demo's buttons stay hidden.
- Keyboard: header, ↻ Replay, the demo buttons (`aria-pressed`, live
  region) and the FAQ.
- A performance trace at 4× CPU and Slow 4G: LCP stays `p.sub` (about
  2.3 s locally without compression), CLS 0. Lighthouse mobile ≥ 90 and
  LCP < 2.5 s, measured with compression on (Vercel compresses; `python3 -m
  http.server` does not, and costs about 7 points and 1 s of simulated LCP).
  Reference, October 2026 with the fixture release: mobile 97, LCP 2.48 s;
  desktop 100; `main` before the showcase: mobile 98, LCP 2.40 s.
- Firefox for the finished states without scroll timelines.
- 0 console errors and no CSP reports.

**Step clips.** The step 3 and 4 clips are not recordings: each is an SVG in
the 1280×800 space of its screenshot (`.clip-fx`, like the step 1 and 2
ellipses), drawn over the still. The moving cover is cut from the same image
(`motion.js` points each `<image class="fx-src">` at the `<img>`'s
`currentSrc`), so it follows the language, the colour mode and the pixel
density. Two patches use the shots' own surfaces (`--shot-modal`,
`--shot-slot`). If the screenshots are re-captured, check the coordinates in
the markup (the review ring, the Accept button, the first candidate; the
English candidate sits 13 px higher) and the `--fx-dy` / `--fx-cy` values in
`site.css`; also the step 1 and 2 ellipses (`.annot-mark`, centred on the
measured text of each locale's shot, not on a guess) and each `.cam-N`
origin, which must sit on its mark. Without `html.motion` the SVG is not displayed, and the replay
buttons, like the hero's, stay in place and are `aria-disabled` while they
play.

**Not done yet: recordings of the real app.** These would be play-once
animated WebP clips, each with a still, as Versorium makes them with
`tests/landing/record.mjs` and `encode-clips.py`. In the mock, running a job
opens the Jobs dialog over the grid and pauses after 25 items, so a clean
recording needs app-side changes first. Planned clips:

- Apply: dashed slots turn into covers.
- Undo: the covers go back to slots.

They need:

- a `?mockPause=off` flag in the mock backend, which otherwise pauses after
  25 items;
- Playwright in the dev dependencies;
- per-file size budgets in `check_site.py`: about 110 kB for each desktop
  clip and 75 kB for each phone clip.

## Screenshots and Open Graph cards

The screenshots under `site/assets/shots/{es,en}/` are real captures of the
browser UI with its mock backend (`make web` in the app repository), whose art is labelled
placeholder art, so no capture shows real box art. Capture each screen at a
1600×1000 viewport with device pixel ratio 2 in light and dark, save them as
`<raw>/<lang>/<screen>-<light|dark>.png` and run
`python3 scripts/site/encode_shots.py <raw>` (needs `cwebp`): it writes the
2560-wide and `@1x` 1280-wide WebP files the `<picture>` elements use.

`make og` (`scripts/site/og.mjs`) renders the 1200×630 cards
`site/assets/og.png` and `og-en.png`: the Lean-To app icon from
`design/icon/app.svg`, the wordmark with its Manila `ROMs` tag, the headline and
the shelf rule, laid out in HTML with the landing's variable Archivo woff2
(at width 75, as the page's headings) and screenshotted by headless Chrome or Chromium (`$CHROME` to pick one).

The favicon, touch and manifest icons (including the maskable one) and the nav
mark (`site/assets/mark.svg`, `mark-dark.svg`, swapped by `theme.js` like the
screenshots) are rasterised or cropped from the app repository's `design/icon/`
by its `pnpm icons` and copied here; the footer keeps the wordmark only, as
[`docs/08-brand/brand.md`](https://github.com/MAECLY/coverly-roms/blob/main/docs/08-brand/brand.md) asks. The display face is Archivo (OFL-1.1), variable (width 75–112,
weight 600–800) and subset to Latin (`site/assets/fonts/`).

## One-time setup (maintainer)

1. **Vercel project** `coverly-roms-landing`: Git-connected to
   `MAECLY/coverly-roms-landing`, production branch `main`, framework
   "Other"; `vercel.json` sets the rest. Optionally a `GITHUB_TOKEN`
   environment variable (a fine-grained token with no permissions) to raise
   the API rate limit of the build.
2. **Domain:** `coverly-roms.maecly.com` added to the project. In Cloudflare
   (the `maecly.com` zone), the `coverly-roms` record points at Vercel as
   the project's domain settings say, **DNS only** (grey cloud), so Vercel
   issues the certificate.
3. **Deploy hook:** Vercel → Project → Settings → Git → Deploy Hooks, one
   for `main`; store its URL as the `VERCEL_DEPLOY_HOOK_URL` secret of
   `MAECLY/coverly-roms` (used by its `landing-redeploy.yml`).
4. **Sync tokens:** Settings → Actions → General → "Allow GitHub Actions to
   create and approve pull requests", so `sync-tokens.yml` can open its pull
   request.
