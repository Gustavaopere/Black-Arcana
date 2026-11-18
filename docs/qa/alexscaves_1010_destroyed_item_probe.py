#!/usr/bin/env python3
"""Read-only discovery probe for the exact Alex's Caves Continued 1.0.10 JAR.

This is NOT a seven-axis certification. It inventories the ACDestroyedItem
declaration, publisher-owned implementers, typed references and native
onDestroyed bodies. It does not establish Minecraft/NeoForge dispatch,
runtime effects, event safety, or a perk mutation hook.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, SHA1, SHA256, SIZE, digest, require, verify_artifact,
)
from alexscaves_1010_action_contract_audit import parse_javap

PREFIX = "com/github/alexmodguy/alexscaves/"
TARGET = PREFIX + "server/item/ACDestroyedItem"
PARENT = PREFIX + "server/item/RadioactiveBlockItem"
MAX_DISASSEMBLED_OWNERS = 40


def assignable(owner, hierarchy, ancestors=()):
    """Publisher class hierarchy only. External classes do not imply a match."""
    if owner == TARGET:
        return True
    if owner in ancestors:
        raise AuditError("cyclic publisher hierarchy")
    row = hierarchy.get(owner)
    if row is None:
        return False
    parents = [row["parent"], *row["interfaces"]]
    return any(assignable(parent, hierarchy, (*ancestors, owner))
               for parent in parents if parent)


def collect(jar):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as archive:
        paths = archive.namelist()
        require(len(paths) == len(set(paths)), "duplicate archive entry")
        class_paths = sorted(p for p in paths if p.endswith(".class"))
        require(len(class_paths) == 1555, "class census drift")
        hierarchy = {}
        referenced = []
        declarations = []
        class_hashes = {}
        for path in class_paths:
            raw = archive.read(path)
            reader = ClassReader(raw)
            require(path == reader.name + ".class", "class path/name drift")
            require(reader.major == 65, "unexpected classfile major")
            hierarchy[reader.name] = {
                "parent": reader.parent,
                "interfaces": reader.interfaces,
                "access": reader.access,
            }
            refs = reader.typed_refs(TARGET)
            if refs:
                referenced.append({
                    "owner": reader.name,
                    "direct_implementer": TARGET in reader.interfaces,
                    "typed_references": refs,
                })
            matches = [m for m in reader.methods if m["name"] == "onDestroyed"]
            if reader.name in (TARGET, PARENT) or refs or TARGET in reader.interfaces:
                class_hashes[reader.name] = digest(raw)
                if matches:
                    declarations.append({
                        "owner": reader.name,
                        "methods": [{
                            "name": m["name"], "descriptor": m["descriptor"],
                            "access": m["access"],
                            "code_sha256": m.get("code_sha256"),
                            "code_size": m.get("code_size"),
                            "exception_handlers": m.get("exception_handlers"),
                        } for m in matches],
                    })
        require(TARGET in hierarchy, "ACDestroyedItem missing from publisher")
        require(hierarchy[TARGET]["access"] & 0x0200, "target not interface")
        direct = sorted(owner for owner, row in hierarchy.items()
                        if owner != TARGET and TARGET in row["interfaces"])
        inherited = sorted(owner for owner in hierarchy
                           if owner != TARGET and owner not in direct
                           and assignable(owner, hierarchy))
        member_callers = sorted({
            row["owner"] for row in referenced
            if any(ref["kind"] in ("method_reference", "interface_method_reference")
                   for ref in row["typed_references"])
        })
        chosen = sorted({TARGET, PARENT, *direct, *inherited, *member_callers})
        require(len(chosen) <= MAX_DISASSEMBLED_OWNERS,
                "disassembly candidate set exceeds bound; explicitly review scope")
        return {
            "artifact": {"file": jar.name, "size_bytes": SIZE,
                         "sha1": SHA1, "sha256": SHA256},
            "claim_scope": "READ_ONLY_SHA_EXACT_DISCOVERY_NOT_CERTIFICATION",
            "static_technical_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_delta": 0,
            "target": TARGET,
            "target_access": hierarchy[TARGET]["access"],
            "target_interfaces": hierarchy[TARGET]["interfaces"],
            "target_parent": hierarchy[TARGET]["parent"],
            "class_entries_scanned": len(class_paths),
            "class_path_roster_sha256": digest(("\n".join(class_paths) + "\n").encode()),
            "typed_reference_owners": referenced,
            "direct_implementers": direct,
            "inherited_implementers_within_publisher": inherited,
            "typed_member_callers": member_callers,
            "on_destroyed_declarations_in_bounded_owners": declarations,
            "bounded_class_sha256": class_hashes,
            "disassembly_owners": chosen,
        }


def disassemble(jar, javap, owners):
    result = {}
    for owner in owners:
        proc = subprocess.run(
            [str(javap), "-classpath", str(jar), "-p", "-c", "-s",
             owner.replace("/", ".")],
            capture_output=True, text=True, timeout=60, check=False,
        )
        require(proc.returncode == 0,
                "javap failure for " + owner + ": " + proc.stderr[:300])
        parsed = parse_javap(proc.stdout, owner)
        methods = []
        for (name, descriptor), body in sorted(parsed.items()):
            if name != "onDestroyed":
                continue
            methods.append({
                "name": name, "descriptor": descriptor,
                "instructions": [
                    {"offset": offset, "opcode": opcode,
                     "operand": operand, "symbol": symbol}
                    for offset, (opcode, operand, symbol) in sorted(body.items())
                ],
            })
        result[owner] = methods
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    for protected in (args.jar, Path(__file__)):
        require(args.output.resolve() != protected.resolve(),
                "cannot overwrite source or publisher artifact")
    require(args.output.suffix == ".json", "JSON output required")
    require(args.javap.is_file(), "javap executable not found")
    report = collect(args.jar)
    report["native_on_destroyed_bodies"] = disassemble(
        args.jar, args.javap, report["disassembly_owners"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    require(not args.output.exists(), "refuse to overwrite evidence")
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print("EXACT-1.0.10 ACDestroyedItem read-only discovery, NOT CERTIFIED")
    print("target:", report["target"])
    print("target declarations:",
          [r for r in report["on_destroyed_declarations_in_bounded_owners"]
           if r["owner"] == TARGET])
    print("direct implementers:", report["direct_implementers"])
    print("bounded exact class SHA-256:", report["bounded_class_sha256"])
    print("bounded onDestroyed declarations:", report["on_destroyed_declarations_in_bounded_owners"])
    print("inherited implementers:", report["inherited_implementers_within_publisher"])
    print("typed method-reference callers:", report["typed_member_callers"])
    for owner, methods in report["native_on_destroyed_bodies"].items():
        for method in methods:
            print("BODY", owner, method["name"], method["descriptor"])
            for row in method["instructions"]:
                print(" ", row["offset"], row["opcode"], row["operand"],
                      row["symbol"])
    print("This is discovery only; engine dispatch, world safety and perks remain unverified.")


if __name__ == "__main__":
    try:
        main()
    except (AuditError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print("ACDestroyedItem probe failed:", exc, file=sys.stderr)
        sys.exit(2)
