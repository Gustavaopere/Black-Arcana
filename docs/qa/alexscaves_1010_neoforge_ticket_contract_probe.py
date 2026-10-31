#!/usr/bin/env python3
"""Cross-artifact read-only ticket audit: exact Alex's Caves 1.0.10 + NeoForge 21.1.248.

Extract selected binary/JVM invocation and lifecycle evidence only. No sources
copied, no controller run, no assertion of ticket release or protected-world QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import GumballStateProbeError, name_of, strict_pairs

NEOFORGE_VERSION = "21.1.248"
ROOT = "net/neoforged/neoforge/common/world/chunk/"
NEO_CLASSES = (
    "TicketController.class",
    "ForcedChunkManager.class",
    "ForcedChunkManager$TicketTracker.class",
    "LoadingValidationCallback.class",
    "TicketHelper.class",
    "RegisterTicketControllersEvent.class",
)
EXPECTED_METHOD_NAMES = {
    "TicketController.class": ("forceChunk",),
    "ForcedChunkManager.class": ("forceChunk", "reinstatePersistentChunks"),
    "ForcedChunkManager$TicketTracker.class": ("add", "remove", "getTickets"),
    "TicketHelper.class": ("removeAllTickets",),
    "RegisterTicketControllersEvent.class": (),
    "LoadingValidationCallback.class": (),
}
TICKET_OWNER = "net/neoforged/neoforge/common/world/chunk/TicketController"
FORCED_OWNER = "net/neoforged/neoforge/common/world/chunk/ForcedChunkManager"
MAX_CLASS_METHODS = 160
MAX_METHOD_INSNS = 2300
MAX_CLASS_BYTES = 850000
MAX_SELECTED_PER_CLASS = 24
MAX_ANCHORS_PER_METHOD = 24
MAX_WINDOW_RADIUS = 5
MAX_SNAPSHOT_BYTES = 60000
MAX_JAR_ENTRIES = 25000
CUES = (
    "forceChunk", "getUUID", "TicketController", "validate",
    "callback", "initialis", "register", "removeAll", "reinstate",
    "getEntityTickets", "getBlockTickets", "TicketHelper",
    "addRegionTicket", "removeRegionTicket", "getDataStorage",
    "isDirty", "setDirty", "getForcedChunks", "getChunk",
    "savedData", "writeModForcedChunks", "readModForcedChunks",
    "ENTITY_TICKING", "ENTITY:", "tickingChunks", "chunks:",
    "getEntityForcedChunks", "getBlockForcedChunks",
)

def mhash(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, separators=(",",":"),
                              ensure_ascii=False).encode("utf8")).hexdigest()

def compact(x):
    return {k:x[k] for k in ("offset","opcode","operand","symbol")}

def evidence(m):
    ins=m["instructions"]
    if len(ins)>MAX_METHOD_INSNS:
        raise GumballStateProbeError("NeoForge method budget exceeded")
    if len({x["offset"] for x in ins})!=len(ins):
        raise GumballStateProbeError("NeoForge duplicate JVM offset")
    chosen=[(i,x) for i,x in enumerate(ins)
            if any(t.lower() in x["symbol"].lower() for t in CUES)]
    if len(chosen)>MAX_ANCHORS_PER_METHOD:
        # Capture SHA/counts, but withhold over-budget callsite detail.
        chosen=chosen[:MAX_ANCHORS_PER_METHOD]
        truncated=True
    else:
        truncated=False
    return {
        "name":name_of(m),"descriptor":m["descriptor"],
        "instructions":len(ins),"method_sha256":mhash(m),
        "total_cue_sites":sum(
            any(t.lower() in x["symbol"].lower() for t in CUES) for x in ins),
        "anchors_truncated":truncated,
        "anchors":[{
            "at":x["offset"],"instruction":compact(x),
            "window":[compact(v) for v in ins[max(0,i-MAX_WINDOW_RADIUS):i+MAX_WINDOW_RADIUS+1]]
        } for i,x in chosen],
    }

def audit(neoforge, publisher, javap_bin, previous):
    if sha_file(publisher)!=(SHA1,SHA256,SIZE):
        raise GumballStateProbeError("exact publisher SHA1/SHA256/size drift")
    documented=json.loads(Path(previous).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
    if (documented["artifact"]["sha256"]!=SHA256
            or documented["candidate_class_count"]!=5):
        raise GumballStateProbeError("not the sealed provider lifecycle evidence")
    nfsha1,nfsha256,nfbytes=sha_file(neoforge)
    if not 100000<=nfbytes<=85000000:
        raise GumballStateProbeError("unexpected NeoForge Maven JAR size")
    with zipfile.ZipFile(neoforge) as jar:
        names=jar.namelist()
        if len(names)>MAX_JAR_ENTRIES or len(names)!=len(set(names)):
            raise GumballStateProbeError("NeoForge JAR duplicate/size drift")
        present=[ROOT+x for x in NEO_CLASSES if ROOT+x in names]
        if len(present)<6:
            raise GumballStateProbeError("NeoForge chunk controller classes not present")
        file_hashes={x:hashlib.sha256(jar.read(x)).hexdigest() for x in present}
        for k in present:
            if not 20<=len(jar.read(k))<=MAX_CLASS_BYTES:
                raise GumballStateProbeError("NeoForge class byte budget")
    records=[]
    for path in present:
        methods=parse_methods(javap(javap_bin,neoforge,path[:-6].replace("/",".")))
        if not 1<=len(methods)<=MAX_CLASS_METHODS:
            raise GumballStateProbeError("NeoForge class method count")
        short=path[len(ROOT):]
        roster=[{"name":name_of(m),"descriptor":m["descriptor"],
                 "instructions":len(m["instructions"]),"method_sha256":mhash(m)}
                for m in methods]
        for wanted in EXPECTED_METHOD_NAMES[short]:
            if not any(x["name"]==wanted for x in roster):
                raise GumballStateProbeError("NeoForge expected method missing: "+wanted)
        interesting=[m for m in methods if name_of(m) in
                     ("forceChunk","add","remove","getTickets","reinstatePersistentChunks","register","registerController",
                      "readModForcedChunks","writeModForcedChunks","removeAllTickets",
                      "validateTickets","getEntityTickets","getBlockTickets")
                     or any("TicketController" in x["symbol"] or "forceChunk" in x["symbol"]
                            for x in m["instructions"])]
        if len(interesting)>MAX_SELECTED_PER_CLASS:
            raise GumballStateProbeError("too many selected NeoForge methods")
        records.append({
            "class_path":path,"class_sha256":file_hashes[path],
            "declared_method_count":len(methods),
            "method_roster":roster,
            "selected_methods":[evidence(m) for m in interesting]
        })
    controller=next((x for x in records if x["class_path"].endswith("/TicketController.class")),None)
    if not controller: raise GumballStateProbeError("TicketController absent")
    entitydesc="(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/Entity;IIZZ)Z"
    if not any(m["name"]=="forceChunk" and m["descriptor"]==entitydesc
               for m in controller["selected_methods"]):
        raise GumballStateProbeError("exact NeoForge entity ticket descriptor missing")
    wrapper=next((x for x in documented["candidate_classes"] if
                  x["class_path"].endswith("/ACPlatform.class")),None)
    if not wrapper:
        raise GumballStateProbeError("publisher wrapper absent")
    provider_sites=[anchor for m in wrapper["relevant_methods"] for anchor in m["site_anchors"]
                    if "TicketController.forceChunk" in anchor["symbol"]]
    if len(provider_sites)!=2:
        raise GumballStateProbeError("publisher adapter overloaded forceChunk sites drift")
    return {
        "schema_version":1,
        "scope":"EXACT_PUBLISHER_1010_VERSUS_EXACT_NEOFORGE_21_1_248_TICKETCONTRACT_STATIC",
        "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "neo":{"version":NEOFORGE_VERSION,"file_sha1":nfsha1,
               "file_sha256":nfsha256,"size_bytes":nfbytes},
        "provider_adapter_static_sha256":wrapper["class_sha256"],
        "provider_force_ticket_calls":provider_sites,
        "neoforge_class_count":len(records),
        "neoforge_classes":records,
        "limits":{
            "runtime_ticket_success":"NOT_OBSERVED",
            "controller_registration_and_callback":"NOT_CLOSED",
            "restart_reinstate_validation":"NOT_CLOSED",
            "unload_crash_and_dimension_transition":"NOT_TESTED",
            "integrated_claims_worldeffectpolicy":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "safe_mutating_hook":"NOT_VERIFIED",
            "perk_contract":"NOT_CERTIFIED",
            "allow_mutation":False,
        },
    }

def deep_bytecode(neoforge, javap_bin):
    """Bounded runtime-independent JVM instruction trace, emitted in CI logs only."""
    target_classes = {
        "TicketController.class": {"forceChunk"},
        "ForcedChunkManager.class": {"forceChunk", "reinstatePersistentChunks",
                                      "lambda$reinstatePersistentChunks$6",
                                      "lambda$reinstatePersistentChunks$10"},
        "TicketHelper.class": {"removeAllTickets"},
        "ForcedChunkManager$TicketTracker.class": {"add","remove","getTickets"},
    }
    output={}
    for short,names in target_classes.items():
        cls=ROOT+short
        methods=parse_methods(javap(javap_bin,neoforge,cls[:-6].replace("/",".")))
        selected={}
        for m in methods:
            if name_of(m) not in names or len(m["instructions"])>110: continue
            key=name_of(m)+":"+m["descriptor"]
            if key in selected: raise GumballStateProbeError("duplicate deep NeoForge method")
            selected[key]=m["instructions"]
        if not selected:
            raise GumballStateProbeError("deep NeoForge selected methods absent")
        output[cls]=selected
    if len(json.dumps(output).encode("utf8"))>80000:
        raise GumballStateProbeError("deep static evidence budget")
    return output

def seal(doc):
    # The method roster and anchored, size-bounded callsite facts are sufficient
    # to detect drift without committing the publisher's full implementation.
    out=dict(doc)
    out["neoforge_classes"]=[]
    for r in doc["neoforge_classes"]:
        out["neoforge_classes"].append({
            **{k:r[k] for k in ("class_path","class_sha256","declared_method_count",
                                "method_roster")},
            "selected_methods":[{
                **{k:m[k] for k in ("name","descriptor","instructions","method_sha256",
                                    "total_cue_sites","anchors_truncated")},
                "site_anchors":[a["instruction"] for a in m["anchors"]]
            } for m in r["selected_methods"]]
        })
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--neoforge",required=True)
    p.add_argument("--publisher",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--previous",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    a=p.parse_args()
    doc=audit(Path(a.neoforge),Path(a.publisher),a.javap,a.previous)
    sealed=seal(doc)
    if a.snapshot:
        expected=json.loads(Path(a.snapshot).read_text(encoding="utf8"),
                            object_pairs_hook=strict_pairs)
        if expected!=sealed:
            raise GumballStateProbeError("NeoForge 21.1.248 ticket snapshot drift")
    raw=json.dumps(doc,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    if len(raw.encode("utf8"))>MAX_SNAPSHOT_BYTES*5:
        raise GumballStateProbeError("Neoforge ticket evidence too large")
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(doc,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("NEOFORGE_TICKETS_211248_BEGIN")
    print(json.dumps(sealed,sort_keys=True,separators=(",",":"),ensure_ascii=False))
    print("NEOFORGE_TICKETS_211248_END")
    print("NEOFORGE_TICKET_WINDOWS_BEGIN")
    print(raw)
    print("NEOFORGE_TICKET_WINDOWS_END")
    print("NEOFORGE_TICKET_DEEP_BEGIN")
    print(json.dumps(deep_bytecode(Path(a.neoforge),a.javap),sort_keys=True,separators=(",",":"),ensure_ascii=False))
    print("NEOFORGE_TICKET_DEEP_END")
    print("NO_RUNTIME_CLEANUP_OR_PROTECTION_CERTIFICATION")

if __name__=="__main__":
    main()
