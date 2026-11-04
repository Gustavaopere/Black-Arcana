#!/usr/bin/env python3
"""Read-only SHA-exact Ferrous Haste consumer evidence for Alex's Caves 1.0.10.

The output is a bounded JVM bytecode snapshot, not a decompilation, a complete
control-flow proof, a live gameplay test, or an authorized mutation hook.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "SHA_EXACT_1010_FERROUS_HASTE_MAGNETIC_WEAPON_SELECTED_JVM_EVIDENCE"
GAUNTLET = BASE + "server/item/GalenaGauntletItem.class"
WEAPON = BASE + "server/entity/item/MagneticWeaponEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/ferrous_haste.json"
TAG = "data/alexscaves/tags/item/enchantable/galena_gauntlet.json"
EXPECTED_CLASS_SHA256 = {
    GAUNTLET: "5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0",
    WEAPON: "a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071",
    REGISTRY: "60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32",
}
SELECT = {
    GAUNTLET: ("use", "onUseTick", "releaseUsing"),
    WEAPON: ("tick", "hurtEntity", "getDigSpeed", "damageItem", "directMovementTowards",
             "isOwnerWearingGauntlet", "getController", "addAdditionalSaveData",
             "readAdditionalSaveData", "plopItem"),
}
PIVOTS = {
    "use": ("CRYSTALLIZATION:", "MAGNETIC_ITEMS:", "startUsingItem:"),
    "onUseTick": ("createEntity:", "setItemStack:", "setControllerUUID:",
                  "addFreshEntity:", "getEntitiesOfClass:"),
    "releaseUsing": ("addCooldown:",),
    "tick": ("FERROUS_HASTE:", "FIELD_EXTENSION:", "enchantLevel:",
              "getUseItem:", "getHitResultOnViewVector:", "hurtEntity:",
              "destroyBlockProgress:", "getDigSpeed:", "destroyBlock:",
              "playerUseCooldown", "damageItem:", "getDestroySpeed:"),
    "hurtEntity": ("ACCompat.hurt:", "postAttackEffects:", "damageItem:",
                    "hurtEnemy:"),
    "getDigSpeed": ("getDestroySpeed:", "miningEfficiencyBonus:",
                    "getBreakSpeed:", "submergedMiningFactor:"),
    "damageItem": ("hurtAndBreakUsedHand:",),
    "directMovementTowards": ("setDeltaMovement:",),
    "isOwnerWearingGauntlet": ("GALENA_GAUNTLET:",),
    "getController": ("getControllerUUID:",),
    "addAdditionalSaveData": ("ControllerUUID", "WeaponStack"),
    "readAdditionalSaveData": ("ControllerUUID", "WeaponStack"),
    "plopItem": ("spawnAtLocation:",)
}
WINDOWS = {
    # Server/player control, haste gate and strike cooldown, selected JVM offsets.
    "tick": ((575, 845), (990, 1190), (1200, 1365)),
}
MAX_METHOD_INSTRUCTIONS = 1900

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def short(ins):
    return {key: ins[key] for key in ("offset", "opcode", "operand", "symbol")}

def select_method(methods, name):
    found = [m for m in methods if name_of(m) == name]
    require(len(found) == 1, "missing/ambiguous method: " + name)
    m = found[0]
    ins = m["instructions"]
    require(2 <= len(ins) <= MAX_METHOD_INSTRUCTIONS, "method size invalid: " + name)
    offsets = [x["offset"] for x in ins]
    require(offsets == sorted(set(offsets)), "duplicate/unsorted offsets: " + name)
    return m

def extract(m):
    name = name_of(m)
    ins = m["instructions"]
    pivots = []
    for needle in PIVOTS.get(name, ()):
        found = [i for i, x in enumerate(ins) if needle in x["symbol"]]
        if found:
            locs = []
            for idx in found[:2]:
                locs.append({"at": ins[idx]["offset"],
                             "window": [short(x) for x in ins[max(0,idx-6):idx+8]]})
            pivots.append({"needle": needle, "matches": len(found), "locations": locs})
    if name == "tick":
        require(any(p["needle"]=="FERROUS_HASTE:" for p in pivots),
                "FERROUS_HASTE missing from compiled player control")
        require(any(p["needle"]=="getHitResultOnViewVector:" for p in pivots),
                "target acquisition absent")
        require(any(p["needle"]=="destroyBlockProgress:" for p in pivots),
                "block mining loop absent")
        require(any(p["needle"]=="hurtEntity:" for p in pivots),
                "attack settlement absent")
    windows = []
    for lo, hi in WINDOWS.get(name, ()):
        selected = [short(x) for x in ins if lo <= x["offset"] <= hi]
        require(8 <= len(selected) <= 350, "selected window too small/large")
        windows.append({"range": [lo, hi], "instructions": selected})
    require(len(pivots) <= 20 and all(len(p["locations"])<=2 for p in pivots),
            "unbounded pivots")
    return {"name":name,"header":m["header"],"descriptor":m["descriptor"],
            "instruction_count":len(ins),
            "parsed_method_sha256":digest_method(m),
            "pivots":pivots,"selected_windows":windows}

def read_json(z, path):
    raw = z.read(path)
    require(10 < len(raw) < 16000, "unbounded or missing JSON resource " + path)
    obj = json.loads(raw)
    require(isinstance(obj, dict), "resource is not JSON object")
    return {"path":path,"bytes":len(raw),"sha256":digest(raw),"json":obj}

def check_json(enchant, tag):
    e = enchant["json"]
    require(e.get("description",{}).get("translate")==
            "enchantment.alexscaves.ferrous_haste", "wrong enchantment")
    require(e.get("supported_items")==
            "#alexscaves:enchantable/galena_gauntlet", "unexpected supported tag")
    require(e.get("max_level")==1, "unexpected max_level")
    require("alexscaves:galena_gauntlet" in tag["json"].get("values", []),
            "Galena Gauntlet is absent from supported item tag")

def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1,SHA256,SIZE),
            "not exact publisher JAR 1.0.10")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names)==len(set(names)), "duplicate archive member")
        for p in (*EXPECTED_CLASS_SHA256, ENCHANT, TAG):
            require(p in names, "publisher JAR member missing: " + p)
        sha = {p:digest(z.read(p)) for p in EXPECTED_CLASS_SHA256}
        require(sha == EXPECTED_CLASS_SHA256, "compiled owner classes differ from exact evidence")
        enchant,tag=read_json(z,ENCHANT),read_json(z,TAG)
        check_json(enchant,tag)
    consumers=[]
    for path, requested in SELECT.items():
        methods = parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        consumers.append({
            "owner":path,"owner_sha256":sha[path],
            "method_count":len(methods),
            "methods":[extract(select_method(methods,name)) for name in requested],
        })
    reg = javap(javap_bin,jar,REGISTRY[:-6].replace("/","."))
    require("FERROUS_HASTE" in reg and "ferrous_haste" in reg,
            "compiled registry field/resource not observed")
    return {
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "enchantment":enchant,"tag":tag,
        "classes":sha,"consumers":consumers,
        "limits":{
            "selected_windows_only":True,
            "complete_cfg":"NOT_RECONSTRUCTED",
            "adjacent_1_1_1_source_authority":False,
            "attack_cooldown_native_runtime":"NOT_PHYSICALLY_TESTED",
            "mining_progress_native_runtime":"NOT_PHYSICALLY_TESTED",
            "block_break_success_permissions":"NOT_CERTIFIED",
            "pvp_alliance_damage_authority":"NOT_VERIFIED",
            "datapack_effective_item_tags":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "perk_certification":"NOT_CERTIFIED",
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    out=audit(a.jar,a.javap)
    if a.seal:
        expected=json.loads(a.seal.read_text(encoding="utf8"))
        require(out==expected,"Ferrous Haste exact seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(out,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
