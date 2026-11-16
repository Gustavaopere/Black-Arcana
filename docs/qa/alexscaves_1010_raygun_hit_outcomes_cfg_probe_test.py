#!/usr/bin/env python3
"""Synthetic, negative and positive regression tests for bounded Raygun CFG."""
import unittest

from alexscaves_1010_ferrous_haste_causal_audit import AuditError
from alexscaves_1010_raygun_hit_outcomes_cfg_probe import (
    FlowError, assert_native_pins, bounded_projection, normal_graph,
    shortest_bounded, verify_snapshot,
)

def ins(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand, "symbol": symbol}

def meth(rows):
    return {"header": "public void sample();", "descriptor": "()V",
            "instructions": rows}

class RaygunHitOutcomeCFGTests(unittest.TestCase):
    def test_conditional_taken_and_fallthrough_are_ordered(self):
        rows = [ins(0,"ifeq","6"), ins(3,"return"), ins(6,"goto","0")]
        graph, direct = normal_graph(meth(rows))
        self.assertEqual(direct, [[0,6],[6,0]])
        self.assertEqual(graph[0], (6,3))
        self.assertEqual(graph[3], ())
        self.assertEqual(graph[6], (0,))

    def test_bounded_reachability_stops_at_loop_boundary(self):
        graph = {0:(2,), 2:(6,), 6:(0,)}
        self.assertIsNone(shortest_bounded(graph,2,0,low=2,high=6))
        self.assertEqual(shortest_bounded(graph,0,2,low=0,high=6),[0,2])

    def test_path_uses_normal_branch_edges_only(self):
        graph = {0:(6,3),3:(9,),6:(9,),9:()}
        self.assertEqual(shortest_bounded(graph,0,9,low=0,high=10),[0,6,9])

    def test_empty_jvm_method_is_rejected(self):
        with self.assertRaisesRegex(FlowError, "invalid JVM offsets"):
            normal_graph(meth([]))

    def test_duplicate_offsets_are_rejected(self):
        with self.assertRaisesRegex(FlowError, "invalid JVM offsets"):
            normal_graph(meth([ins(0,"return"), ins(0,"return")]))

    def test_missing_jump_destination_is_rejected(self):
        with self.assertRaisesRegex(AuditError, "missing branch destination"):
            normal_graph(meth([ins(0,"goto","99"), ins(3,"return")]))

    def test_switch_bytecode_is_rejected(self):
        with self.assertRaisesRegex(FlowError, "switch normal CFG unsupported"):
            normal_graph(meth([ins(0,"tableswitch","{"), ins(3,"return")]))

    def test_unsupported_legacy_subroutine_fails_closed(self):
        with self.assertRaisesRegex(FlowError, "unsupported control transfer"):
            normal_graph(meth([ins(0,"ret","1"),ins(3,"return")]))

    def test_nonterminal_last_instruction_is_rejected(self):
        with self.assertRaisesRegex(FlowError, "unrecognized terminal"):
            normal_graph(meth([ins(0,"aload_0")]))

    def test_native_anchor_mismatch_fails_closed(self):
        with self.assertRaisesRegex(FlowError, "missing/different JVM opcode"):
            assert_native_pins(meth([ins(1044,"return")]))

    def test_outcome_projection_distinguishes_taken_from_fallthrough(self):
        rows = [
            ins(953,"goto","1044"), ins(1044,"ifeq","1157"),
            ins(1088,"ifne","1157"), ins(1119,"invokevirtual","#1"),
            ins(1122,"ifeq","1157"), ins(1154,"invokestatic","#2"),
            ins(1157,"goto","953"),
        ]
        graph,_ = normal_graph(meth(rows))
        result = bounded_projection(graph,rows)
        first = result["conditional_outcome_paths"][0]["outcomes"]
        self.assertFalse(first["branch_taken"]["downstream"]["1119"]
                         ["reachable_in_same_bounded_iteration"])
        self.assertTrue(first["fallthrough"]["downstream"]["1119"]
                        ["reachable_in_same_bounded_iteration"])
        final = result["conditional_outcome_paths"][2]["outcomes"]
        self.assertFalse(final["branch_taken"]["downstream"]["1154"]
                         ["reachable_in_same_bounded_iteration"])
        self.assertTrue(final["fallthrough"]["downstream"]["1154"]
                        ["reachable_in_same_bounded_iteration"])

    def test_snapshots_fail_closed_on_changed_reachability(self):
        real = {"observations":{"head_reachability":{"1119":True}}}
        fake = {"observations":{"head_reachability":{"1119":False}}}
        with self.assertRaisesRegex(FlowError, "normal CFG seal drift"):
            verify_snapshot(real,fake)
        self.assertIs(verify_snapshot(real,real), real)

if __name__ == "__main__":
    unittest.main()
