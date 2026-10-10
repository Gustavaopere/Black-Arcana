#!/usr/bin/env python3
"""Synthetic-report regressions: cross-collector #272 SHA-256 provenance."""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

TARGET = Path(__file__).with_name("nonmagic_272_report_reconcile.py")
spec = importlib.util.spec_from_file_location("nonmagic_272_report_reconcile", TARGET)
reconciler = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(reconciler)

COMMIT = "de80b186357cad20ba5b81892a8682777e96e35a"
FILE = "factory_construction_registry_probe-0.1.0.jar"
MOD_ID = "factory_construction_registry_probe"
SHA = "a" * 64


def reports():
    triage = {
        "schema": "black_arcana_nonmagic_jar_triage_v1",
        "evidence": "ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF",
        "source_commit": COMMIT,
        "attempted": 1,
        "statuses": {"FINGERPRINTED": 1},
        "rows": [{
            "physical_number": 272, "name": "Factory Construction Registry Probe",
            "filename": FILE, "triage_group": "OTHER",
            "status": "FINGERPRINTED", "sha1": "1" * 40,
            "sha256": SHA, "bytes": 512, "archive_member_count": 1,
            "lexical_hint_member_count": 0, "lexical_hint_examples": [],
        }],
    }
    metadata = {
        "schema": "black_arcana_nonmagic_272_metadata_probe_v1",
        "evidence": "EMBEDDED_MOD_ID_ONLY_NOT_SPELL_REGISTRY_OR_RUNTIME_PROOF",
        "expected_mod_id": MOD_ID,
        "status": "MATCHED_EMBEDDED_MOD_ID",
        "registry_entries_verified": False,
        "survival_acquisition_verified": False,
        "spell_count": None,
        "sha256": SHA,
        "embedded_mod_ids": [MOD_ID],
        "physical_number": 272, "filename": FILE,
        "source_commit": COMMIT,
    }
    return triage, metadata


class ReconciliationTests(unittest.TestCase):
    def test_matching_sha_and_id_are_consistent_reports_not_spell_proof(self):
        triage, metadata = reports()
        result = reconciler.reconcile(triage, metadata)
        self.assertEqual("REPORTED_HASHES_AND_MOD_ID_CONSISTENT", result["status"])
        self.assertEqual("REPORT_CONSISTENCY_ONLY_NOT_REAL_INSTANCE_OR_REGISTRY_PROOF", result["evidence"])
        self.assertFalse(result["registry_entries_verified"])
        self.assertFalse(result["survival_acquisition_verified"])
        self.assertIsNone(result["spell_count"])
        self.assertEqual("BLOCKED_MISSING_DOSSIER_AND_REGISTRY_PROOF", result["catalog_status"])
        self.assertNotIn("lexical_hint_examples", result)

    def test_cross_capture_swapped_jar_detected_and_blocks(self):
        triage, metadata = reports()
        metadata["sha256"] = "b" * 64
        result = reconciler.reconcile(triage, metadata)
        self.assertEqual("SHA256_MISMATCH", result["status"])
        self.assertNotIn("sha256", result)
        self.assertFalse(result["registry_entries_verified"])

    def test_unavailable_artifact_never_becomes_proof(self):
        triage, metadata = reports()
        triage["rows"][0].update(status="MISSING")
        for key in ("sha1", "sha256", "bytes", "archive_member_count"):
            triage["rows"][0].pop(key, None)
        triage["statuses"] = {"MISSING": 1}
        metadata.update(status="MISSING_JAR")
        for key in ("sha256", "embedded_mod_ids"):
            metadata.pop(key, None)
        result = reconciler.reconcile(triage, metadata)
        self.assertEqual("COLLECTOR_BLOCKED", result["status"])
        self.assertEqual("MISSING", result["triage_status"])

    def test_metadata_mod_id_mismatch_even_if_same_hash_is_blocked(self):
        triage, metadata = reports()
        metadata.update(status="MOD_ID_MISMATCH", embedded_mod_ids=["other_mod"])
        result = reconciler.reconcile(triage, metadata)
        self.assertEqual("EMBEDDED_MOD_ID_NOT_CONFIRMED", result["status"])

    def test_rejects_cross_snapshot_and_wrong_number_or_filename(self):
        for mutation in (lambda t,m: m.update(source_commit="stale"),
                         lambda t,m: t["rows"][0].update(filename="other.jar"),
                         lambda t,m: m.update(physical_number=273),
                         lambda t,m: t["rows"][0].update(triage_group="LEXICAL_NAME")):
            triage, metadata = reports()
            mutation(triage, metadata)
            self.assertEqual("INVALID_REPORT", reconciler.reconcile(triage, metadata)["status"])

    def test_rejects_forged_duplicate_and_malformed_hash_and_count(self):
        for mutation in (lambda t,m: t["rows"].append(copy.deepcopy(t["rows"][0])),
                         lambda t,m: t["rows"][0].update(sha256="not-a-digest"),
                         lambda t,m: t.update(statuses={"FINGERPRINTED": 489}),
                         lambda t,m: m.update(registry_entries_verified=True),
                         lambda t,m: m.update(spell_count=6),
                         lambda t,m: m.update(embedded_mod_ids=["different_mod"]),
                         lambda t,m: t["rows"][0].update(status=[]),
                         lambda t,m: m.update(status=[])):
            triage, metadata = reports()
            mutation(triage, metadata)
            self.assertEqual("INVALID_REPORT", reconciler.reconcile(triage, metadata)["status"])

    def test_accepts_489_row_scan_with_exhaustive_consistent_counts(self):
        triage, metadata = reports()
        for i, number in enumerate((j for j in range(2, 588) if j != 272), start=1):
            if i > 488:
                break
            row = {"physical_number": number, "filename": f"other-{i}.jar", "status": "MISSING"}
            triage["rows"].append(row)
        triage["attempted"] = 489
        triage["statuses"] = {"MISSING": 488, "FINGERPRINTED": 1}
        self.assertEqual("REPORTED_HASHES_AND_MOD_ID_CONSISTENT", reconciler.reconcile(triage,metadata)["status"])

    def test_result_json_remains_bounded_and_does_not_reemit_raw_reports(self):
        triage, metadata = reports()
        triage["rows"][0]["lexical_hint_examples"] = ["data/secret/spells.json"]
        result = reconciler.reconcile(triage, metadata)
        self.assertNotIn("secret", json.dumps(result))
        self.assertNotIn("rows", result)


if __name__ == "__main__":
    unittest.main()
