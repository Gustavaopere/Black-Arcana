#!/usr/bin/env python3
"""Read-only, bounded Sea Swing JVM discovery for the exact Alex's Caves 1.0.10 JAR.

UNSEALED_DISCOVERY_ONLY: extracting pivots is not certifying complete control
flow, client/server behavior, runtime hooks, or successful world insertion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ITEM = BASE + "server/item/OrtholanceItem.class"
WAVE = BASE + "server/entity/item/WaveEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
RESOURCE = "data/alexscaves/enchantment/sea_swing.json"
TAG = "data/alexscaves/tags/item/enchantable/ortholance.json"
# Existing exact Flinging dossier independently anchors these same 1.0.10 classes.
KNOWN_CLASS_SHA = {
    ITEM: "996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09",
    WAVE: "93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e",
    REGISTRY: "60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32",
}
ITEM_NAMES = frozenset({"hurtEnemy", "acHurtEnemy"})
WAVE_NAMES = frozenset({"tick", "attackEntities", "getLifespan", "getWaitingTicks",
                        "setLifespan", "setWaitingTicks", "getWaveScale", "setWaveScale",
                        "getOwner", "addAdditionalSaveData", "readAdditionalSaveData"})
NEEDLES = {
    "hurtEnemy": ("SEA_SWING:", "enchantLevel:", "hurtAndBreak:", "setLifespan:",
                  "setPos:", "setYRot:", "addFreshEntity:"),
    "acHurtEnemy": ("SEA_SWING:", "enchantLevel:", "hurtAndBreak:", "setLifespan:",
                    "setPos:", "setYRot:", "addFreshEntity:"),
    "tick": ("attackEntities:", "getLifespan:", "getWaitingTicks:", "discard:",
             "setDeltaMovement:"),
    "attackEntities": ("getEntitiesOfClass:", "mobProjectile:", "hurt:", "knockback:",
                       "isAlliedTo:", "getBoundingBox:"),
}
MAX_METHOD_INSTRUCTIONS = 1500
MAX_PIVOTS_PER_METHOD = 10

def require(ok, explanation):
    if not ok:
        raise ValueError(explanation)

def digest(blob):
    return hashlib.sha256(blob).hexdigest()

def select(methods, allowed):
    selected = []
    for method in methods:
        name = name_of(method)
        if name not in allowed:
            continue
        instructions = method["instructions"]
        require(1 <= len(instructions) <= MAX_METHOD_INSTRUCTIONS,
                "unbounded method: " + name)
        offsets = [i["offset"] for i in instructions]
        require(offsets == sorted(set(offsets)), "bad JVM offsets: " + name)
        pivots = []
        for needle in NEEDLES.get(name, ()):
            matched = [n for n, instruction in enumerate(instructions)
                       if needle in instruction["symbol"]]
            if not matched:
                continue
            pivots.append({
                "needle": needle, "hits": len(matched),
                "windows": [
                    [{"offset": i["offset"], "opcode": i["opcode"],
                      "operand": i["operand"], "symbol": i["symbol"]}
                     for i in instructions[max(0, index-7):index+15]]
                    for index in matched[:2]
                ],
            })
        require(len(pivots) <= MAX_PIVOTS_PER_METHOD, "too many pivots: " + name)
        selected.append({
            "name": name, "descriptor": method["descriptor"],
            "instruction_count": len(instructions),
            "parsed_method_sha256": digest_method(method),
            "pivots": pivots,
        })
    return selected

def verify_producer(methods):
    """Prove the Sea Swing gate, wave configuration, and spawn request co-occur."""
    candidate = [method for method in methods
                 if method["name"] in ITEM_NAMES
                 and {p["needle"] for p in method["pivots"]} >=
                 {"SEA_SWING:", "enchantLevel:", "setLifespan:", "addFreshEntity:"}]
    require(len(candidate) == 1, "Sea Swing compiled producer not uniquely located")
    return candidate[0]["name"]

def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "unexpected publisher artifact fingerprint")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicated JAR members")
        for name in (*KNOWN_CLASS_SHA, RESOURCE, TAG):
            require(name in names, "missing exact JAR member: " + name)
        for name, expected in KNOWN_CLASS_SHA.items():
            require(digest(archive.read(name)) == expected,
                    "class differs from existing Flinging evidence: " + name)
        raw = archive.read(RESOURCE)
        require(40 <= len(raw) <= 12000, "invalid Sea Swing resource size")
        config = json.loads(raw)
        require(config.get("description", {}).get("translate") ==
                "enchantment.alexscaves.sea_swing", "unexpected enchantment key")
        require(config.get("supported_items") ==
                "#alexscaves:enchantable/ortholance", "unexpected enchantment target")
        tag_raw = archive.read(TAG)
        require(len(tag_raw) <= 12000, "oversized item tag")
        tag = json.loads(tag_raw)
        require("alexscaves:ortholance" in tag.get("values", []),
                "Ortholance missing from publisher tag")
    item_methods = select(parse_methods(javap(javap_bin, jar, ITEM[:-6].replace("/", "."))), ITEM_NAMES)
    wave_methods = select(parse_methods(javap(javap_bin, jar, WAVE[:-6].replace("/", "."))), WAVE_NAMES)
    producer = verify_producer(item_methods)
    require(any(m["name"] == "tick" for m in wave_methods), "missing WaveEntity.tick")
    registry_javap = javap(javap_bin, jar, REGISTRY[:-6].replace("/", "."))
    require("SEA_SWING" in registry_javap, "Sea Swing registry symbol missing")
    return {
        "schema_version": 1, "scope": "UNSEALED_SEA_SWING_1010_JVM_DISCOVERY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "enchantment": {"id": "alexscaves:sea_swing", "path": RESOURCE,
                        "size_bytes": len(raw), "sha256": digest(raw), "json": config},
        "item_tag": {"path": TAG, "sha256": digest(tag_raw), "json": tag},
        "class_sha256": KNOWN_CLASS_SHA,
        "producer_method": producer,
        "consumers": [{"owner": ITEM, "methods": item_methods},
                      {"owner": WAVE, "methods": wave_methods}],
        "limits": {"complete_cfg": "NOT_RECONSTRUCTED",
                   "resource_datapack_overrides": "NOT_VERIFIED",
                   "effective_damage_and_knockback": "NOT_CERTIFIED",
                   "spawn_success": "NOT_VERIFIED",
                   "mutating_hook": "NOT_VERIFIED",
                   "physical_qa": "NOT_TESTED",
                   "perk_certification": "NOT_CERTIFIED",
                   "mutation": "NO_MUTATION"},
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seal", type=Path)
    args = parser.parse_args()
    result = audit(args.jar, args.javap)
    if args.seal is not None:
        require(result == json.loads(args.seal.read_text(encoding="utf8")),
                "sealed Sea Swing discovery has drifted")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf8")
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))

if __name__ == "__main__":
    main()
