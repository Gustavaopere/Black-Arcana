#!/usr/bin/env python3
"""Read-only publisher 1.0.10 Charting Call / Magic Conch quantity probe.

Exports bounded selected JVM references, branches, constants and method hashes.
Does not reconstruct a complete CFG, execute the mod or prove a mutating hook.
Public 1.1.1 sources are not an exact version authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "EXACT_ALEXSCAVES_1010_CHARTING_CALL_CONCH_QUANTITY_RNG_SELECTED_ABI"
CONCH = BASE + "server/item/MagicConchItem.class"
DEEP_ONE = BASE + "server/entity/living/DeepOneBaseEntity.class"
CLASSES = {
    CONCH:"4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2",
    DEEP_ONE:"185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470",
}
ENCHANTMENTS = {
    "charting_call":"data/alexscaves/enchantment/charting_call.json",
    "lasting_morale":"data/alexscaves/enchantment/lasting_morale.json",
    "taxing_bellow":"data/alexscaves/enchantment/taxing_bellow.json",
    "magic_conch_tag":"data/alexscaves/tags/item/enchantable/magic_conch.json",
}
HASHES = {
    "charting_call":"352ec52d0e21298a921cc10fe5253b0484c0b273adf3fc5713bce046758ccacd",
    "lasting_morale":"8c662fb7f68987d8e564ec053ebccdd9232593e5961d2213bbbed037b270232f",
    "taxing_bellow":"275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1",
    "magic_conch_tag":"730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8",
}
SELECTORS = {
    CONCH: (
        ("releaseUsing",
         "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V",
         (20,39,62,77,86,96,107,126,175,195,215,244,299,354,415,448)),
        ("summonDeepOne",
         "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/entity/LivingEntity;I)Lcom/github/alexmodguy/alexscaves/server/entity/living/DeepOneBaseEntity;",
         (22,28,33,80,118,130,234,268,278,290,297)),
    ),
    DEEP_ONE: (
        ("setSummonedBy","(Lnet/minecraft/world/entity/LivingEntity;I)V",
         (2,10,15)),
        ("tick","()V",(123,133,217,227,238,240,299,311)),
    ),
}
PIVOTS = {
    "releaseUsing": (
        "CHARTING_CALL:", "LASTING_MORALE:", "TAXING_BELLOW:",
        "RandomSource.nextInt:", "Math.max:", "summonDeepOne:",
        "addCooldown:",
    ),
    "summonDeepOne": ("setSummonedBy:","addFreshEntity:","copyTarget:"),
    "setSummonedBy": ("setSummonTime:","summonerUUID:"),
    "tick": ("getSummonTime:","setSummonTime:","remove:"),
}
SYMBOLIC = {"getstatic","putstatic","getfield","putfield","invokestatic",
            "invokevirtual","invokespecial","invokeinterface","invokedynamic"}
NUMERIC = {"ldc","ldc_w","ldc2_w","sipush","bipush"}

def require(ok,msg):
    if not ok:
        raise ValueError(msg)

def slim(ins):
    return {k:ins[k] for k in ("offset","opcode","operand","symbol")}

def find_method(methods,name,desc):
    found=[m for m in methods if name_of(m)==name and m["descriptor"]==desc]
    require(len(found)==1,"missing/duplicate exact method "+name)
    ins=found[0]["instructions"]
    require(3<=len(ins)<=1600,"unexpected compiled method size "+name)
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"unsorted/duplicate JVM offsets "+name)
    return found[0]

def analyze_method(m,anchors):
    name=name_of(m)
    ins=m["instructions"]
    positions={x["offset"]:idx for idx,x in enumerate(ins)}
    require(len(anchors)<=22,"anchor budget exceeded "+name)
    windows=[]
    for at in anchors:
        require(at in positions,"missing fixed exact offset "+name+" @"+str(at))
        idx=positions[at]
        windows.append({"at":at,"selected_instructions":[slim(x) for x in ins[max(0,idx-5):idx+6]]})
    candidate=[slim(x) for x in ins if x["opcode"] in SYMBOLIC or
               x["opcode"] in NUMERIC or
               x["opcode"].startswith(("if","goto","iconst_","fconst_","dconst_"))]
    require(len(candidate)<=400,"bounded reference budget exceeded "+name)
    pivot=[]
    for token in PIVOTS.get(name,()):
        indexes=[idx for idx,x in enumerate(ins) if token in x["symbol"]]
        if indexes:
            idx=indexes[0]
            pivot.append({"marker":token,"matches":len(indexes),
                          "offset":ins[idx]["offset"],
                          "nearby":[slim(x) for x in ins[max(0,idx-4):idx+7]]})
    if name=="releaseUsing":
        require(any(x["marker"]=="CHARTING_CALL:" and x["matches"]==1
                    for x in pivot),"missing/ambiguous Charting Call JVM consumer")
        require(any(x["marker"]=="RandomSource.nextInt:" and x["matches"]>=3
                    for x in pivot),"missing quantity RNG callsites")
        require(any(x["marker"]=="Math.max:" for x in pivot),
                "missing max bound selection")
        require(any(x["marker"]=="summonDeepOne:" for x in pivot),
                "missing summon handoff")
    if name=="summonDeepOne":
        require(any(x["marker"]=="addFreshEntity:" for x in pivot),
                "missing placement/spawn call")
    return {
        "name":name,"descriptor":m["descriptor"],
        "instruction_count":len(ins),"parsed_method_sha256":digest_method(m),
        "selected_numeric_symbolic_and_branch_references":candidate,
        "selected_fixed_windows":windows,
        "selected_pivot_windows":pivot,
        "evidence_scope":"BOUNDED_JVM_WINDOWS_NOT_COMPLETE_CFG",
    }

def resource(z,path):
    raw=z.read(path)
    require(len(raw)<=16000,"oversize publisher JSON resource")
    data=json.loads(raw)
    require(isinstance(data,dict),"non-object exact JSON resource")
    return {"path":path,"sha256":hashlib.sha256(raw).hexdigest(),"json":data}

def audit(jar,javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"publisher 1.0.10 SHA1/SHA256/size mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate exact ZIP paths")
        require(all(p in names for p in (*CLASSES,*ENCHANTMENTS.values())),
                "missing exact provider class/resource")
        classes=[{"path":p,"sha256":hashlib.sha256(z.read(p)).hexdigest()} for p in CLASSES]
        resources={k:resource(z,p) for k,p in ENCHANTMENTS.items()}
    require({v["path"]:v["sha256"] for v in classes}==CLASSES,
            "drift from existing 1.0.10 Magic Conch/Deep One class contracts")
    require({k:v["sha256"] for k,v in resources.items()}==HASHES,
            "drift from existing 1.0.10 Conch enchant resource contracts")
    e=resources["charting_call"]["json"]
    require(e.get("description",{}).get("translate")=="enchantment.alexscaves.charting_call",
            "Charting Call resource identity mismatch")
    require(e.get("supported_items")=="#alexscaves:enchantable/magic_conch",
            "Charting Call support tag mismatch")
    require(e.get("max_level")==4,"Charting Call max level mismatch")
    require("alexscaves:magic_conch" in resources["magic_conch_tag"]["json"].get("values",[]),
            "Magic Conch absent from bundled item tag")
    consumers=[]
    for owner,methods in SELECTORS.items():
        parsed=parse_methods(javap(javap_bin,jar,owner[:-6].replace("/",".")))
        for name,desc,anchors in methods:
            m=find_method(parsed,name,desc)
            consumers.append({"owner":owner,"owner_sha256":CLASSES[owner],
                              "method":analyze_method(m,anchors)})
    return {
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "resource_evidence":resources,"owner_classes":classes,
        "selected_consumers":consumers,
        "bounds_requiring_physical_validation":{
            "charting_level_0":{"deep_one":"3+nextInt(1)","knight":"2+nextInt(1)","mage":"1+nextInt(1)"},
            "positive_level_L":{"deep_one":"3+nextInt(max(L-1,2))",
                                "knight":"2+nextInt(max(L-2,0))",
                                "mage":"1+nextInt(max(L-3,0))"},
            "no_final_spawn_guarantee":True,
            "zero_bound_call_at_low_levels":"EXACT_STATIC_NOT_REPRODUCED_IN_GAME",
        },
        "limits":{
            "complete_control_flow":"NOT_RECONSTRUCTED",
            "RandomSource_nextInt_zero_runtime_result":"NOT_TESTED",
            "actual_requested_and_accepted_summon_counts":"NOT_TESTED",
            "failed_placement_and_consumed_costs":"NOT_TESTED",
            "effective_datapack_tags_and_enchant_levels":"NOT_VERIFIED",
            "gameplay_multiplayer_network_ownership":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "perk_certification":"NOT_CERTIFIED",
        },
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    j=audit(args.jar,args.javap)
    if args.seal:
        require(j==json.loads(args.seal.read_text(encoding="utf8")),
                "sealed Charting Call evidence mismatch")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(j,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
