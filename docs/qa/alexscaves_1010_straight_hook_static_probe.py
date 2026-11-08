#!/usr/bin/env python3
"""Read-only, fail-closed Alex's Caves 1.0.10 Straight Hook JAR discovery.

Captures bounded clean-room JVM witnesses and validates the complete gravity CFG.
Static certification requires the sealed manifest, dossier and seven-axis ledger;
no mutating hook, runtime mutation or physical QA is certified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, sha_file, javap, parse_methods,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ID = "alexscaves:straight_hook"
ENCH = "data/alexscaves/enchantment/straight_hook.json"
TAG = "data/alexscaves/tags/item/enchantable/candy_cane_hook.json"
LANG = "assets/alexscaves/lang/en_us.json"
HOOK = BASE + "server/entity/item/CandyCaneHookEntity.class"
ITEM = BASE + "server/item/CandyCaneHookItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
HOOK_SHA = "e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8"
ITEM_SHA = "d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44"
TAG_SHA = "b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310"
PIVOTS = ("STRAIGHT_HOOK", "RESISTS_GRAVITY", "getGravity:", "isNoGravity:",
          "setNoGravity:", "hasNoGravity:", "getDeltaMovement:", "setDeltaMovement:")
MAX_REPORT_BYTES = 110000


def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def window(method: dict, needle: str, per_method: int = 3) -> list[dict]:
    ins = method["instructions"]
    hits = [i for i, x in enumerate(ins) if needle in x["symbol"]]
    require(len(hits) < 60, "unbounded JVM pivot census: " + needle)
    return [
        {"pivot": needle, "offset": ins[i]["offset"], "matching_instructions": len(hits),
         "instructions": [
             {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}
             for row in (ins if len(ins) <= 40 else ins[max(0, i - 8):min(len(ins), i + 13)])
         ]}
        for i in hits[:per_method]
    ]


def collect_methods(javap_bin: str, jar: Path, member: str) -> dict:
    parsed = parse_methods(javap(javap_bin, jar, member[:-6].replace("/", ".")))
    require(6 <= len(parsed) <= 170, "unexpected method census " + member)
    all_methods = []
    witnesses = []
    for m in parsed:
        name = name_of(m)
        ins = m["instructions"]
        if not ins:
            continue
        positions = [x["offset"] for x in ins]
        require(positions == sorted(set(positions)),
                "duplicate or unordered JVM offsets in " + name)
        require(len(ins) <= 2400, "method too long: " + name)
        meth = {"name": name, "descriptor": m["descriptor"],
                "instructions": len(ins), "parsed_sha256": digest_method(m)}
        all_methods.append(meth)
        pivots = []
        for needle in PIVOTS:
            if needle in ("getDeltaMovement:", "setDeltaMovement:") and name not in (
                    "CandyCaneHookEntity", "tick", "fling", "onHitEntity", "onHitBlock"):
                continue
            pivots.extend(window(m, needle))
        if pivots:
            require(len(pivots) <= 35, "too many method windows: " + name)
            witnesses.append({**meth, "windows": pivots})
    require(len(witnesses) <= 35, "unbounded method witnesses")
    return {"method_count": len(parsed), "methods_with_code": all_methods,
            "bounded_pivot_witnesses": witnesses}



def certify_compiled_branches(hook: dict) -> dict:
    """Verify the entire small gravity CFG and exact enchantment toggle branch."""
    methods = hook["bounded_pivot_witnesses"]
    gravity = [m for m in methods if m["name"] == "getDefaultGravity"
               and m["descriptor"] == "()D"]
    require(len(gravity) == 1 and gravity[0]["instructions"] == 20,
            "missing unique compiled gravity override")
    witnesses = [w for w in gravity[0]["windows"] if w["pivot"] == "RESISTS_GRAVITY"]
    require(len(witnesses) == 1, "gravity field read not proven")
    ins = witnesses[0]["instructions"]
    require(len(ins) == 20, "gravity CFG must be complete")
    by_offset = {row["offset"]: row for row in ins}
    require(len(by_offset) == len(ins), "duplicate gravity JVM offset")
    required = {
        1: ("invokevirtual", "isReeling:()Z", None),
        4: ("ifne", None, "40"),
        11: ("getstatic", "RESISTS_GRAVITY", None),
        23: ("ifeq", None, "44"),
        30: ("invokevirtual", "horizontalDistance:()D", None),
        33: ("ldc2_w", "double 0.05000000074505806d", None),
        37: ("ifle", None, "44"),
        40: ("dconst_0", None, None),
        41: ("goto", None, "47"),
        44: ("ldc2_w", "double 0.07999999821186066d", None),
        47: ("dreturn", None, None),
    }
    for offset, (opcode, symbol, operand) in required.items():
        row = by_offset.get(offset)
        require(row is not None and row["opcode"] == opcode
                and (symbol is None or symbol in row["symbol"])
                and (operand is None or row["operand"] == operand),
                "exact 1.0.10 gravity CFG mismatch at " + str(offset))
    constructors = [m for m in methods if m["name"] == "CandyCaneHookEntity"
                    and "Lnet/minecraft/world/item/ItemStack;" in m["descriptor"]]
    require(len(constructors) == 1, "no unique owner/stack constructor")
    ctor = constructors[0]
    rows = {row["offset"]: row for w in ctor["windows"]
            for row in w["instructions"]}
    init = {
        437: ("getstatic", "STRAIGHT_HOOK", None),
        440: ("invokestatic", "ACCompat.enchantLevel:", None),
        443: ("ifle", None, "460"),
        450: ("getstatic", "RESISTS_GRAVITY", None),
        453: ("iconst_1", None, None),
        457: ("invokevirtual", "SynchedEntityData.set:", None),
    }
    for offset, (opcode, symbol, operand) in init.items():
        row = rows.get(offset)
        require(row is not None and row["opcode"] == opcode
                and (symbol is None or symbol in row["symbol"])
                and (operand is None or row["operand"] == operand),
                "exact Straight Hook constructor branch mismatch at " + str(offset))
    return {
        "method": "CandyCaneHookEntity.getDefaultGravity()D",
        "parsed_method_sha256": gravity[0]["parsed_sha256"],
        "zero_gravity_when_reeling": True,
        "zero_gravity_when_straight_hook_and_horizontal_speed_gt": "0.05000000074505806",
        "otherwise_return_gravity": "0.07999999821186066",
        "enchant_toggle": "level > 0 on launch stack sets RESISTS_GRAVITY=true",
        "strictly_compiled_return_not_physical_gameplay": True,
    }


def audit(jar: Path, javap_bin: str) -> dict:
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "SHA1/SHA256/size mismatch: not the publisher 1.0.10 artifact")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate archive entries")
        for path in (ENCH, TAG, LANG, HOOK, ITEM, REG):
            require(path in names, "required 1.0.10 JAR member missing: " + path)
        hashes = {p: digest(z.read(p)) for p in (ENCH, TAG, LANG, HOOK, ITEM, REG)}
        require(hashes[HOOK] == HOOK_SHA and hashes[ITEM] == ITEM_SHA and
                hashes[TAG] == TAG_SHA, "prior individually audited bytes drift")
        raw_ench, raw_tag = z.read(ENCH), z.read(TAG)
        require(0 < len(raw_ench) <= 12000 and len(raw_tag) <= 12000,
                "enchantment or tag JSON out of bounds")
        enchant, tag = json.loads(raw_ench), json.loads(raw_tag)
        require(enchant.get("description", {}).get("translate") ==
                "enchantment.alexscaves.straight_hook", "wrong enchant identity")
        require(enchant.get("supported_items") ==
                "#alexscaves:enchantable/candy_cane_hook",
                "unrecognized supported-items tag")
        require("alexscaves:candy_cane_hook" in tag.get("values", []),
                "item missing from tag")
        words = json.loads(z.read(LANG))
        texts = {k: v for k, v in words.items()
                 if k.startswith("enchantment.alexscaves.straight_hook")}
        classes = [n for n in names if n.startswith(BASE) and n.endswith(".class")]
        require(100 <= len(classes) <= 3000, "class population outside limits")
        direct_hits = sorted(n for n in classes if b"STRAIGHT_HOOK" in z.read(n))
        require(HOOK in direct_hits and REG in direct_hits and len(direct_hits) <= 16,
                "unexpected direct enchantment token consumers")
        gravity_hits = sorted(n for n in classes if b"RESISTS_GRAVITY" in z.read(n))
        require(HOOK in gravity_hits and len(gravity_hits) <= 25,
                "gravity-state field census mismatch")
    members = {p: collect_methods(javap_bin, jar, p) for p in (HOOK, ITEM)}
    gravity_proof = certify_compiled_branches(members[HOOK])
    owner = members[HOOK]["bounded_pivot_witnesses"]
    constructors = [m for m in owner if m["name"] == "CandyCaneHookEntity"
                    and "Lnet/minecraft/world/item/ItemStack;" in m["descriptor"]]
    require(len(constructors) == 1, "missing unique stack constructor")
    ctor = constructors[0]
    require(any(w["pivot"] == "STRAIGHT_HOOK" for w in ctor["windows"]) and
            any(w["pivot"] == "RESISTS_GRAVITY" for w in ctor["windows"]),
            "compiled Straight Hook constructor branch not witnessed")
    return {
        "schema_version": 1,
        "scope": "STRAIGHT_HOOK_1010_SHA_EXACT_STATIC_GRAVITY_CONTRACT",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "enchantment": {"id": ID, "path": ENCH, "sha256": hashes[ENCH],
                        "bytes": len(raw_ench), "json": enchant},
        "item_tag": {"path": TAG, "sha256": hashes[TAG], "json": tag},
        "lang_en": {"sha256": hashes[LANG], "own_keys": texts},
        "class_hashes": {p: hashes[p] for p in (HOOK, ITEM, REG)},
        "scan": {"classfiles": len(classes), "straight_hook_direct_hits": direct_hits,
                 "gravity_state_direct_hits": gravity_hits},
        "owners": members,
        "compiled_gravity_contract": gravity_proof,
        "limits": {"static_certification": "CERTIFIED_STATIC_CONTRACT_ONLY",
                   "whole_provider_closed": False,
                   "mutating_hook": "NOT_VERIFIED",
                   "physical_qa": "NOT_TESTED",
                   "mutation": "NO_MUTATION",
                   "jvm_scope": "BOUNDED_METHOD_PIVOTS",
                   "gameplay_gravity_reduction": "NOT_TESTED",
                   "persistence_engine": "NOT_VERIFIED",
                   "external_provider_hooks": "NOT_VERIFIED"}
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--seal", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = audit(args.jar, args.javap)
    canonical = json.dumps(report, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"))
    require(len(canonical.encode("utf8")) <= MAX_REPORT_BYTES,
            "clean-room report exceeds size budget")
    if args.seal:
        require(json.loads(args.seal.read_text(encoding="utf8")) == report,
                "Straight Hook SHA-exact evidence seal mismatch")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2,
                                          ensure_ascii=False) + "\n", encoding="utf8")
    print("STRAIGHT_HOOK_DISCOVERY=" + canonical)
    print("STRAIGHT_HOOK_READONLY=NO_MUTATION")


if __name__ == "__main__":
    main()
