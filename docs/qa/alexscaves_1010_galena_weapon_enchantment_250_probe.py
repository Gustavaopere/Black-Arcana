#!/usr/bin/env python3
"""Read-only discovery of weapon identity and enchantment/attribute dispatch.
Exact distributed 21.1.250 and publisher 1.0.10; no game execution.
Reuses the bounded projection; the previous combat and durability seals are unchanged.
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
SOURCES = MC+"world/damagesource/DamageSources"
SOURCE = MC+"world/damagesource/DamageSource"
LIVING = MC+"world/entity/LivingEntity"
ENCH = MC+"world/item/enchantment/Enchantment"
HELPER = MC+"world/item/enchantment/EnchantmentHelper"
STACK = MC+"world/item/ItemStack"
ITEM = MC+"world/item/Item"
PLAYER = MC+"world/entity/player/Player"
MOB = MC+"world/entity/Mob"
TARGETED = MC+"world/item/enchantment/TargetedConditionalEffect"
TELETOR = "com/github/alexmodguy/alexscaves/server/entity/living/TeletorEntity"
COMPAT = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
ATTR_EFFECT = MC+"world/item/enchantment/effects/EnchantmentAttributeEffect"
INVENTORY = MC+"world/entity/player/Inventory"
ENTITY = MC+"world/entity/Entity"
SELECT = {
    SOURCES: {"<init>"},
    SOURCE: {"getWeaponItem"},
    LIVING: {"getWeaponItem","getMainHandItem","getOffhandItem","getItemInHand"},
    PLAYER: {"getWeaponItem","getMainHandItem","getItemBySlot"},
    MOB: {"getWeaponItem","getMainHandItem","getItemBySlot"},
    TELETOR: {"getWeaponItem","getMainHandItem","getItemBySlot"},
    MC+"world/entity/monster/Monster": {"getWeaponItem","getMainHandItem","getItemBySlot"},
    MC+"world/entity/PathfinderMob": {"getWeaponItem","getMainHandItem","getItemBySlot"},
    ENTITY: {"getWeaponItem"},
    INVENTORY: {"getSelected"},
    COMPAT: {"damageBonus"},
    ATTR_EFFECT: {"getModifier"},
    HELPER: {"modifyArmorEffectiveness","getDamageProtection","getEnchantmentLevel",
             "forEachModifier","runIterationOnItem","getItemEnchantmentLevel"},
    ENCH: {"modifyDamageFilteredValue","modifyArmorEffectiveness","modifyDamageProtection",
           "getDamageProtection","getAttributeModifiers","forEachModifier",
           "modifyArmorEffectivness","getSlotItems","matchingSlot"},
    STACK: {"getAttributeModifiers"},
    ITEM: {"getAttributeModifiers","getDefaultAttributeModifiers"},
    TARGETED: {"matches"},
    ENCH+"$1": {"<clinit>"},
    NF+"common/extensions/IItemStackExtension": {"getAttributeModifiers"},
    NF+"common/extensions/IItemExtension": {"getAttributeModifiers","getDefaultAttributeModifiers"},
    NF+"event/EventHooks": {"getItemAttributeModifiers"},
}
PREFIXES = {
    HELPER: ("lambda$modifyArmorEffectiveness$","lambda$getDamageProtection$",
             "lambda$getEnchantmentLevel$","lambda$forEachModifier$"),
    ENCH: ("lambda$modifyDamageFilteredValue$","lambda$modifyArmorEffectiveness$",
           "lambda$modifyDamageProtection$","lambda$getDamageProtection$"),
}
PINS = {
    "net/minecraft/world/damagesource/DamageSource": "6fed4e35eed364877b7cb4601045235d06f29c738b58a616b0bb98520b5f660f",
    "net/minecraft/world/damagesource/DamageSources": "457e0716c0fbeb86b8a228822ce720d7bc91c8808ef43c9f78677b4b28a59a18",
    "net/minecraft/world/entity/LivingEntity": "52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    "net/minecraft/world/entity/Mob": "d1595b3090248ca3999579b3c6e1ff2554a99e7814a61654c976ba01cde5994d",
    "net/minecraft/world/entity/player/Player": "277a886c7267e82baa4378282e3c892f16338c0a6a779f1cf361a0af7d7b09fd",
    "net/minecraft/world/item/Item": "d4234cf5acb218b2056a38845170ec8266e16dc39ae0ed5fe5328cac153af462",
    "net/minecraft/world/item/ItemStack": "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    "net/minecraft/world/item/enchantment/Enchantment": "39f7551189481b8cb331b88605792c75f239f6bd901e2e70c86ba61592a2ca7e",
    "net/minecraft/world/item/enchantment/Enchantment$1": "d3c99c16317393362d998278f727e088aebd5e80abc0b805d6a9e5efc7639b3b",
    "net/minecraft/world/item/enchantment/EnchantmentHelper": "b5da85025991eb5d1c0cd361c1d76a12756768506236e571c2e0a3b550a771bb",
    "net/minecraft/world/item/enchantment/TargetedConditionalEffect": "1c527fbde328b512d7954aa3890977c13d6e95ead45d0ba070018536f56a3616",
    "net/neoforged/neoforge/common/extensions/IItemExtension": "d65a413962ab6bf6cf8c33119b010dd16fcf482c114b8ae8abe5c59da951b088",
    "net/neoforged/neoforge/common/extensions/IItemStackExtension": "244993a9cd1a5e99507c88a0a8e1d65b6ef997d44bd73ab696a510ccf2d0397e",
    "net/neoforged/neoforge/event/EventHooks": "f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b",
    "com/github/alexmodguy/alexscaves/server/entity/living/TeletorEntity": "fa8c02bb83b9f3e267d194bd83d0690e5668e3d414499bb357575ab2f88127f1",
    "com/github/alexmodguy/alexscaves/server/misc/ACCompat": "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    "net/minecraft/world/entity/Entity": "4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
}
# Preserve all 30 executable Code hashes from run 45616664850, plus two reused bodies.
KNOWN = {
    ("net/minecraft/world/damagesource/DamageSource", "getWeaponItem", "()Lnet/minecraft/world/item/ItemStack;"):
        "97878b7b2ba5f8e03328bc346ec304d53321f96454ba21b3c6b1bb219a48f799",
    ("net/minecraft/world/damagesource/DamageSources", "<init>", "(Lnet/minecraft/core/RegistryAccess;)V"):
        "98f93dce5d826e11541bcef35af69ca739c64f9274a6f2ddbd80ea076c32ed33",
    ("net/minecraft/world/entity/LivingEntity", "getMainHandItem", "()Lnet/minecraft/world/item/ItemStack;"):
        "085c3c0d1edeff7d3455cc6e3dd8461a920a1025977139da83d0c310fc859c06",
    ("net/minecraft/world/entity/LivingEntity", "getOffhandItem", "()Lnet/minecraft/world/item/ItemStack;"):
        "664bf9c134ef163abdfc9573bb8f6e51f8e9297ef3ae2dfab5c10f02b535908a",
    ("net/minecraft/world/entity/LivingEntity", "getWeaponItem", "()Lnet/minecraft/world/item/ItemStack;"):
        "ac3e290cf5de03c5f9d54eb34089079d20156e06c7648ceb46d10a361ce1b777",
    ("net/minecraft/world/entity/LivingEntity", "getItemInHand", "(Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/item/ItemStack;"):
        "285bff4c932528659df1da4e336f88aa46b1c5ffbd82688f0f54b9804a878b1d",
    ("net/minecraft/world/entity/Mob", "getItemBySlot", "(Lnet/minecraft/world/entity/EquipmentSlot;)Lnet/minecraft/world/item/ItemStack;"):
        "7138521073688ed851903df2c8d2c8f6f6f1dadf1521f6e14f7f762358fc6807",
    ("net/minecraft/world/entity/player/Player", "getWeaponItem", "()Lnet/minecraft/world/item/ItemStack;"):
        "957f2e67071160ce8d87a2643649329c7af73f174d97ee27fe6ac09dbee7d31c",
    ("net/minecraft/world/entity/player/Player", "getItemBySlot", "(Lnet/minecraft/world/entity/EquipmentSlot;)Lnet/minecraft/world/item/ItemStack;"):
        "3b9adae54ac8b1d03f5c720c23d8ff4d11f9e34d13b7d1bf3394ccc69da9044e",
    ("net/minecraft/world/item/Item", "getDefaultAttributeModifiers", "()Lnet/minecraft/world/item/component/ItemAttributeModifiers;"):
        "34b32e4a706c41bb926536a332e752e87abd4687498d4dbdde650e91e8d16952",
    ("net/minecraft/world/item/enchantment/Enchantment", "modifyDamageProtection", "(Lnet/minecraft/server/level/ServerLevel;ILnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;Lorg/apache/commons/lang3/mutable/MutableFloat;)V"):
        "bea891385d6a4edc7b92009e07e2f0c443bb6158890b32b2f76d5458e37bcb29",
    ("net/minecraft/world/item/enchantment/Enchantment", "modifyDamageFilteredValue", "(Lnet/minecraft/core/component/DataComponentType;Lnet/minecraft/server/level/ServerLevel;ILnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;Lorg/apache/commons/lang3/mutable/MutableFloat;)V"):
        "be30249b17727badbc5e4c3549a61fbdc730bdf30d332239309d6372240c1610",
    ("net/minecraft/world/item/enchantment/Enchantment", "lambda$modifyDamageFilteredValue$7", "(Lorg/apache/commons/lang3/mutable/MutableFloat;ILnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/enchantment/effects/EnchantmentValueEffect;)V"):
        "74318e7df8c993cbd76df293256b0d4334ee85bf63343341d63a9437a8a115ff",
    ("net/minecraft/world/item/enchantment/Enchantment$1", "<clinit>", "()V"):
        "f16671fa89b0633776cc94788c287c67742a22b59e6af4dc83aa06f9c5f82ebd",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "runIterationOnItem", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentVisitor;)V"):
        "6b686fb46d4be3e95586bb5c6bb1e36bee35163ee19054efbff9a2ccc86cc30e",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "runIterationOnItem", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentInSlotVisitor;)V"):
        "c12d8068d1380d966e36b145f1b6d61e2be0a40cd2d708da41091736e419ad0e",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "getDamageProtection", "(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/damagesource/DamageSource;)F"):
        "bffe056d49a25f714023a06c1989c975fa7ca4f069f171030ad729c6eaf8df9e",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "modifyArmorEffectiveness", "(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)F"):
        "271b1f879a673c6e11be023cf122d4e385065653bee3a9a47058718db7849966",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "getEnchantmentLevel", "(Lnet/minecraft/core/Holder;Lnet/minecraft/world/entity/LivingEntity;)I"):
        "a20a8cdc0396aefd2c2efca551413ad7f16410f2672de66acdde7659507bd02c",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "forEachModifier", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlotGroup;Ljava/util/function/BiConsumer;)V"):
        "6bc12daf77faec3fcac897e781947572de220e3e2ee143ef0068acc7e7a28233",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "forEachModifier", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/util/function/BiConsumer;)V"):
        "9bc95f26c74c3cca9296fb14d69c4c240d9ae38bdfecff770776925b7ff33f38",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$forEachModifier$30", "(Lnet/minecraft/world/entity/EquipmentSlot;Ljava/util/function/BiConsumer;Lnet/minecraft/core/Holder;I)V"):
        "218f947ace84d52eaee9b796f4ebea89bbde6e60114783adc6e2705d59eee537",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$forEachModifier$29", "(Lnet/minecraft/core/Holder;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/util/function/BiConsumer;ILnet/minecraft/world/item/enchantment/effects/EnchantmentAttributeEffect;)V"):
        "14de52983aafa95813662eb3ed914cceb6f2de36263e60ba3e901021e4b5abf8",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$forEachModifier$28", "(Lnet/minecraft/world/entity/EquipmentSlotGroup;Ljava/util/function/BiConsumer;Lnet/minecraft/core/Holder;I)V"):
        "7d270bc423529671279b79210eee5703aed04f78267fc65c449a431b32f919ef",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$forEachModifier$27", "(Lnet/minecraft/core/Holder;Lnet/minecraft/world/entity/EquipmentSlotGroup;Ljava/util/function/BiConsumer;ILnet/minecraft/world/item/enchantment/effects/EnchantmentAttributeEffect;)V"):
        "4726d6f73a2ab621018cefdfa85f4776e95631ff259b5106c233eb73ac2b2825",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$modifyArmorEffectiveness$8", "(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;Lorg/apache/commons/lang3/mutable/MutableFloat;Lnet/minecraft/core/Holder;I)V"):
        "ce194a9698f114197d056f066e0f75c99a5ae26676bc04a67db9ab7a3b276cd2",
    ("net/minecraft/world/item/enchantment/EnchantmentHelper", "lambda$getDamageProtection$5", "(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/damagesource/DamageSource;Lorg/apache/commons/lang3/mutable/MutableFloat;Lnet/minecraft/core/Holder;ILnet/minecraft/world/item/enchantment/EnchantedItemInUse;)V"):
        "1845dc7e12360ff9bda52e36c7e136bdf79ef7efb588dd29b3b0c76c004bc51b",
    ("net/minecraft/world/item/enchantment/TargetedConditionalEffect", "matches", "(Lnet/minecraft/world/level/storage/loot/LootContext;)Z"):
        "e4bae561adb3503fd3850587f7a2cde4ef91985e55416a80257cef5160dae9e9",
    ("net/neoforged/neoforge/common/extensions/IItemExtension", "getDefaultAttributeModifiers", "(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;"):
        "2e404c30eab94b85fe4ffe670622c9751ed55e85d9ae3db0439607f5648c3687",
    ("net/neoforged/neoforge/common/extensions/IItemStackExtension", "getAttributeModifiers", "()Lnet/minecraft/world/item/component/ItemAttributeModifiers;"):
        "55b3ceef255914d42b949bd8c80568899f5b103f0fec64c8c804a6b19ffd443e",
    (COMPAT,"damageBonus","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)F"):
        "826663655003c485d93518882019173c5e4d307908d46ba7ff12743c9e506b5e",
    (ENCH,"matchingSlot","(Lnet/minecraft/world/entity/EquipmentSlot;)Z"):
        "6a01f51b51ec17f73171d0dbb46a224fb3bdc2bb34fc0433f62e6eb2fe947481",
}
# Only executable methods with exact prior typed owners are required.
# Candidate overrides, synthetic names and other downstream methods are recorded
# when present; their absence is not a claim about runtime dispatch.
REQUIRED = {
    SOURCE: {"getWeaponItem"},
    HELPER: {"modifyArmorEffectiveness","getDamageProtection","getEnchantmentLevel","forEachModifier","runIterationOnItem","getItemEnchantmentLevel"},
    ENCH: {"modifyDamageFilteredValue","modifyArmorEffectivness","getSlotItems","matchingSlot"},
    COMPAT: {"damageBonus"},
    ATTR_EFFECT: {"getModifier"},
    TARGETED: {"matches"},
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
          "effective_enchantment_set":"NOT_VERIFIED","weapon_identity_runtime":"NOT_VERIFIED",
          "active_datapacks":"NOT_OBSERVED"}

def selected(owner, declaration):
    name=declaration["name"]
    return name in SELECT.get(owner, set()) or name.startswith(PREFIXES.get(owner, ()))

ATTRIBUTE_SIGNATURE = ("getAttributeModifiers", "()Lnet/minecraft/world/item/component/ItemAttributeModifiers;")

def reachable(roots, load):
    """Enumerate bounded declared hierarchy, recording paths, not runtime dispatch."""
    pending=[(root,[root]) for root in roots]
    visited={}
    while pending:
        owner,path=pending.pop(0)
        if owner in visited:
            continue
        require(len(visited)<64,"hierarchy budget")
        visited[owner]=path
        node=load(owner)
        if node is not None:
            pending.extend((parent,path+[parent]) for parent in
                           ([node.parent] if node.parent else [])+node.interfaces)
    return visited

def resolve_stack_attribute(archives, rosters, order, result):
    def load(owner):
        sources=[name for name in order if owner+".class" in rosters[name]]
        if not sources:
            return None
        reader=ClassReader(archives[sources[0]].read(owner+".class"))
        require(reader.name==owner,"hierarchy identity")
        return reader
    paths=reachable([STACK],load)
    candidates=[]
    for owner,path in paths.items():
        reader=load(owner)
        if reader is None:
            continue
        for d in reader.methods:
            if (d["name"],d["descriptor"])!=ATTRIBUTE_SIGNATURE:
                continue
            # An exact executable, non-static body must also have been projected.
            if "code_sha256" in d and not d["access"] & 0x0008:
                rows=[m for m in result.get(owner,{}).get("methods",[])
                      if (m["name"],m["descriptor"])==ATTRIBUTE_SIGNATURE
                      and m.get("executable") and m.get("code_sha256")==d["code_sha256"]]
                require(len(rows)==1,"reachable attribute body not projected "+owner)
                candidates.append({"owner":owner,"path":path,"code_sha256":d["code_sha256"]})
    require(bool(candidates),"no reachable executable attribute descriptor")
    return {"reference_owner":STACK,"name":ATTRIBUTE_SIGNATURE[0],
            "descriptor":ATTRIBUTE_SIGNATURE[1],"reachable_executable_declarations":candidates,
            "scope":"DECLARED_HIERARCHY_ONLY_NOT_RUNTIME_DISPATCH"}

def resolve_weapon_declarations(archives,rosters,order,result):
    def load(owner):
        sources=[name for name in order if owner+".class" in rosters[name]]
        if not sources:
            return None
        rd=ClassReader(archives[sources[0]].read(owner+".class"))
        require(rd.name==owner,"weapon hierarchy identity")
        return rd
    out={}
    signature=("getWeaponItem","()Lnet/minecraft/world/item/ItemStack;")
    for root in (PLAYER,TELETOR):
        paths=reachable([root],load)
        observed=[]
        for owner,path in paths.items():
            rd=load(owner)
            if rd is None:
                continue
            for d in rd.methods:
                if (d["name"],d["descriptor"])==signature and "code_sha256" in d and not d["access"] & 0x0008:
                    rows=[m for m in result.get(owner,{}).get("methods",[])
                          if (m["name"],m["descriptor"])==signature and m.get("executable")
                          and m.get("code_sha256")==d["code_sha256"]]
                    require(len(rows)==1,"reachable weapon body not projected "+owner)
                    observed.append({"owner":owner,"path":path,"code_sha256":d["code_sha256"]})
        require(bool(observed),"no weapon declaration "+root)
        out[root]={"hierarchy":paths,"reachable_executable_declarations":observed}
    return out

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
        attribute_resolution=resolve_stack_attribute(archives,rosters,order,result)
        weapon_resolution=resolve_weapon_declarations(archives,rosters,order,result)
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"attribute_resolution":attribute_resolution,"weapon_resolution":weapon_resolution,"limits":LIMITS}

def self_test():
    require(selected(SOURCE,{"name":"getWeaponItem"}),"weapon source")
    require(selected(HELPER,{"name":"lambda$modifyArmorEffectiveness$99"}),"callback prefix")
    require(selected(ENCH,{"name":"modifyDamageFilteredValue"}),"damage filter")
    require(not selected(HELPER,{"name":"modifyDamage"}),"previous combat scope unchanged")
    require(not selected(HELPER,{"name":"processDurabilityChange"}),"durability scope reused")
    require(not selected("foreign/Enchantment",{"name":"modifyDamageFilteredValue"}),"namespace boundary")
    require(all(names<=SELECT[owner] for owner,names in REQUIRED.items()),"required scope consistency")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    require(STACK not in REQUIRED and selected(STACK,{"name":ATTRIBUTE_SIGNATURE[0]}),
            "do not conflate reference and declaration")
    class Node:
        def __init__(self,parent=None,interfaces=()):
            self.parent=parent
            self.interfaces=list(interfaces)
    graph={"Stack":Node("Object",("Extension",)), "Extension":Node(None,("Base",)),
           "Base":Node(None,("Extension",))}
    paths=reachable(["Stack"],graph.get)
    require(paths=={"Stack":["Stack"],"Object":["Stack","Object"],
                    "Extension":["Stack","Extension"],"Base":["Stack","Extension","Base"]},
            "inherited declaration traversal with cycle and missing external ancestor")
    require(len(KNOWN)==32,"prior executable proof coverage")
    require("modifyArmorEffectivness" in REQUIRED[ENCH],"exact observed native spelling")
    print("PASS: twelve scope, hierarchy and policy checks")

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
        print("ATTRIBUTE_RESOLUTION",json.dumps(report["attribute_resolution"],sort_keys=True))
        print("WEAPON_RESOLUTION",json.dumps(report["weapon_resolution"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
