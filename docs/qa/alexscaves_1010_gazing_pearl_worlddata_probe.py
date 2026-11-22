#!/usr/bin/env python3
"""SHA-pinned read-only ACWorldData Deep One reputation boundary discovery.

Scans all publisher classfiles for direct constant-pool references, then
disassembles the bounded native ACWorldData methods and their exact caller
sites. Constant-pool references alone are not treated as executed calls.
No provider class is loaded, no gameplay simulation, no code transplantation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

WORLD = "com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData"
PEARL = "com/github/alexmodguy/alexscaves/server/item/GazingPearlItem"
REPUTATION_METHOD = "getDeepOneReputation"
CALLER_LIMIT = 100
SELECTED_LIMIT = 100


def relevant_method(name: str) -> bool:
    lower = name.lower()
    return ("reput" in lower or "deepone" in lower or
            name in {"get", "<init>", "<clinit>", "save", "acSave",
                     "lambda$get$0", "load", "read", "saveAdditional", "setDirty"})


def inspect(jar: Path, javap: str) -> dict:
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate publisher ZIP entries")
        classes = sorted(name for name in names if name.endswith(".class"))
        require(len(classes) == 1555, "publisher class roster drift")
        own_raw = z.read(WORLD + ".class")
        rd = ClassReader(own_raw)
        require(rd.name == WORLD and rd.major == 65, "ACWorldData identity drift")
        declarations = rd.methods
        selected_signatures = {
            (m["name"], m["descriptor"])
            for m in declarations
            if relevant_method(m["name"]) and "code_sha256" in m
        }
        require(any(name == REPUTATION_METHOD for name, _ in selected_signatures),
                "reputation getter not declared")
        require(1 <= len(selected_signatures) <= SELECTED_LIMIT,
                "selected WorldData methods exceed bounded scope")
        native = disassemble(jar, javap, WORLD)
        selected_methods = [
            summarize(rd, key, body)
            for key, body in sorted(native.items())
            if key in selected_signatures
        ]
        require(
            {(m["declaration"]["name"], m["declaration"]["descriptor"])
             for m in selected_methods} == selected_signatures,
            "missing declared executable WorldData method",
        )
        # Finite provider-wide reference census. These are references,
        # not proof that a method was called or that a reputation write settled.
        candidates = {}
        for path in classes:
            owner = path[:-6]
            other = ClassReader(z.read(path))
            require(other.name == owner and other.major == 65,
                    "foreign class identity drift")
            refs = []
            for index, entry in enumerate(other.pool):
                if entry is None or entry[0] not in (10, 11):
                    continue
                tag, target, signature = other.resolve(index)
                _, method_name, descriptor = signature
                if (target == WORLD and
                    ("reput" in method_name.lower() or
                     "deepone" in method_name.lower())):
                    refs.append({
                        "constant_pool_index": index,
                        "tag": tag, "name": method_name,
                        "descriptor": descriptor,
                    })
            if refs:
                candidates[owner] = {
                    "class_sha256": digest(z.read(path)),
                    "referenced_signatures": refs,
                }
        require(PEARL in candidates,
                "GazingPearlItem reference to ACWorldData disappeared")
        require(len(candidates) <= CALLER_LIMIT,
                "too many reputation reference owners; narrow scope explicitly")
        for owner, data in candidates.items():
            calls = disassemble(jar, javap, owner)
            indices = {x["constant_pool_index"] for x in data["referenced_signatures"]}
            sites = []
            for key, body in sorted(calls.items()):
                for offset, (opcode, operand, symbol) in sorted(body.items()):
                    match = re.match(r"#(\d+)", operand)
                    if (opcode.startswith("invoke") and match and
                        int(match.group(1)) in indices):
                        sites.append({
                            "caller_method": key[0],
                            "caller_descriptor": key[1],
                            "offset": offset,
                            "opcode": opcode,
                            "symbol": symbol,
                            "constant_pool_index": int(match.group(1)),
                        })
            data["executed_instruction_sites_in_disassembly"] = sites
            selected_callers = {
                (site["caller_method"], site["caller_descriptor"])
                for site in sites
            }
            caller_reader = ClassReader(z.read(owner + ".class"))
            data["referencing_bodies"] = [
                summarize(caller_reader, key, body)
                for key, body in sorted(calls.items())
                if key in selected_callers
            ]
            require(
                {(m["declaration"]["name"], m["declaration"]["descriptor"])
                 for m in data["referencing_bodies"]} == selected_callers,
                "missing targeted reference-caller body: " + owner,
            )
        pearl_sites = candidates[PEARL]["executed_instruction_sites_in_disassembly"]
        require(any(x["caller_method"] == "acInventoryTick" and
                    x["offset"] == 83 and REPUTATION_METHOD in x["symbol"]
                    for x in pearl_sites),
                "known Gazing Pearl getDeepOneReputation site drift")

        return {
            "publisher_classfiles_scanned": len(classes),
            "owner": WORLD,
            "class_sha256": digest(own_raw),
            "hierarchy": {
                "parent": rd.parent, "interfaces": rd.interfaces,
                "access": rd.access,
            },
            "fields": rd.fields,
            "declarations": declarations,
            "selected_method_count": len(selected_methods),
            "selected_methods": selected_methods,
            "reputation_reference_owners": candidates,
            "consumer_limit": CALLER_LIMIT,
            "selection_rule": "method name contains reput or deepone; plus get/construct/load/save/read/setDirty",
            "reference_scope_limit": (
                "JAR-local invoke instructions using constant-pool references "
                "to named ACWorldData reputation/DeepOne methods only"
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", type=str, default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and args.output.suffix == ".json",
            "write-once JSON report required")
    data = {
        "schema_version": 1,
        "scope": "GAZING_PEARL_ACWORLD_DATA_REPUTATION_DISCOVERY_ONLY",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            "installed_copy_verified": False,
        },
        "native": inspect(args.jar, args.javap),
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical(data), encoding="utf8")
    print("REPORT_SHA256", digest(args.output.read_bytes()))
    print("WORLD_CLASS_SHA256", data["native"]["class_sha256"])
    print("WORLD_METHODS", data["native"]["selected_method_count"])
    print("REPUTATION_REF_OWNERS",
          len(data["native"]["reputation_reference_owners"]))
    for method in data["native"]["selected_methods"]:
        d = method["declaration"]
        print("METHOD", d["name"], d["descriptor"],
              method["instruction_count"],
              method["instruction_sha256"])
    for owner, value in data["native"]["reputation_reference_owners"].items():
        print("CONSUMER", owner,
              json.dumps(value["executed_instruction_sites_in_disassembly"],
                         ensure_ascii=False, sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED NO_PHYSICAL_QA")


if __name__ == "__main__":
    main()
