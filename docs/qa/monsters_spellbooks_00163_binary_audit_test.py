#!/usr/bin/env python3
"""Fail-closed safety fixtures for Monsters Spellbooks 0.0.16.3."""
from collections import Counter
import importlib.util
from pathlib import Path
import unittest

MODULE=Path(__file__).with_name("monsters_spellbooks_00163_binary_audit.py")
spec=importlib.util.spec_from_file_location("monsters_spellbooks_00163_binary_audit",MODULE)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class MonstersSpellbooks00163AuditTest(unittest.TestCase):
    def test_source_98_field_class_inventory_is_exact_cardinality(self):
        roster=audit.expected_inventory(audit.INVENTORY.read_text(encoding="utf8"))
        self.assertEqual(98,len(roster))
        self.assertEqual(98,len({v[1] for v in roster.values()}))
        self.assertEqual("SummonWitherArmy",roster["SUMMON_WITHER_ARMY"][1])
        self.assertEqual(audit.FAMILY_COUNTS,dict(Counter(v[0] for v in roster.values())))

    def test_missing_row_fails_closed(self):
        src=audit.INVENTORY.read_text(encoding="utf8")
        src="\n".join(x for x in src.splitlines() if not x.startswith("| 98 |"))
        with self.assertRaises(audit.AuditError):
            audit.expected_inventory(src)

    def test_exact_compiled_resource_from_constructor_and_getter(self):
        disasm="""public class foo.AnticoagulationSpell {
  public foo.AnticoagulationSpell();
    Code:
       0: aload_0
       1: invokespecial #1 // Method x."<init>":()V
       3: aload_0
       4: ldc #2 // String monsterspellbooks
       6: ldc #3 // String anticoagulation
       8: invokestatic #4 // Method net/minecraft/resources/ResourceLocation.fromNamespaceAndPath:(Ljava/lang/String;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;
      11: putfield #5 // Field spellId:Lnet/minecraft/resources/ResourceLocation;
      14: return
  public net.minecraft.resources.ResourceLocation getSpellResource();
    Code:
       0: aload_0
       1: getfield #5 // Field spellId:Lnet/minecraft/resources/ResourceLocation;
       4: areturn
}"""
        self.assertEqual("anticoagulation",audit.spell_id(disasm))
        with self.assertRaises(audit.AuditError):
            audit.spell_id(disasm.replace("String monsterspellbooks","String othermod"))

    def test_compiled_resource_getter_not_just_any_constant(self):
        disasm="""public class Example {
  public ResourceLocation getSpellResource();
    Code:
       0: ldc #2 // String monsterspellbooks
       2: areturn
}"""
        with self.assertRaises(audit.AuditError):
            audit.spell_id(disasm)

    def test_exact_neoforge_mod_id_uses_real_toml_not_comment_scan(self):
        valid = b'modLoader = "javafml"\n[[mods]]\nmodId = "monsterspellbooks"\n'
        self.assertIsNone(audit.require_neoforge_mod_id(valid))
        for bad in (
            b'modLoader = "javafml"\n[[mods]]\nmodId = "othermod"\n',
            b'modLoader = "javafml"\n# modId = "monsterspellbooks"\n[[mods]]\nmodId = "othermod"\n',
            b'modLoader = "javafml"\n[[mods]]\n',
            b'modLoader = "other"\n[[mods]]\nmodId = "monsterspellbooks"\n',
            b'modLoader = "javafml"\n[[mods]]\nmodId = "monsterspellbooks"\n[[mods]]\nmodId = "othermod"\n',
            b'not a toml document = true\n',
            b''
        ):
            with self.subTest(candidate=bad[:80]), self.assertRaises(audit.AuditError):
                audit.require_neoforge_mod_id(bad)
        with self.assertRaises(audit.AuditError):
            audit.require_neoforge_mod_id(b'x' * 256_001)

    def test_wrong_publisher_path_fails_before_introspection(self):
        with self.assertRaises(audit.AuditError):
            audit.audit(Path("/tmp/untrusted-spellbook.jar"),audit.INVENTORY.read_text(encoding="utf8"))

    def test_compiled_field_duplicate_refused(self):
        self.assertEqual(98,len(audit.expected_inventory(audit.INVENTORY.read_text(encoding="utf8"))))
        with self.assertRaises(audit.AuditError):
            audit.registry_pairs("  public static final java.util.function.Supplier<foo> FOO;\n  static {};\n")

if __name__=="__main__":
    unittest.main()
