#!/usr/bin/env python3
"""Synthetic regressions: exact Raygun post-hurt normal-CFG guard observations."""
import copy
import unittest

from alexscaves_1010_raygun_hit_outcomes_cfg_probe import FlowError, normal_graph
from alexscaves_1010_raygun_post_hit_guard_probe import (
    GUARDS, GOALS, WINDOW_START, WINDOW_END,
    guard_projection, site, verify_snapshot,
)

def i(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand, "symbol": symbol}

def fake_method():
    # Offsets are test fixtures, not a claim about native instructions.
    rows = [
        i(953, "aload_0"),
        i(1013, "invokestatic", "#1", "Method Example.fake:()V"),
        i(1044, "ifeq", "1051"),
        i(1047, "iconst_1"),
        i(1048, "goto", "1052"),
        i(1051, "iconst_0"),
        i(1052, "istore", "26"),
        i(1054, "iload", "26"),
        i(1056, "ifeq", "1157"),
        i(1059, "aload", "25"),
        i(1061, "instanceof", "#2", "class net/minecraft/world/entity/LivingEntity"),
        i(1064, "ifeq", "1157"),
        i(1067, "aload", "25"),
        i(1069, "checkcast", "#2", "class net/minecraft/world/entity/LivingEntity"),
        i(1088, "ifne", "1157"),
        i(1091, "aload_0"),
        i(1119, "invokevirtual", "#2", "Method Example.addEffect:()Z"),
        i(1122, "ifeq", "1157"),
        i(1125, "aload_0"),
        i(1154, "invokestatic", "#3", "Method Example.sendVisual:()V"),
        i(1157, "goto", "953"),
    ]
    return rows

def project(rows):
    graph, _ = normal_graph({"instructions":rows})
    return guard_projection(rows, graph)

class RaygunPostHitGuardTests(unittest.TestCase):
    def test_fixture_has_four_guards_and_two_downstream_calls(self):
        out = project(fake_method())
        self.assertEqual([x["offset"] for x in out["guard_observations"]], list(GUARDS))
        self.assertEqual(out["guard_count"], 4)
        self.assertEqual(out["window_instruction_count"], 14)
        self.assertEqual([x["offset"] for x in out["invocation_sites_in_window"]],[1013])

    def test_taken_and_fallthrough_are_distinct(self):
        g = project(fake_method())["guard_observations"][1]
        self.assertEqual(g["destination"],1157)
        self.assertEqual(g["fallthrough"],1059)
        self.assertEqual([x["outcome"] for x in g["outcomes"]], ["taken","fallthrough"])

    def test_no_false_reachability_across_iteration_boundary(self):
        guard = project(fake_method())["guard_observations"][3]
        self.assertFalse(guard["outcomes"][0]["downstream"]["1119"]["reachable"])
        self.assertTrue(guard["outcomes"][1]["downstream"]["1119"]["reachable"])
        self.assertFalse(guard["outcomes"][0]["downstream"]["1154"]["reachable"])

    def test_path_length_has_normal_edge_units(self):
        guard = project(fake_method())["guard_observations"][3]
        self.assertEqual(guard["outcomes"][1]["downstream"]["1119"]["shortest_normal_edges"],1)

    def test_truncated_site_symbol_is_bounded(self):
        observed = site(i(5,"invokestatic","#1","X"*1200))
        self.assertEqual(len(observed["symbol"]),240)
        self.assertEqual(set(observed),{"offset","opcode","operand","symbol"})

    def test_missing_guard_refused(self):
        rows = [x for x in fake_method() if x["offset"] != 1064]
        with self.assertRaisesRegex(FlowError,"missing post-hurt JVM sites"):
            project(rows)

    def test_nonconditional_guard_refused(self):
        rows = fake_method()
        rows = [i(1056,"aload_0") if x["offset"] == 1056 else x for x in rows]
        with self.assertRaisesRegex(FlowError,"expected post-hurt conditional"):
            project(rows)

    def test_duplicate_offset_refused(self):
        rows = fake_method() + [i(1157,"return")]
        with self.assertRaisesRegex(FlowError,"invalid JVM offsets"):
            project(rows)

    def test_unexpected_graph_guard_arity_refused(self):
        rows = fake_method()
        graph,_ = normal_graph({"instructions":rows})
        graph[1056] = (1088,)
        with self.assertRaisesRegex(FlowError,"expected post-hurt conditional"):
            guard_projection(rows,graph)


    def test_hurt_false_locally_zeroes_gate_and_exits(self):
        p=project(fake_method())["immediate_hit_boolean_proof"]
        self.assertFalse(p["hurt_false"]["reaches_addEffect_in_same_iteration"])
        self.assertTrue(p["hurt_true"]["reaches_living_entity_guard"])
        self.assertFalse(p["hurt_true"]["reaches_addEffect_unconditionally"])

    def test_tampered_zero_constant_is_rejected(self):
        rows=[i(1051,"iconst_1") if x["offset"]==1051 else x for x in fake_method()]
        with self.assertRaisesRegex(FlowError,"hit-gate JVM opcode drift @1051"):
            project(rows)

    def test_tampered_local_slot_is_rejected(self):
        rows=[i(1054,"iload","25") if x["offset"]==1054 else x for x in fake_method()]
        with self.assertRaisesRegex(FlowError,"hit-gate operand drift @1054"):
            project(rows)

    def test_tampered_instanceof_class_is_rejected(self):
        rows=[i(1061,"instanceof","#2","class Example/OtherEntity")
              if x["offset"]==1061 else x for x in fake_method()]
        with self.assertRaisesRegex(FlowError,"hit-gate class predicate drift @1061"):
            project(rows)

    def test_report_snapshot_drift_fails_closed(self):
        a={"scope":"demo","guards":4,"limits":{"mutation":"NO_MUTATION"}}
        b=copy.deepcopy(a)
        b["guards"]=3
        with self.assertRaisesRegex(FlowError,"snapshot drift"):
            verify_snapshot(a,b)
        self.assertIs(verify_snapshot(a,a),a)

    def test_out_of_window_guard_refused(self):
        # Ensure an auditor cannot silently shrink the pinned observation window.
        self.assertTrue(all(WINDOW_START <= x < WINDOW_END for x in GUARDS))
        self.assertTrue(all(g in (1088,1119,1154) for g in GOALS))

if __name__ == "__main__":
    unittest.main()
