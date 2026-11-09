#!/usr/bin/env python3
"""Bind Triple Splash's native cast attempts without promoting hits or runtime QA."""
import json
from pathlib import Path
import struct
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/triple-splash.md"
STAFF = "server/item/SeaStaffItem"
BOLT = "server/entity/item/WaterBoltEntity"
LAUNCH_CTOR = "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V"
TYPE_CTOR = "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V"


class TripleSplashContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json")
        validate_structure(d, profile="triple_splash")
        validate_cards(d, P, profile="triple_splash")
        return d

    def method(self, owner, name, descriptor=None):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name
                    and (descriptor is None or m["descriptor"] == descriptor)]
        self.assertEqual(len(selected), 1, (owner, name, descriptor))
        return selected[0]

    def anchors(self, owner, name, descriptor=None):
        return {a["offset"]: a for a in self.method(owner, name, descriptor)["anchors"]}

    def test_literal_identity_exact_rosters_and_bounded_native_evidence(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            STAFF, BOLT, "server/misc/ACCompat", "server/enchantment/ACEnchantmentRegistry",
            "server/item/ACItemRegistry",
        )})
        self.assertEqual(set(d["resources"]), {
            "META-INF/neoforge.mods.toml", "assets/alexscaves/lang/en_us.json",
            "assets/alexscaves/lang/pt_br.json", "data/alexscaves/enchantment/triple_splash.json",
            "data/alexscaves/enchantment/bouncing_bolt.json",
            "data/alexscaves/tags/item/enchantable/sea_staff.json",
            "data/alexscaves/loot_table/gameplay/deep_one_mage_barter.json",
            *("data/minecraft/tags/enchantment/" + tag + ".json" for tag in (
                "in_enchanting_table", "non_treasure", "on_random_loot", "tradeable")),
        })
        self.assertEqual(d["resources"]["data/alexscaves/tags/item/enchantable/sea_staff.json"],
                         "22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e")
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/triple_splash.json"],
                         "6946e2d21814f3e398925f2886a6284b140032b255a05f9598c8e00e2bc315be")
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/bouncing_bolt.json"],
                         "bc103328ad554dd97348becf898d5ecedd2867385d1ffbd756cf04ec302d24e7")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertEqual(d["resources"]["data/minecraft/tags/enchantment/" + tag + ".json"],
                             "6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1")
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertEqual((len(d["classes"]), len(d["resources"]), len(methods),
                          sum(len(m["anchors"]) for m in methods)), (5, 11, 33, 1063))
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))
        partial = {(BOLT, "tick"), ("server/enchantment/ACEnchantmentRegistry", "<clinit>"),
                   ("server/item/ACItemRegistry", "<clinit>")}
        complete = [m for owner, entry in d["classes"].items() for m in entry["methods"]
                    if (owner.removeprefix(PREFIX).removesuffix(".class"), m["name"]) not in partial]
        self.assertEqual((len(complete), sum(len(m["anchors"]) for m in complete)), (30, 878))
        registry = self.anchors("server/enchantment/ACEnchantmentRegistry", "<clinit>")
        self.assertEqual(set(registry), {302, 305, 308})
        self.assertEqual(registry[302]["symbol"], "String triple_splash")
        self.assertIn("key:", registry[305]["symbol"])
        self.assertIn("TRIPLE_SPLASH:", registry[308]["symbol"])
        key = self.anchors("server/enchantment/ACEnchantmentRegistry", "key")
        self.assertIn("Registries.ENCHANTMENT", key[0]["symbol"])
        self.assertEqual(key[3]["symbol"], "String alexscaves")
        item_registry = self.anchors("server/item/ACItemRegistry", "<clinit>")
        self.assertEqual(set(item_registry), {2038, 2041, 2044, 2049, 2052})
        self.assertEqual(item_registry[2041]["symbol"], "String sea_staff")
        self.assertIn("SEA_STAFF:", item_registry[2052]["symbol"])
        supplier = self.anchors("server/item/ACItemRegistry", "lambda$static$108")
        self.assertEqual((len(supplier), supplier[11]["operand"]), (11, "850"))
        self.assertIn("Item$Properties.durability:", supplier[14]["symbol"])
        self.assertIn("Rarity.UNCOMMON", supplier[17]["symbol"])

    def test_server_positive_current_level_selects_three_attempts_with_one_loop(self):
        a = self.anchors(STAFF, "use")
        self.assertEqual((len(a), max(a), a[393]["opcode"]), (189, 393, "areturn"))
        self.assertIn("Level.isClientSide", a[75]["symbol"])
        self.assertEqual((a[78]["opcode"], a[78]["operand"]), ("ifne", "355"))
        self.assertIn("ACEnchantmentRegistry.TRIPLE_SPLASH", a[97]["symbol"])
        self.assertIn("ACCompat.enchantLevel", a[100]["symbol"])
        self.assertEqual((a[103]["opcode"], a[103]["operand"]), ("ifle", "110"))
        self.assertEqual([a[p]["opcode"] for p in (106, 107, 110, 111, 113, 114)],
                         ["iconst_3", "goto", "iconst_1", "istore", "iconst_0", "istore"])
        self.assertEqual((a[107]["operand"], a[111]["operand"], a[114]["operand"]),
                         ("111", "9", "10"))
        self.assertEqual((a[116]["operand"], a[118]["operand"], a[120]["operand"]),
                         ("10", "9", "355"))
        self.assertEqual(a[120]["opcode"], "if_icmpge")
        self.assertEqual((a[349]["opcode"], a[349]["operand"], a[352]["operand"]),
                         ("iinc", "10, 1", "116"))
        self.assertEqual([p for p, v in a.items() if "TRIPLE_SPLASH" in v["symbol"]], [97])
        self.assertFalse(any(v["opcode"] == "imul" for v in a.values()))
        reader = self.anchors("server/misc/ACCompat", "enchantLevel")
        self.assertEqual(len(reader), 24)
        self.assertIn("ItemStack.getEnchantments", reader[1]["symbol"])
        self.assertIn("Holder.is:", reader[42]["symbol"])
        self.assertIn("getIntValue:()I", reader[51]["symbol"])
        self.assertEqual((reader[56]["opcode"], reader[60]["opcode"], reader[61]["opcode"]),
                         ("ireturn", "iconst_0", "ireturn"))

    def test_spread_speeds_and_sibling_state_are_applied_before_ignored_spawn_return(self):
        a = self.anchors(STAFF, "use")
        self.assertEqual((a[125]["operand"], a[128]["opcode"], a[135]["operand"]),
                         ("132", "fconst_0", "143"))
        self.assertEqual((a[138]["symbol"], a[143]["symbol"]),
                         ("float -50.0f", "float 50.0f"))
        self.assertIn('WaterBoltEntity."<init>":' + LAUNCH_CTOR, a[153]["symbol"])
        self.assertIn("getXRot:()F", a[245]["symbol"])
        self.assertIn("getYRot:()F", a[249]["symbol"])
        self.assertEqual((a[252]["operand"], a[254]["opcode"], a[255]["symbol"]),
                         ("11", "fadd", "float -20.0f"))
        self.assertEqual((a[259]["opcode"], a[259]["operand"]), ("ifle", "266"))
        self.assertEqual((a[262]["opcode"], a[266]["opcode"], a[267]["symbol"]),
                         ("fconst_1", "fconst_2", "float 12.0f"))
        self.assertIn("shootFromRotation:", a[269]["symbol"])
        self.assertIn("ENVELOPING_BUBBLE", a[274]["symbol"])
        self.assertEqual((a[280]["opcode"], a[280]["operand"]), ("ifle", "297"))
        self.assertIn("nextBoolean:()Z", a[289]["symbol"])
        self.assertIn("setBubbling:(Z)V", a[294]["symbol"])
        self.assertIn("BOUNCING_BOLT", a[299]["symbol"])
        self.assertEqual((a[305]["opcode"], a[305]["operand"]), ("ifle", "314"))
        self.assertIn("ricochet:Z", a[311]["symbol"])
        self.assertEqual((a[316]["symbol"], a[318]["operand"], a[320]["symbol"]),
                         ("float 0.3f", "5", "float 0.2f"))
        self.assertEqual([a[p]["opcode"] for p in (322, 323, 324)], ["fmul", "fadd", "putfield"])
        self.assertIn("seekAmount:F", a[324]["symbol"])
        self.assertIn("Level.addFreshEntity:", a[345]["symbol"])
        self.assertEqual(a[348]["opcode"], "pop")
        self.assertFalse(any("hurt:" in v["symbol"] for v in a.values()))

    def test_one_target_snapshot_precedes_loop_and_helper_ranks_visible_mobs_from_clip_endpoint(self):
        use = self.anchors(STAFF, "use")
        self.assertEqual(use[81]["symbol"], "double 128.0d")
        self.assertEqual([p for p, v in use.items() if "getClosestLookingAtEntityFor:" in v["symbol"]], [90])
        self.assertLess(90, 116)
        self.assertEqual((use[327]["operand"], use[329]["opcode"], use[329]["operand"]),
                         ("8", "ifnull", "342"))
        self.assertIn("Entity.getUUID:", use[336]["symbol"])
        self.assertIn("setArcingTowards:", use[339]["symbol"])
        a = self.anchors(STAFF, "getClosestLookingAtEntityFor")
        self.assertEqual((len(a), max(a)), (119, 282))
        self.assertIn("ClipContext$Block.VISUAL", a[30]["symbol"])
        self.assertIn("ClipContext$Fluid.NONE", a[33]["symbol"])
        self.assertIn("Level.clip:", a[40]["symbol"])
        self.assertIn("HitResult.getLocation:", a[116]["symbol"])
        self.assertEqual(a[156]["symbol"], "double 15.0d")
        self.assertEqual(a[170]["opcode"], "dload_2")
        for mob, los, exit_offset, destination in ((92, 101, 104, "111"), (235, 244, 247, "277")):
            self.assertIn("entity/Mob", a[mob]["symbol"])
            self.assertIn("hasLineOfSight:", a[los]["symbol"])
            self.assertEqual((a[exit_offset]["opcode"], a[exit_offset]["operand"]), ("ifeq", destination))
        for p in (259, 266):
            self.assertIn("Entity.distanceToSqr:(Lnet/minecraft/world/phys/Vec3;)D", a[p]["symbol"])
        self.assertEqual((a[269]["opcode"], a[270]["opcode"], a[270]["operand"]),
                         ("dcmpg", "ifge", "277"))
        getter = self.anchors(BOLT, "getArcingTowards")
        self.assertIn("Optional.orElse:", getter[14]["symbol"])
        self.assertEqual((getter[22]["opcode"], getter[22]["operand"]), ("ifnonnull", "29"))
        self.assertIn("ServerLevel", getter[33]["symbol"])
        self.assertIn("ServerLevel.getEntity:", getter[37]["symbol"])
        self.assertFalse(any("isAlive" in v["symbol"] for v in getter.values()))

    def test_owner_is_constructor_bound_and_single_post_loop_cost_is_not_per_projectile(self):
        a = self.anchors(STAFF, "use")
        self.assertIn("Stats.ITEM_USED", a[356]["symbol"])
        self.assertEqual([p for p, v in a.items() if "awardStat:" in v["symbol"]], [363])
        self.assertIn("Abilities.instabuild", a[370]["symbol"])
        self.assertEqual((a[373]["opcode"], a[373]["operand"]), ("ifne", "384"))
        self.assertEqual((a[376]["operand"], a[378]["opcode"]), ("4", "iconst_1"))
        self.assertEqual([p for p, v in a.items() if "hurtAndBreak:" in v["symbol"]], [381])
        self.assertGreater(381, 352)
        self.assertIn("ACCompat.useSidedSuccess:", a[390]["symbol"])
        self.assertFalse(any("Cooldown" in v["symbol"] for v in a.values()))
        ctor = self.anchors(BOLT, "<init>", LAUNCH_CTOR)
        self.assertEqual((len(ctor), max(ctor)), (28, 55))
        self.assertIn("setOwner:(Lnet/minecraft/world/entity/Entity;)V", ctor[52]["symbol"])
        hurt = self.anchors("server/misc/ACCompat", "hurt")
        self.assertEqual(len(hurt), 5)
        self.assertIn("Entity.hurt:", hurt[3]["symbol"])
        self.assertEqual(hurt[6]["opcode"], "ireturn")

    def test_bounded_tick_keeps_float_double_gates_and_own_nbt_only_bubbling(self):
        a = self.anchors(BOLT, "tick")
        self.assertEqual((len(a), min(a), max(a)), (177, 0, 721))
        windows = ((0, 158, 83), (281, 402, 58), (553, 559, 5), (655, 721, 31))
        for start, end, count in windows:
            self.assertEqual(sum(start <= offset <= end for offset in a), count)
        self.assertEqual(sum(count for _, _, count in windows), len(a))
        self.assertIn("Projectile.tick:()V", a[1]["symbol"])
        self.assertEqual((a[11]["opcode"], a[11]["operand"]), ("ifne", "161"))
        self.assertEqual((a[20]["opcode"], a[20]["operand"]), ("ifnull", "158"))
        for wide, literal, compare, branch in ((35, 36, 39, 40), (75, 76, 79, 80)):
            self.assertEqual(a[wide]["opcode"], "f2d")
            self.assertEqual(a[literal]["symbol"], "double 0.3d")
            self.assertEqual((a[compare]["opcode"], a[branch]["opcode"], a[branch]["operand"]),
                             ("dcmpl", "ifle", "158"))
        # Java's native float 0.3 widened to double is above the double literal.
        self.assertGreater(struct.unpack(">f", struct.pack(">f", 0.3))[0], 0.3)
        self.assertEqual((a[48]["opcode"], a[48]["operand"]), ("if_icmpne", "158"))
        self.assertEqual(a[56]["symbol"], "float 1.5f")
        self.assertEqual((a[59]["opcode"], a[59]["operand"]), ("ifle", "158"))
        self.assertEqual((a[66]["operand"], a[87]["operand"], a[89]["operand"]), ("20", "40", "158"))
        self.assertEqual(a[97]["symbol"], "float 0.85f")
        self.assertIn("Vec3.normalize:", a[116]["symbol"])
        self.assertIn("setDeltaMovement:", a[155]["symbol"])
        ctor = self.anchors(BOLT, "<init>", TYPE_CTOR)
        self.assertEqual((ctor[31]["opcode"], ctor[36]["opcode"], ctor[41]["symbol"]),
                         ("iconst_m1", "iconst_0", "float 0.3f"))
        for name in ("readAdditionalSaveData", "addAdditionalSaveData"):
            b = self.anchors(BOLT, name)
            self.assertEqual((len(b), max(b), b[11]["opcode"]), (6, 11, "return"))
            self.assertEqual({v["symbol"] for v in b.values() if v["symbol"].startswith("String ")},
                             {"String Bubbling"})
            for forbidden in ("Projectile.", "Owner", "seekAmount", "ricochet", "dieIn", "ARC_TOWARDS"):
                self.assertFalse(any(forbidden in v["symbol"] for v in b.values()), forbidden)

    def test_impact_cancellation_callbacks_and_countdown_are_distinct_from_hurt_acceptance(self):
        a = self.anchors(BOLT, "tick")
        self.assertIn("ProjectileUtil.getHitResultOnMoveVector:", a[662]["symbol"])
        self.assertIn("HitResult$Type.MISS", a[672]["symbol"])
        self.assertEqual((a[675]["opcode"], a[675]["operand"]), ("if_acmpeq", "693"))
        self.assertIn("EventHooks.onProjectileImpact:", a[681]["symbol"])
        self.assertEqual((a[684]["opcode"], a[684]["operand"]), ("ifne", "693"))
        self.assertIn("onHit:", a[690]["symbol"])
        self.assertEqual((a[697]["opcode"], a[697]["operand"]), ("ifle", "721"))
        self.assertEqual([a[p]["opcode"] for p in (705, 706, 707)], ["iconst_1", "isub", "putfield"])
        self.assertIn("discard:()V", a[718]["symbol"])
        hit = self.anchors(BOLT, "onHitEntity")
        self.assertEqual((len(hit), hit[78]["opcode"]), (37, "return"))
        self.assertIn("Level.isClientSide", hit[36]["symbol"])
        self.assertIn("ownedBy:", hit[47]["symbol"])
        for p, opcode in ((39, "ifne"), (50, "ifne"), (58, "if_icmple")):
            self.assertEqual((hit[p]["opcode"], hit[p]["operand"]), (opcode, "78"))
        self.assertEqual(hit[57]["opcode"], "iconst_2")
        self.assertIn("damageMobs:()V", hit[62]["symbol"])
        self.assertEqual((hit[69]["opcode"], hit[74]["opcode"]), ("iconst_m1", "iconst_5"))
        block = self.anchors(BOLT, "onHitBlock")
        self.assertEqual((len(block), block[59]["opcode"]), (28, "return"))
        self.assertEqual((block[39]["opcode"], block[39]["operand"]), ("ifne", "59"))
        self.assertIn("damageMobs:()V", block[43]["symbol"])
        self.assertEqual((block[50]["opcode"], block[55]["opcode"]), ("iconst_m1", "iconst_5"))

    def test_damage_filters_fixed_request_and_ricochet_preserve_native_acceptance_boundary(self):
        a = self.anchors(BOLT, "damageMobs")
        self.assertEqual((len(a), max(a)), (105, 242))
        self.assertIn("DamageSources.mobProjectile:", a[27]["symbol"])
        self.assertEqual({a[p]["symbol"] for p in (35, 38, 41)}, {"double 2.0d"})
        self.assertIn("LivingEntity", a[55]["symbol"])
        for p in (96, 104, 117, 126):
            self.assertEqual((a[p]["opcode"], a[p]["operand"]), ("ifne", "216"))
        self.assertIn("DeepOneBaseEntity", a[101]["symbol"])
        self.assertEqual((a[131]["opcode"], a[131]["operand"]), ("astore", "4"))
        self.assertEqual(a[136]["symbol"], "float 3.0f")
        self.assertIn("ACCompat.hurt:", a[139]["symbol"])
        self.assertEqual((a[142]["opcode"], a[142]["operand"]), ("ifeq", "216"))
        self.assertIn("isBubbling:()Z", a[146]["symbol"])
        self.assertEqual((a[149]["opcode"], a[149]["operand"]), ("ifeq", "216"))
        self.assertEqual(a[172]["operand"], "200")
        self.assertIn("LivingEntity.addEffect:", a[178]["symbol"])
        self.assertEqual(a[181]["opcode"], "pop")
        self.assertIn("ricochet:Z", a[220]["symbol"])
        self.assertEqual((a[223]["operand"], a[228]["operand"], a[232]["opcode"]),
                         ("242", "242", "iconst_0"))
        self.assertIn("onRicochetHit:", a[239]["symbol"])
        ricochet = self.anchors(BOLT, "onRicochetHit")
        self.assertEqual((len(ricochet), max(ricochet)), (122, 270))
        self.assertIn("LivingEntity", ricochet[160]["symbol"])
        self.assertEqual((ricochet[163]["opcode"], ricochet[163]["operand"]), ("ifeq", "270"))
        self.assertIn('"<init>":' + LAUNCH_CTOR, ricochet[182]["symbol"])
        self.assertIn("copyPosition:", ricochet[190]["symbol"])
        self.assertIn("setArcingTowards:", ricochet[200]["symbol"])
        self.assertIn("setBubbling:", ricochet[257]["symbol"])
        self.assertIn("Level.addFreshEntity:", ricochet[266]["symbol"])
        self.assertEqual(ricochet[269]["opcode"], "pop")
        for forbidden in ("TRIPLE_SPLASH", "seekAmount", "ricochet:Z", "enchantLevel"):
            self.assertFalse(any(forbidden in v["symbol"] for v in ricochet.values()), forbidden)

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
        self.assertIn("triple_splash", ids)
        self.assertIn("triple_splash", present)
        missing = sorted(ids - present)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:triple_splash`", crosswalk)
        if missing:
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            self.assertNotRegex(crosswalk, r"A \*\*próxima identidade[^\n]*é `alexscaves:")


if __name__ == "__main__":
    unittest.main()
