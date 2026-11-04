#!/usr/bin/env python3
"""Bounded, read-only discovery of Humungous Hex in exact publisher JAR 1.0.10.

Outputs metadata and small instruction windows for interoperability review.
No decompilation, whole-method export, runtime mutation or gameplay claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, sha_file, javap, parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

BASE = "com/github/alexmodguy/alexscaves/"
ITEM = BASE + "server/item/SugarStaffItem.class"
HEX = BASE + "server/entity/item/SugarStaffHexEntity.class"
ENCHANT = "data/alexscaves/enchantment/humungous_hex.json"
SPELL = "data/alexscaves/enchantment/spell_lasting.json"
TAG = "data/alexscaves/tags/item/enchantable/sugar_staff.json"
LANG = "assets/alexscaves/lang/en_us.json"
EXPECTED = {
    ITEM: "d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f",
    HEX: "39f8d11595654ccebcb78540a2772106f0ae30507490570ac6b2cbe28de8e89c",
    ENCHANT: "8c45ec4c64e1ed5e258ce1a8d6a27b7693275336b76b91d108521fb91a015cc0",
    SPELL: "839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc",
    TAG: "eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc",
}
TARGET_METHODS = {
    ITEM: {"use", "getEnchantmentValue", "isEnchantable"},
    HEX: {"getDimensions", "getHexScale", "setHexScale", "getLifespan",
          "setLifespan", "hurtEntities", "tick", "onSyncedDataUpdated",
          "readAdditionalSaveData", "addAdditionalSaveData"},
}
NEEDLES = {
    "HUMUNGOUS_HEX", "SPELL_LASTING", "setHexScale:", "getHexScale:",
    "getDimensions:", "setLifespan:", "getLifespan:", "getEntitiesOfClass:",
    "distanceTo:", "indirectMagic:", "hurtEntities:", "addCooldown:",
    "setYRot:", "mulPose:", "scale:", "rotate", "render", "float 0.25f",
    "float 4.0f", "float 6.0f", "int 100", "float 1.0f",
}
MAX_CLASSES = 12
MAX_WINDOWS_PER_METHOD = 22

def require(ok: bool, reason: str):
    if not ok:
        raise ValueError(reason)

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def tiny(rows, idx, before=4, after=8):
    return [{key: row[key] for key in ("offset", "opcode", "operand", "symbol")}
            for row in rows[max(0, idx-before):idx+after]]

def summarize(method):
    ins = method["instructions"]
    require(len(ins) <= 1800, "unbounded JVM method")
    require([x["offset"] for x in ins] == sorted({x["offset"] for x in ins}),
            "invalid or duplicate JVM offsets")
    hits = [(i, row) for i, row in enumerate(ins)
            if any(needle in (row["symbol"] or "") for needle in NEEDLES)]
    # Prioritize informative constructor/branch/call sites and keep bounded windows.
    chosen = hits[:MAX_WINDOWS_PER_METHOD]
    return {
        "name": name_of(method), "descriptor": method["descriptor"],
        "instruction_count": len(ins), "parsed_method_sha256": digest_method(method),
        "matched_window_count": len(hits),
        "selected_windows": [{"at": row["offset"], "source": row["symbol"],
                              "instructions": tiny(ins, i)} for i, row in chosen],
    }

def audit(jar: Path, javap_bin: str) -> dict:
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR exact SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as z:
        files = z.namelist()
        require(len(files) == len(set(files)), "ambiguous duplicate ZIP members")
        for path, expected in EXPECTED.items():
            require(path in files and sha(z.read(path)) == expected,
                    "publisher resource/class SHA drift: " + path)
        raw = z.read(ENCHANT)
        enchant = json.loads(raw)
        require(isinstance(enchant, dict), "enchantment JSON must be object")
        require(enchant.get("description", {}).get("translate") ==
                "enchantment.alexscaves.humungous_hex", "incorrect enchantment identity")
        require(enchant.get("max_level") == 2, "unexpected publisher enchantment maximum")
        tag = json.loads(z.read(TAG))
        spell = json.loads(z.read(SPELL))
        langs = json.loads(z.read(LANG))
        translations = {k:v for k,v in langs.items()
                        if "humungous" in k.lower() and isinstance(v,str)}
        render_paths = sorted(p for p in files if
            p.startswith(BASE) and p.endswith(".class") and
            ("SugarStaffHex" in p or "SugarStaff" in p) and p not in (HEX,ITEM))
        require(len(render_paths) <= MAX_CLASSES, "unexpected renderer/class population")
        class_hashes = {p:sha(z.read(p)) for p in (ITEM,HEX,*render_paths)}
        json_report = {
            "id": "alexscaves:humungous_hex", "path": ENCHANT,
            "sha256": sha(raw), "size_bytes": len(raw), "json": enchant,
            "spell_lasting": {"path": SPELL, "sha256": sha(z.read(SPELL)), "json": spell},
            "item_tag": {"path": TAG, "sha256": sha(z.read(TAG)), "json": tag},
            "english_translations": translations,
        }
    classes = []
    for p in (ITEM, HEX, *render_paths):
        try:
            methods = parse_methods(javap(javap_bin, jar, p.removesuffix(".class").replace("/", ".")))
        except Exception as e:
            # Renderer not usable does not justify certifying rendering.
            raise ValueError("unable to inspect SHA-exact class "+p) from e
        selected = TARGET_METHODS.get(p, {"render", "scale", "renderToBuffer", "setupAnim"})
        found = [summarize(m) for m in methods if name_of(m) in selected]
        classes.append({"path":p,"sha256":class_hashes[p],
                        "declared_methods_inspected":len(methods),"selected_methods":found})
    require(any(m["name"] == "use" and m["matched_window_count"]
                for c in classes if c["path"] == ITEM for m in c["selected_methods"]),
            "no observable use behavior")
    report = {
        "schema_version":1,
        "scope":"SHA_EXACT_1010_HUMUNGOUS_HEX_BOUNDED_DISCOVERY_NO_MUTATION",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "resource":json_report,
        "classes":classes,
        "limitations":{"static_only":True,"hook":"NOT_VERIFIED",
                       "physical_qa":"NOT_TESTED","full_provider_closed":False,
                       "complete_cfg":"NOT_CERTIFIED","mutation":"NO_MUTATION"},
    }
    require(len(json.dumps(report,ensure_ascii=False)) < 140_000,
            "bounded Humungous report exceeded output budget")
    return report

def verify_seal(report: dict, seal_path: Path) -> None:
    """Reject drift of the exact-JAR evidence, the card or a claimed ABI anchor."""
    seal = json.loads(seal_path.read_text(encoding="utf8"))
    require(set(seal) == {"schema_version","claim_scope","evidence_grade","artifact",
                        "card","resource","classes","anchors","limits"},
            "seal schema drift")
    require(seal["schema_version"] == 1 and
            seal["claim_scope"] == "STATIC_TECHNICAL_CATALOG_ONLY" and
            seal["evidence_grade"] == "SHA_EXACT_BINARY_BEHAVIOR",
            "seal scope drift")
    limits = seal["limits"]
    require(limits.get("mutating_hook") == "NOT_VERIFIED" and
            limits.get("physical_qa") == "NOT_TESTED" and
            limits.get("provider_universe_closed") is False and
            limits.get("mutation") == "NO_MUTATION" and
            limits.get("future_hook") == "FAIL_CLOSED",
            "unsafe completion claim in seal")
    require(seal["artifact"] == report["artifact"], "artifact identity drift")
    require(seal["resource"] == report["resource"], "exact JSON/resource drift")
    card = seal["card"]
    require(set(card) == {"path","sha256"} and
            card["path"] == "wiki/modpack-catalog/providers/✅-alexs-caves-continued/enchantments/humungous-hex.md",
            "untrusted card path")
    require(sha(Path(card["path"]).read_bytes()) == card["sha256"],
            "stale or altered Humungous card")
    actual_classes = {row["path"]:row for row in report["classes"]}
    require(set(actual_classes) == set(seal["classes"]) and
            len(actual_classes) == 4, "exact class roster drift")
    for path, expected in seal["classes"].items():
        found = actual_classes[path]
        require(found["sha256"] == expected["sha256"], "class SHA drift: "+path)
        methods = {m["name"]+" "+m["descriptor"]:m
                   for m in found["selected_methods"]}
        require(set(methods) == set(expected["method_digests"]),
                "selected method roster drift: "+path)
        for key, digest in expected["method_digests"].items():
            require(methods[key]["parsed_method_sha256"] == digest,
                    "compiled method digest drift: "+path+" "+key)
    require(len(seal["anchors"]) >= 10 and len(seal["anchors"]) <= 30,
            "missing/oversize anchored evidence")
    for anchor in seal["anchors"]:
        require(set(anchor) == {"class","method","descriptor","offset","symbol_contains"},
                "invalid anchor shape")
        found = actual_classes[anchor["class"]]
        selected = [m for m in found["selected_methods"]
                    if m["name"] == anchor["method"] and
                       m["descriptor"] == anchor["descriptor"]]
        require(len(selected) == 1, "missing anchored method")
        windows = selected[0]["selected_windows"]
        require(any(w["at"] == anchor["offset"] and
                    anchor["symbol_contains"] in w["source"] for w in windows),
                "missing compiled window at "+str(anchor["offset"]))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--seal",type=Path)
    args=p.parse_args()
    report=audit(args.jar,args.javap)
    if args.seal:
        verify_seal(report,args.seal)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    # Print only what is necessary to review JSON values and renderer identity.
    print("EXACT_HUMUNGOUS_JSON="+json.dumps(report["resource"],ensure_ascii=False,sort_keys=True))
    for c in report["classes"]:
        print("EXACT_CLASS="+json.dumps({"path":c["path"],"sha256":c["sha256"],
          "methods":[{"name":m["name"],"descriptor":m["descriptor"],
          "instruction_count":m["instruction_count"],
          "parsed_method_sha256":m["parsed_method_sha256"]}
          for m in c["selected_methods"]]},ensure_ascii=False))
    for c in report["classes"]:
        if c["path"].endswith("SugarStaffHexRenderer.class"):
            for method in c["selected_methods"]:
                if method["name"] == "render" and "SugarStaffHexEntity;" in method["descriptor"]:
                    print("EXACT_RENDERER_WINDOWS="+json.dumps(method["selected_windows"],
                        ensure_ascii=False,sort_keys=True))
    print("EXACT_DISCOVERY_VALIDATED: artifact, selected class hashes, item tag and JSON"+
          ("; frozen seal valid" if args.seal else "; unsealed discovery"))
if __name__ == "__main__":
    main()
