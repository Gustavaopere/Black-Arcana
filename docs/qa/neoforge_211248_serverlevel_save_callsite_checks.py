#!/usr/bin/env python3
"""Causal SHA-exact audit of NeoForge 21.1.248 ServerLevel.save shutdown chain."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE1="NEOFORGE_211248_SERVERLEVEL_SAVE_CALLSITE_CENSUS_DISTRIBUTED_ONLY"
SCOPE2="NEOFORGE_211248_SAVEALLCHUNKS_CALLSITE_CENSUS_DISTRIBUTED_ONLY"
MINECRAFT="net/minecraft/server/MinecraftServer"
EXACT_TARGETS=(
    {"owner":"net/minecraft/server/level/ServerLevel",
     "name":"save","descriptor":"(Lnet/minecraft/util/ProgressListener;ZZ)V"},
    {"owner":MINECRAFT,"name":"saveAllChunks","descriptor":"(ZZZ)Z"})
GATES={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
       "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
       "provider_universe_closed":False,"semantic_magic_roots_delta":0,
       "shutdown_path_execution":"NOT_TESTED",
       "server_stop_arguments":"NOT_VERIFIED",
       "async_write_completion":"NOT_TESTED","disk_durability":"NOT_TESTED"}

def no_duplicates(pairs):
    result={}
    for key,value in pairs:
        assert key not in result,("duplicate JSON key",key)
        result[key]=value
    return result

def load(path,limit):
    raw=Path(path).read_bytes()
    assert 0 < len(raw) <= limit,"file size exceeds bounded JSON budget"
    return raw,json.loads(raw,object_pairs_hook=no_duplicates)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical_sha(obj):
    return sha((json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode())

def pivot(method,off,opcode,symbol=None,operand=None):
    rows=[x for x in method["instructions"] if x["offset"]==off]
    assert len(rows)==1,("JVM offset missing",method["declaration"]["name"],off)
    row=rows[0]
    assert row["opcode"]==opcode,("JVM opcode drift",method["declaration"]["name"],off,row["opcode"],opcode)
    if symbol is not None:
        assert symbol in row["symbol"],("JVM symbol drift",method["declaration"]["name"],off)
    if operand is not None:
        assert row["operand"]==operand,("JVM operand drift",method["declaration"]["name"],off)
    return row

def method_key(record):
    return (record["report"],record["archive"],record["owner"],
            record["name"],record["descriptor"])

def check(first,second,manifest):
    a_raw,a=load(first,510000)
    b_raw,b=load(second,510000)
    _,seal=load(manifest,16000)
    assert seal["schema_version"]==1
    assert seal["scope"]=="NEOFORGE_211248_SAVE_SHUTDOWN_CHAIN_DISTRIBUTED_STATIC_ONLY"
    assert seal["evidence"]["discovery_run_id"]==45067244452
    assert seal["evidence"]["artifact_id"]==14772170804
    for name,raw in (("serverlevel_save",a_raw),("saveallchunks",b_raw)):
        e=seal["evidence"][name]
        assert (e["bytes"],e["sha256"])==(len(raw),sha(raw)),("report identity drift",name)
    assert a["scope"]==SCOPE1 and b["scope"]==SCOPE2
    assert a["schema_version"]==b["schema_version"]==1
    assert a["target"]==EXACT_TARGETS[0] and b["target"]==EXACT_TARGETS[1]
    assert a["distribution"]==b["distribution"]
    d=a["distribution"]
    assert d["neoforge_version"]==seal["distribution"]["neoforge_version"]=="21.1.248"
    assert d["minecraft_version"]==seal["distribution"]["minecraft_version"]=="1.21.1"
    for field in ("installer_sha256","neoforge_server_sha256","minecraft_srg_sha256"):
        assert d[field]==seal["distribution"][field],("distribution drift",field)
    assert d["modlauncher_loaded_bytes"]=="NOT_OBSERVED"
    assert len(a["archives"])==len(b["archives"])==len(seal["archives"])==3
    assert sum(x["class_entries_scanned"] for x in a["archives"])==9243
    indices=[]
    discovered={}
    for ri,report in enumerate((a,b)):
        for ai,(archive,ref) in enumerate(zip(report["archives"],seal["archives"])):
            assert archive["archive"]==ref["archive"],"archive order drift"
            assert archive["jar_sha256"]==ref["jar_sha256"],"JAR SHA drift"
            assert archive["class_entries_scanned"]==ref["class_entries_scanned"],"class universe drift"
            assert archive["class_roster_sha256"]==ref["class_roster_sha256"],"class roster drift"
            assert archive["jar_bytes"]==[5675624,14246609,3551268][ai],"JAR size drift"
            assert len(archive["typed_candidates"])==[1,1,1 if ri==0 else 0][ai],"candidate roster drift"
            assert len(archive["direct_invoke_sites"])==ref["first_methods" if ri==0 else "second_methods"],"direct method roster drift"
            for item in archive["direct_invoke_sites"]:
                method=item["method"]
                key=("serverlevel_save" if ri==0 else "saveallchunks",
                     ai,item["owner"],method["declaration"]["name"],
                     method["declaration"]["descriptor"])
                assert key not in discovered,"duplicate direct method"
                assert method["instruction_sha256"]==canonical_sha(method["instructions"]),"instruction content hash mismatch"
                assert method["instruction_count"]==len(method["instructions"]),"instruction roster size drift"
                assert item["class_sha256"]==archive["typed_candidates"][0]["class_sha256"]
                assert len(item["callsites"])==1,"unexpected number of direct invocations"
                call=item["callsites"][0]
                assert call["cp_index"] in archive["typed_candidates"][0]["methodref_indices"],"untyped callsite"
                discovered[key]=(item,method,call)
        for key,value in GATES.items():
            assert report[key]==value,("scope-state drift",key)
    assert seal["states"]==GATES
    expected={method_key(m):m for m in seal["methods"]}
    assert len(expected)==len(seal["methods"])==7 and set(discovered)==set(expected),"JVM method/manifest mismatch"
    for key, (item,method,call) in discovered.items():
        exp=expected[key]
        assert item["class_sha256"]==exp["class_sha256"],"owner class SHA drift"
        assert method["declaration"]["code_sha256"]==exp["code_sha256"],"Code SHA drift"
        assert method["instruction_sha256"]==exp["instruction_sha256"],"instruction SHA drift"
        assert method["instruction_count"]==exp["instruction_count"],"instruction count drift"
        assert (call["offset"],call["opcode"],call["cp_index"])==(
            exp["offset"],exp["opcode"],exp["cp_index"]),"callsite drift"
        symbol="ServerLevel.save:" if key[0]=="serverlevel_save" else "saveAllChunks:"
        pivot(method,exp["offset"],exp["opcode"],symbol,"#"+str(exp["cp_index"]))
    # Exact NeoForge 21.1.248 overlay call chain, rather than SRG fallback.
    stop=discovered[("saveallchunks",0,MINECRAFT,"stopServer","()V")][1]
    save=discovered[("serverlevel_save",0,MINECRAFT,"saveAllChunks","(ZZZ)Z")][1]
    everything=discovered[("saveallchunks",0,MINECRAFT,"saveEverything","(ZZZ)Z")][1]
    gen=discovered[("serverlevel_save",2,
        "net/neoforged/neoforge/server/command/generation/GenerationTask",
        "lambda$acceptChunkResult$5","()V")][1]
    # stopServer: clears noSave on resident levels, then calls
    # saveAllChunks(false,true,false) before level close and storageSource close.
    pivot(stop,115,"aload_2")
    pivot(stop,116,"iconst_0")
    pivot(stop,117,"putfield","ServerLevel.noSave:Z")
    pivot(stop,220,"aload_0")
    pivot(stop,221,"iconst_0")
    pivot(stop,222,"iconst_1")
    pivot(stop,223,"iconst_0")
    pivot(stop,224,"invokevirtual","saveAllChunks:")
    pivot(stop,279,"invokevirtual","ServerLevel.close:")
    pivot(stop,317,"invokevirtual","LevelStorageSource$LevelStorageAccess.close:")
    # saveAllChunks carries boolean #2 unchanged to ServerLevel.save
    # and converts (level.noSave && !forceNoSaveOverride) into skip flag.
    pivot(save,63,"aconst_null")
    pivot(save,64,"iload_2")
    pivot(save,67,"getfield","ServerLevel.noSave:Z")
    pivot(save,70,"ifeq",operand="81")
    pivot(save,73,"iload_3")
    pivot(save,74,"ifne",operand="81")
    pivot(save,77,"iconst_1")
    pivot(save,81,"iconst_0")
    pivot(save,82,"invokevirtual","ServerLevel.save:")
    # In the separate saveEverything entry point the three flags are forwarded.
    pivot(everything,13,"iload_1")
    pivot(everything,14,"iload_2")
    pivot(everything,15,"iload_3")
    pivot(everything,16,"invokevirtual","saveAllChunks:")
    # GenerationTask never executes the ServerLevel.save body: third flag true.
    pivot(gen,4,"aconst_null")
    pivot(gen,5,"iconst_0")
    pivot(gen,6,"iconst_1")
    pivot(gen,7,"invokevirtual","ServerLevel.save:")
    print("PASS: two exact SHA reports, 9243 scanned classes, seven method identities")
    print("PASS: static stopServer(false,true,false) → saveAllChunks → ServerLevel.save branch")
    print("PASS: no phys shutdown, disk durability or mutating hook inferred")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--serverlevel-report",required=True,type=Path)
    p.add_argument("--saveallchunks-report",required=True,type=Path)
    p.add_argument("--manifest",required=True,type=Path)
    a=p.parse_args()
    check(a.serverlevel_report,a.saveallchunks_report,a.manifest)
