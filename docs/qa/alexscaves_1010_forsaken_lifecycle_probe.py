#!/usr/bin/env python3
"""Exact published 1.0.10 Forsaken AI lifecycle symbol audit (read-only).

Static selected-method provenance only: no Minecraft runtime, CFG execution,
automated hook permission or copying provider source implementation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file,javap,parse_methods
from alexscaves_1010_forsaken_sonic_probe import GOAL,ENTITY,CLASS_PINS,strict_pairs,digest_method
from alexscaves_1010_forsaken_helper_probe import exact_method

METHODS={
    GOAL:{
        "canReach":"(Lnet/minecraft/world/entity/LivingEntity;)Z",
        "startCleanJump":"()V",
        "findJumpTarget":"(Lnet/minecraft/world/entity/LivingEntity;Z)Lnet/minecraft/core/BlockPos;",
    },
    ENTITY:{
        "registerGoals":"()V",
        "tick":"()V",
        "customServerAiStep":"()V",
        "setSonarId":"(I)V",
        "setAnimationTick":"(I)V",
        "setLeaping":"(Z)V",
    },
}
HINTS=("sonic","sonar","animat","target","goal","attack","jump","leap",
       "navigation","darkness","running","sight","getrandom","level",
       "setsonic","getsonic","setanimation","isanimation","pickup",
       "schedule","isallied","tickcount","gettick","stun","canreach")
FIELDS=("getfield","putfield","getstatic","putstatic")
OPCODES={"bipush","sipush","ldc","ldc_w","ldc2_w"}
RETS={"return","areturn","ireturn","dreturn","freturn","lreturn"}
MAX_INSTRUCTIONS=4500
MAX_SELECTED=125
MAX_SITES=80
MAX_BRANCHES=220

class LifecycleProbeError(ValueError):
    pass

def selected_symbol(symbol):
    return bool(symbol) and any(tok in symbol.lower() for tok in HINTS)

def anchor(ins):
    return {k:ins[k] for k in ("offset","opcode","operand","symbol")}

def compact(method):
    instructions=method["instructions"]
    if not (0<len(instructions)<=MAX_INSTRUCTIONS):
        raise LifecycleProbeError("method size exceeds bounded audit")
    if len(instructions)!=len({x["offset"] for x in instructions}):
        raise LifecycleProbeError("duplicate instruction offsets")
    candidates=[i for i,v in enumerate(instructions)
                if (v["opcode"].startswith("invoke") or v["opcode"] in FIELDS)
                and selected_symbol(v["symbol"])]
    if len(candidates)>MAX_SELECTED:
        raise LifecycleProbeError("symbolic candidate budget exceeded")
    selected=[]
    for i in candidates:
        selected.append({
            "at":instructions[i]["offset"],
            "instruction":anchor(instructions[i]),
            "window":[anchor(x) for x in instructions[max(0,i-4):i+7]]
        })
    branches=[{"offset":v["offset"],"opcode":v["opcode"],"operand":v["operand"],
               "simple_target":int(v["operand"]) if v["operand"].isdecimal() else None}
              for v in instructions if v["opcode"].startswith("if") or
                  v["opcode"] in ("goto","goto_w","tableswitch","lookupswitch")]
    if len(branches)>MAX_BRANCHES:
        raise LifecycleProbeError("branch budget exceeded")
    numeric=[anchor(v) for v in instructions if v["opcode"] in OPCODES or
             v["opcode"].startswith(("iconst_","fconst_","dconst_","lconst_"))]
    returns=[{"at":v["offset"],"opcode":v["opcode"],
              "window":[anchor(x) for x in instructions[max(0,i-6):i+1]]}
             for i,v in enumerate(instructions) if v["opcode"] in RETS]
    if len(numeric)>500 or len(returns)>100:
        raise LifecycleProbeError("numeric/return budget exceeded")
    return {
        "header":method["header"],"descriptor":method["descriptor"],
        "method_sha256":digest_method(method),
        "instruction_count":len(instructions),
        "selected_symbol_windows":selected,
        "branches":branches,"numeric_constants":numeric,"returns":returns,
        "static_references_only":True,"runtime_reachability":"NOT_VERIFIED",
    }

def audit(jar,javap_bin):
    if sha_file(jar)!=(SHA1,SHA256,SIZE):
        raise LifecycleProbeError("exact published JAR SHA1/SHA256/size mismatch")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        if len(names)!=len(set(names)):
            raise LifecycleProbeError("duplicate JAR members")
        for cl,pin in CLASS_PINS.items():
            if hashlib.sha256(arc.read(cl)).hexdigest()!=pin:
                raise LifecycleProbeError("exact compiled class SHA mismatch")
    classes=[]
    for cl,targets in METHODS.items():
        methods=parse_methods(javap(javap_bin,jar,cl[:-6].replace("/",".")))
        selected=[{"name":name,**compact(exact_method(methods,name,desc))}
                  for name,desc in targets.items()]
        if len(selected)!=len(targets):
            raise LifecycleProbeError("missing exact selected methods")
        classes.append({"class_path":cl,"class_sha256":CLASS_PINS[cl],
                        "selected_methods":selected})
    return {
        "schema_version":1,
        "scope":"EXACT_1010_FORSAKEN_GOAL_REGISTRATION_AND_LIFECYCLE_SYMBOLS_ONLY",
        "jar":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "classes":classes,
        "limits":{"entire_cfg_and_exception_paths":"NOT_RECONSTRUCTED",
                  "goal_scheduler_order_in_world":"NOT_VERIFIED",
                  "target_selection_and_lockon_results":"NOT_VERIFIED",
                  "world_navigation_outcome":"NOT_VERIFIED",
                  "animation_tick_and_sonic_hit_counts":"NOT_VERIFIED",
                  "server_and_client_authority":"NOT_VERIFIED",
                  "mutating_hook":"NOT_VERIFIED",
                  "physical_qa":"NOT_TESTED",
                  "complete_perk_ready":False,"provider_universe_closed":False},
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    report=audit(args.jar,args.javap)
    if args.snapshot:
        frozen=json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
        if frozen!=report:
            raise LifecycleProbeError("tracked lifecycle snapshot differs from exact JAR")
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                   encoding="utf8")
    print("FORSAKEN_LIFECYCLE_1010_BEGIN")
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("FORSAKEN_LIFECYCLE_1010_END")
    print("classes=2 selected_methods=9 STATIC_ONLY_NO_MUTATION")

if __name__=="__main__":
    main()
