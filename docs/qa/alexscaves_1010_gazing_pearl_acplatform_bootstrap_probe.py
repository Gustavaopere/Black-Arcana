#!/usr/bin/env python3
"""Read-only exact JVM invokedynamic/bootstrap audit for ACPlatform bridge.

Audits constant-pool InvokeDynamic, BootstrapMethods and a single factory
adapter invokedynamic in the SHA-verified 1.0.10 publisher JAR. Does not load
provider code or infer engine persistence, callback safety or physical QA.
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

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACPlatform"
FACTORY = "computeIfAbsent"
LOADER = "lambda$computeIfAbsent$1"
METHOD_DESCRIPTOR = (
    "(Lnet/minecraft/world/level/storage/DimensionDataStorage;"
    "Ljava/util/function/Function;Ljava/util/function/Function;"
    "Ljava/util/function/Supplier;Ljava/lang/String;)"
    "Lnet/minecraft/world/level/saveddata/SavedData;"
)


def inspect(jar: Path, javap: str) -> dict:
    verify_artifact(jar)
    with ZipFile(jar) as archive:
        members = archive.namelist()
        require(len(members) == len(set(members)), "duplicate publisher ZIP entries")
        classfiles = [name for name in members if name.endswith(".class")]
        require(len(classfiles) == 1555, "publisher class roster drift")
        raw = archive.read(OWNER + ".class")
    rd = ClassReader(raw)
    require(rd.name == OWNER and rd.major == 65, "ACPlatform classfile mismatch")
    bootstrap = rd.attributes.get("bootstrap_methods")
    require(isinstance(bootstrap, list) and 1 <= len(bootstrap) <= 256,
            "BootstrapMethods table absent or unbounded")
    parsed = disassemble(jar, javap, OWNER)
    exact = [(key, body) for key, body in parsed.items()
             if key == (FACTORY, METHOD_DESCRIPTOR)]
    require(len(exact) == 1, "factory executable declaration missing")
    (signature, body), = exact
    require(7 in body and body[7][0] == "invokedynamic",
            "factory adapter invokedynamic at offset 7 changed")
    require([(off, op) for off, (op, _, _) in body.items()
             if op == "invokedynamic"] == [(7, "invokedynamic")],
            "factory acquired additional dynamic callsites")
    ins = summarize(rd, signature, body)
    offset, opcode, operand, symbol = 7, *body[7]
    cp_match = re.match(r"#(\d+)\s*,", operand)
    require(cp_match is not None, "invokedynamic constant pool operand missing")
    cp_index = int(cp_match.group(1))
    require(0 < cp_index < len(rd.pool), "invalid dynamic constant index")
    tag, value = rd.pool[cp_index]
    require(tag == 18, "bytecode operand not CONSTANT_InvokeDynamic")
    bootstrap_index, name_type_index = value
    require(0 <= bootstrap_index < len(bootstrap), "invalid bootstrap index")
    name_type = rd.resolve(name_type_index)
    require(name_type[0] == 12 and name_type[1] == "apply",
            "dynamic factory method name changed")
    selected = bootstrap[bootstrap_index]
    handle = selected["handle"]
    require(isinstance(handle, dict) and handle.get("reference_kind") == 6,
            "lambda metafactory bootstrap is not REF_invokeStatic")
    require("java/lang/invoke/LambdaMetafactory" in str(handle["reference"]),
            "unexpected bootstrap owner (no inferred factory)")
    arguments = selected["arguments"]
    require(1 <= len(arguments) <= 10, "unbounded bootstrap argument count")
    require(any(isinstance(arg, dict) and
                LOADER in str(arg.get("reference", ""))
                for arg in arguments), "loader lambda MethodHandle not linked")
    lambda_methods = [
        summarize(rd, key, b) for key, b in parsed.items() if key[0] == LOADER
    ]
    require(len(lambda_methods) == 1, "loader adapter method not unique")
    return {
        "owner": OWNER,
        "class_sha256": digest(raw),
        "class_major": rd.major,
        "bootstrap_count": len(bootstrap),
        "bootstrap_table_sha256": digest(canonical(bootstrap).encode("utf8")),
        "factory_method": ins,
        "factory_invokedynamic": {
            "offset": offset,
            "opcode": opcode,
            "operand": operand,
            "javap_symbol": symbol,
            "constant_pool_index": cp_index,
            "bootstrap_index": bootstrap_index,
            "name_type": name_type,
            "bootstrap_entry": selected,
        },
        "loader_adapter_method": lambda_methods[0],
        "source_scope": "JAR publisher 1.0.10 only; not the engine implementation",
    }


def run(jar: Path, javap: str, output: Path) -> None:
    require(output.suffix == ".json" and not output.exists(),
            "SHA-exact report must be write-once")
    native = inspect(jar, javap)
    report = {
        "schema_version": 1,
        "scope": "GAZING_PEARL_ACPLATFORM_INVOKEDYNAMIC_BOOTSTRAP_ONLY",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            "installed_copy_verified": False,
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
    output.write_text(canonical(report), encoding="utf8")
    print("EVIDENCE_SHA256", digest(output.read_bytes()))
    print("OWNER_CLASS_SHA256", native["class_sha256"])
    print("BOOTSTRAP_COUNT", native["bootstrap_count"])
    print("BOOTSTRAP_TABLE_SHA256", native["bootstrap_table_sha256"])
    print("INVOKEDYNAMIC", canonical(native["factory_invokedynamic"]))
    print("FACTORY_CODE_SHA256", native["factory_method"]["declaration"]["code_sha256"])
    print("LAMBDA_CODE_SHA256", native["loader_adapter_method"]["declaration"]["code_sha256"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.jar, args.javap, args.output)
