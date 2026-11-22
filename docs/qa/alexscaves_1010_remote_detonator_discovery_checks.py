#!/usr/bin/env python3
"""Fail-closed SHA-exact RemoteDetonatorItem 1.0.10 discovery verifier.

Verify original read-only publisher report against pinned manifest and
critical causal bytecode sites. This is NOT a runtime authorization,
world-safety signoff, mutating-hook certification or gameplay QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/RemoteDetonatorItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314


def reject_duplicates(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, "duplicate JSON key: " + key
        out[key] = value
    return out


def read_json(path: Path, limit: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= limit, "report size outside bounds"
    return json.loads(raw, object_pairs_hook=reject_duplicates), hashlib.sha256(raw).hexdigest()


def method_seal(method):
    d = method["declaration"]
    return {"name": d["name"], "descriptor": d["descriptor"],
            "instruction_count": method["instruction_count"],
            "instruction_sha256": method["instruction_sha256"]}


def instruction_text(method):
    return " ".join(row["opcode"] + " " + row["operand"] +
                    " " + row["symbol"] for row in method["instructions"])


def check(report_path: Path, manifest_path: Path):
    d, raw_hash = read_json(report_path, 16_000_000)
    m, _ = read_json(manifest_path, 100_000)
    assert raw_hash == m["report"]["sha256"], "native report hash drift"
    assert report_path.stat().st_size == m["report"]["uncompressed_bytes"]
    assert d["schema_version"] == m["schema_version"] == 1
    assert d["scope"] == m["scope"] == "REMOTE_DETONATOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    artifact = {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
        "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert d["artifact"] == m["artifact"] == artifact
    assert d["owner"] == m["owner"] == OWNER
    for key, expected in {
        "resource_census_limit": "FILENAME_MATCHES_ONLY",
        "registry_identity": "NOT_PROVEN_BY_FILENAME_ONLY",
        "typed_consumer_scan": "PUBLISHER_CLASSFILES_ONLY",
        "other_consumers_complete": False,
        "source_revision_parity": "NOT_ASSUMED",
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert d[key] == expected, key
    assert m["limits"] == {
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "source_revision_parity": "NOT_ASSUMED",
        "other_consumers_complete": False,
        "world_safety": "BLOCKED_PENDING_PLATFORM_AND_TARGET_CONSUMERS",
        "registry_bootstrap": "NOT_TESTED", "magic_roots_added": 0,
    }
    n = d["native"]
    assert n["class_entries_scanned"] == 1555
    assert set(n["targets"]) == {OWNER}
    assert "filename_matched_resources" not in n
    o = n["targets"][OWNER]
    seal = m["owner_class"]
    assert o["class_sha256"] == seal["sha256"]
    assert o["hierarchy"]["parent"] == seal["parent"]
    assert o["hierarchy"]["interfaces"] == seal["interfaces"]
    assert o["fields"] == [] and seal["declared_field_count"] == 0
    assert o["descendants"] == [] and o["in_jar_ancestors"] == []
    assert len(o["declarations"]) == seal["method_count"] == 11
    assert len(o["methods"]) == 11
    assert len(o["methods"]) == sum("code_sha256" in x for x in o["declarations"])
    assert [method_seal(v) for v in o["methods"]] == seal["methods"]
    for method in o["methods"]:
        assert method["instruction_count"] == len(method["instructions"])
    assert set(o["consumers"]) == set(m["consumers"])
    for name, contract in m["consumers"].items():
        actual = o["consumers"][name]
        assert actual["class_sha256"] == contract["sha256"]
        assert len(actual["sites"]) == contract["typed_sites"]
        if contract["methods"]:
            assert [method_seal(v) for v in actual["bodies"]] == contract["methods"]
        else:
            assert name == OWNER
    assert d["filename_matched_resource_hashes"] == m["filename_matched_resource_hashes"]
    assert len(m["filename_matched_resource_hashes"]) == 5
    for p, rec in m["filename_matched_resource_hashes"].items():
        assert p.endswith(".json") and "remote" in p
        assert len(rec["sha256"]) == 64 and rec["size"] > 0

    contract = m["native_constraints"]
    assert contract["registry_item"] == "alexscaves:remote_detonator"
    assert contract["storage_keys"] == ["BombPos", "BombDimension", "BombTracked"]
    assert contract["active_check"] == "BombDimension OR BombPos"
    assert contract["passive_validation_period"] == "(entity.tickCount+entity.getId())%20==0 when world and dimension match"
    assert contract["load_chunks_around"] == {
        "for_range": ["-1..1", "-1..1"],
        "force_chunk_requested_count": 9,
        "force_chunk_flag": True,
        "release_found_in_owner_use": False,
    }
    assert contract["possible_world_mismatch"].startswith("use invokes Level.setBlockAndUpdate")
    assert contract["use_attempts_cross_dimension_lookup"] is True
    assert contract["direct_damage"] == "NOT_IN_OWNER"
    assert contract["explosion_direct"] == "NOT_IN_OWNER"
    methods = {v["declaration"]["name"]: instruction_text(v) for v in o["methods"]}
    anchors = {
        "<init>": ["stacksTo", "Item$Properties"],
        "acInventoryTick": ["isClientSide", "isActive", "BombTracked",
            "getBombDimension", "tickCount", "getId", "bipush 20",
            "isLoaded", "REMOTE_DETONATOR_ACTIVATES", "isInWorldBounds",
            "BombPos", "BombDimension", "ACCompat.setTag"],
        "addBombTags": ["BombPos", "putBlockPos", "RESOURCE_KEY_CODEC",
            "BombTracked", "putBoolean"],
        "getBombDimension": ["BombDimension", "Codec.parse", "DataResult.result"],
        "getBombPosition": ["BombPos", "BombDimension", "GlobalPos.of"],
        "isActive": ["BombPos", "BombDimension", "CompoundTag.contains"],
        "loadChunksAround": ["iconst_m1", "iconst_1", "forceChunk",
            "ACCompat.chunkX", "ACCompat.chunkZ"],
        "use": ["getBombPosition", "isClientSide", "ServerLevel",
            "MinecraftServer.getLevel", "loadChunksAround", "iconst_1",
            "REMOTE_DETONATOR_ACTIVATES", "onCaughtFire",
            "double 1000.0d", "REMOTE_DETONATION",
            "BombDimension", "BombPos", "Level.setBlockAndUpdate"],
        "useOn": ["REMOTE_DETONATOR_ACTIVATES", "LODESTONE_COMPASS_LOCK",
            "getAbilities", "instabuild", "getCount", "addBombTags",
            "ItemStack.shrink", "Inventory.add", "Player.drop",
            "ACCompat.sidedSuccess"],
    }
    for name, markers in anchors.items():
        text = methods[name]
        for marker in markers:
            assert marker in text, (name, marker)
    factory = o["consumers"][
        "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
    ]["bodies"][0]
    assert "RemoteDetonatorItem" in instruction_text(factory)
    predicate = o["consumers"][
        "com/github/alexmodguy/alexscaves/client/render/item/ACItemPredicates"
    ]["bodies"][0]
    assert "RemoteDetonatorItem.isActive" in instruction_text(predicate)

    print("PASS: SHA-pinned RemoteDetonatorItem: 11 methods, typed graph, "
          "NBT/chunk/world-write pivot, 5 resources; DISCOVERY ONLY")
    print("REPORT_SHA256", raw_hash)
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    check(args.report, args.manifest)
