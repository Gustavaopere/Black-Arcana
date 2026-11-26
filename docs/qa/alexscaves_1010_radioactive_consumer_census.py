#!/usr/bin/env python3
"""Read-only exact resource and JVM registry consumer census for four RadioactiveItem identities."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble

REG = "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
OWNER = "com/github/alexmodguy/alexscaves/server/item/RadioactiveItem"
FIELDS = {"CHARRED_REMNANT", "FISSILE_CORE", "URANIUM", "URANIUM_SHARD"}
IDS = {"alexscaves:" + field.lower() for field in FIELDS}
ROSTER = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
REG_SHA = "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"
OWNER_SHA = "6a46aa885ce5e5728c22691033b0a0f892d69f6c6fa7dd86a96c8f33c81d9436"
FACTORY_PINS = {
    "lambda$static$74": "a8f68e374288c6495c5ab854c9c17cd777cc30b4be5e4e71a31e41531873d736",
    "lambda$static$73": "97c2de487a982e04941e1183de8616b31f8ca5d1b29a6fd9a009ac03cbe85d20",
    "lambda$static$58": "1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f",
    "lambda$static$59": "1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f",
}

def walk(value, path=()):
    """Yield exact string tokens (including dictionary keys), never substrings."""
    if isinstance(value, dict):
        for key, child in sorted(value.items()):
            yield key, [*path, key], "key"
            yield from walk(child, (*path, key))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk(child, (*path, i))
    elif isinstance(value, str):
        yield value, list(path), "value"

def tag_id(path):
    match = re.fullmatch(r"data/([^/]+)/tags/item/(.+)\.json", path)
    return "#" + match[1] + ":" + match[2] if match else None

def resources(documents):
    """Separate direct ID mentions from potential transitive item-tag consumers."""
    tag_edges = {}
    for path, doc in documents.items():
        tid = tag_id(path)
        if tid and isinstance(doc, dict):
            values = doc.get("values", [])
            require(isinstance(values, list), "invalid tag values " + path)
            tag_edges[tid] = {entry if isinstance(entry, str) else entry.get("id")
                              for entry in values if isinstance(entry, (str, dict))}
    reachable = {item: {item} for item in IDS}
    changed = True
    while changed:
        changed = False
        for item, tokens in reachable.items():
            for tag, members in sorted(tag_edges.items()):
                if tag not in tokens and members & tokens:
                    tokens.add(tag)
                    changed = True
    hits = {}
    for path, doc in sorted(documents.items()):
        rows = []
        for token, location, kind in walk(doc):
            for item, tokens in sorted(reachable.items()):
                if token in tokens or (kind == "value" and location and location[-1] == "tag" and "#" + token in tokens):
                    rows.append({"id": item, "token": token, "path": location, "kind": kind,
                                 "relation": "DIRECT_ID" if token == item else "POTENTIAL_TAG_REFERENCE"})
        if rows:
            hits[path] = rows
    return hits, {item: sorted(tokens - {item}) for item, tokens in sorted(reachable.items())}

def inspect(jar, javap):
    verify_artifact(jar)
    result = {"scope": "STATIC_CONSUMER_CENSUS_ONLY", "mutation": "NO_MUTATION",
              "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
              "physical_qa": "NOT_TESTED", "provider_universe_closed": False,
              "field_consumers": {}, "resource_consumers": {}, "factory_pins": FACTORY_PINS}
    with ZipFile(jar) as z:
        names = z.namelist()
        roster = sorted(p for p in names if p.endswith(".class"))
        require(len(names) == len(set(names)) and len(roster) == 1555, "publisher roster")
        require(digest(("\n".join(roster) + "\n").encode()) == ROSTER, "class roster digest")
        found = set()
        for path in roster:
            raw = z.read(path)
            rd = ClassReader(raw)
            require(rd.name + ".class" == path, "class identity")
            if rd.name == OWNER:
                require(digest(raw) == OWNER_SHA, "RadioactiveItem class pin")
                found.add(OWNER)
            if rd.name == REG:
                require(digest(raw) == REG_SHA, "registry class pin")
                require({d["name"]: d.get("code_sha256") for d in rd.methods
                         if d["name"] in FACTORY_PINS} == FACTORY_PINS, "four factory pins")
                require(FIELDS <= {f["name"] for f in rd.fields}, "four registry fields")
                found.add(REG)
            refs = [x for x in rd.typed_refs(REG) if x["kind"] == "field_reference"
                    and x["name"] in FIELDS]
            if not refs:
                continue
            cp = {x["index"]: x for x in refs}
            methods = []
            for (name, desc), body in sorted(disassemble(jar, javap, rd.name).items()):
                offsets = sorted(body)
                sites = []
                for i, at in enumerate(offsets):
                    op, arg, _ = body[at]
                    m = re.match(r"#(\d+)(?:\s|,|$)", arg)
                    if not m or int(m[1]) not in cp:
                        continue
                    field = cp[int(m[1])]
                    require(op in {"getstatic", "putstatic", "getfield", "putfield"}, "unexpected field opcode")
                    sites.append({"offset": at, "opcode": op, "field": field["name"],
                                  "descriptor": field["descriptor"],
                                  "window": [{"offset": q, "opcode": body[q][0], "symbol": body[q][2]}
                                             for q in offsets[max(0, i-5):i+6]]})
                if sites:
                    declaration = next(d for d in rd.methods if d["name"] == name and d["descriptor"] == desc)
                    methods.append({"name": name, "descriptor": desc,
                                    "code_sha256": declaration["code_sha256"], "sites": sites})
            result["field_consumers"][rd.name] = {"class_sha256": digest(raw), "refs": refs, "methods": methods}
        require(found == {OWNER, REG}, "pinned owners present")
        require(REG in result["field_consumers"], "registry field sites")
        writes = {s["field"] for m in result["field_consumers"][REG]["methods"]
                  if m["name"] == "<clinit>" for s in m["sites"] if s["opcode"] == "putstatic"}
        require(writes == FIELDS, "four field bindings")
        require(len(result["field_consumers"]) <= 100, "field owner budget")
        require(sum(len(m["sites"]) for row in result["field_consumers"].values()
                    for m in row["methods"]) <= 1000, "field site budget")
        docs, fingerprints = {}, {}
        for path in sorted(p for p in names if p.endswith(".json") and p.startswith("data/")):
            raw = z.read(path)
            require(len(raw) <= 4_000_000, "resource size " + path)
            docs[path] = json.loads(raw)
            fingerprints[path] = {"sha256": digest(raw), "size": len(raw)}
        hits, tags = resources(docs)
        result["resource_consumers"] = {p: {**fingerprints[p], "hits": rows} for p, rows in hits.items()}
        result["potential_item_tags"] = tags
        result["data_json_scanned"] = len(docs)
        require(len(hits) <= 500, "resource hit budget")
    return result

def self_test():
    docs = {
        "data/test/tags/item/a.json": {"values": ["alexscaves:uranium", "alexscaves:uranium_extra"]},
        "data/test/tags/item/b.json": {"values": [{"id": "#test:a", "required": False}, "#test:b"]},
        "data/test/recipe/unrelated_name.json": {"ingredient": {"tag": "test:b"}, "marker": "#test:b"},
        "data/test/recipe/false.json": {"item": "alexscaves:uranium_extra"},
        "data/test/tags/block/a.json": {"values": ["alexscaves:uranium"]},
        "data/test/recipe/key.json": {"alexscaves:uranium_shard": True}
    }
    hits, tags = resources(docs)
    require(tags["alexscaves:uranium"] == ["#test:a", "#test:b"], "transitive and cyclic tag reachability")
    require(not tags["alexscaves:uranium_shard"], "separate identity")
    require("data/test/recipe/false.json" not in hits, "substring rejected")
    require(hits["data/test/recipe/key.json"][0]["kind"] == "key", "key location")
    require(tag_id("data/test/tags/block/a.json") is None, "block tag not item tag")
    require(hits["data/test/recipe/unrelated_name.json"][0]["relation"] == "POTENTIAL_TAG_REFERENCE", "tag distinction")
    print("PASS six resource and identity checks")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar and a.output and not a.output.exists(), "write once")
        report = inspect(a.jar, a.javap)
        raw = canonical(report).encode()
        require(len(raw) <= 8_000_000, "report budget")
        with a.output.open("xb") as f:
            f.write(raw)
        print("REPORT_SHA256", digest(raw), "BYTES", len(raw))
        print("DATA_JSON_SCANNED", report["data_json_scanned"])
        for owner, row in report["field_consumers"].items():
            for method in row["methods"]:
                for site in method["sites"]:
                    print("FIELD_SITE", json.dumps({"owner": owner, "name": method["name"],
                          "descriptor": method["descriptor"], "code_sha256": method["code_sha256"],
                          **site}, sort_keys=True))
        for path, row in report["resource_consumers"].items():
            print("RESOURCE", json.dumps({"path": path, **row}, sort_keys=True))
        print("POTENTIAL_TAGS", json.dumps(report["potential_item_tags"], sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
