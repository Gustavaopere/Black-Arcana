#!/usr/bin/env python3
"""Fail-closed identity/structure gate for read-only ResistorShieldItem census.

This gate is a preliminary discovery test, not a SHA-pinned per-object
static certificate. A subsequent per-method manifestation is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OWNER = "com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem"
SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
TERMS = ("resistor_shield", "resistor", "resistance_shield")


def unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, ("duplicate JSON key", key)
        out[key] = value
    return out


def check(path: Path) -> None:
    raw = path.read_bytes()
    assert 0 < len(raw) <= 16_000_000, "report bounds"
    a = json.loads(raw, object_pairs_hook=unique)
    assert a["schema_version"] == 1
    assert a["scope"] == "RESISTOR_SHIELD_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert a["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
        "size_bytes": SIZE, "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert a["owner"] == OWNER
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
        assert a[key] == expected, key
    native = a["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    cls = native["targets"][OWNER]
    assert isinstance(cls["class_sha256"], str) and len(cls["class_sha256"]) == 64
    assert isinstance(cls["hierarchy"]["parent"], str)
    assert isinstance(cls["fields"], list)
    assert len(cls["methods"]) <= 60
    assert len(cls["methods"]) == sum("code_sha256" in x for x in cls["declarations"])
    ids = set()
    for method in cls["methods"]:
        d = method["declaration"]
        ident = d["name"], d["descriptor"]
        assert ident not in ids, ("duplicate method", ident)
        ids.add(ident)
        assert len(method["instruction_sha256"]) == 64
        assert method["instruction_count"] == len(method["instructions"])
    assert len(cls["consumers"]) <= 120
    assert any(name.endswith("/ACItemRegistry") for name in cls["consumers"])
    for name, info in cls["consumers"].items():
        assert isinstance(name, str) and len(info["class_sha256"]) == 64
        assert isinstance(info["sites"], list)
        for body in info["bodies"]:
            assert body["instruction_count"] == len(body["instructions"])
            assert len(body["instruction_sha256"]) == 64
    resources = a["filename_matched_resource_hashes"]
    assert isinstance(resources, dict) and len(resources) <= 200
    for path, proof in resources.items():
        assert path.endswith(".json") and any(t in path.lower() for t in TERMS)
        assert set(proof) == {"size", "sha256"}
        assert type(proof["size"]) is int and proof["size"] > 0
        assert len(proof["sha256"]) == 64
    print("PASS: pinned publisher identity, exact item class census and typed consumers")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    check(args.report)
