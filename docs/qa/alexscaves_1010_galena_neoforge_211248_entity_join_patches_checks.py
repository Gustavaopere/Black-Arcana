#!/usr/bin/env python3
"""Publisher-SHA-exact, fail-closed Galena NeoForge 21.1.248 patch verifier.

Seals metadata and hashed symbol locations, never reconstructed Minecraft
or provider behavior. Adversarial tests deliberately bypass only the outer
report hash; independently committed per-line hashes and rosters must reject.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

REPORT_SHA = "a1a2df01b3537a534d26d9121fbd0103368f82135c1b291c3843a89aaad12114"
REPORT_BYTES = 7298
USERDEV_SHA = "9278d08154a82927391ed5257481f56d6d0fcb147822c6a79ec9b5129799e79a"
DISCOVERY_SCOPE = "GALENA_NEOFORGE_211248_ENTITY_JOIN_PATCH_DISCOVERY_ONLY"
SEAL_SCOPE = "GALENA_NEOFORGE_211248_ENTITY_JOIN_PATCH_SEAL_ONLY"
PREFIX = "patches/net/minecraft/"
PATHS = {
    "ServerLevel": PREFIX + "server/level/ServerLevel.java.patch",
    "PersistentEntitySectionManager": PREFIX +
    "world/level/entity/PersistentEntitySectionManager.java.patch",
    "Level": PREFIX + "world/level/Level.java.patch",
    "LevelWriter": PREFIX + "world/level/LevelWriter.java.patch",
}
WORDS = {
    "EntityJoinLevelEvent", "addFreshEntity", "addNewEntity",
    "isCanceled", "EVENT_BUS", "PersistentEntitySectionManager", "LevelWriter",
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load(path: Path, limit: int):
    raw = path.read_bytes()
    need(0 < len(raw) <= limit, "oversized or empty evidence")
    return json.loads(raw, object_pairs_hook=unique), raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(report, seal, *, raw=None, strict=True):
    need(report["schema"] == seal["schema"] == 1, "schema")
    need(report["scope"] == DISCOVERY_SCOPE and
         seal["scope"] == SEAL_SCOPE, "scope")
    p = seal["provenance"]
    need(p["report_sha256"] == REPORT_SHA and
         p["report_bytes"] == REPORT_BYTES, "report pin")
    if strict:
        need(raw is not None and len(raw) == REPORT_BYTES and
             digest(raw) == REPORT_SHA, "report bytes or hash drift")
    need(p["userdev_sha256"] == USERDEV_SHA and
         p["userdev_bytes"] == 3983248 and
         p["zip_entries"] == 963 and
         p["patch_count"] == 753 and
         p["patch_roster_sha256"] ==
         "22046c708c5774e479f335fcef95a0c526670fbc9dde01fc29281c94102a640f",
         "official publisher archive reference")
    need(p["neoforge"] == "21.1.248" and p["minecraft"] == "1.21.1" and
         p["userdev_filename"] == "neoforge-21.1.248-userdev.jar" and
         p["official_maven"] ==
         "https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.248/neoforge-21.1.248-userdev.jar",
         "published coordinates")
    need(p["initial_discovery_run_id"] == 45186275044 and
         p["initial_discovery_job_id"] == 137732591187 and
         p["observed_branch_sha"] ==
         "01bfa33698acbb1918f357a3f19ebb1661a51367",
         "observational provenance")
    need(p["alexscaves_publisher_sha256"] ==
         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
         "provider publisher fingerprint")
    pub = report["publisher"]
    need(pub == {
        "artifact": "net.neoforged:neoforge:21.1.248:userdev",
        "official_maven": p["official_maven"],
        "filename": p["userdev_filename"],
        "sha256": p["userdev_sha256"],
        "bytes": p["userdev_bytes"],
        "zip_entries": p["zip_entries"],
        "patches": p["patch_count"],
        "patch_roster_sha256": p["patch_roster_sha256"],
    }, "runtime artifact identity")
    targets = report["targets"]
    expected = seal["expected_targets"]
    need(set(targets) == set(expected) == set(PATHS), "target roster")
    all_rows = 0
    for name, row in targets.items():
        pin = expected[name]
        need(row["present"] is pin["present"] and
             row["path"] == PATHS[name], "presence/path: " + name)
        if not pin["present"]:
            need(name == "LevelWriter" and row == {
                "present": False, "path": PATHS[name]}, "unproven absence")
            continue
        need(row["sha256"] == pin["sha256"] and
             row["hunks"] == pin["hunks"], "patch digest/hunks: " + name)
        need(row["retains_patch_source"] is False and
             0 < row["bytes"] <= 2_000_000 and
             row["total_lines"] >= row["hunks"], "patch shape: " + name)
        counts = row["counts_by_kind"]
        need(counts == {k: pin[k.lower()] for k in
                         ("ADD", "DELETE", "CONTEXT")}, "hit counts: " + name)
        hits = row["matched_lines"]
        need(len(hits) == len(pin["hits"]) and
             len(hits) == sum(counts.values()), "hit roster: " + name)
        for actual, anchor in zip(hits, pin["hits"]):
            for key in ("patch_line", "hunk", "kind", "tokens", "line_sha256"):
                need(actual[key] == anchor[key], "forged patch line " + name + ":" + key)
            need(1 <= actual["patch_line"] <= row["total_lines"] and
                 1 <= actual["hunk"] <= row["hunks"] and
                 actual["kind"] in ("ADD", "DELETE", "CONTEXT") and
                 actual["tokens"] == sorted(set(actual["tokens"])) and
                 set(actual["tokens"]).issubset(WORDS) and
                 re.fullmatch(r"[a-f0-9]{64}", actual["line_sha256"]) and
                 isinstance(actual["line_bytes"], int) and
                 0 < actual["line_bytes"] <= 40_000,
                 "malformed line record")
        need([r["patch_line"] for r in hits] ==
             sorted(set(r["patch_line"] for r in hits)),
             "duplicated or unsorted patch lines")
        all_rows += len(hits)
    need(all_rows == 16, "number of observed symbols")
    need(any("EntityJoinLevelEvent" in h["tokens"] and
             "isCanceled" in h["tokens"] and
             h["kind"] == "ADD" for h in
             targets["ServerLevel"]["matched_lines"]), "server event patch absent")
    need(any("EntityJoinLevelEvent" in h["tokens"] and
             "isCanceled" in h["tokens"] and
             h["kind"] == "ADD" for h in
             targets["PersistentEntitySectionManager"]["matched_lines"]),
         "persistence event patch absent")
    limits = report["limitations"]
    need(limits == {
        "official_maven_sha256_verified_by_ci": True,
        "minecraft_transformed_runtime": "NOT_VERIFIED",
        "all_entity_join_callsites_exhausted": False,
        "event_firing_for_galena_weapon": "NOT_VERIFIED",
        "event_cancellation_settlement": "NOT_VERIFIED",
        "item_stack_rollback": "NOT_VERIFIED",
        "spawn_acceptance": "NOT_VERIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "static_contract": "NOT_CERTIFIED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }, "unsafe runtime or integration claim")
    states = seal["states"]
    for key in ("mutating_hook", "physical_qa", "static_contract", "mutation",
                "provider_universe_closed", "semantic_magic_roots_delta"):
        need(states[key] == limits[key], "status drift from seal " + key)
    need(seal["limitations"] == {
        "runtime": "NOT_VERIFIED", "all_callsites": False,
        "spawn_acceptance": "NOT_VERIFIED",
        "event_order": "NOT_VERIFIED", "stack_rollback": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED"
    }, "unsafe seal limitations")
    return all_rows


def adversarial(report, seal):
    cases = []
    def alter(label, path, value):
        c = copy.deepcopy(report)
        obj = c
        for segment in path[:-1]:
            obj = obj[segment]
        obj[path[-1]] = value
        cases.append((label, c, seal))
    for name in ("ServerLevel", "PersistentEntitySectionManager", "Level"):
        for i, anchor in enumerate(report["targets"][name]["matched_lines"]):
            alter(f"forged {name} line {i}",
                  ["targets", name, "matched_lines", i, "line_sha256"], "0"*64)
    alter("fake event observed in gameplay",
          ["limitations", "event_firing_for_galena_weapon"], "VERIFIED")
    alter("fake safe mutating hook", ["limitations", "mutating_hook"], "VERIFIED")
    alter("fake physical QA", ["limitations", "physical_qa"], "PASSED")
    alter("fake certified contract", ["limitations", "static_contract"], "CERTIFIED")
    alter("fake provider closure", ["limitations", "provider_universe_closed"], True)
    alter("fake semantically new spell", ["limitations", "semantic_magic_roots_delta"], 1)
    alter("fake vanilla method body", ["limitations", "minecraft_transformed_runtime"], "VERIFIED")
    alter("fake event order", ["limitations", "event_cancellation_settlement"], "VERIFIED")
    alter("fake rollback", ["limitations", "item_stack_rollback"], "VERIFIED")
    alter("fake spawn acceptance", ["limitations", "spawn_acceptance"], "VERIFIED")
    alter("fake complete callsites", ["limitations", "all_entity_join_callsites_exhausted"], True)
    alter("different official hash", ["publisher", "sha256"], "0"*64)
    alter("modified patch", ["targets", "ServerLevel", "sha256"], "0"*64)
    alter("removed event", ["targets", "ServerLevel", "matched_lines"], [])
    alter("forged no patch", ["targets", "PersistentEntitySectionManager", "present"], False)
    x = copy.deepcopy(seal)
    x["states"]["mutating_hook"] = "VERIFIED"
    cases.append(("forged manifest hook", report, x))
    x = copy.deepcopy(seal)
    x["expected_targets"]["ServerLevel"]["hits"][0]["line_sha256"] = "0"*64
    cases.append(("forged manifest line", report, x))
    denied = 0
    for label, r, s in cases:
        try:
            validate(r, s, strict=False)
        except (ValueError, TypeError, KeyError, IndexError):
            denied += 1
        else:
            raise AssertionError("forgery accepted: " + label)
    need(denied == len(cases) and denied >= 30,
         "insufficient adversarial coverage")
    return denied


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--adversarial", action="store_true")
    a = parser.parse_args()
    report, raw = load(a.report, 250_000)
    seal, _ = load(a.manifest, 250_000)
    hits = validate(report, seal, raw=raw)
    print("PATCH_REPORT_SHA256", digest(raw), "BYTES", len(raw),
          "ANCHORED_PATCH_HITS", hits)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED", adversarial(report, seal))
    print("OK: official 21.1.248 userdev patch-only evidence; NO_MUTATION")


if __name__ == "__main__":
    main()
