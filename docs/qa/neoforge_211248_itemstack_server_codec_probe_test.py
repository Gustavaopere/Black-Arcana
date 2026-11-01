#!/usr/bin/env python3
"""Synthetic fail-closed exact NeoForge server distribution codec ABI tests."""
from __future__ import annotations

import unittest
from unittest.mock import patch
from neoforge_211248_itemstack_server_codec_probe import (
    NeoForgeServerCodecError, audit, method_reference_counts
)


class NeoForgeServerCodecTests(unittest.TestCase):
    def vanilla(self):
        return {
            "scope": "OFFICIAL_MOJANG_VANILLA_1211_ITEMSTACK_STATIC_ABI_CORROBORATION_ONLY",
            "version": "1.21.1",
            "limits": {"neoforge_21_1_248_merged_runtime": "NOT_INSPECTED"}
        }

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
