#!/usr/bin/env python3
"""Regression guards for Peppermint Punting: exact-JAR static contract, no mutators."""
import hashlib,json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
CARD='enchantments/peppermint-punting.md'
SEAL='EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json'
PREFIX='com/github/alexmodguy/alexscaves/'
ITEM=PREFIX+'server/item/SugarStaffItem.class'
ENTITY=PREFIX+'server/entity/item/SpinningPeppermintEntity.class'

class PuntingContract(unittest.TestCase):
    def load(self):
        s=json.loads((P/SEAL).read_text(encoding='utf-8'))
        m=load_manifest(P/'EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json')
        validate_structure(m,profile='multiple_mint')
        validate_cards(m,P,profile='multiple_mint')
        self.assertEqual(s['catalog_family'],'PEPPERMINT_PUNTING_ENCHANTMENT_CONTRACT')
        self.assertEqual(s['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(s['evidence_grade'],'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertEqual(s['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(s['physical_qa'],'NOT_TESTED')
        self.assertEqual(s['mutation'],'NO_MUTATION')
        self.assertFalse(s['provider_universe_closed'])
        self.assertEqual(s['reused_binary_manifest']['same_artifact_sha256'],m['artifact_sha256'])
        self.assertEqual(s['resource']['sha256'],
                         m['resources']['data/alexscaves/enchantment/peppermint_punting.json'])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),s['card']['sha256'])
        return s,m

    def selected(self,m,owner,name):
        methods=[v for v in m['classes'][owner]['methods'] if v['name']==name]
        self.assertEqual(len(methods),1)
        return {v['offset']:v for v in methods[0]['anchors']}

    def test_json_version_level_and_costs(self):
        s,m=self.load()
        j=s['resource']['json']
        self.assertEqual(j['description']['translate'],'enchantment.alexscaves.peppermint_punting')
        self.assertEqual(j['supported_items'],'#alexscaves:enchantable/sugar_staff')
        self.assertEqual((j['weight'],j['max_level'],j['anvil_cost'],j['slots']),(2,1,4,['mainhand']))
        self.assertEqual(j['min_cost'],{'base':1,'per_level_above_first':12})
        self.assertEqual(j['max_cost'],{'base':41,'per_level_above_first':10})
        self.assertEqual(s['item_tag']['values'],['alexscaves:sugar_staff'])
        self.assertEqual(s['english_translations']['enchantment.alexscaves.peppermint_punting.desc'],
                         'Peppermints bounce directly ahead instead of around the attacker')

    def test_selected_anchors_match_the_SHA_exact_parent(self):
        s,m=self.load()
        self.assertEqual(len(s['anchors']),s['limits']['sealed_pivots'])
        self.assertGreaterEqual(len(s['anchors']),130)
        self.assertEqual(set(s['class_hashes']),set([a['class'] for a in s['anchors']]))
        for path,digest in s['class_hashes'].items():
            self.assertEqual(digest,m['classes'][path]['sha256'])
        for anchor in s['anchors']:
            row=self.selected(m,anchor['class'],anchor['method'])[anchor['offset']]
            self.assertEqual({k:row[k] for k in ('offset','opcode','operand','symbol')},
                             {k:anchor[k] for k in ('offset','opcode','operand','symbol')})

    def test_boolean_punting_vs_number_of_peppermints_and_straight(self):
        s,m=self.load()
        a=self.selected(m,ITEM,'use')
        self.assertIn('MULTIPLE_MINT',a[189]['symbol'])
        self.assertIn('PEPPERMINT_PUNTING',a[262]['symbol'])
        self.assertEqual((a[268]['opcode'],a[268]['operand']),('ifle','312'))
        self.assertIn('setStraight',a[274]['symbol'])
        self.assertIn('setStraight',a[315]['symbol'])
        self.assertIn('8.0f',a[300]['symbol'])
        self.assertIn('12.0f',a[337]['symbol'])
        self.assertIn('getYHeadRot',a[282]['symbol'])
        self.assertIn('setYRot',a[295]['symbol'])
        self.assertEqual(a[305]['operand'],'20')
        self.assertEqual(a[201]['operand'],'80')
        self.assertIn('SEEKCANDY',a[349]['symbol'])
        self.assertEqual(a[375]['operand'],'50')
        self.assertIn('addCooldown',a[461]['symbol'])
        self.assertIn('hurtAndBreakUsedHand',a[468]['symbol'])
        self.assertEqual(a[421]['opcode'],'pop')

    def test_tick_overwrites_and_server_straight_motion(self):
        s,m=self.load()
        a=self.selected(m,ENTITY,'tick')
        for n,text in [(63,'3.0f'),(65,'setSpinRadius'),(69,'7.0f'),(71,'setSpinSpeed'),
                       (466,'isStraight'),(476,'isClientSide'),(492,'getSpinSpeed'),
                       (510,'Vec3.yRot'),(523,'setDeltaMovement'),(596,'move'),
                       (737,'hurtEntities')]:
            self.assertIn(text,a[n]['symbol'])
        self.assertEqual((a[469]['opcode'],a[469]['operand']),('ifeq','602'))
        self.assertEqual((a[479]['opcode'],a[479]['operand']),('ifne','736'))

    def test_targeting_damage_hit_ack_and_persistence_not_promoted(self):
        s,m=self.load()
        h=self.selected(m,ENTITY,'hurtEntities')
        self.assertIn('getBoundingBox',h[1]['symbol'])
        self.assertIn('mobProjectile',h[14]['symbol'])
        self.assertIn('3.0f',h[143]['symbol'])
        self.assertIn('ACCompat.hurt',h[145]['symbol'])
        self.assertEqual((h[148]['opcode'],h[148]['operand']),('ifeq','181'))
        self.assertIn('knockback',h[178]['symbol'])
        self.assertIn('discard',h[197]['symbol'])
        load=self.selected(m,ENTITY,'readAdditionalSaveData')
        for offset,key in ((100,'AroundX'),(107,'AroundZ'),(114,'AroundZ')):
            self.assertIn(key,load[offset]['symbol'])
        self.assertNotIn('SEEKING_ENTITY',str(load))
        self.assertEqual(s['limits']['effective_hit'],'NOT_CERTIFIED')

    def test_seven_axes_certificate_and_crosswalk(self):
        s,m=self.load()
        ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        cert=ledger['objects'][P.name+'/'+CARD]
        self.assertEqual(cert['status'],'COMPLETE_PERK_READY')
        self.assertEqual(cert['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(cert['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(cert['physical_qa'],'NOT_TESTED')
        self.assertEqual(set(cert['evidence']),
                         {'identity','behavior','parameters','targeting','costs','integration','validation'})
        self.assertEqual({v['path'] for v in cert['evidence'].values()},
                         {str((P/CARD).relative_to(ROOT))})
        cross=(P/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        for name in ('individual_full_enchantment_dossiers=7/51',
                     'individual_partial_enchantment_dossiers=20/51',
                     'individual_existing_enchantment_dossiers=27/51',
                     '| ✅ | `alexscaves:peppermint_punting`'):
            self.assertIn(name,cross)

if __name__=='__main__':
    unittest.main()
