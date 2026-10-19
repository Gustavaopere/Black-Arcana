#!/usr/bin/env python3
"""Somake 1.0.9: strictly local JVM bridge between constructor float args and controller getter.

A field is certified ONLY if the getter is a complete direct aload_0/getfield/freturn
and the constructor has a unique adjacent aload_0/fload/putfield assignment to it.
Does NOT infer upstream onCast argument mapping or downstream AABB.inflate operands.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows

FQCN="com.somake.somakespells.entity.FuneralBloomControllerEntity"
CONSTRUCTOR="FuneralBloomControllerEntity"
CONSTRUCTOR_DESC="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V"
GETTER_DESC="()F"
FLOAT_SLOTS={3:{"argument":3,"float_ordinal":1},8:{"argument":8,"float_ordinal":2}}
MAX_TEXT=1_400_000
MAX_JAR_BYTES=20_000_000

def local_id(opcode:str, operand:str,stem:str)->int|None:
    if opcode==stem:
        return int(operand) if re.fullmatch(r"\d+",operand) else None
    m=re.fullmatch(re.escape(stem)+r"_([0-3])",opcode)
    return int(m.group(1)) if m else None

SELF_JVM_OWNER=FQCN.replace(".","/")

def field(comment:str)->str|None:
    """Accept unqualified same-class javap symbols or the exact owner only."""
    m=re.fullmatch(r"Field (?:(?P<owner>[A-Za-z0-9_/$]+)\.)?(?P<name>[A-Za-z0-9_$]+):F",comment)
    if not m:return None
    owner=m.group("owner")
    if owner is not None and owner!=SELF_JVM_OWNER:return None
    return m.group("name")

def direct_float_getter(body:list[str])->dict:
    rows=opcode_rows(body)
    if len(rows)!=3:return {"status":"NOT_PROVED","reason":"getter_is_not_exact_three_opcode_direct_field_read"}
    a,b,c=rows
    if local_id(a[1],a[2],"aload")!=0 or b[1]!="getfield" or c[1]!="freturn":
        return {"status":"NOT_PROVED","reason":"non_direct_getter_opcodes"}
    name=field(b[3])
    if not name:return {"status":"NOT_PROVED","reason":"missing_typed_float_field"}
    return {"status":"PROVED_DIRECT_INSTANCE_FLOAT_GETTER","field":name}

def constructor_direct_assignments(body:list[str], target_field:str)->dict:
    rows=opcode_rows(body)
    opcodes=[row[1] for row in rows]
    if any(op.startswith(("if","goto","jsr")) or op in
           ("tableswitch","lookupswitch","athrow","ret","wide") for op in opcodes):
        return {"status":"NOT_PROVED","reason":"constructor_contains_conditional_or_unsupported_control_flow"}
    if opcodes.count("return")!=1 or opcodes[-1]!="return":
        return {"status":"NOT_PROVED","reason":"constructor_has_nonterminal_or_ambiguous_return"}
    assignments=[]
    touched=0
    for i,row in enumerate(rows):
        if row[1]!="putfield" or field(row[3])!=target_field:continue
        touched+=1
        if i<2:continue
        a,b=rows[i-2:i]
        if local_id(a[1],a[2],"aload")!=0:continue
        slot=local_id(b[1],b[2],"fload")
        if slot not in FLOAT_SLOTS:continue
        assignments.append(slot)
    if touched!=1 or len(assignments)!=1:
        return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_direct_constructor_field_binding",
                "field_write_count":touched,"direct_candidate_count":len(assignments)}
    slot=assignments[0]
    return {"status":"PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING",
            "field":target_field,"jvm_local_slot":slot,
            **FLOAT_SLOTS[slot]}

def analyze(text:str)->dict:
    if not text or len(text)>MAX_TEXT:raise GateError("javap length invalid")
    rows=sections(text)
    constructors=[(desc,body) for name,desc,body in rows
                  if name.rsplit(".",1)[-1]==CONSTRUCTOR and desc==CONSTRUCTOR_DESC]
    getters=[(desc,body) for name,desc,body in rows if name=="getRadius" and desc==GETTER_DESC]
    if len(constructors)!=1 or len(getters)!=1:
        raise GateError("missing or ambiguous exact ctor/getRadius descriptor")
    getter=direct_float_getter(getters[0][1])
    binding=({"status":"NOT_PROVED","reason":"no_certified_getter_field"}
             if getter["status"]!="PROVED_DIRECT_INSTANCE_FLOAT_GETTER"
             else constructor_direct_assignments(constructors[0][1],getter["field"]))
    return {
      "constructor_descriptor":CONSTRUCTOR_DESC,
      "constructor_float_argument_slots":[{"jvm_local_slot":slot,**v} for slot,v in FLOAT_SLOTS.items()],
      "getter_descriptor":GETTER_DESC,
      "getter":getter,
      "constructor_to_getter":binding,
      "boundary":"Only direct local-argument store and field getter; caller stack and inflate dataflow not proven."
    }

def inspect(jar:Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<MAX_JAR_BYTES:
        raise GateError("incorrect Somake 1.0.9 artifact")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("publisher SHA mismatch")
    with zipfile.ZipFile(jar) as z:
        entries=z.namelist()
        if len(entries)!=len(set(entries)):raise GateError("duplicate archive members")
        meta=z.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("wrong mod ID")
        if FQCN.replace(".","/")+".class" not in entries:raise GateError("missing controller class")
    p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),FQCN],
                     capture_output=True,text=True,check=False,timeout=50)
    if p.returncode or not p.stdout or len(p.stdout)>MAX_TEXT:raise GateError("javap failed/oversized")
    proof=analyze(p.stdout)
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("artifact changed")
    print("SOMAKE_CONTROLLER_RADIUS_BRIDGE",json.dumps(proof,sort_keys=True))
    status=("PASS_EXACT_SHA_DIRECT_CONSTRUCTOR_RADIUS_BRIDGE"
            if proof["constructor_to_getter"]["status"]=="PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING"
            else "PASS_EXACT_SHA_OBSERVATIONAL_ONLY_BRIDGE_NOT_PROVED")
    return {"status":status,
            "sha1":digest,"fqcn":FQCN,"evidence":proof,
            "limits":["Independent controller getter/constructor analysis, not onCast value provenance.",
                      "A direct float binding is not a player-accessible setter or mutable perk API.",
                      "No wave.inflate, bud.impact AABB argument propagation, loaded server or client proven.",
                      "No JAR, JVM disassembly, classfile, code or assets included."]}
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    x=a.parse_args()
    data=inspect(x.jar)
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_CONTROLLER_RADIUS_BRIDGE_GATE",data["status"],data["sha1"])
if __name__=="__main__":main()
