#!/usr/bin/env python3
"""Read-only, SHA-exact Alex's Caves 1.0.10 Forsaken Sonic Boom flow audit.

Selected JVM symbolic/constant/branch anchors enable interoperability research,
not full provider logic reproduction, runtime simulation or a mutating perk hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, BASE, sha_file, javap, parse_methods
)

GOAL=BASE+"server/entity/ai/ForsakenAttackGoal.class"
ENTITY=BASE+"server/entity/living/ForsakenEntity.class"
CLASS_PINS={
    GOAL:"48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55",
    ENTITY:"72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1",
}
METHOD_PINS={
    (GOAL,"tick","()V"):
        "1fb8ecdd23c6c76d836ee25a4176f788163ef1226220a142a40e5f48d4df8abe",
    (ENTITY,"getSonicDamageAgainst","(Lnet/minecraft/world/entity/LivingEntity;)F"):
        "db47e82eebdb86724b6a71164ca563d0a75910bb143c16b944a5beb63f537d88",
}
SELECTION={
    GOAL:{"tick","canUse","canContinueToUse","start","stop","knockBackAngle",
          "canAttack","getAttackReachSqr"},
    ENTITY:{"hasLineOfSight","getSonicDamageAgainst","getAnimationTick"},
}
HIT_SITES={
    108:"causeForsakenSonicBoomDamage",
    119:"LivingEntity.hurt",
    576:"causeForsakenSonicBoomDamage",
    596:"LivingEntity.hurt",
}
WINDOW_OFFSETS={
    GOAL:{"tick":[0,20,50,75,87,108,119,130,140,180,230,300,400,460,500,
                   540,551,557,576,584,587,590,592,596,600,603,610,620,680,800]},
    ENTITY:{"getSonicDamageAgainst":[7,13,16,19,22,25]},
}
CONST=re.compile(r"^(?:[bidsfl]const_[\w-]+|bipush|sipush|ldc(?:_w|2_w)?)$")
CALLS={"getfield","putfield","getstatic","putstatic","invokevirtual","invokestatic",
       "invokespecial","invokeinterface","invokedynamic"}
BRANCHES={"goto","goto_w","tableswitch","lookupswitch","jsr","jsr_w"}
MAX_SELECTED=22
MAX_ANCHORS_PER_METHOD=500
MAX_WINDOW_SIZE=30

class ForsakenEvidenceError(ValueError):
    pass

def strict_pairs(pairs):
    d={}
    for k,v in pairs:
        if k in d:
            raise ForsakenEvidenceError("duplicate JSON key: "+k)
        d[k]=v
    return d

def method_name(m):
    match=re.search(r"([\w$<>]+)\(",m["header"])
    return match.group(1) if match else None

def clipped(seq,pos,radius=9):
    return [
        {k:i[k] for k in ("offset","opcode","operand","symbol")}
        for i in seq[max(0,pos-radius):pos+radius+1]
    ]

def digest_method(method):
    return hashlib.sha256(json.dumps(
        method,ensure_ascii=False,sort_keys=True,separators=(",",":")
    ).encode("utf8")).hexdigest()

def summarize(path,method):
    name=method_name(method)
    desc=method["descriptor"]
    inst=method["instructions"]
    if not 1<=len(inst)<=1800:
        raise ForsakenEvidenceError("instruction budget for "+str(name))
    byoffset={}
    for ix,item in enumerate(inst):
        if item["offset"] in byoffset:
            raise ForsakenEvidenceError("duplicate bytecode offset")
        byoffset[item["offset"]]=ix
    digest=digest_method(method)
    pin=METHOD_PINS.get((path,name,desc))
    if pin and pin!=digest:
        raise ForsakenEvidenceError("previous SHA-exact method pin differs: "+name)
    symbolic=[{k:i[k] for k in ("offset","opcode","symbol")} for i in inst
              if i["opcode"] in CALLS]
    branches=[{
        "offset":i["offset"],"opcode":i["opcode"],"operand":i["operand"],
        "simple_target":int(i["operand"]) if i["operand"].isdecimal() else None
    } for i in inst if i["opcode"].startswith("if") or i["opcode"] in BRANCHES]
    constants=[{k:i[k] for k in ("offset","opcode","operand","symbol")} for i in inst
               if CONST.match(i["opcode"])]
    if max(len(symbolic),len(branches),len(constants))>MAX_ANCHORS_PER_METHOD:
        raise ForsakenEvidenceError("symbol budget exceeded "+name)
    windows=[]
    for offset in WINDOW_OFFSETS.get(path,{}).get(name,[]):
        if offset in byoffset:
            seq=clipped(inst,byoffset[offset],8)
            if len(seq)>MAX_WINDOW_SIZE:
                raise ForsakenEvidenceError("window budget exceeded")
            windows.append({"at":offset,"instruction_window":seq})
    if path==GOAL and name=="tick":
        sites=[]
        for offset,symbol in HIT_SITES.items():
            if offset not in byoffset:
                raise ForsakenEvidenceError("missing sealed callsite "+str(offset))
            code=inst[byoffset[offset]]
            if not code["opcode"].startswith("invoke") or symbol not in code["symbol"]:
                raise ForsakenEvidenceError("wrong callsite at "+str(offset))
            sites.append({"offset":offset,"symbol":code["symbol"]})
    else:
        sites=[]
    return {
        "header":method["header"],"descriptor":desc,
        "parsed_method_sha256":digest,"instruction_count":len(inst),
        "symbolic_method_and_field_anchors":symbolic,
        "branch_anchors":branches,
        "numeric_constant_anchors":constants,
        "selected_windows":windows,
        "sealed_hurt_factory_sites":sites,
        "runtime_reachability":"NOT_PROVEN",
        "hook_mutability":"NOT_VERIFIED",
    }

def audit(jar,javap_bin):
    if sha_file(jar)!=(SHA1,SHA256,SIZE):
        raise ForsakenEvidenceError("publisher JAR pin mismatch")
    with zipfile.ZipFile(jar) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):
            raise ForsakenEvidenceError("duplicate JAR member")
        for path,pin in CLASS_PINS.items():
            if hashlib.sha256(archive.read(path)).hexdigest()!=pin:
                raise ForsakenEvidenceError("exact class hash drift "+path)
    classes=[]
    for path in (GOAL,ENTITY):
        methods=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        inventory=[{"header":m["header"],"descriptor":m["descriptor"]}
                   for m in methods]
        selected=[]
        for m in methods:
            name=method_name(m)
            if name in SELECTION[path]:
                selected.append({"name":name,**summarize(path,m)})
        if len(selected)>MAX_SELECTED or not selected:
            raise ForsakenEvidenceError("selected method population unsafe")
        classes.append({"class_path":path,"class_sha256":CLASS_PINS[path],
                        "method_inventory":inventory,"selected_methods":selected})
    goal=classes[0]
    hits=[m for m in goal["selected_methods"] if m["name"]=="tick" and m["descriptor"]=="()V"]
    if len(hits)!=1 or len(hits[0]["sealed_hurt_factory_sites"])!=4:
        raise ForsakenEvidenceError("missing exact goal.tick and four anchor sites")
    sonic=[m for m in classes[1]["selected_methods"]
           if m["name"]=="getSonicDamageAgainst" and
           m["descriptor"]=="(Lnet/minecraft/world/entity/LivingEntity;)F"]
    if len(sonic)!=1:
        raise ForsakenEvidenceError("missing exact sonic target helper")
    return {
        "schema_version":1,
        "scope":"EXACT_1010_FORSAKEN_SONIC_SELECTED_CALL_AND_CONTROL_ANCHORS_ONLY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "classes":classes,
        "bounds":{
            "full_source_reproduced":False,
            "methods_selected_only":True,
            "exception_cfg_and_loop_reachability":"NOT_RECONSTRUCTED",
            "runtime_targets_and_damage":"NOT_VERIFIED",
            "data_pack_tags":"NOT_RESOLVED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "complete_perk_ready":False,
            "provider_universe_closed":False,
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    a=p.parse_args()
    result=audit(a.jar,a.javap)
    if a.snapshot:
        target=json.loads(Path(a.snapshot).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
        if target!=result:
            raise ForsakenEvidenceError("SHA-exact snapshot mismatch")
    out=Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("FORSAKEN_SONIC_1010_BEGIN")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("FORSAKEN_SONIC_1010_END")
    print("selected_methods="+str(sum(len(x["selected_methods"]) for x in result["classes"]))+
          " two_factories_two_hurt_calls STATIC_ONLY_NO_HOOK_CERTIFICATION")

if __name__=="__main__":
    main()
