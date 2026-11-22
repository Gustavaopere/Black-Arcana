#!/usr/bin/env python3
"""Offline read-only provenance gate for ResistorShieldItem partial evidence.

Cross-check the single-item partial manifest against SHA-exact support evidence
already in main. This deliberately does not certify the entire item or its
damage/blocking mechanics; the native class-wide report is a separate gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem"
PREFIX = "EXACT-"


def no_duplicate_keys(pairs):
    obj = {}
    for key, val in pairs:
        assert key not in obj, "duplicate JSON key: " + key
        obj[key] = val
    return obj


def read(path):
    raw = path.read_bytes()
    assert 0 < len(raw) < 2_000_000, "unbounded evidence"
    return json.loads(raw, object_pairs_hook=no_duplicate_keys)


def facts(method):
    return method["instruction_count"], method["instruction_sha256"]


def check(directory):
    partial = read(directory / "EXACT-RESISTOR-SHIELD-PARTIAL-EVIDENCE-1.0.10.json")
    registry = (directory / "systems/item-registry.md").read_text(encoding="utf-8")
    enchant = read(directory / "EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json")
    tick = read(directory / "EXACT-TICKING-ITEM-DISCOVERY-1.0.10.json")
    repair = read(directory / "EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json")
    client = read(directory / "EXACT-CLIENT-EXTENSION-1.0.10.json")

    assert partial["schema_version"] == 1
    assert partial["scope"] == "RESISTOR_SHIELD_PARTIAL_IDENTITY_AND_ENCHANTABILITY_ONLY"
    owner = partial["owner"]
    assert owner["name"] == OWNER
    assert partial["states"] == {
        "catalog": "PARTIAL", "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION", "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }
    assert partial["artifact"]["version"] == "1.0.10"
    assert partial["artifact"]["sha256"] == (
        "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
    )
    assert owner["full_method_census"] == "PENDING_NEW_DISCOVERY"
    for source in (tick, repair):
        assert source["artifact"]["sha256"] == partial["artifact"]["sha256"]
        item = source["owners"][OWNER]
        assert item["class_sha256"] == owner["class_sha256"]
        assert item["hierarchy"]["parent"] == owner["parent"]
        assert item["hierarchy"]["interfaces"] == owner["declared_interfaces"]

    # The registry table is deliberately Code SHA (not instruction SHA).
    reg = partial["item_registry"]
    assert reg["resource_id"] == "alexscaves:resistor_shield"
    assert reg["field"] == "ACItemRegistry.RESISTOR_SHIELD"
    assert reg["factory"] == "lambda$static$20"
    row = [line for line in registry.splitlines()
           if line.startswith("| `RESISTOR_SHIELD` |")]
    assert len(row) == 1, "registry binding row missing/duplicated"
    for token in ("alexscaves:resistor_shield", "lambda$static$20",
                  "new " + OWNER, reg["factory_code_sha256"]):
        assert token in row[0], ("registry mismatch", token)

    candidates = [x for x in enchant["owners"]
                  if x["owner"] == "ResistorShieldItem"]
    assert len(candidates) == 1
    e = candidates[0]
    assert e == {
        "owner": "ResistorShieldItem",
        "item_id": reg["resource_id"],
        "factory": reg["factory"],
        "bootstrap_offset": reg["bootstrap_offset"],
        "resource_count": 2,
        "value": 1,
        "declares_count_guard": True,
    }

    by_name = {
        x["name"]: x for x in owner["selected_methods"] + owner["support_callbacks"]
    }
    assert len(by_name) == 6, "partial method roster duplicated"
    assert by_name["getEnchantmentValue"]["behavior"] == "RETURN_LITERAL_1"
    assert by_name["isEnchantable"]["behavior"] == "STACK_COUNT_EQ_1"
    assert len(owner["selected_methods"]) == 2
    assert len(owner["support_callbacks"]) == 4
    tick_native = tick["owners"][OWNER]["methods"]
    repair_native = repair["owners"][OWNER]["methods"]
    assert len(tick_native) == 1
    assert len(repair_native) == 2
    for item in tick_native + repair_native:
        assert facts(item) == facts(by_name[item["name"]]), item["name"]

    callbacks = [x for x in client["callbacks"] if x["owner"] == OWNER]
    assert len(callbacks) == 1
    callback = callbacks[0]["method"]
    assert callback["name"] == "initializeClient"
    assert facts(callback) == facts(by_name[callback["name"]])
    assert callback["code_sha256"] == by_name[callback["name"]]["code_sha256"]
    assert callback["coverage"] == "FULL_BODY"
    assert callbacks[0]["proxy_getter"] == "getISTERProperties"

    mats = by_name["acExtraRepairMaterials"]
    assert mats["referenced_registry_fields"] == [
        "SCARLET_NEODYMIUM_INGOT", "AZURE_NEODYMIUM_INGOT",
    ]
    source_mats = repair_native[0]["materials"]
    assert [v["field"].split(".")[-1] for v in source_mats] == (
        mats["referenced_registry_fields"]
    )
    assert partial["resource_observation"]["paths_and_semantics"] == "NOT_VERIFIED"
    assert partial["contract_axes"]["targeting"] == "NOT_VERIFIED"
    assert partial["contract_axes"]["costs"] == "NOT_VERIFIED"
    print("PASS: exact prior registry, enchantability, repair, tick, "
          "client presentation evidence is consistent with six partial methods")
    print("NO_MUTATION STATIC_CONTRACT_NOT_CERTIFIED PHYSICAL_QA_NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-dir", type=Path, required=True)
    args = parser.parse_args()
    check(args.catalog_dir)
