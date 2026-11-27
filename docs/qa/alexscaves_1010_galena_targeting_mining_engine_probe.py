#!/usr/bin/env python3
"""Exact Galena raycast, mining and block settlement engine discovery.
No gameplay execution, no mutation. Publisher causal callsites are reused.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric, MATH
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

MC = "net/minecraft/"
CHUNK = "net/neoforged/neoforge/common/world/chunk/"
AC = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
WEAPON = "com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
PIN = {
    MC+"world/entity/Entity": "4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    MC+"world/entity/player/Player": "277a886c7267e82baa4378282e3c892f16338c0a6a779f1cf361a0af7d7b09fd",
    MC+"world/item/ItemStack": "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
}
UNIVERSAL_SHA = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
UNIVERSAL_SIZE = 3551268
ALL_BODIES = set()
SELECTED = {
    MC+"world/entity/projectile/ProjectileUtil": {"getHitResultOnViewVector","getHitResult","getEntityHitResult","getHitResultOnMoveVector"},
    MC+"world/entity/Entity": {"canBeHitByProjectile","isPickable","getPickRadius","pick","getEyePosition","getViewVector","getRootVehicle","isPassengerOfSameVehicle"},
    MC+"world/level/BlockGetter": {"clip","clipWithInteractionOverride","traverseBlocks"},
    MC+"world/phys/AABB": {"clip","expandTowards","inflate","contains","intersects"},
    MC+"world/level/Level": {"destroyBlock","destroyBlockProgress","getEntities"},
    MC+"world/level/LevelAccessor": {"destroyBlock"},
    MC+"world/level/block/Block": {"playerDestroy","dropResources","getDrops","popExperience","popResource","playerWillDestroy","getExpDrop"},
    MC+"world/level/block/ShulkerBoxBlock": {"playerDestroy","playerWillDestroy","getDrops"},
    MC+"world/level/block/state/BlockBehaviour$BlockStateBase": {"getDestroySpeed","getDrops","getDestroyProgress","getExpDrop"},
    MC+"world/item/ItemStack": {"mineBlock","getDestroySpeed","isCorrectToolForDrops","hurtEnemy"},
    MC+"world/item/Item": {"mineBlock","getDestroySpeed","isCorrectToolForDrops","hurtEnemy"},
    MC+"world/item/DiggerItem": {"mineBlock","hurtEnemy"},
    MC+"world/entity/player/Player": {"getDestroySpeed","hasCorrectToolForDrops","canInteractWithBlock","causeFoodExhaustion"},
    MC+"server/level/ServerPlayerGameMode": {"destroyBlock","handleBlockBreakAction"},
    "net/neoforged/neoforge/event/EventHooks": {"getBreakSpeed","onPlayerDestroyItem","onBlockBreak"},
    "net/neoforged/neoforge/common/CommonHooks": {"fireBlockBreak","onBlockBreakEvent","onBlockBreak","onBlockDrops"},
    "net/neoforged/neoforge/common/extensions/IBlockExtension": {"getExpDrop"},
    "net/neoforged/neoforge/common/extensions/IBlockStateExtension": {"getExpDrop"},
}
REQUIRED = {
    MC+"world/entity/projectile/ProjectileUtil": {"getHitResultOnViewVector","getEntityHitResult"},
    MC+"world/entity/Entity": {"canBeHitByProjectile"},
    MC+"world/level/Level": {"destroyBlock"},
    MC+"world/level/block/Block": {"playerDestroy","dropResources","popExperience"},
    MC+"world/item/ItemStack": {"mineBlock","getDestroySpeed"},
    MC+"server/level/ServerPlayerGameMode": {"destroyBlock"},
    "net/neoforged/neoforge/event/EventHooks": {"getBreakSpeed","onPlayerDestroyItem"},
}
LIMITS = {
    "actual_target_selection":"NOT_VERIFIED", "actual_block_destruction":"NOT_VERIFIED",
    "actual_drops_and_xp":"NOT_VERIFIED", "actual_claims_authorization":"NOT_VERIFIED",
    "runtime_loaded_bytes":"NOT_OBSERVED",
    "effective_config_and_tags":"NOT_VERIFIED", "world_safety":"BLOCKED",
    "static_contract":"NOT_CERTIFIED", "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED", "mutation":"NO_MUTATION",
    "semantic_magic_roots_delta":0, "provider_universe_closed":False,
}

def selected(owner,name):
    return owner in ALL_BODIES or name in SELECTED.get(owner,())

def scan(server,srg,universal,publisher,javap):
    identity=verify_distribution(server,srg)
    verify_artifact(publisher)
    identity['publisher']={'sha1':SHA1,'sha256':SHA256,'size_bytes':SIZE}
    data=universal.read_bytes()
    require(len(data)==UNIVERSAL_SIZE and hashlib.sha256(data).hexdigest()==UNIVERSAL_SHA,"universal pin mismatch")
    identity.update({"universal_sha256":UNIVERSAL_SHA,"universal_bytes":UNIVERSAL_SIZE})
    owners=sorted(ALL_BODIES|set(SELECTED))
    with ZipFile(server) as overlay, ZipFile(universal) as uni, ZipFile(srg) as vanilla, ZipFile(publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",overlay),("NEOFORGE_UNIVERSAL",uni),("INSTALLED_MINECRAFT_SRG",vanilla),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        classpath=":".join(map(str,(server,universal,srg,publisher)))
        classes={}
        for owner in owners:
            found=[(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False}
                continue
            source,z=found[0]
            raw=z.read(owner+".class")
            sha=digest(raw)
            require(owner not in PIN or sha==PIN[owner],"class SHA drift "+owner)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"owner/Java drift "+owner)
            declarations=[m for m in reader.methods if selected(owner,m["name"])]
            require(REQUIRED.get(owner,set()).issubset({m["name"] for m in declarations}),"required method absent "+owner)
            require(len(declarations)<=85,"method roster budget "+owner)
            parsed=disassemble(classpath,javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"missing body "+owner+str(key))
                body=parsed[key]
                row=analyze(reader,body,d)
                row["instruction_sha256"]=summarize(reader,key,body)["instruction_sha256"]
                row["executable"]=True
                row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym} for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
                row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op.startswith("ldc") and sym.startswith("String ")]
                row["bootstrap_links"]=bootstrap(reader,body)
                row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
                if key[0] in {"getHitResultOnViewVector","getHitResult","getEntityHitResult","destroyBlock","playerDestroy","mineBlock","getBreakSpeed","clip","popExperience"}:
                    row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore"))]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    return {"schema_version":1,"scope":"GALENA_TARGETING_MINING_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    require(selected(MC+"world/entity/projectile/ProjectileUtil","getHitResultOnViewVector"),"raycast scope")
    require(selected(MC+"world/level/Level","destroyBlock"),"world settlement scope")
    require(selected(MC+"server/level/ServerPlayerGameMode","destroyBlock"),"distinct player ingress scope")
    require(not selected("foreign/Level","destroyBlock"),"namespace scope")
    require(LIMITS["mutation"]=="NO_MUTATION","policy drift")
    print("PASS: four scope checks and policy check")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server",type=Path)
    p.add_argument("--srg",type=Path)
    p.add_argument("--universal",type=Path)
    p.add_argument("--publisher",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all((a.server,a.srg,a.universal,a.publisher,a.output)) and not a.output.exists(),"write-once report and artifacts required")
        result=scan(a.server,a.srg,a.universal,a.publisher,a.javap)
        data=canonical(result).encode()
        require(len(data)<=2_500_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:
            f.write(data)
        print("REPORT_SHA256",digest(data),"BYTES",len(data))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"))
            for m in row.get("methods",[]):
                print("METHOD",owner,m["name"],m["descriptor"],m.get("code_sha256"),m.get("instruction_count"))
                if m["executable"]:
                    print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")
