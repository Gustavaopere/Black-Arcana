#!/usr/bin/env python3
"""SHA-exact Sea Swing card regressions; not a mutation or gameplay QA claim."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
JVM = PROVIDER / "EXACT-SEA-SWING-STATIC-1.0.10.json"
CARD = PROVIDER / "enchantments/sea-swing.md"
ITEM = "com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class"
WAVE = "com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class"
OBJECT = "✅-alexs-caves-continued/enchantments/sea-swing.md"


class SeaSwingContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(JVM.read_text(encoding="utf8"))
        cls.card = CARD.read_text(encoding="utf8")

    def method(self, owner, name):
        obj = self.data["methods"][owner][name]
        self.assertEqual(obj["instruction_count"], len(obj["instructions"]))
        self.assertEqual(sorted({i["offset"] for i in obj["instructions"]}),
                         [i["offset"] for i in obj["instructions"]])
        return {x["offset"]: x for x in obj["instructions"]}

    def test_identity_and_original_localized_description_are_exact(self):
        d = self.data
        self.assertEqual(d["scope"], "SEA_SWING_SHA_EXACT_STATIC_CATALOG_EVIDENCE_ONLY")
        self.assertEqual(d["enchantment"]["id"], "alexscaves:sea_swing")
        self.assertEqual(d["enchantment"]["json"]["max_level"], 1)
        self.assertEqual(d["enchantment"]["json"]["weight"], 2)
        self.assertEqual(d["enchantment"]["json"]["slots"], ["mainhand"])
        self.assertEqual(d["item_tag"]["json"]["values"], ["alexscaves:ortholance"])
        self.assertEqual(d["language"]["translations"]["enchantment.alexscaves.sea_swing"],
                         "Sea Swing")

    def test_hurt_enemy_uses_positive_gate_one_wave_and_ignored_spawn_return(self):
        a = self.method(ITEM, "acHurtEnemy")
        self.assertIn("hurtAndBreak", a[6]["symbol"])
        self.assertEqual(a[1]["opcode"], "iconst_1")
        self.assertIn("SEA_SWING", a[17]["symbol"])
        self.assertEqual((a[23]["opcode"], a[23]["operand"]), ("ifle", "97"))
        self.assertIn("WaveEntity", a[26]["symbol"])
        self.assertEqual(a[59]["opcode"], "iconst_5")
        self.assertIn("addFreshEntity", a[93]["symbol"])
        self.assertEqual(a[96]["opcode"], "pop")
        self.assertFalse(any("isClientSide" in x["symbol"] for x in a.values()))

    def test_actual_constructor_resolves_owner_and_has_one_nbt_boundary(self):
        ctor = self.data["constructors"][
            "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V"
        ]["instructions"]
        self.assertIn("setOwner", next(x["symbol"] for x in ctor if x["offset"] == 18))
        setter = self.method(WAVE, "setOwner")
        self.assertIn("owner:", setter[2]["symbol"])
        self.assertIn("ownerUUID:", setter[18]["symbol"])
        getter = self.method(WAVE, "getOwner")
        self.assertIn("ServerLevel.getEntity", getter[35]["symbol"])
        for name in ("readAdditionalSaveData", "addAdditionalSaveData"):
            symbols = [i["symbol"] for i in self.method(WAVE, name).values()]
            self.assertTrue(any("String Owner" in x for x in symbols))
            self.assertTrue(any("String Lifespan" in x for x in symbols))
            self.assertFalse(any("SLAMMING" in x or "WAITING_TICKS" in x
                                 or "WAVE_SCALE" in x or "activeWaveTicks" in x
                                 for x in symbols))
        consumer = self.method(WAVE, "attackEntities")
        self.assertIn("Field owner:", consumer[23]["symbol"])
        self.assertFalse(any("getOwner:" in i["symbol"] for i in consumer.values()))

    def test_tick_wave_area_and_damage_acceptance_are_distinct(self):
        tick = self.method(WAVE, "tick")
        self.assertIn("isClientSide", tick[506]["symbol"])
        self.assertEqual((tick[509]["opcode"], tick[509]["operand"]), ("ifne", "530"))
        self.assertIn("attackEntities", tick[527]["symbol"])
        self.assertIn("getLifespan", tick[575]["symbol"])
        self.assertEqual(tick[44]["opcode"], "return")
        self.assertIn("discard", tick[102]["symbol"])
        attack = self.method(WAVE, "attackEntities")
        self.assertEqual(attack[4]["symbol"], "double 0.5d")
        self.assertIn("mobProjectile", attack[26]["symbol"])
        self.assertIn("DeepOneBaseEntity", attack[80]["symbol"])
        self.assertIn("LivingEntity.hurt", attack[123]["symbol"])
        self.assertEqual(attack[126]["opcode"], "pop")
        self.assertIn("knockback", attack[169]["symbol"])
        slam = self.method(WAVE, "getSlamAmount")
        self.assertIn("float 0.1f", slam[16]["symbol"])

    def test_static_certificate_and_runtime_remain_independent(self):
        j = json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        c = j["objects"][OBJECT]
        self.assertEqual(c["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(c["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(c["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(c["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(c["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs",
            "integration", "validation"
        })
        self.assertTrue(all(x["path"].endswith("enchantments/sea-swing.md")
                            for x in c["evidence"].values()))
        self.assertIn("NO_MUTATION", self.card)
        self.assertIn("| ✅ | `alexscaves:sea_swing`",
                      (PROVIDER/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()
