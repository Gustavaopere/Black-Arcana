#!/usr/bin/env python3
"""Synthetic bounds for the SHA-exact Gumball producer reference probe."""
import unittest
from alexscaves_1010_gumball_producer_probe import (
    MAX_HITS_PER_METHOD, ProducerProbeError, method_row, REF_PATTERN
)


def fake_method(symbols):
    return {
        "header": "public void fire()",
        "descriptor": "()V",
        "instructions": [
            {"offset": 3 * i, "opcode": "invokestatic", "operand": "#1", "symbol": symbol}
            for i, symbol in enumerate(symbols)
        ],
    }


class ProducerProbeTest(unittest.TestCase):
    def test_exact_gumball_reference_names(self):
        self.assertTrue(REF_PATTERN.search(
            "Method com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.<init>:()V"))
        self.assertTrue(REF_PATTERN.search(
            "Field com/github/alexmodguy/alexscaves/server/entity/ACEntityRegistry.GUMBALL:Ljava/util/function/Supplier;"))
        self.assertFalse(REF_PATTERN.search("Method java/lang/Math.random:()D"))

    def test_misses_unrelated_method(self):
        self.assertIsNone(method_row(fake_method(["Method java/lang/Math.random:()D"])))

    def test_selected_window_remains_bounded(self):
        m = fake_method([
            "Method java/lang/Math.random:()D",
            "Method com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.setDamage:(F)V",
            "Method java/lang/Math.random:()D",
        ])
        row = method_row(m)
        self.assertEqual(row["name"], "fire")
        self.assertEqual(len(row["reference_windows"]), 1)
        self.assertEqual(row["reference_windows"][0]["at"], 3)
        self.assertEqual(row["effective_parameter_flow"], "NOT_PROVEN")

    def test_excessive_callsites_fail_closed(self):
        m = fake_method(["Method GumballEntity.setDamage:(F)V"] * (MAX_HITS_PER_METHOD + 1))
        with self.assertRaisesRegex(ProducerProbeError, "selected callsite count exceeded"):
            method_row(m)

    def test_excessive_method_body_fails_closed(self):
        m = fake_method(["Method java/lang/Math.random:()D"] * 3200 +
                        ["Method GumballEntity.<init>:()V"])
        with self.assertRaisesRegex(ProducerProbeError, "unsafe selected method instruction population"):
            method_row(m)


if __name__ == "__main__":
    unittest.main()
