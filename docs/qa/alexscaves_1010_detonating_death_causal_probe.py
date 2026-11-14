#!/usr/bin/env python3
"""Read-only causal probe of Detonating Death in Alex's Caves Continued 1.0.10.

Reproduces full relevant JVM method identities/CFG from the exact publisher JAR,
compares selected historical class/resource hashes and sparse anchors. Never
interprets a method reference as a mutating seam or actual gameplay settlement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods
)
from alexscaves_1010_dreadbow_decision_probe import method_digest
from alexscaves_1010_bouncy_ball_causal_probe import (
    method_switch_tables, branch_edges
)

BASE = "com/github/alexmodguy/alexscaves/"
TOTEM = BASE + "server/item/TotemOfPossessionItem.class"
EXPLOSION = BASE + "server/entity/util/TotemExplosion.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
RES = "data/alexscaves/enchantment/detonating_death.json"
TAG = "data/alexscaves/tags/item/enchantable/totem_of_possession.json"

CLASS_SHAS = {
    TOTEM: "bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e",
    EXPLOSION: "b798d95de5adf72f517a224331675da78277e0ae0e03435b2c8ac72f799cd815",
}
RESOURCE_SHAS = {
    RES: "8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e",
    TAG: "185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf",
}
METHODS = {
    TOTEM: {
        "onUseTick": "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V",
        "getControlledEntity": "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/Entity;",
    },
    EXPLOSION: {"explode": "()V"},
}
PIVOTS = {
    (TOTEM, "onUseTick"): {
        87: ("getstatic", "Explosion$BlockInteraction.KEEP"),
        97: ("invokevirtual", "TotemExplosion.explode"),
        103: ("invokevirtual", "TotemExplosion.finalizeExplosion"),
    },
    (TOTEM, "getControlledEntity"): {
        85: ("invokevirtual", "ServerLevel.getEntity"),
    },
    (EXPLOSION, "explode"): {
        805: ("invokevirtual", "Entity.hurt"),
        888: ("invokevirtual", "Entity.setDeltaMovement"),
    },
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def unique_pairs(pairs):
    obj = {}
    for k, v in pairs:
        require(k not in obj, "duplicate JSON key " + k)
        obj[k] = v
    return obj

def verify_config(metadata):
    require(isinstance(metadata, dict), "metadata is not an object")
    require(metadata.get("description") == {
        "translate": "enchantment.alexscaves.detonating_death"
    }, "enchantment ID drift")
    require(metadata.get("supported_items") ==
            "#alexscaves:enchantable/totem_of_possession", "support tag drift")
    require(metadata.get("weight") == 2 and metadata.get("max_level") == 1
            and metadata.get("anvil_cost") == 4
            and metadata.get("slots") == ["mainhand"]
            and metadata.get("exclusive_set") == "alexscaves:astral_transferring",
            "metadata settings drift")
    require(metadata.get("min_cost") ==
            {"base": 1, "per_level_above_first": 11}, "min-cost drift")
    require(metadata.get("max_cost") ==
            {"base": 41, "per_level_above_first": 10}, "max-cost drift")

def choose(methods, name, descriptor):
    found = [m for m in methods
             if re.search(r"\b" + re.escape(name) + r"\(", m["header"])
             and m["descriptor"] == descriptor]
    require(len(found) == 1, "missing/ambiguous method " + name)
    return found[0]

def compare_sparse_anchors(method, recorded):
    """Existing action manifest has selected anchors, not an exhaustive roster."""
    by = {r["offset"]: r for r in method["instructions"]}
    require(len(by) == len(method["instructions"]), "duplicate JVM offsets")
    require(1 <= len(recorded) <= len(by), "empty/oversize previous anchor list")
    visited = set()
    for anchor in recorded:
        offset = anchor["offset"]
        require(offset in by and offset not in visited,
                "missing/repeated parent anchor @" + str(offset))
        visited.add(offset)
        native = by[offset]
        require(native["opcode"] == anchor["opcode"] and
                native["symbol"] == anchor["symbol"] and
                " ".join(native["operand"].split()) ==
                " ".join(anchor["operand"].split()),
                "historical JVM anchor drift @" + str(offset))
    return len(visited)

def verify_pivots(method, anchors):
    by = {r["offset"]: r for r in method["instructions"]}
    for offset, (opcode, symbol) in anchors.items():
        row = by.get(offset)
        require(row is not None and row["opcode"] == opcode and
                symbol in row["symbol"], "exact JVM causal pivot drift @" + str(offset))

def audit(jar: Path, manifest: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR identity drift")
    parent_raw = manifest.read_bytes()
    parent = json.loads(parent_raw, object_pairs_hook=unique_pairs)
    require(parent["artifact_sha1"] == SHA1 and
            parent["artifact_sha256"] == SHA256 and
            parent["artifact_size_bytes"] == SIZE,
            "parent action manifest artifact identity drift")
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP members")
        for path, expected in {**CLASS_SHAS, **RESOURCE_SHAS}.items():
            require(sha(arc.read(path)) == expected, "JAR member drift " + path)
            if path in CLASS_SHAS:
                require(parent["classes"][path]["sha256"] == expected,
                        "parent class SHA mismatch " + path)
            else:
                require(parent["resources"][path] == expected,
                        "parent resource SHA mismatch " + path)
        metadata = json.loads(arc.read(RES), object_pairs_hook=unique_pairs)
        verify_config(metadata)
        tag = json.loads(arc.read(TAG), object_pairs_hook=unique_pairs)
        require(tag == {"values": ["alexscaves:totem_of_possession"]},
                "eligible-item tag drift")
        owners = sorted(path for path in names if path.startswith(BASE)
                        and path.endswith(".class")
                        and b"DETONATING_DEATH" in arc.read(path))
        require(TOTEM in owners and REGISTRY in owners and len(owners) <= 12,
                "unexpected/missing compiled Detonating Death token owners")

    native = {}
    for owner, requested in METHODS.items():
        source = javap(javap_bin, jar, owner[:-6].replace("/", "."))
        declared = parse_methods(source)
        recorded = parent["classes"][owner]["methods"]
        per_method = {}
        for name, descriptor in requested.items():
            method = choose(declared, name, descriptor)
            prior = [m for m in recorded if m["name"] == name and
                     m["descriptor"] == descriptor]
            require(len(prior) == 1, "parent method missing/ambiguous " + name)
            historical_count = compare_sparse_anchors(method, prior[0]["anchors"])
            verify_pivots(method, PIVOTS[(owner, name)])
            switches = method_switch_tables(method, source)
            edges = branch_edges(method, switches)
            require(1 <= len(method["instructions"]) <= 2200,
                    "unbounded native method")
            per_method[name] = {
                "descriptor": descriptor,
                "parsed_sha256": method_digest(method),
                "instructions": len(method["instructions"]),
                "direct_branches": len(edges),
                "verified_switches": switches,
                "previous_anchors_verified": historical_count,
                "pivot_offsets": sorted(PIVOTS[(owner, name)]),
                "invocations": [
                    {"offset": i["offset"], "target": i["symbol"]}
                    for i in method["instructions"]
                    if i["opcode"].startswith("invoke") and
                    any(part in i["symbol"] for part in (
                        "TotemExplosion", "DamageSources", "ACPlatform.ignoreExplosion",
                        "Entity.hurt", "Entity.setDeltaMovement", "getControlledEntity",
                        "ACCompat.enchantLevel"))
                ],
            }
        native[owner] = per_method
    return {
        "schema_version": 1,
        "scope": "INDIVIDUAL_STATIC_DETONATING_DEATH_CAUSAL_PROBE",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "parent_manifest_sha256": sha(parent_raw),
        "class_sha256": CLASS_SHAS,
        "resource_sha256": RESOURCE_SHAS,
        "compiled_token_owners": owners,
        "metadata": metadata,
        "tag": tag,
        "native": native,
        "limits": {
            "single_native_possession_root": True,
            "new_spell_root": False,
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "individual_static_certificate": "PENDING_SEAL_AND_REVIEW",
            "world_claims_pvp": "NOT_VERIFIED",
            "engine_damage_acceptance": "NOT_TESTED",
            "side_effect_and_authority": "NEEDS_CAUSAL_REVIEW",
        },
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.jar, args.manifest, args.javap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    args.output.write_text(data, encoding="utf8")
    print("DETONATING_DEATH_1010_CAUSAL_PROBE")
    print("compiled_token_owners=" + json.dumps(report["compiled_token_owners"]))
    print("method_counts=" + json.dumps({
        owner: {name: {
            "digest": m["parsed_sha256"], "instructions": m["instructions"],
            "branches": m["direct_branches"],
            "previous_anchors": m["previous_anchors_verified"]
        } for name, m in methods.items()}
        for owner, methods in report["native"].items()}, sort_keys=True))
    print("report_sha256=" + sha(data.encode("utf8")))
    print("STATIC_PROBE_ONLY PENDING_CERTIFICATION NO_MUTATION NOT_TESTED")

if __name__ == "__main__":
    main()
