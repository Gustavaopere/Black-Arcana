#!/usr/bin/env python3
"""Check exact resources and the separately sealed Dark Arrow static contract."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAP = FAMILY / "EXACT-RESOURCE-MANIFEST-1.0.10.json"

class DamageTypeCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(SNAP.read_text(encoding="utf-8"))

    def test_exact_eleven_resource_cards(self):
        ids = set(self.manifest["damage_types"])
        actual = {x.stem.replace("-", "_") for x in FAMILY.glob("*.md")
                  if x.name not in {"INDEX.md", "README.md"}}
        self.assertEqual(ids, actual)
        self.assertEqual(11, len(ids))
        self.assertEqual(6, len(self.manifest["damage_type_tags"]))

    def test_literal_fields_and_direct_tag_memberships(self):
        for id, obj in self.manifest["damage_types"].items():
            with self.subTest(id=id):
                text = (FAMILY / (id.replace("_", "-") + ".md")).read_text(encoding="utf-8")
                self.assertIn("alexscaves:" + id, text)
                self.assertIn(obj["sha256"], text)
                for field in ("message_id", "scaling", "exhaustion"):
                    self.assertIn("| `" + field + "` | `" + str(obj["json"][field]) + "` |", text)
                for tag in self.manifest["direct_tag_entries"][id]:
                    self.assertIn("- `" + tag + "`", text)
                for deny in ("NOT_VERIFIED", "NOT_TESTED"):
                    self.assertIn(deny, text)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if id == "dark_arrow" else "NOT_CERTIFIED", text)
                self.assertIn("**+0 raízes mágicas novas**", text)

    def test_dark_arrow_static_certificate_has_a_sealed_card_and_runtime_limits(self):
        provider = FAMILY.parent
        manifest = json.loads((provider / "EXACT-DREADBOW-CONTRACTS-1.0.10.json").read_text())
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert = ledger["objects"]["✅-alexs-caves-continued/damage-types/dark-arrow.md"]
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(cert["version"], "1.0.10")
        self.assertEqual(cert["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"], "NOT_TESTED")
        self.assertEqual(manifest["cards"]["damage-types/dark-arrow.md"],
                         hashlib.sha256((FAMILY / "dark-arrow.md").read_bytes()).hexdigest())
        self.assertFalse(manifest["provider_universe_closed"])
        self.assertEqual(manifest["semantic_magic_roots"], 8)

    def test_dark_arrow_ambiguity_is_retained(self):
        a = self.manifest["damage_types"]["dark_arrow"]
        b = self.manifest["damage_types"]["desolate_dagger"]
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(a["json"]["message_id"], "desolate_dagger")
        text = (FAMILY / "dark-arrow.md").read_text(encoding="utf-8")
        self.assertIn("dois resource IDs diferentes", text)
        self.assertIn("message_id", text)

if __name__ == "__main__":
    unittest.main()
