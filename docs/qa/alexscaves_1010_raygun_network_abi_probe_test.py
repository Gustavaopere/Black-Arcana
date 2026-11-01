#!/usr/bin/env python3
"""Synthetic fail-closed tests for exact-JAR network ABI snapshots."""
from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from alexscaves_1010_raygun_network_abi_probe import (
    MAX_INSTRUCTIONS, RegistrationProbeError, bounded_method,
    select_network_methods, verify_snapshot, audit, TARGET_METHODS
)


def ins(off, sym="", opcode="invokestatic"):
    return {"offset": off, "opcode": opcode, "symbol": sym, "operand": "#2"}


def method(name, offset=12, symbol="Method UpdateItemTagMessage.read:()V"):
    return {"header": "public static void " + name + "()",
            "descriptor": "()V",
            "instructions": [ins(0, "Method ABC.x:()V"),
                             ins(offset, symbol), ins(offset + 4, "", "return")]}


class ExactNativeNetworkABI(unittest.TestCase):
    def roster(self):
        rows = [method("registerMessages"),
                method("registerPayloads", 10, "Method PayloadRegistrar.register:()V"),
                method("lambda$registerPayloads$0", 5, "Method ACNetworkContext.getSender:()V")]
        return rows

    def test_minimal_synthetic_positive(self):
        selected = select_network_methods(self.roster())
        self.assertEqual([x["name"] for x in selected], list(TARGET_METHODS))
        self.assertEqual(selected[0]["packet_reference_offsets"], [12])
        self.assertEqual(len(selected[0]["parsed_method_sha256"]), 64)
        self.assertTrue(selected[0]["packet_reference_windows"])

    def test_packet_reference_must_be_in_register_messages(self):
        rows = self.roster()
        rows[0]["instructions"][1]["symbol"] = "Method OtherMessage.read:()V"
        with self.assertRaisesRegex(RegistrationProbeError, "direct packet linkage"):
            select_network_methods(rows)

    def test_missing_registration_callback_fails(self):
        rows = self.roster()[:2]
        with self.assertRaisesRegex(RegistrationProbeError, "missing/ambiguous"):
            select_network_methods(rows)

    def test_duplicate_signature_fails(self):
        rows = self.roster()
        rows.append(copy.deepcopy(rows[0]))
        with self.assertRaisesRegex(RegistrationProbeError, "duplicate JVM"):
            select_network_methods(rows)

    def test_duplicate_offset_fails(self):
        rows = self.roster()
        rows[0]["instructions"].append(ins(12, "Method UpdateItemTagMessage.read:()V"))
        with self.assertRaisesRegex(RegistrationProbeError, "duplicate JVM instruction"):
            select_network_methods(rows)

    def test_callback_requires_payload_or_context(self):
        rows = self.roster()
        rows[2]["instructions"][1]["symbol"] = "Method Other.x:()V"
        with self.assertRaisesRegex(RegistrationProbeError, "callback boundary"):
            select_network_methods(rows)

    def test_bounded_oversize_method_rejected(self):
        m = method("registerMessages")
        m["instructions"] = [ins(i, "Method UpdateItemTagMessage.read:()V")
                             for i in range(MAX_INSTRUCTIONS + 1)]
        with self.assertRaisesRegex(RegistrationProbeError, "oversize"):
            bounded_method(m)

    def test_snapshot_rejects_modified_bytecode_digest(self):
        report = {"selected_methods": [{"parsed_method_sha256": "a" * 64}],
                  "limits": {"mutation": "NO_MUTATION"}}
        self.assertTrue(verify_snapshot(report, copy.deepcopy(report)))
        altered = copy.deepcopy(report)
        altered["selected_methods"][0]["parsed_method_sha256"] = "b" * 64
        with self.assertRaisesRegex(RegistrationProbeError, "sealed network ABI"):
            verify_snapshot(report, altered)

    def test_snapshot_rejects_false_physical_status(self):
        report = {"limits": {"physical_qa": "NOT_TESTED"}}
        altered = {"limits": {"physical_qa": "PASS"}}
        with self.assertRaisesRegex(RegistrationProbeError, "sealed network ABI"):
            verify_snapshot(report, altered)

    def test_wrong_publisher_rejected_before_zip_open(self):
        with patch("alexscaves_1010_raygun_network_abi_probe.sha_file",
                   return_value=("bad", "bad", 1)):
            with self.assertRaisesRegex(RegistrationProbeError, "publisher JAR SHA"):
                audit("absent.jar", "javap", {"artifact": {}})


if __name__ == "__main__":
    unittest.main()
