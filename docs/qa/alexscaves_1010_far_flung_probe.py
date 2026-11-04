#!/usr/bin/env python3
"""Read-only SHA-exact Candy Cane Hook / Far Flung ABI discovery and seal.

Selected JVM windows only. No decompilation, full CFG, runtime execution,
hook authorization, source parity, world-safety validation or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ITEM = BASE + "server/item/CandyCaneHookItem.class"
HOOK = BASE + "server/entity/item/CandyCaneHookEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/far_flung.json"
TAG = "data/alexscaves/tags/item/enchantable/candy_cane_hook.json"
SCOPE = "SHA_EXACT_1010_FAR_FLUNG_CANDY_CANE_HOOK_SELECTED_JVM_EVIDENCE"

SELECT = {
    ITEM: ("use", "canLaunchHook", "acInventoryTick", "setLastLaunchedHookUUID",
           "setReelingIn", "getEnchantmentValue", "isEnchantable"),
    HOOK: ("CandyCaneHookEntity", "tick", "fling", "onHitEntity",
           "onHitBlock", "getGravity", "readAdditionalSaveData",
           "addAdditionalSaveData", "setOwner", "getOwner"),
}
FOCUS = {
    "CandyCaneHookEntity": ("FAR_FLUNG:", "SHARP_CANE:", "STRAIGHT_HOOK:",
                            "enchantLevel:", "setDeltaMovement:", "setDamage:"),
    "use": ("CandyCaneHookEntity", "addFreshEntity:", "hurtAndBreak:",
            "setLastLaunchedHookUUID:", "canLaunchHook:"),
    "canLaunchHook": ("LastLaunchedHookUUID", "getEntity:", "isAlive:", "getOwner:"),
    "acInventoryTick": ("isClientSide:", "setReelingIn:",
                        "setLastLaunchedHookUUID:"),
    "setLastLaunchedHookUUID": ("LastLaunchedHookUUID", "setTag:"),
    "setReelingIn": ("Reeling", "setTag:"),
    "getEnchantmentValue": (),
    "isEnchantable": (),
    "tick": ("discard:", "setReeling:", "getHookedEntity:", "getOwner:",
             "setDeltaMovement:", "getEntities:"),
    "fling": ("getHookedPosition:", "setDeltaMovement:"),
    "onHitEntity": ("setHookedEntityUUID:", "setHookedPosition:"),
    "onHitBlock": ("setHookedPosition:", "onProjectileHit:"),
    "getGravity": (),
    "readAdditionalSaveData": ("getUUID:", "getBoolean:", "getFloat:"),
    "addAdditionalSaveData": ("putUUID:", "putBoolean:", "putFloat:"),
    "setOwner": (),
    "getOwner": (),
}

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)

def slim(row: dict) -> dict:
    return {key: row[key] for key in ("offset", "opcode", "operand", "symbol")}

def selected_methods(methods: list, owner: str) -> list:
    selected = []
    for m in methods:
        name = name_of(m)
        if name not in SELECT[owner]:
            continue
        ins = m["instructions"]
        require(1 <= len(ins) <= 2400, "unexpected method length " + name)
        offsets = [x["offset"] for x in ins]
        require(offsets == sorted(set(offsets)), "nonunique or unsorted offsets " + name)
        windows = []
        used = set()
        for token in FOCUS.get(name, ()):
            found = [i for i, x in enumerate(ins) if token in x["symbol"]]
            for idx in found[:2]:
                center = ins[idx]["offset"]
                if (token, center) in used:
                    continue
                used.add((token, center))
                windows.append({
                    "token": token,
                    "offset": center,
                    "matches": len(found),
                    "instructions": [slim(x) for x in ins[max(0, idx-5):idx+9]],
                })
        require(len(windows) <= 32, "unbounded windows " + name)
        selected.append({
            "name": name, "descriptor": m["descriptor"],
            "header": m["header"], "instruction_count": len(ins),
            "parsed_method_sha256": digest_method(m),
            "selected_windows": windows,
        })
    require(len(selected) <= 35, "unbounded method selection")
    return selected

def validate_consumer(rows: list) -> None:
    constructors = [r for r in rows if r["name"] == "CandyCaneHookEntity"
                    and "Lnet/minecraft/world/item/ItemStack;" in r["descriptor"]]
    require(len(constructors) == 1, "missing/ambiguous itemstack constructor")
    require(any(w["token"] == "FAR_FLUNG:" for w in constructors[0]["selected_windows"]),
            "FAR_FLUNG exact consumer not observed")
    require(any(w["token"] == "setDeltaMovement:" for w in constructors[0]["selected_windows"]),
            "launch velocity setter not observed")

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def audit(jar: Path, javap_binary: str) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate JAR entries")
        for path in (ITEM, HOOK, REGISTRY, ENCHANT):
            require(path in names, "required member missing " + path)
        raw = archive.read(ENCHANT)
        require(len(raw) <= 12000, "enchantment JSON oversized")
        enchant = json.loads(raw)
        require(isinstance(enchant, dict)
                and enchant.get("description", {}).get("translate")
                    == "enchantment.alexscaves.far_flung",
                "publisher enchantment identity mismatch")
        class_hashes = {p: digest(archive.read(p)) for p in (ITEM, HOOK, REGISTRY)}
        tag_data = None
        if TAG in names:
            content = archive.read(TAG)
            require(len(content) <= 12000, "tag oversized")
            tag_data = {"sha256": digest(content), "json": json.loads(content)}
    evidence = []
    for owner in (ITEM, HOOK):
        methods = parse_methods(javap(javap_binary, jar, owner[:-6].replace("/", ".")))
        rows = selected_methods(methods, owner)
        if owner == HOOK:
            validate_consumer(rows)
        evidence.append({"owner": owner, "class_sha256": class_hashes[owner],
                         "own_method_count": len(methods), "methods": rows})
    registry_text = javap(javap_binary, jar, REGISTRY[:-6].replace("/", "."))
    require("FAR_FLUNG" in registry_text and "far_flung" in registry_text,
            "compiled Far Flung registry missing")
    return {
        "schema_version": 1, "scope": SCOPE,
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "enchantment": {"id": "alexscaves:far_flung", "resource_path": ENCHANT,
                        "resource_sha256": digest(raw), "json": enchant},
        "item_tag": {"path": TAG, "evidence": tag_data},
        "classes": class_hashes,
        "consumers": evidence,
        "limits": {
            "selected_jvm_windows_only": True,
            "public_source_111_is_exact_authority": False,
            "complete_jvm_cfg": "NOT_RECONSTRUCTED",
            "datapack_effective_tag": "NOT_VERIFIED",
            "launch_distance_observed_in_game": "NOT_TESTED",
            "effective_damage_and_grappling": "NOT_CERTIFIED",
            "server_replay_and_pvp": "NOT_VERIFIED",
            "safe_mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "perk_certification": "NOT_CERTIFIED",
        }
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--seal", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = audit(args.jar, args.javap)
    if args.seal:
        require(result == json.loads(args.seal.read_text(encoding="utf8")),
                "Far Flung SHA-exact evidence seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n",
                               encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    main()
