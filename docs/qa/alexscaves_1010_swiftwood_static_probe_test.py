#!/usr/bin/env python3
"""Negative and positive synthetic checks for exact Swiftwood JAR discovery."""
import unittest

from alexscaves_1010_swiftwood_static_probe import (
    CLUB, ENCH, EXPECTED_CLUB_SHA, EXPECTED_REG_SHA, EXPECTED_TAG_SHA,
    require, sha, windows, exact_attribute_contract,
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

    def test_exact_compiled_attribute_formula_and_negative_tampering(self):
        stats = [
            (5, "getstatic", "Attributes.ATTACK_DAMAGE:", ""),
            (15, "ldc2_w", "double 8.0d", ""),
            (18, "getstatic", "Operation.ADD_VALUE:", ""),
            (29, "getstatic", "Attributes.ATTACK_SPEED:", ""),
            (39, "fconst_0", "", ""),
            (40, "ldc", "float -3.75f", ""),
            (42, "ldc", "float 0.15f", ""),
            (44, "iload_1", "", ""),
            (45, "i2f", "", ""),
            (46, "fmul", "", ""),
            (47, "fadd", "", ""),
            (48, "invokestatic", "Math.min:(FF)F", ""),
            (51, "f2d", "", ""),
            (52, "getstatic", "Operation.ADD_VALUE:", ""),
        ]
        selector = [
            (1, "getstatic", "EquipmentSlot.MAINHAND:", ""),
            (4, "if_acmpeq", "", "9"),
            (7, "aconst_null", "", ""),
            (10, "getstatic", "ACEnchantmentRegistry.SWIFTWOOD:", ""),
            (13, "invokestatic", "ACCompat.enchantLevel:", ""),
            (22, "iconst_0", "", ""),
            (23, "iconst_3", "", ""),
            (24, "invokestatic", "Mth.clamp:(III)I", ""),
            (27, "aaload", "", ""),
            (28, "areturn", "", ""),
        ]
        def meth(name, code):
            return {
                "name": name, "method_sha256": "dummy", "instructions_total": len(code),
                "windows": [{"nearby": [
                    {"offset": off, "opcode": op, "symbol": sym, "operand": operand}
                    for off, op, sym, operand in code]}],
            }
        data = {"selected_methods": [
            meth("getStatsForEnchantmentLevel", stats),
            meth("acModifiers", selector),
            meth("getDefaultAttributeModifiers", [
                (0, "invokestatic", "ACCompat.itemAttributes:", "")]),
            meth("lambda$getDefaultAttributeModifiers$0", [
                (0, "areturn", "", "")]),
        ]}
        self.assertEqual([0, 3], exact_attribute_contract(data)["level_index_clamp"])
        data["selected_methods"][0]["windows"][0]["nearby"][6]["symbol"] = "float 0.1f"
        with self.assertRaisesRegex(ValueError, "exact JVM contract mismatch"):
            exact_attribute_contract(data)

    def test_missing_bridge_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing/ambiguous"):
            exact_attribute_contract({"selected_methods": []})

    def test_assertion_rejects_false(self):
        with self.assertRaisesRegex(ValueError, "fail closed"):
            require(False, "fail closed")

    def test_assertion_accepts_true(self):
        self.assertIsNone(require(True, "ok"))


if __name__ == "__main__":
    unittest.main()
