#!/usr/bin/env python3
"""Synthetic fail-closed regression for read-only Solar Raygun probe."""
from __future__ import annotations

import unittest

from alexscaves_1010_solar_static_probe import bounded, digest, ensure, method_evidence


class SolarReadOnlyTests(unittest.TestCase):
    def setUp(self):
        self.method = {
            "header": "  public void acInventoryTick(net.minecraft.world.item.ItemStack);",
            "descriptor": "()V",
            "instructions": [
                {"offset": 0, "opcode": "aload_0", "operand": "", "symbol": ""},
                {"offset": 1, "opcode": "getstatic", "operand": "#101",
                 "symbol": "Field ACEnchantmentRegistry.SOLAR:ResourceKey;"},
                {"offset": 4, "opcode": "invokestatic", "operand": "#8",
                 "symbol": "Method ACCompat.enchantLevel:(ItemStack,ResourceKey)I"},
                {"offset": 7, "opcode": "ifle", "operand": "15", "symbol": ""},
                {"offset": 15, "opcode": "return", "operand": "", "symbol": ""},
            ],
        }

    def test_digest(self):
        self.assertEqual(
            digest(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_bounded_contains_token_and_branch(self):
        result = bounded(self.method, direct_solar=True)
        self.assertTrue(any("SOLAR" in row["symbol"] for row in result))
        self.assertTrue(any(row["opcode"] == "ifle" for row in result))

    def test_empty_method_fail_closed(self):
        self.method["instructions"] = []
        with self.assertRaisesRegex(ValueError, "method size"):
            bounded(self.method, direct_solar=True)

    def test_oversized_method_fail_closed(self):
        self.method["instructions"] = [
            {"offset": i, "opcode": "nop", "operand": "", "symbol": ""}
            for i in range(1701)]
        with self.assertRaisesRegex(ValueError, "method size"):
            bounded(self.method, direct_solar=True)

    def test_sha_drift_fails(self):
        with self.assertRaisesRegex(ValueError, "previous Raygun method seal mismatch"):
            method_evidence(self.method, {"acInventoryTick ()V": "0" * 64})

    def test_reused_anchor_when_no_prior(self):
        # No arbitrary SHA is treated as authority: evidence records whether
        # a previous independently verified method digest was available.
        out = method_evidence(self.method, {})
        self.assertFalse(out["prior_sha256_matched"])
        self.assertTrue(out["solar_direct_reference"])

    def test_fail_closed_ensure(self):
        with self.assertRaisesRegex(ValueError, "blocked"):
            ensure(False, "blocked")

    def test_large_bounded_window_fail_closed(self):
        self.method["instructions"] = [
            {"offset": i, "opcode": "getstatic", "operand": "#101",
             "symbol": "Field ACEnchantmentRegistry.SOLAR:ResourceKey;"}
            for i in range(500)]
        with self.assertRaisesRegex(ValueError, "Solar discovery window too broad"):
            bounded(self.method, direct_solar=True)


if __name__ == "__main__":
    unittest.main()
