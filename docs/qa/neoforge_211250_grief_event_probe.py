#!/usr/bin/env python3
"""Read-only NeoForge 21.1.250 grief-event audit.

The SHA-exact 21.1.248 probe is reused for bytecode parsing and required
semantic anchors. Comparison to the previous baseline is descriptive only:
equal selected bytecode is not proof of compatibility with land claims.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from neoforge_211248_grief_event_probe import (
    EvidenceError, examine_jar as examine_previous,
    require, verify_seal as verify_previous,
)

VERSION = "21.1.250"
JAR_NAME = "neoforge-21.1.250-universal.jar"
BASELINE_SHA256 = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
SCOPE = "EXACT_NEOFORGE_211250_CAN_ENTITY_GRIEF_EVENT_BYTECODE"
LIMITS = {
    "deployed_modpack_class_loading": "NOT_OBSERVED",
    "third_party_claim_listeners": "NOT_VERIFIED",
    "claim_position_authorization": "NOT_VERIFIED",
    "black_arcana_world_effect_policy": "NOT_VERIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "perk_certification": "NOT_CERTIFIED",
}


def baseline_methods(manifest):
    require(manifest.get("scope") == "EXACT_NEOFORGE_211248_CAN_ENTITY_GRIEF_EVENT_BYTECODE",
            "wrong baseline scope")
    require(manifest.get("artifact", {}).get("sha256") == BASELINE_SHA256,
            "incorrect 21.1.248 baseline SHA-256")
    classes = manifest.get("classes")
    require(isinstance(classes, list) and len(classes) == 2,
            "unexpected baseline class universe")
    output = {}
    for cls in classes:
        owner = cls["owner"]
        require(owner not in output, "duplicate baseline owner")
        output[owner] = cls
    require(set(output) == {"EventHooks", "EntityMobGriefingEvent"},
            "incorrect baseline class names")
    require(sum(len(c["selected_methods"]) for c in classes) == 5,
            "unexpected baseline method count")
    return output


def compare_versions(report, baseline):
    base = baseline_methods(baseline)
    current = report["classes"]
    require(len(current) == 2 and {cls["owner"] for cls in current} == set(base),
            "21.1.250 class universe differs from selected baseline")
    class_rows = []
    method_rows = []
    for cls in current:
        old = base[cls["owner"]]
        require(cls["class_path"] == old["class_path"], "changed class path")
        previous = {(m["name"], m["descriptor"]): m for m in old["selected_methods"]}
        require(len(previous) == len(old["selected_methods"]),
                "duplicate baseline method identity")
        require(len(cls["selected_methods"]) == len(previous),
                "selected method population changed")
        class_rows.append({"owner": cls["owner"],
                           "class_sha256_equal": cls["class_sha256"] == old["class_sha256"]})
        for method in cls["selected_methods"]:
            key = (method["name"], method["descriptor"])
            require(key in previous, "selected method signature changed")
            before = previous[key]
            newrefs = method["selected_references"]
            oldrefs = before["selected_references"]
            method_rows.append({
                "owner": cls["owner"], "name": method["name"],
                "descriptor": method["descriptor"],
                "method_sha256_equal": method["method_sha256"] == before["method_sha256"],
                "instruction_count_equal": method["instruction_count"] == before["instruction_count"],
                "selected_references_exact_equal": newrefs == oldrefs,
                "selected_references_symbolic_sequence_equal":
                    [(x["opcode"], x["symbol"]) for x in newrefs] ==
                    [(x["opcode"], x["symbol"]) for x in oldrefs],
            })
    require(len(method_rows) == 5, "selected method comparison incomplete")
    return {
        "baseline": "net.neoforged:neoforge:21.1.248:universal",
        "baseline_artifact_sha256": BASELINE_SHA256,
        "class_comparison": class_rows,
        "method_comparison": method_rows,
        "all_selected_class_hashes_equal": all(x["class_sha256_equal"] for x in class_rows),
        "all_selected_method_hashes_equal": all(x["method_sha256_equal"] for x in method_rows),
        "all_selected_references_exact_equal": all(
            x["selected_references_exact_equal"] for x in method_rows),
        "all_selected_references_symbolic_sequence_equal": all(
            x["selected_references_symbolic_sequence_equal"] for x in method_rows),
    }


def audit(jar, javap, baseline):
    path = Path(jar)
    require(path.name == JAR_NAME, "wrong 21.1.250 artifact filename")
    report = copy.deepcopy(examine_previous(path, javap))
    # Version-specific reporting; the underlying 248 reader checks the
    # same exact required classes and semantic JVM anchors in the new JAR.
    report["scope"] = SCOPE
    report["artifact"]["coordinates"] = "net.neoforged:neoforge:21.1.250:universal"
    report["limits"] = dict(LIMITS)
    report["baseline_comparison"] = compare_versions(report, baseline)
    require(report["interpretation"] ==
            "STATIC_EVENT_DELEGATION_ONLY_NOT_CLAIM_AUTHORIZATION",
            "unsafe interpretation change")
    require(len(json.dumps(report).encode("utf-8")) < 28_000,
            "comparison report exceeds bounded budget")
    return report


def verify_seal(report, manifest):
    require(verify_previous(report, manifest), "underlying selected bytecode seal failed")
    require(report["baseline_comparison"] == manifest.get("baseline_comparison"),
            "baseline comparison seal drift")
    require(report["scope"] == SCOPE and report["limits"] == LIMITS,
            "scope/safety limits not preserved")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seal")
    args = parser.parse_args()
    try:
        base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        report = audit(args.jar, args.javap, base)
        if args.seal:
            seal = json.loads(Path(args.seal).read_text(encoding="utf-8"))
            verify_seal(report, seal)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",
                          encoding="utf-8")
        print("PASS: NeoForge 21.1.250 selected grief-event compiled evidence; "
              +report["artifact"]["sha256"])
        print("Comparative selected method hash parity: "
              +str(report["baseline_comparison"]["all_selected_method_hashes_equal"]))
        print("NO_MUTATION / NOT_CERTIFIED / claim listeners and physical QA unverified")
    except (EvidenceError, ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, "FAIL-CLOSED: "+str(exc)+"\n")


if __name__ == "__main__":
    main()
