#!/usr/bin/env python3
"""Synthetic fail-closed checks for native receiver, no fake gameplay QA."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from alexscaves_1010_raygun_receiver_identity_probe import (
    IdentityProbeError, method_inventory, extract_receiver_guard, audit,
    CONTEXT, ENTRY, CLASS_PATHS, verify_snapshot
)
from alexscaves_1010_raygun_receiver_probe import ANCHORS, HANDLE
from alexscaves_1010_raygun_receiver_identity_probe import digest_method


def ref(off, opcode, symbol=""):
    return {"offset": off, "opcode": opcode, "symbol": symbol, "operand": ""}


def receiver():
    data = [ref(0, "aload_0")]
    for off, (opcode, symbol) in ANCHORS["handle"].items():
        data.append(ref(off, opcode, symbol + "LTest;"))
    data.extend([ref(44, "ifeq", ""), ref(69, "ifnonnull", ""),
                 ref(175, "return")])
    return {"header": "public static void handle()", "descriptor": HANDLE,
            "instructions": sorted(data, key=lambda x: x["offset"])}


def sealed(m):
    return {"packet_receiver": {
        "descriptor": HANDLE, "parsed_method_sha256": digest_method(m),
        "instruction_count": len(m["instructions"])}}


class IdentityProbeTests(unittest.TestCase):
    def test_expected_class_roster_distinct(self):
        self.assertEqual(len(CLASS_PATHS), len(set(CLASS_PATHS)))
        self.assertTrue(CONTEXT.endswith("ACNetwork$NeoForgeContext.class"))
        self.assertTrue(ENTRY.endswith("ACNetwork$Entry.class"))

    def test_receiver_exact_positive(self):
        m = receiver()
        v = extract_receiver_guard(m, sealed(m))
        self.assertEqual(v["instruction_count"], len(m["instructions"]))
        self.assertEqual(len(v["critical_anchors"]), len(ANCHORS["handle"]))
        self.assertEqual([r["offset"] for r in v["conditional_branches"]], [44, 69])
        self.assertEqual(len(v["bounded_guard_windows"]), 9)

    def test_guard_opcode_drift_rejected(self):
        m = receiver()
        manifest = sealed(m)
        m["instructions"][1]["opcode"] = "invokestatic"
        with self.assertRaisesRegex(IdentityProbeError, "hash drift"):
            extract_receiver_guard(m, manifest)

    def test_guard_anchor_mismatch_rejected_even_when_digest_rebased(self):
        m = receiver()
        row = next(x for x in m["instructions"] if x["offset"] == 174)
        row["symbol"] = "Other.updateTag"
        with self.assertRaisesRegex(IdentityProbeError, "anchor drift"):
            extract_receiver_guard(m, sealed(m))

    def test_wrong_receiver_descriptor_rejected(self):
        m = receiver()
        m["descriptor"] = "()V"
        with self.assertRaisesRegex(IdentityProbeError, "signature"):
            extract_receiver_guard(m, sealed(m))

    def test_receiver_duplicate_jvm_offset_rejected(self):
        m = receiver()
        m["instructions"].append(copy.deepcopy(m["instructions"][1]))
        with self.assertRaisesRegex(IdentityProbeError, "duplicate JVM offset"):
            extract_receiver_guard(m, sealed(m))

    def test_context_reference_selection(self):
        methods = [{"header": "public ServerPlayer getSender()",
                    "descriptor": "()Lnet/minecraft/server/level/ServerPlayer;",
                    "instructions": [ref(0, "aload_0"), ref(1, "getfield", "Field ctx"),
                                     ref(4, "areturn")]}]
        info = method_inventory(methods, {"getSender"})
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0]["name"], "getSender")
        self.assertEqual(len(info[0]["parsed_method_sha256"]), 64)

    def test_ambiguous_context_signature_rejected(self):
        methods = [{"header": "public void getSender()",
                    "descriptor": "()V", "instructions": [ref(0, "return")]}] * 2
        with self.assertRaisesRegex(IdentityProbeError, "duplicate declared"):
            method_inventory(methods, {"getSender"})

    def test_unbounded_context_method_rejected(self):
        methods = [{"header": "public void handle()",
                    "descriptor": "()V",
                    "instructions": [ref(i, "invokestatic", "Method Thing.x")
                                     for i in range(100)]}]
        with self.assertRaisesRegex(IdentityProbeError, "unbounded"):
            method_inventory(methods, {"handle"})

    def fixture_from_seal(self):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-RAYGUN-RECEIVER-IDENTITY-1.0.10.json")
        sealed = json.loads(path.read_text(encoding="utf-8"))
        report = copy.deepcopy(sealed)
        for section, owner in (("network_context_methods", "context"),
                               ("network_entry_methods", "entry")):
            for member in report[section]:
                member["selected_references"] = [
                    {k: row[k] for k in ("offset", "opcode", "symbol")}
                    for row in sealed["critical_native_anchors"]
                    if row["class"] == owner and row["method"] == member["name"]
                ]
        return report, sealed

    def test_sealed_receiver_projection_positive(self):
        report, sealed = self.fixture_from_seal()
        self.assertTrue(verify_snapshot(report, sealed))

    def test_sealed_native_context_anchor_drift_rejected(self):
        report, sealed = self.fixture_from_seal()
        sender = next(x for x in report["network_context_methods"]
                      if x["name"] == "getSender")
        sender["selected_references"][0]["symbol"] = "OtherContext.getUser"
        with self.assertRaisesRegex(IdentityProbeError, "exact ABI anchor"):
            verify_snapshot(report, sealed)

    def test_sealed_receiver_branch_target_drift_rejected(self):
        report, sealed = self.fixture_from_seal()
        report["receiver"]["conditional_branches"][1]["operand"] = "180"
        with self.assertRaisesRegex(IdentityProbeError, "snapshot mismatch"):
            verify_snapshot(report, sealed)

    def test_sealed_false_runtime_or_qa_promotion_rejected(self):
        report, sealed = self.fixture_from_seal()
        changed = copy.deepcopy(sealed)
        changed["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(IdentityProbeError, "snapshot mismatch"):
            verify_snapshot(report, changed)

    def test_wrong_publisher_rejected_before_archive(self):
        with patch("alexscaves_1010_raygun_receiver_identity_probe.sha_file",
                   return_value=("wrong", "wrong", 0)):
            with self.assertRaisesRegex(IdentityProbeError, "publisher"):
                audit("missing.jar", "javap", {}, {})


if __name__ == "__main__":
    unittest.main()
