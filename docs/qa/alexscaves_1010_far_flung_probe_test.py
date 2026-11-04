#!/usr/bin/env python3
"""Synthetic negative regressions for the Far Flung read-only exact-JAR probe."""
import unittest

from alexscaves_1010_far_flung_probe import (
    HOOK, ITEM, SCOPE, digest, require, selected_methods, validate_consumer
)

def method(name, descriptor, ins):
    return {
        "header": "public void " + name + "();",
        "descriptor": descriptor, "instructions": ins
    }

def i(offset, symbol="", op="invokevirtual"):
    return {"offset": offset, "opcode": op, "operand": "", "symbol": symbol}

class FarFlungProbeTests(unittest.TestCase):
    def test_exact_scope(self):
        self.assertIn("1010", SCOPE)
        self.assertEqual(len(digest(b"abc")), 64)

    def test_missing_consumer_fails_closed(self):
        arr = [i(n*3) for n in range(18)]
        c = selected_methods([method(
            "CandyCaneHookEntity", "(Lnet/minecraft/world/item/ItemStack;)V", arr
        )], HOOK)
        with self.assertRaisesRegex(ValueError, "FAR_FLUNG"):
            validate_consumer(c)

    def test_missing_movement_fails_closed(self):
        arr = [i(n*3) for n in range(18)]
        arr[4] = i(12, "Field ACEnchantmentRegistry.FAR_FLUNG:Lnet/minecraft/resources/ResourceKey;", "getstatic")
        c = selected_methods([method(
            "CandyCaneHookEntity", "(Lnet/minecraft/world/item/ItemStack;)V", arr
        )], HOOK)
        with self.assertRaisesRegex(ValueError, "velocity"):
            validate_consumer(c)

    def test_consumer_with_movement_is_selected(self):
        arr = [i(n*3) for n in range(20)]
        arr[4] = i(12, "Field ACEnchantmentRegistry.FAR_FLUNG:Lnet/minecraft/resources/ResourceKey;", "getstatic")
        arr[12] = i(36, "Method setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V")
        c = selected_methods([method(
            "CandyCaneHookEntity", "(Lnet/minecraft/world/item/ItemStack;)V", arr
        )], HOOK)
        validate_consumer(c)
        self.assertEqual(c[0]["selected_windows"][0]["offset"], 12)

    def test_unsorted_offsets_fail_closed(self):
        arr = [i(0), i(3), i(2)]
        with self.assertRaisesRegex(ValueError, "unsorted"):
            selected_methods([method("use", "()V", arr)], ITEM)

    def test_reject_excessive_method_population(self):
        arr = [i(n) for n in range(2401)]
        with self.assertRaisesRegex(ValueError, "length"):
            selected_methods([method("use", "()V", arr)], ITEM)

    def test_missing_explicit_contract(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            require(False, "negative")

if __name__ == "__main__":
    unittest.main()
