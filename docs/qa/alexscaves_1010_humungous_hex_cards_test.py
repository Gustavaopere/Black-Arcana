#!/usr/bin/env python3
"""Guard Humungous Hex's static perimeter and reject false perk/QA promotion."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
CARD='enchantments/humungous-hex.md'
SEAL='EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json'
ITEM='com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.class'
HEX='com/github/alexmodguy/alexscaves/server/entity/item/SugarStaffHexEntity.class'
RENDER='com/github/alexmodguy/alexscaves/client/render/entity/SugarStaffHexRenderer.class'

class HumungousHexContract(unittest.TestCase):
    def contract(self):
        d=json.loads((P/SEAL).read_text(encoding='utf8'))
        self.assertEqual(d['claim_scope'],'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(d['evidence_grade'],'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertFalse(d['limits']['provider_universe_closed'])
        self.assertEqual(d['limits']['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(d['limits']['physical_qa'],'NOT_TESTED')
        self.assertEqual(d['limits']['mutation'],'NO_MUTATION')
        self.assertEqual(hashlib.sha256((P/CARD).read_bytes()).hexdigest(),
                         d['card']['sha256'])
        return d
    def test_json_identity_and_not_cast_cost(self):
        d=self.contract()
        j=d['resource']['json']
        self.assertEqual(d['resource']['id'],'alexscaves:humungous_hex')
        self.assertEqual(j['supported_items'],'#alexscaves:enchantable/sugar_staff')
        self.assertEqual(j['slots'],['mainhand'])
        self.assertEqual([j['weight'],j['max_level'],j['anvil_cost']],[5,2,2])
        self.assertEqual(j['min_cost'],{'base':1,'per_level_above_first':9})
        self.assertEqual(j['max_cost'],{'base':41,'per_level_above_first':10})
        self.assertEqual(d['resource']['item_tag']['json']['values'],
                         ['alexscaves:sugar_staff'])
        self.assertEqual(d['resource']['spell_lasting']['json']['max_level'],3)
    def test_separate_dimensions_targeting_and_renderer(self):
        d=self.contract()
        anchors=d['anchors']
        def has(owner,method,offset,needle):
            return any(x['class']==owner and x['method']==method
                       and x['offset']==offset and needle in x['symbol_contains']
                       for x in anchors)
        self.assertTrue(has(ITEM,'use',118,'setHexScale'))
        self.assertTrue(has(HEX,'getDimensions',4,'4.0f'))
        self.assertTrue(has(HEX,'getDimensions',7,'0.25f'))
        self.assertTrue(has(HEX,'hurtEntities',53,'distanceTo'))
        self.assertTrue(has(HEX,'hurtEntities',145,'indirectMagic'))
        self.assertTrue(has(RENDER,'render',75,'getHexScale'))
        self.assertTrue(has(RENDER,'render',108,'mulPose'))
        self.assertTrue(has(RENDER,'render',119,'scale'))
        for owner in (ITEM,HEX,RENDER):
            self.assertTrue(d['classes'][owner]['method_digests'])
        text=(P/CARD).read_text(encoding='utf8')
        for token in ('4 blocos','5 blocos','6 blocos','distanceTo(hex) <= 4F',
                      '800','NOT_VERIFIED','NO_MUTATION'):
            # 800 is not part of this contract: reject false Gamma Ray contamination.
            if token=='800':self.assertNotIn('800 ticks',text)
            else:self.assertIn(token,text)
    def test_ledger_crosswalk_and_static_only(self):
        d=self.contract()
        data=json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text(encoding='utf8'))
        cert=data['objects'][P.name+'/'+CARD]
        self.assertEqual(cert['status'],'COMPLETE_PERK_READY')
        self.assertEqual(cert['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(cert['physical_qa'],'NOT_TESTED')
        self.assertEqual(set(cert['evidence']),{'identity','behavior','parameters','targeting','costs','integration','validation'})
        self.assertEqual({v['path'] for v in cert['evidence'].values()},{str((P/CARD).relative_to(ROOT))})
        cross=(P/'ENCHANTMENT-PERK-CROSSWALK-1.0.10.md').read_text(encoding='utf8')
        cards=[p for p in (P/'enchantments').glob('*.md') if p.name not in ('INDEX.md','README.md')]
        certified=[k for k in data['objects'] if k.startswith(P.name+'/enchantments/')]
        for needle in (f'individual_full_enchantment_dossiers={len(certified)}/51',
                       f'individual_partial_enchantment_dossiers={len(cards)-len(certified)}/51',
                       f'individual_existing_enchantment_dossiers={len(cards)}/51',
                       '| ✅ | `alexscaves:humungous_hex`'):
            self.assertIn(needle,cross)

if __name__=='__main__':
    unittest.main()
