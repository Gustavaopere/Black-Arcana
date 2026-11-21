#!/usr/bin/env python3
"""Read-only exact-publisher discovery of PrimordialArmorItem (Alex's Caves 1.0.10).

Discovers native methods, all typed class consumers, in-JAR ancestors and
filename-matched resource identities. The output is evidence, NOT a static
per-item certificate, safe mutation hook or gameplay test.
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

OWNER = "com/github/alexmodguy/alexscaves/server/item/PrimordialArmorItem"
ITEM_CANDIDATES = ("primordial_helmet", "primordial_tunic", "primordial_pants")
RESOURCE_TERMS = (*ITEM_CANDIDATES, "primordial_armor")


def discover(jar: Path, javap: str, output: Path):
    verify_artifact(jar)
    require(not output.exists(), "write-once evidence report required")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(set(native["targets"]) == {OWNER}, "Primordial class missing or ambiguous")
    # The reused probe's legacy filename census is unrelated to this owner.
    native.pop("filename_matched_resources", None)
    entry = native["targets"][OWNER]
    require(len(entry["methods"]) == sum("code_sha256" in m for m in entry["declarations"]),
            "not all declared methods were disassembled")
    require(entry["methods"], "PrimordialArmorItem has no native executable method")
    resources = {}
    with ZipFile(jar) as z:
        for name in sorted(z.namelist()):
            if not name.endswith(".json") or not any(t in name.lower() for t in RESOURCE_TERMS):
                continue
            raw = z.read(name)
            json.loads(raw)  # Reject malformed matching resource; do not copy source text.
            resources[name] = {"size": len(raw), "sha256": digest(raw)}
    require(len(resources) <= 100, "unexpectedly broad resource census")
    evidence = {
        "schema_version": 1,
        "scope": "PRIMORDIAL_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10", "sha1": SHA1,
            "sha256": SHA256, "size_bytes": SIZE,
            "installed_dump_comparison": "NOT_VERIFIED",
        },
        "owner": OWNER,
        "registry_candidates_not_individually_certified": list(ITEM_CANDIDATES),
        "native": native,
        "filename_matched_resource_hashes": resources,
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
    output.write_text(canonical(evidence), encoding="utf8")
    print("REPORT_SHA256", digest(output.read_bytes()))
    print("PUBLISHER_SHA256", SHA256, "PUBLISHER_SIZE", SIZE)
    print("OWNER", OWNER, "CLASS_SHA256", entry["class_sha256"])
    print("METHODS", len(entry["methods"]), "DECLARATIONS", len(entry["declarations"]),
          "FIELDS", len(entry["fields"]), "DIRECT_CONSUMER_OWNERS", len(entry["consumers"]),
          "IN_JAR_ANCESTORS", len(entry["in_jar_ancestors"]))
    for m in entry["methods"]:
        d = m["declaration"]
        print("METHOD", d["name"], d["descriptor"], "INSTRUCTIONS",
              m["instruction_count"], "SHA256", m["instruction_sha256"])
        for x in m["instructions"]:
            if x["opcode"].startswith(("invoke", "get", "put", "if")) or x["opcode"] in (
                "ldc", "ldc_w", "ldc2_w", "bipush", "sipush", "new", "instanceof"
            ):
                print("PIVOT", d["name"], x["offset"], x["opcode"],
                      x["operand"], x["symbol"][:180])
    for caller, data in entry["consumers"].items():
        print("TYPED_CONSUMER", caller, "SITES", len(data["sites"]),
              "METHODS", [(m["declaration"]["name"], m["declaration"]["descriptor"])
                          for m in data["bodies"]])
    for name, data in resources.items():
        print("RESOURCE_HASH", name, data["sha256"], data["size"])
    print("LIMITS STATIC_DISCOVERY_ONLY NO_MUTATION NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    discover(args.jar, args.javap, args.output)
