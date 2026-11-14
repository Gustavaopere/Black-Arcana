#!/usr/bin/env python3
"""Read-only individual Dark Nock 1.0.10 causal census.

The full publisher hash, each relevant class hash, selected compiled methods
and the original Dreadbow manifest are prerequisites. This audit makes no
gameplay, source-version-parity or mutating-hook claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods
)
from alexscaves_1010_dreadbow_decision_probe import method_digest

BASE = "com/github/alexmodguy/alexscaves/"
ITEM = BASE + "server/item/DreadbowItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
RESOURCE = "data/alexscaves/enchantment/dark_nock.json"
RELENTLESS = "data/alexscaves/enchantment/relentless_darkness.json"
TAG = "data/alexscaves/tags/item/enchantable/dreadbow.json"
RESOURCE_SHA = "569cb5857db11189b2eb8a1163d53a440587ab02e2f14bc8296aaaf91dcd8033"
EXPECTED = (
    "getMaxLoadTime", "getPowerForTime", "getPullingAmount",
    "acInventoryTick", "releaseUsing", "onUseTick", "use",
    "getUseDuration", "getLerpedUseTime", "getUseTime", "setUseTime",
    "getPerfectShotTicks", "setPerfectShotTicks"
)
# Exact JVM pivots, not extension points or evidence of successful engine effects.
PIVOTS = {
    "getMaxLoadTime": {
        1: ("getstatic", "RELENTLESS_DARKNESS"),
        4: ("invokestatic", "enchantLevel"),
        7: ("ifle", "12"),
        10: ("iconst_5", ""),
        11: ("ireturn", ""),
        12: ("bipush", "40"),
        14: ("bipush", "8"),
        17: ("getstatic", "DARK_NOCK"),
        20: ("invokestatic", "enchantLevel"),
        23: ("imul", ""),
        24: ("isub", ""),
        25: ("ireturn", ""),
    },
    "getPowerForTime": {
        3: ("invokestatic", "getMaxLoadTime"),
        7: ("fdiv", ""),
        11: ("fmul", ""),
        13: ("fconst_2", ""),
        14: ("fmul", ""),
        15: ("fadd", ""),
        16: ("ldc_w", "float 3.0f"),
        19: ("fdiv", ""),
        23: ("fcmpl", ""),
        24: ("ifle", "29"),
        27: ("fconst_1", ""),
        30: ("freturn", ""),
    },
    "getPullingAmount": {
        2: ("invokestatic", "getLerpedUseTime"),
        6: ("invokestatic", "getMaxLoadTime"),
        10: ("fdiv", ""),
        12: ("invokestatic", "Math.min"),
    },
    "releaseUsing": {
        14: ("getstatic", "RELENTLESS_DARKNESS"),
        20: ("ifgt", "899"),
        26: ("invokevirtual", "getUseDuration"),
        37: ("invokestatic", "getPowerForTime"),
        117: ("ifle", "899"),
        203: ("invokestatic", "ProjectileUtil.getHitResultOnViewVector"),
        233: ("invokestatic", "ProjectileUtil.getHitResultOnViewVector"),
        365: ("invokestatic", "Math.ceil"),
        775: ("invokevirtual", "Level.addFreshEntity"),
    },
    "acInventoryTick": {
        39: ("invokevirtual", "Level.isClientSide"),
        42: ("ifeq", "400"),
        149: ("invokestatic", "getMaxLoadTime"),
        184: ("invokestatic", "setUseTime"),
    },
    "onUseTick": {
        23: ("getstatic", "RELENTLESS_DARKNESS"),
        35: ("irem", ""),
        311: ("invokevirtual", "Level.addFreshEntity"),
    },
    "getUseDuration": {0: ("ldc", "int 72000"), 2: ("ireturn", "")},
}

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    o = {}
    for key, value in pairs:
        require(key not in o, "duplicate JSON key: " + key)
        o[key] = value
    return o

def method_for(methods, name: str, desc: str):
    matches = [m for m in methods
               if re.search(r"\b" + re.escape(name) + r"\(", m["header"])
               and m["descriptor"] == desc]
    require(len(matches) == 1, "missing/ambiguous compiled method: " + name)
    return matches[0]

def check_pivots(method: dict, pivots: dict) -> None:
    rows = method["instructions"]
    require(len(rows) == len({r["offset"] for r in rows}),
            "duplicate native bytecode offset")
    at = {r["offset"]: r for r in rows}
    for off, (op, token) in pivots.items():
        row = at.get(off)
        require(row is not None and row["opcode"] == op and
                token in (row["operand"] + " " + row["symbol"]),
                "native causal pivot drift: " + str(off) + " " + token)
    # Direct conditional/goto edges are instruction boundaries, not engine QA.
    for row in rows:
        if row["opcode"].startswith("if") or row["opcode"] in ("goto", "goto_w"):
            require(row["operand"].isdecimal() and int(row["operand"]) in at,
                    "invalid direct branch destination")

def canonical_anchors(method: dict, anchors: list[dict]) -> int:
    rows = {r["offset"]: r for r in method["instructions"]}
    require(len(rows) == len(method["instructions"]), "duplicate native instruction")
    require(1 <= len(anchors) <= 300, "parent anchor budget")
    offsets = set()
    for anchor in anchors:
        off = anchor["offset"]
        require(off not in offsets and off in rows, "missing/duplicate parent offset")
        offsets.add(off)
        for field in ("opcode", "operand", "symbol"):
            require(rows[off][field] == anchor[field],
                    "SHA-exact Dreadbow anchor drift in " + method["header"] +
                    " @" + str(off) + " " + field + ": parent=" +
                    repr(anchor[field]) + " observed=" + repr(rows[off][field]))
    return len(anchors)

def power(ticks: int, maximum: int) -> float:
    require(maximum > 0, "invalid charge denominator")
    x = ticks / maximum
    p = (x * x + 2 * x) / 3
    return min(p, 1.0) if p > 1.0 else p

def first_valid(maximum: int) -> int:
    return next(t for t in range(maximum + 1) if power(t, maximum) > 0.1)

def audit(jar: Path, parent: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR identity mismatch")
    m = json.loads(parent.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)
    require(m["artifact_sha1"] == SHA1 and m["artifact_sha256"] == SHA256
            and m["artifact_size_bytes"] == SIZE,
            "historical Dreadbow manifest mismatch")
    require(m["resources"].get(RESOURCE) == RESOURCE_SHA,
            "Dark Nock fingerprint mismatch in historical manifest")
    expected_class_sha = m["classes"][ITEM]["sha256"]
    records = {x["name"]: x for x in m["classes"][ITEM]["methods"]
               if x["name"] in EXPECTED}
    require(set(records) == set(EXPECTED), "Dreadbow parent method coverage incomplete")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate physical JAR members")
        for owner, entry in m["classes"].items():
            require(sha(z.read(owner)) == entry["sha256"],
                    "parent classfile SHA drift: " + owner)
        require(sha(z.read(RESOURCE)) == RESOURCE_SHA,
                "Dark Nock JAR resource SHA drift")
        for res in (RELENTLESS, TAG):
            require(sha(z.read(res)) == m["resources"][res],
                    "Dreadbow adjacent resource drift: " + res)
        config = json.loads(z.read(RESOURCE), object_pairs_hook=strict_pairs)
        require(config.get("description") ==
                {"translate": "enchantment.alexscaves.dark_nock"}
                and config.get("supported_items") ==
                "#alexscaves:enchantable/dreadbow"
                and config.get("max_level") == 3
                and config.get("weight") == 2
                and config.get("anvil_cost") == 4
                and config.get("slots") == ["mainhand"]
                and "exclusive_set" not in config,
                "published Dark Nock metadata drift")
        for field, base, per_level in (
                ("min_cost", 1, 10), ("max_cost", 41, 10)):
            require(config[field] ==
                    {"base": base, "per_level_above_first": per_level},
                    "Dark Nock enchantment cost metadata drift: " + field)
        tag = json.loads(z.read(TAG), object_pairs_hook=strict_pairs)
        require(tag == {"values": ["alexscaves:dreadbow"]},
                "Dark Nock eligible item tag drift")
        relentless = json.loads(z.read(RELENTLESS),
                               object_pairs_hook=strict_pairs)
        require("alexscaves:dark_nock" in
                relentless.get("exclusive_set", []),
                "Relentless Darkness unilateral exclusion drift")
        token_hits = sorted(path for path in names
                            if path.startswith(BASE) and path.endswith(".class")
                            and b"DARK_NOCK" in z.read(path))
        require(ITEM in token_hits and REG in token_hits and len(token_hits) <= 16,
                "unbounded or missing direct DARK_NOCK compiled owners")
    parsed = parse_methods(javap(javap_bin, jar, ITEM[:-6].replace("/", ".")))
    require(len(parsed) >= len(EXPECTED), "Dreadbow method roster incomplete")
    checked = {}
    for name in EXPECTED:
        old = records[name]
        method = method_for(parsed, name, old["descriptor"])
        count = canonical_anchors(method, old["anchors"])
        check_pivots(method, PIVOTS.get(name, {}))
        checked[name] = {
            "descriptor": method["descriptor"],
            "instruction_count": len(method["instructions"]),
            "parent_anchor_count": count,
            "complete_parsed_method_sha256": method_digest(method),
            "direct_branches": sum(r["opcode"].startswith("if") or
                                   r["opcode"] in ("goto", "goto_w")
                                   for r in method["instructions"]),
        }
    require(sum("DARK_NOCK" in i["symbol"]
                for method in parsed for i in method["instructions"]) == 1,
            "additional native Dreadbow DARK_NOCK callsite")
    charge = [{"level": lev, "max_load_ticks": 40 - 8 * lev,
               "first_nominal_valid_release_tick": first_valid(40 - 8 * lev)}
              for lev in range(4)]
    require([x["first_nominal_valid_release_tick"] for x in charge] ==
            [6, 5, 4, 3], "nominal charge arithmetic drift")
    return {
        "schema_version": 1,
        "claim_scope": "INDIVIDUAL_STATIC_DARK_NOCK_DISCOVERY_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "item_class_sha256": expected_class_sha,
        "resource_sha256": RESOURCE_SHA,
        "parent_manifest_sha256": sha(parent.read_bytes()),
        "resource_config": config,
        "direct_DARK_NOCK_class_token_owners": token_hits,
        "native_method_census": checked,
        "nominal_unmodified_charge": charge,
        "limits": {
            "whole_provider_catalog_closed": False,
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "runtime_server_charge_validation": "NOT_VERIFIED",
            "projectile_spawn_acceptance": "NOT_TESTED",
            "pvp_claims_mastery": "NOT_VERIFIED",
            "data_pack_actual_config": "NOT_VERIFIED",
            "invalid_enchantment_levels": "UNSAFE_UNCERTIFIED",
        },
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    output = audit(args.jar, args.manifest, args.javap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True,
                                     ensure_ascii=False) + "\n", encoding="utf8")
    print("DARK_NOCK_SHA_EXACT_DISCOVERY")
    print("direct_class_tokens=" +
          json.dumps(output["direct_DARK_NOCK_class_token_owners"]))
    print("method_count=" + str(len(output["native_method_census"])))
    print("NO_MUTATION STATIC_DISCOVERY_ONLY")

if __name__ == "__main__":
    main()
