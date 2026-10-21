#!/usr/bin/env python3
"""SHA-exact Somake 1.0.9 downstream entity JVM-symbol audit.

Read-only interoperability evidence: method signatures and symbolic member references.
This does not establish path reachability, live effects, values or public perk hooks.
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

ENTITIES = {
    "fragmented_requiem": "com.somake.somakespells.entity.FragmentedSwordRainEntity",
    "funeral_bloom": "com.somake.somakespells.entity.FuneralBloomControllerEntity",
    "withered_rose_vortex": "com.somake.somakespells.entity.WitheredRoseVortexEntity",
    "custodia_caeli": "com.somake.somakespells.entity.CustodiaCaeliSigilEntity",
    "jingle_bell": "com.somake.somakespells.entity.BellEntity",
}
INDICATORS = {
    "damage": ("DamageSources", "SpellDamageEvent", "applyDamage:", "DamageSource", ".hurt:", "doHurt:", "damageSources:"),
    "entity_targets": ("getEntitiesOfClass:", "getEntities:", "getEntitiesIn", "AABB.", "distanceToSqr:", "canHitEntity:", "canAttack:"),
    "status_effect": ("MobEffectInstance", ".addEffect:", "MobEffects.", "WITHER", "Potion"),
    "healing": ("SpellHealEvent", ".heal:", "getHealing:", "HEALTH"),
    "lifecycle": (".discard:", ".remove:", "shouldBeSaved:", "tickCount:", "getLifetime", "remainingTicks:", ".kill:"),
    "ownership": (".getOwner:", ".getCaster:", "getOwnerUUID:", ".isAlliedTo:", ".isAllied:", "isSpectator:"),
    "world": ("ExplosionEvent", ".explode:", "mobGriefing", ".setBlock:", "Level.destroyBlock:"),
}
ENTITY_FOCUS = re.compile(
    r"^(?:on|get|set|tick|apply|spawn|should|lambda\$|pulse|launch|cancel|prune|"
    r"trigger|find|resolve|finish|process|handle|check|is|can|select|do|perform|"
    r"remove|update|expire|hurt|damage|heal|move|pull)", re.I)
MAX_BYTES = 20_000_000
MAX_MEMBERS_PER_ENTITY = 400

def indicators(methods: list[dict]) -> dict[str, list[str]]:
    """Candidate method names where recognized JVM member references appear."""
    if not isinstance(methods, list):
        raise GateError("invalid method list")
    result: dict[str, list[str]] = {category: [] for category in INDICATORS}
    for record in methods:
        if not isinstance(record, dict) or not isinstance(record.get("members"), list):
            raise GateError("invalid method record")
        name = record.get("method", "")
        for category, tokens in INDICATORS.items():
            if any(any(token in symbol for token in tokens) for symbol in record["members"]):
                if name not in result[category]:
                    result[category].append(name)
    return result

def summarize(parsed: dict) -> dict:
    methods = parsed["methods"]
    if sum(len(x["members"]) for x in methods) > MAX_MEMBERS_PER_ENTITY:
        raise GateError("entity symbol budget exceeded; split bounded audit instead")
    groups = indicators(methods)
    return {
        "declared_methods": parsed["declared_methods"],
        "focus_methods": parsed["focused_methods"],
        "methods": methods,
        "other_declared": parsed["other_declared"],
        "indicator_methods": groups,
        "limits": [
            "A symbolic member reference does not establish branch reachability or effective runtime invocation.",
            "No inference of numeric formula, target/range units, attack count or mutation hook.",
            "Indicator categories are method-reference hints, not verified gameplay classifications.",
        ],
    }

def inspect(jar: Path) -> dict:
    if jar.name != FILENAME or not jar.is_file() or jar.is_symlink():
        raise GateError("wrong artifact path/type")
    stat = jar.stat()
    if not 100 < stat.st_size < MAX_BYTES:
        raise GateError("unexpected JAR byte length")
    data = jar.read_bytes()
    digest = hashlib.sha1(data).hexdigest()
    if digest != SHA1:
        raise GateError(f"physical SHA-1 mismatch: {digest}")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise GateError("duplicate member in signed artifact")
        metadata = archive.read("META-INF/neoforge.mods.toml")
        if len(metadata) > 250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]", metadata):
            raise GateError("provider modId mismatch")
        for spell_id, classname in ENTITIES.items():
            if classname.replace(".", "/") + ".class" not in names:
                raise GateError(f"exact downstream entity class missing: {spell_id}")

    rows: dict[str, dict] = {}
    for spell_id, classname in ENTITIES.items():
        proc = subprocess.run(["javap", "-c", "-s", "-p", "-classpath", str(jar.resolve()), classname],
                              capture_output=True, text=True, timeout=40, check=False)
        if proc.returncode or not proc.stdout or len(proc.stdout) > 1_000_000:
            raise GateError("javap failed or oversized for " + spell_id)
        parsed = parse_javap(proc.stdout, classname.rsplit(".", 1)[-1], focus_pattern=ENTITY_FOCUS)
        row = summarize(parsed)
        rows[spell_id] = {"fqcn": classname, **row}
        print("SOMAKE_ENTITY", spell_id, classname, "methods", row["declared_methods"],
              "focused", row["focus_methods"])
        print("SOMAKE_ENTITY_METHODS", spell_id,
              ",".join(f"{x['method']}{x['descriptor']}" for x in row["methods"]))
        print("SOMAKE_ENTITY_INDICATORS", spell_id, json.dumps(row["indicator_methods"], sort_keys=True))
        # Print a bounded narrow subset; JSON artifact retains all symbolic references.
        for method in row["methods"]:
            if any(method["method"] in names for names in row["indicator_methods"].values()):
                key = [symbol for symbol in method["members"]
                       if any(token in symbol for tokens in INDICATORS.values() for token in tokens)]
                if key:
                    print("SOMAKE_ENTITY_REFS", spell_id, method["method"], json.dumps(key[:36]))

    if hashlib.sha1(jar.read_bytes()).hexdigest() != digest:
        raise GateError("artifact bytes changed during inspection")
    return {
        "evidence": "EXACT_SHA1_ENTITY_METHOD_SYMBOLS_NOT_GAMEPLAY",
        "status": "PASS_STATIC_ENTITY_REFERENCE_DISCOVERY",
        "mod_id": "somakespells", "version": "1.0.9", "sha1": digest,
        "entity_classes": len(rows), "results": rows,
        "boundary": [
            "Provider JAR inspected read-only; no third-party bytecode/assets/source included.",
            "No confirmed player-specific perk setter, runtime cast/hit count, damage or cooldown.",
            "Do not interpret absence of a symbol in a declared method as proof that a delegated effect is absent.",
        ],
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SOMAKE_ENTITY_GATE", result["status"], result["entity_classes"], result["sha1"])

if __name__ == "__main__":
    main()
