#!/usr/bin/env python3
"""Bind Seapairing's passive setter request without promoting engine behavior."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/seapairing.md"
STAFF = "server/item/SeaStaffItem"


class SeapairingContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-SEAPAIRING-CONTRACT-1.0.10.json")
        validate_structure(d, profile="seapairing")
        validate_cards(d, P, profile="seapairing")
        return d

    def method(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return selected[0]

    def anchors(self, owner, name):
        return {a["offset"]: a for a in self.method(owner, name)["anchors"]}

    def test_literal_identity_exact_roster_and_bounded_evidence_counts(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "SEAPAIRING_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            "mixin/ItemStackTickMixin", "server/enchantment/ACEnchantmentRegistry",
            "server/item/ACItemRegistry", "server/item/ACTickingItem", STAFF,
            "server/misc/ACCompat",
        )})
        self.assertEqual(set(d["resources"]), {
            "META-INF/neoforge.mods.toml", "alexscaves.mixins.json",
            "assets/alexscaves/lang/en_us.json", "assets/alexscaves/lang/pt_br.json",
            "data/alexscaves/enchantment/seapairing.json",
            "data/alexscaves/loot_table/gameplay/deep_one_mage_barter.json",
            "data/alexscaves/tags/item/enchantable/sea_staff.json",
            *("data/minecraft/tags/enchantment/" + tag + ".json" for tag in (
                "in_enchanting_table", "non_treasure", "on_random_loot", "tradeable")),
        })
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/seapairing.json"],
                         "e814c593b935bca5a9b84f2ae3aa56d137d9bd099a9e7334b7d4a47fcccfbc57")
        self.assertEqual(d["resources"]["data/alexscaves/tags/item/enchantable/sea_staff.json"],
                         "22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e")
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertEqual((len(d["classes"]), len(d["resources"]), len(methods),
                          sum(len(m["anchors"]) for m in methods)), (6, 11, 15, 452))
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))

    def test_complete_callback_and_dispatch_keep_native_signature_and_slot_boundary(self):
        callback = self.method(STAFF, "acInventoryTick")
        self.assertEqual(callback["descriptor"],
                         "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;"
                         "Lnet/minecraft/world/entity/Entity;Z)V")
        a = self.anchors(STAFF, "acInventoryTick")
        self.assertEqual(set(a), {
            0, 1, 4, 7, 8, 11, 13, 15, 18, 19, 22, 25, 26, 29, 30, 32, 33,
            36, 39, 40, 43, 46, 49, 51, 54, 55, 58, 63, 66, 67, 70, 71, 74,
            77, 78, 79, 80, 83, 84, 85, 88, 91,
        })
        dispatch = self.method("mixin/ItemStackTickMixin", "ac_inventoryTick")
        self.assertEqual(dispatch["descriptor"],
                         "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;"
                         "IZLorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V")
        b = self.anchors("mixin/ItemStackTickMixin", "ac_inventoryTick")
        self.assertEqual(set(b), {0, 1, 4, 6, 8, 11, 13, 15, 18, 21, 23, 26, 28, 30, 32, 33, 34, 36, 41})
        self.assertIn("ItemStack.getItem", b[8]["symbol"])
        self.assertEqual(b[15]["opcode"], "instanceof")
        self.assertIn("ACTickingItem", b[15]["symbol"])
        self.assertEqual((b[18]["opcode"], b[18]["operand"]), ("ifeq", "41"))
        self.assertEqual((b[34]["opcode"], b[34]["operand"]), ("iload", "4"))
        self.assertEqual(b[36]["opcode"], "invokeinterface")
        self.assertIn("ACTickingItem.acInventoryTick:" + callback["descriptor"], b[36]["symbol"])
        self.assertFalse(any(v["opcode"] == "iload_3" or
                             (v["opcode"] == "iload" and v["operand"] == "3") for v in b.values()))
        self.assertEqual(b[41]["opcode"], "return")
        d = self.contract()
        self.assertEqual(d["classes"][PREFIX + "server/item/ACTickingItem.class"]["methods"], [])
        self.assertEqual(d["resources"]["alexscaves.mixins.json"],
                         "6e120e2d2cf226a25cbe3d0605968a184384194354eac0b1153108f74632c140")
        own_methods = d["classes"][PREFIX + STAFF + ".class"]["methods"]
        self.assertEqual((len(own_methods), sum(len(m["anchors"]) for m in own_methods)), (7, 370))

    def test_using_stack_equality_server_and_positive_current_level_gate_without_selected(self):
        a = self.anchors(STAFF, "acInventoryTick")
        self.assertEqual((a[1]["opcode"], a[4]["opcode"], a[4]["operand"]),
                         ("instanceof", "ifeq", "29"))
        self.assertIn("LivingEntity", a[1]["symbol"])
        self.assertIn("LivingEntity.getUseItem", a[15]["symbol"])
        self.assertEqual(a[18]["opcode"], "aload_1")
        self.assertIn("java/lang/Object.equals:(Ljava/lang/Object;)Z", a[19]["symbol"])
        self.assertEqual((a[22]["opcode"], a[22]["operand"]), ("ifeq", "29"))
        self.assertEqual((a[25]["opcode"], a[29]["opcode"], a[30]["operand"]),
                         ("iconst_1", "iconst_0", "5"))
        self.assertIn("Level.isClientSide", a[33]["symbol"])
        self.assertEqual((a[36]["opcode"], a[36]["operand"]), ("ifne", "91"))
        self.assertEqual(a[39]["opcode"], "aload_1")
        self.assertIn("ACEnchantmentRegistry.SEAPAIRING", a[40]["symbol"])
        self.assertIn("ACCompat.enchantLevel", a[43]["symbol"])
        self.assertEqual((a[46]["opcode"], a[46]["operand"]), ("ifle", "91"))
        self.assertEqual((a[49]["opcode"], a[49]["operand"], a[51]["opcode"], a[51]["operand"]),
                         ("iload", "5", "ifne", "91"))
        self.assertFalse(any(v["opcode"] == "iload" and v["operand"] == "4" for v in a.values()))
        for forbidden in ("isUsingItem", "isSameItem", "matches:", "Player", "EquipmentSlot"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)
        reader = self.anchors("server/misc/ACCompat", "enchantLevel")
        self.assertEqual(len(reader), 24)
        self.assertIn("ItemStack.getEnchantments", reader[1]["symbol"])
        self.assertIn("Holder.is:", reader[42]["symbol"])
        self.assertIn("getIntValue:()I", reader[51]["symbol"])
        self.assertEqual((reader[56]["opcode"], reader[60]["opcode"], reader[61]["opcode"]),
                         ("ireturn", "iconst_0", "ireturn"))
        registry = self.anchors("server/enchantment/ACEnchantmentRegistry", "<clinit>")
        self.assertEqual(registry[293]["symbol"], "String seapairing")
        self.assertIn("key:", registry[296]["symbol"])
        self.assertIn("SEAPAIRING:", registry[299]["symbol"])

    def test_strict_rng_threshold_precedes_water_rain_or_bubble_test(self):
        a = self.anchors(STAFF, "acInventoryTick")
        self.assertIn("Level.getRandom", a[55]["symbol"])
        self.assertIn("RandomSource.nextFloat:()F", a[58]["symbol"])
        self.assertEqual(a[63]["symbol"], "float 0.02f")
        self.assertEqual((a[66]["opcode"], a[67]["opcode"], a[67]["operand"]),
                         ("fcmpg", "ifge", "91"))
        self.assertEqual(a[70]["opcode"], "aload_3")
        self.assertIn("Entity.isInWaterRainOrBubble:()Z", a[71]["symbol"])
        self.assertEqual((a[74]["opcode"], a[74]["operand"]), ("ifeq", "91"))
        self.assertEqual([p for p, v in a.items() if "nextFloat" in v["symbol"]], [58])
        self.assertFalse(any(v["opcode"] in ("putfield", "putstatic", "iinc") for v in a.values()))
        for forbidden in ("nextInt", "isInWater:", "getBiome", "getGameTime", "tickCount"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_literal_min_request_has_no_damage_guard_local_clamp_or_level_magnitude(self):
        a = self.anchors(STAFF, "acInventoryTick")
        self.assertEqual([a[p]["opcode"] for p in (77, 78, 79, 80, 83, 84, 85, 88, 91)],
                         ["aload_1", "iconst_0", "aload_1", "invokevirtual", "iconst_1",
                          "isub", "invokestatic", "invokevirtual", "return"])
        self.assertIn("ItemStack.getDamageValue:()I", a[80]["symbol"])
        self.assertIn("java/lang/Math.min:(II)I", a[85]["symbol"])
        self.assertIn("ItemStack.setDamageValue:(I)V", a[88]["symbol"])
        self.assertEqual([v["opcode"] for v in a.values() if v["opcode"] in (
            "iadd", "isub", "imul", "idiv", "i2f", "fadd", "fsub", "fmul", "fdiv")], ["isub"])
        self.assertEqual([p for p, v in a.items() if "enchantLevel" in v["symbol"]], [43])
        self.assertFalse(any(v["opcode"] == "istore" and p > 30 for p, v in a.items()))
        for forbidden in ("Math.max", "isDamaged", "getMaxDamage", "getMaxLevel", "hurt",
                          "addFreshEntity", "shrink", "giveExperience", "setFoodLevel", "setSaturation", "heal:"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_cast_wear_one_and_equipment_properties_remain_separate_from_passive_request(self):
        a = self.anchors(STAFF, "use")
        self.assertEqual(len(a), 189)
        self.assertIn("Player.getAbilities", a[367]["symbol"])
        self.assertIn("Abilities.instabuild:Z", a[370]["symbol"])
        self.assertEqual((a[373]["opcode"], a[373]["operand"]), ("ifne", "384"))
        self.assertEqual(a[378]["opcode"], "iconst_1")
        self.assertIn("ACCompat.hurtAndBreak:", a[381]["symbol"])
        self.assertEqual([p for p, v in a.items() if "hurtAndBreak" in v["symbol"]], [381])
        self.assertFalse(any("SEAPAIRING" in v["symbol"] for v in a.values()))
        delegate = self.anchors("server/misc/ACCompat", "hurtAndBreak")
        self.assertIn("slotOf:", delegate[4]["symbol"])
        self.assertIn("ItemStack.hurtAndBreak:", delegate[7]["symbol"])
        slots = self.anchors("server/misc/ACCompat", "slotOf")
        self.assertIn("EquipmentSlot.MAINHAND", slots[7]["symbol"])
        self.assertIn("EquipmentSlot.OFFHAND", slots[13]["symbol"])
        supplier = self.anchors("server/item/ACItemRegistry", "lambda$static$108")
        self.assertIn("SeaStaffItem", supplier[0]["symbol"])
        self.assertEqual((supplier[11]["opcode"], supplier[11]["operand"]), ("sipush", "850"))
        self.assertIn("Properties.durability:", supplier[14]["symbol"])
        self.assertIn("Rarity.UNCOMMON", supplier[17]["symbol"])
        self.assertEqual(self.anchors(STAFF, "getEnchantmentValue")[0]["opcode"], "iconst_1")
        enchantable = self.anchors(STAFF, "isEnchantable")
        self.assertIn("ItemStack.getCount", enchantable[1]["symbol"])
        self.assertEqual((enchantable[4]["opcode"], enchantable[5]["opcode"], enchantable[5]["operand"]),
                         ("iconst_1", "if_icmpne", "12"))

    def test_seven_certificate_axes_preserve_static_scope_and_engine_boundary(self):
        d = self.contract()
        self.assertEqual(d["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(d["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual((d["mutating_hook"], d["physical_qa"]), ("NOT_VERIFIED", "NOT_TESTED"))
        self.assertFalse(d["provider_universe_closed"])
        self.assertEqual(d["semantic_magic_roots"], 8)
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        certificate = ledger["objects"][P.name + "/" + CARD]
        for key in ("claim_scope", "evidence_grade", "mutating_hook", "physical_qa"):
            self.assertEqual(certificate[key], d[key])
        self.assertEqual(set(certificate["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs", "integration", "validation",
        })
        self.assertEqual({v["path"] for v in certificate["evidence"].values()},
                         {str((P / CARD).relative_to(ROOT))})
        card = (P / CARD).read_text()
        for boundary in ("NO_MUTATION", "fronteira Minecraft ItemStack/engine", "QA física pendente"):
            self.assertIn(boundary, card)

    def test_dynamic_next_missing_identity_matches_live_crosswalk(self):
        inventory = json.loads((P / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ids = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        present = {p.stem.replace("-", "_") for p in (P / "enchantments").glob("*.md")
                   if p.name not in ("INDEX.md", "README.md")}
        self.assertIn("seapairing", ids)
        self.assertIn("seapairing", present)
        missing = sorted(ids - present)
        self.assertTrue(missing)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:seapairing`", crosswalk)
        self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                      + f"`alexscaves:{missing[0]}`;", crosswalk)


if __name__ == "__main__":
    unittest.main()
