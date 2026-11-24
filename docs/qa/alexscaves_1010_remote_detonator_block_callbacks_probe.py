#!/usr/bin/env python3
"""Read-only publisher block callback and registration discovery.

Trace bounded symbolic JVM member references and registry constructor handles.
No game execution, no copied provider implementation, no hook certification.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze

PREFIX = "com/github/alexmodguy/alexscaves/server/"
LIMITS = {
    "effective_tag_membership": "NOT_VERIFIED",
    "registry_bootstrap": "NOT_VERIFIED",
    "actual_ignition_or_spawn": "NOT_VERIFIED",
    "engine_tnt_dispatch": "NOT_VERIFIED",
    "world_safety": "BLOCKED",
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}
CALLBACK_NAMES = {"onCaughtFire", "ignite", "explode", "prime", "wasExploded",
                  "onPlace", "neighborChanged", "useItemOn", "useWithoutItem",
                  "playerWillDestroy", "onProjectileHit", "tick", "<init>",
                  "getFuse", "setFuse", "addAdditionalSaveData", "readAdditionalSaveData",
                  "remove", "getOwner", "setOwner"}


def load(archive, owner):
    raw = archive.read(owner + ".class")
    reader = ClassReader(raw)
    require(reader.name == owner and reader.major == 65, "class identity drift: " + owner)
    return raw, reader


def interesting_class(owner):
    base = owner.rsplit("/", 1)[-1].lower()
    return owner.startswith(PREFIX) and (
        "nuclearbomb" in base or base == "nuclearexplosionentity"
    ) and "$" not in base


def references(body):
    return [row for row in body.values() if any(
        t in row[2].lower() for t in ("nuclearbomb", "nuclearexplosionentity", "oncaughtfire")
    )]


def inspect_methods(reader, parsed, select):
    methods = []
    for key, body in sorted(parsed.items()):
        if not body or not select(key, body):
            continue
        decls = [m for m in reader.methods if (m["name"], m["descriptor"]) == key]
        require(len(decls) == 1 and "code_sha256" in decls[0], "executable declaration mismatch")
        summary = analyze(reader, body, decls[0])
        summary["instruction_sha256"] = summarize(reader, key, body)["instruction_sha256"]
        summary["numeric_literals"] = [
            {"offset": offset, "opcode": opcode, "operand": operand, "symbol": symbol}
            for offset, (opcode, operand, symbol) in sorted(body.items())
            if opcode.startswith(("iconst_", "fconst_", "dconst_", "lconst_"))
            or opcode in {"bipush", "sipush"}
            or (opcode.startswith("ldc") and symbol.startswith(("int ", "float ", "double ", "long ")))
        ]
        methods.append(summary)
    require(len(methods) <= 80, "selected method budget")
    return methods


def registry(archive, jar, javap, owner, targets):
    raw, reader = load(archive, owner)
    parsed = disassemble(jar, javap, owner)
    factories = {}
    for key, body in sorted(parsed.items()):
        if key[0] == "<clinit>":
            continue
        created = [{"offset": p, "owner": s[6:]} for p, (op, _, s) in sorted(body.items())
                   if op == "new" and s.startswith("class ") and s[6:] in targets]
        if created:
            factories[key] = {"method": key[0], "descriptor": key[1],
                              "constructor_owners": created,
                              "instruction_sha256": summarize(reader, key, body)["instruction_sha256"]}
    # Entity factory constructors may be method handles, not NEW instructions.
    bootstrap_links = []
    clinit = parsed.get(("<clinit>", "()V"), {})
    offsets = sorted(clinit)
    for i, offset in enumerate(offsets):
        op, arg, _ = clinit[offset]
        if op != "invokedynamic":
            continue
        match = re.fullmatch(r"#(\d+)(?:\s*,\s*\d+)?", arg)
        require(match is not None, "unparsed registry invokedynamic operand")
        tag, index, _ = reader.resolve(int(match.group(1)))
        require(tag == 18, "registry bootstrap constant kind")
        b = reader.attributes["bootstrap_methods"][index]
        links = []
        for v in b["arguments"]:
            ref = v.get("reference") if isinstance(v, dict) else None
            if not isinstance(ref, list) or len(ref) != 3 or ref[0] not in (10, 11):
                continue
            _, ref_owner, signature = ref
            if ref_owner in targets or (ref_owner == owner and (signature[1], signature[2]) in factories):
                links.append({"kind": v["reference_kind"], "owner": ref_owner,
                              "name": signature[1], "descriptor": signature[2]})
        if links:
            # Nearby registry identifier and field references; not a proof of executed registration.
            context = [{"offset": p, "opcode": clinit[p][0], "symbol": clinit[p][2]}
                       for p in offsets[max(0, i-5):i+6]
                       if clinit[p][2].startswith(("String ", "Field ", "Method ", "InterfaceMethod "))]
            bootstrap_links.append({"offset": offset, "bootstrap_index": index,
                                    "handles": links, "symbolic_context": context})
    return {"owner": owner, "class_sha256": digest(raw),
            "constructor_factories": list(factories.values()), "bootstrap_links": bootstrap_links}


def inspect(jar, javap, output):
    verify_artifact(jar)
    require(not output.exists(), "write-once report required")
    with ZipFile(jar) as z:
        paths = z.namelist()
        require(len(paths) == len(set(paths)), "duplicate archive entries")
        classes = sorted(p[:-6] for p in paths if p.endswith(".class"))
        require(len(classes) == 1555, "publisher roster drift")
        targets = {p for p in classes if interesting_class(p)}
        require(1 <= len(targets) <= 12, "nuclear candidate roster budget")
        data = {}
        for owner in sorted(targets):
            raw, reader = load(z, owner)
            parsed = disassemble(jar, javap, owner)
            # Tick of downstream explosion entity is a separate later causal audit.
            def select(key, body):
                if owner.endswith("/NuclearExplosionEntity") and key[0] == "tick":
                    return False
                return key[0] in CALLBACK_NAMES or bool(references(body))
            methods = inspect_methods(reader, parsed, select)
            data[owner] = {"class_sha256": digest(raw), "parent": reader.parent,
                           "interfaces": reader.interfaces,
                           "declarations": [{"name": m["name"], "descriptor": m["descriptor"],
                                             "code_sha256": m.get("code_sha256")} for m in reader.methods],
                           "selected_methods": methods}
        registry_owners = [p for p in classes if p.rsplit("/", 1)[-1] in {"ACBlockRegistry", "ACEntityRegistry"}
                           and p.startswith(PREFIX)]
        require(len(registry_owners) == 2, "registry owners unresolved")
        registries = {o: registry(z, jar, javap, o, targets) for o in registry_owners}
    report = {"schema_version": 1, "scope": "PUBLISHER_BLOCK_CALLBACK_DISCOVERY_ONLY",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "class_entries_scanned": len(classes), "classes": data, "registries": registries,
              "limits": LIMITS}
    content = canonical(report)
    require(len(content.encode("utf8")) <= 900000, "bounded report size")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf8") as f:
        f.write(content)
    print("BLOCK_REPORT_SHA256", digest(output.read_bytes()), "BYTES", output.stat().st_size)
    for owner, row in data.items():
        print("OWNER", owner, row["class_sha256"], "PARENT", row["parent"])
        for m in row["selected_methods"]:
            print("METHOD", owner, m["name"], m["descriptor"], m["code_sha256"],
                  m["instruction_count"], "REFS", len(m["typed_members"]))
            if any(x in m["name"].lower() for x in ("caughtfire", "explode", "ignite", "prime", "tick", "fuse")):
                print("SEMANTIC", json.dumps(m, sort_keys=True, ensure_ascii=False))
    for owner, row in registries.items():
        print("REGISTRY", json.dumps(row, sort_keys=True, ensure_ascii=False))
    print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")


def self_test():
    for owner, expected in (
        (PREFIX + "block/NuclearBombBlock", True),
        (PREFIX + "entity/item/NuclearExplosionEntity", True),
        (PREFIX + "block/NuclearBombBlock$1", False),
        ("client/render/NuclearBombRenderer", False),
        (PREFIX + "item/RemoteDetonatorItem", False),
    ):
        require(interesting_class(owner) == expected, "candidate selection mismatch")
    print("PASS: five synthetic candidate cases")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
    else:
        require(args.jar is not None and args.output is not None, "jar and output required")
        inspect(args.jar, args.javap, args.output)
