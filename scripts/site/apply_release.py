#!/usr/bin/env python3
"""Fill the landing page in site/ with the published release, or with none.

Used by scripts/site/vercel_build.sh, the Vercel build of the landing
(vercel.json), so the landing follows every release on its own: nothing in site/ names a version, a date, a download link or a file
size. Those places carry markers instead, and this script copies site/ to an
output folder with every marker replaced from the release's GitHub API record
(GET /repos/<repo>/releases/latest). The generated folder is what Vercel
serves; it is never committed.

Plain standard-library Python, so the build needs nothing installed, and
scripts/site/check_site.py and release.test.mjs run it against
scripts/site/fixtures/release.json.

  apply_release.py --release-json F --repo OWNER/NAME --site DIR --out DIR
  apply_release.py --no-release     --repo OWNER/NAME --site DIR --out DIR

Blocks (in any text file, each comment on its own or inline):

  <!-- release:begin --> ... <!-- release:end -->
      kept, without the two comments, when there is a release; dropped
      with --no-release. Every {{release.*}} marker must sit in one.
  <!-- norelease:begin --> ... <!-- norelease:end -->
      the opposite: the "not published yet" state, kept only with
      --no-release.
  <!-- asset:<slot>:begin --> ... <!-- asset:<slot>:end -->
      (.html only) kept, without the two comments, when the release has
      the optional download <slot> (macos_intel, windows_arm,
      windows_arm_msi, cli_windows_arm64); dropped when it does not, and
      always before the first release. Every {{release.<slot>.*}} marker of
      an optional slot must sit in one, or the build fails as an unknown
      marker when the release lacks that file.
  <!-- noasset:<slot>:begin --> ... <!-- noasset:<slot>:end -->
      the opposite: kept only when the release lacks <slot> (the layout of
      releases up to v0.2.0). Asset blocks do not nest; they may hold
      release blocks or sit inside one.

Markers (in any .html, .txt, .webmanifest, .xml or .json file):

  {{release.version}}           0.1.0 (the tag without its "v")
  {{release.date}}              2026-11-02 (published_at, UTC)
  {{release.date_es}}           2 de noviembre de 2026
  {{release.date_en}}           2 November 2026
  {{release.notes_url}}         the release page
  {{release.sha256sums_url}}    the SHA256SUMS asset
  {{release.<file>.url}}        a download, <file> being a slot of DOWNLOADS
  {{release.<file>.name}}       its file name
  {{release.<file>.mib_en}}     its size in MiB, one decimal: 17.3
  {{release.<file>.mib_es}}     the same with a decimal comma: 17,3

Each download slot is resolved by name in two schemes: the release names
the app's stage-builds publishes (Coverly-ROMs_<v>_mac_arm.dmg,
coverly_<v>_linux_x64, ...) first, and the names releases up to v0.2.0 used
(Coverly.ROMs_<v>_universal.dmg, coverly-<v>-linux-x86_64, ...) second.
Optional slots (Intel Mac, Windows ARM64) exist only in the new scheme.

It fails, and so the deploy fails, when the release is a draft or a
pre-release, its tag is not v<SemVer>, any required download or SHA256SUMS
is missing, ambiguous (several files, or one in each naming scheme), empty
or not where the landing would link it, an asset block names no optional
download, is unbalanced, nested, malformed or outside an .html file, a marker is
unknown, left over or outside a release block, a block is unbalanced, a
download the release has is linked nowhere, or a JSON file or JSON-LD block no longer parses.
There is no flag to skip any of that: the landing never links a file that is
not there. --no-release only exists for the time before the first release
(vercel_build.sh uses it only when the API answers 404 for the latest release).
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

PRODUCT = "Coverly ROMs"

# Every download the landing offers: slot -> (required, patterns), {v} being
# the version. The first pattern is the release name the app repository's
# scripts/release/release_tools.py stage-builds publishes
# (Coverly-ROMs_<v>_<platform><kind>, coverly_<v>_<platform>[.exe]); the
# second, when there is one, is the name releases up to v0.2.0 used (Tauri's
# own, "Coverly ROMs" made "Coverly.ROMs"), matched with any safe prefix.
# Exactly one file must match across all of a slot's patterns, so a release
# carrying both schemes for one download is ambiguous and refused. Optional
# slots exist only in the new scheme; a page shows them through
# <!-- asset:<slot> --> blocks.
NEW = r"Coverly-ROMs_{v}_"
OLD = r"[A-Za-z0-9._-]+_{v}_"
DOWNLOADS: dict[str, tuple[bool, tuple[str, ...]]] = {
    "macos_arm": (True, (NEW + r"mac_arm\.dmg", OLD + r"universal\.dmg")),
    "macos_intel": (False, (NEW + r"mac_intel\.dmg",)),
    "windows_x64": (True, (NEW + r"windows_x64-setup\.exe", OLD + r"x64-setup\.exe")),
    "windows_x64_msi": (True, (NEW + r"windows_x64\.msi", OLD + r"x64_[A-Za-z0-9-]+\.msi")),
    "windows_arm": (False, (NEW + r"windows_arm-setup\.exe",)),
    "windows_arm_msi": (False, (NEW + r"windows_arm\.msi",)),
    "linux_x64_appimage": (True, (NEW + r"linux_x64\.AppImage", OLD + r"amd64\.AppImage")),
    "linux_x64_deb": (True, (NEW + r"linux_x64\.deb", OLD + r"amd64\.deb")),
    "linux_arm64_appimage": (True, (NEW + r"linux_arm\.AppImage", OLD + r"aarch64\.AppImage")),
    "linux_arm64_deb": (True, (NEW + r"linux_arm\.deb", OLD + r"arm64\.deb")),
    "cli_macos_arm64": (True, (r"coverly_{v}_mac_arm", r"coverly-{v}-darwin-aarch64")),
    "cli_macos_x64": (True, (r"coverly_{v}_mac_intel", r"coverly-{v}-darwin-x86_64")),
    "cli_windows_x64": (True, (r"coverly_{v}_windows_x64\.exe", r"coverly-{v}-windows-x86_64\.exe")),
    "cli_windows_arm64": (False, (r"coverly_{v}_windows_arm\.exe",)),
    "cli_linux_x64": (True, (r"coverly_{v}_linux_x64", r"coverly-{v}-linux-x86_64")),
    "cli_linux_arm64": (True, (r"coverly_{v}_linux_arm", r"coverly-{v}-linux-aarch64")),
}
ASSET_BLOCK = re.compile(r"<!--\s*(no)?asset:([a-z0-9_]+):(begin|end)\s*-->")
# Anything that looks like an asset block comment; what ASSET_BLOCK leaves
# of it is malformed (a typo would otherwise keep both layouts).
ASSET_COMMENT = re.compile(r"<!--\s*(no)?asset:", re.IGNORECASE)

SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MARKER = re.compile(r"\{\{\s*release\.([^}]*?)\s*\}\}")
LEFTOVER = re.compile(r"\{\{\s*release|release\.[a-z_.0-9]*\}\}")
BLOCK = re.compile(r"<!--\s*(no)?release:(begin|end)\s*-->")
TEXT_SUFFIXES = {".html", ".txt", ".webmanifest", ".xml", ".json"}
JSON_LD = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL
)

MONTHS_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
    "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
MONTHS_EN = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]


class ReleaseError(Exception):
    pass


def mib(size: int) -> str:
    return f"{size / (1024 * 1024):.1f}"


def values(release: dict, repo: str) -> dict[str, str]:
    """Every marker's value, after checking the release is one to link."""
    if release.get("draft") or release.get("prerelease"):
        raise ReleaseError("the release is a draft or a pre-release")
    tag = release.get("tag_name")
    if not isinstance(tag, str) or not tag.startswith("v"):
        raise ReleaseError(f"tag {tag!r} is not v<version>")
    version = tag[1:]
    if not SEMVER.match(version):
        raise ReleaseError(f"tag {tag!r} is not v<SemVer>")

    try:
        published = datetime.datetime.fromisoformat(
            str(release.get("published_at")).replace("Z", "+00:00")
        ).astimezone(datetime.timezone.utc)
    except ValueError as e:
        raise ReleaseError(f"published_at: {e}") from None

    base = f"https://github.com/{repo}/releases"
    notes = f"{base}/tag/{tag}"
    if release.get("html_url") != notes:
        raise ReleaseError(f"html_url {release.get('html_url')!r} is not {notes}")

    assets = [a for a in release.get("assets") or [] if isinstance(a, dict)]

    def asset(
        patterns: tuple[str, ...], label: str, required: bool = True
    ) -> tuple[str, str, int] | None:
        rxs = [re.compile(p.replace("{v}", re.escape(version))) for p in patterns]
        hits = []
        for rx in rxs:
            found = [a for a in assets if rx.fullmatch(str(a.get("name")))]
            if found:
                hits.append(found)
        if not hits:
            if not required:
                return None
            wanted = " or ".join(rx.pattern for rx in rxs)
            raise ReleaseError(f"{tag} has no asset for {label} ({wanted})")
        if len(hits) > 1 or len(hits[0]) > 1:
            names = ", ".join(sorted(str(a.get("name")) for f in hits for a in f))
            raise ReleaseError(f"{tag} has several assets for {label}: {names}")
        a = hits[0][0]
        name = str(a["name"])
        if a.get("state", "uploaded") != "uploaded":
            raise ReleaseError(f"{name} is {a.get('state')}, not uploaded")
        size = a.get("size")
        if not isinstance(size, int) or size <= 0:
            raise ReleaseError(f"{name} is empty")
        url = f"{base}/download/{tag}/{name}"
        if a.get("browser_download_url") != url:
            raise ReleaseError(
                f"{name} downloads from {a.get('browser_download_url')!r},"
                f" not {url}"
            )
        return name, url, size

    out = {
        "version": version,
        "date": published.strftime("%Y-%m-%d"),
        "date_es": (
            f"{published.day} de {MONTHS_ES[published.month - 1]}"
            f" de {published.year}"
        ),
        "date_en": (
            f"{published.day} {MONTHS_EN[published.month - 1]} {published.year}"
        ),
        "notes_url": notes,
    }
    sums = asset((r"SHA256SUMS",), "SHA256SUMS")
    assert sums is not None  # required
    out["sha256sums_url"] = sums[1]
    for label, (required, patterns) in DOWNLOADS.items():
        hit = asset(patterns, label, required)
        if hit is None:
            continue
        name, url, size = hit
        out[f"{label}.name"] = name
        out[f"{label}.url"] = url
        out[f"{label}.mib_en"] = mib(size)
        out[f"{label}.mib_es"] = mib(size).replace(".", ",")
    return out


def blocks(text: str, released: bool, where: str) -> str:
    """Keeps the blocks for this state (without their comments) and drops
    the others; a marker left outside a kept release block is an error."""
    out: list[str] = []
    pos = 0
    open_kind: str | None = None
    for m in BLOCK.finditer(text):
        kind = "norelease" if m.group(1) else "release"
        chunk = text[pos:m.start()]
        if m.group(2) == "begin":
            if open_kind is not None:
                raise ReleaseError(f"{where}: {kind}:begin inside {open_kind}")
            if MARKER.search(chunk):
                raise ReleaseError(f"{where}: a marker sits outside a release block")
            out.append(chunk)
            open_kind = kind
        else:
            if open_kind != kind:
                raise ReleaseError(f"{where}: {kind}:end without its begin")
            if kind == "norelease" and MARKER.search(chunk):
                raise ReleaseError(f"{where}: a marker sits in a norelease block")
            if (kind == "release") == released:
                out.append(chunk)
            open_kind = None
        pos = m.end()
    if open_kind is not None:
        raise ReleaseError(f"{where}: {open_kind}:begin is never closed")
    tail = text[pos:]
    if MARKER.search(tail):
        raise ReleaseError(f"{where}: a marker sits outside a release block")
    out.append(tail)
    return "".join(out)


def asset_blocks(text: str, vals: dict[str, str], where: str) -> str:
    """Keeps <!-- asset:<slot> --> blocks when that optional download is in
    the release and <!-- noasset:<slot> --> blocks when it is not (both
    without their comments). Before the first release no slot resolves."""
    out: list[str] = []
    pos = 0
    open_: tuple[bool, str] | None = None
    for m in ASSET_BLOCK.finditer(text):
        neg, slot, edge = bool(m.group(1)), m.group(2), m.group(3)
        if slot not in DOWNLOADS or DOWNLOADS[slot][0]:
            raise ReleaseError(f"{where}: {m.group(0)} names no optional download")
        chunk = text[pos:m.start()]
        if edge == "begin":
            if open_ is not None:
                raise ReleaseError(f"{where}: {m.group(0)} inside another asset block")
            out.append(chunk)
            open_ = (neg, slot)
        else:
            if open_ != (neg, slot):
                raise ReleaseError(f"{where}: {m.group(0)} without its begin")
            if (f"{slot}.url" in vals) != neg:
                out.append(chunk)
            open_ = None
        pos = m.end()
    if open_ is not None:
        kind = "noasset" if open_[0] else "asset"
        raise ReleaseError(f"{where}: {kind}:{open_[1]}:begin is never closed")
    out.append(text[pos:])
    new = "".join(out)
    if ASSET_COMMENT.search(new):
        raise ReleaseError(f"{where}: a malformed asset block comment is left over")
    return new


def render(text: str, vals: dict[str, str], where: str, used: set[str]) -> str:
    def one(m: re.Match) -> str:
        key = m.group(1)
        if key not in vals:
            raise ReleaseError(f"{where}: unknown marker {m.group(0)}")
        used.add(key)
        return vals[key]

    out = MARKER.sub(one, text)
    if LEFTOVER.search(out):
        raise ReleaseError(f"{where}: a malformed marker is left over")
    return out


def check_json(path: Path, text: str) -> None:
    try:
        if path.suffix in (".json", ".webmanifest"):
            json.loads(text)
        elif path.suffix == ".html":
            for block in JSON_LD.findall(text):
                json.loads(block)
    except json.JSONDecodeError as e:
        raise ReleaseError(f"{path}: no longer valid JSON: {e}") from None


def apply(release: dict | None, repo: str, site: Path, out: Path) -> dict[str, str]:
    """Copies site/ to out/ filled for `release` (None: not published yet)."""
    if not REPO.match(repo):
        raise ReleaseError(f"not an OWNER/NAME repository: {repo!r}")
    vals = values(release, repo) if release is not None else {}
    if not site.is_dir():
        raise ReleaseError(f"{site} is not a folder")
    if out.exists() and any(out.iterdir()):
        raise ReleaseError(f"{out} is not empty")
    if out.resolve().is_relative_to(site.resolve()):
        raise ReleaseError(f"{out} is inside {site}")
    shutil.copytree(site, out, dirs_exist_ok=True)

    used: set[str] = set()
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(out).as_posix()
        if ASSET_COMMENT.search(text) and path.suffix != ".html":
            raise ReleaseError(f"{rel}: asset blocks are only allowed in .html files")
        new = asset_blocks(text, vals, rel)
        new = blocks(new, release is not None, rel)
        new = render(new, vals, rel, used)
        check_json(path.relative_to(out), new)
        if new != text:
            path.write_text(new, encoding="utf-8")

    if release is not None:
        unused = [
            f"{label}.url"
            for label in DOWNLOADS
            if f"{label}.url" in vals and f"{label}.url" not in used
        ]
        if unused:
            raise ReleaseError(f"site/ never links {', '.join(unused)}")
    return vals


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--release-json", type=Path)
    src.add_argument(
        "--no-release",
        action="store_true",
        help="no release is published yet: keep the norelease blocks",
    )
    p.add_argument("--repo", required=True)
    p.add_argument("--site", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args(argv)
    try:
        release = None
        if a.release_json is not None:
            release = json.loads(a.release_json.read_text(encoding="utf-8"))
            if not isinstance(release, dict):
                raise ReleaseError("the release JSON is not an object")
        vals = apply(release, a.repo, a.site, a.out)
    except (OSError, json.JSONDecodeError, ReleaseError) as e:
        print(f"apply_release: {e}", file=sys.stderr)
        return 1
    if release is None:
        print(f"site/ filled for {PRODUCT} with no release published yet")
        return 0
    print(f"site/ filled with {PRODUCT} {vals['version']} ({vals['date']}):")
    for label in DOWNLOADS:
        if f"{label}.url" not in vals:
            continue
        print(f"  {vals[label + '.url']} ({vals[label + '.mib_en']} MiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
