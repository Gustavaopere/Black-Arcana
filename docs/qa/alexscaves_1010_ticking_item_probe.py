#!/usr/bin/env python3
"""SHA-exact discovery of ACTickingItem and native dispatch candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

TARGET = "com/github/alexmodguy/alexscaves/server/item/ACTickingItem"


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
        target = ClassReader(raw)
        require(target.access & 0x0200, "target is not interface")
        signatures = {(m["name"], m["descriptor"]) for m in target.methods}
        require(len(signatures) <= 16, "unexpected interface surface")
        hierarchy, typed, refs, declarations = {}, {}, {}, {}
        for path in classes:
            rd = ClassReader(z.read(path))
            require(rd.name + ".class" == path and rd.major == 65, "class identity drift")
            hierarchy[rd.name] = {"parent": rd.parent, "interfaces": rd.interfaces, "access": rd.access}
            found = rd.typed_refs(TARGET)
            if found:
                typed[rd.name] = found
            declared = [m for m in rd.methods if (m["name"], m["descriptor"]) in signatures]
            if declared:
                declarations[rd.name] = declared
            found = []
            for i, entry in enumerate(rd.pool):
                if entry is None or entry[0] not in (9, 10, 11):
                    continue
                tag, owner, sig = rd.resolve(i)
                if owner == TARGET or (sig[1], sig[2]) in signatures:
                    found.append({"index": i, "tag": tag, "owner": owner,
                                  "name": sig[1], "descriptor": sig[2]})
            if found:
                refs[rd.name] = found
        direct = sorted(o for o, v in hierarchy.items() if o != TARGET and TARGET in v["interfaces"])
        inherited = sorted(o for o in hierarchy if o != TARGET and o not in direct and inherits(o, hierarchy))
        ancestors = set()
        for owner in direct + inherited:
            parent = hierarchy[owner]["parent"]
            while parent in hierarchy and parent not in ancestors:
                ancestors.add(parent)
                parent = hierarchy[parent]["parent"]
        candidates = sorted({TARGET, *direct, *inherited, *ancestors, *typed, *refs, *declarations})
        require(len(candidates) <= 150, "consumer discovery budget exceeded")
        results = {}
        for owner in candidates:
            raw = z.read(owner + ".class")
            rd = ClassReader(raw)
            parsed = disassemble(jar, javap, owner) if any("code_sha256" in m for m in rd.methods) else {}
            by_index = {r["index"]: r for r in refs.get(owner, [])}
            typed_indices = {r["index"] for r in typed.get(owner, []) if "index" in r}
            selected = []
            for key, body in sorted(parsed.items()):
                if not body:
                    continue
                sites = []
                for off, (op, operand, symbol) in sorted(body.items()):
                    if operand.startswith("#"):
                        prefix = operand.split(",", 1)[0].split(" ", 1)[0][1:]
                        if prefix.isdigit() and (int(prefix) in by_index or int(prefix) in typed_indices):
                            sites.append({"offset": off, "opcode": op, "symbol": symbol,
                                          "reference": by_index.get(int(prefix))})
                if key in signatures or sites or (owner == TARGET):
                    require(len(body) <= 3000, "body exceeds discovery budget")
                    item = summarize(rd, key, body)
                    item["typed_sites"] = sites
                    selected.append(item)
            results[owner] = {"class_sha256": digest(raw), "hierarchy": hierarchy[owner],
                              "fields": rd.fields, "declarations": rd.methods,
                              "methods": selected, "bootstrap_methods": rd.attributes.get("bootstrap_methods", [])}
        resource = "alexscaves.mixins.json"
        mixin_raw = z.read(resource)
        mixin_config = json.loads(mixin_raw)
        mixin_summary = {"path": resource, "sha256": digest(mixin_raw),
                         "package": mixin_config.get("package"),
                         "mixin_entries": {k: [v for v in mixin_config.get(k, []) if "ItemStackTickMixin" in v]
                                           for k in ("mixins", "client", "server")}}
        require(any(mixin_summary["mixin_entries"].values()), "expected ItemStackTickMixin declaration absent")
        return {"mixin_summary": mixin_summary, "class_entries_scanned": len(classes),
                "class_roster_sha256": digest(("\n".join(classes) + "\n").encode()),
                "target": TARGET, "target_class_sha256": digest(z.read(TARGET + ".class")),
                "target_access": target.access, "target_fields": target.fields, "target_methods": target.methods,
                "direct_implementers": direct, "inherited_implementers": inherited,
                "in_jar_ancestors": sorted(ancestors), "typed_census": typed,
                "exact_member_refs": refs, "owners": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    a = parser.parse_args()
    require(not a.output.exists() and a.output.suffix == ".json", "new JSON required")
    native = inspect(a.jar, a.javap)
    report = {"schema": "AC_TICKING_ITEM_DISCOVERY_V1", "scope": "DISCOVERY_NOT_CERTIFIED",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "native": native, "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
              "physical_qa": "NOT_TESTED", "provider_universe_closed": False}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(a.output.read_bytes()))
    print("MIXIN_SUMMARY", json.dumps(native["mixin_summary"], sort_keys=True))
    for key in ("target_class_sha256", "target_access", "target_fields", "target_methods",
                "direct_implementers", "inherited_implementers", "in_jar_ancestors",
                "typed_census", "exact_member_refs"):
        print(key.upper(), json.dumps(native[key], sort_keys=True))
    for owner, data in native["owners"].items():
        print("OWNER", owner, data["class_sha256"], json.dumps(data["hierarchy"]))
        for m in data["methods"]:
            print("METHOD", m["declaration"]["name"], m["declaration"]["descriptor"],
                  m["instruction_count"], m["instruction_sha256"])
            for row in m["instructions"]:
                print(" ", row["offset"], row["opcode"], row["operand"], row["symbol"])
    print("END_TICKING_ITEM_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
