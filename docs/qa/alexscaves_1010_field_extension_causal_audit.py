#!/usr/bin/env python3
"""Field Extension 1.0.10 individual read-only static contract certification.

Replays the SHA-exact publisher JAR, the historical bounded Field Extension
windows and the certified 13-method Ferrous Haste Galena Gauntlet/Weapon census.
This is not a mutating hook, gameplay test or independent Black Arcana cast.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file, SHA1, SHA256, SIZE
from alexscaves_1010_ferrous_haste_causal_audit import (
    AuditError, GAUNTLET, WEAPON, REGISTRY, ROOT, audit as ferrous_audit,
    branches, index_methods, require, row, strict_pairs
)
from alexscaves_1010_field_extension_probe import audit as selected_window_audit

SEAL = ROOT / "EXACT-FIELD-EXTENSION-CAUSAL-1.0.10.json"
BASE = "com/github/alexmodguy/alexscaves/"
ENCHANT = "data/alexscaves/enchantment/field_extension.json"
TAG = "data/alexscaves/tags/item/enchantable/galena_gauntlet.json"
# Hard-coded assertions of semantic pivots independent of the certificate JSON.
PIVOTS = {
    519: ("invokevirtual", "isOwnerWearingGauntlet"),
    522: ("ifne", "529"), 530: ("putfield", "comingBack"),
    541: ("invokevirtual", "isOwnerWearingGauntlet"), 544: ("ifeq", "1416"),
    552: ("ldc", "float 30.0f"), 554: ("fstore", "8"),
    557: ("invokevirtual", "getController:"), 564: ("instanceof", "LivingEntity"),
    567: ("ifeq", "646"), 579: ("invokevirtual", "getUseItem:"),
    582: ("getstatic", "GALENA_GAUNTLET"), 593: ("invokevirtual", "ItemStack.is:"),
    596: ("ifeq", "646"), 601: ("invokevirtual", "getUseItem:"),
    608: ("getstatic", "FERROUS_HASTE"), 611: ("invokestatic", "enchantLevel:"),
    614: ("ifle", "621"), 626: ("getstatic", "FIELD_EXTENSION"),
    629: ("invokestatic", "enchantLevel:"), 632: ("istore", "11"),
    634: ("fload", "8"), 636: ("iload", "11"), 638: ("i2f", ""),
    639: ("ldc_w", "float 5.0f"), 642: ("fmul", ""),
    643: ("fadd", ""), 644: ("fstore", "8"),
    651: ("invokedynamic", "Predicate"), 656: ("fload", "8"),
    658: ("f2d", ""), 659: ("invokestatic", "getHitResultOnViewVector:"),
    666: ("instanceof", "EntityHitResult"), 669: ("ifeq", "802"),
    680: ("getfield", "playerUseCooldown"), 683: ("ifne", "802"),
    688: ("invokevirtual", "EntityHitResult.getEntity:"),
    713: ("astore", "5"), 715: ("ldc_w", "float 0.2f"),
    718: ("fstore", "6"), 723: ("invokevirtual", "distanceTo:"),
    728: ("invokevirtual", "getBbWidth:"), 731: ("ldc_w", "float 1.5f"),
    734: ("fadd", ""), 736: ("ifge", "799"),
    740: ("getfield", "strikeProgress"), 745: ("ifge", "766"),
    754: ("ldc", "float 0.35f"), 760: ("putfield", "strikeProgress"),
    766: ("aload_0", ""), 771: ("invokevirtual", "hurtEntity:"),
    775: ("iload", "7"), 777: ("ifeq", "784"),
    780: ("iconst_3", ""), 784: ("iconst_5", ""),
    790: ("invokeinterface", "nextInt:"), 796: ("putfield", "playerUseCooldown"),
    799: ("goto", "928"), 804: ("invokevirtual", "getEyePosition:"),
    810: ("invokevirtual", "getViewVector:"),
    813: ("fload", "8"), 815: ("ldc_w", "float 20.0f"),
    818: ("fsub", ""), 820: ("invokevirtual", "Vec3.scale:"),
    823: ("invokevirtual", "Vec3.add:"), 826: ("astore", "5"),
    833: ("getstatic", "HitResult$Type.BLOCK"), 836: ("if_acmpeq", "862"),
    855: ("fload", "8"), 858: ("dcmpg", ""), 859: ("ifge", "928"),
    864: ("instanceof", "BlockHitResult"), 867: ("ifeq", "928"),
    883: ("invokestatic", "Vec3.atCenterOf:"),
    886: ("invokevirtual", "distanceToSqr:"),
    889: ("ldc2_w", "double 2.25d"), 892: ("dcmpg", ""),
    893: ("ifge", "903"), 898: ("invokevirtual", "getBlockPos:"),
    901: ("astore", "9"), 912: ("invokevirtual", "getBlockState:"),
    915: ("invokevirtual", "BlockState.isAir:"),
    918: ("ifne", "928"), 926: ("astore", "5"),
    930: ("ifnull", "1413"),
}

def load_cert():
    return json.loads(SEAL.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)

def validate_tick(tick):
    assert tick["descriptor"] == "()V"
    require(len(tick["instructions"]) == 744, "unexpected tick body size")
    edges, switches = branches(tick)
    require(len(edges) > 80 and not switches, "tick branch topology incomplete")
    selected = []
    for offset, (opcode, token) in PIVOTS.items():
        r = row(tick, offset, opcode, token)
        selected.append({k: r[k] for k in ("offset", "opcode", "operand", "symbol")})
    require([r["offset"] for r in selected] == sorted(PIVOTS),
            "pivot ordering drift")
    return selected

def validate_individual_seal(report, cert=None):
    cert = load_cert() if cert is None else cert
    require(cert["version"] == "1.0.10" and
            cert["enchantment"] == report["enchantment"] ==
            "alexscaves:field_extension", "individual identity drift")
    require(cert["claim_scope"] == report["claim_scope"] ==
            "STATIC_TECHNICAL_CATALOG_ONLY", "wrong static scope")
    require(cert["evidence_grade"] == report["evidence_grade"] ==
            "SHA_EXACT_BINARY_BEHAVIOR", "wrong evidence grade")
    require(report["artifact"] == cert["artifact"] ==
            {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "publisher artifact identity drift")
    require(cert["legacy_seal"] == "EXACT-FIELD-EXTENSION-1.0.10.json"
            and cert["prior_full_roster"] ==
            "EXACT-FERROUS-HASTE-CAUSAL-1.0.10.json",
            "unrecognized dependency")
    for key in ("resources", "resource_json", "supported_item_tag",
                "class_sha256", "compiled_field_extension_token_owners",
                "census", "pivots", "safety"):
        require(report[key] == cert[key], "individual seal mismatch: " + key)
    require(cert["compiled_field_extension_token_owners"] ==
            sorted([REGISTRY, WEAPON]), "unexpected token consumer roster")
    require(len(cert["pivots"]) == len(PIVOTS), "incomplete pivot list")
    for actual, (offset, (opcode, token)) in zip(report["pivots"], PIVOTS.items()):
        require(actual["offset"] == offset and actual["opcode"] == opcode
                and token in actual["operand"] + " " + actual["symbol"],
                "invalid native Field Extension pivot @" + str(offset))
    census = cert["census"]
    require((census["methods_checked"], census["instructions_checked"],
             census["direct_branches_checked"]) == (13, 1387, 147),
            "full-method counts drift")
    require(len(census["method_census"]) == 13
            and any(x["name"] == "tick" and x["instructions"] == 744
                    for x in census["method_census"]),
            "full native methods not grounded")
    safe = cert["safety"]
    require(safe["mutating_hook"] == "NOT_VERIFIED" and
            safe["physical_qa"] == "NOT_TESTED" and
            safe["mutation"] == "NO_MUTATION" and
            safe["provider_universe_closed"] is False,
            "unsafe hook, QA or universe promotion")
    require(safe["accepted_damage_or_block_break"] == "NOT_CERTIFIED"
            and safe["pvp_claims_los"] == "NOT_CERTIFIED"
            and safe["datapack_loaded"] == "NOT_VERIFIED",
            "unverified gameplay claim")
    contract = cert["contract"]
    require("30F + 5F" in contract["range"]
            and "2.25D" in contract["block"]
            and "playerUseCooldown" in contract["target"]
            and "distance-20F" in contract["fallback"],
            "bounded causal contract changed")
    return cert

def audit(jar: Path, javap_bin: str):
    ferrous = ferrous_audit(jar, javap_bin)
    field = selected_window_audit(jar, javap_bin)
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR SHA1/SHA256/size drift")
    with zipfile.ZipFile(jar) as z:
        tokens = sorted(p for p in z.namelist()
                        if p.startswith(BASE) and p.endswith(".class")
                        and b"FIELD_EXTENSION" in z.read(p))
    require(tokens == sorted([REGISTRY, WEAPON]),
            "new/unverified native FIELD_EXTENSION literal owner")
    methods = index_methods(parse_methods(
        javap(javap_bin, jar, WEAPON[:-6].replace("/", "."))))
    require(("tick", "()V") in methods, "native tick missing")
    pivots = validate_tick(methods[("tick", "()V")])
    census = {
        "methods_checked": ferrous["methods_checked"],
        "instructions_checked": ferrous["instructions_checked"],
        "direct_branches_checked": ferrous["direct_branches_checked"],
        "method_census": [
            {"owner": r["owner"], "name": r["name"],
             "descriptor": r["descriptor"], "instructions": r["instructions"],
             "parsed_method_sha256": r["body_sha256"]}
            for r in ferrous["method_census"]
        ],
    }
    # The Ferrous auditor seals full method bodies/CFG independently. The
    # historical Field auditor seals its full selected JVM windows independently.
    report = {
        "enchantment": "alexscaves:field_extension",
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "artifact": field["artifact"],
        "resources": {
            field["resource"]["path"]: field["resource"]["sha256"],
            field["tag"]["path"]: field["tag"]["sha256"],
        },
        "resource_json": field["resource"]["json"],
        "supported_item_tag": field["tag"]["json"],
        "class_sha256": field["class_sha256"],
        "compiled_field_extension_token_owners": tokens,
        "census": census,
        "pivots": pivots,
        "safety": {
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION", "provider_universe_closed": False,
            "gameplay_reach": "NOT_TESTED", "pvp_claims_los": "NOT_CERTIFIED",
            "accepted_damage_or_block_break": "NOT_CERTIFIED",
            "datapack_loaded": "NOT_VERIFIED",
        },
    }
    validate_individual_seal(report)
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf8")
    print(json.dumps({
        "status": "PASS", "enchantment": report["enchantment"],
        "methods": report["census"]["methods_checked"],
        "instructions": report["census"]["instructions_checked"],
        "branches": report["census"]["direct_branches_checked"],
        "pivots": len(report["pivots"]), "safety": report["safety"],
    }, indent=2))

if __name__ == "__main__":
    main()
