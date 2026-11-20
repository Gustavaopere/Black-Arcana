#!/usr/bin/env python3
"""Replay bounded ACRepairableItem discovery evidence."""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json"


class RepairableCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_REPAIRABLE_REPORT"]).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.native = cls.report["native"]

    def test_exact_report(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["report_sha256"])
        self.assertEqual(self.report["artifact"], self.seal["artifact"])
        for k in ("class_entries_scanned", "target_class_sha256", "target_access", "target_fields",
                  "target_methods", "direct_implementers", "inherited_implementers",
                  "in_jar_ancestors", "typed_census", "exact_member_refs"):
            self.assertEqual(self.native[k], self.seal[k])

    def test_method_hashes_and_calls(self):
        self.assertEqual(set(self.seal["owners"]), set(self.native["owners"]))
        for owner, entry in self.seal["owners"].items():
            data = self.native["owners"][owner]
            self.assertEqual(entry["class_sha256"], data["class_sha256"])
            methods = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m for m in data["methods"]}
            self.assertEqual(len(methods), len(entry["methods"]))
            for m in entry["methods"]:
                actual = methods[(m["name"], m["descriptor"])]
                self.assertEqual(actual["instruction_sha256"], m["instruction_sha256"])
                self.assertEqual(actual["instruction_count"], m["instruction_count"])
                rows = {r["offset"]: r for r in actual["instructions"]}
                for site in m["materials"]:
                    self.assertEqual(rows[site["offset"]]["opcode"], "getstatic")
                    self.assertIn(site["field"] + ":", rows[site["offset"]]["symbol"])
                for site in m["delegate_sites"]:
                    self.assertEqual(rows[site["offset"]]["opcode"], site["opcode"])
                    self.assertEqual(rows[site["offset"]]["symbol"], site["symbol"])

    def test_default_and_override(self):
        for suffix, expected in (("ACRepairableItem", "iconst_0"), ("DesolateDaggerItem", "iconst_1")):
            owner = next(k for k in self.native["owners"] if k.endswith("/" + suffix))
            body = next(m for m in self.native["owners"][owner]["methods"]
                        if m["declaration"]["name"] == "acReplacesTierRepairMaterials")
            self.assertEqual([r["opcode"] for r in body["instructions"]], [expected, "ireturn"])
        self.assertFalse(any(r["name"] == "acReplacesTierRepairMaterials"
                             for rs in self.native["exact_member_refs"].values() for r in rs))

    def test_fail_closed(self):
        for k, v in {"claim_scope": "DISCOVERY_NOT_CERTIFIED", "mutation": "NO_MUTATION",
                     "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
                     "provider_universe_closed": False}.items():
            self.assertEqual(self.seal[k], v)
            if k != "claim_scope":
                self.assertEqual(self.report[k], v)


if __name__ == "__main__":
    unittest.main()
