#!/usr/bin/env python3
"""Fail-closed structural checks for PrimordialArmorItem publisher discovery.

This first-stage checker deliberately does NOT approve per-item static
contracts, runtime protection, hooks, or physical QA. Exact method seals
are added only after the publisher report is physically generated.
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
        assert k not in out, "duplicate JSON key " + k
        out[k] = v
    return out


def verify(path: Path):
    raw = path.read_bytes()
    assert 0 < len(raw) <= 16_000_000, "report exceeds bounded size"
    d = json.loads(raw, object_pairs_hook=unique_pairs)
    assert d["schema_version"] == 1
    assert d["scope"] == "PRIMORDIAL_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert d["artifact"] == {
        "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
        "version": "1.0.10",
        "sha1": SHA1,
        "sha256": SHA256,
        "size_bytes": SIZE,
        "installed_dump_comparison": "NOT_VERIFIED",
    }
    assert d["owner"] == OWNER
    assert tuple(d["registry_candidates_not_individually_certified"]) == NAMES
    assert d["source_revision_parity"] == "NOT_ASSUMED"
    assert d["other_consumers_complete"] is False
    assert d["provider_universe_closed"] is False
    assert d["static_contract"] == "NOT_CERTIFIED"
    assert d["semantic_magic_roots_certified_delta"] == 0
    assert d["mutating_hook"] == "NOT_VERIFIED"
    assert d["physical_qa"] == "NOT_TESTED"
    assert d["mutation"] == "NO_MUTATION"
    native = d["native"]
    assert native["class_entries_scanned"] == 1555
    assert set(native["targets"]) == {OWNER}
    assert "filename_matched_resources" not in native
    item = native["targets"][OWNER]
    assert len(item["class_sha256"]) == 64
    assert item["methods"] and len(item["methods"]) == sum(
        "code_sha256" in m for m in item["declarations"])
    assert isinstance(item["fields"], list)
    assert isinstance(item["consumers"], dict)
    assert any(c.endswith("/ACItemRegistry") for c in item["consumers"])
    for method in item["methods"]:
        assert method["instruction_count"] == len(method["instructions"])
        assert len(method["instruction_sha256"]) == 64
        assert method["declaration"]["name"] and method["declaration"]["descriptor"]
    res = d["filename_matched_resource_hashes"]
    assert isinstance(res, dict) and len(res) <= 100
    for name, info in res.items():
        assert name.endswith(".json")
        assert any(term in name.lower() for term in (*NAMES, "primordial_armor"))
        assert set(info) == {"sha256", "size"}
        assert isinstance(info["size"], int) and info["size"] > 0
        assert len(info["sha256"]) == 64
    print("PASS: pinned PrimordialArmorItem publisher and bounded native discovery only")
    print("REPORT_SHA256", hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    verify(a.report)
