#!/usr/bin/env python3
"""Negative and positive synthetic checks for exact Swiftwood JAR discovery."""
import unittest

from alexscaves_1010_swiftwood_static_probe import (
    CLUB, ENCH, EXPECTED_CLUB_SHA, EXPECTED_REG_SHA, EXPECTED_TAG_SHA,
    require, sha, windows,
)


def row(off, symbol="", op="nop"):
    return {"offset": off, "symbol": symbol, "opcode": op, "operand": ""}


class SwiftwoodStaticProbeTests(unittest.TestCase):
    def test_sha256(self):
        self.assertEqual(sha(b"abc"),
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_known_physical_class_and_tag_digest_shape(self):
        for value in (EXPECTED_CLUB_SHA, EXPECTED_REG_SHA, EXPECTED_TAG_SHA):
            self.assertEqual(64, len(value))
            self.assertTrue(all(ch in "0123456789abcdef" for ch in value))

    def test_identity(self):
        self.assertTrue(CLUB.endswith("/PrimitiveClubItem.class"))
        self.assertEqual("data/alexscaves/enchantment/swiftwood.json", ENCH)

    def test_exact_marker_window(self):
        rows = [row(0), row(3, "Field SWIFTWOOD:"), row(6)]
        win = windows(rows, "SWIFTWOOD")
        self.assertEqual(1, len(win))
        self.assertEqual(3, win[0]["offset"])
        self.assertEqual(3, len(win[0]["nearby"]))

    def test_no_pivot_is_not_proof(self):
        self.assertEqual([], windows([row(0), row(3)], "SWIFTWOOD"))

    def test_many_hits_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unbounded token census"):
            windows([row(i, "SWIFTWOOD") for i in range(49)], "SWIFTWOOD")

    def test_window_cap_two(self):
        out = windows([row(i, "SWIFTWOOD") for i in range(5)], "SWIFTWOOD")
        self.assertEqual(2, len(out))
        self.assertEqual(5, out[0]["matches"])

    def test_assertion_rejects_false(self):
        with self.assertRaisesRegex(ValueError, "fail closed"):
            require(False, "fail closed")

    def test_assertion_accepts_true(self):
        self.assertIsNone(require(True, "ok"))


if __name__ == "__main__":
    unittest.main()
