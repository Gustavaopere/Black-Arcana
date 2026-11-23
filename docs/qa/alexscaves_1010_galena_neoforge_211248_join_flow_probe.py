#!/usr/bin/env python3
"""Read-only structural analysis of exact NeoForge 21.1.248 entity admission patches.

Inspects upstream SHA-exact userdev only. Emits abstract role/ordering markers
and hashes, never original Java patch bodies. Not transformed runtime evidence;
does not prove Galena spawn outcome, stack rollback or a safe mutation hook.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

VERSION = "21.1.248"
USERDEV = "neoforge-21.1.248-userdev.jar"
USERDEV_SHA = "9278d08154a82927391ed5257481f56d6d0fcb147822c6a79ec9b5129799e79a"
PATCHES = {
    "ServerLevel": (
        "patches/net/minecraft/server/level/ServerLevel.java.patch",
        "d9dc7428b5467f35b42e9f972b3eb9079312e660755b77b6be1f880ed88e6249"),
    "PersistentEntitySectionManager": (
        "patches/net/minecraft/world/level/entity/PersistentEntitySectionManager.java.patch",
        "a2a5ef2bdbf3fec5b7db2f7cc4674338358011b3b738622a7f180faeeb2a56a0"),
}

def need(ok, reason):
    if not ok:
        raise ValueError(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def one(lines, token, prefix=None):
    found = [i for i, x in enumerate(lines)
             if token in x and (prefix is None or x.startswith(prefix))]
    need(len(found) == 1, "missing/duplicate token " + token + ": " + str(len(found)))
    return found[0]

def anchor(lines, index, role):
    h = sum(x.startswith("@@") for x in lines[:index + 1])
    need(h > 0, "unanchored patch symbol")
    row = lines[index]
    return {
        "role": role, "line": index + 1, "hunk": h,
        "kind": ("ADD" if row.startswith("+") else
                 "DELETE" if row.startswith("-") else "CONTEXT"),
        "line_sha256": sha(row.encode()), "bytes": len(row.encode()),
    }

def server(raw):
    lines = raw.decode("utf-8").splitlines()
    player = one(lines, "private void addPlayer(ServerPlayer")
    event = one(lines, "EntityJoinLevelEvent(")
    bypass = one(lines, "this.entityManager.addNewEntityWithoutEvent(")
    generic = one(lines, "private boolean addEntity(Entity")
    players_added = [i for i, s in enumerate(lines)
                     if player < i < generic and s.startswith("+") and
                     ".onAddedToLevel();" in s]
    need(len(players_added) == 1, "unexpected player callback")
    ordinary = one(lines, "if (this.entityManager.addNewEntity(", prefix="+")
    window = lines[ordinary:ordinary + 10]
    def added(predicate):
        a = [ordinary + i for i, s in enumerate(window)
             if s.startswith("+") and predicate(s)]
        need(len(a) == 1, "unexpected ordinary entity branch")
        return a[0]
    notified = added(lambda s: ".onAddedToLevel();" in s)
    true = added(lambda s: s.strip().endswith("return true;"))
    false = added(lambda s: s.strip().endswith("return false;"))
    need(player < event < bypass < players_added[0] < generic <
         ordinary < notified < true < false, "ServerLevel admission order")
    need(lines[event].startswith("+") and
         ".isCanceled()) return;" in lines[event],
         "player event must have void cancellation return")
    return {
        "patch_sha256": sha(raw),
        "anchors": [
            anchor(lines, i, role) for i, role in [
                (player, "player_method"), (event, "player_join_cancel_void_return"),
                (bypass, "player_registration_bypasses_second_event"),
                (players_added[0], "player_on_added"),
                (generic, "generic_add_entity_method"),
                (ordinary, "generic_manager_boolean_branch"),
                (notified, "generic_on_added_if_manager_true"),
                (true, "generic_accepted_true"),
                (false, "generic_rejected_false"),
            ]
        ],
        "flow": {
            "player_event_before_bypass_registration": True,
            "player_cancel_returns_void": True,
            "normal_entity_manager_boolean_controls_return": True,
            "normal_entity_on_added_only_if_manager_true": True,
            "complete_transformed_serverlevel_verified": False,
        },
    }

def manager(raw):
    lines = raw.decode("utf-8").splitlines()
    bypass = one(lines, "public boolean addNewEntityWithoutEvent(")
    bypass_call = one(lines, "return this.addEntityWithoutEvent(")
    enter = one(lines, "private boolean addEntity(T ")
    event = one(lines, "EntityJoinLevelEvent(")
    forward = one(lines, "return addEntityWithoutEvent(")
    insert = one(lines, "private boolean addEntityWithoutEvent(")
    uuid = one(lines, "if (!this.addEntityUuid(")
    need(bypass < bypass_call < enter < event < forward < insert < uuid,
         "manager cancellation/UUID order")
    need(lines[event].startswith("+") and
         "instanceof Entity entity" in lines[event] and
         "EVENT_BUS.post" in lines[event] and
         ".isCanceled()) return false;" in lines[event],
         "generic entity cancellation boolean false")
    need("false" in lines[bypass_call] and
         lines[forward].startswith("+") and
         lines[insert].startswith("+"),
         "registration without second event")
    paths = []
    for method, disk in (
        ("addLegacyChunkEntities", "true"),
        ("addWorldGenChunkEntities", "false"),
        ("processPendingLoads", "true"),
    ):
        start = one(lines, method + "(")
        nearby = lines[start:start + 13]
        calls = [start + i for i, s in enumerate(nearby)
                 if s.startswith("+") and "this.addEntity(" in s and
                 s.strip().endswith(disk + ");")]
        callbacks = [start + i for i, s in enumerate(nearby)
                     if s.startswith("+") and "instanceof Entity entity" in s
                     and "entity.onAddedToLevel();" in s]
        need(len(calls) == len(callbacks) == 1 and calls[0] < callbacks[0],
             "load event-callback order: " + method)
        paths.append({
            "method": method, "disk_flag": disk,
            "boolean_return_checked_before_on_added": False,
            "anchors": [
                anchor(lines, start, "load_entrypoint"),
                anchor(lines, calls[0], "bare_add_entity_call"),
                anchor(lines, callbacks[0], "notification_after_call"),
            ],
        })
    return {
        "patch_sha256": sha(raw),
        "anchors": [
            anchor(lines, i, role) for i, role in [
                (bypass, "bypass_method"),
                (bypass_call, "bypass_direct_registration"),
                (enter, "normal_admission_method"),
                (event, "normal_entity_join_cancellation_false"),
                (forward, "forward_to_uuid_registration"),
                (insert, "registration_without_event"),
                (uuid, "uuid_guard_after_cancellation"),
            ]
        ],
        "load_paths": paths,
        "flow": {
            "normal_entity_join_cancel_return_false": True,
            "normal_cancellation_before_uuid_registration": True,
            "player_bypass_prevents_duplicate_event_in_this_patch": True,
            "three_load_notifications_after_unchecked_add_result": True,
            "runtime_effect_of_load_notifications": "NOT_VERIFIED",
        },
    }

def run(jar, output):
    need(jar.name == USERDEV and jar.is_file() and
         jar.stat().st_size == 3_983_248 and
         sha(jar.read_bytes()) == USERDEV_SHA, "upstream userdev identity drift")
    need(output.suffix == ".json" and not output.exists(), "write-once JSON")
    with ZipFile(jar) as archive:
        need(len(archive.namelist()) == len(set(archive.namelist())),
             "duplicate ZIP names")
        mapping = {}
        for name, (path, expected_hash) in PATCHES.items():
            raw = archive.read(path)
            need(sha(raw) == expected_hash, "patch identity changed: " + name)
            mapping[name] = server(raw) if name == "ServerLevel" else manager(raw)
    result = {
        "schema": 1,
        "scope": "GALENA_1010_NEOFORGE_211248_ENTITY_JOIN_CAUSAL_PATCH_DISCOVERY_ONLY",
        "upstream": {"version": VERSION, "userdev": USERDEV,
                     "bytes": 3983248, "sha256": USERDEV_SHA},
        "patches": mapping,
        "limits": {
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
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True,
                                 ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--userdev", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest:
        sample = ["@@ -1 +1 @@", " method()", "+ action();"]
        need(one(sample, "action();", prefix="+") == 2,
             "synthetic parser failure")
        need(anchor(sample, 2, "synthetic")["hunk"] == 1,
             "hunk counter failure")
        try:
            one(sample, "missing()")
        except ValueError:
            pass
        else:
            raise AssertionError("missing symbol accepted")
        print("PASS bounded abstract parser selftest")
        return
    need(args.userdev is not None and args.output is not None,
         "require --userdev and --output")
    result = run(args.userdev, args.output)
    for name, item in result["patches"].items():
        print("PATCH", name, item["patch_sha256"])
        print("FLOW", name, json.dumps(item["flow"], sort_keys=True))
        for row in item["anchors"]:
            print("MARKER", name, row["role"], row["line"],
                  row["hunk"], row["line_sha256"])
        for path in item.get("load_paths", []):
            print("LOAD_PATH", path["method"], path["disk_flag"],
                  "result_checked", path["boolean_return_checked_before_on_added"])
    print("REPORT_SHA256", sha(args.output.read_bytes()),
          "BYTES", args.output.stat().st_size)
    print("NO_MUTATION NOT_CERTIFIED NO_PHYSICAL_QA")

if __name__ == "__main__":
    main()
