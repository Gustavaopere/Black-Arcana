#!/usr/bin/env python3
"""Replay additional tick reference and scoped certificate."""
import hashlib
import json
import os
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
class TickContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert=json.loads((DIR/"EXACT-TICKING-ITEM-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        cls.raw=Path(os.environ["AC_TICK_EXTRA"]).read_bytes()
        cls.report=json.loads(cls.raw)
    def test_extra_report(self):
        exp=self.cert["extra"]
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),exp["report_sha256"])
        self.assertEqual(self.report["native"]["constructor_refs"],exp["native"]["constructor_refs"])
        for owner,group in exp["native"]["classes"].items():
            a=self.report["native"]["classes"][owner]
            for k in ("class_sha256","parent","fields"):self.assertEqual(a[k],group[k])
            self.assertEqual([{k:m[k] for k in ("declaration","instruction_sha256","instruction_count")} for m in a["methods"]],group["methods"])
        for owner,group in exp["vanilla"].items():
            a=self.report["vanilla"]["classes"][owner]
            self.assertEqual(a["class_sha256"],group["class_sha256"])
            ms={(m["named_method"],m["declaration"]["descriptor"]):m for m in a["methods"]}
            self.assertEqual(len(ms),len(group["methods"]))
            for m in group["methods"]:
                self.assertEqual(ms[(m["name"],m["descriptor"])]["instruction_sha256"],m["instruction_sha256"])
                self.assertEqual(ms[(m["name"],m["descriptor"])]["declaration"]["code_sha256"],m["code_sha256"])
    def test_engine_and_hazmat_pivots(self):
        classes=self.report["vanilla"]["classes"]
        player=classes["net.minecraft.world.entity.player.Player"]["methods"][0]
        self.assertTrue(any(r["offset"]==153 and "net.minecraft.world.entity.player.Inventory.tick" in r["named_candidates"] for r in player["refs"]))
        inv=classes["net.minecraft.world.entity.player.Inventory"]["methods"][0]
        rows={r["offset"]:r for r in inv["instructions"]}
        self.assertEqual(rows[5]["operand"],"36")
        self.assertEqual(rows[17]["opcode"],"iconst_4")
        self.assertEqual(rows[28]["opcode"],"iconst_1")
        setter=next(m for m in classes["net.minecraft.world.item.ItemStack"]["methods"] if m["named_method"]=="setDamageValue")
        self.assertTrue(any(r["offset"]==10 and "net.minecraft.util.Mth.clamp" in r["named_candidates"] for r in setter["refs"]))
        self.assertTrue(any(r["offset"]==16 and "net.minecraft.world.item.ItemStack.set" in r["named_candidates"] for r in setter["refs"]))
        haz=next(v for k,v in self.report["native"]["classes"].items() if k.endswith("/HazmatArmorItem"))
        self.assertEqual([r["offset"] for r in haz["methods"][0]["instructions"] if r["opcode"]=="iinc"],[26,53,80,107])
    def test_ledger_and_all_reports(self):
        n=json.loads((DIR/"EXACT-TICKING-ITEM-DISCOVERY-1.0.10.json").read_text(encoding="utf8"))
        b=json.loads((DIR/"EXACT-TICKING-ITEM-BOUNDARY-1.0.10.json").read_text(encoding="utf8"))
        self.assertEqual(n["report_sha256"],self.cert["native_report_sha256"])
        self.assertEqual(b["report_sha256"],self.cert["boundary_report_sha256"])
        self.assertEqual(n["direct_implementers"],self.cert["direct_implementers"])
        self.assertEqual(n["inherited_implementers"],self.cert["inherited_implementers"])
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        item=ledger["objects"]["✅-alexs-caves-continued/systems/ticking-item.md"]
        self.assertEqual(set(item["evidence"]),set(self.cert["axes"]))
        for k in ("claim_scope","evidence_grade","mutation","mutating_hook","physical_qa","perk_certification","runtime_dispatch","provider_universe_closed"):
            self.assertEqual(item[k],self.cert["claims"][k])
if __name__=="__main__":unittest.main()
