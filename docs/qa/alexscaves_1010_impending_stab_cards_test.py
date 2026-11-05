#!/usr/bin/env python3
"""Keep Impending's producer delay and late damage read causally separate."""
import json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'
CARD='enchantments/impending-stab.md'
class ImpendingStabContract(unittest.TestCase):
    def contract(self):
        d=load_manifest(P/'EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json')
        validate_structure(d,profile='impending_stab');validate_cards(d,P,profile='impending_stab')
        return d
    def anchors(self,d,owner,name,descriptor=None):
        rows=[m for m in d['classes'][PREFIX+owner+'.class']['methods'] if m['name']==name and (descriptor is None or m['descriptor']==descriptor)]
        self.assertEqual(len(rows),1,(owner,name,descriptor))
        return {a['offset']:a for a in rows[0]['anchors']}
    def test_singleton_identity_and_all_own_members(self):
        d=self.contract();self.assertEqual(set(d['cards']),{CARD})
        self.assertEqual(d['catalog_family'],'IMPENDING_STAB_ENCHANTMENT_CONTRACT')
        for owner,n in (('server/item/DesolateDaggerItem',6),('server/entity/item/DesolateDaggerEntity',20)):
            self.assertEqual(len(d['classes'][PREFIX+owner+'.class']['methods']),n)
        self.assertEqual(d['resources']['data/alexscaves/enchantment/impending_stab.json'],'bb3918b0fdf897ad70897952d15094e04d8af905b3e2f2db0d2159b762f5ffbc')
        for tag in ('in_enchanting_table','non_treasure','on_random_loot','tradeable'):
            self.assertIn('data/minecraft/tags/enchantment/'+tag+'.json',d['resources'])
        text=(P/CARD).read_text()
        for t in ('exclusive_set','alexscaves:double_stab','NOT_VERIFIED','NOT_TESTED'):self.assertIn(t,text)
    def test_cached_positive_level_selects_two_delay_ranges_not_per_level_delay(self):
        d=self.contract();a=self.anchors(d,'server/item/DesolateDaggerItem','acSpawnDaggers')
        self.assertIn('IMPENDING_STAB',a[1]['symbol']);self.assertEqual(a[7]['operand'],'4')
        self.assertEqual((a[74]['opcode'],a[74]['operand']),('ifle','82'))
        self.assertEqual((a[77]['operand'],a[82]['operand'],a[88]['operand']),('40','20','10'))
        self.assertIn('nextInt',a[90]['symbol']);self.assertEqual(a[95]['opcode'],'iadd')
        self.assertIn('orbitFor',a[96]['symbol']);self.assertIn('DOUBLE_STAB',a[16]['symbol'])
        self.assertEqual((a[23]['opcode'],a[23]['operand']),('if_icmpge','115'))
        self.assertEqual((a[112]['opcode'],a[112]['operand']),('goto','12'))
        self.assertEqual(a[108]['opcode'],'pop')
    def test_stack_and_target_pass_through_without_native_player_binding(self):
        d=self.contract();a=self.anchors(d,'server/item/DesolateDaggerItem','acSpawnDaggers')
        for o,s in ((55,'setTargetId'),(61,'copyPosition'),(67,'setItemStack'),(105,'addFreshEntity')):self.assertIn(s,a[o]['symbol'])
        self.assertFalse(any('setPlayerId' in v['symbol'] or 'ItemStack.copy:' in v['symbol'] for v in a.values()))
        setter=self.anchors(d,'server/entity/item/DesolateDaggerEntity','setItemStack')
        self.assertIn('SynchedEntityData.set',setter[8]['symbol'])
        self.assertFalse(any('ItemStack.copy:' in v['symbol'] for v in setter.values()))
    def test_server_stab_rechecks_level_and_discards_after_rejected_hurt(self):
        a=self.anchors(self.contract(),'server/entity/item/DesolateDaggerEntity','tick')
        self.assertEqual((a[239]['opcode'],a[239]['operand']),('ifne','438'))
        self.assertEqual((a[246]['opcode'],a[246]['operand']),('ifle','269'))
        self.assertIn('isAlive',a[250]['symbol']);self.assertIn('getPlayer',a[294]['symbol'])
        self.assertEqual((a[301]['opcode'],a[301]['operand']),('ifnonnull','308'))
        self.assertIn('getItemStack',a[314]['symbol']);self.assertIn('IMPENDING_STAB',a[317]['symbol'])
        self.assertEqual((a[312]['opcode'],a[323]['opcode'],a[324]['opcode'],a[325]['opcode'],a[326]['opcode']),('fconst_2','i2f','fconst_2','fmul','fadd'))
        self.assertIn('causeDesolateDaggerDamage',a[339]['symbol']);self.assertIn('ACCompat.hurt',a[344]['symbol'])
        self.assertEqual((a[347]['opcode'],a[347]['operand']),('ifeq','434'))
        self.assertIn('discard',a[435]['symbol'])
    def test_custom_state_has_no_own_nbt_and_runtime_is_not_promoted(self):
        d=self.contract();owner='server/entity/item/DesolateDaggerEntity'
        for method in ('readAdditionalSaveData','addAdditionalSaveData'):
            a=self.anchors(d,owner,method);self.assertEqual(len(a),1);self.assertEqual(a[0]['opcode'],'return')
        self.assertEqual(d['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY');self.assertEqual(d['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(d['physical_qa'],'NOT_TESTED');self.assertFalse(d['provider_universe_closed'])
    def test_certificate_seven_axes_and_crosswalk(self):
        self.contract();ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text());cert=ledger['objects'][P.name+'/'+CARD]
        self.assertEqual(set(cert['evidence']),{'identity','behavior','parameters','targeting','costs','integration','validation'})
        self.assertEqual({e['path'] for e in cert['evidence'].values()},{str((P/CARD).relative_to(ROOT))})
        self.assertEqual(cert['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY');self.assertEqual(cert['mutating_hook'],'NOT_VERIFIED');self.assertEqual(cert['physical_qa'],'NOT_TESTED')
        self.assertIn('| ✅ | `alexscaves:impending_stab`',(P/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text())
if __name__=='__main__':unittest.main()
