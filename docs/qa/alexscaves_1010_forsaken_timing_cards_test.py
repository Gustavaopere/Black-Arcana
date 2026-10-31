#!/usr/bin/env python3
"""Pin Forsaken timer/counter and own-NBT documentation to JVM evidence."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract
DIR=Path(__file__).resolve().parents[2]/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"

class ForsakenTimingCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((DIR/"EXACT-FORSAKEN-TIMING-1.0.10.json").read_text(encoding="utf8"))
        cls.goal=next(x["tick"] for k,x in cls.data["timing"].items() if k.endswith("ForsakenAttackGoal.class"))
        cls.entity=next(x["tick"] for k,x in cls.data["timing"].items() if k.endswith("ForsakenEntity.class"))
        cls.own={x["name"]:x for x in cls.data["declared_state_methods"]}
        cls.card=(DIR/"forsaken-sonic-boom.md").read_text(encoding="utf8")
    def window(self,site):
        rows=[x for x in self.goal["sites"] if x["offset"]==site]
        self.assertEqual(len(rows),1)
        return {x["offset"]:x for x in rows[0]["window"]}
    def test_limits(self):
        self.assertEqual(self.data["scope"],"EXACT_1010_FORSAKEN_TICK_WINDOWS_AND_OWN_NBT_DECLARATIONS_ONLY")
        self.assertFalse(self.data["limits"]["declared_method_absence_proves_no_world_persistence"])
        self.assertFalse(self.data["limits"]["complete_perk_ready"])
        self.assertEqual(self.data["limits"]["mutating_hook"],"NOT_VERIFIED")
    def test_counter(self):
        frame=self.window(72)
        self.assertEqual(frame[71]["opcode"],"isub")
        self.assertIn("attemptSonicDamageIn",frame[72]["symbol"])
    def test_blast_cadence(self):
        frame=self.window(423)
        self.assertEqual(frame[426]["opcode"],"iconst_5")
        self.assertEqual(frame[427]["opcode"],"irem")
        self.assertEqual(frame[428]["opcode"],"ifne")
        self.assertEqual(self.window(607)[610]["operand"],"40")
    def test_exact_defaults(self):
        rows=self.own["defineSynchedData"]["method"]["sites"]
        for name,site,default,op in (("LEAPING",18,21,"iconst_0"),
                                      ("SONIC_CHARGE",30,33,"iconst_0"),
                                      ("SONAR_ID",54,57,"iconst_m1")):
            line=next(x for x in rows if x["offset"]==site and name in x["symbol"])
            nearby={v["offset"]:v for v in line["window"]}
            self.assertEqual(nearby[default]["opcode"],op)
    def test_own_nbt_decl_not_superclass(self):
        for name in ("addAdditionalSaveData","readAdditionalSaveData"):
            self.assertFalse(self.own[name]["declared_on_exact_class"])
            self.assertIsNone(self.own[name]["method"])
        self.assertTrue(self.own["getAnimationTick"]["declared_on_exact_class"])
    def test_document_provenance(self):
        assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        for name in (self.goal["method_sha256"],self.entity["method_sha256"],
                     self.own["defineSynchedData"]["method"]["method_sha256"],
                     "EXACT-FORSAKEN-TIMING-1.0.10.json","STATIC_TECHNICAL_CATALOG_ONLY",
                     "NOT_VERIFIED","NOT_TESTED","NO_MUTATION"):
            self.assertIn(name,self.card)
if __name__=="__main__":
    unittest.main()
