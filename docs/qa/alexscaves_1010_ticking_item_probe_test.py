#!/usr/bin/env python3
"""Replay native tick discovery and complete selected member callsite crosswalk."""
import hashlib
import json
import os
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TICKING-ITEM-DISCOVERY-1.0.10.json"

class TickDiscovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_TICK_REPORT"]).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.native = cls.report["native"]

    def test_exact_report(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["report_sha256"])
        self.assertEqual(self.report["artifact"], self.seal["artifact"])
        for k in ("mixin_summary","class_entries_scanned","target_class_sha256","target_access","target_fields","target_methods","direct_implementers","inherited_implementers","in_jar_ancestors","typed_census","exact_member_refs"):
            self.assertEqual(self.native[k], self.seal[k])

    def test_method_and_callsite_crosswalk(self):
        self.assertEqual(set(self.native["owners"]), set(self.seal["owners"]))
        for owner, exp in self.seal["owners"].items():
            data = self.native["owners"][owner]
            self.assertEqual(data["class_sha256"], exp["class_sha256"])
            self.assertEqual(data["hierarchy"], exp["hierarchy"])
            methods = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m for m in data["methods"]}
            self.assertEqual(len(methods), len(exp["methods"]))
            for m in exp["methods"]:
                actual = methods[(m["name"], m["descriptor"])]
                self.assertEqual(actual["instruction_sha256"], m["instruction_sha256"])
                self.assertEqual(actual["instruction_count"], m["instruction_count"])
                for key, predicate in (("calls", lambda r: r["opcode"].startswith("invoke")),
                                       ("writes", lambda r: r["opcode"] in ("putfield","putstatic"))):
                    rows = [{k:r[k] for k in ("offset","opcode","symbol")} for r in actual["instructions"] if predicate(r)]
                    self.assertEqual(rows, m[key])

    def test_dispatch_and_inheritance(self):
        owner = next(k for k in self.native["owners"] if k.endswith("/ItemStackTickMixin"))
        method = self.native["owners"][owner]["methods"][0]
        rows = {r["offset"]:r for r in method["instructions"]}
        self.assertEqual(rows[15]["opcode"],"instanceof")
        self.assertEqual(rows[18]["operand"],"41")
        self.assertEqual(rows[23]["opcode"],"checkcast")
        self.assertEqual(rows[36]["opcode"],"invokeinterface")
        self.assertIn("ACTickingItem.acInventoryTick",rows[36]["symbol"])
        self.assertEqual(len(self.native["direct_implementers"]),17)
        self.assertEqual(len(self.native["inherited_implementers"]),1)
        inherited = self.native["owners"][self.native["inherited_implementers"][0]]
        self.assertTrue(inherited["hierarchy"]["parent"].endswith("/RadioactiveBlockItem"))
        self.assertFalse(any(m["name"]=="acInventoryTick" for m in inherited["declarations"]))

    def test_fail_closed(self):
        for k,v in {"scope":"DISCOVERY_NOT_CERTIFIED","mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}.items():
            self.assertEqual(self.seal[k],v)
            self.assertEqual(self.report[k],v)

if __name__ == "__main__":
    unittest.main()
