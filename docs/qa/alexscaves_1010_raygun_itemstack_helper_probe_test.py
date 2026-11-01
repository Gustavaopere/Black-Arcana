#!/usr/bin/env python3
"""Fail-closed synthetic tests; no claims about server NBT validation."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from alexscaves_1010_raygun_itemstack_helper_probe import (
    HELPER, READ, WRITE, TARGETS, HelperProbeError, selected_abi, audit, verify_snapshot
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

    def sealed_fixture(self):
        p = (Path(__file__).resolve().parents[2] /
             "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
             "EXACT-RAYGUN-ITEMSTACK-HELPER-1.0.10.json")
        seal = json.loads(p.read_text(encoding="utf8"))
        report = copy.deepcopy(seal)
        report["selected_methods"] = []
        for method in seal["methods"]:
            refs = [dict((k, anchor[k]) for k in ("offset", "opcode", "symbol"))
                    for anchor in seal["stream_codec_abi_anchors"]
                    if anchor["method"] == method["name"]]
            report["selected_methods"].append({
                **method, "selected_symbolic_references": refs,
                "conditional_and_jump_offsets": []
            })
        return report, seal

    def test_exact_optional_stream_codec_snapshot(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_snapshot(report, seal))

    def test_wrong_read_stream_codec_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected_methods"][0]["selected_symbolic_references"][0][
            "symbol"] = "Field DifferentCodec.CODEC:"
        with self.assertRaisesRegex(HelperProbeError, "exact shaded helper codec"):
            verify_snapshot(report, seal)

    def test_wrong_buffer_cast_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected_methods"][1]["selected_symbolic_references"][1][
            "symbol"] = "class io/netty/buffer/ByteBuf"
        with self.assertRaisesRegex(HelperProbeError, "exact shaded helper codec"):
            verify_snapshot(report, seal)

    def test_false_security_certification_rejected(self):
        report, seal = self.sealed_fixture()
        report["limits"]["nbt_size_depth_and_fields"] = "VERIFIED"
        with self.assertRaisesRegex(HelperProbeError, "safety statuses"):
            verify_snapshot(report, seal)

    def test_changed_native_method_sha_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected_methods"][0]["method_sha256"] = "f" * 64
        with self.assertRaisesRegex(HelperProbeError, "snapshot mismatch"):
            verify_snapshot(report, seal)

    def test_new_helper_control_flow_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected_methods"][0]["conditional_and_jump_offsets"] = [{
            "offset": 4, "opcode": "ifeq", "operand": "7"}]
        with self.assertRaisesRegex(HelperProbeError, "branch logic"):
            verify_snapshot(report, seal)

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
