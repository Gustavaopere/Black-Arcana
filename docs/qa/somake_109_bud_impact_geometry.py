#!/usr/bin/env python3
"""SHA-exact clean-room Somake 1.0.9 Funeral Bloom Bud impact geometry scout.

Only derived topological facts and bounded typed operand windows are emitted.
Provider source, bytecode, full disassembly, JAR and assets are never exported.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, zipfile
from pathlib import Path
from collections import Counter
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows

CLASS="com.somake.somakespells.entity.FuneralBloomBudEntity"
DESC="(Lnet/minecraft/server/level/ServerLevel;)V"
MAX_TEXT=1_400_000

def category(op,symbol):
    if not op.startswith("invoke"):return ""
    if "AABB.inflate:(DDD)" in symbol:return "aabb_inflate_DDD"
    if "getBoundingBox:()" in symbol:return "get_bounding_box"
    if "getEntitiesOfClass:" in symbol:return "query_living_entities"
    if "DamageSources.applyDamage:" in symbol:return "apply_damage"
    if "SpellHealEvent" in symbol:return "spell_heal_event"
    if ".heal:" in symbol:return "heal"
    if "MobEffects.WITHER" in symbol:return "wither"
    if ".addEffect:" in symbol:return "add_effect"
    if ".push:" in symbol:return "push"
    if "isAlliedTo:" in symbol:return "is_allied"
    if "getOwner:" in symbol:return "get_owner"
    if "getCaster:" in symbol:return "get_caster"
    if "getImpactDamage:" in symbol:return "get_impact_damage"
    if "getEntities:" in symbol:return "query_entities"
    m=re.search(r"(?:Method|InterfaceMethod) (?:[^ .]+\.)?([A-Za-z_$][A-Za-z0-9_$]*):\(",symbol)
    return "other_"+m.group(1) if m else "unknown"

def literal_tag(op,comment):
    if op.startswith(("ldc","bipush","sipush")):
        m=re.search(r"(?:double|float|int)\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)",comment)
        if m:return "bounded_numeric_constant:"+m.group(1)[:40]
        return "symbolic_literal"
    if re.fullmatch(r"[dfi]const_[0-5]",op):return op
    return ""

def impact_scout(declared):
    members=[body for name,desc,body in declared if name=="impact" and desc==DESC]
    if len(members)!=1:return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_impact_method"}
    rows=opcode_rows(members[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"unexpected_impact_instruction_count","instruction_count":len(rows)}
    calls=[{"index":i,"kind":category(op,comment)}
           for i,(_,op,_,comment) in enumerate(rows) if op.startswith("invoke")]
    grouped={tag:[item["index"] for item in calls if item["kind"]==tag]
             for tag in ("get_bounding_box","aabb_inflate_DDD","query_living_entities",
                         "apply_damage","spell_heal_event","heal","is_allied","get_owner",
                         "get_impact_damage","push","add_effect")}
    if len(grouped["aabb_inflate_DDD"])!=1 or not grouped["query_living_entities"]:
        return {"status":"NOT_PROVED","reason":"missing_nonunique_box_or_query",
                "inflates":len(grouped["aabb_inflate_DDD"]),"queries":len(grouped["query_living_entities"])}
    def window(site,back=14,ahead=9):
        start=max(0,site-back);end=min(len(rows),site+ahead+1)
        return [{"index":i,"opcode":rows[i][1],
                 "typed_value":literal_tag(rows[i][1],rows[i][3]),
                 "call":category(rows[i][1],rows[i][3]) if rows[i][1].startswith("invoke") else "",
                 "local_slot":(rows[i][2] if rows[i][1] in ("aload","astore","fload","fstore","dload","dstore","iload","istore") else "")}
                for i in range(start,end)]
    branches=[]
    position={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    for i,(_,op,arg,_) in enumerate(rows):
        if not (op.startswith(("if","goto"))):continue
        dest=arg.split(" ",1)[0] if arg else ""
        if not dest.isdecimal() or int(dest) not in position:
            return {"status":"NOT_PROVED","reason":"unresolved_impact_branch"}
        branches.append({"index":i,"op":op,"target_index":position[int(dest)]})
    return {
       "status":"OBSERVED_BUD_IMPACT_TOPOLOGY_ONLY",
       "instruction_count":len(rows),
       "calls_by_category":grouped,
       "calls_order":calls[:90],
       "conditional_count":sum(b["op"].startswith("if") for b in branches),
       "branch_indices":branches[:45],
       "aabb_window":window(grouped["aabb_inflate_DDD"][0]),
       "query_windows":[window(i,6,5) for i in grouped["query_living_entities"][:2]],
       "damage_windows":[window(i,8,5) for i in grouped["apply_damage"][:2]],
       "opcode_histogram":dict(sorted(Counter(op for _,op,_,_ in rows).items())),
       "boundary":"Observed shapes only. Box operand values, query identity, damage/heal branches, procs and hooks not proved",
    }


def prove_impact_box_and_query(declared):
    """Prove exact impact-position AABB operand dataflow, not damage reachability."""
    names=[b for n,d,b in declared if n=="impact" and d==DESC]
    if len(names)!=1:return {"status":"NOT_PROVED","reason":"impact_method_ambiguous"}
    rows=opcode_rows(names[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"impact_release_instruction_drift"}
    def fail(reason,**details):return {"status":"NOT_PROVED","reason":reason,**details}
    def local(i,kind,slot):
        _,op,arg,_=rows[i]
        return op==kind+"_"+str(slot) or (op==kind and arg==str(slot))
    def literal(i,value):
        _,op,_,comment=rows[i]
        m=re.fullmatch(r"double ([-+]?\d+(?:\.\d+)?)(?:d)?",comment)
        return op=="ldc2_w" and m is not None and float(m.group(1))==value
    exact_ctor='Method net/minecraft/world/phys/AABB."<init>":(Lnet/minecraft/world/phys/Vec3;Lnet/minecraft/world/phys/Vec3;)V'
    exact_inflate="Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"
    new_box=rows[16][1]=="new" and rows[16][3]=="class net/minecraft/world/phys/AABB"
    input_shape=(new_box and rows[17][1]=="dup" and local(18,"aload",2)
                 and local(19,"aload",2) and rows[20][1]=="invokespecial"
                 and rows[20][3]==exact_ctor)
    if not input_shape:
        return fail("AABB_constructor_or_impact_vec3_operands_mismatch",
                    new_box=new_box,slot2_arguments=local(18,"aload",2) and local(19,"aload",2),
                    constructor_symbol_matches=rows[20][3]==exact_ctor)
    if not (literal(21,1.75) and literal(22,1.35) and literal(23,1.75)
            and rows[24][1]=="invokevirtual" and rows[24][3]==exact_inflate
            and local(25,"astore",5)):
        return fail("AABB_expansion_literals_or_result_local_not_proved")
    exact_query=(
        "Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:"
        "(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;)Ljava/util/List;"
    )
    alt_query=(
        "Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:"
        "(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;"
    )
    query_symbol=rows[31][3]
    if not (local(28,"aload",1) and rows[29][1] in ("ldc","ldc_w")
            and rows[29][3]=="class net/minecraft/world/entity/LivingEntity"
            and local(30,"aload",5) and rows[31][1]=="invokevirtual"
            and query_symbol in (exact_query,alt_query)):
        return fail("inflated_AABB_local5_not_query_input",
                    server_argument_slot=local(28,"aload",1),
                    entity_class_is_living=rows[29][3]=="class net/minecraft/world/entity/LivingEntity",
                    aabb_argument_slot=local(30,"aload",5),
                    query_symbol_variant="two_args" if query_symbol==exact_query else
                    ("three_args" if query_symbol==alt_query else "unknown"))
    for i,(_,op,operand,_) in enumerate(rows):
        if 16<=i<=31:continue
        if op.startswith(("if","goto","jsr")):
            target=operand.split(" ",1)[0] if operand else ""
            if not target.isdecimal():return fail("unrecognized_branch_target")
            pcs={pc:j for j,(pc,_,_,_) in enumerate(rows)}
            t=pcs.get(int(target))
            if t is None:return fail("branch_target_missing")
            if 16<t<=31:return fail("external_branch_inside_box_dataflow")
        elif op in ("tableswitch","lookupswitch","ret","wide","jsr_w"):
            return fail("unsupported_control_flow")
    origin=(local(0,"aload",0) and rows[1][1]=="invokevirtual"
            and rows[1][3] in (
                "Method getImpactPosition:()Lnet/minecraft/world/phys/Vec3;",
                "Method com/somake/somakespells/entity/FuneralBloomBudEntity.getImpactPosition:()Lnet/minecraft/world/phys/Vec3;",
            )
            and local(2,"astore",2))
    return {
        "status":"PROVED_BUD_INFLATED_BOX_CONSUMED_BY_LIVING_ENTITY_QUERY",
        "impact_method_instruction_count":279,
        "impact_position_to_local2":origin,
        "aabb_constructor_operands":["local2_Vec3","local2_Vec3"],
        "inflate_double_xyz":["1.75","1.35","1.75"],
        "inflated_aabb_stored_local":5,
        "query_aabb_loaded_local":5,
        "query_entity_class":"LivingEntity",
        "query_descriptor_mode":"two_args" if query_symbol==exact_query else "three_args",
        "aabb_constructor_index":20,"inflate_index":24,
        "query_index":31,
        "boundary":"Geometry and query argument only. Per-target eligibility, actual impact damage, healing, status, targeting perks NOT proved.",
    }

def certify_exact_impact_geometry_109(proof):
    """Fail SHA-pinned 1.0.9 if the original bud AABB/query dataflow changes."""
    expected={
        "status":"PROVED_BUD_INFLATED_BOX_CONSUMED_BY_LIVING_ENTITY_QUERY",
        "impact_method_instruction_count":279,
        "impact_position_to_local2":True,
        "aabb_constructor_operands":["local2_Vec3","local2_Vec3"],
        "inflate_double_xyz":["1.75","1.35","1.75"],
        "inflated_aabb_stored_local":5,
        "query_aabb_loaded_local":5,
        "query_entity_class":"LivingEntity",
        "query_descriptor_mode":"two_args",
        "aabb_constructor_index":20,
        "inflate_index":24,
        "query_index":31,
        "boundary":"Geometry and query argument only. Per-target eligibility, actual impact damage, healing, status, targeting perks NOT proved.",
    }
    if not isinstance(proof,dict) or any(proof.get(key)!=v for key,v in expected.items()):
        raise GateError("Somake 1.0.9 bud impact geometry and query fingerprint drift")

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("Somake publisher filename/size invalid")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("publisher SHA mismatch")
    with zipfile.ZipFile(jar) as archive:
        names=archive.namelist()
        if len(set(names))!=len(names) or CLASS.replace(".","/")+".class" not in names:
            raise GateError("missing class or duplicate ZIP member")
        toml=archive.read("META-INF/neoforge.mods.toml")
        if len(toml)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",toml):
            raise GateError("mod id mismatch")
    j=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
          capture_output=True,text=True,timeout=60,check=False)
    if j.returncode or not j.stdout or len(j.stdout)>MAX_TEXT:
        raise GateError("javap failed or output exceeded budget")
    x=impact_scout(sections(j.stdout))
    if x.get("status")!="OBSERVED_BUD_IMPACT_TOPOLOGY_ONLY":
        raise GateError("impact topology unproved:"+x.get("reason","unknown"))
    geo=prove_impact_box_and_query(sections(j.stdout))
    print("SOMAKE_BUD_GEOMETRY_PROOF",json.dumps(geo,sort_keys=True))
    certify_exact_impact_geometry_109(geo)
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=sha:
        raise GateError("source artifact changed during inspection")
    return {"status":"SHA_EXACT_BUD_IMPACT_SCOUT","mod_id":"somakespells",
            "version":"1.0.9","sha1":sha,"impact":x,"geometry":geo,
            "limitations":"static topology only, no gameplay or provider per-player setter"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_BUD_IMPACT_SCOUT",json.dumps(result["impact"],sort_keys=True))
    print("SOMAKE_BUD_IMPACT_SHA",result["sha1"])
    print("SOMAKE_BUD_IMPACT_GEOMETRY_GATE","PASS_SHA_EXACT_1_75_1_35_1_75_TO_LIVING_QUERY")
if __name__=="__main__":
    main()
