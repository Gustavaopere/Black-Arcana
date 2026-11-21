#!/usr/bin/env python3
"""Read-only native discovery of RemoteDetonatorItem in Alex's Caves 1.0.10.

Reuses the pinned publisher-JAR class census to enumerate own executable
methods, typed consumers, inherited in-JAR bodies, resources by filename and
SHA exact provenance. No item effect is certified by this discovery.
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

OWNER = "com/github/alexmodguy/alexscaves/server/item/RemoteDetonatorItem"
RESOURCE_TERMS = ("remote_detonator", "remote_detonation", "detonator")


def discover(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "discovery evidence must be write-once")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(set(native["targets"]) == {OWNER}, "missing native RemoteDetonatorItem")
    native.pop("filename_matched_resources", None)

    obj = native["targets"][OWNER]
    require(obj["methods"], "no executable RemoteDetonatorItem methods")
    require(len(obj["methods"]) == sum(
        "code_sha256" in entry for entry in obj["declarations"]
    ), "owner executable body census does not cover all declarations")
    require(any(owner.endswith("/ACItemRegistry")
                for owner in obj["consumers"]), "no typed registry owner")

    resources = {}
    with ZipFile(jar) as z:
        for path in sorted(z.namelist()):
            if not path.endswith(".json") or not any(
                term in path.lower() for term in RESOURCE_TERMS
            ):
                continue
            raw = z.read(path)
            json.loads(raw)
            resources[path] = {"sha256": digest(raw), "size": len(raw)}
    require(len(resources) <= 200, "unbounded resource discovery")

    report = {
        "schema_version": 1,
        "scope": "REMOTE_DETONATOR_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10",
            "sha1": SHA1,
            "sha256": SHA256,
            "size_bytes": SIZE,
            "installed_dump_comparison": "NOT_VERIFIED",
        },
        "owner": OWNER,
        "native": native,
        "filename_matched_resource_hashes": resources,
        "resource_census_limit": "FILENAME_MATCHES_ONLY",
        "registry_identity": "NOT_PROVEN_BY_FILENAME_ONLY",
        "typed_consumer_scan": "PUBLISHER_CLASSFILES_ONLY",
        "other_consumers_complete": False,
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
    print("PUBLISHER_SHA256", SHA256, "SIZE", SIZE)
    print("OWNER", OWNER, "CLASS_SHA256", obj["class_sha256"])
    print("OWNER_METHODS", len(obj["methods"]),
          "DECLARATIONS", len(obj["declarations"]),
          "FIELDS", len(obj["fields"]),
          "TYPED_CONSUMER_OWNERS", len(obj["consumers"]),
          "IN_JAR_ANCESTORS", len(obj["in_jar_ancestors"]))
    for method in obj["methods"]:
        declaration = method["declaration"]
        print("METHOD", declaration["name"], declaration["descriptor"],
              "COUNT", method["instruction_count"],
              "SHA256", method["instruction_sha256"])
    for consumer_name, consumer in obj["consumers"].items():
        print("CONSUMER", consumer_name, consumer["class_sha256"],
              "REFERENCES", len(consumer["sites"]),
              "BODIES", json.dumps([
                  {"method": m["declaration"]["name"],
                   "descriptor": m["declaration"]["descriptor"],
                   "instruction_count": m["instruction_count"],
                   "instruction_sha256": m["instruction_sha256"]}
                  for m in consumer["bodies"]
              ], sort_keys=True))
    for name, data in resources.items():
        print("RESOURCE", name, data["sha256"], data["size"])
    print("DISCOVERY_ONLY NO_MUTATION PHYSICAL_QA_NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    discover(args.jar, args.javap, args.output)
