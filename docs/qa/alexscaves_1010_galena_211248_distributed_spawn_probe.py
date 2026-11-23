#!/usr/bin/env python3
"""Read-only exact NeoForge 21.1.248 installed-distribution entity-admission ABI.

Examines official --installServer NeoForge overlay and Minecraft 1.21.1 SRG
classfiles, not ModLauncher-transformed classes or the physical modpack. Emits
only class/method hashes, descriptors and selected typed JVM callsite metadata.
Does NOT ship Mojang/NeoForge code, test Galena spawn or certify hooks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble
from neoforge_211248_custom_data_delegate_probe import choose_archive
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNERS = {
    "Level": "net/minecraft/world/level/Level",
    "ServerLevel": "net/minecraft/server/level/ServerLevel",
    "LevelWriter": "net/minecraft/world/level/LevelWriter",
    "PersistentEntitySectionManager": (
        "net/minecraft/world/level/entity/PersistentEntitySectionManager"),
}
TARGET_NAMES = {
    "addFreshEntity", "addFreshEntityWithPassengers",
    "tryAddFreshEntityWithPassengers", "addEntity", "addPlayer",
    "addDuringTeleport", "addWithUUID", "addNewEntity",
    "addNewEntityWithoutEvent", "addEntityWithoutEvent",
}
CALLEE_NAMES = TARGET_NAMES | {"onAddedToLevel"}
MAX_CLASS_BYTES = 650_000
MAX_METHODS = 1000
MAX_SELECTED = 32
MAX_INSTRUCTIONS = 6500
MAX_CALLS = 125

def callsites(reader: ClassReader, body: dict) -> list[dict]:
    results = []
    for offset, (opcode, operand, symbol) in sorted(body.items()):
        if not opcode.startswith("invoke") or opcode == "invokedynamic":
            continue
        match = re.match(r"#(\d+)(?:\s|$)", operand)
        if not match:
            continue
        index = int(match.group(1))
        require(0 < index < len(reader.pool), "invalid invoked constant")
        entry = reader.pool[index]
        if entry is None or entry[0] not in (10, 11):
            continue
        _, owner, pair = reader.resolve(index)
        _, name, descriptor = pair
        if (name not in CALLEE_NAMES and
                not owner.endswith("/EntityJoinLevelEvent")):
            continue
        results.append({
            "offset": offset, "opcode": opcode, "cp_index": index,
            "owner": owner, "name": name, "descriptor": descriptor,
        })
    require(len(results) <= MAX_CALLS, "selected callsite budget")
    return results

def summary(reader: ClassReader, key: tuple, body: dict) -> dict:
    declarations = [m for m in reader.methods
                    if (m["name"], m["descriptor"]) == key]
    require(len(declarations) == 1, "method identity not unique: " + str(key))
    row = declarations[0]
    require(len(body) <= MAX_INSTRUCTIONS, "bounded method body exceeded")
    branches = {"conditional": 0, "unconditional": 0, "switch": 0,
                "returns": 0, "throws": 0}
    for opcode, _, _ in body.values():
        if opcode.startswith("if"):
            branches["conditional"] += 1
        elif opcode in ("goto", "goto_w", "jsr", "jsr_w"):
            branches["unconditional"] += 1
        elif opcode in ("tableswitch", "lookupswitch"):
            branches["switch"] += 1
        elif opcode.endswith("return"):
            branches["returns"] += 1
        elif opcode == "athrow":
            branches["throws"] += 1
    return {
        "name": key[0], "descriptor": key[1], "code_sha256": row["code_sha256"],
        "code_size": row["code_size"], "instruction_count": len(body),
        "branch_shape": branches, "calls": callsites(reader, body),
    }

def inspect(server: Path, srg: Path, javap: str) -> dict:
    verified = verify_distribution(server, srg)
    with ZipFile(server) as neo, ZipFile(srg) as minecraft:
        a, b = set(neo.namelist()), set(minecraft.namelist())
        require(len(a) == len(neo.namelist()) and
                len(b) == len(minecraft.namelist()),
                "duplicate entries in exact distributed JAR")
        classes = {}
        for key, owner in OWNERS.items():
            path = owner + ".class"
            origin = choose_archive(path, a, b)
            require(origin in ("NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"),
                    "distributed engine owner unavailable: " + key)
            blob = (neo if origin == "NEOFORGE_OVERLAY" else minecraft).read(path)
            require(64 <= len(blob) <= MAX_CLASS_BYTES and
                    blob[:4] == b"\xca\xfe\xba\xbe",
                    "bounded classfile identity")
            classes[key] = (owner, origin, blob)

    classpath = str(server) + ":" + str(srg)
    result = {}
    for key, (owner, origin, blob) in classes.items():
        reader = ClassReader(blob)
        require(reader.name == owner and reader.major == 65 and
                len(reader.methods) <= MAX_METHODS,
                "classfile JVM identity/size changed: " + key)
        methods = [m for m in reader.methods if m["name"] in TARGET_NAMES]
        require(len(methods) <= MAX_SELECTED, "method subset budget")
        parsed = disassemble(classpath, javap, owner)
        selected = []
        for m in sorted(methods, key=lambda x: (x["name"], x["descriptor"])):
            method_key = (m["name"], m["descriptor"])
            require(method_key in parsed, "missing javap method declaration")
            body = parsed[method_key]
            if "code_sha256" in m:
                selected.append(summary(reader, method_key, body))
            else:
                require(not body and m["access"] & (0x0400 | 0x0100),
                        "method missing Code without abstract/native status")
                selected.append({
                    "name": m["name"], "descriptor": m["descriptor"],
                    "abstract_or_native": True, "access": m["access"],
                })
        result[key] = {
            "owner": owner, "source_archive": origin,
            "sha256": digest(blob), "java_major": reader.major,
            "parent": reader.parent, "interfaces": reader.interfaces,
            "declared_method_count": len(reader.methods),
            "selected_methods": selected,
            "not_modlauncher_transformed": True,
        }
    return {
        "schema": 1,
        "scope": "GALENA_NEOFORGE_211248_DISTRIBUTED_ENTITY_ADMISSION_ABI_DISCOVERY_ONLY",
        "artifact": verified,
        "classes": result,
        "limits": {
            "installed_modpack_parity": "NOT_VERIFIED",
            "modlauncher_transformed_bytecode": "NOT_OBSERVED",
            "real_galena_entity_join_event": "NOT_VERIFIED",
            "callsite_dispatch_without_transformers": "NOT_VERIFIED",
            "galena_stack_settlement": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_delta": 0,
        },
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", type=Path, required=True)
    p.add_argument("--srg", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    require(args.output.suffix == ".json" and not args.output.exists(),
            "write-once JSON evidence")
    result = inspect(args.server, args.srg, args.javap)
    raw = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n"
    require(0 < len(raw) <= 200_000, "report size budget")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest(), "BYTES", len(raw))
    for k, obj in result["classes"].items():
        print("CLASS", k, obj["source_archive"], obj["sha256"],
              "DECLARED", obj["declared_method_count"],
              "SELECTED", len(obj["selected_methods"]))
        for method in obj["selected_methods"]:
            print("METHOD", k, method["name"], method["descriptor"],
                  method.get("code_sha256", "ABSTRACT"), "CALLS",
                  len(method.get("calls", [])))
            for c in method.get("calls", []):
                print("CALL", k, method["name"], c)
    print("NO_MUTATION NO_MODLAUNCHER_PROOF NO_PHYSICAL_QA")

if __name__ == "__main__":
    main()
