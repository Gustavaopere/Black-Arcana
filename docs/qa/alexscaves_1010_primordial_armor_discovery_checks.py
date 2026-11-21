#!/usr/bin/env python3
"""Fail-closed SHA-exact seal of Primordial Armor discovery-only evidence.

Pins the publisher report, exact method declarations/bodies and five typed
consumers. This never approves per-item perks, hooks or physical gameplay.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/PrimordialArmorItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
NAMES = ("primordial_helmet", "primordial_tunic", "primordial_pants")


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        assert k not in out, "duplicate JSON key: " + k
        out[k] = v
    return out


def read(path: Path, limit: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= limit, "evidence report exceeds size budget"
    return json.loads(raw, object_pairs_hook=unique_pairs), hashlib.sha256(raw).hexdigest()


def record(method):
    d = method["declaration"]
    return {"name": d["name"], "descriptor": d["descriptor"],
            "instruction_count": method["instruction_count"],
            "instruction_sha256": method["instruction_sha256"]}


def flattened(method):
    return " ".join(row["opcode"] + " " + row["operand"] + " " + row["symbol"]
                    for row in method["instructions"])


def verify(path: Path, manifest_path: Path):
    r, report_hash = read(path, 16_000_000)
    m, _ = read(manifest_path, 100_000)
    assert report_hash == m["report"]["sha256"], "report hash drift"
    assert r["schema_version"] == m["schema_version"] == 1
    assert r["scope"] == m["scope"] == "PRIMORDIAL_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert r["artifact"] == m["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1,
        "sha256": SHA256, "size_bytes": SIZE,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert r["owner"] == m["native_class"]["owner"] == OWNER
    assert tuple(r["registry_candidates_not_individually_certified"]) == NAMES
    assert r["source_revision_parity"] == "NOT_ASSUMED"
    assert r["other_consumers_complete"] is False
    assert r["provider_universe_closed"] is False
    assert r["static_contract"] == "NOT_CERTIFIED"
    assert r["semantic_magic_roots_certified_delta"] == 0
    assert r["mutating_hook"] == "NOT_VERIFIED"
    assert r["physical_qa"] == "NOT_TESTED"
    assert r["mutation"] == "NO_MUTATION"
    l = m["limits"]
    assert l == {
        "status": "PARTIAL", "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
        "new_magic_roots": 0, "other_food_consumers_complete": False,
        "fooddata_engine_effects": "NOT_VERIFIED",
    }
    assert m["static_behavior"] == {
        "worn_pieces_range": [0,3], "counting_method": "getExtraSaturationFromArmor",
        "raw_meat_tag": "RAW_MEATS", "base_food_bonus_per_piece": 1,
        "saturation_modifier_argument_bonus_per_piece": 0.125,
        "raw_meat_consumer": "PlayerMixin.ac_eat",
        "block_consumer": "DinosaurChopBlock.eat",
        "data_dynamics": "ENGINE_NOT_VERIFIED",
    }
    native = r["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    owner = native["targets"][OWNER]
    spec = m["native_class"]
    assert owner["class_sha256"] == spec["sha256"]
    assert len(owner["declarations"]) == spec["declarations"] == 4
    assert len(owner["methods"]) == spec["code_methods"] == 4
    assert len(owner["fields"]) == spec["fields"] == 0
    assert len(owner["consumers"]) == spec["typed_consumer_owners"] == 5
    assert not owner["in_jar_ancestors"], "unexpected in-jar ancestor"
    assert len(owner["methods"]) == sum("code_sha256" in x for x in owner["declarations"])
    assert [record(x) for x in owner["methods"]] == spec["methods"]
    for x in owner["methods"]:
        assert len(x["instructions"]) == x["instruction_count"]

    consumers = owner["consumers"]
    assert set(consumers) == set(m["consumer_methods"])
    for cname, cspec in m["consumer_methods"].items():
        actual = consumers[cname]
        assert len(actual["sites"]) == cspec["sites"], cname
        assert [record(x) for x in actual["bodies"]] == cspec["methods"], cname

    assert r["filename_matched_resource_hashes"] == m["resources"]
    assert len(m["resources"]) == 8
    for name, data in m["resources"].items():
        assert name.endswith(".json")
        assert any(x in name for x in (*NAMES, "primordial_armor"))
        assert len(data["sha256"]) == 64 and data["size"] > 0
    own = {x["declaration"]["name"]: flattened(x) for x in owner["methods"]}
    counter = own["getExtraSaturationFromArmor"]
    for needle in ("PRIMORDIAL_HELMET", "PRIMORDIAL_TUNIC", "PRIMORDIAL_PANTS",
                   "EquipmentSlot.HEAD", "EquipmentSlot.CHEST", "EquipmentSlot.LEGS",
                   "ItemStack.is", "iinc 1, 1"):
        assert needle in counter, ("counter", needle)
    assert "primordial_armor_1.png" in own["getArmorTexture"]
    assert "primordial_armor_0.png" in own["getArmorTexture"]
    for cname, name, tokens in (
        ("com/github/alexmodguy/alexscaves/mixin/PlayerMixin", "ac_eat",
         ("RAW_MEATS", "getExtraSaturationFromArmor", "FoodData.eat", "nutrition",
          "saturationModifier", "float 0.125f")),
        ("com/github/alexmodguy/alexscaves/server/block/DinosaurChopBlock", "eat",
         ("canEat", "DINOSAUR_CHOP", "getExtraSaturationFromArmor",
          "foodAmount", "saturationAmount", "float 0.125f", "FoodData.eat")),
    ):
        method = next(x for x in consumers[cname]["bodies"]
                      if x["declaration"]["name"] == name)
        text = flattened(method)
        for token in tokens:
            assert token in text, (cname, token)
    print("PASS: exact four Primordial owner methods, five typed consumers, "
          "eight resource identities; PARTIAL NO_MUTATION")
    print("REPORT_SHA256", report_hash)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    verify(args.report, args.manifest)
