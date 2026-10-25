#!/usr/bin/env python3
"""Test generator and checker agree without certifying undocumented perks."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import check_perk_ready_indexes as checker
import generate_perk_ready_indexes as generator

class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.root = self.repo / "wiki/modpack-catalog/providers"
        self.leaf = self.root / "✅-sample" / "skills" / "individual"
        self.leaf.mkdir(parents=True)
        (self.leaf / "air-dash.md").write_text("# Air Dash\n", encoding="utf8")
        self.meta = self.repo / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
        self.meta.parent.mkdir(parents=True)
        self.meta.write_text(json.dumps({
            "schema_version": 1, "objects": {}, "providers": {}, "known_rosters": {}
        }), encoding="utf8")
        self.patch1 = patch.object(checker, "PROVIDERS", self.root)
        self.patch2 = patch.object(checker, "LEDGER", self.meta)
        self.patch3 = patch.object(generator, "ROOT", self.root)
        self.patch1.start()
        self.patch2.start()
        self.patch3.start()

    def tearDown(self):
        self.patch3.stop()
        self.patch2.stop()
        self.patch1.stop()
        self.temp.cleanup()

    def render(self):
        ledger = checker.read_ledger(checker.LEDGER)
        dirs, mods, cards = checker.inventory()
        for folder in dirs:
            (folder / "INDEX.md").write_text(
                generator.directory_index(folder, dirs, cards, ledger), encoding="utf8")
        (self.root / "INDEX.md").write_text(
            generator.global_index(mods, cards, ledger), encoding="utf8")

    def test_generator_produces_full_hierarchy_and_check_passes(self):
        self.render()
        result = checker.check(self.repo)
        self.assertEqual([], result["problems"])
        self.assertEqual(4, result["expected_indexes"])
        self.assertEqual(1, result["candidate_cards"])
        self.assertIn("Air Dash", (self.root / "✅-sample/INDEX.md").read_text(encoding="utf8"))

    def test_new_card_detected_until_regenerated(self):
        self.render()
        (self.leaf / "wind-shield.md").write_text("# Wind Shield\n", encoding="utf8")
        self.assertNotEqual([], checker.check(self.repo)["problems"])
        self.render()
        result = checker.check(self.repo)
        self.assertEqual([], result["problems"])
        self.assertEqual(2, result["candidate_cards"])

    def test_legacy_green_name_never_certifies_mod(self):
        self.render()
        self.assertIn("0/1", (self.root / "INDEX.md").read_text(encoding="utf8"))
        self.assertIn("⚠️", (self.root / "✅-sample/INDEX.md").read_text(encoding="utf8"))

if __name__ == "__main__":
    unittest.main()
