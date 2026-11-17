#!/usr/bin/env python3
"""Read-only SHA-exact X-Ray 1.0.10 individual native causal contract.

Composes the frozen Gamma and Energy audits. Native targeting requests are
distinguished from Minecraft trace internals, accepted hits and world outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import alexscaves_1010_gamma_ray_causal_audit as gamma
from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_energy_efficiency_probe import CLASS_REG, CLASS_REG_SHA, PARENT_HASHES, CANONICAL_METHODS, method_select, unique_pairs
from alexscaves_1010_raygun_local_flow_probe import CLASS, CLASS_SHA256, digest_method, local_access
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges, method_switch_tables

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
RES = gamma.X_RAY
GAMMA_RES = gamma.RES
TAG = gamma.TAG
EXACT_X_RAY, EXACT_GAMMA, EXACT_TAG = gamma.EXACT_X_RAY, gamma.EXACT_GAMMA, gamma.EXACT_TAG
CLASS_HASHES = {CLASS: CLASS_SHA256, CLASS_REG: CLASS_REG_SHA}
RESOURCE_HASHES = {name: gamma.RESOURCE_HASHES[name] for name in (RES, GAMMA_RES, TAG)}
TOKEN_OWNERS = sorted(CLASS_HASHES)
GAMMA_REPORT_SHA256 = "cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c"
ENERGY_REPORT_SHA256 = "0bb9e77b51908adaf6b679f483c484d5b4da5169cd4cb440e0c7a31b9c6dcfb3"
PRIOR_SEALS = {
    "EXACT-GAMMA-RAY-CAUSAL-1.0.10.json": GAMMA_REPORT_SHA256,
    "EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json": "a499370fe6bea484e7ac1d0d2afcf74a170495c913c151f73239253067f82a68",
}
SOURCE_HELPERS = (
    "alexscaves_1010_xray_causal_audit.py",
    "alexscaves_1010_gamma_ray_causal_audit.py",
    "alexscaves_1010_energy_efficiency_probe.py",
    "alexscaves_1010_damage_consumer_probe.py",
    "alexscaves_1010_raygun_local_flow_probe.py",
    "alexscaves_1010_bouncy_ball_causal_probe.py",
    "alexscaves_1010_bouncy_ball_probe.py",
    "alexscaves_1010_gumball_state_probe.py",
    "alexscaves_1010_raygun_radiation_guard_probe.py",
)
SAFETY = {
    "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
    "provider_universe_closed": False, "whole_raygun_card": "PARTIAL",
    "network_authorization": "NOT_VERIFIED", "codec_and_packet_delivery": "NOT_VERIFIED",
    "effective_charge_settlement": "NOT_TESTED", "effective_world_datapack": "NOT_VERIFIED",
    "accepted_damage_and_effects": "NOT_TESTED", "claims_and_pvp": "NOT_VERIFIED",
    "wall_penetration": "NOT_VERIFIED", "projectile_util_internals": "NOT_VERIFIED",
    "global_nearest_entity": "NOT_VERIFIED", "actual_pixels_and_delivery": "NOT_TESTED",
    "mastery_credit_for_periodic_radiation": "NOT_VERIFIED", "exception_edges": "NOT_RECONSTRUCTED",
}

# The complete 523-instruction/57-direct-branch body is already verified by
# Gamma. These additional operand paths establish the individual X-Ray role.
TICK_PIVOTS = {
    35: ("ldc_w", "float 25.0f"), 38: ("fload", "7"), 40: ("fmul", ""), 41: ("fstore", "8"),
    43: ("aload_3", ""), 44: ("getstatic", "ACEnchantmentRegistry.X_RAY:"),
    47: ("invokestatic", "ACCompat.enchantLevel:"), 50: ("ifle", "57"),
    53: ("iconst_1", ""), 54: ("goto", "58"), 57: ("iconst_0", ""), 58: ("istore", "9"),
    60: ("aload_2", ""), 61: ("invokedynamic", "#0:test:"), 66: ("fload", "8"), 68: ("f2d", ""),
    69: ("invokestatic", "ProjectileUtil.getHitResultOnViewVector:"), 72: ("astore", "10"),
    74: ("aload_2", ""), 75: ("fload", "8"), 77: ("f2d", ""), 78: ("fconst_0", ""),
    79: ("iconst_0", ""), 80: ("invokevirtual", "LivingEntity.pick:"), 83: ("astore", "11"),
    85: ("aload_2", ""), 86: ("fconst_0", ""), 87: ("invokevirtual", "LivingEntity.getViewVector:"),
    90: ("fload", "8"), 92: ("f2d", ""), 93: ("invokevirtual", "Vec3.scale:"),
    96: ("aload_2", ""), 97: ("invokevirtual", "LivingEntity.getEyePosition:"),
    100: ("invokevirtual", "Vec3.add:"), 103: ("astore", "12"),
    105: ("iload", "9"), 107: ("ifeq", "115"), 110: ("aload", "12"),
    112: ("goto", "120"), 115: ("aload", "11"), 117: ("invokevirtual", "HitResult.getLocation:"),
    120: ("astore", "13"), 122: ("iload", "9"), 124: ("ifeq", "132"),
    127: ("aload", "12"), 129: ("goto", "137"), 132: ("aload", "11"),
    134: ("invokevirtual", "HitResult.getLocation:"), 137: ("astore", "14"),
    211: ("invokevirtual", "Level.isClientSide:"), 214: ("ifeq", "322"),
    218: ("aload", "13"), 223: ("aload", "13"), 228: ("aload", "13"),
    233: ("invokestatic", "setRayPosition:"),
    563: ("aconst_null", ""), 564: ("astore", "20"), 566: ("aconst_null", ""), 567: ("astore", "21"),
    569: ("iload", "9"), 571: ("ifeq", "669"), 574: ("aload_2", ""),
    575: ("invokevirtual", "LivingEntity.getBoundingBox:"), 578: ("fload", "8"),
    580: ("f2d", ""), 581: ("invokevirtual", "AABB.inflate:(D)"), 584: ("astore", "22"),
    586: ("fconst_1", ""), 587: ("fstore", "23"), 589: ("aload_2", ""),
    590: ("invokevirtual", "LivingEntity.getEyePosition:"), 593: ("astore", "24"),
    595: ("fload", "23"), 597: ("fload", "8"), 599: ("fcmpg", ""), 600: ("ifge", "666"),
    603: ("aload", "24"), 605: ("aload_2", ""), 606: ("fconst_1", ""),
    607: ("invokevirtual", "LivingEntity.getViewVector:"), 610: ("invokevirtual", "Vec3.add:"),
    613: ("astore", "24"), 615: ("aload", "24"), 617: ("aload_2", ""), 618: ("fconst_1", ""),
    619: ("invokevirtual", "LivingEntity.getViewVector:"), 622: ("invokevirtual", "Vec3.add:"), 625: ("astore", "25"),
    627: ("aload_1", ""), 628: ("aload_2", ""), 629: ("aload", "24"), 631: ("aload", "25"),
    633: ("aload", "22"), 635: ("invokedynamic", "#0:test:"),
    640: ("invokestatic", "ProjectileUtil.getEntityHitResult:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/phys/Vec3;Lnet/minecraft/world/phys/Vec3;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Lnet/minecraft/world/phys/EntityHitResult;"),
    643: ("astore", "26"), 645: ("aload", "26"), 647: ("ifnull", "657"),
    650: ("aload", "26"), 652: ("astore", "10"), 654: ("goto", "666"),
    657: ("fload", "23"), 659: ("fconst_1", ""), 660: ("fadd", ""), 661: ("fstore", "23"),
    663: ("goto", "595"), 666: ("goto", "734"),
    669: ("aload", "10"), 671: ("instanceof", "BlockHitResult"), 674: ("ifeq", "734"),
    677: ("aload", "10"), 679: ("checkcast", "BlockHitResult"), 682: ("astore", "22"),
    684: ("aload", "22"), 686: ("invokevirtual", "BlockHitResult.getBlockPos:"), 689: ("astore", "23"),
    691: ("aload_1", ""), 692: ("aload", "23"), 694: ("invokevirtual", "Level.getBlockState:"), 697: ("astore", "24"),
    699: ("aload", "22"), 701: ("invokevirtual", "BlockHitResult.getDirection:"), 704: ("astore", "20"),
    706: ("aload", "24"), 708: ("invokevirtual", "BlockState.isAir:"), 711: ("ifne", "734"),
    714: ("aload", "24"), 716: ("aload_1", ""), 717: ("aload", "23"), 719: ("aload", "20"),
    721: ("invokevirtual", "BlockState.isFaceSturdy:"), 724: ("ifeq", "734"),
    727: ("aload", "10"), 729: ("invokevirtual", "HitResult.getLocation:"), 732: ("astore", "21"),
    734: ("aload", "10"), 736: ("instanceof", "EntityHitResult"), 739: ("ifeq", "768"),
    742: ("aload", "10"), 744: ("checkcast", "EntityHitResult"), 747: ("astore", "22"),
    749: ("aload", "22"), 751: ("invokevirtual", "EntityHitResult.getEntity:"),
    754: ("invokevirtual", "Entity.position:"), 757: ("astore", "21"),
    759: ("getstatic", "Direction.UP:"), 762: ("astore", "20"), 764: ("aload", "21"), 766: ("astore", "14"),
    768: ("aload", "21"), 770: ("ifnull", "874"), 773: ("iload", "5"),
    775: ("iconst_2", ""), 776: ("irem", ""), 777: ("ifne", "874"),
    834: ("astore", "23"), 874: ("aload_1", ""),
    875: ("invokevirtual", "Level.isClientSide:"), 878: ("ifne", "1160"),
    881: ("iload", "5"), 883: ("iload", "6"), 885: ("isub", ""),
    886: ("iconst_3", ""), 887: ("irem", ""), 888: ("ifne", "1160"),
    891: ("new", "AABB"), 895: ("aload", "14"), 897: ("ldc2_w", "double -1.0d"),
    900: ("ldc2_w", "double -1.0d"), 903: ("ldc2_w", "double -1.0d"),
    906: ("invokevirtual", "Vec3.add:(DDD)"), 909: ("aload", "14"),
    911: ("dconst_1", ""), 912: ("dconst_1", ""), 913: ("dconst_1", ""),
    914: ("invokevirtual", "Vec3.add:(DDD)"), 917: ("invokespecial", "AABB."),
    932: ("istore", "23"), 938: ("invokedynamic", "#0:test:"), 943: ("invokevirtual", "Level.getEntities:"),
}
REGISTRY_PIVOTS = {194: ("ldc_w", "String x_ray"), 197: ("invokestatic", "key:(Ljava/lang/String;)"), 200: ("putstatic", "X_RAY:")}
KEY_PIVOTS = {0: ("getstatic", "Registries.ENCHANTMENT:"), 3: ("ldc", "String alexscaves"), 5: ("aload_0", ""), 6: ("invokestatic", "ResourceLocation.fromNamespaceAndPath:"), 9: ("invokestatic", "ResourceKey.create:"), 12: ("areturn", "")}
KEY_SHA256 = "40210390d9ab29d32b359bd02dbf74e41083d829b341905ca272bbc6b681a9f1"
CLINIT_SHA256 = 'c8d1d26f8fed7476bac1f90cc58329630cf3e86830079b4dd0bc06d18027f525'
CLINIT_INSTRUCTIONS = 182
SLOT_ACCESS = {
    8: [(41, "fstore"), (66, "fload"), (75, "fload"), (90, "fload"), (578, "fload"), (597, "fload")],
    9: [(58, "istore"), (105, "iload"), (122, "iload"), (569, "iload")],
    10: [(72, "astore"), (652, "astore"), (669, "aload"), (677, "aload"), (727, "aload"), (734, "aload"), (742, "aload")],
    11: [(83, "astore"), (115, "aload"), (132, "aload")],
    12: [(103, "astore"), (110, "aload"), (127, "aload")],
    13: [(120, "astore"), (218, "aload"), (223, "aload"), (228, "aload"), (494, "aload"), (518, "aload"), (527, "aload")],
    14: [(137, "astore"), (766, "astore"), (895, "aload"), (909, "aload")],
    23: [(587, "fstore"), (595, "fload"), (657, "fload"), (661, "fstore"), (689, "astore"), (692, "aload"), (717, "aload"), (834, "astore"), (848, "aload"), (853, "aload"), (858, "aload"), (932, "istore"), (1114, "iload")],
}
PUBLISHER_ENCHANTMENT_HASHES = {
    "data/alexscaves/enchantment/arrow_inducting.json": "80d52e42318ad732b32ba6118dea8f5b315b8d2d702da32d202ff95246a973e5",
    "data/alexscaves/enchantment/astral_transferring.json": "41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2",
    "data/alexscaves/enchantment/bonking.json": "f03c4e8c2f8b00b3668b8d7bf14276647b3e0324c159c6336b189a258571a86a",
    "data/alexscaves/enchantment/bouncing_bolt.json": "bc103328ad554dd97348becf898d5ecedd2867385d1ffbd756cf04ec302d24e7",
    "data/alexscaves/enchantment/bouncy_ball.json": "003c602b45f66154304a0cabdff36b71450da876b071bd355ad604e2cab632ca",
    "data/alexscaves/enchantment/charting_call.json": "352ec52d0e21298a921cc10fe5253b0484c0b273adf3fc5713bce046758ccacd",
    "data/alexscaves/enchantment/chomping_spirit.json": "f0fb73c3e1c564831375009736264848190a6a6edd126b36bb3802ff356fa6e7",
    "data/alexscaves/enchantment/crystallization.json": "b2394e226f7d31843e6d459ef48e21bb955be3d174b3d63eb7ef0a66f0fee3da",
    "data/alexscaves/enchantment/dark_nock.json": "569cb5857db11189b2eb8a1163d53a440587ab02e2f14bc8296aaaf91dcd8033",
    "data/alexscaves/enchantment/dazing_sweep.json": "c86a7aceb5dfec02083dabc93ab51dc5253fbeb616c013a5f33f343656c26318",
    "data/alexscaves/enchantment/detonating_death.json": "8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e",
    "data/alexscaves/enchantment/double_stab.json": "554b3d0fb8e157ef912716cba8180b43cae340f01ee64ca931465b1d2884ff71",
    "data/alexscaves/enchantment/energy_efficiency.json": "c5771a00e6dd2dd0a693369a110a943354b074dde27b9f3c9d1dcb4a8440cf3a",
    "data/alexscaves/enchantment/enveloping_bubble.json": "d984c8cc3f8d72bffa2fce0972a2449b393907f7686626cc6135bf2a8260ed5a",
    "data/alexscaves/enchantment/explosive_flavor.json": "2da6cbf1a482c69cb268a65667a4b25ea402bc3d9c7b055ef2bd7e5d8f2d08e8",
    "data/alexscaves/enchantment/far_flung.json": "a7f48d6ad8eca7a883b3d930313d6962334b0b43a0d6722cb2e60831e9ed8e8c",
    "data/alexscaves/enchantment/ferrous_haste.json": "38db83ed098b276532ad99d652f0614a4ec85b23c1dacb1f17d614a9a3d2f819",
    "data/alexscaves/enchantment/field_extension.json": "c0f2998a08abbefc53a67447ad9e899cdb43bf8a0144a38d53d5fde2b90eb43e",
    "data/alexscaves/enchantment/flinging.json": "0680721d1687f85991e11ee33908b67aa8b720339e7b09eeaaaf92cf604356f2",
    "data/alexscaves/enchantment/gamma_ray.json": "4873ef951ef2afff56e8734740e68c0e4bec4b2d69e893632a9f97dc317630fd",
    "data/alexscaves/enchantment/heavy_slam.json": "927532341a9a53ac73c081f99d7f9b4703f9fa3245c1fdafb609dfdba7733c8a",
    "data/alexscaves/enchantment/herd_phalanx.json": "294818f10b6327c0ca06ef4510d599bba0a61a6c47ffc044236268411ccc0616",
    "data/alexscaves/enchantment/humungous_hex.json": "8c45ec4c64e1ed5e258ce1a8d6a27b7693275336b76b91d108521fb91a015cc0",
    "data/alexscaves/enchantment/impending_stab.json": "bb3918b0fdf897ad70897952d15094e04d8af905b3e2f2db0d2159b762f5ffbc",
    "data/alexscaves/enchantment/lasting_morale.json": "8c662fb7f68987d8e564ec053ebccdd9232593e5961d2213bbbed037b270232f",
    "data/alexscaves/enchantment/multiple_mint.json": "e7357f60b417fa10f5c64518dc51ab61365dca1a410c342ef2aa0604de40af03",
    "data/alexscaves/enchantment/peppermint_punting.json": "ebe5a66b3d69d1d4384149959893712a7458ed9acfcc9064fa58fd16e8ba412b",
    "data/alexscaves/enchantment/plummeting_flight.json": "163b032e37c716f0ef172a37b739a6d61340dab7c629c070698f8543999ec830",
    "data/alexscaves/enchantment/precise_volley.json": "59efc44222dcd59530e13a50cb413a2db0c875213ced1a2ac9de2ef982615f53",
    "data/alexscaves/enchantment/rapid_possession.json": "449eda001a6bb6507ef4e43cc18e601659d970e8bd7d43967aff32dfed07288a",
    "data/alexscaves/enchantment/relentless_darkness.json": "94edb103571eba0d0ca503b8a9455d4643a0f414c758b4ca79d49bbcdf9f473e",
    "data/alexscaves/enchantment/sated_blade.json": "9f9857ce8d742c377ae7a88a1e4261825c3359a90311f5bfaa3d1a3c792fa86b",
    "data/alexscaves/enchantment/sea_swing.json": "f5e7985f7941b02a47966fa1135f3fc3ceff05b60d9eee015cbb6b33c7eb9c3a",
    "data/alexscaves/enchantment/seapairing.json": "e814c593b935bca5a9b84f2ae3aa56d137d9bd099a9e7334b7d4a47fcccfbc57",
    "data/alexscaves/enchantment/second_wave.json": "68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c",
    "data/alexscaves/enchantment/seekcandy.json": "7e564925928b90368d9042f1b722f89464bfbd708abf69ced0d785b5871f0a74",
    "data/alexscaves/enchantment/shaded_respite.json": "0c5bc4a73c8779c7bc0da2eb47a59e1263ac6c2ef6dead0cbfe5223c73e05872",
    "data/alexscaves/enchantment/sharp_cane.json": "d9d75a98966a4881b93ea877d2e8d9be15539dc7a162ba32de5dce112b41c181",
    "data/alexscaves/enchantment/sightless.json": "1e7d093a0d459e2e6a29b40cd625b4fb1f990285343b53e4421c8f3727b2ecb9",
    "data/alexscaves/enchantment/soak_seeking.json": "cfec967d084e9dc3870b90bc05d62375524af447ae280aa7fea63458e644b66b",
    "data/alexscaves/enchantment/solar.json": "6b89d32889d8da9adfad072c534ae76627b1c620d489951bf1095f1805809b80",
    "data/alexscaves/enchantment/spell_lasting.json": "839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc",
    "data/alexscaves/enchantment/straight_hook.json": "75508b5c035e6e240a17ca3e31a4757838cb03e6b7f444e2ece49df284cc3b6f",
    "data/alexscaves/enchantment/swiftwood.json": "3d19fac156679ac53f49424b9bb828ad44a003d3d33a8b14dda303d50fc17551",
    "data/alexscaves/enchantment/targeted_ricochet.json": "adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e",
    "data/alexscaves/enchantment/taxing_bellow.json": "275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1",
    "data/alexscaves/enchantment/triple_splash.json": "6946e2d21814f3e398925f2886a6284b140032b255a05f9598c8e00e2bc315be",
    "data/alexscaves/enchantment/triple_split.json": "fd4f773c48969b4c2537f443cc80d91e1385d545763be78feaefc5816ac551a0",
    "data/alexscaves/enchantment/tsunami.json": "37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242",
    "data/alexscaves/enchantment/twilight_perfection.json": "82a8e06c07b66be33a330bdbeb1bc867d03ce13a49ab2505fa06504fe5f044e1",
    "data/alexscaves/enchantment/x_ray.json": "612b1f7b126cea12085dea00736115b05fd4789bf9fc9ff6c4344a427135b0f8"
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def check_pivots(method, expected):
    rows = method["instructions"]
    offsets = [r["offset"] for r in rows]
    require(offsets == sorted(set(offsets)), "duplicate/unordered X-Ray native offsets")
    by = {r["offset"]: r for r in rows}
    result = []
    for offset, (opcode, token) in sorted(expected.items()):
        row = by.get(offset)
        match = row is not None and row["opcode"] == opcode
        if match:
            match = row["operand"] == token if not token or re.fullmatch(r"-?\d+", token) else token in row["operand"] + " " + row["symbol"]
        require(match, "X-Ray native causal pivot drift @" + str(offset))
        result.append({key: row[key] for key in ("offset", "opcode", "operand", "symbol")})
    return result


def local_slots(method):
    check_pivots(method, {})
    result = {}
    for slot, expected in SLOT_ACCESS.items():
        rows = [r for r in method["instructions"] if (local_access(r) or (-1, ""))[0] == slot]
        require([(r["offset"], r["opcode"]) for r in rows] == expected, "X-Ray local" + str(slot) + " use/definition drift")
        result[str(slot)] = [{**{key: r[key] for key in ("offset", "opcode", "operand", "symbol")}, "access": local_access(r)[1]} for r in rows]
    refs = [r["offset"] for r in method["instructions"] if "ACEnchantmentRegistry.X_RAY:" in r["symbol"]]
    require(refs == [44], "X-Ray native lookup population drift")
    return result


def verify_resources(raw):
    require(set(raw) == set(RESOURCE_HASHES), "X-Ray publisher resource roster drift")
    require({name: digest(value) for name, value in raw.items()} == RESOURCE_HASHES, "X-Ray publisher resource fingerprint drift")
    parsed = {name: json.loads(value, object_pairs_hook=unique_pairs) for name, value in raw.items()}
    require(parsed[RES] == EXACT_X_RAY and parsed[GAMMA_RES] == EXACT_GAMMA and parsed[TAG] == EXACT_TAG, "X-Ray metadata/exclusion/item tag drift")
    return parsed


def registry_clinit(source):
    # The shared declaration parser deliberately omits static {}. Normalize
    # exactly one declaration only, then seal the complete parsed initializer.
    normalized, count = re.subn(r"(?m)^  static \{\};$", "  private static void nativeClinit();", source)
    require(count == 1, "missing/ambiguous native registry initializer")
    return method_select(parse_methods(normalized), "nativeClinit", "()V")


def publisher_enchantment_census(raw, inventory):
    require(set(raw) == set(PUBLISHER_ENCHANTMENT_HASHES) and len(raw) == 51, "publisher enchantment JSON population drift")
    observed = {name: digest(value) for name, value in raw.items()}
    require(observed == PUBLISHER_ENCHANTMENT_HASHES, "publisher enchantment JSON hash drift")
    ids = sorted(Path(name).stem for name in raw)
    require(inventory["counts"]["enchantment_jsons"] == 51 and ids == inventory["remaining_family_inventory"]["enchantment_ids"], "publisher enchantment IDs/inventory drift")
    return {"scope": "EXACT_PUBLISHER_ENCHANTMENT_JSON_ROSTER_ONLY_NOT_RUNTIME_REGISTRY_CLOSURE", "count": 51, "ids": ids, "resource_sha256": observed, "inventory_ids_match": True}


def audit(jar: Path, javap_bin: str):
    jar = Path(jar)
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE), "publisher 1.0.10 JAR fingerprint drift")
    for name, expected in PRIOR_SEALS.items():
        require(digest((PROVIDER / name).read_bytes()) == expected, "prior independent seal drift: " + name)
    inherited = gamma.audit(jar, javap_bin)
    require(digest(canonical(inherited).encode("utf8")) == GAMMA_REPORT_SHA256, "frozen Gamma composed report drift")
    require(inherited["composed_energy_report_sha256"] == ENERGY_REPORT_SHA256, "frozen Energy composed report drift")
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        require(set(CLASS_HASHES) | set(RESOURCE_HASHES) <= set(names), "missing X-Ray native class or resource")
        require({name: digest(arc.read(name)) for name in CLASS_HASHES} == CLASS_HASHES, "X-Ray compiled class fingerprint drift")
        resources = verify_resources({name: arc.read(name) for name in RESOURCE_HASHES})
        owners = sorted(name for name in names if name.startswith("com/github/alexmodguy/alexscaves/") and name.endswith(".class") and b"X_RAY" in arc.read(name))
        require(owners == TOKEN_OWNERS, "compiled X_RAY token owner census drift")
        raw_enchants = {name: arc.read(name) for name in names if re.fullmatch(r"data/alexscaves/enchantment/[^/]+\.json", name)}
    inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text(encoding="utf8"), object_pairs_hook=unique_pairs)
    publisher = publisher_enchantment_census(raw_enchants, inventory)
    sources = {owner: javap(javap_bin, jar, owner[:-6].replace("/", ".")) for owner in CLASS_HASHES}
    declared = {owner: parse_methods(source) for owner, source in sources.items()}
    require({owner: len(methods) for owner, methods in declared.items()} == {CLASS: 26, CLASS_REG: 4}, "X-Ray declared method census drift")
    tick = method_select(declared[CLASS], "onUseTick", CANONICAL_METHODS["onUseTick"])
    key = method_select(declared[CLASS_REG], "key", "(Ljava/lang/String;)Lnet/minecraft/resources/ResourceKey;")
    clinit = registry_clinit(sources[CLASS_REG])
    census, pivots, selected_edges = [], [], []
    specs = [(CLASS, "onUseTick", tick, PARENT_HASHES["onUseTick"], 523, 57, TICK_PIVOTS), (CLASS_REG, "key", key, KEY_SHA256, 6, 0, KEY_PIVOTS), (CLASS_REG, "<clinit>", clinit, CLINIT_SHA256, CLINIT_INSTRUCTIONS, 0, REGISTRY_PIVOTS)]
    for owner, name, method, body_hash, count, branches, expected in specs:
        native_source = sources[owner].replace("  static {};", "  private static void nativeClinit();") if name == "<clinit>" else sources[owner]
        edges = gamma.verify_method(method, native_source, body_hash, count, branches)
        census.append({"owner": owner, "name": name, "descriptor": method["descriptor"], "body_sha256": digest_method(method), "instructions": count, "direct_branches": len(edges)})
        pivots.extend({"owner": owner, "name": name, **row} for row in check_pivots(method, expected))
        selected_edges.extend({"owner": owner, "name": name, **row} for row in edges if row["offset"] in expected)
    slots = local_slots(tick)
    return {
        "schema_version": 1, "version": "1.0.10", "enchantment": "alexscaves:x_ray",
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY", "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_sha256": CLASS_HASHES, "resource_sha256": RESOURCE_HASHES,
        "resource_json": resources[RES], "gamma_ray_resource_json": resources[GAMMA_RES], "supported_item_tag": resources[TAG],
        "compiled_token_owners": owners, "publisher_enchantment_census": publisher,
        "source_helper_sha256": {"docs/qa/" + name: digest((Path(__file__).parent / name).read_bytes()) for name in SOURCE_HELPERS},
        "prior_seal_sha256": PRIOR_SEALS,
        "composed_gamma_report_sha256": GAMMA_REPORT_SHA256, "composed_energy_report_sha256": inherited["composed_energy_report_sha256"],
        "inherited_native_contract": {"source": "EXACT-GAMMA-RAY-CAUSAL-1.0.10.json", "onUseTick_instructions": 523, "onUseTick_direct_branches": 57, "native_method_count": len(inherited["census"]["method_census"]), "method_census": inherited["census"]["method_census"], "visual_consumers_scope": inherited["visual_consumers"]["scope"], "visual_method_count": len(inherited["visual_consumers"]["method_census"]), "projectile_predicate_bootstrap": {**inherited["projectile_predicate_bootstrap"], "xray_additional_invokedynamic_offset": 635}, "network_authorization": "NOT_VERIFIED", "codec_and_packet_delivery": "NOT_VERIFIED"},
        "census": {"declared_methods": {CLASS: 26, CLASS_REG: 4}, "method_census": census},
        "pivots": pivots, "selected_direct_edges": selected_edges, "local_slot_accesses": slots,
        "xray_boolean_slot": {"slot": 9, "writes": [58], "reads": [105, 122, 569], "predicate": "ACCompat.enchantLevel(stack,X_RAY)>0"},
        "range_slot": {"slot": 8, "writes": [41], "reads": [66, 75, 90, 578, 597], "formula": "25.0F*warmup_progress(local7)"},
        "endpoint_slots": {"full_endpoint": 12, "client_visual_endpoint": 13, "damage_endpoint": 14, "initial_selection": "XRay?local12:local11.pick_location", "entity_result_replaces_damage_endpoint_at": 766},
        "loop_slot23": {"type_in_loop": "float", "writes": [587, 661], "reads": [595, 657], "initial": 1.0, "step": 1.0, "guard": "local23<local8", "later_reuse": {"block_position_store": 689, "impact_position_store": 834, "status_amplifier_store": 932}},
        "static_contract": {
            "registry_mapping": "String x_ray@194 -> key@197 -> X_RAY@200; key uses Registries.ENCHANTMENT and namespace alexscaves",
            "range": "25.0F*warmup_progress; X-Ray does not increase local8",
            "full_endpoint": "eyePosition+getViewVector(0F)*local8 -> local12@103",
            "initial_endpoints": "local13@120 and local14@137 independently choose local12 when X-Ray, otherwise local11=LivingEntity.pick(local8,0F,false).getLocation()",
            "client_visual_endpoint": "isClientSide branch forwards local13 components to setRayPosition@233; delivery and pixels NOT_TESTED",
            "scan_aabb": "shooter.getBoundingBox().inflate((double)local8) -> local22@584; expansion equals local8 on each axis",
            "scan_loop": "float23=1F; local24=eye; while(float23<local8): local24+=getViewVector(1F); local25=local24+getViewVector(1F); getEntityHitResult(level,shooter,local24,local25,local22,predicatebootstrap0)@640; null increments float23 by1F",
            "scan_break": "first nonnull segment result -> local10@652; break@654->666->734; no explicit global nearest-distance comparison; helper internals NOT_VERIFIED",
            "scan_first_segment": "eye+viewVector(1F) to eye+2*viewVector(1F); initial eye-to-eye+view segment is not added by this supplemental loop",
            "scan_no_hit": "initial local10 from getHitResultOnViewVector@69 remains unchanged if no supplemental result",
            "block_sturdy": "only X-Ray false branch@669: BlockHitResult and !isAir and isFaceSturdy(level,blockPos,direction)@721 set impact local21; this branch does not replace damage endpoint14; X-Ray skips@666->734",
            "entity_endpoint": "EntityHitResult after either branch -> entity.position()@754 -> impact21 and damage14@766; direction20=UP",
            "impact_and_damage_separation": "local21 null@770 or elapsed%2!=0@777 skips only impact visuals to874; server cadence/AABB query follows independently, so a non-entity result retains the initially chosen local14 geometry without proving an accepted hit",
            "target_volume": "AABB(local14+(-1D,-1D,-1D),local14+(1D,1D,1D))@891-917",
            "native_pipeline_reference": "frozen Gamma contract: server !isClientSide && (elapsed-15)%3==0; target filters exclude shooter, alliances both ways and same vehicle; X-Ray has no damage/status boolean read or separate bonus",
            "native_damage_status": inherited["static_contract"]["damage_request"] | {"effect_duration_ticks": 800, "gamma_false_amplifier": 0, "gamma_true_amplifier": 4, "status_gate": inherited["static_contract"]["status_gate"]},
            "exclusion": "publisher X-Ray JSON exclusive_set=[alexscaves:gamma_ray]; Gamma JSON has no exclusive_set; effective datapack NOT_VERIFIED",
            "world_boundary": "native calls and branches do not prove actual wall penetration, global nearest selection, protected/PvP hits, accepted damage/effects or an authoritative mutating hook",
        },
        "safety": SAFETY,
    }


def verify_seal(actual, expected):
    require(isinstance(expected, dict) and expected.get("claim_scope") == "STATIC_TECHNICAL_CATALOG_ONLY" and expected.get("safety") == SAFETY, "unsafe X-Ray seal scope or safety drift")
    require(actual == expected, "X-Ray exact native causal seal drift")


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
            verify_seal(expected, expected)
        report = audit(args.jar, args.javap)
        if expected is not None:
            verify_seal(report, expected)
        data = canonical(report)
        require(len(data.encode("utf8")) < 125000, "X-Ray bounded evidence report budget exceeded")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf8")
        print("PASS: SHA-exact X-Ray 1.0.10 static native causal contract")
        print("onUseTick=523 instructions;57 direct branches;local9 write58 reads105,122,569")
        print("publisher_enchantment_jsons=51;token_owners=2")
        print("report_sha256=" + digest(data.encode("utf8")))
        print("STATIC_TECHNICAL_CATALOG_ONLY NO_MUTATION NOT_VERIFIED NOT_TESTED")
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
