#!/usr/bin/env python3
"""Fail-closed synthetic checks for delegated stream codec discovery."""
from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from neoforge_211248_custom_data_delegate_probe import (
    CLASS_PATHS, DelegatedCodecProbeError,
    EXPECTED_SERVER_BYTES, MAX_REFS_PER_METHOD,
    PINNED_SERVER_JAR_SHA256, audit, interesting_instruction,
    selected_method, snapshot_limits, verify_safe_report,
)


def ins(offset, opcode, symbol=""):
    return {"offset": offset, "opcode": opcode,
            "operand": "", "symbol": symbol}


def synthetic_method(rows):
    return {"header": "public static void sample();",
            "descriptor": "()V", "instructions": rows}


def empty_report():
    return {
        "scope": "NEOFORGE_211248_DISTRIBUTED_CUSTOM_DATA_DELEGATE_DISCOVERY_ONLY",
        "artifact": {
            "server_jar_sha256": PINNED_SERVER_JAR_SHA256,
            "server_jar_bytes": EXPECTED_SERVER_BYTES,
        },
        "classes": {key: {"class_path": path} for key, path in CLASS_PATHS.items()},
        "limits": snapshot_limits(),
    }


class DelegateDiscoveryTests(unittest.TestCase):

    def test_complete_scope_is_safe(self):
        self.assertTrue(verify_safe_report(empty_report()))

    def test_fake_nbt_byte_limit_is_rejected(self):
        data = empty_report()
        data["limits"]["actual_delegated_nbt_byte_limit"] = "2097152"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "promotion"):
            verify_safe_report(data)

    def test_fake_nbt_depth_limit_is_rejected(self):
        data = empty_report()
        data["limits"]["actual_delegated_nbt_depth_limit"] = "512"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "promotion"):
            verify_safe_report(data)

    def test_fake_sender_authorization_is_rejected(self):
        data = empty_report()
        data["limits"]["raygun_entity_authorization"] = "VERIFIED"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "promotion"):
            verify_safe_report(data)

    def test_fake_hook_or_physical_qa_is_rejected(self):
        data = empty_report()
        data["limits"]["mutating_hook"] = "VERIFIED"
        data["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "promotion"):
            verify_safe_report(data)

    def test_missing_class_scope_is_rejected(self):
        data = empty_report()
        del data["classes"]["custom_data"]
        with self.assertRaisesRegex(DelegatedCodecProbeError, "inventory"):
            verify_safe_report(data)

    def test_unverified_distribution_is_rejected(self):
        data = empty_report()
        data["artifact"]["server_jar_sha256"] = "0" * 64
        with self.assertRaisesRegex(DelegatedCodecProbeError, "identity"):
            verify_safe_report(data)

    def test_symbolic_extraction_and_digest(self):
        row = selected_method(synthetic_method([
            ins(0, "getstatic", "Field CUSTOM_DATA:Lnet/minecraft/core/component/DataComponentType;"),
            ins(3, "invokevirtual", "Method net/minecraft/network/FriendlyByteBuf.readNbt:()Lnet/minecraft/nbt/CompoundTag;"),
            ins(6, "invokevirtual", "Method irrelevant.unrelated:()V"),
            ins(9, "return"),
        ]))
        self.assertEqual([r["offset"] for r in row["matching_references"]], [0, 3])
        self.assertEqual(len(row["method_sha256"]), 64)

    def test_non_symbolic_op_does_not_pass_as_guard(self):
        self.assertFalse(interesting_instruction(ins(5, "ifeq", "CUSTOM_DATA")))
        self.assertFalse(interesting_instruction(ins(5, "invokevirtual", "ordinaryMethod")))

    def test_duplicate_jvm_offsets_are_rejected(self):
        row = ins(4, "getstatic", "Field CUSTOM_DATA;")
        with self.assertRaisesRegex(DelegatedCodecProbeError, "duplicate JVM"):
            selected_method(synthetic_method([row, copy.deepcopy(row)]))

    def test_reference_budget_is_enforced(self):
        refs = [ins(i*3, "getstatic", "Field CUSTOM_DATA:")
                for i in range(MAX_REFS_PER_METHOD + 1)]
        with self.assertRaisesRegex(DelegatedCodecProbeError, "reference budget"):
            selected_method(synthetic_method(refs))

    def test_wrong_jar_fails_before_zip(self):
        with patch("neoforge_211248_custom_data_delegate_probe.sha256_file",
                   return_value=("wrong", EXPECTED_SERVER_BYTES)):
            with self.assertRaisesRegex(DelegatedCodecProbeError, "SHA/size"):
                audit("not-present.jar", "javap")

    def test_wrong_size_fails_before_zip(self):
        with patch("neoforge_211248_custom_data_delegate_probe.sha256_file",
                   return_value=(PINNED_SERVER_JAR_SHA256, 0)):
            with self.assertRaisesRegex(DelegatedCodecProbeError, "SHA/size"):
                audit("not-present.jar", "javap")


if __name__ == "__main__":
    unittest.main()
