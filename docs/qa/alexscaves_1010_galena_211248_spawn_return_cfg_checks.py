#!/usr/bin/env python3
"""SHA-exact fail-closed Galena 21.1.248 distributed spawn return-CFG checks.

First revalidates the established 53-workflow distributed-spawn ABI contract,
then pins the added branch edges, return literals and typed control flow.
No ModLauncher/installed runtime, side effects, rollback or hooks are certified.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

from alexscaves_1010_galena_211248_distributed_spawn_checks import validate as validate_parent

REPORT_SHA = "19ce72117b30cbb716cd385638ebbcdf40b8ea68690a0c4a07aa9b53b8bad579"
REPORT_BYTES = 18311
SCOPE_REPORT = "GALENA_NEOFORGE_211248_DISTRIBUTED_SPAWN_RETURN_CFG_DISCOVERY_ONLY"
SCOPE_SEAL = "GALENA_NEOFORGE_211248_DISTRIBUTED_SPAWN_RETURN_CFG_STATIC_SEAL_ONLY"
SCOPE_PARENT = "GALENA_NEOFORGE_211248_DISTRIBUTED_ENTITY_ADMISSION_ABI_DISCOVERY_ONLY"
EXPECTED_METHODS = {
    ("ServerLevel", "addFreshEntity"),
    ("ServerLevel", "addEntity"),
    ("PersistentEntitySectionManager", "addNewEntity"),
    ("PersistentEntitySectionManager", "addEntity"),
    ("PersistentEntitySectionManager", "addEntityWithoutEvent"),
}
SAFE_STATES = {
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
    "provider_universe_closed": False, "semantic_magic_roots_delta": 0,
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def uniq(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, "duplicate JSON key: " + k)
        d[k] = v
    return d


def load(path: Path, limit=100_000):
    raw = path.read_bytes()
    need(0 < len(raw) < limit, "missing or excessive evidence")
    return json.loads(raw, object_pairs_hook=uniq), raw


def method(report, owner, name):
    selected = [m for m in report["classes"][owner]["selected_methods"]
                if m["name"] == name]
    need(len(selected) == 1 and "cfg" in selected[0],
         "missing exact CFG method " + owner + "." + name)
    return selected[0]


def outgoing(methodrow, name, offset):
    calls = [c for c in methodrow["calls"] if c["name"] == name
             and c["offset"] == offset]
    need(len(calls) == 1, "missing typed invoked method " + name + "@" + str(offset))
    return calls[0]


def pivot(report):
    server_add = method(report, "ServerLevel", "addEntity")
    server_fresh = method(report, "ServerLevel", "addFreshEntity")
    man_add = method(report, "PersistentEntitySectionManager", "addEntity")
    man_new = method(report, "PersistentEntitySectionManager", "addNewEntity")
    man_bypass = method(report, "PersistentEntitySectionManager", "addEntityWithoutEvent")

    outgoing(server_fresh, "addEntity", 2)
    need(server_fresh["cfg"]["terminal_sites"] == [
         {"offset":5, "opcode":"ireturn", "previous_opcode":"invokevirtual"}],
         "ServerLevel fresh-entity boolean is not forwarded directly")
    outgoing(man_new, "addEntity", 3)
    need(man_new["cfg"]["terminal_sites"] == [
         {"offset":6, "opcode":"ireturn", "previous_opcode":"invokevirtual"}],
         "manager new-entity boolean is not forwarded directly")

    outgoing(server_add, "addNewEntity", 32)
    outgoing(server_add, "onAddedToLevel", 39)
    need(any(b["offset"] == 35 and b["opcode"] == "ifeq"
             and b["target"] == 44 and b["fallthrough"] == 38
             for b in server_add["cfg"]["branches"]),
         "server does not branch after admission")
    need(server_add["cfg"]["terminal_sites"] == [
        {"offset":26, "opcode":"ireturn", "previous_opcode":"iconst_0"},
        {"offset":43, "opcode":"ireturn", "previous_opcode":"iconst_1"},
        {"offset":45, "opcode":"ireturn", "previous_opcode":"iconst_0"}],
         "server success/fail terminal paths changed")

    outgoing(man_add, "isCanceled", 36)
    outgoing(man_add, "addEntityWithoutEvent", 47)
    need(any(b["offset"] == 39 and b["opcode"] == "ifeq"
             and b["target"] == 44 and b["fallthrough"] == 42
             for b in man_add["cfg"]["branches"]),
         "join cancellation conditional changed")
    need(man_add["cfg"]["terminal_sites"] == [
        {"offset":43, "opcode":"ireturn", "previous_opcode":"iconst_0"},
        {"offset":50, "opcode":"ireturn", "previous_opcode":"invokevirtual"}],
         "join cancellation false-return changed")
    need(man_bypass["cfg"]["terminal_sites"] == [
        {"offset":9, "opcode":"ireturn", "previous_opcode":"iconst_0"},
        {"offset":106, "opcode":"ireturn", "previous_opcode":"iconst_1"}],
         "non-event registration terminal paths changed")


def validate(report, seal, parent, *, raw=None, strict=True):
    need(report["schema"] == seal["schema"] == 1 and
         report["scope"] == SCOPE_REPORT and seal["scope"] == SCOPE_SEAL,
         "scope/schema drift")
    p = seal["provenance"]
    need(p["report_sha256"] == REPORT_SHA and p["report_bytes"] == REPORT_BYTES,
         "canonical source hash pin drift")
    if strict:
        need(raw is not None and len(raw) == REPORT_BYTES and sha(raw) == REPORT_SHA,
             "exact report bytes/hash changed")

    need(p["discovery_run"] == 45223070726 and
         p["discovery_job"] == 137862201325 and
         p["source_head"] == "e7ae329b24a748649242c1a6909461349b58251c" and
         p["neoforge_version"] == "21.1.248" and
         p["minecraft_version"] == "1.21.1" and
         p["installer_sha256"] ==
         "68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c" and
         p["server_overlay_sha256"] ==
         "1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359" and
         p["minecraft_srg_sha256"] ==
         "26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71" and
         p["provider_jar_sha256"] ==
         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c" and
         p["prior_distributed_seal"] ==
         "EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.json",
         "upstream report provenance")

    # The parent SHA-exact manifest confirms the identities and all sixteen
    # typed callsites; bypass *only* its original raw-report hash because this
    # new report adds separately pinned CFG summaries.
    stripped = copy.deepcopy(report)
    stripped["scope"] = SCOPE_PARENT
    for entry in stripped["classes"].values():
        for row in entry["selected_methods"]:
            row.pop("cfg", None)
            row.pop("exception_handler_count", None)
    validate_parent(stripped, parent, strict=False)

    anchors = seal["exact_methods"]
    need(len(anchors) == 5 and
         {(x["owner"], x["name"]) for x in anchors} == EXPECTED_METHODS,
         "missing or duplicate CFG anchor owners")
    total_branches = total_terminals = 0
    for pin in anchors:
        owner, name = pin["owner"], pin["name"]
        m = method(report, owner, name)
        c = m["cfg"]
        need((m["descriptor"], m["code_sha256"], m["code_size"]) ==
             (pin["descriptor"], pin["code_sha256"], pin["code_bytes"]),
             "executable method fingerprint changed " + owner + "." + name)
        need(m["exception_handler_count"] == pin["exception_handler_count"] == 0 and
             c["exception_edges_modeled"] is pin["exception_edges_modeled"] is False,
             "unexpected exception handlers/unsupported exceptional CFG")
        need((c["instruction_count"], c["edges"], c["reachable_count"],
              c["unreachable_count"], c["edge_roster_sha256"]) ==
             (pin["instructions"], pin["edges"], pin["reachable"],
              pin["unreachable"], pin["edge_sha256"]),
             "normal-flow graph identity changed " + owner + "." + name)
        expected_branches = [
            {k:b[k] for k in ("offset","opcode","target","fallthrough")}
            for b in pin["branches"]]
        expected_terminals = [
            {k:t[k] for k in ("offset","opcode","previous_opcode")}
            for t in pin["terminals"]]
        need(c["branches"] == expected_branches and
             c["terminal_sites"] == expected_terminals,
             "JVM branch/terminal pivot drift " + owner + "." + name)
        need(c["reachable_count"] == c["instruction_count"] and
             c["unreachable_count"] == 0 and
             all(t["opcode"] == "ireturn" for t in c["terminal_sites"]),
             "unmodeled/unsupported return branch")
        total_branches += len(c["branches"])
        total_terminals += len(c["terminal_sites"])
    need((total_branches, total_terminals) == (8, 9),
         "branch or exit count drift")
    need(seal["states"] == SAFE_STATES and
         seal["limits"] == {
             "modlauncher_transformed_classes":"NOT_OBSERVED",
             "executed_galena_cancel":"NOT_VERIFIED",
             "return_handling_in_galena":"BOOLEAN_DISCARDED_IN_PUBLISHER_JAR",
             "inventory_rollback":"NOT_VERIFIED",
             "server_protection":"NOT_VERIFIED",
             "exception_flow":"NOT_MODELED",
             "full_provider_universe":"NOT_PROVEN",
             "any_mutating_hook":"NO_MUTATION",
         }, "unsafe status promotion")
    need(report["limits"]["mutation"] == "NO_MUTATION" and
         report["limits"]["static_contract"] == "NOT_CERTIFIED" and
         report["limits"]["physical_qa"] == "NOT_TESTED",
         "unsafe report status")
    pivot(report)
    return (len(anchors), total_branches, total_terminals)


def adversarial(report, seal, parent):
    cases = []
    def alter(label, path, value):
        c=copy.deepcopy(report)
        obj=c
        for part in path[:-1]:
            obj=obj[part]
        obj[path[-1]]=value
        cases.append((label,c,seal))
    for owner,name in EXPECTED_METHODS:
        c=method(report,owner,name)
        base=next(i for i,m in enumerate(report["classes"][owner]["selected_methods"])
                  if m["name"] == name)
        path=["classes",owner,"selected_methods",base]
        alter("method Code forged "+owner+name,path+["code_sha256"],"0"*64)
        alter("CFG edges forged "+owner+name,path+["cfg","edge_roster_sha256"],"0"*64)
        alter("physical exception handler "+owner+name,path+["exception_handler_count"],1)
        for i,b in enumerate(c["cfg"]["branches"]):
            alter("branch destination forged "+owner+name+str(i),
                  path+["cfg","branches",i,"target"],b["target"]+1)
        for i,t in enumerate(c["cfg"]["terminal_sites"]):
            alter("terminal opcode forged "+owner+name+str(i),
                  path+["cfg","terminal_sites",i,"previous_opcode"],"nop")
    for key,new in (
        ("installed_modpack_parity","VERIFIED"),
        ("modlauncher_transformed_bytecode","VERIFIED"),
        ("real_galena_entity_join_event","VERIFIED"),
        ("callsite_dispatch_without_transformers","VERIFIED"),
        ("galena_stack_settlement","VERIFIED"),
        ("physical_qa","PASSED"),
        ("static_contract","CERTIFIED"),
        ("mutating_hook","VERIFIED"),
        ("mutation","MUTATION"),
        ("provider_universe_closed",True),
        ("semantic_magic_roots_delta",1),
    ):
        alter("unsupported state "+key,["limits",key],new)
    s=copy.deepcopy(seal)
    s["states"]["mutating_hook"]="VERIFIED"
    cases.append(("sealed hook fabrication",report,s))
    s=copy.deepcopy(seal)
    s["exact_methods"][0]["edge_sha256"]="0"*64
    cases.append(("sealed graph fabrication",report,s))
    rejected=0
    for label,c,sc in cases:
        try:
            validate(c,sc,parent,strict=False)
        except (ValueError,KeyError,TypeError,IndexError):
            rejected+=1
        else:
            raise AssertionError("forged CFG accepted: "+label)
    need(rejected == len(cases) and rejected >= 35,
         "insufficient adversarial coverage")
    return rejected


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--parent",type=Path,required=True)
    p.add_argument("--adversarial",action="store_true")
    a=p.parse_args()
    report,raw=load(a.report,250_000)
    seal,_=load(a.manifest,100_000)
    parent,_=load(a.parent,100_000)
    n,b,t=validate(report,seal,parent,raw=raw)
    print("RETURN_CFG_REPORT_SHA256",sha(raw),"BYTES",len(raw),
          "METHODS",n,"BRANCHES",b,"TERMINALS",t)
    if a.adversarial:
        print("ADVERSARIAL_REJECTED",adversarial(report,seal,parent))
    print("OK: SHA-exact distributed JVM return graph; NO_MUTATION NOT_CERTIFIED")


if __name__=="__main__":
    main()
