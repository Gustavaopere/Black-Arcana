#!/usr/bin/env python3
"""Bounded read-only Ink Bomb item/entity defaults and chocolate recipe codec discovery.

Project exact distributed method bodies, typed calls, exception-table entries and
bootstrap handles. No game execution, loaded-mod inference or mutation.
"""
from __future__ import annotations
import argparse
import json
import re
from contextlib import ExitStack
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, bootstrap

MC = "net/minecraft/"
P = "com/github/alexmodguy/alexscaves/server/"
PROPS = MC+"world/item/Item$Properties"
ITEM = MC+"world/item/Item"
STACK = MC+"world/item/ItemStack"
COMP = MC+"core/component/DataComponents"
TYPE = MC+"world/entity/EntityType"
BUILDER = TYPE+"$Builder"
RECIPE = MC+"world/item/crafting/ShapelessRecipe$Serializer"
INK = P+"item/InkBombItem"
REGISTRY = P+"item/ACItemRegistry"
ENTITYREG = P+"entity/ACEntityRegistry"
SELECT = {
    PROPS: {"<init>", "buildComponents", "buildAndValidateComponents", "validateComponents", "component", "stacksTo"},
    ITEM: {"<init>", "components", "getDefaultInstance", "getDefaultMaxStackSize"},
    STACK: {"getMaxStackSize", "getMaxDamage", "lambda$static$3", "lambda$static$6", "lambda$static$7"},
    COMP: {"<clinit>"},
    MC+"core/component/DataComponentMap": {"builder", "composite"},
    MC+"core/component/DataComponentMap$Builder": {"set", "addAll", "build"},
    TYPE: {"<init>", "getDimensions", "clientTrackingRange", "updateInterval", "trackDeltas"},
    BUILDER: {"<init>", "of", "build", "sized", "clientTrackingRange", "updateInterval",
              "setUpdateInterval", "setTrackingRange", "setShouldReceiveVelocityUpdates"},
    RECIPE: {"<clinit>", "codec", "streamCodec", "<init>", "fromNetwork", "toNetwork"},
    INK: {"<init>", "use"},
    REGISTRY: {"lambda$static$105", "lambda$static$106", "lambda$static$164"},
    ENTITYREG: {"lambda$static$43"},
}
PINS = {
    PROPS:"35f8678fef22d0d45136b8f2e7250067f579e072b4bb2dc1bbf9c806c7b0748b",
    ITEM:"d4234cf5acb218b2056a38845170ec8266e16dc39ae0ed5fe5328cac153af462",
    STACK:"072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    COMP:"fee338af2dbe21bd35781275b01752b72e9178b4314b9d574934a0cddc464716",
    TYPE:"48c9761c2756859bf6734d6d623532e382fa78d52f73e33a6671c8a9fef2cb8d",
    INK:"4d663e3810455f285e55f50a1fd6c75454d0c88c42fc241cc794e83a5f50162b",
    REGISTRY:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
    ENTITYREG:"7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072",
}
KNOWN = {
    (PROPS,"<init>","()V"):"91fd20ff4ac88d8a1516a2bd89ed6c288a6546839db4a268fb15d30671e879f3",
    (PROPS,"buildAndValidateComponents","()Lnet/minecraft/core/component/DataComponentMap;"):
        "ce196929d6466b4ddf1d652d18a7827b1e79831f5bfd93997d81f874a5975b10",
    (STACK,"lambda$static$3","(Lcom/mojang/serialization/codecs/RecordCodecBuilder$Instance;)Lcom/mojang/datafixers/kinds/App;"):
        "dc6750c881e2b856e770b6292081224e4048a6cbea15468efcffb0cd4e04c226",
}
REQUIRED = {
    PROPS:{"buildComponents","buildAndValidateComponents"}, COMP:{"<clinit>"},
    BUILDER:{"<init>","sized","build"}, RECIPE:{"<clinit>","codec"},
    INK:{"<init>","use"}, REGISTRY:{"lambda$static$105","lambda$static$106","lambda$static$164"},
    ENTITYREG:{"lambda$static$43"},
}
DIST = {
    "installer": ("0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60", 6972109),
    "server": ("1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359", 5675624),
    "srg": ("26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71", 14246609),
    "universal": ("1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956", 3551255),
}
LIMITS = {"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED","physical_qa":"NOT_TESTED",
          "mutating_hook":"NOT_VERIFIED","mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED",
          "effective_registry_components":"NOT_VERIFIED","effective_entity_tracking":"NOT_VERIFIED",
          "actual_recipe_acceptance":"NOT_VERIFIED"}

def selected(owner, declaration):
    return (declaration["name"] in SELECT.get(owner, set())
            or (owner == RECIPE and declaration["name"].startswith("lambda$")))

def project_component_defaults(reader, body, decl):
    # Narrow projection of the complete initializer: only typed writes to
    # exact fields and the bounded common-item-component construction window.
    offsets=sorted(body)
    pivots={}
    for at,(op,arg,_) in body.items():
        if op != "putstatic": continue
        m=re.match(r"#(\d+)(?:\s|,|$)",arg)
        if not m: continue
        i=int(m.group(1))
        if reader.pool[i][0] != 9: continue
        _,owner,(_,name,desc)=reader.resolve(i)
        if owner==COMP and name in {"MAX_STACK_SIZE","MAX_DAMAGE","DAMAGE","COMMON_ITEM_COMPONENTS"}:
            pivots[name]=at
    require(set(pivots)=={"MAX_STACK_SIZE","MAX_DAMAGE","DAMAGE","COMMON_ITEM_COMPONENTS"},"component initializer field pivots")
    center=offsets.index(pivots["COMMON_ITEM_COMPONENTS"])
    window=offsets[max(0,center-100):center+1]
    members=[]
    for at in window:
        op,arg,symbol=body[at]
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        if match and reader.pool[int(match[1])][0] in (9,10,11):
            _,owner,(_,name,desc)=reader.resolve(int(match[1]))
            members.append({"offset":at,"opcode":op,"owner":owner,"name":name,"descriptor":desc})
    return {"name":decl["name"],"descriptor":decl["descriptor"],"code_sha256":decl["code_sha256"],
            "instruction_sha256":summarize(reader,(decl["name"],decl["descriptor"]),body)["instruction_sha256"],
            "instruction_count":len(body),"projection":"BOUNDED_COMMON_ITEM_COMPONENTS_WINDOW",
            "field_write_pivots":pivots,"typed_members":members,
            "numeric_operands":[{"offset":at,"opcode":body[at][0],"operand":body[at][1],"symbol":body[at][2]}
                                for at in window if numeric(body[at][0],body[at][2])],
            "opcode_window":[{"offset":at,"opcode":body[at][0]} for at in window]}

def scan(args):
    identity={}
    for name,(sha,size) in DIST.items():
        raw=getattr(args,name).read_bytes()
        require(len(raw)==size and digest(raw)==sha,"distribution mismatch "+name)
        identity[name]={"sha256":sha,"bytes":size}
    verify_artifact(args.publisher)
    identity["publisher"]={"sha1":SHA1,"sha256":SHA256,"bytes":SIZE}
    order=("server","universal","srg","publisher")
    seen=set()
    result={}
    with ExitStack() as stack:
        archives={name:stack.enter_context(ZipFile(getattr(args,name))) for name in order}
        rosters={}
        for name,z in archives.items():
            paths=z.namelist()
            require(len(paths)==len(set(paths)),"duplicate paths "+name)
            rosters[name]=set(paths)
        cp=":".join(str(getattr(args,name)) for name in order)
        for owner in sorted(SELECT):
            sources=[name for name in order if owner+".class" in rosters[name]]
            if not sources:
                require(owner not in REQUIRED and owner not in PINS,"required owner absent "+owner)
                result[owner]={"present":False}
                continue
            raw=archives[sources[0]].read(owner+".class")
            sha=digest(raw)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"class identity "+owner)
            require(owner not in PINS or sha==PINS[owner],"prior class identity "+owner)
            declarations=[d for d in reader.methods if selected(owner,d)]
            require(len(declarations)<=32,"per-owner method budget")
            require(REQUIRED.get(owner,set())<={d["name"] for d in declarations if "code_sha256" in d},
                    "required executable name absent "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"])
                qualified=(owner,*key)
                if "code_sha256" not in d:
                    require(qualified not in KNOWN,"prior Code absent "+str(qualified))
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"missing parsed method "+str(qualified))
                if qualified in KNOWN:
                    require(d["code_sha256"]==KNOWN[qualified],"prior Code mismatch "+str(qualified))
                    seen.add(qualified)
                row=(project_component_defaults(reader,parsed[key],d)
                     if owner==COMP and key[0]=="<clinit>" else projection(reader,key,parsed[key],d))
                row["exception_handlers"]=d["exception_handlers"]
                row["executable"]=True
                methods.append(row)
            result[owner]={"present":True,"source":sources[0],"available_sources":sources,"class_sha256":sha,
                           "parent":reader.parent,"interfaces":reader.interfaces,
                           "declared_signatures":[[d["name"],d["descriptor"]] for d in reader.methods],
                           "methods":methods}
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    for owner,name,sha in ((REGISTRY,"lambda$static$105","c69181618911cbcd762e36a54c5de44dae0a49af9b0841994acddb24b4630096"),
                           (REGISTRY,"lambda$static$106","78b65499de90c40a538c2b78c0b5d60b12730fc55811b77593c435e0f8d97993"),
                           (REGISTRY,"lambda$static$164","f18af631ec58d5bf8d6b350215a8fab261c218eac2b135b5d8c4fced5e106d53"),
                           (ENTITYREG,"lambda$static$43","5f095071ddceb4d09df9169080fcd8cda9d0fdbe185340560e692aa7b63d0fe7")):
        rows=[m for m in result[owner]["methods"] if m["name"]==name]
        require(len(rows)==1 and rows[0].get("code_sha256")==sha,"known registry Code mismatch "+name)
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"limits":LIMITS}

def self_test():
    require(selected(PROPS,{"name":"buildComponents"}),"observed body selection")
    require(selected(RECIPE,{"name":"lambda$static$0"}),"recipe bootstrap candidates")
    require(not selected(RECIPE,{"name":"unrelated"}),"out-of-scope recipe method")
    require(not selected(REGISTRY,{"name":"lambda$static$107"}),"unrelated factory")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: five scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in (*DIST,"publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--linkage",action="store_true",help="separate extended supplier and codec linkage report")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in (*DIST,"publisher","output")) and not a.output.exists(),
                "all exact inputs and write-once output required")
        if a.linkage:
            SELECT[STACK].update({"<clinit>", "lambda$static$4", "lambda$static$8",
                                  "validateStrict", "validateComponents"})
            SELECT[TYPE].update({"defaultTrackingRangeSupplier", "defaultUpdateIntervalSupplier",
                                 "defaultTrackDeltasSupplier"})
            SELECT[BUILDER].update({"lambda$setUpdateInterval$1", "lambda$setTrackingRange$2",
                                    "lambda$setShouldReceiveVelocityUpdates$3"})
            SELECT[ITEM].update({"getMaxStackSize", "getMaxDamage"})
            REQUIRED[STACK] = {"<clinit>", "lambda$static$4"}
            REQUIRED[TYPE] = {"defaultTrackingRangeSupplier", "defaultUpdateIntervalSupplier",
                              "defaultTrackDeltasSupplier"}
            REQUIRED[BUILDER].update({"lambda$setUpdateInterval$1", "lambda$setTrackingRange$2",
                                      "lambda$setShouldReceiveVelocityUpdates$3"})
            PINS[BUILDER] = "426b62fad78c0cadfdc7867a2ed48adb2977e80bd5447228a65638197a4e9c09"
        report=scan(a)
        raw=canonical(report).encode()
        require(len(raw)<=3_000_000,"report byte budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as out:
            out.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
            for m in row.get("methods",[]):
                print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
