#!/usr/bin/env python3
"""Raygun 1.0.10: bounded physical-JAR charge and use-tick evidence.

Reuses the fully sealed 26-method native roster and prior normal-CFG manifest.
This is discovery of cost sites, not general symbolic execution, authority for
C2S charge, a perk hook, or a gameplay/QA certification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_all_method_seal import ARTIFACT, OWNER, CLASS_SHA256, load
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_raygun_hit_outcomes_cfg_probe import (
    audit as replay_historical_audit, verify_snapshot as verify_historical,
    require,
)

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / ("wiki/modpack-catalog/providers/✅-alexs-caves-continued/"
                   "EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json")
SCOPE = "SHA_EXACT_1010_RAYGUN_USE_TICK_CHARGE_CONSUMER_DISCOVERY_ONLY"
METHODS = (
    "onUseTick", "acInventoryTick", "use", "hasCharge", "getCharge",
    "setCharge", "getUseTime", "setUseTime", "getBarWidth",
)
NEEDLES = (
    "getCharge:", "setCharge:", "getUseTime:", "setUseTime:",
    "hasCharge:", ".ENERGY_EFFICIENCY:", "enchantLevel:",
    "ChargeUsed", "UseTime",
)
MAX_SITES_PER_METHOD = 22
MAX_REPORT_BYTES = 36000

def slim(row):
    return {key: row[key][:320] if isinstance(row[key], str) else row[key]
            for key in ("offset", "opcode", "operand", "symbol")}

def selected_sites(method):
    rows = method["instructions"]
    offsets = [x["offset"] for x in rows]
    require(bool(rows) and offsets == sorted(set(offsets)),
            "duplicate/invalid charge method JVM offsets")
    matches = [
        i for i, r in enumerate(rows)
        if any(needle in r["symbol"] or needle in r["operand"] for needle in NEEDLES)
    ]
    require(len(matches) <= MAX_SITES_PER_METHOD,
            "unbounded charge-related reference count")
    return [{
        "offset": rows[i]["offset"],
        "site": slim(rows[i]),
        "before": [slim(row) for row in rows[max(0, i - 6):i]],
        "after": [slim(row) for row in rows[i + 1:i + 7]],
    } for i in matches]

def selected_instruction_window(method, start, end):
    """A bounded operator/reference view, never an entire method body."""
    require(start < end and end-start <= 85, "unbounded charge window")
    relevant = []
    for row in method["instructions"]:
        if not start <= row["offset"] < end:
            continue
        op = row["opcode"]
        if (op.startswith(("if", "invoke", "iconst_", "fconst_", "iload", "istore",
                           "fload", "fstore")) or op in {
                           "goto", "getstatic", "getfield", "putfield",
                           "sipush", "bipush", "ldc", "ldc_w", "iadd", "isub",
                           "imul", "idiv", "irem", "fadd", "fsub", "fmul",
                           "fdiv", "i2f", "f2i", "f2d", "i2d", "fcmpg", "fcmpl",
                           "dup", "aconst_null",
                           }):
            relevant.append(slim(row))
    require(len(relevant) <= 70, "charge selected operator budget exceeded")
    return relevant

def projection(methods):
    by_name = {}
    for m in methods:
        ident = name_of(m)
        require(ident not in by_name, "ambiguous overloaded charge method " + ident)
        by_name[ident] = m
    require(all(name in by_name for name in METHODS), "Raygun charge method missing")
    onuse = by_name["onUseTick"]
    require(any(x["offset"] == 246 and "ENERGY_EFFICIENCY" in x["symbol"]
                for x in onuse["instructions"]), "Energy Efficiency native anchor drift")
    output = []
    for name in METHODS:
        m = by_name[name]
        relevant = selected_sites(m)
        output.append({
            "name": name,
            "descriptor": m["descriptor"],
            "parsed_method_sha256": digest_method(m),
            "instruction_count": len(m["instructions"]),
            "charge_related_references": relevant,
        })
    return {
        "selected_methods": output,
        "onUseTick_energy_efficiency_operator_window":
            selected_instruction_window(onuse, 222, 295),
        "onUseTick_activation_operator_window":
            selected_instruction_window(onuse, 130, 190),
        "charge_related_site_count": sum(len(x["charge_related_references"])
                                         for x in output),
    }

def audit(jar: Path, javap_bin: str):
    prior = replay_historical_audit(jar, javap_bin)
    verify_historical(prior, load(BASELINE))
    methods = parse_methods(javap(javap_bin, jar, OWNER[:-6].replace("/", ".")))
    require(len(methods) == 26, "Raygun physical class method population drift")
    evidence = projection(methods)
    require(evidence["charge_related_site_count"] > 0,
            "no native charge references discovered")
    result = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": ARTIFACT,
        "class_path": OWNER,
        "class_sha256": CLASS_SHA256,
        "baseline_snapshot": BASELINE.name,
        "observations": evidence,
        "limitations": {
            "charge_per_tick_formula": "NOT_CERTIFIED_UNTIL_JVM_CAUSAL_INTERPRETATION",
            "energy_efficiency_cost_impact": "NOT_CERTIFIED",
            "same_tick_multiple_calls": "NOT_RECONSTRUCTED",
            "server_owned_charge": "NOT_VERIFIED",
            "packet_replay_and_tag_authorization": "NOT_VERIFIED",
            "exceptional_cfg_and_transformed_runtime": "NOT_VERIFIED",
            "perk_static_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
        },
    }
    require(len(json.dumps(result, ensure_ascii=False).encode("utf8")) <= MAX_REPORT_BYTES,
            "clean-room output budget exceeded")
    return result

def verify_snapshot(actual, expected):
    require(actual == expected, "Raygun exact charge cost snapshot drift")
    return actual

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--snapshot", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--print-candidate", action="store_true")
    args = p.parse_args()
    report = audit(args.jar, args.javap)
    if args.snapshot:
        verify_snapshot(report, load(args.snapshot))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",
                               encoding="utf8")
    if args.print_candidate:
        print("RAYGUN_CHARGE_COST_BEGIN")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("RAYGUN_CHARGE_COST_END")
    print(json.dumps({
        "result": "SHA_EXACT_CHARGE_COST_SNAPSHOT_VERIFIED" if args.snapshot
                  else "UNSEALED_CHARGE_COST_DISCOVERY",
        "methods": len(report["observations"]["selected_methods"]),
        "selected_refs": report["observations"]["charge_related_site_count"],
        "safety": report["limitations"]["mutation"],
    }))

if __name__ == "__main__":
    main()
