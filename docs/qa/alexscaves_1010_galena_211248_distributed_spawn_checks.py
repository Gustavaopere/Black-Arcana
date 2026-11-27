#!/usr/bin/env python3
"""Fail-closed exact official distributed NeoForge 21.1.248 spawn ABI verifier.

Checks class/code/typed-JVM-invocation fingerprints; rejects forged reports
and fabricated runtime/physical certifications. Not ModLauncher-transformed
code and NOT a safe Galena mutation hook.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

REPORT_SHA = "b83db649e207ae7edf4fe8cc6c4c8db935fbe8ef6ceaccc15859a1a535f15342"
REPORT_BYTES = 13544
REPORT_SCOPE = "GALENA_NEOFORGE_211248_DISTRIBUTED_ENTITY_ADMISSION_ABI_DISCOVERY_ONLY"
SEAL_SCOPE = "GALENA_NEOFORGE_211248_DISTRIBUTED_ENTITY_ADMISSION_ABI_SEAL_ONLY"
NEO_SERVER_SHA = "1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359"
MC_SRG_SHA = "26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71"
CLASS_NAMES = {
    "Level": "net/minecraft/world/level/Level",
    "ServerLevel": "net/minecraft/server/level/ServerLevel",
    "LevelWriter": "net/minecraft/world/level/LevelWriter",
    "PersistentEntitySectionManager":
        "net/minecraft/world/level/entity/PersistentEntitySectionManager",
}
STATUS = {
    "installed_modpack_parity": "NOT_VERIFIED",
    "modlauncher_transformed_bytecode": "NOT_OBSERVED",
    "real_galena_entity_join_event": "NOT_VERIFIED",
    "callsite_dispatch_without_transformers": "NOT_VERIFIED",
    "galena_stack_settlement": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "static_contract": "NOT_CERTIFIED",
    "mutating_hook": "NOT_VERIFIED",
    "mutation": "NO_MUTATION",
    "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def unique(pairs):
    result = {}
    for key, val in pairs:
        need(key not in result, "duplicate JSON key " + key)
        result[key] = val
    return result

def load(path, limit):
    raw = Path(path).read_bytes()
    need(0 < len(raw) <= limit, "invalid evidence file size")
    return json.loads(raw, object_pairs_hook=unique), raw

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def call_subset(entry, owner, name, descriptor):
    return [c for m in entry["selected_methods"]
            for c in m.get("calls", [])
            if m["name"] == name and
            c["owner"] == owner and c["name"] == descriptor[0] and
            c["descriptor"] == descriptor[1]]

def validate(report, seal, *, raw=None, strict=True):
    need(report["schema"] == seal["schema"] == 1, "schema")
    need(report["scope"] == REPORT_SCOPE and seal["scope"] == SEAL_SCOPE,
         "wrong report/seal scope")
    meta = seal["provenance"]
    need(meta["report_sha256"] == REPORT_SHA and
         meta["report_bytes"] == REPORT_BYTES,
         "source report provenance")
    if strict:
        need(raw is not None and len(raw) == REPORT_BYTES and
             sha(raw) == REPORT_SHA, "report exact SHA/size")
    need(meta["report_run_id"] == 45211836269 and
         meta["report_job_id"] == 137822418958 and
         meta["report_head_sha"] ==
         "d7cfda2d7b79948433216798f7358eb27b4c98f9",
         "observational workflow provenance")
    need(meta["official_neoforge_installer_sha256"] ==
         "68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c"
         and meta["distributed_server_sha256"] == NEO_SERVER_SHA
         and meta["minecraft_srg_sha256"] == MC_SRG_SHA
         and meta["publisher_alexscaves_sha256"] ==
         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
         and meta["mc_version"] == "1.21.1"
         and meta["neo_version"] == "21.1.248"
         and meta["java_major"] == 65, "publisher identifiers")
    art = report["artifact"]
    need(art["neoforge_version"] == "21.1.248" and
         art["minecraft_version"] == "1.21.1"
         and art["neoforge_server_sha256"] == NEO_SERVER_SHA
         and art["minecraft_srg_sha256"] == MC_SRG_SHA
         and art["installer_sha256"] ==
         meta["official_neoforge_installer_sha256"]
         and art["neoforge_server_bytes"] == 5675624
         and art["modlauncher_loaded_bytes"] == "NOT_OBSERVED",
         "distributed engine artifact mismatch")
    need(set(report["classes"]) == set(seal["classes"]) == set(CLASS_NAMES),
         "class roster changed")
    n_methods, n_calls = 0, 0
    for owner, record in report["classes"].items():
        pin = seal["classes"][owner]
        need(record["owner"] == CLASS_NAMES[owner] and
             record["source_archive"] == pin["origin"] and
             record["sha256"] == pin["sha256"] and
             record["java_major"] == 65 and
             record["declared_method_count"] == pin["declared_method_count"]
             and record["not_modlauncher_transformed"] is True,
             "class origin or declaration drift " + owner)
        got_methods = record["selected_methods"]
        expected = pin["methods"]
        need(len(got_methods) == pin["selected_count"] == len(expected),
             "selected method count " + owner)
        need([(m["name"],m["descriptor"]) for m in got_methods] ==
             [(m["name"],m["descriptor"]) for m in expected],
             "method roster or order " + owner)
        for m, exact in zip(got_methods, expected):
            need(m.get("code_sha256","ABSTRACT") == exact["code_sha256"],
                 "code SHA changed " + owner + "." + m["name"])
            if exact["code_sha256"] == "ABSTRACT":
                need(m["abstract_or_native"] is True and
                     m.get("calls",[]) == [], "abstract/native changed")
                continue
            need(isinstance(m["code_size"],int) and
                 0 < m["code_size"] <= 150000 and
                 isinstance(m["instruction_count"],int) and
                 0 < m["instruction_count"] <= 6500,
                 "unbounded code/method metadata")
            shape = m["branch_shape"]
            need(set(shape) == {"conditional","unconditional","switch",
                                "returns","throws"} and
                 all(isinstance(x,int) and 0 <= x <= m["instruction_count"]
                     for x in shape.values()), "bad branch shape")
            calls = m["calls"]
            need(len(calls) == exact["call_count"] ==
                 len(exact["calls"]), "typed callsite count")
            for c, expected_call in zip(calls, exact["calls"]):
                for key in ("offset","opcode","cp_index","owner",
                            "name","descriptor"):
                    need(c[key] == expected_call[key],
                         "forged callsite " + owner + "." + m["name"] + "." + key)
                need(re.fullmatch(r"invoke(?:virtual|interface|static|special)",c["opcode"])
                     and 0 <= c["offset"] <= 150000
                     and 0 < c["cp_index"] < 65536,
                     "invalid callsite shape")
            n_calls += len(calls)
            n_methods += 1
    need(n_calls == 16 and n_methods == 11,
         "exact distributed class/method/callsite coverage")
    require_calls = (
        ("ServerLevel","addFreshEntity",
         "net/minecraft/server/level/ServerLevel","addEntity",2),
        ("ServerLevel","addEntity",
         "net/minecraft/world/level/entity/PersistentEntitySectionManager","addNewEntity",32),
        ("PersistentEntitySectionManager","addNewEntity",
         "net/minecraft/world/level/entity/PersistentEntitySectionManager","addEntity",3),
        ("PersistentEntitySectionManager","addEntity",
         "net/neoforged/neoforge/event/entity/EntityJoinLevelEvent","<init>",25),
        ("PersistentEntitySectionManager","addEntity",
         "net/neoforged/neoforge/event/entity/EntityJoinLevelEvent","isCanceled",36),
        ("PersistentEntitySectionManager","addEntity",
         "net/minecraft/world/level/entity/PersistentEntitySectionManager","addEntityWithoutEvent",47),
    )
    for owner, method, callee, name, offset in require_calls:
        hits = [c for m in report["classes"][owner]["selected_methods"]
                if m["name"] == method for c in m.get("calls",[])
                if c["owner"] == callee and c["name"] == name
                and c["offset"] == offset]
        need(len(hits) == 1, "missing pinned spawn-chain link " + owner + "." + method)
    need(report["limits"] == STATUS and
         seal["states"] == {k:STATUS[k] for k in seal["states"]}
         and set(seal["states"]) == {
             "static_contract","mutating_hook","physical_qa",
             "mutation","provider_universe_closed","semantic_magic_roots_delta"
         }, "unsafe mutation or runtime promotion")
    return n_methods, n_calls

def adversarial(report, seal):
    cases=[]
    def mutate(label, path, value):
        obj=copy.deepcopy(report)
        target=obj
        for part in path[:-1]:
            target=target[part]
        target[path[-1]]=value
        cases.append((label,obj,seal))
    for owner, record in report["classes"].items():
        mutate("forged class hash "+owner,
               ["classes",owner,"sha256"],"0"*64)
        for i,m in enumerate(record["selected_methods"]):
            if "code_sha256" in m:
                mutate("forged method hash "+owner+str(i),
                       ["classes",owner,"selected_methods",i,"code_sha256"],"0"*64)
            for j,c in enumerate(m.get("calls",[])):
                mutate("forged callsite "+owner+str(i)+":"+str(j),
                       ["classes",owner,"selected_methods",i,"calls",j,"owner"],
                       "net/minecraft/fake/Unverified")
    for k,v in (
        ("installed_modpack_parity","VERIFIED"),
        ("modlauncher_transformed_bytecode","VERIFIED"),
        ("real_galena_entity_join_event","VERIFIED"),
        ("callsite_dispatch_without_transformers","VERIFIED"),
        ("galena_stack_settlement","VERIFIED"),
        ("physical_qa","PASSED"),("static_contract","CERTIFIED"),
        ("mutating_hook","VERIFIED"),("mutation","MUTATION"),
        ("provider_universe_closed",True),("semantic_magic_roots_delta",1)):
        mutate("unsafe report status "+k,["limits",k],v)
    mutate("wrong engine",["artifact","neoforge_version"],"21.1.250")
    x=copy.deepcopy(seal)
    x["states"]["mutating_hook"]="VERIFIED"
    cases.append(("forged sealed status",report,x))
    x=copy.deepcopy(seal)
    x["classes"]["ServerLevel"]["sha256"]="0"*64
    cases.append(("forged sealed class hash",report,x))
    for label,r,s in cases:
        try:
            validate(r,s,strict=False)
        except (ValueError, KeyError, TypeError, IndexError):
            continue
        raise AssertionError("unsafe distributed spawn forgery accepted: "+label)
    need(len(cases)>=35, "adversarial coverage")
    return len(cases)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--adversarial",action="store_true")
    a=p.parse_args()
    report,raw=load(a.report,250000)
    seal,_=load(a.manifest,50000)
    methods,calls=validate(report,seal,raw=raw)
    print("EXACT_REPORT_SHA256",sha(raw),"BYTES",len(raw),
          "METHODS",methods,"TYPED_CALLS",calls)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED",adversarial(report,seal))
    print("OK: distributed ABI only; no installed ModLauncher/gameplay proof")

if __name__=="__main__":
    main()
