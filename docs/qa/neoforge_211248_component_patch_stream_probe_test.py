#!/usr/bin/env python3
"""Fail-closed tests for SHA-exact DataComponentPatch read-only ABI."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch

from neoforge_211248_component_patch_stream_probe import (
    ComponentPatchProbeError, selected_method, audit,
    PINNED_SERVER_JAR_SHA256, EXPECTED_JAR_SIZE
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
