#!/usr/bin/env python3
"""SHA-exact Alex's Caves 1.0.10 Swiftwood Primitive Club static discovery.

This clean-room, read-only probe records resource/class fingerprints, own
method digests, and bounded JVM windows. It cannot certify dynamic attribute
application, hook safety, or gameplay without a separate individual dossier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ENCH = "data/alexscaves/enchantment/swiftwood.json"
TAG = "data/alexscaves/tags/item/enchantable/primitive_club.json"
LANG = "assets/alexscaves/lang/en_us.json"
CLUB = BASE + "server/item/PrimitiveClubItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
COMPAT = BASE + "server/misc/ACCompat.class"
EXPECTED_CLUB_SHA = "92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac"
EXPECTED_TAG_SHA = "71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43"
EXPECTED_REG_SHA = "60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32"
PIVOTS = (
    "SWIFTWOOD", "enchantLevel:", "getStatsForEnchantmentLevel:",
    "ATTACK_SPEED", "ATTACK_DAMAGE", "AttributeModifier", "itemAttributes:",
    "Mth.clamp:", "Math.min:", "getAttributeModifiers:", "acModifiers:",
    "float -3.75f", "float 0.15f", "double 8.0d", "float 0.0f",
    "ItemAttributeModifiers", "getEnchantmentValue:", "primitive_club",
)
SELECTION = (
    "PrimitiveClubItem", "getStatsForEnchantmentLevel", "getAttributeModifiers",
    "acModifiers", "getEnchantmentValue", "isEnchantable", "hurtEnemy",
    "acHurtEnemy", "mineBlock", "onLeftClickEntity", "onEntitySwing",
    "acInventoryTick",
)
MAX_BYTES = 95000


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def windows(ins: list[dict], token: str, max_pivots: int = 2) -> list[dict]:
    hits = [i for i, row in enumerate(ins) if token in row["symbol"]]
    require(len(hits) <= 48, "unbounded token census " + token)
    return [
        {"needle": token, "offset": ins[i]["offset"], "matches": len(hits),
         "nearby": [
             {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}
             for row in ins[max(0, i - 6):min(len(ins), i + 10)]
         ]}
        for i in hits[:max_pivots]
    ]


def extract(jar: Path, javap_bin: str, owner: str, *, allow_empty: bool) -> dict:
    methods = parse_methods(javap(javap_bin, jar, owner[:-6].replace("/", ".")))
    require(2 <= len(methods) <= 240, "unbounded or missing class methods")
    index = []
    relevant = []
    for method in methods:
        name = name_of(method)
        ins = method["instructions"]
        if not ins:
            continue
        require(0 < len(ins) <= 4000, "JVM method size outside bounds: " + name)
        offsets = [x["offset"] for x in ins]
        require(offsets == sorted(set(offsets)), "duplicate/unsorted JVM instructions")
        identity = {"name": name, "descriptor": method["descriptor"],
                    "instructions_total": len(ins),
                    "method_sha256": digest_method(method)}
        index.append(identity)
        if owner == CLUB and (name in SELECTION or
            any("SWIFTWOOD" in x["symbol"] for x in ins)):
            rows = []
            for pivot in PIVOTS:
                rows.extend(windows(ins, pivot))
            require(sum(len(w["nearby"]) for w in rows) <= 470,
                    "unbounded clean-room club windows")
            relevant.append({**identity, "windows": rows})
        elif owner == COMPAT and name in ("enchantLevel", "itemAttributes"):
            rows = []
            for pivot in ("ATTRIBUTE_MODIFIERS", "getAttributeModifiers:",
                          "getEnchantments:", "enchantLevel:", "ItemAttributeModifiers",
                          "getOrDefault:", "forEachModifier:"):
                rows.extend(windows(ins, pivot, max_pivots=1))
            require(sum(len(w["nearby"]) for w in rows) <= 160,
                    "unbounded compat windows")
            relevant.append({**identity, "windows": rows})
    require(len(relevant) <= 35 and len(index) <= 240, "too many chosen JVM methods")
    if not allow_empty:
        require(bool(relevant), "no compiled owner methods")
    return {"parsed_method_count": len(methods),
            "all_method_signatures_and_digests": index,
            "selected_methods": relevant}


def audit(jar: Path, javap_bin: str) -> dict:
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "installed/publisher Alex's Caves physical SHA mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate JAR entries")
        for path in (ENCH, TAG, LANG, CLUB, REG, COMPAT):
            require(path in names, "missing exact publisher JAR entry: " + path)
        hashes = {p: sha(archive.read(p))
                  for p in (ENCH, TAG, LANG, CLUB, REG, COMPAT)}
        require(hashes[CLUB] == EXPECTED_CLUB_SHA and
                hashes[TAG] == EXPECTED_TAG_SHA and
                hashes[REG] == EXPECTED_REG_SHA,
                "prior individually witnessed Primitive Club identity drift")
        raw_ench, raw_tag = archive.read(ENCH), archive.read(TAG)
        require(0 < len(raw_ench) <= 12000 and
                0 < len(raw_tag) <= 12000, "unbounded resource JSON")
        enchant = json.loads(raw_ench)
        tag = json.loads(raw_tag)
        require(enchant.get("description", {}).get("translate") ==
                "enchantment.alexscaves.swiftwood", "wrong enchantment identity")
        require(enchant.get("supported_items") ==
                "#alexscaves:enchantable/primitive_club", "unexpected supported tag")
        require("alexscaves:primitive_club" in tag.get("values", []),
                "Primitive Club missing from item tag")
        words = json.loads(archive.read(LANG))
        own_keys = {k: v for k, v in words.items()
                    if k.startswith("enchantment.alexscaves.swiftwood")}
        classes = [n for n in names if n.startswith(BASE) and n.endswith(".class")]
        require(100 <= len(classes) <= 3000, "unbounded class population")
        tokens = sorted(n for n in classes if b"SWIFTWOOD" in archive.read(n))
        require(CLUB in tokens and REG in tokens and len(tokens) <= 30,
                "unexpected direct SWIFTWOOD owner census")
    owners = {p: extract(jar, javap_bin, p, allow_empty=(p == COMPAT))
              for p in (CLUB, COMPAT)}
    club = owners[CLUB]["selected_methods"]
    require(any(any(w["needle"] == "SWIFTWOOD" for w in m["windows"])
                for m in club), "no Swiftwood level consumer in club")
    return {
        "schema_version": 1,
        "claim_scope": "SWIFTWOOD_1010_EXACT_JAR_DISCOVERY_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "enchantment": {"id": "alexscaves:swiftwood", "path": ENCH,
                        "sha256": hashes[ENCH], "bytes": len(raw_ench),
                        "json": enchant},
        "item_tag": {"path": TAG, "sha256": hashes[TAG], "json": tag},
        "language": {"path": LANG, "sha256": hashes[LANG], "entries": own_keys},
        "class_hashes": {p: hashes[p] for p in (CLUB, REG, COMPAT)},
        "class_census": {"count": len(classes),
                         "direct_SWIFTWOOD_token_hits": tokens},
        "owners": owners,
        "limits": {"static_contract": "NOT_CERTIFIED",
                   "mutating_hook": "NOT_VERIFIED",
                   "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
                   "source_111_matches_installed_1010": False,
                   "effective_attribute_stack": "NOT_TESTED",
                   "third_party_modifiers": "NOT_VERIFIED",
                   "provider_universe_closed": False}
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--seal", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = audit(args.jar, args.javap)
    require(len(json.dumps(result, separators=(",", ":")).encode()) <= MAX_BYTES,
            "bounded report size exceeded")
    if args.seal:
        require(result == json.loads(args.seal.read_text(encoding="utf8")),
                "Swiftwood individual SHA-exact seal differs from binary")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf8")
    print("SWIFTWOOD_REPORT=" + json.dumps(result, separators=(",", ":"),
                                           ensure_ascii=False))
    print("SWIFTWOOD_DISCOVERY=NO_MUTATION")


if __name__ == "__main__":
    main()
