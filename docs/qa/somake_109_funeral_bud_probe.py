#!/usr/bin/env python3
"""Somake 1.0.9: SHA-exact FuneralBloomBudEntity symbolic interoperability audit.

Method descriptors, references and branch counts only. No publisher bytecode,
source bodies, assets or executable third-party artifacts in generated output.
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

FQCN = "com.somake.somakespells.entity.FuneralBloomBudEntity"
FOCUS_ALL_NAMED = re.compile(r"^[A-Za-z_$]")
CATEGORIES = {
    "damage": ("DamageSources.applyDamage:", "LivingEntity.hurt:", "Entity.hurt:",
               "getDamageSource:", "SpellDamageEvent", "DamageSource"),
    "healing": ("SpellHealEvent", "LivingEntity.heal:", "Player.heal:",
                "getHealing:", "getHealth:", "setHealth:"),
    "targets": ("AABB.inflate:", "getEntitiesOfClass:", "getEntities:",
                "distanceToSqr:", "isAlliedTo:", "isSpectator:", "canAttack:"),
    "status": ("MobEffects.WITHER", "MobEffectInstance", ".addEffect:"),
    "lifecycle": ("discard:", "remove:", "getLifetime", "tickCount",
                  "onAntiMagic:", "cancel", "shouldBeSaved:"),
    "ownership": ("getOwner:", "getCaster:", "isAlliedTo:", "getOwnerUUID:",
                  "getUUID:", "ownerUUID", "getServerPlayer:"),
    "world": ("Level.explode:", "Level.setBlock:", "Level.destroyBlock:",
              "mobGriefing", "ExplosionEvent"),
}
MAX_JAR_SIZE = 20_000_000
MAX_REFS = 460

def classify(methods: list[dict]) -> dict[str, list[str]]:
    result = {name: [] for name in CATEGORIES}
    for entry in methods:
        if not isinstance(entry, dict) or not isinstance(entry.get("members"), list):
            raise GateError("malformed method evidence")
        method = entry.get("method")
        if not isinstance(method, str):
            raise GateError("invalid method name")
        for tag, needles in CATEGORIES.items():
            if any(needle in member for member in entry["members"] for needle in needles):
                if method not in result[tag]:
                    result[tag].append(method)
    return result

def summarize(parsed: dict) -> dict:
    methods = parsed["methods"]
    if len(methods) > 140 or sum(len(x["members"]) for x in methods) > MAX_REFS:
        raise GateError("oversized symbol cohort")
    if not methods:
        raise GateError("no named methods captured")
    # Non-public package-private methods or static init can be excluded by
    # javap text parser; do not pretend this is complete runtime call graph.
    return {
        "declared_methods_in_javap_parser": parsed["declared_methods"],
        "named_methods_analyzed": len(methods),
        "other_declared": parsed["other_declared"],
        "methods": methods,
        "candidate_categories": classify(methods),
    }

def inspect(jar: Path) -> dict:
    if jar.is_symlink() or not jar.is_file() or jar.name != FILENAME:
        raise GateError("unexpected publisher JAR path")
    if not 100 < jar.stat().st_size < MAX_JAR_SIZE:
        raise GateError("unexpected publisher JAR size")
    initial_hash = hashlib.sha1(jar.read_bytes()).hexdigest()
    if initial_hash != SHA1:
        raise GateError("Somake physical SHA-1 mismatch")
    with zipfile.ZipFile(jar) as zf:
        if len(set(zf.namelist())) != len(zf.namelist()):
            raise GateError("duplicate ZIP entry")
        metadata = zf.read("META-INF/neoforge.mods.toml")
        if len(metadata) > 250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]", metadata):
            raise GateError("mod ID mismatch")
        if FQCN.replace(".", "/") + ".class" not in zf.namelist():
            raise GateError("FuneralBloomBudEntity missing in exact JAR")
    p = subprocess.run(["javap", "-p", "-s", "-c", "-classpath",
                        str(jar.resolve()), FQCN],
                       capture_output=True, text=True, timeout=50, check=False)
    if p.returncode or len(p.stdout) > 1_000_000 or not p.stdout:
        raise GateError("bounded javap failed")
    data = summarize(parse_javap(p.stdout, "FuneralBloomBudEntity",
                                  focus_pattern=FOCUS_ALL_NAMED))
    if hashlib.sha1(jar.read_bytes()).hexdigest() != initial_hash:
        raise GateError("publisher bytes changed during analysis")
    for method in data["methods"]:
        print("SOMAKE_BUD_METHOD", method["method"], method["descriptor"],
              "branches", method["branches"], "symbol_count", len(method["members"]))
        if method["members"]:
            print("SOMAKE_BUD_REFS", method["method"], json.dumps(method["members"]))
    print("SOMAKE_BUD_CATEGORIES", json.dumps(data["candidate_categories"], sort_keys=True))
    return {
        "status": "PASS_STATIC_BUD_METHOD_SYMBOLS_ONLY",
        "evidence": "EXACT_SHA1_FUNERAL_BLOOM_BUD_JVM_REFERENCES",
        "jar_sha1": initial_hash, "mod_id": "somakespells", "version": "1.0.9",
        "class": FQCN, **data,
        "limits": [
            "Method and callsite presence alone does not demonstrate runtime reachability, branch outcomes, damage, healing, target number or duration.",
            "A published JVM method or setter is not a contract to mutate a player-specific perk.",
            "No gameplay, actual config, client, save/reload or full modpack validation executed.",
            "No third-party implementation, classfile, bytecode, asset or JAR exported.",
        ],
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    result = inspect(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SOMAKE_BUD_GATE", result["status"], result["jar_sha1"],
          result["named_methods_analyzed"])

if __name__ == "__main__":
    main()
