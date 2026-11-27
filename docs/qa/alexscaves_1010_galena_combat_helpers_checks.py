#!/usr/bin/env python3
"""Fail-closed publisher-only verification of 14 Galena ACCompat helper bodies.

Pins the immutable 1.0.10 publisher, full report, 21 typed caller sites,
14 entire native methods, exact invokedynamic bootstrap lambda and 34 JVM
semantic pivots. Does not certify Galena item, engine outcomes, hooks or QA.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

REPORT_SHA = "a88dbcda0906f344ecfcd8d4ecea0ea7ba0babae2013643f938a1a2604861bfa"
REPORT_BYTES = 44637
PUBLISHER_SHA = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
CLASS_SHA = "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b"
CALLER_SHA = "c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9"
OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
REPORT_SCOPE = "GALENA_ACCOMPAT_COMBAT_BRIDGES_DISCOVERY_NOT_CERTIFIED"
SEAL_SCOPE = "ALEXSCAVES_1010_GALENA_ACCOMPAT_COMBAT_BRIDGES_STATIC_SUBCONTRACT"
NAMES = frozenset({
    "addCooldown", "attackDamageBonus", "createEntity", "damageBonus",
    "enchantLevel", "enchantLevelOn", "hurt", "hurtAndBreakUsedHand",
    "knockback", "miningEfficiencyBonus", "postAttackEffects",
    "submergedMiningFactor", "useConsume", "useFail",
})
STATE = {
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "perk_certification": "NOT_CERTIFIED", "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION", "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0, "engine_effects": "NOT_VERIFIED",
    "installed_runtime": "NOT_VERIFIED",
}
LIMITS = {
    "delegated_engine_damage_acceptance": "NOT_VERIFIED",
    "delegated_armor_and_attributes": "NOT_VERIFIED",
    "delegated_neoforge_event_and_mining": "NOT_VERIFIED",
    "world_and_inventory_safety": "NOT_VERIFIED",
    "installed_runtime_transformations": "NOT_VERIFIED",
    "other_consumers_complete": False,
}

def need(test, message):
    if not test:
        raise ValueError(message)

def unique(pairs):
    values = {}
    for key, value in pairs:
        need(key not in values, "duplicate JSON key " + key)
        values[key] = value
    return values

def load(path: Path, size: int):
    raw = path.read_bytes()
    need(0 < len(raw) <= size, "report or seal size limit")
    return json.loads(raw, object_pairs_hook=unique), raw

def canonical(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf8")

def sha(b):
    return hashlib.sha256(b).hexdigest()

def method_check(body, spec, *, label):
    decl = body["declaration"]
    need(decl["name"] == spec["name"] and decl["descriptor"] == spec["descriptor"],
         "method signature drift " + label)
    need(decl["code_sha256"] == spec["code_sha256"],
         "method original Code digest drift " + label)
    instructions = body["instructions"]
    need(body["instruction_count"] == spec["instruction_count"] == len(instructions),
         "method instruction count drift " + label)
    need(body["instruction_sha256"] == spec["instruction_sha256"] ==
         sha(canonical(instructions)), "method instruction seal drift " + label)
    offsets = [row["offset"] for row in instructions]
    need(offsets == sorted(set(offsets)), "JVM offsets ambiguous " + label)
    actual = {row["offset"]: row for row in instructions}
    seen = set()
    for pivot in spec["pivots"]:
        off = pivot["offset"]
        need(off not in seen, "duplicate expected pivot " + label)
        seen.add(off)
        row = actual.get(off)
        need(row is not None and row["opcode"] == pivot["opcode"] and
             pivot["fragment"] in str(row["operand"]) + " " + str(row["symbol"]),
             "causal JVM pivot drift " + label + " @" + str(off))
    return len(seen)

def validate(report, seal, *, raw=None, strict=True):
    need(seal["schema_version"] == report["schema_version"] == 1, "schema version")
    need(seal["scope"] == SEAL_SCOPE and report["scope"] == REPORT_SCOPE,
         "evidence scope drift")
    proof = seal["report"]
    need(proof["sha256"] == REPORT_SHA and proof["bytes"] == REPORT_BYTES and
         proof["caller_sha256"] == CALLER_SHA and proof["caller_bytes"] == 1780492 and
         proof["run_id"] == 45175127051 and proof["job_id"] == 137694263147 and
         proof["artifact_id"] == 14817659241, "immutable provenance drift")
    if strict:
        need(raw is not None and len(raw) == REPORT_BYTES and
             sha(raw) == REPORT_SHA, "publisher report SHA/size drift")
    art = report["artifact"]
    need(art == seal["publisher"] and art["sha256"] == PUBLISHER_SHA and
         art["size_bytes"] == 75279314 and art["version"] == "1.0.10" and
         art["installed_dump_parity"] == "NOT_VERIFIED", "publisher identity drift")
    need(seal["states"] == STATE, "unsafe boundary-state drift")
    for k in ("static_contract", "mutating_hook", "perk_certification",
              "physical_qa", "mutation", "provider_universe_closed",
              "semantic_magic_roots_delta"):
        need(report[k] == STATE[k], "report unsafe state " + k)
    need(report["limits"] == LIMITS, "unverified external dependency promoted")
    cl = report["class"]
    class_ident = {k:cl[k] for k in ("owner", "sha256", "major",
                                     "declared_methods", "fields")}
    need(class_ident == seal["class"] == {
        "owner": OWNER, "sha256": CLASS_SHA, "major": 65,
        "declared_methods": 200, "fields": 3
    }, "native helper classfile identity drift")
    bodies = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m
              for m in cl["selected_methods"]}
    specs = seal["methods"]
    need(len(specs) == len(bodies) == len(cl["selected_methods"]) == 14,
         "selected method roster cardinality drift")
    need({x["name"] for x in specs} == NAMES and
         len({(x["name"], x["descriptor"]) for x in specs}) == 14,
         "selected method signature set drift")
    need(set(bodies) == {(x["name"], x["descriptor"]) for x in specs},
         "native callable method signature drift")
    total = 0
    for s in specs:
        total += method_check(bodies[(s["name"], s["descriptor"])], s, label=s["name"])
    cb = cl["attack_damage_bootstrap_callback"]
    spec_cb = seal["attack_damage_callback"]
    handle = cb["resolved_handle"]
    need(cb["bootstrap_index"] == spec_cb["bootstrap_index"] == 2 and
         handle["owner"] == OWNER and handle["name"] == spec_cb["name"] and
         handle["descriptor"] == spec_cb["descriptor"] and
         handle["name"].startswith("lambda$attackDamageBonus$") and
         handle["reference_kind"] == 6,
         "invokedynamic bootstrap handle drift")
    need({x["declaration"]["name"] for x in cl["selected_methods"]} == NAMES,
         "direct helper overlap/ambiguity")
    total += method_check(cb["method"], spec_cb,
                          label="attackDamageBonus invokedynamic callback")
    need(total == 34, "causal pivot total drift: " + str(total))
    calls = report["caller_evidence"]
    need(calls["source_sha256"] == CALLER_SHA and
         calls["source_bytes"] == 1780492, "caller evidence changed")
    projection = ("caller_owner", "caller_name", "offset", "callee_name",
                  "callee_descriptor")
    actual = [{key:site[key] for key in projection} for site in calls["typed_callsites"]]
    need(actual == seal["typed_caller_sites"] and len(actual) == 21,
         "21 typed Galena caller sites drift")
    need(all(s["opcode"] == "invokestatic" for s in calls["typed_callsites"]),
         "caller JVM opcode drift")
    need({(x["callee_name"], x["callee_descriptor"]) for x in actual}
         == set(bodies), "caller/helper target descriptor mismatch")
    need({x["callee_name"] for x in actual} == NAMES,
         "uncovered selected helper")
    return total

def adversarial(original, original_seal):
    cases=[]
    def case(label, fn, expected=None):
        cases.append((label,fn,expected))
    for name in sorted(NAMES):
        spec = next(x for x in original_seal["methods"] if x["name"] == name)
        pivot = spec["pivots"][0]
        def mutate_report(report, seal, key=name, offset=pivot["offset"]):
            method = next(x for x in report["class"]["selected_methods"]
                          if x["declaration"]["name"] == key)
            ins = next(x for x in method["instructions"] if x["offset"] == offset)
            ins["opcode"] = "nop"
            method["instruction_sha256"] = sha(canonical(method["instructions"]))
            next(x for x in seal["methods"] if x["name"] == key)["instruction_sha256"] = method["instruction_sha256"]
        case("forged re-sealed helper " + name,mutate_report,"causal JVM pivot")
    def alter_callback(report, seal):
        cb = report["class"]["attack_damage_bootstrap_callback"]["method"]
        pivot=next(x for x in cb["instructions"] if x["offset"] == 22)
        pivot["opcode"]="nop"
        cb["instruction_sha256"]=sha(canonical(cb["instructions"]))
        seal["attack_damage_callback"]["instruction_sha256"]=cb["instruction_sha256"]
    case("forged re-sealed lambda",alter_callback,"causal JVM pivot")
    case("fabricated addon hook",lambda r,s:s["states"].__setitem__("mutating_hook","VERIFIED"))
    case("fabricated physical QA",lambda r,s:s["states"].__setitem__("physical_qa","PASSED"))
    case("fabricated engine",lambda r,s:s["states"].__setitem__("engine_effects","VERIFIED"))
    case("fabricated provider closure",lambda r,s:s["states"].__setitem__("provider_universe_closed",True))
    case("fabricated root",lambda r,s:s["states"].__setitem__("semantic_magic_roots_delta",1))
    case("wrong callback bootstrap",lambda r,s:r["class"]["attack_damage_bootstrap_callback"].__setitem__("bootstrap_index",3))
    case("wrong caller offset",lambda r,s:r["caller_evidence"]["typed_callsites"][0].__setitem__("offset",9999))
    case("wrong helper method descriptor",lambda r,s:s["methods"][0].__setitem__("descriptor","()V"))
    case("wrong publisher",lambda r,s:r["artifact"].__setitem__("sha256","0"*64))
    case("wrong native class",lambda r,s:r["class"].__setitem__("sha256","0"*64))
    case("wrong report scope",lambda r,s:r.__setitem__("scope","EXECUTABLE"))
    case("missing method",lambda r,s:r["class"]["selected_methods"].pop())
    case("wrong class flags",lambda r,s:r["class"].__setitem__("declared_methods",199))
    case("wrong evidence id",lambda r,s:s["report"].__setitem__("caller_sha256","0"*64))
    rejected=0
    for label,mutator,expected in cases:
        r,s=copy.deepcopy((original,original_seal))
        mutator(r,s)
        try:
            validate(r,s,strict=False)
        except (ValueError,KeyError,TypeError,AssertionError,IndexError) as exc:
            if expected is not None:
                need(expected in str(exc), "wrong rejection gate: "+label+" "+str(exc))
            rejected+=1
        else:
            raise AssertionError("forged audit report accepted: " + label)
    need(rejected == len(cases) and rejected >= 25,
         "negative fixture count incomplete")
    return rejected

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",required=True,type=Path)
    p.add_argument("--manifest",required=True,type=Path)
    p.add_argument("--adversarial",action="store_true")
    args=p.parse_args()
    report, raw = load(args.report,100_000)
    seal, _ = load(args.manifest,90_000)
    pivots=validate(report,seal,raw=raw)
    negative=adversarial(report,seal) if args.adversarial else 0
    print("PASS: 14 SHA-exact Galena helpers, 1 bootstrap lambda, 21 caller sites,",
          pivots,"JVM pivots; adversarial rejected",negative)
    print("LIMITS STATIC_SUBCONTRACT_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")

if __name__ == "__main__":
    main()
