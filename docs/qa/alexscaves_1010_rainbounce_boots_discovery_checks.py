#!/usr/bin/env python3
"""Fail-closed structural gate for SHA-exact RainbounceBootsItem discovery.

This preliminary gate is not a native semantic contract: method-specific
hashes and consumers require a separately pinned seal after inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314


def unique_pairs(pairs):
    result = {}
    for key, val in pairs:
        assert key not in result, "duplicate JSON key: " + key
        result[key] = val
    return result


def check(path: Path) -> None:
    raw = path.read_bytes()
    assert 0 < len(raw) <= 16_000_000, "unexpected report size"
    d = json.loads(raw, object_pairs_hook=unique_pairs)
    assert d["schema_version"] == 1
    assert d["scope"] == "RAINBOUNCE_BOOTS_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert d["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
        "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert d["owner"] == OWNER
    assert d["registry_candidate_not_individually_certified"] == "rainbounce_boots"
    assert d["source_revision_parity"] == "NOT_ASSUMED"
    for name, expected in {
        "other_consumers_complete": False,
        "provider_universe_closed": False,
        "static_contract": "NOT_CERTIFIED",
        "semantic_magic_roots_certified_delta": 0,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }.items():
        assert d[name] == expected, name

    native = d["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    obj = native["targets"][OWNER]
    assert len(obj["class_sha256"]) == 64
    assert obj["methods"]
    assert len(obj["methods"]) == sum(
        "code_sha256" in method for method in obj["declarations"])
    assert isinstance(obj["consumers"], dict)
    assert any(c.endswith("/ACItemRegistry") for c in obj["consumers"])
    fingerprints = set()
    for method in obj["methods"]:
        descriptor = method["declaration"]
        identity = descriptor["name"], descriptor["descriptor"]
        assert identity not in fingerprints, "duplicate method identity"
        fingerprints.add(identity)
        assert method["instruction_count"] == len(method["instructions"])
        assert len(method["instruction_sha256"]) == 64
    files = d["filename_matched_resource_hashes"]
    assert isinstance(files, dict) and 1 <= len(files) <= 100
    for name, record in files.items():
        assert name.endswith(".json") and "rainbounce" in name.lower()
        assert set(record) == {"sha256", "size"}
        assert len(record["sha256"]) == 64
        assert type(record["size"]) is int and record["size"] > 0
    print("PASS: pinned publisher; executable Rainbounce owner; typed registry;"
          " resource hash census — DISCOVERY ONLY")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    check(args.report)
