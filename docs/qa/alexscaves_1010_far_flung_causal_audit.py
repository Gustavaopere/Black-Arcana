#!/usr/bin/env python3
"""Publisher 1.0.10 Far Flung read-only FULL-METHOD causal audit.

Re-checks every instruction in the 17 previously sealed native methods. Does
NOT generate runnable hooks, copy JAR methods into the repository, or claim
gameplay QA. The optional --inspect prints bounded disassembly to CI logs for
manual causal review; it is not an authority substitute for SHA-locked methods.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

REPO = Path(__file__).resolve().parents[2]
PROVIDER = REPO / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
BASE = "com/github/alexmodguy/alexscaves/"
ITEM = BASE + "server/item/CandyCaneHookItem.class"
HOOK = BASE + "server/entity/item/CandyCaneHookEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/far_flung.json"
TAG = "data/alexscaves/tags/item/enchantable/candy_cane_hook.json"
SEAL = "EXACT-FAR-FLUNG-1.0.10.json"
EXTRA_METHODS = {
    ITEM: (
        "isHookLaunchedInWorld", "isActive", "getLaunchedHookUUID",
        "isReelingIn",
    ),
    HOOK: (
        "isOwnerHoldingHook", "postReel", "getHookedEntity",
        "getPlayerOwner", "getDefaultGravity", "defineSynchedData",
    ),
}

class FarFlungAuditError(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise FarFlungAuditError(reason)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_pairs(pairs):
    result = {}
    for name, value in pairs:
        require(name not in result, "duplicate publisher JSON key " + name)
        result[name] = value
    return result


def load_history():
    return json.loads((PROVIDER / SEAL).read_text(encoding="utf8"),
                      object_pairs_hook=unique_pairs)


def identity(method):
    return (name_of(method), method["descriptor"])


def index_methods(methods):
    out = {}
    for m in methods:
        ident = identity(m)
        require(ident not in out, "duplicate JVM method " + repr(ident))
        out[ident] = m
    return out


def row(method, offset, opcode=None, contains=None):
    matches = [r for r in method["instructions"] if r["offset"] == offset]
    require(len(matches) == 1, "missing or duplicate JVM offset " + str(offset))
    a = matches[0]
    if opcode is not None:
        require(a["opcode"] == opcode, "opcode drift @" + str(offset))
    if contains is not None:
        require(contains in a["symbol"] + " " + a["operand"],
                "symbol/value drift @" + str(offset))
    return a


def check_pivots(method, pivots):
    for at, opcode, fragment in pivots:
        row(method, at, opcode, fragment)


def direct_branch_count(m):
    """Check that all direct unconditional/conditional branch destinations exist."""
    offsets = [r["offset"] for r in m["instructions"]]
    require(offsets and offsets == sorted(set(offsets)), "invalid JVM offsets")
    allowed = set(offsets)
    seen = []
    for r in m["instructions"]:
        op = r["opcode"]
        if op.startswith("if") or op in {"goto", "goto_w", "jsr", "jsr_w"}:
            match = re.match(r"^(\d+)$", r["operand"].strip())
            require(match is not None, "unparsed direct branch @" + str(r["offset"]))
            dest = int(match.group(1))
            require(dest in allowed, "branch target out of method @" + str(r["offset"]))
            seen.append((r["offset"], dest))
    return len(seen)


def physical_audit(jar: Path, javap_bin="javap", inspect=False):
    history = load_history()
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher SHA identity drift")
    require(history["artifact"] == {
        "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "previous publisher seal mismatch")
    require(history["enchantment"]["id"] == "alexscaves:far_flung",
            "enchantment ID mismatch")
    require(history["item_tag"]["path"] == TAG, "item tag ID mismatch")
    expected_json = {
        "description": {"translate": "enchantment.alexscaves.far_flung"},
        "supported_items": "#alexscaves:enchantable/candy_cane_hook",
        "weight": 10,
        "max_level": 3,
        "min_cost": {"base": 1, "per_level_above_first": 6},
        "max_cost": {"base": 41, "per_level_above_first": 10},
        "anvil_cost": 1, "slots": ["mainhand"],
    }
    require(history["enchantment"]["json"] == expected_json,
            "enchantment declarative values drift")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate JAR members")
        for path, expected_sha in history["classes"].items():
            require(sha256(z.read(path)) == expected_sha,
                    "physical class hash drift " + path)
        require(sha256(z.read(ENCHANT)) == history["enchantment"]["resource_sha256"],
                "physical enchantment SHA drift")
        require(sha256(z.read(TAG)) == history["item_tag"]["evidence"]["sha256"],
                "physical item-tag SHA drift")
        data = json.loads(z.read(ENCHANT), object_pairs_hook=unique_pairs)
        tag = json.loads(z.read(TAG), object_pairs_hook=unique_pairs)
        require(data == expected_json and tag == {"values": ["alexscaves:candy_cane_hook"]},
                "physical enchantment/tag values drift")
        owners = sorted(name for name in names if name.endswith(".class")
                        and name.startswith(BASE)
                        and b"FAR_FLUNG" in z.read(name))
    require(owners == sorted([REGISTRY, HOOK]),
            "unexpected FAR_FLUNG class token owners: " + repr(owners))
    bootstrap_raw = subprocess.run(
        [str(javap_bin), "-classpath", str(jar), "-v", "-p",
         HOOK[:-6].replace("/", ".")],
        capture_output=True, text=True, timeout=45, check=True,
    ).stdout
    require(len(bootstrap_raw) < 3_500_000, "unbounded verbose bytecode")
    bootstrap_match = re.search(
        r"BootstrapMethods:\s*\n\s*0:.*?(?=\n\s*1:|\nInnerClasses:|\Z)",
        bootstrap_raw, re.S,
    )
    require(bootstrap_match is not None, "missing invokedynamic bootstrap #0")
    boot = bootstrap_match.group(0)
    if inspect:
        print("=== BOOTSTRAP_LIVE_ENTITY_PREDICATE ===")
        print(boot[:2000])
    require("net/minecraft/world/entity/Entity.isAlive:()Z" in boot,
            "Entity::isAlive bootstrap not established for getEntities")

    inspected = {}
    method_report = []
    total_ins, total_branches = 0, 0
    for group in history["consumers"]:
        owner = group["owner"]
        require(owner in (ITEM, HOOK), "unexpected historical owner")
        native = index_methods(parse_methods(
            javap(javap_bin, jar, owner[:-6].replace("/", "."))))
        require(len(native) == group["own_method_count"],
                "owner own method population changed")
        if inspect:
            print("=== METHOD_ROSTER " + owner + " ===")
            print(json.dumps([(name, desc, len(method["instructions"]))
                              for (name, desc), method in native.items()],
                             ensure_ascii=False))
        require(len(group["methods"]) >= 7, "missing selected owner methods")
        for previous in group["methods"]:
            ident = (previous["name"], previous["descriptor"])
            require(ident in native, "missing previously sealed full method " + repr(ident))
            m = native[ident]
            require(len(m["instructions"]) == previous["instruction_count"],
                    "full JVM instruction count drift " + repr(ident))
            require(digest_method(m) == previous["parsed_method_sha256"],
                    "full JVM method digest drift " + repr(ident))
            nbranch = direct_branch_count(m)
            method_report.append({
                "owner": owner, "method": ident[0],
                "descriptor": ident[1],
                "instructions": len(m["instructions"]),
                "direct_branches": nbranch,
                "full_parsed_method_sha256": digest_method(m),
            })
            total_ins += len(m["instructions"])
            total_branches += nbranch
            inspected[(owner, ident)] = m
        for name in EXTRA_METHODS[owner]:
            candidates = [((nm, desc), method)
                          for (nm, desc), method in native.items()
                          if nm == name]
            require(len(candidates) == 1, "missing/ambiguous adjacent method " + name)
            ident, native_method = candidates[0]
            require((owner, ident) not in inspected,
                    "duplicate core/adjacent method " + name)
            nbranch = direct_branch_count(native_method)
            method_report.append({
                "owner": owner, "method": name,
                "descriptor": ident[1], "instructions": len(native_method["instructions"]),
                "direct_branches": nbranch,
                "full_parsed_method_sha256": digest_method(native_method),
                "evidence_role": "ADJACENT_CONSUMER_FULL_BODY",
            })
            total_ins += len(native_method["instructions"])
            total_branches += nbranch
            inspected[(owner, ident)] = native_method
            if inspect:
                print("=== ADJACENT_METHOD " + owner + "." + name + " ===")
                for ins in native_method["instructions"]:
                    print(str(ins["offset"]) + ": " + ins["opcode"]
                          + " " + ins["operand"] + " // " + ins["symbol"])

    def m(owner, name, descriptor=None):
        values = [obj for (path, (nm, desc)), obj in inspected.items()
                  if path == owner and nm == name
                  and (descriptor is None or desc == descriptor)]
        require(len(values) == 1, "missing or ambiguous method " + owner + "." + name)
        return values[0]

    producer = m(ITEM, "use")
    launch = m(HOOK, "CandyCaneHookEntity",
               "(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;Z)V")
    canlaunch = m(ITEM, "canLaunchHook")
    tick = m(HOOK, "tick")
    fling = m(HOOK, "fling")
    check_pivots(producer, [
        (42, "invokestatic", "canLaunchHook:"),
        (45, "ifeq", "221"),
        (125, "new", "CandyCaneHookEntity"),
        (145, "invokespecial", "CandyCaneHookEntity"),
        (153, "invokevirtual", "setOwner:"),
        (159, "invokevirtual", "setReeling:"),
        (163, "invokevirtual", "isClientSide:"),
        (166, "ifne", "176"),
        (172, "invokevirtual", "addFreshEntity:"),
        (175, "pop", ""),
        (183, "invokestatic", "setLastLaunchedHookUUID:"),
        (189, "invokestatic", "setReelingIn:"),
        (299, "invokestatic", "hurtAndBreak:"),
        (328, "invokestatic", "hurtAndBreak:"),
    ])
    check_pivots(launch, [
        (248, "aload", "19"), (250, "invokevirtual", "Vec3.length:"),
        (253, "dstore", "20"), (255, "ldc2_w", "double 0.5d"),
        (259, "getstatic", "FAR_FLUNG:"),
        (262, "invokestatic", "ACCompat.enchantLevel:"),
        (265, "i2d", ""), (266, "ldc2_w", "double 0.2d"),
        (269, "dmul", ""), (270, "dadd", ""), (271, "dstore", "22"),
        (273, "aload", "19"), (275, "dload", "22"),
        (277, "dload", "20"),
        (279, "ddiv", ""), (280, "ldc2_w", "double 0.5d"),
        (283, "dadd", ""), (288, "invokeinterface", "RandomSource.nextGaussian:"),
        (293, "ldc2_w", "double 0.0045d"),
        (296, "dmul", ""), (297, "dadd", ""),
        (302, "ddiv", ""), (303, "ldc2_w", "double 0.5d"),
        (306, "dadd", ""), (311, "invokeinterface", "RandomSource.nextGaussian:"),
        (316, "ldc2_w", "double 0.0045d"),
        (319, "dmul", ""), (320, "dadd", ""),
        (325, "ddiv", ""), (326, "ldc2_w", "double 0.5d"),
        (329, "dadd", ""), (334, "invokeinterface", "RandomSource.nextGaussian:"),
        (339, "ldc2_w", "double 0.0045d"),
        (342, "dmul", ""), (343, "dadd", ""),
        (344, "invokevirtual", "Vec3.multiply:"),
        (352, "invokevirtual", "setDeltaMovement:"),
        (423, "getstatic", "SHARP_CANE:"),
        (426, "invokestatic", "ACCompat.enchantLevel:"),
        (433, "invokevirtual", "setDamage:"),
        (437, "getstatic", "STRAIGHT_HOOK:"),
        (440, "invokestatic", "ACCompat.enchantLevel:"),
    ])
    check_pivots(canlaunch, [
        (21, "ldc", "LastLaunchedHookUUID"),
        (31, "ldc", "LastLaunchedHookUUID"),
        (48, "invokevirtual", "ServerLevel.getEntity:"),
        (70, "invokevirtual", "Entity.isAlive:"),
        (78, "invokevirtual", "getOwner:"),
    ])
    check_pivots(tick, [
        (23, "invokevirtual", "Level.isClientSide:"),
        (26, "ifne", "607"),
        (5, "invokevirtual", "getOwner:"),
        (10, "invokevirtual", "getHookedEntity:"),
        (111, "invokevirtual", "setReeling:"),
        (128, "invokevirtual", "setReeling:"),
        (201, "invokevirtual", "discard:"),
        (214, "invokevirtual", "discard:"),
        (360, "invokevirtual", "AABB.inflate:"),
        (375, "invokedynamic", "test:"),
        (380, "invokevirtual", "getEntities:"),
        (417, "ifeq", "435"), (429, "invokevirtual", "getHeadEntity:"),
        (449, "ifne", "514"), (457, "ifne", "514"),
        (467, "invokevirtual", "Entity.is:"),
        (481, "invokevirtual", "distanceTo:"),
        (487, "invokevirtual", "distanceTo:"),
        (496, "instanceof", "GumWormEntity"),
        (504, "instanceof", "GumWormEntity"),
        (525, "invokevirtual", "getUUID:"),
        (528, "invokevirtual", "setHookedEntityUUID:"),
        (532, "invokevirtual", "getDamage:"),
        (537, "ifeq", "563"),
        (546, "invokevirtual", "DamageSources.thrown:"),
        (559, "invokevirtual", "Entity.hurt:"), (562, "pop", ""),
        (1099, "invokevirtual", "move:"),
        (1123, "invokevirtual", "Vec3.scale:"),
        (1136, "invokevirtual", "setDeltaMovement:"),
        (1170, "invokevirtual", "fling:"),
    ])
    check_pivots(fling, [
        (1, "invokevirtual", "getHookedPosition:"),
        (79, "invokevirtual", "setDeltaMovement:"),
        (147, "invokevirtual", "setDeltaMovement:"),
        (50, "ifle", "61"), (55, "dconst_1", ""),
        (56, "invokevirtual", "Vec3.scale:"),
        (118, "ifle", "129"), (123, "dconst_1", ""),
        (124, "invokevirtual", "Vec3.scale:"),
    ])
    require(any("getLaunchedHookUUID:" in r["symbol"] for r in
                m(HOOK, "isOwnerHoldingHook")["instructions"]),
            "holding-hook identity not derived from stack UUID")
    require(any("CandyCaneHookItem.setLastLaunchedHookUUID:" in r["symbol"]
                for r in m(HOOK, "postReel")["instructions"]),
            "post-reel stack UUID cleanup absent")
    require(any("ServerLevel.getEntity:" in r["symbol"]
                for r in m(HOOK, "getHookedEntity")["instructions"]),
            "server-hooked-entity UUID lookup absent")
    for name, descriptor in [
        ("readAdditionalSaveData", "(Lnet/minecraft/nbt/CompoundTag;)V"),
        ("addAdditionalSaveData", "(Lnet/minecraft/nbt/CompoundTag;)V"),
    ]:
        nbt = m(HOOK, name, descriptor)
        require(any("Reeling" in r["symbol"] for r in nbt["instructions"]),
                "missing Reeling NBT boundary")
        require(any("HookedEntityUUID" in r["symbol"] for r in nbt["instructions"]),
                "missing target UUID NBT boundary")
        require(any("Offhand" in r["symbol"] for r in nbt["instructions"]),
                "missing Offhand NBT boundary")

    result = {
        "schema_version": 1,
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "release": "1.0.10",
        "artifact_sha1": SHA1,
        "artifact_sha256": SHA256,
        "enchantment": "alexscaves:far_flung",
        "methods_checked": len(method_report),
        "instructions_checked": total_ins,
        "direct_branches_checked": total_branches,
        "compiled_far_flung_owners": owners,
        "alive_predicate_bootstrap_sha256": sha256(boot.encode("utf8")),
        "method_census": method_report,
        "limits": {
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION", "provider_universe_closed": False,
            "complete_gameplay_physics": "NOT_TESTED",
            "server_mutation_authority": "NOT_VERIFIED",
        },
    }
    if inspect:
        for method, start, end, label in [
            (launch, 215, 358, "CONSTRUCTOR_VECTOR"),
            (canlaunch, 0, 123, "LAUNCH_ADMISSION"),
            (tick, 0, 220, "TICK_SERVER_AUTHORITY"),
            (tick, 320, 650, "TICK_TARGETING_AND_DAMAGE"),
            (tick, 850, 1250, "TICK_MOVEMENT_CLEANUP"),
            (fling, 0, 180, "FLING"),
        ]:
            print("=== " + label + " (" + str(len(method["instructions"])) + " instructions total) ===")
            for r in method["instructions"]:
                if start <= r["offset"] <= end:
                    print(str(r["offset"]) + ": " + r["opcode"] + " "
                          + r["operand"] + " // " + r["symbol"])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = physical_audit(args.jar, args.javap, inspect=args.inspect)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf8")
    print(json.dumps({
        "status": "PASS", "claim_scope": result["claim_scope"],
        "release": result["release"],
        "methods_checked": result["methods_checked"],
        "instructions_checked": result["instructions_checked"],
        "direct_branches_checked": result["direct_branches_checked"],
        "compiled_far_flung_owners": result["compiled_far_flung_owners"],
        "safety": result["limits"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
