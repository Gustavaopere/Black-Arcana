#!/usr/bin/env python3
"""Fail-closed ACPlatform JVM bootstrap mapping checker for publisher 1.0.10.

Performs reproducible bytecode linkage checks on existing evidence. Does not
certify the Gazing Pearl item, minecraft SavedData settlement, physical QA
or any mutating integration point.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACPlatform"
LOADER = "lambda$computeIfAbsent$1"
STATES = {
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}


def read(path: Path, limit: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= limit, ("evidence size out of bounds", str(path))
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out, ("duplicate key", key)
            out[key] = value
        return out
    return raw, json.loads(raw, object_pairs_hook=pairs)


def normalized_sha(value):
    s = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return hashlib.sha256(s.encode("utf8")).hexdigest()


def pivot(method, offset, opcode, needle=None):
    hits = [x for x in method["instructions"] if x["offset"] == offset]
    assert len(hits) == 1, ("unexpected JVM offset", offset)
    actual = hits[0]
    assert actual["opcode"] == opcode, ("JVM opcode changed", offset)
    if needle is not None:
        assert needle in actual["symbol"], ("JVM callsite target changed", offset)


def check(report: Path, manifest: Path):
    raw, source = read(report, 100_000)
    _, seal = read(manifest, 20_000)
    assert source["schema_version"] == seal["schema_version"] == 1
    assert source["scope"] == seal["scope"] == (
        "GAZING_PEARL_ACPLATFORM_INVOKEDYNAMIC_BOOTSTRAP_ONLY")
    assert hashlib.sha256(raw).hexdigest() == seal["evidence"]["report_sha256"]
    assert len(raw) == seal["evidence"]["report_bytes"]
    assert seal["evidence"]["run_id"] == 45013296440
    assert seal["evidence"]["artifact_id"] == 14750956691
    assert source["artifact"] == seal["artifact"]
    assert source["artifact"]["installed_copy_verified"] is False
    for key, value in STATES.items():
        assert source[key] == value and seal["states"][key] == value
    assert len(seal["states"]) == len(STATES)

    native, expected = source["native"], seal["native"]
    assert native["owner"] == expected["owner"] == OWNER
    assert native["class_sha256"] == expected["class_sha256"]
    assert native["bootstrap_count"] == expected["bootstrap_count"] == 3
    assert native["bootstrap_table_sha256"] == expected["bootstrap_table_sha256"]
    d = native["factory_invokedynamic"]
    assert (d["offset"],d["opcode"]) == (7,"invokedynamic")
    assert (d["bootstrap_index"],d["constant_pool_index"]) == (
        expected["bootstrap_index"],expected["constant_pool_index"]) == (0,136)
    assert d["operand"] == "#136, 0"
    assert d["name_type"] == [
        12, expected["invokedynamic_name"], expected["invokedynamic_descriptor"]]
    assert d["name_type"] == [
        12, "apply", "(Ljava/util/function/Function;)Ljava/util/function/BiFunction;"]
    assert d["bootstrap_entry"] == expected["bootstrap_entry"]
    entry = d["bootstrap_entry"]
    handle = entry["handle"]
    assert handle["reference_kind"] == 6
    assert handle["reference"][0] == 10
    assert handle["reference"][1] == "java/lang/invoke/LambdaMetafactory"
    assert handle["reference"][2][1] == "metafactory"
    assert len(entry["arguments"]) == 3
    assert entry["arguments"][0] == "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;"
    linked = entry["arguments"][1]
    assert linked["reference_kind"] == 6
    assert linked["reference"][0] == 10
    assert linked["reference"][1] == OWNER
    assert linked["reference"][2][0] == 12
    assert linked["reference"][2][1] == LOADER
    assert linked["reference"][2][2] == expected["methods"][1]["descriptor"]
    assert entry["arguments"][2] == (
        "(Lnet/minecraft/nbt/CompoundTag;"
        "Lnet/minecraft/core/HolderLookup$Provider;)"
        "Lnet/minecraft/world/level/saveddata/SavedData;")

    factory = native["factory_method"]
    adapter = native["loader_adapter_method"]
    assert len(expected["methods"]) == 2
    for method, summary in ((factory,expected["methods"][0]),(adapter,expected["methods"][1])):
        decl = method["declaration"]
        assert (decl["name"],decl["descriptor"]) == (
            summary["name"], summary["descriptor"])
        assert decl["code_sha256"] == summary["code_sha256"]
        assert method["instruction_count"] == summary["instruction_count"]
        assert len(method["instructions"]) == method["instruction_count"]
        assert method["instruction_sha256"] == summary["instruction_sha256"]
        assert normalized_sha(method["instructions"]) == method["instruction_sha256"]
    assert factory["declaration"]["name"] == "computeIfAbsent"
    assert adapter["declaration"]["name"] == LOADER
    pivot(factory,7,"invokedynamic","InvokeDynamic #0:apply:")
    pivot(factory,13,"invokespecial",'SavedData$Factory."<init>":')
    pivot(factory,18,"invokevirtual","DimensionDataStorage.computeIfAbsent:")
    assert [x["offset"] for x in factory["instructions"]
            if x["opcode"] == "invokedynamic"] == [7]
    pivot(adapter,2,"invokeinterface","Function.apply:")
    pivot(adapter,7,"checkcast","SavedData")
    for method in (factory, adapter):
        assert not any(x["opcode"] == "aload_2" or
                       (x["opcode"] == "aload" and x["operand"] == "2")
                       for x in method["instructions"]), "unused local unexpectedly consumed"
    print("PASS: JVM cp#136 BootstrapMethods[0] LambdaMetafactory -> ACPlatform.lambda$computeIfAbsent$1")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("STATIC_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--report", type=Path, required=True)
    cli.add_argument("--manifest", type=Path, required=True)
    args = cli.parse_args()
    check(args.report, args.manifest)
