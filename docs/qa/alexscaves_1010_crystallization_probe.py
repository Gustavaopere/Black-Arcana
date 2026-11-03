#!/usr/bin/env python3
"""Read-only Alex's Caves Continued 1.0.10 Crystallization / Galena Gauntlet probe.

Records selected compiled JVM callsites and resource bytes from SHA-exact publisher JAR.
This is not a complete CFG, a runtime/gameplay test, or a mutating integration API.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "EXACT_ALEXSCAVES_1010_CRYSTALLIZATION_GALENA_GAUNTLET_SELECTED_ABI"
GAUNTLET = BASE + "server/item/GalenaGauntletItem.class"
WEAPON = BASE + "server/entity/item/MagneticWeaponEntity.class"
ENCH_REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
TAG_REGISTRY = BASE + "server/misc/ACTagRegistry.class"
OWNER_CLASSES = (GAUNTLET, WEAPON, ENCH_REGISTRY, TAG_REGISTRY)
ENCHANT = "data/alexscaves/enchantment/crystallization.json"
TAGS = {
    "gauntlet": "enchantable/galena_gauntlet.json",
    "crystallization": "galena_gauntlet_crystallization_items.json",
    "ferromagnetic": "ferromagnetic_items.json",
}
METHODS = {
    GAUNTLET: ("use", "onUseTick", "releaseUsing"),
    WEAPON: ("tick", "hurtEntity", "getController", "getTarget",
             "isOwnerWearingGauntlet", "plopItem", "addAdditionalSaveData",
             "readAdditionalSaveData"),
}
PIVOTS = {
    "use": ("CRYSTALLIZATION:", "GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:",
            "MAGNETIC_ITEMS:", "hurtAndBreakUsedHand:", "startUsingItem:"),
    "onUseTick": ("CRYSTALLIZATION:", "GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:",
                  "MAGNETIC_ITEMS:", "getEntitiesOfClass:", "inflate:",
                  "createEntity:", "setItemStack:", "setControllerUUID:",
                  "setCount:", "addFreshEntity:"),
    "releaseUsing": ("addCooldown:",),
    "tick": ("FIELD_EXTENSION:", "FERROUS_HASTE:", "getHitResultOnViewVector:",
              "hurtEntity:", "destroyBlockProgress:", "destroyBlock:", "plopItem:"),
    "hurtEntity": ("ACCompat.hurt:", "postAttackEffects:", "damageItem:", "hurtEnemy:"),
    "getController": ("getControllerUUID:",),
    "getTarget": ("TARGET_ID:",),
    "isOwnerWearingGauntlet": ("GALENA_GAUNTLET:",),
    "plopItem": ("spawnAtLocation:",),
    "addAdditionalSaveData": ("ControllerUUID", "WeaponStack"),
    "readAdditionalSaveData": ("ControllerUUID", "WeaponStack"),
}
MANDATORY = {
    "use": ("CRYSTALLIZATION:", "GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:", "MAGNETIC_ITEMS:"),
    "onUseTick": ("CRYSTALLIZATION:", "GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:", "MAGNETIC_ITEMS:",
                  "getEntitiesOfClass:", "addFreshEntity:"),
    "releaseUsing": ("addCooldown:",),
    "tick": ("FIELD_EXTENSION:", "FERROUS_HASTE:", "getHitResultOnViewVector:"),
    "hurtEntity": ("ACCompat.hurt:",),
}
MAX_METHOD_INSTRUCTIONS = 2000
MAX_RESOURCE_BYTES = 32000

def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)

def short(ins: dict) -> dict:
    return {k: ins[k] for k in ("offset", "opcode", "operand", "symbol")}

def exact_method(parsed: list, name: str) -> dict:
    matching = [m for m in parsed if name_of(m) == name]
    require(len(matching) == 1, "missing or duplicate exact JVM method: " + name)
    m = matching[0]
    instructions = m["instructions"]
    require(2 <= len(instructions) <= MAX_METHOD_INSTRUCTIONS,
            "out of bounds method instruction count: " + name)
    offsets = [i["offset"] for i in instructions]
    require(offsets == sorted(set(offsets)),
            "non-unique or unsorted JVM offsets: " + name)
    return m

def evidence(m: dict, name: str) -> dict:
    instructions = m["instructions"]
    pivots = []
    for symbol in PIVOTS.get(name, ()):
        matched = [index for index, item in enumerate(instructions)
                   if symbol in item["symbol"]]
        if not matched:
            continue
        # Bounded local windows, not complete Java source or CFG.
        entries = []
        for idx in matched[:2]:
            entries.append({
                "at": instructions[idx]["offset"],
                "window": [short(x) for x in instructions[max(0,idx-5):idx+7]],
            })
        pivots.append({"needle": symbol, "match_count": len(matched),
                       "locations": entries})
    observed = {x["needle"] for x in pivots}
    for needed in MANDATORY.get(name, ()):
        require(needed in observed, "missing critical compiled pivot " + name + ": " + needed)
    return {
        "name": name, "descriptor": m["descriptor"],
        "instruction_count": len(instructions),
        "parsed_method_sha256": digest_method(m),
        "pivot_windows": pivots,
        "scope": "BOUNDED_SELECTED_JVM_WINDOWS_NOT_COMPLETE_CFG",
    }

def json_resource(z: zipfile.ZipFile, path: str) -> dict:
    raw = z.read(path)
    require(0 < len(raw) <= MAX_RESOURCE_BYTES, "resource length out of bounds: " + path)
    data = json.loads(raw)
    require(isinstance(data, dict), "non-object JSON resource: " + path)
    return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw), "json": data}

def find_tag(names: set[str], suffix: str) -> str:
    options = [f"data/alexscaves/tags/{singular}/{suffix}"
               for singular in ("item", "items")]
    present = [p for p in options if p in names]
    require(len(present) == 1, "missing or ambiguous exact publisher item tag: " + suffix)
    return present[0]

def check_resources(resources: dict) -> None:
    ench = resources["enchantment"]["json"]
    require(ench.get("description", {}).get("translate") ==
            "enchantment.alexscaves.crystallization", "wrong enchantment identity")
    require(ench.get("supported_items") ==
            "#alexscaves:enchantable/galena_gauntlet", "wrong supported item tag")
    require(ench.get("max_level") == 1, "unexpected publisher max level")
    require("alexscaves:galena_gauntlet" in resources["gauntlet"]["json"].get("values", []),
            "gauntlet absent from publisher support tag")
    require("#alexscaves:ferromagnetic_items" in
            resources["crystallization"]["json"].get("values", []),
            "missing base ferromagnetic subset in crystallization tag")
    require(isinstance(resources["ferromagnetic"]["json"].get("values"), list),
            "missing ferromagnetic item roster")

def audit(jar: Path, javap_bin: str) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "JAR SHA-1/SHA-256/length is not publisher Alex's Caves 1.0.10")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate entries in physical publisher JAR")
        all_names = set(names)
        require(ENCHANT in all_names, "missing crystallization JSON resource")
        require(all(p in all_names for p in OWNER_CLASSES), "missing compiled owner class")
        tag_files = {name: find_tag(all_names, path) for name,path in TAGS.items()}
        resources = {"enchantment": json_resource(z, ENCHANT)}
        resources.update({name: json_resource(z, path) for name,path in tag_files.items()})
        check_resources(resources)
        classes = [{"path": path, "sha256": hashlib.sha256(z.read(path)).hexdigest()}
                   for path in OWNER_CLASSES]
    consumers = []
    for owner, requested in METHODS.items():
        parsed = parse_methods(javap(javap_bin, jar, owner[:-6].replace("/", ".")))
        for name in requested:
            consumers.append({
                "owner": owner,
                "class_sha256": next(item["sha256"] for item in classes if item["path"]==owner),
                "method": evidence(exact_method(parsed, name), name),
            })
    return {
        "schema_version": 1, "scope": SCOPE,
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "resource_evidence": resources, "class_evidence": classes,
        "selected_consumers": consumers,
        "limits": {
            "compiled_methods_examined": "BOUNDED_SELECTED_WINDOWS_ONLY",
            "full_control_flow": "NOT_RECONSTRUCTED",
            "external_source_declared_version": "1.1.1_NOT_JAR_CONTRACT",
            "effective_enchanting_datapack_tags": "NOT_VERIFIED",
            "item_eligibility_in_real_modpack": "NOT_TESTED",
            "accepted_spawn_and_inventory_loss": "NOT_TESTED",
            "PvP_claims_block_protection_multiplayer": "NOT_VERIFIED",
            "effective_targeting_mining_damage_and_cooldown": "NOT_TESTED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "perk_certification": "NOT_CERTIFIED",
        },
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path)
    p.add_argument("--seal", type=Path)
    a = p.parse_args()
    result = audit(a.jar, a.javap)
    if a.seal is not None:
        require(json.loads(a.seal.read_text(encoding="utf-8")) == result,
                "exact publisher 1.0.10 Crystallization evidence seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print("BEGIN_EXACT_CRYSTALLIZATION_EVIDENCE")
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
    print("END_EXACT_CRYSTALLIZATION_EVIDENCE")

if __name__ == "__main__":
    main()
