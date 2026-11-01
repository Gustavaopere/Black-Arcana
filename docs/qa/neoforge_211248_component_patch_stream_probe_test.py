#!/usr/bin/env python3
"""Fail-closed tests for SHA-exact DataComponentPatch read-only ABI."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from neoforge_211248_component_patch_stream_probe import (
    ComponentPatchProbeError, selected_method, audit,
    PINNED_SERVER_JAR_SHA256, EXPECTED_JAR_SIZE, verify_snapshot
)


def instruction(offset, opcode, symbol="", operand=""):
    return {"offset":offset,"opcode":opcode,"symbol":symbol,"operand":operand}


def method(instructions=None):
    return {"header":"public static void example();",
            "descriptor":"()V",
            "instructions": instructions if instructions is not None else [
                instruction(0,"getstatic","Field DataComponentPatch.STREAM_CODEC:LStreamCodec;"),
                instruction(3,"ifeq","","9"),
                instruction(6,"invokeinterface","StreamCodec.encode:"),
                instruction(9,"return")]}


class ComponentPatchSelectedAbiTests(unittest.TestCase):
    def prior(self):
        return {"scope":"OFFICIAL_NEOFORGE_211248_INSTALLED_SERVER_CLASSFILE_NOT_LOADED_RUNTIME",
                "neoforge_version":"21.1.248","limits":{"mutation":"NO_MUTATION"}}

    def sealed_fixture(self):
        path=(Path(__file__).resolve().parents[2] /
              "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
              "EXACT-NEOFORGE-211248-COMPONENT-PATCH-ABI.json")
        seal=json.loads(path.read_text(encoding="utf8"))
        report=copy.deepcopy(seal)
        report["static_stream_codec_initializer"]={
            "optional_codec_putstatic_offset":49,
            "selected_preassignment_abi":[
                {"offset":42,"opcode":"new",
                 "symbol":"class net/minecraft/core/component/DataComponentPatch$1"},
                {"offset":46,"opcode":"invokespecial",
                 "symbol":"Method net/minecraft/core/component/DataComponentPatch$1.\"<init>\":()V"},
                {"offset":49,"opcode":"putstatic",
                 "symbol":"Field STREAM_CODEC:Lnet/minecraft/network/codec/StreamCodec;"}
            ]
        }
        report["stream_codec_count_prefix"]=copy.deepcopy(
            seal["counter_and_initial_capacity_abi"])
        report["stream_codec_implementation"]={
            "class_path":seal["codec_class_path"],
            "class_sha256":seal["codec_class_sha256"],
            "methods":[{
                **signature,
                "selected_refs":[
                    {k:row[k] for k in ("offset","opcode","operand","symbol")}
                    for row in seal["critical_codec_abi"]
                    if (row["method"],row["descriptor"]) ==
                       (signature["name"],signature["descriptor"])
                ]
            } for signature in seal["codec_method_signatures"]]
        }
        return report,seal

    def test_exact_decoding_codecs_and_capacity_seal(self):
        report,seal=self.sealed_fixture()
        self.assertTrue(verify_snapshot(report,seal))

    def test_fake_entry_count_limit_rejected(self):
        report,seal=self.sealed_fixture()
        report["limits"]["data_component_patch_entry_limits"]="65536"
        with self.assertRaisesRegex(ComponentPatchProbeError,"false gameplay"):
            verify_snapshot(report,seal)

    def test_wrong_65536_capacity_literal_rejected(self):
        report,seal=self.sealed_fixture()
        source=next(x for x in report["stream_codec_count_prefix"]
                    if x["offset"]==33)
        source["symbol"]="int 128"
        with self.assertRaisesRegex(ComponentPatchProbeError,"initial map capacity"):
            verify_snapshot(report,seal)

    def test_read_count_loop_drift_rejected(self):
        report,seal=self.sealed_fixture()
        source=next(x for x in report["stream_codec_implementation"]["methods"][1]
                    ["selected_refs"] if x["offset"]==49)
        source["operand"]="152"
        with self.assertRaisesRegex(ComponentPatchProbeError,"decode/encode pivot"):
            verify_snapshot(report,seal)

    def test_component_value_codec_dispatch_drift_rejected(self):
        report,seal=self.sealed_fixture()
        source=next(x for x in report["stream_codec_implementation"]["methods"][1]
                    ["selected_refs"] if x["offset"]==68)
        source["symbol"]="Method UnknownCodec.decode:()V"
        with self.assertRaisesRegex(ComponentPatchProbeError,"decode/encode pivot"):
            verify_snapshot(report,seal)

    def test_wrong_component_codec_class_sha_rejected(self):
        report,seal=self.sealed_fixture()
        report["stream_codec_implementation"]["class_sha256"]="a"*64
        with self.assertRaisesRegex(ComponentPatchProbeError,"class hash drift"):
            verify_snapshot(report,seal)

    def test_manifest_cannot_claim_physical_qa(self):
        report,seal=self.sealed_fixture()
        seal["limits"]["physical_qa"]="PASS"
        with self.assertRaisesRegex(ComponentPatchProbeError,"snapshot mismatch"):
            verify_snapshot(report,seal)

    def test_symbolic_and_branch_references(self):
        row=selected_method(method())
        self.assertEqual([x["offset"] for x in row["selected_refs"]],[0,6])
        self.assertEqual([x["offset"] for x in row["conditional_branches"]],[3])
        self.assertEqual(len(row["method_sha256"]),64)

    def test_changed_duplicate_jvm_offset_fails(self):
        m=method()
        m["instructions"].append(copy.deepcopy(m["instructions"][1]))
        with self.assertRaisesRegex(ComponentPatchProbeError,"duplicate JVM"):
            selected_method(m)

    def test_oversized_native_method_fails(self):
        m=method([instruction(i,"nop") for i in range(1801)])
        with self.assertRaisesRegex(ComponentPatchProbeError,"instruction budget"):
            selected_method(m)

    def test_excessive_references_fail(self):
        m=method([instruction(i*3,"invokestatic","Method Other.call:()V")
                  for i in range(96)])
        with self.assertRaisesRegex(ComponentPatchProbeError,"reference budget"):
            selected_method(m)

    def test_excessive_branch_population_fails(self):
        m=method([instruction(i*3,"ifnonnull","","100") for i in range(81)])
        with self.assertRaisesRegex(ComponentPatchProbeError,"branch budget"):
            selected_method(m)

    def test_false_upstream_mutation_fails(self):
        old=self.prior()
        old["limits"]["mutation"]="ALLOW"
        with self.assertRaisesRegex(ComponentPatchProbeError,"authority drift"):
            audit("missing.jar","javap",old)

    def test_wrong_distribution_hash_fails_before_zip_read(self):
        with patch("neoforge_211248_component_patch_stream_probe.sha256_file",
                   return_value=("wrong",EXPECTED_JAR_SIZE)):
            with self.assertRaisesRegex(ComponentPatchProbeError,"SHA/size"):
                audit("missing.jar","javap",self.prior())

    def test_wrong_distribution_size_fails(self):
        with patch("neoforge_211248_component_patch_stream_probe.sha256_file",
                   return_value=(PINNED_SERVER_JAR_SHA256,0)):
            with self.assertRaisesRegex(ComponentPatchProbeError,"SHA/size"):
                audit("missing.jar","javap",self.prior())


if __name__ == "__main__":
    unittest.main()
