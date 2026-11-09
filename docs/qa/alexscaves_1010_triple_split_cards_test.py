#!/usr/bin/env python3
"""Bind Triple Split's firing snapshot and child attempts without runtime promotion."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/triple-split.md"
ITEM = "server/item/ShotGumItem"
BALL = "server/entity/item/GumballEntity"
COMPAT = "server/misc/ACCompat"
LAUNCH_CTOR = "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V"
TYPE_CTOR = "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V"


class TripleSplitContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json")
        validate_structure(d, profile="triple_split")
        validate_cards(d, P, profile="triple_split")
        return d

    def method(self, owner, name, descriptor=None):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name
                    and (descriptor is None or m["descriptor"] == descriptor)]
        self.assertEqual(len(selected), 1, (owner, name, descriptor))
        return selected[0]

    def anchors(self, owner, name, descriptor=None):
        return {a["offset"]: a for a in self.method(owner, name, descriptor)["anchors"]}

    def test_literal_identity_exact_rosters_and_bounded_partial_producer(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "TRIPLE_SPLIT_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            ITEM, BALL, COMPAT, "server/enchantment/ACEnchantmentRegistry",
            "server/item/ACItemRegistry", "server/entity/ACEntityRegistry", "server/misc/ACDamageTypes",
        )})
        self.assertEqual(set(d["resources"]), {
            "META-INF/neoforge.mods.toml", "assets/alexscaves/lang/en_us.json",
            "assets/alexscaves/lang/pt_br.json", "data/alexscaves/enchantment/triple_split.json",
            "data/alexscaves/enchantment/targeted_ricochet.json",
            "data/alexscaves/tags/item/enchantable/shot_gum.json", "data/alexscaves/recipe/shot_gum.json",
            *("data/minecraft/tags/enchantment/" + tag + ".json" for tag in (
                "in_enchanting_table", "non_treasure", "on_random_loot", "tradeable")),
        })
        for path, expected in (
            ("data/alexscaves/enchantment/triple_split.json",
             "fd4f773c48969b4c2537f443cc80d91e1385d545763be78feaefc5816ac551a0"),
            ("data/alexscaves/enchantment/targeted_ricochet.json",
             "adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e"),
            ("data/alexscaves/tags/item/enchantable/shot_gum.json",
             "3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d"),
            ("data/alexscaves/recipe/shot_gum.json",
             "11851d66a5e83898a166bb8f92fda1660f305bdc20b1dd0c2f8b5939ae2425a1"),
        ):
            self.assertEqual(d["resources"][path], expected)
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertEqual(d["resources"]["data/minecraft/tags/enchantment/" + tag + ".json"],
                             "6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1")
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))
        self.assertLessEqual(sum(len(m["anchors"]) for m in methods), 8192)
        # The actual producer has 285 instructions. These disjoint windows seal 254,
        # excluding the 31 visual/tag-update instructions at offsets 12 through 78.
        a = self.anchors(ITEM, "acInventoryTick")
        self.assertEqual((len(a), min(a), max(a)), (254, 0, 607))
        self.assertEqual(sum(0 <= offset <= 10 for offset in a), 6)
        self.assertEqual(sum(81 <= offset <= 607 for offset in a), 248)
        self.assertFalse(any(12 <= offset <= 78 for offset in a))
        registry = self.anchors("server/enchantment/ACEnchantmentRegistry", "<clinit>")
        self.assertEqual(set(registry), {437, 440, 443})
        self.assertEqual(registry[437]["symbol"], "String triple_split")
        self.assertIn("key:", registry[440]["symbol"])
        self.assertIn("TRIPLE_SPLIT:", registry[443]["symbol"])
        key = self.anchors("server/enchantment/ACEnchantmentRegistry", "key")
        self.assertIn("Registries.ENCHANTMENT", key[0]["symbol"])
        self.assertEqual(key[3]["symbol"], "String alexscaves")

    def test_firing_snapshot_requires_shooting_and_t5_and_positive_level_becomes_boolean(self):
        a = self.anchors(ITEM, "acInventoryTick")
        self.assertIn("isShooting:", a[1]["symbol"])
        self.assertIn("getShootTime:", a[7]["symbol"])
        self.assertEqual((a[4]["operand"], a[10]["operand"]), ("5", "6"))
        self.assertEqual((a[81]["operand"], a[83]["opcode"], a[84]["opcode"], a[84]["operand"]),
                         ("6", "iconst_5", "if_icmpne", "553"))
        self.assertEqual((a[87]["operand"], a[89]["opcode"], a[89]["operand"]), ("5", "ifeq", "553"))
        self.assertIn("playSound:", a[126]["symbol"])
        self.assertEqual(a[130]["opcode"], "iconst_0")
        self.assertIn("setShooting:", a[131]["symbol"])
        self.assertEqual([p for p, v in a.items() if "TRIPLE_SPLIT" in v["symbol"]], [155])
        self.assertIn("ACCompat.enchantLevel:", a[158]["symbol"])
        self.assertEqual((a[161]["opcode"], a[161]["operand"]), ("ifle", "168"))
        self.assertEqual([a[p]["opcode"] for p in (164, 165, 168, 169)],
                         ["iconst_1", "goto", "iconst_0", "istore"])
        self.assertEqual((a[165]["operand"], a[169]["operand"], a[439]["operand"]), ("169", "10", "10"))
        self.assertIn("setSplitsOnHit:(Z)V", a[441]["symbol"])
        self.assertLess(169, 294)  # One snapshot precedes all primary construction.
        self.assertFalse(any(v["opcode"] == "imul" for p, v in a.items() if 154 <= p <= 169))
        self.assertFalse(any(v["opcode"].startswith("iload") and v["operand"] == "4" for v in a.values()))
        reader = self.anchors(COMPAT, "enchantLevel")
        self.assertEqual(len(reader), 24)
        self.assertIn("ItemStack.getEnchantments", reader[1]["symbol"])
        self.assertIn("Holder.is:", reader[42]["symbol"])
        self.assertIn("getIntValue:()I", reader[51]["symbol"])
        self.assertEqual((reader[56]["opcode"], reader[60]["opcode"], reader[61]["opcode"]),
                         ("ireturn", "iconst_0", "ireturn"))

    def test_primary_quantity_owner_state_and_single_debit_surround_only_gated_insertion(self):
        a = self.anchors(ITEM, "acInventoryTick")
        self.assertIn("EXPLOSIVE_FLAVOR", a[172]["symbol"])
        self.assertEqual((a[186]["operand"], a[296]["operand"]), ("11", "11"))
        self.assertEqual((a[298]["opcode"], a[298]["operand"], a[301]["opcode"], a[305]["opcode"]),
                         ("ifeq", "305", "iconst_1", "iconst_2"))
        self.assertEqual((a[306]["opcode"], a[306]["operand"], a[512]["operand"], a[515]["operand"]),
                         ("if_icmpge", "518", "16, 1", "294"))
        self.assertIn('GumballEntity."<init>":' + LAUNCH_CTOR, a[316]["symbol"])
        ctor = self.anchors(BALL, "<init>", LAUNCH_CTOR)
        self.assertEqual(len(ctor), 10)
        self.assertIn("setOwner:(Lnet/minecraft/world/entity/Entity;)V", ctor[18]["symbol"])
        self.assertIn("setMaximumBounces:(I)V", a[487]["symbol"])
        self.assertEqual(a[492]["symbol"], "float 4.0f")
        self.assertIn("setDamage:(F)V", a[495]["symbol"])
        self.assertEqual((a[468]["symbol"], a[474]["symbol"], a[477]["symbol"]),
                         ("float 0.5f", "float 1.5f", "float 5.0f"))
        self.assertIn("Level.isClientSide:", a[499]["symbol"])
        self.assertEqual((a[502]["opcode"], a[502]["operand"]), ("ifne", "512"))
        self.assertIn("Level.addFreshEntity:", a[508]["symbol"])
        self.assertEqual(a[511]["opcode"], "pop")
        self.assertLess(495, 499)  # Construction and setters precede the local server gate.
        self.assertIn("Player.isCreative:", a[533]["symbol"])
        self.assertEqual((a[536]["opcode"], a[536]["operand"]), ("ifne", "553"))
        self.assertEqual([p for p, v in a.items() if "setGumballsLeft:" in v["symbol"]], [550])
        self.assertEqual([a[p]["opcode"] for p in (544, 545, 546)], ["iconst_1", "isub", "iconst_0"])
        self.assertIn("Math.max:(II)I", a[547]["symbol"])
        self.assertGreater(550, 515)  # Debit follows the loop and ignores insertion acceptance.

    def test_on_hit_calls_super_before_owner_gumball_and_non_split_bounce_filters(self):
        a = self.anchors(BALL, "onHit")
        self.assertEqual((len(a), max(a)), (79, 171))
        self.assertEqual(a[2]["opcode"], "invokespecial")
        self.assertIn("ThrowableProjectile.onHit:", a[2]["symbol"])
        self.assertIn("VoxelShape.isEmpty:", a[43]["symbol"])
        self.assertEqual((a[46]["opcode"], a[46]["operand"]), ("ifne", "57"))
        self.assertIn("bounceFromDirection:", a[54]["symbol"])
        self.assertIn("ownedBy:", a[77]["symbol"])
        self.assertEqual((a[80]["opcode"], a[80]["operand"], a[90]["opcode"], a[90]["operand"]),
                         ("ifne", "171", "ifne", "171"))
        self.assertIn("GumballEntity", a[87]["symbol"])
        self.assertIn("hitEntityIds:", a[94]["symbol"])
        self.assertIn("java/util/List.add:", a[107]["symbol"])
        self.assertEqual(a[112]["opcode"], "pop")
        self.assertFalse(any("contains:" in v["symbol"] for v in a.values()))
        self.assertIn("splitsOnHit:()Z", a[155]["symbol"])
        self.assertEqual((a[158]["opcode"], a[158]["operand"]), ("ifne", "171"))
        self.assertIn("bounceFromDirection:", a[168]["symbol"])
        hit = self.anchors(BALL, "onHitEntity")
        self.assertFalse(any("hitEntityIds" in v["symbol"] for v in hit.values()))

    def test_hurt_return_and_skipped_owner_alliance_damage_do_not_gate_split(self):
        a = self.anchors(BALL, "onHitEntity")
        self.assertEqual((len(a), max(a)), (162, 349))
        self.assertIn("getDamage:()F", a[11]["symbol"])
        self.assertEqual(a[14]["operand"], "4")
        self.assertIn("getPossessedByLicowitchId:", a[31]["symbol"])
        self.assertIn("getPossessingLicowitch:", a[44]["symbol"])
        self.assertIn("isFriendlyFire:", a[71]["symbol"])
        self.assertEqual((a[74]["opcode"], a[74]["operand"], a[77]["opcode"]), ("ifeq", "78", "return"))
        self.assertIn("Entity.level:", a[79]["symbol"])
        self.assertIn("Level.registryAccess:", a[82]["symbol"])
        self.assertEqual(a[85]["opcode"], "aload_3")
        self.assertIn("causeGumballDamage:", a[86]["symbol"])
        self.assertEqual((a[92]["opcode"], a[92]["operand"]), ("ifnull", "119"))
        self.assertIn("Entity.is:", a[97]["symbol"])
        for p in (100, 108, 116):
            self.assertEqual((a[p]["opcode"], a[p]["operand"]), ("ifne", "143"))
        self.assertEqual([a[p]["opcode"] for p in (103, 104, 111, 112)],
                         ["aload_2", "aload_3", "aload_3", "aload_2"])
        for p in (105, 113):
            self.assertIn("Entity.isAlliedTo:", a[p]["symbol"])
        self.assertEqual((a[137]["opcode"], a[137]["operand"]), ("fload", "4"))
        self.assertIn("Entity.hurt:", a[139]["symbol"])
        self.assertEqual(a[142]["opcode"], "pop")
        self.assertIn("splitsOnHit:()Z", a[144]["symbol"])
        self.assertEqual((a[147]["opcode"], a[147]["operand"]), ("ifeq", "349"))
        source = self.anchors("server/misc/ACDamageTypes", "causeGumballDamage")
        self.assertEqual(len(source), 13)
        self.assertFalse(any("Projectile" in v["symbol"] for v in source.values()))

    def test_three_child_attempts_then_parent_discard_have_no_local_spawn_acceptance_guard(self):
        a = self.anchors(BALL, "onHitEntity")
        self.assertEqual((a[150]["opcode"], a[151]["operand"], a[153]["operand"], a[155]["opcode"]),
                         ("iconst_0", "6", "6", "iconst_3"))
        self.assertEqual((a[156]["opcode"], a[156]["operand"]), ("if_icmpge", "345"))
        self.assertIn("ACEntityRegistry.GUMBALL", a[159]["symbol"])
        self.assertIn("ACCompat.createEntity:", a[174]["symbol"])
        self.assertIn("Level.addFreshEntity:", a[335]["symbol"])
        self.assertEqual((a[338]["opcode"], a[339]["operand"], a[342]["operand"]), ("pop", "6, 1", "153"))
        self.assertIn("discard:()V", a[346]["symbol"])
        loop = {p: v for p, v in a.items() if 159 <= p <= 342}
        self.assertFalse(any(v["opcode"] in ("ifnull", "ifnonnull") for v in loop.values()))
        for forbidden in ("isClientSide", "setOwner:", "hitEntityIds", "enchantLevel", "setGumballsLeft"):
            self.assertFalse(any(forbidden in v["symbol"] for v in loop.values()), forbidden)
        self.assertEqual([p for p, v in loop.items() if v["opcode"].startswith("if")], [226])
        tick = self.anchors(BALL, "tick")
        self.assertEqual(len(tick), 165)
        self.assertEqual((tick[190]["opcode"], tick[190]["operand"]), ("if_icmplt", "294"))
        self.assertEqual((tick[197]["symbol"], tick[200]["opcode"], tick[200]["operand"]),
                         ("float 20.0f", "ifle", "253"))
        self.assertIn("Level.isClientSide:", tick[207]["symbol"])
        self.assertEqual((tick[210]["opcode"], tick[210]["operand"]), ("ifne", "263"))
        self.assertIn("getOwner:", tick[218]["symbol"])
        self.assertEqual((tick[229]["symbol"], tick[237]["opcode"], tick[238]["opcode"]),
                         ("double 0.5d", "fconst_2", "iconst_0"))
        self.assertIn("ExplosionInteraction.NONE", tick[239]["symbol"])
        self.assertIn("Level.explode:", tick[242]["symbol"])
        self.assertIn("discard:", tick[247]["symbol"])

    def test_geometry_recomputes_current_heading_and_places_children_at_victim_eyes_plus_motion(self):
        a = self.anchors(BALL, "onHitEntity")
        self.assertIn("getDeltaMovement:", a[183]["symbol"])
        self.assertIn("Vec3.normalize:", a[186]["symbol"])
        self.assertIn("Vec3.x:D", a[193]["symbol"])
        self.assertIn("Vec3.z:D", a[198]["symbol"])
        self.assertIn("Mth.atan2:(DD)D", a[201]["symbol"])
        self.assertEqual([a[p]["opcode"] for p in (204, 205, 209, 213)], ["d2f", "fneg", "fmul", "fdiv"])
        self.assertEqual((a[206]["symbol"], a[210]["symbol"]), ("float 180.0f", "float 3.1415927f"))
        self.assertEqual((a[220]["opcode"], a[221]["opcode"]), ("dconst_0", "dconst_0"))
        self.assertIn("isExplosive:()Z", a[223]["symbol"])
        self.assertEqual((a[226]["opcode"], a[226]["operand"], a[229]["symbol"], a[235]["symbol"]),
                         ("ifeq", "235", "double 0.699999988079071d", "double 1.5d"))
        self.assertEqual((a[243]["symbol"], a[247]["symbol"], a[250]["operand"]),
                         ("float 30.0f", "float 30.0f", "6"))
        self.assertEqual([a[p]["opcode"] for p in (246, 252, 253, 254, 255, 259, 260)],
                         ["fadd", "i2f", "fmul", "fsub", "f2d", "dneg", "d2f"])
        self.assertIn("Math.toRadians:", a[256]["symbol"])
        self.assertIn("Vec3.yRot:", a[261]["symbol"])
        self.assertEqual((a[264]["operand"], a[268]["opcode"], a[272]["operand"], a[282]["operand"]),
                         ("10", "aload_2", "10", "10"))
        self.assertIn("Entity.getEyePosition:", a[269]["symbol"])
        self.assertIn("Vec3.add:", a[274]["symbol"])
        self.assertIn("setPos:", a[277]["symbol"])
        self.assertIn("setDeltaMovement:", a[284]["symbol"])
        self.assertTrue(all(153 < p < 339 for p in (183, 223, 269)))

    def test_child_factory_omits_owner_and_copies_current_parameters_while_disabling_split(self):
        a = self.anchors(BALL, "onHitEntity")
        factory = self.anchors(COMPAT, "createEntity")
        self.assertEqual(len(factory), 4)
        self.assertIn("EntityType.create:(Lnet/minecraft/world/level/Level;)", factory[2]["symbol"])
        self.assertEqual(factory[5]["opcode"], "areturn")
        ctor = self.anchors(BALL, "<init>", TYPE_CTOR)
        self.assertEqual(len(ctor), 19)
        self.assertIn("ThrowableProjectile", ctor[3]["symbol"])
        self.assertIn("java/util/ArrayList", ctor[7]["symbol"])
        self.assertIn("hitEntityIds:", ctor[14]["symbol"])
        self.assertEqual(ctor[27]["operand"], "12")
        self.assertIn("RandomSource.nextInt:", ctor[29]["symbol"])
        self.assertIn("setColor:", ctor[34]["symbol"])
        self.assertFalse(any("setOwner:" in v["symbol"] for v in ctor.values()))
        self.assertEqual(a[289]["opcode"], "iconst_0")
        self.assertIn("setSplitsOnHit:(Z)V", a[290]["symbol"])
        for getter, setter, name, signature in (
            (296, 299, "getDamage", "setDamage:(F)V"),
            (305, 308, "targetsOnBounce", "setTargetsOnBounce:(Z)V"),
            (314, 317, "isExplosive", "setExplosive:(Z)V"),
            (323, 326, "getMaximumBounces", "setMaximumBounces:(I)V"),
        ):
            self.assertEqual(a[getter - 1]["opcode"], "aload_0")
            self.assertIn(name + ":", a[getter]["symbol"])
            self.assertIn(signature, a[setter]["symbol"])
            self.assertGreater(getter, 139)  # The getters run after the external hurt callback.
        self.assertEqual([p for p, v in a.items() if "getDamage:" in v["symbol"]], [11, 296])
        for forbidden in ("getBounces:", "setBounces:", "setColor:", "setOwner:"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_sync_defaults_color_only_own_nbt_and_static_axes_keep_dynamic_live_queue(self):
        d = self.contract()
        a = self.anchors(BALL, "defineSynchedData")
        self.assertEqual(len(a), 43)
        for field, offset, default in (
            ("MAXIMUM_BOUNCES", 1, "iconst_5"), ("BOUNCES", 13, "iconst_0"),
            ("COLOR", 25, "iconst_0"), ("DAMAGE", 37, "fconst_2"),
            ("TARGETS_ON_BOUNCE", 49, "iconst_0"), ("SPLITS_ON_HIT", 61, "iconst_0"),
            ("EXPLOSIVE", 73, "iconst_0"),
        ):
            self.assertIn(field + ":", a[offset]["symbol"])
            self.assertEqual(a[offset + 3]["opcode"], default)
        for name in ("splitsOnHit", "setSplitsOnHit"):
            b = self.anchors(BALL, name)
            self.assertEqual(len(b), 7)
            self.assertTrue(any("SPLITS_ON_HIT:" in v["symbol"] for v in b.values()))
            self.assertFalse(any(v["opcode"].startswith("if") for v in b.values()))
        for name in ("readAdditionalSaveData", "addAdditionalSaveData"):
            b = self.anchors(BALL, name)
            self.assertEqual((len(b), max(b), b[16]["opcode"]), (9, 16, "return"))
            self.assertEqual(b[2]["opcode"], "invokespecial")
            self.assertIn("ThrowableProjectile." + name + ":", b[2]["symbol"])
            self.assertEqual({v["symbol"] for v in b.values() if v["symbol"].startswith("String ")}, {"String Color"})
            for forbidden in ("SPLITS_ON_HIT", "DAMAGE", "EXPLOSIVE", "MAXIMUM_BOUNCES", "BOUNCES", "hitEntityIds"):
                self.assertFalse(any(forbidden in v["symbol"] for v in b.values()), forbidden)
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
        self.assertEqual({v["path"] for v in certificate["evidence"].values()}, {str((P / CARD).relative_to(ROOT))})
        self.assertIn("NO_MUTATION", (P / CARD).read_text())
        inventory = json.loads((P / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ids = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        present = {p.stem.replace("-", "_") for p in (P / "enchantments").glob("*.md")
                   if p.name not in ("INDEX.md", "README.md")}
        self.assertIn("triple_split", ids)
        self.assertIn("triple_split", present)
        missing = sorted(ids - present)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:triple_split`", crosswalk)
        if missing:
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            self.assertNotRegex(crosswalk, r"A \*\*próxima identidade[^\n]*é `alexscaves:")


if __name__ == "__main__":
    unittest.main()
