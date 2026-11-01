#!/usr/bin/env python3
"""Read-only, bounded evidence of RaygunItem in the installed 1.0.10 JAR.

Inspects classfile/selected JVM methods. Does NOT certify runtime, hooks,
player attribution, targets, damage acceptance or all possible emitters.
No provider bytecode, resources or complete method bodies are exported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import (
    name_of, summarize, strict_pairs
)

CLASS = "com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
CLASS_SHA256 = "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
FACTORY_OFFSET = 1026
FACTORY_SIGNATURE = "causeRaygunDamage"
MAX_METHODS = 35
MAX_REPORT_BYTES = 400_000
BASE_NAMES = {
    "RaygunItem", "onUseTick", "use", "releaseUsing", "getUseDuration",
    "inventoryTick", "getBarWidth", "getBarColor", "isBarVisible"
}
DYNAMIC_NAME = re.compile(
    r"^(?:get|set|can|has|is|on).*(?:ray|beam|charge|energy|ammo|cooldown|"
    r"damage|heat|use|time|tick|target|shoot)", re.IGNORECASE
)


class RaygunProbeError(ValueError):
    pass


def is_focus(method):
    name = name_of(method)
    return name in BASE_NAMES or bool(DYNAMIC_NAME.search(name))


def validate_impact_method(method):
    """Assert the exact catalogued direct factory callsite exists once."""
    if name_of(method) != "onUseTick":
        raise RaygunProbeError("invalid impact method identity")
    hit = [row for row in method["instructions"] if row["offset"] == FACTORY_OFFSET]
    if len(hit) != 1 or hit[0]["opcode"] != "invokestatic" or (
        FACTORY_SIGNATURE not in hit[0]["symbol"]
    ):
        raise RaygunProbeError("missing/moved exact Raygun damage factory")
    if not method["descriptor"].endswith(";)V") and not method["descriptor"].endswith("I)V"):
        raise RaygunProbeError("unexpected Raygun onUseTick descriptor")
    return {
        "offset": FACTORY_OFFSET, "opcode": hit[0]["opcode"],
        "symbol": hit[0]["symbol"], "descriptor": method["descriptor"]
    }


def selected_report(methods):
    if len(methods) != len({(name_of(m), m["descriptor"]) for m in methods}):
        raise RaygunProbeError("duplicate declared JVM method")
    relevant = [m for m in methods if is_focus(m) and m["instructions"]]
    if not 1 <= len(relevant) <= MAX_METHODS:
        raise RaygunProbeError("out-of-bounds selected method population")
    impact = [m for m in relevant if name_of(m) == "onUseTick"]
    if len(impact) != 1:
        raise RaygunProbeError("one exact onUseTick expected")
    call = validate_impact_method(impact[0])
    output = []
    for method in relevant:
        points = [11, 69, 249, 640, 943, FACTORY_OFFSET, 1119] if method is impact[0] else []
        output.append(summarize(method, points))
    return {"method_count": len(output), "damage_factory_callsite": call,
            "selected_methods": output}


def audit(jar: Path, javap_bin: Path):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise RaygunProbeError("publisher JAR SHA/size differs from installed modlist")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or CLASS not in names:
            raise RaygunProbeError("archive class identity/duplicate member")
        digest = hashlib.sha256(archive.read(CLASS)).hexdigest()
        if digest != CLASS_SHA256:
            raise RaygunProbeError("Raygun class hash mismatch")
    methods = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    report = selected_report(methods)
    out = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_SELECTED_METHOD_REFERENCES_AND_NUMERIC_OPERANDS_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS, "class_sha256": CLASS_SHA256,
        "declared_method_count": len(methods),
        **report,
        "limits": {
            "provider_source_or_complete_bytecode_exported": False,
            "control_flow_and_exception_edges": "NOT_FULLY_RECONSTRUCTED",
            "true_hit_acceptance_or_damage": "NOT_TESTED",
            "effective_targeting_and_world_protection": "NOT_VERIFIED",
            "cost_cooldown_mutability": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False
        }
    }
    if len(json.dumps(out, ensure_ascii=False).encode("utf-8")) > MAX_REPORT_BYTES:
        raise RaygunProbeError("bounded evidence report exceeded budget")
    return out



def check_snapshot(report, snapshot):
    """Fail closed on all selected SHA-exact identity/operand assertions."""
    for key in ("schema_version", "scope", "artifact", "class_path",
                "class_sha256", "declared_method_count", "method_count"):
        if report.get(key) != snapshot.get(key):
            raise RaygunProbeError("sealed metadata drift: " + key)
    selected = {m["name"] + " " + m["descriptor"]: m
                for m in report["selected_methods"]}
    if len(selected) != report["method_count"]:
        raise RaygunProbeError("duplicate selected method identity")
    for key, digest in snapshot["selected_method_digests"].items():
        if key not in selected or selected[key]["parsed_method_sha256"] != digest:
            raise RaygunProbeError("sealed method digest drift: " + key)
    if not 1 <= len(snapshot["anchors"]) <= 40:
        raise RaygunProbeError("critical anchor budget exceeded")
    if len({(x["method"], x["kind"], x["offset"]) for x in snapshot["anchors"]}) != len(snapshot["anchors"]):
        raise RaygunProbeError("duplicate sealed Raygun anchor")
    by_name = {}
    for m in report["selected_methods"]:
        by_name.setdefault(m["name"], []).append(m)
    for anchor in snapshot["anchors"]:
        methods = by_name.get(anchor["method"], [])
        if len(methods) != 1:
            raise RaygunProbeError("missing or ambiguous sealed method")
        rows = methods[0].get(anchor["kind"])
        if not isinstance(rows, list):
            raise RaygunProbeError("unrecognized sealed anchor category")
        hits = [x for x in rows if x.get("offset") == anchor["offset"]]
        if len(hits) != 1:
            raise RaygunProbeError("missing or duplicate sealed offset")
        row = hits[0]
        for key in ("opcode", "operand"):
            if key in anchor and row.get(key) != anchor[key]:
                raise RaygunProbeError("sealed Raygun opcode/operand drift")
        if anchor.get("symbol_contains") not in (None, "") and anchor["symbol_contains"] not in row.get("symbol", ""):
            raise RaygunProbeError("sealed Raygun symbolic owner drift")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    snapshot = json.loads(args.snapshot.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)
    check_snapshot(report, snapshot)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False,
                                      sort_keys=True) + "\n", encoding="utf8")
    print("raygun_1010_selected_methods=" + str(report["method_count"]) +
          " static_only=no_runtime_or_mutating_hook_certification")


if __name__ == "__main__":
    main()
