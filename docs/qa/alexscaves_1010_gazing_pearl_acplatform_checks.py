#!/usr/bin/env python3
"""Fail-closed checks for the exact 1.0.10 ACPlatform storage bridge.

Source: publisher JAR discovery report, not an executable perk integration.
Do not promote Gazing Pearl, SavedData engine semantics, or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACPlatform"
WORLD = "com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData"
CITADEL = "com/github/alexmodguy/alexscaves/citadel/server/world/CitadelServerData"
EXPECTED_STATES = {
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}


def unique(pairs):
    result = {}
    for key, val in pairs:
        assert key not in result, ("duplicate JSON key", key)
        result[key] = val
    return result


def read(path: Path, max_bytes: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= max_bytes, ("report/manifest length", str(path))
    return raw, json.loads(raw, object_pairs_hook=unique)


def normalized_sha(obj):
    source = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def check_body(method, expected):
    d = method["declaration"]
    assert (d["name"], d["descriptor"]) == (expected["name"], expected["descriptor"])
    assert d["access"] == expected["access"]
    assert d["code_sha256"] == expected["code_sha256"]
    assert d["code_size"] == expected["code_size"]
    assert method["instruction_count"] == expected["instruction_count"]
    instructions = method["instructions"]
    assert len(instructions) == expected["instruction_count"]
    offsets = [x["offset"] for x in instructions]
    assert offsets == sorted(set(offsets))
    assert method["instruction_sha256"] == expected["instruction_sha256"]
    assert normalized_sha(instructions) == expected["instruction_sha256"]


def pivot(method, offset, opcode, symbol_fragment=None, operand=None):
    by_offset = {step["offset"]: step for step in method["instructions"]}
    assert offset in by_offset, ("missing JVM offset", offset)
    ins = by_offset[offset]
    assert ins["opcode"] == opcode, ("JVM opcode changed", offset)
    if symbol_fragment is not None:
        assert symbol_fragment in ins["symbol"], ("call/constant target drift", offset)
    if operand is not None:
        assert ins["operand"] == operand, ("operand drift", offset)


def assert_no_second_function_load(method):
    # ACC platform method locals: index 2 is the second Function parameter.
    # Synthetic loader lambda local 2 is the HolderLookup.Provider parameter.
    for ins in method["instructions"]:
        assert not (ins["opcode"] == "aload_2" or
                    (ins["opcode"] == "aload" and ins["operand"] == "2")), (
                        "previously unused local now consumed", ins["offset"])


def check(report_path: Path, manifest_path: Path):
    raw, report = read(report_path, 100_000)
    _, seal = read(manifest_path, 25_000)
    assert report["scope"] == seal["scope"] == (
        "GAZING_PEARL_ACPLATFORM_STORAGE_BRIDGE_DISCOVERY_ONLY")
    assert report["schema_version"] == seal["schema_version"] == 1
    assert len(raw) == seal["evidence"]["report_bytes"]
    assert hashlib.sha256(raw).hexdigest() == seal["evidence"]["report_sha256"]
    assert seal["evidence"]["run_id"] == 45011825823
    assert seal["evidence"]["artifact_id"] == 14750315491
    assert report["artifact"] == seal["artifact"]
    assert report["artifact"]["installed_binary_parity"] == "NOT_VERIFIED"
    assert all(report[k] == v and seal["states"][k] == v
               for k, v in EXPECTED_STATES.items())
    assert len(seal["states"]) == len(EXPECTED_STATES)

    n = report["native"]
    platform = seal["platform"]
    assert n["classfiles_scanned"] == 1555
    assert n["owner"] == platform["owner"] == OWNER
    assert n["class_sha256"] == platform["class_sha256"]
    assert n["hierarchy"]["parent"] == platform["parent"] == "java/lang/Object"
    assert n["hierarchy"]["access"] == platform["access"] == 33
    assert len(n["fields"]) == platform["field_count"] == 3
    assert len(n["method_declarations"]) == platform["method_declarations"] == 43
    assert len(n["platform_named_candidates"]) == platform["platform_named_candidates"] == 0
    assert n["has_executable_body"] is True
    assert len(n["exact_native_method"]) == 1
    assert len(n["loader_adapter_lambda"]) == 1

    methods = n["exact_native_method"] + n["loader_adapter_lambda"]
    assert [x["declaration"]["name"] for x in methods] == [
        "computeIfAbsent", "lambda$computeIfAbsent$1"]
    for method, expected in zip(methods, platform["methods"]):
        check_body(method, expected)
    native, adapter = methods
    assert n["exact_declaration"] == native["declaration"]

    for offset, opcode, symbol, operand in (
        (0, "aload_0", None, None),
        (1, "new", "SavedData$Factory", None),
        (5, "aload_3", None, None),  # supplier
        (6, "aload_1", None, None),  # first function only
        (7, "invokedynamic", "BiFunction", None),
        (12, "aconst_null", None, None),  # DataFixTypes argument
        (13, "invokespecial", 'SavedData$Factory."<init>":', None),
        (16, "aload", None, "4"),
        (18, "invokevirtual", "DimensionDataStorage.computeIfAbsent:", None),
        (21, "areturn", None, None),
    ):
        pivot(native, offset, opcode, symbol, operand)
    assert_no_second_function_load(native)

    for offset, opcode, symbol in (
        (0, "aload_0", None),
        (1, "aload_1", None),
        (2, "invokeinterface", "Function.apply:"),
        (7, "checkcast", "SavedData"),
        (10, "areturn", None),
    ):
        pivot(adapter, offset, opcode, symbol)
    assert_no_second_function_load(adapter)

    callers = n["direct_referencing_owners"]
    assert len(callers) == len(platform["callers"]) == 2
    assert set(callers) == {WORLD, CITADEL}
    for expected in platform["callers"]:
        owner = expected["owner"]
        item = callers[owner]
        assert item["class_sha256"] == expected["class_sha256"]
        assert len(item["typed_references"]) == 1
        assert item["typed_references"][0]["descriptor"] == (
            platform["methods"][0]["descriptor"])
        sites = item["invoke_sites"]
        assert len(sites) == 1
        site = sites[0]
        assert site["caller"] == expected["caller"] == "get"
        assert site["caller_descriptor"] == expected["descriptor"]
        assert site["offset"] == expected["offset"]
        assert site["opcode"] == "invokestatic"
        assert "ACPlatform.computeIfAbsent:" in site["symbol"]
        assert len(item["referencing_caller_bodies"]) == 1
        caller = item["referencing_caller_bodies"][0]
        assert caller["declaration"]["name"] == expected["caller"]
        assert caller["declaration"]["descriptor"] == expected["descriptor"]
        assert caller["declaration"]["code_sha256"] == expected["code_sha256"]
        assert caller["instruction_count"] == expected["instruction_count"]
        assert caller["instruction_sha256"] == expected["instruction_sha256"]
        assert normalized_sha(caller["instructions"]) == expected["instruction_sha256"]
        pivot(caller, expected["offset"], "invokestatic",
              "ACPlatform.computeIfAbsent:")
        if owner == WORLD:
            pivot(caller, 39, "ldc", "alexscaves_world_data")
            pivot(caller, 53, "invokevirtual", "setDirty:")
        else:
            pivot(caller, 29, "ldc", "alexscaves_citadel_world_data")
            pivot(caller, 39, "invokevirtual", "setDirty:")

    print("PASS: native factory 11 JVM instructions, synthetic adapter 5, two exact callers")
    print("EVIDENCE_SHA256", hashlib.sha256(raw).hexdigest())
    print("NO_MUTATION NOT_CERTIFIED PHYSICAL_QA_NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    check(args.report, args.manifest)
