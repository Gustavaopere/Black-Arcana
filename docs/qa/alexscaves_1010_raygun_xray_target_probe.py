#!/usr/bin/env python3
"""Exact Alex's Caves 1.0.10 Raygun targeting: bounded JVM branch windows.

Clean-room interop research. Does not export complete proprietary method bodies,
reconstruct all exceptional CFG edges, prove runtime targeting, or certify perks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of

CLASS="com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
CLASS_SHA256="3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
EXACT_DESCRIPTOR="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"
METHOD_SHA256="b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5"
PIVOTS={
    "xray_enchantment":44,
    "view_vector_trace":69,
    "entity_trace":640,
    "server_target_enumeration":943,
    "damage_factory":1026,
    "hurt_request":1041,
}
SELECTOR_WORDS=("X_RAY","GAMMA_RAY","ProjectileUtil.","Level.getEntities:",
                "Entity.isAlliedTo:","LivingEntity.isAlliedTo:",
                "isPassengerOfSameVehicle:","causeRaygunDamage:","ACCompat.hurt:")
SCOPE="EXACT_ALEXSCAVES_1010_RAYGUN_XRAY_TARGET_BRANCH_WINDOWS_ONLY"
LIMITS={
    "complete_control_flow_graph":"NOT_RECONSTRUCTED",
    "exception_edges":"NOT_RECONSTRUCTED",
    "effective_range_or_target_count":"NOT_CERTIFIED",
    "line_of_sight_and_claim_resolution":"NOT_VERIFIED",
    "xray_enchantment_semantics":"SELECTED_BYTECODE_ONLY",
    "server_runtime_authority":"NOT_VERIFIED",
    "safe_mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}
MAX_BYTES=27000
class ProbeError(ValueError):pass
def require(ok,msg):
    if not ok:raise ProbeError(msg)
def digest_method(method):
    return hashlib.sha256(json.dumps(method,sort_keys=True,ensure_ascii=False,
                  separators=(",",":")).encode("utf-8")).hexdigest()

def select_windows(method):
    ins=method["instructions"]
    require(200<len(ins)<1900,"unexpected Raygun onUseTick instruction population")
    offs=[x["offset"] for x in ins]
    require(len(offs)==len(set(offs)) and offs==sorted(offs),
            "duplicate or unordered JVM instruction offsets")
    positions={x["offset"]:i for i,x in enumerate(ins)}
    windows=[]
    for title,offset in PIVOTS.items():
        require(offset in positions,"missing/changed anchor "+title)
        index=positions[offset]
        item=ins[index]
        if title=="xray_enchantment":
            require(".X_RAY:" in item["symbol"],"X_RAY field no longer at pinned offset")
        if title=="view_vector_trace":
            require("ProjectileUtil.getHitResultOnViewVector" in item["symbol"],
                    "view-vector trace callsite moved")
        if title=="entity_trace":
            require("ProjectileUtil.getEntityHitResult" in item["symbol"],
                    "entity trace callsite moved")
        if title=="server_target_enumeration":
            require("Level.getEntities:" in item["symbol"],
                    "server target list callsite moved")
        if title=="damage_factory":
            require("causeRaygunDamage:" in item["symbol"],
                    "native damage source callsite moved")
        if title=="hurt_request":
            require("ACCompat.hurt:" in item["symbol"],
                    "native damage request callsite moved")
        neighborhood=ins[max(0,index-9):index+10]
        require(len(neighborhood)<=19,"oversize selected evidence window")
        windows.append({"name":title,"offset":offset,
                        "anchor_opcode":item["opcode"],"anchor_symbol":item["symbol"],
                        "window":neighborhood})
    markers=[]
    for x in ins:
        if any(s in x["symbol"] for s in SELECTOR_WORDS):
            markers.append({"offset":x["offset"],"opcode":x["opcode"],
                            "symbol":x["symbol"]})
    require(len(markers)<=65,"selected marker population exceeds budget")
    branch_neighborhoods=[]
    for w in windows:
        branches=[{"offset":x["offset"],"opcode":x["opcode"],"operand":x["operand"]}
                  for x in w["window"]
                  if x["opcode"].startswith("if") or
                     x["opcode"] in ("goto","goto_w")]
        branch_neighborhoods.append({"pivot":w["name"],"branches":branches})
    return {
        "method_name":"onUseTick",
        "method_descriptor":EXACT_DESCRIPTOR,
        "parsed_method_sha256":digest_method(method),
        "instruction_count":len(ins),
        "reference_markers":markers,
        "windows":windows,
        "branch_neighborhoods":branch_neighborhoods,
        "interpretation":"BOUNDED_JVM_WINDOWS_NOT_COMPLETE_CFG_OR_RANGE_CERTIFICATION",
    }

def audit(jar,javap_path):
    jar=Path(jar)
    require(jar.name=="alexscaves-1.0.10.jar","unexpected publisher JAR filename")
    require(sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher JAR SHA/size mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP entries")
        require(CLASS in names,"missing exact Raygun class")
        require(hashlib.sha256(z.read(CLASS)).hexdigest()==CLASS_SHA256,
                "RaygunItem class SHA drift")
    methods=parse_methods(javap(javap_path,jar,CLASS[:-6].replace("/",".")))
    candidates=[m for m in methods if name_of(m)=="onUseTick"
                and m["descriptor"]==EXACT_DESCRIPTOR]
    require(len(methods)==26 and len(candidates)==1,
            "unexpected Raygun declared methods / onUseTick identity")
    method=candidates[0]
    require(digest_method(method)==METHOD_SHA256,"Raygun exact onUseTick drift")
    result={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class_path":CLASS,"class_sha256":CLASS_SHA256,
        "declared_method_count":len(methods),
        "selected":select_windows(method),
        "limits":LIMITS,
        "interpretation":"STATIC_SELECTED_BRANCH_WINDOWS_NO_EFFECTIVE_OR_MUTABLE_TARGETING",
    }
    require(len(json.dumps(result,ensure_ascii=False).encode("utf8"))<MAX_BYTES,
            "selected interop evidence exceeds budget")
    return result

def verify_seal(observed,seal):
    require(seal.get("scope")==SCOPE,"incorrect sealed scope")
    require(seal.get("limits")==LIMITS,"unsafe limit promotion")
    require(observed==seal,"Raygun exact selected target/trace evidence drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    args=ap.parse_args()
    try:
        report=audit(args.jar,args.javap)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf8")))
        out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",
                       encoding="utf8")
        print("PASS: exact Alex's Caves 1.0.10 Raygun selected targeting windows")
        print("pivots="+str(len(report["selected"]["windows"]))+
              ", selected_markers="+str(len(report["selected"]["reference_markers"])))
        print("NO_MUTATION / NOT_CERTIFIED / full CFG & physical QA outstanding")
    except (ProbeError,ValueError,KeyError,TypeError,OSError) as exc:
        ap.exit(1,"FAIL-CLOSED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
