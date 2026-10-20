#!/usr/bin/env python3
"""Somake 1.0.9 radius consumer *references*, not inferred value propagation.

SHA-pinned, bounded javap method-level callsites for three exact classfiles.
No provider implementation, bytecode, classes, or JARs exported.
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
from somake_109_cast_refs import SYMBOL
from somake_109_funeral_bud_probe import isolate_named_methods

CLASSES={
    "spell":"com.somake.somakespells.spells.blood.FuneralBloomSpell",
    "controller":"com.somake.somakespells.entity.FuneralBloomControllerEntity",
    "bud":"com.somake.somakespells.entity.FuneralBloomBudEntity",
}
METHODS={
    "spell":("onCast","getRadius"),
    "controller":("tick","launchWave"),
    "bud":("tick","impact"),
}
KEYS={
    "radius":("getRadius:", "getRadius("),
    "spawn_controller":("FuneralBloomControllerEntity.",),
    "wave":("launchWave:", "FuneralBloomBudEntity."),
    "aabb":("AABB.inflate:", "getBoundingBox:", "AABB.<init>:"),
    "query":("getEntitiesOfClass:", "getEntities:", "distanceToSqr:"),
    "damage":("DamageSources.applyDamage:", "LivingEntity.hurt:", "getImpactDamage:"),
    "heal":("SpellHealEvent", "LivingEntity.heal:", "getHealing:"),
    "owner":("getOwner:", "getCaster:", "isAlliedTo:"),
}
MAX_TEXT=1_400_000
MAX_METHODS=180
MAX_METHOD_INSTRUCTIONS=2800
MAX_SYMBOLS_PER_METHOD=110
MAX_SYMBOL_LEN=900

def prove_wave_inflate_operands(body:list[str])->dict:
    """Certify a complete *local* JVM operand sequence, never world effects."""
    rows=opcode_rows(body)
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)>250:return fail("wave_method_exceeds_budget")
    inflate_symbol="Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"
    radius_symbols={
        "Method getRadius:()F",
        "Method com/somake/somakespells/entity/FuneralBloomControllerEntity.getRadius:()F",
    }
    inflates=[i for i,r in enumerate(rows) if r[1]=="invokevirtual" and r[3]==inflate_symbol]
    if len(inflates)!=1:return fail("unique_AABB_inflate_call_not_proved")
    idx=inflates[0]
    if idx<7:return fail("not_enough_instructions_for_aabb_arguments")
    getter_idx=[i for i,r in enumerate(rows) if r[1]=="invokevirtual" and r[3] in radius_symbols]
    before=[g for g in getter_idx if g<idx]
    def is_radius_triple(start):
        a,b,c=rows[start:start+3]
        return a[1]=="aload_0" and b[1]=="invokevirtual" and b[3] in radius_symbols and c[1]=="f2d"
    if idx>=9 and before==[idx-8,idx-5,idx-2] and all(
        is_radius_triple(j) for j in (idx-9,idx-6,idx-3)
    ):
        first=idx-9
        proof={
            "status":"PROVED_THREE_AABB_INFLATE_ARGUMENTS_FROM_CONTROLLER_RADIUS",
            "axes":["X","Y","Z"],"conversion":"F_TO_D",
            "source_method":"FuneralBloomControllerEntity.getRadius:()F",
            "aabb_method_descriptor":"(DDD)Lnet/minecraft/world/phys/AABB;",
            "certified_expression":"inflate(f2d(getRadius()),f2d(getRadius()),f2d(getRadius()))",
            "source_call_count":3,
        }
    elif idx>=7 and before==[idx-6,idx-2] and (
        is_radius_triple(idx-7) and is_radius_triple(idx-3)
    ):
        first=idx-7
        # Only typed constant creation can certify Y without dataflow beyond
        # this exact contiguous JVM argument sequence.
        from somake_109_numeric_fingerprint import decode_numeric
        import math
        _,op,operand,comment=rows[idx-4]
        literal=decode_numeric(op,operand,comment)
        if not literal or literal[0]!="double":
            return fail("vertical_double_argument_not_typed_constant")
        try: vertical=float(literal[1])
        except ValueError:return fail("invalid_vertical_double_literal")
        if not math.isfinite(vertical) or not -4096<=vertical<=4096:
            return fail("vertical_double_literal_nonfinite_or_unbounded")
        proof={
            "status":"PROVED_AABB_XZ_CONTROLLER_RADIUS_Y_LITERAL_DOUBLE",
            "radius_axes":["X","Z"],
            "vertical_double_literal":literal[1],
            "conversion":"F_TO_D",
            "source_method":"FuneralBloomControllerEntity.getRadius:()F",
            "aabb_method_descriptor":"(DDD)Lnet/minecraft/world/phys/AABB;",
            "source_call_count":2,
            "certified_expression":"inflate(f2d(getRadius()),vertical_literal_double,f2d(getRadius()))",
        }
    else:
        return fail("aabb_xyz_argument_producer_sequence_not_proved")
    # A branch to the *inside* of an expression could bypass a producer.
    # It would invalidate all claims even if the nearby opcodes matched.
    first_pc=rows[first][0]
    last_pc=rows[idx][0]
    for i,(pc,op,operand,_) in enumerate(rows):
        if first<=i<=idx:continue
        if op.startswith(("if","goto","jsr")):
            target=operand.split(" ",1)[0]
            if not re.fullmatch(r"\d+",target):
                return fail("unrecognized_external_branch_target")
            if first_pc<int(target)<=last_pc:
                return fail("external_branch_enters_argument_stack_window")
        elif op in ("tableswitch","lookupswitch","jsr_w","ret","wide"):
            return fail("unsupported_external_branch_topology")
    proof["method_instruction_count"]=len(rows)
    proof["boundary"]=(
        "Local AABB.inflate DDD operand provenance only. AABB receiver origin, "
        "query consumption, target eligibility, effective range and perk API NOT proved."
    )
    return proof


def wave_query_aabb_link(body:list[str])->dict:
    """Certify direct, bounded AABB return handoff into the exact entity query.

    The JVM stack already has ServerLevel and Class before the AABB receiver.
    Without intervening stack mutations, the inflated AABB remains the
    query's AABB argument. A predicate value is tracked independently.
    """
    rows=opcode_rows(body)
    def fail(reason,**extra):return {"status":"NOT_PROVED","reason":reason,**extra}
    if len(rows)>250:return fail("unbounded_wave_method")
    box="Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"
    query=("Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:"
           "(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;"
           "Ljava/util/function/Predicate;)Ljava/util/List;")
    box_indices=[i for i,r in enumerate(rows) if r[1]=="invokevirtual" and r[3]==box]
    query_indices=[i for i,r in enumerate(rows) if r[1]=="invokevirtual" and r[3]==query]
    if len(box_indices)!=1 or len(query_indices)!=1:
        return fail("nonunique_or_missing_box_or_query",inflate_call_count=len(box_indices),
                    entity_query_call_count=len(query_indices))
    start,end=box_indices[0],query_indices[0]
    if end<=start:return fail("query_not_after_box")
    between=rows[start+1:end]
    shape=[op for _,op,_,_ in between]
    from collections import Counter
    def window_summary():
        # Aggregate only: no publisher instruction sequence or JVM disassembly.
        loads=sorted(set(op for op in shape if op.startswith(("aload","iload","fload","dload"))))
        stores=sorted(set(op for op in shape if op.startswith(("astore","istore","fstore","dstore"))))
        methods=sorted(set(comment for _,op,_,comment in between if op.startswith("invoke")
                           and op!="invokedynamic"))
        dynamic=sorted(set(comment for _,op,_,comment in between if op=="invokedynamic"))
        return {"between_instruction_count":len(shape),"opcode_histogram":dict(sorted(Counter(shape).items())),
                "load_opcodes":loads[:20],"store_opcodes":stores[:20],
                "intervening_method_symbols":methods[:12],"lambda_descriptors":dynamic[:6]}
    if len(shape)>15:return fail("intervening_window_exceeds_budget",**window_summary())
    for i,(pc,op,operand,_) in enumerate(rows):
        if start<=i<=end:continue
        if op.startswith(("if","goto","jsr")):
            dest=operand.split()[0] if operand else ""
            if not re.fullmatch(r"\d+",dest):
                return fail("unknown_external_branch_target")
            if rows[start][0]<int(dest)<=rows[end][0]:
                return fail("external_branch_enters_query_window")
        elif op in ("tableswitch","lookupswitch","jsr_w","ret","wide"):
            return fail("unhandled_external_branch")
    if shape==["invokedynamic"] and re.fullmatch(
       r"InvokeDynamic #\d+:[A-Za-z0-9_$]+:\(\)Ljava/util/function/Predicate;",
       between[0][3]):
        mode="direct_stack"
    elif shape==["aload_0","invokedynamic"] and re.fullmatch(
       r"InvokeDynamic #\d+:[A-Za-z0-9_$]+:"
       r"\(Lcom/somake/somakespells/entity/FuneralBloomControllerEntity;\)"
       r"Ljava/util/function/Predicate;",between[1][3]):
        mode="captured_this_predicate"
    elif shape==["astore_3","new","dup","aload_1","ldc","aload_3",
                 "aload_0","aload_2","invokedynamic"]:
        # The return value of inflate is the top-of-stack AABB; astore_3
        # consumes it. No intervening write to slot 3 is possible in this
        # complete bounded window. aload_3 then supplies the exact query AABB.
        new_symbol=between[1][3]
        klass=between[4][3]
        pred=between[8][3]
        if not re.fullmatch(r"class [A-Za-z0-9_/$]+",new_symbol):
            return fail("unrecognized_collection_allocation_symbol")
        if klass!="class net/minecraft/world/entity/LivingEntity":
            return fail("query_entity_class_not_living_entity")
        if not re.fullmatch(
            r"InvokeDynamic #\d+:test:"
            r"\(Lcom/somake/somakespells/entity/FuneralBloomControllerEntity;"
            r"Lnet/minecraft/world/entity/LivingEntity;\)"
            r"Ljava/util/function/Predicate;",pred):
            return fail("predicate_capture_descriptor_unproven")
        mode="via_local_3"
    else:
        return fail("intervening_predicate_stack_not_certified",**window_summary())
    return {
        "status":"PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY",
        "inflate_call_count":1,"entity_query_call_count":1,
        "aabb_transport":mode,
        "predicate_semantics":"unknown_predicate_body",
        "between_instruction_count":len(shape),
        "query_descriptor":"(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
        "instruction_count":len(rows),
        "boundary":"Proves query AABB argument only. Predicate eligibility, returned targets, spawn and impact unproven.",
    }

def certify_exact_wave_query_109(proof:dict)->None:
    """Fail exact physical Somake release when certified wave query link drifts."""
    expected={
        "status":"PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY",
        "inflate_call_count":1,
        "entity_query_call_count":1,
        "aabb_transport":"via_local_3",
        "between_instruction_count":9,
        "query_descriptor":"(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
        "predicate_semantics":"unknown_predicate_body",
        "instruction_count":196,
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=value for k,value in expected.items()):
        raise GateError("Somake 1.0.9 exact wave-AABB local-3 query link drift")

def wave_radius_aabb_shape(body:list[str])->dict:
    """Return bounded callsite topology only; never infer values by co-occurrence."""
    rows=opcode_rows(body)
    if len(rows)>250:raise GateError("oversized Funeral Bloom wave method")
    radius=[];inflates=[]
    for i,(_,op,_,symbol) in enumerate(rows):
        if op in ("invokevirtual","invokespecial"):
            if symbol in (
                "Method getRadius:()F",
                "Method com/somake/somakespells/entity/FuneralBloomControllerEntity.getRadius:()F"):
                radius.append(i)
            if symbol=="Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;":
                inflates.append(i)
    if not radius or not inflates:
        return {"status":"NOT_PROVED","reason":"radius_or_inflate_not_found",
                "radius_call_count":len(radius),"inflate_call_count":len(inflates)}
    pairs=[(r,a) for r in radius for a in inflates if r<a]
    branch=sum(op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch")
               for _,op,_,_ in rows)
    if not pairs:
        return {"status":"NOT_PROVED","reason":"radius_does_not_precede_inflate",
                "radius_call_count":len(radius),"inflate_call_count":len(inflates)}
    r,a=min(pairs,key=lambda pair:pair[1]-pair[0])
    between=rows[r+1:a]
    callnames=sorted(set(symbol for _,op,_,symbol in between if op.startswith("invoke")))
    if len(callnames)>30:return {"status":"NOT_PROVED","reason":"intervening_method_symbol_budget"}
    return {
        "status":"STRUCTURAL_ONLY_NO_AABB_OPERAND_PROVENANCE",
        "radius_call_count":len(radius),
        "inflate_call_count":len(inflates),
        "radius_before_inflate":True,
        "instruction_count":len(rows),
        "f2d_instruction_count":sum(op=="f2d" for _,op,_,_ in rows),
        "branch_instruction_count":branch,
        "invokedynamic_instruction_count":sum(op=="invokedynamic" for _,op,_,_ in rows),
        "nearest_radius_to_inflate_instruction_gap":a-r-1,
        "intervening_method_symbols":callnames,
        "intervening_branch_instruction_count":sum(
            op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch")
            for _,op,_,_ in between),
        "intervening_float_to_double_count":sum(op=="f2d" for _,op,_,_ in between),
        "intervening_double_arithmetic_count":sum(op in
            ("dadd","dsub","dmul","ddiv","dneg","drem") for _,op,_,_ in between),
        "getter_to_inflate_gaps":sorted([a-x-1 for x in radius if x<a],reverse=True),
        "f2d_to_inflate_gaps":sorted([a-i-1 for i,row in enumerate(rows)
                                       if i<a and row[1]=="f2d"],reverse=True),
        "getter_receiver_is_controller_this":[
            bool(i>0 and rows[i-1][1]=="aload_0") for i in radius if i<a],
        "double_local_load_count_pre_inflate":sum(
            op=="dload" or re.fullmatch(r"dload_[0-3]",op) is not None
            for _,op,_,_ in rows[:a]),
        "double_local_store_count_pre_inflate":sum(
            op=="dstore" or re.fullmatch(r"dstore_[0-3]",op) is not None
            for _,op,_,_ in rows[:a]),
        "boundary":"Callsite order and opcode counts only; AABB DDD operand stack and world hitbox NOT proved."
    }

def certify_exact_wave_aabb_109(proof:dict)->None:
    """Hard-gate version-exact wave-axis evidence on every physical run."""
    expected={
        "status":"PROVED_AABB_XZ_CONTROLLER_RADIUS_Y_LITERAL_DOUBLE",
        "radius_axes":["X","Z"],
        "vertical_double_literal":"10.5",
        "source_call_count":2,
        "conversion":"F_TO_D",
        "source_method":"FuneralBloomControllerEntity.getRadius:()F",
        "aabb_method_descriptor":"(DDD)Lnet/minecraft/world/phys/AABB;",
        "method_instruction_count":196,
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("exact Somake 1.0.9 wave AABB XZ/Y operand proof drift")

def calls_in_method(body:list[str])->dict:
    """Only bytecode callsite comments; fields are separately counted."""
    if len(body)>4500:raise GateError("oversized method section")
    records=[]
    fields=[]
    dynamic_invokes=0
    opcount=0
    for line in body:
        before,sep,after=line.partition("//")
        match=re.match(r"^\s*\d+:\s+([a-z][a-z0-9_]*)(?:\s+.*?)?$",before)
        if match:
            opcount+=1
            if opcount>MAX_METHOD_INSTRUCTIONS:raise GateError("oversized method")
            op=match.group(1)
            if op.startswith("invoke") and not sep:
                raise GateError("invocation missing JVM symbol")
            if not sep:continue
            comment=after.strip()
            if len(comment)>MAX_SYMBOL_LEN:raise GateError("symbol oversized")
            sm=SYMBOL.match(comment)
            if op=="invokedynamic":
                if not re.match(r"^InvokeDynamic\s+#\d+:[^ ]+",comment):
                    raise GateError("invalid invokedynamic bootstrap descriptor")
                dynamic_invokes+=1
            elif op.startswith("invoke"):
                if not sm or sm.group(1) not in ("Method","InterfaceMethod"):
                    raise GateError("invocation missing JVM symbol for "+op)
                records.append(sm.group(2))
            elif op in ("getfield","putfield","getstatic","putstatic"):
                if sm and sm.group(1)=="Field":
                    fields.append(sm.group(2))
    if len(records)>MAX_SYMBOLS_PER_METHOD:raise GateError("unbounded callsites")
    return {
        "instruction_count":opcount,
        "invoke_count":len(records),
        "invokedynamic_count":dynamic_invokes,
        "callsite_symbols":sorted(set(records)),
        "field_symbols":sorted(set(fields))[:40],
        "classified":{category:sorted(set(x for x in records if any(k in x for k in keywords)))
                      for category,keywords in KEYS.items()},
    }

def lambda_selection_candidate_inventory(declared:list[tuple[str,str,list[str]]])->dict:
    """Fingerprint wave lambda candidates without assuming invokedynamic linkage."""
    if not isinstance(declared,list) or len(declared)>MAX_METHODS:
        raise GateError("unbounded method declarations for predicate candidates")
    found=[];seen=set()
    for name,descriptor,body in declared:
        if not re.fullmatch(r"lambda\$launchWave\$[0-9]+",name):continue
        key=(name,descriptor)
        if key in seen:raise GateError("duplicate wave lambda method signature")
        seen.add(key)
        if len(found)>=12:raise GateError("unbounded wave lambda candidate count")
        if not re.fullmatch(r"\([^)]{0,350}\)(?:[ZVIBCDFJS]|\[*L[A-Za-z0-9_/$]+;)",descriptor):
            raise GateError("wave lambda invalid or unsupported descriptor")
        opcodes=opcode_rows(body)
        if len(opcodes)>240:raise GateError("wave lambda method exceeds budget")
        inventory=calls_in_method(body)
        symbols=inventory["callsite_symbols"]
        fields=inventory["field_symbols"]
        found.append({
            "method":name,
            "descriptor":descriptor,
            "instruction_count":len(opcodes),
            "conditional_branch_count":sum(op.startswith("if") for _,op,_,_ in opcodes),
            "invoke_count":inventory["invoke_count"],
            "invokedynamic_count":inventory["invokedynamic_count"],
            "mentions_isValidTarget":any("isValidTarget:" in x for x in symbols),
            "mentions_getRadius":any("getRadius:" in x for x in symbols),
            "mentions_maxTargets":any("maxTargets:" in x for x in fields),
            "mentions_activeTargetIds":any("activeTargetIds:" in x for x in fields),
            "callsite_symbols":symbols[:35],
            "field_symbols":fields[:22],
        })
    if not found:
        return {"status":"NOT_PROVED","reason":"no_wave_lambda_method_candidate"}
    return {
        "status":"PREDICATE_HELPER_CANDIDATES_ONLY",
        "candidate_count":len(found),
        "candidates":sorted(found,key=lambda x:(x["method"],x["descriptor"])),
        "boundary":"BOOTSTRAP_BINDING_NOT_PROVED"
    }

def wave_predicate_branch_topology(declared:list[tuple[str,str,list[str]]])->dict:
    """Certify exact 1.0.9 Lambda0 boolean paths from typed JVM shape.

    Returns *derived* branch truth table, not native code, executable method
    bodies or the identities of the captured LivingEntity arguments.
    """
    desc="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
    bodies=[body for name,d,body in declared if name=="lambda$launchWave$0" and d==desc]
    if len(bodies)>1:raise GateError("ambiguous exact boolean Predicate helper")
    def fail(reason,**meta):return {"status":"NOT_PROVED","reason":reason,**meta}
    if not bodies:return fail("exact_boolean_helper_missing")
    rows=opcode_rows(bodies[0])
    if len(rows)>32:raise GateError("oversized boolean Predicate body")
    labels=[]
    for _,op,_,symbol in rows:
        if "isValidTarget:" in symbol:labels.append("isValidTarget")
        elif "LivingEntity.getUUID:" in symbol:labels.append("getUUID")
        elif "Set.contains:" in symbol:labels.append("Set.contains")
    branches=[op for _,op,_,_ in rows if op.startswith("if")]
    if labels!=["isValidTarget","getUUID","Set.contains"]:
        return fail("predicate_callsite_order_or_ownership_not_proved")
    if len(rows)!=15 or branches!=["ifeq","ifne"]:
        return fail("exact_wave_boolean_branch_shape_not_proved",
                    instruction_count=len(rows),conditional_opcodes=branches)
    exact_ops=["aload_0","aload_1","aload_2","invokevirtual","ifeq",
               "aload_0","getfield","aload_2","invokevirtual",
               "invokeinterface","ifne","iconst_1","goto","iconst_0","ireturn"]
    if [op for _,op,_,_ in rows]!=exact_ops:
        return fail("wave_boolean_stack_opcode_shape_not_proved",
                    instruction_count=len(rows),ordered_checks=labels,
                    conditional_opcodes=branches,
                    opcode_histogram={op:sum(r[1]==op for r in rows)
                                      for op in sorted(set(r[1] for r in rows))})
    sym=[r[3] for r in rows]
    if sym[3] not in (
        "Method isValidTarget:(Lnet/minecraft/world/entity/LivingEntity;"
        "Lnet/minecraft/world/entity/LivingEntity;)Z",
        "Method com/somake/somakespells/entity/FuneralBloomControllerEntity."
        "isValidTarget:(Lnet/minecraft/world/entity/LivingEntity;"
        "Lnet/minecraft/world/entity/LivingEntity;)Z",
    ):
        return fail("isValidTarget_owner_or_descriptor_unproved")
    if sym[6] not in (
        "Field activeTargetIds:Ljava/util/Set;",
        "Field com/somake/somakespells/entity/FuneralBloomControllerEntity."
        "activeTargetIds:Ljava/util/Set;",
    ):
        return fail("activeTargetIds_field_owner_or_descriptor_unproved")
    if sym[8] not in (
        "Method net/minecraft/world/entity/LivingEntity.getUUID:()Ljava/util/UUID;",
        "Method net/minecraft/world/entity/Entity.getUUID:()Ljava/util/UUID;",
    ):
        return fail("target_uuid_call_owner_or_descriptor_unproved")
    if sym[9] not in (
        "InterfaceMethod java/util/Set.contains:(Ljava/lang/Object;)Z",
        "Method java/util/Set.contains:(Ljava/lang/Object;)Z",
    ):
        return fail("set_contains_owner_or_descriptor_unproved")
    for i,targetindex in ((4,13),(10,13),(12,14)):
        word=rows[i][2].split(" ",1)[0]
        if not re.fullmatch(r"\d+",word) or int(word)!=rows[targetindex][0]:
            return fail("unexpected_predicate_branch_or_join_destination",
                        branch_ordinal={4:1,10:2,12:3}[i])
    return {
        "status":"PROVED_WAVE_PREDICATE_VALID_AND_NOT_ACTIVE",
        "method":"lambda$launchWave$0",
        "instruction_count":15,
        "ordered_checks":labels,
        "conditional_opcodes":branches,
        "conditional_destination_kinds":["boolean_0","boolean_0"],
        "boolean_return_count":1,
        "semantic_guards":["true_only_if_valid","false_if_active_uuid"],
        "return_constant_categories":["1","0"],
        "boolean_call_adjacent_to_branch":[True,True],
        "inferred_boolean_rule":"isValidTarget(capturedLivingEntityA,capturedLivingEntityB) && !activeTargetIds.contains(capturedLivingEntityB.getUUID())",
        "boundary":"Pure JVM boolean helper logic; actual captured role/teams/PvP and query target outcomes NOT proved.",
    }


def wave_predicate_bootstrap_binding(verbose:str, wave_body:list[str], inventory:dict)->dict:
    """Prove invokedynamic #0's LambdaMetafactory *symbolic* implementation target.

    Never infer boolean outcomes or copy third-party bytecode/implementation.
    """
    def reject(reason,**metadata):return {"status":"NOT_PROVED","reason":reason,**metadata}
    if not verbose or len(verbose)>MAX_TEXT:
        return reject("missing_or_unbounded_verbose_class")
    rows=opcode_rows(wave_body)
    invoke=(
        "InvokeDynamic #0:test:"
        "(Lcom/somake/somakespells/entity/FuneralBloomControllerEntity;"
        "Lnet/minecraft/world/entity/LivingEntity;)Ljava/util/function/Predicate;"
    )
    matching=[r for r in rows if r[1]=="invokedynamic" and r[3]==invoke]
    if len(matching)!=1:return reject("missing_or_ambiguous_query_predicate_dynamic_call")
    if inventory.get("status")!="PREDICATE_HELPER_CANDIDATES_ONLY":
        return reject("lambda_inventory_not_certified")
    desc="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
    candidates=[item for item in inventory.get("candidates",[])
                if item.get("method")=="lambda$launchWave$0"
                and item.get("descriptor")==desc]
    if len(candidates)!=1:return reject("boolean_predicate_helper_missing_from_inventory")
    start=re.search(r"(?m)^BootstrapMethods:\s*$",verbose)
    if not start:return reject("BootstrapMethods_attribute_missing")
    tail=verbose[start.end():]
    if len(tail)>120_000:return reject("bootstrap_metadata_exceeds_budget")
    headers=list(re.finditer(r"(?m)^  ([0-9]+): (.+)$",tail))
    if not 1<=len(headers)<=100:return reject("unbounded_or_missing_bootstrap_entries")
    target=[i for i,match in enumerate(headers) if match.group(1)=="0"]
    if len(target)!=1:return reject("ambiguous_bootstrap_index_zero")
    k=target[0]
    block=tail[headers[k].start():headers[k+1].start() if k+1<len(headers) else len(tail)]
    if len(block)>9000:return reject("bootstrap_entry_exceeds_budget")
    if "REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:" not in headers[k].group(2):
        return reject("wrong_lambda_bootstrap_factory")
    pattern=(
        r"(?m)^\s*#\d+ REF_invokeVirtual "
        r"com/somake/somakespells/entity/FuneralBloomControllerEntity"
        r"\.lambda\$launchWave\$0:"
        +re.escape(desc)+r"\s*$"
    )
    if len(re.findall(pattern,block))!=1:
        handles=re.findall(r"(?m)^\s*#\d+ (REF_invoke[A-Za-z]+) ([^\n]{1,350})",block)
        diagnostic=[{"kind":kind,"member":member}
                    for kind,member in handles if "lambda$launchWave$" in member]
        return reject("missing_or_ambiguous_exact_boolean_wave_helper_handle",
                      bootstrap0_wave_handles=diagnostic[:8],
                      bootstrap0_total_handles=len(handles))
    handle_lines=re.findall(r"(?m)^\s*#\d+ REF_invoke(?:Static|Virtual|Special|Interface) "
                            r"[^\n]{1,350}lambda\$launchWave\$[0-9]+:[^\n]*$",block)
    if len(handle_lines)!=1:return reject("other_wave_lambda_handle_inside_query_bootstrap")
    return {
        "status":"PROVED_QUERY_PREDICATE_BOOTSTRAP_TO_LAUNCHWAVE_LAMBDA0",
        "bootstrap_index":0,
        "implementation_method":"lambda$launchWave$0",
        "implementation_descriptor":desc,
        "helper_instruction_count":candidates[0]["instruction_count"],
        "helper_conditional_branch_count":candidates[0]["conditional_branch_count"],
        "references_isValidTarget":candidates[0]["mentions_isValidTarget"],
        "references_activeTargetIds":candidates[0]["mentions_activeTargetIds"],
        "boundary":"BODY_BRANCH_OUTCOMES_NOT_PROVED",
    }

def certify_exact_wave_predicate_109(link:dict, inventory:dict)->None:
    """Reject predicate bootstrap or method fingerprints other than exact 1.0.9."""
    predicate={
        "status":"PROVED_QUERY_PREDICATE_BOOTSTRAP_TO_LAUNCHWAVE_LAMBDA0",
        "bootstrap_index":0,
        "implementation_method":"lambda$launchWave$0",
        "implementation_descriptor":"(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
        "helper_instruction_count":15,
        "helper_conditional_branch_count":2,
        "references_isValidTarget":True,
        "references_activeTargetIds":True,
        "boundary":"BODY_BRANCH_OUTCOMES_NOT_PROVED",
    }
    if not isinstance(link,dict) or any(link.get(k)!=v for k,v in predicate.items()):
        raise GateError("Somake 1.0.9 Predicate bootstrap binding drift")
    if not isinstance(inventory,dict) or inventory.get("status")!="PREDICATE_HELPER_CANDIDATES_ONLY" or inventory.get("candidate_count")!=2:
        raise GateError("Somake 1.0.9 wave helper inventory count drift")
    candidates=inventory.get("candidates",[])
    if not isinstance(candidates,list) or len(candidates)!=2:
        raise GateError("Somake 1.0.9 wave helper set drift")
    expected=[
        {"method":"lambda$launchWave$0",
         "descriptor":"(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
         "instruction_count":15,"conditional_branch_count":2,
         "mentions_isValidTarget":True,"mentions_activeTargetIds":True},
        {"method":"lambda$launchWave$1",
         "descriptor":"(Lnet/minecraft/world/entity/LivingEntity;)D",
         "instruction_count":4,"conditional_branch_count":0,
         "mentions_isValidTarget":False,"mentions_activeTargetIds":False},
    ]
    for i,spec in enumerate(expected):
        candidate=candidates[i]
        if not isinstance(candidate,dict) or any(candidate.get(k)!=v for k,v in spec.items()):
            raise GateError("Somake 1.0.9 wave helper fingerprint drift")

def analyze_javap(text:str, label:str)->dict:
    if not text or len(text)>MAX_TEXT:raise GateError("oversized class output")
    declared=sections(isolate_named_methods(text))
    if len(declared)>MAX_METHODS:raise GateError("too many class methods")
    selected={}
    for name,desc,body in declared:
        if name not in METHODS[label]:continue
        key=name+desc
        if key in selected:raise GateError("duplicate selected signature")
        selected[key]=calls_in_method(body)
    for target in METHODS[label]:
        if not any(k.startswith(target+"(") for k in selected):
            raise GateError("missing focused method: "+label+"."+target)
    if len(selected)>14:raise GateError("excessive method overloads")
    report={"fqcn":CLASSES[label],"selected_methods":selected}
    if label=="controller":
        candidates=[body for name,desc,body in declared
                    if name=="launchWave" and desc=="(Lnet/minecraft/server/level/ServerLevel;)V"]
        if len(candidates)!=1:raise GateError("missing exact launchWave descriptor")
        report["wave_radius_aabb_shape"]=wave_radius_aabb_shape(candidates[0])
        report["wave_inflate_operand_proof"]=prove_wave_inflate_operands(candidates[0])
        report["wave_query_aabb_link"]=wave_query_aabb_link(candidates[0])
        report["wave_lambda_candidates"]=lambda_selection_candidate_inventory(declared)
        report["wave_predicate_branch_topology"]=wave_predicate_branch_topology(declared)
    return report

def certify_exact_consumer_surface(outcome:dict)->None:
    """Ensure exact version callsite relations do not silently change."""
    def single(label,method):
        methods=outcome[label]["selected_methods"]
        found=[row for key,row in methods.items() if key.startswith(method+"(")]
        if len(found)!=1:raise GateError("missing/ambiguous "+label+"."+method)
        return found[0]
    spell=single("spell","onCast")
    tick=single("controller","tick")
    wave=single("controller","launchWave")
    impact=single("bud","impact")
    def require(record,category,match,label):
        symbols=record["classified"][category]
        if not any(match in x for x in symbols):
            raise GateError("exact downstream callsite missing: "+label)
    require(spell,"radius","getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F","spell getter")
    require(spell,"spawn_controller",'''FuneralBloomControllerEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V''',"controller constructor")
    require(tick,"radius","getRadius:()F","controller.tick radius access")
    require(tick,"wave","launchWave:(Lnet/minecraft/server/level/ServerLevel;)V","controller wave dispatch")
    require(wave,"radius","getRadius:()F","wave radius access")
    require(wave,"aabb","AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;","wave AABB")
    require(wave,"query","getEntitiesOfClass:","wave targeting")
    require(wave,"wave",'''FuneralBloomBudEntity."<init>":''',"bud creation")
    require(impact,"aabb","AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;","impact AABB")
    require(impact,"query","getEntitiesOfClass:","impact target query")
    require(impact,"damage","DamageSources.applyDamage:","impact damage")
    require(impact,"heal","SpellHealEvent","impact heal event")
    if impact["classified"]["radius"]:
        raise GateError("unanticipated direct getRadius in bud impact")
    if spell["invokedynamic_count"]<1 or wave["invokedynamic_count"]<1:
        raise GateError("dynamic invocation fingerprint changed")

def inspect(jar:Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong Somake file")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("Somake release mismatch")
    with zipfile.ZipFile(jar) as z:
        members=z.namelist()
        if len(members)!=len(set(members)):raise GateError("duplicate zip members")
        meta=z.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("publisher modid mismatch")
        for cls in CLASSES.values():
            if cls.replace(".","/")+".class" not in members:raise GateError("missing class")
    outcome={}
    for label,cls in CLASSES.items():
        process=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),cls],
                               capture_output=True,text=True,timeout=50,check=False)
        if process.returncode or len(process.stdout)>MAX_TEXT:
            raise GateError("javap failed or exceeded budget: "+label)
        result=analyze_javap(process.stdout,label)
        if label=="controller":
            verbose=subprocess.run(["javap","-v","-p","-classpath",str(jar.resolve()),cls],
                                   capture_output=True,text=True,timeout=50,check=False)
            if verbose.returncode or not verbose.stdout or len(verbose.stdout)>MAX_TEXT:
                raise GateError("bounded controller bootstrap metadata unavailable")
            wave=[body for name,desc,body in sections(process.stdout)
                  if name=="launchWave" and desc=="(Lnet/minecraft/server/level/ServerLevel;)V"]
            if len(wave)!=1:raise GateError("ambiguous controller wave bootstrap caller")
            result["wave_predicate_bootstrap"]=wave_predicate_bootstrap_binding(
                verbose.stdout,wave[0],result["wave_lambda_candidates"])
        outcome[label]=result
        for method,metrics in result["selected_methods"].items():
            print("SOMAKE_RADIUS_CONSUMER",label,method,
                  "ops",metrics["instruction_count"],
                  "invokes",metrics["invoke_count"],"dynamic",metrics["invokedynamic_count"],
                  "classified",json.dumps(metrics["classified"],sort_keys=True),
                  "fields",json.dumps(metrics["field_symbols"]))
    certify_exact_consumer_surface(outcome)
    certify_exact_wave_aabb_109(outcome["controller"]["wave_inflate_operand_proof"])
    certify_exact_wave_query_109(outcome["controller"]["wave_query_aabb_link"])
    certify_exact_wave_predicate_109(outcome["controller"]["wave_predicate_bootstrap"],
                                    outcome["controller"]["wave_lambda_candidates"])
    print("SOMAKE_WAVE_RADIUS_AABB_SHAPE",json.dumps(outcome["controller"]["wave_radius_aabb_shape"],sort_keys=True))
    print("SOMAKE_WAVE_AABB_OPERANDS",json.dumps(outcome["controller"]["wave_inflate_operand_proof"],sort_keys=True))
    print("SOMAKE_WAVE_QUERY_AABB_LINK",json.dumps(outcome["controller"]["wave_query_aabb_link"],sort_keys=True))
    print("SOMAKE_WAVE_LAMBDA_CANDIDATES",json.dumps(outcome["controller"]["wave_lambda_candidates"],sort_keys=True))
    print("SOMAKE_WAVE_PREDICATE_BOOTSTRAP",json.dumps(outcome["controller"]["wave_predicate_bootstrap"],sort_keys=True))
    print("SOMAKE_WAVE_PREDICATE_EXACT_GATE", "PASS_EXACT_LAMBDA0_REF_INVOKEVIRTUAL_AND_HELPERS")
    print("SOMAKE_WAVE_PREDICATE_BRANCH_TOPOLOGY",json.dumps(outcome["controller"]["wave_predicate_branch_topology"],sort_keys=True))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("JAR changed")
    return {"status":"PASS_SHA_EXACT_WAVE_QUERY_PREDICATE_BOOTSTRAP_BOUND",
            "publisher_sha1":digest,"version":"1.0.9","mod_id":"somakespells",
            "scope":outcome,
            "limits":[
                "Method-level callsite and exact descriptors are pinned but NOT constructor-argument mapping or value propagation.",
                "Without dataflow, a radius getter call does NOT prove it is the radius of an AABB or projectile.",
                "No loaded modpack, live player, Survival, client or multiplayer evidence.",
                "No provider JAR, classfile, bytecode or implementation exported.",
                "No provider-native mutation or RPG perk adapter approved."
            ]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    data=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_RADIUS_CONSUMER_GATE",data["status"],data["publisher_sha1"])
if __name__=="__main__":
    main()
