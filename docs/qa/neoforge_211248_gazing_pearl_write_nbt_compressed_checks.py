#!/usr/bin/env python3
"""Fail-closed exact NeoForge 21.1.248 IOUtilities atomic-write JVM contract.

Positive: pinned official JAR report + typed bootstrap + semantic file-operation
offsets. Negative tests recompute all external and instruction hashes but must
still fail on independent JVM bytecode/CFG pivots.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE="NEOFORGE_211248_IOUTILITIES_WRITE_NBT_COMPRESSED_DISTRIBUTED_ONLY"
JAR="90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
CLASS="3c4cfda19b620562486ca18af3d7c095c94a54c31d1028bf8e5d9860952e115a"


def pair_unique(pairs):
    out={}
    for key,value in pairs:
        assert key not in out, ("duplicate JSON member",key)
        out[key]=value
    return out


def loaded(path,limit):
    raw=Path(path).read_bytes()
    assert 0<len(raw)<=limit, ("evidence size budget",path)
    return raw,json.loads(raw,object_pairs_hook=pair_unique)


def sha_canonical(value):
    payload=(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf8")
    return hashlib.sha256(payload).hexdigest()


def selected(report,name):
    matches=[m for m in report["selected_methods"] if m["declaration"]["name"]==name]
    assert len(matches)==1, ("ambiguous method",name)
    return matches[0]


def pivot(report,name,offset,opcode,symbol="",operand=None):
    m=selected(report,name)
    matches=[x for x in m["instructions"] if x["offset"]==offset]
    assert len(matches)==1, ("missing bytecode pivot",name,offset)
    instruction=matches[0]
    assert instruction["opcode"]==opcode, ("JVM opcode drift",name,offset)
    assert symbol in instruction["symbol"],("JVM semantic target drift",name,offset)
    if operand is not None:
        assert instruction["operand"]==operand,("JVM operand/branch drift",name,offset)
    return instruction


def check(report_path,manifest_path):
    raw,r=loaded(report_path,190_000)
    _,seal=loaded(manifest_path,18_000)
    assert r["schema_version"]==seal["schema_version"]==1
    assert r["scope"]==seal["scope"]==SCOPE
    assert seal["evidence"]["run_id"]==45047273632
    assert seal["evidence"]["artifact_id"]==14764335789
    assert seal["evidence"]["report_bytes"]==len(raw)
    assert seal["evidence"]["report_sha256"]==hashlib.sha256(raw).hexdigest()
    assert r["artifact"]==seal["engine"]
    assert r["artifact"]["neoforge_version"]=="21.1.248"
    assert r["artifact"]["modlauncher_loaded_bytes"]=="NOT_OBSERVED"
    assert r["universal_library"]==seal["library"]
    assert r["universal_library"]["sha256"]==JAR
    assert r["universal_library"]["worker_class_sha256"]==CLASS
    assert r["owner"]==seal["owner"]=="net/neoforged/neoforge/common/IOUtilities"
    assert r["owner_major"]==65
    assert r["write_callback"]["owner"]==seal["write_callback"]["owner"]
    assert r["write_callback"]["class_sha256"]==seal["write_callback"]["class_sha256"]
    assert r["write_callback"]["access"]==seal["write_callback"]["access"]==1537
    assert len(r["write_callback"]["methods"])==1
    callback=r["write_callback"]["methods"][0]
    assert (callback["name"],callback["descriptor"],callback["access"])==(
        seal["write_callback"]["method_name"],
        seal["write_callback"]["method_desc"],
        seal["write_callback"]["method_access"])
    assert "code_sha256" not in callback
    assert len(r["method_roster"])==len(r["selected_methods"])==len(seal["methods"])==14
    assert sha_canonical(r["method_roster"])==seal["method_roster_sha256"]
    assert not r["non_executable_declarations"]
    for name, record in seal["methods"].items():
        m=selected(r,name)
        assert m["declaration"]["code_sha256"]==record["code_sha256"]
        assert m["instruction_sha256"]==record["instruction_sha256"]
        assert sha_canonical(m["instructions"])==record["instruction_sha256"]
        assert m["instruction_count"]==record["instruction_count"]==len(m["instructions"])
        offsets=[i["offset"] for i in m["instructions"]]
        assert offsets==sorted(set(offsets)),("JVM ordering/duplicate",name)
    assert set(x["declaration"]["name"] for x in r["selected_methods"])==set(seal["methods"])
    assert r["modlauncher_class"]==seal["limits"]["loaded_modlauncher"]=="NOT_OBSERVED"
    assert r["installed_modpack_parity"]==seal["limits"]["modpack_exact_binary"]=="NOT_VERIFIED"
    assert r["actual_file_io"]==seal["limits"]["physical_save_and_reload"]=="NOT_TESTED"
    assert r["actual_error_recovery"]=="NOT_TESTED"
    assert r["durability_after_restart"]==seal["limits"]["crash_durability"]=="NOT_TESTED"
    for key in ("NbtIo_writeCompressed_implementation","filesystem_provider_atomic_move",
                "shutdown_wait_callsite","reputation_sync"):
        assert seal["limits"][key] in ("NOT_AUDITED","NOT_TESTED","NOT_VERIFIED")
    for key, value in seal["states"].items():
        assert r[key]==value
    assert seal["states"]=={
        "static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
        "provider_universe_closed":False,"semantic_magic_roots_delta":0}

    # Real constant-pool -> BootstrapMethods -> LambdaMetafactory -> WriteCallback
    for caller,cp,bs_index,lamb in (
        ("writeNbtCompressed",88,1,"lambda$writeNbtCompressed$1"),
        ("writeNbt",96,2,"lambda$writeNbt$2")
    ):
        call=r["bootstrap_links"][caller]
        exp=seal["bootstrap"][caller]
        assert call["offset"]==2
        assert call["cp_index"]==exp["cp_index"]==cp
        assert call["bootstrap_index"]==exp["bootstrap_index"]==bs_index
        assert call["bootstrap_table_count"]==exp["bootstrap_table_count"]==3
        assert call["bootstrap_table_sha256"]==exp["bootstrap_table_sha256"]
        assert call["operand"]=="#%d, 0"%cp
        entry=call["entry"]
        assert entry["handle"]["reference_kind"]==6
        assert entry["handle"]["reference"][1]=="java/lang/invoke/LambdaMetafactory"
        assert entry["handle"]["reference"][2][1]=="metafactory"
        assert len(entry["arguments"])==3
        link=call["linked_local"]
        assert link["name"]==exp["lambda"]==lamb
        assert link["handle"]["reference_kind"]==exp["reference_kind"]==6
        assert link["handle"]["reference"][1]==r["owner"]
        assert link["handle"]["reference"][2][1]==lamb
        assert entry["arguments"][1]==link["handle"]
        assert selected(r,lamb)["declaration"]["code_sha256"]==link["code_sha256"]

    pivots=(
        ("writeNbtCompressed",2,"invokedynamic","InvokeDynamic #1:write:","#88, 0"),
        ("writeNbtCompressed",7,"invokestatic","atomicWrite:",None),
        ("lambda$writeNbtCompressed$1",11,"invokestatic","NbtIo.writeCompressed:",None),
        ("lambda$writeNbtCompressed$1",15,"invokevirtual","BufferedOutputStream.close:",None),
        ("atomicWrite",1,"invokeinterface","Path.getParent:",None),
        ("atomicWrite",17,"ldc",".neoforge-tmp",None),
        ("atomicWrite",23,"invokestatic","Files.createTempFile:",None),
        ("atomicWrite",31,"invokestatic","FileChannel.open:",None),
        ("atomicWrite",39,"invokestatic","CloseShieldOutputStream.wrap:",None),
        ("atomicWrite",47,"invokeinterface","IOUtilities$WriteCallback.write:",None),
        ("atomicWrite",53,"iconst_1","",None),
        ("atomicWrite",54,"invokevirtual","FileChannel.force:",None),
        ("atomicWrite",101,"getstatic","StandardCopyOption.ATOMIC_MOVE:",None),
        ("atomicWrite",105,"invokestatic","Files.move:",None),
        ("atomicWrite",121,"getstatic","StandardCopyOption.REPLACE_EXISTING:",None),
        ("atomicWrite",125,"invokestatic","Files.move:",None),
        ("atomicWrite",134,"invokestatic","Files.deleteIfExists:",None),
        ("atomicWrite",150,"athrow","",None),
        ("<clinit>",6,"getstatic","StandardOpenOption.WRITE:",None),
        ("<clinit>",12,"getstatic","StandardOpenOption.TRUNCATE_EXISTING:",None),
        ("waitUntilIOWorkerComplete",3,"invokevirtual","CompletableFuture.join:",None),
        ("waitUntilIOWorkerComplete",8,"invokestatic","CompletableFuture.completedFuture:",None),
        ("waitUntilIOWorkerComplete",11,"putstatic","saveDataTasks:",None),
        ("withIOWorker",7,"invokevirtual","CompletableFuture.thenRunAsync:",None)
    )
    for name,off,op,sym,operand in pivots:
        pivot(r,name,off,op,sym,operand)
    handlers=selected(r,"atomicWrite")["declaration"]["exception_handlers"]
    assert handlers==seal["atomic_handlers"]==[
        {"start":35,"end":57,"target":68,"catch":"java/lang/Throwable"},
        {"start":74,"end":78,"target":81,"catch":"java/lang/Throwable"},
        {"start":93,"end":109,"target":112,
         "catch":"java/nio/file/AtomicMoveNotSupportedException"},
        {"start":27,"end":129,"target":132,"catch":"java/lang/Exception"},
        {"start":133,"end":138,"target":141,"catch":"java/lang/Exception"}
    ]
    assert selected(r,"writeNbtCompressed")["declaration"]["exception_handlers"]==[]
    print("PASS: exact NeoForge 21.1.248 writeNbtCompressed → atomicWrite + move fallback")
    print("REPORT_SHA256",hashlib.sha256(raw).hexdigest())
    print("NOT_MODLAUNCHER NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    a=p.parse_args()
    check(a.report,a.manifest)
