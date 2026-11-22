#!/usr/bin/env python3
"""Fail-closed SHA-exact Resistor Shield helper/resource discovery verifier.

Read-only: validates a publisher JAR-derived dependency report against a
human-reviewed manifest. Does not certify gameplay, hooks, or provider closure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
ARTIFACT = {
    "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
    "sha1": "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570",
    "sha256": "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
    "size_bytes": 75279314,
    "installed_binary_parity": "NOT_VERIFIED",
}
STATES = {
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "provider_universe_closed": False,
    "mutation": "NO_MUTATION",
}


def unique(pairs):
    output = {}
    for key, value in pairs:
        assert key not in output, "duplicate JSON key: " + key
        output[key] = value
    return output


def read(path, limit):
    raw = path.read_bytes()
    assert 0 < len(raw) <= limit, ("invalid report or manifest length", path)
    return raw, json.loads(raw, object_pairs_hook=unique)


def canonical_json_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False).encode("utf8")
    return hashlib.sha256(raw).hexdigest()


def check(report_path: Path, manifest_path: Path) -> None:
    manifest_raw, seal = read(manifest_path, 50_000)
    report_raw, report = read(report_path, 500_000)
    assert seal["schema_version"] == report["schema_version"] == 1
    assert seal["scope"] == report["scope"] == (
        "RESISTOR_SHIELD_TRANSITIVE_DEPENDENCY_DISCOVERY_ONLY"
    )
    assert seal["artifact"] == ARTIFACT == report["artifact"]
    assert all(report[k] == v and seal["states"][k] == v
               for k, v in STATES.items())
    assert len(seal["states"]) == len(STATES)
    assert hashlib.sha256(report_raw).hexdigest() == (
        seal["evidence"]["report_sha256"]
    ), "publisher helper report SHA drift"
    assert len(report_raw) == seal["evidence"]["report_bytes"]
    assert seal["evidence"]["run_id"] == 44981995099
    assert seal["evidence"]["artifact_id"] == 14738305848
    cls = report["helper_class"]
    assert cls["owner"] == seal["helper_class"]["owner"] == OWNER
    assert cls["class_sha256"] == seal["helper_class"]["sha256"]
    assert cls["superclass"] == "java/lang/Object"
    assert cls["scope"] == "ONLY_DIRECTLY_NAMED_HELPERS_NOT_ALL_TRANSITIVE_CONSUMERS"
    methods = cls["methods"]
    actual = {}
    for method in methods:
        d = method["declaration"]
        key = (d["name"], d["descriptor"])
        assert key not in actual, ("duplicate native helper", key)
        assert method["instruction_count"] == len(method["instructions"])
        actual[key] = {
            "instruction_count": method["instruction_count"],
            "instruction_sha256": method["instruction_sha256"],
            "code_sha256": d["code_sha256"],
        }
    expected = {}
    for method in seal["methods"]:
        key = (method["name"], method["descriptor"])
        assert key not in expected, ("duplicate manifest helper", key)
        expected[key] = {k: method[k] for k in (
            "instruction_count", "instruction_sha256", "code_sha256"
        )}
    assert len(actual) == len(expected) == 10
    assert actual == expected, "helper method name/descriptor/fingerprint drift"

    by_name = {}
    for method in methods:
        by_name.setdefault(method["declaration"]["name"], []).append(method)
    assert set(by_name) == {
        "enchantLevel", "useConsume", "knockback", "hurtAndBreakUsedHand",
        "getTag", "getOrCreateTag", "setTag", "getInt", "getBoolean",
    }
    assert len(by_name["getInt"]) == 2, "getInt overload coverage mismatch"

    def pivot(name, offset, opcode, symbol=None):
        assert len(by_name[name]) == 1, ("ambiguous method", name)
        by_offset = {x["offset"]: x for x in by_name[name][0]["instructions"]}
        assert offset in by_offset, ("missing JVM offset", name, offset)
        ins = by_offset[offset]
        assert ins["opcode"] == opcode, ("opcode drift", name, offset)
        if symbol:
            assert symbol in ins["symbol"], ("call target drift", name, offset)

    for name, offset, opcode, symbol in (
        ("enchantLevel", 1, "invokevirtual", "ItemStack.getEnchantments:"),
        ("enchantLevel", 42, "invokeinterface", "Holder.is:"),
        ("enchantLevel", 51, "invokeinterface", "Entry.getIntValue:"),
        ("enchantLevel", 60, "iconst_0", None),
        ("useConsume", 1, "invokestatic", "InteractionResultHolder.consume:"),
        ("knockback", 5, "invokevirtual", "LivingEntity.knockback:"),
        ("hurtAndBreakUsedHand", 4, "invokevirtual", "getUsedItemHand:"),
        ("hurtAndBreakUsedHand", 7, "invokestatic", "slotOf:"),
        ("hurtAndBreakUsedHand", 10, "invokevirtual", "ItemStack.hurtAndBreak:"),
        ("getTag", 1, "getstatic", "DataComponents.CUSTOM_DATA"),
        ("getTag", 20, "invokevirtual", "CustomData.copyTag:"),
        ("getOrCreateTag", 1, "getstatic", "DataComponents.CUSTOM_DATA"),
        ("getOrCreateTag", 19, "invokespecial", 'CompoundTag."<init>":'),
        ("getOrCreateTag", 26, "invokevirtual", "CustomData.copyTag:"),
        ("setTag", 8, "invokevirtual", "ItemStack.remove:"),
        ("setTag", 20, "invokestatic", "CustomData.of:"),
        ("setTag", 23, "invokevirtual", "ItemStack.set:"),
        ("getBoolean", 2, "invokevirtual", "CompoundTag.getBoolean:"),
    ):
        pivot(name, offset, opcode, symbol)

    actual_resources = report["resources"]
    expected_resources = seal["resources"]
    assert set(actual_resources) == set(expected_resources) and len(expected_resources) == 4
    for path, proof in expected_resources.items():
        result = actual_resources[path]
        assert result["sha256"] == proof["sha256"]
        assert result["size_bytes"] == proof["size_bytes"]
        assert canonical_json_hash(result["parsed_json"]) == (
            proof["canonical_json_sha256"]
        ), ("semantic JSON changed", path)
    recipe = actual_resources["data/alexscaves/recipe/resistor_shield.json"]["parsed_json"]
    assert recipe["type"] == "minecraft:crafting_shaped"
    assert recipe["pattern"] == ["SSS", " H ", "AAA"]
    assert recipe["result"]["id"] == "alexscaves:resistor_shield"
    assert {k: v["item"] for k, v in recipe["key"].items()} == {
        "S": "alexscaves:scarlet_neodymium_ingot",
        "A": "alexscaves:azure_neodymium_ingot",
        "H": "alexscaves:heart_of_iron",
    }
    tag = actual_resources[
        "data/alexscaves/tags/item/enchantable/resistor_shield.json"
    ]["parsed_json"]
    assert tag == {"values": ["alexscaves:resistor_shield"]}
    adv = actual_resources[
        "data/alexscaves/advancement/alexscaves/resistor_shield.json"
    ]["parsed_json"]
    assert adv["parent"] == "alexscaves:alexscaves/defeat_magnetron"
    assert adv["criteria"]["resistor_shield"]["trigger"] == (
        "minecraft:inventory_changed"
    )
    model = actual_resources[
        "assets/alexscaves/models/item/resistor_shield.json"
    ]["parsed_json"]
    assert model["parent"] == "builtin/entity"
    assert model["textures"]["particle"] == (
        "alexscaves:block/heart_of_iron_0"
    )
    print("PASS: exact publisher helpers, callsites, resource JSON and fail-closed states")
    print("EVIDENCE_SHA256", hashlib.sha256(report_raw).hexdigest())
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    check(args.report, args.manifest)
