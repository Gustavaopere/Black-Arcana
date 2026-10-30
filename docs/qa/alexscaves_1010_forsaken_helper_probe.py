#!/usr/bin/env python3
"""Bounded SHA-exact Forsaken animation, damage-gate and knockback helper audit.

Source is the installed Alex's Caves Continued 1.0.10 publisher JAR only.
This is clean-room interoperability evidence, not copied implementation,
observed gameplay, a complete control-flow graph, or permission to mutate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,BASE,sha_file,javap,parse_methods
from alexscaves_1010_forsaken_sonic_probe import GOAL,ENTITY,CLASS_PINS,strict_pairs,digest_method

COMPAT=BASE+"server/misc/ACCompat.class"
EXACT_CLASSES={**CLASS_PINS,COMPAT:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b"}
TARGETS={
    GOAL:[
        ("isMovementFrozen","()Z"),
        ("tryAnimation","(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)Z"),
        ("checkAndDealDamage","(Lnet/minecraft/world/entity/LivingEntity;DF)Z"),
        ("knockBackAngle","(Lnet/minecraft/world/entity/LivingEntity;DF)V"),
    ],
    ENTITY:[
        ("hasSonicCharge","()Z"),
        ("setSonicCharge","(Z)V"),
        ("getSonarTarget","()Lnet/minecraft/world/entity/Entity;"),
        ("getAnimation","()Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;"),
        ("setAnimation","(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)V"),
    ],
    COMPAT:[
        ("knockback","(Lnet/minecraft/world/entity/LivingEntity;DDD)V"),
    ],
}
KNOWN_SHA={
    (GOAL,"knockBackAngle","(Lnet/minecraft/world/entity/LivingEntity;DF)V"):
        "8ef9a3e156ca8311e23507cde598367388a0ceffd92e5bf7fd33f09f003003fa",
}
FIELD={"getfield","putfield","getstatic","putstatic"}
BRANCH={"goto","goto_w","tableswitch","lookupswitch"}
NUMERIC={"bipush","sipush","ldc","ldc_w","ldc2_w"}
RETURNS={"ireturn","lreturn","freturn","dreturn","areturn","return"}

class ForsakenHelperError(ValueError):
    pass

def exact_method(methods,name,descriptor):
    options=[m for m in methods
             if m["descriptor"]==descriptor and
                (name+"(") in m["header"]]
    if len(options)!=1:
        raise ForsakenHelperError("JVM method ambiguous/missing "+name+" "+descriptor)
    return options[0]

def instruction_record(i):
    return {key:i[key] for key in ("offset","opcode","operand","symbol")}

def bounded_window(seq,i,before=7,after=7):
    return [instruction_record(x) for x in seq[max(0,i-before):i+after+1]]

def compact(method,path,name):
    instructions=method["instructions"]
    if not 1<=len(instructions)<=1400:
        raise ForsakenHelperError("unbounded instruction population "+name)
    if len({x["offset"] for x in instructions})!=len(instructions):
        raise ForsakenHelperError("duplicate bytecode offsets")
    descriptor=method["descriptor"]
    digest=digest_method(method)
    previous=KNOWN_SHA.get((path,name,descriptor))
    if previous and digest!=previous:
        raise ForsakenHelperError("prior certified method digest changed: "+name)
    symbols=[];branches=[];numeric=[];exits=[]
    for index,inst in enumerate(instructions):
        opcode=inst["opcode"]
        if opcode.startswith("invoke") or opcode in FIELD:
            symbols.append(instruction_record(inst))
        if opcode.startswith("if") or opcode in BRANCH:
            branches.append({
                **instruction_record(inst),
                "simple_target":int(inst["operand"]) if inst["operand"].isdecimal() else None,
            })
        if (opcode in NUMERIC or opcode.startswith(("iconst_","lconst_","fconst_","dconst_"))):
            numeric.append(instruction_record(inst))
        if opcode in RETURNS:
            exits.append({"at":inst["offset"],"opcode":opcode,
                          "window":bounded_window(instructions,index,11,0)})
    if max(map(len,(symbols,branches,numeric,exits)))>250:
        raise ForsakenHelperError("anchor budget exceeded "+name)
    return {
        "name":name,"header":method["header"],"descriptor":descriptor,
        "method_sha256":digest,
        "instruction_count":len(instructions),
        "symbolic_invocations_and_fields":symbols,
        "branch_anchors":branches,
        "constant_anchors":numeric,
        "return_instruction_windows":exits,
        "decision_reachability":"NOT_VERIFIED",
        "dynamic_targets_and_damage":"NOT_TESTED",
        "mutating_hook":"NOT_VERIFIED",
    }

def audit(jar,javap_bin):
    if sha_file(jar)!=(SHA1,SHA256,SIZE):
        raise ForsakenHelperError("publisher artifact SHA1/SHA256/size mismatch")
    out=[]
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        if len(names)!=len(set(names)):
            raise ForsakenHelperError("duplicate JAR members")
        for path, expected in EXACT_CLASSES.items():
            actual=hashlib.sha256(arc.read(path)).hexdigest()
            if actual!=expected:
                raise ForsakenHelperError("exact class SHA drift: "+path)
            methods=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
            entries=[]
            for name,descriptor in TARGETS[path]:
                entries.append(compact(exact_method(methods,name,descriptor),path,name))
            out.append({"class_path":path,"class_sha256":actual,"methods":entries})
    return {
        "schema_version":1,
        "scope":"EXACT_1010_FORSAKEN_SELECTED_ANIMATION_AND_KNOCKBACK_HELPER_ABI_ONLY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "classes":out,
        "limits":{
            "method_bodies_copied":False,
            "selected_methods_only":True,
            "goal_scheduler_and_minecraft_base_classes":"NOT_AUDITED",
            "execution_cfg_and_exception_paths":"NOT_RECONSTRUCTED",
            "real_hit_counts_and_damage":"NOT_VERIFIED",
            "permission_and_pvp":"NOT_VERIFIED",
            "runtime_knockback_acceptance":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "complete_perk_ready":False,
            "provider_universe_closed":False,
        }
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True)
    parser.add_argument("--javap",required=True)
    parser.add_argument("--snapshot")
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result=audit(args.jar,args.javap)
    if args.snapshot:
        frozen=json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
        if frozen!=result:
            raise ForsakenHelperError("SHA-exact helper snapshot drift")
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FORSAKEN_HELPERS_1010_BEGIN")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("FORSAKEN_HELPERS_1010_END")
    print("classes="+str(len(result["classes"]))+
          " selected_methods="+str(sum(len(x["methods"]) for x in result["classes"]))+
          " STATIC_ONLY_NO_MUTATION")

if __name__=="__main__":
    main()
