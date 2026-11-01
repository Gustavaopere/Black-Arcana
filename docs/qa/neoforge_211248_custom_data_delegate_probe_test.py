#!/usr/bin/env python3
"""Fail-closed synthetic checks for delegated stream codec discovery."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from neoforge_211248_custom_data_delegate_probe import (
    CLASS_PATHS, DelegatedCodecProbeError,
    EXPECTED_SERVER_BYTES, MAX_REFS_PER_METHOD,
    PINNED_SERVER_JAR_SHA256, PINNED_SRG_JAR_SHA256, audit, choose_archive, interesting_instruction,
    selected_method, snapshot_limits, snapshot_projection,
    verify_safe_report, verify_snapshot,
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
            "server_srg_jar_sha256": PINNED_SRG_JAR_SHA256,
        },
        "classes": {key: {"class_path": path} for key, path in CLASS_PATHS.items()},
        "limits": snapshot_limits(),
    }


class DelegateDiscoveryTests(unittest.TestCase):

    def sealed_fixture(self):
        file = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-NEOFORGE-211248-CUSTOM-DATA-DELEGATE-ABI.json")
        snapshot = json.loads(file.read_text(encoding="utf8"))
        report = empty_report()
        report["schema_version"] = 1
        report["classes"] = {
            key: {
                **entry,
                "matching_methods": [],
            }
            for key, entry in snapshot["class_identities"].items()
        }
        registry = snapshot["data_components_custom_data_reference"]
        report["classes"]["data_components"]["matching_methods"] = [{
            "name": registry["name"],
            "descriptor": registry["descriptor"],
            "method_sha256": registry["method_sha256"],
            "matching_references": [{
                "offset": registry["offset"], "opcode": registry["opcode"],
                "symbol": registry["symbol"],
            }],
        }]
        for item in snapshot["nbt_accounter_supplier_sites"]:
            report["classes"]["byte_buf_codecs"]["matching_methods"].append({
                "name": item["name"],
                "descriptor": item["descriptor"],
                "method_sha256": item["method_sha256"],
                "matching_references": [
                    {
                        "offset": item["literal_offset"],
                        "opcode": item["literal_opcode"],
                        "symbol": item["literal_symbol"],
                    },
                    {
                        "offset": item["create_offset"],
                        "opcode": item["create_opcode"],
                        "symbol": item["create_symbol"],
                    },
                ],
            })
        return report, snapshot

    def test_sealed_supplier_anchors_hold(self):
        report, snapshot = self.sealed_fixture()
        self.assertTrue(verify_snapshot(report, snapshot))

    def test_literal_drift_rejected_before_seal(self):
        report, snapshot = self.sealed_fixture()
        report["classes"]["byte_buf_codecs"]["matching_methods"][0][
            "matching_references"][0]["symbol"] = "long 4194304l"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "literal/call"):
            verify_snapshot(report, snapshot)

    def test_registry_method_digest_drift_rejected(self):
        report, snapshot = self.sealed_fixture()
        report["classes"]["data_components"]["matching_methods"][0][
            "method_sha256"] = "0" * 64
        with self.assertRaisesRegex(DelegatedCodecProbeError, "snapshot mismatch"):
            verify_snapshot(report, snapshot)

    def test_cannot_promote_literal_to_raygun_limit(self):
        report, snapshot = self.sealed_fixture()
        snapshot["literal_interpretation"] = "RAYGUN_2_MIB_MAX"
        with self.assertRaisesRegex(DelegatedCodecProbeError, "snapshot mismatch"):
            verify_snapshot(report, snapshot)

    def test_overlay_precedence_over_distributed_srg(self):
        self.assertEqual(
            choose_archive("CustomData", {"CustomData"}, {"CustomData"}),
            "NEOFORGE_OVERLAY",
        )
        self.assertEqual(
            choose_archive("CustomData", set(), {"CustomData"}),
            "INSTALLED_MINECRAFT_SRG",
        )
        self.assertEqual(
            choose_archive("CustomData", set(), set()),
            "NOT_FOUND_IN_BOTH_INSTALLED_ARCHIVES",
        )

    def test_count_literal_near_accounter_is_preserved_as_evidence_only(self):
        row = selected_method(synthetic_method([
            ins(0, "ldc2_w", "long 2097152l"),
            ins(3, "invokestatic", "Method net/minecraft/nbt/NbtAccounter.create:(J)Lnet/minecraft/nbt/NbtAccounter;"),
            ins(6, "areturn"),
        ]))
        self.assertEqual([x["offset"] for x in row["matching_references"]], [0, 3])

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
