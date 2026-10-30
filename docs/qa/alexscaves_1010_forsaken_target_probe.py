#!/usr/bin/env python3
"""Bounded, exact 1.0.10 Forsaken TARGETING predicate and goal lifecycle ABI.

Publisher JAR provenance; static, selected method evidence ONLY.
Does not validate scheduling, multiplayer targeting outcomes or mutating hooks.
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
from alexscaves_1010_forsaken_helper_probe import COMPAT,EXACT_CLASSES

SELECTION={
    ENTITY:[("lambda$static$0","(Lnet/minecraft/world/entity/LivingEntity;)Z")],
    COMPAT:[("targetSelector","(Ljava/util/function/Predicate;)Ljava/util/function/Predicate;")],
    GOAL:[("canUse","()Z"),("start","()V"),("stop","()V")],
}
MAX_INSTR=420
MAX_WINDOWS=90
MAX_BRANCHES=85
KEYOPS=("invoke","getfield","putfield","getstatic","putstatic","instanceof",
        "checkcast","invokedynamic","new")

class ForsakenTargetingError(ValueError):
    pass

def exact(methods,name,desc):
    selected=[m for m in methods
              if m["descriptor"]==desc and re.search(r"(?<![A-Za-z0-9_$])"+re.escape(name)+r"\(",m["header"])]
    if len(selected)!=1:
        raise ForsakenTargetingError("missing/ambiguous target ABI "+name)
    return selected[0]

def row(inst):
    return {key:inst[key] for key in ("offset","opcode","operand","symbol")}

def compact(m):
    ins=m["instructions"]
    if not 1<=len(ins)<=MAX_INSTR:
        raise ForsakenTargetingError("targeting method instruction budget exceeded")
    if len({i["offset"] for i in ins})!=len(ins):
        raise ForsakenTargetingError("duplicate bytecode offset")
    sites=[]
    for n,inst in enumerate(ins):
        if inst["opcode"].startswith(KEYOPS):
            sites.append({"offset":inst["offset"],"instruction":row(inst),
                          "window":[row(v) for v in ins[max(0,n-5):n+9]]})
    if len(sites)>MAX_WINDOWS:
        raise ForsakenTargetingError("symbol-window count exceeded")
    branches=[row(i) for i in ins
              if i["opcode"].startswith("if") or i["opcode"] in ("goto","goto_w","tableswitch","lookupswitch")]
    constants=[row(i) for i in ins
               if i["opcode"].startswith(("iconst_","fconst_","dconst_","lconst_"))
               or i["opcode"] in ("bipush","sipush","ldc","ldc_w","ldc2_w")]
    if max(len(branches),len(constants))>MAX_BRANCHES:
        raise ForsakenTargetingError("branch/numeric bound exceeded")
    returns=[{"offset":i["offset"],"opcode":i["opcode"]}
             for i in ins if i["opcode"] in ("ireturn","areturn","return","athrow")]
    return {"header":m["header"],"descriptor":m["descriptor"],
            "parsed_method_sha256":digest_method(m),"instruction_count":len(ins),
            "selected_symbolic_windows":sites,"branch_anchors":branches,
            "constant_anchors":constants,"exit_sites":returns,
            "runtime_goal_reachability":"NOT_VERIFIED"}

def audit(jar,javap_bin):
    if sha_file(jar)!=(SHA1,SHA256,SIZE):
        raise ForsakenTargetingError("SHA1/SHA256/size JAR pin mismatch")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        if len(names)!=len(set(names)):
            raise ForsakenTargetingError("duplicate member")
        for path,sha in EXACT_CLASSES.items():
            if hashlib.sha256(arc.read(path)).hexdigest()!=sha:
                raise ForsakenTargetingError("class pin mismatch "+path)
    classes=[]
    for path,targets in SELECTION.items():
        methods=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        selected=[{"name":name,**compact(exact(methods,name,desc))}
                  for name,desc in targets]
        classes.append({"class_path":path,"class_sha256":EXACT_CLASSES[path],
                        "selected_methods":selected})
    predicate=classes[0]["selected_methods"][0]
    bridge=classes[1]["selected_methods"][0]
    if predicate["descriptor"]!="(Lnet/minecraft/world/entity/LivingEntity;)Z":
        raise ForsakenTargetingError("lambda descriptor drift")
    if bridge["descriptor"]!="(Ljava/util/function/Predicate;)Ljava/util/function/Predicate;":
        raise ForsakenTargetingError("predicate bridge descriptor drift")
    return {"schema_version":1,
            "scope":"EXACT_1010_FORSAKEN_TARGET_PREDICATE_AND_GOAL_GATES_ONLY",
            "publisher_jar":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "classes":classes,
            "limits":{"selected_provider_methods_only":True,
                      "vanilla_goal_scheduler_and_targeting":"NOT_AUDITED",
                      "other_mods_datapacks_tags":"NOT_RESOLVED",
                      "target_results_owner_pvp":"NOT_VERIFIED",
                      "call_graph_and_exception_cfg":"NOT_RECONSTRUCTED",
                      "mutating_hook":"NOT_VERIFIED",
                      "physical_qa":"NOT_TESTED",
                      "complete_perk_ready":False,
                      "provider_universe_closed":False}}

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
            raise ForsakenTargetingError("sealed exact targeting evidence changed")
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("FORSAKEN_TARGETS_1010_BEGIN")
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("FORSAKEN_TARGETS_1010_END")
    print("classes=3 selected_methods=5 STATIC_ONLY_NO_MUTATION")
if __name__=="__main__":
    main()
