#!/usr/bin/env python3
"""SHA-exact read-only Field Extension resource and MagneticWeaponEntity range probe.

Reuses the sealed Ferrous Haste 1.0.10 class/ABI audit as a dependency.
Captures bounded additional JVM windows, not a full CFG or a mutation API.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_ferrous_haste_probe import (
    GAUNTLET, WEAPON, REGISTRY, TAG, audit as ferrous_audit
)

SCOPE = "SHA_EXACT_1010_FIELD_EXTENSION_MAGNETIC_WEAPON_RANGE_SELECTED_JVM_EVIDENCE"
ENCHANT = "data/alexscaves/enchantment/field_extension.json"
RANGES = ((495, 680), (680, 930), (930, 1005))
MUST_HAVE = {
    626: ("getstatic", "FIELD_EXTENSION"),
    629: ("invokestatic", "enchantLevel:"),
    632: ("istore", ""),
    636: ("iload", ""),
    638: ("i2f", ""),
    639: ("ldc_w", "float 5.0f"),
    642: ("fmul", ""),
    643: ("fadd", ""),
    644: ("fstore", ""),
    656: ("fload", ""),
    658: ("f2d", ""),
    659: ("invokestatic", "getHitResultOnViewVector:"),
}

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def compact(row: dict) -> dict:
    return {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}

def resource(z, path):
    raw=z.read(path)
    require(10 <= len(raw) <= 14000, "resource bytes out of bounds: "+path)
    d=json.loads(raw)
    require(isinstance(d,dict), "resource not a JSON object")
    return {"path":path,"size_bytes":len(raw),"sha256":digest(raw),"json":d}

def verify_enchant(res,tag):
    j=res["json"]
    require(j.get("description",{}).get("translate") ==
            "enchantment.alexscaves.field_extension", "wrong field extension identity")
    require(j.get("supported_items") ==
            "#alexscaves:enchantable/galena_gauntlet", "wrong supported-items tag")
    require(j.get("max_level")==4, "unexpected maximum level")
    require(j.get("weight")==10, "unexpected weight")
    require("alexscaves:galena_gauntlet" in tag["json"].get("values",[]),
            "Gauntlet missing from exact supported tag")

def locate_tick(methods):
    found=[x for x in methods if name_of(x)=="tick" and x.get("descriptor")=="()V"]
    require(len(found)==1,"missing or ambiguous MagneticWeaponEntity.tick")
    m=found[0]
    rows=m["instructions"]
    require(len(rows)==744,"unexpected exact 1.0.10 tick instruction count")
    offsets=[x["offset"] for x in rows]
    require(offsets==sorted(set(offsets)), "unsorted/duplicate bytecode offsets")
    return m

def validate_windows(rows):
    by_offset={x["offset"]:x for x in rows}
    for offset,(op,needle) in MUST_HAVE.items():
        x=by_offset.get(offset)
        require(x is not None and x["opcode"]==op and needle in x["symbol"],
                "missing/wrong field extension ABI @"+str(offset))
    for lo,hi in RANGES:
        excerpt=[x for x in rows if lo<=x["offset"]<=hi]
        require(10<=len(excerpt)<=300,
                "range window too narrow/large: "+str((lo,hi)))
    # Require a source value for the scalar and later use by native raycast;
    # this is not a proof of all caller-side filters or actual observed reach.
    require(by_offset[644]["operand"]=="8" and by_offset[656]["operand"]=="8",
            "range local is not shared with provider-native raycast")

def selected_windows(rows):
    validate_windows(rows)
    return [
        {"offset_range":[lo,hi],
         "instructions":[compact(x) for x in rows if lo<=x["offset"]<=hi]}
        for lo,hi in RANGES
    ]

def audit(jar:Path,javap_bin:str):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"publisher JAR SHA or size mismatch")
    prior=ferrous_audit(jar,javap_bin)
    prior_tick=next(x for x in prior["consumers"]
                    if x["owner"]==WEAPON)["methods"][0]
    require(prior_tick["name"]=="tick","Ferrous reference tick missing")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicated JAR members")
        require(ENCHANT in names and TAG in names, "exact resource/tag missing")
        enchant=resource(z,ENCHANT)
        tag=resource(z,TAG)
        verify_enchant(enchant,tag)
    methods=parse_methods(javap(javap_bin,jar,WEAPON[:-6].replace("/",".")))
    tick=locate_tick(methods)
    require(digest_method(tick)==prior_tick["parsed_method_sha256"],
            "new and prior exact tick parse differ")
    rows=tick["instructions"]
    windows=selected_windows(rows)
    return {
        "schema_version":1,
        "scope":SCOPE,
        "artifact":prior["artifact"],
        "resource":enchant,
        "tag":tag,
        "class_sha256":{
            WEAPON:prior["classes"][WEAPON],
            GAUNTLET:prior["classes"][GAUNTLET],
            REGISTRY:prior["classes"][REGISTRY],
        },
        "consumer":{
            "class":WEAPON,"method":"tick","descriptor":"()V",
            "parsed_method_sha256":digest_method(tick),
            "instruction_count":len(rows),
            "selected_windows":windows,
        },
        "reused_exact_contract":{
            "source":"EXACT-FERROUS-HASTE-1.0.10.json",
            "class_and_method_digests_agree":True,
        },
        "limits":{
            "selected_jvm_windows_only":True,
            "complete_cfg":"NOT_RECONSTRUCTED",
            "effective_range_in_game":"NOT_TESTED",
            "targeting_pvp_los_claims":"NOT_CERTIFIED",
            "datapack_effective_tags":"NOT_VERIFIED",
            "adjacent_source_111_not_authoritative":True,
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "perk_certification":"NOT_CERTIFIED",
            "mutation":"NO_MUTATION",
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    out=audit(args.jar,args.javap)
    if args.seal:
        require(out==json.loads(args.seal.read_text(encoding="utf8")),
                "Field Extension 1.0.10 evidence seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf8")
    print(json.dumps(out,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
