#!/usr/bin/env python3
"""SHA-exact read-only boundary seal for Remote Detonator in publisher 1.0.10.

This verifies binary dispatch into the NeoForge TicketController and
BlockState.onCaughtFire, NOT runtime effects, tickets, safety or mod hooks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, "duplicate key: " + key
        out[key] = value
    return out


def read(path: Path, cap: int):
    raw = path.read_bytes()
    assert 0 < len(raw) <= cap, "bounds"
    return json.loads(raw, object_pairs_hook=unique), len(raw), hashlib.sha256(raw).hexdigest()


def seal(method):
    decl = method["declaration"]
    return {
        "name": decl["name"],
        "descriptor": decl["descriptor"],
        "instruction_count": method["instruction_count"],
        "instruction_sha256": method["instruction_sha256"],
    }


def at(method, offset):
    entries = [ins for ins in method["instructions"] if ins["offset"] == offset]
    assert len(entries) == 1, "offset absent or ambiguous"
    return entries[0]


def check(report_path: Path, manifest_path: Path):
    report, size, digest = read(report_path, 250_000)
    manifest, _, _ = read(manifest_path, 100_000)
    assert size == manifest["report"]["uncompressed_bytes"] == 10014
    assert digest == manifest["report"]["sha256"] == (
        "9187ac7516c239f2177481121b6cc6d8baa3574ae534258bcdcffc231aac3ee6"
    )
    assert report["schema_version"] == manifest["schema_version"] == 1
    assert report["scope"] == "REMOTE_DETONATOR_BOUNDARY_DISCOVERY_NOT_CERTIFIED"
    assert manifest["scope"] == (
        "REMOTE_DETONATOR_BOUNDARIES_SHA_EXACT_DISCOVERY_NOT_WORLD_SAFETY_CERTIFICATION"
    )
    publisher = {
        "sha1": "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570",
        "sha256": "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
        "size_bytes": 75279314,
    }
    assert report["artifact"] == publisher
    assert manifest["artifact"] == {**publisher, "version": "1.0.10"}
    for key, expected in {
        "platform_effective_implementation": "NOT_VERIFIED",
        "ticket_lifetime": "NOT_VERIFIED",
        "world_safety": "BLOCKED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert report[key] == expected, key
    for key, expected in {
        "boundary_status": "READ_ONLY_BINARY_DISPATCH_CONFIRMED",
        "engine_effect_acceptance": "NOT_VERIFIED",
        "world_safety": "BLOCKED",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert manifest[key] == expected, key

    assert set(report["selected"]) == set(manifest["owners"])
    for name, expected in manifest["owners"].items():
        item = report["selected"][name]
        assert item["class_sha256"] == expected["class_sha256"]
        assert len(item["methods"]) == len(expected["methods"])
        assert [seal(m) for m in item["methods"]] == expected["methods"]
        for method in item["methods"]:
            assert method["instruction_count"] == len(method["instructions"])

    platform = report["selected"][
        "com/github/alexmodguy/alexscaves/server/misc/ACPlatform"
    ]["methods"]
    assert len(platform) == 2
    for method in platform:
        instructions = method["instructions"]
        assert "ticketController" in at(method, 0)["symbol"]
        assert at(method, 3)["opcode"] == "ifnull"
        assert at(method, 3)["operand"] == "24"
        assert "TicketController.forceChunk" in at(method, 20)["symbol"]
        assert at(method, 23)["opcode"] == "pop"
        assert at(method, 24)["opcode"] == "return"
    caught = report["selected"][
        "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
    ]["methods"][0]
    assert "BlockState.onCaughtFire" in at(caught, 6)["symbol"]
    assert at(caught, 9)["opcode"] == "return"

    print("PASS: SHA-exact TicketController delegation, nullable controller and "
          "discarded boolean, BlockState.onCaughtFire direct dispatch")
    print("REPORT_SHA256", digest)
    print("NO_MUTATION WORLD_SAFETY_BLOCKED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    check(args.report, args.manifest)
