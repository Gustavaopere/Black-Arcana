#!/usr/bin/env python3
"""Read-only, SHA-exact discovery of ACItemRegistry bindings, no registry execution."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, rows, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_food_builder_probe import refs_for

PREFIX = "com/github/alexmodguy/alexscaves/"
TARGET = PREFIX + "server/item/ACItemRegistry"
BRIDGE = PREFIX + "server/misc/ACDeferredRegister"
TARGET_SHA = "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"
SUPPLIER = "Ljava/util/function/Supplier;"
EXPECTED_FIELDS = {
    "Ljava/util/Map;": 1,
    "Lnet/minecraft/world/item/Rarity;": 4,
    "L" + PREFIX + "server/item/ACArmorMaterial;": 6,
    "L" + BRIDGE + ";": 1,
    SUPPLIER: 188,
}


def cp_index(operand):
    match = re.match(r"#(\d+)", operand)
    return int(match.group(1)) if match else None


def inspect_methods(jar, javap, z, owner):
    raw = z.read(owner + ".class")
    rd = ClassReader(raw)
    require(rd.name == owner and rd.major == 65, "class identity drift")
    parsed = disassemble(jar, javap, owner)
    coded = {(m["name"], m["descriptor"]) for m in rd.methods if "code_sha256" in m}
    require({key for key, body in parsed.items() if body} == coded,
            "declared/code coverage drift: " + owner)
    methods = [summarize(rd, key, body) for key, body in sorted(parsed.items()) if body]
    return rd, parsed, {"class_sha256": digest(raw), "parent": rd.parent,
                        "interfaces": rd.interfaces, "fields": rd.fields,
                        "declarations": rd.methods, "methods": methods,
                        "bootstrap_methods": rd.attributes.get("bootstrap_methods", [])}


def inspect(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        entries = z.namelist()
        require(len(entries) == len(set(entries)), "duplicate ZIP members")
        classes = sorted(p for p in entries if p.endswith(".class"))
        require(len(classes) == 1555, "class roster drift")
        rd, parsed, target = inspect_methods(jar, javap, z, TARGET)
        require(target["class_sha256"] == TARGET_SHA, "registry class hash drift")
        field_types = dict(Counter(f["descriptor"] for f in rd.fields))
        require(field_types == EXPECTED_FIELDS, "registry field roster drift")
        fields = {f["name"]: f for f in rd.fields}
        require(len(fields) == 200, "duplicate registry field names")
        refs = {x["index"]: x for x in refs_for(rd, {TARGET, BRIDGE})}
        bootstrap = target["bootstrap_methods"]
        # Preserve the actual initializer slices and bootstrap references. A slice
        # is a lexical write window, not proof of a single causal producer.
        bindings = {}
        segment = []
        for row in rows(parsed[("<clinit>", "()V")]):
            segment.append(row)
            ref = refs.get(cp_index(row["operand"]))
            if row["opcode"] != "putstatic" or not ref or ref["owner"] != TARGET:
                continue
            name = ref["name"]
            require(name in fields and ref["descriptor"] == fields[name]["descriptor"],
                    "unknown registry field write")
            dynamic = []
            bridge_calls = []
            for ins in segment:
                sym = ins["symbol"]
                mat = re.search(r"InvokeDynamic #(\d+):", sym)
                if ins["opcode"] == "invokedynamic":
                    require(mat is not None and int(mat[1]) < len(bootstrap),
                            "unresolved bootstrap index")
                    idx = int(mat[1])
                    dynamic.append({"offset": ins["offset"], "index": idx,
                                    "bootstrap": bootstrap[idx]})
                member = refs.get(cp_index(ins["operand"]))
                if member and member["owner"] == BRIDGE and ins["opcode"].startswith("invoke"):
                    bridge_calls.append({"offset": ins["offset"], "reference": member})
            bindings.setdefault(name, []).append({
                "write_offset": row["offset"], "window_sha256": digest(canonical(segment).encode()),
                "window": segment, "dynamic_sites": dynamic, "bridge_calls": bridge_calls})
            segment = []
        supplier_names = sorted(name for name, f in fields.items() if f["descriptor"] == SUPPLIER)
        missing = sorted(set(supplier_names) - bindings.keys())
        multiple = sorted(name for name in bindings if len(bindings[name]) != 1)
        # No assumptions about uniqueness or registry IDs: record unresolved or
        # multiple writes for review, including all remaining initializer rows.
        _, _, bridge = inspect_methods(jar, javap, z, BRIDGE)
        nested = {}
        for path in classes:
            if path.startswith(TARGET + "$") or path.startswith(BRIDGE + "$"):
                owner = path[:-6]
                _, _, nested[owner] = inspect_methods(jar, javap, z, owner)
        census = {}
        for path in classes:
            other = ClassReader(z.read(path))
            require(other.name + ".class" == path and other.major == 65, "class identity drift")
            typed = {owner: other.typed_refs(owner) for owner in (TARGET, BRIDGE)}
            typed = {owner: matches for owner, matches in typed.items() if matches}
            member_refs = refs_for(other, {TARGET, BRIDGE})
            if typed or member_refs:
                census[other.name] = {"typed": typed, "member_refs": member_refs}
        return {"class_entries_scanned": len(classes),
                "class_roster_sha256": digest(("\n".join(classes) + "\n").encode()),
                "target": target, "bridge": bridge, "nested_classes": nested,
                "field_types": field_types, "bindings": bindings,
                "supplier_fields": supplier_names, "supplier_fields_without_initializer_write": missing,
                "multiple_initializer_write_fields": multiple, "initializer_tail": segment,
                "typed_census": census}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and args.output.suffix == ".json", "new JSON required")
    native = inspect(args.jar, args.javap)
    report = {"schema": "AC_ITEM_REGISTRY_DISCOVERY_V1", "scope": "DISCOVERY_NOT_CERTIFIED",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "native": native, "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
              "physical_qa": "NOT_TESTED", "provider_universe_closed": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(args.output.read_bytes()))
    print("FIELDS", json.dumps(native["field_types"], sort_keys=True))
    print("CLASSES", native["class_entries_scanned"])
    print("SUPPLIERS", len(native["supplier_fields"]))
    print("MISSING_WRITES", json.dumps(native["supplier_fields_without_initializer_write"]))
    print("MULTIPLE_WRITES", json.dumps(native["multiple_initializer_write_fields"]))
    for owner, data in [(TARGET, native["target"]), (BRIDGE, native["bridge"]),
                        *sorted(native["nested_classes"].items())]:
        print("OWNER", owner, data["class_sha256"], len(data["declarations"]),
              len(data["methods"]), len(data["bootstrap_methods"]))
        for m in data["methods"]:
            print("METHOD", owner, m["declaration"]["name"], m["declaration"]["descriptor"],
                  m["instruction_count"], m["instruction_sha256"])
            if owner != TARGET or not m["declaration"]["name"].startswith("lambda$"):
                # Registry clinit windows are emitted separately below.
                if m["declaration"]["name"] != "<clinit>" or owner != TARGET:
                    print("BODY", json.dumps(m["instructions"], sort_keys=True))
    for name, windows in sorted(native["bindings"].items()):
        print("BINDING", name, json.dumps([{"write_offset": w["write_offset"],
              "dynamic_sites": w["dynamic_sites"], "bridge_calls": w["bridge_calls"],
              "literal_strings": [ins["symbol"] for ins in w["window"] if
                                  ins["symbol"].startswith("String ")]}
              for w in windows], sort_keys=True))
    print("CENSUS_OWNER_COUNT", len(native["typed_census"]))
    for owner, data in sorted(native["typed_census"].items()):
        print("CENSUS", owner, json.dumps(Counter(
            ref["owner"] for ref in data["member_refs"]), sort_keys=True))
    print("END_ITEM_REGISTRY_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
