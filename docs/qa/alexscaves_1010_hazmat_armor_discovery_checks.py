#!/usr/bin/env python3
"""Fail-closed structural validation for a *discovery-only* Hazmat report.

This deliberately does not certify item effects, hooks, the full radiation
call graph, or physical gameplay. A later exact method seal is still required.
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
        if key in result:
            raise AssertionError("duplicate report key: " + key)
        result[key] = value
    return result


def check(path: Path) -> None:
    raw = path.read_bytes()
    assert len(raw) < 16_000_000, "report size budget exceeded"
    obj = json.loads(raw, object_pairs_hook=pairs_unique)
    assert obj["schema_version"] == 1
    assert obj["scope"] == "HAZMAT_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert obj["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1,
        "sha256": SHA256, "size_bytes": SIZE,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert obj["owner"] == OWNER
    assert tuple(obj["registry_candidates_not_individually_certified"]) == NAMES
    for key, expected in {
        "other_radiation_consumers_complete": False,
        "engine_and_external_armor_effects_verified": False,
        "source_revision_parity": "NOT_ASSUMED",
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert obj[key] == expected, key
    native = obj["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    item = native["targets"][OWNER]
    assert len(item["class_sha256"]) == 64
    assert item["fields"] is not None
    assert item["methods"], "empty owner body list"
    assert len(item["methods"]) == sum(
        "code_sha256" in entry for entry in item["declarations"]
    )
    seen = set()
    for method in item["methods"]:
        d = method["declaration"]
        signature = (d["name"], d["descriptor"])
        assert signature not in seen, signature
        seen.add(signature)
        assert method["instruction_count"] == len(method["instructions"])
        assert len(method["instruction_sha256"]) == 64
    assert any(name.endswith("/ACItemRegistry") for name in item["consumers"])
    hashes = obj["filename_matched_resource_hashes"]
    assert isinstance(hashes, dict)
    for name, record in hashes.items():
        assert name.endswith(".json") and "hazmat" in name.lower()
        assert set(record) == {"sha256", "size"}
        assert len(record["sha256"]) == 64 and record["size"] > 0
    print("PASS: pinned JAR, complete native Hazmat owner method roster, "
          "typed registration, resource hashes; DISCOVERY ONLY")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    check(args.report)
