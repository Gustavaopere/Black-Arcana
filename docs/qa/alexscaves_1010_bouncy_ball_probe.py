#!/usr/bin/env python3
"""SHA-exact read-only 1.0.10 Bouncy Ball Shot Gum/Gumball audit.

Selected JVM method references and bounded offsets only. Reuses separately
sealed exact Gumball owner/producer contracts; does not export source, certify
effective gameplay, or establish any stable mutating API.
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

SCOPE = "EXACT_ALEXSCAVES_1010_BOUNCY_BALL_SHOTGUM_BOUNCE_LIMIT_SELECTED_ABI"
SHOT = BASE+"server/item/ShotGumItem.class"
BALL = BASE+"server/entity/item/GumballEntity.class"
GUMBEEPER = BASE+"server/entity/living/GumbeeperEntity.class"
CLASSES = {
    SHOT:"08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238",
    BALL:"343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535",
    GUMBEEPER:"6a24f05a730218352a083da32f233c3d48fb5f85a6f24f1ba45d78c422b0266c",
}
ENCH="data/alexscaves/enchantment/bouncy_ball.json"
TAG="data/alexscaves/tags/item/enchantable/shot_gum.json"
OTHER="data/alexscaves/enchantment/targeted_ricochet.json"
SELECTION = {
    SHOT:(
        ("acInventoryTick",
         "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V",
         "6f9325406aaf142af4b415bff94b9123882b72a2ab981370d9be30a5e7c18093",
         (130,138,155,172,190,205,316,434,441,448,480,487,495,508,533,541,550,560,569,587,600)),
    ),
    BALL:(
        ("bounceFromDirection","(Lnet/minecraft/core/Direction;)V",
         "0f687d784c92e2b8e7eebfc3cc9a85041b5fdfb37c6c5e4a32aaa2489df66282",
         (39,46,101,167,183,189,242,287)),
        ("getMaximumBounces","()I",
         "c45e92256a3739bc4614241d9d6cc8e814632cbc8950109980a57495046d1573",()),
        ("setMaximumBounces","(I)V",
         "6ccec525f7d55393d30907d20a4d3fe5e48583df2c41f70fa87be0e214808da9",()),
        ("getBounces","()I",None,()),
        ("setBounces","(I)V",None,()),
    ),
    GUMBEEPER:(
        ("shootGumball","(Lnet/minecraft/world/entity/LivingEntity;)V",
         "26380c4830c57381fa6d39220234305da5b408e7ad11bf56878e061b6e45ecb2",()),
    )
}
SYMBOLS={"getfield","putfield","getstatic","putstatic","invokestatic",
         "invokevirtual","invokespecial","invokeinterface","invokedynamic"}
NUM={"bipush","sipush","ldc","ldc_w","ldc2_w"}
PIVOTS={
    "acInventoryTick":("BOUNCY_BALL:","enchantLevel:","setMaximumBounces:"),
    "bounceFromDirection":("getMaximumBounces:","getBounces:","setBounces:","discard:"),
}
WINDOW_RADIUS=5

def require(value,reason):
    if not value: raise ValueError(reason)

def slim(x):
    return {k:x[k] for k in ("offset","opcode","operand","symbol")}

def method(methods,name,descriptor):
    matched=[m for m in methods if name_of(m)==name and m["descriptor"]==descriptor]
    require(len(matched)==1,"missing or duplicate exact method "+name)
    m=matched[0]
    ins=m["instructions"]
    require(1<=len(ins)<=1800,"method instruction population out of bounds")
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"unsorted or duplicated JVM offsets")
    return m

def select_native(m,name,expected,anchors):
    ins=m["instructions"]
    digest=digest_method(m)
    if expected is not None:
        require(digest==expected,"drift from previously sealed Gumball exact method "+name)
    refs=[slim(x) for x in ins if x["opcode"] in SYMBOLS]
    branches=[slim(x) for x in ins if x["opcode"].startswith(("if","goto"))]
    numbers=[slim(x) for x in ins if x["opcode"] in NUM or x["opcode"].startswith(("iconst_","fconst_","dconst_"))]
    # Full-method inventories are bounded and symbolic/branch/numeric only;
    # do not export entire method or decompiled expression sequences.
    require(len(refs)<=130 and len(branches)<=145 and len(numbers)<=145,
            "symbol/branch/constant evidence budget exceeded "+name)
    by_offset={x["offset"]:i for i,x in enumerate(ins)}
    windows=[]
    require(len(anchors)<=28,"unexpected anchor set")
    for anchor in anchors:
        require(anchor in by_offset,"preexisting exact anchor missing "+name+" @"+str(anchor))
        idx=by_offset[anchor]
        xs=ins[max(0,idx-WINDOW_RADIUS):idx+WINDOW_RADIUS+1]
        windows.append({"at":anchor,"selected_instructions":[slim(x) for x in xs]})
    pivots=[]
    for token in PIVOTS.get(name,()):
        matches=[i for i,x in enumerate(ins) if token in x["symbol"]]
        if matches:
            i=matches[0]
            pivots.append({"marker":token,"matches":len(matches),
                           "offset":ins[i]["offset"],
                           "selected_instructions":[slim(x) for x in ins[max(0,i-5):i+7]]})
    if name=="acInventoryTick":
        require(any(x["marker"]=="BOUNCY_BALL:" and x["matches"]==1 for x in pivots),
                "missing unique Bouncy Ball shot producer")
        require(any(x["marker"]=="setMaximumBounces:" for x in pivots),
                "missing Gumball max-bounces setter in Shot Gum")
    if name=="bounceFromDirection":
        for needed in ("getMaximumBounces:","getBounces:","setBounces:"):
            require(any(x["marker"]==needed for x in pivots),
                    "missing Gumball bounce consumer "+needed)
    return {"name":name,"header":m["header"],"descriptor":m["descriptor"],
            "instruction_count":len(ins),"parsed_method_sha256":digest,
            "selected_symbolic_refs":refs,"selected_branches":branches,
            "selected_numeric_operands":numbers,"prior_exact_anchor_windows":windows,
            "selected_pivots":pivots,
            "scope":"BOUNDED_JVM_REFERENCES_AND_WINDOWS_NOT_FULL_CFG"}

def resource(z,path):
    raw=z.read(path)
    require(len(raw)<=16000,"unexpected resource length "+path)
    obj=json.loads(raw)
    require(isinstance(obj,dict),"non-object resource "+path)
    return {"path":path,"sha256":hashlib.sha256(raw).hexdigest(),"json":obj}

def audit(jar,javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"installed publisher JAR SHA mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate publisher entries")
        for path in (*CLASSES,ENCH,TAG,OTHER):
            require(path in names,"missing publisher path "+path)
        resources=[resource(z,path) for path in (ENCH,TAG,OTHER)]
        classes=[{"class":p,"sha256":hashlib.sha256(z.read(p)).hexdigest()}
                 for p in CLASSES]
    require({x["class"]:x["sha256"] for x in classes}==CLASSES,
            "drift from existing exact Gumball/Shot Gum class contracts")
    ench,tag,_=resources
    e=ench["json"]
    require(e.get("description",{}).get("translate")=="enchantment.alexscaves.bouncy_ball",
            "enchantment identity mismatch")
    require(e.get("supported_items")=="#alexscaves:enchantable/shot_gum",
            "enchantment item tag changed")
    require(e.get("max_level")==3,"Bouncy Ball max level mismatch")
    require("alexscaves:shot_gum" in tag["json"].get("values",[]),
            "Shot Gum absent from item tag")
    consumers=[]
    for owner,selection in SELECTION.items():
        parsed=parse_methods(javap(javap_bin,jar,owner[:-6].replace("/",".")))
        for name,descriptor,expected,anchors in selection:
            consumers.append({"owner":owner,"sha256":CLASSES[owner],
                              "method":select_native(method(parsed,name,descriptor),
                                                     name,expected,anchors)})
    return {"schema_version":1,"scope":SCOPE,
            "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "resources":{"bouncy_ball":ench,"shot_gum_item_tag":tag,
                         "targeted_ricochet":resources[2]},
            "owner_classes":classes,"selected_consumers":consumers,
            "limits":{"public_111_exact_parameter_authority":False,
                      "complete_jvm_control_flow":"NOT_RECONSTRUCTED",
                      "ricochet_counts_observed_in_game":"NOT_TESTED",
                      "level_out_of_range_datapacks":"NOT_VERIFIED",
                      "effective_enchanting_tags":"NOT_VERIFIED",
                      "Gumbeeper_uses_item_enchantment":"NOT_EVIDENCED",
                      "additional_mutating_hooks":"NOT_VERIFIED",
                      "physical_qa":"NOT_TESTED",
                      "mutation":"NO_MUTATION",
                      "perk_certification":"NOT_CERTIFIED"}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",type=Path,required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--seal",type=Path)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    result=audit(a.jar,a.javap)
    if a.seal:
        require(result==json.loads(a.seal.read_text(encoding="utf8")),
                "sealed Bouncy Ball exact JVM manifest drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
