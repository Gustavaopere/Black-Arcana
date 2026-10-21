#!/usr/bin/env python3
"""Somake Blood Cut 1.0.9 Post-event callsite investigation.

Clean-room method signatures and bounded opcode coordinates only. Call order
does not prove operand origins: those need a separate JVM stack dataflow gate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_blood_cut_cfg import EFFECT_CLASS, EVENT, EVENT_DESCRIPTOR, graph_paths
from somake_109_blood_cut_event_gate import inspect as certify_annotations
from somake_109_radius_irons_contract import sections, opcode_rows

MODIFIER_DESC="(ILnet/minecraft/world/entity/LivingEntity;)F"
SOURCE_DESC="()Lnet/minecraft/world/entity/Entity;"
AMP_DESC="()I"
APPLY_MEMBER="DamageSources.applyDamage:"
NEW_DAMAGE_MEMBER="LivingDamageEvent$Post.getNewDamage:"


def examine_event_callsite(rows: list[tuple[int,str,str,str]]) -> dict:
    if not 5 <= len(rows) <= 200:
        raise GateError("unbounded event instruction count")
    offsets=[r[0] for r in rows]
    if offsets!=sorted(set(offsets)):
        raise GateError("invalid native method instruction order")
    def refs(member):
        return [(i,c) for i,(_,op,_,c) in enumerate(rows)
                if op.startswith("invoke") and member in c]
    modifiers=refs("getDamageModifier:")
    amps=refs("MobEffectInstance.getAmplifier:")
    sources=refs("DamageSource.getEntity:")
    damage=refs(APPLY_MEMBER)
    new_damage=refs(NEW_DAMAGE_MEMBER)
    if len(modifiers)!=1 or len(amps)!=1 or not 1<=len(sources)<=4 or len(damage)!=1:
        raise GateError("ambiguous/missing typed Blood Cut event callsite")
    if len(new_damage)>1:
        raise GateError("ambiguous original damage read")
    mod_i,mod_ref=modifiers[0]
    if MODIFIER_DESC not in mod_ref or re.search(r"getDamageModifier:\(",mod_ref) is None:
        raise GateError("modifier JVM method descriptor changed")
    if not all(AMP_DESC in c for _,c in amps) or not all(SOURCE_DESC in c for _,c in sources):
        raise GateError("amplifier/source typed descriptor changed")
    if not (amps[0][0] < mod_i and min(i for i,_ in sources) < mod_i
            and mod_i < damage[0][0]):
        raise GateError("unexpected provider callsite ordering")
    # Deliberately export only bounded opcode kinds, no byte offsets,
    # method bodies or constant-pool arguments.
    prior=[r[1] for r in rows[max(0,mod_i-10):mod_i]]
    after=[r[1] for r in rows[mod_i+1:mod_i+5]]
    return {
        "assurance":"STATIC_CALLSITES_ONLY",
        "instruction_count":len(rows),
        "modifier_call_index":mod_i,
        "modifier_calls":len(modifiers),
        "amplifier_reads":len(amps),
        "amplifier_call_indices":[i for i,_ in amps],
        "source_entity_reads":len(sources),
        "source_entity_call_indices":[i for i,_ in sources],
        "secondary_damage_call_indices":[i for i,_ in damage],
        "event_damage_read_indices":[i for i,_ in new_damage],
        "preceding_modifier_opcode_kinds":prior,
        "following_modifier_opcode_kinds":after,
        "entry_opcode_kinds":[r[1] for r in rows[:15]],
        "slot1_store_instruction_indices":[i for i,(_,op,arg,_) in enumerate(rows) if op=="astore_1" or (op=="astore" and arg.strip()=="1")],
        "limitations":"Call ordering and local opcode mnemonics are not typed stack provenance; no claim of amplifier/entity mapping, event guard truth, or applied damage."
    }



def certify_native_damage_expression(rows):
    """Certify one uninterrupted eight-op typed stack segment, not game damage."""
    sites=[i for i,(_,op,_,c) in enumerate(rows)
           if op.startswith("invoke") and "getDamageModifier:" in c]
    if len(sites)!=1:
        raise GateError("missing/ambiguous Blood Cut modifier call")
    mod_i=sites[0]
    if mod_i<5 or mod_i+2>=len(rows):
        raise GateError("not enough instructions around native modifier")
    segment=rows[mod_i-5:mod_i+3]
    opcodes=[op for _,op,_,_ in segment]
    expected=["aload_0","invokevirtual","aload_2","invokevirtual",
              "aload_1","invokestatic","fmul","fstore_3"]
    if opcodes!=expected:
        raise GateError("native event × modifier JVM float stack sequence drift")
    get_new=segment[1][3]
    get_amp=segment[3][3]
    get_mod=segment[5][3]
    if (NEW_DAMAGE_MEMBER not in get_new or "getNewDamage:()F" not in get_new
            or "MobEffectInstance.getAmplifier:()I" not in get_amp
            or "getDamageModifier:"+MODIFIER_DESC not in get_mod):
        raise GateError("typed event/modifier operand call changed")
    inside={pc for pc,_,_,_ in segment[1:]}
    # No non-fallthrough branch may jump into the middle of this expression.
    for i,(_,op,arg,_) in enumerate(rows):
        if not op.startswith(("if","goto")):
            continue
        if not re.fullmatch(r"\d+",arg.strip()):
            raise GateError("unsupported branch argument")
        if int(arg.strip()) in inside:
            raise GateError("branch into native float operand sequence")
    return {
        "assurance":"DIRECT_TYPED_FLOAT_HANDOFF",
        "modifier_call_index":mod_i,
        "source_damage_read_index":mod_i-4,
        "effect_amplifier_read_index":mod_i-2,
        "result_store_opcode":"fstore_3",
        "return_expression":"event.getNewDamage * getDamageModifier(effect.getAmplifier,local_1)",
        "limits":"This local_1 load has its source established by the independent source-actor gate; this expression alone does not prove final damage, all branch predicates or complete recursion safety."
    }



def certify_native_source_actor(rows):
    """Verify event damage source entity is guarded and cast to LivingEntity local_1."""
    if len(rows)<11:
        raise GateError("native entry method too short")
    entry=rows[:10]
    expected=["aload_0","invokevirtual","invokevirtual","astore_2",
              "aload_2","instanceof","ifeq","aload_2","checkcast","astore_1"]
    if [op for _,op,_,_ in entry]!=expected:
        raise GateError("source entity guarded entry fingerprint drift")
    get_source=entry[1][3]
    get_entity=entry[2][3]
    if ("getSource:()Lnet/minecraft/world/damagesource/DamageSource;" not in get_source
            or "DamageSource.getEntity:()Lnet/minecraft/world/entity/Entity;" not in get_entity):
        raise GateError("damage-source entity JVM descriptor changed")
    guarded_type="class net/minecraft/world/entity/LivingEntity"
    if (guarded_type not in entry[5][3] or guarded_type not in entry[8][3]):
        raise GateError("native source entity guard/cast type changed")
    target=entry[6][2]
    if not re.fullmatch(r"\d+",target):
        raise GateError("invalid source guard branch operand")
    offset_to_index={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    target_i=offset_to_index.get(int(target))
    if target_i is None or rows[target_i][1]!="return":
        raise GateError("source guard must fail to a return")
    stores=[i for i,(_,op,arg,_) in enumerate(rows)
            if op=="astore_1" or (op=="astore" and arg.strip()=="1")]
    if stores!=[9]:
        raise GateError("source typed local_1 assigned outside canonical guard")
    return {
        "assurance":"SOURCE_ENTITY_TYPED_LOCAL1",
        "origin":"event.getSource().getEntity()",
        "verified_cast_type":"LivingEntity",
        "source_entity_call_index":2,
        "cast_to_living_index":8,
        "local1_store_index":9,
        "guard_failed_returns_without_downstream_modifier":target_i==len(rows)-1,
        "boundary":"DamageSource.getEntity is not automatically the original spell caster, player, or owner; no runtime event/recursion fact certified."
    }


def certify_effect_holder_receiver(rows):
    """Verify Blood Cut effect lookup on typed source entity and null-effect guard."""
    getters=[i for i,(_,op,_,c) in enumerate(rows)
             if op.startswith("invoke") and "LivingEntity.getEffect:" in c]
    if len(getters)!=1:
        raise GateError("missing/ambiguous native LivingEntity effect getter")
    g=getters[0]
    if g<2 or g+3>=len(rows):
        raise GateError("not enough JVM instructions around effect getter")
    expected=["aload_1","getstatic","invokevirtual","astore_2","aload_2","ifnull"]
    opcodes=[op for _,op,_,_ in rows[g-2:g+4]]
    if opcodes!=expected:
        raise GateError("Blood Cut native effect source/guard opcode sequence drift")
    if ("ModMobEffects.BLOOD_CUT:" not in rows[g-1][3]
            or "getEffect:" not in rows[g][3]
            or "Lnet/minecraft/world/effect/MobEffectInstance;" not in rows[g][3]):
        raise GateError("native Blood Cut effect registry/getter descriptor drift")
    target=rows[g+3][2]
    offset_to_index={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    if not re.fullmatch(r"\d+",target) or int(target) not in offset_to_index:
        raise GateError("invalid null-effect guard target")
    if rows[offset_to_index[int(target)]][1]!="return":
        raise GateError("missing effect must lead to a normal return")
    amplifiers=[i for i,(_,op,_,c) in enumerate(rows)
                if op.startswith("invoke") and "MobEffectInstance.getAmplifier:()I" in c]
    if len(amplifiers)!=1 or amplifiers[0]<=g+3:
        raise GateError("effect amplifier source missing/ambiguous")
    amp=amplifiers[0]
    if rows[amp-1][1]!="aload_2":
        raise GateError("effect amplifier receiver must be guarded local_2")
    for index,(_,op,arg,_) in enumerate(rows[g+1:amp],start=g+1):
        if op=="astore_2" and index != g+1:
            raise GateError("intervening effect local_2 overwrite")
        if op=="astore" and arg.strip()=="2":
            raise GateError("intervening effect local_2 overwrite")
    return {
        "assurance":"BLOOD_CUT_FROM_SOURCE_ENTITY",
        "effect_receiver_local":"local_1",
        "effect_storage_local":"local_2",
        "verified_effect_id":"BLOOD_CUT",
        "effect_lookup_index":g,
        "null_effect_guard_index":g+3,
        "amplifier_receiver_verified":"local_2",
        "boundary":"Native getter obtains Blood Cut effect from the damage source LivingEntity, not necessarily the original caster. Event dispatch, proc eligibility and actual damage remain unproven."
    }


def certify_early_post_damage_exclusion(rows):
    """Report only the type gate and branch direction of a bounded early check."""
    if len(rows)<16:
        raise GateError("early Post-event guard not inspectable")
    part=rows[10:16]
    if [op for _,op,_,_ in part[:5]]!=[
        "aload_0","invokevirtual","instanceof","ifeq","return"]:
        raise GateError("native early event type guard changed")
    if "getSource:" not in part[1][3]:
        raise GateError("guarded early event source getter missing")
    matched=re.search(r"\bclass\s+([A-Za-z0-9_/$.]+)",part[2][3])
    if not matched:
        raise GateError("missing typed instanceof class token")
    t=part[3][2].strip()
    if not re.fullmatch(r"\d+",t) or int(t)!=part[5][0]:
        raise GateError("unexpected early exclusion fallthrough target")
    return {
      "assurance":"EXACT_EARLY_INSTANCEOF_RETURN_BRANCH",
      "guarded_getter":"event.getSource()",
      "excluded_class_internal_name":matched.group(1),
      "on_instanceof_true":"return before Blood Cut modifier and secondary damage",
      "on_instanceof_false":"continue at next native Post-event block",
      "boundary":"This source-type exclusion is proved only as compiled branch logic; it does not prove all recursion modes, event routing or actual damage."
    }


def inspect(jar:Path) -> dict:
    jar=Path(jar)
    if jar.name!=FILENAME or jar.is_symlink() or not jar.is_file():
        raise GateError("invalid exact artifact path")
    old=certify_annotations(jar)
    if old["artifact_sha1"]!=SHA1:raise GateError("event declaration identity drift")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),EFFECT_CLASS],
                     capture_output=True,text=True,timeout=40,check=False)
    if p.returncode or not 100<len(p.stdout)<1_500_000:
        raise GateError("javap bounded Blood Cut event inspection failed")
    found=[opcode_rows(body) for n,d,body in sections(p.stdout)
           if n==EVENT and d==EVENT_DESCRIPTOR]
    if len(found)!=1:
        raise GateError("Blood Cut typed Post handler missing/ambiguous")
    graph=graph_paths(found[0],expected_branches=5)
    result=examine_event_callsite(found[0])
    direct_float=certify_native_damage_expression(found[0])
    source_actor=certify_native_source_actor(found[0])
    effect_holder=certify_effect_holder_receiver(found[0])
    early_guard=certify_early_post_damage_exclusion(found[0])
    if len(found[0])!=103 or graph["syntactic_paths_to_apply"]!=2 or graph["syntactic_paths_without_apply"]!=3:
        raise GateError("Blood Cut native event CFG changed")
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError("JAR mutated during read")
    return {"status":"PASS_SHA_EXACT_BLOOD_CUT_SOURCE_EFFECT_FLOAT_AND_SPELL_SOURCE_EXCLUSION",
            "provider":"somakespells","version":"1.0.9","sha1":SHA1,
            "event":"BloodCutEffect.onLivingDamage(LivingDamageEvent.Post)",
            "callsite_evidence":result,
            "direct_float_stack_handoff":direct_float,
            "source_actor_provenance":source_actor,
            "effect_holder_provenance":effect_holder,
            "early_type_exclusion":early_guard,
            "limits":"Source LivingEntity, Blood Cut effect owner, amplifier, typed float product and SpellDamageSource exclusion proven statically; no live event dispatch, final damage, full recursion closure or per-player perk hook verified."}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    evidence=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(evidence,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("BLOOD_CUT_EVENT_CALLSITES",evidence["status"],evidence["sha1"])
    print("BLOOD_CUT_ARG_PROXIMITY",json.dumps(evidence["callsite_evidence"],sort_keys=True))
    print("BLOOD_CUT_FLOAT_HANDOFF",json.dumps(evidence["direct_float_stack_handoff"],sort_keys=True))
    print("BLOOD_CUT_SOURCE_ACTOR",json.dumps(evidence["source_actor_provenance"],sort_keys=True))
    print("BLOOD_CUT_EFFECT_OWNER",json.dumps(evidence["effect_holder_provenance"],sort_keys=True))
    print("BLOOD_CUT_EARLY_EXCLUSION",json.dumps(evidence["early_type_exclusion"],sort_keys=True))


if __name__=="__main__":
    main()
