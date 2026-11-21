#!/usr/bin/env python3
"""Structural fail-closed gate for RemoteDetonatorItem publisher JAR discovery.

This pre-seal validator does NOT certify method behavior. A later per-object
manifest must pin all relevant method and consumer hashes before any card
can receive even a partial technical interpretation.
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


def reject_duplicate_keys(pairs):
    out = {}
    for k, v in pairs:
        assert k not in out, "duplicate JSON key: " + k
        out[k] = v
    return out


def check(path: Path) -> None:
    raw = path.read_bytes()
    assert 0 < len(raw) <= 16_000_000, "discovery report size outside bounds"
    report = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
    assert report["schema_version"] == 1
    assert report["scope"] == "REMOTE_DETONATOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert report["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1,
        "sha256": SHA256, "size_bytes": SIZE,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert report["owner"] == OWNER
    for k, v in {
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
        assert report[k] == v, k

    native = report["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}, "unexpected other native targets"
    assert "filename_matched_resources" not in native
    owner = native["targets"][OWNER]
    assert len(owner["class_sha256"]) == 64
    assert owner["hierarchy"]["parent"], "missing declared superclass"
    assert isinstance(owner["fields"], list)
    assert len(owner["methods"]) > 0
    assert len(owner["methods"]) == sum(
        "code_sha256" in value for value in owner["declarations"]
    ), "missing executable methods"
    assert any(name.endswith("/ACItemRegistry") for name in owner["consumers"])
    identities = set()
    for method in owner["methods"]:
        d = method["declaration"]
        identity = d["name"], d["descriptor"]
        assert identity not in identities, "duplicate method identity"
        identities.add(identity)
        assert len(method["instruction_sha256"]) == 64
        assert method["instruction_count"] == len(method["instructions"])
    for name, consumer in owner["consumers"].items():
        assert len(consumer["class_sha256"]) == 64, name
        assert isinstance(consumer["sites"], list), name
        for entry in consumer["bodies"]:
            assert len(entry["instruction_sha256"]) == 64
            assert entry["instruction_count"] == len(entry["instructions"])
    resources = report["filename_matched_resource_hashes"]
    assert isinstance(resources, dict) and len(resources) <= 200
    for name, proof in resources.items():
        assert name.endswith(".json") and any(term in name.lower() for term in ("remote_detonator", "remote_detonation", "detonator", "remote_control"))
        assert set(proof) == {"sha256", "size"}
        assert len(proof["sha256"]) == 64
        assert type(proof["size"]) is int and proof["size"] > 0
    print("PASS: exact publisher identity, RemoteDetonator owner, "
          "bounded method/consumer/resource census, FAIL-CLOSED")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    check(args.report)
