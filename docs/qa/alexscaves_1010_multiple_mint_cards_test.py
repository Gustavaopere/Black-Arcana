#!/usr/bin/env python3
"""Keep Multiple Mint quantity, angle and entity settlement causally distinct."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import (
    load_manifest, validate_cards, validate_structure,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/multiple-mint.md"


class MultipleMintContract(unittest.TestCase):
    def contract(self):
        manifest = load_manifest(PROVIDER / "EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json")
        validate_structure(manifest, profile="multiple_mint")
        validate_cards(manifest, PROVIDER, profile="multiple_mint")
        return manifest

    def anchors(self, owner, name):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name]
        self.assertEqual(len(selected), 1, (owner, name))
        return {a["offset"]: a for a in selected[0]["anchors"]}

    def test_literal_identity_and_item_entity_rosters(self):
        manifest = self.contract()
        self.assertEqual(set(manifest["cards"]), {CARD})
        self.assertEqual(manifest["catalog_family"], "MULTIPLE_MINT_ENCHANTMENT_CONTRACT")
        self.assertEqual(len(manifest["classes"][PREFIX + "server/item/SugarStaffItem.class"]["methods"]), 5)
        self.assertEqual(len(manifest["classes"][PREFIX + "server/entity/item/SpinningPeppermintEntity.class"]["methods"]), 28)
        self.assertEqual(manifest["resources"]["data/alexscaves/enchantment/multiple_mint.json"],
                         "e7357f60b417fa10f5c64518dc51ab61365dca1a410c342ef2aa0604de40af03")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertIn("data/minecraft/tags/enchantment/" + tag + ".json", manifest["resources"])

    def test_single_pre_cost_count_read_also_supplies_angle_denominator(self):
        a = self.anchors("server/item/SugarStaffItem", "use")
        self.assertEqual(len(a), 226)
        self.assertIn("isClientSide", a[8]["symbol"])
        self.assertEqual((a[11]["opcode"], a[11]["operand"]), ("ifne", "471"))
        self.assertEqual((a[37]["opcode"], a[37]["operand"]), ("ifeq", "186"))
        self.assertEqual(a[186]["opcode"], "iconst_3")
        self.assertEqual([p for p, v in a.items() if "MULTIPLE_MINT" in v["symbol"]], [189])
        self.assertIn("enchantLevel", a[192]["symbol"])
        self.assertEqual((a[195]["opcode"], a[196]["opcode"], a[196]["operand"]),
                         ("iadd", "istore", "7"))
        self.assertEqual((a[210]["operand"], a[212]["opcode"], a[212]["operand"]),
                         ("7", "if_icmpge", "428"))
        self.assertEqual((a[396]["operand"], a[399]["opcode"], a[400]["opcode"]),
                         ("360", "imul", "i2f"))
        self.assertEqual((a[401]["operand"], a[403]["opcode"], a[404]["opcode"]),
                         ("7", "i2f", "fdiv"))
        self.assertIn("setStartAngle", a[405]["symbol"])

    def test_spawn_result_does_not_gate_iteration_or_final_costs(self):
        a = self.anchors("server/item/SugarStaffItem", "use")
        self.assertIn("setOwner", a[389]["symbol"])
        self.assertIn("addFreshEntity", a[418]["symbol"])
        self.assertEqual(a[421]["opcode"], "pop")
        self.assertEqual((a[422]["opcode"], a[422]["operand"]), ("iinc", "10, 1"))
        self.assertEqual((a[425]["opcode"], a[425]["operand"]), ("goto", "208"))
        self.assertFalse(any(v["opcode"].startswith("if") for p, v in a.items() if 418 <= p <= 425))
        self.assertIn("addCooldown", a[461]["symbol"])
        self.assertEqual(a[466]["opcode"], "iconst_1")
        self.assertIn("hurtAndBreakUsedHand", a[468]["symbol"])
        self.assertEqual([p for p, v in a.items() if "hurtAndBreakUsedHand" in v["symbol"]], [468])

    def test_native_dimensions_damage_aabb_and_seek_discard_stay_distinct(self):
        registry = self.anchors("server/entity/ACEntityRegistry", "lambda$static$75")
        self.assertIn("0.8f", registry[11]["symbol"])
        self.assertIn("0.4f", registry[14]["symbol"])
        self.assertIn("Builder.sized", registry[17]["symbol"])
        a = self.anchors("server/entity/item/SpinningPeppermintEntity", "hurtEntities")
        self.assertIn("getBoundingBox", a[1]["symbol"])
        self.assertIn("mobProjectile", a[14]["symbol"])
        self.assertIn("getEntitiesOfClass", a[27]["symbol"])
        self.assertFalse(any("inflate" in v["symbol"] or "getSpinRadius" in v["symbol"] for v in a.values()))
        self.assertIn("3.0f", a[143]["symbol"])
        self.assertIn("ACCompat.hurt", a[145]["symbol"])
        self.assertEqual((a[148]["opcode"], a[148]["operand"]), ("ifeq", "181"))
        self.assertIn("knockback", a[178]["symbol"])
        self.assertEqual((a[185]["opcode"], a[185]["operand"]), ("ifeq", "200"))
        self.assertIn("getSeekingEntityId", a[189]["symbol"])
        self.assertEqual((a[193]["opcode"], a[193]["operand"]), ("if_icmpeq", "200"))
        self.assertIn("discard", a[197]["symbol"])

    def test_motion_overwrites_and_captured_center_remain_explicit(self):
        a = self.anchors("server/entity/item/SpinningPeppermintEntity", "tick")
        self.assertEqual(len(a), 256)
        self.assertIn("3.0f", a[63]["symbol"])
        self.assertIn("setSpinRadius", a[65]["symbol"])
        self.assertIn("7.0f", a[69]["symbol"])
        self.assertIn("setSpinSpeed", a[71]["symbol"])
        self.assertIn("getSpinAroundPosition", a[75]["symbol"])
        self.assertEqual(a[78]["opcode"], "astore_1")
        self.assertEqual(a[602]["opcode"], "aload_1")
        self.assertEqual(a[687]["opcode"], "aload_1")

    def test_lifespan_initialization_unguarded_decrement_and_server_discard_fallthrough(self):
        a = self.anchors("server/entity/item/SpinningPeppermintEntity", "tick")
        self.assertEqual((a[9]["opcode"], a[9]["operand"]), ("if_icmpne", "20"))
        self.assertIn("getLifespan", a[14]["symbol"])
        self.assertIn("despawnsIn", a[17]["symbol"])
        self.assertEqual((a[32]["opcode"], a[32]["operand"]), ("ifle", "48"))
        self.assertEqual(a[41]["opcode"], "isub")
        self.assertIn("despawnsIn", a[42]["symbol"])
        self.assertFalse(any("isClientSide" in v["symbol"] for p, v in a.items() if 28 <= p <= 45))
        self.assertIn("isClientSide", a[52]["symbol"])
        self.assertEqual((a[55]["opcode"], a[55]["operand"]), ("ifne", "62"))
        self.assertIn("discard", a[59]["symbol"])
        self.assertEqual(a[62]["opcode"], "aload_0")
        self.assertIn("hurtEntities", a[737]["symbol"])

    def test_nbt_requires_y_but_loads_x_z_z_without_seeking_id(self):
        owner = "server/entity/item/SpinningPeppermintEntity"
        load = self.anchors(owner, "readAdditionalSaveData")
        save = self.anchors(owner, "addAdditionalSaveData")
        self.assertIn("AroundY", load[75]["symbol"])
        self.assertEqual((load[81]["opcode"], load[81]["operand"]), ("ifeq", "126"))
        for offset, key in ((100, "AroundX"), (107, "AroundZ"), (114, "AroundZ")):
            self.assertIn(key, load[offset]["symbol"])
        self.assertIn('"<init>":(DDD)', load[120]["symbol"])
        self.assertIn("AroundY", save[61]["symbol"])
        self.assertIn("Vec3.y", save[65]["symbol"])
        for body in (save, load):
            self.assertFalse(any("SEEKING_ENTITY" in v["symbol"] or "SeekingEntity" in v["symbol"] for v in body.values()))

    def test_cooldown_precedence_and_player_item_key(self):
        a = self.anchors("server/item/SugarStaffItem", "use")
        self.assertEqual((a[201]["operand"], a[305]["operand"], a[375]["operand"]),
                         ("80", "20", "50"))
        self.assertEqual((a[344]["opcode"], a[344]["operand"]), ("ifnull", "379"))
        self.assertIn("SEEKCANDY", a[349]["symbol"])
        self.assertEqual((a[355]["opcode"], a[355]["operand"]), ("ifle", "379"))
        self.assertEqual(a[459]["operand"], "9")
        helper = self.anchors("server/misc/ACCompat", "addCooldown")
        self.assertIn("ItemStack.getItem", helper[5]["symbol"])
        self.assertIn("ItemCooldowns.addCooldown", helper[9]["symbol"])

    def test_owner_resolution_and_seven_axes_do_not_promote_runtime(self):
        a = self.anchors("server/entity/item/SpinningPeppermintEntity", "getOwner")
        self.assertEqual((a[4]["opcode"], a[4]["operand"]), ("ifnonnull", "54"))
        self.assertIn("ServerLevel", a[18]["symbol"])
        self.assertIn("getEntity:(Ljava/util/UUID;)", a[35]["symbol"])
        self.assertIn("LivingEntity", a[40]["symbol"])
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
        self.assertIn("| ✅ | `alexscaves:multiple_mint`", crosswalk)


if __name__ == "__main__":
    unittest.main()
