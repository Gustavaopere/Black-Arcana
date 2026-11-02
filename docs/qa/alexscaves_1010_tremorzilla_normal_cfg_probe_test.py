#!/usr/bin/env python3
"""Synthetic normal-JVM control-flow and guard dominator regressions."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from alexscaves_1010_tremorzilla_normal_cfg_probe import (
    NormalCFGError, normal_edges, traverse, dominators,
    analyze_method, verify_sealed_snapshot
)


def op(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand, "symbol": symbol}


def simple(*instructions):
    return list(instructions)


def mk_method(name, instructions):
    return {"header": "public boolean " + name + "();",
            "descriptor": "()Z", "instructions": instructions}


def block_method():
    return mk_method("breakBlocksAround", [
        op(0, "aload_0"),
        op(12, "invokestatic", symbol="Method ACPlatform.canEntityGrief:()Z"),
        op(15, "ifeq", "352"),
        op(22, "invokevirtual", symbol="Method Level.isClientSide:()Z"),
        op(25, "ifne", "352"),
        op(249, "invokevirtual", symbol="Method Level.destroyBlock:()Z"),
        op(268, "invokestatic", symbol="Method ACCompat.onBlockExploded:()V"),
        op(296, "invokestatic", symbol="Method ACCompat.createEntity:()LEntity;"),
        op(349, "invokevirtual", symbol="Method Level.addFreshEntity:()Z"),
        op(352, "ireturn"),
    ])


class NormalCFGTests(unittest.TestCase):

    def seal_fixture(self):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-TREMORZILLA-NORMAL-CFG-1.0.10.json")
        exact = json.loads(path.read_text(encoding="utf-8"))
        return copy.deepcopy(exact), exact

    def test_positive_exact_sealed_normal_cfg(self):
        report, seal = self.seal_fixture()
        self.assertTrue(verify_sealed_snapshot(report, seal))

    def test_wrong_dominator_result_rejected(self):
        report, seal = self.seal_fixture()
        report["methods"][0]["sites"][0]["guards"][0]["dominates_normal_paths"] = False
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_false_raycast_assumption_rejected(self):
        report, seal = self.seal_fixture()
        report["methods"][1]["sites"][1]["guards"][1]["dominates_normal_paths"] = True
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_wrong_edge_count_rejected(self):
        report, seal = self.seal_fixture()
        report["methods"][0]["normal_edge_count"] += 1
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_wrong_method_sha_rejected(self):
        report, seal = self.seal_fixture()
        report["methods"][0]["method_sha256"] = "0" * 64
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_false_pvp_world_policy_claim_rejected(self):
        report, seal = self.seal_fixture()
        report["limits"]["claims_and_world_protection"] = "VERIFIED"
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_false_physical_QA_rejected(self):
        report, seal = self.seal_fixture()
        report["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(NormalCFGError, "drift"):
            verify_sealed_snapshot(report, seal)

    def test_positive_conditional_edges_and_exit(self):
        graph = normal_edges(simple(op(0, "iconst_0"), op(1, "ifeq", "5"),
                                    op(4, "return"), op(5, "return")))
        self.assertEqual(graph[1], [4, 5])
        self.assertEqual(graph[4], [])

    def test_dominator_with_guard(self):
        graph = normal_edges(simple(op(0, "iconst_0"), op(1, "ifeq", "5"),
                                    op(4, "return"), op(5, "return")))
        self.assertIn(0, dominators(graph, 0)[5])
        self.assertIn(1, dominators(graph, 0)[5])

    def test_bypass_path_disproves_guard_dominance(self):
        graph = normal_edges(simple(op(0, "ifeq", "8"),
                                    op(3, "invokestatic"),
                                    op(5, "goto", "8"),
                                    op(8, "return")))
        self.assertNotIn(3, dominators(graph, 0)[8])
        self.assertIn(8, traverse(graph, 0, forbidden=3))

    def test_loop_backedge_converges(self):
        graph = normal_edges(simple(op(0, "iconst_0"), op(1, "ifeq", "9"),
                                    op(4, "goto", "1"), op(9, "return")))
        self.assertIn(1, dominators(graph, 0)[9])
        self.assertEqual(traverse(graph, 0), {0, 1, 4, 9})

    def test_duplicate_offsets_rejected(self):
        with self.assertRaisesRegex(NormalCFGError, "unordered/duplicate"):
            normal_edges(simple(op(0, "iconst_0"), op(0, "return")))

    def test_unordered_offsets_rejected(self):
        with self.assertRaisesRegex(NormalCFGError, "unordered/duplicate"):
            normal_edges(simple(op(1, "iconst_0"), op(0, "return")))

    def test_unresolved_goto_fails_closed(self):
        with self.assertRaisesRegex(NormalCFGError, "missing branch target"):
            normal_edges(simple(op(0, "goto", "100"), op(3, "return")))

    def test_dynamic_switch_fails_closed(self):
        with self.assertRaisesRegex(NormalCFGError, "unparsed JVM transfer"):
            normal_edges(simple(op(0, "tableswitch", "{"), op(25, "return")))

    def test_jsr_or_ret_fails_closed(self):
        for instr in ("ret", "jsr", "wide"):
            with self.subTest(instr=instr):
                with self.assertRaisesRegex(NormalCFGError, "unparsed JVM transfer"):
                    normal_edges(simple(op(0, instr, "5"), op(5, "return")))

    def test_non_numeric_target_fails_closed(self):
        with self.assertRaisesRegex(NormalCFGError, "non-numeric JVM branch"):
            normal_edges(simple(op(0, "ifne", "#xxx"), op(3, "return")))

    def test_no_implicit_fallthrough_from_method_end(self):
        with self.assertRaisesRegex(NormalCFGError, "unterminated method CFG"):
            normal_edges(simple(op(0, "aload_0")))

    def test_unreachable_vertex_excluded(self):
        graph = normal_edges(simple(op(0, "goto", "8"), op(3, "return"),
                                    op(8, "return")))
        self.assertNotIn(3, dominators(graph, 0))

    def test_positive_exact_anchor_matrix_synthetic(self):
        m = block_method()
        result = analyze_method(m)
        self.assertEqual(len(result["sites"]), 4)
        self.assertTrue(all(g["dominates_normal_paths"]
                            for site in result["sites"] for g in site["guards"]))
        self.assertEqual(result["name"], "breakBlocksAround")

    def test_bypass_world_mutation_is_reported_not_hidden(self):
        m = block_method()
        m["instructions"][0] = op(0, "ifeq", "249")
        result = analyze_method(m)
        destroy = result["sites"][0]
        self.assertTrue(destroy["guards"][0]["bypass_normal_path_exists"])
        self.assertFalse(destroy["guards"][0]["dominates_normal_paths"])

    def test_missing_guard_callsite_fails_closed(self):
        m = block_method()
        m["instructions"][1]["symbol"] = "Method Wrong.check:()Z"
        with self.assertRaisesRegex(NormalCFGError, "callsite drift"):
            analyze_method(m)

    def test_missing_mutation_site_fails_closed(self):
        m = block_method()
        m["instructions"][5]["symbol"] = "Method unrelated:()V"
        with self.assertRaisesRegex(NormalCFGError, "callsite drift"):
            analyze_method(m)

    def test_missing_reachable_site_fails_closed(self):
        m = block_method()
        m["instructions"][4] = op(25, "goto", "352")
        with self.assertRaisesRegex(NormalCFGError, "unreachable"):
            analyze_method(m)


if __name__ == "__main__":
    unittest.main()
