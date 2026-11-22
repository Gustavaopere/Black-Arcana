#!/usr/bin/env python3
"""SHA-exact, fail-closed NeoForge 21.1.248 NbtIo compressed JVM checks.

All source provenance is pinned to the official --installServer distribution.
The positive check does not establish live NBT fidelity, disk durability or
the transformed ModLauncher runtime. Forged reports must fail on JVM pivots,
not on incidental report formatting or length differences.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE="NEOFORGE_211248_NBTIO_COMPRESSED_WRITE_DISTRIBUTED_ONLY"
CLASSES={
    "nbtio":("net/minecraft/nbt/NbtIo",
             "6c124951f395280964900afe4c0c2a550d4808901c3362519806202fd48024d0"),
    "fallback":("net/minecraft/nbt/NbtIo$StringFallbackDataOutput",
                "0dd70203d2a454f6cf95ab854640062e39d0372cdf2665c734aa16b4fd7847ba"),
}
STATE={
    "static_contract":"NOT_CERTIFIED",
    "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "provider_universe_closed":False,
    "semantic_magic_roots_delta":0,
}
DISTRIBUTION={
    "minecraft_version":"1.21.1",
    "neoforge_version":"21.1.248",
    "installer_sha256":"68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c",
    "neoforge_server_sha256":"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",
    "neoforge_server_bytes":5675624,
    "minecraft_srg_sha256":"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",
    "minecraft_srg_bytes":14246609,
    "modlauncher_loaded_bytes":"NOT_OBSERVED",
}
WRITE_STREAM="(Lnet/minecraft/nbt/CompoundTag;Ljava/io/OutputStream;)V"
WRITE_DATA="(Lnet/minecraft/nbt/CompoundTag;Ljava/io/DataOutput;)V"
WRITE_PATH="(Lnet/minecraft/nbt/CompoundTag;Ljava/nio/file/Path;)V"
WRITE_TAG="(Lnet/minecraft/nbt/Tag;Ljava/io/DataOutput;)V"


def unique_object(pairs):
    res={}
    for key,val in pairs:
        assert key not in res,("duplicate JSON property",key)
        res[key]=val
    return res


def loaded(path,max_bytes):
    raw=Path(path).read_bytes()
    assert 0<len(raw)<=max_bytes,"unbounded source report/manifest"
    return raw,json.loads(raw,object_pairs_hook=unique_object)


def canonical_sha(obj):
    content=(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode("utf8")
    return hashlib.sha256(content).hexdigest()


def method(row,name,descriptor=None):
    matches=[m for m in row["selected_methods"]
             if m["declaration"]["name"]==name and
             (descriptor is None or m["declaration"]["descriptor"]==descriptor)]
    assert len(matches)==1,("JVM method signature ambiguous",row["owner"],name,descriptor)
    return matches[0]


def pivot(row,name,descriptor,offset,op,symbol="",operand=None):
    item=method(row,name,descriptor)
    matches=[i for i in item["instructions"] if i["offset"]==offset]
    assert len(matches)==1,("JVM offset missing",row["owner"],name,offset)
    instruction=matches[0]
    assert instruction["opcode"]==op,("JVM opcode drift",row["owner"],name,offset)
    assert symbol in instruction["symbol"],("JVM method/call target drift",row["owner"],name,offset)
    if operand is not None:
        assert instruction["operand"]==operand,("JVM operand drift",row["owner"],name,offset)
    return instruction


def check(report_path,seal_path):
    raw,r=loaded(report_path,250_000)
    _,seal=loaded(seal_path,22_000)
    assert r["schema_version"]==seal["schema_version"]==1
    assert r["scope"]==seal["scope"]==SCOPE
    assert seal["evidence"]["run_id"]==45055281886
    assert seal["evidence"]["artifact_id"]==14767252409
    assert len(raw)==seal["evidence"]["report_bytes"]
    assert hashlib.sha256(raw).hexdigest()==seal["evidence"]["report_sha256"]
    assert r["distribution"]==seal["distribution"]==DISTRIBUTION
    assert r["modlauncher_loaded"]==seal["limits"]["loaded_modlauncher"]=="NOT_OBSERVED"
    assert r["physical_installed_modpack_parity"]==seal["limits"]["physical_installed_modpack_parity"]=="NOT_VERIFIED"
    assert r["filesystem_write_or_restart"]==seal["limits"]["filesystem_write_or_restart"]=="NOT_TESTED"
    assert r["actual_nbt_reload"]==seal["limits"]["actual_nbt_reload"]=="NOT_TESTED"
    assert r["shutdown_wait_callsite"]==seal["limits"]["shutdown_wait_callsite"]=="NOT_VERIFIED"
    assert seal["limits"]["compoundtag_write_virtual_dispatch"]=="NOT_AUDITED"
    assert seal["limits"]["fallback_utf_exception_observed_in_real_save"]=="NOT_TESTED"
    assert r["physical_qa"]=="NOT_TESTED"
    for k,v in STATE.items():
        assert r[k]==seal["states"][k]==v
    assert set(seal["states"])==set(STATE)
    assert r["scope_limit"]=="exact official 21.1.248 distributed JVM only"
    assert r["publisher_callsite"]==(
        "SavedData.lambda$save$0 → IOUtilities.writeNbtCompressed → "
        "IOUtilities.lambda$writeNbtCompressed$1 → "
        "NbtIo.writeCompressed(CompoundTag,OutputStream)")

    outer=r["class"]
    fallback=r["string_fallback"]
    for label,row in (("nbtio",outer),("fallback",fallback)):
        exp=seal["classes"][label]
        owner,sha=CLASSES[label]
        assert row["owner"]==exp["owner"]==owner
        assert row["class_sha256"]==exp["class_sha256"]==sha
        assert row["source_archive"]==exp["source_archive"]=="NEOFORGE_OVERLAY"
        assert row["class_major"]==exp["class_major"]==65
        assert row["declared_method_count"]==exp["declared_method_count"]
        assert len(row["selected_methods"])==len(exp["methods"])
        assert row["non_executable_declarations"]==[]
        names=[(m["declaration"]["name"],m["declaration"]["descriptor"])
               for m in row["selected_methods"]]
        assert names==[(m["name"],m["descriptor"]) for m in exp["methods"]]
        for m,want in zip(row["selected_methods"],exp["methods"]):
            decl=m["declaration"]
            assert decl["code_sha256"]==want["code_sha256"]
            assert m["instruction_count"]==want["instruction_count"]==len(m["instructions"])
            assert m["instruction_sha256"]==want["instruction_sha256"]
            assert canonical_sha(m["instructions"])==want["instruction_sha256"]
            offs=[i["offset"] for i in m["instructions"]]
            assert offs==sorted(set(offs)),("JVM offsets not unique/ordered",want["name"])
    assert outer["declared_method_count"]==22
    assert canonical_sha(outer["declared_methods"])==seal["classes"]["nbtio"]["roster_sha256"]
    assert outer["field_names"]==seal["classes"]["nbtio"]["fields"]==["SYNC_OUTPUT_OPTIONS"]
    assert fallback["parent"]==seal["classes"]["fallback"]["parent"]=="net/minecraft/util/DelegateDataOutput"
    assert fallback["fields"]==seal["classes"]["fallback"]["fields"]==[]

    # Compressed OutputStream path used by the verified IOUtilities lambda.
    for row,name,desc,off,opcode,sym,operand in (
        (outer,"createCompressorStream",None,8,"new","java/util/zip/GZIPOutputStream",None),
        (outer,"createCompressorStream",None,13,"invokespecial",'GZIPOutputStream."<init>":',None),
        (outer,"createCompressorStream",None,16,"invokespecial",'BufferedOutputStream."<init>":',None),
        (outer,"createCompressorStream",None,19,"invokespecial",'DataOutputStream."<init>":',None),
        (outer,"writeCompressed",WRITE_STREAM,1,"invokestatic","createCompressorStream:",None),
        (outer,"writeCompressed",WRITE_STREAM,7,"invokestatic","write:(Lnet/minecraft/nbt/CompoundTag;Ljava/io/DataOutput;)V",None),
        (outer,"writeCompressed",WRITE_STREAM,15,"invokevirtual","DataOutputStream.close:",None),
        (outer,"write",WRITE_DATA,2,"invokestatic","writeUnnamedTagWithFallback:",None),
        (outer,"writeUnnamedTagWithFallback",None,1,"new","NbtIo$StringFallbackDataOutput",None),
        (outer,"writeUnnamedTagWithFallback",None,6,"invokespecial",'StringFallbackDataOutput."<init>":',None),
        (outer,"writeUnnamedTagWithFallback",None,9,"invokestatic","writeUnnamedTag:",None),
        (outer,"writeUnnamedTag",WRITE_TAG,2,"invokeinterface","Tag.getId:",None),
        (outer,"writeUnnamedTag",WRITE_TAG,7,"invokeinterface","DataOutput.writeByte:",None),
        (outer,"writeUnnamedTag",WRITE_TAG,18,"ifeq","","36"),
        (outer,"writeUnnamedTag",WRITE_TAG,24,"invokeinterface","DataOutput.writeUTF:",None),
        (outer,"writeUnnamedTag",WRITE_TAG,31,"invokeinterface","Tag.write:",None),
        (fallback,"<init>",None,2,"invokespecial",'DelegateDataOutput."<init>":',None),
        (fallback,"writeUTF","(Ljava/lang/String;)V",2,"invokespecial","DelegateDataOutput.writeUTF:",None),
        (fallback,"writeUTF","(Ljava/lang/String;)V",12,"invokestatic","Util.logAndPauseIfInIde:",None),
        (fallback,"writeUTF","(Ljava/lang/String;)V",16,"ldc","String","#21"),
        (fallback,"writeUTF","(Ljava/lang/String;)V",18,"invokespecial","DelegateDataOutput.writeUTF:",None),
    ):
        pivot(row,name,desc,off,opcode,sym,operand)
    expected_compressed_handlers=[
        {"start":5,"end":10,"target":21,"catch":"java/lang/Throwable"},
        {"start":26,"end":30,"target":33,"catch":"java/lang/Throwable"},
    ]
    assert method(outer,"writeCompressed",WRITE_STREAM)["declaration"]["exception_handlers"]==expected_compressed_handlers
    expected_fallback_handlers=[{"start":0,"end":5,"target":8,"catch":"java/io/UTFDataFormatException"}]
    assert method(fallback,"writeUTF","(Ljava/lang/String;)V")["declaration"]["exception_handlers"]==expected_fallback_handlers
    assert seal["classes"]["fallback"]["utf_handler"]==expected_fallback_handlers
    # Different overload: file-path writes are not the IOUtilities callsite.
    assert method(outer,"writeCompressed",WRITE_PATH)["declaration"]["code_sha256"]!=(
        method(outer,"writeCompressed",WRITE_STREAM)["declaration"]["code_sha256"])
    print("PASS: exact NeoForge 21.1.248 NbtIo GZIP/UTF string fallback writer bytecode")
    print("REPORT_SHA256",hashlib.sha256(raw).hexdigest())
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED NOT_MODLAUNCHER")


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--report",type=Path,required=True)
    cli.add_argument("--manifest",type=Path,required=True)
    a=cli.parse_args()
    check(a.report,a.manifest)
