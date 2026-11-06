#!/usr/bin/env python3
"""Bind Relentless firing cadence independently from its client load state."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/relentless-darkness.md"


class RelentlessDarknessContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json")
        validate_structure(d, profile="relentless_darkness")
        validate_cards(d, P, profile="relentless_darkness")
        return d

    def anchors(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return {a["offset"]: a for a in selected[0]["anchors"]}

    def test_identity_resource_and_acquisition_are_sealed_for_singleton(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(d["catalog_family"], "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT")
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/relentless_darkness.json"],
                         "94edb103571eba0d0ca503b8a9455d4643a0f414c758b4ca79d49bbcdf9f473e")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertIn("data/minecraft/tags/enchantment/" + tag + ".json", d["resources"])
        self.assertIn("data/alexscaves/recipe/dreadbow.json", d["resources"])

    def test_release_exits_and_tick_uses_remaining_modulo_without_charge_gate(self):
        release = self.anchors("server/item/DreadbowItem", "releaseUsing")
        self.assertIn("RELENTLESS_DARKNESS", release[14]["symbol"])
        self.assertEqual((release[20]["opcode"], release[20]["operand"]), ("ifgt", "899"))
        a = self.anchors("server/item/DreadbowItem", "onUseTick")
        self.assertEqual(len(a), 175)
        self.assertEqual((a[13]["opcode"], a[13]["operand"]), ("ifeq", "382"))
        self.assertIn("RELENTLESS_DARKNESS", a[23]["symbol"])
        self.assertEqual((a[29]["opcode"], a[29]["operand"]), ("ifle", "382"))
        self.assertEqual((a[32]["operand"], a[34]["opcode"], a[35]["opcode"]),
                         ("4", "iconst_3", "irem"))
        self.assertEqual((a[36]["opcode"], a[36]["operand"]), ("ifne", "382"))
        for forbidden in ("getUseTime", "getMaxLoadTime", "getPowerForTime", "PerfectShot", "PRECISE_VOLLEY", "TWILIGHT_PERFECTION"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_visual_load_five_and_increment_three_do_not_become_cadence(self):
        maximum = self.anchors("server/item/DreadbowItem", "getMaxLoadTime")
        self.assertIn("RELENTLESS_DARKNESS", maximum[1]["symbol"])
        self.assertEqual((maximum[7]["opcode"], maximum[7]["operand"]), ("ifle", "12"))
        self.assertEqual(maximum[10]["opcode"], "iconst_5")
        a = self.anchors("server/item/DreadbowItem", "acInventoryTick")
        self.assertIn("isClientSide", a[39]["symbol"])
        self.assertEqual((a[42]["opcode"], a[42]["operand"]), ("ifeq", "400"))
        self.assertEqual((a[36]["opcode"], a[36]["operand"]), ("istore", "6"))
        self.assertEqual((a[173]["opcode"], a[178]["opcode"]), ("iconst_3", "iadd"))
        self.assertIn("setUseTime", a[184]["symbol"])
        self.assertEqual((a[266]["operand"], a[268]["operand"]), ("6", "10"))
        self.assertEqual((a[270]["opcode"], a[270]["operand"]), ("if_icmplt", "278"))
        self.assertEqual(a[274]["opcode"], "iconst_0")
        self.assertIn("setUseTime", a[275]["symbol"])

    def test_count_conversion_damage_and_direction_are_the_continuous_path(self):
        a = self.anchors("server/item/DreadbowItem", "onUseTick")
        self.assertIn("isConvertibleArrow", a[127]["symbol"])
        self.assertEqual((a[134]["opcode"], a[134]["operand"]), ("ifeq", "152"))
        self.assertEqual((a[137]["opcode"], a[142]["opcode"], a[148]["opcode"]),
                         ("iconst_1", "iconst_2", "iadd"))
        self.assertIn("nextInt", a[143]["symbol"])
        self.assertEqual(a[195]["opcode"], "fconst_2")
        self.assertIn("setShadowArrowDamage", a[196]["symbol"])
        self.assertIn("getViewVector", a[258]["symbol"])
        self.assertIn("4.0f", a[280]["symbol"])
        self.assertIn("3.0f", a[283]["symbol"])
        self.assertEqual((a[295]["opcode"], a[296]["opcode"]), ("fmul", "fadd"))
        self.assertIn("shoot", a[299]["symbol"])
        self.assertEqual((a[304]["opcode"], a[305]["opcode"]), ("fconst_2", "fadd"))

    def test_spawn_boolean_discard_and_pickup_order_do_not_certify_acceptance(self):
        a = self.anchors("server/item/DreadbowItem", "onUseTick")
        self.assertIn("Pickup.ALLOWED", a[171]["symbol"])
        self.assertIn("DarkArrowEntity", a[182]["symbol"])
        self.assertIn("addFreshEntity", a[311]["symbol"])
        self.assertEqual(a[314]["opcode"], "pop")
        self.assertIn("createArrow", a[321]["symbol"])
        self.assertIn("Pickup.CREATIVE_ONLY", a[328]["symbol"])
        self.assertEqual((a[334]["opcode"], a[337]["operand"]), ("iinc", "162"))

    def test_costs_are_post_loop_per_callback_with_creative_and_shade_gates(self):
        a = self.anchors("server/item/DreadbowItem", "onUseTick")
        self.assertIn("isCreative", a[342]["symbol"])
        self.assertEqual((a[345]["opcode"], a[345]["operand"]), ("ifne", "382"))
        self.assertEqual((a[350]["opcode"], a[350]["operand"]), ("ifne", "360"))
        self.assertEqual(a[354]["opcode"], "iconst_1")
        self.assertIn("hurtAndBreakUsedHand", a[357]["symbol"])
        self.assertEqual((a[362]["opcode"], a[362]["operand"]), ("ifeq", "376"))
        self.assertIn("Items.ARROW", a[367]["symbol"])
        self.assertEqual((a[373]["opcode"], a[373]["operand"]), ("ifne", "382"))
        self.assertEqual(a[378]["opcode"], "iconst_1")
        self.assertIn("ItemStack.shrink", a[379]["symbol"])
        self.assertFalse(any("isClientSide" in v["symbol"] for v in a.values()))

    def test_start_use_still_needs_ammo_or_creative_before_shade_consumers(self):
        a = self.anchors("server/item/DreadbowItem", "use")
        self.assertIn("getProjectile", a[10]["symbol"])
        self.assertIn("isCreative", a[16]["symbol"])
        self.assertEqual((a[23]["opcode"], a[23]["operand"]), ("ifne", "34"))
        self.assertIn("isEmpty", a[28]["symbol"])
        self.assertEqual((a[31]["opcode"], a[31]["operand"]), ("ifne", "109"))
        self.assertFalse(any("SHADED_RESPITE" in v["symbol"] for v in a.values()))

    def test_certificate_and_crosswalk_keep_runtime_states_independent(self):
        data = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        certificate = data["objects"][P.name + "/" + CARD]
        self.assertEqual(certificate["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(certificate["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(certificate["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(certificate["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(certificate["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs", "integration", "validation",
        })
        self.assertEqual({e["path"] for e in certificate["evidence"].values()},
                         {str((P / CARD).relative_to(ROOT))})
        self.assertIn("| ✅ | `alexscaves:relentless_darkness`", (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text())


if __name__ == "__main__":
    unittest.main()
