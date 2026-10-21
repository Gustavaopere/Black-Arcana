#!/usr/bin/env python3
"""Clean-room, SHA-exact Somake 1.0.9 Funeral Bloom impact-entity JVM audit.

Emits only method names, JVM descriptors, bounded member references, and branch
counts. No decompiled implementation bodies, class bytes, constants or assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_cast_refs import parse_javap
from somake_109_funeral_bud_probe import isolate_named_methods

FQCN = "com.somake.somakespells.entity.FuneralBloomImpactEntity"
FOCUS_ALL = re.compile(r"^[A-Za-z_$]")
MAX_JAR_BYTES = 20_000_000
MAX_REF_TOTAL = 460
SIGNALS = {
    "damage": ("DamageSources.applyDamage:", "LivingEntity.hurt:", "Entity.hurt:",
               "SpellDamageEvent", "getDamageSource:"),
    "healing": ("SpellHealEvent", "LivingEntity.heal:", "Player.heal:",
                "setHealth:"),
    "targeting": ("getEntitiesOfClass:", "getEntities:", "AABB.inflate:",
                  "distanceToSqr:", "isAlliedTo:", "isSpectator:"),
    "status": ("MobEffectInstance", "MobEffects.WITHER", "LivingEntity.addEffect:"),
    "lifecycle": ("discard:", "remove:", "kill:", "tickCount", "getLifetime",
                  "shouldBeSaved:", "getDuration:"),
    "ownership": ("getOwner:", "getCaster:", "getOwnerUUID:", "getUUID:"),
    "particles_sounds": ("sendParticles:", "spawnParticles:", "playSound:",
                         "ParticleHelper", "ModParticles", "SoundEvents"),
    "world_effects": ("destroyBlock:", "setBlock:", "explode:", "mobGriefing",
                      "ExplosionEvent"),
}

def summarize(parsed: dict) -> dict:
    methods = parsed["methods"]
    if not methods or len(methods) > 140:
        raise GateError("missing or excessive named impact methods")
    if sum(len(m["members"]) for m in methods) > MAX_REF_TOTAL:
        raise GateError("impact symbolic reference budget exceeded")
    seen = {(m["method"], m["descriptor"]) for m in methods}
    if len(seen) != len(methods):
        raise GateError("duplicate impact method identity")
    categories = {category: [] for category in SIGNALS}
    for m in methods:
        for category, keys in SIGNALS.items():
            if any(any(k in symbol for k in keys) for symbol in m["members"]):
                categories[category].append(m["method"] + m["descriptor"])
    return {
        "declared_methods": parsed["declared_methods"],
        "named_methods": len(methods),
        "methods": methods,
        "categories_by_method": categories,
        "other_declared": parsed["other_declared"],
    }

def inspect(jar: Path) -> dict:
    if not jar.is_file() or jar.is_symlink() or jar.name != FILENAME:
        raise GateError("publisher artifact filename/type mismatch")
    if not 100 < jar.stat().st_size < MAX_JAR_BYTES:
        raise GateError("unexpected artifact size")
    digest = hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest != SHA1:
        raise GateError("Somake 1.0.9 exact SHA-1 mismatch")
    with zipfile.ZipFile(jar) as zf:
        members = zf.namelist()
        if len(members) != len(set(members)):
            raise GateError("duplicate jar members")
        metadata = zf.read("META-INF/neoforge.mods.toml")
        if len(metadata) > 250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]", metadata):
            raise GateError("provider identity mismatch")
        if FQCN.replace(".", "/") + ".class" not in members:
            raise GateError("FuneralBloomImpactEntity missing from exact artifact")
    p = subprocess.run(
        ["javap", "-p", "-s", "-c", "-classpath", str(jar.resolve()), FQCN],
        check=False, capture_output=True, text=True, timeout=50
    )
    if p.returncode or not p.stdout or len(p.stdout) > 1_000_000:
        raise GateError("bounded javap failed")
    parsed = parse_javap(isolate_named_methods(p.stdout), "FuneralBloomImpactEntity",
                         focus_pattern=FOCUS_ALL)
    result = summarize(parsed)
    if hashlib.sha1(jar.read_bytes()).hexdigest() != digest:
        raise GateError("physical artifact changed during audit")
    for method in result["methods"]:
        print("SOMAKE_IMPACT_METHOD", method["method"], method["descriptor"],
              "branches", method["branches"], "members", len(method["members"]))
        if method["members"]:
            print("SOMAKE_IMPACT_REFS", method["method"], json.dumps(method["members"]))
    print("SOMAKE_IMPACT_CATEGORIES", json.dumps(result["categories_by_method"], sort_keys=True))
    return {
        "status": "PASS_STATIC_IMPACT_METHOD_SYMBOLS_ONLY",
        "evidence": "SOMAKE_1_0_9_SHA_EXACT_FUNERAL_IMPACT_ENTITY",
        "mod_id": "somakespells",
        "version": "1.0.9",
        "sha1": digest,
        "class": FQCN,
        **result,
        "limitations": [
            "Symbolic references and branches do not establish runtime behavior, reachability, damage, healing, or collision.",
            "No confirmed API or hook for per-player mutation of effects by perks.",
            "No tested client, multiplayer, provider-loaded, Survival, configuration, or Stage acceptance.",
            "No third-party implementation, JAR, bytecode, text, or asset exported.",
        ],
    }

def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("--jar", required=True, type=Path)
    a.add_argument("--output", required=True, type=Path)
    args = a.parse_args()
    result = inspect(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SOMAKE_IMPACT_GATE", result["status"], result["sha1"], result["named_methods"])

if __name__ == "__main__":
    main()
