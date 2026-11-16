#!/usr/bin/env python3
"""Read-only full-method exact 1.0.10 Ferrous Haste causal and branch audit.

Historical SHA-exact publisher manifest anchors the 13 native method bodies.
No copied implementation, no mutating hook, no live Minecraft game assertions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

BASE = "com/github/alexmodguy/alexscaves/"
GAUNTLET = BASE + "server/item/GalenaGauntletItem.class"
WEAPON = BASE + "server/entity/item/MagneticWeaponEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/ferrous_haste.json"
TAG = "data/alexscaves/tags/item/enchantable/galena_gauntlet.json"
ROOT = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
HISTORY = ROOT / "EXACT-FERROUS-HASTE-1.0.10.json"

class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def strict_pairs(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, "duplicate JSON key " + key)
        answer[key] = value
    return answer


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load_history():
    return json.loads(HISTORY.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)


def index_methods(methods):
    out = {}
    for m in methods:
        ident = (name_of(m), m["descriptor"])
        require(ident not in out, "duplicate compiled method identity " + str(ident))
        out[ident] = m
    return out


def row(method, offset, opcode=None, token=None):
    values = [x for x in method["instructions"] if x["offset"] == offset]
    require(len(values) == 1, "missing/duplicate opcode @" + str(offset))
    value = values[0]
    if opcode is not None:
        require(value["opcode"] == opcode, "unexpected opcode @" + str(offset))
    if token is not None:
        require(token in value["symbol"] + " " + value["operand"],
                "unexpected JVM token @" + str(offset))
    return value


def branches(method):
    offsets = [r["offset"] for r in method["instructions"]]
    require(offsets and offsets == sorted(set(offsets)),
            "non-unique/unsorted native bytecode positions")
    known = set(offsets)
    edges = []
    switches = []
    for r in method["instructions"]:
        if r["opcode"].startswith("if") or r["opcode"] in {"goto", "goto_w", "jsr", "jsr_w"}:
            match = re.fullmatch(r"\d+", r["operand"])
            require(match is not None, "unparsed branch operand @" + str(r["offset"]))
            dest = int(match.group())
            require(dest in known, "missing branch destination " + str(dest))
            edges.append([r["offset"], dest])
        elif r["opcode"] in {"tableswitch", "lookupswitch"}:
            switches.append(r["offset"])
    return edges, switches


def check_pivots(method, expected):
    for offset, opcode, token in expected:
        row(method, offset, opcode, token)


def audit(jar, javap_bin, inspect=False):
    history = load_history()
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "wrong publisher artifact SHA1/SHA256/size")
    require(history["artifact"] == {"sha1": SHA1, "sha256": SHA256,
                                   "size_bytes": SIZE},
            "historical publisher identity changed")
    expected_e = {
        "description": {"translate": "enchantment.alexscaves.ferrous_haste"},
        "supported_items": "#alexscaves:enchantable/galena_gauntlet",
        "weight": 2,
        "max_level": 1,
        "min_cost": {"base": 1, "per_level_above_first": 15},
        "max_cost": {"base": 41, "per_level_above_first": 10},
        "anvil_cost": 4,
        "slots": ["mainhand", "offhand"],
    }
    require(history["enchantment"]["json"] == expected_e,
            "historical enchantment JSON values changed")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate JAR entries")
        for p, sha in history["classes"].items():
            require(digest(z.read(p)) == sha, "native class hash drift " + p)
        for name, key in [(ENCHANT, "enchantment"), (TAG, "tag")]:
            require(digest(z.read(name)) == history[key]["sha256"],
                    "resource bytes SHA drift " + name)
            data = json.loads(z.read(name), object_pairs_hook=strict_pairs)
            require(data == history[key]["json"],
                    "resource JSON canonical drift " + name)
        require(json.loads(z.read(ENCHANT), object_pairs_hook=strict_pairs) == expected_e,
                "unexpected compiled enchantment metadata")
        require(json.loads(z.read(TAG), object_pairs_hook=strict_pairs) ==
                {"values": ["alexscaves:galena_gauntlet"]}, "unexpected tag items")
        tokenized = sorted(path for path in names if path.startswith(BASE)
                           and path.endswith(".class") and
                           b"FERROUS_HASTE" in z.read(path))
    require(REGISTRY in tokenized and WEAPON in tokenized,
            "compiled FERROUS_HASTE owner/consumer missing")
    require(len(tokenized) <= 10, "unbounded additional token consumers")

    method_rows = []
    native = {}
    verbose_code = {}
    for group in history["consumers"]:
        owner = group["owner"]
        require(owner in (GAUNTLET, WEAPON), "unrecognized owner")
        compiled_text = javap(javap_bin, jar, owner[:-6].replace("/", "."))
        verbose_code[owner] = compiled_text
        parsed = index_methods(parse_methods(compiled_text))
        require(len(parsed) == group["method_count"],
                "method population drift " + owner)
        for historical in group["methods"]:
            ident = (historical["name"], historical["descriptor"])
            require(ident in parsed, "missing full native method " + str(ident))
            m = parsed[ident]
            require(len(m["instructions"]) == historical["instruction_count"],
                    "full native instruction count drift " + str(ident))
            require(digest_method(m) == historical["parsed_method_sha256"],
                    "full native body hash drift " + str(ident))
            edges, switches = branches(m)
            method_rows.append({
                "owner": owner, "name": ident[0], "descriptor": ident[1],
                "instructions": len(m["instructions"]),
                "body_sha256": digest_method(m),
                "direct_branches": len(edges),
                "switch_offsets": switches,
            })
            native[(owner, ident[0])] = m
        if inspect:
            print("=== METHOD_ROSTER " + owner + " ===")
            print(json.dumps([
                [name, desc, len(method["instructions"])]
                for (name, desc), method in parsed.items()
            ], ensure_ascii=False))

    def method(owner, name):
        require((owner, name) in native, "unsealed consumer " + name)
        return native[(owner, name)]

    tick = method(WEAPON, "tick")
    check_pivots(tick, [
        (579, "invokevirtual", "getUseItem:"),
        (582, "getstatic", "GALENA_GAUNTLET:"),
        (608, "getstatic", "FERROUS_HASTE:"),
        (611, "invokestatic", "ACCompat.enchantLevel:"),
        (614, "ifle", "621"),
        (622, "istore", "7"),
        (626, "getstatic", "FIELD_EXTENSION:"),
        (629, "invokestatic", "ACCompat.enchantLevel:"),
        (639, "ldc_w", "float 5.0f"),
        (659, "invokestatic", "ProjectileUtil.getHitResultOnViewVector:"),
        (680, "getfield", "playerUseCooldown:"),
        (683, "ifne", "802"),
        (771, "invokevirtual", "hurtEntity:"),
        (775, "iload", "7"),
        (777, "ifeq", "784"), (780, "iconst_3", ""),
        (784, "iconst_5", ""), (789, "iconst_5", ""),
        (790, "invokeinterface", "RandomSource.nextInt:"),
        (795, "iadd", ""),
        (796, "putfield", "playerUseCooldown:"),
        (1013, "invokevirtual", "BlockState.getDestroySpeed:"),
        (1025, "invokevirtual", "getDigSpeed:"),
        (1034, "ifle", "1413"),
        (1118, "fdiv", ""), (1121, "ifeq", "1129"),
        (1124, "bipush", "8"), (1129, "bipush", "10"),
        (1131, "i2f", ""), (1132, "fdiv", ""),
        (1143, "putfield", "destroyBlockProgress:"),
        (1168, "invokevirtual", "Level.destroyBlockProgress:"),
        (1177, "iflt", "1413"),
        (1187, "ifne", "1413"),
        (1192, "invokevirtual", "damageItem:"),
        (1213, "invokevirtual", "ItemStack.mineBlock:"),
        (1290, "invokevirtual", "Level.destroyBlock:"),
        (1329, "invokevirtual", "Level.destroyBlock:"),
        (1332, "istore", "20"),
        (1360, "invokevirtual", "Block.playerDestroy:"),
        (1365, "ifeq", "1408"),
        (1405, "invokevirtual", "Block.popExperience:"),
    ])
    check_pivots(method(WEAPON, "hurtEntity"), [
        (99, "invokestatic", "ACCompat.hurt:"),
        (102, "ifeq", "194"),
        (115, "invokestatic", "postAttackEffects:"),
        (120, "invokevirtual", "damageItem:"),
        (239, "invokevirtual", "ItemStack.hurtEnemy:"),
        (242, "pop", ""),
    ])
    check_pivots(method(GAUNTLET, "onUseTick"), [
        (124, "invokevirtual", "getEntitiesOfClass:"),
        (216, "invokestatic", "createEntity:"),
        (228, "invokevirtual", "setItemStack:"),
        (252, "invokevirtual", "setControllerUUID:"),
        (258, "invokevirtual", "addFreshEntity:"),
    ])
    check_pivots(method(WEAPON, "getDigSpeed"), [
        (9, "invokevirtual", "getDestroySpeed:"),
        (26, "invokestatic", "miningEfficiencyBonus:"),
        (157, "invokestatic", "submergedMiningFactor:"),
        (183, "invokestatic", "getBreakSpeed:"),
    ])

    raw_weapon = verbose_code[WEAPON]
    match_switch = re.search(
        r"(?m)^\s*77:\s+tableswitch\s+\{[^\n]*\n"
        r"(?P<cases>(?:\s*(?:[0-9]+|default):\s*[0-9]+\s*\n)+)"
        r"\s*\}",
        raw_weapon,
    )
    require(match_switch is not None,
            "mining fatigue tableswitch case table not parsed")
    switch_pairs = re.findall(r"(?m)^\s*([0-9]+|default):\s*([0-9]+)\s*$",
                              match_switch.group("cases"))
    require([k for k, v in switch_pairs] ==
            ["0", "1", "2", "3", "default"],
            "unexpected mining fatigue switch labels")
    dig_offsets = {r["offset"] for r in method(WEAPON, "getDigSpeed")["instructions"]}
    require(all(int(v) in dig_offsets for k, v in switch_pairs),
            "mining fatigue switch destination absent")
    if inspect:
        print("=== DIG_SPEED_SWITCH === " + json.dumps(switch_pairs))
        for selected, lo, hi, title in [
            (tick, 0, 220, "TICK_COOLDOWN_AND_STATE"),
            (tick, 555, 850, "TICK_ATTACK_GATE"),
            (tick, 890, 1430, "TICK_MINING"),
            (tick, 1420, 1700, "TICK_COOLDOWN_DECREMENT_AND_RETURN"),
            (method(WEAPON,"hurtEntity"), 0, 270, "DAMAGE_AND_COST"),
            (method(WEAPON,"getDigSpeed"), 0, 210, "DIG_SPEED"),
            (method(GAUNTLET,"onUseTick"), 60, 300, "SPAWN"),
        ]:
            print("=== " + title + " (" + str(len(selected["instructions"])) + ") ===")
            for i in selected["instructions"]:
                if lo <= i["offset"] <= hi:
                    print(str(i["offset"]) + ": " + i["opcode"] + " "
                          + i["operand"] + " // " + i["symbol"])

    return {
        "schema_version": 1,
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "enchantment": "alexscaves:ferrous_haste",
        "artifact": history["artifact"],
        "compiled_ferrous_haste_token_owners": tokenized,
        "methods_checked": len(method_rows),
        "instructions_checked": sum(x["instructions"] for x in method_rows),
        "direct_branches_checked": sum(x["direct_branches"] for x in method_rows),
        "switches": [x for x in method_rows if x["switch_offsets"]],
        "dig_speed_switch_targets": switch_pairs,
        "method_census": method_rows,
        "safety": {
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION", "provider_universe_closed": False,
            "damage_accepted": "NOT_CERTIFIED", "block_break_accepted": "NOT_CERTIFIED",
            "multiplayer_world_policy": "NOT_VERIFIED",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", type=Path, required=True)
    ap.add_argument("--javap", default="javap")
    ap.add_argument("--inspect", action="store_true")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    out = audit(args.jar, args.javap, inspect=args.inspect)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print(json.dumps({
        "status":"PASS",
        "methods_checked":out["methods_checked"],
        "instructions_checked":out["instructions_checked"],
        "direct_branches_checked":out["direct_branches_checked"],
        "switches":out["switches"],
        "owners":out["compiled_ferrous_haste_token_owners"],
        "safety":out["safety"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
