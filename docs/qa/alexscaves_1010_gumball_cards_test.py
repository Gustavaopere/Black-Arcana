#!/usr/bin/env python3
"""Require the two complete Gumball contracts and the native activation/source boundaries."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX = "com/github/alexmodguy/alexscaves/"

OWN_METHOD_ROSTERS = {'com/github/alexmodguy/alexscaves/server/item/ShotGumItem.class': [('<init>', '()V'),
                                                                    ('initializeClient',
                                                                     '(Ljava/util/function/Consumer;)V'),
                                                                    ('getEnchantmentValue', '()I'),
                                                                    ('isEnchantable',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('shouldCauseReequipAnimation',
                                                                     '(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;Z)Z'),
                                                                    ('getLerpedShootTime',
                                                                     '(Lnet/minecraft/world/item/ItemStack;F)F'),
                                                                    ('getLerpedCrankAngle',
                                                                     '(Lnet/minecraft/world/item/ItemStack;F)F'),
                                                                    ('getShootTime',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)I'),
                                                                    ('setShootTime',
                                                                     '(Lnet/minecraft/world/item/ItemStack;I)V'),
                                                                    ('getCrankAngle',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)F'),
                                                                    ('setCrankAngle',
                                                                     '(Lnet/minecraft/world/item/ItemStack;F)V'),
                                                                    ('getGumballsLeft',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)I'),
                                                                    ('setGumballsLeft',
                                                                     '(Lnet/minecraft/world/item/ItemStack;I)V'),
                                                                    ('isShooting',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('setShooting',
                                                                     '(Lnet/minecraft/world/item/ItemStack;Z)V'),
                                                                    ('hasAmmo',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('use',
                                                                     '(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;'),
                                                                    ('getUseDuration',
                                                                     '(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I'),
                                                                    ('acInventoryTick',
                                                                     '(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V'),
                                                                    ('shouldBeHeldUpright',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('findAmmo',
                                                                     '(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/item/ItemStack;'),
                                                                    ('isBarVisible',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('getBarWidth',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)I'),
                                                                    ('getBarColor',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)I'),
                                                                    ('lambda$static$0',
                                                                     '(Lnet/minecraft/world/item/ItemStack;)Z'),
                                                                    ('<clinit>', '()V')],
 'com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class': [('<init>',
                                                                              '(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V'),
                                                                             ('<init>',
                                                                              '(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V'),
                                                                             ('defineSynchedData',
                                                                              '(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V'),
                                                                             ('getAddEntityPacket',
                                                                              '(Lnet/minecraft/server/level/ServerEntity;)Lnet/minecraft/network/protocol/Packet;'),
                                                                             ('lerpTo', '(DDDFFI)V'),
                                                                             ('lerpMotion', '(DDD)V'),
                                                                             ('tick', '()V'),
                                                                             ('bounceFromDirection',
                                                                              '(Lnet/minecraft/core/Direction;)V'),
                                                                             ('getMaximumBounces', '()I'),
                                                                             ('setMaximumBounces', '(I)V'),
                                                                             ('getBounces', '()I'),
                                                                             ('setBounces', '(I)V'),
                                                                             ('getDamage', '()F'),
                                                                             ('setDamage', '(F)V'),
                                                                             ('getColor', '()I'),
                                                                             ('setColor', '(I)V'),
                                                                             ('targetsOnBounce', '()Z'),
                                                                             ('setTargetsOnBounce', '(Z)V'),
                                                                             ('splitsOnHit', '()Z'),
                                                                             ('setSplitsOnHit', '(Z)V'),
                                                                             ('isExplosive', '()Z'),
                                                                             ('setExplosive', '(Z)V'),
                                                                             ('getDefaultGravity', '()D'),
                                                                             ('onHit',
                                                                              '(Lnet/minecraft/world/phys/HitResult;)V'),
                                                                             ('onHitEntity',
                                                                              '(Lnet/minecraft/world/phys/EntityHitResult;)V'),
                                                                             ('addAdditionalSaveData',
                                                                              '(Lnet/minecraft/nbt/CompoundTag;)V'),
                                                                             ('readAdditionalSaveData',
                                                                              '(Lnet/minecraft/nbt/CompoundTag;)V'),
                                                                             ('getExplodeProgress', '(F)F'),
                                                                             ('<clinit>', '()V')]}

ENCHANTMENT_RESOURCES = {'data/alexscaves/enchantment/bouncy_ball.json': '003c602b45f66154304a0cabdff36b71450da876b071bd355ad604e2cab632ca',
 'data/alexscaves/enchantment/explosive_flavor.json': '2da6cbf1a482c69cb268a65667a4b25ea402bc3d9c7b055ef2bd7e5d8f2d08e8',
 'data/alexscaves/enchantment/targeted_ricochet.json': 'adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e',
 'data/alexscaves/enchantment/triple_split.json': 'fd4f773c48969b4c2537f443cc80d91e1385d545763be78feaefc5816ac551a0'}


class GumballContractCards(unittest.TestCase):
    def anchors(self, manifest, owner, name, descriptor):
        path = owner if owner.startswith(PREFIX) else PREFIX + owner + ".class"
        methods = [m for m in manifest["classes"][path]["methods"]
                   if (m["name"], m["descriptor"]) == (name, descriptor)]
        self.assertEqual(len(methods), 1, (path, name, descriptor))
        return {a["offset"]: a for a in methods[0]["anchors"]}

    def test_full_own_methods_activation_and_three_native_emitters_are_sealed(self):
        final = assert_sealed_damage_contract(self, "gumball")
        for owner, expected in OWN_METHOD_ROSTERS.items():
            with self.subTest(owner=owner):
                methods = final["classes"][owner]["methods"]
                self.assertEqual({(m["name"], m["descriptor"]) for m in methods}, set(expected))
        self.assertEqual(len(OWN_METHOD_ROSTERS[PREFIX + "server/item/ShotGumItem.class"]), 26)
        self.assertEqual(len(OWN_METHOD_ROSTERS[PREFIX + "server/entity/item/GumballEntity.class"]), 29)
        mixin = self.anchors(final, "mixin/ItemStackTickMixin", "ac_inventoryTick",
                            "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;IZLorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V")
        self.assertIn("ACTickingItem", mixin[15]["symbol"])
        self.assertEqual((mixin[18]["opcode"], mixin[18]["operand"]), ("ifeq", "41"))
        self.assertIn("ACTickingItem.acInventoryTick:", mixin[36]["symbol"])
        self.assertEqual(mixin[36]["opcode"], "invokeinterface")
        self.assertIn("alexscaves.mixins.json", final["resources"])
        self.assertIn("alexscaves.mixins.json", final["contract_evidence"]["equipment/shot-gum.md"]["resources"])
        tag_update = self.anchors(final, "server/item/UpdatesStackTags", "updateTagFromServer",
                                  "(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V")
        self.assertIn("ACCompat.setTag:", tag_update[2]["symbol"])
        message = self.anchors(final, "server/message/UpdateItemTagMessage", "handle",
                               "(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V")
        self.assertIn("UpdatesStackTags.updateTagFromServer:", message[174]["symbol"])
        item = self.anchors(final, "server/item/ShotGumItem", "acInventoryTick",
                           "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V")
        self.assertIn('GumballEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V', item[316]["symbol"])
        for method, descriptor, constructor, spawn in (
            ("shootGumball", "(Lnet/minecraft/world/entity/LivingEntity;)V", 80, 274),
            ("tick", "()V", 385, 527),
        ):
            emitter = self.anchors(final, "server/entity/living/GumbeeperEntity", method, descriptor)
            self.assertIn('GumballEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V', emitter[constructor]["symbol"])
            self.assertIn("Level.addFreshEntity:", emitter[spawn]["symbol"])
        for card in ("equipment/shot-gum.md", "damage-types/gumball.md"):
            text = (PROVIDER / card).read_text(encoding="utf8")
            for limit in ("NOT_VERIFIED", "NOT_TESTED", "NO_MUTATION"):
                self.assertIn(limit, text)

    def test_split_source_chain_and_four_native_enchantment_resources_remain_distinct(self):
        final = assert_sealed_damage_contract(self, "gumball")
        primary = self.anchors(final, "server/entity/item/GumballEntity", "<init>",
                               "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V")
        self.assertIn("setOwner:", primary[18]["symbol"])
        helper = self.anchors(final, "server/misc/ACCompat", "createEntity",
                              "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/Entity;")
        self.assertIn("EntityType.create:", helper[2]["symbol"])
        self.assertEqual(helper[5]["opcode"], "areturn")
        registry = self.anchors(final, "server/entity/ACEntityRegistry", "lambda$static$67",
                                "()Lnet/minecraft/world/entity/EntityType;")
        self.assertEqual(registry[0]["opcode"], "invokedynamic")
        impact = self.anchors(final, "server/entity/item/GumballEntity", "onHitEntity",
                              "(Lnet/minecraft/world/phys/EntityHitResult;)V")
        self.assertIn("getOwner:", impact[6]["symbol"])
        self.assertEqual(impact[9]["opcode"], "astore_3")
        self.assertEqual(impact[85]["opcode"], "aload_3")
        self.assertIn("causeGumballDamage:", impact[86]["symbol"])
        self.assertIn("ACCompat.createEntity:", impact[174]["symbol"])
        historical = json.loads((PROVIDER / "EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json").read_text(encoding="utf8"))
        for row in historical["classes"]:
            current = self.anchors(final, row["class_path"], row["name"], row["descriptor"])
            for anchor in row["essential_anchors"] + row["arithmetic_chain"]:
                self.assertEqual(current[anchor["offset"]], anchor)
        for path, expected in ENCHANTMENT_RESOURCES.items():
            with self.subTest(resource=path):
                self.assertEqual(final["resources"][path], expected)
                self.assertIn(path, final["contract_evidence"]["equipment/shot-gum.md"]["resources"])


if __name__ == "__main__":
    unittest.main()
