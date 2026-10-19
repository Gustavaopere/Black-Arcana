#!/usr/bin/env python3
"""Bounded typed JVM abstract interpreter for exact Somake Funeral Bloom radius.

Records symbolic return values and a proven null guard for each complete path.
No disassembly, provider implementation or class bytes are exported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from collections import deque
from pathlib import Path
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import (
    SOMAKE_CLASS, SOMAKE_GETTER_DESC, sections, opcode_rows, radius_cfg
)
from somake_109_numeric_fingerprint import decode_numeric

MAX_STEPS=180
MAX_EXPR=1400

def interpret(body:list[str], descriptor:str)->dict:
    """All opcodes on both paths must be modeled or a proof is refused."""
    def reject(why):return {"status":"NOT_PROVED","reason":why}
    if descriptor!=SOMAKE_GETTER_DESC:return reject("wrong_radius_descriptor")
    try:
        topology=radius_cfg(body)
        code=opcode_rows(body)
    except GateError as e:return reject("invalid_cfg:"+str(e))
    if topology["branch_predicates"]!=["ifnonnull"] or topology["conditional_branches"]!=1:
        return reject("unexpected_branch_topology")
    offsets={row[0]:i for i,row in enumerate(code)}
    queue=deque([(code[0][0],(),((0,"R","this"),(1,"I","level"),(2,"R","caster")),(),())])
    finished=[]
    steps=0
    while queue:
        steps+=1
        if steps>MAX_STEPS or len(queue)>40:return reject("path_budget")
        pc,stack_snapshot,local_snapshot,guards,calls=queue.popleft()
        if pc not in offsets:return reject("bad_pc")
        idx=offsets[pc]
        _,op,operand,comment=code[idx]
        next_pc=code[idx+1][0] if idx+1<len(code) else None
        stack=list(stack_snapshot)
        locals_map={n:(typ,value) for n,typ,value in local_snapshot}
        call_list=list(calls)
        def pop(kind):
            if not stack or stack[-1][0]!=kind:raise GateError("stack_expected_"+kind)
            return stack.pop()[1]
        def push(kind,value):
            if len(value)>MAX_EXPR or len(stack)>=18:raise GateError("expression_budget")
            stack.append((kind,value))
        def onward(target,guard=None):
            if target not in offsets:raise GateError("missing_successor")
            snapshot=tuple((n,k,v) for n,(k,v) in sorted(locals_map.items()))
            queue.append((target,tuple(stack),snapshot,
                          guards if guard is None else (guard,),tuple(call_list)))
        try:
            num=decode_numeric(op,operand,comment)
            if num:
                typ={"int":"I","float":"F","double":"D","long":"J"}[num[0]]
                if typ=="J":return reject("unsupported_long_literal")
                push(typ,num[1])
            elif re.fullmatch(r"[aifd]load(?:_[0-9]+)?",op):
                n=int(op.split("_")[-1]) if "_" in op else int(operand) if operand.isdecimal() else -1
                typ={"a":"R","i":"I","f":"F","d":"D"}[op[0]]
                if n not in locals_map or locals_map[n][0]!=typ:return reject("untracked_local_load")
                push(*locals_map[n])
            elif re.fullmatch(r"[aifd]store(?:_[0-9]+)?",op):
                n=int(op.split("_")[-1]) if "_" in op else int(operand) if operand.isdecimal() else -1
                typ={"a":"R","i":"I","f":"F","d":"D"}[op[0]]
                if not 3<=n<=12:return reject("unexpected_local_slot")
                locals_map[n]=(typ,pop(typ))
            elif op=="ifnonnull":
                subject=pop("R")
                if subject!="caster" or guards:return reject("unproved_null_guard_subject")
                target=operand.split()[0]
                if not target.isdecimal() or next_pc is None:return reject("bad_null_branch")
                onward(int(target),"caster != null")
                onward(next_pc,"caster == null")
                continue
            elif op in ("goto","goto_w"):
                target=operand.split()[0]
                if not target.isdecimal():return reject("invalid_goto")
                onward(int(target))
                continue
            elif op in ("fadd","fsub","fmul","fdiv","dadd","dsub","dmul","ddiv"):
                kind={"f":"F","d":"D"}[op[0]]
                right=pop(kind);left=pop(kind)
                operator={"add":"+","sub":"-","mul":"*","div":"/"}[op[1:]]
                push(kind,"("+left+operator+right+")")
            elif op in ("d2f","i2f","f2d","i2d"):
                src={"d":"D","i":"I","f":"F"}[op[0]]
                dest={"d":"D","f":"F"}[op[-1]]
                push(dest,op+"("+pop(src)+")")
            elif op in ("fneg","dneg"):
                kind={"f":"F","d":"D"}[op[0]]
                push(kind,"(-"+pop(kind)+")")
            elif op=="dup":
                if not stack or stack[-1][0]=="D":return reject("invalid_dup")
                push(*stack[-1])
            elif op=="pop":
                if not stack or stack[-1][0]=="D":return reject("invalid_pop")
                stack.pop()
            elif op in ("invokestatic","invokevirtual","invokeinterface"):
                if re.search(r"\bgetSchoolType:\(\)Lio/redspace/ironsspellbooks/api/spells/SchoolType;",comment):
                    if op!="invokevirtual" or pop("R")!="this":return reject("unproved_schooltype_receiver")
                    push("R","schoolType()");call_list.append("getSchoolType")
                elif re.search(r"\bSchoolType\.getPowerFor:\(Lnet/minecraft/world/entity/LivingEntity;\)D",comment):
                    if op!="invokevirtual":return reject("bad_schoolpower_opcode")
                    caster=pop("R");school=pop("R")
                    if caster!="caster" or school!="schoolType()":
                        return reject("unproved_schoolpower_arguments")
                    push("D","schoolPower(caster)");call_list.append("SchoolType.getPowerFor")
                elif re.search(r"\bMath\.max:\(FF\)F",comment):
                    if op!="invokestatic":return reject("bad_math_opcode")
                    b=pop("F");a=pop("F")
                    push("F","Math.max_f32("+a+","+b+")");call_list.append("Math.max")
                elif re.search(r"\bMth\.clamp:\(FFF\)F",comment):
                    if op!="invokestatic":return reject("bad_clamp_opcode")
                    high=pop("F");low=pop("F");value=pop("F")
                    if (low,high)!=("10.0","15.0"):return reject("unexpected_clamp_limits")
                    push("F","Mth.clamp_f32("+value+","+low+","+high+")")
                    call_list.append("Mth.clamp")
                else:return reject("unrecognized_provider_invocation")
            elif op=="freturn":
                value=pop("F")
                if stack or len(guards)!=1:return reject("unbalanced_return")
                finished.append({"condition":guards[0],"jvm_float_expression":value,
                                 "calls":call_list})
                continue
            else:return reject("unsupported_opcode_"+op)
            if next_pc is None:return reject("missing_return")
            onward(next_pc)
        except (GateError,IndexError,ValueError,KeyError) as e:
            return reject("typed_transfer_rejected:"+str(e))
    if len(finished)!=2 or sorted(x["condition"] for x in finished)!=["caster != null","caster == null"]:
        return reject("missing_or_duplicate_complete_paths")
    return {"status":"PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",
            "guards":["caster == null","caster != null"],
            "paths":sorted(finished,key=lambda x:x["condition"]),
            "jvm_instructions":topology["instruction_count"],
            "limitations":"Symbolic return only; not loaded gameplay, LOS, hitbox or per-player perk API."}

EXPECTED_EXACT_109_RADIUS_PATHS = {
    "caster != null": {
        "jvm_float_expression": "Mth.clamp_f32(((9.5+(i2f(level)*0.82))+(Math.max_f32(0,(d2f(schoolPower(caster))-1))*0.65)),10.0,15.0)",
        "calls": ["getSchoolType", "SchoolType.getPowerFor", "Math.max", "Mth.clamp"],
    },
    "caster == null": {
        "jvm_float_expression": "Mth.clamp_f32(((9.5+(i2f(level)*0.82))+(Math.max_f32(0,(1-1))*0.65)),10.0,15.0)",
        "calls": ["Math.max", "Mth.clamp"],
    },
}

def certify_exact_109(proof:dict)->None:
    """Lock both complete return paths to the exact installed publisher release."""
    if proof.get("status")!="PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION":
        raise GateError("no complete proof")
    paths=proof.get("paths",[])
    if len(paths)!=2 or len({p.get("condition") for p in paths})!=2:
        raise GateError("ambiguous or duplicated radius branches")
    if proof.get("jvm_instructions")!=28:
        raise GateError("JVM method fingerprint drift")
    by_condition={p["condition"]:p for p in paths}
    if set(by_condition)!=set(EXPECTED_EXACT_109_RADIUS_PATHS):
        raise GateError("unexpected radius branch guard")
    for condition,expected in EXPECTED_EXACT_109_RADIUS_PATHS.items():
        actual=by_condition[condition]
        if any(actual.get(k)!=v for k,v in expected.items()):
            raise GateError("exact Somake radius symbolic return drift: "+condition)


def inspect(jar:Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong Somake filename/type/size")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("wrong publisher SHA1")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise GateError("duplicate archive entries")
        meta=z.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("incorrect publisher mod ID")
        if SOMAKE_CLASS.replace(".","/")+".class" not in names:raise GateError("missing class")
    out=subprocess.run(["javap","-c","-s","-p","-classpath",str(jar.resolve()),SOMAKE_CLASS],
                       capture_output=True,text=True,timeout=50,check=False)
    if out.returncode or not out.stdout or len(out.stdout)>1_500_000:raise GateError("javap budget/error")
    methods=[(desc,body) for name,desc,body in sections(out.stdout) if name=="getRadius"]
    if len(methods)!=1:raise GateError("missing/ambiguous getter")
    desc,body=methods[0]
    proof=interpret(body,desc)
    print("SOMAKE_RADIUS_TYPED_PATHS",json.dumps(proof,sort_keys=True))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("JAR changed while inspecting")
    if proof["status"]!="PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION":
        raise GateError("strict proof incomplete: "+proof["reason"])
    certify_exact_109(proof)
    return {"status":"PASS_EXACT_SOMAKE_RADIUS_TWO_PATH_RETURN",
            "sha1":digest,"fqcn":SOMAKE_CLASS,"descriptor":desc,
            "proof":proof,"boundary":"Static JVM proof only; no observed loaded provider or safe mutator."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    data=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_RADIUS_TYPED_GATE",data["status"],data["sha1"])

if __name__=="__main__":main()
