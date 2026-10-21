#!/usr/bin/env python3
"""Somake Blood Cut 1.0.9: fail-closed, SHA-exact JVM branch topology.

Exports only derived CFG path counts, guard locations, and bounded numeric/member
fingerprints; it never exports publisher classfiles, method bodies or assets.
Static reachability is NOT runtime branch truth, damage frequency or proc safety.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_blood_cut_event_gate import inspect as certify_annotations

EVENT = "onLivingDamage"
EVENT_DESCRIPTOR = "(Lnet/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post;)V"
MODIFIER = "getDamageModifier"
MODIFIER_DESCRIPTOR = "(ILnet/minecraft/world/entity/LivingEntity;)F"
EFFECT_CLASS = "com.somake.somakespells.effect.blood.BloodCutEffect"
DAMAGE_MEMBER = "io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:"
INPUT_MEMBER = "LivingDamageEvent$Post.getNewDamage:"
MAX_PATHS = 4096


def graph_paths(rows: list[tuple[int, str, str, str]], *, expected_branches: int | None = None) -> dict:
    """Enumerate bounded *syntactic* normal-control paths, with JVM-PC target checks."""
    if not 2 <= len(rows) <= 300:
        raise GateError("unbounded JVM instruction set")
    pcs = [r[0] for r in rows]
    if pcs != sorted(set(pcs)):
        raise GateError("duplicate/unordered JVM instruction PC")
    locations = {pc:i for i,pc in enumerate(pcs)}
    graph = {}
    branches = []
    terminators = set()
    damage_sites = []
    read_sites = []
    for i,(pc,op,operand,comment) in enumerate(rows):
        if op in ("tableswitch","lookupswitch","jsr","jsr_w","ret","wide"):
            raise GateError("unsupported JVM control flow")
        if op.startswith("invoke") and DAMAGE_MEMBER in comment:
            damage_sites.append(i)
        if op.startswith("invoke") and INPUT_MEMBER in comment:
            read_sites.append(i)
        next_index = i+1 if i+1 < len(rows) else None
        if op.startswith(("if","goto")):
            match = re.fullmatch(r"\d+",operand.strip())
            if not match:
                raise GateError("invalid branch operand")
            target_pc = int(match.group())
            if target_pc not in locations:
                raise GateError("branch target does not match JVM instruction")
            target = locations[target_pc]
            if target <= i:
                raise GateError("backedge requires separate bounded loop analysis")
            conditional = op.startswith("if")
            if conditional and next_index is None:
                raise GateError("conditional at method end")
            destinations = (target,next_index) if conditional else (target,)
            graph[i] = tuple(destinations)
            branches.append({"index":i,"opcode":op,"target_index":target,
                             "fallthrough_index":next_index if conditional else None})
        elif op.endswith("return") or op=="athrow":
            graph[i]=()
            terminators.add(i)
        elif next_index is not None:
            graph[i]=(next_index,)
        else:
            raise GateError("fallthrough after final instruction")
    if expected_branches is not None and len(branches) != expected_branches:
        raise GateError("native branch fingerprint drift")
    if len(damage_sites)!=1 or len(read_sites)!=1:
        raise GateError("missing or ambiguous damage/new-damage event callsite")
    damage = damage_sites[0]
    # Dynamic programming counts syntactic paths in the *acyclic* validated CFG.
    path_counter = {}
    for i in range(len(rows)-1,-1,-1):
        if i in terminators:
            path_counter[i]=(1 if i==damage else 0, 0 if i==damage else 1)
        else:
            hit=0; miss=0
            for dst in graph[i]:
                h,m=path_counter[dst]
                hit+=h
                miss+=m
            if i==damage:
                hit+=miss;miss=0
            if hit+miss>MAX_PATHS:
                raise GateError("too many symbolic paths")
            path_counter[i]=(hit,miss)
    # Reachability restriction: no uncatalogued dead instructions.
    reached={0}; queue=[0]
    while queue:
        index=queue.pop()
        for other in graph[index]:
            if other not in reached:
                reached.add(other);queue.append(other)
    if len(reached)!=len(rows):
        raise GateError("unreachable instructions: fail closed")
    if len(terminators)==0:
        raise GateError("no terminal method return")
    guard_rows=[]
    for branch in branches:
        taken=path_counter[branch["target_index"]]
        follow=(path_counter[branch["fallthrough_index"]]
                if branch["fallthrough_index"] is not None else None)
        guard_rows.append({**branch,
                           "target_paths_to_apply":taken[0],
                           "target_paths_without_apply":taken[1],
                           "fallthrough_paths_to_apply":follow[0] if follow else None,
                           "fallthrough_paths_without_apply":follow[1] if follow else None})
    return {
        "instruction_count":len(rows),
        "branch_count":len(branches),
        "return_sites":len(terminators),
        "get_new_damage_index":read_sites[0],
        "secondary_apply_damage_index":damage,
        "syntactic_paths_to_apply":path_counter[0][0],
        "syntactic_paths_without_apply":path_counter[0][1],
        "branch_outcomes":guard_rows,
        "boundary":"Syntactic CFG paths ignore runtime truth values, exceptions, dynamic dispatch, nested events, and concurrency. Not a safe hook or recursion proof."
    }


def modifier_fingerprint(rows: list[tuple[int,str,str,str]]) -> dict:
    """Numeric operand/operator census, NOT symbolic expression or final multiplier."""
    if len(rows)!=19:
        raise GateError("unexpected modifier compiled instruction count")
    branches=[op for _,op,_,_ in rows if op.startswith(("if","goto"))]
    if len(branches)!=2:
        raise GateError("expected two modifier transfers")
    names=[comment for _,op,_,comment in rows if op.startswith("invoke")]
    if sum("BloodCutSpell.getEntityPowerMultiplier:" in v for v in names)!=1:
        raise GateError("native power multiplier reference drift")
    numeric=[]
    for pc,op,arg,comment in rows:
        if op in ("bipush","sipush") and re.fullmatch(r"-?\d+",arg):
            numeric.append({"kind":"integer","value":int(arg)})
        elif re.fullmatch(r"[ifd]const_[0-5]",op):
            numeric.append({"kind":op[0],"value":int(op[-1])})
        elif op.startswith("ldc"):
            m=re.search(r"\b(float|double|int|long)\s+(-?\d+(?:\.\d+)?)(?:[fdl])?\b",comment)
            if m:
                numeric.append({"kind":m.group(1),"value":m.group(2)})
    return {
       "instruction_count":len(rows),
       "branch_opcodes":branches,
       "numeric_literals":numeric[:12],
       "arithmetic_opcodes":[op for _,op,_,_ in rows if op in
                             ("fmul","fadd","fsub","fdiv","dmul","dadd","dsub","ddiv",
                              "imul","iadd","isub","idiv","i2f","d2f")],
       "terminal_freturns":sum(op=="freturn" for _,op,_,_ in rows),
       "power_multiplier_calls":1,
       "boundary":"Operand census only: cannot infer complete formula, branch truth, level mapping, effect cap, or a safe perk mutation."
    }


def inspect(jar: Path) -> dict:
    prior=certify_annotations(jar)
    if prior["artifact_sha1"]!=SHA1:
        raise GateError("previous event/annotation proof drift")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),EFFECT_CLASS],
                     capture_output=True,text=True,check=False,timeout=40)
    if p.returncode or not 100<len(p.stdout)<1_500_000:
        raise GateError("javap exact BloodCutEffect failed")
    methods=sections(p.stdout)
    selected={}
    for name,desc in ((EVENT,EVENT_DESCRIPTOR),(MODIFIER,MODIFIER_DESCRIPTOR)):
        matches=[opcode_rows(body) for n,d,body in methods if n==name and d==desc]
        if len(matches)!=1:
            raise GateError("missing or ambiguous typed method "+name)
        selected[name]=matches[0]
    event=graph_paths(selected[EVENT],expected_branches=5)
    modifier=modifier_fingerprint(selected[MODIFIER])
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError("artifact changed after inspection")
    return {
       "status":"PASS_SHA_EXACT_BLOOD_CUT_NORMAL_CFG_AND_MODIFIER_OPERANDS_ONLY",
       "provider":"somakespells","version":"1.0.9","sha1":SHA1,
       "effect_class":EFFECT_CLASS,"annotation_gate":"PASS",
       "event":event,"modifier":modifier,
       "limits":["No live event dispatch, actual damage, recursion outcome or per-player hook proved.",
                 "No classfiles, JAR, raw bytecode or method body exported."]
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    if args.jar.name!=FILENAME:
        raise GateError("wrong file")
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_BLOOD_CUT_CFG",result["status"],result["sha1"])
    print("EVENT_GRAPH",json.dumps(result["event"],sort_keys=True))
    print("MODIFIER_NUMERIC",json.dumps(result["modifier"],sort_keys=True))


if __name__=="__main__":
    main()
