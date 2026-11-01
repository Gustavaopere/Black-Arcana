#!/usr/bin/env python3
"""Synthetic negative controls for SHA-exact Raygun class audit."""
import unittest

from alexscaves_1010_raygun_control_probe import (
    CLASS, CLASS_SHA256, FACTORY_OFFSET, RaygunProbeError,
    is_focus, selected_report, validate_impact_method
)


def instr(offset, opcode, symbol=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol, "operand": ""}


def method(name, instructions, descriptor="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"):
    return {"header": "public void " + name + "()", "descriptor": descriptor,
            "instructions": instructions}


class RaygunControlProbeTest(unittest.TestCase):
    def impact(self):
        return method("onUseTick", [
            instr(0, "aload_0"),
            instr(FACTORY_OFFSET, "invokestatic",
                  "Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.causeRaygunDamage:(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;"),
            instr(1030, "return")
        ])

    def test_sha_exact_class_identifiers_are_pinned(self):
        self.assertTrue(CLASS.endswith("/RaygunItem.class"))
        self.assertEqual(len(CLASS_SHA256), 64)

    def test_expected_callsite_is_recovered(self):
        info = validate_impact_method(self.impact())
        self.assertEqual(info["offset"], FACTORY_OFFSET)
        self.assertEqual(info["opcode"], "invokestatic")

    def test_missing_or_wrong_offset_rejected(self):
        bad = self.impact()
        bad["instructions"][1]["offset"] = 1025
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_wrong_factory_rejected(self):
        bad = self.impact()
        bad["instructions"][1]["symbol"] = "Method causeNukeDamage:()V"
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_client_or_virtual_call_not_mistaken_for_factory(self):
        bad = self.impact()
        bad["instructions"][1]["opcode"] = "invokevirtual"
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_duplicate_on_use_tick_fails_closed(self):
        with self.assertRaisesRegex(RaygunProbeError, "duplicate declared"):
            selected_report([self.impact(), self.impact()])

    def test_bounded_report_contains_selected_window(self):
        res = selected_report([self.impact(), method("other", [instr(0, "return")])])
        self.assertEqual(res["method_count"], 1)
        self.assertEqual(res["selected_methods"][0]["selected_windows"][0]["at"], FACTORY_OFFSET)
        self.assertTrue(is_focus(self.impact()))
        self.assertFalse(is_focus(method("unrelated", [instr(0, "return")])))

    def test_no_impact_method_fails_closed(self):
        with self.assertRaisesRegex(RaygunProbeError, "one exact"):
            selected_report([method("use", [instr(0, "return")])])

    def test_bad_descriptor_is_rejected(self):
        bad = self.impact()
        bad["descriptor"] = "()I"
        with self.assertRaisesRegex(RaygunProbeError, "unexpected"):
            validate_impact_method(bad)


if __name__ == "__main__":
    unittest.main()
