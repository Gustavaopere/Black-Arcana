#!/usr/bin/env python3
"""Bounded, read-only inspection of the exact FTB Chunks 2101.1.22 explosion seam.

This records selected JVM ABI and symbolic call sites only. It cannot prove
land-claim enforcement, effective event registration, or per-block safety.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from neoforge_211248_grief_event_probe import EvidenceError, parse_methods, require

JAR_NAME = "ftb-chunks-neoforge-2101.1.22.jar"
ARTIFACT_SHA256 = "4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217"
CLASS_PATH = "dev/ftb/mods/ftbchunks/neoforge/FTBChunksForge.class"
CLASS_SHA256 = "64d32b0e46d2e9c454fb78ad656348965971fa4a443251bf8b9ecf465cc5f553"
EXPLOSION_DESCRIPTOR = "(Lnet/neoforged/neoforge/event/level/ExplosionEvent$Detonate;)V"
MAX_REPORT = 29000
LIMITS = {
    "native_explosion_dispatch": "NOT_VERIFIED",
    "mixin_and_datapack_behavior": "NOT_VERIFIED",
    "loaded_claim_configuration": "NOT_VERIFIED",
    "blockstate_on_block_exploded": "NOT_VERIFIED",
    "direct_level_destroy_block": "NOT_VERIFIED",
    "claim_per_affected_block": "NOT_CERTIFIED",
    "world_effect_policy": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutating_hook": "NOT_VERIFIED",
    "mutation": "NO_MUTATION",
    "perk_certification": "NOT_CERTIFIED",
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def selected_summary(method):
    ins=method["instructions"]
    require(1 <= len(ins) <= 1200, "unexpected selected explosion method size")
    offsets=[i["offset"] for i in ins]
    require(offsets==sorted(set(offsets)), "duplicate JVM offsets")
    refs=[{"offset":i["offset"],"opcode":i["opcode"],"symbol":i["symbol"]}
          for i in ins if i["symbol"] and i["opcode"].startswith(
             ("invoke","get","put","new","checkcast","instanceof"))]
    branches=[{"offset":i["offset"],"opcode":i["opcode"],"operand":i["operand"]}
              for i in ins if i["opcode"].startswith(("if","goto")) or
              i["opcode"] in ("ireturn","areturn","return")]
    require(len(refs)<=150 and len(branches)<=150, "selected explosion output too large")
    return {"name":method["name"],"descriptor":method["descriptor"],
            "instruction_count":len(ins),
            "method_sha256":sha(json.dumps(ins,sort_keys=True,separators=(",",":")).encode()),
            "references":refs,"branches_and_returns":branches,
            "scope":"STATIC_REFERENCE_SITES_NOT_EFFECTIVE_RUNTIME"}

def inspect(jar,javap):
    jar=Path(jar)
    require(jar.name==JAR_NAME, "wrong FTB exact artifact filename")
    require(jar.is_file() and 10000 < jar.stat().st_size < 5_000_000, "missing/oversized JAR")
    data=jar.read_bytes()
    require(sha(data)==ARTIFACT_SHA256, "publisher JAR hash drift")
    require(zipfile.is_zipfile(jar),"not a valid JAR")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)), "duplicate ZIP member")
        require(CLASS_PATH in names,"missing publisher protection class")
        require(sha(z.read(CLASS_PATH))==CLASS_SHA256,"publisher protection class drift")
    proc=subprocess.run([javap,"-classpath",str(jar),"-p","-s","-c",
                         CLASS_PATH[:-6].replace("/",".")],
                        text=True,capture_output=True,timeout=45,check=False)
    require(proc.returncode==0,"javap failed "+proc.stderr[:180])
    methods=parse_methods(proc.stdout)
    require(1 <= len(methods) <= 240, "unexpected publisher method population")
    primary=[m for m in methods if m["descriptor"]==EXPLOSION_DESCRIPTOR]
    require(len(primary)==1,
            "missing/ambiguous ExplosionEvent.Detonate handler; found="+str(len(primary)))
    name=primary[0]["name"]
    # Compiler-generated helpers are collected as a distinct subpopulation;
    # no method or ownership inference is made from their names alone.
    lambdas=[m for m in methods if m["name"].startswith("lambda$"+name+"$")]
    require(len(lambdas)<=18, "unexpected explosion lambda population")
    selected=[primary[0]]+lambdas
    require(len({(m["name"],m["descriptor"]) for m in selected})==len(selected),
            "ambiguous explosion JVM descriptors")
    items=[selected_summary(m) for m in selected]
    allrefs=[r["symbol"] for item in items for r in item["references"]]
    markers={
        "explosion_affected_blocks": "getAffectedBlocks:",
        "explosion_affected_entities": "getAffectedEntities:",
        "chunk_dimension_position": "ChunkDimPos",
        "claimed_chunk_lookup": "ClaimedChunkManagerImpl.getChunk:",
        "allow_explosions_check": "allowExplosions:",
        "block_position_iteration": "BlockPos",
        "chunk_position_iteration": "ChunkPos",
        "list_mutation": "List.clear:",
        "event_cancel": "setCanceled:",
        "direct_world_block_break": "Level.destroyBlock:",
    }
    result={
      "schema_version":1,
      "scope":"FTBCHUNKS_2101_1_22_EXACT_EXPLOSION_SELECTED_ABI_ONLY",
      "artifact":{"coordinates":"dev.ftb.mods:ftb-chunks-neoforge:2101.1.22",
                  "size_bytes":len(data),"sha256":sha(data)},
      "class":{"path":CLASS_PATH,"sha256":CLASS_SHA256,
               "declared_method_count":len(methods)},
      "primary_handler_name":name,
      "selected_methods":items,
      "observed_symbolic_anchors":{k:any(v in r for r in allrefs)
                                   for k,v in markers.items()},
      "interpretation":"SELECTED_COMPILED_REFERENCES_ONLY_NOT_CLAIM_PROTECTION_CERTIFICATION",
      "limits":LIMITS
    }
    require(len(json.dumps(result).encode("utf-8"))<MAX_REPORT,
            "bounded report output budget exceeded")
    return result

def verify_seal(observed,seal):
    require(seal.get("scope")=="FTBCHUNKS_2101_1_22_EXACT_EXPLOSION_SELECTED_ABI_ONLY",
            "unexpected sealed scope")
    require(seal.get("limits")==LIMITS, "unsafe certificate promotion")
    require(observed==seal,"SHA-exact FTB explosion ABI drift")
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--output",required=True)
    parser.add_argument("--seal")
    args=parser.parse_args()
    try:
        report=inspect(args.jar,args.javap)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf-8")))
        out=Path(args.output)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("PASS: exact FTB Chunks explosion ABI inventory; "+
              report["artifact"]["sha256"])
        print("selected_methods="+str(len(report["selected_methods"]))+
              ", labels="+json.dumps(report["observed_symbolic_anchors"],sort_keys=True))
        print("NO_MUTATION / NOT_CERTIFIED / per-block claims and world QA unverified")
    except (EvidenceError,ValueError,KeyError,TypeError,OSError,
            subprocess.TimeoutExpired) as exc:
        parser.exit(1,"FAIL-CLOSED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
