#!/usr/bin/env python3
"""SHA-exact clean-room controller-field provenance survey for Somake 1.0.9.

Metadata limited to method descriptors, field operations, typed numeric/local
operand windows and Set call categories. No JAR, classfiles, method bodies,
source, third-party assets or unrestricted disassembly leave the CI runner.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows
from somake_109_bud_wither_construction import (
    CONTROLLER,BUD,certify_wither_constructor_handoff,
    certify_exact_wither_handoff_109,
)
from somake_109_bud_operand_provenance import operand_contract,certify_exact_bud_operand_contract_109
from somake_109_wave_maxtargets import prove_wave_list_cap,certify_exact_wave_list_cap_109,prove_wave_loop_spawn_sites,certify_exact_wave_loop_109

FIELDS={"witherDuration","witherAmplifier","impactDamage","activeTargetIds"}
MAX_TEXT=1_500_000
def field(row):
    _,op,_,comment=row
    if op not in ("putfield","getfield","getstatic","putstatic"):return None
    m=re.search(r"\bField (?:[\w/$]+\.)?([\w$]+):([^\s]+)",comment)
    return (m.group(1),m.group(2)) if m else None

def token(i,row):
    _,op,operand,comment=row
    item={"index":i,"op":op}
    m=re.match(r"^([a-z]+)(?:load|store)_([0-9]+)$",op)
    if m:item["slot"]=int(m.group(2))
    elif op in ("aload","astore","iload","istore","fload","fstore","dload","dstore"):
        if operand.isdecimal():item["slot"]=int(operand)
    elif op=="iinc":
        m=re.fullmatch(r"(\d+),\s*(-?\d+)",operand)
        if m:item["slot"]=int(m.group(1));item["increment"]=int(m.group(2))
    elif op.startswith("iconst_"):item["constant"]=op.removeprefix("iconst_")
    elif op in ("bipush","sipush") and operand.lstrip("-").isdigit():item["constant"]=int(operand)
    elif op.startswith("ldc"):
        m=re.search(r"\b(?:float|double|int|long) ([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",comment)
        if m:item["constant"]=m.group(1)
    f=field(row)
    if f:item["field"],item["descriptor"]=f
    if op.startswith("invoke"):
        m=re.search(r"(?:Method|InterfaceMethod) ([^:]+):(\([^ ]*\)[^ ]+)",comment)
        if m:
            item["call"]=m.group(1).rsplit(".",1)[-1].replace('"',"")[:85]
            item["descriptor"]=m.group(2)[:150]
            if m.group(1).startswith("java/util/Set.") or ".Set." in m.group(1):item["family"]="set"
            if "FuneralBloom" in m.group(1):item["family"]="funeral_bloom"
    return item

def scan(methods):
    found=[]
    for name,desc,body in methods:
        rows=opcode_rows(body)
        targets=[(i,f[0],f[1],op) for i,(pc,op,operand,comment) in enumerate(rows)
                 if (f:=field(rows[i])) is not None and f[0] in FIELDS]
        if not targets:continue
        if len(targets)>45:return {"status":"NOT_PROVED","reason":"too_many_field_operations"}
        blocks=[]
        for i,fn,fd,operation in targets:
            blocks.append({
                "site":i,"field":fn,"descriptor":fd,"operation":operation,
                "window":[token(j,rows[j]) for j in range(max(0,i-8),min(len(rows),i+5))]
            })
        set_calls=[token(i,row) for i,row in enumerate(rows)
                   if row[1].startswith("invoke") and ("java/util/Set." in row[3]
                   or "java/util/Collection." in row[3] or "getUUID:()" in row[3])]
        found.append({
            "name":name,"descriptor":desc,"instruction_count":len(rows),
            "field_sites":blocks,"set_calls":set_calls[:25],
        })
    if len(found)>36:return {"status":"NOT_PROVED","reason":"too_many_methods"}
    if not any(any(z["field"]=="witherDuration" and z["operation"]=="putfield" for z in m["field_sites"]) for m in found):
        return {"status":"NOT_PROVED","reason":"no_wither_duration_write"}
    return {
        "status":"OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY",
        "methods":found,"method_count":len(found),
        "boundary":"Presence and typed operands only; not a proven spell-level formula, persisted ownership, cross-bud dedup or per-player adapter",
    }


def prove_controller_field_lifecycle(methods):
    """Exact 1.0.9 controller constructor/NBT write/UUID set *call* dataflow.

    Membership and prune are per-controller instance field operations.
    They do not imply global/cross-controller deduplication, persistence
    of activeTargetIds, successful spawn or mutable per-player hooks.
    """
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    def lookup(name,desc):
        found=[opcode_rows(b) for n,d,b in methods if n==name and d==desc]
        return found[0] if len(found)==1 else None
    base_desc="(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V"
    special_desc="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V"
    nbt_desc="(Lnet/minecraft/nbt/CompoundTag;)V"
    prune_desc="(Lnet/minecraft/server/level/ServerLevel;)V"
    lambda_desc="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
    base=lookup(CONTROLLER,base_desc)
    specialized=lookup(CONTROLLER,special_desc)
    load=lookup("readAdditionalSaveData",nbt_desc)
    save=lookup("addAdditionalSaveData",nbt_desc)
    prune=lookup("pruneTargets",prune_desc)
    predicate=lookup("lambda$launchWave$0",lambda_desc)
    if any(x is None for x in (base,specialized,load,save,prune,predicate)):
        return fail("constructor_persistence_or_filter_method_missing")
    def op(rows,i,name):return len(rows)>i and rows[i][1]==name
    def local(rows,i,method,slot):
        return op(rows,i,f"{method}_{slot}") or (op(rows,i,method) and rows[i][2]==str(slot))
    def f(rows,i,method,name,desc):
        return len(rows)>i and op(rows,i,method) and field(rows[i])==(name,desc)
    def call(rows,i,member,desc):
        t=token(i,rows[i]) if len(rows)>i else {}
        return t.get("call")==member and t.get("descriptor")==desc
    def maxint(rows,i):
        return op(rows,i,"invokestatic") and call(rows,i,"max","(II)I") and "java/lang/Math.max:(II)I" in rows[i][3]
    if not (local(base,4,"aload",0) and op(base,5,"bipush") and base[5][2]=="80"
            and f(base,6,"putfield","witherDuration","I")
            and local(base,10,"aload",0) and op(base,11,"bipush")
            and base[11][2]=="8" and f(base,12,"putfield","maxTargets","I")
            and local(base,13,"aload",0) and op(base,14,"new")
            and op(base,15,"dup") and op(base,16,"invokespecial")
            and call(base,16,"<init>","()V")
            and f(base,17,"putfield","activeTargetIds","Ljava/util/Set;")):
        return fail("base_defaults_or_unique_set_initialization_drift")
    if not (local(specialized,23,"aload",0)
            and op(specialized,24,"iconst_1") and local(specialized,25,"iload",7)
            and maxint(specialized,26) and f(specialized,27,"putfield","maxTargets","I")
            and local(specialized,28,"aload",0) and local(specialized,29,"fload",8)
            and f(specialized,30,"putfield","impactDamage","F")
            and local(specialized,31,"aload",0) and op(specialized,32,"bipush")
            and specialized[32][2]=="30" and local(specialized,33,"iload",9)
            and maxint(specialized,34) and f(specialized,35,"putfield","witherDuration","I")
            and local(specialized,36,"aload",0) and op(specialized,37,"iconst_0")
            and local(specialized,38,"iload",10) and maxint(specialized,39)
            and f(specialized,40,"putfield","witherAmplifier","I")):
        return fail("controller_special_ctor_clamp_or_source_local_drift")
    if not (local(load,29,"aload",0) and local(load,30,"aload",1)
            and call(load,32,"getFloat","(Ljava/lang/String;)F")
            and f(load,33,"putfield","impactDamage","F")
            and local(load,34,"aload",0) and op(load,35,"bipush") and load[35][2]=="30"
            and local(load,36,"aload",1) and call(load,38,"getInt","(Ljava/lang/String;)I")
            and maxint(load,39) and f(load,40,"putfield","witherDuration","I")
            and local(load,41,"aload",0) and op(load,42,"iconst_0")
            and local(load,43,"aload",1) and call(load,45,"getInt","(Ljava/lang/String;)I")
            and maxint(load,46) and f(load,47,"putfield","witherAmplifier","I")):
        return fail("NBT_restore_float_or_integer_bounds_drift")
    if not (f(save,28,"getfield","impactDamage","F")
            and call(save,29,"putFloat","(Ljava/lang/String;F)V")
            and f(save,33,"getfield","witherDuration","I")
            and call(save,34,"putInt","(Ljava/lang/String;I)V")
            and f(save,38,"getfield","witherAmplifier","I")
            and call(save,39,"putInt","(Ljava/lang/String;I)V")):
        return fail("NBT_store_field_mapping_drift")
    if not (local(prune,35,"aload",4)
            and call(prune,36,"getTargetUuid","()Ljava/util/UUID;")
            and call(prune,37,"add","(Ljava/lang/Object;)Z")
            and local(prune,40,"aload",0)
            and f(prune,41,"getfield","activeTargetIds","Ljava/util/Set;")
            and local(prune,42,"aload",2)
            and call(prune,43,"retainAll","(Ljava/util/Collection;)Z")):
        return fail("prune_targets_current_UUID_collection_and_retainAll_drift")
    if not (local(predicate,0,"aload",0) and local(predicate,1,"aload",1)
            and local(predicate,2,"aload",2)
            and call(predicate,3,"isValidTarget","(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z")
            and op(predicate,4,"ifeq")
            and local(predicate,5,"aload",0)
            and f(predicate,6,"getfield","activeTargetIds","Ljava/util/Set;")
            and local(predicate,7,"aload",2)
            and call(predicate,8,"getUUID","()Ljava/util/UUID;")
            and call(predicate,9,"contains","(Ljava/lang/Object;)Z")
            and op(predicate,10,"ifne")):
        return fail("predicate_same_candidate_UUID_membership_guard_drift")
    return {
        "status":"PROVED_CONTROLLER_CONSTRUCTOR_NBT_AND_LOCAL_UUID_MEMBERSHIP_OPERATIONS",
        "base_wither_default":80,"base_max_targets_default":8,
        "active_target_set":"new_object_assigned_to_this.activeTargetIds_in_base_ctor",
        "specialized_max_targets":"Math.max_int(1,ctor_int_slot7)",
        "specialized_damage":"ctor_float_slot8",
        "specialized_wither_duration":"Math.max_int(30,ctor_int_slot9)",
        "specialized_wither_amplifier":"Math.max_int(0,ctor_int_slot10)",
        "nbt_reload_wither_duration":"Math.max_int(30,CompoundTag.getInt)",
        "nbt_reload_wither_amplifier":"Math.max_int(0,CompoundTag.getInt)",
        "nbt_reload_impact_damage":"CompoundTag.getFloat",
        "nbt_save_fields":["impactDamage","witherDuration","witherAmplifier"],
        "prune":"this.activeTargetIds.retainAll(derived_target_UUID_collection)",
        "wave_lambda":"isValidTarget(ownerArg,candidateArg) AND NOT this.activeTargetIds.contains(candidateArg.getUUID())",
        "boundary":"Per-instance membership/prune and field read/write only; no cross-controller dedup, UUID persistence, spell-level assignment, live gameplay or mutator API proven",
    }

def certify_exact_controller_lifecycle_109(proof):
    expected={
        "status":"PROVED_CONTROLLER_CONSTRUCTOR_NBT_AND_LOCAL_UUID_MEMBERSHIP_OPERATIONS",
        "base_wither_default":80,"base_max_targets_default":8,
        "active_target_set":"new_object_assigned_to_this.activeTargetIds_in_base_ctor",
        "specialized_max_targets":"Math.max_int(1,ctor_int_slot7)",
        "specialized_damage":"ctor_float_slot8",
        "specialized_wither_duration":"Math.max_int(30,ctor_int_slot9)",
        "specialized_wither_amplifier":"Math.max_int(0,ctor_int_slot10)",
        "nbt_reload_wither_duration":"Math.max_int(30,CompoundTag.getInt)",
        "nbt_reload_wither_amplifier":"Math.max_int(0,CompoundTag.getInt)",
        "nbt_reload_impact_damage":"CompoundTag.getFloat",
        "nbt_save_fields":["impactDamage","witherDuration","witherAmplifier"],
        "prune":"this.activeTargetIds.retainAll(derived_target_UUID_collection)",
        "wave_lambda":"isValidTarget(ownerArg,candidateArg) AND NOT this.activeTargetIds.contains(candidateArg.getUUID())",
        "boundary":"Per-instance membership/prune and field read/write only; no cross-controller dedup, UUID persistence, spell-level assignment, live gameplay or mutator API proven",
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("Somake 1.0.9 controller assignment/UUID membership fingerprint drift")

def inspect(jar:Path):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("untrusted filename/size")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("wrong publisher SHA")
    with zipfile.ZipFile(jar) as a:
        names=a.namelist()
        if len(names)!=len(set(names)) or any(c.replace(".","/")+".class" not in names for c in (CONTROLLER,BUD)):
            raise GateError("class not in exact JAR or ZIP duplicate")
        meta=a.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("wrong mod ID")
    def methods(cls):
        p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),cls],
                         capture_output=True,text=True,timeout=60,check=False)
        if p.returncode or not p.stdout or len(p.stdout)>MAX_TEXT:raise GateError("bounded javap failed")
        return sections(p.stdout)
    controller=methods(CONTROLLER);bud=methods(BUD)
    certify_exact_bud_operand_contract_109(operand_contract(bud))
    certify_exact_wave_list_cap_109(prove_wave_list_cap(controller))
    certify_exact_wave_loop_109(prove_wave_loop_spawn_sites(controller))
    certify_exact_wither_handoff_109(certify_wither_constructor_handoff(bud,controller))
    proof=scan(controller)
    lifecycle=prove_controller_field_lifecycle(controller)
    print("SOMAKE_CONTROLLER_LIFECYCLE_PROOF",json.dumps(lifecycle,sort_keys=True))
    certify_exact_controller_lifecycle_109(lifecycle)
    if proof["status"]!="OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY":
        raise GateError("controller source observation failed:"+proof.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("artifact altered")
    return {"mod_id":"somakespells","version":"1.0.9","sha1":digest,"survey":proof,"lifecycle":lifecycle}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_CONTROLLER_FIELD_SURVEY",json.dumps(result["survey"],sort_keys=True))
    print("SOMAKE_CONTROLLER_FIELD_SHA",result["sha1"])
    print("SOMAKE_CONTROLLER_LIFECYCLE_GATE","PASS_SHA_EXACT_CONSTRUCTOR_NBT_LOCAL_UUID_MEMBERSHIP")

if __name__=="__main__":
    main()
