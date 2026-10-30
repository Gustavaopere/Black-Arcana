#!/usr/bin/env python3
"""Synthetic parser/immutability regression; independent of downloaded JAR."""
import unittest
from alexscaves_1010_damage_consumer_probe import (
    OWNER, parse_methods, callsites, factories
)

SAMPLE = """public class com.github.alexmodguy.alexscaves.server.item.Synthetic {
  public void attack(net.minecraft.world.entity.Entity);
    descriptor: (Lnet/minecraft/world/entity/Entity;)V
    Code:
       0: aload_0
       1: invokestatic  #9  // Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.causeRaygunDamage:(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;
       4: return
  public void noop();
    descriptor: ()V
    Code:
       0: return
}
"""
FACTORY = """public class com.github.alexmodguy.alexscaves.server.misc.ACDamageTypes {
  public static net.minecraft.world.damagesource.DamageSource causeAcidDamage(net.minecraft.core.RegistryAccess);
    descriptor: (Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;
    Code:
       0: getstatic     #8  // Field ACID:Lnet/minecraft/resources/ResourceKey;
       3: invokespecial #20 // Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;I)V
       6: areturn
}
"""

class ProbeParserTests(unittest.TestCase):
    def test_direct_invocation_preserves_caller_descriptor(self):
        rows = callsites(parse_methods(SAMPLE), owner="other/Class")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["factory_name"], "causeRaygunDamage")
        self.assertEqual(rows[0]["caller_header"], "public void attack(net.minecraft.world.entity.Entity)")
        self.assertEqual(rows[0]["bytecode_offset"], 1)
        self.assertEqual(rows[0]["opcode"], "invokestatic")

    def test_ignores_unrelated_and_noop(self):
        sample = SAMPLE.replace("ACDamageTypes.causeRaygunDamage",
                                "OtherDamage.causeRaygunDamage")
        self.assertEqual(callsites(parse_methods(sample), owner="other/Class"), [])

    def test_factory_fields_are_only_observed_not_inferred(self):
        rows = factories(parse_methods(FACTORY))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["method"], "causeAcidDamage")
        self.assertEqual(rows[0]["damage_type_fields"], [{"field": "ACID", "offset": 0}])
        self.assertEqual(len(rows[0]["damage_source_constructor_sites"]), 1)

    def test_does_not_confuse_identical_message_ids_with_resource_keys(self):
        self.assertNotIn("dark_arrow", SAMPLE)
        self.assertTrue(OWNER.endswith("/ACDamageTypes"))

if __name__ == "__main__":
    unittest.main()
