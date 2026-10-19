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

def getter_structural_shape(body:list[str])->dict:
    """Bounded semantic aggregate; never export opcode sequence or raw method body."""
    rows=opcode_rows(body)
    if len(rows)>250:raise GateError("getter inspection budget exceeded")
    reads=set()
    invokes=set()
    math_count=0
    branch_count=0
    for _,op,_,comment in rows:
        if op=="getfield":
            name=field(comment)
            if name:reads.add(name)
        elif op.startswith("invoke"):
            m=re.fullmatch(r"(?:Method|InterfaceMethod) (.{1,190})",comment)
            if not m:raise GateError("unrecognized getter JVM method symbol")
            invokes.add(m.group(1))
        if op.startswith(("fadd","fsub","fmul","fdiv","dadd","dsub","dmul","ddiv","i2f","d2f","fneg","dneg")):
            math_count+=1
        if op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch"):
            branch_count+=1
    if len(reads)>18 or len(invokes)>28:
        raise GateError("getter symbol budget exceeded")
    return {
        "instruction_count":len(rows),
        "float_field_names_read":sorted(reads),
        "float_arithmetic_and_conversion_instructions":math_count,
        "branch_instruction_count":branch_count,
        "invoked_method_symbols":sorted(invokes),
        "float_return_instructions":sum(row[1]=="freturn" for row in rows),
        "proof_status":"STRUCTURAL_ONLY_NO_ARGUMENT_PROVENANCE",
    }

def synced_entity_float_getter(body:list[str])->dict:
    """Recognize the complete seven-opcode synced-data float retrieval, if present."""
    rows=opcode_rows(body)
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=7:return fail("not_seven_opcode_synced_float_getter")
    ops=[x[1] for x in rows]
    if ops!=["aload_0","getfield","getstatic","invokevirtual",
             "checkcast","invokevirtual","freturn"]:
        return fail("unrecognized_synced_float_getter_flow")
    data=re.fullmatch(
      r"Field (?:(?:[A-Za-z0-9_/$]+)\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/SynchedEntityData;",
      rows[1][3])
    accessor=re.fullmatch(
      r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
      rows[2][3])
    if not data or not accessor:
        return fail("synched_data_or_accessor_type_not_proven")
    if accessor.group(1) not in (None,SELF_JVM_OWNER):
        return fail("accessor_not_owned_by_controller")
    expected_get=(
      "Method net/minecraft/network/syncher/SynchedEntityData.get:"
      "(Lnet/minecraft/network/syncher/EntityDataAccessor;)Ljava/lang/Object;")
    expected_float="Method java/lang/Float.floatValue:()F"
    if rows[3][3]!=expected_get or rows[4][3]!="class java/lang/Float" or rows[5][3]!=expected_float:
        return fail("synched_data_get_or_float_unbox_signature_not_proven")
    return {
      "status":"PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER",
      "entity_data_field":data.group(1),
      "accessor_field":accessor.group(2),
      "accessor_owner":accessor.group(1) or SELF_JVM_OWNER,
      "value_conversion":"java/lang/Float.floatValue:()F",
      "boundary":"Read-only getter dataflow; constructor EntityData.set and onCast args remain unproved.",
    }

def synced_radius_constructor_setter(body:list[str],accessor_field:str)->dict:
    """Prove a unique, adjacent JVM float argument -> synced accessor set call."""
    rows=opcode_rows(body)
    if len(rows)>700:return {"status":"NOT_PROVED","reason":"constructor_instruction_budget"}
    if any(op.startswith(("if","goto","jsr")) or op in
           ("tableswitch","lookupswitch","athrow","ret","wide") for _,op,_,_ in rows):
        return {"status":"NOT_PROVED","reason":"conditional_constructor_dataflow_not_supported"}
    if sum(op=="return" for _,op,_,_ in rows)!=1 or rows[-1][1]!="return":
        return {"status":"NOT_PROVED","reason":"ambiguous_constructor_return"}
    set_desc=(
      "Method net/minecraft/network/syncher/SynchedEntityData.set:"
      "(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V")
    data_field=(
      "Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;")
    box_float="Method java/lang/Float.valueOf:(F)Ljava/lang/Float;"
    candidates=[]
    seen_accessors=0
    for i,(_,op,_,comment) in enumerate(rows):
        if op!="getstatic":continue
        m=re.fullmatch(
          r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
          comment)
        if not m or m.group(2)!=accessor_field or m.group(1) not in (None,SELF_JVM_OWNER):
            continue
        seen_accessors+=1
        if i<2 or i+3>=len(rows):continue
        pre=rows[i-2:i]
        aft=rows[i+1:i+4]
        if local_id(pre[0][1],pre[0][2],"aload")!=0:
            continue
        if pre[1][1]!="getfield" or pre[1][3]!=data_field:
            continue
        slot=local_id(aft[0][1],aft[0][2],"fload")
        if slot not in FLOAT_SLOTS:continue
        if (aft[1][1],aft[1][3])!=("invokestatic",box_float):continue
        if (aft[2][1],aft[2][3])!=("invokevirtual",set_desc):continue
        candidates.append(slot)
    if seen_accessors!=1 or len(candidates)!=1:
        return {"status":"NOT_PROVED","reason":"unique_direct_synched_set_not_proved",
                "accessor_reads":seen_accessors,"matching_assignments":len(candidates)}
    return {"status":"PROVED_DIRECT_CONSTRUCTOR_FLOAT_TO_SYNCED_RADIUS",
            "accessor_field":accessor_field,
            "jvm_local_slot":candidates[0],
            **FLOAT_SLOTS[candidates[0]],
            "boundary":"Ctor-level call only; onCast argument mapping and subsequent setter writes remain unknown."}

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

def synced_accessor_method_inventory(methods:list,accessor_name:str)->dict:
    """Method-level symbols only; no code, offsets, control/data flow exported."""
    found=[]
    for name,desc,body in methods:
        rows=opcode_rows(body)
        direct_accessors=0
        set_calls=0
        boxed_float_calls=0
        floads=set()
        for _,op,operand,comment in rows:
            if op=="getstatic":
                m=re.fullmatch(
                  r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
                  comment)
                if m and m.group(2)==accessor_name and m.group(1) in (None,SELF_JVM_OWNER):
                    direct_accessors+=1
            if op=="invokevirtual" and comment==(
              "Method net/minecraft/network/syncher/SynchedEntityData.set:"
              "(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V"):
                set_calls+=1
            if op=="invokestatic" and comment=="Method java/lang/Float.valueOf:(F)Ljava/lang/Float;":
                boxed_float_calls+=1
            fl=local_id(op,operand,"fload")
            if fl is not None:floads.add(fl)
        if direct_accessors or set_calls:
            found.append({"method":name,"descriptor":desc,
                          "direct_getstatic_accessor_count":direct_accessors,
                          "synched_data_set_call_count":set_calls,
                          "float_box_call_count":boxed_float_calls,
                          "float_local_load_slots":sorted(floads)})
    if len(found)>35:raise GateError("excess accessor method report")
    return {"status":"STRUCTURAL_METHOD_REFERENCE_DISCOVERY_ONLY",
            "accessor":accessor_name,
            "methods_examined":len(methods),
            "methods_with_relevant_symbols":found,
            "limits":"Co-occurrence is not proof that the accessor is passed to set or that the float comes from a constructor slot."}

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
    synced=synced_entity_float_getter(getters[0][1])
    synced_binding=({"status":"NOT_PROVED","reason":"no_certified_synched_accessor"}
         if synced["status"]!="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
         else synced_radius_constructor_setter(constructors[0][1],synced["accessor_field"]))
    return {
      "constructor_descriptor":CONSTRUCTOR_DESC,
      "constructor_float_argument_slots":[{"jvm_local_slot":slot,**v} for slot,v in FLOAT_SLOTS.items()],
      "getter_descriptor":GETTER_DESC,
      "getter":getter,
      "synced_data_getter":synced,
      "constructor_to_synced_accessor":synced_binding,
      "synced_accessor_method_inventory":(
          synced_accessor_method_inventory(rows,synced["accessor_field"])
          if synced["status"]=="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
          else {"status":"NOT_PROVED","reason":"getter_accessor_not_certified"}),
      "getter_structure":getter_structural_shape(getters[0][1]),
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
            else ("PASS_EXACT_SHA_SYNCED_FLOAT_CONSTRUCTOR_BRIDGE"
                  if proof["constructor_to_synced_accessor"]["status"]=="PROVED_DIRECT_CONSTRUCTOR_FLOAT_TO_SYNCED_RADIUS"
                  else ("PASS_EXACT_SHA_SYNCED_FLOAT_GETTER_CONSTRUCTOR_BRIDGE_NOT_PROVED"
                        if proof["synced_data_getter"]["status"]=="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
                        else "PASS_EXACT_SHA_OBSERVATIONAL_ONLY_BRIDGE_NOT_PROVED")))
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
