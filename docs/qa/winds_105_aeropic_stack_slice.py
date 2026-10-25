#!/usr/bin/env python3
"""Bounded basic-block JVM abstract stack for Aeropic recast receiver source.

A positive result proves the bytecode receiver producer in that block only.
It never resolves Supplier implementation, virtual dispatch, or player state.
Unknown opcodes and control-flow entry points fail closed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as prior
import winds_105_aeropic_supplier_receiver_slice as direct

MAX_INSTRUCTIONS = 72
FIELD = direct.SPELL_SUPPLIER
SUPPLIER_GET = direct.SUPPLIER_GET
ABSTRACT = direct.ABSTRACT_SPELL
RECAST = prior.RECAST
UNKNOWN = "UNKNOWN_INITIAL_OR_UNRESOLVED_VALUE"
SUPPLIER_FIELD = "ACROBATICS_SPELL_SUPPLIER_FIELD"
SUPPLIER_RESULT = "ACROBATICS_SPELL_SUPPLIER_GET_RESULT"
CHECKED_SPELL = "SUPPLIER_RESULT_CHECKCAST_ABSTRACTSPELL"

class SliceError(ValueError):
    pass

def descriptor(signature:str) -> tuple[int,bool]:
    """Count logical JVM arguments and return, not word slots."""
    if "(" not in signature or ")" not in signature:
        raise SliceError("unparseable method JVM descriptor")
    s=signature[signature.find("(")+1:signature.find(")")]
    n=0
    i=0
    while i<len(s):
        while i<len(s) and s[i]=="[":
            i+=1
        if i>=len(s):
            raise SliceError("truncated array descriptor")
        if s[i]=="L":
            j=s.find(";",i)
            if j<0:
                raise SliceError("unterminated object descriptor")
            i=j+1
        elif s[i] in "BCDFIJSZ":
            i+=1
        else:
            raise SliceError("unknown type in method descriptor")
        n+=1
    ret=signature[signature.find(")")+1:]
    if not ret:
        raise SliceError("missing return descriptor")
    return n, ret[0]!="V"

def _load(op:str):
    for prefix in ("aload","iload","fload","dload","lload"):
        if op==prefix or op.startswith(prefix+"_"):
            return "load",prefix
    for prefix in ("astore","istore","fstore","dstore","lstore"):
        if op==prefix or op.startswith(prefix+"_"):
            return "store",prefix
    return None

def _local_id(op:str) -> str:
    return op.rsplit("_",1)[-1] if "_" in op else "UNSPECIFIED_INDEX"

def _run(start:list[dict], method:str) -> dict:
    """No merges allowed. Initial stack unknown, explicit values tracked."""
    # Unknown initial values below the first observed instruction are added
    # on demand, but never treated as a proven object or receiver.
    stack=[]
    locals_map={}
    source_seen=False
    cast_seen=False
    def pop():
        return stack.pop() if stack else UNKNOWN
    for row in start:
        op=row["opcode"]
        symbol=row.get("symbol","")
        if row.get("branch") or op in ("athrow","return","ireturn","areturn",
                                      "tableswitch","lookupswitch","jsr","ret"):
            raise SliceError("control flow or return in candidate stack slice")
        if op=="getstatic":
            stack.append(SUPPLIER_FIELD if symbol==FIELD else UNKNOWN)
            source_seen |= symbol==FIELD
        elif op=="checkcast":
            value=pop()
            is_checked=value==SUPPLIER_RESULT and symbol==ABSTRACT
            stack.append(CHECKED_SPELL if is_checked else UNKNOWN)
            cast_seen |= is_checked
        elif op in ("invokeinterface","invokevirtual","invokespecial","invokestatic"):
            argc,returns=descriptor(symbol.split(":",1)[1] if ":" in symbol else "")
            args=[pop() for _ in range(argc)]
            receiver=pop() if op!="invokestatic" else None
            if symbol==RECAST:
                if op!="invokevirtual":
                    raise SliceError("unexpected recast invoke opcode")
                return {
                    "source":("COMPILED_SUPPLIER_GET_CAST_RECEIVER"
                              if receiver==CHECKED_SPELL else "NOT_PROVEN"),
                    "source_field_seen":source_seen,
                    "supplier_cast_seen":cast_seen,
                    "receiver_provenance":receiver if receiver==CHECKED_SPELL else "NOT_PROVEN",
                }
            if returns:
                if op=="invokeinterface" and symbol==SUPPLIER_GET and receiver==SUPPLIER_FIELD:
                    stack.append(SUPPLIER_RESULT)
                else:
                    stack.append(UNKNOWN)
        elif (kind:=_load(op)) is not None:
            family=kind[1]
            key=_local_id(op)
            if kind[0]=="load":
                # Unsuffixed javap local indices were deliberately not parsed.
                # Never alias two different locals through an invented key.
                stack.append(locals_map.get((family[0],key),UNKNOWN)
                             if key!="UNSPECIFIED_INDEX" else UNKNOWN)
            else:
                value=pop()
                if key!="UNSPECIFIED_INDEX":
                    locals_map[(family[0],key)]=value
        elif op in {"iconst_m1","aconst_null","fconst_0","fconst_1","fconst_2",
                     "lconst_0","lconst_1","dconst_0","dconst_1","bipush","sipush",
                     "ldc","ldc_w","ldc2_w"} or op.startswith("iconst_"):
            stack.append(UNKNOWN)
        elif op=="new":
            stack.append(UNKNOWN)
        elif op=="getfield":
            pop()
            stack.append(UNKNOWN)
        elif op=="putfield":
            pop()
            pop()
        elif op=="putstatic":
            pop()
        elif op=="dup":
            if not stack:
                raise SliceError("dup without bounded stack owner")
            stack.append(stack[-1])
        elif op=="pop":
            pop()
        elif op=="nop" or op=="iinc":
            pass
        elif op in ("iadd","isub","imul","idiv","irem","iand","ior","ixor",
                    "fadd","fsub","fmul","fdiv","dadd","dsub","dmul","ddiv",
                    "ladd","lsub","lmul","ldiv","ishl","ishr","iushr"):
            pop()
            pop()
            stack.append(UNKNOWN)
        elif op in ("i2f","i2d","i2l","f2i","f2d","d2i","d2f","l2i",
                    "ineg","fneg","dneg","lneg","arraylength","instanceof"):
            pop()
            stack.append(UNKNOWN)
        elif op=="aaload":
            pop()
            pop()
            stack.append(UNKNOWN)
        elif op=="aastore":
            pop()
            pop()
            pop()
        else:
            raise SliceError("unsupported JVM instruction in candidate slice: "+op)
    raise SliceError("target recast call not reached")

def classify(rows:list[dict], name:str) -> dict:
    indices=[i for i,row in enumerate(rows)
             if row["opcode"].startswith("invoke") and row.get("symbol")==RECAST]
    if len(indices)!=1:
        raise SliceError("wrong target recast call population "+name)
    end=indices[0]
    if rows[end]["opcode"]!="invokevirtual":
        raise SliceError("recast invocation opcode drift")
    sources=[i for i,row in enumerate(rows[:end]) if row["opcode"]=="getstatic"
             and row.get("symbol")==FIELD]
    reason="NO_MATCHING_SUPPLIER_FIELD_WITHIN_BOUNDED_BASIC_BLOCK"
    positive=None
    if sources:
        source=sources[-1]
        run=rows[source:end+1]
        if len(run)>MAX_INSTRUCTIONS:
            reason="SOURCE_OUTSIDE_BOUNDED_SLICE"
        else:
            lo,hi=run[0]["offset"],run[-1]["offset"]
            # No branch target at a point *inside* the candidate expression.
            # A jump to its first instruction is allowed: it begins a whole block.
            for row in rows:
                if row.get("branch") and (
                    row.get("branch_target") is None or
                    lo < row["branch_target"] <= hi
                ):
                    reason="EXTERNAL_CONTROL_FLOW_ENTRY_OR_UNRESOLVED_SWITCH"
                    break
            else:
                try:
                    positive=_run(run,name)
                    reason=None if positive["source"]!="NOT_PROVEN" else "RECEIVER_NOT_FROM_CHECKED_SUPPLIER_RESULT"
                except SliceError as exc:
                    reason="FAIL_CLOSED_"+str(exc)
    return {
        "method":name,
        "compiled_receiver_source":positive["source"] if positive else "NOT_PROVEN",
        "evidence_grade":("SINGLE_BASIC_BLOCK_SYMBOLIC_STACK"
                          if positive and positive["source"]!="NOT_PROVEN"
                          else "NOT_PROVEN"),
        "non_proof_reason":reason,
        "recast_invoke_symbol":RECAST,
        "runtime_receiver_concrete_class":"NOT_PROVEN",
        "supplier_actual_spell_class":"NOT_PROVEN",
        "dynamic_override_executed":"NOT_PROVEN",
        "return_value_to_PlayerRecasts":"NOT_PROVEN",
        "safe_perk_mutator":"NOT_PROVEN",
    }

def audit(jar:Path)->dict:
    identity=physical.audit(jar)
    try:
        p=subprocess.run(["javap","-c","-p","-classpath",str(jar),prior.EFFECT],
                         capture_output=True,text=True,check=True,timeout=30)
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        raise SliceError("frozen JAR javap inspection failed") from exc
    methods=direct.methods_from_javap(p.stdout)
    sites={name:classify(methods[name],name) for name in prior.EXPECTED_CALLER_METHODS}
    return {"result":"PASS_EXACT_JVM_BASIC_BLOCK_RECAST_RECEIVER_CLASSIFICATION",
            "sha1":identity["sha1"],"provider":"wind_spellbooks",
            "release":"1.0.5","call_sites":sites,
            "compiled_jvm_stack_observations_only":True,
            "untrusted_provider_code_copied":False,
            "host_installed_checksum":"NOT_VERIFIED",
            "runtime_dispatch":"NOT_PROVEN",
            "safe_mutating_hook":"NOT_PROVEN",
            "physical_gameplay":"NOT_TESTED"}

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        doc=audit(args.jar)
        code=0
    except (SliceError,direct.SliceError,physical.AuditError,ValueError,OSError,TypeError,KeyError) as exc:
        doc={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    payload=json.dumps(doc,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
