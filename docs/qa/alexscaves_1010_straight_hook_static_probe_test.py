#!/usr/bin/env python3
"""Synthetic fail-closed tests for the exact Straight Hook discovery probe."""
import unittest

from alexscaves_1010_straight_hook_static_probe import (
    HOOK, ITEM, HOOK_SHA, ITEM_SHA, TAG_SHA, window, require, digest,
)


def ins(offset: int, symbol: str = "", opcode: str = "nop") -> dict:
    return {"offset": offset, "opcode": opcode, "operand": "", "symbol": symbol}


def method(rows: list[dict]) -> dict:
    return {"instructions": rows}


class TestStraightHookProbe(unittest.TestCase):
    def test_identity_constants_are_sha256(self):
        for value in (HOOK_SHA, ITEM_SHA, TAG_SHA):
            self.assertEqual(len(value), 64)
            self.assertTrue(all(ch in "0123456789abcdef" for ch in value))

    def test_distinct_hook_and_item(self):
        self.assertNotEqual(HOOK, ITEM)

    def test_hash_is_real_sha256(self):
        self.assertEqual(digest(b"abc"),
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_straight_enchantment_pivot(self):
        result = window(method([ins(0), ins(3, "Field STRAIGHT_HOOK:"), ins(6)]),
                        "STRAIGHT_HOOK")
        self.assertEqual(1, len(result))
        self.assertEqual(3, result[0]["offset"])

    def test_gravity_state_pivot(self):
        result = window(method([ins(0), ins(3, "Field RESISTS_GRAVITY:"),
                                ins(6, "Method setNoGravity:")]), "RESISTS_GRAVITY")
        self.assertEqual([3], [row["offset"] for row in result])

    def test_no_pivot_is_not_fake_evidence(self):
        self.assertEqual([], window(method([ins(1), ins(2)]), "STRAIGHT_HOOK"))

    def test_evidence_is_bounded(self):
        entries = [ins(i, "STRAIGHT_HOOK") for i in range(60)]
        with self.assertRaisesRegex(ValueError, "unbounded JVM pivot"):
            window(method(entries), "STRAIGHT_HOOK")

    def test_require_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "test failure"):
            require(False, "test failure")

    def test_true_require_is_noop(self):
        self.assertIsNone(require(True, "should not fail"))


if __name__ == "__main__":
    unittest.main()
