#!/usr/bin/env python3
"""Exact Alex's Caves Continued 1.0.10 Double Stab native read-only JVM audit.

Reuses historical SHA-exact Desolate Dagger anchors, validates complete compiled
consumer methods and direct CFG, and separates spawn requests from accepted
entities, attacks, damage and Mastery. It does not authorize runtime mutation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods
)
from alexscaves_1010_dreadbow_decision_probe import method_digest
from alexscaves_1010_bouncy_ball_causal_probe import (
    method_switch_tables, branch_edges
)

BASE = "com/github/alexmodguy/alexscaves/"
ITEM = BASE + "server/item/DesolateDaggerItem.class"
ENTITY = BASE + "server/entity/item/DesolateDaggerEntity.class"
COMPAT = BASE + "server/misc/ACCompat.class"
DAMAGE = BASE + "server/misc/ACDamageTypes.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
RES = "data/alexscaves/enchantment/double_stab.json"
TAG = "data/alexscaves/tags/item/enchantable/desolate_dagger.json"
OTHER = "data/alexscaves/enchantment/impending_stab.json"
CLASS_SHAS = {
    ITEM:"ca020279666b45f5d8ede7082ba20c026a870989a6d90166fd1587af921a95ef",
    ENTITY:"f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351",
    COMPAT:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    DAMAGE:"389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6",
    REG:"60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32",
}
RESOURCE_SHAS = {
    RES:"554b3d0fb8e157ef912716cba8180b43cae340f01ee64ca931465b1d2884ff71",
    TAG:"c350c3e59d1bbff4d9fd24fa54c96e5fa075682f862c9eba0081c4ef2b97b264",
    OTHER:"bb3918b0fdf897ad70897952d15094e04d8af905b3e2f2db0d2159b762f5ffbc",
}
STACK_VICTIM_ATTACKER = (
    "(Lnet/minecraft/world/item/ItemStack;"
    "Lnet/minecraft/world/entity/LivingEntity;"
    "Lnet/minecraft/world/entity/LivingEntity;)"
)
METHODS = {
    ITEM: {"hurtEnemy":STACK_VICTIM_ATTACKER+"Z",
           "acSpawnDaggers":STACK_VICTIM_ATTACKER+"V"},
    ENTITY: {"tick":"()V",
             "getTargetEntity":"()Lnet/minecraft/world/entity/Entity;",
             "getPlayer":"()Lnet/minecraft/world/entity/Entity;",
             "addAdditionalSaveData":"(Lnet/minecraft/nbt/CompoundTag;)V",
             "readAdditionalSaveData":"(Lnet/minecraft/nbt/CompoundTag;)V",
             "setItemStack":"(Lnet/minecraft/world/item/ItemStack;)V"},
    COMPAT: {
        "enchantLevel":"(Lnet/minecraft/world/item/ItemStack;"
                       "Lnet/minecraft/resources/ResourceKey;)I",
        "createEntity":"(Lnet/minecraft/world/entity/EntityType;"
                       "Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/Entity;",
        "hurt":"(Lnet/minecraft/world/entity/Entity;"
               "Lnet/minecraft/world/damagesource/DamageSource;F)Z",
    },
    DAMAGE: {
        "causeDesolateDaggerDamage":"(Lnet/minecraft/core/RegistryAccess;"
                                    "Lnet/minecraft/world/entity/Entity;)"
                                    "Lnet/minecraft/world/damagesource/DamageSource;"
    },
}
PIVOTS = {
    (ITEM,"hurtEnemy"):{
        4:("invokespecial","SwordItem.hurtEnemy"),7:("ifeq","19"),
        14:("invokevirtual","acSpawnDaggers"),
    },
    (ITEM,"acSpawnDaggers"):{
        1:("getstatic","IMPENDING_STAB"),
        16:("getstatic","DOUBLE_STAB"),
        19:("invokestatic","ACCompat.enchantLevel"),
        22:("iadd",""),
        23:("if_icmpge","115"),
        41:("invokestatic","ACCompat.createEntity"),
        55:("invokevirtual","DesolateDaggerEntity.setTargetId"),
        61:("invokevirtual","DesolateDaggerEntity.copyPosition"),
        67:("invokevirtual","DesolateDaggerEntity.setItemStack"),
        74:("ifle","82"),
        90:("invokeinterface","RandomSource.nextInt"),
        96:("putfield","orbitFor"),
        105:("invokevirtual","Level.addFreshEntity"),
        108:("pop",""),
        109:("iinc","5, 1"),
        112:("goto","12"),
    },
    (ENTITY,"tick"):{
        13:("invokevirtual","getTargetEntity"),
        21:("invokevirtual","Level.isClientSide"),
        236:("invokevirtual","Level.isClientSide"),
        281:("invokevirtual","setStab"),
        294:("invokevirtual","getPlayer"),
        317:("getstatic","IMPENDING_STAB"),
        339:("invokestatic","causeDesolateDaggerDamage"),
        344:("invokestatic","ACCompat.hurt"),
        369:("getstatic","SATED_BLADE"),
        435:("invokevirtual","discard"),
    },
    (ENTITY,"setItemStack"):{
        8:("invokevirtual","SynchedEntityData.set"),
    },
    (COMPAT,"enchantLevel"):{
        1:("invokevirtual","ItemStack.getEnchantments"),
        42:("invokeinterface","Holder.is"),
        56:("ireturn",""),
        60:("iconst_0",""),
    },
}

def require(value, message):
    if not value:
        raise ValueError(message)

def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def unique_pairs(pairs):
    result = {}
    for key,val in pairs:
        require(key not in result,"duplicate JSON key: "+key)
        result[key] = val
    return result

def select(methods, name, descriptor):
    matches = [m for m in methods if m["descriptor"] == descriptor
               and re.search(r"\b"+re.escape(name)+r"\(",m["header"])]
    require(len(matches)==1,"missing/ambiguous compiled method "+name)
    return matches[0]

def compare_anchors(method, anchors):
    by = {row["offset"]:row for row in method["instructions"]}
    require(len(by)==len(method["instructions"]), "duplicate native JVM offset")
    require(0<len(anchors)<=len(by),"missing/overlarge historical evidence")
    seen = set()
    for old in anchors:
        pos = old["offset"]
        require(pos not in seen and pos in by,"missing/duplicate prior offset")
        seen.add(pos)
        now = by[pos]
        require((now["opcode"]," ".join(now["operand"].split()),now["symbol"])==
                (old["opcode"]," ".join(old["operand"].split()),old["symbol"]),
                "historical published bytecode drift @"+str(pos))
    return len(seen)

def check_pivots(method, pivots):
    by = {row["offset"]:row for row in method["instructions"]}
    for pos,(opcode,marker) in pivots.items():
        row = by.get(pos)
        require(row is not None and row["opcode"]==opcode and
                marker in (row["symbol"]+" "+row["operand"]),
                "native Double Stab pivot drift @"+str(pos))

def check_config(config, tag, impending):
    require(config.get("description")==
            {"translate":"enchantment.alexscaves.double_stab"},
            "Double Stab JSON identity drift")
    require(config.get("supported_items")=="#alexscaves:enchantable/desolate_dagger"
            and config.get("weight")==2 and config.get("max_level")==1
            and config.get("anvil_cost")==4 and config.get("slots")==["mainhand"]
            and "exclusive_set" not in config,
            "Double Stab publisher metadata drift")
    require(config.get("min_cost")=={"base":1,"per_level_above_first":12}
            and config.get("max_cost")=={"base":41,"per_level_above_first":10},
            "Double Stab enchanting costs drift")
    require(tag=={"values":["alexscaves:desolate_dagger"]},
            "Desolate Dagger tag drift")
    require(impending.get("exclusive_set")==["alexscaves:double_stab"],
            "Impending Stab asymmetric exclusion metadata drift")

def check_causal_counters(chosen):
    item = chosen[(ITEM,"acSpawnDaggers")]["instructions"]
    hurt = chosen[(ITEM,"hurtEnemy")]["instructions"]
    tick = chosen[(ENTITY,"tick")]["instructions"]
    find = lambda rows,needle: [r["offset"] for r in rows if needle in r["symbol"]]
    require(find(item,"ACEnchantmentRegistry.DOUBLE_STAB")==[16],
            "additional/altered Double Stab lookup")
    require(find(item,"ACEnchantmentRegistry.IMPENDING_STAB")==[1],
            "unexpected initial Impending Stab lookup")
    require(find(item,"Level.addFreshEntity:")==[105],
            "unexpected native spawn handoff count")
    require(find(item,"DesolateDaggerEntity.setPlayerId:")==[],
            "producer now assigns a player ID: re-audit owner")
    require(find(item,"Level.isClientSide:")==[],
            "producer now has a side guard: re-audit authority")
    require(find(hurt,"SwordItem.hurtEnemy:")==[4] and
            find(hurt,"acSpawnDaggers:")==[14],
            "primary melee hook no longer delegates once")
    require(find(tick,"ACCompat.hurt:")==[344],
            "unexpected native dagger damage request count")
    require(find(tick,"ACDamageTypes.causeDesolateDaggerDamage:")==[339],
            "unexpected native damage-source request count")
    require(find(tick,"ACEnchantmentRegistry.DOUBLE_STAB")==[],
            "Double Stab now affects downstream entity tick")

def audit(jar:Path, manifest:Path, javap_bin:str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "installed publisher 1.0.10 JAR sha/size mismatch")
    source_bytes = manifest.read_bytes()
    prior = json.loads(source_bytes,object_pairs_hook=unique_pairs)
    require((prior["artifact_sha1"],prior["artifact_sha256"],
             prior["artifact_size_bytes"])==(SHA1,SHA256,SIZE),
            "historical dagger manifest artifact identity drift")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP archive members")
        for p,d in {**CLASS_SHAS,**RESOURCE_SHAS}.items():
            require(sha(arc.read(p))==d,"native publisher member SHA drift "+p)
            documented = (prior["classes"][p]["sha256"] if p in CLASS_SHAS
                          else prior["resources"][p])
            require(documented==d,"historical manifest member drift "+p)
        config=json.loads(arc.read(RES),object_pairs_hook=unique_pairs)
        tag=json.loads(arc.read(TAG),object_pairs_hook=unique_pairs)
        impending=json.loads(arc.read(OTHER),object_pairs_hook=unique_pairs)
        check_config(config,tag,impending)
        owners=sorted(p for p in names if p.startswith(BASE)
                      and p.endswith(".class") and
                      b"DOUBLE_STAB" in arc.read(p))
        require(REG in owners and ITEM in owners and len(owners)<=14,
                "missing/unbounded compiled Double Stab token owners")
    compiled={}
    chosen={}
    for owner, names in METHODS.items():
        source=javap(javap_bin,jar,owner[:-6].replace("/","."))
        methods=parse_methods(source)
        historical=prior["classes"][owner]["methods"]
        individual={}
        for name,desc in names.items():
            method=select(methods,name,desc)
            previous=[m for m in historical if m["name"]==name and
                      m["descriptor"]==desc]
            require(len(previous)==1,"missing/ambiguous parent method "+name)
            old_count=compare_anchors(method,previous[0]["anchors"])
            check_pivots(method,PIVOTS.get((owner,name),{}))
            switches=method_switch_tables(method,source)
            edges=branch_edges(method,switches)
            chosen[(owner,name)]=method
            individual[name]={
                "descriptor":desc,
                "method_sha256":method_digest(method),
                "instructions":len(method["instructions"]),
                "direct_branches":len(edges),
                "switch_tables":switches,
                "historical_anchors":old_count,
            }
        compiled[owner]=individual
    check_causal_counters(chosen)
    return {
        "schema_version":1,
        "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "parent_manifest_sha256":sha(source_bytes),
        "class_sha256":CLASS_SHAS,
        "resource_sha256":RESOURCE_SHAS,
        "compiled_token_owners":owners,
        "metadata":config,
        "tag":tag,
        "parent_exclusive_set":impending["exclusive_set"],
        "native":compiled,
        "nominal_spawn_attempts":{"no_enchant":1,"level_1":2,
                                  "conditional_formula":"1+L re-read per iteration",
                                  "accepted_spawns":"NOT_VERIFIED"},
        "limits":{
            "single_native_melee_root":True,
            "new_spell_root":False,
            "independent_projectile_spell":False,
            "server_side_spawn_guard_in_item":"ABSENT_IN_EXAMINED_METHOD",
            "factory_null_guard_in_item":"ABSENT_IN_EXAMINED_METHOD",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "world_claim_and_pvp":"NOT_VERIFIED",
            "damage_acceptance":"NOT_TESTED",
            "mastery_receipt_and_dedupe":"NOT_VERIFIED",
            "provider_universe_closed":False,
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--manifest",required=True,type=Path)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--seal",type=Path)
    a=p.parse_args()
    result=audit(a.jar,a.manifest,a.javap)
    serialized=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode("utf8")
    if a.seal:
        sealed=json.loads(a.seal.read_text(encoding="utf8"),
                          object_pairs_hook=unique_pairs)
        expected={
            "schema_version":1,
            "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
            "artifact":result["artifact"],
            "parent_manifest_sha256":result["parent_manifest_sha256"],
            "full_report_sha256":sha(serialized),
            "class_sha256":result["class_sha256"],
            "resource_sha256":result["resource_sha256"],
            "compiled_token_owners":result["compiled_token_owners"],
            "native_method_sha256":{
                owner:{name:m["method_sha256"] for name,m in ms.items()}
                for owner,ms in result["native"].items()},
            "native_instruction_counts":{
                owner:{name:m["instructions"] for name,m in ms.items()}
                for owner,ms in result["native"].items()},
            "native_direct_branch_counts":{
                owner:{name:m["direct_branches"] for name,m in ms.items()}
                for owner,ms in result["native"].items()},
            "native_historical_anchor_counts":{
                owner:{name:m["historical_anchors"] for name,m in ms.items()}
                for owner,ms in result["native"].items()},
            "nominal_spawn_attempts":result["nominal_spawn_attempts"],
            "limits":result["limits"],
        }
        require(expected==sealed,"individual Double Stab full-report seal drift")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(serialized)
    print("DOUBLE_STAB_1010_STATIC")
    print("compiled_token_owners="+json.dumps(result["compiled_token_owners"]))
    print("native_counts="+json.dumps({
        owner:{name:{k:m[k] for k in ("method_sha256","instructions",
                       "direct_branches","historical_anchors")}
               for name,m in ms.items()}
        for owner,ms in result["native"].items()},sort_keys=True))
    print("parent_manifest_sha256="+result["parent_manifest_sha256"])
    print("report_sha256="+sha(serialized))
    print("NO_MUTATION NOT_TESTED")

if __name__=="__main__":
    main()
