#!/usr/bin/env python3
"""Spirit Dinosaur static closure must preserve causal and runtime boundaries."""
import hashlib
import json
from pathlib import Path
import unittest
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'

class SpiritDinosaurContract(unittest.TestCase):
    def anchors(self,d,owner,name,descriptor=None):
        rows=[m for m in d['classes'][PREFIX+owner+'.class']['methods']
              if m['name']==name and (descriptor is None or m['descriptor']==descriptor)]
        self.assertEqual(len(rows),1,(owner,name,descriptor))
        return {a['offset']:a for a in rows[0]['anchors']}

    def test_complete_own_rosters_and_historical_snapshot_preserved(self):
        d=assert_sealed_damage_contract(self,'spirit_dinosaur')
        for owner,count in (('server/entity/item/DinosaurSpiritEntity',32),
                            ('server/entity/item/DinosaurSpiritEntity$DinosaurType',5),
                            ('server/entity/item/ExtinctionSpearEntity',18),
                            ('server/item/ExtinctionSpearItem',9),('server/item/SpearItem',12)):
            self.assertEqual(len(d['classes'][PREFIX+owner+'.class']['methods']),count,owner)
        self.assertEqual(hashlib.sha256((P/'EXACT-SPIRIT-DINOSAUR-1.0.10.json').read_bytes()).hexdigest(),
                         '5d7f62a1dc12d1fa9bbe7ae6445ef926bd46eddf91d4eae0505660a1d65dc887')
        enum=self.anchors(d,'server/entity/item/DinosaurSpiritEntity','getDinosaurType')
        self.assertTrue(any(a['opcode']=='arraylength' for a in enum.values()))
        self.assertTrue(any('Mth.clamp' in a['symbol'] for a in enum.values()))
        self.assertTrue(any(a['opcode']=='aaload' for a in enum.values()))

    def test_opposite_damage_flags_and_fading_fallthrough(self):
        d=assert_sealed_damage_contract(self,'spirit_dinosaur')
        spirit='server/entity/item/DinosaurSpiritEntity';spear='server/entity/item/ExtinctionSpearEntity'
        a=self.anchors(d,spirit,'tickTremorsaurus')
        for offset,symbol in ((116,'dealtDamage'),(131,'causeSpiritDinosaurDamage'),(143,'ACCompat.hurt'),(151,'dealtDamage'),(156,'setFading')):
            self.assertIn(symbol,a[offset]['symbol'])
        self.assertEqual((a[146]['opcode'],a[146]['operand']),('ifeq','154'))
        self.assertEqual(a[142]['opcode'],'i2f')
        tick=self.anchors(d,spirit,'tick')
        self.assertIn('discard',tick[195]['symbol'])
        self.assertIn('tickTremorsaurus',tick[322]['symbol'])
        self.assertFalse(any(v['opcode']=='return' for k,v in tick.items() if 195<k<322))
        b=self.anchors(d,spear,'onHitEntity')
        for offset,symbol in ((58,'causeSpiritDinosaurDamage'),(65,'dealtDamage'),(85,'igniteForSeconds'),(92,'ACCompat.hurt'),(277,'addFreshEntity')):
            self.assertIn(symbol,b[offset]['symbol'])
        self.assertEqual((b[95]['opcode'],b[95]['operand']),('ifeq','281'))
        self.assertEqual(b[108]['opcode'],'return')
        self.assertEqual(b[280]['opcode'],'pop')

    def test_native_costs_producers_and_separate_explosion(self):
        d=assert_sealed_damage_contract(self,'spirit_dinosaur')
        item='server/item/ExtinctionSpearItem'
        release=self.anchors(d,item,'releaseUsing')
        for offset,symbol in ((48,'hurtAndBreak'),(59,'<init>'),(85,'shootFromRotation'),(110,'addFreshEntity'),(153,'shrink'),(171,'killGrottoGhostsFor')):
            self.assertIn(symbol,release[offset]['symbol'])
        self.assertEqual(release[113]['opcode'],'pop')
        for method,kind in (('acHurtEnemy','TREMORSAURUS'),('onUseTick','GROTTOCERATOPS')):
            rows=self.anchors(d,item,method)
            self.assertTrue(any(kind in a['symbol'] for a in rows.values()))
            self.assertTrue(any('addFreshEntity' in a['symbol'] for a in rows.values()))
        impact=self.anchors(d,'server/entity/item/ExtinctionSpearEntity','onHitEntity')
        self.assertIn('SUBTERRANODON',impact[201]['symbol'])
        boom=self.anchors(d,'server/entity/item/ExtinctionSpearEntity','explode')
        self.assertTrue(any('TephraExplosion' in a['symbol'] for a in boom.values()))
        self.assertFalse(any('causeSpiritDinosaurDamage' in a['symbol'] for a in boom.values()))
        for key in ('chomping_spirit','herd_phalanx','plummeting_flight'):
            self.assertIn('data/alexscaves/enchantment/'+key+'.json',d['resources'])
        self.assertEqual(d['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(d['physical_qa'],'NOT_TESTED')
        self.assertFalse(d['provider_universe_closed'])

    def test_scope_inventory_matches_certificates_without_provider_closure(self):
        inventory=json.loads((P/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        self.assertFalse(inventory['whole_provider_catalog_closed'])
        for family,directory in (('damage_types','damage-types'),('equipment_contracts','equipment')):
            status=inventory['family_catalog_status'][family]
            certified={key[len(P.name)+1:] for key,value in ledger['objects'].items()
                       if key.startswith(P.name+'/'+directory+'/') and value['status']=='COMPLETE_PERK_READY'}
            self.assertEqual(set(status['cards']),certified)
            self.assertEqual(status['documented_static_contracts'],len(certified))

if __name__=='__main__':unittest.main()
