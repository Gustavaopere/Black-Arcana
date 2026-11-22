#!/usr/bin/env python3
"""Read-only SHA-exact discovery of Resistor Shield transitive helper contracts.

No provider code is executed. Resources are parsed for audit, not embedded in
runtime. This is an observation, not hook or gameplay certification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require,
    verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

COMPAT = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
REQUIRED = {
    "enchantLevel", "useConsume", "knockback", "hurtAndBreakUsedHand",
    "getTag", "getOrCreateTag", "setTag", "getInt", "getBoolean",
}
RESOURCES = {
    "assets/alexscaves/models/item/resistor_shield.json":
        (1275, "90e6f55395b5da2c68cb0d858aa9b8a773e46a7cd3027500f5249d0f675acb47"),
    "data/alexscaves/advancement/alexscaves/resistor_shield.json":
        (735, "0a4dae9d1e074b98ae2127ea855c9684cd9e18d56fbd8c2f4c7049924508936f"),
    "data/alexscaves/recipe/resistor_shield.json":
        (433, "2d2c648cc1db20b024ba3643c4e3c281b270039299d32ea8a3e9b8e8262f77af"),
    "data/alexscaves/tags/item/enchantable/resistor_shield.json":
        (55, "2b5d57ffc709293f994b472c07cd44ed34647efec41106b819621c060366f3e0"),
}


def probe(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "dependency report must be write-once")
    with ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        classfiles = [name for name in names if name.endswith(".class")]
        require(len(classfiles) == 1555, "publisher class roster changed")
        owner_bytes = archive.read(COMPAT + ".class")
        reader = ClassReader(owner_bytes)
        require(reader.name == COMPAT and reader.major == 65, "helper class mismatch")
        parsed = disassemble(jar, javap, COMPAT)
        methods = [
            summarize(reader, signature, body)
            for signature, body in sorted(parsed.items())
            if signature[0] in REQUIRED
        ]
        found = {method["declaration"]["name"] for method in methods}
        require(found == REQUIRED, "expected native helpers missing")
        require(9 <= len(methods) <= 60, "unbounded helper overloads")
        resources = {}
        for path, (size, expected_sha) in RESOURCES.items():
            raw = archive.read(path)
            require(len(raw) == size, "resource size drift: " + path)
            require(digest(raw) == expected_sha, "resource hash drift: " + path)
            resources[path] = {
                "sha256": expected_sha,
                "size_bytes": size,
                "parsed_json": json.loads(raw),
            }
    evidence = {
        "schema_version": 1,
        "scope": "RESISTOR_SHIELD_TRANSITIVE_DEPENDENCY_DISCOVERY_ONLY",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            "installed_binary_parity": "NOT_VERIFIED",
        },
        "helper_class": {
            "owner": COMPAT,
            "class_sha256": digest(owner_bytes),
            "superclass": reader.parent,
            "methods": methods,
            "scope": "ONLY_DIRECTLY_NAMED_HELPERS_NOT_ALL_TRANSITIVE_CONSUMERS",
        },
        "resources": resources,
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "provider_universe_closed": False,
        "mutation": "NO_MUTATION",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(evidence), encoding="utf8")
    print("EVIDENCE_SHA256", digest(output.read_bytes()))
    print("COMPAT_CLASS_SHA256", digest(owner_bytes))
    for method in methods:
        declaration = method["declaration"]
        print("METHOD", declaration["name"], declaration["descriptor"],
              method["instruction_count"], method["instruction_sha256"])
    for path, value in resources.items():
        print("RESOURCE", path, value["sha256"], value["size_bytes"])
    print("DISCOVERY_ONLY NOT_CERTIFIED NO_MUTATION NO_PHYSICAL_QA")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", type=str, default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    probe(args.jar, args.javap, args.output)
