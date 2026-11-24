#!/usr/bin/env python3
"""Read-only discovery of the next uncovered item classes, not certificates."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
import alexscaves_1010_burrowing_cave_map_probe as census
from alexscaves_1010_armor_material_audit import (
    SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)

PREFIX = "com/github/alexmodguy/alexscaves/server/item/"
TARGETS = tuple(PREFIX + n for n in (
    "HolocoderItem", "HotChocolateBottleItem", "InkBombItem",
))
TERMS = ("holocoder", "hot_chocolate", "ink_bomb")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    verify_artifact(a.jar)
    require(not a.output.exists(), "write-once report")
    census.TARGETS = TARGETS
    native = census.inspect(a.jar, a.javap)
    require(native["class_entries_scanned"] == 1555, "class roster drift")
    require(set(native["targets"]) == set(TARGETS), "target coverage drift")
    native.pop("filename_matched_resources", None)
    for owner, row in native["targets"].items():
        require(len(row["methods"]) == sum(
            "code_sha256" in d for d in row["declarations"]
        ), "incomplete executable body coverage: " + owner)
        require(any(c.endswith("/ACItemRegistry") for c in row["consumers"]),
                "typed registry reference absent: " + owner)
    resources = {}
    with ZipFile(a.jar) as z:
        for name in sorted(z.namelist()):
            if name.endswith(".json") and any(t in name.lower() for t in TERMS):
                raw = z.read(name)
                resources[name] = {"sha256": digest(raw), "size": len(raw),
                                   "json": json.loads(raw)}
    require(len(resources) <= 200, "resource bound")
    report = {
        "schema_version": 1,
        "scope": "THREE_ITEM_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
                     "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED"},
        "native": native,
        "filename_matched_resources": resources,
        "resource_limit": "FILENAME_MATCHES_ONLY",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "provider_universe_closed": False,
        "mutation": "NO_MUTATION",
        "semantic_magic_roots_certified_delta": 0,
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(a.output.read_bytes()), "BYTES", a.output.stat().st_size)
    for owner, row in native["targets"].items():
        print("TARGET", owner, json.dumps({k: v for k, v in row.items()
              if k not in ("methods", "consumers", "ancestors", "typed_census", "member_refs")}, sort_keys=True))
        for method in row["methods"]:
            print("METHOD", owner, json.dumps(method, sort_keys=True))
        for consumer, evidence in row["consumers"].items():
            print("CONSUMER", owner, consumer, json.dumps({
                "class_sha256": evidence["class_sha256"],
                "sites": evidence["sites"],
                "bodies": [census.compact(m) for m in evidence["bodies"]]
            }, sort_keys=True))
        for parent, evidence in row["ancestors"].items():
            print("ANCESTOR", owner, parent, json.dumps({
                "class_sha256": evidence["class_sha256"],
                "methods": [census.compact(m) for m in evidence["methods"]]
            }, sort_keys=True))
    print("RESOURCES", json.dumps(resources, sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_STATIC_CERTIFICATION")

if __name__ == "__main__":
    main()
