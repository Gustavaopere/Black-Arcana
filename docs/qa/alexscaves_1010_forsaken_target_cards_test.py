#!/usr/bin/env python3
"""Sealed, bounded Forsaken target eligibility evidence and pending runtime guards."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE
from alexscaves_1010_forsaken_target_probe import SELECTION
from alexscaves_1010_forsaken_helper_probe import EXACT_CLASSES
ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/'wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types'

class ForsakenTargetCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads((DIR/'EXACT-FORSAKEN-TARGETING-1.0.10.json').read_text(encoding='utf8'))
        cls.card=(DIR/'forsaken-sonic-boom.md').read_text(encoding='utf8')
        cls.methods={m['name']:m for c in cls.doc['classes'] for m in c['selected_methods']}
    def test_exact_scope_roster_and_pending_runtime(self):
        self.assertEqual(self.doc['scope'],'EXACT_1010_FORSAKEN_TARGET_PREDICATE_AND_GOAL_GATES_ONLY')
        self.assertEqual(self.doc['publisher_jar'],{'sha1':SHA1,'sha256':SHA256,'size_bytes':SIZE})
        roster={c['class_path']:[(m['name'],m['descriptor']) for m in c['selected_methods']] for c in self.doc['classes']}
        self.assertEqual(roster,SELECTION)
        self.assertEqual(sum(len(m['instructions']) for m in self.methods.values()),52)
        for c in self.doc['classes']:
            self.assertEqual(c['class_sha256'],EXACT_CLASSES[c['class_path']])
        self.assertEqual(self.doc['limits']['mutating_hook'],'NOT_VERIFIED')
        self.assertEqual(self.doc['limits']['physical_qa'],'NOT_TESTED')
        self.assertFalse(self.doc['limits']['complete_perk_ready'])
        self.assertFalse(self.doc['limits']['provider_universe_closed'])
    def instructions(self,name):
        return {i['offset']:i for i in self.methods[name]['instructions']}
    def test_exclusion_predicate_branches(self):
        i=self.instructions('lambda$static$0')
        self.assertIn('FORSAKEN_IGNORES',i[7]['symbol'])
        self.assertIn('Holder$Reference.is:',i[10]['symbol'])
        self.assertEqual((i[13]['opcode'],i[13]['operand']),('ifne','20'))
        self.assertEqual(i[16]['opcode'],'iconst_1')
        self.assertEqual(i[20]['opcode'],'iconst_0')
        self.assertEqual(i[21]['opcode'],'ireturn')
    def test_adapter_preserves_input_reference(self):
        instructions=self.methods['targetSelector']['instructions']
        self.assertEqual([(i['offset'],i['opcode']) for i in instructions],[(0,'aload_0'),(1,'areturn')])
        self.assertEqual(self.methods['targetSelector']['selected_symbolic_windows'],[])
        self.assertEqual(self.methods['targetSelector']['branch_anchors'],[])
    def test_goal_entry_and_resets_remain_distinct(self):
        can=self.instructions('canUse')
        self.assertIn('getTarget:',can[4]['symbol'])
        self.assertEqual((can[9]['opcode'],can[9]['operand']),('ifnull','23'))
        self.assertIn('isAlive:',can[13]['symbol'])
        self.assertEqual((can[16]['opcode'],can[16]['operand']),('ifeq','23'))
        start=self.instructions('start')
        for value,write,field in [(1,2,'navigationCheckCooldown'),(6,7,'jumpEnqueued'),(27,28,'attemptSonicDamageIn')]:
            self.assertEqual(start[value]['opcode'],'iconst_0')
            self.assertIn(field,start[write]['symbol'])
        self.assertIn('RandomSource.nextBoolean:',start[18]['symbol'])
        self.assertIn('sonicEnqueued',start[23]['symbol'])
        stop=self.instructions('stop')
        self.assertEqual(stop[1]['opcode'],'iconst_0')
        self.assertEqual(stop[6]['opcode'],'iconst_0')
        self.assertEqual(stop[14]['opcode'],'iconst_0')
        self.assertIn('jumpEnqueued',stop[2]['symbol'])
        self.assertIn('sonicEnqueued',stop[7]['symbol'])
        self.assertIn('setRunning:',stop[15]['symbol'])
        self.assertFalse(any('attemptSonicDamageIn' in i['symbol'] for i in stop.values()))
    def test_card_cites_each_identity_and_does_not_promote(self):
        for cls in self.doc['classes']:
            self.assertIn(cls['class_sha256'],self.card)
            for m in cls['selected_methods']:
                self.assertIn(m['descriptor'],self.card)
                self.assertIn(m['parsed_method_sha256'],self.card)
        for token in ['EXACT-FORSAKEN-TARGETING-1.0.10.json','52 instruções em cinco métodos',
                      'NOT_CERTIFIED','NOT_VERIFIED','NOT_TESTED','NO_MUTATION']:
            self.assertIn(token,self.card)

if __name__=='__main__':
    unittest.main()
