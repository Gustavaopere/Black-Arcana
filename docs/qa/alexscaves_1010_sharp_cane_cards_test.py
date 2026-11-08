#!/usr/bin/env python3
"""Bind Sharp Cane's snapshot and native acquisition branch without runtime promotion."""
import json
from pathlib import Path
import unittest

from alexscaves_1010_action_contract_audit import load_manifest, validate_cards, validate_structure

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"
CARD = "enchantments/sharp-cane.md"
HOOK = "server/entity/item/CandyCaneHookEntity"
ITEM = "server/item/CandyCaneHookItem"
LAUNCH_CTOR = ("(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;"
               "Lnet/minecraft/world/item/ItemStack;Z)V")


class SharpCaneContract(unittest.TestCase):
    def contract(self):
        d = load_manifest(P / "EXACT-SHARP-CANE-CONTRACT-1.0.10.json")
        validate_structure(d, profile="sharp_cane")
        validate_cards(d, P, profile="sharp_cane")
        return d

    def method(self, owner, name, descriptor=None):
        methods = self.contract()["classes"][PREFIX + owner + ".class"]["methods"]
        selected = [m for m in methods if m["name"] == name
                    and (descriptor is None or m["descriptor"] == descriptor)]
        self.assertEqual(len(selected), 1, (owner, name, descriptor))
        return selected[0]

    def anchors(self, owner, name, descriptor=None):
        return {a["offset"]: a for a in self.method(owner, name, descriptor)["anchors"]}

    def test_literal_identity_resource_roster_and_registry_binding(self):
        d = self.contract()
        self.assertEqual(set(d["cards"]), {CARD})
        self.assertEqual(set(d["contract_evidence"]), {CARD})
        self.assertEqual(d["catalog_family"], "SHARP_CANE_ENCHANTMENT_CONTRACT")
        self.assertEqual(set(d["classes"]), {PREFIX + owner + ".class" for owner in (
            HOOK, ITEM, "server/item/ACItemRegistry", "server/enchantment/ACEnchantmentRegistry",
            "server/misc/ACCompat",
        )})
        methods = [m for entry in d["classes"].values() for m in entry["methods"]]
        self.assertEqual((len(d["classes"]), len(d["resources"]), len(methods),
                          sum(len(m["anchors"]) for m in methods)), (5, 10, 50, 1409))
        self.assertTrue(all(1 <= len(m["anchors"]) <= 256 for m in methods))
        self.assertEqual(d["resources"]["data/alexscaves/enchantment/sharp_cane.json"],
                         "d9d75a98966a4881b93ea877d2e8d9be15539dc7a162ba32de5dce112b41c181")
        self.assertEqual(d["resources"]["data/alexscaves/tags/item/enchantable/candy_cane_hook.json"],
                         "b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310")
        for tag in ("in_enchanting_table", "non_treasure", "on_random_loot", "tradeable"):
            self.assertEqual(d["resources"]["data/minecraft/tags/enchantment/" + tag + ".json"],
                             "6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1")
        registry = self.anchors("server/enchantment/ACEnchantmentRegistry", "<clinit>")
        self.assertEqual(set(registry), {473, 476, 479})
        self.assertEqual(registry[473]["symbol"], "String sharp_cane")
        self.assertIn("key:", registry[476]["symbol"])
        self.assertIn("SHARP_CANE:", registry[479]["symbol"])
        key = self.anchors("server/enchantment/ACEnchantmentRegistry", "key")
        self.assertIn("Registries.ENCHANTMENT", key[0]["symbol"])
        self.assertEqual(key[3]["symbol"], "String alexscaves")

    def test_constructor_snapshots_three_float_times_level_and_synchronized_default_zero(self):
        a = self.anchors(HOOK, "<init>", LAUNCH_CTOR)
        self.assertEqual((len(a), max(a), a[460]["opcode"]), (231, 460, "return"))
        self.assertEqual(a[422]["opcode"], "aload_3")
        self.assertIn("ACEnchantmentRegistry.SHARP_CANE", a[423]["symbol"])
        self.assertIn("ACCompat.enchantLevel", a[426]["symbol"])
        self.assertEqual([a[p]["opcode"] for p in (429, 430, 432, 433)],
                         ["i2f", "ldc", "fmul", "invokevirtual"])
        self.assertEqual(a[430]["symbol"], "float 3.0f")
        self.assertIn("setDamage:(F)V", a[433]["symbol"])
        self.assertEqual({p for p in a if 421 <= p <= 433},
                         {421, 422, 423, 426, 429, 430, 432, 433})
        setter = self.anchors(HOOK, "setDamage")
        getter = self.anchors(HOOK, "getDamage")
        self.assertEqual((len(setter), len(getter)), (7, 7))
        self.assertIn("DAMAGE:", setter[4]["symbol"])
        self.assertEqual(setter[7]["opcode"], "fload_1")
        self.assertIn("Float.valueOf:(F)", setter[8]["symbol"])
        self.assertIn("SynchedEntityData.set:", setter[11]["symbol"])
        self.assertIn("DAMAGE:", getter[4]["symbol"])
        self.assertIn("SynchedEntityData.get:", getter[7]["symbol"])
        self.assertIn("Float.floatValue:()F", getter[13]["symbol"])
        define = self.anchors(HOOK, "defineSynchedData")
        self.assertEqual(len(define), 47)
        self.assertIn("DAMAGE:", define[71]["symbol"])
        self.assertEqual(define[74]["opcode"], "fconst_0")
        self.assertIn("Float.valueOf:(F)", define[75]["symbol"])
        self.assertIn("SynchedEntityData$Builder.define:", define[78]["symbol"])
        tick = self.anchors(HOOK, "tick")
        self.assertEqual([p for p, v in tick.items() if "getDamage:()F" in v["symbol"]],
                         [532, 556])
        for forbidden in ("enchantLevel", "SHARP_CANE", "ItemStack"):
            self.assertFalse(any(forbidden in v["symbol"] for v in tick.values()), forbidden)

    def test_partial_tick_prefix_orders_super_capture_server_and_existing_target_branch(self):
        d = self.contract()
        a = self.anchors(HOOK, "tick")
        self.assertEqual((len(a), min(a), max(a)), (256, 0, 563))
        self.assertEqual(sum(p <= 562 for p in a), 255)
        self.assertLess(len(a), 546)
        self.assertIn("ThrowableProjectile.tick:()V", a[1]["symbol"])
        self.assertIn("getOwner:", a[5]["symbol"])
        self.assertIn("getHookedEntity:", a[10]["symbol"])
        self.assertIn("getPlayerOwner:", a[15]["symbol"])
        self.assertIn("Level.isClientSide:()Z", a[23]["symbol"])
        self.assertEqual((a[26]["opcode"], a[26]["operand"]), ("ifne", "607"))
        self.assertEqual((a[221]["opcode"], a[221]["operand"]), ("ifnull", "355"))
        self.assertIn("Entity.isAlive:()Z", a[225]["symbol"])
        self.assertIn("GumWormEntity.getHookPosition:", a[321]["symbol"])
        self.assertIn("Entity.getBbHeight:()F", a[337]["symbol"])
        self.assertEqual(a[340]["symbol"], "float 0.5f")
        for p in (236, 327, 352):
            self.assertEqual((a[p]["opcode"], a[p]["operand"]), ("goto", "563"))
        self.assertFalse(any("Entity.hurt:" in v["symbol"]
                             for p, v in a.items() if 220 <= p <= 352))
        partial = {(HOOK, "tick"), ("server/enchantment/ACEnchantmentRegistry", "<clinit>"),
                   ("server/item/ACItemRegistry", "<clinit>")}
        complete = [m for owner, entry in d["classes"].items() for m in entry["methods"]
                    if (owner.removeprefix(PREFIX).removesuffix(".class"), m["name"]) not in partial]
        self.assertEqual((len(complete), sum(len(m["anchors"]) for m in complete)), (47, 1146))
        card = (P / CARD).read_text()
        self.assertIn("546 instruções e permanece PARTIAL", card.replace("**", ""))
        self.assertIn("não se declara tick integral ou CFG integral completo", card)

    def test_search_aabb_alive_bootstrap_segment_and_owner_selection_filters(self):
        d = self.contract()
        a = self.anchors(HOOK, "tick")
        self.assertIn("getBoundingBox:", a[356]["symbol"])
        self.assertEqual(a[359]["opcode"], "dconst_1")
        self.assertIn("AABB.inflate:(D)", a[360]["symbol"])
        self.assertEqual(a[375]["opcode"], "invokedynamic")
        self.assertEqual(a[375]["symbol"], "InvokeDynamic #0:test:()Ljava/util/function/Predicate;")
        self.assertIn("Level.getEntities:(Lnet/minecraft/world/entity/Entity;", a[380]["symbol"])
        # The whole class hash seals BootstrapMethods, including #0 -> Entity.isAlive.
        # The invokedynamic anchor alone does not name its method-handle target.
        self.assertEqual(d["classes"][PREFIX + HOOK + ".class"]["sha256"],
                         "e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8")
        self.assertRegex((P / CARD).read_text(), r"BootstrapMethods[^\n]*Entity\.isAlive\(\)")
        self.assertIn("GumWormSegmentEntity", a[414]["symbol"])
        self.assertIn("GumWormSegmentEntity.getHeadEntity:", a[429]["symbol"])
        self.assertEqual((a[441]["opcode"], a[441]["operand"]), ("ifnull", "514"))
        self.assertIn("CandyCaneHookEntity", a[446]["symbol"])
        self.assertIn("projectile/Projectile", a[454]["symbol"])
        for p in (449, 457, 470):
            self.assertEqual((a[p]["opcode"], a[p]["operand"]), ("ifne", "514"))
        self.assertEqual((a[460]["opcode"], a[461]["opcode"], a[461]["operand"]),
                         ("aload_1", "ifnull", "510"))
        self.assertIn("Entity.is:(Lnet/minecraft/world/entity/Entity;)Z", a[467]["symbol"])
        self.assertEqual([p for p, v in a.items() if "Entity.distanceTo:" in v["symbol"]],
                         [481, 487])
        self.assertEqual((a[490]["opcode"], a[491]["opcode"], a[491]["operand"]),
                         ("fcmpg", "iflt", "510"))
        for p in (496, 504):
            self.assertIn("GumWormEntity", a[p]["symbol"])
        self.assertEqual((a[499]["opcode"], a[499]["operand"]), ("ifeq", "514"))
        self.assertEqual((a[507]["opcode"], a[507]["operand"]), ("ifne", "514"))
        self.assertEqual((a[510]["opcode"], a[512]["opcode"], a[512]["operand"]),
                         ("aload", "astore", "6"))

    def test_uuid_precedes_zero_equality_gate_thrown_hurt_and_discarded_boolean(self):
        a = self.anchors(HOOK, "tick")
        self.assertEqual((a[519]["opcode"], a[519]["operand"]), ("ifnull", "563"))
        self.assertIn("Entity.getUUID:()Ljava/util/UUID;", a[525]["symbol"])
        self.assertIn("setHookedEntityUUID:", a[528]["symbol"])
        self.assertIn("getDamage:()F", a[532]["symbol"])
        self.assertEqual([a[p]["opcode"] for p in (535, 536, 537)],
                         ["fconst_0", "fcmpl", "ifeq"])
        self.assertEqual(a[537]["operand"], "563")
        self.assertIn("damageSources:", a[541]["symbol"])
        self.assertEqual((a[544]["opcode"], a[545]["opcode"]), ("aload_0", "aload_1"))
        self.assertIn("DamageSources.thrown:(Lnet/minecraft/world/entity/Entity;"
                      "Lnet/minecraft/world/entity/Entity;)", a[546]["symbol"])
        self.assertEqual((a[549]["opcode"], a[549]["operand"]), ("astore", "7"))
        self.assertEqual((a[551]["operand"], a[553]["operand"]), ("6", "7"))
        self.assertIn("getDamage:()F", a[556]["symbol"])
        self.assertIn("Entity.hurt:(Lnet/minecraft/world/damagesource/DamageSource;F)Z",
                      a[559]["symbol"])
        self.assertEqual((a[562]["opcode"], a[563]["opcode"]), ("pop", "aload_0"))
        self.assertEqual([p for p, v in a.items() if "Entity.hurt:" in v["symbol"]], [559])
        for forbidden in ("hurtAndBreak", "giveExperience", "awardStat"):
            self.assertFalse(any(forbidden in v["symbol"]
                                 for p, v in a.items() if 517 <= p <= 562), forbidden)

    def test_complete_hit_callback_sets_position_and_uuid_without_damage_request(self):
        a = self.anchors(HOOK, "onHitEntity")
        self.assertEqual((len(a), max(a), a[45]["opcode"]), (24, 45, "return"))
        self.assertIn("Vec3.ZERO:", a[1]["symbol"])
        self.assertIn("setDeltaMovement:", a[4]["symbol"])
        self.assertIn("EntityHitResult.getLocation:", a[9]["symbol"])
        self.assertIn("setHookedPosition:", a[12]["symbol"])
        self.assertIn("EntityHitResult.getEntity:", a[16]["symbol"])
        self.assertIn("GumWormSegmentEntity", a[21]["symbol"])
        self.assertEqual((a[24]["opcode"], a[24]["operand"]), ("ifeq", "37"))
        self.assertIn("GumWormSegmentEntity.getHeadEntity:", a[33]["symbol"])
        self.assertIn("Entity.getUUID:", a[39]["symbol"])
        self.assertIn("setHookedEntityUUID:", a[42]["symbol"])
        for forbidden in ("DAMAGE", "getDamage", "hurt:", "damageSources", "enchantLevel"):
            self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)

    def test_complete_own_nbt_overrides_preserve_hook_flags_but_do_not_serialize_damage(self):
        for name, count, end in (("readAdditionalSaveData", 23, 48),
                                 ("addAdditionalSaveData", 22, 45)):
            a = self.anchors(HOOK, name)
            with self.subTest(method=name):
                self.assertEqual((len(a), max(a), a[end]["opcode"]), (count, end, "return"))
                self.assertIn("ThrowableProjectile." + name + ":", a[2]["symbol"])
                strings = {v["symbol"] for v in a.values() if v["symbol"].startswith("String ")}
                self.assertEqual(strings, {"String Reeling", "String HookedEntityUUID", "String Offhand"})
                for forbidden in ("DAMAGE", "getDamage", "setDamage", "Float", "enchantLevel"):
                    self.assertFalse(any(forbidden in v["symbol"] for v in a.values()), forbidden)
        read = self.anchors(HOOK, "readAdditionalSaveData")
        self.assertEqual((read[23]["opcode"], read[23]["operand"]), ("ifeq", "37"))
        self.assertIn("setHookedEntityUUID:", read[34]["symbol"])
        write = self.anchors(HOOK, "addAdditionalSaveData")
        self.assertEqual((write[20]["opcode"], write[20]["operand"]), ("ifnull", "34"))
        self.assertIn("ACCompat.putUUID:", write[31]["symbol"])

    def test_complete_item_launch_eligibility_spawn_attempt_and_reeling_cost_branches(self):
        a = self.anchors(ITEM, "use")
        self.assertEqual((len(a), max(a), a[403]["opcode"]), (188, 403, "areturn"))
        self.assertIn("Level.isClientSide:()Z", a[30]["symbol"])
        self.assertEqual((a[33]["opcode"], a[33]["operand"]), ("ifne", "398"))
        self.assertIn("canLaunchHook:", a[42]["symbol"])
        self.assertEqual((a[45]["opcode"], a[45]["operand"]), ("ifeq", "221"))
        self.assertEqual([a[p]["opcode"] for p in (129, 130, 131)],
                         ["aload_2", "aload_1", "aload"])
        self.assertEqual(a[131]["operand"], "4")
        self.assertIn("InteractionHand.OFF_HAND", a[134]["symbol"])
        self.assertIn('CandyCaneHookEntity."<init>":' + LAUNCH_CTOR, a[145]["symbol"])
        self.assertIn("setOwner:", a[153]["symbol"])
        self.assertEqual(a[158]["opcode"], "iconst_0")
        self.assertIn("setReeling:", a[159]["symbol"])
        self.assertIn("Level.addFreshEntity:", a[172]["symbol"])
        self.assertEqual(a[175]["opcode"], "pop")
        self.assertIn("setLastLaunchedHookUUID:", a[183]["symbol"])
        self.assertIn("setReelingIn:", a[189]["symbol"])
        gate = self.anchors(ITEM, "canLaunchHook")
        self.assertEqual((len(gate), max(gate)), (54, 119))
        self.assertIn("ServerLevel", gate[7]["symbol"])
        self.assertEqual(gate[21]["symbol"], "String LastLaunchedHookUUID")
        self.assertIn("ServerLevel.getEntity:", gate[48]["symbol"])
        self.assertIn("CandyCaneHookEntity", gate[55]["symbol"])
        self.assertIn("CandyCaneHookEntity.isAlive:", gate[70]["symbol"])
        self.assertIn("CandyCaneHookEntity.getOwner:", gate[78]["symbol"])
        self.assertIn("Entity.is:", gate[90]["symbol"])
        self.assertEqual((gate[97]["opcode"], gate[97]["operand"]), ("ifeq", "114"))
        self.assertIn("getHandLaunchedFrom:", gate[104]["symbol"])
        self.assertEqual((gate[107]["opcode"], gate[107]["operand"]), ("if_acmpeq", "114"))
        self.assertEqual([p for p, v in a.items() if "ACCompat.hurtAndBreak:" in v["symbol"]],
                         [299, 328])
        for stack, one, call, check, jump, destination in (
            (294, 296, 299, 275, 278, 302), (323, 325, 328, 304, 307, 398),
        ):
            self.assertEqual(a[stack]["opcode"], "aload")
            self.assertEqual(a[one]["opcode"], "iconst_1")
            self.assertIn("ACCompat.hurtAndBreak:", a[call]["symbol"])
            self.assertIn("isReelingIn:", a[check]["symbol"])
            self.assertEqual((a[jump]["opcode"], a[jump]["operand"]), ("ifne", str(destination)))
        self.assertEqual((a[294]["operand"], a[323]["operand"]), ("5", "4"))
        self.assertFalse(any("SHARP_CANE" in v["symbol"] for v in a.values()))

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
        self.assertIn("sharp_cane", ids)
        self.assertIn("sharp_cane", present)
        missing = sorted(ids - present)
        crosswalk = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("| ✅ | `alexscaves:sharp_cane`", crosswalk)
        if missing:
            self.assertIn("A **próxima identidade em ordem alfabética** sem ficha individual é "
                          + f"`alexscaves:{missing[0]}`;", crosswalk)
        else:
            self.assertNotRegex(crosswalk, r"A \*\*próxima identidade[^\n]*é `alexscaves:")


if __name__ == "__main__":
    unittest.main()
