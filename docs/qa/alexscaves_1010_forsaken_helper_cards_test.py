#!/usr/bin/env python3
"""Sealed exact Forsaken predicate and knockback helper card assertions."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract
ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAP=DIR/"EXACT-FORSAKEN-HELPERS-1.0.10.json"
CARD=DIR/"forsaken-sonic-boom.md"

class ForsakenHelpersCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(SNAP.read_text(encoding="utf-8"))
        cls.methods={m["name"]:m for c in cls.doc["classes"] for m in c["methods"]}
        cls.card=CARD.read_text(encoding="utf-8")
    def test_scope_and_limitations(self):
        self.assertEqual(self.doc["scope"],"EXACT_1010_FORSAKEN_SELECTED_ANIMATION_AND_KNOCKBACK_HELPER_ABI_ONLY")
        self.assertEqual(len(self.doc["classes"]),3)
        self.assertEqual(len(self.methods),10)
        self.assertFalse(self.doc["limits"]["complete_perk_ready"])
        self.assertEqual(self.doc["limits"]["mutating_hook"],"NOT_VERIFIED")
    def symbols(self,name):
        return " ".join(x["symbol"] for x in self.methods[name]["symbolic_invocations_and_fields"])
    def test_animation_gates_and_freeze(self):
        self.assertIn("NO_ANIMATION",self.symbols("tryAnimation"))
        self.assertIn("setAnimation:",self.symbols("tryAnimation"))
        self.assertEqual(self.methods["tryAnimation"]["branch_anchors"][0]["simple_target"],23)
        self.assertIn("ANIMATION_LEFT_PICKUP",self.symbols("isMovementFrozen"))
        self.assertIn("ANIMATION_RIGHT_PICKUP",self.symbols("isMovementFrozen"))
    def test_sonic_state_and_sonar_null_guard(self):
        self.assertIn("SynchedEntityData.get",self.symbols("hasSonicCharge"))
        self.assertIn("SONIC_CHARGE",self.symbols("hasSonicCharge"))
        self.assertIn("SynchedEntityData.set",self.symbols("setSonicCharge"))
        self.assertIn("SONAR_ID",self.symbols("getSonarTarget"))
        self.assertIn("Level.getEntity:",self.symbols("getSonarTarget"))
        self.assertTrue(any(x["opcode"]=="iconst_m1" for x in self.methods["getSonarTarget"]["constant_anchors"]))
    def test_melee_uses_mobattack_not_sonic(self):
        refs=self.symbols("checkAndDealDamage")
        self.assertIn("DamageSources.mobAttack:",refs)
        self.assertIn("Attributes.ATTACK_DAMAGE",refs)
        self.assertIn("ACCompat.hurt:",refs)
        self.assertNotIn("causeForsakenSonicBoomDamage",refs)
    def test_knockback_is_a_delegation(self):
        refs=self.symbols("knockback")
        self.assertIn("LivingEntity.knockback:",refs)
        self.assertEqual(len(self.methods["knockback"]["symbolic_invocations_and_fields"]),1)
        self.assertEqual(self.methods["knockback"]["branch_anchors"],[])
        self.assertIn("ACCompat.knockback:",self.symbols("knockBackAngle"))
    def test_card_evidence_pins_and_unverified_hook(self):
        assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        for cls in self.doc["classes"]:
            self.assertIn(cls["class_sha256"],self.card)
            for m in cls["methods"]:
                self.assertIn(m["method_sha256"],self.card)
                self.assertIn(m["descriptor"],self.card)
        for token in ("STATIC_TECHNICAL_CATALOG_ONLY","NOT_VERIFIED","NOT_TESTED","NO_MUTATION",
                      "EXACT-FORSAKEN-HELPERS-1.0.10.json"):
            self.assertIn(token,self.card)
if __name__=="__main__":
    unittest.main()
