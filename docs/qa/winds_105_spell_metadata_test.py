#!/usr/bin/env python3
"""Synthetic parser and fail-closed fixtures; no gameplay or publisher artifact implied."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).with_name("winds_105_spell_metadata.py")
spec = importlib.util.spec_from_file_location("winds_105_spell_metadata", PATH)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

SAMPLE = '''public class demo.WindJumpSpell {
  public demo.WindJumpSpell();
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
  public void onCast();
    Code:
       0: fconst_1
       1: ldc #2 // Float 2.5f
       3: invokevirtual #3 // Method net/minecraft/world/entity/Entity.setDeltaMovement:()V
       6: invokestatic #4 // Method foo/Bar.getRange:()F
       9: return
}'''

class WindMetadataTests(unittest.TestCase):
    def test_extracts_symbols_and_literals_by_method(self):
        result = audit.summarize_disassembly(SAMPLE)
        row = result['public void onCast();']
        self.assertIn('net/minecraft/world/entity/Entity.setDeltaMovement:()V', row['invoked_symbols'])
        self.assertIn('foo/Bar.getRange:()F', row['invoked_symbols'])
        self.assertEqual(['1', '2.5'], row['literal_operands'])
        self.assertNotIn('foo/Bar.getRange:()F', result['public demo.WindJumpSpell();']['invoked_symbols'])
    def test_field_read_write_and_numeric_control_are_method_scoped(self):
        disassembly = SAMPLE.replace(
            '       9: return',
            """       9: getfield #5 // Field demo/WindJumpSpell.radius:F
      12: getstatic #6 // Field demo/SpellConfig.DEFAULT_RADIUS:F
      15: fadd
      16: ifge 23
      19: putfield #7 // Field demo/WindJumpSpell.lastRadius:F
      22: return
      23: return""")
        result = audit.summarize_disassembly(disassembly)
        row = result['public void onCast();']
        self.assertEqual(
            ['demo/SpellConfig.DEFAULT_RADIUS:F', 'demo/WindJumpSpell.radius:F'],
            row['read_fields'])
        self.assertEqual(['demo/WindJumpSpell.lastRadius:F'], row['written_fields'])
        self.assertEqual(['fadd'], row['numeric_opcodes'])
        self.assertEqual(['ifge'], row['branch_opcodes'])
        for key in ('read_fields', 'written_fields', 'numeric_opcodes', 'branch_opcodes'):
            self.assertEqual([], result['public demo.WindJumpSpell();'][key])
        # A field access and fadd prove only structural presence, not a radius formula.
        self.assertNotIn('formula', row)

    def test_no_unjustified_field_from_comment_free_opcodes(self):
        disassembly = SAMPLE.replace(
            '       9: return',
            '       9: getfield #99\\n      12: putstatic #98\\n      15: return')
        row = audit.summarize_disassembly(disassembly)['public void onCast();']
        self.assertEqual([], row['read_fields'])
        self.assertEqual([], row['written_fields'])

    def test_missing_method_fails_closed(self):
        with self.assertRaises(audit.AuditError):
            audit.summarize_disassembly('public class NotJava;')
    def test_wrong_or_missing_jar_fails_before_inspection(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(audit.AuditError):
                audit.audit(Path(p) / audit.JAR_NAME)
            bad = Path(p) / audit.JAR_NAME
            bad.write_bytes(b'forged')
            with self.assertRaises(audit.AuditError):
                audit.audit(bad)
    def test_inventory_fixed_at_seven_ids(self):
        self.assertEqual(7, len(audit.ROSTER))
        self.assertEqual('AeropicSpell', audit.ROSTER['aeropic'])
        self.assertNotIn('acrobatic', audit.ROSTER)

if __name__ == '__main__':
    unittest.main()
