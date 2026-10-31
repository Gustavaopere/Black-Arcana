#!/usr/bin/env python3
"""Fail-closed bounded Gumball state-probe synthetic regressions."""
import unittest
from alexscaves_1010_gumball_state_probe import (
    GumballStateProbeError, classify, name_of, summarize
)


def fake(name, instructions):
    return {
        "header": "public void " + name + "()",
        "descriptor": "()V",
        "instructions": instructions,
    }


def inst(offset, opcode, symbol="", operand=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol,
            "operand": operand}


class GumballStateProbeTests(unittest.TestCase):
    def test_method_name_preserves_overloads(self):
        m = fake("onHitEntity", [inst(0, "return")])
        self.assertEqual(name_of(m), "onHitEntity")
        self.assertEqual(m["descriptor"], "()V")

    def test_correct_anchor_types_and_windows(self):
        m = fake("shootGumball", [
            inst(0, "aload_0"),
            inst(1, "getfield", "Field value:F", "#1"),
            inst(4, "iconst_2"),
            inst(5, "ifeq", "", "12"),
            inst(8, "invokevirtual", "Method setDamage:(F)V", "#3"),
            inst(11, "return"),
        ])
        r = summarize(m, [4, 8])
        self.assertEqual([v["offset"] for v in r["numeric_constants"]], [4])
        self.assertEqual([v["offset"] for v in r["branches"]], [5])
        self.assertEqual([v["offset"] for v in r["symbolic_references"]], [1, 8])
        self.assertEqual([v["at"] for v in r["selected_windows"]], [4, 8])
        self.assertEqual(r["runtime_reachability"], "NOT_PROVEN")

    def test_missing_exact_offset_is_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError, "missing fixed"):
            summarize(fake("tick", [inst(0, "return")]), [42])

    def test_duplicate_instruction_offsets_are_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate bytecode"):
            summarize(fake("tick", [inst(1, "aload_0"), inst(1, "return")]), [])

    def test_maximum_window_budget_is_enforced(self):
        with self.assertRaisesRegex(GumballStateProbeError, "too many evidence windows"):
            summarize(fake("tick", [inst(0, "return")]), [0]*21)

    def test_classification_does_not_report_all_bytecode(self):
        self.assertIsNone(classify(inst(0, "aload_0")))
        self.assertEqual(classify(inst(0, "invokestatic")), "symbols")
        self.assertEqual(classify(inst(0, "ifne")), "branches")


if __name__ == "__main__":
    unittest.main()
