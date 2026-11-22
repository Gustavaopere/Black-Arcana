#!/usr/bin/env python3
"""Fail-closed SHA-exact Deep One reputation ACWorldData discovery checker.

The contract is bytecode-only; it does not certify gameplay, writable APIs,
Minecraft SavedData settlement or the Gazing Pearl item as a whole.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

def unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, ("duplicate key", key)
        out[key] = value
    return out

def read(path, maximum):
    raw = path.read_bytes()
    assert 0 < len(raw) <= maximum, ("unexpected evidence size", path)
    return raw, json.loads(raw, object_pairs_hook=unique)

def digest_rows(rows):
    # The producer uses alexscaves_1010_armor_material_audit.canonical.
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return hashlib.sha256(raw.encode("utf8")).hexdigest()

def signature(row):
    d = row["declaration"]
    return d["name"], d["descriptor"]

def method_fingerprints(rows):
    out = {}
    for method in rows:
        key = signature(method)
        assert key not in out, ("duplicate method", key)
        assert method["instruction_count"] == len(method["instructions"])
        offsets = [ins["offset"] for ins in method["instructions"]]
        assert len(offsets) == len(set(offsets)) and offsets == sorted(offsets)
        assert method["instruction_sha256"] == digest_rows(method["instructions"])
        d = method["declaration"]
        out[key] = {
            "instruction_count": method["instruction_count"],
            "instruction_sha256": method["instruction_sha256"],
            "code_sha256": d["code_sha256"],
        }
    return out

def manifest_fingerprints(rows):
    out = {}
    for m in rows:
        key = m["name"], m["descriptor"]
        assert key not in out
        out[key] = {k:m[k] for k in
                    ("instruction_count", "instruction_sha256", "code_sha256")}
    return out

def check_pivot(method, offset, opcode, operand=None, symbol=None):
    by_offset = {r["offset"]: r for r in method["instructions"]}
    assert offset in by_offset, ("missing JVM offset", signature(method), offset)
    instruction = by_offset[offset]
    assert instruction["opcode"] == opcode, ("JVM opcode drift", signature(method), offset)
    if operand is not None:
        assert operand in instruction["operand"], ("JVM literal/branch drift", signature(method), offset)
    if symbol is not None:
        assert symbol in instruction["symbol"], ("JVM target drift", signature(method), offset)

def check(report_path: Path, manifest_path: Path) -> None:
    raw, report = read(report_path, 500_000)
    _, manifest = read(manifest_path, 100_000)
    assert report["schema_version"] == manifest["schema_version"] == 1
    assert report["scope"] == manifest["scope"] == "GAZING_PEARL_ACWORLD_DATA_REPUTATION_DISCOVERY_ONLY"
    assert len(raw) == manifest["evidence"]["report_bytes"] == 77203
    assert hashlib.sha256(raw).hexdigest() == manifest["evidence"]["report_sha256"]
    assert manifest["evidence"]["run_id"] == 45009967780
    assert manifest["evidence"]["artifact_id"] == 14749775926
    assert report["artifact"]["sha256"] == manifest["source"]["publisher_sha256"]
    assert report["artifact"]["sha1"] == manifest["source"]["installed_sha1_ledger"]
    assert report["artifact"]["size_bytes"] == 75279314
    assert report["artifact"]["installed_copy_verified"] is False
    assert manifest["source"]["installed_copy_verified"] is False
    for key, val in manifest["limitations"].items():
        assert report[key] == val, ("unsafe certification drift", key)

    native = report["native"]
    owner = manifest["owner"]
    assert native["publisher_classfiles_scanned"] == 1555
    assert native["owner"] == owner["name"]
    assert native["class_sha256"] == owner["class_sha256"]
    assert native["hierarchy"]["parent"] == owner["parent"]
    assert len(native["fields"]) == owner["fields"] == 6
    assert len(native["declarations"]) == owner["declarations"] == 17
    assert native["selected_method_count"] == len(native["selected_methods"]) == 8
    expected_methods = manifest_fingerprints(owner["methods"])
    actual_methods = method_fingerprints(native["selected_methods"])
    assert len(expected_methods) == 8
    assert actual_methods == expected_methods, "owner methods differ from publisher seal"
    methods = {m["declaration"]["name"]: m for m in native["selected_methods"]}
    assert len(methods) == 8, "unexpected overload in selected owner methods"
    for name, offset, opcode, operand, symbol in (
        ("get", 1, "instanceof", None, "ServerLevel"),
        ("get", 4, "ifeq", "58", None),
        ("get", 11, "getstatic", None, "Level.OVERWORLD"),
        ("get", 39, "ldc", None, "alexscaves_world_data"),
        ("get", 41, "invokestatic", None, "ACPlatform.computeIfAbsent:"),
        ("get", 53, "invokevirtual", None, "setDirty:"),
        ("get", 58, "aconst_null", None, None),
        ("getDeepOneReputation", 1, "ifnonnull", "8", None),
        ("getDeepOneReputation", 4, "iconst_0", None, None),
        ("getDeepOneReputation", 17, "invokeinterface", None, "Map.getOrDefault:"),
        ("setDeepOneReputation", 6, "bipush", "-100", None),
        ("setDeepOneReputation", 8, "bipush", "100", None),
        ("setDeepOneReputation", 10, "invokestatic", None, "Mth.clamp:"),
        ("setDeepOneReputation", 16, "invokeinterface", None, "Map.put:"),
        ("load", 9, "ldc", None, "DeepOneReputations"),
        ("load", 22, "invokestatic", None, "ACCompat.getList:"),
        ("load", 51, "invokestatic", None, "ACCompat.getUUID:"),
        ("load", 58, "invokestatic", None, "ACCompat.getInt:"),
        ("load", 64, "invokeinterface", None, "Map.put:"),
        ("save", 2, "invokevirtual", None, "acSave:"),
        ("acSave", 4, "invokeinterface", None, "Map.isEmpty:"),
        ("acSave", 9, "ifne", "119", None),
        ("acSave", 24, "invokeinterface", None, "Map.entrySet:"),
        ("acSave", 78, "invokestatic", None, "ACCompat.putUUID:"),
        ("acSave", 98, "invokevirtual", None, "CompoundTag.putInt:"),
        ("acSave", 115, "invokevirtual", None, "CompoundTag.put:"),
        ("acSave", 169, "aload_1", None, None),
        ("lambda$get$0", 8, "invokevirtual", None, "acSave:"),
    ):
        check_pivot(methods[name], offset, opcode, operand, symbol)

    consumers = native["reputation_reference_owners"]
    assert len(consumers) == 3
    assert set(consumers) == {m["owner"] for m in manifest["consumer_bodies"]}
    actual_consumer_methods = {}
    observed_sites = set()
    for ownername, data in consumers.items():
        assert len(data["class_sha256"]) == 64
        selected = method_fingerprints(data["referencing_bodies"])
        for (name, desc), values in selected.items():
            actual_consumer_methods[(ownername, name, desc)] = values
        for site in data["executed_instruction_sites_in_disassembly"]:
            assert site["opcode"].startswith("invoke")
            callee = site["symbol"]
            matched = ("getDeepOneReputation" if "getDeepOneReputation:" in callee
                       else "setDeepOneReputation" if "setDeepOneReputation:" in callee
                       else None)
            assert matched is not None
            observed_sites.add((ownername, site["caller_method"],site["offset"],matched))
    expected_consumer_methods = {
        (x["owner"], x["name"], x["descriptor"]):
            {k:x[k] for k in ("instruction_count","instruction_sha256","code_sha256")}
        for x in manifest["consumer_bodies"]
    }
    assert len(actual_consumer_methods) == len(expected_consumer_methods) == 4
    assert actual_consumer_methods == expected_consumer_methods
    expected_sites = {(x["owner"],x["method"],x["offset"],x["callee"])
                      for x in manifest["consumer_sites"]}
    assert len(observed_sites) == len(expected_sites) == 5
    assert observed_sites == expected_sites

    caller = {
        (own, m["declaration"]["name"]): m
        for own, data in consumers.items() for m in data["referencing_bodies"]
    }
    # The client guard is in the DeepOneBaseEntity caller, not in
    # the public setter itself.
    base = "com/github/alexmodguy/alexscaves/server/entity/living/DeepOneBaseEntity"
    mine = "com/github/alexmodguy/alexscaves/server/entity/living/MineGuardianEntity"
    pearl = "com/github/alexmodguy/alexscaves/server/item/GazingPearlItem"
    for name, exit_at in (("getReputationOf","32"),("setReputationOf","28")):
        check_pivot(caller[(base,name)],7,"ifne",exit_at,None)
    check_pivot(caller[(base,"getReputationOf")],28,"invokevirtual",None,"getDeepOneReputation:")
    check_pivot(caller[(base,"setReputationOf")],25,"invokevirtual",None,"setDeepOneReputation:")
    for offset, opcode, operand, symbol in (
        (13,"ifne","85",None),
        (27,"ifeq","85",None),
        (51,"invokevirtual",None,"getDeepOneReputation:"),
        (58,"ifge","85",None),
        (73,"invokeinterface",None,"RandomSource.nextInt:"),
        (79,"iadd",None,None),
        (80,"iconst_1",None,None),
        (81,"iadd",None,None),
        (82,"invokevirtual",None,"setDeepOneReputation:"),
    ):
        check_pivot(caller[(mine,"dropAllDeathLoot")],offset,opcode,operand,symbol)
    check_pivot(caller[(pearl,"acInventoryTick")],4,"ifne","95",None)
    check_pivot(caller[(pearl,"acInventoryTick")],40,"ifle","95",None)
    check_pivot(caller[(pearl,"acInventoryTick")],83,"invokevirtual",None,"getDeepOneReputation:")
    print("PASS: exact ACWorldData/consumer SHA, serialization and 5 reputation sites")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    a=p.parse_args()
    check(a.report,a.manifest)
