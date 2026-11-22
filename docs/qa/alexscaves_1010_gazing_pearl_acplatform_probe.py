#!/usr/bin/env python3
"""Read-only publisher-1.0.10 ACPlatform storage bridge discovery.

Discover the exact ACPlatform.computeIfAbsent contract used by ACWorldData.get.
Scan all provider classfiles for direct method references, not arbitrary hooks.
A constant-pool reference is not automatically an executed callsite. Provider
classes are never loaded or executed. Minecraft SavedData internals and the
physically installed copy of the JAR remain out of scope.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PLATFORM = "com/github/alexmodguy/alexscaves/server/misc/ACPlatform"
WORLD = "com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData"
DESCRIPTOR = (
    "(Lnet/minecraft/world/level/storage/DimensionDataStorage;"
    "Ljava/util/function/Function;Ljava/util/function/Function;"
    "Ljava/util/function/Supplier;Ljava/lang/String;)"
    "Lnet/minecraft/world/level/saveddata/SavedData;"
)
LIMIT = 80


def inspect(jar: Path, javap: str) -> dict:
    verify_artifact(jar)
    with ZipFile(jar) as archive:
        paths = archive.namelist()
        require(len(paths) == len(set(paths)), "duplicate publisher ZIP paths")
        classes = sorted(p for p in paths if p.endswith(".class"))
        require(len(classes) == 1555, "unexpected publisher classfile universe")
        platform_bytes = archive.read(PLATFORM + ".class")
        rd = ClassReader(platform_bytes)
        require(rd.name == PLATFORM and rd.major == 65,
                "ACPlatform class identity drift")
        declared = [m for m in rd.methods
                    if m["name"] == "computeIfAbsent"
                    and m["descriptor"] == DESCRIPTOR]
        require(len(declared) == 1, "ACPlatform exact declaration missing or ambiguous")
        implemented = "code_sha256" in declared[0]
        platform_parsed = disassemble(jar, javap, PLATFORM)
        exact = [
            summarize(rd, key, body)
            for key, body in platform_parsed.items()
            if key == ("computeIfAbsent", DESCRIPTOR)
        ]
        require(len(exact) == int(implemented),
                "ACPlatform executable body/declaration discrepancy")
        lambda_declarations = [
            m for m in rd.methods
            if m["name"] == "lambda$computeIfAbsent$1" and "code_sha256" in m
        ]
        require(len(lambda_declarations) == 1,
                "factory loader adapter lambda not uniquely declared")
        loader_lambda = [
            summarize(rd, key, body)
            for key, body in platform_parsed.items()
            if key[0] == "lambda$computeIfAbsent$1"
        ]
        require(len(loader_lambda) == 1,
                "factory loader adapter lambda body missing")
        # Other platform-named implementations are candidates, not aliases
        # inferred from package names. Preserve their distinct provenance.
        platform_helpers = []
        references = {}
        for path in classes:
            owner = path[:-6]
            raw = archive.read(path)
            other = ClassReader(raw)
            require(other.name == owner and other.major == 65,
                    "classfile identity mismatch")
            if (owner != PLATFORM and "platform" in owner.lower() and
                    any(m["name"] == "computeIfAbsent" for m in other.methods)):
                platform_helpers.append({
                    "owner": owner, "class_sha256": digest(raw),
                    "declarations": [m for m in other.methods
                                     if m["name"] == "computeIfAbsent"],
                })
            matches = []
            for index, entry in enumerate(other.pool):
                if entry is None or entry[0] not in (10, 11):
                    continue
                tag, target, signature = other.resolve(index)
                _, name, descriptor = signature
                if target == PLATFORM and name == "computeIfAbsent":
                    matches.append({
                        "pool_index": index,
                        "constant_tag": tag,
                        "descriptor": descriptor,
                    })
            if matches:
                references[owner] = {
                    "class_sha256": digest(raw),
                    "typed_references": matches,
                }
        require(len(platform_helpers) <= 12, "platform helper roster unbounded")
        require(WORLD in references and len(references) <= LIMIT,
                "ACWorldData direct reference missing or owner roster unbounded")
        require(any(x["descriptor"] == DESCRIPTOR
                    for x in references[WORLD]["typed_references"]),
                "ACWorldData method signature changed")
        for owner, info in references.items():
            parsed = disassemble(jar, javap, owner)
            indices = {x["pool_index"] for x in info["typed_references"]}
            sites = []
            for (name, descriptor), body in sorted(parsed.items()):
                for offset, (opcode, operand, symbol) in sorted(body.items()):
                    found = re.match(r"#(\d+)", operand)
                    if (opcode.startswith("invoke") and found and
                            int(found.group(1)) in indices):
                        sites.append({
                            "caller": name,
                            "caller_descriptor": descriptor,
                            "offset": offset,
                            "opcode": opcode,
                            "symbol": symbol,
                            "pool_index": int(found.group(1)),
                        })
            info["invoke_sites"] = sites
            reader = ClassReader(archive.read(owner + ".class"))
            selected_keys = {(x["caller"], x["caller_descriptor"]) for x in sites}
            info["referencing_caller_bodies"] = [
                summarize(reader, key, body)
                for key, body in sorted(parsed.items())
                if key in selected_keys
            ]
            require(
                {(m["declaration"]["name"], m["declaration"]["descriptor"])
                 for m in info["referencing_caller_bodies"]} == selected_keys,
                "missing executable referencing caller body: " + owner,
            )
        require(any(
            x["caller"] == "get" and x["offset"] == 41
            and "ACPlatform.computeIfAbsent:" in x["symbol"]
            for x in references[WORLD]["invoke_sites"]
        ), "known ACWorldData.get @41 bridge missing")
        return {
            "classfiles_scanned": len(classes),
            "owner": PLATFORM,
            "class_sha256": digest(platform_bytes),
            "hierarchy": {
                "parent": rd.parent, "interfaces": rd.interfaces,
                "access": rd.access,
            },
            "fields": rd.fields,
            "method_declarations": rd.methods,
            "exact_declaration": declared[0],
            "has_executable_body": implemented,
            "exact_native_method": exact,
            "loader_adapter_lambda": loader_lambda,
            "platform_named_candidates": platform_helpers,
            "direct_referencing_owners": references,
            "limits": {
                "reference_owners": LIMIT,
                "other_platform_declaring_classes": 12,
                "constant_pool_only_is_not_invocation": True,
                "external_engine_saveddata": "NOT_INSPECTED",
            },
        }


def run(jar: Path, javap: str, output: Path) -> None:
    require(output.suffix == ".json" and not output.exists(),
            "write-once JSON output required")
    native = inspect(jar, javap)
    report = {
        "schema_version": 1,
        "scope": "GAZING_PEARL_ACPLATFORM_STORAGE_BRIDGE_DISCOVERY_ONLY",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            "installed_binary_parity": "NOT_VERIFIED",
        },
        "native": native,
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding="utf-8")
    print("REPORT_SHA256", digest(output.read_bytes()))
    print("PLATFORM_CLASS_SHA256", native["class_sha256"])
    print("EXACT_DECLARATION", native["exact_declaration"])
    print("EXACT_BODY_PRESENT", native["has_executable_body"])
    for method in (*native["exact_native_method"], *native["loader_adapter_lambda"]):
        print("METHOD", method["declaration"]["name"],
              method["declaration"]["descriptor"],
              method["instruction_count"], method["instruction_sha256"])
        for step in method["instructions"]:
            if step["opcode"].startswith(("invoke", "get", "if")):
                print("PIVOT", step["offset"], step["opcode"],
                      step["operand"], step["symbol"][:250])
    print("PLATFORM_CANDIDATES", native["platform_named_candidates"])
    print("DIRECT_CALLERS", {
        owner: {"invoke_sites": info["invoke_sites"],
                "method_sha256": [
                    m["instruction_sha256"] for m in info["referencing_caller_bodies"]
                ]}
        for owner, info in native["direct_referencing_owners"].items()
    })
    print("DISCOVERY_ONLY NOT_CERTIFIED NO_MUTATION NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    run(args.jar, args.javap, args.output)
