#!/usr/bin/env python3
"""Tests for roadmap.py, against the small app in scripts/site/fixtures/app/.

  python3 -I scripts/site/roadmap_test.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE / "fixtures/app"
sys.dont_write_bytecode = True  # no __pycache__ in the working tree
_spec = importlib.util.spec_from_file_location("roadmap", HERE / "roadmap.py")
assert _spec is not None and _spec.loader is not None
rm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rm)


def text(n: int) -> dict[str, str]:
    return {"es": f"texto {n}", "en": f"text {n}"}


def data_for(app: dict[str, str]) -> dict:
    """A roadmap.json that matches the fixture app exactly."""
    return {
        "schema": 1,
        "source": {
            "app_repo": "MAECLY/coverly-roms", "app_commit": "abc1234",
            "todo_sha256": rm.sha256(app["todo"]), "changelog_sha256": rm.sha256(app["changelog"]),
            "tracker_sha256": rm.sha256(app["tracker"]), "synced": "2026-11-02",
        },
        "released": [
            {"version": "0.1.0", "date": "2026-10-17", "items": [text(1)]},
            {"version": "0.2.0", "date": "2026-10-25", "items": [text(2)]},
        ],
        "unreleased": {"after_pr": 27, "prs": [28, 31], "items": [dict(text(3), prs=[28])]},
        "shipped": ["1"],
        "next": [
            {"id": "2", "public": True, "teaser": True, "status": "almost",
             "progress": {"done": 2, "total": 5}, "after": [], "title": text(4), "summary": text(5)},
            {"id": "2.1", "public": True, "status": "blocked",
             "progress": {"done": 0, "total": 2}, "after": ["2"], "title": text(6), "summary": text(7)},
        ],
    }


PAGE = "<main>\n<!-- roadmap:{0}:begin -->\nstale\n<!-- roadmap:{0}:end -->\n</main>\n"


def site_for(root: Path) -> Path:
    site = root / "site"
    for rel, (_, names) in rm.PAGES.items():
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(PAGE.format(n) for n in names), encoding="utf-8")
    f = site / "features/index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('<span class="tag" data-since="0.1.0">v0.1.0</span>'
                 '<span class="tag" data-since="next">Próxima versión</span>', encoding="utf-8")
    return site


class ParseApp(unittest.TestCase):
    def setUp(self):
        self.app = rm.read_app(APP)

    def test_todo_counts_nested_boxes_and_subheadings_but_not_fences(self):
        todo = rm.parse_todo(self.app["todo"])
        self.assertEqual(sorted(todo), ["1", "2", "2.1"])
        self.assertEqual((todo["1"]["done"], todo["1"]["total"]), (2, 2))
        self.assertEqual((todo["2"]["done"], todo["2"]["total"]), (2, 5))
        self.assertEqual((todo["2.1"]["done"], todo["2.1"]["total"]), (0, 2))
        self.assertEqual(todo["2.1"]["title"], "Two point one")

    def test_changelog_versions_oldest_first_without_unreleased(self):
        self.assertEqual(rm.parse_changelog(self.app["changelog"]),
                         [("0.1.0", "2026-10-17"), ("0.2.0", "2026-10-25")])

    def test_merged_prs_only_from_the_log(self):
        self.assertEqual(rm.merged_prs(self.app["tracker"]), {3, 28, 31})


class Validate(unittest.TestCase):
    def setUp(self):
        self.app = rm.read_app(APP)
        self.data = data_for(self.app)

    def test_fixture_data_is_valid_and_in_sync(self):
        self.assertEqual(rm.validate(self.data), [])
        self.assertEqual(rm.drift(self.data, self.app), [])

    def test_refuses_bad_status_order_parity_and_after(self):
        d = copy.deepcopy(self.data)
        d["next"][0]["status"] = "soon"
        d["next"][1]["after"] = ["9"]
        d["next"][1]["title"] = {"es": "solo español", "en": ""}
        d["released"].reverse()
        d["next"][0]["progress"] = {"done": 7, "total": 5}
        errs = "\n".join(rm.validate(d))
        for want in ("status 'soon'", "after '9'", "title: needs non-empty es and en",
                     "is not newer than", "0 <= done <= total"):
            self.assertIn(want, errs)

    def test_a_block_without_copy_is_refused_even_when_private(self):
        d = copy.deepcopy(self.data)
        d["next"].append({"id": "3", "public": False, "status": "planned", "progress": {"done": 0, "total": 1},
                          "after": [], "title": {"es": "", "en": ""}, "summary": {"es": "", "en": ""}})
        self.assertTrue(any("next 3 title" in e for e in rm.validate(d)))


class Drift(unittest.TestCase):
    def setUp(self):
        self.app = rm.read_app(APP)
        self.data = data_for(self.app)

    def errs(self, app=None, data=None) -> str:
        return "\n".join(rm.drift(data or self.data, app or self.app))

    def test_progress_that_moved_in_todo(self):
        app = dict(self.app, todo=self.app["todo"].replace("- [ ] Under the ###.", "- [x] Under the ###."))
        e = self.errs(app=app)
        self.assertIn("next 2.progress is 2/5, TODO says 3/5", e)
        self.assertIn("source.todo_sha256", e)

    def test_a_new_todo_block_and_a_removed_one(self):
        app = dict(self.app, todo=self.app["todo"].replace("## 2.1. Two point one", "## 3. Three"))
        e = self.errs(app=app)
        self.assertIn("TODO block 3 (Three) is not in roadmap.json", e)
        self.assertIn("2.1 is not a block of TODO.md any more", e)

    def test_a_new_release_in_the_changelog(self):
        app = dict(self.app, changelog=self.app["changelog"].replace(
            "## [Unreleased]", "## [Unreleased]\n\n## [0.3.0] - 2026-11-20"))
        self.assertIn("CHANGELOG [('0.1.0', '2026-10-17'), ('0.2.0', '2026-10-25'), ('0.3.0', '2026-11-20')]",
                      self.errs(app=app))

    def test_a_merged_pr_missing_from_unreleased(self):
        app = dict(self.app, tracker=self.app["tracker"] + "- **2026-11-01** — PR #32 (systems) mergeado.\n")
        self.assertIn("TRACKER logs PR #32 merged after the last release", self.errs(app=app))

    def test_a_shipped_block_that_reopened(self):
        app = dict(self.app, todo=self.app["todo"].replace("- [x] Also done.", "- [ ] Also done."))
        self.assertIn("shipped 1: TODO has 1 of 2 done", self.errs(app=app))


class Facts(unittest.TestCase):
    def test_facts_match_the_systems_registry_and_credits(self):
        app = rm.read_app(APP)
        good = {"systems": 3, "credits": 2, "families": {"console": 1, "handheld": 1, "arcade": 1}}
        self.assertEqual(rm.facts_drift(good, app), [])
        bad = dict(good, systems=50, credits=1, families={"console": 3})
        e = "\n".join(rm.facts_drift(bad, app))
        for want in ("systems is 50, the app has 3", "credits is 1, the app lists 2", "families"):
            self.assertIn(want, e)


class Render(unittest.TestCase):
    def setUp(self):
        self.data = data_for(rm.read_app(APP))

    def test_slots_scale_past_24_and_show_any_progress(self):
        svg = rm.slots(1, 27)
        self.assertEqual(svg.count("h6v8h-6z"), 1)
        self.assertEqual(svg.count("h5v7h-5z"), 23)
        self.assertEqual(rm.slots(0, 3).count("h5v7h-5z"), 3)
        self.assertIn('aria-hidden="true" focusable="false"', svg)

    def test_teaser_upcoming_and_released(self):
        teaser = rm.render(self.data, "es", "teaser")
        self.assertIn('data-id="2"', teaser)
        self.assertNotIn('data-id="2.1"', teaser)
        up = rm.render(self.data, "en", "upcoming")
        self.assertIn("Waits for: text 4.", up)
        self.assertIn("Waiting on another block", up)
        self.assertIn("2 of 5 tasks", up)
        rel = rm.render(self.data, "es", "released")
        self.assertIn('<time datetime="2026-10-17">17 de octubre de 2026</time>', rel)
        self.assertIn("Próxima versión", rel)
        self.assertIn("25 October 2026", rm.render(self.data, "en", "released"))


class Pages(unittest.TestCase):
    def setUp(self):
        self.app = rm.read_app(APP)
        self.data = data_for(self.app)
        self.tmp = Path(tempfile.mkdtemp())
        self.site = site_for(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_stale_blocks_fail_until_written(self):
        errs = rm.blocks(self.site, self.data, write=False)
        self.assertEqual(len(errs), 4)
        self.assertEqual(rm.blocks(self.site, self.data, write=True), [])
        self.assertEqual(rm.blocks(self.site, self.data, write=False), [])

    def test_unknown_version_tag_on_features(self):
        f = self.site / "features/index.html"
        f.write_text(f.read_text() + '<span data-since="9.9.9">v9.9.9</span>', encoding="utf-8")
        rm.blocks(self.site, self.data, write=True)
        self.assertTrue(any("data-since='9.9.9'" in e for e in rm.blocks(self.site, self.data, write=False)))

    def test_update_moves_unreleased_into_a_new_version(self):
        app = dict(self.app,
                   changelog=self.app["changelog"].replace("## [Unreleased]", "## [Unreleased]\n\n## [0.3.0] - 2026-11-20"),
                   todo=self.app["todo"] + "\n## 4. Four\n\n- [ ] One.\n")
        notes = rm.update(self.data, app, "def5678", self.site, "2026-11-21")
        rel = self.data["released"][-1]
        self.assertEqual((rel["version"], rel["date"], rel["items"]), ("0.3.0", "2026-11-20", [text(3)]))
        self.assertEqual(self.data["unreleased"], {"after_pr": 31, "prs": [], "items": []})
        self.assertIn('data-since="0.3.0">v0.3.0<', (self.site / "features/index.html").read_text())
        added = self.data["next"][-1]
        self.assertEqual((added["id"], added["public"], added["progress"]), ("4", False, {"done": 0, "total": 1}))
        self.assertTrue(any("new TODO block 4" in n for n in notes))
        self.assertEqual(self.data["source"]["app_commit"], "def5678")
        self.assertEqual(rm.drift(self.data, app), [])
        # The new block has no copy yet: --check refuses it until a person writes it.
        self.assertTrue(rm.validate(self.data))

    def test_dump_keeps_the_committed_layout(self):
        # --update rewrites the file with dump(): it must not reflow every line.
        real = (HERE.parent.parent / "site/data/roadmap.json").read_text(encoding="utf-8")
        self.assertEqual(rm.dump(json.loads(real)), real)
        self.assertEqual(json.loads(rm.dump(self.data)), self.data)


if __name__ == "__main__":
    unittest.main(verbosity=1)
