#!/usr/bin/env python3
"""Synthetic normal CFG regressions; no proprietary classfiles in fixtures."""
import unittest
from somake_109_blood_cut_cfg import graph_paths, modifier_fingerprint
from somake_109_perk_method_probe import GateError

INPUT="Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getNewDamage:()F"
DAMAGE="Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z"


def valid_cfg():
    # JVM byte offsets, not list indices; branch either skips secondary damage or reaches it.
    return [(0,"aload_0","",""),(1,"invokevirtual","",INPUT),
            (4,"ifeq","15",""),(7,"iconst_1","",""),
            (8,"invokestatic","",DAMAGE),(11,"pop","",""),
            (12,"goto","16",""),(15,"nop","",""),(16,"return","","")]


class GraphTests(unittest.TestCase):
    def test_gate_path_and_skip_path_are_distinct(self):
        report=graph_paths(valid_cfg(),expected_branches=2)
        self.assertEqual(1,report["syntactic_paths_to_apply"])
        self.assertEqual(1,report["syntactic_paths_without_apply"])
        self.assertEqual(4,report["secondary_apply_damage_index"])
        self.assertEqual(1,report["get_new_damage_index"])
        self.assertEqual(2,report["branch_count"])

    def test_missing_target_rejected(self):
        rows=valid_cfg()
        rows[2]=(4,"ifeq","14","")
        with self.assertRaises(GateError):
            graph_paths(rows)

    def test_duplicate_pc_rejected(self):
        rows=valid_cfg()
        rows[3]=(4,"iconst_1","","")
        with self.assertRaises(GateError):
            graph_paths(rows)

    def test_loop_requires_separate_analysis(self):
        rows=valid_cfg()
        rows[6]=(12,"goto","1","")
        with self.assertRaises(GateError):
            graph_paths(rows)

    def test_duplicated_secondary_call_rejected(self):
        rows=valid_cfg()
        rows[5]=(11,"invokestatic","",DAMAGE)
        with self.assertRaises(GateError):
            graph_paths(rows)

    def test_missing_event_damage_input_rejected(self):
        rows=valid_cfg()
        rows[1]=(1,"invokevirtual","","Method example.getHealth:()F")
        with self.assertRaises(GateError):
            graph_paths(rows)

    def test_branch_fingerprint_drift_rejected(self):
        with self.assertRaises(GateError):
            graph_paths(valid_cfg(),expected_branches=5)

    def test_no_valid_terminal_rejected(self):
        rows=valid_cfg()
        rows[-1]=(16,"nop","","")
        with self.assertRaises(GateError):
            graph_paths(rows)


class ModifierTests(unittest.TestCase):
    def test_missing_exact_native_size_fails(self):
        with self.assertRaises(GateError):
            modifier_fingerprint([(0,"freturn","","")])

    def test_no_power_multiplier_fails(self):
        rows=[(i,"nop","","") for i in range(19)]
        rows[2]=(2,"ifeq","8","")
        rows[8]=(8,"goto","18","")
        with self.assertRaises(GateError):
            modifier_fingerprint(rows)


if __name__=="__main__":
    unittest.main()
