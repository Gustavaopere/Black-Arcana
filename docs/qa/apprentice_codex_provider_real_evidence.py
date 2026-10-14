#!/usr/bin/env python3
"""Validate completeness of Apprentice's Codex real-modpack QA evidence records.

This intentionally cannot verify that gameplay happened. It never promotes a
stage or treats CI, screenshots, URLs, or operator assertions as physical PASS.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/qa/apprentice-codex-provider-real-evidence.json"
PROVIDER_JAR = "apprentice_codex-0.9.7.1+mc1.21.1.jar"
PROVIDER_SHA1 = "b514315add32b93b0049c8673075627d7ef812e0"
PROVIDER_SHA256 = "f0dfab67154f344c02c6fbe561f73456fa46ed9d018fae661dcdf4da95c67fe2"
SOURCE_PIN = "305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e"
SCHEMA = "black_arcana_apprentice_codex_provider_real_v1"
EVIDENCE_CLASS = "OPERATOR_REPORTED_MANUAL_QA_NOT_AUTOMATIC_GAMEPLAY_PROOF"
STATES = {"PENDING", "PASS", "FAIL", "BLOCKED"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SCENARIOS = {
    "AC-P01": ("exact_provider_jar", "correct_mod_ids_and_versions",
               "dedicated_server_boot", "real_client_spell_registry"),
    "AC-P02": ("baseline_without_cast_damage", "tick_cadence_measured",
               "server_damage_attribution", "cancel_despawn_observed"),
    "AC-P03": ("normal_impact_baseline", "antimagic_before_burst",
               "amplified_burst_observed", "owner_ally_world_safety_checked"),
    "AC-P04": ("pastel_staff_held", "precast_cancel_observed",
               "staff_affinity_applied", "mana_cooldown_audited"),
    "AC-P05": ("item_identity_swap_tested", "repair_amounts_recorded",
               "relog_restart_tested", "no_duplicate_repair_or_cost"),
}
KINDS = {"video", "screenshot", "client_log", "server_log", "world_snapshot",
         "instance_manifest"}


def _iso_utc(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0


def _evidence_item(item: object) -> bool:
    if not isinstance(item, dict) or set(item) != {"kind", "uri", "sha256"}:
        return False
    if item["kind"] not in KINDS or not isinstance(item["uri"], str):
        return False
    uri = item["uri"]
    if not (uri.startswith("https://") or uri.startswith("docs/qa/evidence/")):
        return False
    if ".." in uri or any(c.isspace() for c in uri):
        return False
    return isinstance(item["sha256"], str) and HEX64.fullmatch(item["sha256"]) is not None


def validate(doc: object) -> list[str]:
    """Return errors, not PASS/FAIL conclusions about gameplay."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be an object"]
    if set(doc) != {"schema", "evidence_class", "provider", "campaign", "rows"}:
        errors.append("root keys mismatch")
    if doc.get("schema") != SCHEMA or doc.get("evidence_class") != EVIDENCE_CLASS:
        errors.append("schema/evidence class mismatch")
    provider = doc.get("provider")
    expected_provider = {
        "jar": PROVIDER_JAR, "mod_id": "apprenticecodex",
        "sha1": PROVIDER_SHA1, "sha256": PROVIDER_SHA256,
        "source_pin": SOURCE_PIN,
    }
    if provider != expected_provider:
        errors.append("provider identity differs from exact binary provenance")
    campaign = doc.get("campaign")
    if not isinstance(campaign, dict) or set(campaign) != {
        "candidate_sha", "black_arcana_jar_sha256",
        "modlist_commit", "instance_manifest_sha256", "minecraft",
        "neoforge", "irons_version", "operator_tag", "started_utc",
    }:
        errors.append("campaign shape mismatch")
        campaign = {}
    if campaign.get("minecraft") != "1.21.1":
        errors.append("Minecraft version mismatch")
    core_keys = ("candidate_sha", "black_arcana_jar_sha256", "modlist_commit",
                 "instance_manifest_sha256", "neoforge", "irons_version",
                 "operator_tag", "started_utc")
    values = [campaign.get(k) for k in core_keys]
    frozen = all(v is not None for v in values)
    unstarted = all(v is None for v in values)
    if not (frozen or unstarted):
        errors.append("candidate metadata must be all frozen or all null")
    if frozen:
        if not (isinstance(campaign["candidate_sha"], str)
                and HEX40.fullmatch(campaign["candidate_sha"])
                and isinstance(campaign["modlist_commit"], str)
                and HEX40.fullmatch(campaign["modlist_commit"])):
            errors.append("candidate and modlist need exact 40-hex SHAs")
        for k in ("black_arcana_jar_sha256", "instance_manifest_sha256"):
            if not (isinstance(campaign[k], str) and HEX64.fullmatch(campaign[k])):
                errors.append(f"{k} requires a 64-hex digest")
        for k in ("neoforge", "irons_version", "operator_tag"):
            if not isinstance(campaign[k], str) or not campaign[k].strip():
                errors.append(f"{k} must be nonblank")
        if not _iso_utc(campaign["started_utc"]):
            errors.append("started_utc requires offset-aware UTC ISO-8601")
    rows = doc.get("rows")
    if not isinstance(rows, list) or len(rows) != len(SCENARIOS):
        return errors + ["rows must enumerate each of five scenarios exactly"]
    seen: set[str] = set()
    for i, row in enumerate(rows):
        name = row.get("id") if isinstance(row, dict) else None
        prefix = name if isinstance(name, str) else f"row {i}"
        if not isinstance(row, dict) or set(row) != {
            "id", "state", "assertions", "observed", "checked_utc",
            "evidence", "blocker",
        }:
            errors.append(f"{prefix}: invalid row keys")
            continue
        if name not in SCENARIOS or name in seen:
            errors.append(f"{prefix}: unknown or duplicate scenario")
            continue
        seen.add(name)
        state = row["state"]
        if state not in STATES:
            errors.append(f"{prefix}: invalid state")
            continue
        assertions = row["assertions"]
        if not isinstance(assertions, dict) or set(assertions) != set(SCENARIOS[name]):
            errors.append(f"{prefix}: missing/extra assertions")
            continue
        if any(type(v) not in (bool, type(None)) for v in assertions.values()):
            errors.append(f"{prefix}: assertions must be bool or null")
        evidence = row["evidence"]
        if not isinstance(evidence, list) or not all(_evidence_item(e) for e in evidence):
            errors.append(f"{prefix}: invalid evidence references/digests")
            continue
        if state == "PENDING":
            if (any(v is not None for v in assertions.values())
                    or row["observed"] is not None or row["checked_utc"] is not None
                    or evidence or row["blocker"] is not None):
                errors.append(f"{prefix}: PENDING must contain no observations")
            continue
        if not _iso_utc(row["checked_utc"]):
            errors.append(f"{prefix}: checked_utc missing or non-UTC")
        if state in ("PASS", "FAIL"):
            if not frozen:
                errors.append(f"{prefix}: cannot claim result before exact candidate freeze")
            if not isinstance(row["observed"], str) or len(row["observed"].strip()) < 30:
                errors.append(f"{prefix}: detailed observed behavior required")
            if len(evidence) < 2:
                errors.append(f"{prefix}: require at least two captured evidence objects")
            if row["blocker"] is not None:
                errors.append(f"{prefix}: PASS/FAIL cannot have blocker")
            if state == "PASS" and not all(v is True for v in assertions.values()):
                errors.append(f"{prefix}: PASS requires all assertions observed true")
            if state == "FAIL" and not any(v is False for v in assertions.values()):
                errors.append(f"{prefix}: FAIL requires an explicitly false assertion")
        else:  # BLOCKED: cannot be silently promoted
            if not isinstance(row["blocker"], str) or len(row["blocker"].strip()) < 20:
                errors.append(f"{prefix}: BLOCKED must explain concrete blocker")
            if any(v is not None for v in assertions.values()):
                errors.append(f"{prefix}: BLOCKED does not certify assertions")
    if seen != set(SCENARIOS):
        errors.append("missing mandatory scenario")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"schema_valid": False, "error": str(exc)}))
        return 1
    errors = validate(data)
    rows = data.get("rows", []) if isinstance(data, dict) else []
    counts = {state: sum(
        1 for r in rows if isinstance(r, dict) and r.get("state") == state
    ) for state in ("PASS", "FAIL", "BLOCKED", "PENDING")}
    print(json.dumps({
        "schema_valid": not errors, "counts": counts,
        "all_manual_rows_reported_pass": not errors and counts["PASS"] == len(SCENARIOS),
        "physical_gameplay_authenticity_verified_by_automation": False,
        "stage_promotion_authorized": False, "errors": errors,
    }, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
