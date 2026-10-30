#!/usr/bin/env python3
"""Parser/provenance fail-closed regression tests with synthetic bytecode."""
import unittest
from alexscaves_1010_damage_helper_probe import (
    EvidenceMismatch, select_method, summarize_method, strict_pairs
)

def m(name="hurt", desc="(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z"):
    return {
        "header": "public static boolean " + name + "(net.minecraft.world.entity.Entity, net.minecraft.world.damagesource.DamageSource, float)",
        "descriptor": desc,
        "instructions": [
            {"offset": 0, "opcode": "fload_2", "operand": "", "symbol": ""},
            {"offset": 1, "opcode": "ldc", "operand": "#12", "symbol": "float 0.65f"},
            {"offset": 3, "opcode": "fmul", "operand": "", "symbol": ""},
            {"offset": 4, "opcode": "ifgt", "operand": "10", "symbol": ""},
            {"offset": 7, "opcode": "iconst_0", "operand": "", "symbol": ""},
            {"offset": 8, "opcode": "ireturn", "operand": "", "symbol": ""},
            {"offset": 10, "opcode": "invokestatic", "operand": "#7",
             "symbol": "Method ACCompat.hurt:(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z"},
            {"offset": 13, "opcode": "ireturn", "operand": "", "symbol": ""}
        ],
    }

DESC="(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z"

class HelpersProbeTests(unittest.TestCase):
    def test_exact_descriptor(self):
        self.assertEqual(select_method([m()], "hurt", DESC)["descriptor"], DESC)

    def test_wrong_descriptor_rejected(self):
        with self.assertRaisesRegex(EvidenceMismatch, "missing/ambiguous"):
            select_method([m()], "hurt", "()V")

    def test_multiple_matching_methods_rejected(self):
        with self.assertRaisesRegex(EvidenceMismatch, "missing/ambiguous"):
            select_method([m(), m()], "hurt", DESC)

    def test_duplicate_bytecode_offsets_rejected(self):
        bad = m()
        bad["instructions"].append(bad["instructions"][0])
        with self.assertRaisesRegex(EvidenceMismatch, "duplicate bytecode"):
            select_method([bad], "hurt", DESC)

    def test_numeric_and_arithmetic_are_observed_not_inferred(self):
        observed = summarize_method(m())
        self.assertEqual(observed["numeric_constants"][0]["symbol"], "float 0.65f")
        self.assertEqual(observed["arithmetic_opcodes"][0]["opcode"], "fmul")
        self.assertEqual(observed["branch_opcodes"][0]["simple_target"], 10)
        self.assertEqual(observed["semantics_and_effective_values"], "NOT_CERTIFIED")

    def test_return_windows_are_bounded(self):
        result = summarize_method(m())
        self.assertEqual(len(result["return_windows"]), 2)
        self.assertEqual(result["return_windows"][0]["offset"], 8)
        self.assertLessEqual(len(result["return_windows"][1]["local_instruction_window"]), 13)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(EvidenceMismatch, "duplicate JSON"):
            strict_pairs([("a", 1), ("a", 2)])

if __name__ == "__main__":
    unittest.main()
