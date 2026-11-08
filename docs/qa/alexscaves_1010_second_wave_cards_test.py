#!/usr/bin/env python3
"""Seal Second Wave 1.0.10 scoped static behaviors; no perk hook/physical QA."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
DOC=P/"EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json"
CARD=P/"enchantments/second-wave.md"
OBJ="✅-alexs-caves-continued/enchantments/second-wave.md"

class SecondWaveStaticCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DOC.read_text(encoding="utf8"))
        cls.card=CARD.read_text(encoding="utf8")
        cls.ins={}
        for label in ("pivot_windows","flow_windows"):
            for win in cls.data["release_using"][label]:
                for inst in win["instructions"]:
                    o=inst["offset"]
                    if o in cls.ins and cls.ins[o]!=inst:
                        raise AssertionError("conflicting exact JVM windows at "+str(o))
                    cls.ins[o]=inst
        for inst in cls.data["release_using"]["selected_block_operands"]:
            o=inst["offset"]
            if o in cls.ins and cls.ins[o]!=inst:
                raise AssertionError("inconsistent opcode census")
            cls.ins[o]=inst
    def pivot(self, offset, op=None, symbol=None, operand=None):
        inst=self.ins[offset]
        if op is not None: self.assertEqual(inst["opcode"],op)
        if symbol is not None: self.assertIn(symbol,inst["symbol"])
        if operand is not None: self.assertEqual(inst["operand"],str(operand))
        return inst
    def test_publisher_identity_provenance_and_universe(self):
        d=self.data
        self.assertEqual(d["scope"],"SECOND_WAVE_1010_BOUNDED_READONLY_DISCOVERY")
        self.assertEqual(d["enchantment"]["id"],"alexscaves:second_wave")
        self.assertEqual(d["enchantment"]["sha256"],
            "68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c")
        j=d["enchantment"]["json"]
        self.assertEqual(j["max_level"],1)
        self.assertEqual(j["weight"],2)
        self.assertEqual(j["min_cost"],{"base":1,"per_level_above_first":12})
        self.assertEqual(j["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(j["exclusive_set"],["alexscaves:tsunami"])
        self.assertEqual(j["slots"],["mainhand"])
        self.assertEqual(d["item_tag"]["json"]["values"],["alexscaves:ortholance"])
        scan=d["provider_class_census"]
        self.assertEqual(scan["classfiles_scanned"],1555)
        self.assertEqual(scan["constant_pool_class_hits"],[
          "com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class",
          "com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class"])
    def test_full_method_fingerprint_and_positive_level_gate(self):
        m=self.data["release_using"]
        self.assertEqual(m["instruction_count"],435)
        self.assertEqual(m["method_sha256"],
                         "00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae")
        self.pivot(460,op="getstatic",symbol="SECOND_WAVE")
        self.pivot(463,op="invokestatic",symbol="enchantLevel")
        self.pivot(466,op="ifle",operand=705)
        self.pivot(474,op="invokestatic",symbol="Math.max")
        self.pivot(486,op="if_icmpge",operand=705)
        self.pivot(495,op="fdiv")
        self.pivot(503,op="ldc",symbol="float 3.0f")
        self.pivot(506,op="f2i")
        self.pivot(507,op="iadd")
    def test_two_wave_entities_delayed_per_iteration_and_no_spawn_ack(self):
        for o in (535,620): self.pivot(o,op="invokespecial",symbol="WaveEntity")
        for o in (563,648): self.pivot(o,op="invokevirtual",symbol="setLifespan")
        for o in (604,689): self.pivot(o,op="invokevirtual",symbol="setWaitingTicks")
        for o in (602,687): self.pivot(o,op="bipush",operand=8)
        for o in (610,695): self.pivot(o,op="invokevirtual",symbol="addFreshEntity")
        for o in (613,698): self.pivot(o,op="pop")
        self.pivot(702,op="goto",operand=482)
        for o in (587,672): self.pivot(o,op="ldc",symbol="float 60.0f")
        for o in (590,675): self.pivot(o,op="bipush",operand=15)
    def test_native_wave_damage_owner_and_persistence_are_independent(self):
        prior=json.loads((P/"EXACT-SEA-SWING-STATIC-1.0.10.json").read_text(encoding="utf8"))
        self.assertEqual(prior["artifact"],self.data["artifact"])
        self.assertEqual(prior["class_sha256"],self.data["class_sha256"])
        w=prior["methods"]["com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class"]
        def anchor(name,offset):
            return next(x for x in w[name]["instructions"] if x["offset"]==offset)
        self.assertIn("mobProjectile",anchor("attackEntities",26)["symbol"])
        self.assertIn("hurt",anchor("attackEntities",123)["symbol"])
        self.assertEqual(anchor("attackEntities",126)["opcode"],"pop")
        self.assertIn("knockback",anchor("attackEntities",169)["symbol"])
        self.assertIn("ServerLevel.getEntity",anchor("getOwner",35)["symbol"])
        self.assertIn("String Owner",anchor("addAdditionalSaveData",8)["symbol"])
        self.assertIn("String Lifespan",anchor("addAdditionalSaveData",18)["symbol"])
        self.assertFalse(any("WAITING_TICKS" in x["symbol"] for x in w["addAdditionalSaveData"]["instructions"]))
        self.assertIn("isClientSide",anchor("tick",506)["symbol"])
    def test_static_certificate_does_not_certify_mutation_or_physical_qa(self):
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        c=ledger["objects"][OBJ]
        self.assertEqual(c["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(c["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(c["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(c["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(c["evidence"]),{"identity","behavior","parameters","targeting","costs","integration","validation"})
        self.assertTrue(all(e["path"].endswith("enchantments/second-wave.md") for e in c["evidence"].values()))
        self.assertIn("NO_MUTATION",self.card)
        x=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8")
        self.assertIn("| ✅ | `alexscaves:second_wave`",x)

if __name__=="__main__": unittest.main()
