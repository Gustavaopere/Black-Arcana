#!/usr/bin/env python3
"""Reproducible exact-binary Sea Swing static *catalog* evidence (read-only).

This probe cannot certify mutation hooks, physical modpack QA, actual accepted
damage/spawns, or a complete Minecraft lifecycle. SHA-pinned JVM instructions
are interoperability locators, not copied implementation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ITEM = BASE + "server/item/OrtholanceItem.class"
WAVE = BASE + "server/entity/item/WaveEntity.class"
LANG = "assets/alexscaves/lang/en_us.json"
DISCOVERY = "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SEA-SWING-DISCOVERY-1.0.10.json"
METHODS = {
    ITEM: ("hurtEnemy", "acHurtEnemy"),
    WAVE: ("getOwner", "setOwner", "defineSynchedData", "getDimensions",
           "onSyncedDataUpdated", "readAdditionalSaveData",
           "addAdditionalSaveData", "getLifespan", "setLifespan",
           "getWaitingTicks", "setWaitingTicks", "getWaveScale",
           "setWaveScale", "isSlamming", "setSlamming", "tick", "attackEntities"),
}
MAX_INS = 950
MAX_TOTAL_INS = 1300
MAX_JAR_LANG_SIZE = 300000

def require(ok: bool, reason: str):
    if not ok:
        raise ValueError(reason)

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def compact(ins: dict) -> dict:
    return {key: ins[key] for key in ("offset", "opcode", "operand", "symbol")}

def select_full(methods: list, names: tuple[str, ...]) -> dict:
    selected = {}
    for method in methods:
        name = name_of(method)
        if name not in names:
            continue
        require(name not in selected, "ambiguous method overload: " + name)
        ins = method["instructions"]
        require(1 <= len(ins) <= MAX_INS, "method exceeds bounded audit: " + name)
        offsets = [i["offset"] for i in ins]
        require(offsets == sorted(set(offsets)), "invalid offset sequence: " + name)
        selected[name] = {
            "descriptor": method["descriptor"], "instruction_count": len(ins),
            "parsed_method_sha256": digest_method(method),
            "instructions": [compact(i) for i in ins],
        }
    require(set(selected) == set(names),
            "missing exact Wave/Ortholance methods: " + str(sorted(set(names)-set(selected))))
    return selected

def check_dependency(discovery: dict, computed: dict) -> None:
    require(discovery.get("scope") == "UNSEALED_SEA_SWING_1010_JVM_DISCOVERY",
            "unexpected baseline discovery scope")
    require(computed["artifact"]["sha1"] == discovery["artifact"]["sha1"]
            and computed["artifact"]["sha256"] == discovery["artifact"]["sha256"],
            "publisher provenance mismatch")
    require(computed["class_sha256"] == discovery["class_sha256"],
            "classfiles differ from prior audited Sea Swing discovery")
    require(computed["enchantment"] == discovery["enchantment"],
            "enchantment resource mutated after discovery")
    for owner in discovery["consumers"]:
        actual = computed["methods"][owner["owner"]]
        for previous in owner["methods"]:
            current = actual[previous["name"]]
            require(current["parsed_method_sha256"] == previous["parsed_method_sha256"]
                    and current["instruction_count"] == previous["instruction_count"],
                    "prior exact method evidence drift: " + previous["name"])
            ins = {i["offset"]: i for i in current["instructions"]}
            for pivot in previous["pivots"]:
                for window in pivot["windows"]:
                    for expected in window:
                        require(ins.get(expected["offset"]) == expected,
                                "prior exact JVM window drift: " + previous["name"])

def compiled_static_boundaries(doc: dict) -> None:
    item = doc["methods"][ITEM]["acHurtEnemy"]["instructions"]
    wave = doc["methods"][WAVE]["attackEntities"]["instructions"]
    tick = doc["methods"][WAVE]["tick"]["instructions"]
    def at(items, offset):
        found = [x for x in items if x["offset"] == offset]
        require(len(found) == 1, "missing bytecode anchor: " + str(offset))
        return found[0]
    require("SEA_SWING" in at(item, 17)["symbol"], "producer enchantment gate missing")
    require((at(item, 23)["opcode"], at(item, 23)["operand"]) == ("ifle", "97"),
            "producer gate branch changed")
    require(at(item, 59)["opcode"] == "iconst_5", "wave lifespan 5 not observed")
    require("addFreshEntity" in at(item, 93)["symbol"]
            and at(item, 96)["opcode"] == "pop",
            "spawn request/unchecked boolean boundary changed")
    require("AABB.inflate" in at(wave, 13)["symbol"]
            and at(wave, 4)["symbol"].endswith("0.5d"),
            "damage candidate AABB boundary changed")
    require("mobProjectile" in at(wave, 26)["symbol"], "damage source changed")
    require("LivingEntity.hurt" in at(wave, 123)["symbol"]
            and at(wave, 126)["opcode"] == "pop",
            "damage acceptance boundary changed")
    require("knockback" in at(wave, 169)["symbol"],
            "wave knockback downstream boundary changed")
    require("getWaitingTicks" in at(tick, 13)["symbol"]
            and at(tick, 44)["opcode"] == "return",
            "initial wait boundary changed")
    require("attackEntities" in at(tick, 527)["symbol"],
            "per-tick area attack call changed")
    require("getLifespan" in at(tick, 575)["symbol"],
            "wave lifespan settlement changed")

def audit(jar: Path, javap_bin: str, prior: Path) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR SHA mismatch")
    discovery_raw = prior.read_bytes()
    require(1000 <= len(discovery_raw) <= 250000, "unbounded discovery dependency")
    discovery = json.loads(discovery_raw)
    with zipfile.ZipFile(jar) as archive:
        filenames = archive.namelist()
        require(len(filenames) == len(set(filenames)), "duplicated JAR member")
        require(LANG in filenames, "missing shipped language resource")
        raw = archive.read(LANG)
        require(100 < len(raw) <= MAX_JAR_LANG_SIZE, "language resource size drift")
        strings = json.loads(raw)
        translations = {}
        for key in ("enchantment.alexscaves.sea_swing",
                    "enchantment.alexscaves.sea_swing.desc"):
            value = strings.get(key)
            require(isinstance(value, str) and bool(value.strip()),
                    "missing publisher Sea Swing localization: " + key)
            translations[key] = value
        class_digests = {}
        for owner in discovery["class_sha256"]:
            require(owner in filenames, "missing classfile: " + owner)
            class_digests[owner] = sha(archive.read(owner))
    result = {
        "schema_version": 1,
        "scope": "SEA_SWING_SHA_EXACT_STATIC_CATALOG_EVIDENCE_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "discovery_sha256": sha(discovery_raw),
        "enchantment": discovery["enchantment"],
        "item_tag": discovery["item_tag"],
        "class_sha256": {**discovery["class_sha256"]},
        "language": {"path": LANG, "sha256": sha(raw), "translations": translations},
        "methods": {},
        "limits": {
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "actual_spawn_success": "NOT_VERIFIED",
            "actual_damage_acceptance": "NOT_TESTED",
            "third_party_protection_and_pvp": "NOT_TESTED",
            "complete_gameplay_lifecycle": "NOT_TESTED",
            "mutation": "NO_MUTATION",
        },
    }
    require(class_digests == result["class_sha256"],
            "classfiles drifted against first audit")
    total = 0
    for owner, required in METHODS.items():
        methods = parse_methods(javap(javap_bin, jar, owner[:-6].replace("/", ".")))
        selected = select_full(methods, required)
        total += sum(x["instruction_count"] for x in selected.values())
        require(total <= MAX_TOTAL_INS, "total selected bytecode exceeds budget")
        result["methods"][owner] = selected
    check_dependency(discovery, result)
    compiled_static_boundaries(result)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--discovery", type=Path, default=Path(DISCOVERY))
    p.add_argument("--seal", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = audit(args.jar, args.javap, args.discovery)
    if args.seal is not None:
        require(result == json.loads(args.seal.read_text(encoding="utf8")),
                "Sea Swing static contract seal drift")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n",
                               encoding="utf8")
    print(json.dumps({
        "artifact": result["artifact"], "translations": result["language"]["translations"],
        "method_instruction_counts": {owner: {n: m["instruction_count"]
                                    for n, m in methods.items()}
                                      for owner, methods in result["methods"].items()},
        "status": "STATIC_EVIDENCE_ONLY_NOT_PERK_HOOK_OR_PHYSICAL_QA",
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
