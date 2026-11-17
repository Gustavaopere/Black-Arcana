#!/usr/bin/env python3
"""Raygun contract evidence, historical preservation and scoped index regressions."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
AXES = {'identity', 'behavior', 'parameters', 'targeting', 'costs', 'integration', 'validation'}


class RaygunContractCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / 'EXACT-RAYGUN-CONTRACT-1.0.10.json').read_text())
        cls.card = (PROVIDER / 'damage-types/raygun.md').read_text()
        cls.proof = (PROVIDER / 'EXACT-RAYGUN-CONTRACT-1.0.10.md').read_text()
        cls.ledger = json.loads((ROOT / 'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        cls.inventory = json.loads((PROVIDER / 'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())

    def method(self, name):
        rows = [r for r in self.seal['method_dispositions'] if r['method'].split(' ', 1)[0] == name]
        self.assertEqual(len(rows), 1)
        return rows[0]

    def test_literal_damage_metadata_and_direct_tag_scope(self):
        resource = self.seal['primary_resource']
        self.assertEqual(resource['path'], 'data/alexscaves/damage_type/raygun.json')
        self.assertEqual(resource['sha256'], 'dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35')
        self.assertEqual(resource['json'], {'message_id': 'raygun', 'scaling': 'never', 'exhaustion': 0.3})
        tags = self.seal['direct_damage_type_tags']
        self.assertEqual(tags['scope'], 'EXACT_PUBLISHER_DIRECT_MEMBERSHIPS_ONLY')
        self.assertEqual(tags['count'], 3)
        self.assertEqual({Path(p).stem for p in tags['json']}, {'bypasses_cooldown', 'is_explosion', 'is_projectile'})
        self.assertTrue(all('alexscaves:raygun' in v['values'] for v in tags['json'].values()))

    def test_every_old_method_has_behavior_evidence_beyond_its_fingerprint(self):
        old = json.loads((PROVIDER / 'EXACT-RAYGUN-ALL-METHODS-1.0.10.json').read_text())
        self.assertEqual(old['scope'], 'SHA_EXACT_1010_RAYGUN_26_METHOD_BODY_FINGERPRINTS_ONLY')
        dispositions = self.seal['method_dispositions']
        self.assertEqual(len(dispositions), 26)
        self.assertEqual(self.seal['census'], {'declared_methods': 26, 'instruction_total': 1111, 'direct_branch_total': 107})
        self.assertEqual([{k: row[k] for k in old['methods'][0]} for row in dispositions], old['methods'])
        for row in dispositions:
            self.assertTrue(row['disposition']); self.assertGreater(len(row['facts']), 8)
            self.assertTrue(row['pivots'])
            self.assertEqual(row['evidence'], 'WHOLE_BODY_IDENTITY_PLUS_BOUNDED_SEMANTIC_PIVOTS')
            name = row['method'].split(' ', 1)[0]
            self.assertIn(name, self.card)
        init = self.seal['static_initialization']
        self.assertEqual(init['instructions'], 3)
        self.assertIn('NOT_IN_26_METHOD', init['scope'])

    def test_setters_ui_and_interpolation_are_raw_state_not_cost_receipts(self):
        for name in ['setCharge', 'setUseTime']:
            self.assertIn('raw', self.method(name)['facts'])
            self.assertIn('clamp', self.method(name)['facts'])
        self.assertIn('Vec3.ZERO', self.method('getRayPosition')['facts'])
        self.assertIn('null', self.method('getLerpedRayPosition')['facts'])
        self.assertIn('float', self.method('getLerpedRayPosition')['facts'])
        for name in ['getLerpedUseTime', 'getLerpedRayPosition', 'isBarVisible', 'getBarWidth', 'getBarColor', 'appendHoverText', 'shouldCauseReequipAnimation']:
            self.assertEqual(self.method(name)['disposition'], 'UI_ONLY')
        self.assertIn('1000-ChargeUsed', self.method('appendHoverText')['facts'])

    def test_reload_and_release_do_not_become_an_immediate_new_cast(self):
        use = self.method('use')['facts']
        for token in ['shrink', 'Creative', 'useFail', 'No immediate start']:
            self.assertIn(token, use)
        self.assertIn('URANIUM_ROD', self.method('lambda$static$0')['facts'])
        release = self.method('releaseUsing')['facts']
        for token in ['client', 'sound', 'no own charge or UseTime reset']:
            self.assertIn(token, release)
        self.assertEqual(self.seal['static_contract']['parameters']['duration_ticks'], 72000)

    def test_cost_warmup_and_damage_gate_have_distinct_causality(self):
        contract = self.seal['static_contract']
        self.assertIn('Client only', contract['costs']['client_expenditure'])
        self.assertIn('warmup>=1', contract['costs']['client_expenditure'])
        self.assertIn('no extra elapsed>=15 guard', contract['parameters']['server_damage_gate'])
        self.assertIn('(elapsed-15)%3==0', contract['parameters']['server_damage_gate'])
        for text in [self.card, self.proof]:
            self.assertIn('0/3/6/9/12', text)
            self.assertIn('Energy Efficiency', text)
            self.assertIn('Solar', text)

    def test_target_volume_and_visual_impact_are_not_conflated(self):
        targeting = self.seal['static_contract']['targeting']
        self.assertIn('first nonnull', targeting['scan_break'])
        self.assertIn('remains unchanged', targeting['scan_no_hit'])
        self.assertIn('local21', targeting['impact_and_damage_separation'])
        for text in [self.card, self.proof]:
            self.assertIn('cubo de lado 2', text)
            self.assertIn('Mastery', text)
            self.assertIn('Irradiated', text)
            self.assertIn('Radiation', text)

    def test_network_boundary_and_anvil_remain_conditional_delegates(self):
        boundary = self.seal['static_contract']['integration']['network_boundary']
        self.assertEqual(boundary['claim'], 'CONDITIONAL_CLIENT_INPUT_TAG_WRITE_ONLY')
        for key in ['authorization', 'sanitization', 'replay_protection', 'codec_and_delivery']:
            self.assertEqual(boundary[key], 'NOT_VERIFIED')
        anvil = self.seal['anvil_delegate']
        self.assertEqual(anvil['marker_declared_methods'], 0)
        self.assertEqual(anvil['limits']['complete_anvil_cfg'], 'NOT_RECONSTRUCTED')
        for token in ['setCharge', 'setDamageValue', 'uranium']:
            self.assertIn(token, anvil['facts'])

    def test_old_card_is_preserved_as_non_candidate_history(self):
        archive = PROVIDER / 'damage-types/EXACT-RAYGUN-HISTORICAL-CARD-1.0.10.md'
        raw = archive.read_bytes()
        self.assertEqual(len(raw), 57610)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '75f033bc9c27195c85ca952e0b70bc18ff00f5f1aba1955e58242c98c11e0f87')
        self.assertIn(archive.name, self.card); self.assertIn(archive.name, self.proof)
        import sys
        sys.path.insert(0, str(ROOT / 'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        self.assertFalse(canonical.is_card(archive))

    def test_composed_seals_preserve_their_frozen_bytes(self):
        composed = self.seal['composed_evidence']
        self.assertGreaterEqual(len(composed['prior_seal_sha256']), 10)
        for name, expected in composed['prior_seal_sha256'].items():
            self.assertEqual(hashlib.sha256((PROVIDER / name).read_bytes()).hexdigest(), expected, name)
        self.assertEqual(composed['composed_xray_report_sha256'], '158f03ac7f0369f0a5d90113493ff41314e3d55ea0388a903bd47caf3355aaff')
        self.assertEqual(composed['composed_gamma_report_sha256'], 'cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c')

    def test_seven_axis_certificate_is_individual_static_only(self):
        self.assertEqual(set(self.seal['static_contract']), AXES)
        certificate = self.ledger['objects'][PROVIDER.name + '/damage-types/raygun.md']
        self.assertEqual(set(certificate['evidence']), AXES)
        self.assertEqual(certificate['claim_scope'], 'STATIC_TECHNICAL_CATALOG_ONLY')
        for evidence in certificate['evidence'].values():
            self.assertEqual(Path(evidence['path']).name, 'EXACT-RAYGUN-CONTRACT-1.0.10.md')
            self.assertTrue((ROOT / evidence['path']).is_file())
        self.assertNotIn(PROVIDER.name, self.ledger['providers'])
        self.assertEqual(self.seal['safety']['mutating_hook'], 'NOT_VERIFIED')
        self.assertEqual(self.seal['safety']['physical_qa'], 'NOT_TESTED')
        self.assertEqual(self.seal['safety']['mutation'], 'NO_MUTATION')
        self.assertFalse(self.seal['safety']['provider_universe_closed'])
        for text in [self.card, self.proof]:
            for token in ['STATIC_TECHNICAL_CATALOG_ONLY', 'NOT_VERIFIED', 'NOT_TESTED', 'NOT_CERTIFIED', 'NO_MUTATION', '1.1.1']:
                self.assertIn(token, text)

    def test_damage_current_eleven_and_historical_nine_are_separate(self):
        family = self.inventory['family_catalog_status']['damage_types']
        self.assertEqual(family['documented_static_contracts'], 9)
        self.assertEqual(len(family['cards']), 9)
        self.assertEqual(family['current_documented_static_contracts'], 11)
        self.assertEqual(set(family['current_cards']) - set(family['cards']), {'damage-types/tremorzilla-beam.md', 'damage-types/raygun.md'})
        self.assertEqual(len(family['current_cards']), 11)
        self.assertTrue(all(PROVIDER.name + '/' + card in self.ledger['objects'] for card in family['current_cards']))
        self.assertEqual(set(self.inventory['remaining_family_inventory']['damage_type_ids']), {Path(c).stem.replace('-', '_') for c in family['current_cards']})
        self.assertFalse(self.inventory['whole_provider_catalog_closed'])

    def test_scoped_indexes_show_completion_without_provider_promotion(self):
        child = (PROVIDER / 'damage-types/INDEX.md').read_text()
        self.assertIn('**Catálogo desta árvore:** ✅', child)
        self.assertIn('11/11', child); self.assertIn('100.0%', child)
        provider_index = (PROVIDER / 'INDEX.md').read_text()
        self.assertIn('81/81', provider_index); self.assertIn('100.0%', provider_index)
        self.assertIn('**Catálogo desta árvore:** ⚠️', provider_index)
        self.assertNotIn(PROVIDER.name, self.ledger['providers'])


if __name__ == '__main__':
    unittest.main()
