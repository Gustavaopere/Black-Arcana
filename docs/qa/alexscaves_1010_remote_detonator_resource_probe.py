#!/usr/bin/env python3
"""Read-only semantic projection of five SHA-pinned publisher resources.

No tag expansion, datapack merge, registry bootstrap, world mutation or QA.
The projection deliberately retains only interoperability identifiers and flags.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile

PREFIX = "data/alexscaves/"
TAG = PREFIX + "tags/block/remote_detonator_activates.json"
RECIPE = PREFIX + "recipe/remote_detonator.json"
ADV = PREFIX + "advancement/alexscaves/remote_detonation.json"
MODEL = "assets/alexscaves/models/item/remote_detonator.json"
ACTIVE = "assets/alexscaves/models/item/remote_detonator_active.json"
PINS = {
    TAG: (92, "766354b4a4a5cddd65f046119b7846e19ed8bd542ee9ce535033676cf8a71057"),
    RECIPE: (424, "d0d8b3f95160749b813b7e4818941f39aeb90d63188a591a595ce5fb9cb8cf82"),
    ADV: (492, "34b6e52f88977310e5f4cb77e0e233e8546551bb64eed1f188a8b1164293d3a5"),
    MODEL: (253, "e2633935ced3d79fb4d2d1be9265c9f31d8f315ed54bf028ee638f8fc9a2dc2b"),
    ACTIVE: (119, "e1ec3e273a11705bfcb5cb3cab48236be2fea18ecd55e9f0cf85e1c3a3e94ec3"),
}
JAR_SHA = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
JAR_SIZE = 75279314
LIMITS = {
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
    "effective_tag": "NOT_VERIFIED", "registry_bootstrap": "NOT_VERIFIED",
    "world_safety": "BLOCKED", "ticket_lifetime": "NOT_VERIFIED",
    "provider_universe_closed": False, "semantic_magic_roots_delta": 0,
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def decode(raw):
    result = json.loads(raw, object_pairs_hook=unique)
    need(isinstance(result, dict), "resource must be an object")
    return result


def tag_projection(value):
    need(set(value) <= {"replace", "values"} and "values" in value, "tag shape")
    replace = value.get("replace", False)
    need(type(replace) is bool and isinstance(value["values"], list), "tag types")
    need(len(value["values"]) <= 64, "tag bound")
    rows = []
    for entry in value["values"]:
        if isinstance(entry, str):
            identifier, required = entry, True
        else:
            need(isinstance(entry, dict) and "id" in entry
                 and set(entry) <= {"id", "required"}, "tag entry shape")
            identifier, required = entry["id"], entry.get("required", True)
        need(isinstance(identifier, str) and
             re.fullmatch(r"#?[a-z0-9_.-]+:[a-z0-9_./-]+", identifier) is not None
             and type(required) is bool, "tag entry types")
        rows.append({"id": identifier, "required": required,
                     "kind": "TAG_REFERENCE" if identifier.startswith("#") else "BLOCK_ID"})
    return {"replace": replace, "declared_entries": rows,
            "effective_membership": "NOT_VERIFIED"}


def project(resources):
    tag = tag_projection(resources[TAG])
    recipe = resources[RECIPE]
    result = recipe["result"]
    need(isinstance(result, dict), "recipe result shape")
    criteria = resources[ADV]["criteria"]
    need(isinstance(criteria, dict) and all(isinstance(v, dict) for v in criteria.values()),
         "criteria shape")
    return {"tag": tag,
            "recipe": {"type": recipe["type"], "result": result},
            "advancement": {"criterion_triggers": {k: v["trigger"] for k, v in criteria.items()}},
            "models": {p: {"parent": resources[p].get("parent"),
                            "override_predicates": [v["predicate"]
                              for v in resources[p].get("overrides", [])]}
                       for p in (MODEL, ACTIVE)}}


def inspect(jar, output):
    need(jar.stat().st_size == JAR_SIZE, "publisher size drift")
    with jar.open("rb") as stream:
        need(hashlib.file_digest(stream, "sha256").hexdigest() == JAR_SHA, "publisher hash drift")
    resources = {}
    with ZipFile(jar) as archive:
        for path, (size, expected) in PINS.items():
            need(archive.namelist().count(path) == 1, "missing or duplicate resource: " + path)
            need(archive.getinfo(path).file_size == size, "resource size drift: " + path)
            raw = archive.read(path)
            need(hashlib.sha256(raw).hexdigest() == expected, "resource hash drift: " + path)
            resources[path] = decode(raw)
    report = {"schema_version": 1, "scope": "PUBLISHER_RESOURCE_PROJECTION_ONLY",
              "publisher_sha256": JAR_SHA, "resource_count": len(resources),
              "resource_pins": {p: {"bytes": n, "sha256": h} for p, (n, h) in PINS.items()},
              "projection": project(resources), "limits": LIMITS}
    raw = (json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(raw)
    print("RESOURCE_REPORT_SHA256", hashlib.sha256(raw).hexdigest(), "BYTES", len(raw))
    print("RESOURCE_PROJECTION", json.dumps(report["projection"], sort_keys=True))
    print("NO_MUTATION WORLD_SAFETY_BLOCKED NOT_CERTIFIED")


def self_test():
    example = tag_projection({"values": ["test:block", {"id": "#test:optional", "required": False}]})
    need(example == {"replace": False, "declared_entries": [
        {"id": "test:block", "required": True, "kind": "BLOCK_ID"},
        {"id": "#test:optional", "required": False, "kind": "TAG_REFERENCE"}],
        "effective_membership": "NOT_VERIFIED"}, "wrong tag projection")
    cases = [
        b'{"values":[],"values":[]}', b'[]',
        b'{"replace":"true","values":[]}', b'{"values":"test:block"}',
        b'{"values":[{"id":"test:block","required":0}]}',
        b'{"values":[{"id":"test:block","extra":true}]}',
        b'{"values":["unqualified"]}', b'{"values":[null]}',
        b'{"values":[],"unexpected":true}',
    ]
    for raw in cases:
        try:
            tag_projection(decode(raw))
        except ValueError:
            continue
        raise AssertionError("malformed tag accepted: " + repr(raw))
    print("PASS: tag projection; rejected", len(cases), "malformed synthetic cases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        need(args.jar is not None and args.output is not None, "jar and output required")
        inspect(args.jar, args.output)
