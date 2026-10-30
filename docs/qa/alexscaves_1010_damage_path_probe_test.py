#!/usr/bin/env python3
"""Synthetic bounded probe regressions; exact JAR checks run separately in CI."""
import unittest
from alexscaves_1010_damage_path_probe import (
    ProbeError, branch_anchors, risk_calls, select_context, strict_pairs
)

M = {
    "header": "public void tick()",
    "descriptor": "()V",
    "instructions": [
        {"offset": 0, "opcode": "aload_0", "operand": "", "symbol": ""},
        {"offset": 1, "opcode": "ifnonnull", "operand": "30", "symbol": ""},
        {"offset": 4, "opcode": "invokestatic", "operand": "#1",
         "symbol": "Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.causeNukeDamage:(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;"},
        {"offset": 7, "opcode": "invokevirtual", "operand": "#2",
         "symbol": "Method net/minecraft/world/entity/LivingEntity.hurt:(Lnet/minecraft/world/damagesource/DamageSource;F)Z"},
        {"offset": 10, "opcode": "return", "operand": "", "symbol": ""}
    ]
}
S = {
    "bytecode_offset": 4, "opcode": "invokestatic", "factory_name": "causeNukeDamage",
    "factory_descriptor": "(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;"
}

class PathAnchorsTest(unittest.TestCase):
    def test_window_and_branch_are_literal(self):
        observed = select_context(M, [S])
        self.assertEqual(observed["parsed_instruction_count"], 5)
        self.assertEqual(observed["factory_windows"][0]["invocation_offset"], 4)
        self.assertEqual(observed["branch_opcode_anchors"],
                         [{"offset": 1, "opcode": "ifnonnull",
                           "operand": "30", "simple_target": 30}])
        self.assertEqual(observed["method_semantics"], "NOT_PROVEN_FROM_ANCHORS")
        self.assertEqual(len(observed["selected_symbolic_invocations"]), 2)

    def test_wrong_factory_fails_closed(self):
        with self.assertRaisesRegex(ProbeError, "target drift"):
            select_context(M, [{**S, "factory_name": "causeAcidDamage"}])

    def test_wrong_offset_fails_closed(self):
        with self.assertRaisesRegex(ProbeError, "missing pinned"):
            select_context(M, [{**S, "bytecode_offset": 15}])

    def test_duplicate_offsets_fail_closed(self):
        with self.assertRaisesRegex(ProbeError, "duplicate bytecode offset"):
            select_context({**M, "instructions": M["instructions"] * 2}, [S])

    def test_duplicate_json_keys_fail_closed(self):
        with self.assertRaisesRegex(ProbeError, "duplicate JSON key"):
            strict_pairs([("scope", "a"), ("scope", "b")])

    def test_no_branch_is_deduced_from_invocations(self):
        self.assertEqual(branch_anchors(M["instructions"])[0]["simple_target"], 30)
        self.assertIn("hurt", risk_calls(M["instructions"])[-1]["symbol"])

if __name__ == "__main__":
    unittest.main()
