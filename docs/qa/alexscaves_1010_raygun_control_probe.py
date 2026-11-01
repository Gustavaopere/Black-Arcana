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
        points = [FACTORY_OFFSET] if method is impact[0] else []
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False,
                                      sort_keys=True) + "\n", encoding="utf8")
    print("raygun_1010_selected_methods=" + str(report["method_count"]) +
          " static_only=no_runtime_or_mutating_hook_certification")


if __name__ == "__main__":
    main()
