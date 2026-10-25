#!/usr/bin/env python3
"""Synthetic normal-CFG tests. No copied provider code or gameplay claims."""
import copy
import unittest
import winds_105_aeropic_recast_cfg as cfg

def row(offset, opcode, symbol=None, target=None):
    r = {"offset": offset, "opcode": opcode}
    if symbol is not None:
        r["symbol"] = symbol
    if target is not None:
        r.update(branch=True, branch_target=target)
    return r

SIMPLE = [
    row(0, "getstatic", cfg.SOURCE),
    row(3, "invokeinterface", cfg.parser.SUPPLIER_GET),
    row(8, "checkcast", cfg.parser.ABSTRACT_SPELL),
    row(11, "iload_2"), row(12, "aload_1"),
    row(13, "invokevirtual", cfg.RECAST),
    row(16, "ireturn"),
]

class CFGTopologyTests(unittest.TestCase):
    def test_linear_source_dominates(self):
        result = cfg.classify(copy.deepcopy(SIMPLE), "onEffectAdded")
        self.assertEqual(1, result["supplier_field_reads_dominating_recast"])
        self.assertEqual(0, result["conditional_and_direct_jump_count"])
        self.assertEqual("BOUNDED_NORMAL_CFG_TOPOLOGY_ONLY", result["cfg_evidence_grade"])
        self.assertEqual("NOT_PROVEN_BY_CFG_TOPOLOGY", result["compiled_receiver_source"])

    def test_branch_join_dominating_source(self):
        rows = [row(0, "getstatic", cfg.SOURCE), row(3, "ifeq", target=8),
                row(6, "aload_0"), row(8, "iload_2"), row(10, "aload_1"),
                row(11, "invokevirtual", cfg.RECAST), row(14, "ireturn")]
        result = cfg.classify(rows, "applyEffectTick")
        self.assertEqual(1, result["supplier_field_reads_dominating_recast"])
        self.assertEqual(1, result["normal_route_join_instruction_count"])

    def test_optional_source_does_not_dominate(self):
        rows = [row(0, "ifeq", target=6), row(3, "getstatic", cfg.SOURCE),
                row(6, "iload_2"), row(8, "aload_1"),
                row(9, "invokevirtual", cfg.RECAST), row(12, "ireturn")]
        result = cfg.classify(rows, "applyEffectTick")
        self.assertEqual(0, result["supplier_field_reads_dominating_recast"])
        self.assertEqual(1, result["supplier_field_reads_on_some_normal_route"])

    def test_unreachable_source_not_counted_as_route(self):
        rows = [row(0, "goto", target=8), row(3, "getstatic", cfg.SOURCE),
                row(6, "return"), row(8, "iload_2"), row(10, "aload_1"),
                row(11, "invokevirtual", cfg.RECAST), row(14, "ireturn")]
        result = cfg.classify(rows, "applyEffectTick")
        self.assertEqual(0, result["supplier_field_reads_on_some_normal_route"])

    def test_unreachable_target_not_proven(self):
        rows = [row(0, "return"), row(3, "getstatic", cfg.SOURCE),
                row(6, "iload_2"), row(7, "aload_1"),
                row(8, "invokevirtual", cfg.RECAST), row(11, "ireturn")]
        r = cfg.classify(rows, "applyEffectTick")
        self.assertFalse(r["recast_reachable_on_normal_cfg"])
        self.assertEqual(0, r["supplier_field_reads_dominating_recast"])

    def test_exception_table_closes_dominator_claim(self):
        r = cfg.classify(SIMPLE, "onEffectAdded", exception_table=True)
        self.assertIsNone(r["supplier_field_reads_dominating_recast"])
        self.assertIn("UNMODELED_EXCEPTION_HANDLER_EDGES", r["non_proof_reasons"])

    def test_bad_target_fails_closed(self):
        rows = [row(0, "getstatic", cfg.SOURCE), row(3, "ifeq", target=99),
                row(6, "invokevirtual", cfg.RECAST), row(9, "ireturn")]
        r = cfg.classify(rows, "applyEffectTick")
        self.assertIsNone(r["supplier_field_reads_dominating_recast"])
        self.assertIn("UNRESOLVED_OR_INVALID_JUMP_TARGET", r["non_proof_reasons"])

    def test_switch_fails_closed(self):
        rows = [row(0, "tableswitch"), row(3, "getstatic", cfg.SOURCE),
                row(6, "invokevirtual", cfg.RECAST), row(9, "ireturn")]
        r = cfg.classify(rows, "applyEffectTick")
        self.assertEqual("FAIL_CLOSED_INCOMPLETE_CFG", r["cfg_evidence_grade"])

    def test_wrong_source_symbol_not_counted(self):
        rows = copy.deepcopy(SIMPLE)
        rows[0]["symbol"] = "provider/ModSpellRegistry.OTHER:Ljava/util/function/Supplier;"
        r = cfg.classify(rows, "onEffectAdded")
        self.assertEqual(0, r["supplier_field_reads_dominating_recast"])

    def test_duplicate_invoke_fails_closed(self):
        rows = copy.deepcopy(SIMPLE)
        rows.insert(-1, row(15, "invokevirtual", cfg.RECAST))
        with self.assertRaisesRegex(cfg.ControlFlowError, "population"):
            cfg.classify(rows, "onEffectAdded")

    def test_changed_invoke_opcode_fails_closed(self):
        rows = copy.deepcopy(SIMPLE)
        rows[-2]["opcode"] = "invokestatic"
        with self.assertRaisesRegex(cfg.ControlFlowError, "population"):
            cfg.classify(rows, "onEffectAdded")

    def test_duplicate_offsets_fails_closed(self):
        rows = copy.deepcopy(SIMPLE)
        rows[-1]["offset"] = 13
        with self.assertRaisesRegex(cfg.ControlFlowError, "offsets"):
            cfg.classify(rows, "onEffectAdded")

    def test_cyclic_graph_fixed_point(self):
        rows = [row(0, "getstatic", cfg.SOURCE), row(3, "ifeq", target=10),
                row(6, "goto", target=3), row(10, "iload_2"),
                row(12, "aload_1"), row(13, "invokevirtual", cfg.RECAST),
                row(16, "ireturn")]
        self.assertEqual(1, cfg.classify(rows, "applyEffectTick")["supplier_field_reads_dominating_recast"])

    def test_nonterminal_last_instruction_fails_closed(self):
        r = cfg.classify(SIMPLE[:-1], "onEffectAdded")
        self.assertEqual("FAIL_CLOSED_INCOMPLETE_CFG", r["cfg_evidence_grade"])

    def test_safe_hook_and_dispatch_always_not_proven(self):
        r = cfg.classify(SIMPLE, "onEffectAdded")
        self.assertEqual("NOT_PROVEN", r["safe_mutating_hook"])
        self.assertEqual("NOT_PROVEN", r["return_value_to_PlayerRecasts"])
        self.assertEqual("NOT_PROVEN", r["dynamic_override_executed"])

if __name__ == "__main__":
    unittest.main()
