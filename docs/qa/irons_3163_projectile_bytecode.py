#!/usr/bin/env python3
"""Fail-closed, clean-room bytecode evidence for Iron's 1.21.1-3.16.3.

Only reads class signatures, method invocation names, and control-flow hints.
Does not load the mod, copy implementation, or claim runtime/GameTest proof.
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

ROOT = "io.redspace.ironsspellbooks"
CLASSES = {
    "volley_controller": "entity.spells.ArrowVolleyEntity",
    "volley_arrow": "entity.spells.small_magic_arrow.SmallMagicArrow",
    "summoned_skeleton": "entity.mobs.SummonedSkeleton",
    "poison_cloud": "entity.spells.poison_cloud.PoisonCloud",
}
EXPECTED_FILENAME = "irons_spellbooks-1.21.1-3.16.3.jar"
EXPECTED_CURSEFORGE_ID = 8680204


def method_block(disassembly: str, name: str) -> str:
    """Extract one method using javap's two-space declaration boundaries."""
    lines = disassembly.splitlines()
    pattern = re.compile(r"^  (?:public|protected|private)\b.*\b"
                         + re.escape(name) + r"\([^)]*\);$")
    starts = [i for i, line in enumerate(lines) if pattern.match(line)]
    if len(starts) != 1:
        raise ValueError(f"Expected exactly one declared method {name}: found {len(starts)}")
    start = starts[0]
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if re.match(r"^  (?:public|protected|private)\b.*[;{]$", line):
            end = i
            break
        if line == "}":
            end = i
            break
    return "\n".join(lines[start:end])


def javap(jar: Path, dotted: str) -> str:
    cmd = ["javap", "-classpath", str(jar), "-p", "-c", dotted]
    out = subprocess.run(cmd, text=True, capture_output=True, timeout=30, check=False)
    if out.returncode:
        raise RuntimeError(f"javap failed for {dotted}: {out.stderr[:500]}")
    if "Compiled from" not in out.stdout and "class " not in out.stdout:
        raise RuntimeError(f"Unexpected javap output: {dotted}")
    return out.stdout


def analyze(jar: Path) -> dict:
    if not jar.is_file() or jar.stat().st_size < 10_000_000:
        raise ValueError("Missing or implausibly small Iron's JAR")
    if jar.name != EXPECTED_FILENAME:
        raise ValueError(f"Expected filename {EXPECTED_FILENAME}, received {jar.name}")
    with ZipFile(jar) as z:
        members = set(z.namelist())
        for name in CLASSES.values():
            member = (ROOT + "." + name).replace(".", "/") + ".class"
            if member not in members:
                raise ValueError(f"Missing required class: {member}")
        meta = [p for p in members if p in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml")]
        mod_metadata = "\n".join(z.read(p).decode("utf-8", "replace") for p in meta)
        if not meta or "irons_spellbooks" not in mod_metadata:
            raise ValueError("Missing expected NeoForge mod ID metadata")
    dis = {key: javap(jar, ROOT + "." + short) for key, short in CLASSES.items()}
    tick = method_block(dis["volley_controller"], "tick")
    shoot = method_block(dis["volley_arrow"], "shoot")
    volley_hit = method_block(dis["volley_arrow"], "onHitEntity")
    cloud_effect = method_block(dis["poison_cloud"], "applyEffect")
    if "tickCount" not in tick or "SmallMagicArrow" not in dis["volley_controller"]:
        raise ValueError("Volley controller does not match expected static markers")
    if "ARROW_VOLLEY_SPELL" not in volley_hit:
        raise ValueError("Volley arrow damage-source marker absent")
    if "setDeltaMovement" not in shoot:
        raise ValueError("SmallMagicArrow shoot-setDeltaMovement marker absent")
    if "POISON_CLOUD" not in cloud_effect or "hurt" not in cloud_effect:
        raise ValueError("PoisonCloud direct-hurt damage marker absent")
    if not re.search(r"extends net\.minecraft\.world\.entity\.monster\.Skeleton", dis["summoned_skeleton"]):
        raise ValueError("SummonedSkeleton no longer directly extends expected Minecraft Skeleton")
    declared_ranged = bool(re.search(r"^  (?:public|protected|private).*\bperformRangedAttack\(", dis["summoned_skeleton"], re.M))
    calls_super_tick = bool(re.search(r"invokespecial\s+[^\n]*// Method [^\n]*\.tick:\(\)V", tick))
    direct_tick_write = bool(re.search(r"putfield\s+[^\n]*tickCount", tick))
    report = {
        "source": "published NeoForge JAR fetched externally; binary inspection only",
        "artifact_filename": jar.name,
        "curseforge_file_id_claimed_by_workflow": EXPECTED_CURSEFORGE_ID,
        "sha256": hashlib.sha256(jar.read_bytes()).hexdigest(),
        "bytes": jar.stat().st_size,
        "java": subprocess.run(["java", "-version"], capture_output=True, text=True, check=True).stderr.splitlines()[0],
        "tick_controller": {
            "tick_method_present": True,
            "reads_tickCount": "tickCount" in tick,
            "calls_super_tick": calls_super_tick,
            "writes_tickCount_directly": direct_tick_write,
            "risk": ("UNVERIFIED_TICKCOUNT_PROGRESSION"
                     if not calls_super_tick and not direct_tick_write else "REQUIRES_RUNTIME_QA"),
        },
        "volley_small_arrow": {
            "shoot_sets_delta_movement": True,
            "shoot_calls_getSpeed": "getSpeed" in shoot,
            "on_hit_uses_arrow_volley_source": True,
        },
        "summoned_skeleton": {
            "direct_parent_is_vanilla_skeleton": True,
            "declares_performRangedAttack": declared_ranged,
            "inherited_arrow_damage_source": "NOT_PROVEN_BY_THIS_JAR",
        },
        "poison_cloud": {
            "direct_hurt_method": True,
            "invokes_damage_sources_applyDamage": "DamageSources.applyDamage" in cloud_effect,
            "spell_damage_event_for_cloud": "NOT_PROVEN_BY_THIS_METHOD",
        },
        "limitations": [
            "No modpack-installed JAR fingerprint provided: published artifact may differ",
            "No Minecraft/NeoForge 1.21.1 game class bytecode inspected",
            "No game tick, world, PvP, reload, or dedicated server execution",
            "Method calls in bytecode are not proof of callback/event order in live gameplay",
        ],
    }
    return report


def self_test() -> None:
    fake = ("public class Example {\n"
            "  public void tick();\n"
            "    Code:\n"
            "       0: aload_0\n"
            "       1: getfield #1 // Field tickCount:I\n"
            "\n"
            "  public void other();\n"
            "    Code:\n"
            "       0: return\n"
            "}\n")
    assert "tickCount" in method_block(fake, "tick")
    assert "other" not in method_block(fake, "tick")
    try:
        method_block(fake, "absent")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing method must fail closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("PASS: javap method boundary self-test")
        else:
            if args.jar is None or args.output is None:
                parser.error("--jar and --output are mandatory")
            evidence = analyze(args.jar)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
            print(json.dumps(evidence, indent=2, sort_keys=True))
    except (OSError, ValueError, RuntimeError, AssertionError, subprocess.TimeoutExpired) as e:
        print(f"FAIL_CLOSED: {e}", file=sys.stderr)
        raise SystemExit(1)
