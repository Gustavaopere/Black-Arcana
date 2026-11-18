#!/usr/bin/env python3
"""SHA-exact read-only discovery of ACDynamicAttributeItem 1.0.10.

This is a discovery probe, not a static-contract certification, hook or runtime
test. It separates class declarations, interface implementers and typed call
references. JVM instruction slices are evidence of requests, not engine output.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, SHA1, SHA256, SIZE, digest, require, verify_artifact
)
from alexscaves_1010_action_contract_audit import parse_javap

PREFIX = "com/github/alexmodguy/alexscaves/"
TARGET = PREFIX + "server/item/ACDynamicAttributeItem"
CALLBACK = "acModifiers"
HELPER = PREFIX + "server/misc/ACCompat"
MAX_OWNERS = 45
METHOD_NAMES = frozenset({
    "acModifiers", "getAttributeModifiers", "getDefaultAttributeModifiers",
    "getOrCreateDurabilityAttributes", "getStatsForEnchantmentLevel",
    "itemAttributes", "lambda$getDefaultAttributeModifiers$0"
})


def inherited_target(owner, hierarchy, visited=()):
    if owner == TARGET:
        return True
    if owner in visited:
        raise AuditError("cyclic class hierarchy")
    info = hierarchy.get(owner)
    if info is None:
        return False
    return any(inherited_target(parent, hierarchy, (*visited, owner))
               for parent in [info["parent"], *info["interfaces"]]
               if parent)


def inspect(jar):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as archive:
        paths = archive.namelist()
        require(len(paths) == len(set(paths)), "duplicate ZIP members")
        class_paths = sorted(x for x in paths if x.endswith(".class"))
        require(len(class_paths) == 1555, "class count drift")
        hierarchy = {}
        class_hashes = {}
        typed_owners = []
        method_references = []
        declarations = []
        for path in class_paths:
            raw = archive.read(path)
            reader = ClassReader(raw)
            require(path == reader.name + ".class", "ZIP path and declared owner differ")
            require(reader.major == 65, "unexpected classfile major")
            hierarchy[reader.name] = {
                "access": reader.access,
                "parent": reader.parent,
                "interfaces": reader.interfaces,
            }
            refs = reader.typed_refs(TARGET)
            if refs:
                typed_owners.append({
                    "owner": reader.name,
                    "implements_directly": TARGET in reader.interfaces,
                    "typed_references": refs,
                })
            names = [m for m in reader.methods if m["name"] == CALLBACK]
            if names:
                declarations.append({
                    "owner": reader.name,
                    "methods": [{
                        "descriptor": m["descriptor"],
                        "access": m["access"],
                        "code_sha256": m.get("code_sha256"),
                        "code_size": m.get("code_size"),
                        "exception_handlers": m.get("exception_handlers"),
                    } for m in names],
                })
            for idx, entry in enumerate(reader.pool):
                if entry is None or entry[0] not in (10, 11):
                    continue
                tag, owner, signature = reader.resolve(idx)
                if signature[1] == CALLBACK:
                    method_references.append({
                        "caller": reader.name,
                        "constant_pool_index": idx,
                        "kind": "Methodref" if tag == 10 else "InterfaceMethodref",
                        "target_owner": owner,
                        "descriptor": signature[2],
                    })
            if refs or names or reader.name in (TARGET, HELPER):
                class_hashes[reader.name] = digest(raw)
        require(TARGET in hierarchy, "interface missing")
        require(hierarchy[TARGET]["access"] & 512, "target must be an interface")
        direct = sorted(o for o, h in hierarchy.items()
                        if o != TARGET and TARGET in h["interfaces"])
        inherited = sorted(o for o in hierarchy
                           if o != TARGET and o not in direct
                           and inherited_target(o, hierarchy))
        callers = sorted({r["caller"] for r in method_references})
        relevant = sorted({TARGET, HELPER, *direct, *inherited, *callers})
        require(0 < len(direct) <= 30, "direct implementer roster absent or unbounded")
        require(len(relevant) <= MAX_OWNERS, "too many owners for bounded inspection")
        return {
            "scope": "SHA_EXACT_DISCOVERY_ONLY_NOT_CERTIFIED",
            "artifact": {"size_bytes": SIZE, "sha1": SHA1, "sha256": SHA256,
                         "filename": jar.name},
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "target": TARGET,
            "class_entries_scanned": len(class_paths),
            "class_path_roster_sha256": digest(("\n".join(class_paths) + "\n").encode()),
            "target_metadata": hierarchy[TARGET],
            "typed_owners": typed_owners,
            "direct_implementers": direct,
            "inherited_implementers": inherited,
            "callback_declarations": declarations,
            "callback_typed_member_references": method_references,
            "class_sha256": class_hashes,
            "disassembly_owners": relevant,
        }


def disassemble(jar, javap, owners):
    methods = {}
    for owner in owners:
        completed = subprocess.run(
            [str(javap), "-classpath", str(jar), "-p", "-c", "-s",
             owner.replace("/", ".")],
            capture_output=True, text=True, timeout=60, check=False
        )
        require(completed.returncode == 0,
                "javap failed " + owner + ": " + completed.stderr[:250])
        parsed = parse_javap(completed.stdout, owner)
        selected = []
        for (name, descriptor), body in sorted(parsed.items()):
            if name not in METHOD_NAMES:
                continue
            selected.append({
                "name": name,
                "descriptor": descriptor,
                "instructions": [
                    {"offset": offset, "opcode": opcode,
                     "operand": operand, "symbol": symbol}
                    for offset, (opcode, operand, symbol) in sorted(body.items())
                ],
            })
        methods[owner] = selected
    return methods


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jar", required=True, type=Path)
    ap.add_argument("--javap", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    require(args.javap.is_file(), "javap not a file")
    require(args.output.suffix == ".json", "output must end .json")
    require(args.output.resolve() not in
            {args.jar.resolve(), Path(__file__).resolve()}, "unsafe overwrite")
    require(not args.output.exists(), "refusing to overwrite evidence")
    report = inspect(args.jar)
    report["native_methods"] = disassemble(
        args.jar, args.javap, report["disassembly_owners"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("ACDynamicAttributeItem SHA-exact 1.0.10 DISCOVERY ONLY")
    print("target:", report["target"])
    print("direct implementers:", report["direct_implementers"])
    print("inherited implementers:", report["inherited_implementers"])
    print("typed reference callers:", report["callback_typed_member_references"])
    print("method declarations:", report["callback_declarations"])
    print("class sha256:", report["class_sha256"])
    for owner, methods in report["native_methods"].items():
        for method in methods:
            print("METHOD", owner, method["name"], method["descriptor"],
                  "instructions=", len(method["instructions"]))
            for ins in method["instructions"]:
                print(" ", ins["offset"], ins["opcode"],
                      ins["operand"], ins["symbol"])
    print("END DISCOVERY; dynamic dispatch/engine/perk authorization NOT VERIFIED")


if __name__ == "__main__":
    try:
        main()
    except (AuditError, OSError, ValueError, zipfile.BadZipFile,
            subprocess.TimeoutExpired) as e:
        print("ACDynamicAttributeItem discovery failed:", e, file=sys.stderr)
        sys.exit(2)
