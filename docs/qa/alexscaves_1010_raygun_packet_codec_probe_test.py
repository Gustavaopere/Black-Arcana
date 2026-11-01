#!/usr/bin/env python3
"""Synthetic fail-closed regression suite for read-only Raygun wire codec ABI."""
from __future__ import annotations

import copy
import unittest
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
    def test_expected_refs_without_repeating_full_provider_body(self):
        m = bounded_method(method())
        self.assertEqual(m["name"], "write")
        self.assertEqual([x["offset"] for x in m["abi_references"]], [1, 4])
        self.assertEqual(len(m["method_sha256"]), 64)

    def test_field_reads_and_writes_are_selected(self):
        self.assertTrue(include_ref("getfield", "Field entityId:I"))
        self.assertTrue(include_ref("putfield", "Field itemStackFrom:LItemStack;"))
        self.assertFalse(include_ref("aload_0", ""))
        self.assertFalse(include_ref("return", ""))

    def test_duplicate_jvm_offset_fails(self):
        m = method()
        m["instructions"].append(copy.deepcopy(m["instructions"][1]))
        with self.assertRaisesRegex(CodecProbeError, "duplicate packet JVM"):
            bounded_method(m)

    def test_unbounded_method_fails(self):
        m = method(rows=[
            {"offset": i, "opcode": "nop", "operand": "", "symbol": ""}
            for i in range(851)])
        with self.assertRaisesRegex(CodecProbeError, "unbounded packet method"):
            bounded_method(m)

    def test_snapshot_matches_only_exact_record(self):
        original = {"methods": [{"method_sha256": "a" * 64, "name": "write",
                                  "descriptor": "()V"}]}
        # A real snapshot requires at least two methods (handler + codec path).
        with self.assertRaisesRegex(CodecProbeError, "packet method count"):
            verify_snapshot(original, copy.deepcopy(original))
        original["methods"].append({"method_sha256": "b" * 64, "name": "handle",
                                    "descriptor": "(I)V"})
        self.assertTrue(verify_snapshot(original, copy.deepcopy(original)))
        altered = copy.deepcopy(original)
        altered["methods"][0]["method_sha256"] = "c" * 64
        with self.assertRaisesRegex(CodecProbeError, "snapshot mismatch"):
            verify_snapshot(original, altered)

    def test_duplicate_signature_in_snapshot_fails(self):
        original = {"methods": [{"name": "write", "descriptor": "()V"},
                                {"name": "write", "descriptor": "()V"}]}
        with self.assertRaisesRegex(CodecProbeError, "ambiguous"):
            verify_snapshot(original, original)

    def test_false_security_promotion_rejected(self):
        original = {"methods": [{"name": "write", "descriptor": "()V"},
                                {"name": "handle", "descriptor": "()V"}],
                    "limits": {"mutation": "NO_MUTATION"}}
        altered = copy.deepcopy(original)
        altered["limits"]["mutation"] = "ALLOWED"
        with self.assertRaisesRegex(CodecProbeError, "snapshot mismatch"):
            verify_snapshot(original, altered)

    def test_wrong_publisher_rejected_before_zip_read(self):
        with patch("alexscaves_1010_raygun_packet_codec_probe.sha_file",
                   return_value=("bad", "bad", 0)):
            with self.assertRaisesRegex(CodecProbeError, "publisher identity"):
                audit("missing.jar", "javap", {}, {})


if __name__ == "__main__":
    unittest.main()
