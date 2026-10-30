#!/usr/bin/env python3
"""SHA-pinned selected Forsaken timing and persistence ABI evidence (1.0.10).

Records compiled call/field windows and declared NBT-related methods only.
Does NOT prove whole-program persistence, executed animation/hit cadence,
vanilla superclass NBT, multiplayer authority or a mutating perk hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file,javap,parse_methods
from alexscaves_1010_forsaken_sonic_probe import GOAL,ENTITY,CLASS_PINS,strict_pairs,digest_method

METHOD_SHA={
    GOAL:"1fb8ecdd23c6c76d836ee25a4176f788163ef1226220a142a40e5f48d4df8abe",
    ENTITY:"733efd62558f45ce4d8390e43fb09baff389490f8d96f9be709952a6a284341f",
}
METHODS_NBT={
    "addAdditionalSaveData":"(Lnet/minecraft/nbt/CompoundTag;)V",
    "readAdditionalSaveData":"(Lnet/minecraft/nbt/CompoundTag;)V",
    "defineSynchedData":"(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V",
    "getAnimationTick":"()I",
}
GOAL_FIELDS=("attemptSonicDamageIn","sonicEnqueued","ANIMATION_SONIC_ATTACK",
             "ANIMATION_SONIC_BLAST","getAnimationTick","setSonicCharge",
             "ANIMATION_GROUND_SMASH","getTarget")
ENTITY_FIELDS=("ANIMATION_SONIC_ATTACK","ANIMATION_SONIC_BLAST",
               "getAnimationTick","updateAnimations","SONAR_ID","SONIC_CHARGE",
               "setAnimationTick")
MAX_WINDOWS=70
MAX_METHODS=10
MAX_INSTRUCTIONS=2400

class ForsakenTimingError(ValueError):
    pass

def name(m):
    found=re.search(r"([A-Za-z0-9_$]+)\(",m["header"])
    return found.group(1) if found else ""

def row(v):
    return {k:v[k] for k in ("offset","opcode","operand","symbol")}

def window(seq,index,prior=8,later=9):
    return [row(v) for v in seq[max(0,index-prior):min(len(seq),index+later+1)]]

def pick(method,keywords):
    ins=method["instructions"]
    if not (1<=len(ins)<=MAX_INSTRUCTIONS):
        raise ForsakenTimingError("method instruction bound exceeded")
    if len({v["offset"] for v in ins})!=len(ins):
        raise ForsakenTimingError("duplicate bytecode offsets")
    selected=[{"offset":v["offset"],"symbol":v["symbol"],"window":window(ins,i)}
              for i,v in enumerate(ins)
              if (v["opcode"].startswith("invoke") or v["opcode"] in
                  ("getfield","putfield","getstatic","putstatic"))
              and any(k in v["symbol"] for k in keywords)]
    if len(selected)>MAX_WINDOWS:
        raise ForsakenTimingError("selected-site budget exceeded")
    branches=[{"offset":v["offset"],"opcode":v["opcode"],
               "target":int(v["operand"]) if v["operand"].isdecimal() else None}
              for v in ins if v["opcode"].startswith("if") or v["opcode"] in
              ("goto","goto_w","tableswitch","lookupswitch")]
    constants=[row(v) for v in ins if v["opcode"].startswith(
               ("iconst_","fconst_","dconst_","lconst_")) or
               v["opcode"] in ("bipush","sipush","ldc","ldc_w","ldc2_w")]
    if len(branches)>240 or len(constants)>300:
        raise ForsakenTimingError("branch/constant budget exceeded")
    return {"header":method["header"],"descriptor":method["descriptor"],
            "method_sha256":digest_method(method),"instruction_count":len(ins),
            "sites":selected,"branch_anchors":branches,"constant_anchors":constants}

def exact_method(methods,label,descriptor):
    found=[m for m in methods if name(m)==label and m["descriptor"]==descriptor]
    if len(found)!=1:
        raise ForsakenTimingError("missing or duplicate declared method "+label)
    return found[0]

def find_own(methods,label,descriptor):
    matches=[m for m in methods if name(m)==label and m["descriptor"]==descriptor]
    if len(matches)>1:
        raise ForsakenTimingError("duplicate selected own declaration "+label)
    return matches[0] if matches else None

def audit(jar,javap_bin):
    if sha_file(jar)!=(SHA1,SHA256,SIZE):
        raise ForsakenTimingError("publisher JAR SHA1/SHA256/size mismatch")
    with zipfile.ZipFile(jar) as archive:
        members=archive.namelist()
        if len(members)!=len(set(members)):
            raise ForsakenTimingError("duplicate JAR members")
        for path,sha in CLASS_PINS.items():
            if hashlib.sha256(archive.read(path)).hexdigest()!=sha:
                raise ForsakenTimingError("class SHA-256 drift")
    parsed={}
    for path in (GOAL,ENTITY):
        parsed[path]=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        if not 10<=len(parsed[path])<=200:
            raise ForsakenTimingError("unexpected class method count")
    timing={}
    for path,keys in ((GOAL,GOAL_FIELDS),(ENTITY,ENTITY_FIELDS)):
        meth=exact_method(parsed[path],"tick","()V")
        result=pick(meth,keys)
        if result["method_sha256"]!=METHOD_SHA[path]:
            raise ForsakenTimingError("prior sealed tick method differs")
        timing[path]={"class_sha256":CLASS_PINS[path],"tick":result}
    found=[]
    for label,descriptor in METHODS_NBT.items():
        own=find_own(parsed[ENTITY],label,descriptor)
        found.append({"name":label,"descriptor":descriptor,
                      "declared_on_exact_class":own is not None,
                      "method":pick(own,("CompoundTag","get","put","SONIC",
                                         "SONAR","LEAP","animation","SynchedEntityData",
                                         "define","super")) if own else None})
    return {
        "schema_version":1,
        "scope":"EXACT_1010_FORSAKEN_TICK_WINDOWS_AND_OWN_NBT_DECLARATIONS_ONLY",
        "jar":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "timing":timing,"declared_state_methods":found,
        "limits":{
            "superclass_and_other_mixins_persistence":"NOT_AUDITED",
            "declared_method_absence_proves_no_world_persistence":False,
            "precise_server_execution_or_animation_cadence":"NOT_VERIFIED",
            "tick_to_real_time_mapping":"NOT_MEASURED",
            "damage_settlement_and_hit_counts":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "complete_perk_ready":False,
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    data=audit(args.jar,args.javap)
    if args.snapshot:
        frozen=json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
        if frozen!=data:
            raise ForsakenTimingError("sealed published JAR evidence drift")
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("FORSAKEN_TIMING_1010_BEGIN")
    print(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("FORSAKEN_TIMING_1010_END")
    print("classes=2 exact_tick_methods=2 own_state_candidates=4 STATIC_ONLY_NO_MUTATION")

if __name__=="__main__":
    main()
