#!/usr/bin/env python3
"""Tests for systems.py: the path rounding, the maker table, the grouping,
the blocks and the checks, on the files in site/ and small made-up data.

  python3 -I scripts/site/systems_test.py
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
SITE = HERE.parents[1] / "site"
sys.dont_write_bytecode = True  # no __pycache__ in the working tree
_spec = importlib.util.spec_from_file_location("systems", HERE / "systems.py")
assert _spec is not None and _spec.loader is not None
sy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sy)


def row(sid: str, fam: str, mk: str | None, icon: bool = True, name: str | None = None) -> dict:
    return {"id": sid, "name": name or sid.upper(), "short": name or sid.upper(), "family": fam, "maker": mk, "keys": [sid],
            "icon": icon, "abbr": None if icon else sid.upper()[:4]}


class RoundPath(unittest.TestCase):
    def test_rounds_and_keeps_compact_numbers_apart(self):
        self.assertEqual(sy.round_path("m58.446 24.601.003-.007"), "m58.4 24.6 0 0")
        self.assertEqual(sy.round_path("M1.26 2.04L3.96.5"), "M1.3 2L4 .5")

    def test_arc_flags_stay_flags(self):
        # svgo may pack the flags against the next number ("0 012 2").
        self.assertEqual(sy.round_path("a2 2 0 012.04 2"), "a2 2 0 0 1 2 2")
        self.assertEqual(sy.round_path("a.96.96 0 0 0-.723-1.152"), "a1 1 0 0 0-.7-1.2")

    def test_implicit_lineto_after_moveto(self):
        self.assertEqual(sy.round_path("m0 0 1.04 1.04 2 2z"), "m0 0 1 1 2 2z")

    def test_bad_data_raises(self):
        with self.assertRaises(ValueError):
            sy.round_path("M1 x")

    def test_fmt(self):
        self.assertEqual([sy.fmt(x) for x in (0.04, -0.04, 0.5, -0.55, 12.0)], ["0", "0", ".5", "-.6", "12"])


class Makers(unittest.TestCase):
    def test_libretro_prefix(self):
        self.assertEqual(sy.maker("gba", "Nintendo - Game Boy Advance"), "Nintendo")

    def test_table_wins(self):
        self.assertEqual(sy.maker("sufami", "Nintendo - Sufami Turbo"), "Bandai")
        self.assertEqual(sy.maker("msx", "Microsoft - MSX"), "MSX")
        self.assertEqual(sy.maker("switch", None), "Nintendo")

    def test_no_maker(self):
        self.assertIsNone(sy.maker("mame", "MAME"))
        self.assertIsNone(sy.maker("doom", "DOOM"))
        self.assertIsNone(sy.maker("solarus", None))

    def test_short(self):
        self.assertEqual(sy.short("psx", "Sony PlayStation", "Sony"), "PlayStation")
        self.assertEqual(sy.short("megadrive", "Sega Mega Drive / Genesis", "Sega"), "Mega Drive")
        self.assertEqual(sy.short("n64", "Nintendo 64", "Nintendo"), "Nintendo 64")
        self.assertEqual(sy.short("nds", "Nintendo DS", "Nintendo"), "Nintendo DS")
        self.assertEqual(sy.short("msxturbor", "MSX turbo R", "MSX"), "MSX turbo R")
        self.assertEqual(sy.short("nes", "Nintendo Entertainment System", "Nintendo"), "NES")

    def test_keys(self):
        self.assertEqual(sy.keys("gba", "Game Boy Advance", ["GBA", "gameboyadvance"]), ["gba"])
        self.assertEqual(sy.keys("wii", "Nintendo Wii", ["WII"]), [])
        self.assertEqual(sy.keys("snes", "Super Nintendo", ["SFC", "snes", "Super Nintendo", "a", "b"]),
                         ["snes", "sfc", "a"])


class Groups(unittest.TestCase):
    rows = [row("a", "console", "Sega"), row("b", "console", "Nintendo"), row("c", "console", "Sega"),
            row("d", "console", "Coleco"), row("e", "arcade", "Capcom", name="Zed"),
            row("f", "arcade", None, name="alpha")]

    def test_makers_with_two_or_more_then_the_rest(self):
        g = sy.groups(self.rows, "console")
        self.assertEqual([(m, [r["id"] for r in rs]) for m, rs in g], [("Sega", ["a", "c"]), (None, ["b", "d"])])

    def test_arcade_is_alphabetical_and_flat(self):
        g = sy.groups(self.rows, "arcade")
        self.assertEqual([(m, [r["id"] for r in rs]) for m, rs in g], [(None, ["f", "e"])])

    def test_render_marks_icons_and_abbreviations(self):
        data = {"systems": [row("gba", "handheld", "Nintendo"), row("cps1", "arcade", "Capcom", icon=False)]}
        out = sy.render(data, "en")
        self.assertIn('<i data-i="gba"></i>GBA</li>', out)
        self.assertIn('<li data-k="cps1 capcom"><i data-a="CPS1"></i>CPS1</li>', out)
        self.assertIn('data-fact="families.handheld">1</span>', out)
        self.assertIn("<h5>Other makers", out)


class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for rel in ("index.html", "en/index.html", "data/systems.json", "data/facts.json", "assets/art/systems.svg"):
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(SITE / rel, self.tmp / rel)
        self.data = json.loads((self.tmp / "data/systems.json").read_text(encoding="utf-8"))
        self.sprite = (self.tmp / "assets/art/systems.svg").read_text(encoding="utf-8")
        self.facts = json.loads((self.tmp / "data/facts.json").read_text(encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_site_passes(self):
        self.assertEqual(sy.validate(self.data, self.sprite, self.facts), [])
        self.assertEqual(sy.blocks(self.tmp, self.data, write=False), [])
        self.assertEqual(sy.main(["--check", "--site", str(self.tmp)]), 0)

    def test_missing_symbol_fails(self):
        sprite = self.sprite.replace('<symbol id="gba"', '<symbol id="gbx"')
        self.assertTrue(any("symbols" in e for e in sy.validate(self.data, sprite, self.facts)))

    def test_facts_mismatch_fails(self):
        facts = copy.deepcopy(self.facts)
        facts["systems"] += 1
        self.assertTrue(any("facts.json systems" in e for e in sy.validate(self.data, self.sprite, facts)))

    def test_edited_list_fails_and_write_fixes_it(self):
        page = self.tmp / "en/index.html"
        page.write_text(page.read_text(encoding="utf-8").replace(">Game Boy Advance<", ">GBA<"), encoding="utf-8")
        self.assertTrue(sy.blocks(self.tmp, self.data, write=False))
        sy.blocks(self.tmp, self.data, write=True)
        self.assertEqual(sy.blocks(self.tmp, self.data, write=False), [])

    def test_renamed_system_in_json_fails_the_block(self):
        data = copy.deepcopy(self.data)
        data["systems"][0]["name"] += " (renamed)"
        self.assertTrue(sy.blocks(self.tmp, data, write=False))


if __name__ == "__main__":
    unittest.main(verbosity=1)
