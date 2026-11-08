#!/usr/bin/env python3
"""Synthetic fail-closed regression tests for Soak Seeking exact JAR probe."""
from __future__ import annotations

import unittest
from alexscaves_1010_soak_seeking_static_probe import (
    require, sha256, verify_anchors, choose_instructions,
)


class SoakSeekingStaticProbeTests(unittest.TestCase):
    def setUp(self):
        self.row = {"offset": 314, "opcode": "getstatic", "operand": "#183",
                    "symbol": "Field ACEnchantmentRegistry.SOAK_SEEKING:ResourceKey;"}
        self.method = {"descriptor": "()V", "instructions": [dict(self.row)]}
        self.ref = {"name": "use", "descriptor": "()V",
                    "anchors": [dict(self.row)]}

    def test_sha_primitive(self):
        self.assertEqual(
            sha256(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_exact_anchor_passes(self):
        self.assertEqual(verify_anchors(self.method, self.ref), 1)

    def test_modified_operand_fails(self):
        self.method["instructions"][0]["operand"] = "#184"
        with self.assertRaisesRegex(ValueError, "operand"):
            verify_anchors(self.method, self.ref)

    def test_modified_opcode_fails(self):
        self.method["instructions"][0]["opcode"] = "putstatic"
        with self.assertRaisesRegex(ValueError, "opcode"):
            verify_anchors(self.method, self.ref)

    def test_missing_anchor_fails(self):
        self.method["instructions"][0]["offset"] = 313
        with self.assertRaisesRegex(ValueError, "missing anchor"):
            verify_anchors(self.method, self.ref)

    def test_descriptor_fails(self):
        self.method["descriptor"] = "(I)V"
        with self.assertRaisesRegex(ValueError, "descriptor"):
            verify_anchors(self.method, self.ref)

    def test_missing_reference_fails(self):
        self.ref["anchors"] = []
        with self.assertRaisesRegex(ValueError, "independent anchors"):
            verify_anchors(self.method, self.ref)

    def test_bounded_inspection(self):
        rows = choose_instructions(self.method)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["offset"], 314)

    def test_empty_method_fails(self):
        self.method["instructions"] = []
        with self.assertRaisesRegex(ValueError, "invalid method length"):
            choose_instructions(self.method)

    def test_fail_closed_raises(self):
        with self.assertRaises(ValueError):
            require(False, "blocked")


if __name__ == "__main__":
    unittest.main()
