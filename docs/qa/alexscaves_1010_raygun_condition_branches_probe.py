#!/usr/bin/env python3
"""SHA-exact Raygun 1.0.10 selected condition branches; no full CFG or runtime.

A bounded JVM dataflow *observation* around X_RAY and GAMMA_RAY local slots.
Branch targets are statically validated. No claim about all reachable paths,
provider callback safety, actual gameplay damage, or player authority.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import (
    SHA1, SHA256, SIZE, CLASS, CLASS_SHA256, DESC, METHOD_SHA256,
    AuditError, require, digest_method, sha_file,
)
import hashlib
import zipfile

SCOPE="EXACT_ALEXSCAVES_1010_RAYGUN_XRAY_GAMMA_SELECTED_CONDITION_BRANCHES"
READS={"xray_local9":[105,122,569],
       "gamma_local18":[367,402,922,1029,1138]}
CONTEXT={"xray_enchant":47,"xray_store":58,
         "gamma_enchant":332,"gamma_store":346,
         "raytrace":69,"damage":1041}
LIMITS={
    "compiled_branch_targets":"STATIC_JVM_OFFSETS_ONLY",
    "full_control_flow_and_exception_cfg":"NOT_RECONSTRUCTED",
    "all_reaching_definitions":"NOT_RECONSTRUCTED",
    "exception_flow":"NOT_RECONSTRUCTED",
    "enchantment_effectiveness":"NOT_CERTIFIED",
    "range_or_line_of_sight":"NOT_CERTIFIED",
    "damage_hit_acceptance":"NOT_CERTIFIED",
    "claims_pvp_authorization":"NOT_VERIFIED",
    "safe_runtime_mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}
MAX_BYTES=34000
TARGET=re.compile(r"^\s*(\d+)(?:\s|$)")
def row(ins):return {key:ins[key] for key in ("offset","opcode","operand","symbol")}
def selected_branches(method):
    ins=method["instructions"]
    require(400<=len(ins)<=900,"Raygun 1.0.10 unexpected method length")
    offsets=[i["offset"] for i in ins]
    require(offsets==sorted(set(offsets)),"invalid Raygun JVM offsets")
    positions={v["offset"]:i for i,v in enumerate(ins)}
    require(len(positions)==len(ins),"invalid offset population")
    out=[]
    def bounded(name,offset,pre=3,post=5):
        require(offset in positions,"missing selected branch offset: "+name)
        i=positions[offset]
        return {"name":name,"offset":offset,
                "instructions":[row(x) for x in ins[max(0,i-pre):i+post+1]]}
    for kind,read_offs in READS.items():
        found=[]
        for off in read_offs:
            require(off in positions,"missing local-slot read "+str(off))
            i=positions[off]
            inst=ins[i]
            slot="9" if kind=="xray_local9" else "18"
            require(inst["opcode"]=="iload" and inst["operand"]==slot,
                    "selected local-slot identity drift @"+str(off))
            require(i+1<len(ins),"truncated branch followup")
            next_inst=ins[i+1]
            immediate=None
            if next_inst["opcode"].startswith("if"):
                target=TARGET.match(next_inst["operand"])
                require(target is not None,"unsupported conditional branch target")
                to=int(target.group(1))
                require(to in positions,"conditional target outside method")
                require(i+2<len(ins),"missing fall-through instruction")
                immediate={"opcode":next_inst["opcode"],
                           "offset":next_inst["offset"],
                           "taken_target":to,
                           "fallthrough_target":ins[i+2]["offset"],
                           "interpretation":"JVM_DIRECT_CONDITIONAL_NOT_GLOBAL_REACHABILITY"}
            found.append({**bounded(kind+"@"+str(off),off,pre=4,post=6),
                          "immediate_conditional":immediate})
        out.append({"slot":9 if kind=="xray_local9" else 18,
                    "kind":kind,"uses":found})
    anchors=[]
    for key,offset in CONTEXT.items():
        anchors.append(bounded(key,offset,pre=5,post=5))
    checks={
        47:"ACCompat.enchantLevel:",
        332:".GAMMA_RAY:",
        58:"9",
        346:"18",
        69:"ProjectileUtil.getHitResultOnViewVector:",
        1041:"ACCompat.hurt:",
    }
    for offset,needle in checks.items():
        inst=ins[positions[offset]]
        require(needle in (inst["operand"]+" "+inst["symbol"]),
                "critical Raygun symbolic anchor drift "+str(offset))
    core={
        "method":"onUseTick","descriptor":DESC,
        "parsed_method_sha256":digest_method(method),
        "instruction_count":len(ins),
        "selected_local_consumers":out,
        "selected_producer_and_effect_anchors":anchors,
        "interpretation":"SELECTED_DIRECT_BRANCH_EDGES_ONLY_NOT_COMPLETE_DEF_USE_OR_CFG",
    }
    require(len(json.dumps(core,ensure_ascii=False).encode())<MAX_BYTES,
            "bounded report too large")
    return core

def analyze(jar,javap_path):
    jar=Path(jar)
    require(jar.name=="alexscaves-1.0.10.jar","unexpected artifact filename")
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"physical publisher checksum mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)) and CLASS in names,
                "missing class/duplicate ZIP entry")
        require(hashlib.sha256(z.read(CLASS)).hexdigest()==CLASS_SHA256,
                "publisher Raygun class SHA mismatch")
    methods=parse_methods(javap(javap_path,jar,CLASS[:-6].replace("/",".")))
    chosen=[m for m in methods if name_of(m)=="onUseTick" and
            m["descriptor"]==DESC]
    require(len(methods)==26 and len(chosen)==1,"wrong method identity")
    require(digest_method(chosen[0])==METHOD_SHA256,"Raygun pinned method SHA drift")
    out={"schema_version":1,"scope":SCOPE,
         "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
         "class":{"path":CLASS,"sha256":CLASS_SHA256},
         "branch_observations":selected_branches(chosen[0]),
         "limits":LIMITS,
         "interpretation":"NO_MUTATION_CONDITION_BRANCHES_NOT_PROVIDER_RUNTIME_CERTIFICATION"}
    require(len(json.dumps(out,ensure_ascii=False).encode())<46000,
            "output budget exceeded")
    return out

def check_seal(actual,sealed):
    require(sealed.get("scope")==SCOPE,"wrong evidence scope")
    require(sealed.get("limits")==LIMITS,"unsafe safety-gate drift")
    require(actual==sealed,"selected Raygun branch ABI drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    a=ap.parse_args()
    try:
        observed=analyze(a.jar,a.javap)
        if a.seal:
            check_seal(observed,json.loads(Path(a.seal).read_text(encoding="utf8")))
        path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(observed,ensure_ascii=False,indent=2)+"\n",
                        encoding="utf8")
        branches=[u["immediate_conditional"]
                  for slot in observed["branch_observations"]["selected_local_consumers"]
                  for u in slot["uses"]]
        print("PASS: exact 1.0.10 X_RAY/GAMMA_RAY local reads inspected")
        print("local_reads="+str(len(branches))+
              " immediate_conditional="+str(sum(b is not None for b in branches)))
        print("NO_MUTATION / NOT_CERTIFIED / no full CFG or physical QA")
    except (AuditError,ValueError,KeyError,OSError,TypeError) as e:
        ap.exit(1,"FAIL-CLOSED: "+str(e)+"\n")
if __name__=="__main__":main()
