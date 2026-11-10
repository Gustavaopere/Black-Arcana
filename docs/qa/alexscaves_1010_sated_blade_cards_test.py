#!/usr/bin/env python3
"""Bind Sated Blade's accepted-hit saturation path and source prerequisites."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/sated-blade.md"
ENTITY = "server/entity/item/DesolateDaggerEntity"


class SatedBladeContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-SATED-BLADE-CONTRACT-1.0.10.json")
        validate_structure(d, profile="sated_blade")
        validate_cards(d, P, profile="sated_blade")
        return d

    def anchors(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return {a["offset"]: a for a in selected[0]["anchors"]}

    def test_literal_identity_resource_and_acquisition(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(d["catalog_family"], "SATED_BLADE_ENCHANTMENT_CONTRACT")
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/sated_blade.json"],
                         "9f9857ce8d742c377ae7a88a1e4261825c3359a90311f5bfaa3d1a3c792fa86b")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertIn("data/minecraft/tags/enchantment/" + tag + ".json", d["resources"])
        self.assertIn("assets/alexscaves/lang/pt_br.json", d["resources"])

    def test_complete_sated_region_stays_within_old_tick_budget(self):
        a = self.anchors(ENTITY, "tick")
        self.assertEqual(len(a), 254)
        region = {p: v for p, v in a.items() if 365 <= p <= 435}
        self.assertEqual(len(region), 32)
        self.assertTrue({365, 375, 377, 395, 397, 411, 416, 424, 434} <= set(region))
        self.assertIn("SATED_BLADE", region[369]["symbol"])

    def test_accepted_hurt_positive_level_and_player_source_all_gate_benefit(self):
        a = self.anchors(ENTITY, "tick")
        self.assertIn("ACCompat.hurt", a[344]["symbol"])
        self.assertEqual((a[347]["opcode"], a[347]["operand"]), ("ifeq", "434"))
        self.assertIn("getItemStack", a[366]["symbol"])
        self.assertIn("enchantLevel", a[372]["symbol"])
        self.assertEqual((a[375]["opcode"], a[375]["operand"]), ("istore", "8"))
        self.assertEqual((a[379]["opcode"], a[379]["operand"]), ("ifle", "434"))
        self.assertEqual(a[382]["operand"], "6")
        self.assertIn("Player", a[384]["symbol"])
        self.assertEqual((a[387]["opcode"], a[387]["operand"]), ("ifeq", "434"))

    def test_saturation_is_pre_addition_gate_not_hp_food_level_or_local_clamp(self):
        a = self.anchors(ENTITY, "tick")
        self.assertIn("getSaturationLevel", a[402]["symbol"])
        self.assertIn("5.0f", a[405]["symbol"])
        self.assertEqual((a[407]["opcode"], a[408]["opcode"], a[408]["operand"]),
                         ("fcmpg", "ifge", "434"))
        self.assertIn("getSaturationLevel", a[421]["symbol"])
        self.assertEqual((a[424]["operand"], a[426]["opcode"]), ("8", "i2f"))
        self.assertIn("0.1f", a[427]["symbol"])
        self.assertEqual((a[429]["opcode"], a[430]["opcode"]), ("fmul", "fadd"))
        self.assertIn("FoodData.setSaturation:(F)V", a[431]["symbol"])
        for forbidden in ("Math.min", "heal:", "setFoodLevel", "setExhaustion", "hurtAndBreak"):
            self.assertFalse(any(forbidden in v["symbol"] for p, v in a.items() if 365 <= p <= 435))

    def test_source_fallback_and_native_producer_do_not_bind_player(self):
        a = self.anchors(ENTITY, "tick")
        self.assertIn("getPlayer:()Lnet/minecraft/world/entity/Entity;", a[294]["symbol"])
        self.assertEqual((a[301]["opcode"], a[301]["operand"]), ("ifnonnull", "308"))
        self.assertEqual((a[304]["opcode"], a[310]["operand"]), ("aload_0", "6"))
        producer = self.anchors("server/item/DesolateDaggerItem", "acSpawnDaggers")
        for offset, token in ((55, "setTargetId"), (61, "copyPosition"), (67, "setItemStack")):
            self.assertIn(token, producer[offset]["symbol"])
        for token in ("setPlayerId", "SATED_BLADE", "ItemStack.copy:"):
            self.assertFalse(any(token in v["symbol"] for v in producer.values()))
        setter = self.anchors(ENTITY, "setItemStack")
        self.assertIn("SynchedEntityData.set", setter[8]["symbol"])
        self.assertFalse(any("ItemStack.copy:" in v["symbol"] for v in setter.values()))

    def test_server_path_and_discard_do_not_wait_for_a_sated_success(self):
        a = self.anchors(ENTITY, "tick")
        self.assertEqual((a[239]["opcode"], a[239]["operand"]), ("ifne", "438"))
        for gate in (347, 379, 387, 408):
            self.assertEqual(a[gate]["operand"], "434")
        self.assertEqual(a[434]["opcode"], "aload_0")
        self.assertIn("discard", a[435]["symbol"])
        self.assertIn("getZ", a[439]["symbol"])

    def test_default_player_id_and_empty_custom_nbt_preserve_binding_limit(self):
        a = self.anchors(ENTITY, "defineSynchedData")
        self.assertIn("PLAYER_ID", a[13]["symbol"])
        self.assertEqual(a[16]["opcode"], "iconst_m1")
        for name in ("readAdditionalSaveData", "addAdditionalSaveData"):
            body = self.anchors(ENTITY, name)
            self.assertEqual(len(body), 1)
            self.assertEqual(body[0]["opcode"], "return")

    def test_seven_axes_and_crosswalk_do_not_promote_runtime(self):
        d = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        c = d["objects"][P.name + "/" + CARD]
        self.assertEqual(c["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(c["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(c["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(c["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(c["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs", "integration", "validation",
        })
        self.assertEqual({v["path"] for v in c["evidence"].values()}, {str((P / CARD).relative_to(ROOT))})
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:sated_blade`", crosswalk)
        inventory = json.loads((P / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ids = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        present = {p.stem.replace("-", "_") for p in (P / "enchantments").glob("*.md")
                   if p.name not in ("INDEX.md", "README.md")}
        missing = sorted(ids - present)
        if missing:
            # While dossier creation is incomplete, the public queue must
            # point to the actual next missing publisher identity.
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            # Having one card per JSON does not certify those cards, the
            # complete provider universe, mutating hooks or physical QA.
            self.assertEqual(len(ids), 51)
            self.assertTrue(ids <= present)
            self.assertIn("individual_existing_enchantment_dossiers=51/51", crosswalk)
            self.assertIn("whole_provider_catalog_closed=false", crosswalk)
            self.assertIn("mutating_hook=NOT_VERIFIED", crosswalk)
            self.assertIn("physical_qa=NOT_TESTED", crosswalk)
            self.assertIn("mutation=NO_MUTATION", crosswalk)


if __name__ == "__main__":
    unittest.main()
