#!/usr/bin/env python3
"""Exact physical-ledger NeoForge 21.1.250 block-drop dispatch and settlement discovery.
No gameplay execution or world mutation. Finite causal boundaries, not proof of permission.
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
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_universal

MC = "net/minecraft/"
CHUNK = "net/neoforged/neoforge/common/world/chunk/"
AC = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
WEAPON = "com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
PIN = {
    MC+"world/level/Level": "74a062f0d480674152fa4665bd7b483fca52de8dd3b07178c1a6c40d3fae3fae",
    MC+"world/level/LevelAccessor": "283c9be08df726ba3a89efa219cc2ea6573aca27379435a08a3b71e90345b138",
    MC+"world/level/block/Block": "8e07f9765ce7d3f086c98f99a5ddc9eea15b36e466c2413328c6598f8ef64f3f",
    MC+"world/level/block/ShulkerBoxBlock": "f4b98ff98f221137f6c97b6bcba28285dca380fad71e23a0c2c3e7f5acc205f1",
    "net/neoforged/neoforge/common/CommonHooks": "86c8a56c77fff474bf4fe90f0354ad32698f018b5e19dc52a2725ee5ff96c73e",
}
UNIVERSAL_SHA = "1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956"
UNIVERSAL_SIZE = 3551255
ALL_BODIES = set()
SELECTED = {
    MC+"world/level/LevelWriter": {"destroyBlock","removeBlock"},
    MC+"world/level/LevelAccessor": {"destroyBlock"},
    MC+"world/level/Level": {"destroyBlock","setBlockAndUpdate","setBlock"},
    MC+"world/level/block/Block": {"beginCapturingDrops","stopCapturingDrops","dropResources","popResource","popResourceFromFace","playerDestroy","getDrops"},
    MC+"world/level/block/state/BlockBehaviour": {"getDrops","getLootTable","spawnAfterBreak"},
    MC+"world/level/block/state/BlockBehaviour$BlockStateBase": {"getDrops","spawnAfterBreak"},
    MC+"world/level/block/BaseEntityBlock": {"getDrops"},
    MC+"world/level/block/ShulkerBoxBlock": {"getDrops","onRemove","playerWillDestroy"},
    MC+"world/level/storage/loot/LootParams$Builder": {"<init>","withParameter","withOptionalParameter","getOptionalParameter","withDynamicDrop","create"},
    MC+"world/level/storage/loot/LootParams": {"addDynamicDrops","getParameter","getOptionalParameter","getLuck"},
    MC+"world/level/storage/loot/LootTable": {"getRandomItems","getRandomItemsRaw","createStackSplitter"},
    MC+"world/level/storage/loot/LootContext$Builder": {"<init>","create"},
    MC+"world/level/storage/loot/parameters/LootContextParamSets": {"<clinit>"},
    "net/neoforged/neoforge/common/CommonHooks": {"handleBlockDrops","fireBlockBreak","modifyLoot"},
    "net/neoforged/neoforge/event/level/BlockDropsEvent": {"<init>","getDrops","getDroppedExperience","setDroppedExperience","getBreaker","getTool","getBlockEntity","getLevel"},
    "net/neoforged/neoforge/event/level/BlockEvent$BreakEvent": {"<init>","getPlayer","getExpToDrop","setExpToDrop"},
    "net/neoforged/neoforge/common/extensions/IBlockExtension": {"getExpDrop","onDestroyedByPlayer","canHarvestBlock"},
    "net/neoforged/neoforge/common/extensions/IBlockStateExtension": {"getExpDrop","onDestroyedByPlayer","canHarvestBlock"},
}
REQUIRED = {
    MC+"world/level/Level": {"destroyBlock"},
    MC+"world/level/block/Block": {"beginCapturingDrops","stopCapturingDrops","dropResources","popResource","playerDestroy"},
    MC+"world/level/block/state/BlockBehaviour": {"getDrops"},
    MC+"world/level/block/state/BlockBehaviour$BlockStateBase": {"getDrops"},
    MC+"world/level/storage/loot/LootParams$Builder": {"create","withParameter","withOptionalParameter"},
    "net/neoforged/neoforge/common/CommonHooks": {"handleBlockDrops","fireBlockBreak"},
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
    if owner in ALL_BODIES or name in SELECTED.get(owner,()):return True
    prefix={
        MC+"world/level/block/Block":("lambda$dropResources$","lambda$popResource$","lambda$popResourceFromFace$"),
        MC+"world/level/block/ShulkerBoxBlock":("lambda$getDrops$",),
        MC+"world/level/storage/loot/LootTable":("lambda$getRandomItems$","lambda$createStackSplitter$"),
        "net/neoforged/neoforge/common/CommonHooks":("lambda$handleBlockDrops$",),
        MC+"world/level/storage/loot/parameters/LootContextParamSets":("lambda$static$",),
    }.get(owner,())
    return bool(prefix) and name.startswith(prefix)

def scan(installer,server,srg,universal,publisher,javap):
    identity={'neoforge_version':'21.1.250','minecraft_version':'1.21.1'}
    for label,path,expected,expected_size in (
        ('installer',installer,'0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60',6972109),
        ('server',server,'1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359',5675624),
        ('srg',srg,'26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71',14246609)):
        raw=path.read_bytes()
        require(digest(raw)==expected and len(raw)==expected_size,'physical-ledger distribution pin '+label)
        identity[label]={'sha256':expected,'bytes':expected_size}
    verify_universal(universal,'universal')
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
                print("PROJECT_METHOD",owner,*key,flush=True)
                row=analyze(reader,body,d)
                row["instruction_sha256"]=summarize(reader,key,body)["instruction_sha256"]
                row["executable"]=True
                row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym} for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
                row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op.startswith("ldc") and sym.startswith("String ")]
                row["bootstrap_links"]=bootstrap(reader,body)
                row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
                row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore")) or op=="iinc"]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    return {"schema_version":1,"scope":"GALENA_DROP_SETTLEMENT_250_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    require(selected(MC+"world/level/LevelWriter","destroyBlock"),"forwarding scope")
    require(selected(MC+"world/level/block/Block","beginCapturingDrops"),"capture scope")
    require(selected("net/neoforged/neoforge/common/CommonHooks","handleBlockDrops"),"settlement scope")
    require(selected(MC+"world/level/block/Block","lambda$dropResources$1"),"callback scope")
    require(not selected("foreign/Block","dropResources"),"namespace scope")
    require(LIMITS["mutation"]=="NO_MUTATION","policy drift")
    print("PASS: five scope checks and policy check")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--installer",type=Path)
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
        require(all((a.installer,a.server,a.srg,a.universal,a.publisher,a.output)) and not a.output.exists(),"write-once report and artifacts required")
        result=scan(a.installer,a.server,a.srg,a.universal,a.publisher,a.javap)
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
, 'lambda$popResource

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
, 'lambda$getDrops

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
, 'lambda$handleBlockDrops

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
, 'lambda$getRandomItems

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
, 'lambda$static

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
))) and owner != MC+'world/level/block/Block' or (owner==MC+'world/level/block/Block' and name.startswith(('lambda$dropResources

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
, 'lambda$popResource

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
)))

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
