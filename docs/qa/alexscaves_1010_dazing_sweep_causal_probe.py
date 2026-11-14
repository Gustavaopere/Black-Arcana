#!/usr/bin/env python3
"""Exact installed publisher 1.0.10 Dazing Sweep native causal audit.

Read-only: validates the original SHA-pinned effect manifest, compiled method
bodies/branches, explicit attack and effect handoffs and publisher JSON.
A JVM reference is not a verified mutating hook, live damage receipt, accepted
status, physical QA, or a new Black Arcana spell.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods
)
from alexscaves_1010_dreadbow_decision_probe import method_digest
from alexscaves_1010_bouncy_ball_causal_probe import (
    method_switch_tables, branch_edges,
)

BASE = "com/github/alexmodguy/alexscaves/"
CLUB = BASE + "server/item/PrimitiveClubItem.class"
STUN = BASE + "server/potion/StunnedEffect.class"
VISUAL = BASE + "server/message/UpdateEffectVisualityEntityMessage.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
RES = "data/alexscaves/enchantment/dazing_sweep.json"
TAG = "data/alexscaves/tags/item/enchantable/primitive_club.json"
RES_SHA = "c86a7aceb5dfec02083dabc93ab51dc5253fbeb616c013a5f33f343656c26318"
TAG_SHA = "71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43"
CLUB_SHA = "92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac"
STUN_SHA = "1ca7aea9ca512e10f2c06da58093e6197c57645ce2d32fc03cce0869d21a0a9e"
VISUAL_SHA = "4fb1a0200619ce7597470ebd500d6da12bd190a32910bde7ebbc6ac9e9298280"

# Compiled 1.0.10 JVM offsets, NOT a stable modding API.
PIVOTS = {
    (CLUB, "hurtEnemy"): {
        4: ("invokevirtual", "acHurtEnemy"),
    },
    (CLUB, "acHurtEnemy"): {
        6: ("invokestatic", "ACCompat.hurtAndBreak"),
        13: ("invokevirtual", "Level.isClientSide"),
        16: ("ifne", "392"),
        36: ("invokeinterface", "RandomSource.nextFloat"),
        41: ("ldc", "float 0.8f"),
        44: ("ifge", "361"),
        51: ("getstatic", "ACEffectRegistry.STUNNED"),
        65: ("sipush", "150"),
        72: ("sipush", "150"),
        75: ("invokeinterface", "RandomSource.nextInt"),
        84: ("invokespecial", "MobEffectInstance"),
        92: ("invokevirtual", "LivingEntity.addEffect"),
        95: ("ifeq", "361"),
        119: ("invokestatic", "AlexsCaves.sendMSGToAll"),
        136: ("getstatic", "DAZING_SWEEP"),
        139: ("invokestatic", "ACCompat.enchantLevel"),
        146: ("ifle", "361"),
        152: ("ldc", "float 1.2f"),
        170: ("invokestatic", "AABB.ofSize"),
        182: ("invokedynamic", "InvokeDynamic"),
        187: ("invokevirtual", "Level.getEntities"),
        199: ("invokeinterface", "Iterator.hasNext"),
        204: ("ifeq", "361"),
        222: ("invokevirtual", "Entity.is"),
        225: ("ifne", "358"),
        231: ("invokevirtual", "Entity.isAlliedTo"),
        234: ("ifne", "358"),
        240: ("invokevirtual", "Entity.distanceTo"),
        246: ("ifgt", "358"),
        251: ("instanceof", "LivingEntity"),
        254: ("ifeq", "358"),
        268: ("getstatic", "ACEffectRegistry.STUNNED"),
        282: ("bipush", "80"),
        288: ("bipush", "80"),
        299: ("invokespecial", "MobEffectInstance"),
        315: ("invokevirtual", "DamageSources.mobAttack"),
        318: ("fconst_1", ""),
        319: ("invokevirtual", "LivingEntity.hurt"),
        322: ("pop", ""),
        327: ("invokevirtual", "LivingEntity.addEffect"),
        330: ("ifeq", "358"),
        355: ("invokestatic", "AlexsCaves.sendMSGToAll"),
        358: ("goto", "197"),
    },
}
METHODS = {
    CLUB: ("acHurtEnemy", "hurtEnemy"),
    STUN: ("shouldTick", "tick"),
    VISUAL: ("handle",),
}
CLASS_SHAS = {CLUB: CLUB_SHA, STUN: STUN_SHA, VISUAL: VISUAL_SHA}

def require(ok: bool, reason: str):
    if not ok:
        raise ValueError(reason)

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def unique_pairs(pairs):
    result = {}
    for key, val in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = val
    return result

def normalized_operand(value: str) -> str:
    # javap can print the same invokeinterface operand as '#110, 1' or
    # '#110,  1'; exact JAR+class hashes still guard binary identity.
    return " ".join(value.split())

def match_previous(method, anchors):
    rows = method["instructions"]
    require(1 <= len(rows) <= 2500, "unbounded declared method")
    offsets = [r["offset"] for r in rows]
    require(len(offsets) == len(set(offsets)), "duplicate JVM instruction offset")
    by = {r["offset"]: r for r in rows}
    seen = set()
    require(1 <= len(anchors) <= 450, "parent evidence unbounded")
    for anchor in anchors:
        offset = anchor["offset"]
        require(offset not in seen and offset in by, "missing/duplicate parent JVM offset")
        seen.add(offset)
        native = by[offset]
        require(native["opcode"] == anchor["opcode"] and
                normalized_operand(native["operand"]) ==
                normalized_operand(anchor["operand"]) and
                native["symbol"] == anchor["symbol"],
                "previous publisher JVM window drift: " + method["header"] +
                " @" + str(offset))
    require(len(anchors) == len(rows), "previous JVM roster not full-method evidence")
    return len(rows)

def check_pivots(method, expected):
    by = {r["offset"]: r for r in method["instructions"]}
    for offset, (opcode, token) in expected.items():
        row = by.get(offset)
        require(row is not None and row["opcode"] == opcode and
                token in (row["operand"] + " " + row["symbol"]),
                "native Dazing Sweep pivot drift: " + method["header"] + " @" + str(offset))

def check_direct_cfg(method, javap_text=None):
    """Reconstruct native if/goto and every javap switch case/default edge."""
    if javap_text is None:
        require(not any(r["opcode"] in ("tableswitch", "lookupswitch")
                        for r in method["instructions"]),
                "unhandled JVM switch without method disassembly")
        switches = []
    else:
        switches = method_switch_tables(method, javap_text)
    edges = branch_edges(method, switches)
    return len(edges), switches

def select_declared(methods, name, descriptor):
    matches = [m for m in methods
               if re.search(r"\b" + re.escape(name) + r"\(", m["header"])
               and m["descriptor"] == descriptor]
    require(len(matches) == 1, "missing or ambiguous native method: " + name)
    return matches[0]

def check_config(config):
    require(isinstance(config, dict) and config.get("description") ==
            {"translate": "enchantment.alexscaves.dazing_sweep"},
            "Dazing Sweep resource identity drift")
    require(config.get("supported_items") == "#alexscaves:enchantable/primitive_club"
            and config.get("weight") == 2 and config.get("max_level") == 2
            and config.get("anvil_cost") == 4 and config.get("slots") == ["mainhand"]
            and "exclusive_set" not in config, "Dazing Sweep metadata drift")
    for field, base in (("min_cost", 1), ("max_cost", 41)):
        require(config.get(field) ==
                {"base": base, "per_level_above_first": 10},
                "Dazing Sweep enchanting costs drift: " + field)

def audit(jar: Path, manifest_path: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "installed 1.0.10 publisher artifact differs")
    raw = manifest_path.read_bytes()
    prior = json.loads(raw, object_pairs_hook=unique_pairs)
    require(prior["artifact_sha1"] == SHA1 and
            prior["artifact_sha256"] == SHA256 and
            prior["artifact_size_bytes"] == SIZE and
            prior["resources"][RES] == RES_SHA and
            prior["resources"][TAG] == TAG_SHA,
            "canonical previous effects manifest identity drift")
    for owner, expected_sha in CLASS_SHAS.items():
        require(prior["classes"][owner]["sha256"] == expected_sha,
                "previous classfile identity drift")
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate physical JAR member")
        for owner, entry in prior["classes"].items():
            require(sha(arc.read(owner)) == entry["sha256"],
                    "historical effect class SHA mismatch: " + owner)
        for p in (RES, TAG):
            require(sha(arc.read(p)) == prior["resources"][p],
                    "Dazing Sweep exact resource SHA mismatch: " + p)
        config = json.loads(arc.read(RES), object_pairs_hook=unique_pairs)
        check_config(config)
        tag = json.loads(arc.read(TAG), object_pairs_hook=unique_pairs)
        require(tag == {"values": ["alexscaves:primitive_club"]},
                "Primitive Club eligible tag mismatch")
        owners = sorted(p for p in names if p.startswith(BASE) and p.endswith(".class")
                        and b"DAZING_SWEEP" in arc.read(p))
        require(REG in owners and CLUB in owners and len(owners) <= 12,
                "unbounded/missing native DAZING_SWEEP references")
        require(b"canBeHitByProjectile" in arc.read(CLUB),
                "compiled Dazing Sweep predicate bootstrap constant absent")
    native = {}
    for owner, names in METHODS.items():
        disassembly = javap(javap_bin, jar, owner[:-6].replace("/", "."))
        compiled = parse_methods(disassembly)
        from_parent = prior["classes"][owner]["methods"]
        covered = {}
        for name in names:
            matches = [v for v in from_parent if v["name"] == name]
            require(len(matches) == 1, "missing/ambiguous parent consumer " + owner + ":" + name)
            old = matches[0]
            method = select_declared(compiled, name, old["descriptor"])
            count = match_previous(method, old["anchors"])
            check_pivots(method, PIVOTS.get((owner, name), {}))
            branch_count, switches = check_direct_cfg(method, disassembly)
            covered[name] = {
                "descriptor": old["descriptor"],
                "full_method_parsed_sha256": method_digest(method),
                "instruction_count": count,
                "direct_branch_count": branch_count,
                "validated_switch_tables": switches,
                "prior_anchor_count": len(old["anchors"]),
            }
        native[owner] = covered
    all_club = parse_methods(javap(javap_bin, jar, CLUB[:-6].replace("/", ".")))
    direct_calls = sum("DAZING_SWEEP" in r["symbol"]
                       for method in all_club for r in method["instructions"])
    require(direct_calls == 1, "unexpected second PrimitiveClub DAZING_SWEEP lookup")
    return {
        "schema_version": 1,
        "claim_scope": "INDIVIDUAL_STATIC_DAZING_SWEEP_CAUSAL",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "parent_manifest_sha256": sha(raw),
        "resource_sha256": RES_SHA,
        "tag_sha256": TAG_SHA,
        "native_DAZING_SWEEP_class_tokens": owners,
        "class_sha256": CLASS_SHAS,
        "consumer_methods": native,
        "nominal_geometry": [
            {"level": lev, "aabb_side": float(lev + 1.2),
             "aabb_half_side": float((lev + 1.2) / 2),
             "distance_filter": float(lev + 1.2)}
            for lev in (1, 2)],
        "primary": {"rng_gate": "nextFloat()<0.8F",
                    "requested_stunned_ticks": [150, 299],
                    "requires_primary_addEffect_accepted": True},
        "secondary": {"requested_stunned_ticks": [80, 159],
                      "requested_damage": 1.0,
                      "damage_source": "DamageSources.mobAttack(attacker)",
                      "damage_boolean_discarded_before_status": True,
                      "status_notification_only_after_addEffect_accepted": True,
                      "separate_proc_probability": False,
                      "explicit_numeric_candidate_budget": False},
        "limits": {
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "whole_provider_closed": False,
            "server_effect_acceptance": "NOT_TESTED",
            "world_claim_and_pvp": "NOT_VERIFIED",
            "external_classpath_and_engine": "NOT_VERIFIED",
            "mastery_settlement_and_dedupe": "NOT_VERIFIED",
            "invalid_level_behavior": "NOT_TESTED",
        },
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--seal", type=Path)
    args = p.parse_args()
    obj = audit(args.jar, args.manifest, args.javap)
    report = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) +
              "\n").encode("utf8")
    if args.seal:
        seal = json.loads(args.seal.read_text(encoding="utf8"),
                          object_pairs_hook=unique_pairs)
        expected = {
            "schema_version": 1, "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "artifact": obj["artifact"],
            "parent_manifest_sha256": obj["parent_manifest_sha256"],
            "full_report_sha256": sha(report),
            "resource_sha256": RES_SHA,
            "tag_sha256": TAG_SHA,
            "native_DAZING_SWEEP_class_tokens": obj["native_DAZING_SWEEP_class_tokens"],
            "class_sha256": obj["class_sha256"],
            "consumer_method_sha256": {
                owner: {name: data["full_method_parsed_sha256"]
                        for name, data in methods.items()}
                for owner, methods in obj["consumer_methods"].items()},
            "consumer_instruction_counts": {
                owner: {name: data["instruction_count"]
                        for name, data in methods.items()}
                for owner, methods in obj["consumer_methods"].items()},
            "consumer_direct_branch_counts": {
                owner: {name: data["direct_branch_count"]
                        for name, data in methods.items()}
                for owner, methods in obj["consumer_methods"].items()},
            "consumer_validated_switch_tables": {
                owner: {name: data["validated_switch_tables"]
                        for name, data in methods.items()}
                for owner, methods in obj["consumer_methods"].items()},
            "nominal_geometry": obj["nominal_geometry"],
            "limits": obj["limits"],
        }
        require(seal == expected, "Dazing Sweep individual full report seal drift")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(report)
    print("DAZING_SWEEP_1010_CAUSAL")
    print("owners=" + json.dumps(obj["native_DAZING_SWEEP_class_tokens"]))
    print("methods=" + str(sum(map(len, obj["consumer_methods"].values()))))
    print("instructions=" + str(sum(m["instruction_count"]
        for ms in obj["consumer_methods"].values() for m in ms.values())))
    print("branches=" + str(sum(m["direct_branch_count"]
        for ms in obj["consumer_methods"].values() for m in ms.values())))
    print("report_sha256=" + sha(report))
    print("STATIC_ONLY NO_MUTATION NOT_TESTED")

if __name__ == "__main__":
    main()
