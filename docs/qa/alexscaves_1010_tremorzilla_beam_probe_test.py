#!/usr/bin/env python3
"""Synthetic negative/positive contracts for exact Tremorzilla beam audit."""
import unittest
from alexscaves_1010_tremorzilla_beam_probe import (
    CLASS, CLASS_SHA, DESCRIPTOR, FACTORY_OFFSET, BeamProbeError,
    bounded, inspect, method_digest, verify_factory, window, verify_sealed_snapshot
)


def op(offset, opcode, operand='', symbol=''):
    return {'offset': offset, 'opcode': opcode, 'operand': operand, 'symbol': symbol}


def method(name='hurtEntitiesAround', desc=DESCRIPTOR):
    return {'header': 'public boolean ' + name + '()',
            'descriptor': desc,
            'instructions': [
                op(0, 'aload_0'),
                op(69, 'invokevirtual', symbol='Method Level.registryAccess:()LRegistryAccess;'),
                op(FACTORY_OFFSET, 'invokestatic',
                   symbol='Method ACDamageTypes.causeTremorzillaBeamDamage:(LRegistryAccess;LEntity;)LDamageSource;'),
                op(79, 'fconst_1'),
                op(81, 'invokestatic', symbol='Method ACCompat.hurt:(LEntity;LDamageSource;F)Z'),
                op(84, 'ifeq', '112'),
                op(112, 'ireturn'),
            ]}


class ExactTremorzillaBeamTests(unittest.TestCase):
    def test_exact_class_identity(self):
        self.assertTrue(CLASS.endswith('/TremorzillaEntity.class'))
        self.assertEqual(len(CLASS_SHA), 64)

    def test_positive_caller_anchor(self):
        a = verify_factory(method())
        self.assertEqual(a['bytecode_offset'], 76)

    def test_wrong_damage_type_rejected(self):
        m = method()
        m['instructions'][2]['symbol'] = 'Method ACDamageTypes.causeNukeDamage:()V'
        with self.assertRaisesRegex(BeamProbeError, 'factory invocation'):
            verify_factory(m)

    def test_relocated_factory_rejected(self):
        m = method()
        m['instructions'][2]['offset'] = 77
        with self.assertRaisesRegex(BeamProbeError, 'factory invocation'):
            verify_factory(m)

    def test_opcode_change_rejected(self):
        m = method()
        m['instructions'][2]['opcode'] = 'invokevirtual'
        with self.assertRaisesRegex(BeamProbeError, 'factory invocation'):
            verify_factory(m)

    def test_descriptor_change_rejected(self):
        with self.assertRaisesRegex(BeamProbeError, 'wrong damage consumer'):
            verify_factory(method(desc='()V'))

    def test_missing_method_rejected(self):
        with self.assertRaisesRegex(BeamProbeError, 'missing/ambiguous'):
            inspect([method(name='other')])

    def test_duplicate_method_rejected(self):
        with self.assertRaisesRegex(BeamProbeError, 'duplicate parsed'):
            inspect([method(), method()])

    def test_duplicate_instruction_offset_rejected(self):
        m = method()
        m['instructions'].append(op(76, 'return'))
        with self.assertRaisesRegex(BeamProbeError, 'duplicated target'):
            inspect([m])

    def test_positive_inspection_no_runtime_claim(self):
        x = inspect([method()])
        self.assertEqual(x['damage_factory_anchor']['bytecode_offset'], 76)
        self.assertEqual(x['damage_method']['exact_damage_and_target_filters'],
                         'INSPECTION_REQUIRED')
        self.assertEqual(x['damage_method']['references']['observed_total'], 3)
        self.assertEqual(len(x['damage_method']['parsed_method_sha256']), 64)

    def test_bounded_export_marks_truncation(self):
        x = bounded(list(range(6)), 2)
        self.assertEqual(x['exported'], [0, 1])
        self.assertTrue(x['truncated'])

    def test_offset_window_is_bounded(self):
        x = window(method(), 76, before=1, after=1)
        self.assertEqual(len(x['instruction_window']), 3)

    def test_method_hash_mutates_if_symbol_changes(self):
        m = method()
        before = method_digest(m)
        m['instructions'][2]['symbol'] += '_CHANGED'
        self.assertNotEqual(before, method_digest(m))


    def sealed_fixture(self):
        body = inspect([method()])
        report = {
            'schema_version': 1, 'scope': 'synthetic', 'artifact': {'sha1': 'test'},
            'class_path': CLASS, 'class_sha256': CLASS_SHA, **body
        }
        seal = {
            'schema_version': 1, 'scope': 'synthetic', 'artifact': {'sha1': 'test'},
            'class_path': CLASS, 'class_sha256': CLASS_SHA,
            'declared_method_count': report['declared_method_count'],
            'damage_factory_anchor': report['damage_factory_anchor'],
            'selected_method_digests': [
                {'name': 'hurtEntitiesAround', 'descriptor': DESCRIPTOR,
                 'sha256': report['damage_method']['parsed_method_sha256']}
            ],
            'local_callers': [],
            'method_anchors': [
                {'group': 'references', 'offset': 76, 'opcode': 'invokestatic',
                 'symbol_contains': 'causeTremorzillaBeamDamage:'}
            ]
        }
        return report, seal

    def test_positive_sealed_fixture_passes(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_sealed_snapshot(report, seal))

    def test_changed_method_hash_rejected(self):
        report, seal = self.sealed_fixture()
        seal['selected_method_digests'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(BeamProbeError, 'method digest'):
            verify_sealed_snapshot(report, seal)

    def test_changed_opcode_rejected(self):
        report, seal = self.sealed_fixture()
        seal['method_anchors'][0]['opcode'] = 'invokevirtual'
        with self.assertRaisesRegex(BeamProbeError, 'opcode anchor drift'):
            verify_sealed_snapshot(report, seal)

    def test_duplicate_sealed_anchor_rejected(self):
        report, seal = self.sealed_fixture()
        seal['method_anchors'].append(dict(seal['method_anchors'][0]))
        with self.assertRaisesRegex(BeamProbeError, 'duplicate sealed'):
            verify_sealed_snapshot(report, seal)

    def test_unexpected_callers_rejected(self):
        report, seal = self.sealed_fixture()
        seal['local_callers'] = [{'method': 'tickBreath', 'descriptor': '()V', 'sites': [552]}]
        with self.assertRaisesRegex(BeamProbeError, 'producer/callsite drift'):
            verify_sealed_snapshot(report, seal)

    def test_changed_exact_operand_rejected(self):
        report, seal = self.sealed_fixture()
        seal['method_anchors'][0]['operand_equals'] = '12345'
        with self.assertRaisesRegex(BeamProbeError, 'operand drift'):
            verify_sealed_snapshot(report, seal)

if __name__ == '__main__':
    unittest.main()
