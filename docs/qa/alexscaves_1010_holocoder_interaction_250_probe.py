#!/usr/bin/env python3
"""Bounded read-only Holocoder interaction ingress and inventory settlement discovery.

Project exact distributed method bodies, typed calls, exception-table entries and
bootstrap handles. No game execution, loaded-mod inference or mutation.
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
PACKET = MC+"network/protocol/game/ServerboundInteractPacket"
LISTENER = MC+"server/network/ServerGamePacketListenerImpl"
PLAYER = MC+"world/entity/player/Player"
INV = MC+"world/entity/player/Inventory"
HOOKS = NF+"event/EventHooks"
EVENT = NF+"event/entity/player/PlayerInteractEvent"
SELECT = {
    PACKET: {"getTarget","dispatch","isUsingSecondaryAction","handle"},
    LISTENER: {"handleInteract","handleUseItemOn"},
    MC+"server/level/ServerPlayerGameMode": {"useItemOn"},
    PLAYER: {"interactOn","addItem","drop","canInteractWithEntity","canInteractWithBlock","entityInteractionRange","blockInteractionRange"},
    INV: {"add","addResource","getSlotWithRemainingSpace","getFreeSlot","hasRemainingSpaceForItem"},
    MC+"world/item/ItemStack": {"interactLivingEntity","shrink","setCount"},
    MC+"world/entity/item/ItemEntity": {"setNoPickUpDelay","setThrower","setTarget","setOwner"},
    MC+"world/level/block/state/BlockBehaviour$BlockStateBase": {"useItemOn","useWithoutItem"},
    HOOKS: {"onPlayerDestroyItem"},
    NF+"common/CommonHooks": {"onInteractEntity","onInteractEntityAt","onRightClickBlock","onPlayerTossEvent"},
    MC+"world/item/crafting/ShapedRecipe$Serializer": {"<clinit>"},
    EVENT: {"getItemStack","getHand","getCancellationResult","setCancellationResult"},
    EVENT+"$EntityInteract": {"<init>","getTarget","setCanceled"},
    EVENT+"$RightClickBlock": {"getUseBlock","getUseItem","getCancellationResult","setCanceled"},
    P+"event/CommonEvents": {"playerEntityInteract","acPlayerEntityInteract"},
    P+"block/HologramProjectorBlock": {"acUse","useItemOn","useWithoutItem"},
    P+"misc/ACPlatform": {"serializeEntity","setThrower"},
}
PINS = {
    P+"event/CommonEvents":"d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43",
    P+"block/HologramProjectorBlock":"ec685ba2b8db000916105c2696f61372e7ee9f93893529bfe196c262dce465fe",
    MC+"world/item/ItemStack":"072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    HOOKS:"f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b",
}
KNOWN = {
    (P+"event/CommonEvents","playerEntityInteract","(Lnet/neoforged/neoforge/event/entity/player/PlayerInteractEvent$EntityInteract;)V"):
        "44cf312d726d32a58c7fecbcf9ad5343f74c876aa65fde68560fe39109a3428f",
    (P+"event/CommonEvents","acPlayerEntityInteract","(Lnet/neoforged/neoforge/event/entity/player/PlayerInteractEvent$EntityInteract;)Z"):
        "50a28415d8f42606dbb9c6530476bf13257fe018cfbf924e0140f243049d2e93",
    (P+"misc/ACPlatform","serializeEntity","(Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/nbt/CompoundTag;"):
        "c21f4f21673302dc2313d610adb2c4b2371d841182a35908be14c4da1cedc1b3",
}
REQUIRED = {
    NF+"common/CommonHooks":{"onInteractEntity","onInteractEntityAt","onRightClickBlock","onPlayerTossEvent"},
    MC+"world/item/crafting/ShapedRecipe$Serializer":{"<clinit>"},
    LISTENER:{"handleInteract","handleUseItemOn"},
    PACKET:{"dispatch","getTarget"},
    MC+"server/level/ServerPlayerGameMode":{"useItemOn"},
    PLAYER:{"interactOn","addItem","drop"},
    INV:{"add","addResource"},
    MC+"world/item/ItemStack":{"shrink","setCount"},
    P+"event/CommonEvents":{"playerEntityInteract","acPlayerEntityInteract"},
    P+"block/HologramProjectorBlock":{"acUse","useItemOn"},
    P+"misc/ACPlatform":{"serializeEntity","setThrower"},
}
NESTED_NAMES = {"onInteraction","onAttack","performInteraction","dispatch","getType","getActionType"}
DIST = {
    "installer": ("0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60", 6972109),
    "server": ("1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359", 5675624),
    "srg": ("26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71", 14246609),
    "universal": ("1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956", 3551255),
}
LIMITS = {"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED","physical_qa":"NOT_TESTED",
          "mutating_hook":"NOT_VERIFIED","mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED",
          "capture_inventory_settlement":"NOT_VERIFIED","physical_packet_authority":"NOT_VERIFIED"}

def selected(owner, declaration):
    return declaration["name"] in SELECT.get(owner, set())

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
        nested=sorted({path[:-6] for paths in rosters.values() for path in paths
                       if path.endswith(".class") and path.startswith((LISTENER+"$",PACKET+"$"))})
        require(len(nested)<=48,"nested packet roster budget")
        for owner in nested:
            source=next(name for name in order if owner+".class" in rosters[name])
            reader=ClassReader(archives[source].read(owner+".class"))
            names={d["name"] for d in reader.methods} & NESTED_NAMES
            if names:
                SELECT[owner]=names|{"<init>"}
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
                row["exception_handlers"]=d["exception_handlers"]
                row["executable"]=True
                methods.append(row)
            result[owner]={"present":True,"source":sources[0],"available_sources":sources,"class_sha256":sha,
                           "parent":reader.parent,"interfaces":reader.interfaces,
                           "declared_signatures":[[d["name"],d["descriptor"]] for d in reader.methods],
                           "methods":methods}
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"nested_packet_candidates":nested,"limits":LIMITS}

def self_test():
    require(selected(LISTENER,{"name":"handleInteract"}),"network ingress")
    require(selected(PLAYER,{"name":"interactOn"}),"native dispatch")
    require(selected(INV,{"name":"add"}),"inventory settlement")
    require(not selected("foreign/Inventory",{"name":"add"}),"namespace")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: five scope and policy checks")

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
