#!/usr/bin/env python3
"""Fail-closed Raygun 1.0.10 packet ABI regressions, no gameplay claims."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from alexscaves_1010_raygun_packet_codec_probe import (
    CodecProbeError, bounded_method, include_ref, verify_snapshot, audit,
)


def method(name="write", rows=None):
    if rows is None:
        rows = [
            {"offset": 0, "opcode": "aload_0", "symbol": "", "operand": ""},
            {"offset": 1, "opcode": "getfield", "symbol": "Field entityId:I", "operand": "#2"},
            {"offset": 4, "opcode": "invokevirtual", "symbol": "ByteBuf.writeVarInt:(I)V",
             "operand": "#3"},
            {"offset": 7, "opcode": "return", "symbol": "", "operand": ""},
        ]
    return {"header": "public void " + name + "()", "descriptor": "()V",
            "instructions": rows}


class CodecAbiSyntheticTests(unittest.TestCase):
    def fixture(self):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-RAYGUN-PACKET-CODEC-1.0.10.json")
        sealed = json.loads(path.read_text(encoding="utf8"))
        report = copy.deepcopy(sealed)
        for row in report["methods"]:
            row["abi_references"] = [
                {k: a[k] for k in ("offset", "opcode", "symbol")}
                for a in sealed["codec_abi_anchors"] if a["method"] == row["name"]
            ]
        return report, sealed

    def test_selected_references_without_full_provider_body(self):
        row = bounded_method(method())
        self.assertEqual(row["name"], "write")
        self.assertEqual([x["offset"] for x in row["abi_references"]], [1, 4])
        self.assertEqual(len(row["method_sha256"]), 64)

    def test_jvm_field_selection(self):
        self.assertTrue(include_ref("getfield", "Field entityId:I"))
        self.assertTrue(include_ref("putfield", "Field itemStackFrom:LItemStack;"))
        self.assertFalse(include_ref("aload_0", ""))
        self.assertFalse(include_ref("return", ""))

    def test_duplicate_instruction_offset_rejected(self):
        row = method()
        row["instructions"].append(copy.deepcopy(row["instructions"][1]))
        with self.assertRaisesRegex(CodecProbeError, "duplicate packet JVM"):
            bounded_method(row)

    def test_unbounded_method_rejected(self):
        row = method(rows=[
            {"offset": i, "opcode": "nop", "operand": "", "symbol": ""}
            for i in range(851)])
        with self.assertRaisesRegex(CodecProbeError, "unbounded packet method"):
            bounded_method(row)

    def test_exact_four_method_seal_positive(self):
        report, sealed = self.fixture()
        self.assertTrue(verify_snapshot(report, sealed))

    def test_wrong_codec_method_digest_rejected(self):
        report, sealed = self.fixture()
        report["methods"][1]["method_sha256"] = "b" * 64
        with self.assertRaisesRegex(CodecProbeError, "snapshot mismatch"):
            verify_snapshot(report, sealed)

    def test_changed_item_deserialization_call_rejected(self):
        report, sealed = self.fixture()
        selected = report["methods"][1]["abi_references"]
        selected[1]["symbol"] = selected[1]["symbol"].replace(
            "PacketBufferUtils.readItemStack", "Untrusted.read")
        with self.assertRaisesRegex(CodecProbeError, "opcode/field anchor"):
            verify_snapshot(report, sealed)

    def test_changed_entity_id_field_rejected(self):
        report, sealed = self.fixture()
        report["methods"][2]["abi_references"][0]["symbol"] = "Field arbitraryId:I"
        with self.assertRaisesRegex(CodecProbeError, "opcode/field anchor"):
            verify_snapshot(report, sealed)

    def test_changed_write_stack_call_rejected(self):
        report, sealed = self.fixture()
        report["methods"][2]["abi_references"][3]["symbol"] = "Method Other.write:()V"
        with self.assertRaisesRegex(CodecProbeError, "opcode/field anchor"):
            verify_snapshot(report, sealed)

    def test_false_runtime_status_rejected(self):
        report, sealed = self.fixture()
        report["limits"]["mutation"] = "ALLOW"
        with self.assertRaisesRegex(CodecProbeError, "status or limits"):
            verify_snapshot(report, sealed)

    def test_false_security_status_in_seal_rejected(self):
        report, sealed = self.fixture()
        sealed["limits"]["sender_entity_id_binding"] = "VERIFIED"
        with self.assertRaisesRegex(CodecProbeError, "snapshot mismatch"):
            verify_snapshot(report, sealed)

    def test_incomplete_method_roster_rejected(self):
        report, sealed = self.fixture()
        report["methods"].pop()
        with self.assertRaisesRegex(CodecProbeError, "method count"):
            verify_snapshot(report, sealed)

    def test_duplicate_packet_abi_signature_rejected(self):
        report, sealed = self.fixture()
        report["methods"][1]["descriptor"] = report["methods"][0]["descriptor"]
        report["methods"][1]["name"] = report["methods"][0]["name"]
        with self.assertRaisesRegex(CodecProbeError, "method roster/order"):
            verify_snapshot(report, sealed)

    def test_wrong_publisher_rejected_before_read(self):
        with patch("alexscaves_1010_raygun_packet_codec_probe.sha_file",
                   return_value=("bad", "bad", 0)):
            with self.assertRaisesRegex(CodecProbeError, "publisher identity"):
                audit("missing.jar", "javap", {}, {})


if __name__ == "__main__":
    unittest.main()
