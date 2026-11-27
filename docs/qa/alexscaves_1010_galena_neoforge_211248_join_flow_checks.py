#!/usr/bin/env python3
"""SHA-exact NeoForge 21.1.248 Galena join-flow PATCH evidence verifier.

Rejects report/status/line forgeries even when only the outer report digest
is deliberately bypassed in adversarial simulations. No runtime or hook is
certified. Does not distribute third-party Java bodies.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

REPORT_SHA = "39605a4b034b7e43cc301111b4d7352aad67b5a1dd4cc78cefc6b9f8b31bcce7"
REPORT_BYTES = 8996
UPSTREAM_SHA = "9278d08154a82927391ed5257481f56d6d0fcb147822c6a79ec9b5129799e79a"
REPORT_SCOPE = "GALENA_1010_NEOFORGE_211248_ENTITY_JOIN_CAUSAL_PATCH_DISCOVERY_ONLY"
SEAL_SCOPE = "GALENA_1010_NEOFORGE_211248_ENTITY_JOIN_CAUSAL_PATCH_SEAL_ONLY"
CLASSES = ("ServerLevel", "PersistentEntitySectionManager")
ROLE_KINDS = {
    "ServerLevel": {
        "player_method": "CONTEXT",
        "player_join_cancel_void_return": "ADD",
        "player_registration_bypasses_second_event": "ADD",
        "player_on_added": "ADD",
        "generic_add_entity_method": "CONTEXT",
        "generic_manager_boolean_branch": "ADD",
        "generic_on_added_if_manager_true": "ADD",
        "generic_accepted_true": "ADD",
        "generic_rejected_false": "ADD",
    },
    "PersistentEntitySectionManager": {
        "bypass_method": "ADD",
        "bypass_direct_registration": "ADD",
        "normal_admission_method": "CONTEXT",
        "normal_entity_join_cancellation_false": "ADD",
        "forward_to_uuid_registration": "ADD",
        "registration_without_event": "ADD",
        "uuid_guard_after_cancellation": "CONTEXT",
    },
}
PATCH_PATHS = {
    "ServerLevel":
        "patches/net/minecraft/server/level/ServerLevel.java.patch",
    "PersistentEntitySectionManager":
        "patches/net/minecraft/world/level/entity/PersistentEntitySectionManager.java.patch",
}

def need(ok, label):
    if not ok:
        raise ValueError(label)

def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key " + key)
        out[key] = value
    return out

def load(path, limit):
    raw = Path(path).read_bytes()
    need(0 < len(raw) <= limit, "empty/oversized evidence")
    return json.loads(raw, object_pairs_hook=unique), raw

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def validate(report, seal, *, raw=None, strict=True):
    need(report["schema"] == seal["schema"] == 1, "schema mismatch")
    need(report["scope"] == REPORT_SCOPE and seal["scope"] == SEAL_SCOPE,
         "scope mismatch")
    provenance = seal["provenance"]
    need(provenance["report_sha256"] == REPORT_SHA and
         provenance["report_bytes"] == REPORT_BYTES,
         "source report hash altered")
    if strict:
        need(raw is not None and len(raw) == REPORT_BYTES and
             digest(raw) == REPORT_SHA, "report exact bytes/hash drift")
    need(provenance["official_maven"] ==
         "https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.248/neoforge-21.1.248-userdev.jar"
         and provenance["neoforge"] == "21.1.248"
         and provenance["minecraft"] == "1.21.1"
         and provenance["userdev_filename"] == "neoforge-21.1.248-userdev.jar"
         and provenance["userdev_bytes"] == 3983248
         and provenance["userdev_sha256"] == UPSTREAM_SHA,
         "upstream identity")
    need(provenance["first_successful_run_id"] == 45208324051 and
         provenance["first_successful_job_id"] == 137810026496 and
         provenance["source_head_sha"] ==
         "75f565da91bb88b9b0ebfa223335a2967306a5a2",
         "source workflow provenance")
    need(provenance["alexscaves_provider_sha256"] ==
         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
         "provider source identity")
    need(report["upstream"] == {
        "version": "21.1.248",
        "userdev": "neoforge-21.1.248-userdev.jar",
        "bytes": 3983248, "sha256": UPSTREAM_SHA,
    }, "report engine version")
    need(set(report["patches"]) == set(seal["classes"]) == set(CLASSES),
         "patch owner roster")
    number = 0
    for name in CLASSES:
        record = report["patches"][name]
        pin = seal["classes"][name]
        need(record["patch_sha256"] == pin["patch_sha256"] and
             re.fullmatch("[a-f0-9]{64}", record["patch_sha256"]),
             "patch fingerprint " + name)
        need(record["flow"] == pin["flow"], "semantic markers " + name)
        got, expected = record["anchors"], pin["anchors"]
        need(len(got) == len(expected) == len(ROLE_KINDS[name]),
             "anchor roster size")
        need([x["role"] for x in got] == list(ROLE_KINDS[name]),
             "anchor order/role drift")
        positions = []
        for row, ref in zip(got, expected):
            for key in ("role", "line", "hunk", "line_sha256"):
                need(row[key] == ref[key], "forged exact anchor " + name + "." + key)
            need(row["kind"] == ROLE_KINDS[name][row["role"]] and
                 0 < row["line"] <= 1000 and
                 0 < row["hunk"] <= 300 and
                 isinstance(row["bytes"], int) and
                 0 < row["bytes"] <= 10000 and
                 re.fullmatch("[a-f0-9]{64}", row["line_sha256"]),
                 "invalid type/shape of line anchor " + name)
            positions.append(row["line"])
        need(positions == sorted(set(positions)), "anchor order " + name)
        number += len(got)
    need(number == 16, "unverified method anchors")
    loads = report["patches"]["PersistentEntitySectionManager"]["load_paths"]
    need(len(loads) == 3, "incomplete load path list")
    expected_paths = seal["classes"]["PersistentEntitySectionManager"]["load_paths"]
    need([{k:x[k] for k in ("method", "disk_flag",
                            "boolean_return_checked_before_on_added")}
          for x in loads] == expected_paths, "incorrect load routing")
    for p in loads:
        a = p["anchors"]
        need(len(a) == 3 and
             [x["role"] for x in a] == [
                 "load_entrypoint", "bare_add_entity_call",
                 "notification_after_call"] and
             [x["kind"] for x in a] == ["CONTEXT", "ADD", "ADD"] and
             a[1]["line"] + 1 == a[2]["line"] and
             a[1]["hunk"] == a[2]["hunk"] and
             [x["line"] for x in a] == sorted(set(x["line"] for x in a)) and
             all(re.fullmatch("[a-f0-9]{64}", x["line_sha256"]) for x in a) and
             all(isinstance(x["bytes"], int) and 0 < x["bytes"] <= 10000 for x in a),
             "malformed load-path anchors")
    limit = report["limits"]
    need(limit == {
        "installed_runtime": "NOT_VERIFIED",
        "transformed_minecraft_bytecode": "NOT_VERIFIED",
        "merged_patch_runtime_equivalence": False,
        "all_join_callsites_exhausted": False,
        "galena_spawn_outcome": "NOT_VERIFIED",
        "stack_restoration": "NOT_VERIFIED",
        "world_protection": "NOT_VERIFIED",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }, "unsupported runtime claim")
    need(all(seal["states"][k] == limit[k] for k in seal["states"]) and
         set(seal["states"]) == {
             "static_contract", "mutating_hook", "physical_qa", "mutation",
             "provider_universe_closed", "semantic_magic_roots_delta"
         }, "unsafe seal state")
    return number, len(loads)

def adversarial(report, seal):
    cases = []
    def mutate(label, path, new):
        r = copy.deepcopy(report)
        cur = r
        for part in path[:-1]:
            cur = cur[part]
        cur[path[-1]] = new
        cases.append((label, r, seal))
    for name in CLASSES:
        for i, a in enumerate(report["patches"][name]["anchors"]):
            mutate("forged anchor " + name + str(i),
                   ["patches", name, "anchors", i, "line_sha256"],
                   "0" * 64 if a["line_sha256"] != "0"*64 else "1"*64)
        mutate("forged patch digest " + name,
               ["patches", name, "patch_sha256"], "0"*64)
    for key, new in (
        ("installed_runtime", "VERIFIED"),
        ("transformed_minecraft_bytecode", "VERIFIED"),
        ("merged_patch_runtime_equivalence", True),
        ("all_join_callsites_exhausted", True),
        ("galena_spawn_outcome", "VERIFIED"),
        ("stack_restoration", "VERIFIED"),
        ("world_protection", "VERIFIED"),
        ("static_contract", "CERTIFIED"),
        ("mutating_hook", "VERIFIED"),
        ("physical_qa", "PASSED"),
        ("mutation", "MUTATION"),
        ("provider_universe_closed", True),
        ("semantic_magic_roots_delta", 1),
    ):
        mutate("unsafe promotion " + key, ["limits", key], new)
    for i in range(3):
        mutate("fake load callback tested " + str(i),
               ["patches", "PersistentEntitySectionManager", "load_paths",
                i, "boolean_return_checked_before_on_added"], True)
    mutate("wrong engine", ["upstream", "version"], "21.1.250")
    mutate("wrong event order",
           ["patches", "ServerLevel", "flow",
            "normal_entity_on_added_only_if_manager_true"], False)
    mutate("forged manager admission",
           ["patches", "PersistentEntitySectionManager", "flow",
            "normal_entity_join_cancel_return_false"], False)
    for label, r, s in cases:
        try:
            validate(r, s, strict=False)
        except (ValueError, KeyError, IndexError, TypeError):
            continue
        raise AssertionError("forgery accepted: " + label)
    need(len(cases) >= 35, "adversarial coverage insufficient")
    return len(cases)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--adversarial", action="store_true")
    a = p.parse_args()
    report, raw = load(a.report, 50000)
    seal, _ = load(a.manifest, 50000)
    count, paths = validate(report, seal, raw=raw)
    print("EXACT_REPORT_SHA256", digest(raw),
          "BYTES", len(raw), "METHOD_ANCHORS", count,
          "LOAD_PATHS", paths)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED", adversarial(report, seal))
    print("OK: read-only patch flow verified; NO_MUTATION/NOT_CERTIFIED")

if __name__ == "__main__":
    main()
