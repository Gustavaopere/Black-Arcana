#!/usr/bin/env python3
"""Selected Raygun 1.0.10 X_RAY/GAMMA_RAY branch-consumer ABI evidence.

Interop-only static JVM observations from the exact publisher JAR.
No source/decompiled method is exported; no complete CFG or reaching
definitions; no gameplay/world-protection/authorized-perk certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import (
    CLASS, CLASS_SHA256, DESC, METHOD_SHA256, digest_method, AuditError, require,
)

SCOPE="EXACT_ALEXSCAVES_1010_RAYGUN_BRANCH_CONSUMER_SELECTED_JVM_SEAMS"
REGIONS=(
    ("xray_optional_entity_trace",569,669),
    ("gamma_enumeration_selector",920,962),
    ("gamma_effect_visual_dispatch",1125,1161),
)
PINNED={
    569:("iload","9"),571:("ifeq","669"),
    575:("invokevirtual","LivingEntity.getBoundingBox:"),
    640:("invokestatic","ProjectileUtil.getEntityHitResult:"),
    647:("ifnull","657"),
    922:("iload","18"),924:("ifeq","931"),927:("iconst_4",""),
    931:("iconst_0",""),932:("istore","23"),
    943:("invokevirtual","Level.getEntities:"),
    1138:("iload","18"),1140:("ifeq","1147"),
    1143:("iconst_4",""),1147:("iconst_0",""),
}
METHOD_REFS={"invokevirtual","invokestatic","invokeinterface","invokespecial",
             "invokedynamic"}
BRANCHES={"goto","goto_w","ifnull","ifnonnull"}
BRANCH_OFF=re.compile(r"^\s*(\d+)(?:\s|$)")
LOCAL_LOAD=re.compile(r"^(?:[ialfd]load)(?:_([0-3]))?$")
LOCAL_STORE=re.compile(r"^(?:[ialfd]store)(?:_([0-3]))?$")
SLOT23="23"
LIMITS={
    "method_dataflow":"NOT_RECONSTRUCTED",
    "full_control_flow_and_exception_edges":"NOT_RECONSTRUCTED",
    "selected_offsets":"SHA_EXACT_COMPILED_ONLY",
    "xray_line_of_sight_and_range":"NOT_CERTIFIED",
    "gamma_effect_value_semantics":"NOT_CERTIFIED",
    "damage_source_or_hit_acceptance":"NOT_CERTIFIED",
    "pvp_and_territory_protection":"NOT_VERIFIED",
    "runtime_transformation":"NOT_OBSERVED",
    "safe_mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}

def _local_index(ins):
    op=ins["opcode"]
    m=LOCAL_LOAD.match(op) or LOCAL_STORE.match(op)
    if not m:
        return None
    if m.group(1) is not None:
        return int(m.group(1))
    match=BRANCH_OFF.match(ins["operand"])
    require(match is not None,"unparseable JVM variable index")
    return int(match.group(1))

def _trim(ins):
    return {k:ins[k] for k in ("offset","opcode","operand","symbol")}

def inspect_selected(method):
    ins=method["instructions"]
    require(450<=len(ins)<=900,"unexpected Raygun method population")
    positions={x["offset"]:n for n,x in enumerate(ins)}
    require(len(positions)==len(ins) and list(positions)==sorted(positions),
            "duplicate or nonmonotonic JVM offsets")
    for off,(op,marker) in PINNED.items():
        require(off in positions,"missing pinned JVM offset "+str(off))
        x=ins[positions[off]]
        require(x["opcode"]==op and marker in (x["operand"]+" "+x["symbol"]),
                "drift in pinned Raygun consumer "+str(off))
    regions=[]
    for name,low,high in REGIONS:
        hits=[x for x in ins if low<=x["offset"]<high]
        require(10<=len(hits)<=95,"bounded region population changed "+name)
        calls=[];edges=[];numeric=[];locals_seen=[]
        for x in hits:
            op=x["opcode"]
            if op in METHOD_REFS:
                calls.append({"offset":x["offset"],"opcode":op,"symbol":x["symbol"]})
            if op.startswith("if") or op in BRANCHES:
                to=BRANCH_OFF.match(x["operand"])
                require(to is not None,"unknown direct branch syntax "+str(x["offset"]))
                target=int(to.group(1))
                require(target in positions,"branch points outside JVM instructions")
                index=positions[x["offset"]]
                require(index+1<len(ins),"missing branch fallthrough")
                edges.append({"offset":x["offset"],"opcode":op,
                              "taken_target":target,
                              "sequential_next":ins[index+1]["offset"]})
            if op.startswith(("iconst_","fconst_")) or op in ("bipush","sipush","ldc","ldc_w"):
                numeric.append({"offset":x["offset"],"opcode":op,
                                "operand":x["operand"],"symbol":x["symbol"]})
            index=_local_index(x)
            if index in (9,18,23):
                locals_seen.append({"offset":x["offset"],"opcode":op,
                                    "operand":x["operand"]})
        require(len(calls)<=25 and len(edges)<=32 and len(numeric)<=35 and len(locals_seen)<=25,
                "selected metadata population beyond budget")
        regions.append({
            "name":name,"offset_range_inclusive_exclusive":[low,high],
            "instruction_count":len(hits),"method_calls":calls,"branch_edges":edges,
            "numeric_operands":numeric,"selected_local_accesses":locals_seen,
            "interpretation":"SELECTED_STATIC_CLASSFILE_METADATA_ONLY",
        })
    # Across the same method, identify reads/writes of the slot receiving 4/0
    # at @932, without claiming that all accesses have the same reaching def.
    accesses=[]
    for i,x in enumerate(ins):
        if _local_index(x)!=23:continue
        accesses.append({
            "offset":x["offset"],"opcode":x["opcode"],
            "access":"WRITE" if "store" in x["opcode"] else "READ",
            "neighbors":[_trim(row) for row in ins[max(0,i-2):i+3]],
        })
    require(1<=len(accesses)<=15,"slot23 consumer population invalid")
    require(any(x["offset"]==932 and x["access"]=="WRITE" for x in accesses),
            "4/0 receiver local23 missing")
    report={
        "method_name":"onUseTick","method_descriptor":DESC,
        "parsed_method_sha256":digest_method(method),
        "instruction_count":len(ins),
        "regions":regions,
        "selected_slot23_accesses":accesses,
        "interpretation":"BOUNDED_BRANCH_CONSUMER_SEAMS_NOT_COMPLETE_CFG_OR_AUTHORITATIVE_PERKS",
    }
    require(len(json.dumps(report,ensure_ascii=False).encode())<27000,
            "bounded selected method report too large")
    return report

def analyze(jar,javap_bin):
    p=Path(jar)
    require(p.name=="alexscaves-1.0.10.jar","unexpected publisher file")
    require(sha_file(p)==(SHA1,SHA256,SIZE),
            "publisher JAR SHA and size drift")
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        require(len(names)==len(set(names)) and CLASS in names,
                "missing class or duplicate archive member")
        require(hashlib.sha256(z.read(CLASS)).hexdigest()==CLASS_SHA256,
                "compiled Raygun class drift")
    methods=parse_methods(javap(javap_bin,p,CLASS[:-6].replace("/",".")))
    found=[m for m in methods if name_of(m)=="onUseTick"
           and m["descriptor"]==DESC]
    require(len(methods)==26 and len(found)==1,
            "Raygun class method signature/roster drift")
    require(digest_method(found[0])==METHOD_SHA256,
            "exact Raygun method checksum drift")
    result={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class_path":CLASS,"class_sha256":CLASS_SHA256,
        "observations":inspect_selected(found[0]),
        "limits":LIMITS,
        "interpretation":"STATIC_BRANCH_CONSUMER_CATALOG_ONLY_NO_RUNTIME_OR_MUTATION",
    }
    require(len(json.dumps(result,ensure_ascii=False).encode())<32000,
            "evidence export exceeds strict budget")
    return result

def verify_seal(actual,expected):
    require(expected.get("scope")==SCOPE,"wrong manifest scope")
    require(expected.get("limits")==LIMITS,"unsafe manifest safety promotion")
    require(actual==expected,"selected 1.0.10 Raygun consumer seam drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    args=ap.parse_args()
    try:
        report=analyze(args.jar,args.javap)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf8")))
        out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
        print("PASS: exact Raygun 1.0.10 selected branch-consumer seams")
        print("regions="+str(len(report["observations"]["regions"]))+
              ", selected_slot23_accesses="+str(len(report["observations"]["selected_slot23_accesses"])))
        print("NO_MUTATION / NOT_CERTIFIED / physical QA not tested")
    except (AuditError,KeyError,ValueError,TypeError,OSError,zipfile.BadZipFile) as exc:
        ap.exit(1,"FAIL-CLOSED: "+str(exc)+"\n")

if __name__=="__main__":main()
