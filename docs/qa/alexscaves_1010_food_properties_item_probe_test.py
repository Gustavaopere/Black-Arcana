#!/usr/bin/env python3
"""Regression assertions for the bounded empty-marker disposition."""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-FOOD-PROPERTIES-ITEM-MARKER-1.0.10.json"


class MarkerDisposition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_FOOD_PROPERTIES_REPORT"]).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.native = cls.report["native"]

    def test_exact_report(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["native_report_sha256"])
        self.assertEqual(self.report["artifact"], self.seal["artifact"])

    def test_empty_declaration(self):
        self.assertEqual(self.native["target"], self.seal["target"])
        self.assertEqual(self.native["target_class_sha256"], self.seal["target_class_sha256"])
        self.assertEqual(self.native["target_access"], 1537)
        self.assertEqual(self.native["target_fields"], [])
        self.assertEqual(self.native["target_methods"], [])

    def test_whole_jar_census(self):
        self.assertEqual(self.native["class_entries_scanned"], self.seal["class_entries_scanned"])
        self.assertEqual(self.native["direct_implementers"], self.seal["direct_implementers"])
        self.assertEqual(self.native["inherited_implementers"], [])
        self.assertEqual(set(self.native["typed_census"]),
                         {self.seal["target"], *self.seal["direct_implementers"]})
        self.assertEqual(self.native["exact_member_refs"], {})

    def test_implementer_not_independent_marker_behavior(self):
        owners = self.native["owners"]
        target = owners[self.seal["target"]]
        self.assertEqual(target["methods"], [])
        impl = self.seal["direct_implementers"][0]
        parent = owners[impl]["hierarchy"]["parent"]
        self.assertTrue(parent.endswith("/CaveInfoItem"))
        self.assertEqual(len(owners[impl]["methods"]), 8)
        self.assertEqual(len(owners[parent]["methods"]), 7)
        self.assertEqual(self.seal["disposition"], "EMPTY_MARKER_SUPPORT_ONLY")
        self.assertEqual(self.seal["additional_cards"], 0)
        self.assertEqual(self.seal["semantic_magic_roots_added"], 0)

    def test_fail_closed(self):
        for key, value in {"mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
                           "physical_qa": "NOT_TESTED", "provider_universe_closed": False}.items():
            self.assertEqual(self.seal[key], value)
            self.assertEqual(self.report[key], value)
        self.assertEqual(self.seal["perk_certification"], "NOT_CERTIFIED")


if __name__ == "__main__":
    unittest.main()
