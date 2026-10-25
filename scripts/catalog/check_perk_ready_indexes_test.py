#!/usr/bin/env python3
"""Synthetic ledger/index checks, including anti-false-green conditions."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import check_perk_ready_indexes as c

class IndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.mods = self.root / "wiki/modpack-catalog/providers"
        self.mod = self.mods / "✅-example"
        self.sub = self.mod / "spells"
        self.sub.mkdir(parents=True)
        (self.mod / "README.md").write_text("historical ✅ inventory\n", encoding="utf8")
        (self.sub / "fire-bolt.md").write_text("# Fire Bolt\n", encoding="utf8")
        (self.sub / "README.md").write_text("# Registry\n", encoding="utf8")
        self.manifest = self.root / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
        self.manifest.parent.mkdir(parents=True)
        self.ledger = {"schema_version": 1, "objects": {}, "providers": {}, "known_rosters": {}}
        self.save_manifest()
        self.write_indexes()

    def tearDown(self):
        self.tmp.cleanup()

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.ledger), encoding="utf8")

    def write_indexes(self, marker="⚠️", done=0, total=1):
        line = f"| {marker} | Fire Bolt | [ficha/fire-bolt.md](fire-bolt.md) |"
        (self.sub / "INDEX.md").write_text(
            f"**Homologadas para perks (somente fichas detectadas): {done}/{total}.**\n{line}\n", encoding="utf8")
        (self.mod / "INDEX.md").write_text(
            f"**Homologadas para perks (somente fichas detectadas): {done}/{total}.**\n"
            f"| {marker} | Fire Bolt | [spells/fire-bolt.md](spells/fire-bolt.md) |\n"
            "([navigation](spells/INDEX.md))\n", encoding="utf8")
        (self.mods / "INDEX.md").write_text(
            "**Mods com escopo integral certificado: 0/1.**\n"
            "| ⚠️ | Example | 1 | 0 | [Ver fichas](✅-example/INDEX.md) |\n", encoding="utf8")

    def test_valid_snapshot_with_warning(self):
        result = c.check(self.root)
        self.assertEqual([], result["problems"])
        self.assertEqual((2, 1, 1, 0),
                         (result["directories"], result["providers"], result["candidate_cards"],
                          result["certified_cards"]))

    def test_old_green_directory_is_not_perk_complete(self):
        result = c.check(self.root)
        self.assertEqual(0, result["certified_providers"])

    def test_missing_subfolder_index_rejected(self):
        (self.sub / "INDEX.md").unlink()
        self.assertTrue(any("missing subfolder" in x for x in c.check(self.root)["problems"]))

    def test_stale_denominator_rejected(self):
        self.write_indexes(total=2)
        self.assertTrue(any("denominator" in x for x in c.check(self.root)["problems"]))

    def test_false_green_item_rejected(self):
        self.write_indexes(marker="✅")
        self.assertTrue(any("wrong card status" in x for x in c.check(self.root)["problems"]))

    def test_missing_child_navigation_rejected(self):
        content = (self.mod / "INDEX.md").read_text(encoding="utf8")
        (self.mod / "INDEX.md").write_text(content.replace("(spells/INDEX.md)", "(other/INDEX.md)"),
                                            encoding="utf8")
        self.assertTrue(any("child-index" in x for x in c.check(self.root)["problems"]))

    def test_added_card_requires_index_refresh(self):
        (self.sub / "new-ability.md").write_text("# New Ability\n", encoding="utf8")
        self.assertTrue(any("denominator" in x for x in c.check(self.root)["problems"]))

    def test_documents_do_not_inflate_object_denominator(self):
        (self.sub / "TECHNICAL-MATRIX.md").write_text("# Evidence\n", encoding="utf8")
        self.assertEqual([], c.check(self.root)["problems"])

    def test_unproved_certificate_rejected(self):
        self.ledger["objects"] = {"✅-example/spells/fire-bolt.md": {"status": "COMPLETE_PERK_READY"}}
        self.save_manifest()
        with self.assertRaisesRegex(c.CatalogIndexError, "missing required"):
            c.check(self.root)

    def test_verified_card_requires_snapshot_update(self):
        self.ledger["objects"] = {"✅-example/spells/fire-bolt.md": {
            "status": "COMPLETE_PERK_READY",
            "evidence": {k: "reviewed evidence link" for k in c.REQUIRED_EVIDENCE},
        }}
        self.save_manifest()
        self.assertTrue(any("stale completion" in x for x in c.check(self.root)["problems"]))

    def test_provider_closed_requires_evidence(self):
        self.ledger["providers"] = {"✅-example": {"universe_closed": True}}
        self.save_manifest()
        with self.assertRaisesRegex(c.CatalogIndexError, "cannot close"):
            c.check(self.root)

    def test_duplicate_manifest_keys_rejected(self):
        self.manifest.write_text('{"schema_version":1,"objects":{},"objects":{},"providers":{}}', encoding="utf8")
        with self.assertRaisesRegex(c.CatalogIndexError, "duplicate JSON key"):
            c.check(self.root)

if __name__ == "__main__":
    unittest.main()
