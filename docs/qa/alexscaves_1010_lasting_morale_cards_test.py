#!/usr/bin/env python3
"""Keep Lasting Morale's shared time, settlement and persistence bounded."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import (
    load_manifest, validate_cards, validate_structure,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/lasting-morale.md"


class LastingMoraleContract(unittest.TestCase):
    def contract(self):
        manifest = load_manifest(PROVIDER / "EXACT-LASTING-MORALE-CONTRACT-1.0.10.json")
        validate_structure(manifest, profile="lasting_morale")
        validate_cards(manifest, PROVIDER, profile="lasting_morale")
        return manifest

    def anchors(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return {a["offset"]: a for a in selected[0]["anchors"]}

    def test_singleton_identity_and_all_conch_own_methods(self):
        manifest = self.contract()
        self.assertEqual(set(manifest["cards"]), {CARD})
        self.assertEqual(manifest["catalog_family"], "LASTING_MORALE_ENCHANTMENT_CONTRACT")
        methods = manifest["classes"][PREFIX + "server/item/MagicConchItem.class"]["methods"]
        self.assertEqual({m["name"] for m in methods}, {
            "<init>", "isFoil", "releaseUsing", "use", "getEnchantmentValue",
            "isEnchantable", "getUseDuration", "getUseAnimation", "summonDeepOne",
        })
        self.assertEqual(manifest["resources"]["data/alexscaves/enchantment/lasting_morale.json"],
                         "8c662fb7f68987d8e564ec053ebccdd9232593e5961d2213bbbed037b270232f")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertIn("data/minecraft/tags/enchantment/" + tag + ".json", manifest["resources"])

    def test_charge_and_cost_precede_post_cost_level_read_and_server_guard(self):
        a = self.anchors("server/item/MagicConchItem", "releaseUsing")
        self.assertEqual(len(a), 211)
        self.assertIn("playSound", a[20]["symbol"])
        self.assertEqual((a[39]["operand"], a[41]["opcode"], a[41]["operand"]),
                         ("25", "if_icmple", "451"))
        self.assertIn("Math.min", a[62]["symbol"])
        self.assertIn("hurtAndBreakUsedHand", a[77]["symbol"])
        self.assertIn("LASTING_MORALE", a[90]["symbol"])
        self.assertEqual([p for p, v in a.items() if "LASTING_MORALE" in v["symbol"]], [90])
        self.assertIn("enchantLevel", a[93]["symbol"])
        self.assertEqual((a[86]["operand"], a[96]["operand"]), ("1200", "400"))
        self.assertEqual((a[99]["opcode"], a[100]["opcode"], a[101]["operand"]),
                         ("imul", "iadd", "8"))
        self.assertIn("isClientSide", a[104]["symbol"])
        self.assertEqual((a[107]["opcode"], a[107]["operand"]), ("ifne", "418"))

    def test_same_local_feeds_three_summons_and_item_cooldown_without_success_gate(self):
        a = self.anchors("server/item/MagicConchItem", "releaseUsing")
        for load, call in ((265, 267), (320, 322), (375, 377), (446, 448)):
            self.assertEqual((a[load]["opcode"], a[load]["operand"]), ("iload", "8"))
            self.assertIn("addCooldown" if call == 448 else "summonDeepOne", a[call]["symbol"])
        final_branches = [(p, v["opcode"], v["operand"]) for p, v in a.items()
                          if 418 <= p <= 448 and v["opcode"].startswith("if")]
        self.assertEqual(final_branches, [(422, "ifeq", "451")])
        self.assertIn("Player", a[419]["symbol"])
        helper = self.anchors("server/misc/ACCompat", "addCooldown")
        self.assertIn("ItemStack.getItem", helper[5]["symbol"])
        self.assertIn("ItemCooldowns.addCooldown", helper[9]["symbol"])

    def test_non_null_spawn_return_does_not_certify_world_insertion(self):
        a = self.anchors("server/item/MagicConchItem", "summonDeepOne")
        self.assertEqual(len(a), 134)
        for offset, symbol in ((234, "setSummonedBy"), (268, "finalizeSpawn"),
                               (278, "checkSpawnObstruction"), (290, "addFreshEntity"),
                               (297, "copyTarget")):
            self.assertIn(symbol, a[offset]["symbol"])
        self.assertEqual((a[281]["opcode"], a[281]["operand"]), ("ifeq", "303"))
        self.assertEqual(a[293]["opcode"], "pop")
        self.assertEqual((a[300]["opcode"], a[302]["opcode"]), ("aload", "areturn"))

    def test_expiry_needs_server_and_zero_progress_then_requests_discarded_removal(self):
        a = self.anchors("server/entity/living/DeepOneBaseEntity", "tick")
        self.assertLess(len(a), 256)
        self.assertEqual((a[126]["opcode"], a[126]["operand"]), ("ifle", "197"))
        self.assertEqual(a[212]["opcode"], "fsub")
        self.assertEqual((a[220]["opcode"], a[220]["operand"]), ("ifle", "288"))
        self.assertIn("isClientSide", a[227]["symbol"])
        self.assertEqual((a[230]["opcode"], a[230]["operand"]), ("ifne", "243"))
        self.assertEqual((a[238]["opcode"], a[239]["opcode"]), ("iconst_1", "isub"))
        self.assertIn("setSummonTime", a[240]["symbol"])
        self.assertEqual((a[295]["opcode"], a[295]["operand"]), ("ifne", "314"))
        self.assertIn("summonedProgress", a[299]["symbol"])
        self.assertEqual((a[304]["opcode"], a[304]["operand"]), ("ifgt", "314"))
        self.assertIn("DISCARDED", a[308]["symbol"])
        self.assertIn("remove", a[311]["symbol"])

    def test_uuid_condition_controls_time_nbt_and_progress_is_not_saved(self):
        owner = "server/entity/living/DeepOneBaseEntity"
        save = self.anchors(owner, "addAdditionalSaveData")
        load = self.anchors(owner, "readAdditionalSaveData")
        self.assertIn("ConchSummoned", save[80]["symbol"])
        self.assertIn("summonerUUID", save[91]["symbol"])
        self.assertEqual((save[94]["opcode"], save[94]["operand"]), ("ifnull", "119"))
        self.assertIn("ConchUUID", save[98]["symbol"])
        self.assertIn("ConchTime", save[109]["symbol"])
        self.assertIn("ConchUUID", load[110]["symbol"])
        self.assertIn("contains", load[113]["symbol"])
        self.assertEqual((load[116]["opcode"], load[116]["operand"]), ("ifeq", "141"))
        self.assertIn("setSummonTime", load[138]["symbol"])
        for body in (save, load):
            self.assertFalse(any("summonedProgress" in v["symbol"] for v in body.values()))

    def test_copy_target_precedence_and_target_side_alliance_filters(self):
        a = self.anchors("server/entity/living/DeepOneBaseEntity", "copyTarget")
        self.assertEqual((a[13]["opcode"], a[13]["operand"]), ("ifne", "92"))
        self.assertIn("getLastHurtMob", a[19]["symbol"])
        self.assertEqual((a[22]["opcode"], a[22]["operand"]), ("ifnull", "33"))
        self.assertEqual((a[30]["opcode"], a[30]["operand"]), ("goto", "45"))
        self.assertIn("getLastHurtByMob", a[34]["symbol"])
        for candidate, other, call in ((56, 57, 58), (72, 73, 74)):
            self.assertEqual(a[candidate]["opcode"], "aload_3")
            self.assertEqual(a[other]["opcode"], "aload_1" if other == 57 else "aload_0")
            self.assertIn("isAlliedTo", a[call]["symbol"])

    def test_certificate_has_seven_axes_without_mutation_or_physical_promotion(self):
        data = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        certificate = data["objects"][PROVIDER.name + "/" + CARD]
        self.assertEqual(certificate["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(certificate["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(certificate["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(certificate["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(certificate["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs", "integration", "validation",
        })
        self.assertEqual({e["path"] for e in certificate["evidence"].values()},
                         {str((PROVIDER / CARD).relative_to(ROOT))})
        crosswalk = (PROVIDER / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:lasting_morale`", crosswalk)


if __name__ == "__main__":
    unittest.main()
