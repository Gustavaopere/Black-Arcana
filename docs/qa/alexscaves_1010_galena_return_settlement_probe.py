#!/usr/bin/env python3
"""Read-only exact Galena inventory restitution and fallback drop boundaries.

No runtime spawn simulation or item mutation. Prior publisher tick and spawn
admission proofs are reused; this projection examines distinct settlement.
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
    AC: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    WEAPON: "a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071",
    MC+"world/item/ItemStack": "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    MC+"world/entity/Entity": "4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    MC+"world/entity/player/Player": "277a886c7267e82baa4378282e3c892f16338c0a6a779f1cf361a0af7d7b09fd",
}
UNIVERSAL_SHA = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
UNIVERSAL_SIZE = 3551268
ALL_BODIES = set()
SELECTED = {
    AC: {"spawnAtLocation"},
    WEAPON: {"plopItem","getItemStack","setItemStack","addAdditionalSaveData","readAdditionalSaveData","getController"},
    MC+"world/entity/player/Player": {"addItem","drop"},
    MC+"world/entity/player/Inventory": {"add","addResource","getSlotWithRemainingSpace","getFreeSlot","hasRemainingSpaceForItem","placeItemBackInInventory","setItem","getItem","setChanged"},
    MC+"world/item/ItemStack": {"copy","copyWithCount","setCount","getCount","grow","shrink","isEmpty","isSameItemSameComponents","getMaxStackSize","isStackable","limitSize","split"},
    MC+"world/entity/Entity": {"spawnAtLocation","remove","setRemoved","discard"},
    MC+"world/entity/item/ItemEntity": {"<init>","setItem","getItem","playerTouch","setDefaultPickUpDelay"},
    "net/neoforged/neoforge/common/CommonHooks": {"onPlayerTossEvent","onItemPickup"},
}
REQUIRED = {
    AC: {"spawnAtLocation"},
    WEAPON: {"plopItem"},
    MC+"world/entity/player/Player": {"addItem"},
    MC+"world/entity/player/Inventory": {"add","addResource"},
    MC+"world/item/ItemStack": {"setCount","shrink","copy"},
    MC+"world/entity/Entity": {"spawnAtLocation","remove"},
    MC+"world/entity/item/ItemEntity": {"<init>","getItem"},
}
LIMITS = {
    "actual_inventory_restitution":"NOT_VERIFIED", "actual_spawn_acceptance":"NOT_VERIFIED",
    "actual_item_loss":"NOT_OBSERVED", "actual_item_duplication":"NOT_OBSERVED",
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
                if key[0] in {"add","addResource","spawnAtLocation","drop","plopItem","setCount","grow","shrink"}:
                    row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore"))]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    return {"schema_version":1,"scope":"GALENA_INVENTORY_RETURN_DROP_SETTLEMENT_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    require(selected(MC+"world/entity/player/Inventory","add"),"inventory scope")
    require(selected(WEAPON,"plopItem"),"publisher scope")
    require(selected(MC+"world/entity/Entity","spawnAtLocation"),"drop scope")
    require(not selected("foreign/Inventory","add"),"namespace scope")
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
        require(len(data)<=1_500_000,"report budget")
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
