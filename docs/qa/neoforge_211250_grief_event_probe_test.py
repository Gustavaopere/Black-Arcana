#!/usr/bin/env python3
"""Synthetic comparator tests. The real JAR is only tested by the CI workflow."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from neoforge_211250_grief_event_probe import (
    BASELINE_SHA256, EvidenceError, LIMITS, SCOPE,
    audit, baseline_methods, compare_versions, verify_seal,
)

BASE = (Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers" /
        "✅-alexs-caves-continued/NEOFORGE-211248-GRIEF-EVENT-ABI.json")


class Version250GriefTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads(BASE.read_text(encoding="utf-8"))
        self.fake250 = copy.deepcopy(self.baseline)
        self.fake250["artifact"]["sha256"] = "f"*64
        self.fake250["artifact"]["size_bytes"] = 3551269

    def patched_audit(self):
        with patch("neoforge_211250_grief_event_probe.examine_previous",
                   return_value=self.fake250):
            return audit("neoforge-21.1.250-universal.jar", "javap", self.baseline)

    def test_exact_pinned_baseline_identity(self):
        self.assertEqual(self.baseline["artifact"]["sha256"], BASELINE_SHA256)
        self.assertEqual(len(baseline_methods(self.baseline)), 2)

    def test_positive_structural_comparison_and_safety(self):
        report = self.patched_audit()
        self.assertEqual(report["scope"], SCOPE)
        self.assertEqual(report["limits"], LIMITS)
        self.assertEqual(report["artifact"]["coordinates"],
                         "net.neoforged:neoforge:21.1.250:universal")
        self.assertTrue(report["baseline_comparison"]["all_selected_method_hashes_equal"])
        self.assertTrue(report["baseline_comparison"]["all_selected_class_hashes_equal"])
        self.assertEqual(len(report["baseline_comparison"]["method_comparison"]), 5)
        self.assertTrue(verify_seal(report, copy.deepcopy(report)))

    def test_wrong_248_artifact_path_fails_closed(self):
        with patch("neoforge_211250_grief_event_probe.examine_previous",
                   return_value=self.fake250):
            with self.assertRaisesRegex(EvidenceError, "wrong 21.1.250"):
                audit("neoforge-21.1.248-universal.jar", "javap", self.baseline)

    def test_changed_baseline_digest_rejected(self):
        bad = copy.deepcopy(self.baseline)
        bad["artifact"]["sha256"] = "0"*64
        with self.assertRaisesRegex(EvidenceError, "incorrect 21.1.248"):
            compare_versions(self.fake250, bad)

    def test_changed_baseline_method_universe_rejected(self):
        bad = copy.deepcopy(self.baseline)
        bad["classes"][1]["selected_methods"].pop()
        with self.assertRaisesRegex(EvidenceError, "baseline method count"):
            compare_versions(self.fake250, bad)

    def test_method_drift_cannot_be_silently_called_parity(self):
        self.fake250["classes"][0]["selected_methods"][0]["method_sha256"] = "0"*64
        observed = self.patched_audit()
        self.assertFalse(observed["baseline_comparison"]["all_selected_method_hashes_equal"])
        self.assertTrue(observed["baseline_comparison"]["all_selected_references_exact_equal"])

    def test_callsite_drift_cannot_be_silently_called_parity(self):
        ref = self.fake250["classes"][0]["selected_methods"][0]["selected_references"][0]
        ref["symbol"] = "Method incompatible:()V"
        observed = self.patched_audit()
        self.assertFalse(observed["baseline_comparison"]["all_selected_references_exact_equal"])
        self.assertFalse(observed["baseline_comparison"]["all_selected_references_symbolic_sequence_equal"])

    def test_callsite_offset_change_not_same_exact_abi(self):
        self.fake250["classes"][0]["selected_methods"][0]["selected_references"][0]["offset"] += 1
        observed = self.patched_audit()
        self.assertFalse(observed["baseline_comparison"]["all_selected_references_exact_equal"])
        self.assertTrue(observed["baseline_comparison"]["all_selected_references_symbolic_sequence_equal"])

    def test_missing_new_method_rejected(self):
        self.fake250["classes"][1]["selected_methods"].pop()
        with self.assertRaisesRegex(EvidenceError, "method population changed"):
            self.patched_audit()

    def test_seal_rejects_changed_comparison_and_safety(self):
        observed = self.patched_audit()
        bad = copy.deepcopy(observed)
        bad["baseline_comparison"]["all_selected_method_hashes_equal"] = False
        with self.assertRaisesRegex(EvidenceError, "comparison seal"):
            verify_seal(observed, bad)
        bad = copy.deepcopy(observed)
        bad["limits"]["mutation"] = "ALLOWED"
        with self.assertRaisesRegex(EvidenceError, "seal mismatch: limits"):
            verify_seal(observed, bad)


if __name__ == "__main__":
    unittest.main()
