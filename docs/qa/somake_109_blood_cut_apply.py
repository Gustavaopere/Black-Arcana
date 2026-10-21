#!/usr/bin/env python3
"""Somake 1.0.9 secondary DamageSources.applyDamage callsite — clean-room survey.

Reports only bounded derived metadata and abbreviated opcodes/member symbols.
It does not export the publisher method body/JAR, reconstruct host settlement,
or certify actual damage, target eligibility, or per-player perk hooks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from somake_109_perk_method_probe import GateError, FILENAME, SHA1
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_blood_cut_cfg import EFFECT_CLASS, EVENT, EVENT_DESCRIPTOR, graph_paths
from somake_109_blood_cut_event_args import inspect as verify_event

APPLY="io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:"
MAX_ROWS=180

def survey_application(rows):
    if not 5<=len(rows)<=MAX_ROWS:
        raise GateError("applyDamage JVM instruction cohort outside bounded survey")
    pcs=[pc for pc,_,_,_ in rows]
    if pcs!=sorted(set(pcs)):
        raise GateError("invalid or duplicate JVM program counters")
    sites=[i for i,(_,op,_,comment) in enumerate(rows)
           if APPLY in comment]
    if len(sites)!=1:
        raise GateError("non-unique/missing DamageSources.applyDamage symbol")
    i=sites[0]
    pc,op,operand,comment=rows[i]
    if op!="invokestatic" or not re.search(r"applyDamage:\([^)]*\)[VZIFDLjava/\[;]+",comment):
        raise GateError("applyDamage must be typed invokestatic")
    if i<3 or i>=len(rows)-1:
        raise GateError("applyDamage call lacks bounded predecessor/successor")
    before=rows[max(0,i-21):i]
    after=rows[i+1:min(len(rows),i+4)]
    # Not bytecode: only an index-scoped machine-opcode summary.
    typed_sites=[]
    for j,(p,k,arg,c) in enumerate(rows[max(0,i-42):i+1],start=max(0,i-42)):
        if k.startswith("invoke"):
            symbol=(c.split(":",1)[0].split(" ",1)[-1]) if c else ""
            typed_sites.append({"index":j,"category":k,"symbol":symbol[-125:]})
    return {
        "assurance":"STATIC_CALLSITE_SURVEY_ONLY",
        "instruction_count":len(rows),
        "apply_damage_callsite_count":1,
        "apply_damage_instruction_index":i,
        "apply_damage_jvm_descriptor":comment.split("applyDamage:",1)[-1].strip(),
        "preceding_opcode_kinds":[op for _,op,_,_ in before],
        "following_opcode_kinds":[op for _,op,_,_ in after],
        "invocation_opcode_families":sorted(set("invoke" for _,op,_,_ in rows if op.startswith("invoke"))),
        "nearby_typed_invocation_symbols":typed_sites[-12:],
        "final_invocation_descriptors":[{
            "index":j,"symbol":c.split(":",1)[0].split(" ",1)[-1][-125:],
            "descriptor":c.split(":",1)[1].strip()[:240]
        } for j,(_,k,_,c) in enumerate(rows[max(0,i-14):i+1],start=max(0,i-14))
            if k.startswith("invoke") and ":" in c],
        "final_cast_types":[{"index":j,"type":c[:120]} for j,(_,k,_,c) in
            enumerate(rows[max(0,i-14):i+1],start=max(0,i-14))
            if k=="checkcast"],
        "local_3_float_store_indices":[j for j,(_,o,arg,_) in enumerate(rows[:i]) if o=="fstore_3" or o=="fstore" and arg.strip()=="3"],
        "limit":"Symbol/type and opcode-window survey only: no stack argument provenance, target, actual host damage or heal validated."
    }


def inspect(jar:Path)->dict:
    jar=Path(jar)
    if jar.name!=FILENAME or not jar.is_file() or jar.is_symlink():
        raise GateError("wrong/missing physical provider artifact")
    original=verify_event(jar)
    if original["sha1"]!=SHA1:
        raise GateError("upstream event causal evidence SHA drift")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),EFFECT_CLASS],
                     capture_output=True,text=True,check=False,timeout=40)
    if p.returncode or not 100<len(p.stdout)<1_500_000:
        raise GateError("javap exact provider inspection failed")
    matches=[opcode_rows(body) for n,d,body in sections(p.stdout)
             if n==EVENT and d==EVENT_DESCRIPTOR]
    if len(matches)!=1:
        raise GateError("missing/ambiguous Blood Cut Post method")
    graph=graph_paths(matches[0],expected_branches=5)
    report=survey_application(matches[0])
    if graph["secondary_apply_damage_index"]!=report["apply_damage_instruction_index"]:
        raise GateError("CFG/applyDamage evidence incoherent")
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError("JAR changed during inspection")
    return {"status":"PASS_SHA_EXACT_BLOOD_CUT_APPLY_DAMAGE_CALLSITE_SCOUT",
            "sha1":SHA1,"provider":"somakespells","version":"1.0.9",
            "method":"BloodCutEffect.onLivingDamage(LivingDamageEvent.Post)",
            "apply_callsite":report,
            "limit":"Scout does not demonstrate call argument origins or healing. No mutating integration allowed."}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("BLOOD_CUT_APPLY_SCOUT",result["status"],result["sha1"])
    print("BLOOD_CUT_APPLY_WINDOW",json.dumps(result["apply_callsite"],sort_keys=True))


if __name__=="__main__":
    main()
