#!/usr/bin/env python3
"""Read-only SHA-exact Gamma Ray 1.0.10 native causal contract.

Composes the existing Energy Efficiency whole-method audit and radiation guard
proof. Reports static requests and direct JVM edges, never gameplay execution,
network authorization, an effective datapack, or a safe mutating hook.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_energy_efficiency_probe import (
    audit as energy_audit, CANONICAL_METHODS, PARENT_HASHES, CLASS_REG,
    CLASS_REG_SHA, method_select, unique_pairs,
)
from alexscaves_1010_raygun_local_flow_probe import CLASS, CLASS_SHA256, digest_method, local_access
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges, method_switch_tables
from alexscaves_1010_raygun_radiation_guard_probe import probe_method, inspect_default_tag

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
RES = "data/alexscaves/enchantment/gamma_ray.json"
X_RAY = "data/alexscaves/enchantment/x_ray.json"
TAG = "data/alexscaves/tags/item/enchantable/raygun.json"
RESISTANCE = "data/alexscaves/tags/entity_type/resists_radiation.json"
COMPAT = "com/github/alexmodguy/alexscaves/server/misc/ACCompat.class"
DAMAGE = "com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class"
IRRADIATED = "com/github/alexmodguy/alexscaves/server/potion/IrradiatedEffect.class"
SOURCE = "com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages.class"
CLASS_HASHES = {
    CLASS: CLASS_SHA256, CLASS_REG: CLASS_REG_SHA,
    COMPAT: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    DAMAGE: "389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6",
    IRRADIATED: "ee532620f143ff83773b08cf52f72b0b20b3fb6e85b18ed7b39dfd930465ba5c",
    SOURCE: "9f15d81ecf6efcd6a22b331af8babe5920dc48ee815f22ab033fb8e0c8a0fe39",
}
DECLARED_COUNTS = {CLASS: 26, COMPAT: 199, DAMAGE: 12, IRRADIATED: 4, SOURCE: 3}
RESOURCE_HASHES = {
    RES: "4873ef951ef2afff56e8734740e68c0e4bec4b2d69e893632a9f97dc317630fd",
    X_RAY: "612b1f7b126cea12085dea00736115b05fd4789bf9fc9ff6c4344a427135b0f8",
    TAG: "8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d",
    RESISTANCE: "1bb63c275f31f6744c071cda8ced3e1225401c5aa1dff2ea7fa3c7949e46a6c4",
}
EXACT_GAMMA = {
    "description": {"translate": "enchantment.alexscaves.gamma_ray"},
    "supported_items": "#alexscaves:enchantable/raygun", "weight": 2,
    "max_level": 1, "min_cost": {"base": 1, "per_level_above_first": 18},
    "max_cost": {"base": 41, "per_level_above_first": 10},
    "anvil_cost": 4, "slots": ["mainhand"],
}
EXACT_X_RAY = {
    "description": {"translate": "enchantment.alexscaves.x_ray"},
    "supported_items": "#alexscaves:enchantable/raygun", "weight": 10,
    "max_level": 1, "min_cost": {"base": 1, "per_level_above_first": 12},
    "max_cost": {"base": 41, "per_level_above_first": 10},
    "anvil_cost": 1, "slots": ["mainhand"],
    "exclusive_set": ["alexscaves:gamma_ray"],
}
EXACT_TAG = {"values": ["alexscaves:raygun"]}
TOKEN_OWNERS = sorted([
    CLASS, CLASS_REG,
    "com/github/alexmodguy/alexscaves/client/render/item/ACItemstackRenderer.class",
    "com/github/alexmodguy/alexscaves/client/render/item/RaygunRenderHelper.class",
])
ITEM_RENDERER = "com/github/alexmodguy/alexscaves/client/render/item/ACItemstackRenderer.class"
RAY_RENDERER = "com/github/alexmodguy/alexscaves/client/render/item/RaygunRenderHelper.class"
VISUAL_CLASS_HASHES = {
    ITEM_RENDERER: "18e350579f407c7c9509e230aa17b68b1113c166352e812482934ec3fdc1bd7e",
    RAY_RENDERER: "bade390453dfd0749302c3ea1a1b6a7840bc24dbd0cdb44897b1bc2495eaaadc",
}
VISUAL_METHODS = [
    (ITEM_RENDERER, "renderByItem", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemDisplayContext;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;II)V", "b409b1c334dae2bcf0ed11c0327dd36850adf755fd88c7b434f169bad8197f87", 1771),
    (RAY_RENDERER, "renderRaysFor", "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/phys/Vec3;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;FZI)V", "2862f26fbb27c44fdd180a77f64a8bf1165e98619d083063157f52ef99ae3eae", 209),
]
VISUAL_PIVOTS = {
    ITEM_RENDERER: {
        1967: ("aload_1", ""), 1968: ("getstatic", "GAMMA_RAY:"),
        1971: ("invokestatic", "ACCompat.enchantLevel:"), 1974: ("ifle", "1981"),
        1977: ("iconst_1", ""), 1978: ("goto", "1982"), 1981: ("iconst_0", ""),
        1982: ("istore", "14"), 1984: ("iload", "14"), 1986: ("ifeq", "1995"),
        1989: ("getstatic", "RAYGUN_BLUE_TEXTURE:"), 1992: ("goto", "1998"),
        1995: ("getstatic", "RAYGUN_TEXTURE:"), 1998: ("astore", "15"),
        2000: ("iload", "14"), 2002: ("ifeq", "2011"),
        2005: ("getstatic", "RAYGUN_BLUE_ACTIVE_TEXTURE:"), 2008: ("goto", "2014"),
        2011: ("getstatic", "RAYGUN_ACTIVE_TEXTURE:"), 2014: ("astore", "16"),
    },
    RAY_RENDERER: {
        62: ("aload", "7"), 64: ("getstatic", "GAMMA_RAY:"),
        67: ("invokestatic", "ACCompat.enchantLevel:"), 70: ("ifle", "77"),
        73: ("iconst_1", ""), 74: ("goto", "78"), 77: ("iconst_0", ""),
        78: ("istore", "11"), 178: ("iload", "11"), 180: ("invokestatic", "renderRay:"),
        221: ("iload", "11"), 223: ("invokestatic", "renderRay:"),
        292: ("aload", "7"), 294: ("getstatic", "GAMMA_RAY:"),
        297: ("invokestatic", "ACCompat.enchantLevel:"), 300: ("ifle", "307"),
        303: ("iconst_1", ""), 304: ("goto", "308"), 307: ("iconst_0", ""),
        308: ("istore", "11"), 408: ("iload", "11"), 410: ("invokestatic", "renderRay:"),
        433: ("iload", "11"), 435: ("invokestatic", "renderRay:"),
    },
}
PRIOR_SEALS = {
    "EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json": "a499370fe6bea484e7ac1d0d2afcf74a170495c913c151f73239253067f82a68",
    "EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json": "fa135a619a12d3a615d11a5a604ab9c796f7247f3bb4e48df1e4e5adee17728e",
    "EXACT-RADIATION-CONTRACT-1.0.10.json": "dbc2d323339cccc2c4a95dbf9667ebdb453617711b7bc7f1f11cb5615d924fd7",
}
SAFETY = {
    "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION", "provider_universe_closed": False,
    "network_authorization": "NOT_VERIFIED", "codec_and_packet_delivery": "NOT_VERIFIED",
    "effective_charge_settlement": "NOT_TESTED", "effective_world_datapack": "NOT_VERIFIED",
    "accepted_damage_and_effects": "NOT_TESTED", "claims_and_pvp": "NOT_VERIFIED",
    "mastery_credit_for_periodic_radiation": "NOT_VERIFIED",
    "exception_edges": "NOT_RECONSTRUCTED", "whole_raygun_card": "PARTIAL",
}

# Native predicates are pinned independently from the full parsed body digest.
# Operand fragments are meaningful JVM values/symbols, never inferred names.
TICK_PIVOTS = {
    3: ("invokevirtual", "getUseDuration:"), 9: ("istore", "5"),
    11: ("bipush", "15"), 13: ("istore", "6"),
    19: ("if_icmpge", "32"), 28: ("fdiv", ""), 33: ("fstore", "7"),
    35: ("ldc_w", "float 25.0f"), 38: ("fload", "7"),
    40: ("fmul", ""), 41: ("fstore", "8"),
    61: ("invokedynamic", "#0:test:"),
    69: ("invokestatic", "ProjectileUtil.getHitResultOnViewVector:"),
    137: ("astore", "14"), 140: ("invokestatic", "hasCharge:"),
    143: ("ifne", "210"), 169: ("invokevirtual", "stopUsingItem:"),
    209: ("return", ""), 214: ("ifeq", "322"),
    246: ("getstatic", "ENERGY_EFFICIENCY:"),
    249: ("invokestatic", "ACCompat.enchantLevel:"),
    319: ("invokestatic", "setCharge:"),
    331: ("aload_3", ""), 332: ("getstatic", "GAMMA_RAY:"),
    335: ("invokestatic", "ACCompat.enchantLevel:"),
    338: ("ifle", "345"), 341: ("iconst_1", ""),
    342: ("goto", "346"), 345: ("iconst_0", ""), 346: ("istore", "18"),
    357: ("ifeq", "402"), 364: ("iflt", "402"),
    367: ("iload", "18"), 369: ("ifeq", "386"),
    372: ("getstatic", "BLUE_RAYGUN_EXPLOSION:"),
    386: ("getstatic", "RAYGUN_EXPLOSION:"),
    402: ("iload", "18"), 404: ("ifeq", "421"),
    407: ("getstatic", "BLUE_HAZMAT_BREATHE:"), 421: ("getstatic", "HAZMAT_BREATHE:"),
    560: ("invokevirtual", "Level.addParticle:"),
    766: ("astore", "14"),
    875: ("invokevirtual", "isClientSide:"), 878: ("ifne", "1160"),
    881: ("iload", "5"), 883: ("iload", "6"),
    885: ("isub", ""), 886: ("iconst_3", ""),
    887: ("irem", ""), 888: ("ifne", "1160"),
    891: ("new", "AABB"), 895: ("aload", "14"),
    897: ("ldc2_w", "double -1.0d"), 900: ("ldc2_w", "double -1.0d"),
    903: ("ldc2_w", "double -1.0d"), 906: ("invokevirtual", "Vec3.add:"),
    909: ("aload", "14"), 911: ("dconst_1", ""),
    912: ("dconst_1", ""), 913: ("dconst_1", ""),
    914: ("invokevirtual", "Vec3.add:"), 917: ("invokespecial", "AABB."),
    922: ("iload", "18"), 924: ("ifeq", "931"),
    927: ("iconst_4", ""), 928: ("goto", "932"),
    931: ("iconst_0", ""), 932: ("istore", "23"),
    938: ("invokedynamic", "#0:test:"), 943: ("invokevirtual", "Level.getEntities:"),
    960: ("ifeq", "1160"), 978: ("invokevirtual", "Entity.is:"),
    981: ("ifne", "1157"), 987: ("invokevirtual", "isAlliedTo:"),
    990: ("ifne", "1157"), 996: ("invokevirtual", "isAlliedTo:"),
    999: ("ifne", "1157"), 1005: ("invokevirtual", "isPassengerOfSameVehicle:"),
    1008: ("ifne", "1157"), 1013: ("instanceof", "TremorzillaEntity"),
    1016: ("ifne", "1047"), 1025: ("aload_2", ""),
    1026: ("invokestatic", "causeRaygunDamage:"), 1029: ("iload", "18"),
    1031: ("ifeq", "1038"), 1034: ("fconst_2", ""),
    1035: ("goto", "1041"), 1038: ("ldc_w", "float 1.5f"),
    1041: ("invokestatic", "ACCompat.hurt:"), 1044: ("ifeq", "1051"),
    1047: ("iconst_1", ""), 1048: ("goto", "1052"),
    1051: ("iconst_0", ""), 1052: ("istore", "26"),
    1054: ("iload", "26"), 1056: ("ifeq", "1157"),
    1061: ("instanceof", "LivingEntity"), 1064: ("ifeq", "1157"),
    1082: ("getstatic", "RESISTS_RADIATION:"),
    1085: ("invokevirtual", "Holder$Reference.is:"), 1088: ("ifne", "1157"),
    1097: ("getstatic", "IRRADIATED:"), 1108: ("invokestatic", "ACCompat.effect:"),
    1111: ("sipush", "800"), 1114: ("iload", "23"),
    1116: ("invokespecial", "MobEffectInstance."),
    1119: ("invokevirtual", "LivingEntity.addEffect:"), 1122: ("ifeq", "1157"),
    1138: ("iload", "18"), 1140: ("ifeq", "1147"),
    1143: ("iconst_4", ""), 1144: ("goto", "1148"),
    1147: ("iconst_0", ""), 1148: ("sipush", "800"),
    1151: ("invokespecial", "UpdateEffectVisualityEntityMessage."),
    1154: ("invokestatic", "sendMSGToAll:"),
    1157: ("goto", "953"), 1160: ("return", ""),
}

# owner, name, descriptor, whole parsed body SHA256, instructions, direct branches
HELPERS = [
    (COMPAT, "enchantLevel", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I", "775387837bd0e7dbbd2fd04cd5de0375a6ccd2813de5db375fd152f8b63ad8dc", 24, 3),
    (COMPAT, "hurt", "(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z", "77997f2089224cd768dc079fb789bc5ffa96c8647bf5c0cabe932b8c3a3702b5", 5, 0),
    (DAMAGE, "causeRaygunDamage", "(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;", "160e3b07f7d14162ff90739c9005faac1ee7a2ffbe0c73b6626cd9f78645ba6a", 13, 0),
    (DAMAGE, "causeRadiationDamage", "(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;", "8f61976678e2fc06746efd8b4b9451ad9b5b0c9d6ee6ce69fe7495d52d82a2f9", 12, 0),
    (IRRADIATED, "tick", "(Lnet/minecraft/world/entity/LivingEntity;I)V", "68bd2733471bac19320e1bb31c7e5d3fb8656842f4d2e2541c319b76b3e00c37", 42, 4),
    (IRRADIATED, "shouldTick", "(II)Z", "4b6d3c038ae9b8007d3bdeef4eb15a67d82da8bce872da5c4cd29435526fe8d1", 24, 4),
    (SOURCE, "<init>", "(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V", "60a6077687ecc4dbfaa0312570ca6e622c84aa9110043af2399ad5f2264f6f85", 8, 0),
    (SOURCE, "<init>", "(Lnet/minecraft/core/Holder$Reference;I)V", "3e68eb959a5ae3f99249df4019c0e26d59090b97991c7c8211e18280e4d8b08d", 7, 0),
]
HELPER_PIVOTS = {
    (COMPAT, "enchantLevel"): {1: ("invokevirtual", "ItemStack.getEnchantments:"), 4: ("invokevirtual", "ItemEnchantments.entrySet:"), 19: ("ifeq", "60"), 42: ("invokeinterface", "Holder.is:"), 47: ("ifeq", "57"), 51: ("invokeinterface", "getIntValue:"), 56: ("ireturn", ""), 57: ("goto", "13"), 60: ("iconst_0", ""), 61: ("ireturn", "")},
    (COMPAT, "hurt"): {0: ("aload_0", ""), 1: ("aload_1", ""), 2: ("fload_2", ""), 3: ("invokevirtual", "Entity.hurt:"), 6: ("ireturn", "")},
    (DAMAGE, "causeRaygunDamage"): {19: ("getstatic", "RAYGUN:"), 27: ("aload_1", ""), 28: ("iconst_1", ""), 29: ("invokespecial", "(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V"), 32: ("areturn", "")},
    (DAMAGE, "causeRadiationDamage"): {19: ("getstatic", "RADIATION:"), 27: ("iconst_2", ""), 28: ("invokespecial", "(Lnet/minecraft/core/Holder$Reference;I)V"), 31: ("areturn", "")},
    (IRRADIATED, "tick"): {1: ("invokestatic", "HazmatArmorItem.getWornAmount:"), 8: ("ldc", "float 0.25f"), 35: ("invokevirtual", "causeFoodExhaustion:"), 39: ("instanceof", "RaycatEntity"), 42: ("ifne", "83"), 59: ("ldc", "float 0.1f"), 63: ("ifge", "83"), 74: ("invokestatic", "causeRadiationDamage:"), 79: ("invokevirtual", "LivingEntity.hurt:")},
    (IRRADIATED, "shouldTick"): {1: ("ifgt", "6"), 4: ("iconst_0", ""), 6: ("sipush", "200"), 10: ("idiv", ""), 14: ("if_icmple", "32"), 19: ("irem", ""), 22: ("idiv", ""), 23: ("if_icmpne", "30")},
}


def verify_bootstrap(javap_bin, jar):
    result = subprocess.run([str(javap_bin), "-classpath", str(jar), "-v", "-p", CLASS[:-6].replace("/", ".")], capture_output=True, text=True, timeout=45, check=False)
    require(result.returncode == 0 and 0 < len(result.stdout) < 1000000, "Raygun verbose bootstrap extraction failed")
    match = re.search(r"BootstrapMethods:\s*\n  0: ([\s\S]*?)(?=\n  1:)", result.stdout)
    require(match is not None, "missing unique Raygun bootstrap0")
    block = match.group(1)
    require("REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:" in block and
            "REF_invokeVirtual net/minecraft/world/entity/Entity.canBeHitByProjectile:()Z" in block and
            "(Ljava/lang/Object;)Z" in block and "(Lnet/minecraft/world/entity/Entity;)Z" in block,
            "Raygun bootstrap0 projectile predicate drift")
    return {"index": 0, "factory": "java/lang/invoke/LambdaMetafactory.metafactory", "implementation": "REF_invokeVirtual net/minecraft/world/entity/Entity.canBeHitByProjectile:()Z", "invokedynamic_offsets": [61, 938]}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def verify_resources(raw):
    require(set(raw) == set(RESOURCE_HASHES), "publisher resource roster drift")
    require({name: digest(value) for name, value in raw.items()} == RESOURCE_HASHES,
            "publisher resource fingerprint drift")
    parsed = {name: json.loads(value, object_pairs_hook=unique_pairs) for name, value in raw.items()}
    require(parsed[RES] == EXACT_GAMMA and parsed[X_RAY] == EXACT_X_RAY and parsed[TAG] == EXACT_TAG,
            "Gamma/X-Ray metadata or supported item tag drift")
    return parsed


def check_pivots(method, expected):
    rows = method["instructions"]
    offsets = [r["offset"] for r in rows]
    require(offsets == sorted(set(offsets)), "duplicate/unordered native offsets")
    by = {r["offset"]: r for r in rows}
    selected = []
    for offset, (opcode, token) in sorted(expected.items()):
        row = by.get(offset)
        require(row is not None and row["opcode"] == opcode and token in row["operand"] + " " + row["symbol"],
                "Gamma native causal pivot drift @" + str(offset))
        selected.append({key: row[key] for key in ("offset", "opcode", "operand", "symbol")})
    return selected


def verify_method(method, source, body_hash, count, branches):
    require(digest_method(method) == body_hash, "whole native method fingerprint drift")
    require(len(method["instructions"]) == count, "native instruction census drift")
    edges = branch_edges(method, method_switch_tables(method, source))
    require(len(edges) == branches, "native direct branch census drift")
    return edges


def gamma_slot(method):
    accesses = [(row["offset"], local_access(row)) for row in method["instructions"]]
    writes = [offset for offset, access in accesses if access and access[0] == 18 and access[1] != "READ"]
    reads = [offset for offset, access in accesses if access == (18, "READ")]
    require(writes == [346] and reads == [367, 402, 922, 1029, 1138], "Gamma boolean local18 use/definition drift")
    refs = [r["offset"] for r in method["instructions"] if "ACEnchantmentRegistry.GAMMA_RAY:" in r["symbol"]]
    require(refs == [332], "Gamma native lookup population drift")
    return {"slot": 18, "writes": writes, "reads": reads, "predicate": "ACCompat.enchantLevel(stack,GAMMA_RAY)>0"}


def check_visual_pivots(owner, method):
    require(owner in VISUAL_PIVOTS, "unexpected Gamma visual consumer")
    rows = check_pivots(method, VISUAL_PIVOTS[owner])
    refs = [r["offset"] for r in method["instructions"] if "ACEnchantmentRegistry.GAMMA_RAY:" in r["symbol"]]
    require(refs == ({ITEM_RENDERER: [1968], RAY_RENDERER: [64, 294]}[owner]), "Gamma visual lookup census drift")
    return rows


def visual_consumers(jar, javap_bin):
    methods, pivots = [], []
    for owner, name, descriptor, body_hash, count in VISUAL_METHODS:
        source = javap(javap_bin, jar, owner[:-6].replace("/", "."))
        method = method_select(parse_methods(source), name, descriptor)
        require(digest_method(method) == body_hash, "Gamma visual method identity drift")
        require(len(method["instructions"]) == count, "Gamma visual instruction census drift")
        methods.append({"owner": owner, "name": name, "descriptor": descriptor, "body_sha256": body_hash, "instructions": count})
        pivots.extend({"owner": owner, "name": name, **row} for row in check_visual_pivots(owner, method))
    return {
        "scope": "SELECTED_NATIVE_CLIENT_VISUAL_CONSUMERS_ONLY",
        "class_sha256": VISUAL_CLASS_HASHES, "method_census": methods, "pivots": pivots,
        "texture_selection": "renderByItem: enchantLevel>0 selects RAYGUN_BLUE_TEXTURE and RAYGUN_BLUE_ACTIVE_TEXTURE; otherwise RAYGUN_TEXTURE and RAYGUN_ACTIVE_TEXTURE",
        "ray_forwarding": "renderRaysFor: positive Gamma booleans at local11 writes78/308 are passed as final renderRay argument at178/221/408/433",
        "whole_method_sha256_role": "IDENTITY_AND_DRIFT_ONLY_NOT_FULL_RENDERING_CFG",
        "limits": {"complete_rendering_cfg": "NOT_RECONSTRUCTED", "actual_pixels_and_delivery": "NOT_TESTED", "downstream_renderRay_implementation": "NOT_VERIFIED", "mutating_hook": "NOT_VERIFIED", "mutation": "NO_MUTATION"},
    }


def audit(jar: Path, javap_bin: str):
    jar = Path(jar)
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE), "publisher 1.0.10 JAR fingerprint drift")
    # The immutable earlier seals remain independent evidence boundaries.
    for name, expected in PRIOR_SEALS.items():
        require(digest((PROVIDER / name).read_bytes()) == expected, "prior independent seal drift: " + name)
    energy = energy_audit(jar, javap_bin)
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        require(set(CLASS_HASHES) | set(VISUAL_CLASS_HASHES) | set(RESOURCE_HASHES) <= set(names), "missing native class or resource")
        require({name: digest(arc.read(name)) for name in CLASS_HASHES} == CLASS_HASHES, "native compiled class fingerprint drift")
        require({name: digest(arc.read(name)) for name in VISUAL_CLASS_HASHES} == VISUAL_CLASS_HASHES, "Gamma visual compiled class fingerprint drift")
        raw_resources = {name: arc.read(name) for name in RESOURCE_HASHES}
        resources = verify_resources(raw_resources)
        owners = sorted(name for name in names if name.startswith("com/github/alexmodguy/alexscaves/") and name.endswith(".class") and b"GAMMA_RAY" in arc.read(name))
        require(owners == TOKEN_OWNERS, "compiled GAMMA_RAY token owner census drift")
    sources = {owner: javap(javap_bin, jar, owner[:-6].replace("/", ".")) for owner in DECLARED_COUNTS}
    declared = {owner: parse_methods(source) for owner, source in sources.items()}
    require({owner: len(methods) for owner, methods in declared.items()} == DECLARED_COUNTS, "native declared method census drift")
    bootstrap = verify_bootstrap(javap_bin, jar)
    specs = [(CLASS, name, descriptor, PARENT_HASHES[name], energy["native_methods"][name]["instructions"], {"onUseTick": 57, "hasCharge": 2, "getCharge": 2, "setCharge": 0}[name]) for name, descriptor in CANONICAL_METHODS.items()] + HELPERS
    method_census, pivots, direct_edges = [], [], []
    selected = {}
    for owner, name, descriptor, body_hash, count, branches in specs:
        selector = "ACDamageTypes$DamageSourceRandomMessages" if name == "<init>" else name
        method = method_select(declared[owner], selector, descriptor)
        edges = verify_method(method, sources[owner], body_hash, count, branches)
        selected[(owner, name)] = method
        method_census.append({"owner": owner, "name": name, "descriptor": descriptor, "body_sha256": digest_method(method), "instructions": count, "direct_branches": len(edges)})
        expected = TICK_PIVOTS if (owner, name) == (CLASS, "onUseTick") else HELPER_PIVOTS.get((owner, name), {})
        if owner == SOURCE:
            expected = {0: ("aload_0", ""), 1: ("aload_1", ""), 3: ("invokespecial", "DamageSource.\"<init>\":(Lnet/minecraft/core/Holder;Lnet/minecraft/world/entity/Entity;)V")} if "Entity;" in descriptor else {0: ("aload_0", ""), 1: ("aload_1", ""), 2: ("invokespecial", "DamageSource.\"<init>\":(Lnet/minecraft/core/Holder;)V")}
        pivots.extend({"owner": owner, "name": name, **row} for row in check_pivots(method, expected))
        direct_edges.extend({"owner": owner, "name": name, **row} for row in edges)
    tick = selected[(CLASS, "onUseTick")]
    slot = gamma_slot(tick)
    guard = probe_method(tick)
    default_resistance = inspect_default_tag(raw_resources[RESISTANCE])
    return {
        "schema_version": 1, "version": "1.0.10", "enchantment": "alexscaves:gamma_ray",
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY", "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_sha256": CLASS_HASHES, "resource_sha256": RESOURCE_HASHES,
        "resource_json": resources[RES], "x_ray_resource_json": resources[X_RAY], "supported_item_tag": resources[TAG],
        "publisher_default_resistance_tag": default_resistance, "compiled_token_owners": owners,
        "census": {"declared_methods": {owner: len(methods) for owner, methods in declared.items()}, "method_census": method_census},
        "pivots": pivots, "direct_edges": direct_edges, "gamma_boolean_slot": slot, "projectile_predicate_bootstrap": bootstrap,
        "radiation_guard": guard, "prior_seal_sha256": PRIOR_SEALS,
        "visual_consumers": visual_consumers(jar, javap_bin),
        "composed_energy_report_sha256": digest(canonical(energy).encode("utf8")),
        "static_contract": {
            "range": "25.0F*warmup_progress; Gamma does not alter range",
            "server_damage_gate": "!level.isClientSide() && (elapsed-15)%3==0; no extra elapsed>=15 guard",
            "target_volume": "AABB(local14+(-1D,-1D,-1D),local14+(1D,1D,1D))",
            "target_filters": ["projectile hit predicate", "not shooter identity", "not allied in either direction", "not passenger of same vehicle"],
            "damage_request": {"gamma_false": 1.5, "gamma_true": 2.0, "source": "causeRaygunDamage(registryAccess,shooter)"},
            "status_gate": "(Tremorzilla || ACCompat.hurt returns true) && LivingEntity && !RESISTS_RADIATION",
            "effect_request": {"duration_ticks": 800, "gamma_false_amplifier": 0, "gamma_true_amplifier": 4},
            "visual_gate": "LivingEntity.addEffect returns true", "visual_variants": [0, 4],
            "particle_variants": ["RAYGUN_EXPLOSION/BLUE_RAYGUN_EXPLOSION", "HAZMAT_BREATHE/BLUE_HAZMAT_BREATHE"],
            "irradiated_reference": "effects/irradiated.md; amplifier0 has no periodic tick; amplifier4 nominal shouldTick divisor50; periodic radiation factory has no shooter argument; Mastery credit NOT_VERIFIED",
            "charge_reference": "EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json; client charge write and message authorization remain separate",
            "exclusion": "Gamma JSON has no exclusive_set; X-Ray JSON explicitly lists gamma_ray; publisher default only",
        },
        "safety": SAFETY,
    }


def verify_seal(actual, expected):
    require(expected.get("claim_scope") == "STATIC_TECHNICAL_CATALOG_ONLY" and expected.get("safety") == SAFETY, "unsafe Gamma seal scope or safety drift")
    require(actual == expected, "Gamma exact native causal seal drift")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--seal", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        expected = None
        if args.seal:
            expected = json.loads(args.seal.read_text(encoding="utf8"), object_pairs_hook=unique_pairs)
            require(expected.get("claim_scope") == "STATIC_TECHNICAL_CATALOG_ONLY" and expected.get("safety") == SAFETY, "unsafe Gamma seal scope or safety drift")
        report = audit(args.jar, args.javap)
        if expected is not None:
            verify_seal(report, expected)
        data = canonical(report)
        require(len(data.encode("utf8")) < 160000, "Gamma evidence report budget exceeded")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf8")
        print("PASS: SHA-exact Gamma Ray 1.0.10 static native causal contract")
        print("method_census=" + str(len(report["census"]["method_census"])))
        print("onUseTick=523 instructions;57 direct branches;local18 write346 reads367,402,922,1029,1138")
        print("report_sha256=" + digest(data.encode("utf8")))
        print("STATIC_TECHNICAL_CATALOG_ONLY NO_MUTATION NOT_VERIFIED NOT_TESTED")
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
