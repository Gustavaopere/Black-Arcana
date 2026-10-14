#!/usr/bin/env python3
"""Synthetic contract tests. No third-party mod code or JAR is executed."""
import importlib.util
import sys
import unittest
from pathlib import Path

SRC=Path(__file__).with_name("ess_requiem_017_binary_audit.py")
spec=importlib.util.spec_from_file_location("ess_requiem_audit",SRC)
audit=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=audit
spec.loader.exec_module(audit)


def inventory():
    ids=[f"synthetic_{i:02d}" for i in range(58)]
    return "\n".join(
        f"| " + chr(96) + f"ess_requiem:{name}" + chr(96)
        + f" | {'EXCLUDED' if i < 5 else 'COUNTED_SOURCE_PINNED'} | test |"
        for i,name in enumerate(ids)
    )


def registry_class_text():
    return """public class Synthetic {
  public static final java.util.function.Supplier<io.redspace.ironsspellbooks.api.spells.AbstractSpell> FIRST;
  public static final java.util.function.Supplier<io.redspace.ironsspellbooks.api.spells.AbstractSpell> SECOND;

  static {};
    Code:
       0: new           #10  // class net/ender/ess_requiem/spells/FirstSpell
       3: dup
       4: invokespecial #12  // Method net/ender/ess_requiem/spells/FirstSpell."<init>":()V
       7: invokestatic  #14  // Method registerSpell:(Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;)Lnet/neoforged/neoforge/registries/DeferredHolder;
      10: putstatic     #15  // Field FIRST:Ljava/util/function/Supplier;
      13: new           #16  // class net/ender/ess_requiem/spells/SecondSpell
      16: dup
      17: invokespecial #18  // Method net/ender/ess_requiem/spells/SecondSpell."<init>":()V
      20: invokestatic  #14  // Method registerSpell:(Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;)Lnet/neoforged/neoforge/registries/DeferredHolder;
      23: putstatic     #19  // Field SECOND:Ljava/util/function/Supplier;
}
"""


def spell_class_text(root="spark"):
    return """public class net.ender.ess_requiem.spells.SyntheticSpell {
  private final net.minecraft.resources.ResourceLocation spellId;

  public net.ender.ess_requiem.spells.SyntheticSpell();
    Code:
       0: aload_0
       1: invokespecial #1  // Method java/lang/Object."<init>":()V
       4: aload_0
       5: getstatic     #2  // Field net/ender/ess_requiem/EndersSpellsAndStuffRequiem.MOD_ID:Ljava/lang/String;
       8: ldc           #3  // String """ + root + """
      10: invokestatic  #4  // Method net/minecraft/resources/ResourceLocation.fromNamespaceAndPath:(Ljava/lang/String;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;
      13: putfield      #5  // Field spellId:Lnet/minecraft/resources/ResourceLocation;

  public net.minecraft.resources.ResourceLocation getSpellResource();
    Code:
       0: aload_0
       1: getfield      #5  // Field spellId:Lnet/minecraft/resources/ResourceLocation;
       4: areturn
}
"""


class RegistryIdentityTests(unittest.TestCase):
    def test_inventory_requires_58_unique_with_53_counted_and_5_excluded(self):
        result=audit.expected_inventory(inventory())
        self.assertEqual(len(result),58)
        self.assertEqual(sum(v=="EXCLUDED" for v in result.values()),5)
        with self.assertRaises(audit.AuditError):
            audit.expected_inventory(inventory().replace("synthetic_57","synthetic_56"))
        with self.assertRaises(audit.AuditError):
            audit.expected_inventory(inventory().replace(" | EXCLUDED |"," | COUNTED_SOURCE_PINNED |",1))

    def test_registry_pairs_exact_field_and_construction_owner(self):
        result=audit.registry_classes(registry_class_text(),2)
        self.assertEqual(result,{
            "FIRST":"net.ender.ess_requiem.spells.FirstSpell",
            "SECOND":"net.ender.ess_requiem.spells.SecondSpell"
        })

    def test_registry_rejects_duplicate_or_missing_fields(self):
        with self.assertRaises(audit.AuditError):
            audit.registry_classes(registry_class_text().replace("Field SECOND:","Field FIRST:"),2)
        with self.assertRaises(audit.AuditError):
            audit.registry_classes(registry_class_text().replace("class net/ender/ess_requiem/spells/SecondSpell","class net/ender/ess_requiem/spells/FirstSpell"),2)

    def test_compiled_spell_id_is_extracted_from_constructor_and_getter(self):
        self.assertEqual(audit.spell_id(spell_class_text()),"spark")
        self.assertEqual(audit.spell_id(spell_class_text("eldritch_bolt")),"eldritch_bolt")

    def test_getter_must_return_stored_id(self):
        with self.assertRaises(audit.AuditError):
            audit.spell_id(spell_class_text().replace("1: getfield","1: getstatic"))
        with self.assertRaises(audit.AuditError):
            audit.spell_id(spell_class_text("Not-Valid"))

    def test_publisher_sha_is_mandatory_before_javap(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            fake=Path(td)/audit.JAR_NAME
            fake.write_bytes(b"not a publisher jar")
            with patch.object(audit,"run_javap",side_effect=AssertionError("must not call javap")):
                with self.assertRaises(audit.AuditError):
                    audit.audit(fake,inventory())


if __name__=="__main__":
    unittest.main()
