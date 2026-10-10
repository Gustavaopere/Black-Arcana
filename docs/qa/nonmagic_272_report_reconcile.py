#!/usr/bin/env python3
"""Read-only consistency gate for separately captured #272 ZIP and metadata reports.

This does not inspect the installed JAR, certify spells, or establish that
submitted reports came from a real instance. Never promote catalog status.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

SOURCE = "de80b186357cad20ba5b81892a8682777e96e35a"
FILENAME = "factory_construction_registry_probe-0.1.0.jar"
MOD_ID = "factory_construction_registry_probe"
TRIAGE_EVIDENCE = "ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF"
METADATA_EVIDENCE = "EMBEDDED_MOD_ID_ONLY_NOT_SPELL_REGISTRY_OR_RUNTIME_PROOF"
SHA1 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
TRIAGE_STATUSES = {
    "FINGERPRINTED", "MISSING", "UNSAFE_SYMLINK", "UNSAFE_OUT_OF_ROOT",
    "INVALID_ZIP_JAR", "CHANGED_DURING_SCAN", "TOO_MANY_MEMBERS",
    "OVERSIZED", "UNREADABLE",
}
METADATA_STATUSES = {
    "MATCHED_EMBEDDED_MOD_ID", "MOD_ID_MISMATCH", "UNREADABLE", "MISSING_JAR",
    "UNSAFE_SYMLINK", "OVERSIZED_JAR", "INVALID_JAR", "TOO_MANY_MEMBERS",
    "MISSING_NEOFORGE_METADATA", "AMBIGUOUS_NEOFORGE_METADATA",
    "METADATA_OVERSIZED", "INVALID_NEOFORGE_METADATA", "CHANGED_DURING_SCAN",
}


def _digest(value: object, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and bool(pattern.fullmatch(value))


def _valid(triage: object, metadata: object) -> bool:
    if not isinstance(triage, dict) or not isinstance(metadata, dict):
        return False
    if (
        triage.get("schema") != "black_arcana_nonmagic_jar_triage_v1"
        or triage.get("evidence") != TRIAGE_EVIDENCE
        or triage.get("source_commit") != SOURCE
        or metadata.get("schema") != "black_arcana_nonmagic_272_metadata_probe_v1"
        or metadata.get("evidence") != METADATA_EVIDENCE
        or metadata.get("source_commit") != SOURCE
        or metadata.get("physical_number") != 272
        or metadata.get("filename") != FILENAME
        or metadata.get("expected_mod_id") != MOD_ID
        or metadata.get("registry_entries_verified") is not False
        or metadata.get("survival_acquisition_verified") is not False
        or metadata.get("spell_count", "MISSING") is not None
        or not isinstance(metadata.get("status"), str)
        or metadata.get("status") not in METADATA_STATUSES
    ):
        return False
    rows = triage.get("rows")
    attempted = triage.get("attempted")
    statuses = triage.get("statuses")
    if (
        not isinstance(rows, list)
        or not isinstance(attempted, int) or isinstance(attempted, bool)
        or attempted not in (1, 489) or len(rows) != attempted
        or not isinstance(statuses, dict)
    ):
        return False
    numbers: set[int] = set()
    names: set[str] = set()
    counts: Counter[str] = Counter()
    chosen = []
    for row in rows:
        if not isinstance(row, dict):
            return False
        number, filename, state = (row.get(k) for k in ("physical_number", "filename", "status"))
        if (
            not isinstance(number, int) or isinstance(number, bool)
            or number < 2 or number > 587 or number in numbers
            or not isinstance(filename, str) or not filename.endswith(".jar")
            or filename in names or "/" in filename or "\\" in filename
            or not isinstance(state, str) or state not in TRIAGE_STATUSES
        ):
            return False
        numbers.add(number)
        names.add(filename)
        counts[state] += 1
        if number == 272:
            chosen.append(row)
        if state == "FINGERPRINTED":
            if not _digest(row.get("sha1"), SHA1) or not _digest(row.get("sha256"), SHA256):
                return False
        elif "sha1" in row or "sha256" in row:
            return False
    if len(chosen) != 1 or chosen[0].get("filename") != FILENAME or chosen[0].get("triage_group") != "OTHER":
        return False
    if (
        any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in statuses.values())
        or dict(counts) != statuses
    ):
        return False
    metadata_status = metadata["status"]
    embedded_ids = metadata.get("embedded_mod_ids")
    if metadata_status in ("MATCHED_EMBEDDED_MOD_ID", "MOD_ID_MISMATCH"):
        if (
            not _digest(metadata.get("sha256"), SHA256)
            or not isinstance(embedded_ids, list) or not embedded_ids
            or any(not isinstance(v, str) or not v for v in embedded_ids)
            or len(embedded_ids) != len(set(embedded_ids))
        ):
            return False
        matches = MOD_ID in embedded_ids
        if matches != (metadata_status == "MATCHED_EMBEDDED_MOD_ID"):
            return False
    elif "sha256" in metadata or "embedded_mod_ids" in metadata:
        return False
    return True


def reconcile(triage: dict, metadata: dict) -> dict:
    """Check claimed capture identity, not provenance, install, registry or gameplay."""
    result = {
        "schema": "black_arcana_nonmagic_272_cross_report_reconciliation_v1",
        "evidence": "REPORT_CONSISTENCY_ONLY_NOT_REAL_INSTANCE_OR_REGISTRY_PROOF",
        "source_commit": SOURCE,
        "physical_number": 272,
        "filename": FILENAME,
        "status": "INVALID_REPORT",
        "catalog_status": "BLOCKED_MISSING_DOSSIER_AND_REGISTRY_PROOF",
        "registry_entries_verified": False,
        "survival_acquisition_verified": False,
        "spell_count": None,
    }
    if not _valid(triage, metadata):
        return result
    target = next(row for row in triage["rows"] if row["physical_number"] == 272)
    result["triage_status"] = target["status"]
    result["metadata_status"] = metadata["status"]
    if target["status"] != "FINGERPRINTED" or metadata["status"] not in (
        "MATCHED_EMBEDDED_MOD_ID", "MOD_ID_MISMATCH"
    ):
        result["status"] = "COLLECTOR_BLOCKED"
    elif target["sha256"] != metadata["sha256"]:
        result["status"] = "SHA256_MISMATCH"
    elif metadata["status"] != "MATCHED_EMBEDDED_MOD_ID":
        result["status"] = "EMBEDDED_MOD_ID_NOT_CONFIRMED"
    else:
        result["status"] = "REPORTED_HASHES_AND_MOD_ID_CONSISTENT"
        result["sha256"] = target["sha256"]
    return result


def _read_json(path: Path) -> object:
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("report exceeds 16 MiB")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, required=True, help="JSON generated by the #272 or full 489-JAR triage")
    parser.add_argument("--metadata", type=Path, required=True, help="JSON generated by the #272 NeoForge metadata probe")
    args = parser.parse_args()
    try:
        output = reconcile(_read_json(args.triage), _read_json(args.metadata))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["status"] == "REPORTED_HASHES_AND_MOD_ID_CONSISTENT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
