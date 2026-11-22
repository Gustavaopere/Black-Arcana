#!/usr/bin/env python3
"""Read-only SHA-exact class and typed-consumer census for ResistorShieldItem.

Publisher Alex's Caves 1.0.10 (physical NeoForge 1.21.1 JAR) only.
No gameplay behavior, hooks, damage, effects or IDs are certified here.
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

OWNER = "com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem"
TERMS = ("resistor_shield", "resistor", "resistance_shield")

EXPECTED_CLASS_SHA = "ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741"
EXPECTED_PARENT = "net/minecraft/world/item/ShieldItem"
EXPECTED_INTERFACES = {
    "com/github/alexmodguy/alexscaves/server/item/ACClientExtensionItem",
    "com/github/alexmodguy/alexscaves/server/item/ACEnchantableItem",
    "com/github/alexmodguy/alexscaves/server/item/ACRepairableItem",
    "com/github/alexmodguy/alexscaves/server/item/ACTickingItem",
}
KNOWN_INTERFACE_BODIES = {
    ("getEnchantmentValue", "()I"): (
        2, "d943c5fe0bd38038ce70963c73b8759ba3d76c8c00d31c1a2141268dc4e0ee0a",
    ),
    ("isEnchantable", "(Lnet/minecraft/world/item/ItemStack;)Z"): (
        8, "9cd84b0255be269f2bf50fce0095c14fa5d484831fd35063e71f4c9814aa6b4f",
    ),
}


def discover(jar: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists(), "publisher report must be write-once")
    census.TARGETS = (OWNER,)
    native = census.inspect(jar, javap)
    require(native["class_entries_scanned"] == 1555, "class-count drift")
    require(set(native["targets"]) == {OWNER}, "target roster drift")
    native.pop("filename_matched_resources", None)
    cls = native["targets"][OWNER]
    # Independent, previously SHA-certified 1.0.10 ACEnchantableItem evidence.
    # This binds the new *census* to a known exact class, without promoting
    # a complete item's gameplay contract or a mutating hook.
    require(cls["class_sha256"] == EXPECTED_CLASS_SHA,
            "ResistorShieldItem class drift against prior native audit")
    require(cls["hierarchy"]["parent"] == EXPECTED_PARENT,
            "ResistorShieldItem superclass drift")
    require(set(cls["hierarchy"]["interfaces"]) == EXPECTED_INTERFACES,
            "ResistorShieldItem interface roster drift")
    selected = {
        (m["declaration"]["name"], m["declaration"]["descriptor"]):
        (m["instruction_count"], m["instruction_sha256"])
        for m in cls["methods"]
    }
    require(all(selected.get(k) == v for k, v in KNOWN_INTERFACE_BODIES.items()),
            "native enchantability methods drift against previously certified audit")
    require(cls["class_sha256"] and len(cls["class_sha256"]) == 64,
            "owner fingerprint absent")
    require(len(cls["methods"]) == sum(
        "code_sha256" in declaration for declaration in cls["declarations"]
    ), "executable method coverage drift")
    require(any(name.endswith("/ACItemRegistry")
                for name in cls["consumers"]), "typed item registry not found")
    require(len(cls["consumers"]) <= 120, "consumer bound exceeded")
    require(len(cls["methods"]) <= 60, "method bound exceeded")

    resources = {}
    with ZipFile(jar) as z:
        for name in sorted(z.namelist()):
            if not name.endswith(".json") or not any(t in name.lower() for t in TERMS):
                continue
            raw = z.read(name)
            json.loads(raw)
            resources[name] = {"sha256": digest(raw), "size": len(raw)}
    require(len(resources) <= 200, "resource roster unbounded")

    report = {
        "schema_version": 1,
        "scope": "RESISTOR_SHIELD_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
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
    print("PUBLISHER_SHA256", SHA256, "JAR_SIZE", SIZE)
    print("OWNER", OWNER, "CLASS_SHA256", cls["class_sha256"])
    print("METHOD_COUNT", len(cls["methods"]), "DECL_COUNT", len(cls["declarations"]),
          "FIELD_COUNT", len(cls["fields"]), "CONSUMERS", len(cls["consumers"]),
          "IN_JAR_ANCESTORS", len(cls["in_jar_ancestors"]),
          "DESCENDANTS", len(cls["descendants"]))
    for method in cls["methods"]:
        d = method["declaration"]
        print("METHOD", d["name"], d["descriptor"], method["instruction_count"],
              method["instruction_sha256"])
    for consumer, evidence in cls["consumers"].items():
        print("CONSUMER", consumer, evidence["class_sha256"],
              "TYPED_SITES", len(evidence["sites"]))
        for method in evidence["bodies"]:
            d = method["declaration"]
            print("CONSUMER_METHOD", consumer, d["name"], d["descriptor"],
                  method["instruction_count"], method["instruction_sha256"])
    for path, rec in resources.items():
        print("RESOURCE", path, rec["sha256"], rec["size"])
    print("DISCOVERY_ONLY NO_MUTATION NO_STATIC_CERTIFICATION")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    discover(args.jar, args.javap, args.output)
