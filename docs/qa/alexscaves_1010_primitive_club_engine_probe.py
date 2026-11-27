#!/usr/bin/env python3
"""Read-only Primitive Club effect settlement and inherited engine boundary discovery.
Publisher and distributed NeoForge 21.1.250 references, not transformed runtime.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection, identified, verify_universal, ARTIFACTS
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P = "com/github/alexmodguy/alexscaves/server/"
M = "net/minecraft/"
I = P+"item/PrimitiveClubItem"
C = P+"misc/ACCompat"
E = P+"potion/StunnedEffect"
R = P+"item/ACItemRegistry"
L = M+"world/entity/LivingEntity"
ALL = {I,E}
SELECT = {
    R: {"lambda$static$40"},
    C: {"enchantLevel","itemAttributes","hurtAndBreak","hurt"},
    P+"event/CommonEvents": {"livingDie","acLivingAttack","livingAttack"},
    P+"message/UpdateEffectVisualityEntityMessage": {"handle"},
    L: {"addEffect","canBeAffected","onEffectAdded","onEffectUpdated","onEffectRemoved","tickEffects","removeEffect","removeEffectNoUpdate","hurt","swing","getAttributeValue"},
    M+"world/effect/MobEffectInstance": {"<init>","update","tick","tickDownDuration","getDuration","getAmplifier"},
    M+"world/effect/MobEffect": {"addAttributeModifiers","removeAttributeModifiers","applyEffectTick","shouldApplyEffectTickThisTick","onEffectAdded"},
    M+"world/entity/Entity": {"canBeHitByProjectile","isPickable","isAlliedTo","distanceTo","isAlive"},
    M+"world/entity/player/Player": {"attack","getAttackStrengthScale","getCurrentItemAttackStrengthDelay","resetAttackStrengthTicker"},
    M+"world/item/ItemStack": {"hurtEnemy","hurtAndBreak","isDamageableItem","forEachModifier","getEnchantments","isValidRepairItem"},
    M+"world/item/component/ItemAttributeModifiers": {"forEach"},
    M+"world/damagesource/DamageSources": {"mobAttack"},
    M+"world/level/Level": {"getEntities"},
    M+"world/phys/AABB": {"ofSize","intersects"},
    M+"world/item/enchantment/EnchantmentHelper": {"forEachModifier","processDurabilityChange"},
    "net/neoforged/neoforge/common/CommonHooks": {"onPlayerAttackTarget","onMobEffectApplicable","onMobEffectAdded","onMobEffectRemove","onMobEffectExpired","onLivingDeath"},
    M+"world/entity/Mob": {"dropCustomDeathLoot","getEquipmentDropChance","setDropChance"},
}
REQUIRED = {
    I: {"<init>","acHurtEnemy","hurtEnemy","onLeftClickEntity","onEntitySwing","acInventoryTick","getStatsForEnchantmentLevel","acModifiers","mineBlock","isValidRepairItem"},
    E: {"tick","shouldTick"},
    R: {"lambda$static$40"},
    C: {"enchantLevel","itemAttributes","hurtAndBreak","hurt"},
    L: {"addEffect","canBeAffected","tickEffects","hurt"},
    M+"world/effect/MobEffectInstance": {"update","tick"},
    M+"world/entity/player/Player": {"attack","getAttackStrengthScale","getCurrentItemAttackStrengthDelay"},
    M+"world/entity/Entity": {"canBeHitByProjectile","isAlliedTo","distanceTo"},
    M+"world/phys/AABB": {"ofSize"},
    M+"world/item/ItemStack": {"hurtAndBreak","isDamageableItem"},
    M+"world/damagesource/DamageSources": {"mobAttack"},
    "net/neoforged/neoforge/common/CommonHooks": {"onPlayerAttackTarget"},
}
PINS = {
    I:"92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac",
    E:"1ca7aea9ca512e10f2c06da58093e6197c57645ce2d32fc03cce0869d21a0a9e",
    C:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    P+"event/CommonEvents":"d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43",
    P+"message/UpdateEffectVisualityEntityMessage":"4fb1a0200619ce7597470ebd500d6da12bd190a32910bde7ebbc6ac9e9298280",
}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "runtime_loaded_bytes":"NOT_OBSERVED","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"actual_effect_acceptance":"NOT_VERIFIED"}

def verify_club_registry(reg):
    # Direct NEW factories are not nested invokedynamic factories.
    descriptor = "()Lnet/minecraft/world/item/Item;"
    candidates = [x for x in reg["constructor_factories"]
                  if x["method"] == "lambda$static$40" and x["descriptor"] == descriptor
                  and any(y["owner"] == I for y in x["constructor_owners"])]
    require(len(candidates) == 1,"club direct constructor factory absent or ambiguous")
    links = [x for x in reg["bootstrap_links"] if x["bootstrap_index"] == 52
             and any(y["owner"] == R and y["name"] == "lambda$static$40"
                     and y["descriptor"] == descriptor and y["kind"] == 6
                     for y in x["handles"])
             and any(y["symbol"] == "String primitive_club" for y in x["symbolic_context"])
             and any(y["symbol"].startswith("Field PRIMITIVE_CLUB:") for y in x["symbolic_context"])]
    require(len(links) == 1,"club registry bootstrap identity absent or ambiguous")

def inspect(args):
    select = {k:set(v) for k,v in SELECT.items()}
    required = {k:set(v) for k,v in REQUIRED.items()}
    if args.schema == 2:
        # Exact delegated callsites discovered in schema 1; retain schema 1 seal.
        extra = {
            "net/neoforged/neoforge/common/CommonHooks": {"canMobEffectBeApplied"},
            "net/neoforged/neoforge/event/EventHooks": {"onEffectRemoved"},
            M+"world/effect/MobEffectInstance": {"onEffectStarted","onEffectAdded","isShorterDurationThan","hasRemainingDuration","isInfiniteDuration"},
            M+"world/effect/MobEffect$AttributeTemplate": {"create"},
            L: {"die","dropCustomDeathLoot"},
        }
        for owner,names in extra.items():
            select.setdefault(owner,set()).update(names)
            required.setdefault(owner,set()).update(names)
    verify_artifact(args.publisher)
    verify_universal(args.universal, "universal")
    require(not args.output.exists(), "write-once report required")
    artifact = {
        "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "neoforge_version":"21.1.250",
        "installer":identified(args.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(args.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(args.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"],
    }
    with ZipFile(args.server) as ov, ZipFile(args.universal) as uni, ZipFile(args.srg) as mc, ZipFile(args.publisher) as mod:
        archives = [("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _, z in archives:
            require(len(z.namelist()) == len(set(z.namelist())), "duplicate archive path")
        roster = [(name,z,set(z.namelist())) for name,z in archives]
        cp = ":".join(map(str,(args.server,args.universal,args.srg,args.publisher)))
        require(sum(p.endswith(".class") for p in mod.namelist())==1555,"publisher class roster")
        reg=registry(mod,args.publisher,args.javap,R,{I})
        verify_club_registry(reg)
        recipe_path="data/alexscaves/recipe/primitive_club.json"
        recipe=mod.read(recipe_path)
        require(digest(recipe)=="b93f005c5632388ca6f34e3a114a8e0a4cf1c2ae99ae9bb0ed2edc2c73dddcc0","recipe pin")
        resources={recipe_path:{"sha256":digest(recipe),"bytes":len(recipe),"data":json.loads(recipe)}}
        classes = {}
        for owner in sorted(ALL | set(select)):
            found = [(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in required,"required owner absent "+owner)
                classes[owner] = {"present":False}
                continue
            source,z = found[0]
            raw=z.read(owner+".class")
            sha=digest(raw)
            rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity "+owner)
            require(owner not in PINS or sha==PINS[owner],"prior class pin "+owner)
            decls=[d for d in rd.methods if owner in ALL or d["name"] in select.get(owner,set())]
            require(required.get(owner,set()) <= {d["name"] for d in decls},"required declaration absent "+owner)
            require(len(decls)<=120,"method budget "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and parsed[key],"body absent "+owner+str(key))
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner in ALL:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d} ==
                        {k for k,v in parsed.items() if v},"complete executable roster mismatch "+owner)
            if owner == R:
                require(any(d["name"]=="lambda$static$40" and d.get("code_sha256")=="f88517fec12d13fcfc61890e09e7310f0a000ab35eea36adc82ddd7af3bab032" for d in decls),"club factory Code hash drift")
            classes[owner]={"present":True,"source":source,"available_sources":[k for k,_ in found],
                            "class_sha256":sha,"parent":rd.parent,"interfaces":rd.interfaces,
                            "fields":rd.fields,"declarations":rd.methods,"methods":methods}
    report={"schema_version":args.schema,"scope":"PRIMITIVE_CLUB_ENGINE_DISCOVERY_ONLY" if args.schema==1 else "PRIMITIVE_CLUB_EFFECT_DELEGATION_DISCOVERY_ONLY",
            "artifact":artifact,"classes":classes,"item_registry":reg,"resources":resources,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=10_000_000,"report byte budget")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("xb") as f:
        f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,row in classes.items():
        print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
        for method in row.get("methods",[]):
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("REGISTRY",json.dumps(reg,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS) <= ALL | set(SELECT),"pins out of scope")
    require(REQUIRED[I] >= {"acHurtEnemy","onLeftClickEntity","onEntitySwing"},"producer coverage")
    require(REQUIRED[L] >= {"addEffect","canBeAffected","tickEffects"},"effect coverage")
    require(LIMITS["static_contract"]=="NOT_CERTIFIED" and LIMITS["mutation"]=="NO_MUTATION","policy")
    fixture = {"constructor_factories":[{"method":"lambda$static$40","descriptor":"()Lnet/minecraft/world/item/Item;",
                "constructor_owners":[{"offset":0,"owner":I}]}],
               "nested_factories":[],
               "bootstrap_links":[{"bootstrap_index":52,"handles":[{"kind":6,"owner":R,"name":"lambda$static$40",
                  "descriptor":"()Lnet/minecraft/world/item/Item;"}],"symbolic_context":[
                  {"symbol":"String primitive_club"},{"symbol":"Field PRIMITIVE_CLUB:Ljava/util/function/Supplier;"}]}]}
    verify_club_registry(fixture)
    from copy import deepcopy
    from alexscaves_1010_armor_material_audit import AuditError
    for field in ("constructor_factories","bootstrap_links"):
        bad=deepcopy(fixture)
        bad[field]=[]
        try:
            verify_club_registry(bad)
        except AuditError:
            pass
        else:
            raise AssertionError("missing "+field+" accepted")
    print("PASS: discovery scope, direct factory and negative guards")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--schema",type=int,choices=(1,2),default=1)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"all inputs required")
        inspect(a)
