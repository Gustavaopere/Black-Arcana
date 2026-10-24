#!/usr/bin/env python3
"""Frozen clean-room direct-invoke count contract for the exact Wind 1.0.5 JAR.

Zero cross-class direct calls in THIS namespace is not zero gameplay consumers.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as binary
import winds_105_getter_consumer_edges as edges

CALL_COUNTS = {
    "aeropic": {"getRecastCount": 1},
    "almighty_push": {"getDuration": 2, "getRange": 2},
    "iron_slash": {"getDistance": 2},
    "tailwind": {"getPercentAirSpeed": 1, "getPercentJump": 1},
    "tornado": {"getDuration": 2},
    "wind_jump": {"getFloatDuration": 3, "getJumpStrength": 2},
}
CLASS_COUNT = 64
INVOKE_COUNT = 16

class ContractError(ValueError):
    pass

def validate(document: dict) -> int:
    if not isinstance(document, dict):
        raise ContractError("not a JSON object")
    for key, expected in {
        "result": "PASS_SHA_EXACT_CROSS_CLASS_DIRECT_CALL_INVENTORY",
        "sha1": binary.EXPECTED_SHA1,
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "classes_inspected": CLASS_COUNT,
        "getters_scoped": 9,
        "explicit_invokes_found": INVOKE_COUNT,
        "out_of_declaring_spell_invokes": 0,
    }.items():
        if document.get(key) != expected:
            raise ContractError("JAR direct-call evidence differs at " + key)
    got = document.get("selected_getters")
    if not isinstance(got, dict) or set(got) != set(CALL_COUNTS):
        raise ContractError("wrong getter spell roster")
    total = 0
    for spell, getters in CALL_COUNTS.items():
        actual = got.get(spell)
        if not isinstance(actual, dict) or set(actual) != set(getters):
            raise ContractError("wrong getter method roster for " + spell)
        owner = binary.BASE + binary.ROSTER[spell]
        for getter, expected_count in getters.items():
            record = actual[getter]
            if record.get("runtime_getter_to_sink_flow") != "NOT_PROVEN":
                raise ContractError("false causal-flow promotion: " + spell + "." + getter)
            calls = record.get("direct_calls")
            if not isinstance(calls, list) or len(calls) != expected_count:
                raise ContractError("changed direct invoke instruction count")
            if record.get("calls_outside_declaring_spell_class") != 0:
                raise ContractError("changed cross-class direct invoke count")
            allowed = edges.GETTERS[spell][getter]
            expected_ref = owner.replace(".", "/") + "." + getter + ":" + allowed
            for call in calls:
                if (call.get("caller_class") != owner
                        or call.get("callee_spell") != spell
                        or call.get("callee_getter") != getter
                        or call.get("callee_jvm_ref") != expected_ref
                        or call.get("evidence") != "DIRECT_COMPILED_INVOKE_ONLY"):
                    raise ContractError("callsite provenance drift")
            total += len(calls)
    if total != INVOKE_COUNT:
        raise ContractError("inconsistent total invoke count")
    return total

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",type=Path,required=True)
    args=parser.parse_args()
    try:
        count=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ContractError,OSError,ValueError,TypeError) as exc:
        print("FAIL_CLOSED: " + str(exc))
        return 1
    print(f"PASS: {CLASS_COUNT} Wind classes; {count} JVM direct invoke instructions; 0 provider-internal cross-class invokes; no gameplay or perks inference")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
