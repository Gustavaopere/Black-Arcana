#!/usr/bin/env python3
"""Bounded clean-room operand/provenance scout for Somake 1.0.9 bud impact.

Only emits derived JVM types, operand local indices, bounded literal values and
method/field identifiers, never provider code, bytecode, classfiles or JARs.
No inferred caster/target roles or mutation hook claims.
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
    CLASS, DESC, prove_impact_box_and_query, certify_exact_impact_geometry_109,
)
from somake_109_bud_impact_damage_gates import (
    certify_damage_success_effect_path, certify_exact_damage_effect_gate_109,
    certify_heal_guard_and_event_path, certify_exact_heal_event_gate_109,
)

RANGES=((0,32),(32,62),(62,89),(89,120),(120,144),(144,173))
MAX_BODY=1_400_000

def classify_comment(op,comment):
    if op in ("getfield","getstatic","putfield","putstatic"):
        m=re.search(r"\bField (?:[\w/$]+\.)?([\w$]+):",comment)
        return {"kind":"field","name":m.group(1)[:70] if m else "unknown"}
    if op.startswith("invoke"):
        m=re.search(r"(?:Method|InterfaceMethod) (?:[\w/$]+\.)?([\w$<>]+):(\([^ ]*\).*)$",comment)
        if m:
            name=m.group(1).replace('"',"")[:70]
            descriptor=m.group(2)
            return {"kind":"call","name":name,"descriptor":descriptor[:130]}
        return {"kind":"call","name":"unknown"}
    if op in ("instanceof","checkcast","new"):
        m=re.search(r"\bclass ([\w/$]+)",comment)
        return {"kind":"class","type":m.group(1)[:115] if m else "unknown"}
    if op.startswith(("ldc","bipush","sipush")):
        m=re.search(r"\b(?:double|float|int|long) (-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)[dfl]?\b",comment)
        return {"kind":"literal","value":m.group(1)} if m else {"kind":"literal","value":"symbolic"}
    return {}

def describe_instruction(rows,index):
    _,op,operand,comment=rows[index]
    out={"i":index,"op":op}
    if re.fullmatch(r"[afid](?:load|store)_[0-9]+",op):
        out["slot"]=int(op[-1])
    elif op in ("aload","astore","fload","fstore","iload","istore","dload","dstore"):
        if not operand.isdecimal():raise ValueError("non_numeric_local")
        out["slot"]=int(operand)
    elif op=="iinc":
        m=re.fullmatch(r"(\d+),\s*(-?\d+)",operand)
        if not m:raise ValueError("invalid_increment")
        out["slot"]=int(m.group(1))
        out["increment"]=int(m.group(2))
    elif op in ("bipush","sipush") and operand.lstrip("-").isdecimal():
        out["immediate"]=int(operand)
    out.update(classify_comment(op,comment))
    return out

def scout(declared):
    matches=[body for name,desc,body in declared if name=="impact" and desc==DESC]
    if len(matches)!=1:return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_impact"}
    rows=opcode_rows(matches[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"physical_shape_drift"}
    try:
        samples=[
            {"range":f"{a}:{b}","ops":[describe_instruction(rows,i) for i in range(a,b)]}
            for a,b in RANGES
        ]
    except ValueError as exc:
        return {"status":"NOT_PROVED","reason":str(exc)}
    return {
        "status":"OBSERVED_TYPED_OPERAND_WINDOWS_ONLY",
        "instruction_count":279,
        "ranges":samples,
        "boundary":"Derived JVM operand windows only. Slot roles, Wither parameters, push, healing formula and hook availability NOT_PROVED",
    }


def operand_contract(declared):
    """Exact 1.0.9 native owner, pre-existing Wither, impulse, and heal formula.

    Source-pin only local deterministic call/branch arithmetic. Never claim a
    successful damage, event delivery, entity movement, healed HP or perk seam.
    """
    found=[b for n,d,b in declared if n=="impact" and d==DESC]
    if len(found)!=1:return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_impact"}
    rows=opcode_rows(found[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"wrong_release_shape"}
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    def op(i,v):return rows[i][1]==v
    def local(i,kind,slot):
        return op(i,f"{kind}_{slot}") or (op(i,kind) and rows[i][2]==str(slot))
    def member(i,name,desc):
        tag=classify_comment(rows[i][1],rows[i][3])
        return tag.get("kind")=="call" and tag.get("name")==name and tag.get("descriptor")==desc
    def field(i,name):
        tag=classify_comment(rows[i][1],rows[i][3])
        return tag.get("kind")=="field" and tag.get("name")==name
    def exact_float(i,val):
        m=re.search(r"\bfloat\s+([-+]?\d+(?:\.\d+)?)(?:f)?\b",rows[i][3])
        return op(i,"ldc_w") and m is not None and float(m.group(1))==val
    def exact_double(i,val):
        m=re.search(r"\bdouble\s+([-+]?\d+(?:\.\d+)?)(?:d)?\b",rows[i][3])
        return op(i,"ldc2_w") and m is not None and float(m.group(1))==val
    pcs={pc:j for j,(pc,_,_,_) in enumerate(rows)}
    def jump(i):
        t=rows[i][2].split(" ",1)[0]
        return pcs.get(int(t)) if t.isdecimal() else None
    owner=(
        local(3,"aload",0)
        and member(4,"getOwner","()Lnet/minecraft/world/entity/Entity;")
        and local(5,"astore",3)
        and local(6,"aload",3)
        and op(7,"instanceof")
        and "class net/minecraft/world/entity/LivingEntity" in rows[7][3]
        and op(8,"ifeq") and jump(8)==14
        and local(9,"aload",3) and op(10,"checkcast")
        and "class net/minecraft/world/entity/LivingEntity" in rows[10][3]
        and local(11,"astore",5)
        and local(12,"aload",5) and op(13,"goto") and jump(13)==15
        and op(14,"aconst_null") and local(15,"astore",4)
    )
    if not owner:return fail("owner_to_nullable_living_local4_not_exact")
    # A bypassing jump into the conditional increment would invalidate its
    # provenance even when the immediate instructions still look correct.
    for i,(_,branch_op,operand,_) in enumerate(rows):
        if not branch_op.startswith(("if","goto","jsr")):continue
        dest=operand.split(" ",1)[0] if operand else ""
        target=pcs.get(int(dest)) if dest.isdecimal() else None
        if target is None:return fail("non_numeric_or_missing_branch_target")
        if target==144:return fail("alternate_ingress_into_preexisting_wither_counter")
    if not local(101,"aload",8):
        return fail("preexisting_wither_receiver_not_same_victim")
    counter=(
        op(26,"iconst_0") and local(27,"istore",6)
        and field(102,"WITHER") and member(103,"hasEffect","(Lnet/minecraft/core/Holder;)Z")
        and local(104,"istore",14)
        and local(142,"iload",14) and op(143,"ifeq") and jump(143)==145
        and op(144,"iinc") and rows[144][2].replace(" ","")=="6,1"
    )
    if not counter:return fail("existing_wither_boolean_and_counter_increment_not_exact")
    damage=(member(118,"applyDamage","(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z")
           and op(119,"ifeq") and jump(119)==145)
    if not damage:return fail("damage_success_enclosing_increment_not_exact")
    params=(
        field(123,"WITHER") and local(124,"aload",0)
        and op(125,"getfield") and field(125,"witherDuration")
        and local(126,"aload",0) and op(127,"getfield") and field(127,"witherAmplifier")
        and [rows[i][1] for i in (128,129,130)]==["iconst_0","iconst_1","iconst_1"]
        and op(131,"invokespecial") and 'MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V' in rows[131][3]
        and member(132,"addEffect","(Lnet/minecraft/world/effect/MobEffectInstance;)Z")
    )
    if not params:return fail("wither_duration_amplifier_or_flags_drift")
    impulse=(local(134,"aload",8) and op(135,"dconst_0")
             and exact_double(136,0.34) and op(137,"dconst_0")
             and member(138,"push","(DDD)V")
             and local(139,"aload",8) and op(140,"iconst_1")
             and field(141,"hurtMarked") and op(141,"putfield"))
    if not impulse:return fail("vertical_impulse_and_hurt_marking_not_exact")
    heal=(
        local(146,"aload",4) and op(147,"ifnull") and jump(147)==173
        and local(148,"iload",6) and op(149,"ifle") and jump(149)==173
        and exact_float(150,3.75) and exact_float(151,1.25)
        and local(152,"iload",6) and op(153,"i2f") and op(154,"fmul")
        and member(155,"min","(FF)F") and local(156,"fstore",7)
        and local(170,"aload",4) and local(171,"fload",7)
        and member(172,"heal","(F)V")
    )
    if not heal:return fail("float_heal_capped_counter_formula_not_exact")
    return {
        "status":"PROVED_BUD_OWNER_PREEXISTING_WITHER_COUNTER_AND_CAPPED_HEAL_INPUT",
        "owner_source":"bud.getOwner():Entity",
        "owner_local":3,"conditional_living_owner_local":4,
        "owner_guard_type":"LivingEntity","owner_nonliving_fallback":"null",
        "counter_local":6,"counter_initial":0,
        "counter_condition":"applyDamage_true_AND_victim_had_WITHER_before_damage",
        "preexisting_wither_boolean_local":14,
        "wither_duration_field":"witherDuration:int",
        "wither_amplifier_field":"witherAmplifier:int",
        "wither_flags":["false","true","true"],
        "push_receiver_local":8,"push_vector_xyz":[0.0,0.34,0.0],
        "push_marks_hurtMarked":True,
        "heal_formula":"min_f32(3.75f,1.25f*float32(counter_local6))",
        "heal_receiver_local":4,"heal_amount_local":7,
        "boundary":"No healing result, effective damage, caster/player identity, underlying event cancellation or hook per player proved",
    }

def certify_exact_bud_operand_contract_109(proof):
    expected={
        "status":"PROVED_BUD_OWNER_PREEXISTING_WITHER_COUNTER_AND_CAPPED_HEAL_INPUT",
        "owner_source":"bud.getOwner():Entity",
        "owner_local":3,"conditional_living_owner_local":4,
        "owner_guard_type":"LivingEntity","owner_nonliving_fallback":"null",
        "counter_local":6,"counter_initial":0,
        "counter_condition":"applyDamage_true_AND_victim_had_WITHER_before_damage",
        "preexisting_wither_boolean_local":14,
        "wither_duration_field":"witherDuration:int",
        "wither_amplifier_field":"witherAmplifier:int",
        "wither_flags":["false","true","true"],
        "push_receiver_local":8,"push_vector_xyz":[0.0,0.34,0.0],
        "push_marks_hurtMarked":True,
        "heal_formula":"min_f32(3.75f,1.25f*float32(counter_local6))",
        "heal_receiver_local":4,"heal_amount_local":7,
        "boundary":"No healing result, effective damage, caster/player identity, underlying event cancellation or hook per player proved",
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("Somake 1.0.9 impact native owner/status/impulse/heal fingerprint drift")

def inspect(jar:Path):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("Somake JAR identity/size mismatch")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("Somake JAR SHA-1 mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or CLASS.replace(".","/")+".class" not in names:
            raise GateError("ZIP duplication or expected class absent")
        mods=z.read("META-INF/neoforge.mods.toml")
        if len(mods)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",mods):
            raise GateError("unexpected mod ID")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
                     capture_output=True,text=True,timeout=60,check=False)
    if p.returncode or not p.stdout or len(p.stdout)>MAX_BODY:
        raise GateError("javap failed or exceeded bound")
    methods=sections(p.stdout)
    certify_exact_impact_geometry_109(prove_impact_box_and_query(methods))
    certify_exact_damage_effect_gate_109(certify_damage_success_effect_path(methods))
    certify_exact_heal_event_gate_109(certify_heal_guard_and_event_path(methods))
    evidence=scout(methods)
    contract=operand_contract(methods)
    print("SOMAKE_BUD_PROVENANCE_PROOF",json.dumps(contract,sort_keys=True))
    certify_exact_bud_operand_contract_109(contract)
    if evidence["status"]!="OBSERVED_TYPED_OPERAND_WINDOWS_ONLY":
        raise GateError("operand scouting failed")
    return {"sha1":digest,"version":"1.0.9","mod_id":"somakespells",
            "scout":evidence,"source_pinned_contract":contract,"boundary":"Read-only native compiled observation, NOT provider runtime/behavior"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    args=a.parse_args()
    proof=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(proof,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_BUD_OPERAND_SCOUT",json.dumps(proof["scout"],sort_keys=True))
    print("SOMAKE_BUD_OPERAND_SHA",proof["sha1"])
    print("SOMAKE_BUD_PROVENANCE_GATE", "PASS_SHA_EXACT_OWNER_WITHER_COUNTER_IMPULSE_AND_HEAL")

if __name__=="__main__":
    main()
