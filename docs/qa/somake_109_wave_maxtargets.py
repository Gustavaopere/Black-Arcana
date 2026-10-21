#!/usr/bin/env python3
"""Clean-room Somake wave cardinality scout: observations, not inferred cap.
Publisher bytecode/JAR/method bodies are not written to the repository or output.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, zipfile
from collections import Counter
from pathlib import Path
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_radius_consumers import (wave_max_targets_surface,
    native_isvalidtarget_surface, certify_exact_native_selection_109)
from somake_109_native_filter_middle import CLASS

DESC="(Lnet/minecraft/server/level/ServerLevel;)V"
FIELD={"Field maxTargets:I",
       "Field com/somake/somakespells/entity/FuneralBloomControllerEntity.maxTargets:I"}

def kind(symbol):
    m=re.search(r"(?:Method|InterfaceMethod)\s+(.+?):\(",symbol)
    if not m:return "unknown"
    member=m.group(1)
    name=member.rsplit(".",1)[-1].replace('"',"")
    for tag,words in {
        "bud":("FuneralBloomBudEntity",),
        "query":("getEntitiesOfClass",),
        "list":("java/util/List","java/util/Iterator","java/util/Collection"),
        "sort":("java/util/Collections","java/util/Comparator","java/util/stream"),
        "spawn":("addFreshEntity",),
        "entity":("LivingEntity","net/minecraft/world/entity/Entity"),
        "other":("",),
    }.items():
        if any(w in member for w in words):return tag+"."+name
    return "other."+name

def wave_cardinality_scout(declared):
    matches=[body for n,d,body in declared if n=="launchWave" and d==DESC]
    if len(matches)!=1:return {"status":"NOT_PROVED","reason":"ambiguous_wave"}
    rows=opcode_rows(matches[0])
    pc_to_idx={pc:i for i,(pc,*_) in enumerate(rows)}
    fields=[i for i,(_,op,_,c) in enumerate(rows) if op=="getfield" and c in FIELD]
    bud=[i for i,(_,op,_,c) in enumerate(rows) if op=="invokespecial" and
         c.startswith('Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":')]
    if len(rows)!=196 or len(fields)!=2 or len(bud)!=1:
        return {"status":"NOT_PROVED","reason":"wave_release_shape_drift",
                "instruction_count":len(rows),"field_count":len(fields),"bud_count":len(bud)}
    branches=[]
    for i,(_,op,operand,_) in enumerate(rows):
        if not (op.startswith("if") or op.startswith("goto")):continue
        target=operand.split(" ",1)[0]
        if not target.isdecimal() or int(target) not in pc_to_idx:
            return {"status":"NOT_PROVED","reason":"unresolved_branch_target"}
        branches.append({"index":i,"opcode":op,"target_index":pc_to_idx[int(target)]})
    calls=[{"index":i,"method_category":kind(c),"dispatch":op}
           for i,(_,op,_,c) in enumerate(rows) if op.startswith("invoke")]
    def window(site):
        start=max(0,site-9);end=min(len(rows),site+11)
        locals_=[{"index":j,"slot_operation":rows[j][1]}
                 for j in range(start,end) if re.fullmatch(r"[a-z](?:load|store)_[0-9]+",rows[j][1])]
        events=[{"index":j,"opcode":rows[j][1]}
                for j in range(start,end) if rows[j][1] in
                ("iadd","isub","iinc","iconst_0","iconst_1","dup","dup2","pop","swap","checkcast","arraylength")]
        return {"near_index":site,"local_operations":locals_[:28],"other_events":events[:28]}
    return {"status":"OBSERVED_WAVE_BRANCH_AND_MAXTARGETS_CALLSITES_ONLY",
            "instruction_count":len(rows),
            "max_targets_field_read_indices":fields,"bud_constructor_indices":bud,
            "branch_map":branches,
            "call_inventory":calls[:80],
            "opcode_histogram":dict(sorted(Counter(op for _,op,_,_ in rows).items())),
            "site_windows":[window(i) for i in fields+bud+[b["index"] for b in branches]],
            "boundary":"No target-count cap, list order, bud spawn cardinality, runtime or perk seam proved"}


def prove_wave_list_cap(declared):
    """Pin data flow from list.size to maxTargets and List.subList upper bound.

    This establishes a candidate-list slice, not bud spawn cardinality.
    """
    matches=[body for n,d,body in declared if n=="launchWave" and d==DESC]
    if len(matches)!=1:return {"status":"NOT_PROVED","reason":"ambiguous_wave"}
    rows=opcode_rows(matches[0])
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len(rows)!=196:return fail("not_exact_196_instruction_release")
    def isload(i,slot):
        _,op,arg,_=rows[i]
        return op==f"aload_{slot}" or (op=="aload" and arg==str(slot))
    def isstore(i,slot):
        _,op,arg,_=rows[i]
        return op==f"astore_{slot}" or (op=="astore" and arg==str(slot))
    def call(i,opcode,member):
        return rows[i][1]==opcode and rows[i][3] in (
            "InterfaceMethod "+member,
            "Method "+member,
        )
    if not (isload(40,2) and call(41,"invokeinterface","java/util/List.size:()I")
            and isload(42,0) and rows[43][1]=="getfield" and rows[43][3] in FIELD
            and rows[44][1]=="if_icmple"):
        return fail("size_and_cap_conditional_operands_not_exact")
    positions={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    target=rows[44][2].split(" ",1)[0]
    if not target.isdecimal() or positions.get(int(target))!=51:
        return fail("oversize_branch_skip_not_the_list_join")
    if not (isload(45,2) and rows[46][1]=="iconst_0" and isload(47,0)
            and rows[48][1]=="getfield" and rows[48][3] in FIELD
            and call(49,"invokeinterface","java/util/List.subList:(II)Ljava/util/List;")
            and isstore(50,2)):
        return fail("maxTargets_not_upper_bound_of_sublist_or_stored_result")
    if not isload(53,2) or not call(54,"invokeinterface","java/util/List.iterator:()Ljava/util/Iterator;"):
        return fail("iterator_not_proved_to_consume_bounded_slot")
    for i,(_,op,arg,_) in enumerate(rows):
        if i==44:continue
        if op.startswith(("if","goto","jsr")):
            dest=arg.split(" ",1)[0]
            if not dest.isdecimal():return fail("non_numeric_external_branch")
            idx=positions.get(int(dest))
            if idx is None:return fail("unresolved_external_branch")
            if 40<idx<51 and not 40<=i<=50:return fail("branch_enters_cap_argument_window")
        elif op in ("tableswitch","lookupswitch","ret","wide","jsr_w"):
            return fail("unsupported_control_flow_topology")
    return {
        "status":"PROVED_WAVE_CANDIDATE_LIST_TRUNCATION",
        "method":"launchWave","instruction_count":196,
        "list_local":2,"size_call_index":41,
        "first_cap_field_index":43,"conditional_index":44,
        "truncation_condition":"list_size_greater_than_maxTargets",
        "branch_skip_index":51,"slice_start_literal":0,"slice_upper_source":"maxTargets_field",
        "second_cap_field_index":48,"sublist_call_index":49,"list_store_index":50,
        "iterator_call_index":54,
        "boundary":"List is truncated for oversize input; not bud count, nonnegative cap, owner roles or gameplay",
    }

def certify_exact_wave_list_cap_109(proof):
    expected={
        "status":"PROVED_WAVE_CANDIDATE_LIST_TRUNCATION",
        "method":"launchWave","instruction_count":196,
        "list_local":2,"size_call_index":41,
        "first_cap_field_index":43,"conditional_index":44,
        "truncation_condition":"list_size_greater_than_maxTargets",
        "branch_skip_index":51,"slice_start_literal":0,"slice_upper_source":"maxTargets_field",
        "second_cap_field_index":48,"sublist_call_index":49,"list_store_index":50,
        "iterator_call_index":54,
        "boundary":"List is truncated for oversize input; not bud count, nonnegative cap, owner roles or gameplay",
    }
    if not isinstance(proof,dict) or any(proof.get(k)!=v for k,v in expected.items()):
        raise GateError("Somake 1.0.9 candidate list maxTargets truncation fingerprint drift")

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong Somake file")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("wrong Somake publisher hash")
    with zipfile.ZipFile(jar) as z:
        if len(z.namelist())!=len(set(z.namelist())):raise GateError("duplicate ZIP member")
        if CLASS.replace(".","/")+".class" not in z.namelist():raise GateError("no controller")
        toml=z.read("META-INF/neoforge.mods.toml")
        if len(toml)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",toml):
            raise GateError("wrong mod ID")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
                     capture_output=True,text=True,timeout=60,check=False)
    if p.returncode or len(p.stdout)>1_400_000:raise GateError("javap failed/unbounded")
    declarations=sections(p.stdout)
    wave=[body for n,d,body in declarations if n=="launchWave" and d==DESC]
    if len(wave)!=1:raise GateError("wrong native wave signature")
    certify_exact_native_selection_109(native_isvalidtarget_surface(declarations),
                                      wave_max_targets_surface(wave[0]))
    evidence=wave_cardinality_scout(declarations)
    proof=prove_wave_list_cap(declarations)
    certify_exact_wave_list_cap_109(proof)
    if evidence["status"]!="OBSERVED_WAVE_BRANCH_AND_MAXTARGETS_CALLSITES_ONLY":
        raise GateError("wave structure changed")
    return {"version":"1.0.9","mod_id":"somakespells","sha1":sha,
            "wave":evidence,"candidate_cap":proof,"limit":"read-only clean-room observation; cap and gameplay NOT proved"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_WAVE_MAXTARGETS_SCOUT",json.dumps(result["wave"],sort_keys=True))
    print("SOMAKE_WAVE_MAXTARGETS_CAP",json.dumps(result["candidate_cap"],sort_keys=True))
    print("SOMAKE_WAVE_MAXTARGETS_SHA",result["sha1"])
if __name__=="__main__":
    main()
