#!/usr/bin/env python3
"""Synthetic binary string markers, no publisher JAR contents or code."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_irons_lifesteal_host import find_lifesteal_class_names, certify_post_hit_lifesteal

class HostSymbolIndexTests(unittest.TestCase):
    def test_identifies_owner_and_consumer_from_marker(self):
        rows=[
          ("io/redspace/ironsspellbooks/damage/SpellDamageSource.class",
           b"XgetLifestealPercentY"),
          ("io/redspace/ironsspellbooks/events/SpellDamageEvents.class",
           b"GET_LIFESTEAL_PERCENT"),
          ("example/Unrelated.class",b"damage only"),
        ]
        self.assertEqual(
          ["io.redspace.ironsspellbooks.damage.SpellDamageSource",
           "io.redspace.ironsspellbooks.events.SpellDamageEvents"],
          find_lifesteal_class_names(rows))

    def test_duplicate_archive_class_member_rejected(self):
        rows=[("example/A.class",b"lifesteal"),("example/A.class",b"lifesteal")]
        with self.assertRaises(GateError):
            find_lifesteal_class_names(rows)

    def test_suspicious_class_member_rejected(self):
        with self.assertRaises(GateError):
            find_lifesteal_class_names([("../escape.class",b"lifesteal")])

    def test_marker_absence_must_fail_closed(self):
        with self.assertRaises(GateError):
            find_lifesteal_class_names([("example/A.class",b"unrelated")])


def host_fixture():
    rows=[(i*3,"nop","","") for i in range(65)]
    modifications={
       13:("invokevirtual","","Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getNewDamage:()F"),
       14:("fstore_3","",""),
       16:("invokevirtual","","Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getEntity:()Lnet/minecraft/world/entity/LivingEntity;"),
       17:("astore","4",""),
       19:("invokevirtual","","Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getSource:()Lnet/minecraft/world/damagesource/DamageSource;"),
       20:("invokevirtual","","Method net/minecraft/world/damagesource/DamageSource.getEntity:()Lnet/minecraft/world/entity/Entity;"),
       21:("astore","5",""),
       22:("aload","5",""),
       23:("instanceof","#69","class net/minecraft/world/entity/LivingEntity"),
       24:("ifeq","120",""),
       25:("aload","5",""),
       26:("checkcast","#69","class net/minecraft/world/entity/LivingEntity"),
       27:("astore","6",""),
       28:("aload_2","",""),
       29:("invokevirtual","","Method io/redspace/ironsspellbooks/damage/SpellDamageSource.getLifestealPercent:()F"),
       30:("fconst_0","",""),
       31:("fcmpl","",""),
       32:("ifle","120",""),
       33:("aload","6",""),
       34:("aload_2","",""),
       35:("invokevirtual","","Method io/redspace/ironsspellbooks/damage/SpellDamageSource.getLifestealPercent:()F"),
       36:("fload_3","",""),
       37:("fmul","",""),
       38:("invokevirtual","","Method net/minecraft/world/entity/LivingEntity.heal:(F)V"),
    }
    for i,(op,arg,comment) in modifications.items():
        rows[i]=(i*3,op,arg,comment)
    return rows

class PostHitLifestealStackTests(unittest.TestCase):
    def test_heal_source_entity_for_new_damage_times_rate(self):
        report=certify_post_hit_lifesteal(host_fixture())
        self.assertEqual("HOST_POSTHIT_TYPED_HEAL_STACK",report["assurance"])
        self.assertEqual("event.getSource().getEntity() as LivingEntity",report["heal_receiver"])
        self.assertEqual("getLifestealPercent() * event.getNewDamage()",report["requested_heal_expression"])

    def test_target_entity_is_not_heal_receiver(self):
        rows=host_fixture()
        rows[33]=(99,"aload","4","")
        with self.assertRaises(GateError):
            certify_post_hit_lifesteal(rows)

    def test_mutated_amount_local_rejected(self):
        rows=host_fixture()
        rows[36]=(108,"fload","4","")
        with self.assertRaises(GateError):
            certify_post_hit_lifesteal(rows)

    def test_wrong_lifesteal_getter_rejected(self):
        rows=host_fixture()
        rows[35]=(105,"invokevirtual","","Method io/redspace/ironsspellbooks/damage/SpellDamageSource.getFreezeTicks:()I")
        with self.assertRaises(GateError):
            certify_post_hit_lifesteal(rows)

    def test_missing_positive_percent_guard_rejected(self):
        rows=host_fixture()
        rows[32]=(96,"ifge","120","")
        with self.assertRaises(GateError):
            certify_post_hit_lifesteal(rows)

    def test_wrong_source_actor_type_rejected(self):
        rows=host_fixture()
        rows[26]=(78,"checkcast","#69","class net/minecraft/world/entity/player/Player")
        with self.assertRaises(GateError):
            certify_post_hit_lifesteal(rows)

if __name__=="__main__":
    unittest.main()
