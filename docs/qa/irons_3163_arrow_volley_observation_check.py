#!/usr/bin/env python3
"""Classify one passive Arrow Volley QA trace without fabricating gameplay evidence.

This consumes only the bounded companion's log summary. A matching trace is
evidence that must still be tied to a real modpack fingerprint, test conditions,
and NeoForge version; it is never an automatic Stage acceptance.
"""
import argparse
import json
import re
from pathlib import Path

TAG = "[BLACK_ARCANA_ARROW_VOLLEY_QA]"
EXPECTED_IRONS_SHA256 = "13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73"
EXPECTED_IRONS_BYTES = 13890046
LOG_FIELDS = (
    "controller", "join_game_tick", "controller_join_age", "status",
    "observed_ticks", "first_age", "last_age",
    "age_monotonic", "sample_gaps", "age_step_mismatches",
    "nonfresh_arrow_joins", "candidate_joins", "confirmed_present_at_post",
    "ambiguous_joins", "candidate_budget_exceeded", "leave_seen", "removal"
)


def field(line, name):
    match = re.search(r"\b" + re.escape(name) + r"=([^\s]+)", line)
    if not match:
        raise ValueError(f"Missing {name}")
    return match.group(1)


def parse_rows(line):
    match = re.search(r"\bjoin_counts_per_tick=\{([^}]*)\}", line)
    if not match:
        raise ValueError("Missing join_counts_per_tick map")
    pairs = []
    if match.group(1).strip():
        for token in match.group(1).split(","):
            match_pair = re.fullmatch(r"\s*(\d+)=(\d+)\s*", token)
            if not match_pair:
                raise ValueError("Invalid tick count map entry")
            pairs.append((int(match_pair.group(1)), int(match_pair.group(2))))
    return pairs


def provider_fingerprint_valid(text):
    lines = [line for line in text.splitlines()
             if TAG in line and "type=provider_fingerprint " in line
             and "mod_id=irons_spellbooks " in line]
    if len(lines) != 1:
        return False
    line = lines[0]
    try:
        return (field(line, "status") == "OBSERVED"
                and field(line, "expected_match") == "true"
                and field(line, "sha256") == EXPECTED_IRONS_SHA256
                and int(field(line, "bytes")) == EXPECTED_IRONS_BYTES)
    except ValueError:
        return False


def evaluate(text, level, controller=None):
    if level not in range(1, 7):
        raise ValueError("Level must be 1..6")
    traces = [line for line in text.splitlines()
              if TAG in line and "type=end " in line]
    if controller:
        traces = [line for line in traces
                  if field(line, "controller") == controller]
    if len(traces) != 1:
        raise ValueError(f"Expected exactly one complete session, found {len(traces)}")
    line = traces[0]
    obj = {key: field(line, key) for key in LOG_FIELDS}
    rows = parse_rows(line)
    expected_rows = level + 4
    per_row = 5 + level // 2
    expected = expected_rows * per_row
    actual = int(obj["candidate_joins"])
    confirmed = int(obj["confirmed_present_at_post"])
    reasons = []
    fp_verified = provider_fingerprint_valid(text)
    if not fp_verified:
        reasons.append("PROVIDER_FINGERPRINT_UNVERIFIED")
    if obj["status"] != "LEFT_LEVEL" or not obj["leave_seen"] == "true":
        reasons.append("NO_CONFIRMED_LEAVE_EVENT")
    if obj["removal"] != "DISCARDED":
        reasons.append("UNEXPECTED_REMOVAL_REASON")
    if obj["age_monotonic"] != "true":
        reasons.append("AGE_NONMONOTONIC")
    if int(obj["last_age"]) < expected_rows * 5:
        reasons.append("INSUFFICIENT_CONTROLLER_TICKS")
    if obj["candidate_budget_exceeded"] != "false":
        reasons.append("CANDIDATE_BUDGET_EXCEEDED")
    if int(obj["ambiguous_joins"]) != 0:
        reasons.append("AMBIGUOUS_OWNER_PROXIMITY")
    if actual != expected or confirmed != expected:
        reasons.append("COUNT_NOT_CONFIRMED")
    if len(rows) != expected_rows or any(amount != per_row for _, amount in rows):
        reasons.append("ROW_PATTERN_MISMATCH")
    if any(rows[i][0] - rows[i-1][0] != 5 for i in range(1, len(rows))):
        reasons.append("ROW_INTERVAL_MISMATCH")
    # A stream with correct five-tick gaps can still be shifted arbitrarily.
    # Tie every reported row to the controller's observed world insertion tick.
    join_tick = int(obj["join_game_tick"])
    expected_last_row_age = expected_rows * 5
    actual_row_ticks = [tick for tick, _ in rows]
    expected_row_ticks = [join_tick + step * 5
                          for step in range(1, expected_rows + 1)]
    if actual_row_ticks != expected_row_ticks:
        reasons.append("ROW_START_OFFSET_MISMATCH")

    # At the server Post tick, initial age is expected to be 0 or 1
    # for a fresh controller. Later initial ages suggest a reload/skipped
    # sampling and may not be used to validate a complete new cast.
    if int(obj["controller_join_age"]) != 0:
        reasons.append("CONTROLLER_NONFRESH_JOIN")
    if int(obj["sample_gaps"]) != 0:
        reasons.append("CONTROLLER_SAMPLE_GAPS")
    if int(obj["age_step_mismatches"]) != 0:
        reasons.append("CONTROLLER_AGE_STEP_MISMATCH")
    if int(obj["nonfresh_arrow_joins"]) != 0:
        reasons.append("NONFRESH_ARROW_CANDIDATE")
    age_start = int(obj["first_age"])
    samples = int(obj["observed_ticks"])
    if age_start not in (0, 1) or samples < expected_last_row_age - 1:
        reasons.append("CONTROLLER_OBSERVATION_INCOMPLETE")
    age_end = int(obj["last_age"])
    if not expected_last_row_age <= age_end <= expected_last_row_age + 1:
        reasons.append("CONTROLLER_DISCARD_AGE_MISMATCH")

    if sum(n for _, n in rows) != actual:
        reasons.append("JOIN_SUMMARY_INCONSISTENT")
    return {
        "level": level,
        "controller": obj["controller"],
        "provider_fingerprint_matches_publisher_in_log": fp_verified,
        "expected_rows": expected_rows,
        "expected_arrows": expected,
        "candidate_join_count": actual,
        "confirmed_present_at_server_post": confirmed,
        "result": "TRACE_CONSISTENT_NOT_GAMETEST" if not reasons else "FAIL_CLOSED",
        "fail_reasons": reasons,
        "limits": [
            "Owner/proximity association is heuristic, not canonical cast ancestry",
            "Join event is an insertion attempt; post-tick presence is a limited check",
            "Matching Iron's checksum is a log claim; retain authentic log provenance",
            "NeoForge/pack fingerprint and physical acceptance still need independent QA",
            "This parser does not execute Minecraft or certify reload/chunk behavior",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", type=Path, required=True)
    p.add_argument("--spell-level", type=int, required=True)
    p.add_argument("--controller")
    p.add_argument("--report", type=Path)
    args = p.parse_args()
    try:
        result = evaluate(args.log.read_text(), args.spell_level, args.controller)
    except (OSError, ValueError) as e:
        p.exit(2, f"FAIL_CLOSED: {e}\n")
    report = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report)
    print(report, end="")
    if result["fail_reasons"]:
        p.exit(1, "FAIL_CLOSED: trace does not meet model acceptance\n")


if __name__ == "__main__":
    main()
