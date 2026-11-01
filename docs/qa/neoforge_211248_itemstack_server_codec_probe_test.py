#!/usr/bin/env python3
"""Synthetic fail-closed exact NeoForge server distribution codec ABI tests."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from neoforge_211248_itemstack_server_codec_probe import (
    NeoForgeServerCodecError, audit, method_reference_counts, verify_snapshot
)


class NeoForgeServerCodecTests(unittest.TestCase):
    def vanilla(self):
        return {
            "scope": "OFFICIAL_MOJANG_VANILLA_1211_ITEMSTACK_STATIC_ABI_CORROBORATION_ONLY",
            "version": "1.21.1",
            "limits": {"neoforge_21_1_248_merged_runtime": "NOT_INSPECTED"}
        }

    def sealed_fixture(self):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-NEOFORGE-211248-ITEMSTACK-SERVER-ABI.json")
        seal = json.loads(path.read_text(encoding="utf8"))
        report = copy.deepcopy(seal)
        report["optional_codec_initializer"] = {
            "optional_codec_putstatic_offset": seal["codec_static_assignment_offset"]
        }
        report["optional_codec_implementation"] = {
            "class_path": seal["codec_class_path"],
            "class_sha256": seal["codec_class_sha256"],
            "methods": [
                {
                    "name": m["name"], "descriptor": m["descriptor"],
                    "selected_refs": [
                        {k: r[k] for k in ("offset", "opcode", "operand", "symbol")}
                        for r in seal["critical_codec_abi"]
                        if (r["method"], r["descriptor"]) ==
                           (m["name"], m["descriptor"])
                    ]
                } for m in seal["codec_methods"]
            ]
        }
        return report, seal

    def test_exact_211248_distribution_seal_positive(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_snapshot(report, seal))

    def test_modified_distribution_binary_digest_fails(self):
        report, seal = self.sealed_fixture()
        report["installed_server_jar_sha256"] = "0" * 64
        with self.assertRaisesRegex(NeoForgeServerCodecError, "JAR identity"):
            verify_snapshot(report, seal)

    def test_malformed_entity_count_branch_fails(self):
        report, seal = self.sealed_fixture()
        decode = report["optional_codec_implementation"]["methods"][1]
        decode["selected_refs"][1]["operand"] = "180"
        with self.assertRaisesRegex(NeoForgeServerCodecError, "critical branch"):
            verify_snapshot(report, seal)

    def test_component_patch_reader_changed_fails(self):
        report, seal = self.sealed_fixture()
        decode = report["optional_codec_implementation"]["methods"][1]
        decode["selected_refs"][5]["symbol"] = "Field UnknownCodec.CODEC:"
        with self.assertRaisesRegex(NeoForgeServerCodecError, "critical branch"):
            verify_snapshot(report, seal)

    def test_replaced_codec_class_sha_fails(self):
        report, seal = self.sealed_fixture()
        report["optional_codec_implementation"]["class_sha256"] = "a" * 64
        with self.assertRaisesRegex(NeoForgeServerCodecError, "codec class"):
            verify_snapshot(report, seal)

    def test_false_modlauncher_verification_fails(self):
        report, seal = self.sealed_fixture()
        report["limits"]["jvm_modlauncher_class_loaded"] = "PASS"
        with self.assertRaisesRegex(NeoForgeServerCodecError, "false security"):
            verify_snapshot(report, seal)

    def test_fake_physical_qa_in_manifest_fails(self):
        report, seal = self.sealed_fixture()
        seal["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(NeoForgeServerCodecError, "sealed official"):
            verify_snapshot(report, seal)

    def test_limit_missing_prior_vanilla_scope(self):
        with self.assertRaisesRegex(NeoForgeServerCodecError, "scope/policy"):
            audit("none.jar", "javap", {**self.vanilla(), "version": "1.21.2"})

    def test_limit_false_vanilla_neoforge_promotion(self):
        prior = self.vanilla()
        prior["limits"]["neoforge_21_1_248_merged_runtime"] = "VERIFIED"
        with self.assertRaisesRegex(NeoForgeServerCodecError, "scope/policy"):
            audit("none.jar", "javap", prior)

    def test_invalid_server_jar_budget_rejected(self):
        with patch("neoforge_211248_itemstack_server_codec_probe.sha256_file",
                   return_value=("0" * 64, 2)):
            with self.assertRaisesRegex(NeoForgeServerCodecError, "size implausible"):
                audit("none.jar", "javap", self.vanilla())

    def test_empty_method_roster_rejected(self):
        with self.assertRaisesRegex(NeoForgeServerCodecError, "method count"):
            method_reference_counts({"methods": []})

    def test_unbounded_codec_method_roster_rejected(self):
        with self.assertRaisesRegex(NeoForgeServerCodecError, "method count"):
            method_reference_counts({"methods": [{}] * 13})

    def test_bounded_semantic_reference_counts(self):
        selected = {"methods": [
            {"name": "decode", "descriptor": "(Ljava/lang/Object;)Ljava/lang/Object;",
             "instruction_count": 8,
             "selected_refs": [{"offset": 1, "opcode": "checkcast"}]},
            {"name": "encode", "descriptor": "(Ljava/lang/Object;Ljava/lang/Object;)V",
             "instruction_count": 11, "selected_refs": []}
        ]}
        result = method_reference_counts(selected)
        self.assertEqual(result[0]["reference_count"], 1)
        self.assertEqual(result[1]["reference_count"], 0)


if __name__ == "__main__":
    unittest.main()
