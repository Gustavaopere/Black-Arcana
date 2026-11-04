#!/usr/bin/env python3
"""Keep Herd Phalanx spawn, selection and event semantics static and separate."""
import hashlib,json,unittest
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,validate_cards
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
PREFIX='com/github/alexmodguy/alexscaves/'
CARD='enchantments/herd-phalanx.md'
class HerdPhalanxContract(unittest.TestCase):
    def contract(self):
        d=load_manifest(P/'EXACT-HERD-PHALANX-CONTRACT-1.0.10.json')
        validate_structure(d,profile='herd_phalanx');validate_cards(d,P,profile='herd_phalanx')
        return d
    def anchors(self,d,owner,name):
        ms=[m for m in d['classes'][PREFIX+owner+'.class']['methods'] if m['name']==name]
        self.assertEqual(len(ms),1,(owner,name))
        return {a['offset']:a for a in ms[0]['anchors']}
    def test_singleton_identity_and_required_complete_chain(self):
        d=self.contract();self.assertEqual(set(d['cards']),{CARD})
        self.assertEqual(d['catalog_family'],'HERD_PHALANX_ENCHANTMENT_CONTRACT')
        for owner,name in (('server/item/ExtinctionSpearItem','onUseTick'),('server/item/ExtinctionSpearItem','killGrottoGhostsFor'),('server/entity/item/DinosaurSpiritEntity','tickGrottoceratops'),('server/event/CommonEvents','acCancelDamage'),('server/event/CommonEvents','livingHurt')):
            self.assertTrue(self.anchors(d,owner,name))
        self.assertEqual(d['resources']['data/alexscaves/enchantment/herd_phalanx.json'],'294818f10b6327c0ca06ef4510d599bba0a61a6c47ffc044236268411ccc0616')
        for name in ('in_enchanting_table','non_treasure','on_random_loot','tradeable'):
            self.assertIn('data/minecraft/tags/enchantment/'+name+'.json',d['resources'])
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),d['cards'][CARD])
    def test_initial_equality_count_loop_and_ignored_insertion(self):
        d=self.contract();a=self.anchors(d,'server/item/ExtinctionSpearItem','onUseTick')
        self.assertEqual((a[8]['opcode'],a[8]['operand']),('if_icmpne','132'))
        self.assertEqual(a[36]['opcode'],'iconst_3');self.assertIn('HERD_PHALANX',a[38]['symbol'])
        self.assertEqual(a[44]['opcode'],'iadd');self.assertEqual(a[52]['opcode'],'fdiv')
        self.assertEqual((a[62]['opcode'],a[62]['operand']),('if_icmpge','132'))
        for o,s in ((77,'createEntity'),(93,'GROTTOCERATOPS'),(105,'setPlayerUUID'),(116,'setRotateOffset'),(122,'addFreshEntity')):
            self.assertIn(s,a[o]['symbol'])
        self.assertEqual(a[125]['opcode'],'pop')
        self.assertFalse(any('setEnchantmentLevel' in v['symbol'] for v in a.values()))
        use=self.anchors(d,'server/item/SpearItem','getUseDuration');self.assertIn('72000',use[0]['symbol'])
    def test_box_uuid_and_asymmetric_selection_are_not_rewritten(self):
        d=self.contract();a=self.anchors(d,'server/item/ExtinctionSpearItem','killGrottoGhostsFor')
        for o in (12,15,18):self.assertIn('30.0d',a[o]['symbol'])
        self.assertIn('AABB.inflate',a[21]['symbol'])
        self.assertIn('getPlayerUUID',a[55]['symbol']);self.assertIn('UUID.equals',a[62]['symbol'])
        self.assertIn('getDinosaurType',a[70]['symbol']);self.assertIn('isFading',a[81]['symbol'])
        self.assertEqual((a[104]['opcode'],a[105]['opcode']),('aload_2','aload_0'))
        self.assertEqual((a[109]['opcode'],a[109]['operand']),('aload','4'))
        self.assertEqual(a[111]['opcode'],'aload_2');self.assertIn('distanceTo',a[112]['symbol'])
        self.assertEqual((a[116]['opcode'],a[116]['operand']),('ifle','122'))
        self.assertIn('setFading',a[135]['symbol'])
    def test_native_pre_zero_damage_and_orbit_stop_have_independent_guards(self):
        d=self.contract();a=self.anchors(d,'server/event/CommonEvents','livingHurt')
        self.assertIn('acCancelDamage',a[8]['symbol']);self.assertEqual(a[15]['opcode'],'fconst_0')
        self.assertIn('LivingDamageEvent$Pre.setNewDamage',a[16]['symbol'])
        self.assertFalse(any('setCanceled' in v['symbol'] for v in a.values()))
        orbit=self.anchors(d,'server/entity/item/DinosaurSpiritEntity','tickGrottoceratops')
        self.assertEqual((orbit[8]['opcode'],orbit[9]['opcode'],orbit[10]['opcode']),('iconst_5','imul','i2f'))
        self.assertIn('Math.toRadians',orbit[27]['symbol']);self.assertIn('0.25d',orbit[62]['symbol'])
        self.assertEqual((orbit[83]['opcode'],orbit[83]['operand']),('ifne','112'))
        self.assertIn('setFading',orbit[109]['symbol'])
        tick=self.anchors(d,'server/entity/item/DinosaurSpiritEntity','tick')
        self.assertIn('discard',tick[195]['symbol']);self.assertIn('tickGrottoceratops',tick[314]['symbol'])
        self.assertFalse(any(v['opcode']=='return' for k,v in tick.items() if 195<k<314))
    def test_seven_static_fields_and_crosswalk_keep_runtime_pending(self):
        d=self.contract();ledger=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text());cert=ledger['objects'][P.name+'/'+CARD]
        for x in (d,cert):
            self.assertEqual(x['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
            self.assertEqual(x['mutating_hook'],'NOT_VERIFIED');self.assertEqual(x['physical_qa'],'NOT_TESTED')
        self.assertFalse(d['provider_universe_closed'])
        self.assertEqual(set(cert['evidence']),{'identity','behavior','parameters','targeting','costs','integration','validation'})
        self.assertEqual({v['path'] for v in cert['evidence'].values()},{str((P/CARD).relative_to(ROOT))})
        cross=(P/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text()
        for m in ('individual_full_enchantment_dossiers=2/51','individual_partial_enchantment_dossiers=20/51','individual_existing_enchantment_dossiers=22/51','| ✅ | `alexscaves:herd_phalanx`'):
            self.assertIn(m,cross)
if __name__=='__main__':unittest.main()
