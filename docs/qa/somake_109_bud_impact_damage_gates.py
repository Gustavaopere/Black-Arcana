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


def certify_damage_success_effect_path(declared):
    """Prove native boolean result gates Wither call and push *attempts*.

    Never equate applyDamage(true), addEffect or push invocation with damage
    amount, successful status, applied knockback or modpack gameplay.
    """
    members=[b for n,d,b in declared if n=="impact" and d==DESC]
    if len(members)!=1:return {"status":"NOT_PROVED","reason":"ambiguous_impact"}
    rows=opcode_rows(members[0])
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=279:return fail("instruction_count_drift")
    if call_indices(rows,"DamageSources.applyDamage:")!=[118] or not (
        rows[118][1]=="invokestatic" and rows[118][3].endswith(")Z")
        and rows[119][1]=="ifeq" and branch_target(rows,119)==145
    ):return fail("boolean_damage_call_to_false_skip_not_proved")
    if call_indices(rows,".addEffect:")!=[132] or call_indices(rows,".push:")!=[138]:
        return fail("effect_or_push_call_count_drift")
    if not (rows[123][1]=="getstatic"
        and re.search(r"Field net/minecraft/world/effect/MobEffects\.WITHER:",rows[123][3])
        and rows[131][1]=="invokespecial"
        and 'MobEffectInstance."<init>":' in rows[131][3]
        and rows[132][1]=="invokevirtual"
        and rows[133][1]=="pop"
        and rows[138][1]=="invokevirtual"):
        return fail("wither_instance_and_effect_invocation_chain_unproven")
    if any(rows[i][1].startswith(("if","goto","jsr")) or
           rows[i][1] in ("tableswitch","lookupswitch","ret","wide","jsr_w",
                          "return","ireturn","athrow") for i in range(120,139)):
        return fail("bypass_inside_damage_success_effect_block")
    positions={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    if len(positions)!=279:return fail("ambiguous_jvm_offsets")
    for i,(_,op,arg,_) in enumerate(rows):
        if not op.startswith(("if","goto","jsr")):continue
        target=arg.split(" ",1)[0] if arg else ""
        dest=positions.get(int(target)) if target.isdecimal() else None
        if dest is None:return fail("unrecognized_branch_target")
        if 120<=dest<=138 and not 120<=i<=138:
            return fail("external_control_enters_effect_without_damage_success")
    if not (rows[143][1]=="ifeq" and branch_target(rows,143)==145 and
            rows[144][1]=="iinc" and rows[145][1]=="goto"
            and branch_target(rows,145)==34):
        return fail("post_effect_loop_branch_unproven")
    return {
        "status":"PROVED_WAVE_BUD_DAMAGE_TRUE_PATH_REACHES_WITHER_AND_PUSH_CALLS",
        "instruction_count":279,
        "damage_call_index":118,"damage_return_type":"boolean",
        "damage_false_branch_index":119,"damage_false_branch_target_index":145,
        "wither_field_index":123,"effect_constructor_index":131,
        "add_effect_index":132,"add_effect_return_discarded":True,
        "push_index":138,"post_effect_branch_index":143,
        "post_effect_skip_index":145,"loop_back_index":34,
        "effect_region_has_external_ingress":False,
        "boundary":"Conditional callsites only; neither damage amount, effect success, push magnitude, target roles, hit dedup nor perk API proved",
    }

def certify_exact_damage_effect_gate_109(proof):
    expected={
        "status":"PROVED_WAVE_BUD_DAMAGE_TRUE_PATH_REACHES_WITHER_AND_PUSH_CALLS",
        "instruction_count":279,
        "damage_call_index":118,"damage_return_type":"boolean",
        "damage_false_branch_index":119,"damage_false_branch_target_index":145,
        "wither_field_index":123,"effect_constructor_index":131,
        "add_effect_index":132,"add_effect_return_discarded":True,
        "push_index":138,"post_effect_branch_index":143,
        "post_effect_skip_index":145,"loop_back_index":34,
        "effect_region_has_external_ingress":False,
        "boundary":"Conditional callsites only; neither damage amount, effect success, push magnitude, target roles, hit dedup nor perk API proved",
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("Somake 1.0.9 bud damage-result/Wither/push CFG fingerprint drift")

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
    gated=certify_damage_success_effect_path(d)
    print("SOMAKE_BUD_DAMAGE_EFFECT_GATE_PROOF",json.dumps(gated,sort_keys=True))
    certify_exact_damage_effect_gate_109(gated)
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:
        raise GateError("JAR changed during inspection")
    return {"status":"SHA_EXACT_BUD_DAMAGE_BRANCH_SCOUT","sha1":digest,
            "version":"1.0.9","mod_id":"somakespells","damage_flow":proof,
            "damage_effect_gate":gated,
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
    print("SOMAKE_BUD_DAMAGE_EFFECT_GATE", "PASS_SHA_EXACT_BOOLEAN_DAMAGE_WITHER_AND_PUSH")
if __name__=="__main__":
    main()
