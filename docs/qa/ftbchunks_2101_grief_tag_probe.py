#!/usr/bin/env python3
"""Read-only, bounded ABI/resource inventory for exact FTB Chunks 2101.1.22.

Do not infer claims permission from one event, nor reproduce vendor code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from neoforge_211248_grief_event_probe import parse_methods, require, EvidenceError

JAR_NAME = "ftb-chunks-neoforge-2101.1.22.jar"
COORDINATES = "dev.ftb.mods:ftb-chunks-neoforge:2101.1.22"
CLASS_SUFFIX = "/NeoEventListeners.class"
TAG_PATH = "data/ftbchunks/tags/entity_type/entity_mob_griefing_blacklist.json"
METHOD_NAME = "mobGriefing"
METHOD_DESC = "(Lnet/neoforged/neoforge/event/entity/EntityMobGriefingEvent;)V"
MAX_JAR = 5_000_000
MAX_REPORT = 24_000

def digest(b):
    return hashlib.sha256(b).hexdigest()

def validate_tag(raw):
    require(len(raw) < 12_000, "FTB entity tag too large")
    parsed = json.loads(raw)
    require(isinstance(parsed, dict), "invalid entity tag JSON")
    values = parsed.get("values")
    require(isinstance(values,list) and len(values) <= 70, "invalid blacklist population")
    ids = []
    for v in values:
        if isinstance(v,str):
            token=v
        elif isinstance(v,dict) and set(v) <= {"id","required"}:
            token=v.get("id")
        else:
            raise EvidenceError("unsupported tag entry")
        require(isinstance(token,str) and 1 <= len(token) <= 150,
                "invalid entity tag id")
        ids.append(token)
    require(len(ids)==len(set(ids)), "duplicate entity tag identifier")
    replace=parsed.get("replace",False)
    require(isinstance(replace,bool), "invalid tag replace policy")
    return {"path":TAG_PATH, "sha256":digest(raw),
            "replace":replace, "declared_values":ids, "value_count":len(ids),
            "note":"JAR-local tag only; datapacks and other mods can override/append."}

def analyze_method(method):
    ins = method["instructions"]
    require(1 <= len(ins) <= 550, "unexpected mob grief method instruction count")
    offsets = [i["offset"] for i in ins]
    require(offsets==sorted(set(offsets)), "duplicate JVM offsets")
    refs = [{"offset":i["offset"],"opcode":i["opcode"],"symbol":i["symbol"]}
            for i in ins if i["symbol"] and i["opcode"].startswith(
                ("invoke","get","put","new","checkcast"))]
    jumps = [{"offset":i["offset"],"opcode":i["opcode"],"operand":i["operand"]}
             for i in ins if i["opcode"].startswith(("if","goto")) or
             i["opcode"] in ("return","ireturn","areturn")]
    require(len(refs) <= 95 and len(jumps) <= 75, "bounded method report limit")
    symbols = [i["symbol"] for i in refs]
    needles = {
       "entity_event_parameter": "EntityMobGriefingEvent",
       "entity_type_tag_test": "Entity.is:",
       "tag_registry_reference": "ENTITY_MOB_GRIEFING_BLACKLIST_TAG",
       "claimed_chunk_access": "ClaimedChunkManagerImpl",
       "chunk_position_from_entity": "ChunkDimPos",
       "chunk_allow_mob_griefing": "allowMobGriefing:",
       "event_set_can_grief": "setCanGrief:",
       "client_side_test": "isClientSide",
    }
    return {
      "name":method["name"],"descriptor":method["descriptor"],
      "instruction_count":len(ins),
      "method_sha256":digest(json.dumps(ins,sort_keys=True,separators=(",",":")).encode()),
      "selected_references":refs,"branches_and_returns":jumps,
      "symbolic_presence":{k:any(v in s for s in symbols) for k,v in needles.items()},
      "limit":"SYMBOLS_OBSERVED_ONLY_NOT_COMPLETE_CFG",
    }

def audit(jar,javap):
    jar=Path(jar)
    require(jar.name==JAR_NAME, "wrong FTB Chunks 2101.1.22 artifact filename")
    require(jar.is_file() and 10000 < jar.stat().st_size < MAX_JAR,
            "unexpected exact JAR size")
    binary=jar.read_bytes()
    require(zipfile.is_zipfile(jar), "invalid JAR archive")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR entries")
        candidates=[p for p in names if p.endswith(CLASS_SUFFIX)]
        require(len(candidates)==1, "missing/ambiguous NeoEventListeners class")
        selected_class=candidates[0]
        require(TAG_PATH in names, "FTB blacklist tag missing from published JAR")
        tag=validate_tag(z.read(TAG_PATH))
        class_digest=digest(z.read(selected_class))
    fqcn=selected_class[:-6].replace("/",".")
    proc=subprocess.run([javap,"-classpath",str(jar),"-p","-s","-c",fqcn],
                        capture_output=True,text=True,timeout=45,check=False)
    require(proc.returncode==0, "javap failed: "+proc.stderr[:200])
    methods=parse_methods(proc.stdout)
    chosen=[m for m in methods if m["name"]==METHOD_NAME and m["descriptor"]==METHOD_DESC]
    require(len(chosen)==1, "missing/ambiguous exact EntityMobGriefingEvent handler")
    item=analyze_method(chosen[0])
    report={
      "schema_version":1,
      "scope":"EXACT_FTBCHUNKS_2101_1_22_GRIEF_EVENT_AND_DEFAULT_TAG_ONLY",
      "artifact":{"coordinates":COORDINATES,"size_bytes":len(binary),"sha256":digest(binary)},
      "class_path":selected_class,"class_sha256":class_digest,
      "method":item,"default_entity_tag":tag,
      "interpretation":"EVENT_HANDLER_AND_JAR_LOCAL_TAG_NOT_CLAIM_PERMISSION",
      "limits":{
        "external_data_pack_tag_resolutions":"NOT_VERIFIED",
        "tremorzilla_entity_type_tag_membership":"NOT_VERIFIED",
        "claim_region_per_affected_block":"NOT_VERIFIED",
        "actual_loaded_claim_state":"NOT_VERIFIED",
        "event_bus_registration":"NOT_VERIFIED",
        "black_arcana_world_effect_policy":"NOT_VERIFIED",
        "mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION",
        "perk_certification":"NOT_CERTIFIED",
      }
    }
    require(len(json.dumps(report).encode("utf-8")) < MAX_REPORT,
            "FTB report export budget exceeded")
    return report

def verify_seal(report,seal):
    require(report==seal, "SHA-exact FTB Chunks tag/event seal drift")
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",required=True)
    p.add_argument("--seal")
    args=p.parse_args()
    try:
        report=audit(args.jar,args.javap)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf-8")))
        out=Path(args.output)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("PASS: SHA-exact FTB Chunks 2101.1.22 discovery; sha256="
              +report["artifact"]["sha256"])
        print("Event handler callsite presence: "+json.dumps(report["method"]["symbolic_presence"],sort_keys=True))
        print("NO_MUTATION / NOT_CERTIFIED / deployed claims and datapacks unverified")
    except (EvidenceError,ValueError,KeyError,OSError,subprocess.TimeoutExpired,TypeError) as e:
        p.exit(1,"FAIL-CLOSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
