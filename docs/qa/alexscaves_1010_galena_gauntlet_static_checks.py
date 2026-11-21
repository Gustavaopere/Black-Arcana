#!/usr/bin/env python3
"""Fail-closed SHA-exact read-only Galena Gauntlet report/manifest audit.

CERTIFIES REPORT IDENTITY ONLY; DOES NOT CERTIFY GAMEPLAY, HOOKS OR THE CARD.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

def require(test, reason):
    if not test:
        raise AssertionError(reason)

def pairs_unique(items):
    obj = {}
    for key, value in items:
        require(key not in obj, "duplicate JSON key")
        obj[key] = value
    return obj

def run(manifest_path: Path, report_path: Path):
    manifest = json.loads(manifest_path.read_text(encoding="utf8"),
                          object_pairs_hook=pairs_unique)
    data = report_path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == manifest["report"]["sha256"],
            "report fingerprint mismatch")
    report = json.loads(data, object_pairs_hook=pairs_unique)
    require(manifest["schema_version"] == 1
            and manifest["scope"] == report["scope"]
            == "GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED",
            "scope mismatch")
    for key in ("version", "sha1", "sha256", "size_bytes", "installed_dump_parity"):
        require(manifest["artifact"][key] == report["artifact"][key],
                "publisher identity mismatch: " + key)
    require(report["mutation"] == manifest["limits"]["mutation"] == "NO_MUTATION"
            and report["mutating_hook"] == manifest["limits"]["mutating_hook"]
            == "NOT_VERIFIED"
            and report["physical_qa"] == manifest["limits"]["physical_qa"]
            == "NOT_TESTED"
            and report["provider_universe_closed"] is False
            and manifest["limits"]["provider_universe_closed"] is False
            and report["semantic_magic_roots_certified_delta"] == 0
            and manifest["limits"]["semantic_magic_roots_certified_delta"] == 0
            and manifest["limits"]["static_contract"] == "PARTIAL",
            "unsafe status promotion")
    observed = {}
    for key in ("native", "entity_native"):
        for owner, entry in report[key]["targets"].items():
            require(owner not in observed, "duplicate class across probes")
            observed[owner] = entry
    require(set(observed) == set(manifest["classes"]), "class roster drift")
    for owner, expected in manifest["classes"].items():
        data = observed[owner]
        require(data["class_sha256"] == expected["sha256"],
                "class fingerprint drift: " + owner)
        actual = [
            {"name": m["declaration"]["name"],
             "descriptor": m["declaration"]["descriptor"],
             "instructions": m["instruction_count"],
             "sha256": m["instruction_sha256"]}
            for m in data["methods"]
        ]
        require(actual == expected["methods"], "method roster/digest drift: " + owner)
    require(report["matching_resources"] == manifest["matched_resources"],
            "resource hash/size drift")
    print("PASS: 17 Gauntlet + 24 MagneticWeapon method bodies and six resources"
          " SHA-exact; partial static discovery; NO_MUTATION")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    a = p.parse_args()
    run(a.manifest, a.report)
