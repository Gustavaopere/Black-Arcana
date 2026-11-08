#!/usr/bin/env python3
"""Read-only, SHA-exact 1.0.10 Solar enchantment and Raygun consumer discovery.

Prints bounded JVM operand windows only; no provider JAR/source is committed.
Not a mutating hook or a physical/runtime acceptance claim.
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

CATALOG = Path("wiki/modpack-catalog/providers/✅-alexs-caves-continued")
CONTROL = CATALOG / "EXACT-RAYGUN-CONTROL-1.0.10.json"
ENCH = "data/alexscaves/enchantment/solar.json"
EN = "assets/alexscaves/lang/en_us.json"
PT = "assets/alexscaves/lang/pt_br.json"
RAYGUN = BASE + "server/item/RaygunItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
TICK_MIXIN = BASE + "mixin/ItemStackTickMixin.class"
TICK_IFACE = BASE + "server/item/ACTickingItem.class"
COMPAT = BASE + "server/misc/ACCompat.class"
KNOWN_RAYGUN_SHA = "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
MAX_REPORT = 85000

FOCUS = (
    "getCharge", "setCharge", "hasCharge", "use", "onUseTick",
    "acInventoryTick", "inventoryTick", "releaseUsing",
)
SYMBOLS = (
    "SOLAR", "enchantLevel", "ChargeUsed", "getCharge", "setCharge",
    "getSunAngle", "canSeeSky", "isDay", "isRaining", "isThundering",
    "isInWaterRainOrBubble", "getBrightness", "isClientSide",
    "onUseTick", "getUseItem", "isUsingItem", "setUseTime",
    "getUseTime", "ACTickingItem", "acInventoryTick", "getGameTime",
    "getRandom", "nextInt", "nextFloat", "getBlockPos",
    "getPos", "getSkyDarken", "sun", "weather", "tickCount",
    "UpdateItemTagMessage", "hurtAndBreak", "getDamageValue",
    "getMaxDamage", "getTag", "getOrCreateTag", "getCustomData",
)
NUMERIC = {"ldc", "ldc_w", "ldc2_w", "bipush", "sipush", "iinc"}


def ensure(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bounded(method: dict, *, direct_solar: bool) -> list[dict]:
    ins = method["instructions"]
    ensure(0 < len(ins) <= 1700, "unexpected method size")
    matches = [i for i, r in enumerate(ins) if
               any(token in r["symbol"] for token in SYMBOLS)]
    chosen = set(range(min(5, len(ins))))
    chosen.update(range(max(0, len(ins) - 5), len(ins)))
    for i in matches[:55]:
        chosen.update(range(max(0, i - 4), min(len(ins), i + 5)))
    if direct_solar:
        solar_sites = [i for i, r in enumerate(ins) if "SOLAR" in r["symbol"]]
        for start in solar_sites:
            # Include local conditional chain around the enchant level read.
            chosen.update(range(max(0, start - 6), min(len(ins), start + 22)))
            # Include constants and branch operands in bounded nearby region.
            for i in range(max(0, start - 12), min(len(ins), start + 85)):
                if ins[i]["opcode"] in NUMERIC or ins[i]["opcode"].startswith("if"):
                    chosen.update(range(max(0, i - 1), min(len(ins), i + 2)))
    ensure(len(chosen) <= 315, "JVM extraction exceeds bounded clean-room limit")
    return [{k: ins[i][k] for k in ("offset", "opcode", "operand", "symbol")}
            for i in sorted(chosen)]


def method_evidence(method: dict, previous_digests: dict) -> dict:
    name = name_of(method)
    target = name + " " + method["descriptor"]
    computed = digest_method(method)
    previous = previous_digests.get(target)
    if previous is not None:
        ensure(previous == computed, "previous Raygun method seal mismatch: " + name)
    direct = any("SOLAR" in x["symbol"] for x in method["instructions"])
    return {
        "name": name, "descriptor": method["descriptor"],
        "instructions_total": len(method["instructions"]),
        "method_sha256": computed, "prior_sha256_matched": previous is not None,
        "solar_direct_reference": direct,
        "selected_jvm": bounded(method, direct_solar=direct),
    }


def discover(jar: Path, java_bin: str, control_path: Path = CONTROL) -> dict:
    ensure(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher/JAR identity mismatch")
    control_bytes = control_path.read_bytes()
    control = json.loads(control_bytes)
    ensure(control["class_path"] == RAYGUN and
           control["class_sha256"] == KNOWN_RAYGUN_SHA and
           control["artifact"]["sha256"] == SHA256,
           "prior Raygun class and artifact baseline drift")
    with zipfile.ZipFile(jar) as z:
        members = z.namelist()
        ensure(len(members) == len(set(members)), "duplicate archive entry")
        mandatory = (ENCH, EN, PT, REG, RAYGUN, TICK_IFACE, TICK_MIXIN, COMPAT)
        ensure(all(p in members for p in mandatory), "missing Raygun/Solar resources")
        classes = sorted(p for p in members if
                         p.startswith(BASE) and p.endswith(".class"))
        ensure(100 <= len(classes) <= 3000, "unexpected class inventory")
        hits = [p for p in classes if b"SOLAR" in z.read(p)]
        ensure(RAYGUN in hits and REG in hits and len(hits) <= 16,
               "unexpected Solar direct token census")
        json_enchant = json.loads(z.read(ENCH))
        tag_id = json_enchant["supported_items"]
        ensure(isinstance(tag_id, str) and
               tag_id.startswith("#alexscaves:enchantable/"),
               "unexpected tag data")
        tag_name = "data/alexscaves/tags/item/enchantable/" + tag_id.rsplit("/", 1)[-1] + ".json"
        ensure(tag_name in members, "missing declared supported_items tag")
        json_tag = json.loads(z.read(tag_name))
        translations = {}
        for lang, file in (("en_us", EN), ("pt_br", PT)):
            content = json.loads(z.read(file))
            translations[lang] = {
                k: v for k, v in content.items()
                if k.startswith("enchantment.alexscaves.solar")
            }
        resources = {p: {"sha256": digest(z.read(p)),
                         "bytes": len(z.read(p))}
                     for p in (ENCH, tag_name, EN, PT)}
        hashes = {p: digest(z.read(p)) for p in
                  (REG, RAYGUN, TICK_MIXIN, TICK_IFACE, COMPAT)}
        ensure(hashes[RAYGUN] == KNOWN_RAYGUN_SHA, "Raygun compiled class drift")
    raygun_methods = parse_methods(javap(java_bin, jar, RAYGUN[:-6].replace("/", ".")))
    ensure(15 <= len(raygun_methods) <= 60, "unexpected declared Raygun methods")
    direct_methods = [m for m in raygun_methods if
                      any("SOLAR" in row["symbol"] for row in m["instructions"])]
    ensure(direct_methods, "no direct SOLAR JVM method references found")
    chosen_names = set(FOCUS) | {name_of(m) for m in direct_methods}
    chosen = [m for m in raygun_methods if
              name_of(m) in chosen_names and m["instructions"]]
    ensure(len(chosen) == len({(name_of(m), m["descriptor"]) for m in chosen}),
           "ambiguous declared Raygun method")
    method_evidences = [method_evidence(m, control["selected_method_digests"])
                        for m in chosen]
    mixin_methods = parse_methods(javap(
        java_bin, jar, TICK_MIXIN[:-6].replace("/", ".")))
    mixin_calls = [m for m in mixin_methods if
                   name_of(m) == "ac_inventoryTick" or
                   any("acInventoryTick" in row["symbol"] for row in m["instructions"])]
    ensure(mixin_calls, "no ItemStackTickMixin dispatch found")
    mixin_evidence = [method_evidence(m, {}) for m in mixin_calls if m["instructions"]]
    output = {
        "schema_version": 1, "scope": "SOLAR_1010_READONLY_JAR_DISCOVERY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "prior_raygun_control_sha256": digest(control_bytes),
        "class_census": {"classes_scanned": len(classes), "solar_token_hits": hits},
        "class_sha256": hashes, "resources": resources,
        "solar_enchantment_json": json_enchant,
        "supported_item_tag": json_tag, "supported_item_tag_path": tag_name,
        "translations": translations,
        "raygun_method_count": len(raygun_methods),
        "raygun_methods": method_evidences,
        "tick_dispatch": mixin_evidence,
        "limits": {"provider_closed": False, "mutating_hook": "NOT_VERIFIED",
                   "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
                   "loaded_datapacks": "NOT_VERIFIED",
                   "charge_authority": "NOT_CERTIFIED",
                   "effective_recharge": "NOT_TESTED"},
    }
    ensure(len(json.dumps(output).encode("utf-8")) < MAX_REPORT,
           "probe report exceeds bounded clean-room limit")
    return output


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--control", type=Path, default=CONTROL)
    p.add_argument("--seal", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = discover(args.jar, args.javap, args.control)
    print("SOLAR_DISCOVERY_JSON=" +
          json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    if args.seal:
        ensure(json.loads(args.seal.read_text(encoding="utf-8")) == report,
               "Solar SHA-exact manifest drift")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
    print("SOLAR_PROBE=READONLY_NO_MUTATION")


if __name__ == "__main__":
    main()
