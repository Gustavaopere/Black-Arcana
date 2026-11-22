#!/usr/bin/env python3
"""Bounded JAR trace of the Remote Detonator's two privileged boundaries.

This is read-only. The platform dispatcher may delegate to a substituted
implementation outside the publisher jar, so an observed bytecode method
alone is not a safe hook or an effective chunk-ticket lifecycle guarantee.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PREFIX = "com/github/alexmodguy/alexscaves/server/misc/"
OWNERS = {
    PREFIX + "ACPlatform": ("forceChunk",),
    PREFIX + "ACCompat": ("onCaughtFire",),
}


def inspect(jar: Path, javap: str, output: Path):
    verify_artifact(jar)
    require(not output.exists(), "report must be write-once")
    selected = {}
    with ZipFile(jar) as z:
        classfiles = [p for p in z.namelist() if p.endswith(".class")]
        require(len(classfiles) == 1555, "class roster drift")
        for owner, names in sorted(OWNERS.items()):
            raw = z.read(owner + ".class")
            cls = ClassReader(raw)
            require(cls.name == owner and cls.major == 65, "class identity drift")
            methods = disassemble(jar, javap, owner)
            declarations = [m for m in cls.methods if m["name"] in names]
            require(all(any(m["name"] == name for m in declarations)
                        for name in names), "missing expected direct boundary")
            relevant = [summarize(cls, key, value)
                        for key, value in sorted(methods.items())
                        if key[0] in names]
            require(len(relevant) == sum("code_sha256" in d for d in declarations),
                    "downstream owner executable bodies missing")
            selected[owner] = {
                "class_sha256": digest(raw),
                "parent": cls.parent,
                "interfaces": cls.interfaces,
                "declarations": declarations,
                "methods": relevant,
            }
    document = {
        "schema_version": 1,
        "scope": "REMOTE_DETONATOR_BOUNDARY_DISCOVERY_NOT_CERTIFIED",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "selected": selected,
        "platform_effective_implementation": "NOT_VERIFIED",
        "ticket_lifetime": "NOT_VERIFIED",
        "world_safety": "BLOCKED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(document), encoding="utf8")
    print("BOUNDARY_REPORT_SHA256", digest(output.read_bytes()))
    for owner, item in selected.items():
        print("BOUNDARY", owner, "CLASS", item["class_sha256"])
        for m in item["methods"]:
            d = m["declaration"]
            print("METHOD", owner, d["name"], d["descriptor"],
                  m["instruction_count"], m["instruction_sha256"])
            for ins in m["instructions"]:
                if (ins["opcode"].startswith("invoke") or "chunk" in ins["symbol"].lower()
                        or "fire" in ins["symbol"].lower()):
                    print("PIVOT", d["name"], ins["offset"], ins["opcode"],
                          ins["symbol"][:230])
    print("BOUNDARY_NOT_CERTIFIED NO_MUTATION")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inspect(args.jar, args.javap, args.output)
