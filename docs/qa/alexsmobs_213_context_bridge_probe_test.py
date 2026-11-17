#!/usr/bin/env python3
"""Deterministic synthetic fail-closed checks, not gameplay or physical QA."""
import copy
import unittest

from alexsmobs_213_context_bridge_probe import (
    bootstrap_candidates, is_direct_implementer, method_projection,
    verify_snapshot,
)
from alexsmobs_213_transmutation_c2s_probe import TransmuteProbeError


def row(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode,
            "operand": operand, "symbol": symbol}


class ContextBridgeTests(unittest.TestCase):
    def test_interface_implementation_requires_direct_declaration(self):
        self.assertTrue(is_direct_implementer(
            "class X implements com.github.alexthe666.alexsmobs.message.AMNetContext {\n}"
        ))
        self.assertFalse(is_direct_implementer(
            "class X {\n  // AMNetContext incidental reference\n}"
        ))

    def test_plain_reference_is_not_implementation(self):
        self.assertFalse(is_direct_implementer(
            "class MessageTransmuteFromMenu$Handler {\n"
            "  void handle(AMNetContext context);\n}"
        ))

    def test_projection_preserves_causal_jvm_offsets_not_full_method(self):
        m = {
            "header": "public void handle();", "descriptor": "()V",
            "instructions": [
                row(0, "aload_0"),
                row(1, "invokeinterface", "#3", "InterfaceMethod AMNetContext.getSender:()V"),
                row(6, "astore_1"),
                row(7, "return"),
            ],
        }
        p = method_projection(m)
        self.assertEqual(p["instruction_count"], 4)
        self.assertEqual(p["relevant_references"][0]["site"]["offset"], 1)
        self.assertEqual(p["relevant_references"][0]["following"]["offset"], 6)

    def test_irrelevant_method_excluded(self):
        self.assertIsNone(method_projection({
            "header": "public void unrelated();", "descriptor": "()V",
            "instructions": [row(0, "return")],
        }))

    def test_get_sender_getter_is_recorded_even_without_calls(self):
        p = method_projection({
            "header": "public net.minecraft.server.level.ServerPlayer getSender();",
            "descriptor": "()Lnet/minecraft/server/level/ServerPlayer;",
            "instructions": [row(0, "aconst_null"), row(1, "areturn")],
        })
        self.assertEqual(p["method"], "getSender")
        self.assertEqual(p["relevant_references"], [])

    def test_bootstrap_is_a_candidate_not_verified_linkage(self):
        sample = (
            "BootstrapMethods:\n"
            "  0: #111 REF_invokeStatic other/Unrelated.run:()V\n"
            "    Method arguments:\n"
            "      #222 ()V\n"
            "  1: #113 REF_invokeStatic owner.lambda$setup$1:()V\n"
            "    Method arguments:\n"
            "      #223 ()V\n"
            "InnerClasses:\n"
        )
        result = bootstrap_candidates(sample)
        self.assertEqual(len(result), 1)
        self.assertIn("lambda$setup$1", result[0][0])

    def test_missing_bootstrap_means_unknown_not_approval(self):
        self.assertEqual(bootstrap_candidates("no bootstrap section"), [])

    def test_sha_exact_snapshot_rejects_changed_observation(self):
        original = {"classes": [], "limitations": {"mutation": "NO_MUTATION"}}
        verify_snapshot(original, copy.deepcopy(original))
        revised = copy.deepcopy(original)
        revised["limitations"]["mutation"] = "ALLOWED"
        with self.assertRaises(TransmuteProbeError):
            verify_snapshot(revised, original)


if __name__ == "__main__":
    unittest.main()
