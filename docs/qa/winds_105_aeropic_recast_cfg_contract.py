#!/usr/bin/env python3
"""Independent SHA-exact Aeropic normal-CFG evidence contract; no runtime claims."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import winds_105_spell_metadata as physical

TOP = {
    "result": "PASS_SHA_EXACT_AEROPIC_NORMAL_CFG_TOPOLOGY_AUDIT",
    "provider": "wind_spellbooks", "release": "1.0.5",
    "sha1": physical.EXPECTED_SHA1,
    "scope": "NORMAL_CFG_GEOMETRY_NOT_OPERAND_STACK_PROOF",
    "bytecode_or_offsets_redistributed": False,
    "installed_host_checksum": "NOT_VERIFIED",
    "runtime_receiver_class": "NOT_PROVEN",
    "safe_mutating_hook": "NOT_PROVEN",
    "physical_gameplay": "NOT_TESTED",
}

ROWS = {
    "applyEffectTick": {
        "instruction_count": 288,
        "conditional_and_direct_jump_count": 20,
        "normal_entry_reachable_instructions": 288,
        "normal_routes_reaching_recast_instructions": 222,
        "normal_route_join_instruction_count": 5,
        "supplier_field_reads_total": 3,
        "supplier_field_reads_on_some_normal_route": 3,
        "supplier_field_reads_dominating_recast": 1,
    },
    "onEffectAdded": {
        "instruction_count": 43,
        "conditional_and_direct_jump_count": 2,
        "normal_entry_reachable_instructions": 43,
        "normal_routes_reaching_recast_instructions": 34,
        "normal_route_join_instruction_count": 0,
        "supplier_field_reads_total": 1,
        "supplier_field_reads_on_some_normal_route": 1,
        "supplier_field_reads_dominating_recast": 1,
    },
}

SAFE_ROW = {
    "recast_reachable_on_normal_cfg": True,
    "cfg_evidence_grade": "BOUNDED_NORMAL_CFG_TOPOLOGY_ONLY",
    "non_proof_reasons": [],
    "compiled_receiver_source": "NOT_PROVEN_BY_CFG_TOPOLOGY",
    "return_value_to_PlayerRecasts": "NOT_PROVEN",
    "dynamic_override_executed": "NOT_PROVEN",
    "safe_mutating_hook": "NOT_PROVEN",
}

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    if not isinstance(doc, dict):
        raise ContractError("invalid result type")
    for key, expected in TOP.items():
        if doc.get(key) != expected:
            raise ContractError("release, scope or authority drift: " + key)
    sites = doc.get("call_sites")
    if not isinstance(sites, dict) or set(sites) != set(ROWS):
        raise ContractError("exactly two recast callsites required")
    for method, counts in ROWS.items():
        observed = sites[method]
        if not isinstance(observed, dict) or observed.get("method") != method:
            raise ContractError("wrong callsite identity: " + method)
        for key, expected in {**counts, **SAFE_ROW}.items():
            if type(observed.get(key)) is not type(expected) or observed.get(key) != expected:
                raise ContractError("frozen evidence or proof drift: " + method + "." + key)
    return len(sites)

def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--json", type=Path, required=True)
    args = cli.parse_args()
    try:
        count = validate(json.loads(args.json.read_text(encoding="utf8")))
    except (ContractError, ValueError, TypeError, KeyError, OSError) as exc:
        print("FAIL_CLOSED: " + str(exc))
        return 1
    print("PASS: %d pinned SHA-exact Aeropic CFG sites, no receiver dataflow or mutator proof" % count)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
