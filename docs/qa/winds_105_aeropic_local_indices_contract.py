#!/usr/bin/env python3
"""Freeze reviewed SHA-exact local-index Aeropic results without runtime claims."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as physical

EXPECTED = {
    "applyEffectTick": {
        "all_load_store_instructions": 111,
        "unsuffixed_load_store_indices_parsed": 77,
        "compiled_receiver_probe": "NOT_PROVEN",
        "probe_non_proof_reason": "FAIL_CLOSED_control flow or return in candidate stack slice",
    },
    "onEffectAdded": {
        "all_load_store_instructions": 18,
        "unsuffixed_load_store_indices_parsed": 6,
        "compiled_receiver_probe": "COMPILED_SUPPLIER_GET_CAST_RECEIVER",
        "probe_non_proof_reason": None,
    },
}
FIXED = {
    "result": "PASS_EXACT_JAR_AEROPIC_LOCAL_INDEX_PROBE",
    "provider": "wind_spellbooks",
    "release": "1.0.5",
    "sha1": physical.EXPECTED_SHA1,
    "original_negative_contract_unchanged": True,
    "installed_host_checksum": "NOT_VERIFIED",
    "runtime_dispatch": "NOT_PROVEN",
    "physical_gameplay": "NOT_TESTED",
    "safe_mutating_hook": "NOT_PROVEN",
    "published_provider_bytecode": False,
}

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    if not isinstance(doc, dict):
        raise ContractError("invalid JSON document")
    for key, value in FIXED.items():
        if doc.get(key) != value:
            raise ContractError("frozen release or runtime authority drift: " + key)
    sites = doc.get("call_sites")
    if not isinstance(sites, dict) or set(sites) != set(EXPECTED):
        raise ContractError("expected exactly two Aeropic recast callsites")
    for method, values in EXPECTED.items():
        row = sites[method]
        if not isinstance(row, dict):
            raise ContractError("missing Aeropic callsite row: " + method)
        for key, value in values.items():
            if row.get(key, object()) != value:
                raise ContractError("compiled provenance drift: " + method + "." + key)
        required = {
            "method": method,
            "operand_index_state": "EXACT_EXPLICIT_INDICES_OR_COMPACT_SUFFIX",
            "binary_candidate_requires_manual_review": True,
            "dynamic_override_executed": "NOT_PROVEN",
            "return_value_to_PlayerRecasts": "NOT_PROVEN",
            "safe_mutating_hook": "NOT_PROVEN",
        }
        for key, value in required.items():
            if row.get(key) != value:
                raise ContractError("unsafe authority or consumer promotion: " + method + "." + key)
    return len(EXPECTED)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", type=Path, required=True)
    args = p.parse_args()
    try:
        count = validate(json.loads(args.json.read_text(encoding="utf8")))
    except (ContractError, KeyError, OSError, TypeError, ValueError) as exc:
        print("FAIL_CLOSED: " + str(exc))
        return 1
    print("PASS: %d exact Aeropic JVM callsites frozen; runtime and hooks NOT_PROVEN" % count)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
