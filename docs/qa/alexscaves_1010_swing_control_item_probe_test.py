#!/usr/bin/env python3
"""Replay exact swing control discovery and local causal pivots."""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.json"


class SwingDiscovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_SWING_REPORT"]).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.native = cls.report["native"]

    def test_exact_report(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["report_sha256"])
        self.assertEqual(self.report["artifact"], self.seal["artifact"])
        for k in ("class_entries_scanned", "target_class_sha256", "target_access", "target_fields",
                  "target_methods", "direct_implementers", "inherited_implementers",
                  "in_jar_ancestors", "typed_census", "exact_member_refs"):
            self.assertEqual(self.native[k], self.seal[k])

    def test_method_crosswalk(self):
        self.assertEqual(set(self.native["owners"]), set(self.seal["owners"]))
        for owner, expected in self.seal["owners"].items():
            data = self.native["owners"][owner]
            self.assertEqual(data["class_sha256"], expected["class_sha256"])
            self.assertEqual(data["hierarchy"], expected["hierarchy"])
            actual = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m for m in data["methods"]}
            self.assertEqual(len(actual), len(expected["methods"]))
            for m in expected["methods"]:
                row = actual[(m["name"], m["descriptor"])]
                self.assertEqual(row["instruction_sha256"], m["instruction_sha256"])
                self.assertEqual(row["instruction_count"], m["instruction_count"])

    def test_predicate_pivots(self):
        owner = self.seal["direct_implementers"][0]
        methods = {m["declaration"]["name"]: {r["offset"]: r for r in m["instructions"]}
                   for m in self.native["owners"][owner]["methods"]}
        left = methods["onLeftClickEntity"]
        self.assertIn("getAttackStrengthScale", left[2]["symbol"])
        self.assertEqual(left[5]["opcode"], "f2d")
        self.assertEqual(left[6]["symbol"], "double 0.95d")
        self.assertEqual((left[9]["opcode"], left[10]["opcode"], left[19]["opcode"]), ("dcmpg", "iflt", "ifeq"))
        swing = methods["onEntitySwing"]
        self.assertEqual(swing[1]["opcode"], "instanceof")
        self.assertEqual((swing[18]["opcode"], swing[19]["opcode"], swing[27]["opcode"], swing[28]["opcode"]), ("fcmpg", "ifge", "fcmpl", "ifle"))
        self.assertEqual(swing[34]["opcode"], "iconst_m1")
        self.assertIn("swingTime:I", swing[35]["symbol"])
        self.assertEqual(swing[35]["opcode"], "putfield")

    def test_fail_closed(self):
        for k, v in {"scope": "DISCOVERY_NOT_CERTIFIED", "mutation": "NO_MUTATION",
                     "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
                     "provider_universe_closed": False}.items():
            self.assertEqual(self.seal[k], v)
            self.assertEqual(self.report[k], v)


if __name__ == "__main__":
    unittest.main()
