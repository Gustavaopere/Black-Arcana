#!/usr/bin/env python3
"""Synthetic fail-closed bytecode identity checks, independent of publisher JAR."""
import unittest
import ars_5131_exact_ids_binary_audit as audit

GLYPH_CTOR = """
Compiled from "EffectBlink.java"
public class com.hollingsworth.arsnouveau.common.spell.effect.EffectBlink {
  private com.hollingsworth.arsnouveau.common.spell.effect.EffectBlink();
    Code:
       0: aload_0
       1: getstatic #17  // Field com/hollingsworth/arsnouveau/common/lib/GlyphLib.EffectBlinkID:Ljava/lang/String;
       4: ldc #19        // String Blink
       6: invokespecial #22  // Method com/hollingsworth/arsnouveau/api/spell/AbstractEffect."<init>":(Ljava/lang/String;Ljava/lang/String;)V
       9: return
}
"""
RITUAL = """
public class com.hollingsworth.arsnouveau.common.ritual.RitualFlight {
  public net.minecraft.resources.ResourceLocation getRegistryName();
    Code:
       0: getstatic #9  // Field com/hollingsworth/arsnouveau/common/lib/RitualLib.FLIGHT:Ljava/lang/String;
       3: invokestatic #12  // Method com/hollingsworth/arsnouveau/ArsNouveau.prefix:(Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;
       6: areturn
}
"""
SPECIAL = """
public class com.hollingsworth.arsnouveau.common.spell.effect.EffectReset {
  public com.hollingsworth.arsnouveau.common.spell.effect.EffectReset();
    Code:
       0: aload_0
       1: ldc #9  // String reset
       3: ldc #10 // String Reset
       5: invokespecial #17  // Method com/hollingsworth/arsnouveau/api/spell/AbstractEffect."<init>":(Ljava/lang/String;Ljava/lang/String;)V
       8: return
}
"""

class ExactIdTests(unittest.TestCase):
    def test_manifest_consistent_with_prior_registry_and_catalog(self):
        g,r=audit.manifests()
        self.assertEqual((85,24),(len(g),len(r)))
        self.assertEqual("ars_nouveau:glyph_sense_magic",g["EffectSenseMagic"])
        self.assertEqual("ars_nouveau:ritual_challenge",r["RitualPillagerRaid"])
    def test_glyph_class_and_compiled_field(self):
        self.assertEqual("ars_nouveau:glyph_blink",
            audit.glyph_id(GLYPH_CTOR,"EffectBlink",{"EffectBlinkID":"glyph_blink"}))
    def test_sense_magic_static_same_class_constructor(self):
        dis="""public class EffectSenseMagic {
  static {};
    Code:
       0: new #1 // class com/hollingsworth/arsnouveau/common/spell/effect/EffectSenseMagic
       3: dup
       4: getstatic #2 // Field com/hollingsworth/arsnouveau/common/lib/GlyphLib.EffectSenseMagicID:Ljava/lang/String;
       7: ldc #3 // String Sense Magic
       9: invokespecial #4 // Method "<init>":(Ljava/lang/String;Ljava/lang/String;)V
      12: putstatic #5 // Field INSTANCE:Lcom/hollingsworth/arsnouveau/common/spell/effect/EffectSenseMagic;
      15: return
}"""
        self.assertEqual("ars_nouveau:glyph_sense_magic",audit.glyph_id(dis,"EffectSenseMagic",{"EffectSenseMagicID":"glyph_sense_magic"}))
        with self.assertRaises(audit.AuditError):
            audit.glyph_id(dis.replace('Method "<init>"','Method "fake"'),"EffectSenseMagic",{"EffectSenseMagicID":"glyph_sense_magic"})
    def test_glyph_id_swap_fails(self):
        with self.assertRaisesRegex(audit.AuditError,"mismatch"):
            audit.reconcile({"EffectBlink":"ars_nouveau:glyph_blink"},
                            {"EffectBlink":"ars_nouveau:glyph_harm"},"glyph")
    def test_missing_glyph_field_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.glyph_id(GLYPH_CTOR,"EffectBlink",{})
    def test_duplicate_glyph_field_fails(self):
        mutated=GLYPH_CTOR.replace('4: ldc #19','4: getstatic #23 // Field com/hollingsworth/arsnouveau/common/lib/GlyphLib.EffectHarmID:Ljava/lang/String;\n       5: ldc #19')
        with self.assertRaises(audit.AuditError):
            audit.glyph_id(mutated,"EffectBlink",{"EffectBlinkID":"glyph_blink","EffectHarmID":"glyph_harm"})
    def test_wrong_constructor_fails(self):
        bad=GLYPH_CTOR.replace('AbstractEffect."<init>":','OtherClass."<init>":')
        with self.assertRaises(audit.AuditError):
            audit.glyph_id(bad,"EffectBlink",{"EffectBlinkID":"glyph_blink"})
    def test_special_unprefixed_reset(self):
        self.assertEqual("ars_nouveau:reset",audit.glyph_id(SPECIAL,"EffectReset",{}))
    def test_wrong_special_literal_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.glyph_id(SPECIAL.replace('String reset','String fake'),"EffectReset",{})
    def test_ritual_class_to_id(self):
        self.assertEqual("ars_nouveau:ritual_flight",
            audit.ritual_id(RITUAL,"RitualFlight",{"FLIGHT":"ritual_flight"}))
    def test_ritual_wrong_namespace_factory_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.ritual_id(RITUAL.replace("ArsNouveau.prefix:","AnotherMod.prefix:"),
                            "RitualFlight",{"FLIGHT":"ritual_flight"})
    def test_ritual_extra_instruction_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.ritual_id(RITUAL.replace("6: areturn","6: nop\n       7: areturn"),
                            "RitualFlight",{"FLIGHT":"ritual_flight"})
    def test_glyph_prefix_factory_bytecode(self):
        content="""public class Lib {
  public static java.lang.String prependGlyph(java.lang.String);
    Code:
       0: aload_0
       1: invokedynamic #7,  0
       6: areturn

BootstrapMethods:
  0: #42 ...
    Method arguments:
      #44 glyph_\\u0001
}"""
        audit.check_prepend(content,"prependGlyph","glyph_")
        with self.assertRaises(audit.AuditError):
            audit.check_prepend(content.replace("glyph_","bad_"),"prependGlyph","glyph_")
    def test_namespace_binding_exact(self):
        content="""public class ArsNouveau {
  public static net.minecraft.resources.ResourceLocation prefix(java.lang.String);
    Code:
       0: ldc #1  // String ars_nouveau
       2: aload_0
       3: invokestatic #2  // Method net/minecraft/resources/ResourceLocation.fromNamespaceAndPath:(Ljava/lang/String;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;
       6: areturn
}"""
        audit.check_namespace(content)
        with self.assertRaises(audit.AuditError):
            audit.check_namespace(content.replace("String ars_nouveau","String other"))
    def test_duplicate_compiled_ids_fail(self):
        with self.assertRaises(audit.AuditError):
            audit.reconcile({"A":"ars_nouveau:glyph_a","B":"ars_nouveau:glyph_b"},
                            {"A":"ars_nouveau:glyph_a","B":"ars_nouveau:glyph_a"},"glyph")

if __name__=="__main__":
    unittest.main()
