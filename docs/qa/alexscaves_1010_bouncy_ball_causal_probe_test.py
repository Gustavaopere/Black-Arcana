#!/usr/bin/env python3
"""Fail-closed synthetic coverage for SHA-exact Bouncy Ball causal audit."""
import unittest
from alexscaves_1010_bouncy_ball_causal_probe import (
    branch_edges, pivots, pairs_unique, check_nbt_color_only
)

def instruction(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode,
            "operand": operand, "symbol": symbol}

def method(rows):
    return {"header": "public void test()", "descriptor": "()V",
            "instructions": rows}

class BouncyBallCausalTests(unittest.TestCase):
    def test_direct_edge_and_goto_back_edge(self):
        rows = [instruction(0, "ifeq", "4"), instruction(3, "goto", "0"),
                instruction(4, "return")]
        self.assertEqual(branch_edges(method(rows)),
                         [rows[0], rows[1]])

    def test_branch_target_must_exist(self):
        with self.assertRaisesRegex(ValueError, "branch target"):
            branch_edges(method([instruction(0, "ifeq", "6"),
                                 instruction(3, "return")]))

    def test_switch_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            branch_edges(method([instruction(0, "tableswitch"),
                                 instruction(3, "return")]))

    def test_duplicate_jvm_offset_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "non-canonical"):
            branch_edges(method([instruction(0, "nop"),
                                 instruction(0, "return")]))

    def test_missing_causal_pivot_fails(self):
        with self.assertRaisesRegex(ValueError, "causal offset"):
            pivots(method([instruction(0, "nop")]), ((4, "getBounces"),))

    def test_wrong_causal_pivot_fails(self):
        with self.assertRaisesRegex(ValueError, "causal pivot changed"):
            pivots(method([instruction(4, "iconst_2")]), ((4, "imul"),))

    def test_manifest_duplicate_key_fails(self):
        with self.assertRaisesRegex(ValueError, "duplicate manifest"):
            pairs_unique([("artifact", 1), ("artifact", 2)])

    def test_local_nbt_color_does_not_imply_bounce_persistence(self):
        writer = [instruction(i, "nop") for i in range(9)]
        reader = [instruction(i, "nop") for i in range(9)]
        writer[1] = instruction(1, "ldc_w", symbol="String Color")
        writer[4] = instruction(4, "invokevirtual", symbol="Method putInt:()V")
        reader[1] = instruction(1, "ldc_w", symbol="String Color")
        reader[4] = instruction(4, "invokevirtual", symbol="Method setColor:(I)V")
        result = check_nbt_color_only([
            {"header": "public void addAdditionalSaveData()", "descriptor": "()V",
             "instructions": writer},
            {"header": "public void readAdditionalSaveData()", "descriptor": "()V",
             "instructions": reader},
        ])
        self.assertEqual(len(result), 2)

    def test_nbt_bounces_added_requires_reaudit(self):
        writer = [instruction(i, "nop") for i in range(9)]
        reader = [instruction(i, "nop") for i in range(9)]
        writer[1] = instruction(1, "ldc_w", symbol="String Color")
        writer[3] = instruction(3, "invokevirtual", symbol="Method getBounces:()I")
        writer[4] = instruction(4, "invokevirtual", symbol="Method putInt:()V")
        reader[1] = instruction(1, "ldc_w", symbol="String Color")
        reader[4] = instruction(4, "invokevirtual", symbol="Method setColor:(I)V")
        with self.assertRaisesRegex(ValueError, "handles bounce state"):
            check_nbt_color_only([
                {"header": "public void addAdditionalSaveData()", "descriptor": "()V",
                 "instructions": writer},
                {"header": "public void readAdditionalSaveData()", "descriptor": "()V",
                 "instructions": reader},
            ])

if __name__ == "__main__":
    unittest.main()
