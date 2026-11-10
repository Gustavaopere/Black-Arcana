#!/usr/bin/env python3
"""Bind the single Tsunami attempt, separate attacks, and partial wave lifecycle."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/tsunami.md"
ITEM = "server/item/OrtholanceItem"
WAVE = "server/entity/item/WaveEntity"
COMPAT = "server/misc/ACCompat"
ITEM_REGISTRY = "server/item/ACItemRegistry"
ENTITY_REGISTRY = "server/entity/ACEntityRegistry"
REGISTRY = "server/enchantment/ACEnchantmentRegistry"
LAUNCH_CTOR = "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V"
TYPE_CTOR = "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V"


class TsunamiContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-TSUNAMI-CONTRACT-1.0.10.json")
        validate_structure(d, profile="tsunami")
        validate_cards(d, P, profile="tsunami")
        return d

    def anchors(self, owner, name, descriptor=None):
        selected = [m for m in self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
                    if m["name"] == name and (descriptor is None or m["descriptor"] == descriptor)]
        self.assertEqual(len(selected), 1, (owner, name, descriptor))
        return {a["offset"]: a for a in selected[0]["anchors"]}

    def test_literal_singleton_rosters_and_both_partial_method_windows(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "TSUNAMI_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            ITEM, WAVE, COMPAT, REGISTRY, ITEM_REGISTRY, ENTITY_REGISTRY,
        )})
        self.assertEqual(set(d["resources"]), {
            "META-INF/neoforge.mods.toml", "assets/alexscaves/lang/en_us.json",
            "assets/alexscaves/lang/pt_br.json", "data/alexscaves/enchantment/tsunami.json",
            "data/alexscaves/enchantment/second_wave.json",
            "data/alexscaves/tags/item/enchantable/ortholance.json",
            "data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json",
            *("data/minecraft/tags/enchantment/" + tag + ".json" for tag in (
                "in_enchanting_table", "non_treasure", "on_random_loot", "tradeable")),
        })
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertEqual((len(methods), sum(len(m["anchors"]) for m in methods)), (51, 901))
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))
        self.assertLessEqual(sum(len(m["anchors"]) for m in methods), 8192)
        # 435 native instructions; 236 from normal/Second Wave paths are omitted.
        release = self.anchors(ITEM, "releaseUsing")
        self.assertEqual((len(release), min(release), max(release)), (199, 0, 869))
        self.assertEqual(sum(o <= 244 for o in release), 123)
        self.assertEqual(sum(o >= 705 for o in release), 76)
        self.assertFalse(any(247 <= o <= 702 for o in release))
        # 318 native instructions; 153 interpolation/client-particle instructions omitted.
        tick = self.anchors(WAVE, "tick")
        self.assertEqual((len(tick), min(tick), max(tick)), (165, 0, 619))
        self.assertEqual(sum(o <= 186 for o in tick), 98)
        self.assertEqual(sum(o >= 486 for o in tick), 67)
        self.assertFalse(any(189 <= o <= 483 for o in tick))

    def test_resources_and_registry_preserve_reverse_exclusion_as_its_own_authority(self):
        d = self.contract()
        for path, expected in (
            ("data/alexscaves/enchantment/tsunami.json",
             "37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242"),
            ("data/alexscaves/enchantment/second_wave.json",
             "68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c"),
            ("data/alexscaves/tags/item/enchantable/ortholance.json",
             "1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac"),
            ("data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json",
             "57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818"),
        ):
            self.assertEqual(d["resources"][path], expected)
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertEqual(d["resources"]["data/minecraft/tags/enchantment/" + tag + ".json"],
                             "6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1")
        registry = self.anchors(REGISTRY, "<clinit>")
        self.assertEqual(set(registry), {239, 242, 245})
        self.assertEqual(registry[239]["symbol"], "String tsunami")
        self.assertIn("key:", registry[242]["symbol"])
        self.assertIn("TSUNAMI:", registry[245]["symbol"])
        key = self.anchors(REGISTRY, "key")
        self.assertIn("Registries.ENCHANTMENT", key[0]["symbol"])
        self.assertEqual(key[3]["symbol"], "String alexscaves")

    def test_release_charge_and_positive_level_snapshot_precede_nonpositive_return(self):
        a = self.anchors(ITEM, "releaseUsing")
        self.assertIn("getUseDuration:", a[3]["symbol"])
        self.assertEqual([a[o]["opcode"] for o in (6, 8, 9)], ["iload", "isub", "iconst_0"])
        self.assertEqual(a[10]["operand"], "60")
        self.assertIn("Mth.clamp:(III)I", a[12]["symbol"])
        self.assertIn("FLINGING:", a[18]["symbol"])
        self.assertIn("TSUNAMI:", a[27]["symbol"])
        self.assertIn("ACCompat.enchantLevel:", a[30]["symbol"])
        self.assertEqual((a[33]["opcode"], a[33]["operand"]), ("ifle", "40"))
        self.assertEqual([a[o]["opcode"] for o in (36, 40, 41)], ["iconst_1", "iconst_0", "istore"])
        self.assertEqual((a[45]["opcode"], a[45]["operand"]), ("ifle", "869"))
        self.assertEqual((a[99]["opcode"], a[99]["operand"]), ("if_icmplt", "836"))
        self.assertIn("Level.isClientSide:", a[103]["symbol"])
        self.assertEqual((a[106]["opcode"], a[106]["operand"]), ("ifne", "836"))
        duration = self.anchors(ITEM, "getUseDuration")
        self.assertEqual((len(duration), duration[0]["symbol"], duration[2]["opcode"]),
                         (2, "int 72000", "ireturn"))
        reader = self.anchors(COMPAT, "enchantLevel")
        self.assertEqual(len(reader), 24)
        self.assertIn("Holder.is:", reader[42]["symbol"])
        self.assertEqual((reader[56]["opcode"], reader[60]["opcode"]), ("ireturn", "iconst_0"))
        self.assertFalse(any("clamp" in v["symbol"] for v in reader.values()))

    def test_launch_vector_retains_prior_motion_and_does_not_assign_wave_velocity(self):
        a = self.anchors(ITEM, "releaseUsing")
        self.assertEqual((a[48]["symbol"], a[57]["symbol"], a[80]["symbol"]),
                         ("float 0.1f", "float 0.1f", "float 0.15f"))
        for offset, name in ((64, "LivingEntity.getDeltaMovement:"), (69, "getViewVector:"),
                             (72, "Vec3.normalize:"), (87, "Vec3.multiply:"), (90, "Vec3.add:")):
            self.assertIn(name, a[offset]["symbol"])
        self.assertEqual((a[149]["opcode"], a[150]["operand"]), ("iconst_5", "10"))
        self.assertIn("LivingEntity.position:", a[153]["symbol"])
        self.assertEqual(a[156]["operand"], "9")
        self.assertIn("Vec3.add:", a[158]["symbol"])
        self.assertIn("Vec3.x:D", a[178]["symbol"])
        self.assertIn("LivingEntity.getY:()D", a[182]["symbol"])
        self.assertIn("Vec3.z:D", a[187]["symbol"])
        self.assertIn("WaveEntity.setPos:(DDD)V", a[190]["symbol"])
        self.assertEqual([a[o]["operand"] for o in (215, 220)], ["9", "9"])
        self.assertIn("Mth.atan2:(DD)D", a[225]["symbol"])
        self.assertEqual(a[228]["symbol"], "double 57.2957763671875d")
        self.assertEqual([a[o]["opcode"] for o in (231, 232, 233)], ["dmul", "d2f", "fneg"])
        branch = {o: v for o, v in a.items() if 144 <= o <= 244}
        self.assertFalse(any("setDeltaMovement:" in v["symbol"] for v in branch.values()))
        self.assertEqual([o for o, v in a.items() if "setDeltaMovement:" in v["symbol"]], [866])
        self.assertEqual((a[844]["operand"], a[847]["symbol"], a[857]["symbol"]),
                         ("853", "float 0.2f", "float 0.1f"))

    def test_one_attempt_sets_twenty_two_five_and_jumps_over_second_wave_even_if_forced(self):
        a = self.anchors(ITEM, "releaseUsing")
        self.assertEqual((a[146]["opcode"], a[146]["operand"]), ("ifeq", "247"))
        self.assertIn('WaveEntity."<init>":' + LAUNCH_CTOR, a[169]["symbol"])
        for value, call, expected, setter in (
            (195, 197, "20", "setLifespan:(I)V"),
            (202, 204, "float 5.0f", "setWaveScale:(F)V"),
            (209, 210, "iconst_2", "setWaitingTicks:(I)V"),
        ):
            self.assertIn(expected, (a[value]["operand"], a[value]["symbol"], a[value]["opcode"]))
            self.assertIn(setter, a[call]["symbol"])
        attempts = [o for o, v in a.items() if "Level.addFreshEntity:" in v["symbol"]]
        self.assertEqual(attempts, [240])
        self.assertEqual(a[243]["opcode"], "pop")
        self.assertEqual((a[244]["opcode"], a[244]["operand"]), ("goto", "705"))
        self.assertEqual(a[705]["symbol"], "class net/minecraft/world/phys/AABB")
        # The selected producer explicitly omits offsets247–702. Its unconditional
        # edge skips both normal primary emission and the Second Wave reader/loop.
        self.assertFalse(any(247 <= o <= 702 for o in a))
        self.assertFalse(any("SECOND_WAVE:" in v["symbol"] for v in a.values()))
        self.assertEqual([o for o, v in a.items() if v["opcode"] == "new" and "WaveEntity" in v["symbol"]], [163])

    def test_direct_attack_uses_distinct_box_source_los_and_dismount_after_dropped_hurt(self):
        a = self.anchors(ITEM, "releaseUsing")
        self.assertEqual([a[o]["operand"] for o in (717, 719)], ["9", "10"])
        self.assertIn("Vec3.scale:", a[722]["symbol"])
        self.assertIn('AABB."<init>":', a[728]["symbol"])
        self.assertEqual(a[731]["opcode"], "dconst_1")
        self.assertIn("AABB.inflate:(D)", a[732]["symbol"])
        self.assertIn("DamageSources.mobAttack:", a[742]["symbol"])
        self.assertIn("ACCompat.attackDamageBonus:", a[748]["symbol"])
        for call, branch, opcode, target, name in (
            (793, 796, "ifne", "833", "isAlliedTo:"),
            (802, 805, "ifne", "833", "equals:"),
            (811, 814, "ifeq", "833", "hasLineOfSight:"),
        ):
            self.assertIn(name, a[call]["symbol"])
            self.assertEqual((a[branch]["opcode"], a[branch]["operand"]), (opcode, target))
        self.assertIn("LivingEntity.hurt:", a[824]["symbol"])
        self.assertEqual(a[827]["opcode"], "pop")
        self.assertIn("LivingEntity.stopRiding:", a[830]["symbol"])
        helper = self.anchors(COMPAT, "attackDamageBonus")
        self.assertIn("EquipmentSlot.MAINHAND", helper[5]["symbol"])
        self.assertIn("ItemStack.forEachModifier:", helper[14]["symbol"])
        summation = self.anchors(COMPAT, "lambda$attackDamageBonus$2")
        self.assertIn("Attributes.ATTACK_DAMAGE", summation[6]["symbol"])
        self.assertIn("AttributeModifier.amount:()D", summation[22]["symbol"])
        self.assertEqual(summation[25]["opcode"], "dadd")
        self.assertFalse(any("operation:" in v["symbol"].lower() for v in summation.values()))

    def test_wave_attack_uses_current_box_field_owner_distinct_filters_and_unconditional_followups(self):
        a = self.anchors(WAVE, "attackEntities")
        self.assertEqual(len(a), 81)
        self.assertIn("getBoundingBox:", a[1]["symbol"])
        self.assertEqual([a[o]["symbol"] for o in (4, 7, 10)], ["double 0.5d"] * 3)
        self.assertIn("AABB.inflate:(DDD)", a[13]["symbol"])
        self.assertEqual(a[23]["symbol"], "Field owner:Lnet/minecraft/world/entity/LivingEntity;")
        self.assertIn("DamageSources.mobProjectile:", a[26]["symbol"])
        for offset, expected in ((72, "isAlliedTo:"), (80, "DeepOneBaseEntity"),
                                 (99, "LivingEntity.equals:"), (111, "LivingEntity.isAlliedTo:")):
            self.assertIn(expected, a[offset]["symbol"])
        self.assertEqual((a[90]["opcode"], a[90]["operand"]), ("ifnull", "117"))
        self.assertEqual([a[o]["opcode"] for o in (120, 121, 122)], ["fload_1", "fconst_1", "fadd"])
        self.assertIn("LivingEntity.hurt:", a[123]["symbol"])
        self.assertEqual(a[126]["opcode"], "pop")
        self.assertIn("setSlamming:(Z)V", a[129]["symbol"])
        self.assertEqual((a[134]["symbol"], a[137]["symbol"]), ("double 0.1d", "double 0.5d"))
        self.assertEqual([a[o]["opcode"] for o in (140, 141, 142, 143)], ["fload_1", "f2d", "dmul", "dadd"])
        self.assertIn("Mth.sin:", a[152]["symbol"])
        self.assertIn("Mth.cos:", a[164]["symbol"])
        self.assertEqual(a[167]["opcode"], "fneg")
        self.assertIn("ACCompat.knockback:", a[169]["symbol"])
        self.assertEqual((a[172]["opcode"], a[172]["operand"]), ("goto", "47"))
        for forbidden in ("getOwner:", "hasLineOfSight:", "hitEntityIds", "ACDamageTypes", "isSlamming:"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)
        knockback = self.anchors(COMPAT, "knockback")
        self.assertEqual(len(knockback), 6)
        self.assertIn("LivingEntity.knockback:(DDD)V", knockback[5]["symbol"])

    def test_wait_returns_on_zero_transition_and_slam_discard_does_not_return_immediately(self):
        a = self.anchors(WAVE, "tick")
        self.assertEqual((a[16]["opcode"], a[16]["operand"]), ("ifle", "45"))
        self.assertIn("Level.isClientSide:", a[23]["symbol"])
        self.assertEqual((a[26]["opcode"], a[26]["operand"]), ("ifne", "39"))
        self.assertEqual([a[o]["opcode"] for o in (34, 35)], ["iconst_1", "isub"])
        self.assertIn("setWaitingTicks:(I)V", a[36]["symbol"])
        self.assertIn("setInvisible:(Z)V", a[41]["symbol"])
        self.assertEqual(a[44]["opcode"], "return")
        self.assertEqual((a[68]["symbol"], a[79]["opcode"]), ("float 10.0f", "fconst_1"))
        self.assertIn("discard:()V", a[102]["symbol"])
        self.assertEqual(a[105]["opcode"], "aload_0")
        self.assertEqual((a[578]["opcode"], a[578]["operand"]), ("if_icmpgt", "604"))
        self.assertEqual((a[585]["operand"], a[587]["operand"]), ("10", "609"))
        self.assertEqual(a[597]["symbol"], "double 0.04d")
        self.assertIn("setSlamming:(Z)V", a[606]["symbol"])
        self.assertEqual(a[616]["symbol"], "Field activeWaveTicks:I")

    def test_wave_server_attack_formula_precedes_move_and_scale_does_not_multiply_acceleration(self):
        a = self.anchors(WAVE, "tick")
        self.assertIn("isNoGravity:()Z", a[106]["symbol"])
        self.assertIn("ACCompat.isInWaterOrBubble:", a[113]["symbol"])
        self.assertEqual(a[125]["symbol"], "double -0.03999999910593033d")
        self.assertEqual(a[140]["symbol"], "float 10.0f")
        self.assertIn("Math.min:(FF)F", a[144]["symbol"])
        self.assertEqual([a[o]["opcode"] for o in (152, 153, 156, 160)],
                         ["dconst_0", "dconst_0", "fmul", "fmul"])
        self.assertEqual(a[157]["symbol"], "float 0.2f")
        self.assertEqual(a[169]["opcode"], "fneg")
        self.assertIn("Vec3.yRot:", a[175]["symbol"])
        accel = {o: v for o, v in a.items() if 135 <= o <= 178}
        self.assertFalse(any("getWaveScale:" in v["symbol"] for v in accel.values()))
        self.assertEqual((a[509]["opcode"], a[509]["operand"]), ("ifne", "530"))
        self.assertIn("getSlamAmount:(F)F", a[515]["symbol"])
        self.assertEqual([a[o]["opcode"] for o in (518, 519, 520, 521, 526)],
                         ["fconst_2", "fmul", "fconst_1", "fadd", "fadd"])
        self.assertIn("getWaveScale:()F", a[523]["symbol"])
        self.assertIn("attackEntities:(F)V", a[527]["symbol"])
        self.assertIn("move:", a[550]["symbol"])
        self.assertEqual([a[o]["symbol"] for o in (534, 555, 558, 561)],
                         ["double 0.8999999761581421d", "double 0.9900000095367432d",
                          "double 0.9800000190734863d", "double 0.9900000095367432d"])
        slam = self.anchors(WAVE, "getSlamAmount")
        self.assertEqual((len(slam), slam[16]["symbol"], slam[18]["opcode"]), (13, "float 0.1f", "fmul"))

    def test_synchronized_defaults_unclamped_accessors_and_dynamic_dimensions(self):
        a = self.anchors(WAVE, "defineSynchedData")
        self.assertEqual(len(a), 31)
        for field, offset, value, expected in (
            ("SLAMMING", 1, 4, "iconst_0"), ("LIFESPAN", 13, 16, "bipush"),
            ("WAITING_TICKS", 26, 29, "iconst_0"), ("Y_ROT", 38, 41, "fconst_0"),
            ("WAVE_SCALE", 50, 53, "fconst_1"),
        ):
            self.assertIn(field + ":", a[offset]["symbol"])
            self.assertEqual(a[value]["opcode"], expected)
        self.assertEqual(a[16]["operand"], "10")
        for name, field in (("getWaveScale", "WAVE_SCALE"), ("setWaveScale", "WAVE_SCALE"),
                            ("getLifespan", "LIFESPAN"), ("setLifespan", "LIFESPAN"),
                            ("getWaitingTicks", "WAITING_TICKS"), ("setWaitingTicks", "WAITING_TICKS"),
                            ("getYRot", "Y_ROT"), ("setYRot", "Y_ROT"),
                            ("isSlamming", "SLAMMING"), ("setSlamming", "SLAMMING")):
            b = self.anchors(WAVE, name)
            self.assertEqual(len(b), 7)
            self.assertTrue(any(field + ":" in v["symbol"] for v in b.values()))
            self.assertFalse(any(v["opcode"].startswith("if") for v in b.values()))
        dimensions = self.anchors(WAVE, "getDimensions")
        self.assertIn("Entity.getDimensions:", dimensions[2]["symbol"])
        self.assertIn("getWaveScale:()F", dimensions[6]["symbol"])
        self.assertIn("EntityDimensions.scale:(F)", dimensions[9]["symbol"])
        refresh = self.anchors(WAVE, "onSyncedDataUpdated")
        self.assertIn("WAVE_SCALE:", refresh[0]["symbol"])
        self.assertIn("refreshDimensions:()V", refresh[11]["symbol"])
        supplier = self.anchors(ENTITY_REGISTRY, "lambda$static$47")
        self.assertEqual([supplier[o]["symbol"] for o in (11, 14)], ["float 0.9f"] * 2)
        self.assertEqual([supplier[o]["opcode"] for o in (20, 24)], ["iconst_1"] * 2)
        self.assertIn("setShouldReceiveVelocityUpdates:", supplier[21]["symbol"])
        self.assertIn("setUpdateInterval:", supplier[25]["symbol"])
        registry = self.anchors(ENTITY_REGISTRY, "<clinit>")
        self.assertEqual(set(registry), {823, 826, 829, 834, 837})
        self.assertEqual(registry[826]["symbol"], "String wave")
        self.assertIn("InvokeDynamic #163:", registry[829]["symbol"])

    def test_initial_owner_uuid_resolver_and_own_nbt_are_distinct_surfaces(self):
        ctor = self.anchors(WAVE, "<init>", LAUNCH_CTOR)
        self.assertIn("setOwner:", ctor[18]["symbol"])
        self.assertEqual(len(self.anchors(WAVE, "<init>", TYPE_CTOR)), 5)
        setter = self.anchors(WAVE, "setOwner")
        self.assertEqual((len(setter), setter[2]["opcode"], setter[18]["opcode"]), (12, "putfield", "putfield"))
        self.assertIn("LivingEntity.getUUID:", setter[15]["symbol"])
        getter = self.anchors(WAVE, "getOwner")
        self.assertEqual(len(getter), 27)
        self.assertIn("ServerLevel.getEntity:", getter[35]["symbol"])
        for name, count in (("readAdditionalSaveData", 19), ("addAdditionalSaveData", 14)):
            b = self.anchors(WAVE, name)
            self.assertEqual(len(b), count)
            self.assertFalse(any(v["opcode"] == "invokespecial" for v in b.values()))
            self.assertEqual({v["symbol"] for v in b.values() if v["symbol"].startswith("String ")},
                             {"String Owner", "String Lifespan"})
            for forbidden in ("WAVE_SCALE", "WAITING_TICKS", "Y_ROT", "SLAMMING", "slamProgress", "activeWaveTicks", "TSUNAMI"):
                self.assertFalse(any(forbidden in v["symbol"] for v in b.values()), forbidden)
        self.assertFalse(any("getOwner:" in v["symbol"] for v in self.anchors(WAVE, "attackEntities").values()))

    def test_use_failure_and_one_used_hand_wear_request_precede_spawn_outcome(self):
        a = self.anchors(ITEM, "use")
        self.assertEqual(len(a), 20)
        self.assertIn("getDamageValue:()I", a[9]["symbol"])
        self.assertIn("getMaxDamage:()I", a[14]["symbol"])
        self.assertEqual([a[o]["opcode"] for o in (17, 18)], ["iconst_1", "isub"])
        self.assertEqual((a[19]["opcode"], a[19]["operand"]), ("if_icmplt", "28"))
        self.assertIn("ACCompat.useFail:", a[24]["symbol"])
        self.assertIn("Player.startUsingItem:", a[30]["symbol"])
        self.assertIn("ACCompat.useConsume:", a[35]["symbol"])
        release = self.anchors(ITEM, "releaseUsing")
        self.assertEqual(release[133]["opcode"], "iconst_1")
        self.assertEqual([o for o, v in release.items() if "hurtAndBreakUsedHand:" in v["symbol"]], [135])
        wear = self.anchors(COMPAT, "hurtAndBreakUsedHand")
        self.assertIn("LivingEntity.getUsedItemHand:", wear[4]["symbol"])
        self.assertIn("slotOf:", wear[7]["symbol"])
        self.assertIn("ItemStack.hurtAndBreak:", wear[10]["symbol"])
        for forbidden in ("isCreative", "instabuild", "Cooldown", "Mana", "Stamina", "consume"):
            self.assertFalse(any(forbidden in v["symbol"] for v in release.values()), forbidden)
        supplier = self.anchors(ITEM_REGISTRY, "lambda$static$110")
        self.assertEqual(supplier[11]["operand"], "340")
        self.assertIn("Rarity.UNCOMMON", supplier[17]["symbol"])
        registry = self.anchors(ITEM_REGISTRY, "<clinit>")
        self.assertEqual(set(registry), {2072, 2075, 2078, 2083, 2086})
        self.assertEqual(registry[2075]["symbol"], "String ortholance")
        self.assertIn("InvokeDynamic #117:", registry[2078]["symbol"])
        native = self.anchors(ITEM, "<init>")
        self.assertEqual((native[20]["symbol"], native[44]["symbol"]),
                         ("double 5.0d", "double -2.4000000953674316d"))

    def test_static_axes_and_dynamic_remaining_queue_do_not_promote_runtime(self):
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
        self.assertEqual({v["path"] for v in certificate["evidence"].values()}, {str((P / CARD).relative_to(ROOT))})
        self.assertIn("NO_MUTATION", (P / CARD).read_text())
        inventory = json.loads((P / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ids = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        present = {p.stem.replace("-", "_") for p in (P / "enchantments").glob("*.md")
                   if p.name not in ("INDEX.md", "README.md")}
        self.assertIn("tsunami", ids)
        self.assertIn("tsunami", present)
        missing = sorted(ids - present)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:tsunami`", crosswalk)
        if missing:
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            self.assertNotRegex(crosswalk, r"A \*\*próxima identidade[^\n]*é `alexscaves:")


if __name__ == "__main__":
    unittest.main()
