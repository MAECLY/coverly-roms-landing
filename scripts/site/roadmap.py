#!/usr/bin/env python3
"""The roadmap data file and the pages it feeds. Standard library only.

  roadmap.py --check [--app PATH]   validate site/data/roadmap.json and the
                                    generated blocks; with --app, also
                                    compare it with the app's TODO.md,
                                    CHANGELOG.md and docs/TRACKER.md
  roadmap.py --update PATH          fill the machine fields from the app and
                                    regenerate the blocks
  roadmap.py --write                regenerate the blocks from the JSON only
  roadmap.py --remote               --check --app against the app's main on
                                    GitHub; warns only (Vercel build)

One file, site/data/roadmap.json, feeds /roadmap/, /en/roadmap/ and the
#siguiente teaser of both homes. The pages carry the blocks already
generated, between <!-- roadmap:NAME:begin --> and <!-- roadmap:NAME:end -->,
so the HTML is the finished page and the browser never reads the JSON.

Who writes what (docs/landing-redesign-plan.md §5): --update writes
source.*, the released versions and dates (CHANGELOG), next[].progress (the
- [x] / - [ ] boxes of each "## N." of TODO.md, up to the next "##") and
adds a TODO block it has never seen as "public": false with empty copy,
which --check refuses until a person writes it. A person writes every
text, status, public and teaser. When CHANGELOG has a version the file
does not, --update moves "unreleased" into it and turns the /features
version tags marked data-since="next" into that version.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "site/data/roadmap.json"
SITE = ROOT / "site"
REPO = "MAECLY/coverly-roms"
APP_FILES = {"todo": "TODO.md", "changelog": "CHANGELOG.md", "tracker": "docs/TRACKER.md"}
# Read too, for site/data/facts.json (the numbers the pages print).
FACT_FILES = {"systems": "crates/coverly-core/src/systems/systems.toml", "credits": "credits/credits.json"}
FACTS = ROOT / "site/data/facts.json"
STATUS = {
    "verifying": ("Hecho, falta probarlo", "Done, being tested"),
    "almost": ("Casi listo", "Almost there"),
    "research": ("En investigación", "Being researched"),
    "planned": ("Planificado", "Planned"),
    "blocked": ("Espera a otro bloque", "Waiting on another block"),
    "parked": ("Aparcado", "Parked"),
}
# Which blocks each page carries, and its language.
PAGES = {
    "index.html": ("es", ["teaser"]),
    "en/index.html": ("en", ["teaser"]),
    "roadmap/index.html": ("es", ["released", "upcoming"]),
    "en/roadmap/index.html": ("en", ["released", "upcoming"]),
}
FEATURES = ["features/index.html", "en/features/index.html"]
SLOTS = 24
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
MONTHS = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
           "septiembre", "octubre", "noviembre", "diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}
WORDS = {
    "es": {"next": "Próxima versión", "unreleased": "Ya en el código, aún sin publicar.",
           "of": "de", "tasks": "tareas", "after": "Espera a", "see": "Ver la hoja de ruta"},
    "en": {"next": "Next version", "unreleased": "Already in the code, not published yet.",
           "of": "of", "tasks": "tasks", "after": "Waits for", "see": "See the roadmap"},
}


class Drift(Exception):
    """The data file and the app (or the pages) disagree."""


# ── reading the app ───────────────────────────────────────────────────

def parse_todo(text: str) -> dict[str, dict[str, int | str]]:
    """{id: {done, total, title}} for every "## N." section of TODO.md:
    every checkbox (any indent, any ### inside) up to the next "## "."""
    out: dict[str, dict[str, int | str]] = {}
    cur = None
    fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if fence:
            continue
        if line.startswith("## "):
            m = re.match(r"## (\d+(?:\.\d+)?)\.\s+(.*)", line)
            cur = m.group(1) if m else None
            if cur:
                out[cur] = {"done": 0, "total": 0, "title": m.group(2).strip()}
            continue
        if cur:
            m = re.match(r"\s*[-*] \[([ xX])\]", line)
            if m:
                out[cur]["total"] += 1
                out[cur]["done"] += m.group(1) != " "
    return out


def parse_changelog(text: str) -> list[tuple[str, str]]:
    """[(version, date)] of every released heading, oldest first."""
    found = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})", text, re.M)
    return sorted(found, key=lambda v: tuple(int(x) for x in v[0].split(".")))


def merged_prs(text: str) -> set[int]:
    """PR numbers the TRACKER's Bitácora logs as merged."""
    body = text.split("## Bitácora", 1)[-1]
    out: set[int] = set()
    for line in body.splitlines():
        if line.startswith("- **") and re.search(r"merge(ad[oa]|d)\b", line):
            out.update(int(n) for n in re.findall(r"PR #(\d+)", line))
    return out


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_app(path: Path) -> dict[str, str]:
    out = {k: (path / rel).read_text(encoding="utf-8") for k, rel in APP_FILES.items()}
    out.update({k: (path / rel).read_text(encoding="utf-8") for k, rel in FACT_FILES.items() if (path / rel).is_file()})
    return out


def facts_drift(facts: dict, app: dict[str, str]) -> list[str]:
    """facts.json against the app's systems registry and credits list."""
    e: list[str] = []
    if "systems" in app:
        blocks_ = re.split(r"^\[\[system\]\][ \t]*$", app["systems"], flags=re.M)[1:]
        n = len(blocks_)
        if facts.get("systems") != n:
            e.append(f"facts.json systems is {facts.get('systems')}, the app has {n}")
        count: dict[str, int] = {}
        for block in blocks_:
            m = re.search(r'^family\s*=\s*"(\w+)"', block, re.M)
            fam = m.group(1) if m else "console"
            count[fam] = count.get(fam, 0) + 1
        if facts.get("families") != count:
            e.append(f"facts.json families {facts.get('families')} != the app's {count}")
    if "credits" in app:
        n = len(json.loads(app["credits"]).get("entries", []))
        if facts.get("credits") != n:
            e.append(f"facts.json credits is {facts.get('credits')}, the app lists {n}")
    return e


def read_remote() -> dict[str, str]:
    out = {}
    for k, rel in {**APP_FILES, **FACT_FILES}.items():
        url = f"https://api.github.com/repos/{REPO}/contents/{rel}?ref=main"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310 (fixed https host)
            out[k] = base64.b64decode(json.load(r)["content"]).decode("utf-8")
    return out


# ── validating ────────────────────────────────────────────────────────

def vkey(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


def pair(errors: list[str], where: str, obj: object) -> None:
    if not isinstance(obj, dict) or set(obj) - {"es", "en", "prs"} or \
            not all(isinstance(obj.get(k), str) and obj.get(k, "").strip() for k in ("es", "en")):
        errors.append(f"{where}: needs non-empty es and en text")


def validate(data: dict) -> list[str]:
    e: list[str] = []
    if data.get("schema") != 1:
        e.append("schema is not 1")
    src = data.get("source", {})
    for k in ("app_repo", "app_commit", "todo_sha256", "changelog_sha256", "tracker_sha256", "synced"):
        if not isinstance(src.get(k), str) or not src.get(k):
            e.append(f"source.{k} missing")
    rel = data.get("released", [])
    last = None
    for i, r in enumerate(rel):
        v, d = r.get("version", ""), r.get("date", "")
        if not SEMVER.match(v):
            e.append(f"released[{i}].version {v!r} is not x.y.z")
            continue
        try:
            dt.date.fromisoformat(d)
        except ValueError:
            e.append(f"released[{i}].date {d!r} is not an ISO date")
        if last and vkey(v) <= vkey(last):
            e.append(f"released[{i}] {v} is not newer than {last}")
        last = v
        if not r.get("items"):
            e.append(f"released {v} has no items")
        for j, it in enumerate(r.get("items", [])):
            pair(e, f"released {v} item {j}", it)
    un = data.get("unreleased", {})
    if not isinstance(un.get("after_pr"), int):
        e.append("unreleased.after_pr is not a number")
    for j, it in enumerate(un.get("items", [])):
        pair(e, f"unreleased item {j}", it)
    ids = [n.get("id") for n in data.get("next", [])]
    if len(set(ids)) != len(ids):
        e.append("next: an id appears twice")
    for n in data.get("next", []):
        w = f"next {n.get('id')}"
        if n.get("status") not in STATUS:
            e.append(f"{w}: status {n.get('status')!r} not in {sorted(STATUS)}")
        if not isinstance(n.get("public"), bool):
            e.append(f"{w}: public is not true or false")
        p = n.get("progress", {})
        if not (isinstance(p.get("done"), int) and isinstance(p.get("total"), int) and 0 <= p["done"] <= p["total"]):
            e.append(f"{w}: progress needs 0 <= done <= total")
        for a in n.get("after", []):
            if a not in ids:
                e.append(f"{w}: after {a!r} is not an id in next")
        # Copy is required even when not public: a block --update added
        # fails here until a person writes it (and decides public).
        pair(e, f"{w} title", n.get("title"))
        pair(e, f"{w} summary", n.get("summary"))
        if n.get("teaser") and not n.get("public"):
            e.append(f"{w}: a teaser must be public")
    if set(data.get("shipped", [])) & set(ids):
        e.append("an id is both shipped and in next")
    return e


def drift(data: dict, app: dict[str, str]) -> list[str]:
    """What the app says that the data file does not."""
    e: list[str] = []
    fix = "run make roadmap APP=<app> and review the diff"
    src = data["source"]
    for k in APP_FILES:
        if src.get(f"{k}_sha256") != sha256(app[k]):
            e.append(f"source.{k}_sha256: {APP_FILES[k]} changed in the app; {fix}")
    todo = parse_todo(app["todo"])
    known = {n["id"]: n for n in data["next"]}
    for tid, t in todo.items():
        if tid in data.get("shipped", []):
            if t["done"] != t["total"]:
                e.append(f"shipped {tid}: TODO has {t['done']} of {t['total']} done; move it back to next")
        elif tid not in known:
            e.append(f"TODO block {tid} ({t['title']}) is not in roadmap.json; {fix}")
        elif (known[tid]["progress"]["done"], known[tid]["progress"]["total"]) != (t["done"], t["total"]):
            p = known[tid]["progress"]
            e.append(f"next {tid}.progress is {p['done']}/{p['total']}, TODO says {t['done']}/{t['total']}; {fix}")
    for tid in list(known) + list(data.get("shipped", [])):
        if tid not in todo:
            e.append(f"{tid} is not a block of TODO.md any more")
    log = parse_changelog(app["changelog"])
    have = [(r["version"], r["date"]) for r in data["released"]]
    if have != log:
        e.append(f"released {have} != CHANGELOG {log}; {fix}")
    merged = {n for n in merged_prs(app["tracker"]) if n > data["unreleased"]["after_pr"]}
    missing = sorted(merged - set(data["unreleased"]["prs"]))
    if missing:
        e.append(f"TRACKER logs PR {', '.join('#%d' % n for n in missing)} merged after the last "
                 f"release; add it to unreleased.prs (and its items)")
    return e


# ── rendering ─────────────────────────────────────────────────────────

def esc(s: str) -> str:
    return html.escape(s, quote=False)


def nice_date(iso: str, lang: str) -> str:
    d = dt.date.fromisoformat(iso)
    m = MONTHS[lang][d.month - 1]
    return f"{d.day} de {m} de {d.year}" if lang == "es" else f"{d.day} {m} {d.year}"


def slots(done: int, total: int) -> str:
    """A row of mini slots: total of them (24 at most, scaled), done solid."""
    n = min(total, SLOTS) or 1
    k = round(done * n / total) if total else 0
    if done and not k:
        k = 1
    w = n * 9 - 3
    d = "".join(f"M{i * 9} 0h6v8h-6z" for i in range(k))
    o = "".join(f"M{i * 9 + .5} .5h5v7h-5z" for i in range(k, n))
    return (f'<svg class="art rm-bar" viewBox="0 0 {w} 8" width="{w}" height="8" aria-hidden="true" '
            f'focusable="false"><path class="rm-f" d="{d}"/><path class="rm-o" d="{o}"/></svg>')


def item(n: dict, lang: str, names: dict[str, str], level: str) -> str:
    w = WORDS[lang]
    p = n["progress"]
    after = ""
    if n.get("after"):
        after = f'<p class="rm-after">{w["after"]}: {esc(", ".join(names[a] for a in n["after"]))}.</p>'
    return (f'<li class="rm-item" data-id="{n["id"]}" data-status="{n["status"]}">'
            f'<{level}>{esc(n["title"][lang])}</{level}><p>{esc(n["summary"][lang])}</p>{after}'
            f'<p class="rm-state"><span class="rm-status">{STATUS[n["status"]][lang == "en"]}</span>'
            f'{slots(p["done"], p["total"])}<span class="rm-count">{p["done"]} {w["of"]} {p["total"]} {w["tasks"]}</span></p></li>')


def render(data: dict, lang: str, block: str) -> str:
    names = {n["id"]: n["title"][lang] for n in data["next"] if n.get("public")}
    if block == "teaser":
        rows = [item(n, lang, names, "h3") for n in data["next"] if n.get("teaser")]
        return '<ol class="rm-next rm-teaser">\n' + "\n".join(rows) + "\n</ol>"
    if block == "upcoming":
        rows = [item(n, lang, names, "h3") for n in data["next"] if n.get("public")]
        return '<ol class="rm-next">\n' + "\n".join(rows) + "\n</ol>"
    out = []
    for r in data["released"]:
        v = r["version"]
        lis = "".join(f"<li>{esc(i[lang])}</li>" for i in r["items"])
        out.append(f'<section class="rm-rel" aria-labelledby="v{v.replace(".", "-")}">'
                   f'<h3 id="v{v.replace(".", "-")}"><span class="rm-tag">v{v}</span> '
                   f'<time datetime="{r["date"]}">{nice_date(r["date"], lang)}</time></h3>'
                   f'<ul class="rm-done">{lis}</ul></section>')
    un = data["unreleased"]
    if un.get("items"):
        lis = "".join(f"<li>{esc(i[lang])}</li>" for i in un["items"])
        out.append(f'<section class="rm-rel rm-unrel" aria-labelledby="v-next"><h3 id="v-next">'
                   f'{WORDS[lang]["next"]}</h3><p>{WORDS[lang]["unreleased"]}</p>'
                   f'<ul class="rm-done">{lis}</ul></section>')
    return "\n".join(out)


def blocks(site: Path, data: dict, write: bool) -> list[str]:
    """Regenerate every roadmap block; the pages that differ (or are written)."""
    e: list[str] = []
    for rel, (lang, names) in PAGES.items():
        page = site / rel
        if not page.is_file():
            e.append(f"{rel} is missing")
            continue
        text = page.read_text(encoding="utf-8")
        new = text
        for name in names:
            pat = re.compile(rf"(<!-- roadmap:{name}:begin -->\n).*?(<!-- roadmap:{name}:end -->)", re.S)
            if not pat.search(new):
                e.append(f"{rel}: no roadmap:{name} block")
                continue
            new = pat.sub(lambda m: m.group(1) + render(data, lang, name) + "\n" + m.group(2), new)
        if new != text:
            if write:
                page.write_text(new, encoding="utf-8")
            else:
                e.append(f"{rel}: the roadmap blocks differ from roadmap.json (run make roadmap)")
    versions = {r["version"] for r in data["released"]}
    for rel in FEATURES:
        page = site / rel
        if page.is_file():
            for v in re.findall(r'data-since="([^"]*)"', page.read_text(encoding="utf-8")):
                if v != "next" and v not in versions:
                    e.append(f"{rel}: data-since={v!r} is not a released version or next")
    return e


# ── updating ──────────────────────────────────────────────────────────

def update(data: dict, app: dict[str, str], commit: str, site: Path, today: str) -> list[str]:
    """Fill the machine fields from the app. Returns notes for the person."""
    notes: list[str] = []
    data["source"].update({
        "app_commit": commit,
        "todo_sha256": sha256(app["todo"]),
        "changelog_sha256": sha256(app["changelog"]),
        "tracker_sha256": sha256(app["tracker"]),
        "synced": today,
    })
    log = parse_changelog(app["changelog"])
    have = {r["version"] for r in data["released"]}
    for v, d in log:
        for r in data["released"]:
            if r["version"] == v:
                r["date"] = d
    new = [(v, d) for v, d in log if v not in have]
    if new:
        v, d = new[-1]
        un = data["unreleased"]
        data["released"].append({"version": v, "date": d, "items": [
            {"es": i["es"], "en": i["en"]} for i in un.get("items", [])]})
        merged = merged_prs(app["tracker"])
        un.update({"after_pr": max(merged | {un["after_pr"]}), "prs": [], "items": []})
        for rel in FEATURES:
            page = site / rel
            if page.is_file():
                text = page.read_text(encoding="utf-8")
                text = re.sub(r'data-since="next">[^<]*<', f'data-since="{v}">v{v}<', text)
                page.write_text(text, encoding="utf-8")
        notes.append(f"moved unreleased into {v} ({d}); check its items")
    todo = parse_todo(app["todo"])
    known = {n["id"]: n for n in data["next"]}
    for tid, t in todo.items():
        if tid in data.get("shipped", []):
            continue
        if tid in known:
            known[tid]["progress"] = {"done": t["done"], "total": t["total"]}
        else:
            data["next"].append({"id": tid, "public": False, "status": "planned",
                                 "progress": {"done": t["done"], "total": t["total"]}, "after": [],
                                 "title": {"es": "", "en": ""}, "summary": {"es": "", "en": ""}})
            notes.append(f"new TODO block {tid} ({t['title']}): added as not public, write its copy")
    return notes


def dump(data: dict) -> str:
    """The file's own layout, so --update only touches what changed: two-space
    indent, lists of scalars on one line, and a dict of scalars (or scalar
    lists) on one line when it sits in a list or two levels down."""
    def j(v): return json.dumps(v, ensure_ascii=False)
    def scalar(v): return not isinstance(v, (dict, list))
    def flat(vs): return all(scalar(x) or (isinstance(x, list) and all(map(scalar, x))) for x in vs)

    def enc(v, ind: int = 0, in_list: bool = False) -> str:
        pad = "  " * ind
        if isinstance(v, dict):
            if flat(v.values()) and (in_list or ind >= 2):
                return "{ " + ", ".join(f"{j(k)}: {enc(x)}" for k, x in v.items()) + " }"
            body = ",\n".join(f"{pad}  {j(k)}: {enc(x, ind + 1)}" for k, x in v.items())
            return "{\n" + body + "\n" + pad + "}"
        if isinstance(v, list):
            if all(map(scalar, v)):
                return "[" + ", ".join(map(j, v)) + "]"
            return "[\n" + ",\n".join(f"{pad}  {enc(x, ind + 1, True)}" for x in v) + "\n" + pad + "]"
        return j(v)
    return enc(data) + "\n"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    p.add_argument("--check", action="store_true")
    p.add_argument("--app", type=Path)
    p.add_argument("--update", type=Path, metavar="APP")
    p.add_argument("--remote", action="store_true")
    p.add_argument("--write", action="store_true")
    p.add_argument("--data", type=Path, default=DATA)
    p.add_argument("--site", type=Path, default=SITE)
    p.add_argument("--facts", type=Path, default=FACTS)
    a = p.parse_args(argv)
    data = json.loads(a.data.read_text(encoding="utf-8"))
    if a.remote:
        try:
            app = read_remote()
            errs = validate(data) or drift(data, app) + facts_drift(json.loads(a.facts.read_text(encoding="utf-8")), app)
        except Exception as x:  # noqa: BLE001 (a warning, never a failed deploy)
            errs = [f"could not read the app from GitHub: {x}"]
        for m in errs:
            print(f"::warning::roadmap.json: {m}")
        print(f"roadmap: {len(errs)} warning(s) against {REPO}@main")
        return 0
    if a.update:
        app = read_app(a.update)
        run = subprocess.run(["git", "-C", str(a.update), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True)
        commit = run.stdout.strip() or data["source"]["app_commit"]
        for n in update(data, app, commit, a.site, dt.date.today().isoformat()):
            print(f"roadmap: {n}")
        a.data.write_text(dump(data), encoding="utf-8")
        errs = validate(data) + blocks(a.site, data, write=True)
        for m in errs:
            print(f"roadmap: {m}", file=sys.stderr)
        return 1 if errs else 0
    errs = validate(data)
    if not errs:
        errs = blocks(a.site, data, write=a.write)
        if a.app:
            app = read_app(a.app)
            errs += drift(data, app) + facts_drift(json.loads(a.facts.read_text(encoding="utf-8")), app)
    for m in errs:
        print(f"FAIL roadmap {m}")
    print(f"roadmap: {len(errs)} failure(s)" + (f" (against {a.app})" if a.app else ""))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
