#!/usr/bin/env python3
"""Fail-closed synthetic coverage for Spell Lasting SHA-exact static auditor."""
from __future__ import annotations

import unittest

from alexscaves_1010_spell_lasting_static_probe import (
    ITEM, HEX, relevant_windows, method_report, require, sha,
)


def ins(offset, opcode="nop", operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand,
            "symbol": symbol}


def method(name="use", descriptor="()V", rows=None):
    return {"header": "public void " + name + "();",
            "descriptor": descriptor,
            "instructions": rows if rows is not None else [
                ins(0, "getstatic", "#1", "Field ACEnchantmentRegistry.SPELL_LASTING:ResourceKey;"),
                ins(3, "iconst_1"),
                ins(4, "return")
            ]}


class SpellLastingTests(unittest.TestCase):
    def test_sha(self):
        self.assertEqual(sha(b"abc"),
                         "ba7816bf8f01cfea414140de5dae2223b00361f20015ad")

    def test_owner_window_has_symbol(self):
        windows = relevant_windows(method(), ITEM)
        self.assertTrue(any("SPELL_LASTING" in w["symbol"] for w in windows))

    def test_tick_lifespan_window(self):
        windows = relevant_windows(method("tick", "()V",
                       [ins(0, "invokevirtual", "#1", "Method getLifespan:()I"),
                        ins(3, "putfield", "#2", "Field despawnsIn:I"),
                        ins(6, "return")]), HEX)
        self.assertEqual(2, len(windows))

    def test_no_anchor_makes_no_independent_claim(self):
        result = method_report(method(), ITEM, {"methods": []})
        self.assertEqual(0, result["prior_exact_anchors_verified"])

    def test_anchor_agreement(self):
        m = method()
        baseline = {"methods": [{"name": "use", "descriptor": "()V",
                                 "anchors": [ins(0, "getstatic", "#1",
                                                  "Field ACEnchantmentRegistry.SPELL_LASTING:ResourceKey;")]}]}
        result = method_report(m, ITEM, baseline)
        self.assertEqual(1, result["prior_exact_anchors_verified"])

    def test_changed_operand_fail_closed(self):
        m = method()
        baseline = {"methods": [{"name": "use", "descriptor": "()V",
                                 "anchors": [ins(0, "getstatic", "#2",
                                                  "Field ACEnchantmentRegistry.SPELL_LASTING:ResourceKey;")]}]}
        with self.assertRaisesRegex(ValueError, "exact previous contract anchor mismatch"):
            method_report(m, ITEM, baseline)

    def test_duplicate_baseline_fails(self):
        m = method()
        ref = {"name": "use", "descriptor": "()V", "anchors": []}
        with self.assertRaisesRegex(ValueError, "ambiguous previous JVM"):
            method_report(m, ITEM, {"methods": [ref, ref]})

    def test_unsorted_offsets_fail_closed(self):
        m = method(rows=[ins(5), ins(0)])
        with self.assertRaisesRegex(ValueError, "duplicate/unsorted"):
            relevant_windows(m, HEX)

    def test_empty_method_fails(self):
        with self.assertRaisesRegex(ValueError, "empty or unbounded"):
            relevant_windows(method(rows=[]), ITEM)

    def test_unbounded_method_fails(self):
        with self.assertRaisesRegex(ValueError, "empty or unbounded"):
            relevant_windows(method(rows=[ins(i) for i in range(1801)]), HEX)

    def test_report_budget_fails(self):
        m = method(rows=[ins(i, "getstatic", "#1",
                           "Field ACEnchantmentRegistry.SPELL_LASTING:ResourceKey;")
                         for i in range(250)])
        with self.assertRaisesRegex(ValueError, "clean-room"):
            relevant_windows(m, ITEM)

    def test_require_guard(self):
        with self.assertRaisesRegex(ValueError, "blocked"):
            require(False, "blocked")


if __name__ == "__main__":
    unittest.main()
