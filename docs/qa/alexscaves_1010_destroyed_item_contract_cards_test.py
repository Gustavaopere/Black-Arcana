#!/usr/bin/env python3
"""Destruction callback semantics, registry identity and certification boundaries."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'
TARGET=PREFIX+'server/item/ACDestroyedItem'
IMPL=PREFIX+'server/item/RadioactiveOnDestroyedBlockItem'
AXES={'identity','behavior','parameters','targeting','costs','integration','validation'}


class DestroyedItemContractCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/'EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json').read_text())
        cls.card=(PROVIDER/'systems/destroyed-item.md').read_text()
        cls.proof=(PROVIDER/'EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md').read_text()
        cls.inventory=json.loads((PROVIDER/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        cls.ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())

    def callback(self):
        rows=[m for m in self.seal['native_methods'][IMPL] if m['name']=='onDestroyed']
        self.assertEqual(len(rows),1)
        return rows[0]

    def test_abstract_interface_and_concrete_body_remain_distinct(self):
        abstract=self.seal['native_methods'][TARGET]
        self.assertEqual(len(abstract),1)
        self.assertEqual(abstract[0]['access'],1025)
        self.assertEqual(abstract[0]['coverage'],'ABSTRACT_DECLARATION')
        self.assertEqual(abstract[0]['instructions'],[])
        callback=self.callback()
        self.assertEqual(callback['code_size'],170)
        self.assertEqual(callback['code_sha256'],'34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881')
        self.assertEqual(callback['exception_handlers'],[])
        self.assertEqual(self.seal['class_sha256'][TARGET],'2ccc084cf825941414561ed02362fc3776b5ddddd699c8c62952818956771100')

    def test_publisher_census_does_not_invent_interface_dispatch(self):
        census=self.seal['typed_reference_census']
        self.assertEqual(census['class_entries_scanned'],1555)
        self.assertEqual(census['direct_implementers'],[IMPL])
        self.assertEqual(census['concrete_implementers_within_publisher'],[IMPL])
        self.assertEqual(census['inherited_implementers_within_publisher'],[])
        self.assertEqual(len(census['typed_reference_owners']),2)
        self.assertEqual(len(census['on_destroyed_declarations']),3)
        self.assertEqual(len(census['on_destroyed_member_references']),1)
        upstream=self.seal['callback_semantics']['upstream_call']
        self.assertEqual(upstream['symbolic_owner'],PREFIX+'server/item/RadioactiveBlockItem')
        self.assertFalse(upstream['parent_declares_two_argument_method'])
        self.assertIn('normal return',upstream['causal_bound'])

    def test_super_guards_discard_spawn_and_explosion_have_separate_order(self):
        rows={r['offset']:r for r in self.callback()['instructions']}
        self.assertEqual(rows[3]['opcode'],'invokespecial')
        self.assertIn('isCreativePlayer',rows[7]['symbol'])
        self.assertIn('isRemoved',rows[14]['symbol'])
        self.assertIn('discard:',rows[21]['symbol'])
        self.assertIn('addFreshEntity:',rows[135]['symbol'])
        self.assertEqual(rows[138]['opcode'],'pop')
        self.assertIn('explode:',rows[165]['symbol'])
        semantics=self.seal['callback_semantics']
        self.assertEqual([g['return_offset'] for g in semantics['guards']],[169,169])
        self.assertFalse(semantics['local_client_side_guard'])
        self.assertFalse(semantics['local_rng'])

    def test_waste_drum_is_the_only_positive_selector_five_consumer(self):
        bridge=self.seal['registration_bridge']
        self.assertEqual(bridge['owner'],PREFIX+'server/block/ACBlockRegistry')
        self.assertEqual(bridge['destroyed_selector'],5)
        self.assertEqual(bridge['destroyed_factory'],'lambda$getBlockSupplier$441')
        self.assertEqual(bridge['explicit_selector_counts']['5'],1)
        positives=bridge['positive_registrations']
        self.assertEqual([r['name'] for r in positives],['waste_drum'])
        self.assertEqual(positives[0]['registry_field'],'WASTE_DRUM')
        self.assertEqual(positives[0]['selector_offset'],2200)
        self.assertEqual(bridge['ordinary_radioactive_selector'],4)
        self.assertEqual(bridge['ordinary_radioactive_factory'],'lambda$getBlockSupplier$440')
        negatives=bridge['negative_registrations']
        self.assertEqual({r['name'] for r in negatives},{'radrock_uranium_ore','block_of_uranium','unrefined_waste'})
        self.assertTrue(all(r['selector']==4 for r in negatives))
        self.assertIn('WASTE_DRUM',self.card)
        self.assertIn('selector',json.dumps(bridge))

    def test_inventory_radiation_chance_is_not_callback_rng(self):
        bridge=self.seal['registration_bridge']
        self.assertEqual(bridge['destroyed_factory_chance_field_input'],0.01)
        self.assertEqual(bridge['ordinary_radioactive_chance_field_input'],0.001)
        self.assertFalse(self.seal['callback_semantics']['local_rng'])
        symbols=' '.join(r['symbol'] for r in self.callback()['instructions'])
        self.assertNotIn('nextFloat:',symbols)
        self.assertNotIn('randomChanceOfRadiation',symbols)
        self.assertIn('randomChanceOfRadiation',self.seal['integration_bounds']['constructor_chance'])

    def test_cloud_status_payload_and_lifetime_are_not_one_timer(self):
        cloud=self.seal['callback_semantics']['cloud']
        self.assertEqual((cloud['effect_input_duration_ticks'],cloud['effect_input_amplifier']),(9600,1))
        self.assertEqual((cloud['radius'],cloud['cloud_duration_ticks'],cloud['wait_time_ticks']),(2.0,12000,0))
        self.assertEqual((cloud['color'],cloud['particle_supplier'],cloud['effect_supplier']),(7853582,'GAMMAROACH','IRRADIATED'))
        self.assertIn('-cloud.getRadius()',cloud['radius_per_tick_expression'])
        self.assertFalse(cloud['add_fresh_entity_boolean_checked'])
        self.assertFalse(cloud['owner_assignment_in_callback'])

    def test_explosion_source_strength_and_interaction_are_requests(self):
        explosion=self.seal['callback_semantics']['explosion']
        self.assertIsNone(explosion['source_entity'])
        self.assertEqual(explosion['strength'],1.8)
        self.assertEqual(explosion['interaction'],'BLOCK')
        self.assertIn('y+0.5',explosion['position'])
        self.assertFalse(explosion['returned_explosion_used'])
        for text in [self.card,self.proof]:
            for token in ['WorldEffectPolicy','Mastery','NO_MUTATION']:
                self.assertIn(token,text)

    def test_external_reference_is_250_while_runtime_remains_unverified(self):
        reference=PROVIDER/'EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json'
        self.assertTrue(reference.is_file())
        for text in [self.card,self.proof]:
            for token in ['21.1.250','21.1.248','patch','NOT_VERIFIED','NOT_TESTED']:
                self.assertIn(token,text)
        self.assertIn('actual installed transformed',self.seal['callback_semantics']['upstream_call']['causal_bound'])

    def test_historical_partial_card_and_probe_scope_are_preserved(self):
        archive=PROVIDER/'systems/EXACT-DESTROYED-ITEM-HISTORICAL-CARD-1.0.10.md'
        raw=archive.read_bytes()
        self.assertEqual(len(raw),9143)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'80e185f57698f54181bf49bf11998fb67499f158d8c9ec50d3aee01fbb2bec9d')
        self.assertIn(archive.name,self.card)
        probe=(ROOT/'docs/qa/alexscaves_1010_destroyed_item_probe.py').read_text()
        self.assertIn('READ_ONLY_SHA_EXACT_DISCOVERY_NOT_CERTIFICATION',probe)
        self.assertIn('NOT_CERTIFIED',probe)
        import sys
        sys.path.insert(0,str(ROOT/'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        self.assertFalse(canonical.is_card(archive))

    def test_certificate_has_seven_static_axes_and_no_provider_promotion(self):
        self.assertEqual(set(self.seal['axes']),AXES)
        entry=self.ledger['objects'][PROVIDER.name+'/systems/destroyed-item.md']
        self.assertEqual(set(entry['evidence']),AXES)
        self.assertEqual(entry['artifact_sha1'],self.seal['artifact']['sha1'])
        for evidence in entry['evidence'].values():
            self.assertEqual(Path(evidence['path']).name,'EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md')
            self.assertTrue((ROOT/evidence['path']).is_file())
        claims=self.seal['claims']
        self.assertEqual(claims['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(claims['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(claims['physical_qa'],'NOT_TESTED')
        self.assertEqual(claims['mutation'],'NO_MUTATION')
        self.assertFalse(claims['provider_universe_closed'])
        self.assertEqual(claims['semantic_magic_roots_delta'],0)
        self.assertNotIn(PROVIDER.name,self.ledger['providers'])

    def test_prefix_promotes_existing_candidate_without_counting_archive(self):
        support=self.inventory['integration_support_inventory']
        prefix=support['reviewed_prefix']
        roster=self.inventory['remaining_family_inventory']['item_outer_classes']
        self.assertEqual([r['class'] for r in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[3]['card'],'systems/destroyed-item.md')
        self.assertEqual(prefix[3]['additional_cards'],0)
        self.assertEqual(support['next_alphabetical_uncovered_scope'],roster[len(prefix)])
        self.assertFalse(support['family_universe_closed'])
        self.assertFalse(self.inventory['whole_provider_catalog_closed'])

    def test_current_indexes_derive_from_actual_cards_and_separate_provider_scope(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        for folder in [PROVIDER,PROVIDER/'systems']:
            cards=[p for p in folder.rglob('*.md') if canonical.is_card(p)]
            certified=sum(canonical.certified(p,self.ledger) for p in cards)
            index=(folder/'INDEX.md').read_text()
            self.assertIn(f'{certified}/{len(cards)}',index)
            if folder==PROVIDER:
                self.assertIn('**Catálogo desta árvore:** ⚠️',index)
            elif certified==len(cards):
                self.assertIn('**Catálogo desta árvore:** ✅',index)
                self.assertIn('100.0%',index)
        index=(PROVIDER/'systems/INDEX.md').read_text()
        row=next(line for line in index.splitlines() if '[ficha/destroyed-item.md](destroyed-item.md)' in line)
        self.assertTrue(row.startswith('| ✅ |'))
        self.assertIn('| ✅ certificado |',row)


if __name__=='__main__':unittest.main()
