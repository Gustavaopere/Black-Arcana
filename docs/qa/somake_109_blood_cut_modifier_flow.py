#!/usr/bin/env python3
"""Fail-closed symbolic float return analysis for Somake 1.0.9 BloodCutEffect.

Never emit raw JVM disassembly, classfiles or publisher code. Expressions below
are derived normal-flow stack algebra, not game damage, configured coefficients,
final proc frequency, or writable perk parameters.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

from somake_109_perk_method_probe import GateError, SHA1
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_blood_cut_cfg import EFFECT_CLASS, MODIFIER, MODIFIER_DESCRIPTOR
from somake_109_blood_cut_event_gate import inspect as certify_annotations

MEMBER = re.compile(r"(?:Method|InterfaceMethod) ([^:]+):(\([^)]*\)[^\s]+)")
LITERAL = re.compile(r"\bfloat\s+([-+]?(?:\d+(?:\.\d*)?|\.\d+))(?:f)?\b")

def symbolic_modifier(rows):
    if len(rows) != 19:
        raise GateError("modifier instruction-count drift")
    pcs=[r[0] for r in rows]
    if pcs != sorted(set(pcs)):
        raise GateError("malformed method PC order")
    index={pc:i for i,pc in enumerate(pcs)}
    branches=[op for _,op,_,_ in rows if op.startswith(("if","goto"))]
    if branches != ["ifnonnull","goto"]:
        raise GateError("modifier requires one nonnull guard and one unconditional skip")
    finished=[]
    pending=[(0,tuple(),tuple(),tuple())]
    visited=set()
    while pending:
        if len(pending)>16 or len(visited)>100:
            raise GateError("symbolic state budget exceeded")
        i,stack,constraints,stored=pending.pop()
        if (i,stack,constraints,stored) in visited:
            raise GateError("symbolic cycle or duplicate state")
        visited.add((i,stack,constraints,stored))
        if not 0<=i<len(rows):raise GateError("instruction falls outside method")
        pc,op,arg,comment=rows[i]
        values=list(stack)
        local_values=dict(stored)
        def pop():
            if not values:raise GateError("JVM operand stack underflow")
            return values.pop()
        def go(nextindex):pending.append((nextindex,tuple(values),constraints,tuple(sorted(local_values.items()))))
        if re.fullmatch(r"[aifd]load_[0-3]",op):
            slot=op.split("_")[-1]
            values.append(local_values.get(slot,("arg",slot)))
        elif op in ("aload","iload","fload","dload") and re.fullmatch(r"\d+",arg):
            values.append(local_values.get(arg,("arg",arg)))
        elif re.fullmatch(r"[aifd]store_[0-3]",op):
            local_values[op.split("_")[-1]]=pop()
        elif op in ("astore","istore","fstore","dstore") and re.fullmatch(r"\d+",arg):
            local_values[arg]=pop()
        elif re.fullmatch(r"iconst_[0-5]",op) or re.fullmatch(r"fconst_[0-2]",op):
            values.append(("literal",op.rsplit("_",1)[-1]))
        elif op in ("bipush","sipush") and re.fullmatch(r"-?\d+",arg):
            values.append(("literal",arg))
        elif op.startswith("ldc"):
            m=LITERAL.search(comment)
            if not m:raise GateError("unhandled numeric constant")
            values.append(("literal_float",m.group(1)))
        elif op in ("iadd","fadd","imul","fmul","fsub","fdiv"):
            right=pop();left=pop()
            values.append((op,left,right))
        elif op=="i2f":
            values.append(("i2f",pop()))
        elif op=="nop":
            pass
        elif op=="getstatic":
            if "ModSpells.BLOOD_CUT:" not in comment:
                raise GateError("unrecognized static owner")
            values.append(("spell_holder","BLOOD_CUT"))
        elif op=="checkcast":
            if not values:raise GateError("cast on empty operand stack")
        elif op.startswith("invoke"):
            m=MEMBER.search(comment)
            if not m:raise GateError("unrecognized method reference")
            owner,desc=m.groups()
            if "DeferredHolder.get" in owner and desc=="()Ljava/lang/Object;":
                receiver=pop()
                if receiver!=("spell_holder","BLOOD_CUT"):
                    raise GateError("unexpected deferred-holder provenance")
                values.append(("blood_cut_spell","BLOOD_CUT"))
            elif "BloodCutSpell.getEntityPowerMultiplier" in owner and desc=="(Lnet/minecraft/world/entity/LivingEntity;)F":
                actor=pop();spell=pop()
                if spell!=("blood_cut_spell","BLOOD_CUT"):
                    raise GateError("power multiplier owner drift")
                values.append(("entity_power_multiplier",actor))
            else:
                raise GateError("unresolved invocation in modifier: "+owner[-85:])
        elif op=="ifnonnull":
            object_ref=pop()
            if object_ref != ("arg","1"):
                raise GateError("nullable guard actor provenance changed")
            if not re.fullmatch(r"\d+",arg) or int(arg) not in index:
                raise GateError("invalid conditional target")
            if index[int(arg)] <= i:raise GateError("unsupported backward edge")
            frozen=tuple(sorted(local_values.items()))
            pending.append((index[int(arg)],tuple(values),constraints+("arg1 != null",),frozen))
            pending.append((i+1,tuple(values),constraints+("arg1 == null",),frozen))
            continue
        elif op=="goto":
            if not re.fullmatch(r"\d+",arg) or int(arg) not in index:
                raise GateError("invalid unconditional target")
            if index[int(arg)]<=i:raise GateError("unsupported goto backedge")
            go(index[int(arg)])
            continue
        elif op=="freturn":
            value=pop()
            if values:raise GateError("extra operand at freturn")
            finished.append({"guard":" & ".join(constraints),"expression":value})
            continue
        else:
            raise GateError("unsupported JVM opcode in strict float path: "+op)
        go(i+1)
    if len(finished)!=2 or {x["guard"] for x in finished}!={"arg1 == null","arg1 != null"}:
        raise GateError("expected exact two nullable-caster return paths")
    for path in finished:
        if not isinstance(path["expression"],tuple) or not path["expression"]:
            raise GateError("empty JVM return expression")
    return sorted(finished,key=lambda x:x["guard"])


def inspect(jar:Path):
    import hashlib, subprocess
    from somake_109_blood_cut_cfg import MODIFIER
    gate=certify_annotations(jar)
    if gate["artifact_sha1"]!=SHA1:raise GateError("SHA upstream gate drift")
    p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),EFFECT_CLASS],
        capture_output=True,text=True,timeout=40,check=False)
    if p.returncode or not 100<len(p.stdout)<1_500_000:
        raise GateError("exact class inspect failed")
    matches=[opcode_rows(body) for n,d,body in sections(p.stdout) if n==MODIFIER and d==MODIFIER_DESCRIPTOR]
    if len(matches)!=1:raise GateError("modifier exact signature missing")
    results=symbolic_modifier(matches[0])
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:raise GateError("JAR hash drift")
    return {"status":"PASS_SHA_EXACT_BLOOD_CUT_BOUNDED_FLOAT_DATAFLOW",
        "provider":"somakespells","version":"1.0.9","sha1":SHA1,
        "method":"BloodCutEffect.getDamageModifier(int,LivingEntity):float",
        "return_paths":results,
        "boundary":"Derived expressions at JVM freturn; not applied damage, effective host config, recursion protection, or modifiable hooks."}


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("BLOOD_CUT_FLOAT_DATAFLOW",result["status"],result["sha1"])
    print("FLOAT_RETURN_PATHS",json.dumps(result["return_paths"],sort_keys=True))


if __name__=="__main__":main()
