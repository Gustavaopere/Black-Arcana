#!/usr/bin/env python3
"""Read-only SHA-exact HazmatArmorItem 1.0.10 discovery.

The installed publisher artifact is authenticated before inspection. This is
an evidence-gathering probe, not a static contract certificate or mutating hook.
No third-party source/asset is copied into the Black Arcana runtime.
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

OWNER = "com/github/alexmodguy/alexscaves/server/item/HazmatArmorItem"
ITEM_IDS = (
    "hazmat_mask", "hazmat_chestplate", "hazmat_leggings", "hazmat_boots",
)


def discover(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "write-once report required")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(set(native["targets"]) == {OWNER}, "missing/ambiguous Hazmat owner")
    # The reusable all-class probe collects an unrelated legacy filename
    # census; replace it with a scoped, hashes-only inventory.
    native.pop("filename_matched_resources", None)
    resources = {}
    with ZipFile(jar) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith(".json") or "hazmat" not in name.lower():
                continue
            raw = archive.read(name)
            json.loads(raw)  # Fail closed if a matching resource is malformed.
            resources[name] = {"sha256": digest(raw), "size": len(raw)}
    item = native["targets"][OWNER]
    require(item["methods"], "owner has no executable methods")
    require(len(item["methods"]) == sum(
        "code_sha256" in method for method in item["declarations"]
    ), "native body coverage mismatch")
    report = {
        "schema_version": 1,
        "scope": "HAZMAT_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10", "sha1": SHA1,
            "sha256": SHA256, "size_bytes": SIZE,
            "installed_dump_comparison": "NOT_VERIFIED",
        },
        "owner": OWNER,
        "registry_candidates_not_individually_certified": list(ITEM_IDS),
        "native": native,
        "filename_matched_resource_hashes": resources,
        "other_radiation_consumers_complete": False,
        "engine_and_external_armor_effects_verified": False,
        "source_revision_parity": "NOT_ASSUMED",
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
    print("ARTIFACT_SHA256", SHA256, "SIZE", SIZE)
    print("OWNER", OWNER, "CLASS_SHA256", item["class_sha256"])
    print("DECLARATIONS", len(item["declarations"]),
          "EXECUTABLE", len(item["methods"]), "FIELDS", len(item["fields"]),
          "CONSUMERS", len(item["consumers"]),
          "ANCESTORS", len(item["in_jar_ancestors"]))
    for method in item["methods"]:
        d = method["declaration"]
        print("METHOD", d["name"], d["descriptor"],
              "INSTRUCTIONS", method["instruction_count"],
              "SHA256", method["instruction_sha256"])
        for ins in method["instructions"]:
            if ins["opcode"].startswith(("invoke", "get", "put", "if")) or ins["opcode"] in (
                "ldc", "ldc_w", "ldc2_w", "sipush", "bipush", "new", "instanceof",
            ):
                print("PIVOT", d["name"], ins["offset"], ins["opcode"],
                      ins["operand"], ins["symbol"][:180])
    for caller, entry in item["consumers"].items():
        print("TYPED_CONSUMER", caller, "SITES", len(entry["sites"]),
              "METHODS", [(m["declaration"]["name"], m["declaration"]["descriptor"])
                          for m in entry["bodies"]])
    for name, entry in resources.items():
        print("RESOURCE_HASH", name, entry["sha256"], entry["size"])
    print("LIMITS STATIC_DISCOVERY_ONLY NO_MUTATION NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    discover(args.jar, args.javap, args.output)
