#!/usr/bin/env python3
"""Clean-room Somake 1.0.9 bud impact damage-success branch scout.

Never exports publisher bytecode, full disassembly or JAR. Reuses the pinned
impact geometry gate as a required precursor, then emits bounded CFG facts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_bud_impact_geometry import (
    CLASS, DESC, certify_exact_impact_geometry_109, prove_impact_box_and_query,
)

def branch_target(rows,idx):
    arg=rows[idx][2].split(" ",1)[0]
    pc={r[0]:i for i,r in enumerate(rows)}
    return pc.get(int(arg)) if arg.isdecimal() else None

def call_indices(rows,needle):
    return [i for i,(_,op,_,comment) in enumerate(rows) if
            op.startswith("invoke") and needle in comment]

def impact_damage_branch_scout(declared):
    candidates=[b for name,desc,b in declared if name=="impact" and desc==DESC]
    if len(candidates)!=1:return {"status":"NOT_PROVED","reason":"exact_impact_method_missing_or_ambiguous"}
    rows=opcode_rows(candidates[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"unexpected_impact_instruction_count","count":len(rows)}
    damage=call_indices(rows,"DamageSources.applyDamage:")
    status=call_indices(rows,".addEffect:")
    push=call_indices(rows,".push:")
    event=call_indices(rows,"SpellHealEvent.")
    healing=call_indices(rows,".heal:")
    observed={
        "damage_call_indices":damage,"status_call_indices":status,"push_call_indices":push,
        "spell_heal_event_indices":event,"heal_call_indices":healing,
        "damage_dispatch":rows[118][1],
        "damage_returns_boolean":rows[118][3].endswith(")Z"),
        "branch_after_damage":rows[119][1],
        "damage_branch_target":branch_target(rows,119),
        "post_status_branch":rows[143][1],
        "post_status_branch_target":branch_target(rows,143),
        "loop_back_edge":branch_target(rows,145),
        "effect_field_categories":[
            {"instruction_index":i,
             "field_category":"wither" if "WITHER" in c.upper() else (
                 "other_mob_effect" if "MobEffects" in c else "other")}
            for i,(_,op,_,c) in enumerate(rows[120:139],start=120)
            if op=="getstatic"
        ][:14],
        "damage_neighbors":[
            {"index":i,"opcode":rows[i][1],
             "call_category":("damage" if i in damage else "status" if i in status
                              else "push" if i in push else "other" if rows[i][1].startswith("invoke") else ""),
             "local_kind":rows[i][1].split("_")[0] if rows[i][1].startswith(("aload","fload","iload")) else ""}
            for i in range(108,146)
        ],
        "boundary":"Structural facts only; no targets, Wither identity, damage success, gameplay or perk API inferred"
    }
    if damage!=[118] or status!=[132] or push!=[138]:
        return {"status":"NOT_PROVED","reason":"damage_status_push_native_sites_drift",
                "damage_count":len(damage),"status_count":len(status),"push_count":len(push)}
    if rows[119][1]!="ifeq" or branch_target(rows,119)!=145:
        return {"status":"NOT_PROVED","reason":"damage_return_branch_shape_drift",**observed}
    observed["status"]="OBSERVED_DAMAGE_RETURN_GATE_AND_EFFECT_CALL_SITES"
    return observed

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("invalid Somake publisher file")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("unexpected Somake SHA1")
    with zipfile.ZipFile(jar) as archive:
        entries=archive.namelist()
        if len(entries)!=len(set(entries)) or CLASS.replace(".","/")+".class" not in entries:
            raise GateError("duplicate entries or class missing")
        m=archive.read("META-INF/neoforge.mods.toml")
        if len(m)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",m):
            raise GateError("Somake mod id mismatch")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
                     capture_output=True,text=True,timeout=60,check=False)
    if p.returncode or not p.stdout or len(p.stdout)>1_400_000:
        raise GateError("bounded javap failure")
    d=sections(p.stdout)
    certify_exact_impact_geometry_109(prove_impact_box_and_query(d))
    proof=impact_damage_branch_scout(d)
    if proof["status"]!="OBSERVED_DAMAGE_RETURN_GATE_AND_EFFECT_CALL_SITES":
        raise GateError("Somake native impact damage gate changed")
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:
        raise GateError("JAR changed during inspection")
    return {"status":"SHA_EXACT_BUD_DAMAGE_BRANCH_SCOUT","sha1":digest,
            "version":"1.0.9","mod_id":"somakespells","damage_flow":proof,
            "limits":"Static call/branch topology only; provider-loaded behavior and perk hooks unproven"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    x=a.parse_args()
    v=inspect(x.jar)
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(v,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_BUD_DAMAGE_BRANCH_SCOUT",json.dumps(v["damage_flow"],sort_keys=True))
    print("SOMAKE_BUD_DAMAGE_BRANCH_SHA",v["sha1"])
if __name__=="__main__":
    main()
