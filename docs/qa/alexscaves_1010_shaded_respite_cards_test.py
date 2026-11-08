#!/usr/bin/env python3
"""Bind Shaded Respite's native light/cost predicates without runtime promotion."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/shaded-respite.md"
BOW = "server/item/DreadbowItem"


class ShadedRespiteContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json")
        validate_structure(d, profile="shaded_respite")
        validate_cards(d, P, profile="shaded_respite")
        return d

    def method(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return selected[0]

    def anchors(self, owner, name):
        return {a["offset"]: a for a in self.method(owner, name)["anchors"]}

    def test_literal_identity_roster_resources_and_registry_binding(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "SHADED_RESPITE_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            BOW, "server/item/ACItemRegistry", "server/enchantment/ACEnchantmentRegistry",
            "server/misc/ACCompat", "server/potion/DarknessIncarnateEffect",
        )})
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertEqual((len(d["classes"]), len(d["resources"]), len(methods),
                          sum(len(m["anchors"]) for m in methods)), (5, 10, 19, 522))
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/shaded_respite.json"],
                         "0c5bc4a73c8779c7bc0da2eb47a59e1263ac6c2ef6dead0cbfe5223c73e05872")
        self.assertEqual(d["resources"]["data/alexscaves/tags/item/enchantable/dreadbow.json"],
                         "f22db4f6335af0cc185f0478c482c3c666a86afa430f06bdabc78ccc662076d5")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertIn("data/minecraft/tags/enchantment/" + tag + ".json", d["resources"])
        registry = self.anchors("server/enchantment/ACEnchantmentRegistry", "<clinit>")
        self.assertEqual(set(registry), {419, 422, 425})
        self.assertEqual(registry[419]["symbol"], "String shaded_respite")
        self.assertIn("key:", registry[422]["symbol"])
        self.assertIn("SHADED_RESPITE:", registry[425]["symbol"])

    def test_release_local_windows_are_complete_within_unchanged_budget(self):
        a = self.anchors(BOW, "releaseUsing")
        self.assertEqual(len(a), 125)
        self.assertLess(len(a), 391)
        self.assertEqual({p for p in a if 0 <= p <= 84}, {
            0, 1, 4, 7, 8, 11, 13, 14, 17, 20, 23, 24, 25, 26, 29, 31, 32,
            34, 36, 37, 40, 42, 43, 46, 49, 52, 53, 56, 57, 59, 60, 63,
            66, 69, 71, 73, 76, 79, 80, 83, 84,
        })
        self.assertEqual({p for p in a if 136 <= p <= 182}, {
            136, 138, 139, 142, 144, 146, 149, 151, 154, 157, 160, 161,
            164, 167, 169, 170, 172, 173, 175, 178, 180, 182,
        })
        self.assertEqual({p for p in a if 857 <= p <= 899}, {
            857, 859, 862, 865, 867, 870, 871, 872, 874, 877, 879, 882,
            884, 887, 890, 893, 895, 896, 899,
        })
        self.assertIn("Player", a[1]["symbol"])
        self.assertEqual((a[4]["opcode"], a[4]["operand"]), ("ifeq", "899"))
        self.assertIn("RELENTLESS_DARKNESS", a[14]["symbol"])
        self.assertEqual((a[20]["opcode"], a[20]["operand"]), ("ifgt", "899"))

    def test_release_positive_level_darkness_and_conditional_common_arrow_fallback(self):
        a = self.anchors(BOW, "releaseUsing")
        self.assertEqual(a[59]["opcode"], "aload_1")
        self.assertIn("SHADED_RESPITE", a[60]["symbol"])
        self.assertIn("enchantLevel", a[63]["symbol"])
        self.assertEqual((a[66]["opcode"], a[66]["operand"]), ("ifle", "83"))
        self.assertEqual((a[71]["opcode"], a[71]["operand"]), ("bipush", "11"))
        self.assertIn("DarknessIncarnateEffect.isInLight", a[73]["symbol"])
        self.assertEqual((a[76]["opcode"], a[76]["operand"]), ("ifne", "83"))
        self.assertEqual((a[79]["opcode"], a[83]["opcode"], a[84]["operand"]),
                         ("iconst_1", "iconst_0", "9"))
        self.assertIn("Player.getProjectile", a[139]["symbol"])
        self.assertEqual((a[144]["operand"], a[146]["opcode"], a[146]["operand"]),
                         ("9", "ifeq", "169"))
        self.assertIn("ItemStack.isEmpty", a[151]["symbol"])
        self.assertEqual((a[154]["opcode"], a[154]["operand"]), ("ifeq", "169"))
        self.assertIn("Items.ARROW:", a[161]["symbol"])
        self.assertIn('ItemStack."<init>"', a[164]["symbol"])
        self.assertIn("createArrow:", a[175]["symbol"])
        self.assertEqual((a[182]["opcode"], a[182]["operand"]), ("ifnull", "899"))

    def test_initial_use_gate_factory_and_conversion_do_not_mean_free_survival_start(self):
        use = self.anchors(BOW, "use")
        self.assertEqual(len(use), 51)
        self.assertIn("Player.getProjectile", use[10]["symbol"])
        self.assertIn("Player.isCreative", use[16]["symbol"])
        self.assertEqual((use[23]["opcode"], use[23]["operand"]), ("ifne", "34"))
        self.assertIn("ItemStack.isEmpty", use[28]["symbol"])
        self.assertEqual((use[31]["opcode"], use[31]["operand"]), ("ifne", "109"))
        self.assertIn("startUsingItem", use[100]["symbol"])
        self.assertIn("useFail", use[111]["symbol"])
        self.assertFalse(any("SHADED_RESPITE" in v["symbol"] for v in use.values()))
        factory = self.anchors(BOW, "createArrow")
        self.assertEqual(len(factory), 29)
        self.assertIn("ItemStack.isEmpty", factory[1]["symbol"])
        self.assertIn("Player.getProjectile", factory[9]["symbol"])
        self.assertIn("ArrowItem", factory[23]["symbol"])
        self.assertIn("Items.ARROW:", factory[37]["symbol"])
        self.assertIn("ArrowItem.createArrow:", factory[55]["symbol"])
        conversion = self.anchors(BOW, "isConvertibleArrow")
        self.assertEqual(len(conversion), 14)
        self.assertIn("projectile/Arrow", conversion[1]["symbol"])
        self.assertIn("Arrow.getColor:()I", conversion[13]["symbol"])
        self.assertEqual(conversion[16]["opcode"], "iconst_m1")
        self.assertEqual((conversion[17]["opcode"], conversion[17]["operand"]),
                         ("if_icmpne", "24"))
        self.assertFalse(any("ItemStack.is:" in v["symbol"] for v in conversion.values()))

    def test_complete_relentless_callback_rechecks_shaded_without_initial_ammo_gate(self):
        a = self.anchors(BOW, "onUseTick")
        self.assertEqual(len(a), 175)
        self.assertIn("ProjectileWeaponItem.onUseTick", a[6]["symbol"])
        self.assertIn("Player", a[10]["symbol"])
        self.assertIn("RELENTLESS_DARKNESS", a[23]["symbol"])
        self.assertEqual((a[29]["opcode"], a[29]["operand"]), ("ifle", "382"))
        self.assertEqual((a[34]["opcode"], a[35]["opcode"], a[36]["operand"]),
                         ("iconst_3", "irem", "382"))
        self.assertIn("SHADED_RESPITE", a[40]["symbol"])
        self.assertIn("enchantLevel", a[43]["symbol"])
        self.assertEqual((a[46]["opcode"], a[46]["operand"]), ("ifle", "62"))
        self.assertEqual((a[50]["opcode"], a[50]["operand"]), ("bipush", "11"))
        self.assertIn("isInLight", a[52]["symbol"])
        self.assertEqual((a[55]["opcode"], a[55]["operand"]), ("ifne", "62"))
        self.assertEqual(a[63]["operand"], "6")
        self.assertIn("Player.getProjectile", a[84]["symbol"])
        self.assertEqual((a[91]["opcode"], a[91]["operand"], a[99]["operand"]),
                         ("ifeq", "114", "114"))
        self.assertIn("Items.ARROW:", a[106]["symbol"])
        self.assertIn("createArrow:", a[120]["symbol"])
        self.assertFalse(any(v["opcode"] in ("ifnull", "ifnonnull") for v in a.values()))
        for forbidden in ("Level.isClientSide", "stopUsingItem", "isInWater", "giveExperience"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_complete_light_and_phase_helpers_use_root_vehicle_block_light_and_threshold(self):
        light = self.anchors("server/potion/DarknessIncarnateEffect", "isInLight")
        self.assertEqual(len(light), 29)
        self.assertIn("LivingEntity.getRootVehicle", light[1]["symbol"])
        self.assertIn("Entity.blockPosition", light[4]["symbol"])
        self.assertIn("LightLayer.BLOCK", light[12]["symbol"])
        self.assertIn("Level.getBrightness", light[16]["symbol"])
        self.assertIn("Level.canSeeSky", light[25]["symbol"])
        self.assertEqual((light[28]["opcode"], light[28]["operand"]), ("ifeq", "45"))
        self.assertIn("sunAboveHorizon", light[36]["symbol"])
        self.assertEqual((light[39]["opcode"], light[39]["operand"]), ("ifeq", "45"))
        self.assertEqual((light[42]["opcode"], light[42]["operand"]), ("bipush", "15"))
        self.assertEqual((light[47]["opcode"], light[47]["operand"]), ("if_icmplt", "54"))
        self.assertEqual((light[50]["opcode"], light[54]["opcode"]), ("iconst_1", "iconst_0"))
        phase = self.anchors("server/misc/ACCompat", "sunAboveHorizon")
        self.assertEqual(len(phase), 16)
        self.assertEqual(phase[1]["opcode"], "fconst_1")
        self.assertIn("Level.getTimeOfDay:(F)F", phase[2]["symbol"])
        self.assertEqual((phase[7]["symbol"], phase[15]["symbol"]), ("float 0.259f", "float 0.74f"))
        self.assertEqual((phase[11]["opcode"], phase[11]["operand"]), ("iflt", "22"))
        self.assertEqual((phase[19]["opcode"], phase[19]["operand"]), ("ifle", "26"))
        self.assertFalse(any(v["opcode"] == "aload_1" for v in phase.values()))
        for forbidden in ("hasEffect", "getEffect", "isRaining", "LightLayer.SKY"):
            self.assertFalse(any(forbidden in v["symbol"] for v in light.values()), forbidden)

    def test_release_and_callback_costs_separate_creative_wear_and_exact_normal_arrow_item(self):
        for name, positions in (
            ("releaseUsing", (859, 862, 865, 867, 877, 871, 874, 879, 893, 884, 887, 890, 899, 895, 896)),
            ("onUseTick", (342, 345, 348, 350, 360, 354, 357, 362, 376, 367, 370, 373, 382, 378, 379)),
        ):
            a = self.anchors(BOW, name)
            creative, skip_all, eligible, skip_wear, ammo_gate, wear_one, wear_call, not_eligible, shrink_start, arrow, item_test, common, end, shrink_one, shrink = positions
            with self.subTest(consumer=name):
                self.assertIn("Player.isCreative", a[creative]["symbol"])
                self.assertEqual((a[skip_all]["opcode"], a[skip_all]["operand"]), ("ifne", str(end)))
                self.assertEqual(a[eligible]["opcode"], "iload")
                self.assertEqual((a[skip_wear]["opcode"], a[skip_wear]["operand"]), ("ifne", str(ammo_gate)))
                self.assertEqual(a[wear_one]["opcode"], "iconst_1")
                self.assertIn("ACCompat.hurtAndBreakUsedHand", a[wear_call]["symbol"])
                self.assertEqual((a[not_eligible]["opcode"], a[not_eligible]["operand"]), ("ifeq", str(shrink_start)))
                self.assertIn("Items.ARROW:", a[arrow]["symbol"])
                self.assertIn("ItemStack.is:(Lnet/minecraft/world/item/Item;)Z", a[item_test]["symbol"])
                self.assertEqual((a[common]["opcode"], a[common]["operand"]), ("ifne", str(end)))
                self.assertEqual(a[shrink_one]["opcode"], "iconst_1")
                self.assertIn("ItemStack.shrink:(I)V", a[shrink]["symbol"])
        delegate = self.anchors("server/misc/ACCompat", "hurtAndBreakUsedHand")
        self.assertEqual(len(delegate), 8)
        self.assertIn("LivingEntity.getUsedItemHand", delegate[4]["symbol"])
        self.assertIn("slotOf", delegate[7]["symbol"])
        self.assertIn("ItemStack.hurtAndBreak", delegate[10]["symbol"])

    def test_seven_certificate_axes_static_limits_and_dynamic_alphabetical_queue(self):
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
        self.assertIn("NO_MUTATION", (P / CARD).read_text())
        inventory = json.loads((P / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ids = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        present = {p.stem.replace("-", "_") for p in (P / "enchantments").glob("*.md")
                   if p.name not in ("INDEX.md", "README.md")}
        self.assertIn("shaded_respite", ids)
        self.assertIn("shaded_respite", present)
        missing = sorted(ids - present)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:shaded_respite`", crosswalk)
        if missing:
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            self.assertNotRegex(crosswalk, r"A \*\*próxima identidade[^\n]*é `alexscaves:")


if __name__ == "__main__":
    unittest.main()
