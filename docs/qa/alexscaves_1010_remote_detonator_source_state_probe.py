#!/usr/bin/env python3
"""Focused read-only exact TNT source/calculator and Remote Detonator state boundaries.

Reuses distributed archive identity; records arithmetic and member pivots,
not a replacement implementation or a transformed-runtime observation.
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
from alexscaves_1010_remote_detonator_resource_probe import PINS, RECIPE, ADV, decode, need
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

MC = "net/minecraft/"
CHUNK = "net/neoforged/neoforge/common/world/chunk/"
AC = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
TRIGGER = "com/github/alexmodguy/alexscaves/server/misc/ACAdvancementTrigger"
TRIGGER_REGISTRY = TRIGGER + "Registry"
PRIMED = MC+"world/entity/item/PrimedTnt"
PIN = {
    MC+"world/level/Explosion": "3b656cd810d9fbbe001b4477ee5dff9f243c75d42458cd54fababed971da3e07",
    MC+"world/level/ExplosionDamageCalculator": "3151422d92b8c3bb8c399afb977bbf041136998dee337c10c54f60d73ca8a6a6",
    MC+"world/level/EntityBasedExplosionDamageCalculator": "b9a1fe9a2d1a8134028576e69d512766483df3a0f38e83819682f895c6fdf827",
    AC: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
}
UNIVERSAL_SHA = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
UNIVERSAL_SIZE = 3551268
ALL_BODIES = {MC+"world/level/ExplosionDamageCalculator",MC+"world/level/EntityBasedExplosionDamageCalculator"}
SELECTED = {
    MC+"world/level/Explosion": {"<init>","getDefaultDamageSource","getIndirectSourceEntityInternal","getIndirectSourceEntity","getDirectSourceEntity","makeDamageCalculator","getSeenPercent","radius","center"},
    MC+"world/damagesource/DamageSources": {"explosion","source"},
    MC+"world/damagesource/DamageSource": {"<init>","getEntity","getDirectEntity","isIndirect"},
    MC+"world/item/component/CustomData": {"<init>","of","copyTag","getUnsafe","update","set","isEmpty","<clinit>"},
    MC+"world/item/ItemStack": {"get","getOrDefault","set","remove","save","saveOptional","parse","parseOptional","copy","copyWithCount","applyComponents","use","useOn"},
    AC: {"getTag","getOrCreateTag","setTag","putBlockPos","getBlockPos","mayInteract","contains","getCompound","posFromTag","getInt","getBoolean","useSuccess","usePass"},
    TRIGGER: {"<init>","trigger","getId","codec","createInstance"},
    TRIGGER_REGISTRY: set(),
    PRIMED: {"<clinit>"},
    MC+"nbt/CompoundTag": {"contains","getCompound","getInt","getBoolean"},
    MC+"server/level/ServerPlayerGameMode": {"useItem","useItemOn"},
    MC+"server/network/ServerGamePacketListenerImpl": {"handleUseItem","handleUseItemOn"},
}
REQUIRED = {
    MC+"world/level/Explosion": {"getDefaultDamageSource","getIndirectSourceEntityInternal","getDirectSourceEntity"},
    MC+"world/level/ExplosionDamageCalculator": {"getEntityDamageAmount"},
    MC+"world/item/component/CustomData": {"of","copyTag"},
    AC: {"getTag","getOrCreateTag","setTag","putBlockPos","getBlockPos","posFromTag"},
    TRIGGER_REGISTRY: set(),
    TRIGGER: set(),
    MC+"server/level/ServerPlayerGameMode": {"useItem","useItemOn"},
    MC+"server/network/ServerGamePacketListenerImpl": {"handleUseItem","handleUseItemOn"},
}
LIMITS = {
    "actual_ignition":"NOT_VERIFIED", "actual_damage":"NOT_VERIFIED",
    "actual_ticket_acceptance":"NOT_VERIFIED", "actual_ticket_release":"NOT_VERIFIED",
    "actual_persistent_ticket_leak":"NOT_OBSERVED", "runtime_loaded_bytes":"NOT_OBSERVED",
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
    owners=set(ALL_BODIES)|set(SELECTED)
    with ZipFile(server) as overlay, ZipFile(universal) as uni, ZipFile(srg) as vanilla, ZipFile(publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",overlay),("NEOFORGE_UNIVERSAL",uni),("INSTALLED_MINECRAFT_SRG",vanilla),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        classpath=":".join(map(str,(server,universal,srg,publisher)))
        # Discover nested portal calculator and trigger classes by exact namespace;
        # do not assume their names or presence.
        nested={entry[:-6] for _,_,entries in roster for entry in entries
                if entry.endswith(".class") and (entry.startswith(PRIMED+"$") or entry.startswith(TRIGGER+"$"))}
        require(len(nested)<=12,"nested class scope")
        classes={}
        for owner in sorted(owners|nested):
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
            declarations=[m for m in reader.methods if selected(owner,m["name"]) or owner in nested]
            require(REQUIRED.get(owner,set()).issubset({m["name"] for m in declarations}),"required method absent "+owner)
            require(len(declarations)<=85,"method roster budget "+owner)
            parsed=disassemble(classpath,javap,owner)
            methods=[]
            special={}
            if owner==TRIGGER_REGISTRY:
                key=("<clinit>","()V")
                require(key in parsed and bool(parsed[key]),"missing advancement registry initializer")
                body=parsed[key]
                offsets=sorted(body)
                hits=[at for at,(op,arg,sym) in body.items() if "REMOTE_DETONATION" in sym or sym=="String remote_detonation"]
                require(0<len(hits)<=8,"remote advancement registry anchors")
                windows=[]
                for at in hits:
                    i=offsets.index(at)
                    windows.append({"anchor":at,"pivots":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]}
                        for q in offsets[max(0,i-7):i+4]]})
                special={"registry_initializer_sha256":summarize(reader,key,body)["instruction_sha256"],"remote_detonation_windows":windows,
                         "bootstrap_links":bootstrap(reader,body)}
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
                row["type_operands"]=[{"offset":at,"opcode":op,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op in {"instanceof","checkcast","new"}]
                if key[0] in {"getEntityDamageAmount","getIndirectSourceEntityInternal","getDefaultDamageSource","explosion","source","<init>","posFromTag","getInt","getCompound","contains"}:
                    row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore"))]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods,"special":special}
        resources={}
        for path in (RECIPE,ADV):
            n,h=PINS[path]
            raw=mod.read(path)
            require(len(raw)==n and digest(raw)==h,"resource drift "+path)
            resources[path]=decode(raw)
        recipe=resources[RECIPE]
        adv=resources[ADV]
        require(recipe.get("type")=="minecraft:crafting_shaped","recipe type drift")
        require(isinstance(recipe.get("pattern"),list) and isinstance(recipe.get("key"),dict),"recipe shape")
        require(isinstance(adv.get("criteria"),dict),"advancement shape")
        projected={"recipe":{k:recipe[k] for k in ("type","pattern","key","result")},
                   "advancement":{k:adv[k] for k in ("parent","criteria","requirements","rewards") if k in adv}}
    return {"schema_version":2,"scope":"REMOTE_DETONATOR_SOURCE_STATE_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"publisher_resource_projection":projected,"limits":LIMITS}

def self_test():
    require(selected(MC+"world/level/Explosion","getIndirectSourceEntityInternal"),"source filter")
    require(selected(AC,"setTag"),"publisher adapter filter")
    require(not selected(AC,"unrelated"),"adapter scope")
    require(not selected("foreign/Explosion","getIndirectSourceEntityInternal"),"namespace scope")
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
        require(len(data)<=1_800_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:
            f.write(data)
        print("REPORT_SHA256",digest(data),"BYTES",len(data))
        print("RESOURCE_PROJECTION",json.dumps(result["publisher_resource_projection"],sort_keys=True))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"))
            if row.get("special"):
                print("REGISTRY_PROJECTION",json.dumps(row["special"],sort_keys=True))
            for m in row.get("methods",[]):
                print("METHOD",owner,m["name"],m["descriptor"],m.get("code_sha256"),m.get("instruction_count"))
                if m["executable"]:
                    print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")
