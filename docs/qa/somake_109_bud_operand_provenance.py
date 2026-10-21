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
    if evidence["status"]!="OBSERVED_TYPED_OPERAND_WINDOWS_ONLY":
        raise GateError("operand scouting failed")
    return {"sha1":digest,"version":"1.0.9","mod_id":"somakespells",
            "scout":evidence,"boundary":"Read-only native compiled observation, NOT provider runtime/behavior"}

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

if __name__=="__main__":
    main()
