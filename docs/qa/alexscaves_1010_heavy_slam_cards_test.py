#!/usr/bin/env python3
"""Guard the Heavy Slam static contract without authorizing runtime mutation."""
import json
import hashlib
from pathlib import Path
import unittest
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
CORE='com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem.class'
CARD='enchantments/heavy-slam.md'

class HeavySlamContract(unittest.TestCase):
    def contract(self):
        d=load_manifest(P/'EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json')
        validate_structure(d,profile='heavy_slam');validate_cards(d,P,profile='heavy_slam')
        return d
    def on_use(self,d):
        ms=[m for m in d['classes'][CORE]['methods'] if m['name']=='onUseTick']
        self.assertEqual(len(ms),1)
        return {a['offset']:a for a in ms[0]['anchors']}
    def test_literal_singleton_and_all_own_members(self):
        d=self.contract()
        self.assertEqual(set(d['cards']),{CARD})
        self.assertEqual(d['catalog_family'],'HEAVY_SLAM_ENCHANTMENT_CONTRACT')
        self.assertEqual(len(d['classes'][CORE]['methods']),20)
        self.assertEqual({m['name'] for m in d['classes'][CORE]['methods']},{'<init>','initializeClient','use','appendHoverText','getEnchantmentValue','isEnchantable','onUseTick','acExtraRepairMaterials','isValidRepairItem','releaseUsing','acInventoryTick','setUseTime','setSwitchTime','setPolarity','getUseTime','getLerpedUseTime','getSwitchTime','getLerpedSwitchTime','isScarlet','shouldCauseReequipAnimation'})
        for p in ('data/alexscaves/enchantment/heavy_slam.json','data/alexscaves/tags/item/enchantable/resistor_shield.json','assets/alexscaves/lang/en_us.json'):
            self.assertIn(p,d['resources'])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),d['cards'][CARD])
    def test_first_slam_formula_and_separate_five_tick_sampling(self):
        a=self.on_use(self.contract())
        self.assertEqual((a[28]['opcode'],a[28]['operand']),('bipush','10'))
        self.assertEqual((a[35]['opcode'],a[35]['operand']),('bipush','12'))
        self.assertEqual((a[367]['opcode'],a[367]['operand']),('bipush','10'))
        self.assertEqual((a[374]['opcode'],a[375]['opcode']),('iconst_5','irem'))
        self.assertEqual((a[376]['opcode'],a[376]['operand']),('ifne','584'))
        self.assertIn('HEAVY_SLAM',a[48]['symbol'])
        self.assertEqual((a[480]['operand'],a[484]['opcode'],a[485]['opcode'],a[486]['opcode'],a[487]['opcode']),('6','iconst_3','imul','iadd','i2f'))
        self.assertEqual(a[491]['opcode'],'fconst_2')
    def test_hurt_acceptance_does_not_guard_movement_or_target_independent_cost(self):
        a=self.on_use(self.contract())
        for o,symbol in ((390,'AABB.inflate'),(438,'isAlliedTo'),(456,'distanceTo'),(472,'mobAttack'),(492,'LivingEntity.hurt'),(537,'ACCompat.knockback'),(578,'ACCompat.knockback'),(601,'hurtAndBreakUsedHand')):
            self.assertIn(symbol,a[o]['symbol'])
        self.assertEqual(a[495]['opcode'],'pop')
        self.assertEqual((a[64]['opcode'],a[64]['operand']),('ifeq','365'))
        self.assertEqual((a[462]['opcode'],a[462]['operand']),('ifgt','581'))
        self.assertEqual((a[588]['opcode'],a[588]['operand']),('if_icmpne','604'))
        self.assertEqual((a[595]['opcode'],a[595]['operand']),('ifne','604'))
        self.assertEqual(a[599]['opcode'],'iconst_1')
    def test_azure_uses_same_user_x_twice_without_editorial_repair(self):
        a=self.on_use(self.contract())
        self.assertEqual((a[559]['opcode'],a[563]['opcode']),('aload_2','aload_2'))
        self.assertIn('getX',a[560]['symbol']);self.assertIn('getX',a[564]['symbol'])
        self.assertEqual(a[567]['opcode'],'dsub')
        self.assertEqual(a[568]['opcode'],'aload_2')
        self.assertEqual((a[572]['opcode'],a[572]['operand']),('aload','12'))
        self.assertIn('getZ',a[569]['symbol']);self.assertIn('getZ',a[574]['symbol'])
    def test_certificate_crosswalk_and_independent_runtime_limits(self):
        d=self.contract();ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        cert=ledger['objects'][P.name+'/'+CARD]
        for x in (d,cert):
            self.assertEqual(x['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
            self.assertEqual(x['mutating_hook'],'NOT_VERIFIED');self.assertEqual(x['physical_qa'],'NOT_TESTED')
        self.assertFalse(d['provider_universe_closed'])
        self.assertEqual(set(cert['evidence']),{'identity','behavior','parameters','targeting','costs','integration','validation'})
        self.assertEqual({v['path'] for v in cert['evidence'].values()},{str((P/CARD).relative_to(ROOT))})
        cards=list((P/'enchantments').glob('*.md'));cards=[p for p in cards if p.name not in ('INDEX.md','README.md')]
        certified=[k for k in ledger['objects'] if k.startswith(P.name+'/enchantments/')]
        self.assertEqual(certified,[P.name+'/'+CARD])
        self.assertEqual(len(cards),21)
        cross=(P/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        for marker in ('individual_full_enchantment_dossiers=1/51','individual_partial_enchantment_dossiers=20/51','individual_existing_enchantment_dossiers=21/51','| ✅ | `alexscaves:heavy_slam`'):
            self.assertIn(marker,cross)

if __name__=='__main__':unittest.main()
