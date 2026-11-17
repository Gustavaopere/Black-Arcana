#!/usr/bin/env python3
"""Fail-closed Raygun consolidated native contract tests.

Set AC_RAYGUN_CONTRACT_JAR and AC_RAYGUN_CONTRACT_JAVAP for physical tests.
Minecraft, networking and gameplay are never executed by these tests.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import alexscaves_1010_raygun_contract_audit as audit

SCRIPT = Path(audit.__file__).resolve()


class RaygunContractAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = audit.load(audit.SEAL)
        cls.rows = {row['method'].split(' ', 1)[0]: row for row in cls.seal['method_dispositions']}

    def test_seven_axes_and_all_methods_have_semantic_dispositions(self):
        self.assertEqual(set(self.seal['static_contract']), {'identity', 'behavior', 'parameters', 'targeting', 'costs', 'integration', 'validation'})
        self.assertEqual(self.seal['census'], {'declared_methods': 26, 'instruction_total': 1111, 'direct_branch_total': 107})
        self.assertEqual(set(self.rows), set(audit.METHOD_FACTS))
        self.assertEqual(len(self.seal['method_dispositions']), 26)
        self.assertTrue(all(row['facts'] and row['pivots'] and row['disposition'] != 'FINGERPRINT_ONLY' for row in self.rows.values()))
        self.assertEqual(self.seal['static_initialization']['instructions'], 3)
        self.assertNotIn('nativeClinit', self.rows)

    def test_publisher_primary_metadata_and_direct_tag_boundary(self):
        self.assertEqual(self.seal['primary_resource'], {'path': audit.PRIMARY, 'sha256': audit.PRIMARY_HASH, 'json': {'exhaustion': 0.3, 'message_id': 'raygun', 'scaling': 'never'}})
        tags = self.seal['direct_damage_type_tags']
        self.assertEqual(tags['count'], 3)
        self.assertEqual(tags['resource_sha256'], audit.DIRECT_TAG_HASHES)
        self.assertTrue(all('alexscaves:raygun' in value['values'] and value['replace'] is False for value in tags['json'].values()))
        self.assertIn('nested vanilla tag resolution NOT_VERIFIED', tags['limits'])

    def test_native_use_solar_state_and_ui_pivots_reject_semantic_drift(self):
        changes = [('use', 65, 'opcode', 'invokeinterface'), ('use', 167, 'symbol', 'Method ACCompat.useConsume:'), ('acInventoryTick', 83, 'opcode', 'iflt'), ('acInventoryTick', 118, 'operand', '130'), ('setCharge', 6, 'symbol', 'String UseTime'), ('getRayPosition', 16, 'operand', '19'), ('getLerpedRayPosition', 16, 'opcode', 'nop'), ('getBarWidth', 12, 'symbol', 'float 100.0f'), ('releaseUsing', 13, 'opcode', 'ifne')]
        for name, row in self.rows.items():
            audit.gamma.check_pivots({'instructions': row['pivots']}, audit.METHOD_PIVOTS[name])
        for name, offset, key, value in changes:
            method = {'instructions': copy.deepcopy(self.rows[name]['pivots'])}
            next(row for row in method['instructions'] if row['offset'] == offset)[key] = value
            with self.subTest(name=name, offset=offset), self.assertRaisesRegex(ValueError, 'pivot drift'):
                audit.gamma.check_pivots(method, audit.METHOD_PIVOTS[name])

    def test_duplicate_unordered_missing_pivots_fail_closed(self):
        rows = self.rows['setCharge']['pivots']
        for changed in (rows + [rows[0]], list(reversed(rows)), rows[1:]):
            with self.subTest(rows=len(changed)), self.assertRaises(ValueError):
                audit.gamma.check_pivots({'instructions': changed}, audit.METHOD_PIVOTS['setCharge'])

    def test_method_roster_missing_extra_or_overloaded_is_rejected(self):
        frozen = self.seal['method_dispositions']
        with self.assertRaisesRegex(ValueError, 'native roster'):
            audit.verify_dispositions([], frozen)
        fake = [{'header': 'public int missing();', 'descriptor': '()I', 'instructions': []}] * 26
        with self.assertRaisesRegex(ValueError, 'duplicate or overloaded'):
            audit.verify_dispositions(fake, frozen)

    def test_conditional_network_write_remains_outside_authorization_claims(self):
        boundary = self.seal['static_contract']['integration']['network_boundary']
        self.assertEqual(boundary['claim'], 'CONDITIONAL_CLIENT_INPUT_TAG_WRITE_ONLY')
        self.assertIn('DataComponents.CUSTOM_DATA', boundary['conditional_receiver'])
        for key in ('authorization', 'sanitization', 'replay_protection', 'codec_and_delivery'):
            self.assertEqual(boundary[key], 'NOT_VERIFIED')
        self.assertEqual(self.seal['safety'], audit.SAFETY)
        self.assertFalse(self.seal['safety']['provider_universe_closed'])
        self.assertEqual(self.seal['safety']['unaccounted_native_roots'], 0)

    def test_cadence_and_charge_repair_are_separate_native_contracts(self):
        parameters = self.seal['static_contract']['parameters']
        self.assertIn('no extra elapsed>=15', parameters['server_damage_gate'])
        self.assertIn('Client only', self.seal['static_contract']['costs']['client_expenditure'])
        self.assertIn('useFail even after reload', self.rows['use']['facts'])
        self.assertIn('no clamp', self.rows['setUseTime']['facts'])
        self.assertIn('does not clamp', self.rows['setCharge']['facts'])
        self.assertIn('not reset for later enchantments', self.seal['anvil_delegate']['facts'])
        self.assertIn('no charge refill', self.seal['anvil_delegate']['facts'])
        self.assertEqual(self.seal['anvil_delegate']['marker_declared_methods'], 0)

    def test_seal_drift_and_scope_promotion_are_rejected(self):
        audit.verify_seal(self.seal, self.seal)
        changes = [lambda s: s['primary_resource']['json'].update(message_id='alexscaves.raygun'), lambda s: s['method_dispositions'].pop(), lambda s: s['method_dispositions'][0]['pivots'][0].update(opcode='nop'), lambda s: s['anvil_delegate'].update(body_sha256='0'*64), lambda s: s['composed_evidence']['prior_seal_sha256'].update({'EXACT-XRAY-CAUSAL-1.0.10.json': '0'*64}), lambda s: s['static_contract']['parameters'].update(warmup_ticks=16), lambda s: s['safety'].update(network_authorization='VERIFIED'), lambda s: s['safety'].update(provider_universe_closed=True), lambda s: s['safety'].update(unaccounted_native_roots=1), lambda s: s.update(claim_scope='GAMEPLAY_CERTIFIED')]
        for idx, change in enumerate(changes):
            changed = copy.deepcopy(self.seal)
            change(changed)
            with self.subTest(mutation=idx), self.assertRaises(ValueError):
                audit.verify_seal(self.seal, changed)

    def test_unsealed_resource_rosters_and_duplicate_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'primary resource fingerprint'):
            audit.verify_resources(b'{}', {})
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
            json.loads('{"scaling":"never","scaling":"always"}', object_pairs_hook=audit.unique_pairs)


class PublisherRaygunContractCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jar = os.environ.get('AC_RAYGUN_CONTRACT_JAR')
        javap = os.environ.get('AC_RAYGUN_CONTRACT_JAVAP')
        if not jar or not javap:
            raise unittest.SkipTest('set AC_RAYGUN_CONTRACT_JAR and AC_RAYGUN_CONTRACT_JAVAP for physical publisher tests')
        cls.jar, cls.javap = Path(jar), Path(javap)
        if not cls.jar.is_file() or not cls.javap.is_file():
            raise AssertionError('configured physical JAR/javap does not exist')
        cls.expected = audit.SEAL.read_bytes()

    def run_cli(self, output, *, jar=None, javap=None, seal=audit.SEAL):
        return subprocess.run([sys.executable, str(SCRIPT), '--jar', str(jar or self.jar), '--javap', str(javap or self.javap), '--seal', str(seal), '--output', str(output)], capture_output=True, text=True, timeout=300, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

    def test_physical_cli_exact_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'report.json'
            for _ in range(2):
                result = self.run_cli(output)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(output.read_bytes(), self.expected)

    def test_physical_cli_refuses_wrong_artifact_unsafe_scope_and_duplicate_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output, wrong, seal = tmp / 'report.json', tmp / 'wrong.jar', tmp / 'seal.json'
            output.write_text('preserve failed-run output\n')
            wrong.write_bytes(b'not the publisher artifact')
            result = self.run_cli(output, jar=wrong)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('artifact fingerprint drift', result.stderr)
            changed = json.loads(self.expected)
            changed['safety']['network_authorization'] = 'VERIFIED'
            seal.write_text(audit.canonical(changed))
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unsafe Raygun', result.stderr)
            seal.write_text('{"claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY","claim_scope":"GAMEPLAY"}')
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('duplicate JSON key', result.stderr)
            self.assertEqual(output.read_text(), 'preserve failed-run output\n')

    def test_physical_cli_refuses_new_accessor_and_anvil_native_transcript_mutations(self):
        for old, new in [('16: d2f', '16: dneg'), ('class com/github/alexmodguy/alexscaves/server/item/AlwaysCombinableOnAnvil', 'class com/github/alexmodguy/alexscaves/server/item/OtherMarker')]:
            with self.subTest(native=old), tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                output, wrapper = tmp / 'report.json', tmp / 'javap-mutated'
                # A successful external javap process lies about a method that
                # is additional to the inherited targeting/damage pipeline.
                wrapper.write_text('#!' + sys.executable + '\nimport subprocess,sys\nr=subprocess.run(' + repr([str(self.javap)]) + '+sys.argv[1:],capture_output=True,text=True)\nsys.stdout.write(r.stdout.replace(' + repr(old) + ',' + repr(new) + '))\nsys.stderr.write(r.stderr)\nsys.exit(r.returncode)\n')
                wrapper.chmod(0o755)
                result = self.run_cli(output, javap=wrapper)
                self.assertNotEqual(result.returncode, 0)
                self.assertRegex(result.stderr, 'fingerprint seal drift|pivot drift|identity drift|seal drift|prior seal changed')
                self.assertFalse(output.exists())

    def test_physical_damage_type_and_direct_tag_resource_mutations(self):
        with zipfile.ZipFile(self.jar) as arc:
            primary = arc.read(audit.PRIMARY)
            tags = {path: arc.read(path) for path in audit.DIRECT_TAG_HASHES}
        audit.verify_resources(primary, tags)
        with self.assertRaisesRegex(ValueError, 'resource fingerprint'):
            audit.verify_resources(primary.replace(b'"never"', b'"always"'), tags)
        with self.assertRaisesRegex(ValueError, 'tag roster'):
            audit.verify_resources(primary, {path: value for path, value in list(tags.items())[1:]})
        changed = dict(tags)
        changed[next(iter(changed))] = b'{"replace":false,"values":[]}'
        with self.assertRaisesRegex(ValueError, 'tag fingerprint'):
            audit.verify_resources(primary, changed)


if __name__ == '__main__':
    unittest.main()
