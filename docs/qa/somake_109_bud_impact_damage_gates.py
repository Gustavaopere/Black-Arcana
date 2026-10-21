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


def heal_conditional_scout(declared):
    m=[b for n,d,b in declared if n=="impact" and d==DESC]
    if len(m)!=1:return {"status":"NOT_PROVED","reason":"ambiguous_impact"}
    rows=opcode_rows(m[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"impact_drift"}
    return {
        "status":"OBSERVED_HEAL_COSITES_ONLY",
        "guard_147":{"opcode":rows[147][1],"target_index":branch_target(rows,147)},
        "guard_149":{"opcode":rows[149][1],"target_index":branch_target(rows,149)},
        "selected_operand_producers":[
            {"index":i,"op":rows[i][1],
             "local":rows[i][2] if rows[i][1] in ("aload","fload","iload","dload") else (
                rows[i][1][-1] if re.fullmatch(r"[afid]load_[0-9]",rows[i][1]) else None)}
            for i in (146,148,150,151,164,165,166,169,170,171)
        ],
        "calls":{
            "event_ctor":call_indices(rows,'SpellHealEvent."<init>":'),
            "event_post":call_indices(rows,".post:"),
            "heal":call_indices(rows,".heal:")
        },
        "post_event_branch_indices":[
            {"index":i,"opcode":rows[i][1],"target_index":branch_target(rows,i)}
            for i in range(146,173) if rows[i][1].startswith(("if","goto"))
        ],
        "boundary":"Only method/branch shapes; heal amount and event validity NOT proved",
    }


def certify_heal_guard_and_event_path(declared):
    """Prove only JVM branch gate, event post and heal call; no healing outcome."""
    members=[b for n,d,b in declared if n=="impact" and d==DESC]
    if len(members)!=1:return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_impact"}
    rows=opcode_rows(members[0])
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=279:return fail("release_impact_instruction_count_drift")
    def local(i,op,slot):
        a,operation,operand,comment=rows[i]
        return operation==op+"_"+str(slot) or (operation==op and operand==str(slot))
    if not (local(146,"aload",4) and rows[147][1]=="ifnull"
            and branch_target(rows,147)==173
            and local(148,"iload",6) and rows[149][1]=="ifle"
            and branch_target(rows,149)==173):
        return fail("nullable_object_and_positive_int_guard_not_exact")
    if call_indices(rows,'SpellHealEvent."<init>":')!=[167]:
        return fail("unique_spell_heal_event_constructor_not_proved")
    if call_indices(rows,".post:")!=[168] or rows[168][1] not in ("invokevirtual","invokeinterface"):
        return fail("event_bus_post_not_proved")
    if not (rows[169][1]=="pop" and local(170,"aload",4)
            and local(171,"fload",7) and rows[172][1]=="invokevirtual"
            and "LivingEntity.heal:(F)V" in rows[172][3]
            and call_indices(rows,".heal:")==[172]):
        return fail("post_ignored_and_heal_target_amount_not_proved")
    for i in range(150,173):
        op=rows[i][1]
        if op.startswith(("if","goto","jsr")) or op in (
            "tableswitch","lookupswitch","ret","jsr_w","wide","return","athrow"):
            return fail("branch_in_heal_region")
    pcs={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    if len(pcs)!=279:return fail("ambiguous_offsets")
    for i,(pc,op,operand,_) in enumerate(rows):
        if not op.startswith(("if","goto","jsr")):continue
        raw=operand.split(" ",1)[0] if operand else ""
        dest=pcs.get(int(raw)) if raw.isdecimal() else None
        if dest is None:return fail("unrecognized_branch")
        if 150<=dest<=172 and not 150<=i<=172:
            return fail("outside_jump_into_heal_region")
    return {
        "status":"PROVED_BUD_HEAL_GUARDED_EVENT_POST_THEN_HEAL_CALL",
        "instruction_count":279,
        "nullable_receiver_slot":4,"guard_ifnull_index":147,"guard_ifnull_skip_index":173,
        "positive_integer_slot":6,"guard_ifle_index":149,"guard_ifle_skip_index":173,
        "event_constructor_index":167,"event_post_index":168,
        "event_post_return_discarded":True,
        "heal_receiver_slot":4,"heal_amount_float_slot":7,"heal_call_index":172,
        "healing_region_external_ingress":False,
        "boundary":"Event and heal calls on normal guarded path only; no true healing amount, cancellation semantics, damage-to-heal attribution, PvP, player role, double-processing or perk hook proved",
    }

def certify_exact_heal_event_gate_109(proof):
    expected={
        "status":"PROVED_BUD_HEAL_GUARDED_EVENT_POST_THEN_HEAL_CALL",
        "instruction_count":279,
        "nullable_receiver_slot":4,"guard_ifnull_index":147,"guard_ifnull_skip_index":173,
        "positive_integer_slot":6,"guard_ifle_index":149,"guard_ifle_skip_index":173,
        "event_constructor_index":167,"event_post_index":168,
        "event_post_return_discarded":True,
        "heal_receiver_slot":4,"heal_amount_float_slot":7,"heal_call_index":172,
        "healing_region_external_ingress":False,
        "boundary":"Event and heal calls on normal guarded path only; no true healing amount, cancellation semantics, damage-to-heal attribution, PvP, player role, double-processing or perk hook proved",
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("Somake 1.0.9 healing gate/SpellHealEvent/target/amount fingerprint drift")

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
    heal_scout=heal_conditional_scout(d)
    print("SOMAKE_BUD_HEAL_GUARD_SCOUT",json.dumps(heal_scout,sort_keys=True))
    heal_gate=certify_heal_guard_and_event_path(d)
    print("SOMAKE_BUD_HEAL_EVENT_GATE_PROOF",json.dumps(heal_gate,sort_keys=True))
    certify_exact_heal_event_gate_109(heal_gate)
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:
        raise GateError("JAR changed during inspection")
    return {"status":"SHA_EXACT_BUD_DAMAGE_BRANCH_SCOUT","sha1":digest,
            "version":"1.0.9","mod_id":"somakespells","damage_flow":proof,
            "damage_effect_gate":gated,"heal_scout":heal_scout,"heal_gate":heal_gate,
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
    print("SOMAKE_BUD_HEAL_EVENT_GATE", "PASS_SHA_EXACT_NONNULL_POSITIVE_COUNTER_POST_THEN_HEAL")
if __name__=="__main__":
    main()
