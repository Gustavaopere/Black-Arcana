#!/usr/bin/env python3
"""Reproduce the ACFoods crosswalk against the independent native report."""
import hashlib
import json
import os
from pathlib import Path
import unittest

from alexscaves_1010_foods_probe import literal

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-FOODS-DISCOVERY-1.0.10.json"


class FoodsCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_FOODS_REPORT"]).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.native = cls.report["native"]

    def test_exact_identity(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["native_report_sha256"])
        self.assertEqual(self.report["artifact"], self.seal["artifact"])
        self.assertEqual(self.native["target_class_sha256"], self.seal["class_sha256"])
        self.assertEqual(self.native["class_entries_scanned"], 1555)

    def test_initializer_and_roster(self):
        self.assertEqual(self.native["initializer"]["instruction_count"], 606)
        self.assertEqual(self.native["builder_call_counts"], self.seal["builder_calls"])
        self.assertEqual(set(self.native["fields"]), {f["field"] for f in self.seal["fields"]})
        self.assertEqual(len(self.seal["fields"]), 63)
        self.assertEqual(len(self.native["supplier_methods"]) + 2, self.seal["declared_methods"])

    def test_every_configuration(self):
        for f in self.seal["fields"]:
            with self.subTest(field=f["field"]):
                native = self.native["configurations"][f["field"]]
                self.assertEqual(native["write_offset"], f["write_offset"])
                self.assertEqual(native["segment_sha256"], f["segment_sha256"])
                self.assertEqual(native["effects"], f["effects"])
                calls = native["builder_calls"]
                self.assertEqual(next(c["value"] for c in calls if c["name"] == "nutrition"), f["nutrition"])
                self.assertEqual(next(c["value"] for c in calls if c["name"] == "saturationMod"), f["saturation_modifier"])
                flags = [{k: v for k, v in c.items() if k in ("name", "argument")} for c in calls
                         if c["name"] not in ("of", "nutrition", "saturationMod", "build", "effect")]
                self.assertEqual(flags, f["flags"])

    def test_every_supplier(self):
        self.assertEqual(set(self.seal["suppliers"]), set(self.native["supplier_methods"]))
        for name, f in self.seal["suppliers"].items():
            with self.subTest(supplier=name):
                method = self.native["supplier_methods"][name]
                rows = method["instructions"]
                i = next(i for i, row in enumerate(rows) if row["opcode"] == "invokespecial"
                         and 'MobEffectInstance."<init>"' in row["symbol"])
                field = next(row["symbol"] for row in rows if row["opcode"] == "getstatic")
                self.assertEqual(field.removeprefix("Field ").split(":")[0], f["field"])
                self.assertEqual(literal(rows[i - 1]), f["ticks"])
                self.assertTrue(rows[i]["symbol"].endswith(":" + f["constructor"]))
                self.assertEqual(method["instruction_sha256"], f["instruction_sha256"])
                self.assertEqual(method["declaration"]["code_sha256"], f["code_sha256"])

    def test_consumer_crosswalk(self):
        actual = {}
        for owner, entry in self.native["consumers"].items():
            actual[owner] = [{**{k: m[k] for k in ("method", "descriptor", "instruction_sha256")},
                              "sites": [{k: s[k] for k in ("field", "offset", "opcode")} for s in m["sites"]]}
                             for m in entry["methods"]]
        self.assertEqual(actual, self.seal["consumers"])
        sites = [s for methods in actual.values() for m in methods for s in m["sites"]]
        self.assertEqual(len(sites), 121)
        self.assertEqual({s["field"] for s in sites}, set(self.native["fields"]))

    def test_counts_and_fail_closed(self):
        self.assertEqual(self.seal["counts"]["effect_fields"], sum(bool(f["effects"]) for f in self.seal["fields"]))
        self.assertEqual(self.seal["counts"]["suppliers"], sum(len(f["effects"]) for f in self.seal["fields"]))
        for k, v in {"mutation":"NO_MUTATION", "mutating_hook":"NOT_VERIFIED",
                     "physical_qa":"NOT_TESTED", "provider_universe_closed":False}.items():
            self.assertEqual(self.seal[k], v)
            self.assertEqual(self.report[k], v)
        self.assertEqual(self.seal["claim_scope"], "DISCOVERY_NOT_CERTIFIED")


if __name__ == "__main__":
    unittest.main()
