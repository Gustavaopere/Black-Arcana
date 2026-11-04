#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 Ortholance Flinging/launch bytecode audit.

Limited JVM windows for interoperability planning; no bytecode copying,
complete CFG assertion, physical modpack QA, mutation or cast certification.
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

SCOPE = "SHA_EXACT_1010_FLINGING_ORTHOLANCE_LAUNCH_SELECTED_JVM_EVIDENCE"
ITEM = BASE + "server/item/OrtholanceItem.class"
WAVE = BASE + "server/entity/item/WaveEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/flinging.json"
TAG = "data/alexscaves/tags/item/enchantable/ortholance.json"
SELECT = {
    ITEM: ("releaseUsing", "use", "mineBlock", "getUseDuration", "getEnchantmentValue"),
    WAVE: ("tick", "setLifespan", "setWaitingTicks", "setWaveScale", "onHitEntity", "onHit"),
}
FOCUS = {
    "releaseUsing": ("FLINGING:", "TSUNAMI:", "SECOND_WAVE:", "enchantLevel:",
                     "getUseDuration:", "clamp:", "getDeltaMovement:",
                     "getViewVector:", "setDeltaMovement:", "addFreshEntity:",
                     "hurtAndBreakUsedHand:", "getEntitiesOfClass:",
                     "hasLineOfSight:", "isAlliedTo:", "hurt:",
                     "setLifespan:", "setWaveScale:", "setWaitingTicks:",
                     "scale:", "multiply:", "setPos:"),
    "use": ("getDamageValue:", "getMaxDamage:", "startUsingItem:", "useFail:"),
    "mineBlock": ("hurtAndBreak:",),
    "tick": ("getOwner:", "getWaitingTicks:", "getLifespan:", "hurt:", "discard:",
             "getEntitiesOfClass:", "setDeltaMovement:"),
    "setLifespan": (),
    "setWaitingTicks": (),
    "setWaveScale": (),
    "onHitEntity": ("hurt:",),
    "onHit": ("hurt:",),
    "getUseDuration": (),
    "getEnchantmentValue": (),
}
METHOD_MAX = 2200
MAX_PIVOT_WINDOWS = 42
MAX_FOCUS_MATCHES = 2

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def compact(i: dict) -> dict:
    return {key: i[key] for key in ("offset", "opcode", "operand", "symbol")}

def select_methods(methods, owner):
    selected = []
    for m in methods:
        name = name_of(m)
        if name not in SELECT[owner]:
            continue
        ins = m["instructions"]
        require(2 <= len(ins) <= METHOD_MAX, "unbounded method " + name)
        offsets = [i["offset"] for i in ins]
        require(offsets == sorted(set(offsets)), "duplicate/unsorted offsets " + name)
        pivots = []
        for needle in FOCUS.get(name, ()):
            found = [idx for idx, i in enumerate(ins) if needle in i["symbol"]]
            if not found:
                continue
            positions = []
            for idx in found[:MAX_FOCUS_MATCHES]:
                positions.append({
                    "offset": ins[idx]["offset"], "instructions": [
                        compact(i) for i in ins[max(0, idx-8):idx+15]
                    ]
                })
            pivots.append({"needle":needle,"hits":len(found),"positions":positions})
        require(len(pivots) <= MAX_PIVOT_WINDOWS,
                "too many selected JVM pivots " + name)
        selected.append({
            "name":name, "descriptor":m["descriptor"],
            "instruction_count":len(ins),
            "parsed_method_sha256":digest_method(m),
            "pivots":pivots,
        })
    require(len(selected) <= 14, "unbounded method selection")
    return selected

def verify_launch(methods):
    found = [m for m in methods if m["name"]=="releaseUsing" and
             m["descriptor"].startswith("(Lnet/minecraft/world/item/ItemStack;")]
    require(len(found)==1, "missing/ambiguous item releaseUsing")
    names = {p["needle"] for p in found[0]["pivots"]}
    for n in ("FLINGING:", "enchantLevel:", "setDeltaMovement:",
              "TSUNAMI:", "getEntitiesOfClass:"):
        require(n in names, "missing compiled launch gate: " + n)

def audit(jar: Path, javap_bin: str):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher JAR SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names)==len(set(names)), "duplicate publisher JAR members")
        for path in (ITEM, WAVE, REGISTRY, ENCHANT):
            require(path in names, "required publisher member missing " + path)
        raw = z.read(ENCHANT)
        require(10 <= len(raw) <= 12000, "invalid Flinging resource size")
        enchant = json.loads(raw)
        require(enchant.get("description",{}).get("translate") ==
                "enchantment.alexscaves.flinging", "wrong Flinging identity")
        require(enchant.get("supported_items") ==
                "#alexscaves:enchantable/ortholance", "unexpected Flinging item tag")
        require(enchant.get("max_level")==3, "unexpected Flinging max level")
        class_hashes={p:digest(z.read(p)) for p in (ITEM,WAVE,REGISTRY)}
        tag = None
        if TAG in names:
            content=z.read(TAG)
            require(len(content)<=12000, "oversize ortholance item tag")
            tag={"path":TAG,"sha256":digest(content),"json":json.loads(content)}
    bodies=[]
    for owner in (ITEM,WAVE):
        methods=parse_methods(javap(javap_bin,jar,owner[:-6].replace("/",".")))
        selected=select_methods(methods,owner)
        if owner==ITEM:
            verify_launch(selected)
        bodies.append({
            "owner":owner,"sha256":class_hashes[owner],
            "own_method_count":len(methods),"selected_methods":selected,
        })
    reg=javap(javap_bin,jar,REGISTRY[:-6].replace("/","."))
    require("FLINGING" in reg and "flinging" in reg, "Flinging registry symbols missing")
    return {
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "enchantment":{"id":"alexscaves:flinging","path":ENCHANT,
                       "size_bytes":len(raw),"sha256":digest(raw),"json":enchant},
        "item_tag":{"expected_path":TAG,"in_jar":tag},
        "class_sha256":class_hashes,
        "consumers":bodies,
        "limits":{
            "selected_jvm_windows_only":True,
            "complete_cfg":"NOT_RECONSTRUCTED",
            "adjacent_version_1_1_1_is_exact_authority":False,
            "effective_launch_distance":"NOT_TESTED",
            "actual_hit_and_wave_damage":"NOT_CERTIFIED",
            "world_safety_loa_pvp_claims":"NOT_VERIFIED",
            "server_client_sync":"NOT_TESTED",
            "datapack_effective_item_tag":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "perk_certification":"NOT_CERTIFIED",
            "mutation":"NO_MUTATION"
        }
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--seal",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=audit(args.jar,args.javap)
    if args.seal:
        require(result==json.loads(args.seal.read_text(encoding="utf8")),
                "Flinging SHA-exact seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
