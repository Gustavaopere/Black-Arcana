#!/usr/bin/env python3
"""Clean-room, SHA-verified direct-call edges for nine selected Wind 1.0.5 getters.

A JVM method containing a getter call AND an entity setter does not establish
that the getter's return is the setter's argument. Keep these evidence classes separate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as binary

LIVING = "Lnet/minecraft/world/entity/LivingEntity;"
LEVEL_TARGET = f"(I{LIVING})"
GETTERS = {
    "aeropic": {"getRecastCount": LEVEL_TARGET + "I"},
    "almighty_push": {"getDuration": "(I)I", "getRange": LEVEL_TARGET + "F"},
    "iron_slash": {"getDistance": LEVEL_TARGET + "F"},
    "tailwind": {"getPercentAirSpeed": "(I)F", "getPercentJump": "(I)F"},
    "tornado": {"getDuration": "(I)I"},
    "wind_jump": {"getFloatDuration": LEVEL_TARGET + "I", "getJumpStrength": LEVEL_TARGET + "F"},
}
# Direct callers verified in the previous 7-class SHA-exact inventory.
# These are methods of the SPELL class itself, NOT global use counts.
EXPECTED_CALLERS = {
    "aeropic": {"getRecastCount": ("getUniqueInfo",)},
    "almighty_push": {
        "getDuration": ("getUniqueInfo", "onCast"),
        "getRange": ("getUniqueInfo", "onCast"),
    },
    "iron_slash": {"getDistance": ("getUniqueInfo", "onCast")},
    "tailwind": {
        "getPercentAirSpeed": ("getUniqueInfo",),
        "getPercentJump": ("getUniqueInfo",),
    },
    "tornado": {"getDuration": ("getUniqueInfo", "onCast")},
    "wind_jump": {
        "getFloatDuration": ("getUniqueInfo", "onCast"),
        "getJumpStrength": ("getJumpHeight", "onCast"),
    },
}
# Exact calls/field accesses co-present inside each spell's onCast.
# NONE is claimed as an operand consumer of an individual getter.
ON_CAST_OBSERVATIONS = {
    "aeropic": {
        "invoked_symbols": (
            "net/minecraft/server/network/ServerGamePacketListenerImpl.teleport:(DDDFF)V",
            "net/minecraft/world/entity/LivingEntity.setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V",
        ),
        "read_fields": (
            "net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry.ACROBATICS:Lnet/neoforged/neoforge/registries/DeferredHolder;",
        ),
    },
    "almighty_push": {
        "invoked_symbols": (
            "net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.setLifetime:(I)V",
            "net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.setRadius:(F)V",
        ),
        "written_fields": (
            "net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.strength:F",
            "net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.amplifier:I",
        ),
    },
    "iron_slash": {
        "invoked_symbols": (
            "io/redspace/ironsspellbooks/spells/ender/TeleportSpell.findTeleportLocation:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;F)Lnet/minecraft/world/phys/Vec3;",
            "performDash:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/phys/Vec3;)V",
        ),
    },
    "tailwind": {
        "invoked_symbols": (
            "net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z",
        ),
        "read_fields": (
            "net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry.TAILWIND:Lnet/neoforged/neoforge/registries/DeferredHolder;",
        ),
    },
    "tornado": {
        "invoked_symbols": (
            "net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setDamage:(F)V",
            "net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setDuration:(I)V",
            "net/raptorzizi/wind_spellbooks/entity/spells/tornado/TornadoEntity.setRadius:(F)V",
        ),
    },
    "wind_jump": {
        "invoked_symbols": (
            "net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z",
            "io/redspace/ironsspellbooks/capabilities/magic/ImpulseCastData.\"<init>\":(FFFZ)V",
        ),
        "written_fields": (
            "io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.amplifier:I",
            "io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.range:F",
            "io/redspace/ironsspellbooks/entity/spells/gust/GustCollider.strength:F",
        ),
    },
}

class EvidenceError(ValueError):
    pass

def _method_name(header: str) -> str:
    start = header.split("(", 1)[0]
    if "(" not in header or " " not in start:
        raise EvidenceError("unreadable Java method declaration")
    return start.rsplit(" ", 1)[-1]

def analyze(inventory: dict) -> dict:
    if inventory.get("result") != "PASS" or inventory.get("sha1") != binary.EXPECTED_SHA1:
        raise EvidenceError("unverified JAR inventory")
    if inventory.get("provider") != "wind_spellbooks" or inventory.get("class_count") != 7:
        raise EvidenceError("wrong provider or class count")
    spells = inventory.get("spells")
    if not isinstance(spells, dict) or set(spells) != set(binary.ROSTER):
        raise EvidenceError("unexpected spell class roster")

    report = {}
    for spell, wanted in GETTERS.items():
        methods = spells[spell]["methods"]
        declarations = {}
        for header, details in methods.items():
            name = _method_name(header) if header != "<clinit>" else "<clinit>"
            if name in declarations:
                raise EvidenceError(f"ambiguous overloaded method: {spell}.{name}")
            declarations[name] = details
        if "onCast" not in declarations or "getUniqueInfo" not in declarations:
            raise EvidenceError(f"missing audited spell entry point: {spell}")
        getter_rows = {}
        for getter, desc in wanted.items():
            if getter not in declarations:
                raise EvidenceError(f"getter declaration not found: {spell}.{getter}")
            symbol = getter + ":" + desc
            actual = sorted(name for name, row in declarations.items()
                            if symbol in row["invoked_symbols"])
            expected = sorted(EXPECTED_CALLERS[spell][getter])
            if actual != expected:
                raise EvidenceError(f"direct caller drift: {spell}.{getter}: {actual!r} != {expected!r}")
            getter_rows[getter] = {
                "callee": symbol,
                "direct_callers": actual,
                "on_cast_direct_call": "onCast" in actual,
                "unique_info_direct_call": "getUniqueInfo" in actual,
                "evidence": "EXACT_JVM_DIRECT_METHOD_INVOCATION_ONLY",
                "effective_consumer_argument_flow": "NOT_PROVEN",
            }

        cast = declarations["onCast"]
        other = {}
        for family, symbols in ON_CAST_OBSERVATIONS[spell].items():
            missing = set(symbols) - set(cast[family])
            if missing:
                raise EvidenceError(f"missing onCast symbol: {spell} {sorted(missing)!r}")
            other[family] = sorted(symbols)
        report[spell] = {
            "getters": getter_rows,
            "on_cast_copresent_sink_symbols": other,
            "copresent_sink_relationship": "SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW",
        }
    if sum(len(x["getters"]) for x in report.values()) != 9:
        raise EvidenceError("nine-getter roster not preserved")
    return {
        "result": "PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY",
        "sha1": binary.EXPECTED_SHA1,
        "release": "1.0.5",
        "provider": "wind_spellbooks",
        "getters_checked": 9,
        "spells_in_scope": len(report),
        "spells": report,
        "limitations": [
            "direct calls only; no external class, reflection, indirect calls or all-provider scan",
            "getUniqueInfo is a named information method; not proof of display-only behavior",
            "onCast co-presence of a getter and a setter does not prove argument dataflow",
            "no runtime testing, no mutator hooks, no RPG/Black Arcana cast ownership change",
        ],
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    try:
        result = analyze(binary.audit(args.jar))
        status = 0
    except (EvidenceError, binary.AuditError, OSError, ValueError, KeyError, TypeError) as exc:
        result = {"result": "FAIL_CLOSED", "reason": str(exc)}
        status = 1
    message = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(message, encoding="utf8")
    print(message)
    return status

if __name__ == "__main__":
    raise SystemExit(main())
