#!/usr/bin/env python3
"""Client-extension ABI, presentation lifetimes and scoped catalog regressions."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'
TARGET=PREFIX+'server/item/ACClientExtensionItem'
EXTENSION='net/neoforged/neoforge/client/extensions/common/IClientItemExtensions'
AXES={'identity','behavior','parameters','targeting','costs','integration','validation'}


class ClientExtensionCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/'EXACT-CLIENT-EXTENSION-1.0.10.json').read_text())
        cls.card=(PROVIDER/'systems/client-extension.md').read_text()
        cls.proof=(PROVIDER/'EXACT-CLIENT-EXTENSION-1.0.10.md').read_text()
        cls.inventory=json.loads((PROVIDER/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        cls.ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())

    def method(self,owner,name):
        methods=[m for m in self.seal['native_methods'][owner] if m['name']==name]
        self.assertEqual(len(methods),1)
        return methods[0]

    def test_abstract_erased_abi_and_generic_type_have_no_executable_body(self):
        interface=self.seal['interface_contract']
        self.assertEqual(interface['owner'],TARGET)
        self.assertEqual(interface['fields'],[])
        self.assertEqual(interface['interfaces'],[])
        self.assertFalse(interface['executable_code'])
        self.assertEqual(interface['declared_methods'],[{'access':1025,'name':'initializeClient','descriptor':'(Ljava/util/function/Consumer;)V'}])
        self.assertEqual(interface['generic_signature'],'(Ljava/util/function/Consumer<L'+EXTENSION+';>;)V')
        self.assertEqual(self.seal['class_sha256'][TARGET],'d3139782c378b7b8eee0b580c912f36095675e31db98310475fbe1b60f5a0362')
        self.assertEqual(self.seal['artifact']['version'],'1.0.10')

    def test_declarations_and_typed_callers_are_different_frozen_sets(self):
        census=self.seal['typed_reference_census']
        self.assertEqual(census['class_entries_scanned'],1555)
        self.assertEqual(len(census['target_owners']),20)
        self.assertEqual(sum(r['implements_directly'] for r in census['target_owners']),19)
        self.assertEqual(len(census['initialize_client_declarations']),23)
        self.assertEqual(census['initialize_client_member_references'],[])
        self.assertEqual({r['owner'] for r in self.seal['callbacks']},{r['owner'] for r in census['target_owners'] if r['implements_directly']})
        for text in [self.card,self.proof]:
            self.assertIn('23',text)
            self.assertIn('reflex',text.lower())
            self.assertIn('ItemProperties.register',text)

    def test_nineteen_callbacks_delegate_to_twelve_six_and_one_owner_routes(self):
        callbacks=self.seal['callbacks']
        self.assertEqual(len(callbacks),19)
        armor=[r for r in callbacks if r['extension_family']=='ARMOR_MODEL']
        native_item=[r for r in callbacks if r['extension_family']=='ITEM_RENDERER' and '/citadel/' not in r['owner']]
        citadel=[r for r in callbacks if '/citadel/' in r['owner']]
        self.assertEqual((len(native_item),len(armor),len(citadel)),(12,6,1))
        self.assertTrue(all(r['proxy_getter']=='getArmorProperties' for r in armor))
        self.assertTrue(all(r['proxy_getter']=='getISTERProperties' for r in native_item+citadel))
        self.assertEqual(citadel[0]['proxy_field_owner'],PREFIX+'citadel/Citadel')
        for callback in callbacks:
            self.assertIn(callback['owner'].rsplit('/',1)[1],self.card)
            method=callback['method']
            self.assertEqual((method['instruction_count'],method['code_size']),(6,16))
            self.assertEqual(method['exception_handlers'],[])
            rows={r['offset']:r for r in method['instructions']}
            self.assertEqual(set(rows),{0,1,4,7,10,15})
            self.assertEqual(rows[7]['opcode'],'checkcast')
            self.assertIn(EXTENSION,rows[7]['symbol'])
            self.assertIn('Consumer.accept:',rows[10]['symbol'])
            self.assertEqual(rows[15]['opcode'],'return')

    def test_three_inherited_spears_resolve_one_existing_callback_body(self):
        census=self.seal['typed_reference_census']['assignability_census']
        self.assertEqual(len(census['direct_implementers']),19)
        self.assertEqual(len(census['concrete_assignable']),22)
        inherited=census['inherited_implementers']
        self.assertEqual({Path(r['owner']).name for r in inherited},{'ExtinctionSpearItem','FrostmintSpearItem','LimestoneSpearItem'})
        for row in inherited:
            self.assertEqual(row['parent'],PREFIX+'server/item/SpearItem')
            self.assertEqual(row['callback_declaring_owner'],PREFIX+'server/item/SpearItem')
            self.assertEqual(row['declared_callbacks'],[])
            self.assertNotIn(row['owner'],{r['owner'] for r in self.seal['callbacks']})
            self.assertIn(row['owner'],self.seal['class_sha256'])
        self.assertEqual(self.seal['typed_reference_census']['registration_event_typed_owners'],[])

    def test_callbacks_do_not_allocate_properties_or_apply_combat(self):
        for callback in self.seal['callbacks']:
            rows=callback['method']['instructions']
            self.assertFalse(any(r['opcode'] in ['new','anewarray','newarray'] for r in rows))
            symbols=' '.join(r['symbol'] for r in rows)
            for absent in ['getEntities:','hurt:','addEffect:','shoot:','setOwner:','startUsingItem:']:
                self.assertNotIn(absent,symbols)
        for text in [self.card,self.proof]:
            for token in ['mana','cooldown','NO_MUTATION','NOT_CERTIFIED']:
                self.assertIn(token.casefold(),text.casefold())

    def test_native_properties_are_shared_but_item_renderer_is_fresh(self):
        client=PREFIX+'client/ClientProxy'
        for name,field in [('getISTERProperties','isterProperties'),('getArmorProperties','armorProperties')]:
            rows=self.method(client,name)['instructions']
            self.assertTrue(any(r['opcode']=='getfield' and field in r['symbol'] for r in rows))
            self.assertFalse(any(r['opcode']=='new' for r in rows))
        native=self.method(PREFIX+'client/render/item/ACItemRenderProperties','getCustomRenderer')['instructions']
        self.assertTrue(any(r['opcode']=='new' and 'ACItemstackRenderer' in r['symbol'] for r in native))
        self.assertFalse(any(r['opcode']=='getfield' for r in native))

    def test_relocated_citadel_has_fresh_properties_with_per_property_renderer(self):
        getter=self.method(PREFIX+'citadel/CitadelClientProxy','getISTERProperties')['instructions']
        self.assertTrue(any(r['opcode']=='new' and 'CitadelItemRenderProperties' in r['symbol'] for r in getter))
        props=PREFIX+'citadel/client/CitadelItemRenderProperties'
        constructor=self.method(props,'<init>')['instructions']
        self.assertTrue(any(r['opcode']=='new' and 'CitadelItemstackRenderer' in r['symbol'] for r in constructor))
        custom=self.method(props,'getCustomRenderer')['instructions']
        self.assertTrue(any(r['opcode']=='getfield' and 'renderer:' in r['symbol'] for r in custom))
        self.assertFalse(any(r['opcode']=='new' for r in custom))
        self.assertIn('Citadel',self.card)

    def test_base_proxy_nulls_do_not_certify_client_proxy_selection(self):
        for owner,name in [(PREFIX+'server/CommonProxy','getISTERProperties'),(PREFIX+'server/CommonProxy','getArmorProperties'),(PREFIX+'citadel/CitadelProxy','getISTERProperties')]:
            self.assertEqual([r['opcode'] for r in self.method(owner,name)['instructions']],['aconst_null','areturn'])
        boundary=self.seal['registration_boundary']
        self.assertEqual(boundary['publisher_typed_initialize_client_callers'],0)
        for key in ['registration_execution','external_engine_callback_dispatch','proxy_selection_and_client_initialization']:
            self.assertEqual(boundary[key],'NOT_VERIFIED')

    def test_armor_selection_is_six_model_routes_with_default_and_unused_slot(self):
        outputs=self.seal['extension_outputs']
        self.assertFalse(outputs['slot_argument_used'])
        roster=outputs['armor_model_roster']
        self.assertEqual([Path(r['item_owner']).name for r in roster],['PrimordialArmorItem','HazmatArmorItem','DivingArmorItem','DarknessArmorItem','RainbounceBootsItem','GingerbreadArmorItem'])
        owner=PREFIX+'client/render/item/ACArmorRenderProperties'
        rows=self.method(owner,'getHumanoidArmorModel')['instructions']
        self.assertFalse(any(r['opcode']=='aload_3' for r in rows))
        self.assertTrue(any('getACArmorModel:' in r['symbol'] for r in rows))
        initializer=self.method(owner,'initializeModels')['instructions']
        self.assertEqual(initializer[0]['opcode'],'iconst_1')
        self.assertEqual(initializer[1]['opcode'],'putstatic')
        self.assertEqual(sum('bakeLayer:' in r['symbol'] for r in initializer),6)

    def test_seven_static_axes_preserve_registration_hook_qa_and_provider_limits(self):
        self.assertEqual(set(self.seal['axes']),AXES)
        entry=self.ledger['objects'][PROVIDER.name+'/systems/client-extension.md']
        self.assertEqual(set(entry['evidence']),AXES)
        for row in entry['evidence'].values():
            self.assertEqual(Path(row['path']).name,'EXACT-CLIENT-EXTENSION-1.0.10.md')
            self.assertTrue((ROOT/row['path']).is_file())
        claims=self.seal['claims']
        self.assertEqual(claims['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(claims['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(claims['physical_qa'],'NOT_TESTED')
        self.assertEqual(claims['mutation'],'NO_MUTATION')
        self.assertEqual(claims['semantic_magic_roots_delta'],0)
        self.assertFalse(claims['provider_universe_closed'])
        self.assertNotIn(PROVIDER.name,self.ledger['providers'])

    def test_prefix_keeps_previous_dispositions_and_adds_only_client_support_card(self):
        support=self.inventory['integration_support_inventory']
        prefix=support['reviewed_prefix']
        roster=self.inventory['remaining_family_inventory']['item_outer_classes']
        self.assertEqual([r['class'] for r in prefix],roster[:len(prefix)])
        self.assertEqual(prefix[0]['card'],'systems/armor-material.md')
        self.assertEqual(prefix[1]['disposition'],'EMPTY_MARKER_SUPPORT_ONLY')
        self.assertIsNone(prefix[1]['card'])
        self.assertEqual(prefix[2]['card'],'systems/client-extension.md')
        self.assertEqual(prefix[2]['additional_cards'],1)
        self.assertEqual(support['next_alphabetical_uncovered_scope'],roster[len(prefix)])
        self.assertFalse(support['family_universe_closed'])

    def test_current_indexes_count_actual_system_cards_without_closing_provider(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        cards=[p for p in PROVIDER.rglob('*.md') if canonical.is_card(p)]
        certified=sum(canonical.certified(p,self.ledger) for p in cards)
        index=(PROVIDER/'INDEX.md').read_text()
        self.assertIn(f'{certified}/{len(cards)}',index)
        self.assertIn('**Catálogo desta árvore:** ⚠️',index)
        system_cards=[p for p in (PROVIDER/'systems').rglob('*.md') if canonical.is_card(p)]
        system_certified=sum(canonical.certified(p,self.ledger) for p in system_cards)
        index=(PROVIDER/'systems/INDEX.md').read_text()
        self.assertIn(f'{system_certified}/{len(system_cards)}',index)
        if system_certified==len(system_cards):
            self.assertIn('**Catálogo desta árvore:** ✅',index)
            self.assertIn('100.0%',index)


if __name__=='__main__':unittest.main()
