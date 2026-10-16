#!/usr/bin/env python3
"""Fail-closed parser for optional Iron's event-phase observer logs.

All example traces in tests are SYNTHETIC. This parser neither runs Minecraft
nor attributes accepted damage / Mastery. No provider session ID is invented.
"""
import argparse
import json
import re
from pathlib import Path

TAG = "[BLACK_ARCANA_PHASE_QA]"
HASH_TAG = "[BLACK_ARCANA_ARROW_VOLLEY_QA]"
EXPECTED_SHA = "13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73"
EXPECTED_BYTES = 13890046

FIELDS = {
    "cast": ("actor_slot", "session_slot", "classification", "prior_recast",
             "tick", "original_level", "event_level_snapshot"),
    "cast_followup": ("actor_slot", "session_slot", "tick", "recast_after",
                      "mana_after_snapshot"),
    "damage_followup": ("attempt_slot", "actor_slot", "target_slot", "tick",
                        "cancelled_event_snapshot", "post_hits", "ambiguous",
                        "iframe_at_event", "iframe_at_post_tick"),
}


def attr(line, key):
    match = re.search(r"(?:^|\s)" + re.escape(key) + r"=([^\s]+)", line)
    if not match:
        raise ValueError(f"Missing {key}")
    return match.group(1)


def verify_fingerprint(lines):
    refs = [line for line in lines
            if HASH_TAG in line and "type=provider_fingerprint " in line
            and "mod_id=irons_spellbooks " in line]
    if len(refs) != 1:
        return False
    try:
        line = refs[0]
        return (attr(line, "status") == "OBSERVED"
                and attr(line, "expected_match") == "true"
                and attr(line, "sha256") == EXPECTED_SHA
                and int(attr(line, "bytes")) == EXPECTED_BYTES)
    except ValueError:
        return False


def assess(log):
    lines = log.splitlines()
    fail = []
    fingerprint = verify_fingerprint(lines)
    if not fingerprint:
        fail.append("PROVIDER_FINGERPRINT_UNVERIFIED")
    events = []
    for line in lines:
        if TAG not in line:
            continue
        if "type=armed " in line:
            continue
        kind = attr(line, "type")
        if kind not in FIELDS:
            fail.append("UNKNOWN_OBSERVER_EVENT_TYPE")
            continue
        record = {"type": kind}
        for name in FIELDS[kind]:
            record[name] = attr(line, name)
        events.append(record)
    if not events:
        fail.append("NO_OBSERVED_PHASE_EVENTS")
    casts = [e for e in events if e["type"] == "cast"]
    followups = [e for e in events if e["type"] == "cast_followup"]
    damage = [e for e in events if e["type"] == "damage_followup"]
    sessions = {}
    for event in casts:
        slot = event["session_slot"]
        classification = event["classification"]
        if classification not in ("ROOT_CANDIDATE", "RECAST_CANDIDATE",
                                  "UNLINKED_RECAST"):
            fail.append("UNKNOWN_CAST_CLASSIFICATION")
            continue
        try:
            tick = int(event["tick"])
            actor = int(event["actor_slot"])
            session = int(slot)
            level = int(event["event_level_snapshot"])
            if not (0 < actor <= 8 and session >= 0 and tick >= 0
                    and 1 <= level <= 5):
                fail.append("CAST_FIELDS_OUT_OF_RANGE")
        except ValueError:
            fail.append("CAST_FIELDS_OUT_OF_RANGE")
            continue
        if classification == "UNLINKED_RECAST":
            fail.append("UNLINKED_RECAST_CANNOT_CREDIT_ROOT")
            continue
        if slot not in sessions:
            if classification != "ROOT_CANDIDATE" or event["prior_recast"] != "false":
                fail.append("MISSING_ROOT_FOR_RECAST")
            sessions[slot] = {"actor": event["actor_slot"], "root": 0,
                              "recasts": 0, "last": tick}
        session_data = sessions[slot]
        if session_data["actor"] != event["actor_slot"]:
            fail.append("SESSION_ACTOR_CHANGED")
        if tick < session_data["last"]:
            fail.append("NONMONOTONIC_CAST_TIME")
        session_data["last"] = tick
        if classification == "ROOT_CANDIDATE":
            session_data["root"] += 1
            if event["prior_recast"] != "false":
                fail.append("ROOT_HAS_EXISTING_RECAST")
        else:
            session_data["recasts"] += 1
            if event["prior_recast"] != "true":
                fail.append("RECAST_WITHOUT_PROVIDER_STATE")
    for slot, value in sessions.items():
        if value["root"] != 1:
            fail.append("SESSION_REQUIRES_EXACTLY_ONE_ROOT")
    followup_keys = [(v["actor_slot"], v["session_slot"], v["tick"])
                     for v in followups]
    if len(followup_keys) != len(set(followup_keys)):
        fail.append("DUPLICATE_CAST_FOLLOWUP")
    if casts and not followups:
        fail.append("NO_CAST_FOLLOWUP")
    for value in followups:
        if value["session_slot"] not in sessions:
            fail.append("FOLLOWUP_WITHOUT_ROOT")
        if value["recast_after"] not in ("true", "false"):
            fail.append("INVALID_RECAST_AFTER")
    for value in damage:
        if value["cancelled_event_snapshot"] not in ("true", "false")                 or value["ambiguous"] not in ("true", "false"):
            fail.append("INVALID_DAMAGE_FLAGS")
        try:
            hits = int(value["post_hits"])
            before = int(value["iframe_at_event"])
            after = int(value["iframe_at_post_tick"])
            if hits < 0 or before < 0 or after < 0:
                fail.append("NEGATIVE_DAMAGE_METRIC")
        except ValueError:
            fail.append("INVALID_DAMAGE_METRIC")
        if value["ambiguous"] == "true":
            fail.append("AMBIGUOUS_HIT_CORRELATION")
        if int(value["post_hits"]) > 1:
            fail.append("MULTIPLE_POST_HITS_IN_ONE_ATTEMPT")
    return {
        "result": "TRACE_CLASSIFIED_NOT_GAMETEST" if not fail else "FAIL_CLOSED",
        "fingerprint_claim_in_log_matches_publisher": fingerprint,
        "cast_events": len(casts), "damage_followups": len(damage),
        "candidate_sessions": len(sessions), "issues": sorted(set(fail)),
        "limits": [
            "No client/server GameTest performed by this parser",
            "Observer session numbers are local, not native provider IDs",
            "Cancellation reflects an event-bus snapshot, not guaranteed final state",
            "Post-hit and i-frame correlation are observational, not causal proof",
            "A matching checksum printed in logs does not authenticate the log origin",
            "No Mastery reward or damage acceptance is approved by this parser",
        ],
    }


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--log", type=Path, required=True)
    cli.add_argument("--report", type=Path)
    args = cli.parse_args()
    try:
        result = assess(args.log.read_text())
        doc = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(doc)
        print(doc, end="")
        if result["issues"]:
            cli.exit(1, "FAIL_CLOSED: trace must not be promoted\n")
    except (OSError, ValueError) as e:
        cli.exit(2, f"FAIL_CLOSED: malformed trace: {e}\n")


if __name__ == "__main__":
    main()
