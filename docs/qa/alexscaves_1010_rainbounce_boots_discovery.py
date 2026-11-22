#!/usr/bin/env python3
"""SHA-exact, read-only RainbounceBootsItem 1.0.10 native discovery.

This is a bounded JAR class/method/consumer/resource inventory, not a static
item certificate, gameplay validation or safe mutation hook. Third-party
code, models and assets are not copied into Black Arcana.
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

OWNER = "com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem"
ITEM_ID_CANDIDATE = "rainbounce_boots"


def discover(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "write-once discovery report required")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(set(native["targets"]) == {OWNER}, "Rainbounce owner missing")
    # Eliminate unrelated filename census inherited from the generic probe.
    native.pop("filename_matched_resources", None)
    item = native["targets"][OWNER]
    require(item["methods"], "Rainbounce owner contains no executable body")
    require(len(item["methods"]) == sum(
        "code_sha256" in m for m in item["declarations"]),
        "Rainbounce method-body coverage mismatch")
    resource_hashes = {}
    with ZipFile(jar) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith(".json") or "rainbounce" not in name.lower():
                continue
            raw = archive.read(name)
            json.loads(raw)
            resource_hashes[name] = {"sha256": digest(raw), "size": len(raw)}
    require(1 <= len(resource_hashes) <= 100,
            "unexpected Rainbounce JSON filename census")

    report = {
        "schema_version": 1,
        "scope": "RAINBOUNCE_BOOTS_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10", "sha1": SHA1,
            "sha256": SHA256, "size_bytes": SIZE,
            "installed_dump_comparison": "NOT_VERIFIED",
        },
        "owner": OWNER,
        "registry_candidate_not_individually_certified": ITEM_ID_CANDIDATE,
        "native": native,
        "filename_matched_resource_hashes": resource_hashes,
        "source_revision_parity": "NOT_ASSUMED",
        "other_consumers_complete": False,
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
    print("PUBLISHER_SHA256", SHA256, "SIZE", SIZE)
    print("OWNER", OWNER, "CLASS_SHA256", item["class_sha256"])
    print("METHODS", len(item["methods"]), "DECLARATIONS", len(item["declarations"]),
          "FIELDS", len(item["fields"]), "CONSUMER_OWNERS", len(item["consumers"]),
          "ANCESTORS", len(item["in_jar_ancestors"]))
    for method in item["methods"]:
        d = method["declaration"]
        print("METHOD", d["name"], d["descriptor"],
              "INSTRUCTIONS", method["instruction_count"],
              "SHA256", method["instruction_sha256"])
        for ins in method["instructions"]:
            if ins["opcode"].startswith(("invoke", "get", "put", "if")) or ins["opcode"] in (
                "ldc", "ldc_w", "ldc2_w", "bipush", "sipush",
                "new", "instanceof", "checkcast",
            ):
                print("PIVOT", d["name"], ins["offset"], ins["opcode"],
                      ins["operand"], ins["symbol"][:180])
    for cname, item_ref in item["consumers"].items():
        print("TYPED_CONSUMER", cname, "SITES", len(item_ref["sites"]),
              "METHODS", [(m["declaration"]["name"], m["declaration"]["descriptor"])
                          for m in item_ref["bodies"]])
    for name, entry in resource_hashes.items():
        print("RESOURCE_HASH", name, entry["sha256"], entry["size"])
    print("LIMITS STATIC_DISCOVERY_ONLY NO_MUTATION NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    discover(args.jar, args.javap, args.output)
