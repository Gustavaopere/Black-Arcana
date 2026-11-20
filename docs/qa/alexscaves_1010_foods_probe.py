#!/usr/bin/env python3
"""SHA-exact ACFoods declaration and supplier/consumer discovery, read-only."""
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

PREFIX = "com/github/alexmodguy/alexscaves/server/item/"
TARGET = PREFIX + "ACFoods"
BUILDER = PREFIX + "ACFoodBuilder"
TARGET_SHA = "a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e"
FOOD_DESC = "Lnet/minecraft/world/food/FoodProperties;"
EFFECT_DESC = "()Lnet/minecraft/world/effect/MobEffectInstance;"
EXPECTED_CALLS = {"of": 63, "nutrition": 63, "saturationMod": 63, "meat": 5,
                  "build": 63, "fast": 6, "bowl": 6, "effect": 46,
                  "alwaysEat": 3, "sound": 3}


def cp_index(operand):
    match = re.match(r"#(\d+)", operand)
    return int(match.group(1)) if match else None


def literal(row):
    op, arg, symbol = row["opcode"], row["operand"], row["symbol"]
    if op == "iconst_m1":
        return -1
    if op.startswith("iconst_"):
        return int(op[-1])
    if op.startswith("fconst_"):
        return float(op[-1])
    if op in ("bipush", "sipush"):
        return int(arg)
    if op in ("ldc", "ldc_w"):
        match = re.fullmatch(r"(int|float) (-?[0-9.eE+\-]+)f?", symbol)
        if match:
            return int(match[2]) if match[1] == "int" else float(match[2])
    raise ValueError("unresolved numeric argument: " + str(row))


def inspect(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        roster = z.namelist()
        require(len(roster) == len(set(roster)), "duplicate ZIP members")
        paths = sorted(x for x in roster if x.endswith(".class"))
        require(len(paths) == 1555, "class roster drift")
        raw = z.read(TARGET + ".class")
        require(digest(raw) == TARGET_SHA, "ACFoods class drift")
        target = ClassReader(raw)
        fields = {f["name"]: f for f in target.fields}
        require(len(fields) == 63 and all(f["descriptor"] == FOOD_DESC and
                f["access"] == 25 for f in fields.values()), "food field roster drift")
        parsed = disassemble(jar, javap, TARGET)
        coded = {(m["name"], m["descriptor"]) for m in target.methods if "code_sha256" in m}
        require(set(k for k, body in parsed.items() if body) == coded, "method coverage drift")
        init = parsed[("<clinit>", "()V")]
        require(len(init) == 606, "initializer instruction count drift")
        refs = {x["index"]: x for x in refs_for(target, {TARGET, BUILDER})}
        bootstrap = target.attributes.get("bootstrap_methods", [])
        require(len(bootstrap) == 46, "bootstrap count drift")
        configs, segment, calls, suppliers = {}, [], Counter(), set()
        for row in rows(init):
            op, operand = row["opcode"], row["operand"]
            i = cp_index(operand)
            ref = refs.get(i)
            if op == "return":
                require(not segment, "unassigned initializer instructions")
                continue
            segment.append(row)
            if op != "putstatic" or not ref or ref["owner"] != TARGET:
                continue
            field = ref["name"]
            require(field in fields and field not in configs, "unknown/duplicate field write")
            conf = {"field": field, "write_offset": row["offset"], "builder_calls": [],
                    "effects": [], "segment_sha256": digest(canonical(segment).encode())}
            for n, item in enumerate(segment):
                member = refs.get(cp_index(item["operand"]))
                if not member or member["owner"] != BUILDER or not item["opcode"].startswith("invoke"):
                    continue
                name = member["name"]
                calls[name] += 1
                entry = {"name": name, "descriptor": member["descriptor"], "offset": item["offset"]}
                if name in {"nutrition", "saturationMod"}:
                    entry["value"] = literal(segment[n - 1])
                if name == "sound":
                    entry["argument"] = segment[n - 1]["symbol"]
                if name == "effect":
                    probability = literal(segment[n - 1])
                    producer = segment[n - 2]
                    require(producer["opcode"] == "invokedynamic", "supplier shape drift")
                    match = re.search(r"InvokeDynamic #(\d+):", producer["symbol"])
                    require(match is not None and int(match[1]) < len(bootstrap), "supplier bootstrap drift")
                    bs = bootstrap[int(match[1])]
                    handles = [x["reference"] for x in bs["arguments"]
                               if isinstance(x, dict) and "reference" in x]
                    require(len(handles) == 1, "supplier handle count drift")
                    handle = handles[0]
                    require(handle[1] == TARGET and handle[2][2] == EFFECT_DESC,
                            "supplier implementation identity drift")
                    key = (handle[2][1], handle[2][2])
                    require(key in coded and key not in suppliers, "unresolved/reused supplier")
                    suppliers.add(key)
                    conf["effects"].append({"offset": item["offset"], "probability": probability,
                                            "supplier": key[0], "bootstrap_index": int(match[1])})
                conf["builder_calls"].append(entry)
            names = [x["name"] for x in conf["builder_calls"]]
            require(names[0] == "of" and names[-1] == "build" and
                    all(names.count(x) == 1 for x in ("of", "nutrition", "saturationMod", "build")),
                    "builder sequence drift " + field)
            configs[field] = conf
            segment = []
        require(set(configs) == set(fields) and dict(calls) == EXPECTED_CALLS,
                "initializer field/call coverage drift")
        require(len(suppliers) == 46 and coded == suppliers | {("<init>", "()V"), ("<clinit>", "()V")},
                "supplier/method inventory drift")
        supplier_methods = {key[0]: summarize(target, key, parsed[key]) for key in sorted(suppliers)}
        census, consumers = {}, {}
        for path in paths:
            rd = ClassReader(z.read(path))
            require(rd.name + ".class" == path and rd.major == 65, "class identity drift")
            typed = rd.typed_refs(TARGET)
            refs = refs_for(rd, {TARGET})
            if typed or refs:
                census[rd.name] = {"typed": typed, "references": refs}
            if rd.name == TARGET or not refs:
                continue
            reference_map = {x["index"]: x for x in refs}
            methods = disassemble(jar, javap, rd.name)
            selected = []
            for key, body in sorted(methods.items()):
                seq = rows(body)
                sites = []
                for n, row in enumerate(seq):
                    ref = reference_map.get(cp_index(row["operand"]))
                    if ref and row["opcode"] in ("getstatic", "putstatic", "getfield", "putfield"):
                        sites.append({"offset": row["offset"], "opcode": row["opcode"],
                                      "field": ref["name"], "descriptor": ref["descriptor"],
                                      "context": seq[max(0, n - 3):n + 5]})
                if sites:
                    require(all(x["field"] in fields for x in sites), "unknown consumer field")
                    selected.append({"method": key[0], "descriptor": key[1],
                                     "instruction_count": len(body),
                                     "instruction_sha256": digest(canonical(seq).encode()),
                                     "sites": sites})
            consumers[rd.name] = {"class_sha256": digest(z.read(path)),
                                  "methods": selected,
                                  "bootstraps": rd.attributes.get("bootstrap_methods", [])}
        return {"class_entries_scanned": len(paths), "target_class_sha256": TARGET_SHA,
                "class_roster_sha256": digest(("\n".join(paths) + "\n").encode()),
                "fields": fields, "builder_call_counts": dict(calls),
                "configurations": configs, "supplier_methods": supplier_methods,
                "initializer": summarize(target, ("<clinit>", "()V"), init),
                "constructor": summarize(target, ("<init>", "()V"), parsed[("<init>", "()V")]),
                "typed_census": census, "consumers": consumers}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    a = parser.parse_args()
    require(not a.output.exists() and a.output.suffix == ".json", "new JSON required")
    native = inspect(a.jar, a.javap)
    report = {"schema": "AC_FOODS_DISCOVERY_V1", "scope": "DISCOVERY_NOT_CERTIFIED",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "native": native, "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
              "physical_qa": "NOT_TESTED", "provider_universe_closed": False}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(a.output.read_bytes()))
    print("COUNTS", json.dumps(native["builder_call_counts"], sort_keys=True))
    for field, data in sorted(native["configurations"].items()):
        print("FOOD", json.dumps(data, sort_keys=True))
    for name, data in sorted(native["supplier_methods"].items()):
        print("SUPPLIER", name, json.dumps(data, sort_keys=True))
    for name, data in sorted(native["consumers"].items()):
        print("CONSUMER", name, json.dumps(data["methods"], sort_keys=True))
    print("TYPED_OWNERS", json.dumps(sorted(native["typed_census"])))
    print("END_AC_FOODS_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
