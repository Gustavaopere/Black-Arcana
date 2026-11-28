#!/usr/bin/env python3
"""Read-only Marine Snow item identity, block mutation and spawn boundaries.
Exact publisher and distributed NeoForge 21.1.250; no game execution.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection, identified, verify_universal, ARTIFACTS

P="com/github/alexmodguy/alexscaves/server/"
M="net/minecraft/"
N="net/neoforged/neoforge/"
I=P+"item/MarineSnowItem"
IR=P+"item/ACItemRegistry"
ID="alexscaves:marine_snow"
PINS={I:"b7515b5195e7ae5f1aa4f82fb2fb9e93faa339ad3a754ea62313ce438db46526",
      IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"}
CODE_PINS={(I,"useOn"):"dec29a166ca2ab5e84b8f78f3c35d157e9403a293a0e97c167cc3a73adbcf206",
           (I,"scanForWater"):"ddd9d511d51511cf1831277df3c24e98fb1def06784b82327e63ccf71adf384d",
           (I,"initGrowth"):"73f1070a2c895ae97a6af0f4decd7e2f989b511b89cd328904986e17f0bc4c83",
           (I,"lambda$initGrowth$0"):"6329ada9dbdbe900f68e49a6134a370eb63c6ca3149014b96be32441baafd95f",
           (I,"lambda$initGrowth$1"):"0740caf393748346c5690ac6b98376eb85788337d545fc6f3b03b1645976d71f",
           (IR,"lambda$static$90"):"d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba"}
SELECT={
    IR:{"lambda$static$90"},
    P+"misc/ACCompat":{"sidedSuccess","lootTable","spawnAtLocation"},
    P+"block/MusselBlock":{"<clinit>","<init>","createBlockStateDefinition","updateShape","getFluidState","getStateForPlacement","canSurvive","randomTick","tick","getShape"},
    M+"world/item/context/UseOnContext":{"<init>","getPlayer","getItemInHand","getClickedPos","getClickLocation","getLevel"},
    M+"world/item/ItemStack":{"useOn","onItemUse","shrink","grow","setCount","getCount","copy","copyWithCount","isEmpty","getMaxStackSize","<init>"},
    M+"world/item/Item":{"useOn","getMaxStackSize","<init>","byBlock"},
    M+"world/item/Item$Properties":{"<init>","buildAndValidateComponents","buildComponents"},
    M+"world/item/BlockItem":{"registerBlocks"},
    M+"world/item/StandingAndWallBlockItem":{"registerBlocks","<init>"},
    M+"world/item/Items":{"registerItem","registerBlock"},
    M+"core/component/DataComponents":set(),
    M+"world/level/block/Block":{"asItem"},
    M+"world/level/block/BaseCoralWallFanBlock":{"asItem"},
    M+"world/entity/Entity":{"spawnAtLocation"},
    M+"world/level/storage/loot/LootTable":{"getRandomItems"},
    M+"server/network/ServerGamePacketListenerImpl":{"handleUseItemOn"},
    M+"server/level/ServerPlayerGameMode":{"useItemOn"},
    N+"common/CommonHooks":{"onPlaceItemIntoWorld","onRightClickBlock"},
    N+"event/EventHooks":{"onRightClickBlock","onBlockPlace","onMultiBlockPlace"},
    M+"world/level/Level":{"setBlockAndUpdate","setBlock","markAndNotifyBlock","mayInteract","addFreshEntity","levelEvent"},
    M+"server/level/ServerLevel":{"setBlock","addFreshEntity","addEntity","mayInteract","levelEvent"},
    M+"world/level/chunk/LevelChunk":{"setBlockState"},
    M+"world/level/block/state/StateHolder":{"hasProperty","getValue","setValue"},
    M+"world/level/block/state/BlockBehaviour$BlockStateBase":{"getFluidState","onPlace","onRemove","updateNeighbourShapes","updateIndirectNeighbourShapes"},
    M+"world/level/block/BaseCoralPlantTypeBlock":{"scanForWater","getFluidState","updateShape","tryScheduleDieTick"},
    M+"world/level/block/CoralBlock":{"tick","onPlace","updateShape","scanForWater"},
    M+"world/level/block/CoralPlantBlock":{"tick","onPlace","updateShape"},
    M+"world/level/block/CoralFanBlock":{"tick","onPlace","updateShape"},
    M+"world/level/block/CoralWallFanBlock":{"tick","onPlace","updateShape","asItem"},
    M+"world/level/block/SpongeBlock":{"onPlace","neighborChanged","tryAbsorbWater","removeWaterBreadthFirstSearch"},
    M+"world/entity/item/ItemEntity":{"<init>","setItem","getItem","tick","merge","tryToMerge","mergeWithNeighbours","isMergable","areMergable","playerTouch"},
    M+"network/syncher/SynchedEntityData":{"set","get","getItem"},
    M+"network/syncher/SynchedEntityData$DataItem":{"<init>","setValue","getValue","value"},
    M+"world/entity/player/Inventory":{"add","addResource","getSlotWithRemainingSpace","getFreeSlot"},
    M+"world/entity/player/Player":{"isCreative","mayUseItemAt","canInteractWithBlock","blockInteractionRange"},
    M+"world/level/entity/PersistentEntitySectionManager":{"addNewEntity","addEntity","addEntityUuid","addEntityWithoutEvent"},
}
REQUIRED={IR:{"lambda$static$90"},P+"misc/ACCompat":{"sidedSuccess"},
          M+"world/item/ItemStack":{"useOn","shrink"},
          M+"world/level/Level":{"setBlockAndUpdate","setBlock"},
          M+"world/entity/item/ItemEntity":{"<init>","setItem"},
          M+"server/level/ServerPlayerGameMode":{"useItemOn"},
          M+"world/level/block/state/StateHolder":{"setValue","getValue"},
          M+"server/level/ServerLevel":{"addFreshEntity","addEntity"}}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "runtime_loaded_bytes":"NOT_OBSERVED","world_effect_acceptance":"NOT_VERIFIED"}
def exact_refs(value,path=()):
    if isinstance(value,dict):
        for k,v in sorted(value.items()):
            if k==ID:yield [list(path+(k,)),"KEY"]
            yield from exact_refs(v,path+(k,))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from exact_refs(v,path+(i,))
    elif value==ID:yield [list(path),"VALUE"]

def inspect(a):
    verify_artifact(a.publisher)
    verify_universal(a.universal,"universal")
    artifact={"publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "installer":identified(a.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(a.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(a.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"],"neoforge_version":"21.1.250"}
    require(not a.output.exists(),"write once")
    with ZipFile(a.server) as ov,ZipFile(a.universal) as un,ZipFile(a.srg) as mc,ZipFile(a.publisher) as mod:
        archives=[("OVERLAY",ov),("UNIVERSAL",un),("SRG",mc),("PUBLISHER",mod)]
        require(all(len(z.namelist())==len(set(z.namelist())) for _,z in archives),"duplicate entries")
        index=[(n,z,set(z.namelist())) for n,z in archives]
        cp=":".join(map(str,(a.server,a.universal,a.srg,a.publisher)))
        roster=sorted(p for p in mod.namelist() if p.endswith(".class"))
        require(len(roster)==1555 and digest(("\n".join(roster)+"\n").encode())=="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed","roster")
        candidates=[]
        digestion=[]
        pigs=[]
        for path in roster:
            rd=ClassReader(mod.read(path))
            require(rd.name+".class"==path and rd.major==65,"publisher identity")
            refs=[v for v in rd.typed_refs(IR) if v["kind"]=="field_reference" and v["name"]=="MARINE_SNOW"]
            typed=rd.typed_refs(I)
            if refs or typed:candidates.append({"owner":rd.name,"field_refs":refs,"typed_refs":typed})
            if b"sea_pig_digestion" in mod.read(path):
                digestion.append(rd.name)
            if rd.name.rsplit("/",1)[-1]=="SeaPigEntity":
                pigs.append(rd.name)
        require(1<=len(digestion)<=20 and len(pigs)==1,"digestion candidate owner budget")
        require(len(candidates)<=100,"candidate budget")
        classes={}
        field_sites=[]
        for candidate in candidates:
            owner=candidate["owner"]
            if not candidate["field_refs"]:continue
            rd=ClassReader(mod.read(owner+".class"))
            body=disassemble(cp,a.javap,owner)
            ids={x["index"] for x in candidate["field_refs"]}
            for key,ins in sorted(body.items()):
                offsets=sorted(ins)
                for i,at in enumerate(offsets):
                    op,arg,sym=ins[at]
                    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if match and int(match[1]) in ids:
                        d=next(v for v in rd.methods if (v["name"],v["descriptor"])==key)
                        field_sites.append({"owner":owner,"method":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],
                            "offset":at,"window":[{"offset":q,"opcode":ins[q][0],"operand":ins[q][1],"symbol":ins[q][2]} for q in offsets[max(0,i-4):i+5]]})
        require(1<=len(field_sites)<=100,"field sites budget")
        loot_owners=set(digestion+pigs)
        tag_owners=[p[:-6] for p in roster if p.endswith("/ACTagRegistry.class")]
        require(len(tag_owners)==1,"tag registry identity")
        tag_rd=ClassReader(mod.read(tag_owners[0]+".class"))
        tag_methods=disassemble(cp,a.javap,tag_owners[0])
        tag_sites=[]
        for key,body in sorted(tag_methods.items()):
            offsets=sorted(body)
            for i,at in enumerate(offsets):
                op,arg,sym=body[at]
                if op=="putstatic" and any("Field "+n+":" in sym for n in ("SEA_PIG_DIGESTS","GROWS_MUSSELS")):
                    decl=next(d for d in tag_rd.methods if (d["name"],d["descriptor"])==key)
                    tag_sites.append({"owner":tag_rd.name,"method":key[0],"code_sha256":decl["code_sha256"],"offset":at,
                        "window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-6):i+1]]})
        require(len(tag_sites)==2,"two exact tag registration sites")
        item_rd=ClassReader(ov.read(M+"world/item/Items.class") if M+"world/item/Items.class" in index[0][2] else mc.read(M+"world/item/Items.class"))
        item_init=disassemble(cp,a.javap,item_rd.name)
        coral_bindings=[]
        for key,body in sorted(item_init.items()):
            if key[0]!="<clinit>":continue
            offsets=sorted(body)
            for i,at in enumerate(offsets):
                op,arg,sym=body[at]
                if op=="getstatic" and any("Blocks."+c+"_CORAL_WALL_FAN:" in sym for c in ("TUBE","BRAIN","BUBBLE","FIRE","HORN")) and "DEAD_" not in sym:
                    decl=next(d for d in item_rd.methods if (d["name"],d["descriptor"])==key)
                    coral_bindings.append({"owner":item_rd.name,"code_sha256":decl["code_sha256"],"offset":at,
                       "window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-8):i+16]]})
        require(len(coral_bindings)==5,"five living wall fan bindings")
        for owner in sorted(set(SELECT)|{I}|loot_owners):
            found=[(n,z) for n,z,paths in index if owner+".class" in paths]
            if not found:
                require(owner not in REQUIRED and owner!=I,"missing required owner "+owner)
                classes[owner]={"present":False};continue
            source,z=found[0];raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            require(owner not in PINS or digest(raw)==PINS[owner],"class pin "+owner)
            parsed=disassemble(cp,a.javap,owner)
            selected_names=SELECT.get(owner,set())
            extra=set()
            if owner in loot_owners:
                for key,body in parsed.items():
                    if any("sea_pig_digestion" in sym.lower() or "SEA_PIG_DIGESTION" in sym or "LootTable" in sym or "getRandomItems" in sym for op,arg,sym in body.values()):
                        extra.add(key)
                    elif owner in pigs and any(token in key[0].lower() for token in ("digest","eat","save","tick","interact","feed","spawn")):
                        extra.add(key)
            decls=[d for d in rd.methods if owner==I or d["name"] in selected_names or (d["name"],d["descriptor"]) in extra]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required method "+owner)
            require(len(decls)<=100,"method budget "+owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                pin=CODE_PINS.get((owner,key[0]))
                require(pin is None or d.get("code_sha256")==pin,"Code pin "+owner+str(key))
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False});continue
                require(key in parsed and 0<len(parsed[key])<=5000,"body budget "+owner+str(key))
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            classes[owner]={"present":True,"source":source,"class_sha256":digest(raw),"parent":rd.parent,
                            "declarations":rd.methods,"methods":methods}
        resources={}
        paths=sorted(p for p in mod.namelist() if p.startswith("data/") and p.endswith(".json"))
        require(len(paths)<=5000,"resource budget")
        for p in paths:
            raw=mod.read(p);require(len(raw)<=2_000_000,"resource size")
            obj=json.loads(raw);hits=list(exact_refs(obj))
            if hits or p.rsplit("/",1)[-1] in {"marine_snow.json","sea_pig_digests.json","grows_mussels.json"}:
                resources[p]={"sha256":digest(raw),"bytes":len(raw),"refs":hits,"data":obj}
        require(len(resources)<=100,"resource hit budget")
        require(digest(mod.read("assets/alexscaves/models/item/marine_snow.json"))=="179f4314608e9b3f7b8351759bc30e0a1641620c978e909f568e9daf31e4451c","model pin")
    report={"schema":4,"artifact":artifact,"classes":classes,"publisher_candidates":candidates,
            "data_json_count":len(paths),"resources":resources,"field_sites":field_sites,"loot_string_owners":digestion,"loot_owners":sorted(loot_owners),"tag_sites":tag_sites,"coral_bindings":coral_bindings,"limits":LIMITS}
    data=canonical(report).encode();require(len(data)<=12000000,"report budget")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("xb") as f:f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,v in classes.items():
        print("OWNER",owner,v.get("source"),v.get("class_sha256"),"METHODS",len(v.get("methods",[])))
        for m in v.get("methods",[]):print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
    print("PUBLISHER_CANDIDATES",json.dumps(candidates,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("FIELD_SITES",json.dumps(field_sites,sort_keys=True))
    print("TAG_SITES",json.dumps(tag_sites,sort_keys=True))
    print("CORAL_BINDINGS",json.dumps(coral_bindings,sort_keys=True))
    print("LOOT_CANDIDATES",json.dumps({"strings":digestion,"owners":sorted(loot_owners)},sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(list(exact_refs({"x":[ID,ID+"_other"],ID:0}))==[[[ID],"KEY"],[["x",0],"VALUE"]],"exact resource filter")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    require(len(CODE_PINS)==6,"prior body pin roster")
    print("PASS scope and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"inputs")
        inspect(a)
