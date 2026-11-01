#!/usr/bin/env python3
"""Fail-closed synthetic tests; no claims about server NBT validation."""
from __future__ import annotations

import copy
import unittest
from unittest.mock import patch
from alexscaves_1010_raygun_itemstack_helper_probe import (
    HELPER, READ, WRITE, TARGETS, HelperProbeError, selected_abi, audit
)


def row(offset, opcode, symbol="", operand="#1"):
    return {"offset": offset, "opcode": opcode,
            "symbol": symbol, "operand": operand}


def method(name="readItemStack", desc=READ, instructions=None):
    if instructions is None:
        instructions = [row(0, "aload_0"), row(1, "invokevirtual",
             "Method FriendlyByteBuf.readVarInt:()I"), row(4, "ifne", "", "12"),
             row(7, "invokestatic", "Method ItemStack.EMPTY:()LItemStack;"),
             row(12, "areturn")]
    return {"header": "public static ItemStack " + name + "()",
            "descriptor": desc, "instructions": instructions}


class NativeHelperProbeTests(unittest.TestCase):
    def test_exact_target_roster(self):
        self.assertEqual(len(TARGETS), 2)
        self.assertEqual(TARGETS, (("readItemStack", READ), ("writeItemStack", WRITE)))
        self.assertTrue(HELPER.endswith("citadel/server/message/PacketBufferUtils.class"))

    def test_selected_symbols_and_branches_only(self):
        m = selected_abi(method())
        self.assertEqual([x["offset"] for x in m["selected_symbolic_references"]], [1, 7])
        self.assertEqual([x["offset"] for x in m["conditional_and_jump_offsets"]], [4])
        self.assertEqual(len(m["method_sha256"]), 64)

    def test_duplicate_jvm_offsets_rejected(self):
        m = method()
        m["instructions"].append(copy.deepcopy(m["instructions"][1]))
        with self.assertRaisesRegex(HelperProbeError, "duplicated"):
            selected_abi(m)

    def test_out_of_order_jvm_offsets_rejected(self):
        m = method()
        m["instructions"][0], m["instructions"][1] = (
            m["instructions"][1], m["instructions"][0])
        with self.assertRaisesRegex(HelperProbeError, "out of order"):
            selected_abi(m)

    def test_oversized_method_rejected(self):
        m = method(instructions=[row(x, "nop") for x in range(1801)])
        with self.assertRaisesRegex(HelperProbeError, "bounded helper"):
            selected_abi(m)

    def test_reference_budget_rejected(self):
        m = method(instructions=[row(x, "invokestatic", "Method X.call:()V")
                                 for x in range(121)])
        with self.assertRaisesRegex(HelperProbeError, "symbolic reference"):
            selected_abi(m)

    def test_branch_budget_rejected(self):
        m = method(instructions=[row(x, "ifne", "", "100")
                                 for x in range(81)])
        with self.assertRaisesRegex(HelperProbeError, "branch export"):
            selected_abi(m)

    def test_publisher_drift_rejected_before_zip(self):
        from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE
        with patch("alexscaves_1010_raygun_itemstack_helper_probe.sha_file",
                   return_value=("wrong", "wrong", 0)):
            with self.assertRaisesRegex(HelperProbeError, "physical 1.0.10"):
                audit("missing.jar", "javap", {
                    "artifact": {"sha1": SHA1, "sha256": SHA256,
                                 "size_bytes": SIZE},
                    "class_sha256": "bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8"
                })


if __name__ == "__main__":
    unittest.main()
