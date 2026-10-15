#!/usr/bin/env python3
"""Synthetic and catalog invariants for the physical-JAR audit."""
import importlib.util
from pathlib import Path
import unittest

target=Path(__file__).with_name("reliquified_artifacts_108_binary_audit.py")
spec=importlib.util.spec_from_file_location("reliquified_artifacts_108_binary_audit",target)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class ReliquifiedArtifacts108BinaryTest(unittest.TestCase):
    def test_48_owner_47_class_51_builder_52_semantic(self):
        triples,classes,owners=audit.expected_inventory(audit.INVENTORY.read_text(encoding="utf8"))
        self.assertEqual((52,47,48),(len(triples),len(classes),len(owners)))
        self.assertEqual(51,sum(map(len,classes.values())))
        self.assertEqual({"drinking"},classes["DrinkingHatItem"])
    def test_compiled_direct_literal_builder(self):
        text="""public class x.Test {
  public x.Test();
    Code:
       0: aload_0
  public x.RelicTemplate constructDefaultRelicTemplate();
    Code:
       0: ldc #7 // String trade_surge
       2: invokestatic #8 // Method it/hurts/sskirillss/relics/api/relics/abilities/AbilityTemplate.builder:(Ljava/lang/String;)Lfoo;
       5: areturn
  public void unrelated();
    Code:
       0: ldc #9 // String not_an_ability
}"""
        self.assertEqual({"trade_surge"},audit.template_roots(text))
    def test_nondirect_builder_fails_closed(self):
        text="""  public x.RelicTemplate constructDefaultRelicTemplate();
    Code:
       0: aload_1
       2: invokestatic #8 // Method x/AbilityTemplate.builder:(Ljava/lang/String;)Lfoo;
"""
        with self.assertRaises(audit.AuditError):
            audit.template_roots(text)
    def test_duplicate_builder_fails_closed(self):
        line="       0: ldc #7 // String jump\n       2: invokestatic #8 // Method x/AbilityTemplate.builder:(Ljava/lang/String;)Lfoo;\n"
        with self.assertRaises(audit.AuditError):
            audit.template_roots("  public x.RelicTemplate constructDefaultRelicTemplate();\n    Code:\n"+line+line)
    def test_bad_publisher_file_fails_closed(self):
        with self.assertRaises(audit.AuditError):
            audit.audit(Path("/tmp/not-an-exact-jar.jar"),audit.INVENTORY.read_text(encoding="utf8"))
    def test_owner_literals(self):
        text="  17: ldc #1 // String umbrella\n  22: ldc #2 // String cloud_in_a_bottle\n"
        self.assertEqual({"umbrella","cloud_in_a_bottle"},audit.mixin_literals(text))
    def test_missing_one_inventory_ability_fails_closed(self):
        body="\n".join(line for line in audit.INVENTORY.read_text(encoding="utf8").splitlines() if not line.startswith("| 52 |"))
        with self.assertRaises(audit.AuditError):
            audit.expected_inventory(body)

if __name__=="__main__":
    unittest.main()
