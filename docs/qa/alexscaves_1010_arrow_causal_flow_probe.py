#!/usr/bin/env python3
"""Read-only exact 1.0.10 Arrow Inducting JVM causal anchor census.

Produces direct callsites, branch destinations, constant operands and method
fingerprints. No decompiled implementation, complete CFG, runtime mutation,
gameplay QA or implied perk certification.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from alexscaves_1010_arrow_inducting_lifecycle_probe import (
    EVENT, ARROW, SHA1, SHA256, SIZE, RESOURCE_HASH, require, audit
)

SCOPE="EXACT_ALEXSCAVES_1010_ARROW_INDUCTING_CAUSAL_JVM_ANCHORS"
EXPECTED_METHODS={EVENT:1,ARROW:12}

def row(record):
    return {k:record[k] for k in ("offset","opcode","symbol")}

def branch(record):
    return {k:record[k] for k in ("offset","opcode","operand")}

def number(record):
    return {k:record[k] for k in ("offset","opcode","operand","symbol")}

def project(data):
    require(data["artifact"]=={"sha1":SHA1,"sha256":SHA256,
                              "size_bytes":SIZE},"publisher artifact identity drift")
    out={}
    for path,expected in EXPECTED_METHODS.items():
        require(path in data["classes"],"missing class: "+path)
        source=data["classes"][path]
        methods=source["methods"]
        require(len(methods)==expected,"declared method inventory drift")
        rows=[]
        keys=set()
        for method in methods:
            key=(method["name"],method["descriptor"])
            require(key not in keys,"duplicate JVM method in census")
            keys.add(key)
            refs=[row(x) for x in method["refs"]]
            branches=[branch(x) for x in method["branch_edges"]]
            scalars=[number(x) for x in method["numeric_operands"]]
            for seq in (refs,branches,scalars):
                offsets=[x["offset"] for x in seq]
                require(offsets==sorted(set(offsets)),
                        "duplicate/unsorted semantic offsets")
            require(len(refs)<=180 and len(branches)<=180 and len(scalars)<=180,
                    "unbounded JVM anchors")
            rows.append({
                "name":method["name"],
                "descriptor":method["descriptor"],
                "method_sha256":method["method_sha256"],
                "instruction_count":method["instruction_count"],
                "direct_references":refs,
                "conditional_and_unconditional_branches":branches,
                "numeric_operands":scalars,
            })
        out[path]={"class_sha256":source["class_sha256"],
                   "declared_method_count":source["parsed_method_count"],
                   "inspected_methods":rows}
    require(any(m["name"]=="acLivingAttack" for m in out[EVENT]["inspected_methods"]),
            "event consumer not in projection")
    require(any(m["name"]=="tick" for m in out[ARROW]["inspected_methods"]),
            "seeking-arrow tick not in projection")
    return {
        "schema_version":1,
        "scope":SCOPE,
        "artifact_sha1":SHA1,
        "artifact_sha256":SHA256,
        "enchantment_json_sha256":RESOURCE_HASH,
        "classes":out,
        "limits":{
            "evidence":"DIRECT_JVM_REFERENCES_BRANCHES_AND_NUMERIC_OPERANDS",
            "full_control_flow_graph":"NOT_RECONSTRUCTED",
            "inherited_arrow_collision_pipeline":"NOT_AUDITED",
            "engine_damage_acceptance":"NOT_VERIFIED",
            "effective_datapacks":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "perk_certification":"NOT_CERTIFIED",
            "mutation":"NO_MUTATION",
        },
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--output",type=Path)
    parser.add_argument("--seal",type=Path)
    parser.add_argument("--emit-json",action="store_true")
    args=parser.parse_args()
    data=project(audit(args.jar,args.javap))
    if args.seal:
        require(data==json.loads(args.seal.read_text(encoding="utf8")),
                "Arrow Inducting exact causal anchors seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf8")
    if args.emit_json:
        print("ARROW_FLOW_JSON="+json.dumps(data,separators=(",",":"),ensure_ascii=False))
    print("ARROW_FLOW_STATUS",
          "SEALED" if args.seal else "UNSEALED_DISCOVERY",
          "METHODS",sum(len(v["inspected_methods"]) for v in data["classes"].values()),
          "NO_MUTATION")

if __name__=="__main__":
    main()
