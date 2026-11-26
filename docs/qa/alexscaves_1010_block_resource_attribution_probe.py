#!/usr/bin/env python3
"""Read-only exact block supplier/consumer and resource attribution audit."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, AuditError, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap
from alexscaves_1010_radioactive_consumer_census import walk

ROOT = "com/github/alexmodguy/alexscaves/"
REG = ROOT + "server/block/ACBlockRegistry"
BASE = ROOT + "citadel/item/BlockItemWithSupplier"
REG_SHA = "b4de04f32f6e1d92eeda55480b8480f7ed69f3813164f330f49d0eced202e54c"
CLINIT_SHA = "d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a"
ROSTER = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
BINDINGS = {
    "radrock_uranium_ore": (2059, 2062, 2067, 2068, 2071, 4),
    "waste_drum": (2192, 2195, 2200, 2201, 2204, 5),
    "block_of_uranium": (2292, 2295, 2300, 2301, 2304, 4),
    "unrefined_waste": (2321, 2324, 2329, 2330, 2333, 4),
}
BLOCK_IDS = {"alexscaves:" + n for n in BINDINGS}
FOOD_IDS = {"alexscaves:" + n for n in (
    "green_soylent", "slam", "spelunkie", "jelly_bean",
    "radiant_essence", "licowitch_radiant_essence")}
ALL_IDS = BLOCK_IDS | FOOD_IDS


def resource_attribution(docs):
    graphs = {"item": {}, "block": {}}
    for path, doc in sorted(docs.items()):
        match = re.fullmatch(r"data/([^/]+)/tags/(item|block)/(.+)\.json", path)
        if not match:
            continue
        require(isinstance(doc, dict) and isinstance(doc.get("values"), list), "tag shape " + path)
        tag = "#" + match[1] + ":" + match[3]
        members = []
        for entry in doc["values"]:
            token = entry if isinstance(entry, str) else entry.get("id") if isinstance(entry, dict) else None
            require(isinstance(token, str), "tag token " + path)
            members.append(token)
        graphs[match[2]][tag] = set(members)
    reachable = {}
    for registry, graph in graphs.items():
        for identity in sorted(ALL_IDS if registry == "item" else BLOCK_IDS):
            tokens = {identity}
            while True:
                more = {tag for tag, members in graph.items() if members & tokens}
                if more <= tokens:
                    break
                tokens |= more
            reachable[(registry, identity)] = tokens - {identity}
    hits = {}
    for path, doc in sorted(docs.items()):
        rows = []
        for token, location, kind in walk(doc):
            if token in ALL_IDS:
                rows.append({"id": token, "path": location, "token": token, "kind": kind,
                             "relation": "DIRECT_ID_REGISTRY_CONTEXT_REQUIRED"})
            normalized = "#" + token if kind == "value" and location and location[-1] == "tag" and not token.startswith("#") else token
            for (registry, identity), tags in sorted(reachable.items()):
                if normalized in tags:
                    rows.append({"id": identity, "path": location, "token": token, "kind": kind,
                                 "relation": "POTENTIAL_" + registry.upper() + "_TAG_REFERENCE"})
        if rows:
            hits[path] = rows
    return hits, {registry + ":" + identity: sorted(tags) for (registry, identity), tags in sorted(reachable.items())}


def project(rd, key, body):
    decl = next(d for d in rd.methods if (d["name"], d["descriptor"]) == key)
    if "code_sha256" not in decl:
        require(not body, "abstract with instructions")
        return {"name": key[0], "descriptor": key[1], "executable": False}
    require(bool(body), "missing executable body")
    return {**projection(rd, key, body, decl), "executable": True}


def inspect(jar, javap):
    verify_artifact(jar)
    report = {"scope": "BLOCK_AND_RESOURCE_STATIC_DISCOVERY_ONLY", "mutation": "NO_MUTATION",
              "static_contract": "NOT_CERTIFIED", "physical_qa": "NOT_TESTED",
              "provider_universe_closed": False, "bindings": {}, "native_owners": {}, "field_consumers": {}}
    with ZipFile(jar) as z:
        names = z.namelist()
        paths = set(names)
        roster = sorted(p for p in names if p.endswith(".class"))
        require(len(names) == len(paths) and len(roster) == 1555, "roster")
        require(digest(("\n".join(roster) + "\n").encode()) == ROSTER, "roster digest")
        raw = z.read(REG + ".class")
        rd = ClassReader(raw)
        require(rd.name == REG and digest(raw) == REG_SHA, "registry pin")
        body = disassemble(jar, javap, REG)
        key = ("<clinit>", "()V")
        require(next(d["code_sha256"] for d in rd.methods if (d["name"], d["descriptor"]) == key) == CLINIT_SHA, "initializer pin")
        init = body[key]
        native = {BASE}
        for name, (literal, indy, selector, call, write, number) in sorted(BINDINGS.items()):
            require(init[literal][2] == "String " + name, "literal " + name)
            require(init[selector][0] == "iconst_" + str(number), "selector " + name)
            require(init[call][0] == "invokestatic" and "registerBlockAndItem:" in init[call][2], "register call " + name)
            require(init[write][0] == "putstatic" and ("Field " + name.upper() + ":") in init[write][2], "field write " + name)
            links = bootstrap(rd, {indy: init[indy]})
            require(len(links) == 1 and len(links[0]["handles"]) == 1, "supplier handle " + name)
            handle = links[0]["handles"][0]
            record = {"offsets": [literal, indy, selector, call, write], "selector": number, "handle": handle}
            if handle["owner"] == REG:
                supplier = (handle["name"], handle["descriptor"])
                require(supplier in body, "supplier body " + name)
                row = project(rd, supplier, body[supplier])
                record["factory"] = row
                targets = {x["target"] for x in row["new_sites"]}
            else:
                require(handle["kind"] == 8 and handle["name"] == "<init>", "unresolved non-registry factory " + name)
                targets = {handle["owner"]}
            record["new_targets"] = sorted(targets)
            native |= {target for target in targets if target.startswith(ROOT) and target + ".class" in paths}
            report["bindings"][name] = record
        props = [k for k in body if k[0] == "blockItemProperties"]
        require(len(props) == 1, "block item properties")
        report["block_item_properties"] = project(rd, props[0], body[props[0]])
        pending = sorted(native)
        while pending:
            owner = pending.pop(0)
            if owner in report["native_owners"]:
                continue
            require(len(report["native_owners"]) < 24, "native hierarchy budget")
            data = z.read(owner + ".class")
            reader = ClassReader(data)
            require(reader.name == owner, "native owner identity")
            parsed = disassemble(jar, javap, owner)
            rows, deferred = [], []
            for k, b in sorted(parsed.items()):
                try:
                    rows.append(project(reader, k, b))
                except AuditError as err:
                    decl = next(d for d in reader.methods if (d["name"], d["descriptor"]) == k)
                    deferred.append({"name": k[0], "descriptor": k[1], "code_sha256": decl.get("code_sha256"),
                                     "reason": str(err), "instruction_count": len(b)})
            report["native_owners"][owner] = {"class_sha256": digest(data), "parent": reader.parent,
                "interfaces": reader.interfaces, "fields": reader.fields, "declarations": reader.methods,
                "methods": rows, "deferred": deferred}
            if reader.parent and reader.parent.startswith(ROOT) and reader.parent + ".class" in paths:
                pending.append(reader.parent)
        fields = {name.upper() for name in BINDINGS}
        for path in roster:
            data = z.read(path)
            reader = ClassReader(data)
            require(reader.name + ".class" == path, "class identity")
            refs = [x for x in reader.typed_refs(REG) if x["kind"] == "field_reference" and x["name"] in fields]
            if not refs:
                continue
            cp = {x["index"]: x for x in refs}
            sites = []
            parsed = body if reader.name == REG else disassemble(jar, javap, reader.name)
            for k, b in sorted(parsed.items()):
                offsets = sorted(b)
                for i, at in enumerate(offsets):
                    op, arg, sym = b[at]
                    match = re.match(r"#(\d+)(?:\s|,|$)", arg)
                    if not match or int(match[1]) not in cp:
                        continue
                    decl = next(d for d in reader.methods if (d["name"], d["descriptor"]) == k)
                    sites.append({"name": k[0], "descriptor": k[1], "code_sha256": decl["code_sha256"],
                                  "offset": at, "opcode": op, "field": cp[int(match[1])]["name"],
                                  "window": [{"offset": q, "opcode": b[q][0], "symbol": b[q][2]}
                                             for q in offsets[max(0, i-5):i+6]]})
            report["field_consumers"][reader.name] = {"class_sha256": digest(data), "refs": refs, "sites": sites}
        require(REG in report["field_consumers"] and len(report["field_consumers"]) <= 100, "consumer owner budget")
        writes = {x["field"] for x in report["field_consumers"][REG]["sites"]
                  if x["name"] == "<clinit>" and x["opcode"] == "putstatic"}
        require(writes == fields, "block field roster")
        docs, pins = {}, {}
        for path in sorted(p for p in names if p.startswith("data/") and p.endswith(".json")):
            data = z.read(path)
            require(len(data) <= 4000000, "resource size " + path)
            docs[path] = json.loads(data)
            pins[path] = {"sha256": digest(data), "size": len(data)}
        require(len(docs) == 1563, "resource roster")
        hits, tags = resource_attribution(docs)
        require(len(hits) <= 500, "resource hit budget")
        report["data_json_scanned"] = len(docs)
        report["resources"] = {path: {**pins[path], "hits": rows} for path, rows in hits.items()}
        report["potential_tags"] = tags
    return report


def self_test():
    docs = {
        "data/test/tags/item/a.json": {"values": ["alexscaves:block_of_uranium"]},
        "data/test/tags/item/b.json": {"values": [{"id": "#test:a", "required": False}, "#test:b"]},
        "data/test/tags/block/a.json": {"values": ["alexscaves:radrock_uranium_ore"]},
        "data/test/recipe/x.json": {"ingredient": {"tag": "test:b"}, "other": "alexscaves:slam"},
        "data/test/recipe/y.json": {"item": "alexscaves:slam_extra"},
    }
    hits, tags = resource_attribution(docs)
    require(tags["item:alexscaves:block_of_uranium"] == ["#test:a", "#test:b"], "cyclic tag closure")
    require(tags["block:alexscaves:block_of_uranium"] == [], "registry separation")
    require(tags["block:alexscaves:radrock_uranium_ore"] == ["#test:a"], "block tag closure")
    require("data/test/recipe/y.json" not in hits, "exact ID")
    require({x["relation"] for x in hits["data/test/recipe/x.json"]} ==
            {"DIRECT_ID_REGISTRY_CONTEXT_REQUIRED", "POTENTIAL_ITEM_TAG_REFERENCE"}, "relation separation")
    require(len(BINDINGS) == 4 and len(ALL_IDS) == 10, "scope")
    print("PASS six exact scope and resource checks")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", type=Path)
    ap.add_argument("--javap", default="javap")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar and a.output and not a.output.exists(), "write once")
        report = inspect(a.jar, a.javap)
        raw = canonical(report).encode()
        require(len(raw) <= 15000000, "report byte budget")
        with a.output.open("xb") as f:
            f.write(raw)
        print("REPORT_SHA256", digest(raw), "BYTES", len(raw), "DATA_JSON", report["data_json_scanned"])
        for name, row in report["bindings"].items():
            print("BINDING", json.dumps({"id": name, **row}, sort_keys=True))
        print("BLOCK_ITEM_PROPERTIES", json.dumps(report["block_item_properties"], sort_keys=True))
        for owner, row in report["native_owners"].items():
            print("OWNER", owner, row["class_sha256"], "PARENT", row["parent"],
                  "METHODS", len(row["methods"]), "DEFERRED", len(row["deferred"]))
            for method in row["methods"]:
                print("SEMANTIC", json.dumps({"owner": owner, **method}, sort_keys=True))
            for method in row["deferred"]:
                print("DEFERRED", json.dumps({"owner": owner, **method}, sort_keys=True))
        for owner, row in report["field_consumers"].items():
            for site in row["sites"]:
                print("FIELD_SITE", json.dumps({"owner": owner, **site}, sort_keys=True))
        for path, row in report["resources"].items():
            print("RESOURCE_ID", json.dumps({"path": path, **row}, sort_keys=True))
        print("END_BLOCK_AND_RESOURCE_DISCOVERY NO_MUTATION")
