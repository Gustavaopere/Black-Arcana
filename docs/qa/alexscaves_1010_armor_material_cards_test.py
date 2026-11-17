#!/usr/bin/env python3
"""Material adapter semantics, support exceptions and scoped catalog regressions."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'
ITEM=PREFIX+'server/item/'
MATERIAL=ITEM+'ACArmorMaterial'
AXES={'identity','behavior','parameters','targeting','costs','integration','validation'}


class ArmorMaterialCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/'EXACT-ARMOR-MATERIAL-1.0.10.json').read_text())
        cls.card=(PROVIDER/'systems/armor-material.md').read_text()
        cls.proof=(PROVIDER/'EXACT-ARMOR-MATERIAL-1.0.10.md').read_text()
        cls.inventory=json.loads((PROVIDER/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        cls.ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())

    def method(self,name,descriptor=None):
        rows=[r for r in self.seal['native_methods'][MATERIAL] if r['name']==name and (descriptor is None or r['descriptor']==descriptor)]
        self.assertEqual(len(rows),1)
        return rows[0]

    def test_exact_material_identity_and_ten_distinct_bodies(self):
        self.assertEqual(self.seal['artifact']['version'],'1.0.10')
        self.assertEqual(self.seal['artifact']['sha1'],'6960b299a39a039ac8a5eb9b07be4ad0e3e0a570')
        self.assertEqual(self.seal['class_sha256'][MATERIAL],'478accf7ab37014dc06a8f3d801348948638dc517db0e21b7fd91d2b47ca40a6')
        rows=self.seal['native_methods'][MATERIAL]
        self.assertEqual(len(rows),10)
        self.assertEqual(len({(r['name'],r['descriptor']) for r in rows}),10)
        self.assertEqual(sum(r['name']=='<init>' for r in rows),2)
        self.assertEqual(sum(r['name']=='<clinit>' for r in rows),1)
        for row in rows:
            self.assertEqual(row['coverage'],'FULL_BODY')
            self.assertEqual(row['instruction_count'],len(row['instructions']))
            self.assertTrue(row['pivots'])
            self.assertIn(row['descriptor'],self.card)

    def test_six_literal_configs_and_indexed_capacity_match_the_dossier(self):
        expected={
            'primordial':(20,[3,4,3,2],25,0.0,'TOUGH_HIDE'),
            'hazmat_suit':(20,[2,4,5,2],25,0.5,'POLYMER_PLATE'),
            'diving_suit':(20,[2,6,5,2],25,0.0,'minecraft:copper_ingot'),
            'darkness':(15,[4,5,1,1],40,0.5,'DARK_TATTERS'),
            'rainbounce':(6,[2,2,1,2],40,0.0,'Ingredient.EMPTY'),
            'gingerbread':(10,[2,4,5,2],25,0.0,'GINGERBREAD_CRUMBS')}
        definitions=self.seal['material_definitions']
        self.assertEqual(len(definitions),6)
        self.assertEqual({r['name'] for r in definitions},set(expected))
        for row in definitions:
            multiplier,defense,enchant,toughness,repair=expected[row['name']]
            self.assertEqual((row['durability_multiplier'],row['damage_reduction_by_ordinal'],row['enchantability'],row['toughness'],row['setup_repair_item']),(multiplier,defense,enchant,toughness,repair))
            self.assertEqual(row['knockback_resistance'],0.0)
            self.assertIn(row['registry_field'],self.card)
            for array in [defense,[v*multiplier for v in [13,15,16,11]]]:
                self.assertIn('['+','.join(map(str,array))+']',self.card)

    def test_durability_and_defense_are_direct_array_indexes_not_slot_name_guesses(self):
        self.assertEqual(self.seal['integration_bounds']['max_damage_array_by_ordinal'],[13,15,16,11])
        properties=self.method('properties')['instructions']
        for op in ['iaload','imul']:
            self.assertIn(op,[r['opcode'] for r in properties])
        self.assertFalse(self.method('properties')['branches'])
        self.assertFalse(self.method('defense')['branches'])
        vanilla=self.method('vanilla')
        self.assertTrue(vanilla['branches'])
        self.assertIn('damageReduction.length',self.seal['integration_bounds']['ordinal_limit'])
        self.assertIn('sem atribuir esses ordinais aos nomes dos slots',self.card)

    def test_raw_alias_and_live_repair_supplier_are_not_global_safe_perk_mutators(self):
        long_ctor=[r for r in self.seal['native_methods'][MATERIAL] if r['name']=='<init>' and r['descriptor'].endswith('FF)V')][0]
        rows={r['offset']:r for r in long_ctor['instructions']}
        self.assertEqual(rows[25]['opcode'],'aload_3')
        self.assertEqual(rows[26]['opcode'],'putfield')
        self.assertIn('damageReduction:[I',rows[26]['symbol'])
        self.assertIn('this',self.seal['integration_bounds']['snapshot_and_live_state'])
        bootstrap=json.dumps(self.seal['material_supplier_bootstrap'])
        self.assertIn('getRepairIngredient',bootstrap)
        self.assertIn('knockbackResistance',self.card)
        for text in [self.card,self.proof]:
            self.assertIn('supplier',text)
            self.assertIn('compartilh',text)

    def test_null_repair_fallback_and_rainbounce_absence_have_bounded_meaning(self):
        getter=self.method('getRepairIngredient')
        self.assertTrue(any(r['opcode']=='ifnonnull' for r in getter['instructions']))
        self.assertTrue(any('Ingredient.EMPTY' in r['symbol'] for r in getter['instructions']))
        setter=self.method('setRepairMaterial')
        self.assertFalse(setter['branches'])
        self.assertEqual(sum(r['opcode']=='putfield' for r in setter['instructions']),1)
        repair=[r['setup_repair_item'] for r in self.seal['material_definitions']]
        self.assertEqual(sum(x!='Ingredient.EMPTY' for x in repair),5)
        for text in [self.card,self.proof]:
            self.assertIn('Rainbounce',text)
            self.assertIn('Ingredient.EMPTY',text)
            self.assertIn('reparo',text)

    def test_native_reference_rosters_do_not_turn_other_pieces_into_certificates(self):
        census=self.seal['typed_reference_census']
        self.assertEqual(census['class_entries_scanned'],1555)
        refs=census['targets'][MATERIAL]
        owners={r['owner'] for r in refs}
        self.assertEqual(owners,{MATERIAL,ITEM+'ACItemRegistry',*(ITEM+n for n in ['DarknessArmorItem','DivingArmorItem','GingerbreadArmorItem','HazmatArmorItem','PrimordialArmorItem','RainbounceBootsItem'])})
        self.assertIn('plain UTF8/String constants do not count',census['method'])
        self.assertIn('não recebem fichas individuais nem certificação integral',self.card)

    def test_empty_marker_is_support_only_and_real_dispatch_uses_other_interface(self):
        marker=self.seal['marker']
        self.assertEqual(marker['fields'],[])
        self.assertEqual(marker['declared_methods'],[])
        self.assertEqual(marker['direct_implementers'],[ITEM+'DarknessArmorItem'])
        self.assertEqual(marker['typed_dispatch_references'],[])
        self.assertEqual(marker['disposition'],'EMPTY_MARKER_SUPPORT_ONLY')
        dispatch=marker['actual_tick_dispatch']
        self.assertEqual(dispatch['receiver_interface'],ITEM+'ACTickingItem')
        self.assertEqual(dispatch['name'],'ac_inventoryTick')
        self.assertEqual((dispatch['type_check_offset'],dispatch['invokeinterface_offset']),(15,36))
        self.assertFalse((PROVIDER/'systems/armor-tick-marker.md').exists())

    def test_target_damage_projectile_and_cast_cost_are_na_in_material_bodies(self):
        calls=[r['symbol'] for m in self.seal['native_methods'][MATERIAL] for r in m['instructions'] if r['opcode'].startswith('invoke')]
        for forbidden in ['getEntities:','hurt:','addEffect:','shoot:','setOwner:','startUsingItem:']:
            self.assertFalse(any(forbidden in c for c in calls),forbidden)
        for text in [self.card,self.proof]:
            for token in ['mana','cooldown','NO_MUTATION','NOT_CERTIFIED']:
                self.assertIn(token,text)

    def test_certificate_requires_all_seven_axes_without_provider_or_gameplay_promotion(self):
        self.assertEqual(set(self.seal['axes']),AXES)
        entry=self.ledger['objects'][PROVIDER.name+'/systems/armor-material.md']
        self.assertEqual(set(entry['evidence']),AXES)
        self.assertEqual(entry['artifact_sha1'],self.seal['artifact']['sha1'])
        for evidence in entry['evidence'].values():
            self.assertEqual(Path(evidence['path']).name,'EXACT-ARMOR-MATERIAL-1.0.10.md')
            self.assertTrue((ROOT/evidence['path']).is_file())
        claims=self.seal['claims']
        self.assertEqual(claims['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(claims['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(claims['physical_qa'],'NOT_TESTED')
        self.assertEqual(claims['mutation'],'NO_MUTATION')
        self.assertEqual(claims['semantic_magic_roots_delta'],0)
        self.assertFalse(claims['provider_universe_closed'])
        self.assertNotIn(PROVIDER.name,self.ledger['providers'])

    def test_reviewed_prefix_preserves_original_roster_and_advances_one_bounded_scope(self):
        support=self.inventory['integration_support_inventory']
        prefix=support['reviewed_prefix']
        roster=self.inventory['remaining_family_inventory']['item_outer_classes']
        self.assertEqual([r['class'] for r in prefix[:2]],['server/item/ACArmorMaterial','server/item/ACArmorTickItem'])
        self.assertEqual([r['class'] for r in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[0]['card'],'systems/armor-material.md')
        self.assertEqual(prefix[0]['additional_cards'],1)
        self.assertIsNone(prefix[1]['card'])
        self.assertEqual(prefix[1]['additional_cards'],0)
        self.assertEqual(prefix[1]['disposition'],'EMPTY_MARKER_SUPPORT_ONLY')
        self.assertEqual(support['next_alphabetical_uncovered_scope'],roster[len(prefix)])
        self.assertFalse(support['family_universe_closed'])
        self.assertFalse(self.inventory['whole_provider_catalog_closed'])

    def test_current_indexes_close_detected_support_cards_without_whole_family_claim(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        certified=sum(k.startswith(PROVIDER.name+'/') for k in self.ledger['objects'])
        observed=sum(canonical.is_card(p) for p in PROVIDER.rglob('*.md'))
        index=(PROVIDER/'INDEX.md').read_text()
        self.assertIn(f'{certified}/{observed}',index)
        self.assertIn('**Catálogo desta árvore:** ⚠️',index)
        support=(PROVIDER/'systems/INDEX.md').read_text()
        support_certified=sum(k.startswith(PROVIDER.name+'/systems/') for k in self.ledger['objects'])
        support_observed=sum(canonical.is_card(p) for p in (PROVIDER/'systems').rglob('*.md'))
        self.assertIn(f'{support_certified}/{support_observed}',support)
        self.assertIn('| ✅ |',support)
        if support_certified==support_observed:
            self.assertIn('**Catálogo desta árvore:** ✅',support)
            self.assertIn('100.0%',support)
        self.assertFalse(self.inventory['family_catalog_status']['integration_support']['family_universe_closed'])


if __name__=='__main__':unittest.main()
