#!/usr/bin/env python3
"""Read-only exact ACFoodPropertiesItem interface and native consumer discovery.

This is discovery evidence, not a certificate or a runtime integration.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

TARGET = "com/github/alexmodguy/alexscaves/server/item/ACFoodPropertiesItem"
TARGET_SHA = "78b5fe9d3b47072e4b1708fbd11129d2669c95a1b913f3bf2ba8946364cb5d3d"


def inherits(owner, hierarchy, chain=()):
    if owner == TARGET:
        return True
    require(owner not in chain, "hierarchy cycle")
    node = hierarchy.get(owner)
    return bool(node and any(inherits(p, hierarchy, (*chain, owner))
                            for p in (node["parent"], *node["interfaces"]) if p))


def inspect(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths = z.namelist()
        require(len(paths) == len(set(paths)), "duplicate ZIP members")
        classes = sorted(p for p in paths if p.endswith(".class"))
        require(len(classes) == 1555, "class roster drift")
        raw = z.read(TARGET + ".class")
        require(digest(raw) == TARGET_SHA, "interface hash drift")
        target = ClassReader(raw)
        require(target.access & 0x0200, "target is not an interface")
        signatures = {(m["name"], m["descriptor"]) for m in target.methods}
        require(len(signatures) <= 16, "unexpected interface surface")
        names = {n for n, _ in signatures}
        hierarchy, typed, refs, declarations = {}, {}, {}, {}
        for path in classes:
            rd = ClassReader(z.read(path))
            require(rd.name + ".class" == path and rd.major == 65, "class identity drift")
            hierarchy[rd.name] = {"parent": rd.parent, "interfaces": rd.interfaces,
                                  "access": rd.access}
            found = rd.typed_refs(TARGET)
            if found:
                typed[rd.name] = found
            declared = [m for m in rd.methods if m["name"] in names]
            if declared:
                declarations[rd.name] = declared
            found = []
            for i, e in enumerate(rd.pool):
                if e is None or e[0] not in (9, 10, 11):
                    continue
                tag, owner, sig = rd.resolve(i)
                if owner == TARGET or (sig[1], sig[2]) in signatures:
                    found.append({"index": i, "tag": tag, "owner": owner,
                                  "name": sig[1], "descriptor": sig[2]})
            if found:
                refs[rd.name] = found
        direct = sorted(o for o, v in hierarchy.items()
                        if o != TARGET and TARGET in v["interfaces"])
        inherited = sorted(o for o in hierarchy if o != TARGET and o not in direct
                           and inherits(o, hierarchy))
        # Capture in-JAR superclass methods of implementers too; a declaration
        # may be serviced by an inherited body rather than a direct override.
        ancestors = set()
        for owner in direct + inherited:
            parent = hierarchy[owner]["parent"]
            while parent in hierarchy and parent not in ancestors:
                ancestors.add(parent)
                parent = hierarchy[parent]["parent"]
        native_owners = {TARGET, *direct, *inherited, *ancestors}
        candidates = sorted(native_owners | set(typed) | set(refs) | set(declarations))
        require(len(candidates) <= 100, "consumer discovery budget exceeded")
        results = {}
        for owner in candidates:
            raw = z.read(owner + ".class")
            rd = ClassReader(raw)
            parsed = disassemble(jar, javap, owner) if any(
                "code_sha256" in m for m in rd.methods) else {}
            by_index = {r["index"]: r for r in refs.get(owner, [])}
            typed_indices = {r["index"] for r in typed.get(owner, []) if "index" in r}
            selected = []
            for key, body in sorted(parsed.items()):
                if not body:
                    continue
                sites = []
                for off, (op, operand, symbol) in sorted(body.items()):
                    match = re.match(r"#(\d+)", operand)
                    if match:
                        i = int(match.group(1))
                        if i in by_index or i in typed_indices:
                            sites.append({"offset": off, "opcode": op, "symbol": symbol,
                                          "reference": by_index.get(i)})
                if owner in native_owners or key[0] in names or sites:
                    require(len(body) <= 2000, "method discovery budget exceeded")
                    item = summarize(rd, key, body)
                    item["typed_sites"] = sites
                    selected.append(item)
            if owner in native_owners:
                for m in rd.methods:
                    if "code_sha256" in m:
                        require(any(x["declaration"]["name"] == m["name"] and
                                    x["declaration"]["descriptor"] == m["descriptor"]
                                    for x in selected), "missing coded native method " + owner)
            results[owner] = {"class_sha256": digest(raw), "hierarchy": hierarchy[owner],
                              "fields": rd.fields, "declarations": rd.methods,
                              "methods": selected,
                              "bootstrap_methods": rd.attributes.get("bootstrap_methods", [])}
        return {"class_entries_scanned": len(classes),
                "class_roster_sha256": digest(("\n".join(classes) + "\n").encode()),
                "target": TARGET, "target_class_sha256": TARGET_SHA,
                "target_access": target.access, "target_fields": target.fields,
                "target_methods": target.methods, "direct_implementers": direct,
                "inherited_implementers": inherited, "in_jar_ancestors": sorted(ancestors),
                "typed_census": typed, "exact_member_refs": refs, "owners": results}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    require(not a.output.exists() and a.output.suffix == ".json", "new JSON required")
    native = inspect(a.jar, a.javap)
    report = {"schema": "AC_FOOD_PROPERTIES_ITEM_DISCOVERY_V1",
              "scope": "DISCOVERY_NOT_CERTIFIED",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "native": native, "mutation": "NO_MUTATION",
              "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
              "provider_universe_closed": False}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(a.output.read_bytes()))
    for key in ("target_access", "target_fields", "target_methods", "direct_implementers",
                "inherited_implementers", "in_jar_ancestors", "typed_census", "exact_member_refs"):
        print(key.upper(), json.dumps(native[key], sort_keys=True))
    for owner, data in native["owners"].items():
        print("OWNER", owner, data["class_sha256"], json.dumps(data["hierarchy"]))
        print("FIELDS", json.dumps(data["fields"]))
        print("DECLARATIONS", json.dumps(data["declarations"]))
        for m in data["methods"]:
            print("METHOD", m["declaration"]["name"], m["declaration"]["descriptor"],
                  m["instruction_count"], m["instruction_sha256"])
            for row in m["instructions"]:
                print(" ", row["offset"], row["opcode"], row["operand"], row["symbol"])
        print("BOOTSTRAPS", json.dumps(data["bootstrap_methods"]))
    print("END_FOOD_PROPERTIES_ITEM_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
