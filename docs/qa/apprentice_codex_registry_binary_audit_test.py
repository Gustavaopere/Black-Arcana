#!/usr/bin/env python3
"""Synthetic Java 21 regression tests: never a physical provider gameplay proof."""
from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('registry_binary', HERE / 'apprentice_codex_registry_binary_audit.py')
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
IDS = ['arcane_beam', 'unite_luna', 'palette_shift']


class RegistryCompiledEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        java = root / 'SpellRegistry.java'
        java.write_text('''package jp.aquafactory.apprenticecodex.registry;
import java.util.function.Supplier;
public class SpellRegistry {
    public static class DeferredHolder {}
    private static DeferredHolder reg(String id, Supplier<?> f) { return new DeferredHolder(); }
    public static final DeferredHolder ARCANE_BEAM = reg("arcane_beam", Object::new);
    public static final DeferredHolder UNITE_LUNA = reg("unite_luna", Object::new);
    public static final DeferredHolder PALETTE_SHIFT = reg("palette_shift", Object::new);
}
''', encoding='utf-8')
        subprocess.run(['javac', '-d', str(root), str(java)], check=True, capture_output=True, text=True)
        output = subprocess.run(['javap', '-c', '-p', '-classpath', str(root), m.CLASS],
                                check=True, capture_output=True, text=True)
        cls.disassembly = output.stdout

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_real_javap_shape_pairs_and_no_false_registry_claim(self):
        parsed, fields = m.parse_static_registrations(self.disassembly)
        self.assertEqual([(id, id.upper()) for id in IDS], parsed)
        self.assertEqual(set(id.upper() for id in IDS), set(fields))
        report = m.reconcile(IDS, self.disassembly, count=3)
        self.assertEqual('PASS', report['status'])
        self.assertEqual(3, report['registration_pairs_count'])

    def test_requires_all_ids_exactly_once(self):
        report = m.reconcile(['arcane_beam', 'unite_luna', 'not_registered'],
                             self.disassembly, count=3)
        self.assertEqual('UNPROVEN_OR_MISMATCH', report['status'])
        self.assertEqual(['not_registered'], report['deviations']['missing_ids'])
        self.assertEqual(['palette_shift'], report['deviations']['unexpected_ids'])

    def test_no_or_wrong_registration_opcodes_fails_closed(self):
        wrong = self.disassembly.replace('invokestatic', 'invokevirtual')
        report = m.reconcile(IDS, wrong, count=3)
        self.assertEqual('UNPROVEN_OR_MISMATCH', report['status'])
        self.assertEqual(0, report['registration_pairs_count'])

    def test_nonregistration_literal_must_not_count(self):
        extra = self.disassembly.replace('39: return',
            '39: ldc #99 // String fake_spell\n      41: pop\n      42: return')
        report = m.reconcile(IDS, extra, count=3)
        self.assertEqual('PASS', report['status'])
        self.assertNotIn('fake_spell', report['registration_ids'])

    def test_swapped_field_must_fail(self):
        swapped = self.disassembly.replace('Field ARCANE_BEAM:', 'Field UNITE_LUNA:')
        report = m.reconcile(IDS, swapped, count=3)
        self.assertEqual('UNPROVEN_OR_MISMATCH', report['status'])
        self.assertIn('arcane_beam:UNITE_LUNA', report['deviations']['field_to_id_mismatches'])

    def test_catalog_reader_exactly_83_and_no_duplicate(self):
        text = '## Exact spell registry — 83/83\n\n' + '\n'.join(
            f'- `apprenticecodex:spell_{i:02d}`' for i in range(83)
        ) + '\n## Another section\n'
        values = m.registry_ids(text)
        self.assertEqual(83, len(values))
        with self.assertRaises(m.AuditError):
            m.registry_ids(text.replace('spell_82', 'spell_81'))
        with self.assertRaises(m.AuditError):
            m.registry_ids(text + '\n## Exact spell registry — 83/83\n')

    def test_wrong_number_of_registrations_is_not_certified(self):
        report = m.reconcile(IDS[:2], self.disassembly, count=2)
        self.assertNotEqual('PASS', report['status'])
        self.assertEqual(3, report['registration_pairs_count'])

    def test_bad_catalog_rejected_before_javap(self):
        with self.assertRaises(m.AuditError):
            m.registry_ids('# not the canonical heading\n- `apprenticecodex:arcane_beam`')

    def test_symlink_or_wrong_archive_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            good = d / m.EXPECTED_JAR
            good.write_bytes(b'not-really-a-jar')
            link = d / 'link.jar'
            link.symlink_to(good)
            with self.assertRaises(m.AuditError):
                m.audit(link, '')
            with self.assertRaises(m.AuditError):
                m.audit(good, '')


if __name__ == '__main__':
    unittest.main()
