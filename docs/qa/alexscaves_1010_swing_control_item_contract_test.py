#!/usr/bin/env python3
"""Replay exact reference and seven-axis certificate."""
import hashlib
import json
import os
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"

class SwingContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = json.loads((DIR / "EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        cls.raw = Path(os.environ["AC_SWING_BOUNDARY"]).read_bytes()
        cls.report = json.loads(cls.raw)

    def test_exact_reference(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.cert["boundary_report_sha256"])
        for owner, group in self.cert["reference"]["vanilla"].items():
            data = self.report["vanilla"]["classes"][owner]
            self.assertEqual(data["class_sha256"], group["class_sha256"])
            methods = {(m["named_method"], m["declaration"]["descriptor"]): m for m in data["methods"]}
            self.assertEqual(len(methods), len(group["methods"]))
            for exp in group["methods"]:
                m = methods[(exp["name"], exp["descriptor"])]
                self.assertEqual(m["declaration"]["code_sha256"], exp["code_sha256"])
                self.assertEqual(m["instruction_sha256"], exp["instruction_sha256"])
        for owner, group in self.cert["reference"]["neoforge"]["classes"].items():
            actual = self.report["neoforge"]["classes"][owner]
            self.assertEqual(actual["class_sha256"], group["class_sha256"])
            methods = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m for m in actual["methods"]}
            self.assertEqual(len(methods), len(group["methods"]))
            for exp in group["methods"]:
                m = methods[(exp["name"], exp["descriptor"])]
                self.assertEqual(m["instruction_sha256"], exp["instruction_sha256"])
        for p, exp in self.cert["reference"]["neoforge"]["patches"].items():
            data = self.report["neoforge"]["patches"][p]
            self.assertEqual(data["present"], exp["present"])
            if exp["present"]:
                self.assertEqual(data["sha256"], exp["sha256"])

    def test_dispatch_and_strength_pivots(self):
        neo = self.report["neoforge"]
        hook = neo["classes"]["net/neoforged/neoforge/common/CommonHooks"]["methods"][0]
        rows = {r["offset"]: r for r in hook["instructions"]}
        self.assertIn("IEventBus.post", rows[12]["symbol"])
        self.assertIn("Item.onLeftClickEntity", rows[47]["symbol"])
        self.assertEqual(rows[50]["opcode"], "ifne")
        self.assertIn("onPlayerAttackTarget", " ".join(x["text"] for x in neo["patches"]["patches/net/minecraft/world/entity/player/Player.java.patch"]["selected"]))
        self.assertIn("stack.onEntitySwing", " ".join(x["text"] for x in neo["patches"]["patches/net/minecraft/world/entity/LivingEntity.java.patch"]["selected"]))
        player = self.report["vanilla"]["classes"]["net.minecraft.world.entity.player.Player"]
        methods = {m["named_method"]: m for m in player["methods"]}
        self.assertEqual([r["opcode"] for r in methods["getCurrentItemAttackStrengthDelay"]["instructions"]][4:8], ["ddiv","ldc2_w","dmul","d2f"])

    def test_ledger_and_fail_closed(self):
        native = json.loads((DIR / "EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.json").read_text(encoding="utf8"))
        self.assertEqual(native["report_sha256"], self.cert["native_report_sha256"])
        self.assertEqual(native["artifact"], self.cert["artifact"])
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        item = ledger["objects"]["✅-alexs-caves-continued/systems/swing-control-item.md"]
        self.assertEqual(set(item["evidence"]), set(self.cert["axes"]))
        for k in ("claim_scope","evidence_grade","mutation","mutating_hook","physical_qa","perk_certification","runtime_dispatch","provider_universe_closed"):
            self.assertEqual(item[k], self.cert["claims"][k])

if __name__ == "__main__":
    unittest.main()
