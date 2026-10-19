#!/usr/bin/env python3
"""Somake 1.0.9: bounded exact-JAR float dataflow proof for Funeral Bloom.

A typed abstract interpreter processes a full straight-line method only when
every JVM instruction/stack operation is supported. It exports one symbolic
return expression or a fail-closed reason. Never emit disassembly or code.
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
from somake_109_cast_refs import DECL, DESC
from somake_109_funeral_bud_probe import isolate_named_methods
from somake_109_numeric_fingerprint import CODE, decode_numeric, fingerprint

FQCN = "com.somake.somakespells.spells.blood.FuneralBloomSpell"
TARGETS = {
    "getImpactDamage": "(ILnet/minecraft/world/entity/LivingEntity;)F",
    "getRadius": "(ILnet/minecraft/world/entity/LivingEntity;)F",
}
MAX_JAR_BYTES = 20_000_000
MAX_TEXT = 1_000_000
MAX_INSTRUCTIONS = 220
MAX_EXPRESSION_LENGTH = 1200

def decode_descriptor(desc: str) -> tuple[list[str],str]:
    m=re.fullmatch(r"\(([^)]*)\)(\[*[ZBCSIJFDV]|\[*L[^;]+;)",desc)
    if not m:
        raise GateError("unsupported JVM descriptor shape")
    argtext,rest=m.groups()
    args=[]
    i=0
    while i<len(argtext):
        c=argtext[i]
        if c=="[":
            while i<len(argtext) and argtext[i]=="[":
                i+=1
            if i>=len(argtext):
                raise GateError("invalid array descriptor")
            if argtext[i]=="L":
                end=argtext.find(";",i)
                if end<0:raise GateError("invalid object array descriptor")
                i=end+1
            else:
                if argtext[i] not in "ZBCSIJFD":raise GateError("bad primitive array")
                i+=1
            args.append("R")
        elif c=="L":
            end=argtext.find(";",i)
            if end<0:raise GateError("invalid object descriptor")
            args.append("R");i=end+1
        elif c in "ZBCSIJFD":
            args.append({"F":"F","D":"D","J":"J"}.get(c,"I"));i+=1
        else:
            raise GateError("unsupported argument type")
    result="R" if rest.startswith(("L","[")) else {"F":"F","D":"D","J":"J","V":"V"}.get(rest,"I")
    return args,result

def float_formula(body:list[str], desc:str)->dict:
    """Abstract interpretation of all instructions; no partial success."""
    def blocked(reason:str)->dict:
        return {"status":"NOT_PROVED","reason":reason}
    if desc!=TARGETS["getImpactDamage"]:
        return blocked("unsupported_selected_signature")
    parsed=[]
    for line in body:
        before,sep,after=line.partition("//")
        m=CODE.match(before)
        if m:parsed.append((m.group(1),(m.group(2) or "").strip(),after.strip() if sep else ""))
    if not 1<=len(parsed)<=MAX_INSTRUCTIONS:
        return blocked("instruction_budget")
    stack:list[tuple[str,str]]=[]
    locals_map={0:("R","this"),1:("I","level_input"),2:("R","caster")}
    calls=[]
    for idx,(opcode,operand,comment) in enumerate(parsed):
        if opcode.startswith(("if","goto","jsr")) or opcode in ("tableswitch","lookupswitch","athrow"):
            return blocked("branch_or_throw")
        try:
            numeric=decode_numeric(opcode,operand,comment)
        except GateError:
            return blocked("invalid_numeric_immediate")
        if numeric is not None:
            typ,num=numeric
            kind={"float":"F","int":"I","double":"D","long":"J"}[typ]
            if kind not in {"F","I"}:return blocked("unsupported_literal_type")
            stack.append((kind,num))
        elif re.fullmatch(r"[aif]load(?:_[0-9]+)?",opcode):
            k=re.search(r"_([0-9]+)$",opcode)
            local=int(k.group(1)) if k else int(operand) if operand.isdigit() else -1
            expected={"aload":"R","iload":"I","fload":"F"}[opcode[:5]]
            item=locals_map.get(local)
            if item is None or item[0]!=expected:return blocked("untracked_local_load")
            stack.append(item)
        elif re.fullmatch(r"[aif]store(?:_[0-9]+)?",opcode):
            k=re.search(r"_([0-9]+)$",opcode)
            local=int(k.group(1)) if k else int(operand) if operand.isdigit() else -1
            expected={"astore":"R","istore":"I","fstore":"F"}[opcode[:6]]
            if not stack or stack[-1][0]!=expected or local<3 or local>8:
                return blocked("unsupported_local_store")
            locals_map[local]=stack.pop()
        elif opcode in ("fadd","fsub","fmul","fdiv"):
            if len(stack)<2 or stack[-1][0]!="F" or stack[-2][0]!="F":
                return blocked("float_arithmetic_type")
            right=stack.pop()[1];left=stack.pop()[1]
            sym={"fadd":"+","fsub":"-","fmul":"*","fdiv":"/"}[opcode]
            stack.append(("F",f"({left}{sym}{right})"))
        elif opcode=="fneg":
            if not stack or stack[-1][0]!="F":return blocked("float_neg_type")
            stack.append(("F","(-"+stack.pop()[1]+")"))
        elif opcode=="i2f":
            if not stack or stack[-1][0]!="I":return blocked("i2f_type")
            stack.append(("F","float("+stack.pop()[1]+")"))
        elif opcode in ("invokevirtual","invokespecial","invokestatic","invokeinterface"):
            if not re.search(r"(?:Method|InterfaceMethod) (?:[A-Za-z0-9_/$]+\.)?getSpellPower:",comment):
                return blocked("unsupported_invocation")
            match=re.search(r"\.getSpellPower:(\([^)]*\)[^ ]+)",comment)
            if not match:return blocked("missing_spellpower_descriptor")
            try:
                argtypes,ret=decode_descriptor(match.group(1))
            except GateError:
                return blocked("unsupported_spellpower_signature")
            if ret!="F":return blocked("spellpower_return_not_float")
            count=len(argtypes)+(0 if opcode=="invokestatic" else 1)
            if len(stack)<count:return blocked("spellpower_stack_underflow")
            args=stack[-count:] if count else []
            if opcode!="invokestatic":
                if args[0][0]!="R":return blocked("spellpower_receiver_type")
                args=args[1:]
            if [x[0] for x in args]!=argtypes:return blocked("spellpower_argument_types")
            del stack[-count:]
            expr="spellPower("+",".join(x[1] for x in args)+")"
            stack.append(("F",expr));calls.append("getSpellPower")
        elif opcode=="freturn":
            if idx!=len(parsed)-1 or len(stack)!=1 or stack[0][0]!="F":
                return blocked("nonterminal_or_invalid_float_return")
            expression=stack.pop()[1]
            if len(expression)>MAX_EXPRESSION_LENGTH:
                return blocked("expression_too_long")
            return {"status":"PROVED_STRAIGHT_LINE_JVM_FLOAT_EXPRESSION",
                    "expression":expression,
                    "external_calls":calls,
                    "precision":"JVM float32 operations; expression is symbolic, not algebraic equivalence under arbitrary real numbers",
                    "limits":"Does not establish effective spell damage, event dispatch, active config, real caster power, player-scoped hook or perk admissibility."}
        else:
            return blocked("unsupported_opcode_"+opcode)
        if len(stack)>24 or len(calls)>5:
            return blocked("stack_or_external_call_budget")
    return blocked("no_return")

def selected_methods(javap_text:str)->dict[str,dict]:
    if not javap_text or len(javap_text)>MAX_TEXT:raise GateError("oversized javap")
    lines=isolate_named_methods(javap_text).splitlines()
    positions=[i for i,line in enumerate(lines) if DECL.match(line)]
    if not 1<=len(positions)<=150:raise GateError("invalid method declarations")
    records={}
    for index,start in enumerate(positions):
        end=positions[index+1] if index+1<len(positions) else len(lines)
        name=lines[start].strip().split("(",1)[0].rsplit(" ",1)[-1]
        if name not in TARGETS:continue
        matches=[m.group(1) for line in lines[start+1:end] if (m:=DESC.match(line))]
        if len(matches)!=1 or matches[0]!=TARGETS[name] or name in records:
            raise GateError("missing/ambiguous exact method descriptor")
        body=lines[start+1:end]
        stats=fingerprint(body)
        records[name]={
            "descriptor":matches[0],
            "numeric_literal_occurrences":stats["numeric_literal_occurrences"],
            "branch_instruction_count":stats["branch_instruction_count"],
            "direct_trailing_clamp_literals":stats["direct_trailing_clamp_literals"],
            "symbolic_dataflow":float_formula(body,matches[0]),
        }
    if set(records)!=set(TARGETS):raise GateError("missing required methods")
    if records["getRadius"]["symbolic_dataflow"]["status"]=="PROVED_STRAIGHT_LINE_JVM_FLOAT_EXPRESSION":
        raise GateError("branchy radius method must not be called straight-line")
    return records

def inspect(jar:Path)->dict:
    if not jar.is_file() or jar.is_symlink() or jar.name!=FILENAME:
        raise GateError("incorrect physical file")
    if not 100<jar.stat().st_size<MAX_JAR_BYTES:raise GateError("wrong JAR size")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("Somake exact SHA-1 mismatch")
    with zipfile.ZipFile(jar) as z:
        members=z.namelist()
        if len(members)!=len(set(members)):raise GateError("duplicate member")
        metadata=z.read("META-INF/neoforge.mods.toml")
        if len(metadata)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",metadata):
            raise GateError("mod ID mismatch")
        if FQCN.replace(".","/")+".class" not in members:raise GateError("missing exact class")
    p=subprocess.run(["javap","-c","-p","-s","-classpath",str(jar.resolve()),FQCN],
                     capture_output=True,text=True,timeout=50,check=False)
    if p.returncode or not p.stdout or len(p.stdout)>MAX_TEXT:raise GateError("javap failure/budget")
    rows=selected_methods(p.stdout)
    for name,row in rows.items():
        print("SOMAKE_FLOAT_DATAFLOW",name,json.dumps(row,sort_keys=True))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("artifact changed during run")
    return {
        "status":"PASS_EXACT_FLOAT_METHODS_WITH_FAIL_CLOSED_DATAFLOW",
        "sha1":digest,
        "class":FQCN,
        "methods":rows,
        "boundary":[
            "This result documents only method return expressions proven by complete abstract JVM interpretation.",
            "A failed proof remains explicitly NOT_PROVED, with no inferred formula.",
            "No third-party implementation, disassembly, classfile or JAR is committed or exported.",
            "No runtime damage, targeting, LOS, player-specific hook, cost or cooldown verified.",
        ]
    }

def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    result=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_FLOAT_GATE",result["status"],result["sha1"])

if __name__=="__main__":
    main()
