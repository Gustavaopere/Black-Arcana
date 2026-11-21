#!/usr/bin/env python3
"""Read-only physical publisher audit of GingerbreadArmorItem 1.0.10.

Discovers native methods, constant-pool consumers, inherited support and
filename-matched resources. Never certifies runtime, hooks or physical QA.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

import alexscaves_1010_burrowing_cave_map_probe as census
from alexscaves_1010_armor_material_audit import (
    SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)

OWNER = "com/github/alexmodguy/alexscaves/server/item/GingerbreadArmorItem"

def run(jar: Path, javap: str, output: Path):
    verify_artifact(jar)
    require(not output.exists(), "write-once report required")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(set(native["targets"]) == {OWNER}, "item class missing/ambiguous")
    resources = {}
    with ZipFile(jar) as archive:
        for path in sorted(archive.namelist()):
            if not path.endswith(".json") or "gingerbread" not in path.lower():
                continue
            raw = archive.read(path)
            resources[path] = {
                "sha256": digest(raw),
                "size": len(raw),
                "json": json.loads(raw),
            }
    report = {
        "schema_version": 1,
        "scope": "GINGERBREAD_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            "installed_dump_comparison": "NOT_VERIFIED",
        },
        "native": native,
        "matching_resources": resources,
        "source_revision_1111_parity": "NOT_ASSUMED",
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(output.read_bytes()))
    print("JAR_SHA256", SHA256, "JAR_SIZE", SIZE)
    item = native["targets"][OWNER]
    print("OWNER", OWNER, "CLASS_SHA256", item["class_sha256"],
          "DECLARATIONS", len(item["declarations"]), "CODE_METHODS",
          len(item["methods"]), "FIELDS", len(item["fields"]),
          "DIRECT_CONSUMERS", len(item["consumers"]),
          "ANCESTORS", len(item["in_jar_ancestors"]))
    for method in item["methods"]:
        d = method["declaration"]
        print("METHOD", d["name"], d["descriptor"],
              "INSTRUCTIONS", method["instruction_count"],
              "SHA256", method["instruction_sha256"])
        for row in method["instructions"]:
            if (row["opcode"].startswith(("invoke", "get", "put", "if"))
                    or row["opcode"] in {"ldc", "ldc_w", "ldc2_w",
                                        "sipush", "bipush", "new"}):
                print("PIVOT", d["name"], row["offset"], row["opcode"],
                      row["operand"], row["symbol"][:150])
    for caller, data in item["consumers"].items():
        print("CONSUMER", caller, "SITES", len(data["sites"]),
              "METHODS", [m["declaration"]["name"] for m in data["bodies"]])
    print("RESOURCES", len(resources), json.dumps(resources, sort_keys=True))
    print("STATIC_DISCOVERY_ONLY NO_MUTATION")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    run(a.jar, a.javap, a.output)
