#!/usr/bin/env python3
"""Fail-closed SHA-exact validation of discovery-only Hazmat evidence.

Pins full report and method/resource roster. Does not certify full armor effects,
external engine behavior, mutating hooks or physical gameplay.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/HazmatArmorItem"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SIZE = 75279314
NAMES = ("hazmat_mask", "hazmat_chestplate", "hazmat_leggings", "hazmat_boots")


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, "duplicate JSON key: " + key
        result[key] = value
    return result


def load(path: Path, budget: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= budget, "evidence size budget exceeded"
    return json.loads(raw, object_pairs_hook=pairs_unique), hashlib.sha256(raw).hexdigest()


def name_body(method):
    return {"name": method["declaration"]["name"],
            "instruction_count": method["instruction_count"],
            "instruction_sha256": method["instruction_sha256"]}


def instructions(method):
    return " ".join(row["symbol"] + " " + row["operand"]
                    for row in method["instructions"])


def check(report_path: Path, manifest_path: Path) -> None:
    manifest, _ = load(manifest_path, 100_000)
    report, report_sha = load(report_path, 16_000_000)
    assert report_sha == manifest["report"]["sha256"], "report identity drift"
    assert report["schema_version"] == manifest["schema_version"] == 1
    assert report["scope"] == manifest["scope"] == "HAZMAT_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert manifest["artifact"] == report["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1,
        "sha256": SHA256, "size_bytes": SIZE,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert report["owner"] == manifest["native_class"]["owner"] == OWNER
    assert tuple(report["registry_candidates_not_individually_certified"]) == NAMES
    assert report["source_revision_parity"] == "NOT_ASSUMED"
    for key, expected in {
        "other_radiation_consumers_complete": False,
        "engine_and_external_armor_effects_verified": False,
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert report[key] == expected, key
    limits = manifest["limits"]
    assert limits["status"] == "PARTIAL"
    assert limits["provider_universe_closed"] is False
    assert limits["static_contract"] == report["static_contract"]
    assert limits["mutating_hook"] == report["mutating_hook"]
    assert limits["physical_qa"] == report["physical_qa"]
    assert limits["mutation"] == report["mutation"]
    assert limits["new_cast_roots"] == report["semantic_magic_roots_certified_delta"]
    assert limits["external_armor_effects"] == "NOT_VERIFIED"
    assert limits["other_consumers"] == "NOT_EXHAUSTIVE"
    native = report["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    item = native["targets"][OWNER]
    spec = manifest["native_class"]
    assert item["class_sha256"] == spec["sha256"]
    assert len(item["declarations"]) == spec["declared_methods"] == 6
    assert len(item["methods"]) == spec["code_methods"] == 6
    assert len(item["fields"]) == spec["fields"] == 0
    assert len(item["consumers"]) == spec["typed_consumer_owners"] == 7
    assert len(item["methods"]) == sum(
        "code_sha256" in entry for entry in item["declarations"]
    )
    assert [name_body(method) for method in item["methods"]] == spec["methods"]
    for method in item["methods"]:
        assert method["instruction_count"] == len(method["instructions"])
    actual_consumers = item["consumers"]
    assert set(actual_consumers) == set(manifest["consumer_methods"])
    for name, expected in manifest["consumer_methods"].items():
        c = actual_consumers[name]
        assert len(c["sites"]) == expected["sites"], name
        assert [name_body(x) for x in c["bodies"]] == expected["methods"], name
    assert len(actual_consumers[
        "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
    ]["sites"]) == 8
    resources = report["filename_matched_resource_hashes"]
    assert len(resources) == manifest["resources"]["filename_matched_count"] == 28
    for path, data in resources.items():
        assert "hazmat" in path.lower() and path.endswith(".json")
        assert set(data) == {"size", "sha256"}
        assert data["size"] > 0 and len(data["sha256"]) == 64
    for area in ("models", "recipes"):
        for name, sha in manifest["resources"][area].items():
            prefix = ("assets/alexscaves/models/item/" if area == "models"
                      else "data/alexscaves/recipe/")
            assert resources[prefix + name + ".json"]["sha256"] == sha
    for name, sha in manifest["resources"]["tag"].items():
        assert resources[name]["sha256"] == sha

    own = {m["declaration"]["name"]: m for m in item["methods"]}
    seen = instructions(own["getWornAmount"])
    for x in ("EquipmentSlot.HEAD", "EquipmentSlot.CHEST",
              "EquipmentSlot.LEGS", "EquipmentSlot.FEET",
              "HAZMAT_MASK", "HAZMAT_CHESTPLATE",
              "HAZMAT_LEGGINGS", "HAZMAT_BOOTS", "ItemStack.is"):
        assert x in seen, x
    for x in ("ACCompat.isWornArmor", "acArmorTick"):
        assert x in instructions(own["acInventoryTick"]), x
    for x in ("HAZMAT_BREATHE", "Math.cos", "Math.toRadians"):
        assert x in instructions(own["acArmorTick"]), x
    for consumer, method_name, terms in [
        ("com/github/alexmodguy/alexscaves/server/item/RadioactiveItem",
         "acInventoryTick", ("getCount", "randomChanceOfRadiation", "getWornAmount",
                             "IRRADIATED", "MobEffectInstance", "sipush 1800", "addEffect")),
        ("com/github/alexmodguy/alexscaves/server/potion/IrradiatedEffect",
         "tick", ("getWornAmount", "float 0.25f", "causeFoodExhaustion",
                  "float 0.4f", "RaycatEntity", "causeRadiationDamage")),
        ("com/github/alexmodguy/alexscaves/server/block/AcidBlock",
         "entityInside", ("RESISTS_ACID", "WEAK_TO_ACID", "getWornAmount",
                          "HazmatArmorItem", "hurtAndBreak", "causeAcidDamage")),
    ]:
        meth = next(x for x in actual_consumers[consumer]["bodies"]
                    if x["declaration"]["name"] == method_name)
        body = instructions(meth)
        for x in terms:
            assert x in body, (consumer, x)
    print("PASS: pinned Hazmat owner six method hashes, seven typed consumers, "
          "28 resource hashes, causal guards, malformed input rejected; PARTIAL NO_MUTATION")
    print("REPORT_SHA256", report_sha)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    args = p.parse_args()
    check(args.report, args.manifest)
