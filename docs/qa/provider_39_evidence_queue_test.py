#!/usr/bin/env python3
"""Synthetic evidence tests for the 39-provider binary-registry queue."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

TARGET = Path(__file__).with_name('provider_39_evidence_queue.py')
spec = importlib.util.spec_from_file_location('provider_39_evidence_queue', TARGET)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixture():
    crosswalk = {f'Provider {n}': f'provider-{n}.jar' for n in range(69)}
    matrix = {f'Provider {n}': {
        'version': '1.0', 'semantic_objects': n + 1,
        'catalog_evidence': 'COUNTED_SOURCE_PINNED' if n % 2 else 'COUNTED_RELEASE_BOUNDED',
    } for n in range(39)}
    rows = [{'provider': name, 'filename': filename, 'status': 'MISSING'}
            for name, filename in crosswalk.items()]
    return matrix, crosswalk, {
        'source': 'PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md',
        'evidence_class': 'READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF',
        'expected': 69,
        'counts': {'FINGERPRINTED': 0, 'MISSING': 69, 'UNSAFE': 0, 'OVERSIZED': 0,
                   'INVALID_JAR': 0, 'UNREADABLE': 0, 'CHANGED_DURING_SCAN': 0},
        'entries': rows,
    }


class Provider39EvidenceQueueTest(unittest.TestCase):
    def test_missing_69_still_keeps_39_pending(self):
        matrix, crosswalk, report = fixture()
        output = mod.build_queue(matrix, crosswalk, report)
        self.assertEqual(39, output['expected_binary_registry_proofs'])
        self.assertEqual(0, output['fingerprinted_pending_registry'])
        self.assertEqual(39, output['blocked_physical_artifact'])
        self.assertTrue(all(x['registry_verified'] is False for x in output['providers']))
        self.assertTrue(all(x['promotion_allowed'] is False for x in output['providers']))

    def test_fingerprinted_arbitrary_zip_never_promotes_exact(self):
        matrix, crosswalk, report = fixture()
        row = report['entries'][0]
        row.update(status='FINGERPRINTED', sha1='1'*40, sha256='a'*64, size_bytes=300)
        report['counts']['FINGERPRINTED'] = 1
        report['counts']['MISSING'] = 68
        out = mod.build_queue(matrix, crosswalk, report)
        provider = next(x for x in out['providers'] if x['provider'] == row['provider'])
        self.assertEqual('FINGERPRINTED_PENDING_REGISTRY', provider['status'])
        self.assertEqual('a'*64, provider['jar_sha256'])
        self.assertEqual('COUNTED_RELEASE_BOUNDED', provider['catalog_evidence'])
        self.assertFalse(provider['registry_verified'])
        self.assertFalse(provider['promotion_allowed'])
        self.assertEqual(1, out['fingerprinted_pending_registry'])

    def test_unregistered_or_duplicated_or_renamed_provider_fails(self):
        for change in ('duplicate', 'missing', 'wrongfile'):
            matrix, crosswalk, report = fixture()
            if change == 'duplicate':
                report['entries'][1] = dict(report['entries'][0])
            elif change == 'missing':
                report['entries'].pop()
            else:
                report['entries'][0]['filename'] = 'spoof.jar'
            with self.subTest(change=change), self.assertRaises(ValueError):
                mod.build_queue(matrix, crosswalk, report)

    def test_digest_status_count_and_evidence_forgery_fail_closed(self):
        for change in ('bad_digest', 'unexpected_digest', 'bad_counts', 'wrong_evidence', 'forged_exact'):
            matrix, crosswalk, report = fixture()
            if change == 'bad_digest':
                report['entries'][0].update(status='FINGERPRINTED', sha1='invalid', sha256='a'*64)
                report['counts']['FINGERPRINTED'] = 1
                report['counts']['MISSING'] = 68
            elif change == 'unexpected_digest':
                report['entries'][0]['sha256'] = 'b'*64
            elif change == 'bad_counts':
                report['counts']['MISSING'] = 68
            elif change == 'wrong_evidence':
                report['evidence_class'] = 'REGISTRY_VERIFIED'
            else:
                matrix['Provider 0']['catalog_evidence'] = 'COUNTED_EXACT'
            with self.subTest(change=change), self.assertRaises(ValueError):
                mod.build_queue(matrix, crosswalk, report)

    def test_source_matrix_must_reconcile_exactly_with_manifest(self):
        matrix, crosswalk, report = fixture()
        del matrix['Provider 0']
        with self.assertRaises(ValueError):
            mod.build_queue(matrix, crosswalk, report)
        matrix, crosswalk, report = fixture()
        matrix['Provider 0']['semantic_objects'] = -5
        with self.assertRaises(ValueError):
            mod.build_queue(matrix, crosswalk, report)

    def test_output_does_not_leak_archive_bodies_or_infer_survival(self):
        matrix, crosswalk, report = fixture()
        report['entries'][0]['bogus_payload'] = 'SECRET FROM THIRD PARTY JAR'
        out = mod.build_queue(matrix, crosswalk, report)
        self.assertNotIn('SECRET FROM THIRD PARTY JAR', json.dumps(out))
        self.assertTrue(all(not x['survival_verified'] for x in out['providers']))


if __name__ == '__main__':
    unittest.main()
