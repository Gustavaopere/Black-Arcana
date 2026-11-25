#!/usr/bin/env python3
"""Bounded Remote Detonator dimension codec and target lookup audit, 1.0.10/21.1.250.
Read-only classfile projection; no game execution or world mutation.
"""
from __future__ import annotations
import argparse
import json
from contextlib import ExitStack
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

MC = "net/minecraft/"
NF = "net/neoforged/neoforge/"
P = "com/github/alexmodguy/alexscaves/server/"
REMOTE = P+"item/RemoteDetonatorItem"
COMPAT = P+"misc/ACCompat"
LEVEL = MC+"world/level/Level"
KEY = MC+"resources/ResourceKey"
LOC = MC+"resources/ResourceLocation"
OPS = MC+"nbt/NbtOps"
TAG = MC+"nbt/CompoundTag"
GLOBAL = MC+"core/GlobalPos"
SERVER = MC+"server/MinecraftServer"
SELECT = {
    REMOTE: {"<init>","acInventoryTick","addBombTags","appendHoverText","getBombDimension","getBombPosition","isActive","lambda$addBombTags$0","loadChunksAround","use","useOn"},
    COMPAT: {"getBlockPos","putBlockPos","posFromTag","getTag","getOrCreateTag","setTag"},
    LEVEL: {"<clinit>","dimension","isLoaded"},
    KEY: {"codec","create","createRegistryKey","location","registry","isFor","<init>"},
    LOC: {"<clinit>","read","parse","tryParse","getNamespace","getPath","toString"},
    OPS: {"getStringValue","createString","get","<clinit>"},
    TAG: {"contains","get","put","remove","getCompound","getBoolean","getInt"},
    GLOBAL: {"of","dimension","pos","<init>"},
    SERVER: {"getLevel"},
    MC+"world/level/ChunkPos": {"<init>","asLong","getX","getZ"},
}
PREFIXES = {KEY:("lambda$codec$",),LOC:("lambda$static$",)}
PINS = {
    REMOTE: "6d6e8cd94df306aec6f99b07af856b477b8e6f34d41aaca06a35921b53f2c4b8",
    COMPAT: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    LEVEL: "74a062f0d480674152fa4665bd7b483fca52de8dd3b07178c1a6c40d3fae3fae",
    TAG: "93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6",
}
KNOWN = {
    (COMPAT,"getTag","(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/nbt/CompoundTag;"):
        "b9e087e9252353b89150604a38e9421c5c258cfb853640d5de2b1b7968d78b13",
    (TAG,"getBoolean","(Ljava/lang/String;)Z"):
        "f767371f026e90d6f4444cda7f08280c44f1615f814b9c9e506e0882ef8def09",
    (TAG,"contains","(Ljava/lang/String;I)Z"):
        "95a0338ac124d2d74d9db18dbc9cdca3a9a42c3dd4de54c2085bef5bdb5eba4e",
}
INSTRUCTION_PINS = {
    (REMOTE,"<init>","()V"): "b1e09b957153a9a6359f7e966a0e90b94486659c93dab03cdd80143d7694857c",
    (REMOTE,"acInventoryTick","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V"): "f4cc16efcad69f1d972579c96944647c63101110402e2cbb7bfb2f6da68a896d",
    (REMOTE,"addBombTags","(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/BlockPos;Lnet/minecraft/nbt/CompoundTag;)V"): "7ee1a457812d9ff8533b207924d21d20402b133e4ebd32ff086d68d0935bc7bc",
    (REMOTE,"appendHoverText","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item$TooltipContext;Ljava/util/List;Lnet/minecraft/world/item/TooltipFlag;)V"): "cde153556ffe430eed0a7b2705567bc75f8f6c92cd9418aeb799bd5df5e8066b",
    (REMOTE,"getBombDimension","(Lnet/minecraft/nbt/CompoundTag;)Ljava/util/Optional;"): "1a390410cb5cbab016724851e1a651fd4058a03b60ddd222d9790ab7378da895",
    (REMOTE,"getBombPosition","(Lnet/minecraft/nbt/CompoundTag;)Lnet/minecraft/core/GlobalPos;"): "2cad344367fe18da88b99d17e0c48f2e783f551c2fe2bc19e1b66b884b372d6f",
    (REMOTE,"isActive","(Lnet/minecraft/world/item/ItemStack;)Z"): "a4206726462cada693fbb76134f1f993eef006fd413472c62a9c875e7bf0f4a7",
    (REMOTE,"lambda$addBombTags$0","(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/nbt/Tag;)V"): "71af9311612389eca81fd9c9d49099631bfa9ac767ba83ec76b510e59271d3b5",
    (REMOTE,"loadChunksAround","(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;Lnet/minecraft/core/BlockPos;Z)V"): "f4f0e6461aac38df4743cfe80382fdebf89502db634317b1698f514034297cb5",
    (REMOTE,"use","(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;"): "ac995eaff92b4b833cbff5449f490c6fb7a754a2cdcfe3daa7b7fccfbe2e7934",
    (REMOTE,"useOn","(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;"): "659147c0f41037f2d3e00d8f9d83a025b13d72badc4dc327bf4a8bf93d83f772",
}
REQUIRED = {
    REMOTE: SELECT[REMOTE],
    COMPAT: {"getBlockPos","putBlockPos"},
    LEVEL: {"<clinit>","dimension"},
    KEY: {"codec","create","location"},
    LOC: {"<clinit>"},
    OPS: {"getStringValue","createString"},
    TAG: {"get","contains","put","remove"},
    GLOBAL: {"of","dimension","pos"},
    SERVER: {"getLevel"},
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
          "dimension_codec_runtime":"NOT_VERIFIED","actual_chunk_lifecycle":"NOT_VERIFIED","world_safety":"BLOCKED",
          "active_datapacks":"NOT_OBSERVED"}

def selected(owner, declaration):
    name=declaration["name"]
    return name in SELECT.get(owner, set()) or name.startswith(PREFIXES.get(owner, ()))

def scan(args):
    identity={}
    for name,(sha,size) in DIST.items():
        raw=getattr(args,name).read_bytes()
        require(len(raw)==size and digest(raw)==sha,"distribution mismatch "+name)
        identity[name]={"sha256":sha,"bytes":size}
    verify_artifact(args.publisher)
    identity["publisher"]={"sha1":SHA1,"sha256":SHA256,"bytes":SIZE}
    order=("server","universal","srg","publisher")
    seen=set(); instructions_seen=set()
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
                row=projection(reader,key,parsed[key],d)
                if qualified in INSTRUCTION_PINS:
                    require(row["instruction_sha256"]==INSTRUCTION_PINS[qualified],"native instruction drift "+str(qualified))
                    instructions_seen.add(qualified)
                row["exception_handlers"]=d["exception_handlers"]
                row["executable"]=True
                methods.append(row)
            result[owner]={"present":True,"source":sources[0],"available_sources":sources,"class_sha256":sha,
                           "parent":reader.parent,"interfaces":reader.interfaces,
                           "declared_signatures":[[d["name"],d["descriptor"]] for d in reader.methods],
                           "methods":methods}
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(instructions_seen==set(INSTRUCTION_PINS),"native roster coverage mismatch")
    require(len(result[REMOTE]["declared_signatures"])==11,"native owner roster drift")
    def native(name):
        rows=[x for x in result[REMOTE]["methods"] if x["name"]==name and x.get("executable")]
        require(len(rows)==1,"exact local method missing "+name)
        return rows[0]
    def references(row,owner,name):
        return any(x["owner"]==owner and x["name"]==name for x in row["typed_members"])
    require(references(native("addBombTags"),LEVEL,"RESOURCE_KEY_CODEC"),"encode key field")
    require(references(native("getBombDimension"),LEVEL,"RESOURCE_KEY_CODEC"),"decode key field")
    require(references(native("use"),SERVER,"getLevel"),"target dimension lookup")
    require(references(native("use"),LEVEL,"setBlockAndUpdate"),"origin level mutation callsite")
    require(references(native("getBombPosition"),GLOBAL,"of"),"global position factory")
    require(sum(len(v.get("methods",[])) for v in result.values())<=180,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"limits":LIMITS}

def self_test():
    require(selected(REMOTE,{"name":"getBombDimension"}),"native decoder")
    require(selected(KEY,{"name":"codec"}),"resource key codec")
    require(selected(KEY,{"name":"lambda$codec$0"}),"codec bootstrap candidate")
    require(not selected("foreign/ResourceKey",{"name":"codec"}),"owner boundary")
    require(len(INSTRUCTION_PINS)==11,"native instruction pins")
    require(all(names<=SELECT[owner] for owner,names in REQUIRED.items()),"required scope")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["world_safety"]=="BLOCKED","policy")
    print("PASS: seven scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in (*DIST,"publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in (*DIST,"publisher","output")) and not a.output.exists(),
                "all exact inputs and write-once output required")
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
