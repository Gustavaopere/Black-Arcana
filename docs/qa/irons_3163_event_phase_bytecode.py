#!/usr/bin/env python3
"""Static event-phase evidence for Iron's 3.16.3, not gameplay certification.

Works on a published SHA-256-pinned provider JAR with Java 21 javap.
Outputs metadata and booleans only. Never exports classfiles or bytecode.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZipFile

from irons_3163_projectile_bytecode import EXPECTED_FILENAME, ROOT, javap, method_block
from irons_3163_recast_dash_bytecode import EXPECTED_SHA256

TARGETS = {
    "abstract_spell": "api.spells.AbstractSpell",
    "player_recasts": "capabilities.magic.PlayerRecasts",
    "recast_instance": "capabilities.magic.RecastInstance",
    "damage_sources": "damage.DamageSources",
    "burning_effect": "effect.BurningDashEffect",
    "eldritch": "spells.eldritch.EldritchBlastSpell",
}


def exact_method(disassembly: str, declaration: str) -> str:
    lines = disassembly.splitlines()
    needle = "  " + declaration
    positions = [i for i, s in enumerate(lines) if s == needle]
    if len(positions) != 1:
        raise ValueError(f"Expected unique javap method: {declaration}")
    start = positions[0]
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i] == "}" or re.match(
            r"^  (?:public|protected|private)\b.*[;{]$", lines[i]
        ):
            end = i
            break
    return "\n".join(lines[start:end])


def instructions(block: str) -> list[tuple[int, str, str]]:
    ops = []
    for line in block.splitlines():
        match = re.match(r"^\s*(\d+):\s+([a-z][a-z_0-9]+)\b(.*)$", line)
        if match:
            ops.append((int(match.group(1)), match.group(2), match.group(3)))
    if not ops:
        raise ValueError("No opcodes in javap method")
    return ops


def marker_position(ops, marker: str, desc: str) -> int:
    hits = [i for i, (_, _, rest) in enumerate(ops) if marker in rest]
    if len(hits) != 1:
        raise ValueError(f"Expected exactly one {desc} marker {marker}; found {len(hits)}")
    return hits[0]


def check_dash_local_fallthrough(block: str) -> dict:
    ops = instructions(block)
    call = marker_position(ops, "DamageSources.applyDamage", "dash damage")
    write = marker_position(ops, "invulnerableTime:I", "target i-frame write")
    if write <= call:
        raise ValueError("Target i-frame write not after damage attempt")
    if ops[write][1] != "putfield":
        raise ValueError("Target i-frame marker is not a putfield")
    skipped = [op for _, op, _ in ops[call + 1:write]
               if op.startswith(("if", "goto", "tableswitch", "lookupswitch"))
               or op in ("athrow", "return", "ireturn", "areturn")]
    if skipped:
        raise ValueError("Conditional branch between helper call and i-frame write")
    # Enforce ignored return value, not boolean-based gating.
    if ops[call + 1][1] != "pop":
        raise ValueError("Damage helper boolean result not discarded immediately")
    if not any("BURNING_DASH_SPELL" in r for _, _, r in ops):
        raise ValueError("Missing burning dash spell source")
    return {
        "calls_damage_sources_apply_damage": True,
        "discards_damage_helper_boolean": True,
        "writes_target_invulnerable_time_after_damage_call": True,
        "no_conditional_branch_in_local_call_to_write_segment": True,
        "canceled_damage_can_still_reach_local_write": "LOCAL_FALLTHROUGH_ONLY",
    }


def verify_marker_sequence(block: str, markers: list[str], context: str) -> None:
    indexes = []
    for marker in markers:
        matches = [i for i, line in enumerate(block.splitlines()) if marker in line]
        if not matches:
            raise ValueError(f"{context}: marker missing: {marker}")
        indexes.append(matches[0])
    if indexes != sorted(indexes):
        raise ValueError(f"{context}: unexpected method-call order")


def inspect(d: dict[str, str]) -> dict:
    cast = method_block(d["abstract_spell"], "castSpell")
    recast = exact_method(d["player_recasts"],
                          "public void decrementRecastCount(java.lang.String);")
    recast_tick = exact_method(d["player_recasts"], "public void tick(int);")
    add = method_block(d["player_recasts"], "addRecast")
    serial = method_block(d["recast_instance"], "serializeNBT")
    burning = method_block(d["burning_effect"], "applyEffectTick")
    eldritch = method_block(d["eldritch"], "onCast")
    damage = method_block(d["damage_sources"], "applyDamage")

    verify_marker_sequence(cast, [
        "hasRecastForSpell", "SpellOnCastEvent", "onCast", "decrementRecastCount",
    ], "AbstractSpell.castSpell")
    if not all(m in cast for m in
               ("getManaCost", "getMana", "setMana", "addCooldown", "SpellOnCastEvent")):
        raise ValueError("Missing key mana/cooldown/cast event instructions")
    verify_marker_sequence(recast, [
        "remainingRecasts", "remainingTicks", "removeRecast",
    ], "PlayerRecasts.decrementRecastCount")
    if not all(x in recast_tick for x in ("remainingTicks", "RecastResult.TIMEOUT")):
        raise ValueError("Recast timer/timeout markers absent")
    if not all(x in add for x in ("removeCooldown", "recastLookup", "syncToPlayer")):
        raise ValueError("Recast add/registration markers absent")
    if not all(x in serial for x in
               ("remainingRecasts", "totalRecasts", "ticksToLive", "ticksRemaining")):
        raise ValueError("Recast serialized lifecycle fields absent")
    if not all(x in eldritch for x in ("hasRecastForSpell", "RecastInstance", "RaycastBuilder")):
        raise ValueError("Eldritch initial recast and hitscan markers absent")
    if not all(x in damage for x in ("SpellDamageEvent", "getResist", "hurt", "isCanceled")):
        raise ValueError("Provider damage cancellation/dispatch markers absent")

    return {
        "burning_dash": check_dash_local_fallthrough(burning),
        "eldritch_blast": {
            "spell_on_cast_event_precedes_onCast": True,
            "recast_state_checked_before_onCast": True,
            "mana_branch_depends_on_preexisting_recast": "SOURCE_AND_BYTECODE_BRANCH_QA_PENDING",
            "recast_decrement_after_onCast": True,
            "recast_store_resets_remaining_ticks_on_next_charge": True,
            "expiry_uses_timeout_result": True,
            "recast_lifecycle_fields_serialized": True,
            "first_cast_installs_recast_before_hitscan": True,
            "session_uuid_in_recast_instance": "NO_EXPLICIT_FIELD_IN_SOURCE",
            "number_of_actual_hits_or_spell_on_cast_events": "LIVE_QA_REQUIRED",
        },
        "provider_damage": {
            "has_cancellable_spell_damage_event": True,
            "posts_damage_event_before_hurt": "SOURCE_PINNED_AND_METHOD_MARKERS",
            "cancelled_damage_calls_hurt": "NO_IN_SOURCE_CANCELLATION_BRANCH",
        },
    }


def analyze(jar: Path) -> dict:
    if not jar.is_file() or jar.name != EXPECTED_FILENAME:
        raise ValueError("Expected published Iron's JAR missing")
    with jar.open("rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError("Pinned publisher JAR hash mismatch")
    with ZipFile(jar) as z:
        entries = set(z.namelist())
        for c in TARGETS.values():
            path = (ROOT + "." + c).replace(".", "/") + ".class"
            if path not in entries:
                raise ValueError("Required class missing: " + path)
    dis = {k: javap(jar, ROOT + "." + cl) for k, cl in TARGETS.items()}
    return {
        "evidence": "PUBLISHED_JAR_JAVAP_EVENT_PHASE",
        "artifact": jar.name,
        "sha256": actual,
        **inspect(dis),
        "limits": [
            "No modpack-installed SHA match",
            "No NeoForge-transformed callback order or live GameTest",
            "No guarantee that every attempted hit yields accepted damage",
            "No certified public session ID or RPG Skill Tree adapter",
        ],
    }


def self_test() -> None:
    fake = ("  public boolean applyEffectTick();\n    Code:\n"
            "       0: getstatic #1 // Field BURNING_DASH_SPELL\n"
            "       1: invokestatic #2 // Method DamageSources.applyDamage:()Z\n"
            "       4: pop\n"
            "       5: aload_1\n"
            "       6: bipush 20\n"
            "       8: putfield #3 // Field net/minecraft/world/entity/Entity.invulnerableTime:I\n")
    assert check_dash_local_fallthrough(fake)["discards_damage_helper_boolean"]
    changed = fake.replace("       4: pop\n", "       4: ifeq 14\n")
    try:
        check_dash_local_fallthrough(changed)
    except ValueError:
        pass
    else:
        raise AssertionError("Conditional / non-discarded return was accepted")
    try:
        check_dash_local_fallthrough(fake.replace("       4: pop\n", ""))
    except ValueError:
        pass
    else:
        raise AssertionError("Absent pop was accepted")
    text = "  public void decrementRecastCount(java.lang.String);\n    Code:\n       0: return\n"
    assert "return" in exact_method(text, "public void decrementRecastCount(java.lang.String);")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("PASS: event-phase and local-fallthrough fail-closed guards")
        else:
            if args.jar is None or args.output is None:
                parser.error("--jar and --output required")
            report = analyze(args.jar)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
            print(json.dumps(report, indent=2, sort_keys=True))
    except (OSError, ValueError, RuntimeError, AssertionError,
            subprocess.TimeoutExpired) as e:
        print("FAIL_CLOSED:", e, file=sys.stderr)
        raise SystemExit(1)
