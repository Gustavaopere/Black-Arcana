#!/usr/bin/env python3
"""Exact publisher SHA-verified discovery of GazingPearlItem and DeepOneReaction.

This only inventories the provider-native binary methods/resources and typed
consumers. It does not certify a static contract, runtime hooks or physical QA.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

import alexscaves_1010_burrowing_cave_map_probe as scan
from alexscaves_1010_armor_material_audit import (
    SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)

PREFIX = "com/github/alexmodguy/alexscaves/server/"
OWNERS = (
    PREFIX + "item/GazingPearlItem",
    PREFIX + "entity/util/DeepOneReaction",
)
RESOURCE_STEM = "gazing_pearl"


def run(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "write-once report required")
    scan.TARGETS = OWNERS
    native = scan.inspect(jar, javap)
    require(set(native["targets"]) == set(OWNERS), "publisher owner roster drift")
    resources = {}
    with ZipFile(jar) as archive:
        for path in sorted(archive.namelist()):
            if path.endswith(".json") and RESOURCE_STEM in path.lower():
                content = archive.read(path)
                resources[path] = {
                    "sha256": digest(content), "size": len(content),
                    "json": json.loads(content),
                }
    report = {
        "schema_version": 1,
        "scope": "GAZING_PEARL_PUBLISHER_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "name": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
            "size_bytes": SIZE, "new_installed_dump_comparison": "NOT_VERIFIED",
        },
        "native": native,
        "filename_matched_resources": resources,
        "semantic_magic_roots_certified_delta": 0,
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(output.read_bytes()))
    print("JAR_SHA256", SHA256, "SIZE", SIZE)
    for owner, item in native["targets"].items():
        print("OWNER", owner, "SHA256", item["class_sha256"],
              "METHODS", len(item["methods"]), "CONSUMERS", len(item["consumers"]),
              "FIELDS", len(item["fields"]))
        for method in item["methods"]:
            d = method["declaration"]
            print("METHOD", owner.split("/")[-1], d["name"], d["descriptor"],
                  "INS", method["instruction_count"],
                  "SHA256", method["instruction_sha256"])
            for ins in method["instructions"]:
                if (ins["opcode"].startswith(("invoke", "get", "put", "if"))
                        or ins["opcode"] in {
                            "ldc", "ldc_w", "ldc2_w", "sipush", "bipush",
                            "new", "checkcast", "instanceof"}):
                    print("PIVOT", owner.split("/")[-1], d["name"],
                          ins["offset"], ins["opcode"],
                          ins["operand"], ins["symbol"][:170])
        print("TYPED_CONSUMERS", owner, sorted(item["consumers"]))
    print("RESOURCES", json.dumps(resources, sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--jar", type=Path, required=True)
    cli.add_argument("--javap", default="javap")
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    run(args.jar, args.javap, args.output)
