#!/usr/bin/env python3
"""SHA-exact official NeoForge 21.1.248 denial-guard evidence checker.

Pins published-distribution classfiles, typed JVM member references, Code
hashes, branch offsets and return sites. Each adversarial change bypasses ONLY
the outer report SHA to test independent manifest/anchor constraints.
No installed ModLauncher runtime, real UUID collision, inventory or gameplay.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

SCOPE_REPORT="GALENA_NEOFORGE_211248_DISTRIBUTED_DENIAL_GUARD_DISCOVERY_ONLY"
SCOPE_SEAL="GALENA_NEOFORGE_211248_DISTRIBUTED_DENIAL_GUARD_STATIC_SEAL_ONLY"
REPORT_SHA="c9b4691fbb4a7c1f54964fe568abad111fd891b51543251b3782545adb6c8473"
REPORT_BYTES=19914
CLASS_SHA={
    "ServerLevel":"19b42e51848fd27df3683dacf694baa5126ee9f0665f12afdc65f82493a1e5a3",
    "PersistentEntitySectionManager":"6351fcb7c7370b77b8d9618474783b58ab3e037c224b5c83481c23908db1fbf4",
}
REPORT_LIMITS={
    "stack_consumption_order":"PUBLISHER_CALL_ORDER_ONLY",
    "minecraft_modlauncher_classes":"NOT_OBSERVED",
    "real_warehouse_inventory":"NOT_TESTED",
    "runtime_spawn_denial":"NOT_VERIFIED",
    "uuid_duplicate_scenario":"NOT_TESTED",
    "world_protection":"NOT_VERIFIED",
    "all_denial_causes_exhausted":False,
    "galena_static_contract":"NOT_CERTIFIED",
    "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "provider_universe_closed":False,
    "semantic_magic_roots_delta":0,
}
SEAL_STATE={
    "static_contract":"NOT_CERTIFIED",
    "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "provider_universe_closed":False,
    "semantic_magic_roots_delta":0,
}
SEAL_LIMITS={
    "modlauncher_loaded_bytecode":"NOT_OBSERVED",
    "installed_modpack":"NOT_VERIFIED",
    "actual_uuid_collision":"NOT_TESTED",
    "actual_spawn_denial":"NOT_TESTED",
    "real_item_loss_or_rollback":"NOT_TESTED",
    "all_failure_paths_exhausted":False,
    "engine_exception_flow":"NOT_MODELED",
    "not_runtime_authority":True,
}

def need(ok, reason):
    if not ok:
        raise ValueError(reason)

def unique(items):
    r={}
    for k,v in items:
        need(k not in r,"duplicate JSON key "+k)
        r[k]=v
    return r

def load(path, ceiling):
    raw=Path(path).read_bytes()
    need(0<len(raw)<=ceiling,"invalid evidence size")
    return json.loads(raw,object_pairs_hook=unique),raw

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(rows):
    return (json.dumps(rows,sort_keys=True,separators=(",",":"),
                       ensure_ascii=False)+"\n").encode()

def get_method(report, owner, name):
    methods=report["classes"][owner]["methods"]
    need(name in methods and methods[name]["present"] is True,
         "missing executable method "+owner+"."+name)
    return methods[name]

def at_ref(method, item):
    hits=[x for x in method["typed_members"]
          if x["offset"]==item["offset"] and x["owner"]==item["owner"]
          and x["name"]==item["name"]
          and ("descriptor" not in item or x["descriptor"]==item["descriptor"])]
    need(len(hits)==1,"typed JVM ref altered "+str(item))

def at_branch(method, item):
    hits=[x for x in method["branches"]
          if all(x[k]==item[k] for k in ("offset","opcode","target","fallthrough"))]
    need(len(hits)==1,"branch pivot altered "+str(item))

def at_terminal(method, item):
    hits=[x for x in method["terminals"]
          if all(x[k]==item[k] for k in ("offset","opcode","previous_opcode"))]
    need(len(hits)==1,"return pivot altered "+str(item))

def validate(report,seal,*,raw=None,strict=True):
    need(report["schema"]==seal["schema"]==1 and
         report["scope"]==SCOPE_REPORT and seal["scope"]==SCOPE_SEAL,
         "schema or scope drift")
    src=seal["provenance"]
    need(src["report_sha256"]==REPORT_SHA and src["report_bytes"]==REPORT_BYTES
         and src["discovery_run"]==45232344296
         and src["discovery_job"]==137894927228
         and src["discovery_head_sha"]=="7bd94be896b2423aa883ab676bc7f21486dbcec7"
         and src["minecraft_version"]=="1.21.1"
         and src["neo_version"]=="21.1.248"
         and src["install_server_overlay_sha256"]==
             "1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359"
         and src["install_srg_sha256"]==
             "26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71"
         and src["publisher_alexscaves_sha256"]==
             "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
         "provenance cannot be changed")
    if strict:
        need(raw is not None and len(raw)==REPORT_BYTES and sha(raw)==REPORT_SHA,
             "exact report bytes/hash mismatch")
    distribution=report["artifact"]
    need(distribution["neoforge_version"]=="21.1.248" and
         distribution["minecraft_version"]=="1.21.1" and
         distribution["neoforge_server_sha256"]==src["install_server_overlay_sha256"]
         and distribution["minecraft_srg_sha256"]==src["install_srg_sha256"]
         and distribution["modlauncher_loaded_bytes"]=="NOT_OBSERVED",
         "distributed engine cannot be replaced by runtime claim")
    need(set(report["classes"])==set(CLASS_SHA)==set(seal["class_sha256"]),
         "class roster")
    for owner,pin in CLASS_SHA.items():
        row=report["classes"][owner]
        need(row["class_sha256"]==pin==seal["class_sha256"][owner] and
             row["source"]=="NEOFORGE_211248_SERVER_OVERLAY_UNTRANSFORMED",
             "class SHA/identity")
    assert_methods=seal["exact_methods"]
    need(len(assert_methods)==4 and
         {(p["owner"],p["name"]) for p in assert_methods}==
         {("ServerLevel","addEntity"),
          ("PersistentEntitySectionManager","addEntity"),
          ("PersistentEntitySectionManager","addEntityUuid"),
          ("PersistentEntitySectionManager","addEntityWithoutEvent")},
         "method roster")
    count_refs=0
    for pin in assert_methods:
        m=get_method(report,pin["owner"],pin["name"])
        need(m["code_sha256"]==pin["code_sha256"] and
             m["instruction_count"]==pin["instructions"] and
             len(m["typed_members"])==pin["members"] and
             len(m["branches"])==pin["branches"] and
             len(m["terminals"])==pin["returns"],
             "Code or method count drift")
        need(sha(canonical(m["typed_members"]))==pin["members_sha256"] and
             sha(canonical(m["branches"]))==pin["branches_sha256"] and
             sha(canonical(m["terminals"]))==pin["terminals_sha256"] and
             m["exception_handler_count"]==0,
             "typed refs/branch/return hashes must match")
        count_refs+=len(m["typed_members"])
    need(count_refs==35,"unexpected member evidence census")

    c=seal["causal_anchors"]
    need(set(c)=={"server_removed_guard","manager_duplicate_uuid_guard",
                  "manager_duplicate_before_registration",
                  "manager_event_cancel_before_uuid","server_manager_result"},
         "causal pivot roster")

    for key in ("server_removed_guard","manager_duplicate_before_registration",
                "manager_event_cancel_before_uuid","server_manager_result"):
        a=c[key]
        m=get_method(report,a["owner"],a["method"])
        at_ref(m,a["typed_ref"])
        at_branch(m,a["branch"])
        at_terminal(m,a["false_return"])
    d=c["manager_duplicate_uuid_guard"]
    m=get_method(report,d["owner"],d["method"])
    for ref in d["typed_refs"]:
        at_ref(m,ref)
    at_branch(m,d["branch"])
    at_terminal(m,d["false_return"])
    at_terminal(m,d["true_return"])
    b=c["manager_duplicate_before_registration"]
    for key,offset in b["post_guard_record"].items():
        search=[r for r in get_method(report,b["owner"],b["method"])["typed_members"]
                if r["offset"]==offset]
        need(len(search)==1,"missing post-UUID registration callback "+key)
    for item in b["non_failure_conditions"]:
        q=[t for t in get_method(report,b["owner"],b["method"])["branches"]
           if t["offset"]==item["offset"] and t["opcode"]==item["opcode"]]
        need(len(q)==1,"nonfailure callback guard altered")
    r=c["server_manager_result"]
    at_ref(get_method(report,r["owner"],r["method"]),r["accepted_callback"])
    at_terminal(get_method(report,r["owner"],r["method"]),r["true_return"])
    need(report["limits"]==REPORT_LIMITS and
         seal["state"]==SEAL_STATE and seal["limits"]==SEAL_LIMITS,
         "unsafe status/certification promotion")
    return len(assert_methods),count_refs


def adversarial(report,seal):
    cases=[]
    def modify(label, path, value):
        r=copy.deepcopy(report)
        target=r
        for part in path[:-1]:
            target=target[part]
        target[path[-1]]=value
        cases.append((label,r,seal))
    for pin in seal["exact_methods"]:
        owner,name=pin["owner"],pin["name"]
        p=["classes",owner,"methods",name]
        modify("forged code "+owner+name,p+["code_sha256"],"0"*64)
        modify("forged typed member "+owner+name,p+["typed_members",0,"owner"],"fake/Owner")
        modify("forged branch "+owner+name,p+["branches",0,"target"],999)
        modify("forged return "+owner+name,p+["terminals",0,"previous_opcode"],"nop")
    for key,value in (
        ("stack_consumption_order","COMPENSATED"),
        ("minecraft_modlauncher_classes","VERIFIED"),
        ("real_warehouse_inventory","VERIFIED"),
        ("runtime_spawn_denial","VERIFIED"),
        ("uuid_duplicate_scenario","PASSED"),
        ("world_protection","VERIFIED"),
        ("all_denial_causes_exhausted",True),
        ("galena_static_contract","CERTIFIED"),
        ("mutating_hook","VERIFIED"),
        ("physical_qa","PASSED"),
        ("mutation","MUTATION"),
        ("provider_universe_closed",True),
        ("semantic_magic_roots_delta",1),
    ):
        modify("unsafe claim "+key,["limits",key],value)
    modify("wrong engine",["artifact","neoforge_version"],"21.1.250")
    modify("fake prior class",["classes","ServerLevel","class_sha256"],"0"*64)
    modify("fake UUID method missing",["classes","PersistentEntitySectionManager",
                                         "methods","addEntityUuid","present"],False)
    for key in ("server_removed_guard","manager_duplicate_uuid_guard",
                "manager_duplicate_before_registration",
                "manager_event_cancel_before_uuid","server_manager_result"):
        s=copy.deepcopy(seal)
        s["causal_anchors"][key]["branch"]["target"]=998
        cases.append(("forged seal branch "+key,report,s))
    s=copy.deepcopy(seal)
    s["exact_methods"][0]["members_sha256"]="0"*64
    cases.append(("forged seal member digest",report,s))
    s=copy.deepcopy(seal)
    s["state"]["mutating_hook"]="VERIFIED"
    cases.append(("forged seal unsafe mutation",report,s))
    for label,r,s in cases:
        try:
            validate(r,s,strict=False)
        except (ValueError,KeyError,TypeError,IndexError):
            continue
        raise AssertionError("adversarial forgery accepted: "+label)
    need(len(cases)>=35,"insufficient adversarial cases")
    return len(cases)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--adversarial",action="store_true")
    a=p.parse_args()
    report,raw=load(a.report,100_000)
    seal,_=load(a.manifest,100_000)
    count,refs=validate(report,seal,raw=raw)
    print("EXACT_REPORT_SHA256",sha(raw),"BYTES",len(raw),
          "METHODS",count,"TYPED_MEMBERS",refs)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED",adversarial(report,seal))
    print("OK: publisher-exact distributed denial guards; NO_MUTATION NO_QA")


if __name__=="__main__":
    main()
