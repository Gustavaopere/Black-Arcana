#!/usr/bin/env python3
"""Scoped, fail-closed javap evidence for two previously catalogued Iron's spells.

The report contains only booleans and metadata, no classfile/disassembly or
third-party code. It is not runtime evidence nor a proof of a pack-installed JAR.
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

from irons_3163_projectile_bytecode import (
    EXPECTED_FILENAME, ROOT, javap, method_block,
)

CLASS_NAMES = {
    "eldritch_spell": "spells.eldritch.EldritchBlastSpell",
    "eldritch_visual": "entity.spells.eldritch_blast.EldritchBlastVisualEntity",
    "dash_spell": "spells.fire.BurningDashSpell",
    "dash_effect": "effect.BurningDashEffect",
}
EXPECTED_SHA256 = "13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73"


def expect_all(block: str, markers: tuple[str, ...], locus: str) -> None:
    missing = [marker for marker in markers if marker not in block]
    if missing:
        raise ValueError(f"{locus}: markers absent: {missing}")


def inspect_disassembly(d: dict[str, str]) -> dict:
    eldritch_cast = method_block(d["eldritch_spell"], "onCast")
    eldritch_recasts = method_block(d["eldritch_spell"], "getRecastCount")
    eldritch_source = method_block(d["eldritch_spell"], "getDamageSource")
    eldritch_visual_tick = method_block(d["eldritch_visual"], "tick")
    visual_saved = method_block(d["eldritch_visual"], "shouldBeSaved")
    dash_cast = method_block(d["dash_spell"], "onCast")
    dash_damage_source = method_block(d["dash_spell"], "getDamageSource")
    dash_effect_tick = method_block(d["dash_effect"], "applyEffectTick")
    dash_every_tick = method_block(d["dash_effect"], "shouldApplyEffectTickThisTick")

    expect_all(eldritch_cast, (
        "RecastInstance", "RaycastBuilder", "EldritchBlastVisualEntity",
        "DamageSources.applyDamage",
    ), "eldritch_spell.onCast")
    expect_all(eldritch_recasts, ("iadd",), "eldritch_spell.getRecastCount")
    expect_all(eldritch_source, ("setIFrames", "indirect"),
               "eldritch_spell.getDamageSource")
    expect_all(eldritch_visual_tick, ("tickCount", "discard"),
               "eldritch_visual.tick")
    expect_all(visual_saved, ("iconst_0", "ireturn"),
               "eldritch_visual.shouldBeSaved")

    expect_all(dash_cast, (
        "ImpulseCastData", "setDeltaMovement", "BURNING_DASH",
        "invulnerableTime", "setSpinAttackType",
    ), "dash_spell.onCast")
    expect_all(dash_damage_source, ("setFireTicks",),
               "dash_spell.getDamageSource")
    expect_all(dash_effect_tick, (
        "DamageSources.applyDamage", "invulnerableTime", "horizontalCollision",
        "BURNING_DASH_SPELL",
    ), "dash_effect.applyEffectTick")
    expect_all(dash_every_tick, ("iconst_1", "ireturn"),
               "dash_effect.shouldApplyEffectTickThisTick")

    lines = dash_effect_tick.splitlines()
    apply_line = next(i for i, s in enumerate(lines)
                      if "DamageSources.applyDamage" in s)
    invuln_line = next(i for i, s in enumerate(lines)
                       if re.search(r"putfield.*invulnerableTime", s))
    if apply_line >= invuln_line:
        raise ValueError("dash effect target i-frame write is not after the damage call")

    return {
        "eldritch_blast": {
            "onCast_creates_recast": True,
            "onCast_uses_raycast_and_damage_helper": True,
            "onCast_spawns_separate_visual": True,
            "recast_count_has_integer_addition": True,
            "damage_source_sets_zero_iframes_and_indirect": True,
            "visual_has_tick_discard": True,
            "visual_shouldBeSaved_false": True,
            "recast_count_exact_numbers": "SOURCE_PLUS_RUNTIME_QA_REQUIRED",
        },
        "burning_dash": {
            "onCast_sets_impulse_and_mob_effect": True,
            "damage_source_sets_fire_ticks": True,
            "effect_calls_damage_helper": True,
            "effect_writes_iframe_counter_after_damage_attempt": True,
            "effect_has_horizontal_collision_branch": True,
            "effect_tick_every_tick_returns_true": True,
            "damage_accepted_each_tick": "NOT_PROVEN_BY_BINARY",
        },
    }


def analyze(jar: Path) -> dict:
    if not jar.is_file() or jar.name != EXPECTED_FILENAME:
        raise ValueError("Exact expected publisher filename/JAR missing")
    with jar.open("rb") as f:
        observed = hashlib.file_digest(f, "sha256").hexdigest()
    if observed != EXPECTED_SHA256:
        raise ValueError("Publisher checksum mismatch")
    with ZipFile(jar) as z:
        names = set(z.namelist())
        for short in CLASS_NAMES.values():
            path = (ROOT + "." + short).replace(".", "/") + ".class"
            if path not in names:
                raise ValueError("Missing expected provider class " + path)
    d = {key: javap(jar, ROOT + "." + short)
         for key, short in CLASS_NAMES.items()}
    report = inspect_disassembly(d)
    report.update({
        "artifact": jar.name, "bytes": jar.stat().st_size,
        "sha256": observed, "evidence": "PUBLISHED_JAR_BYTECODE_STATIC",
        "limitations": [
            "No installed modpack JAR fingerprint comparison",
            "No events or actual in-game damage checked",
            "No proof of NeoForge-transformed behavior or live GameTests",
            "No guaranteed per-hit Mastery attribution or provider hook safety",
        ],
    })
    return report


def self_test() -> None:
    def method(name, *opcodes):
        return ("  public void " + name + "();\n    Code:\n" +
                "\n".join("       " + str(i) + ": " + s
                          for i, s in enumerate(opcodes)) + "\n")
    a = method("onCast", "invokestatic // Method RaycastBuilder",
               "invokestatic // Method DamageSources.applyDamage")
    assert "RaycastBuilder" in method_block(a, "onCast")
    try:
        expect_all(a, ("RecastInstance", "setIFrames"), "fixture")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing required marker must fail closed")
    try:
        expect_all(method("applyEffectTick", "putfield // Field invulnerableTime:I"),
                   ("DamageSources.applyDamage",), "fixture")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing damage call must fail closed")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--jar", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    try:
        if args.self_test:
            self_test()
            print("PASS: scoped source-to-bytecode guard self-tests")
        else:
            if args.jar is None or args.output is None:
                p.error("--jar and --output are required")
            result = analyze(args.jar)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            print(json.dumps(result, indent=2, sort_keys=True))
    except (OSError, ValueError, RuntimeError, AssertionError,
            subprocess.TimeoutExpired) as error:
        print("FAIL_CLOSED:", error, file=sys.stderr)
        raise SystemExit(1)
