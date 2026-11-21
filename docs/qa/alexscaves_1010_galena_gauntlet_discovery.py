#!/usr/bin/env python3
"""Read-only SHA-exact Galena Gauntlet and magnetic-weapon consumer discovery.

This reports JVM evidence without promoting static certification, mutating hooks,
physical QA, new semantic magic roots, or publisher/installed-file parity.
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

ITEM = "com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem"
ENTITY = "com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
CLASS_SHA = {
    ITEM: "5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0",
    ENTITY: "a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071",
}
RESOURCE_TERMS = ("galena_gauntlet", "magnetic_weapon", "ferromagnetic_items")


def inspect_one(jar: Path, javap: str, owner: str) -> dict:
    scan.TARGETS = (owner,)
    result = scan.inspect(jar, javap)
    require(set(result["targets"]) == {owner}, "target roster mismatch")
    require(result["targets"][owner]["class_sha256"] == CLASS_SHA[owner],
            "owner bytes differ from previously sealed physical publisher")
    return result


def run(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "write-once report required")
    native = inspect_one(jar, javap, ITEM)
    entity = inspect_one(jar, javap, ENTITY)
    resources = {}
    with ZipFile(jar) as archive:
        for path in sorted(archive.namelist()):
            if path.endswith(".json") and any(t in path.lower() for t in RESOURCE_TERMS):
                raw = archive.read(path)
                resources[path] = {"sha256": digest(raw), "size": len(raw)}
    report = {
        "schema_version": 1,
        "scope": "GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED",
        "artifact": {"filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
                     "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
                     "size_bytes": SIZE, "installed_dump_parity": "NOT_VERIFIED"},
        "native": native, "entity_native": entity,
        "matching_resources": resources,
        "provider_universe_closed": False,
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(output.read_bytes()))
    print("ARTIFACT", SHA256, SIZE)
    for owner, group in ((ITEM, native), (ENTITY, entity)):
        card = group["targets"][owner]
        print("OWNER", owner, "CLASS_SHA256", card["class_sha256"],
              "METHODS", len(card["methods"]), "FIELDS", len(card["fields"]),
              "CONSUMERS", len(card["consumers"]))
        for method in card["methods"]:
            declaration = method["declaration"]
            instrs = method["instructions"]
            print("METHOD", owner.split("/")[-1], declaration["name"],
                  declaration["descriptor"], "INS", len(instrs),
                  "HASH", method["instruction_sha256"])
            # The complete report is retained in the Actions artifact.
            # Logs are a bounded callsite/constant index, not recovered source.
            for ins in instrs:
                if (ins["opcode"].startswith(("invoke", "get", "put", "if"))
                        or ins["opcode"] in {
                            "ldc", "ldc_w", "ldc2_w", "sipush", "bipush",
                            "new", "checkcast", "instanceof"}):
                    print("PIVOT", owner.split("/")[-1], declaration["name"],
                          ins["offset"], ins["opcode"], ins["symbol"][:190])
    print("RESOURCES", len(resources), json.dumps(resources, sort_keys=True))
    print("BOUNDED_DISCOVERY_ONLY NO_MUTATION")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.jar, args.javap, args.output)
