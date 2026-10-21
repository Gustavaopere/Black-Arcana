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
        "limitations":"Call ordering and local opcode mnemonics are not typed stack provenance; no claim of amplifier/entity mapping, event guard truth, or applied damage."
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
    if len(found[0])!=103 or graph["syntactic_paths_to_apply"]!=2 or graph["syntactic_paths_without_apply"]!=3:
        raise GateError("Blood Cut native event CFG changed")
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError("JAR mutated during read")
    return {"status":"PASS_SHA_EXACT_BLOOD_CUT_TYPED_EVENT_CALLSITE_ORDER_ONLY",
            "provider":"somakespells","version":"1.0.9","sha1":SHA1,
            "event":"BloodCutEffect.onLivingDamage(LivingDamageEvent.Post)",
            "callsite_evidence":result,
            "limits":"No producer-consumer typed stack proof yet; no gameplay, host settlement, recursion or perk hook verified."}


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


if __name__=="__main__":
    main()
