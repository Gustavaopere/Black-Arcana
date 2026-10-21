#!/usr/bin/env python3
"""Bounded clean-room interrogation of Somake 1.0.9 isValidTarget final branch.

Only analytical metadata is persisted. Never export vendor instructions/bytecode.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_radius_consumers import (
    native_isvalidtarget_branch_edges,
    native_isvalidtarget_early_guards,
    certify_exact_native_target_cfg_109,
)
from somake_109_native_filter_middle import middle_guard, certify_exact_native_middle_109

CLASS="com.somake.somakespells.entity.FuneralBloomControllerEntity"
DESC="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
METHODS={
    "distance":re.compile(r"^Method net/minecraft/world/entity/(?:LivingEntity|Entity)\.distanceToSqr:\(DDD\)D$"),
    "radius":re.compile(r"^Method (?:(?:com/somake/somakespells/entity/FuneralBloomControllerEntity)\.)?getRadius:\(\)F$"),
    "x":re.compile(r"^Method net/minecraft/world/entity/(?:LivingEntity|Entity)\.getX:\(\)D$"),
    "y":re.compile(r"^Method net/minecraft/world/entity/(?:LivingEntity|Entity)\.getY:\(\)D$"),
    "z":re.compile(r"^Method net/minecraft/world/entity/(?:LivingEntity|Entity)\.getZ:\(\)D$"),
}
def not_proved(reason, **extra):
    return {"status":"NOT_PROVED","reason":reason,**extra}

def method_kind(symbol):
    for kind,pattern in METHODS.items():
        if pattern.fullmatch(symbol):return kind
    # javap may abbreviate the owner on inherited Entity accessors.
    if symbol in ("Method getX:()D","Method getY:()D","Method getZ:()D"):
        return symbol[10].lower()
    return None

def arithmetic_window(declared):
    """Inspect only 19..36 after independently certified early/middle branches.

    A strict symbolic evaluator attempts to prove the last comparison, but a
    structural observation alone MUST NOT certify numeric or gameplay semantics.
    """
    found=[body for name,desc,body in declared if name=="isValidTarget" and desc==DESC]
    if len(found)!=1:return not_proved("exact_native_method_missing_or_ambiguous")
    rows=opcode_rows(found[0])
    if len(rows)!=41:return not_proved("exact_41_instruction_shape_drift")
    if rows[36][1]!="ifgt" or rows[36][2].split(" ",1)[0]!=str(rows[39][0]):
        return not_proved("last_branch_target_or_opcode_changed")
    if rows[39][1]!="iconst_0" or rows[40][1]!="ireturn":
        return not_proved("last_branch_no_longer_immediately_rejects")
    window=rows[19:37]
    kinds=[(idx,method_kind(comment)) for idx,(_,op,_,comment) in enumerate(rows[19:36],start=19)
           if op.startswith("invoke")]
    kind_list=[k for _,k in kinds]
    facts={
        "window_instruction_count":len(window),
        "last_conditional_index":36,
        "false_return_index":39,
        "call_categories":kind_list,
        "call_positions":[{"instruction_index":i,"category":k if k else "unmodeled"}
                          for i,k in kinds],
        "opcode_histogram":dict(sorted(Counter(op for _,op,_,_ in window).items())),
        "math_opcode_histogram":dict(sorted(Counter(op for _,op,_,_ in window
             if op in ("dadd","dsub","dmul","ddiv","fadd","fsub","fmul","fdiv",
                       "f2d","d2f","dcmpg","dcmpl","fcmpl","fcmpg","dup2")).items())),
        "boundary":"No actual player roles, targeting/perk API, world-space hitbox or gameplay accepted",
    }
    if kind_list.count("distance")!=1 or kind_list.count("radius")!=2:
        return not_proved("distance_or_double_radius_calls_not_found",**facts)
    # A deliberately small type-checked JVM symbolic evaluator rejects unknown opcodes,
    # underflow, receiver confusion, and unsupported method descriptors (FAIL_CLOSED).
    stack=[]
    locals_by_slot={}
    def pop(typ):
        if not stack:raise ValueError("operand_underflow")
        val=stack.pop()
        if val[0]!=typ:raise ValueError("operand_type_mismatch")
        return val[1]
    try:
        for index,(_,op,arg,symbol) in enumerate(window,start=19):
            if op=="nop":continue
            save=re.fullmatch(r"dstore_([0-9]+)",op)
            if save:
                slot=int(save.group(1))
                if slot!=3 or slot in locals_by_slot:raise ValueError("unapproved_or_reassigned_double_local")
                locals_by_slot[slot]=pop("D");continue
            retrieve=re.fullmatch(r"dload_([0-9]+)",op)
            if retrieve:
                slot=int(retrieve.group(1))
                if slot!=3 or slot not in locals_by_slot:raise ValueError("missing_saved_double_local")
                stack.append(("D",locals_by_slot[slot]));continue
            m=re.fullmatch(r"aload_([0-3])",op)
            if m:
                stack.append(("O","slot"+m.group(1)));continue
            if op in ("dconst_0","dconst_1","fconst_0","fconst_1","fconst_2"):
                stack.append(("D" if op.startswith("d") else "F",op.split("_")[1]));continue
            if op in ("ldc","ldc2_w"):
                numeric=re.search(r"(double|float)\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?:[df])?\b",symbol)
                if not numeric:raise ValueError("unsupported_numeric_literal")
                stack.append(("D" if numeric.group(1)=="double" else "F",numeric.group(2)));continue
            if op=="f2d":
                stack.append(("D",pop("F")));continue
            if op=="d2f":
                stack.append(("F",pop("D")));continue
            if op=="dup2":
                if not stack or stack[-1][0]!="D":raise ValueError("bad_dup2")
                stack.append(stack[-1]);continue
            if op in ("dadd","dsub","dmul","ddiv","fadd","fsub","fmul","fdiv"):
                typ="D" if op.startswith("d") else "F"
                b,a=pop(typ),pop(typ)
                stack.append((typ,"("+a+{"dadd":"+","dsub":"-","dmul":"*","ddiv":"/","fadd":"+","fsub":"-","fmul":"*","fdiv":"/"}[op]+b+")"))
                continue
            if op=="invokevirtual":
                k=method_kind(symbol)
                if k is None:raise ValueError("unsupported_callsite")
                if k=="radius":
                    receiver=pop("O")
                    if receiver!="slot0":raise ValueError("radius_receiver_not_controller")
                    stack.append(("F","R"));continue
                if k in ("x","y","z"):
                    receiver=pop("O")
                    stack.append(("D",k+"("+receiver+")"));continue
                if k=="distance":
                    z,y,x=pop("D"),pop("D"),pop("D")
                    receiver=pop("O")
                    stack.append(("D","distSq("+receiver+","+x+","+y+","+z+")"));continue
            if op in ("dcmpg","dcmpl","fcmpg","fcmpl"):
                typ="D" if op.startswith("d") else "F"
                rhs,lhs=pop(typ),pop(typ)
                stack.append(("I","cmp("+lhs+","+rhs+")"));continue
            if index==36 and op=="ifgt":
                test=pop("I")
                if stack:raise ValueError("unexpected_stack_at_conditional")
                facts["status"]="PROVED_FINAL_IFGT_NUMERIC_COMPARISON"
                facts["derived_rejection_condition"]=test+" > 0"
                facts["comparison_semantics"]="Java JVM cmp instruction then ifgt, branches to false return"
                return facts
            raise ValueError("unsupported_operation")
    except ValueError as e:
        return not_proved(str(e),**facts)
    return not_proved("no_terminal_ifgt_value",**facts)

def inspect(jar:Path):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong jar filename or size")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("publisher hash mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise GateError("duplicate zip entries")
        if CLASS.replace(".","/")+".class" not in names:raise GateError("controller class missing")
        metadata=z.read("META-INF/neoforge.mods.toml")
        if len(metadata)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",metadata):
            raise GateError("mod id mismatch")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
                     capture_output=True,text=True,timeout=60,check=False)
    if p.returncode or len(p.stdout)>1_400_000:raise GateError("javap failed/unbounded")
    declared=sections(p.stdout)
    certify_exact_native_target_cfg_109(native_isvalidtarget_branch_edges(declared),
                                        native_isvalidtarget_early_guards(declared))
    certify_exact_native_middle_109(middle_guard(declared))
    res=arithmetic_window(declared)
    return {"status":"PASS_SHA_EXACT_DISTANCE_BRANCH_ANALYSIS","sha1":digest,
            "mod_id":"somakespells","version":"1.0.9","final_branch":res,
            "limits":"This is JVM static analysis, not provider-loaded QA or a mutator seam"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    args=a.parse_args()
    evidence=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(evidence,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_FINAL_DISTANCE_PROBE",json.dumps(evidence["final_branch"],sort_keys=True))
    print("SOMAKE_FINAL_DISTANCE_SHA",evidence["sha1"])
if __name__=="__main__":
    main()
