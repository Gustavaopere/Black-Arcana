#!/usr/bin/env python3
"""X-Ray native dataflow and scoped 51-resource catalog closure regressions."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
ITEM='com/github/alexmodguy/alexscaves/server/item/RaygunItem.class'
REGISTRY='com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class'

class XrayStaticCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((PROVIDER/'EXACT-XRAY-CAUSAL-1.0.10.json').read_text())
        cls.card=(PROVIDER/'enchantments/x-ray.md').read_text()
        cls.proof=(PROVIDER/'EXACT-XRAY-CAUSAL-1.0.10.md').read_text()

    def pivots(self,owner=ITEM,name='onUseTick'):
        rows=[r for r in self.seal['pivots'] if r['owner']==owner and r['name']==name]
        self.assertTrue(rows)
        self.assertEqual(len(rows),len({r['offset'] for r in rows}))
        return {r['offset']:r for r in rows}

    def row(self,rows,offset,opcode=None,token=None):
        self.assertIn(offset,rows)
        if opcode is not None:self.assertEqual(rows[offset]['opcode'],opcode,offset)
        if token is not None:self.assertIn(token,rows[offset]['operand']+' '+rows[offset]['symbol'],offset)

    def test_publisher_and_historical_proofs_remain_exact(self):
        self.assertEqual(self.seal['version'],'1.0.10')
        self.assertEqual(self.seal['enchantment'],'alexscaves:x_ray')
        self.assertEqual(self.seal['artifact'],{'sha1':'6960b299a39a039ac8a5eb9b07be4ad0e3e0a570','sha256':'36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c','size_bytes':75279314})
        for filename,digest in [('EXACT-GAMMA-RAY-CAUSAL-1.0.10.json','cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c'),('EXACT-RAYGUN-XRAY-TARGET-1.0.10.json','4f7bc4a4d9adcc9552ae0e5123b6872e0c1c3ccbec71afe3f44fc0671cb632e2')]:
            self.assertEqual(hashlib.sha256((PROVIDER/filename).read_bytes()).hexdigest(),digest)

    def test_json_exclusion_and_registry_binding(self):
        data=self.seal['resource_json']
        self.assertEqual(data['description']['translate'],'enchantment.alexscaves.x_ray')
        self.assertEqual((data['max_level'],data['weight'],data['anvil_cost']),(1,10,1))
        self.assertEqual(data['min_cost'],{'base':1,'per_level_above_first':12})
        self.assertEqual(data['max_cost'],{'base':41,'per_level_above_first':10})
        self.assertEqual(data['slots'],['mainhand'])
        self.assertEqual(data['exclusive_set'],['alexscaves:gamma_ray'])
        self.assertNotIn('exclusive_set',self.seal['gamma_ray_resource_json'])
        self.assertEqual(self.seal['supported_item_tag'],{'values':['alexscaves:raygun']})
        registry=self.pivots(REGISTRY,'<clinit>')
        self.row(registry,194,token='x_ray');self.row(registry,197,'invokestatic','key:');self.row(registry,200,'putstatic','X_RAY:')

    def test_full_method_and_scoped_boolean_uses(self):
        tick=[r for r in self.seal['census']['method_census'] if r['owner']==ITEM and r['name']=='onUseTick']
        self.assertEqual(len(tick),1)
        self.assertEqual((tick[0]['instructions'],tick[0]['direct_branches']),(523,57))
        self.assertEqual(tick[0]['body_sha256'],'b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5')
        slot=self.seal['xray_boolean_slot']
        self.assertEqual((slot['slot'],slot['writes'],slot['reads']),(9,[58],[105,122,569]))
        p=self.pivots()
        for offset,op,token in [(44,'getstatic','X_RAY:'),(47,'invokestatic','enchantLevel:'),(50,'ifle','57'),(53,'iconst_1',''),(57,'iconst_0',''),(58,'istore','9')]:self.row(p,offset,op,token)

    def test_range_and_initial_endpoints_are_distinct_dataflow(self):
        p=self.pivots()
        for offset,op,token in [(35,'ldc_w','float 25.0f'),(40,'fmul',''),(41,'fstore','8'),(69,'invokestatic','getHitResultOnViewVector:'),(72,'astore','10'),(80,'invokevirtual','LivingEntity.pick:'),(83,'astore','11'),(87,'invokevirtual','getViewVector:'),(93,'invokevirtual','Vec3.scale:'),(97,'invokevirtual','getEyePosition:'),(103,'astore','12'),(107,'ifeq','115'),(110,'aload','12'),(115,'aload','11'),(120,'astore','13'),(124,'ifeq','132'),(127,'aload','12'),(132,'aload','11'),(137,'astore','14')]:self.row(p,offset,op,token)
        self.assertEqual(self.seal['range_slot']['writes'],[41])
        self.assertEqual(self.seal['endpoint_slots']['entity_result_replaces_damage_endpoint_at'],766)

    def test_scan_box_segment_update_and_first_nonnull_break(self):
        p=self.pivots()
        for offset,op,token in [(571,'ifeq','669'),(575,'invokevirtual','getBoundingBox:'),(578,'fload','8'),(581,'invokevirtual','AABB.inflate:'),(584,'astore','22'),(586,'fconst_1',''),(587,'fstore','23'),(590,'invokevirtual','getEyePosition:'),(593,'astore','24'),(600,'ifge','666'),(607,'invokevirtual','getViewVector:'),(613,'astore','24'),(619,'invokevirtual','getViewVector:'),(625,'astore','25'),(640,'invokestatic','ProjectileUtil.getEntityHitResult:'),(643,'astore','26'),(647,'ifnull','657'),(652,'astore','10'),(654,'goto','666'),(659,'fconst_1',''),(660,'fadd',''),(661,'fstore','23'),(663,'goto','595'),(666,'goto','734')]:self.row(p,offset,op,token)
        loop=self.seal['loop_slot23']
        self.assertEqual((loop['initial'],loop['step'],loop['writes']),(1.0,1.0,[587,661]))
        self.assertIn('first nonnull',self.seal['static_contract']['scan_break'])
        self.assertIn('remains unchanged',self.seal['static_contract']['scan_no_hit'])

    def test_typed_slot_reuse_does_not_mix_counter_blockpos_and_amplifier(self):
        rows=self.seal['local_slot_accesses']['23']
        self.assertIn((587,'fstore'),[(r['offset'],r['opcode']) for r in rows])
        self.assertIn((661,'fstore'),[(r['offset'],r['opcode']) for r in rows])
        self.assertIn((689,'astore'),[(r['offset'],r['opcode']) for r in rows])
        self.assertIn((932,'istore'),[(r['offset'],r['opcode']) for r in rows])
        self.assertEqual(self.seal['loop_slot23']['type_in_loop'],'float')

    def test_block_branch_is_bypassed_and_entity_position_controls_damage_center(self):
        p=self.pivots()
        for offset,op,token in [(669,'aload','10'),(671,'instanceof','BlockHitResult'),(706,'aload','24'),(708,'invokevirtual','BlockState.isAir:'),(721,'invokevirtual','isFaceSturdy:'),(732,'astore','21'),(736,'instanceof','EntityHitResult'),(751,'invokevirtual','getEntity:'),(754,'invokevirtual','Entity.position:'),(757,'astore','21'),(759,'getstatic','Direction.UP'),(766,'astore','14')]:self.row(p,offset,op,token)

    def test_impact_visual_gate_does_not_become_damage_gate(self):
        p=self.pivots()
        self.row(p,770,'ifnull','874')
        for offset,op,token in [(875,'invokevirtual','isClientSide:'),(878,'ifne','1160'),(887,'irem',''),(888,'ifne','1160'),(891,'new','AABB'),(895,'aload','14'),(917,'invokespecial','AABB'),(943,'invokevirtual','Level.getEntities:')]:self.row(p,offset,op,token)
        self.assertIn('local21',self.seal['static_contract']['impact_and_damage_separation'])

    def test_inherited_cost_damage_status_and_authorship_are_not_recertified_as_xray_bonuses(self):
        inherited=self.seal['inherited_native_contract']
        self.assertEqual((inherited['native_method_count'],inherited['visual_method_count']),(12,2))
        self.assertEqual(inherited['network_authorization'],'NOT_VERIFIED')
        self.assertEqual(self.seal['composed_gamma_report_sha256'],'cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c')
        for text in [self.card,self.proof]:
            for word in ['Gamma','Irradiated','Mastery','NO_MUTATION','1.1.1']:self.assertIn(word,text)

    def test_publisher_census_and_all_51_certificates_close_only_scoped_catalog(self):
        inventory=json.loads((PROVIDER/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        prefix=PROVIDER.name+'/enchantments/'
        cards=sorted(k.removeprefix(PROVIDER.name+'/') for k in ledger['objects'] if k.startswith(prefix))
        ids={Path(k).stem.replace('-','_') for k in cards}
        census=self.seal['publisher_enchantment_census']
        self.assertEqual(census['count'],51);self.assertEqual(set(census['ids']),ids)
        self.assertEqual(len(census['resource_sha256']),51)
        for p,h in census['resource_sha256'].items():
            self.assertRegex(p,r'^data/alexscaves/enchantment/[a-z_]+\.json$');self.assertRegex(h,r'^[a-f0-9]{64}$')
        family=inventory['family_catalog_status']['enchantments']
        self.assertEqual(family['cards'],cards)
        self.assertEqual((family['identified_objects'],family['individual_dossiers'],family['documented_static_contracts'],family['partial_dossiers']),(51,51,51,0))
        self.assertTrue(family['publisher_json_static_catalog_complete'])
        self.assertFalse(family['family_universe_closed']);self.assertFalse(inventory['whole_provider_catalog_closed'])
        self.assertNotIn(PROVIDER.name,ledger['providers'])

    def test_crosswalk_has_100_percent_and_no_obsolete_enchantment_queue(self):
        text=(PROVIDER/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        for token in ['individual_full_enchantment_dossiers=51/51','individual_partial_enchantment_dossiers=0/51','individual_existing_enchantment_dossiers=51/51','100.0% (51/51)','| ✅ | `alexscaves:x_ray`']:self.assertIn(token,text)
        import sys
        sys.path.insert(0,str(ROOT/'scripts/catalog'))
        import check_perk_ready_indexes as canonical
        ledger=canonical.read_ledger()
        certified=sum(key.startswith(PROVIDER.name+'/') for key in ledger['objects'])
        observed=sum(canonical.is_card(path) for path in PROVIDER.rglob('*.md'))
        self.assertIn(f'{certified}/{observed} contratos estáticos entre fichas observadas',text)
        self.assertNotIn('começando por `alexscaves:',text)
        self.assertIn('damage-types/raygun.md',text);self.assertIn('damage-types/tremorzilla-beam.md',text)
        self.assertEqual(ledger['objects'][PROVIDER.name+'/damage-types/tremorzilla-beam.md']['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        index=(PROVIDER/'enchantments/INDEX.md').read_text()
        self.assertIn('**Catálogo desta árvore:** ✅',index)
        self.assertIn('51/51',index);self.assertIn('100.0%',index)

    def test_static_evidence_does_not_promote_hooks_qa_or_provider(self):
        self.assertEqual(self.seal['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(self.seal['evidence_grade'],'SHA_EXACT_BINARY_BEHAVIOR')
        for k,v in [('mutating_hook','NOT_VERIFIED'),('physical_qa','NOT_TESTED'),('mutation','NO_MUTATION'),('provider_universe_closed',False)]:self.assertEqual(self.seal['safety'][k],v)
        ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text());certificate=ledger['objects'][PROVIDER.name+'/enchantments/x-ray.md']
        self.assertEqual(set(certificate['evidence']),{'identity','behavior','parameters','targeting','costs','integration','validation'})
        for evidence in certificate['evidence'].values():self.assertTrue((ROOT/evidence['path']).is_file())
        for text in [self.card,self.proof]:
            for token in ['STATIC_TECHNICAL_CATALOG_ONLY','NOT_VERIFIED','NOT_TESTED','NO_MUTATION','EXACT-XRAY-CAUSAL-1.0.10.json']:self.assertIn(token,text)

if __name__=='__main__':unittest.main()
