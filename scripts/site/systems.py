#!/usr/bin/env python3
"""The supported systems on the homes, from the app. Standard library only.

  systems.py --write --app PATH   read the app, write site/data/systems.json
                                  and site/assets/art/systems.svg, and
                                  regenerate the list blocks of both homes
  systems.py --write              regenerate the list blocks from the JSON
  systems.py --check [--app PATH] the JSON, the sprite, the blocks and
                                  facts.json agree; with --app, also that
                                  they are what the app would produce

The app (read-only) owns the data (docs/landing-round2-plan.md §1.5):

  crates/coverly-core/src/systems/systems.toml        ids, names, families,
                                                      aliases, libretro names
  src/components/system/systemIcons.generated.ts      the 89 silhouettes
                                                      (RetroArch Assets, XMB
                                                      Monochrome, CC BY 4.0)
  src/components/system/systemFallbacks.ts            FALLBACK_ABBR

The homes carry the list already generated, between <!-- systems:begin -->
and <!-- systems:end -->, grouped by family and, for consoles, handhelds
and computers, by maker. Each system is
<li data-k="aliases"><i data-i="icon id"></i>Name</li>, or <i data-a="ABBR">
when the app has no silhouette for it. The sprite is never referenced by
the HTML: systems.js swaps the placeholders in when the section comes near.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
DATA = SITE / "data/systems.json"
SPRITE = SITE / "assets/art/systems.svg"
FACTS = SITE / "data/facts.json"
APP_FILES = {
    "systems": "crates/coverly-core/src/systems/systems.toml",
    "icons": "src/components/system/systemIcons.generated.ts",
    "fallbacks": "src/components/system/systemFallbacks.ts",
}
PAGES = {"index.html": "es", "en/index.html": "en"}
FAMILIES = ["console", "handheld", "computer", "arcade", "engine"]
# Families split by maker; the others are one alphabetical list (their
# "maker" is a board, an engine or a game).
BY_MAKER = {"console", "handheld", "computer"}
WORDS = {
    "es": {"console": "Consolas", "handheld": "Portátiles", "computer": "Ordenadores",
           "arcade": "Arcade", "engine": "Motores, ports y consolas de fantasía", "other": "Otros fabricantes"},
    "en": {"console": "Consoles", "handheld": "Handhelds", "computer": "Computers",
           "arcade": "Arcade", "engine": "Engines, ports and fantasy consoles", "other": "Other makers"},
}
# The maker is the libretro prefix ("Nintendo - Game Boy" -> Nintendo).
# This table covers the systems without a libretro name, and the prefixes
# that are not a maker (MAME, DOS, FBNeo, game titles, Microsoft for MSX).
MAKER = {
    "gw": "Nintendo", "pokemini": "Nintendo", "switch": "Nintendo", "sufami": "Bandai",
    "jaguarcd": "Atari", "ps5": "Sony", "xboxone": "Microsoft", "xboxseries": "Microsoft",
    "msx": "MSX", "msx2": "MSX", "msxturbor": "MSX", "fmtowns": "Fujitsu", "bbcmicro": "Acorn",
    "coco": "Tandy", "ti99": "Texas Instruments", "c128": "Commodore", "apple2": "Apple",
    "dragon": "Dragon Data", "3do": "3DO", "arduboy": "Arduboy",
    "cps1": "Capcom", "cps2": "Capcom", "cps3": "Capcom", "atomiswave": "Sammy",
    "naomi": "Sega", "naomi2": "Sega", "model2": "Sega", "model3": "Sega", "pgm2": "IGS",
    "triforce": "Namco, Sega, Nintendo", "neogeo": "SNK",
}
NO_MAKER = {"mame", "hbmame", "fbneo", "varcade", "dos", "megaduck", "uzebox"}
# The carousel's label when stripping the maker and the "/ alias" is not
# enough (it is decorative: the list keeps the app's full name).
SHORT = {"nes": "NES", "3do": "3DO", "triforce": "Triforce", "coco": "TRS-80 CoCo",
         "scv": "Super Cassette Vision", "supergrafx": "SuperGrafx", "varcade": "Arcade",
         "cps1": "CPS", "cps2": "CPS II", "cps3": "CPS III"}
KEYS = 3        # aliases kept per system for the search
KEY_LEN = 8     # longer aliases are folder names nobody types
PLACES = 1      # decimals kept in the sprite's path data
LICENCE = "https://creativecommons.org/licenses/by/4.0/"


# ── reading the app ───────────────────────────────────────────────────

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def read_app(path: Path) -> dict[str, str]:
    return {k: (path / rel).read_text(encoding="utf-8") for k, rel in APP_FILES.items()}


def parse_icons(ts: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"^  '?([\w-]+)'?: \{\n    viewBox: '([^']+)',\n    aspect: [\d.]+,\n    body: '((?:[^'\\]|\\.)*)',",
                         ts, re.M):
        out[m.group(1)] = {"viewBox": m.group(2), "body": m.group(3).replace("\\'", "'")}
    return out


def parse_fallbacks(ts: str) -> dict[str, str]:
    m = re.search(r"FALLBACK_ABBR[^=]*=\s*\{(.*?)\n\};", ts, re.S)
    return dict(re.findall(r"^\s+'?([\w-]+)'?: '([^']+)',", m.group(1), re.M)) if m else {}


def maker(sid: str, libretro: str | None) -> str | None:
    if sid in MAKER:
        return MAKER[sid]
    if sid in NO_MAKER or not libretro or " - " not in libretro:
        return None
    return libretro.split(" - ")[0]


def keys(sid: str, name: str, aliases: list[str]) -> list[str]:
    seen = set(re.findall(r"[a-z0-9]+", name.lower()))
    out: list[str] = []
    for a in [sid, *aliases]:
        a = a.lower()
        if len(a) <= KEY_LEN and " " not in a and a not in seen and a not in out:
            out.append(a)
    return out[:KEYS]


def short(sid: str, name: str, mk: str | None) -> str:
    if sid in SHORT:
        return SHORT[sid]
    s = re.split(r" / | \(", name)[0]
    rest = s[len(mk) + 1:] if mk and s.startswith(mk + " ") else ""
    if len(rest) > 2 and rest[0].isupper():  # not "64", "DS", "II", "turbo R"
        s = rest
    return s


def build_data(app: dict[str, str], commit: str) -> dict:
    import tomllib  # Python 3.11+, only needed with the app

    systems = tomllib.loads(app["systems"])["system"]
    icons = parse_icons(app["icons"])
    abbr = parse_fallbacks(app["fallbacks"])
    rows = []
    for s in systems:
        sid = s["id"]
        fam = s.get("family", "arcade" if s.get("arcade") else "console")
        mk = maker(sid, s.get("libretro"))
        rows.append({
            "id": sid, "name": s["name"], "short": short(sid, s["name"], mk), "family": fam, "maker": mk,
            "keys": keys(sid, s["name"], s.get("aliases", [])), "icon": sid in icons,
            "abbr": None if sid in icons else abbr.get(sid, re.sub(r"[^A-Z0-9]", "", sid.upper())[:4] or "?"),
        })
    return {
        "schema": 1,
        "source": {
            "app_repo": "MAECLY/coverly-roms", "app_commit": commit,
            **{f"{k}_sha256": sha256(v) for k, v in app.items()},
        },
        "systems": rows,
    }


# ── the sprite ────────────────────────────────────────────────────────

ARGS = {"m": 2, "l": 2, "h": 1, "v": 1, "c": 6, "s": 4, "q": 4, "t": 2, "a": 7, "z": 0}
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def fmt(x: float) -> str:
    s = f"{round(x, PLACES):.{PLACES}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def round_path(d: str) -> str:
    """Path data with every coordinate rounded to PLACES decimals, written
    compactly (arc flags kept as flags)."""
    out: list[str] = []
    i, cmd, prev_num = 0, "", ""
    while i < len(d):
        ch = d[i]
        if ch.isspace() or ch == ",":
            i += 1
            continue
        if ch.lower() in ARGS:
            cmd = ch
            out.append(ch)
            prev_num = ""
            i += 1
            if ch.lower() == "z":
                continue
            continue
        n = ARGS[cmd.lower()]
        group: list[str] = []
        for k in range(n):
            while i < len(d) and (d[i].isspace() or d[i] == ","):
                i += 1
            if cmd.lower() == "a" and k in (3, 4):
                group.append(d[i])
                i += 1
                continue
            m = NUM.match(d, i)
            if not m:
                raise ValueError(f"bad path data near {d[i:i + 20]!r}")
            group.append(fmt(float(m.group())))
            i = m.end()
        for tok in group:
            if prev_num and not tok.startswith("-") and not (tok.startswith(".") and "." in prev_num):
                out.append(" ")
            out.append(tok)
            prev_num = tok
        if cmd in "mM":
            cmd = "l" if cmd == "m" else "L"
    return "".join(out)


def build_sprite(app: dict[str, str]) -> str:
    icons = parse_icons(app["icons"])
    head = re.search(r"// RetroArch Assets.*\n// (https://\S+)\n// Changes: (.*)", app["icons"])
    src = head.group(1) if head else "https://github.com/libretro/retroarch-assets"
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg">',
        "<!-- System icons: RetroArch Assets, XMB Monochrome theme, (c) libretro contributors,",
        f"     CC BY 4.0 ({LICENCE}). Source: {src}",
        "     Changes: recoloured to currentColor, optimised with SVGO, viewBox cropped (in",
        "     Coverly ROMs), path data rounded to one decimal (here). Generated by",
        "     scripts/site/systems.py from the app; do not edit. -->",
    ]
    for sid, ic in icons.items():
        body = re.sub(r'\sd="([^"]*)"', lambda m: f' d="{round_path(m.group(1))}"', ic["body"])
        body = re.sub(r'<path fill="currentColor"', "<path", body)
        lines.append(f'<symbol id="{sid}" viewBox="{ic["viewBox"]}">{body}</symbol>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


# ── the list blocks ───────────────────────────────────────────────────

def esc(s: str) -> str:
    return html.escape(s, quote=True)


def groups(rows: list[dict], fam: str) -> list[tuple[str | None, list[dict]]]:
    """(maker or None for "other makers", systems) of one family, in the
    app's order; makers with a single system there go to the last group."""
    mine = [r for r in rows if r["family"] == fam]
    if fam not in BY_MAKER:
        return [(None, sorted(mine, key=lambda r: r["name"].lower()))]
    count: dict[str, int] = {}
    for r in mine:
        if r["maker"]:
            count[r["maker"]] = count.get(r["maker"], 0) + 1
    makers = sorted((m for m in count if count[m] > 1), key=lambda m: -count[m])
    out: list[tuple[str | None, list[dict]]] = [(m, [r for r in mine if r["maker"] == m]) for m in makers]
    rest = [r for r in mine if r["maker"] not in makers]
    if rest:
        out.append((None, rest))
    return out


def li(r: dict) -> str:
    k = " ".join(r["keys"] + ([r["maker"].lower()] if r["maker"] and r["family"] not in BY_MAKER else []))
    mark = f'<i data-i="{r["id"]}"></i>' if r["icon"] else f'<i data-a="{esc(r["abbr"])}"></i>'
    attr = ' data-k="' + esc(k) + '"' if k else ""
    if r["short"] != r["name"]:
        attr += ' data-s="' + esc(r["short"]) + '"'
    return f"<li{attr}>{mark}{esc(r['name'])}</li>"


def render(data: dict, lang: str) -> str:
    w = WORDS[lang]
    rows = data["systems"]
    out: list[str] = []
    for fam in FAMILIES:
        n = sum(1 for r in rows if r["family"] == fam)
        if not n:
            continue
        out.append(f'<section class="sys-g" data-f="{fam}"><h4>{esc(w[fam])} '
                   f'<span class="sys-c" data-fact="families.{fam}">{n}</span></h4>')
        for mk, items in groups(rows, fam):
            head = ""
            if fam in BY_MAKER:
                head = f'<h5>{esc(mk or w["other"])} <span class="sys-c">{len(items)}</span></h5>'
            out.append(f'<div class="sys-m">{head}<ul>{"".join(li(r) for r in items)}</ul></div>')
        out.append("</section>")
    return "\n".join(out)


BLOCK = re.compile(r"(<!-- systems:begin -->\n).*?(<!-- systems:end -->)", re.S)


def blocks(site: Path, data: dict, write: bool) -> list[str]:
    e: list[str] = []
    for rel, lang in PAGES.items():
        page = site / rel
        text = page.read_text(encoding="utf-8")
        if not BLOCK.search(text):
            e.append(f"{rel}: no systems block")
            continue
        new = BLOCK.sub(lambda m: m.group(1) + render(data, lang) + "\n" + m.group(2), text)
        if new != text:
            if write:
                page.write_text(new, encoding="utf-8")
            else:
                e.append(f"{rel}: the systems block differs from systems.json (run make systems)")
    return e


# ── checking ──────────────────────────────────────────────────────────

def validate(data: dict, sprite: str, facts: dict) -> list[str]:
    e: list[str] = []
    rows = data.get("systems", [])
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        e.append("systems.json repeats an id")
    symbols = re.findall(r'<symbol id="([\w-]+)"', sprite)
    want = [r["id"] for r in rows if r["icon"]]
    if sorted(symbols) != sorted(want):
        e.append(f"systems.svg symbols != the systems with an icon ({len(symbols)} vs {len(want)})")
    if re.search(r"\b(?:href|xlink:href)=", sprite):
        e.append("systems.svg references another file")
    for r in rows:
        if r["family"] not in FAMILIES:
            e.append(f"{r['id']}: unknown family {r['family']!r}")
        if not r["icon"] and not (r.get("abbr") and len(r["abbr"]) <= 4):
            e.append(f"{r['id']}: no icon and no abbreviation of up to 4 characters")
    if facts.get("systems") != len(rows):
        e.append(f"facts.json systems is {facts.get('systems')}, systems.json has {len(rows)}")
    fams = {f: sum(1 for r in rows if r["family"] == f) for f in FAMILIES}
    if facts.get("families") != {k: v for k, v in fams.items() if v}:
        e.append(f"facts.json families {facts.get('families')} != systems.json {fams}")
    return e


def drift(data: dict, sprite: str, app: dict[str, str]) -> list[str]:
    e: list[str] = []
    want = build_data(app, data["source"].get("app_commit", ""))
    if want["systems"] != data["systems"]:
        a = {r["id"]: r for r in data["systems"]}
        b = {r["id"]: r for r in want["systems"]}
        diff = sorted(set(a) ^ set(b)) or [k for k in b if a.get(k) != b[k]] or ["order"]
        e.append(f"systems.json differs from the app ({', '.join(diff[:6])}); run make systems")
    for k, v in want["source"].items():
        if k.endswith("_sha256") and data["source"].get(k) != v:
            e.append(f"source.{k}: {k.removesuffix('_sha256')} changed in the app; run make systems")
    if build_sprite(app) != sprite:
        e.append("systems.svg differs from the app's icons; run make systems")
    return e


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    p.add_argument("--check", action="store_true")
    p.add_argument("--write", action="store_true")
    p.add_argument("--app", type=Path)
    p.add_argument("--site", type=Path, default=SITE)
    a = p.parse_args(argv)
    data_path, sprite_path = a.site / "data/systems.json", a.site / "assets/art/systems.svg"
    if a.write and a.app:
        app = read_app(a.app)
        run = subprocess.run(["git", "-C", str(a.app), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        data = build_data(app, run.stdout.strip() or "unknown")
        data_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        sprite_path.write_text(build_sprite(app), encoding="utf-8")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    sprite = sprite_path.read_text(encoding="utf-8")
    facts = json.loads((a.site / "data/facts.json").read_text(encoding="utf-8"))
    errs = validate(data, sprite, facts) + blocks(a.site, data, write=a.write)
    if a.app and not a.write:
        errs += drift(data, sprite, read_app(a.app))
    for m in errs:
        print(f"FAIL systems {m}")
    print(f"systems: {len(errs)} failure(s)" + (f" (against {a.app})" if a.app else ""))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
