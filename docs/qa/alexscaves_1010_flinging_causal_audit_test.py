#!/usr/bin/env python3
"""Bounded exact-evidence failures; these do not simulate Minecraft gameplay."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import alexscaves_1010_flinging_causal_audit as audit


class CausalSealTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(audit.SEAL.read_text(encoding='utf8'))

    def reject_changed(self, key, value, both=False):
        report, cert = copy.deepcopy(self.seal), copy.deepcopy(self.seal)
        cert[key] = value
        if both:
            report[key] = copy.deepcopy(value)
        with self.assertRaises(audit.AuditError):
            audit.validate_individual_seal(report, cert)

    def test_exact_seal_accepted(self):
        self.assertEqual(audit.validate_individual_seal(self.seal, self.seal), self.seal)

    def test_self_consistent_wrong_identity_rejected(self):
        self.reject_changed('enchantment', 'alexscaves:tsunami', both=True)

    def test_self_consistent_adjacent_version_rejected(self):
        self.reject_changed('version', '1.1.1', both=True)

    def test_self_consistent_wrong_artifact_rejected(self):
        self.reject_changed('artifact', {**self.seal['artifact'], 'size_bytes': 1}, both=True)

    def test_self_consistent_qa_promotion_rejected(self):
        self.reject_changed('safety', {**audit.SAFETY, 'physical_qa': 'TESTED'}, both=True)

    def test_self_consistent_mutation_promotion_rejected(self):
        self.reject_changed('safety', {**audit.SAFETY, 'mutation': 'ALLOWED'}, both=True)

    def test_self_consistent_hook_promotion_rejected(self):
        self.reject_changed('safety', {**audit.SAFETY, 'mutating_hook': 'VERIFIED'}, both=True)

    def test_runtime_scope_promotion_rejected(self):
        self.reject_changed('claim_scope', 'PERK_READY_RUNTIME', both=True)

    def test_self_consistent_missing_full_method_rejected(self):
        self.reject_changed('method_census', self.seal['method_census'][:-1], both=True)

    def test_self_consistent_missing_resource_rejected(self):
        resources = copy.deepcopy(self.seal['resources']); resources.pop(audit.TAG)
        self.reject_changed('resources', resources, both=True)

    def test_changed_class_hash_rejected(self):
        hashes = copy.deepcopy(self.seal['class_sha256']); hashes[audit.ITEM] = '0'*64
        self.reject_changed('class_sha256', hashes)

    def test_changed_full_method_digest_rejected(self):
        census = copy.deepcopy(self.seal['method_census']); census[0]['body_sha256'] = '0'*64
        self.reject_changed('method_census', census)

    def test_changed_branch_edges_rejected(self):
        census = copy.deepcopy(self.seal['method_census'])
        method = next(x for x in census if x['branch_edges'])
        method['branch_edges'][0][1] += 1
        self.reject_changed('method_census', census)

    def test_added_exception_handler_rejected(self):
        census = copy.deepcopy(self.seal['method_census'])
        census[0]['exception_table'] = [{'from': 0, 'to': 3, 'target': 7, 'type': 'any'}]
        self.reject_changed('method_census', census)

    def test_changed_bootstrap_callback_rejected(self):
        bindings = copy.deepcopy(self.seal['bootstrap_bindings'])
        bindings[0]['callback'] = 'arbitraryCallback'
        self.reject_changed('bootstrap_bindings', bindings)

    def test_second_wave_wrong_two_b_formula_rejected(self):
        contract = {**audit.CONTRACT, 'waves': 'Second Wave adds 2*B delayed requests'}
        self.reject_changed('contract', contract, both=True)

    def test_fixed_aabb_radius_claim_rejected(self):
        contract = {**audit.CONTRACT, 'geometry': 'AABB radius=3 regardless of charge'}
        self.reject_changed('contract', contract, both=True)

    def test_damage_acceptance_claim_rejected(self):
        self.reject_changed('safety', {**audit.SAFETY, 'accepted_damage_or_spawn': 'CERTIFIED'}, both=True)

    def test_new_literal_consumer_rejected(self):
        self.reject_changed('compiled_flinging_token_owners', [audit.ITEM, audit.REGISTRY, 'unproven.class'], both=True)

    def test_declared_level_drift_rejected(self):
        self.reject_changed('resource_json', {**audit.EXPECTED_JSON, 'max_level': 9}, both=True)

    def test_wrong_artifact_fails_before_disassembly(self):
        with tempfile.TemporaryDirectory() as raw:
            jar = Path(raw)/'wrong.jar'; jar.write_bytes(b'not-the-exact-publisher')
            with patch.object(audit, 'javap', side_effect=AssertionError('must not disassemble')):
                with self.assertRaisesRegex(audit.AuditError, 'SHA1/SHA256/size'):
                    audit.extract(jar, 'irrelevant-javap')


class BoundedNativeParsingTests(unittest.TestCase):
    def method(self, rows):
        return {'instructions': [{'offset': at, 'opcode': op, 'operand': arg, 'symbol': ''} for at, op, arg in rows]}

    def test_direct_branch_closed_on_existing_instruction(self):
        self.assertEqual(audit.branch_edges(self.method([(0,'iconst_0',''),(1,'ifeq','5'),(4,'return',''),(5,'return','')])), [[1,5]])

    def test_branch_outside_method_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'outside'):
            audit.branch_edges(self.method([(0,'goto','100'),(3,'return','')]))

    def test_unparsed_branch_operand_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'unparsed'):
            audit.branch_edges(self.method([(0,'goto','1 unknown'),(1,'return','')]))

    def test_duplicate_offsets_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'duplicate/unsorted'):
            audit.branch_edges(self.method([(0,'return',''),(0,'return','')]))

    def test_switch_not_silently_treated_as_direct_cfg(self):
        with self.assertRaisesRegex(audit.AuditError, 'switch/subroutine'):
            audit.branch_edges(self.method([(0,'tableswitch',''),(1,'return','')]))

    def test_empty_method_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'empty'):
            audit.branch_edges(self.method([]))

    def test_excessive_method_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'unbounded'):
            audit.branch_edges(self.method([(n,'nop','') for n in range(1001)]))

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'duplicate JSON'):
            json.loads('{"a":1,"a":2}', object_pairs_hook=audit.strict_pairs)

    def test_exception_table_extracted_separately(self):
        section = 'Exception table:\n       from    to  target type\n          0     4     7   Class java/lang/RuntimeException\n'
        self.assertEqual(audit.exception_table(section), [{'from':0,'to':4,'target':7,'type':'Class java/lang/RuntimeException'}])

    def test_exception_table_heading_without_rows_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'unparsed declared'):
            audit.exception_table('Exception table:\n malformed')

    def test_missing_semantic_method_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, 'missing/ambiguous'):
            audit.checked_pivots({})

    def test_semantic_opcode_drift_rejected_before_seal(self):
        (owner, name), entries = next(iter(audit.PIVOT_SPECS.items()))
        at, op, token = entries[0]
        method = {'instructions':[{'offset':at,'opcode':'nop','operand':'','symbol':token}]}
        with self.assertRaisesRegex(audit.AuditError, 'semantic opcode drift'):
            audit.checked_pivots({(owner,name,'()V'):method})

    def test_static_initializer_has_own_method_identity(self):
        raw = '  static {};\n    descriptor: ()V\n    Code:\n       0: return\n'
        methods = audit.native_index(raw)
        self.assertIn(('__class_init__','()V'), methods)


if __name__ == '__main__':
    unittest.main()
