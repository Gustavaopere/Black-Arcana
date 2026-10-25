#!/usr/bin/env python3
"""Conservative straight-line JVM slice for Aeropic recast receiver provenance.

Proves only an immediately contiguous *compiled operand producer* where one
exists. Does not resolve supplier instance, dynamic dispatch, or a safe hook.
Emits symbolic conclusions, never provider bytecode or full disassembly.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as prior

EFFECT = prior.EFFECT
RECAST = prior.RECAST
CALLERS = prior.EXPECTED_CALLER_METHODS
SPELL_SUPPLIER = (
    "net/raptorzizi/wind_spellbooks/registries/ModSpellRegistry."
    "ACROBATICS_SPELL:Ljava/util/function/Supplier;"
)
SUPPLIER_GET = "java/util/function/Supplier.get:()Ljava/lang/Object;"
ABSTRACT_SPELL = "io/redspace/ironsspellbooks/api/spells/AbstractSpell"

DECL = re.compile(r"^  (?:public|protected|private) [^\n]*\([^;]*\);$")
INSTR = re.compile(r"^\s*(\d+):\s+([a-z][\w]*)\b(.*)$")
FIELD = re.compile(r"^Field\s+(\S+)$")
INVOKE = re.compile(r"^(?:Method|InterfaceMethod)\s+(\S+)$")
TYPE = re.compile(r"^class\s+(\S+)$")
BRANCHES = re.compile(r"^(?:if|goto|jsr|tableswitch|lookupswitch)")
INT_VALUE = re.compile(r"^(?:iload(?:_\d+)?|iconst_[0-5]|iconst_m1|bipush|sipush|ldc|ldc_w)$")
ENTITY_VALUE = re.compile(r"^aload(?:_\d+)?$")

class SliceError(ValueError):
    pass

def methods_from_javap(text: str) -> dict[str,list[dict]]:
    """Read exact method boundaries and selected instructions in local memory."""
    data={}
    method=None
    for line in text.splitlines():
        if DECL.match(line):
            name=line.strip().split("(",1)[0].rsplit(" ",1)[-1]
            method=name if name in CALLERS else None
            if method:
                if method in data:
                    raise SliceError("overloaded recast method: "+method)
                data[method]=[]
            continue
        if line.startswith("  static {};"):
            method=None
            continue
        if method is None:
            continue
        if not (m:=INSTR.match(line)):
            continue
        offset,opcode,operand=m.groups()
        comment=operand.split("//",1)[1].strip() if "//" in operand else ""
        row={"offset":int(offset),"opcode":opcode}
        if opcode.startswith("invoke") and (sym:=INVOKE.match(comment)):
            row["symbol"]=sym.group(1)
        elif opcode in ("getstatic","putstatic","getfield","putfield") and (sym:=FIELD.match(comment)):
            row["symbol"]=sym.group(1)
        elif opcode in ("checkcast","new","instanceof") and (sym:=TYPE.match(comment)):
            row["symbol"]=sym.group(1)
        if BRANCHES.match(opcode):
            row["branch"]=True
            if opcode not in ("tableswitch","lookupswitch") and (target:=re.match(r"^\s+(-?\d+)\b",operand)):
                row["branch_target"]=int(target.group(1))
        data[method].append(row)
    if set(data)!=set(CALLERS):
        raise SliceError("missing one of the two recast methods")
    for method,opcodes in data.items():
        if not opcodes or len(opcodes)>10000:
            raise SliceError("missing/unbounded bytecode in "+method)
        offsets=[x["offset"] for x in opcodes]
        if offsets!=sorted(set(offsets)):
            raise SliceError("duplicate/nonmonotonic JVM offsets")
    return data

def _site(rows:list[dict], method:str) -> dict:
    at=[i for i,row in enumerate(rows)
        if row["opcode"].startswith("invoke") and row.get("symbol")==RECAST]
    if len(at)!=1:
        raise SliceError("recast invocation count drift in "+method)
    n=at[0]
    if rows[n]["opcode"]!="invokevirtual":
        raise SliceError("recast invocation opcode drift in "+method)

    # This is deliberately a *single contiguous basic-block suffix*, not an
    # arbitrary nearest mention of Supplier.get or checkcast in a 24-op window.
    # The receiver must be the Object returned by the Supplier invocation,
    # cast to AbstractSpell, with exactly two simple arguments pushed next.
    suffix=rows[max(0,n-5):n]
    shapes=[x["opcode"] for x in suffix]
    source_proven=False
    failure="NO_MATCHING_UNBRANCHED_FIVE_INSTRUCTION_PRODUCER"
    if len(suffix)==5:
        first,get,cast,intarg,entityarg=suffix
        sequence=(
            first["opcode"]=="getstatic" and first.get("symbol")==SPELL_SUPPLIER
            and get["opcode"]=="invokeinterface" and get.get("symbol")==SUPPLIER_GET
            and cast["opcode"]=="checkcast" and cast.get("symbol")==ABSTRACT_SPELL
            and INT_VALUE.fullmatch(intarg["opcode"]) is not None
            and ENTITY_VALUE.fullmatch(entityarg["opcode"]) is not None
        )
        block_start=first["offset"]
        block_end=rows[n]["offset"]
        # A jump from anywhere in the method to any point between start and
        # invocation would make the suffix non-sequential along that path.
        incoming=[
            row for row in rows if row.get("branch")
            and (row.get("branch_target") is None or
                 block_start < row["branch_target"] <= block_end)
        ]
        internal=[row for row in suffix if row.get("branch")]
        if sequence and not incoming and not internal:
            source_proven=True
            failure=None
        elif sequence:
            failure="CONTROL_FLOW_ENTRY_OR_UNRESOLVED_SWITCH_PREVENTS_PROOF"

    # Immediate use of result is not necessarily transfer to a RecastInstance.
    # Two-step arithmetic evidence is reported only with consecutive opcodes.
    next2=[x["opcode"] for x in rows[n+1:n+3]]
    immediate_arithmetic=("PLUS_ONE_DIRECTLY_AFTER_CALL" if next2==["iconst_1","iadd"]
        else "NONE_PROVEN")
    return {
        "method":method,
        "owner_opcode":"invokevirtual",
        "method_owner_and_descriptor":RECAST,
        "static_receiver_origin":(
            "COMPILED_ACROBATICS_SPELL_SUPPLIER_GET_CAST_TO_ABSTRACTSPELL"
            if source_proven else "NOT_PROVEN"),
        "origin_proof_rule":(
            "STRICT_FIVE_INSTRUCTION_STRAIGHT_LINE_RECEIVER_PRODUCER"
            if source_proven else "NO_SAFE_CONTIGUOUS_SLICE"),
        "non_proof_reason":failure,
        "immediate_result_arithmetic":immediate_arithmetic,
        "supplier_return_class":"NOT_PROVEN",
        "receiver_runtime_type":"NOT_PROVEN",
        "abstractspell_override_target":"NOT_PROVEN",
        "recast_state_value_flow":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN",
    }

def examine(methods:dict[str,list[dict]]) -> dict:
    if set(methods)!=set(CALLERS):
        raise SliceError("wrong source method coverage")
    return {name:_site(methods[name],name) for name in CALLERS}

def report(sha1:str,sites:dict) -> dict:
    if sha1!=physical.EXPECTED_SHA1 or set(sites)!=set(CALLERS):
        raise SliceError("wrong binary identity or method population")
    return {
        "result":"PASS_SHA_EXACT_CONSERVATIVE_AEROPIC_RECEIVER_SLICE",
        "sha1":sha1,"provider":"wind_spellbooks","release":"1.0.5",
        "effect_class":EFFECT,"call_sites":sites,
        "sender_jvm_bytecode_redistributed":False,
        "iron_host_abi":"PUBLISHED_3163_VERIFIED_PR891",
        "installed_host_sha":"NOT_VERIFIED",
        "runtime_recast_dispatch":"NOT_PROVEN",
        "real_client_survival_qa":"NOT_TESTED",
        "safe_mutating_hook":"NOT_PROVEN",
        "limitations":[
            "a matching straight-line expression proves only a compiled Supplier return cast",
            "no supplier implementation or runtime receiver class proof",
            "no branch merge or arbitrary JVM dataflow is claimed",
            "no hook/cooldown/player-state intervention authorized",
        ],
    }

def audit(jar:Path)->dict:
    proof=physical.audit(jar)
    try:
        run=subprocess.run(["javap","-c","-p","-classpath",str(jar),EFFECT],
            capture_output=True,text=True,check=True,timeout=30)
    except (OSError,subprocess.TimeoutExpired,subprocess.CalledProcessError) as exc:
        raise SliceError("javap of frozen AeropicEffect failed") from exc
    return report(proof["sha1"],examine(methods_from_javap(run.stdout)))

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        data=audit(args.jar)
        status=0
    except (SliceError,physical.AuditError,OSError,ValueError,TypeError,KeyError) as exc:
        data={"result":"FAIL_CLOSED","reason":str(exc)}
        status=1
    payload=json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf8")
    print(payload)
    return status

if __name__=="__main__":
    raise SystemExit(main())
