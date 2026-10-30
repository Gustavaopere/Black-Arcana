#!/usr/bin/env python3
"""Check exact resources and the separately sealed Acid/Dark Arrow contracts."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAP = FAMILY / "EXACT-RESOURCE-MANIFEST-1.0.10.json"
STATIC_CONTRACTS = {
    "acid": {
        "manifest": "EXACT-ACID-CONTRACT-1.0.10.json",
        "family": "ACID_DAMAGE_CONTRACT",
        "cards": frozenset({"damage-types/acid.md"}),
    },
    "dark_arrow": {
        "manifest": "EXACT-DREADBOW-CONTRACTS-1.0.10.json",
        "family": "DREADBOW_AND_DARK_ARROW",
        "cards": frozenset({"damage-types/dark-arrow.md", "equipment/dreadbow.md"}),
    },
}

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
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if id in STATIC_CONTRACTS else "NOT_CERTIFIED", text)
                self.assertIn("**+0 raízes mágicas novas**", text)

    def test_two_static_certificates_have_sealed_cards_and_runtime_limits(self):
        provider = FAMILY.parent
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        self.assertEqual(set(STATIC_CONTRACTS), {"acid", "dark_arrow"})
        for id, scope in STATIC_CONTRACTS.items():
            with self.subTest(id=id):
                manifest = json.loads((provider / scope["manifest"]).read_text())
                relative = "damage-types/" + id.replace("_", "-") + ".md"
                cert = ledger["objects"][provider.name + "/" + relative]
                for evidence in (cert, manifest):
                    self.assertEqual(evidence["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
                    self.assertEqual(evidence["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
                    self.assertEqual(evidence["version"], "1.0.10")
                    self.assertEqual(evidence["mutating_hook"], "NOT_VERIFIED")
                    self.assertEqual(evidence["physical_qa"], "NOT_TESTED")
                    self.assertEqual(evidence["artifact_sha1"], self.manifest["artifact"]["sha1"])
                self.assertEqual(cert["status"], "COMPLETE_PERK_READY")
                self.assertEqual(manifest["catalog_family"], scope["family"])
                self.assertEqual(set(manifest["cards"]), scope["cards"])
                self.assertEqual(set(manifest["contract_evidence"]), scope["cards"])
                self.assertEqual(manifest["cards"][relative],
                                 hashlib.sha256((provider / relative).read_bytes()).hexdigest())
                resource = "data/alexscaves/damage_type/" + id + ".json"
                self.assertEqual(manifest["resources"][resource], self.manifest["damage_types"][id]["sha256"])
                self.assertIn(resource, manifest["contract_evidence"][relative]["resources"])
                self.assertFalse(manifest["provider_universe_closed"])
                self.assertEqual(manifest["semantic_magic_roots"], 8)

    def test_other_nine_damage_types_remain_uncertified(self):
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        remaining = set(self.manifest["damage_types"]) - set(STATIC_CONTRACTS)
        self.assertEqual(len(remaining), 9)
        for id in remaining:
            with self.subTest(id=id):
                relative = FAMILY.parent.name + "/damage-types/" + id.replace("_", "-") + ".md"
                self.assertNotIn(relative, ledger["objects"])

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
