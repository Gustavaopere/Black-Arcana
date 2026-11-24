#!/usr/bin/env python3
"""Read-only exact distributed TNT and player-owned ticket settlement discovery.
No game execution, provider code copying, or mutating hook certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

MC = "net/minecraft/"
CHUNK = "net/neoforged/neoforge/common/world/chunk/"
PIN = {
    MC+"world/level/block/TntBlock": "fb116b17eb40038991e262edd4fcc43592f07db5838699039ef2c50ba4981a26",
    CHUNK+"ForcedChunkManager$TicketTracker": "ef9ea888d97efd896f3fd000032c1dc39ed940338d3b6ecef949d4207959a58c",
    CHUNK+"ForcedChunkManager": "5b585bb44efc3822ef4cfb5a09afa44c810e35c38f336a2d03a60f271dcc98f2",
}
UNIVERSAL_SHA = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
UNIVERSAL_SIZE = 3551268
ALL_BODIES = {MC+"world/level/block/TntBlock", MC+"world/entity/item/PrimedTnt",
              CHUNK+"ForcedChunkManager$TicketTracker", CHUNK+"ForcedChunkManager$TicketOwner",
              MC+"world/level/ForcedChunksSavedData"}
SELECTED = {
    CHUNK+"ForcedChunkManager": {"init","reinstatePersistentChunks","gatherTicketsById","writeModForcedChunks","readModForcedChunks","readEntityForcedChunks","readBlockForcedChunks","forceChunk","<clinit>"},
    MC+"world/level/Level": {"explode","setBlockAndUpdate","setBlock"},
    MC+"server/level/ServerLevel": {"explode","addFreshEntity","mayInteract"},
    MC+"world/level/Explosion": {"<init>","explode","finalizeExplosion","getIndirectSourceEntity","getDirectSourceEntity"},
    MC+"world/level/ExplosionDamageCalculator": {"getEntityDamageAmount","getKnockbackMultiplier","shouldDamageEntity","getBlockExplosionResistance","shouldBlockExplode"},
    MC+"world/level/EntityBasedExplosionDamageCalculator": {"getBlockExplosionResistance","shouldBlockExplode"},
}
REQUIRED = {
    MC+"world/level/block/TntBlock": {"onCaughtFire","explode"},
    MC+"world/entity/item/PrimedTnt": {"<init>","tick","explode"},
    CHUNK+"ForcedChunkManager$TicketTracker": {"add","remove","getTickets"},
    CHUNK+"ForcedChunkManager$TicketOwner": {"<init>"},
    MC+"world/level/ForcedChunksSavedData": {"getEntityForcedChunks","getBlockForcedChunks"},
    MC+"world/level/Explosion": {"explode","finalizeExplosion"},
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
    return owner in ALL_BODIES or name in SELECTED.get(owner,()) or (
        owner==CHUNK+"ForcedChunkManager" and name.startswith(("lambda$reinstatePersistentChunks$","lambda$gatherTicketsById$","lambda$init$","lambda$writeModForcedChunks$","lambda$readModForcedChunks$")))

def scan(server,srg,universal,javap):
    identity=verify_distribution(server,srg)
    data=universal.read_bytes()
    require(len(data)==UNIVERSAL_SIZE and hashlib.sha256(data).hexdigest()==UNIVERSAL_SHA,"universal pin mismatch")
    identity.update({"universal_sha256":UNIVERSAL_SHA,"universal_bytes":UNIVERSAL_SIZE})
    owners=sorted(ALL_BODIES|set(SELECTED))
    with ZipFile(server) as overlay, ZipFile(universal) as uni, ZipFile(srg) as vanilla:
        archives=[("NEOFORGE_OVERLAY",overlay),("NEOFORGE_UNIVERSAL",uni),("INSTALLED_MINECRAFT_SRG",vanilla)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        classpath=":".join(map(str,(server,universal,srg)))
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
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    return {"schema_version":1,"scope":"REMOTE_DETONATOR_TNT_AND_TICKET_SETTLEMENT_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    require(selected(MC+"world/entity/item/PrimedTnt","tick"),"entity census")
    require(selected(CHUNK+"ForcedChunkManager","lambda$reinstatePersistentChunks$6"),"callback filter")
    require(not selected(CHUNK+"ForcedChunkManager","unrelated"),"manager filter")
    require(not selected("foreign/TntBlock","explode"),"namespace filter")
    require(LIMITS["mutation"]=="NO_MUTATION","policy drift")
    print("PASS: four scope checks and policy check")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server",type=Path)
    p.add_argument("--srg",type=Path)
    p.add_argument("--universal",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all((a.server,a.srg,a.universal,a.output)) and not a.output.exists(),"write-once report and artifacts required")
        result=scan(a.server,a.srg,a.universal,a.javap)
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
                if m["executable"] and (owner in ALL_BODIES or owner==CHUNK+"ForcedChunkManager" or m["name"] in {"explode","finalizeExplosion"}):
                    print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")
