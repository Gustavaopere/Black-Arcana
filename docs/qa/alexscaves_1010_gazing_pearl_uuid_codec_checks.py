#!/usr/bin/env python3
"""Publisher SHA-exact fail-closed Gazing Pearl UUID codec and typed consumers.

Checks a 1.0.10 publisher JAR metadata report and hostile mutations. Does not
infer Minecraft's effective UUID NBT tag payload or physical persistence.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

REPORT_SHA="3db0c1c42736c6d4c67ab1b0682646d6ba499756ac15f83b7c8e3132548afa3e"
REPORT_BYTES=49616
ROSTER_SHA="9c6440ab63af01c68ff8b2a1f69e8cf45b16f639d7a6847609303bdf95b00eab"
ROSTER_BYTES=44289
REPORT_SCOPE="GAZING_PEARL_1010_ACCOMPAT_UUID_CODEC_DISCOVERY_ONLY"
SEAL_SCOPE="GAZING_PEARL_1010_ACCOMPAT_UUID_CODEC_STATIC_SUBCONTRACT_NOT_CERTIFIED"
COMPAT="com/github/alexmodguy/alexscaves/server/misc/ACCompat"
WORLD="com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData"
SAFE_STATES={
    "static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
    "provider_universe_closed":False,"semantic_magic_roots_delta":0
}
SAFE_LIMITS={
    "installed_copy":"NOT_VERIFIED","engine_uuid_payload_tag_type":"NOT_VERIFIED",
    "modlauncher_runtime":"NOT_OBSERVED","actual_save_restart":"NOT_TESTED",
    **SAFE_STATES
}

def need(ok,reason):
    if not ok: raise ValueError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pairs_unique(pairs):
    result={}
    for k,v in pairs:
        need(k not in result,"duplicate JSON key "+k)
        result[k]=v
    return result

def load(path,limit):
    raw=Path(path).read_bytes()
    need(0<len(raw)<limit,"empty or excessively large evidence")
    return json.loads(raw,object_pairs_hook=pairs_unique),raw

def canonical(data):
    return (json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()

def validate(report,seal,raw=None,strict=True):
    need(report["schema"]==seal["schema"]==1 and
         report["scope"]==REPORT_SCOPE and seal["scope"]==SEAL_SCOPE,
         "schema/scope mismatch")
    p=seal["provenance"]
    need(p["report_sha256"]==REPORT_SHA and p["report_bytes"]==REPORT_BYTES and
         p["discovery_run_id"]==45227358098 and
         p["discovery_job_id"]==137877321301 and
         p["discovery_head_sha"]=="2628fe90cd9185b77fdc0405e94480810a81119b",
         "source run/report provenance changed")
    if strict:
        need(raw is not None and len(raw)==REPORT_BYTES and sha(raw)==REPORT_SHA,
             "publisher report SHA-exact evidence mismatch")
    need(p["publisher_sha1"]=="6960b299a39a039ac8a5eb9b07be4ad0e3e0a570" and
         p["publisher_sha256"]=="36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c" and
         p["publisher_bytes"]==75279314 and
         p["publisher_classfiles"]==1555 and
         p["provider_version"]=="1.0.10" and
         p["minecraft"]=="1.21.1" and
         p["publisher_filename"]=="alexscaves-1.0.10-neoforge+1.21.1.jar",
         "publisher JAR version/identity drift")
    a=report["artifact"]
    need(a=={
        "publisher_filename":p["publisher_filename"],
        "publisher_sha256":p["publisher_sha256"],
        "publisher_bytes":p["publisher_bytes"],
        "physical_install_copy_verified":False
    },"report publisher identity drift")
    compat=report["compat"]; c=seal["compat"]
    need(compat["owner"]==c["owner"]==COMPAT and
         compat["sha256"]==c["class_sha256"]==
         "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b" and
         compat["declared_methods"]==c["declared_methods"]==200,
         "ACCompat publisher identity drift")
    expected=c["uuid_wrappers"]
    wrappers=compat["uuid_wrappers"]
    need(len(wrappers)==len(expected)==2 and
         [x["name"] for x in wrappers]==["getUUID","putUUID"],
         "UUID wrapper declaration roster drift")
    for got,pin in zip(wrappers,expected):
        need((got["name"],got["descriptor"],got["code_sha256"],
              got["instructions"],got["class_sha256"])==
             (pin["name"],pin["descriptor"],pin["code_sha256"],
              pin["instructions"],c["class_sha256"]),
             "ACCompat UUID wrapper Code/descriptor drift")
        require_shape={"conditional":0,"returns":1,"switch":0,"unconditional":0}
        need(got["branch_shape"]==require_shape and
             got["returns_boolean_or_uuid"]==got["descriptor"].split(")")[-1],
             "unexpected wrapper branch/return semantics")
        calls=got["direct_invocations"]
        need(len(calls)==1 and
             calls[0]=={
                 "owner":pin["callee_owner"],"name":pin["callee_name"],
                 "descriptor":pin["callee_descriptor"],"offset":pin["offset"],
                 "cp_index":pin["cp_index"],"kind":"Methodref",
                 "opcode":"invokevirtual"},
             "UUID wrapper native delegation changed")

    world=report["world"]; w=seal["world"]
    need(world["owner"]==w["owner"]==WORLD and
         world["sha256"]==w["class_sha256"]==
         "ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5" and
         world["caller_count"]==2,"ACWorldData authority/callers changed")
    census=report["direct_consumer_census"]
    summary=seal["typed_consumer_census"]
    need(len(census)==summary["owners"]==27 and
         [x["owner"] for x in census]==sorted(set(x["owner"] for x in census)),
         "unbounded/duplicated typed owner roster")
    cm=sum(len(x["callers"]) for x in census)
    cs=sum(len(c["sites"]) for x in census for c in x["callers"])
    need(cm==summary["methods"]==56 and
         cs==summary["callsites"]==63,"consumer method/callsite count drift")
    need(summary["roster_canonical_bytes"]==ROSTER_BYTES and
         summary["roster_sha256"]==ROSTER_SHA and
         len(canonical(census))==ROSTER_BYTES and
         sha(canonical(census))==ROSTER_SHA,"SHA-exact publisher consumer roster drift")
    need(summary["producer_consumers_with_shared_uuid_helper"]==[
         "com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity",WORLD] and
         summary["roster_not_whole_modpack"] is True,
         "cross-object scope confusion")

    ws=[x for x in census if x["owner"]==WORLD]
    need(len(ws)==1 and ws[0]["sha256"]==w["class_sha256"],
         "WorldData class caller absent/ambiguous")
    for fixed in w["selected"]:
        methods=[m for m in ws[0]["callers"] if m["method"]==fixed["method"]]
        need(len(methods)==1 and
             methods[0]["descriptor"]==fixed["descriptor"] and
             methods[0]["code_sha256"]==fixed["code_sha256"] and
             methods[0]["callsite_count"]==1,"WorldData method signature/Code changed")
        call=methods[0]["sites"][0]
        need(call=={
            "owner":COMPAT,"name":fixed["callee"],
            "descriptor":next(x["descriptor"] for x in expected if x["name"]==fixed["callee"]),
            "cp_index":fixed["cp_index"],"offset":fixed["offset"],
            "kind":"Methodref","opcode":"invokestatic"
        },"WorldData exact put/getUUID invocation changed")
    need(report["limits"]==SAFE_LIMITS and seal["states"]==SAFE_STATES and
         seal["limits"]=={
            "installed_copy":"NOT_VERIFIED","modlauncher_runtime":"NOT_OBSERVED",
            "engine_uuid_payload_tag_type":"NOT_VERIFIED",
            "actual_save_restart":"NOT_TESTED","stack_sync":"NOT_VERIFIED",
            "magic_roots_delta":0
         },"unjustified certification or runtime mutation")
    return len(census),cm,cs

def adversarial(report,seal):
    cases=[]
    def forge(label,path,value):
        obj=copy.deepcopy(report);target=obj
        for k in path[:-1]:target=target[k]
        target[path[-1]]=value
        cases.append((label,obj,seal))
    for i,x in enumerate(report["compat"]["uuid_wrappers"]):
        forge("forged wrapper Code "+str(i),
              ["compat","uuid_wrappers",i,"code_sha256"],"0"*64)
        forge("forged wrapper dispatch "+str(i),
              ["compat","uuid_wrappers",i,"direct_invocations",0,"owner"],"fake/CompoundTag")
    for i,o in enumerate(report["direct_consumer_census"]):
        forge("forged consumer class "+str(i),
              ["direct_consumer_census",i,"sha256"],"0"*64)
        for j,m in enumerate(o["callers"]):
            for k,site in enumerate(m["sites"]):
                forge("forged callsite offset "+str(i)+":"+str(j)+":"+str(k),
                      ["direct_consumer_census",i,"callers",j,"sites",k,"offset"],
                      site["offset"]+1)
    for key,new in (
        ("installed_copy","VERIFIED"),("engine_uuid_payload_tag_type","IntArrayTag"),
        ("modlauncher_runtime","VERIFIED"),("actual_save_restart","PASSED"),
        ("static_contract","CERTIFIED"),("mutating_hook","VERIFIED"),
        ("physical_qa","PASSED"),("mutation","MUTATION"),
        ("provider_universe_closed",True),("semantic_magic_roots_delta",1)):
        forge("unsafe promotion "+key,["limits",key],new)
    tamper=copy.deepcopy(seal);tamper["states"]["mutating_hook"]="VERIFIED"
    cases.append(("forged manifest hook",report,tamper))
    tamper=copy.deepcopy(seal);tamper["typed_consumer_census"]["roster_sha256"]="0"*64
    cases.append(("forged manifest SHA",report,tamper))
    rejected=0
    for label,r,s in cases:
        try: validate(r,s,strict=False)
        except (ValueError,KeyError,IndexError,TypeError): rejected+=1
        else: raise AssertionError("forgery accepted: "+label)
    need(rejected==len(cases) and rejected>=100,
         "insufficient adverse test coverage")
    return rejected

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--adversarial",action="store_true")
    a=p.parse_args()
    r,raw=load(a.report,180_000)
    s,_=load(a.manifest,100_000)
    owners,methods,sites=validate(r,s,raw)
    print("EXACT_UUID_REPORT_SHA256",sha(raw),"BYTES",len(raw),
          "OWNERS",owners,"METHODS",methods,"SITES",sites)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED",adversarial(r,s))
    print("OK: publisher UUID wrappers/consumers only; NO_MUTATION NOT_CERTIFIED")

if __name__=="__main__":
    main()
