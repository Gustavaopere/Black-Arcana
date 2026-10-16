#!/usr/bin/env python3
"""Static publisher-JAR evidence for four catalogued Iron's 3.16.3 spells.

No provider implementation is reproduced. Output is bounded metadata/booleans,
not disassembly, runtime observation or a GameTest result.
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
from irons_3163_recast_dash_bytecode import EXPECTED_SHA256, expect_all

CLASS_NAMES = {
    "heartstop_spell": "spells.blood.HeartstopSpell",
    "heartstop_effect": "effect.HeartstopEffect",
    "heartstop_listener": "player.ServerPlayerEvents",
    "synced_data": "capabilities.magic.SyncedSpellData",
    "heal_spell": "spells.holy.HealSpell",
    "greater_heal_spell": "spells.holy.GreaterHealSpell",
    "heal_event": "api.events.SpellHealEvent",
    "blight_spell": "spells.nature.BlightSpell",
    "blight_effect": "effect.BlightEffect",
}


def ordered(block: str, markers: tuple[str, ...], scope: str) -> None:
    indexes = []
    for marker in markers:
        positions = [i for i, line in enumerate(block.splitlines())
                     if marker in line]
        if not positions:
            raise ValueError(f"{scope}: marker absent: {marker}")
        indexes.append(positions[0])
    if indexes != sorted(indexes):
        raise ValueError(f"{scope}: unexpected static marker order")


def audit(dis: dict[str, str]) -> dict:
    hs_cast = method_block(dis["heartstop_spell"], "onCast")
    hs_remove = method_block(dis["heartstop_effect"], "onEffectRemoved")
    hs_damage_pre = method_block(dis["heartstop_listener"], "onBeforeDamageTaken")
    hs_add = method_block(dis["synced_data"], "addHeartstopDamage")
    h_cast = method_block(dis["heal_spell"], "onCast")
    gh_cast = method_block(dis["greater_heal_spell"], "onCast")
    b_cast = method_block(dis["blight_spell"], "onCast")
    b_heal = method_block(dis["blight_effect"], "reduceHealing")
    b_damage = method_block(dis["blight_effect"], "reduceDamageOutput")

    expect_all(hs_cast, ("HEARTSTOP", "getSpellPower", "addEffect"),
               "HeartstopSpell.onCast")
    expect_all(hs_remove, ("getHeartstopAccumulatedDamage", "hurt",
                           "kill", "setHeartstopAccumulatedDamage"),
               "HeartstopEffect.onEffectRemoved")
    expect_all(hs_damage_pre, ("HEARTSTOP", "getOriginalDamage",
                               "addHeartstopDamage", "setNewDamage"),
               "ServerPlayerEvents.onBeforeDamageTaken")
    expect_all(hs_add, ("heartStopAccumulatedDamage", "doSync"),
               "SyncedSpellData.addHeartstopDamage")
    expect_all(h_cast, ("getSpellPower", "SpellHealEvent",
                        "NeoForge", "heal"),
               "HealSpell.onCast")
    expect_all(gh_cast, ("getMaxHealth", "SpellHealEvent", "heal",
                         "HealParticlesPacket"),
               "GreaterHealSpell.onCast")
    ordered(h_cast, ("SpellHealEvent", "NeoForge", "heal:"),
            "HealSpell.onCast")
    ordered(gh_cast, ("getMaxHealth", "SpellHealEvent", "heal:"),
            "GreaterHealSpell.onCast")
    expect_all(dis["heal_event"], ("getTargetEntity", "getHealAmount",
                                   "getSchoolType"),
               "SpellHealEvent")
    expect_all(b_cast, ("TargetEntityCastData", "BLIGHT", "addEffect"),
               "BlightSpell.onCast")
    expect_all(b_heal, ("LivingHealEvent", "BLIGHT", "setAmount"),
               "BlightEffect.reduceHealing")
    expect_all(b_damage, ("LivingIncomingDamageEvent", "BLIGHT",
                          "getEntity", "setAmount"),
               "BlightEffect.reduceDamageOutput")

    return {
        "heartstop": {
            "cast_applies_effect_to_caster": True,
            "damage_pre_accumulates_original_damage": True,
            "damage_pre_overrides_new_damage": True,
            "remove_has_hurt_path": True,
            "remove_has_kill_path": True,
            "remove_resets_accumulator": True,
            "real_kill_at_low_tick_count": "NOT_PROVEN_BY_STATIC",
        },
        "heal": {
            "spell_heal_event_precedes_heal_call": True,
            "event_reports_proposed_amount": True,
            "net_hp_recovery": "REQUIRES_LIVE_HP_SNAPSHOT",
        },
        "greater_heal": {
            "proposed_amount_comes_from_max_health": True,
            "spell_heal_event_precedes_heal_call": True,
            "particle_packet_does_not_certify_healing": True,
            "long_cast_interruption": "NOT_PROVEN_BY_STATIC",
        },
        "blight": {
            "cast_applies_targeted_mob_effect": True,
            "living_heal_event_amount_mutated": True,
            "living_incoming_damage_event_amount_mutated": True,
            "actual_multipliers": "SOURCE_PINNED_FORMULAS_NOT_RUNTIME_MEASURED",
        },
    }


def analyze(jar: Path) -> dict:
    if not jar.is_file() or jar.name != EXPECTED_FILENAME:
        raise ValueError("Expected named publisher JAR missing")
    with jar.open("rb") as f:
        sha = hashlib.file_digest(f, "sha256").hexdigest()
    if sha != EXPECTED_SHA256:
        raise ValueError("Publisher JAR SHA-256 mismatch")
    with ZipFile(jar) as z:
        members = set(z.namelist())
        for name in CLASS_NAMES.values():
            member = (ROOT + "." + name).replace(".", "/") + ".class"
            if member not in members:
                raise ValueError("Required provider class missing: " + member)
    dis = {key: javap(jar, ROOT + "." + name)
           for key, name in CLASS_NAMES.items()}
    report = audit(dis)
    return {
        "evidence": "PUBLISHED_JAR_JAVAP_STATIC_HEALING_HEARTSTOP",
        "artifact": jar.name,
        "sha256": sha,
        "bytes": jar.stat().st_size,
        "classes_examined": len(CLASS_NAMES),
        **report,
        "limits": [
            "Source semantics and classfile symbols are separate evidence",
            "No modpack-installed JAR, NeoForge-transformed events or GameTest",
            "No verified healing HP delta, lethal removal, cast interruption or effect lifecycle",
            "No new safe public API for Mastery, debuff scaling or effect dispel",
        ],
    }


def self_test() -> None:
    good = ("  public void onCast();\n    Code:\n"
            "    0: new #7 // class SpellHealEvent\n"
            "    3: invokevirtual #8 // Field NeoForge.EVENT_BUS\n"
            "    7: invokevirtual #9 // Method LivingEntity.heal:(F)V\n")
    ordered(good, ("SpellHealEvent", "NeoForge", "heal:"), "synthetic")
    reversed_order = good.replace("SpellHealEvent", "TEMP").replace(
        "LivingEntity.heal:", "SpellHealEvent").replace(
        "TEMP", "LivingEntity.heal:")
    try:
        ordered(reversed_order, ("SpellHealEvent", "NeoForge", "heal:"),
                "synthetic")
    except ValueError:
        pass
    else:
        raise AssertionError("Event-after-heal must fail")
    try:
        expect_all("fake", ("BLIGHT", "setAmount"), "synthetic")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing provider marker must fail")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("PASS: healing/Heartstop/Blight static guard self-tests")
        else:
            if args.jar is None or args.output is None:
                parser.error("--jar and --output required")
            report = analyze(args.jar)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
            print(json.dumps(report, indent=2, sort_keys=True))
    except (OSError, RuntimeError, ValueError, AssertionError,
            subprocess.TimeoutExpired) as exc:
        print("FAIL_CLOSED:", exc, file=sys.stderr)
        raise SystemExit(1)
