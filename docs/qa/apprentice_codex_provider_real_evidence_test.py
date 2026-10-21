#!/usr/bin/env python3
"""Guardrails for provider-real QA record completeness, never gameplay certification."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "apprentice_real_qa", HERE / "apprentice_codex_provider_real_evidence.py"
)
assert SPEC and SPEC.loader
qa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qa)


def pending():
    return {
        "schema": qa.SCHEMA,
        "evidence_class": qa.EVIDENCE_CLASS,
        "provider": {
            "jar": qa.PROVIDER_JAR,
            "mod_id": "apprenticecodex",
            "sha1": qa.PROVIDER_SHA1,
            "sha256": qa.PROVIDER_SHA256,
            "source_pin": qa.SOURCE_PIN,
        },
        "campaign": {
            "candidate_sha": None, "black_arcana_jar_sha256": None,
            "modlist_commit": None, "instance_manifest_sha256": None,
            "minecraft": "1.21.1", "neoforge": None, "irons_version": None,
            "operator_tag": None, "started_utc": None,
        },
        "rows": [{
            "id": name, "state": "PENDING",
            "assertions": dict.fromkeys(assertions, None),
            "observed": None, "checked_utc": None, "evidence": [], "blocker": None,
        } for name, assertions in qa.SCENARIOS.items()],
    }


def freeze(doc):
    doc["campaign"].update(
        candidate_sha="a" * 40,
        black_arcana_jar_sha256="b" * 64,
        modlist_commit="c" * 40,
        instance_manifest_sha256="d" * 64,
        neoforge="21.1.248",
        irons_version="3.16.3",
        operator_tag="qa-session-01",
        started_utc="2026-10-14T15:30:00Z",
    )


def capture(doc, scenario="AC-P02", state="PASS"):
    freeze(doc)
    row = next(r for r in doc["rows"] if r["id"] == scenario)
    row["state"] = state
    row["checked_utc"] = "2026-10-14T15:45:00Z"
    row["observed"] = (
        "Controlled real-client observation with frozen server logs and "
        "timestamps recorded for comparison against the expected contract."
    )
    row["evidence"] = [
        {"kind": "video", "uri": "https://example.invalid/qa/video/01", "sha256": "1" * 64},
        {"kind": "server_log", "uri": "docs/qa/evidence/ac-p02/server.log", "sha256": "2" * 64},
    ]
    if state == "PASS":
        row["assertions"] = dict.fromkeys(qa.SCENARIOS[scenario], True)
    elif state == "FAIL":
        keys = qa.SCENARIOS[scenario]
        row["assertions"] = {k: i != 0 for i, k in enumerate(keys)}
    return row


class PhysicalRecordGuardsTest(unittest.TestCase):
    def test_committed_template_is_pending_and_valid(self):
        doc = json.loads(qa.LEDGER.read_text(encoding="utf-8"))
        self.assertEqual([], qa.validate(doc))
        self.assertEqual(5, len(doc["rows"]))
        self.assertTrue(all(r["state"] == "PENDING" for r in doc["rows"]))

    def test_minimal_pending_template_valid(self):
        self.assertEqual([], qa.validate(pending()))

    def test_claiming_pass_without_candidate_or_observations_is_rejected(self):
        doc = pending()
        doc["rows"][0]["state"] = "PASS"
        self.assertTrue(any("cannot claim result" in x for x in qa.validate(doc)))
        self.assertTrue(any("evidence" in x for x in qa.validate(doc)))

    def test_frozen_candidate_must_be_atomic(self):
        doc = pending()
        doc["campaign"]["candidate_sha"] = "a" * 40
        self.assertTrue(any("all frozen or all null" in x for x in qa.validate(doc)))

    def test_full_observation_metadata_does_not_verify_gameplay(self):
        doc = pending()
        capture(doc)
        self.assertEqual([], qa.validate(doc))
        # Validator only inspects records; it has no server/client execution.
        self.assertNotIn("runtime_pass", json.dumps(doc))

    def test_fail_requires_false_assertion_and_captured_data(self):
        doc = pending()
        row = capture(doc, state="FAIL")
        self.assertEqual([], qa.validate(doc))
        row["assertions"] = dict.fromkeys(qa.SCENARIOS["AC-P02"], True)
        self.assertTrue(any("explicitly false" in x for x in qa.validate(doc)))

    def test_blocked_requires_concrete_reason_not_fake_results(self):
        doc = pending()
        row = doc["rows"][0]
        row["state"] = "BLOCKED"
        row["checked_utc"] = "2026-10-14T15:45:00Z"
        row["blocker"] = "No authorized physical instance is available."
        self.assertEqual([], qa.validate(doc))
        row["assertions"]["exact_provider_jar"] = True
        self.assertTrue(any("does not certify" in x for x in qa.validate(doc)))

    def test_invalid_evidence_digest_and_traversal_rejected(self):
        doc = pending()
        row = capture(doc)
        row["evidence"][0]["sha256"] = "unknown"
        self.assertTrue(any("invalid evidence" in x for x in qa.validate(doc)))
        row["evidence"][0]["sha256"] = "1" * 64
        row["evidence"][1]["uri"] = "docs/qa/evidence/../../private.log"
        self.assertTrue(any("invalid evidence" in x for x in qa.validate(doc)))

    def test_source_pin_and_binary_hash_must_not_drift(self):
        doc = pending()
        doc["provider"]["sha1"] = "f" * 40
        self.assertTrue(any("identity differs" in x for x in qa.validate(doc)))

    def test_duplicate_or_missing_mandatory_scenario_fails(self):
        doc = pending()
        doc["rows"][-1]["id"] = doc["rows"][0]["id"]
        self.assertTrue(any("duplicate" in x for x in qa.validate(doc)))
        self.assertTrue(any("missing mandatory" in x for x in qa.validate(doc)))

    def test_reject_nonutc_and_nonboolean_assertions(self):
        doc = pending()
        row = capture(doc)
        row["checked_utc"] = "2026-10-14T12:45:00-03:00"
        row["assertions"]["tick_cadence_measured"] = 1
        self.assertTrue(any("non-UTC" in x for x in qa.validate(doc)))
        self.assertTrue(any("must be bool or null" in x for x in qa.validate(doc)))

    def test_metadata_looks_like_proof_but_is_not_source_of_authenticity(self):
        doc = pending()
        freeze(doc)
        for row in doc["rows"]:
            row["state"] = "PASS"
            row["checked_utc"] = "2026-10-14T16:00:00Z"
            row["observed"] = "Operator-reported test outcome recorded for later independent human review."
            row["assertions"] = dict.fromkeys(qa.SCENARIOS[row["id"]], True)
            row["evidence"] = [
                {"kind": "video", "uri": "https://example.invalid/capture", "sha256": "3" * 64},
                {"kind": "server_log", "uri": "https://example.invalid/log", "sha256": "4" * 64},
            ]
        self.assertEqual([], qa.validate(doc))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observations.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(qa.__file__), "--ledger", str(path)],
                capture_output=True, text=True, check=True,
            )
        report = json.loads(result.stdout)
        self.assertTrue(report["schema_valid"])
        self.assertTrue(report["all_manual_rows_reported_pass"])
        self.assertFalse(report["physical_gameplay_authenticity_verified_by_automation"])
        self.assertFalse(report["stage_promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
