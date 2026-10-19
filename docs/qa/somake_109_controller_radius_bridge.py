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

def direct_synched_radius_setter(body:list[str],accessor_name:str)->dict:
    """Entire seven-opcode method must write its sole float argument to accessor."""
    rows=opcode_rows(body)
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=7:return fail("setter_not_exact_seven_opcode_float_write")
    if [x[1] for x in rows]!=["aload_0","getfield","getstatic","fload_1",
                               "invokestatic","invokevirtual","return"]:
        return fail("setter_has_unknown_transform_or_control_flow")
    if rows[1][3]!="Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;":
        return fail("setter_data_field_not_proven")
    m=re.fullmatch(
        r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
        rows[2][3])
    if not m or m.group(2)!=accessor_name or m.group(1) not in (None,SELF_JVM_OWNER):
        return fail("setter_accessor_not_same_proved_getter")
    if rows[4][3]!="Method java/lang/Float.valueOf:(F)Ljava/lang/Float;":
        return fail("setter_float_box_not_proven")
    if rows[5][3]!=(
        "Method net/minecraft/network/syncher/SynchedEntityData.set:"
        "(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V"):
        return fail("setter_synched_data_set_not_proven")
    return {"status":"PROVED_DIRECT_FLOAT_SETTER_TO_SYNCED_RADIUS",
            "setter_parameter_local_slot":1,
            "accessor_field":accessor_name,
            "boundary":"setRadius(F)V writes its argument; caller and constructor remain separately audited."}

def direct_constructor_setter_call(body:list[str])->dict:
    """Only an immediately adjacent this + raw float constructor-local call."""
    rows=opcode_rows(body)
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if any(op.startswith(("if","goto","jsr")) or op in ("tableswitch","lookupswitch",
             "athrow","ret","wide") for _,op,_,_ in rows):
        return fail("constructor_conditional_provenance_not_supported")
    candidates=[]
    calls=0
    for i,(_,opcode,_,comment) in enumerate(rows):
        if opcode not in ("invokevirtual","invokespecial"):continue
        m=re.fullmatch(r"Method (?:(?:([A-Za-z0-9_/$]+))\.)?setRadius:\(F\)V",comment)
        if not m or m.group(1) not in (None,SELF_JVM_OWNER):
            continue
        calls+=1
        if i<2:continue
        first,second=rows[i-2:i]
        if local_id(first[1],first[2],"aload")!=0:continue
        slot=local_id(second[1],second[2],"fload")
        if slot in FLOAT_SLOTS:candidates.append(slot)
    if calls!=1 or len(candidates)!=1:
        return {"status":"NOT_PROVED","reason":"unique_raw_ctor_float_to_setRadius_not_proven",
                "setRadius_calls":calls,"direct_candidates":len(candidates)}
    return {"status":"PROVED_DIRECT_CTOR_FLOAT_ARGUMENT_TO_SETTER",
            "jvm_local_slot":candidates[0],
            **FLOAT_SLOTS[candidates[0]],
            "boundary":"Ctor passes this float to setRadius; onCast argument source not analyzed."}

def float_literal_f32(row:tuple)->float|None:
    """Only literals javap explicitly types as float, or JVM fconst_0..2."""
    _,op,_,comment=row
    if op in ("fconst_0","fconst_1","fconst_2"):
        return float(op[-1])
    if op not in ("ldc","ldc_w"):
        return None
    m=re.fullmatch(r"float (-?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)[fF]",comment)
    if not m:return None
    v=float(m.group(1))
    if not (-1_000_000<=v<=1_000_000):
        return None
    return v

def certified_clamped_synched_radius_setter(body:list[str],accessor_name:str)->dict:
    """Only exact ten-opcode this.entityData.set(DATA_RADIUS,Float.valueOf(clamp(arg,lo,hi)))."""
    rows=opcode_rows(body)
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=10:return fail("setter_not_exact_ten_opcode_clamp_write")
    if [r[1] for r in rows[:4]]!=["aload_0","getfield","getstatic","fload_1"]:
        return fail("setter_pre_clamp_provenance_not_proved")
    if [r[1] for r in rows[6:]]!=["invokestatic","invokestatic","invokevirtual","return"]:
        return fail("setter_clamp_box_and_write_order_not_proved")
    if rows[1][3]!="Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;":
        return fail("setter_entity_data_field_not_proved")
    m=re.fullmatch(
        r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
        rows[2][3])
    if not m or m.group(2)!=accessor_name or m.group(1) not in (None,SELF_JVM_OWNER):
        return fail("setter_accessor_not_same_proved_getter")
    lo=float_literal_f32(rows[4])
    hi=float_literal_f32(rows[5])
    if lo is None or hi is None or lo>hi:
        return fail("setter_clamp_literal_bounds_not_proved")
    if rows[6][3]!="Method net/minecraft/util/Mth.clamp:(FFF)F":
        return fail("setter_float_clamp_signature_not_proved")
    if rows[7][3]!="Method java/lang/Float.valueOf:(F)Ljava/lang/Float;":
        return fail("setter_float_box_not_proved")
    if rows[8][3]!=( "Method net/minecraft/network/syncher/SynchedEntityData.set:"
                     "(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V"):
        return fail("setter_synched_data_set_not_proved")
    return {"status":"PROVED_CLAMPED_FLOAT_SETTER_TO_SYNCED_RADIUS",
            "accessor_field":accessor_name,
            "setter_parameter_local_slot":1,
            "clamp_lower_float":lo,"clamp_upper_float":hi,
            "jvm_clamp_descriptor":"(FFF)F",
            "boundary":"Setter-local transformation only. Constructor argument, onCast and perk mutability not proven."}

def setter_structural_shape(body:list[str],accessor_name:str)->dict:
    """Bounded reference-level diagnostics; never claim float argument provenance."""
    rows=opcode_rows(body)
    if len(rows)>250:raise GateError("setter inspection budget exceeded")
    accessor_uses=0
    synced_sets=0
    float_boxes=0
    floads=set()
    invoked=set()
    branches=0
    numeric_ops=0
    for _,op,operand,comment in rows:
        slot=local_id(op,operand,"fload")
        if slot is not None:floads.add(slot)
        if op=="getstatic":
            m=re.fullmatch(
              r"Field (?:(?:([A-Za-z0-9_/$]+))\.)?([A-Za-z0-9_$]+):Lnet/minecraft/network/syncher/EntityDataAccessor;",
              comment)
            if m and m.group(2)==accessor_name and m.group(1) in (None,SELF_JVM_OWNER):
                accessor_uses+=1
        if op in ("invokestatic","invokevirtual","invokespecial","invokeinterface"):
            m=re.fullmatch(r"(?:Method|InterfaceMethod) (.{1,190})",comment)
            if not m:raise GateError("unrecognized setter JVM method symbol")
            invoked.add(m.group(1))
            if comment==("Method net/minecraft/network/syncher/SynchedEntityData.set:"
                         "(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V"):
                synced_sets+=1
            if comment=="Method java/lang/Float.valueOf:(F)Ljava/lang/Float;":
                float_boxes+=1
        if op.startswith(("if","goto","jsr")) or op in ("tableswitch","lookupswitch"):
            branches+=1
        if op in ("fadd","fsub","fmul","fdiv","frem","fneg","dadd","dsub",
                  "dmul","ddiv","drem","dneg","i2f","d2f","f2d","f2i","f2l"):
            numeric_ops+=1
    if len(invoked)>28 or len(floads)>12:raise GateError("setter symbol budget exceeded")
    return {
        "proof_status":"STRUCTURAL_ONLY_NO_SETTER_ARGUMENT_CAUSALITY",
        "instruction_count":len(rows),
        "owned_accessor_getstatic_count":accessor_uses,
        "synched_data_set_call_count":synced_sets,
        "float_box_call_count":float_boxes,
        "float_local_load_slots":sorted(floads),
        "branch_instruction_count":branches,
        "numeric_operation_or_conversion_count":numeric_ops,
        "return_instruction_count":sum(op=="return" for _,op,_,_ in rows),
        "invoked_method_symbols":sorted(invoked),
        "boundary":"Co-occurrence, even without arithmetic, is not a dataflow proof or public perk hook.",
    }

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

SPELL_FQCN="com.somake.somakespells.spells.blood.FuneralBloomSpell"
ONCAST_DESC=("(Lnet/minecraft/world/level/Level;ILnet/minecraft/world/entity/LivingEntity;"
             "Lio/redspace/ironsspellbooks/api/spells/CastSource;"
             "Lio/redspace/ironsspellbooks/api/magic/MagicData;)V")
GET_RADIUS_CALL_DESC="(ILnet/minecraft/world/entity/LivingEntity;)F"
CTOR_OWNER=FQCN.replace(".","/")
SPELL_OWNER=SPELL_FQCN.replace(".","/")

def descriptor_types(descriptor:str)->tuple[list[str],str]:
    """Parse exact JVM method descriptors, rejecting unsupported or malformed types."""
    if not descriptor.startswith("(") or ")" not in descriptor:
        raise GateError("malformed method descriptor")
    end=descriptor.index(")")
    raw=descriptor[1:end]
    result=[]
    pos=0
    while pos<len(raw):
        start=pos
        while pos<len(raw) and raw[pos]=="[":pos+=1
        if pos>=len(raw):raise GateError("incomplete array type")
        if raw[pos]=="L":
            terminator=raw.find(";",pos)
            if terminator<0:raise GateError("unterminated reference type")
            pos=terminator+1
        elif raw[pos] in "BCDFIJSZ":
            pos+=1
        else:
            raise GateError("invalid descriptor argument")
        result.append(raw[start:pos])
        if len(result)>18:raise GateError("too many arguments")
    ret=descriptor[end+1:]
    if not re.fullmatch(r"(?:V|[BCDFIJSZ]|\[*L[A-Za-z0-9_/$]+;|\[[BCDFIJSZ])",ret):
        raise GateError("invalid descriptor return")
    return result,ret

def oncast_controller_radius_argument(body:list[str])->dict:
    """Prove only a bounded straight-line NEW→INVOKESPECIAL constructor stack slice.

    Does not inspect, serialize or return third-party implementation/bytecode.
    Unsupported opcodes, branches and local provenance all fail closed.
    """
    rows=opcode_rows(body)
    expected_ctor="Method "+CTOR_OWNER+'."<init>":'+CONSTRUCTOR_DESC
    newclass="class "+CTOR_OWNER
    starts=[i for i,r in enumerate(rows) if r[1]=="new" and r[3]==newclass]
    ends=[i for i,r in enumerate(rows) if r[1]=="invokespecial" and r[3]==expected_ctor]
    def stop(reason,**metadata):
        return {"status":"NOT_PROVED","reason":reason,**metadata}
    if len(starts)!=1 or len(ends)!=1 or starts[0]>=ends[0]:
        return stop("unique_controller_allocation_and_ctor_call_not_proved",
                    allocations=len(starts),constructor_calls=len(ends))
    start,end=starts[0],ends[0]
    lower,upper=rows[start][0],rows[end][0]
    # Reject any external control-flow ingress that can skip part of the window.
    # Local linearity alone cannot prove all predecessor stacks are equivalent.
    for i,(pc,op,operand,_) in enumerate(rows):
        if start<=i<=end:continue
        if op.startswith(("if","goto")):
            target=operand.split(" ",1)[0]
            if not re.fullmatch(r"\\d+",target):
                return stop("unrecognized_external_branch_target")
            if lower<int(target)<=upper:
                return stop("external_branch_enters_constructor_argument_window")
        elif op in ("tableswitch","lookupswitch","jsr","ret","wide"):
            return stop("unsupported_external_control_flow")
    window=rows[start:end+1]
    if len(window)>65:return stop("constructor_window_budget_exceeded")
    if any((op.startswith(("if","goto","jsr")) or op in
            ("tableswitch","lookupswitch","athrow","ret","wide","monitorenter",
             "monitorexit","invokedynamic") or op.endswith("return"))
           for _,op,_,_ in window):
        return stop("non_linear_or_unsupported_constructor_argument_window",
                    instruction_count=len(window))
    stack=[]
    locals_seen={}
    def push(typ,tag):
        stack.append((typ,tag))
        if len(stack)>45:raise GateError("callsite stack budget exceeded")
    def pop(expected=None):
        if not stack:raise GateError("constructor window stack underflow")
        typ,tag=stack.pop()
        if expected is not None:
            if expected in ("I","F","D","J") and typ!=expected:
                raise GateError("callsite primitive stack type mismatch")
            if expected.startswith(("L","[")) and not typ.startswith(("L","[")):
                raise GateError("callsite reference stack type mismatch")
        return (typ,tag)
    try:
        for _,op,operand,comment in window:
            if op=="new":
                if comment!=newclass:raise GateError("nested allocation unmodelled")
                push("L"+CTOR_OWNER+";","uninit_controller")
            elif op=="dup":
                if not stack or not stack[-1][0].startswith(("L","[")):
                    raise GateError("unsafe reference dup")
                push(*stack[-1])
            elif op=="swap":
                if len(stack)<2 or stack[-1][0] in ("D","J") or stack[-2][0] in ("D","J"):
                    raise GateError("unsafe swap")
                stack[-1],stack[-2]=stack[-2],stack[-1]
            elif op=="pop":
                pop()
            elif any(op==root or re.fullmatch(root+r"_[0-3]",op)
                     for root in ("aload","iload","fload","dload","lload")):
                root=op.split("_",1)[0]
                slot=local_id(op,operand,root)
                if slot is None:raise GateError("unrecognized load slot")
                typ={"aload":"Ljava/lang/Object;","iload":"I",
                     "fload":"F","dload":"D","lload":"J"}[root]
                tag=("this_spell" if root=="aload" and slot==0 else
                     locals_seen.get(slot,(typ,"local_unknown"))[1])
                push(typ,tag)
            elif any(op==root or re.fullmatch(root+r"_[0-3]",op)
                     for root in ("astore","istore","fstore","dstore","lstore")):
                root=op.split("_",1)[0]
                slot=local_id(op,operand,root)
                if slot is None:raise GateError("unrecognized store slot")
                typ={"astore":"Ljava/lang/Object;","istore":"I",
                     "fstore":"F","dstore":"D","lstore":"J"}[root]
                locals_seen[slot]=pop(typ)
            elif op in ("aconst_null",):
                push("Ljava/lang/Object;","null")
            elif op in ("iconst_m1","iconst_0","iconst_1","iconst_2","iconst_3",
                        "iconst_4","iconst_5","bipush","sipush"):
                push("I","constant")
            elif op in ("fconst_0","fconst_1","fconst_2"):
                push("F","constant")
            elif op in ("dconst_0","dconst_1","lconst_0","lconst_1"):
                push("D" if op.startswith("d") else "J","constant")
            elif op in ("ldc","ldc_w","ldc2_w"):
                if comment.startswith("float "):typ="F"
                elif comment.startswith("double "):typ="D"
                elif comment.startswith("long "):typ="J"
                elif comment.startswith("int "):typ="I"
                elif comment.startswith(("String ","class ")):typ="Ljava/lang/Object;"
                else:raise GateError("unsupported constant type")
                push(typ,"constant")
            elif op in ("i2f","d2f","f2d","i2d","f2i"):
                source={"i2f":"I","d2f":"D","f2d":"F","i2d":"I","f2i":"F"}[op]
                out={"i2f":"F","d2f":"F","f2d":"D","i2d":"D","f2i":"I"}[op]
                pop(source);push(out,"derived")
            elif op in ("fadd","fsub","fmul","fdiv","iadd","isub","imul","idiv"):
                typ="F" if op.startswith("f") else "I"
                pop(typ);pop(typ);push(typ,"derived")
            elif op in ("getfield","getstatic"):
                m=re.fullmatch(r"Field [A-Za-z0-9_/$\.]+:([A-Za-z0-9_/$;\[]+)",comment)
                if not m:raise GateError("unrecognized field descriptor")
                if op=="getfield":pop("Ljava/lang/Object;")
                push(m.group(1),"field_unknown")
            elif op=="checkcast":
                typ,tag=pop("Ljava/lang/Object;")
                if not re.fullmatch(r"class [A-Za-z0-9_/$]+",comment):
                    raise GateError("unsafe checkcast symbol")
                push(typ,tag)
            elif op in ("invokevirtual","invokespecial","invokestatic","invokeinterface"):
                m=re.fullmatch(r"(?:Method|InterfaceMethod) ([^:]{1,350}):(\([^)]*\).{1,200})",comment)
                if not m:raise GateError("unrecognized invocation descriptor")
                method,desc=m.groups()
                argtypes,ret=descriptor_types(desc)
                arguments=[pop(t) for t in reversed(argtypes)][::-1]
                receiver=pop("Ljava/lang/Object;") if op!="invokestatic" else None
                if comment==expected_ctor:
                    if receiver!=( "L"+CTOR_OWNER+";","uninit_controller"):
                        raise GateError("constructor receiver is not new controller")
                    if len(arguments)!=10 or arguments[2][0]!="F" or arguments[7][0]!="F":
                        raise GateError("constructor signature/float slots inconsistent")
                    return {"status":(
                         "PROVED_ONCAST_GET_RADIUS_TO_FIRST_CTOR_FLOAT"
                         if arguments[2][1]=="spell_getRadius" else
                         "NOT_PROVED"),
                         "reason":("exact_getRadius_call_stack_argument"
                                   if arguments[2][1]=="spell_getRadius" else
                                   "first_ctor_float_source_not_exact_spell_getRadius"),
                         "first_float_argument_source":arguments[2][1],
                         "second_float_argument_source":arguments[7][1],
                         "constructor_argument_ordinal":3,
                         "controller_constructor_descriptor":CONSTRUCTOR_DESC,
                         "instruction_window_count":len(window),
                         "boundary":"onCast callsite only; downstream AABBs, mutability and provider-loaded QA unproved."}
                is_radius=(method in ("getRadius",SPELL_OWNER+".getRadius")
                           and desc==GET_RADIUS_CALL_DESC and
                           receiver is not None and receiver[1]=="this_spell")
                if ret!="V":
                    push(ret,"spell_getRadius" if is_radius else "other_method")
            else:
                raise GateError("unsupported callsite opcode "+op)
    except GateError as e:
        return stop("argument_provenance_not_modelled",classification=str(e),
                    instruction_count=len(window))
    return stop("constructor_call_not_reached")

def analyze(text:str,spell_javap:str|None=None)->dict:
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
    setters=[body for name,desc,body in rows if name=="setRadius" and desc=="(F)V"]
    setter=({"status":"NOT_PROVED","reason":"missing_or_ambiguous_setRadius"}
       if len(setters)!=1 or synced["status"]!="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
       else direct_synched_radius_setter(setters[0],synced["accessor_field"]))
    clamped_setter=({"status":"NOT_PROVED","reason":"missing_or_ambiguous_setRadius"}
       if len(setters)!=1 or synced["status"]!="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
       else certified_clamped_synched_radius_setter(setters[0],synced["accessor_field"]))
    ctor_call=({"status":"NOT_PROVED","reason":"setter_not_proven"}
       if setter["status"]!="PROVED_DIRECT_FLOAT_SETTER_TO_SYNCED_RADIUS"
          and clamped_setter["status"]!="PROVED_CLAMPED_FLOAT_SETTER_TO_SYNCED_RADIUS"
       else direct_constructor_setter_call(constructors[0][1]))
    setter_shape=(
        setter_structural_shape(setters[0],synced["accessor_field"])
        if len(setters)==1 and synced["status"]=="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
        else {"proof_status":"NOT_PROVED","reason":"setter_or_synced_accessor_unavailable"})
    oncast_proof={"status":"NOT_PROVED","reason":"onCast_javap_not_provided"}
    if spell_javap is not None:
        candidate=[body for name,desc,body in sections(spell_javap)
                   if name=="onCast"]
        if len(candidate)!=1:
            raise GateError("missing or ambiguous Somake onCast")
        oncast_proof=oncast_controller_radius_argument(candidate[0])
    return {
      "oncast_to_controller":oncast_proof,
      "setter_structure":setter_shape,
      "clamped_setter_to_synced_accessor":clamped_setter,
      "constructor_descriptor":CONSTRUCTOR_DESC,
      "constructor_float_argument_slots":[{"jvm_local_slot":slot,**v} for slot,v in FLOAT_SLOTS.items()],
      "getter_descriptor":GETTER_DESC,
      "getter":getter,
      "synced_data_getter":synced,
      "constructor_to_synced_accessor":synced_binding,
      "setter_to_synced_accessor":setter,
      "constructor_to_setter":ctor_call,
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
    spell=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),SPELL_FQCN],
                         capture_output=True,text=True,check=False,timeout=50)
    if spell.returncode or not spell.stdout or len(spell.stdout)>MAX_TEXT:
        raise GateError("Somake onCast class javap failed/oversized")
    proof=analyze(p.stdout,spell.stdout)
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("artifact changed")
    print("SOMAKE_CONTROLLER_RADIUS_BRIDGE",json.dumps(proof,sort_keys=True))
    status=("PASS_EXACT_SHA_DIRECT_CONSTRUCTOR_RADIUS_BRIDGE"
            if proof["constructor_to_getter"]["status"]=="PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING"
            else ("PASS_EXACT_SHA_CTOR_FLOAT_VIA_SYNCED_RADIUS_SETTER"
                  if (proof["setter_to_synced_accessor"]["status"]=="PROVED_DIRECT_FLOAT_SETTER_TO_SYNCED_RADIUS"
                      and proof["constructor_to_setter"]["status"]=="PROVED_DIRECT_CTOR_FLOAT_ARGUMENT_TO_SETTER")
                  else ("PASS_EXACT_SHA_CTOR_FLOAT_VIA_CLAMPED_SYNCED_RADIUS_SETTER"
                        if (proof["clamped_setter_to_synced_accessor"]["status"]=="PROVED_CLAMPED_FLOAT_SETTER_TO_SYNCED_RADIUS"
                            and proof["constructor_to_setter"]["status"]=="PROVED_DIRECT_CTOR_FLOAT_ARGUMENT_TO_SETTER")
                        else ("PASS_EXACT_SHA_CLAMPED_FLOAT_SETTER_CONSTRUCTOR_NOT_PROVED"
                              if proof["clamped_setter_to_synced_accessor"]["status"]=="PROVED_CLAMPED_FLOAT_SETTER_TO_SYNCED_RADIUS"
                              else ("PASS_EXACT_SHA_SYNCED_FLOAT_CONSTRUCTOR_BRIDGE"
                        if proof["constructor_to_synced_accessor"]["status"]=="PROVED_DIRECT_CONSTRUCTOR_FLOAT_TO_SYNCED_RADIUS"
                        else ("PASS_EXACT_SHA_SYNCED_FLOAT_GETTER_CONSTRUCTOR_BRIDGE_NOT_PROVED"
                              if proof["synced_data_getter"]["status"]=="PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER"
                              else "PASS_EXACT_SHA_OBSERVATIONAL_ONLY_BRIDGE_NOT_PROVED"))))))
    return {"status":status,
            "sha1":digest,"fqcn":FQCN,"evidence":proof,
            "limits":["onCast callsite proof is local to the certified invocation window; receiver-level, semantics and AABB operands remain separate.",
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
