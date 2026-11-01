#!/usr/bin/env python3
"""Fail-closed synthetic Spirit Dinosaur factory/operand audit regressions."""
import unittest
from alexscaves_1010_spirit_dinosaur_probe import CLASSES, SpiritProbeError, caller_anchor, compact, summarize

def i(offset, opcode, symbol='', operand=''):
    return {'offset':offset,'opcode':opcode,'symbol':symbol,'operand':operand}

def specimen():
    path, entry = next(iter(CLASSES.items()))
    m = {'header':'private void '+entry['method']+'()', 'descriptor':entry['descriptor'],
         'instructions':[i(0,'aload_0'),i(entry['offset'],'invokestatic',
           'Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.causeSpiritDinosaurDamage:(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;'),i(entry['offset']+4,'fconst_2'),i(entry['offset']+5,'return')]}
    return entry,m

class SpiritDinosaurEvidenceTest(unittest.TestCase):
    def test_two_unique_exact_class_hashes(self):
        self.assertEqual(len(CLASSES),2)
        self.assertEqual(len(set(x['sha'] for x in CLASSES.values())),2)
        self.assertTrue(all(len(x['sha'])==64 for x in CLASSES.values()))
    def test_exact_factory_identified(self):
        e,m=specimen()
        self.assertEqual(caller_anchor(m,e)['offset'],131)
    def test_moved_factory_rejected(self):
        e,m=specimen();m['instructions'][1]['offset']+=1
        with self.assertRaisesRegex(SpiritProbeError,'drift'): caller_anchor(m,e)
    def test_wrong_factory_rejected(self):
        e,m=specimen();m['instructions'][1]['symbol']='Method causeNukeDamage:()V'
        with self.assertRaisesRegex(SpiritProbeError,'drift'): caller_anchor(m,e)
    def test_changed_descriptor_rejected(self):
        e,m=specimen();m['descriptor']='()V'
        with self.assertRaisesRegex(SpiritProbeError,'drift'): caller_anchor(m,e)
    def test_bounded_reference_window(self):
        e,m=specimen();out=summarize(m,[131])
        self.assertEqual(out['selected_windows'][0]['offset'],131)
        self.assertEqual(out['damage_accepted_or_counted'],'NOT_VERIFIED')
        self.assertEqual(len(out['parsed_method_sha256']),64)
    def test_wrong_selected_offset_rejected(self):
        e,m=specimen()
        with self.assertRaisesRegex(SpiritProbeError,'offset missing'): summarize(m,[1026])
    def test_duplicate_instruction_offset_rejected(self):
        e,m=specimen();m['instructions'].append(i(131,'return'))
        with self.assertRaisesRegex(SpiritProbeError,'offsets'): summarize(m,[131])
    def test_oversize_method_rejected(self):
        e,m=specimen();m['instructions']=[i(n,'aload_0') for n in range(6501)]
        with self.assertRaisesRegex(SpiritProbeError,'count'): summarize(m,[])
    def test_no_unbounded_source_export(self):
        row=i(5,'aload_0');row['source_body']='secret'
        self.assertNotIn('source_body', compact(row))

if __name__ == '__main__':
    unittest.main()
