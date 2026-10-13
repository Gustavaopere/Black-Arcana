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
    def test_pinned_real_matrix_maps_all_39_to_the_69_crosswalk(self):
        matrix = mod.load_matrix()
        crosswalk = mod.load_crosswalk()
        self.assertEqual(39, len(matrix))
        self.assertEqual(69, len(crosswalk))
        self.assertTrue(set(matrix).issubset(crosswalk))
        self.assertEqual(915, sum(x['semantic_objects'] for x in matrix.values()))
        self.assertEqual('ars_nouveau-1.21.1-5.13.1.jar', crosswalk['Ars Nouveau'])

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

    def test_real_frozen_campaign_has_fourteen_existing_exact_registries(self):
        matrix = mod.load_matrix()
        self.assertEqual(39, len(matrix))
        self.assertEqual(14, sum(
            x['catalog_evidence'] == 'COUNTED_EXACT' for x in matrix.values()
        ))
        self.assertEqual(
            {'version': '21.3.0', 'semantic_objects': 5,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Ars Additions'],
        )
        self.assertEqual(
            {'version': '1.6.16', 'semantic_objects': 9,
             'catalog_evidence': 'COUNTED_EXACT'}, matrix['Ars Controle'])
        self.assertEqual(
            {'version': '2.7.6', 'semantic_objects': 11,
             'catalog_evidence': 'COUNTED_EXACT'}, matrix['Ars Technica'])
        self.assertEqual({'version': '2.0.2', 'semantic_objects': 18,
                          'catalog_evidence': 'COUNTED_EXACT'}, matrix['Ars Zero'])
        self.assertEqual(
            {'version': '5.0.4b', 'semantic_objects': 1,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Ars Hex'],
        )
        self.assertEqual(
            {'version': '0.1.3-alpha', 'semantic_objects': 1,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Crystal Chronicles'],
        )
        self.assertEqual(
            {'version': '1.1.9', 'semantic_objects': 4,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Dreamless Spells'],
        )
        self.assertEqual(
            {'version': '1.1.1', 'semantic_objects': 5,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Paladin Spells'],
        )
        self.assertEqual(
            {'version': '1.0.5', 'semantic_objects': 7,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix["Wind's Spellbooks"],
        )
        self.assertEqual(
            {'version': 'physical 0.1.2 / embedded 0.1.0', 'semantic_objects': 6,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Backported Spellbooks'],
        )
        self.assertEqual(
            {'version': '1.3.3 Version B', 'semantic_objects': 4,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix['Deeper & Darker Spellbooks'],
        )
        self.assertEqual({'version': '1.1.0-1.21.1', 'semantic_objects': 12,
                          'catalog_evidence': 'COUNTED_EXACT'},
                         matrix["GTBC's Geomancy Plus"])
        self.assertEqual(
            {'version': '1.0.5.1-1.21.1', 'semantic_objects': 6,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix["Farmer's Spell 'n Spellbooks"],
        )
        self.assertEqual(
            {'version': '3.3.4', 'semantic_objects': 5,
             'catalog_evidence': 'COUNTED_EXACT'},
            matrix["Ars 'n' Spells"],
        )

    def test_preexisting_exact_registry_does_not_come_from_fingerprint(self):
        matrix, crosswalk, report = fixture()
        original = 'Provider 1'
        filename = crosswalk.pop(original)
        row = matrix.pop(original)
        self.assertEqual(2, row['semantic_objects'])
        matrix['Ars Additions'] = {
            'version': '21.3.0', 'semantic_objects': 5,
            'catalog_evidence': 'COUNTED_EXACT',
        }
        crosswalk['Ars Additions'] = filename
        next(r for r in report['entries'] if r['provider'] == original
             )['provider'] = 'Ars Additions'
        output = mod.build_queue(matrix, crosswalk, report)
        self.assertEqual(39, len(output['providers']))
        self.assertEqual(1, output['catalog_exact_preexisting'])
        self.assertEqual(38, output['registry_proofs_remaining'])
        self.assertEqual(0, output['registry_proofs_completed'])
        self.assertEqual(39, output['blocked_physical_artifact'])
        item = next(x for x in output['providers']
                    if x['provider'] == 'Ars Additions')
        self.assertEqual('CATALOG_EXACT_PRIOR_INDEPENDENT_AUDIT',
                         item['status'])
        self.assertEqual('MISSING', item['physical_status'])
        self.assertFalse(item['registry_verified'])
        self.assertFalse(item['promotion_allowed'])
        self.assertFalse(item['survival_verified'])
        # A later arbitrary fingerprint is still not the independent proof.
        report_row = next(x for x in report['entries']
                          if x['provider'] == 'Ars Additions')
        report_row.update(status='FINGERPRINTED', sha1='a'*40,
                          sha256='b'*64, size_bytes=300)
        report['counts']['FINGERPRINTED'] = 1
        report['counts']['MISSING'] = 68
        after = mod.build_queue(matrix, crosswalk, report)
        exact = next(x for x in after['providers']
                     if x['provider'] == 'Ars Additions')
        self.assertEqual('CATALOG_EXACT_PRIOR_INDEPENDENT_AUDIT',
                         exact['status'])
        self.assertFalse(exact['registry_verified'])
        self.assertFalse(exact['promotion_allowed'])
        self.assertEqual(1, after['catalog_exact_preexisting'])
        self.assertEqual(38, after['registry_proofs_remaining'])

    def test_exact_registry_label_requires_known_identity_and_exact_count(self):
        matrix, crosswalk, report = fixture()
        matrix['Provider 0']['catalog_evidence'] = 'COUNTED_EXACT'
        with self.assertRaises(ValueError):
            mod.build_queue(matrix, crosswalk, report)
        matrix, crosswalk, report = fixture()
        filename = crosswalk.pop('Provider 1')
        matrix.pop('Provider 1')
        matrix['Ars Additions'] = {
            'version': '21.3.0', 'semantic_objects': 6,
            'catalog_evidence': 'COUNTED_EXACT',
        }
        crosswalk['Ars Additions'] = filename
        next(r for r in report['entries'] if r['provider'] == 'Provider 1'
             )['provider'] = 'Ars Additions'
        with self.assertRaises(ValueError):
            mod.build_queue(matrix, crosswalk, report)

    def test_fourteen_independent_prior_exact_providers_not_report_promoted(self):
        matrix, crosswalk, report = fixture()
        for name, orig, version, count in (
            ('Ars Additions', 'Provider 1', '21.3.0', 5),
            ('Ars Hex', 'Provider 2', '5.0.4b', 1),
            ('Crystal Chronicles', 'Provider 3', '0.1.3-alpha', 1),
            ('Dreamless Spells', 'Provider 4', '1.1.9', 4),
            ('Paladin Spells', 'Provider 5', '1.1.1', 5),
            ("Wind's Spellbooks", 'Provider 6', '1.0.5', 7),
            ('Backported Spellbooks', 'Provider 7', 'physical 0.1.2 / embedded 0.1.0', 6),
            ('Deeper & Darker Spellbooks', 'Provider 8', '1.3.3 Version B', 4),
            ("GTBC's Geomancy Plus", 'Provider 9', '1.1.0-1.21.1', 12),
            ("Farmer's Spell 'n Spellbooks", 'Provider 10', '1.0.5.1-1.21.1', 6),
            ("Ars 'n' Spells", 'Provider 11', '3.3.4', 5),
            ('Ars Controle', 'Provider 12', '1.6.16', 9),
            ('Ars Technica', 'Provider 13', '2.7.6', 11),
            ('Ars Zero', 'Provider 14', '2.0.2', 18),
        ):
            filename = crosswalk.pop(orig)
            matrix.pop(orig)
            crosswalk[name] = filename
            matrix[name] = dict(version=version, semantic_objects=count,
                                catalog_evidence='COUNTED_EXACT')
            next(r for r in report['entries'] if r['provider'] == orig
                 )['provider'] = name
        result = mod.build_queue(matrix, crosswalk, report)
        self.assertEqual(14, result['catalog_exact_preexisting'])
        self.assertEqual(25, result['registry_proofs_remaining'])
        self.assertEqual(0, result['registry_proofs_completed'])
        exact_rows = [x for x in result['providers']
                      if x['status'] == 'CATALOG_EXACT_PRIOR_INDEPENDENT_AUDIT']
        self.assertEqual({'Ars Additions', 'Ars Hex', 'Crystal Chronicles',
                          'Dreamless Spells', 'Paladin Spells', "Wind's Spellbooks", 'Backported Spellbooks',
                          'Deeper & Darker Spellbooks', "GTBC's Geomancy Plus",
                          "Farmer's Spell 'n Spellbooks", "Ars 'n' Spells", 'Ars Controle', 'Ars Technica', 'Ars Zero'},
                         {x['provider'] for x in exact_rows})
        self.assertTrue(all(not x['registry_verified'] and
                            not x['promotion_allowed'] and
                            not x['survival_verified'] for x in exact_rows))

    def test_output_does_not_leak_archive_bodies_or_infer_survival(self):
        matrix, crosswalk, report = fixture()
        report['entries'][0]['bogus_payload'] = 'SECRET FROM THIRD PARTY JAR'
        out = mod.build_queue(matrix, crosswalk, report)
        self.assertNotIn('SECRET FROM THIRD PARTY JAR', json.dumps(out))
        self.assertTrue(all(not x['survival_verified'] for x in out['providers']))


if __name__ == '__main__':
    unittest.main()
