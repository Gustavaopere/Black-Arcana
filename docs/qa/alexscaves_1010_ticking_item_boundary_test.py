#!/usr/bin/env python3
"""Replay exact inventory boundary and callback profiles."""
import hashlib
import json
import os
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"

class TickBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((DIR / "EXACT-TICKING-ITEM-BOUNDARY-1.0.10.json").read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_TICK_BOUNDARY"]).read_bytes()
        cls.report = json.loads(cls.raw)

    def test_report_and_annotation(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["report_sha256"])
        self.assertEqual(self.report["native_annotation"], self.seal["annotation"])
        text = str(self.report["native_annotation"]["annotations"])
        self.assertIn('value="HEAD"', text)
        self.assertIn("inventoryTick(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;IZ)V", text)
        self.assertNotIn("cancellable=true", text)

    def test_profiles(self):
        self.assertEqual(set(self.report["profiles"]), set(self.seal["profiles"]))
        for owner, expected in self.seal["profiles"].items():
            actual = self.report["profiles"][owner]
            for k in ("descriptor","code_sha256","instruction_sha256","instruction_count","returns"):
                self.assertEqual(actual[k], expected[k])
            self.assertEqual([{k:r[k] for k in ("offset","opcode","operand")} for r in actual["branches"]], expected["branches"])
            for name in ("constant","call","field"):
                self.assertEqual(len(actual[{"constant":"constants","call":"calls","field":"fields"}[name]]), expected[name+"_count"])

    def test_official_reference(self):
        for owner, group in self.seal["vanilla"].items():
            actual = self.report["vanilla"]["classes"][owner]
            self.assertEqual(actual["class_sha256"], group["class_sha256"])
            methods = {(m["named_method"], m["declaration"]["descriptor"]):m for m in actual["methods"]}
            self.assertEqual(len(methods), len(group["methods"]))
            for exp in group["methods"]:
                m=methods[(exp["name"],exp["descriptor"])]
                self.assertEqual(m["declaration"]["code_sha256"],exp["code_sha256"])
                self.assertEqual(m["instruction_sha256"],exp["instruction_sha256"])
        for p, exp in self.seal["neoforge"]["patches"].items():
            a=self.report["neoforge"]["patches"][p]
            self.assertEqual(a["present"],exp["present"])
            if exp["present"]:
                self.assertEqual(a["sha256"],exp["sha256"])
        inv=self.report["neoforge"]["patches"]["patches/net/minecraft/world/entity/player/Inventory.java.patch"]
        self.assertIn("this.selected == slot", "\n".join(x["text"] for x in inv["selected"]))

    def test_local_mutation_pivots_not_hooks(self):
        profiles=self.report["profiles"]
        def record(suffix):
            return next(v for k,v in profiles.items() if k.endswith("/"+suffix))
        club=record("PrimitiveClubItem")
        self.assertTrue(any(r["offset"]==50 and "swingTime:I" in r["symbol"] for r in club["fields"]))
        staff=record("SeaStaffItem")
        self.assertTrue(any(r["offset"]==85 and "Math.min:(II)I" in r["symbol"] for r in staff["calls"]))
        rad=record("RadioactiveItem")
        self.assertEqual(rad["instruction_sha256"],record("RadioactiveBlockItem")["instruction_sha256"])
        self.assertTrue(any(r["offset"]==126 and r["operand"]=="1800" for r in rad["constants"]))
        for k in ("scope","mutation","mutating_hook","physical_qa"):
            self.assertEqual(self.report[k],self.seal[k])

if __name__=="__main__":
    unittest.main()
