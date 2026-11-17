#!/usr/bin/env python3
"""Read-only, SHA-exact Raygun 1.0.10 consolidated static catalog contract.

Replays independent historical probes without changing their discovery scopes.
Every declared item method has a bounded semantic disposition in addition to its
whole-body identity. Requests and client input writes never certify gameplay,
packet authorization, a mutating hook, or provider-wide discovery closure.
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

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_raygun_all_method_seal import ARTIFACT, OWNER, CLASS_SHA256, unique_pairs
import alexscaves_1010_raygun_all_method_seal as all_methods
import alexscaves_1010_raygun_method_census_probe as method_census
import alexscaves_1010_raygun_charge_ammo_flow_probe as charge_ammo
import alexscaves_1010_raygun_charge_cost_probe as charge_cost
import alexscaves_1010_raygun_post_hit_guard_probe as post_hit
import alexscaves_1010_raygun_hit_outcomes_cfg_probe as hit_cfg
import alexscaves_1010_raygun_receiver_probe as receiver
import alexscaves_1010_raygun_receiver_cfg_probe as receiver_cfg
import alexscaves_1010_xray_causal_audit as xray
import alexscaves_1010_gamma_ray_causal_audit as gamma

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-RAYGUN-CONTRACT-1.0.10.json'
PRIMARY = 'data/alexscaves/damage_type/raygun.json'
PRIMARY_HASH = 'dc1095e92e0695b302100993af8fafd72c8d6b948d90717e667a6ced2ae1bc35'
EXACT_PRIMARY = {'exhaustion': 0.3, 'message_id': 'raygun', 'scaling': 'never'}
DIRECT_TAG_HASHES = {
    'data/minecraft/tags/damage_type/bypasses_cooldown.json': '0bc51535f4e629ac4f0654411d218781a2474a4560728c6f107bd233ed021990',
    'data/minecraft/tags/damage_type/is_explosion.json': '15bd614968d8b1876e9759243cc20f09e9cbda75bfa288e221fdf45a1c5c20f5',
    'data/minecraft/tags/damage_type/is_projectile.json': 'bd2df4b9538f61ab6cd1c4405397983ae4108c8fed073c7ffc726845f7d82e9e',
}
PRIOR_SEALS = {
    'EXACT-RAYGUN-ALL-METHODS-1.0.10.json': '324cc3b3c31806516dd77a7c5876de12b471d9d82cb4cf1e6bd83705729a9c82',
    'EXACT-RAYGUN-CHARGE-AMMO-FLOW-1.0.10.json': '19ec9ad9f9c5d6a05526dcfdfdbf4ac49e377b25e9450b40546946b39175e3fe',
    'EXACT-RAYGUN-CHARGE-COST-1.0.10.json': '6547f72877aa6a59102ed1bd17c01eafe61c63dd0f92532ea0536db6fb1e1989',
    'EXACT-RAYGUN-POST-HIT-GUARDS-1.0.10.json': '2deb54234a8832e337ce3b0e1350ded242f3e3fbe675160bcd81018054636b4c',
    'EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json': '48bcbc54ae95b500670de056c340d22f5a0e3b40e5c3e23cbbd514e890a3c1c0',
    'EXACT-RAYGUN-RECEIVER-1.0.10.json': 'fce345cdfcddf73435f3224296a7cb39cfed7b9f595bade34805659f40b110ae',
    'EXACT-RAYGUN-RECEIVER-IDENTITY-1.0.10.json': 'cac61bf80f18ef05290841820293ac976d7358d603acf9ee4a2cf070f82f64b4',
    'EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json': '819f9d27b56da6364622dc478984e8166b419f3ed173a2406cff92007287155d',
    'EXACT-XRAY-CAUSAL-1.0.10.json': '158f03ac7f0369f0a5d90113493ff41314e3d55ea0388a903bd47caf3355aaff',
    'EXACT-GAMMA-RAY-CAUSAL-1.0.10.json': 'cf36a14f33464b6bd75f476b03dc654f11b9fb0f9676ec6337cc442c7c1e2b7c',
}
ANVIL_MARKER = 'com/github/alexmodguy/alexscaves/server/item/AlwaysCombinableOnAnvil.class'
EVENTS = 'com/github/alexmodguy/alexscaves/server/event/CommonEvents.class'
EXTRA_CLASSES = {
    ANVIL_MARKER: 'd6d9ba639692a4e2964eca9163842f2fdfbfc98584b2d1b07155a4c780edf13c',
    EVENTS: 'd132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43',
}
SAFETY = {
    'mutating_hook': 'NOT_VERIFIED', 'physical_qa': 'NOT_TESTED',
    'mutation': 'NO_MUTATION', 'provider_universe_closed': False,
    'unaccounted_native_roots': 0,
    'network_authorization': 'NOT_VERIFIED', 'network_sanitization': 'NOT_VERIFIED',
    'network_replay_protection': 'NOT_VERIFIED', 'codec_and_packet_delivery': 'NOT_VERIFIED',
    'effective_charge_settlement': 'NOT_TESTED', 'accepted_damage_and_effects': 'NOT_TESTED',
    'effective_world_datapack': 'NOT_VERIFIED', 'claims_and_pvp': 'NOT_VERIFIED',
    'exception_edges_and_transformed_runtime': 'NOT_RECONSTRUCTED',
    'complete_rendering_cfg': 'NOT_RECONSTRUCTED',
}

# The bounded pivots are predicates, constants, state keys and direct delegates.
# Independent full-body fingerprints cover instructions omitted from this view.
METHOD_PIVOTS = {
    'RaygunItem': {8: ('iconst_1', ''), 9: ('invokevirtual', 'Properties.stacksTo:'), 12: ('invokespecial', 'Item."<init>":')},
    'initializeClient': {1: ('getstatic', 'AlexsCaves.PROXY:'), 4: ('invokevirtual', 'getISTERProperties:'), 10: ('invokeinterface', 'Consumer.accept:')},
    'getEnchantmentValue': {0: ('iconst_1', ''), 1: ('ireturn', '')},
    'isEnchantable': {1: ('invokevirtual', 'ItemStack.getCount:'), 4: ('iconst_1', ''), 5: ('if_icmpne', '12'), 8: ('iconst_1', ''), 12: ('iconst_0', '')},
    'hasCharge': {1: ('invokestatic', 'getCharge:'), 4: ('sipush', '1000'), 7: ('if_icmpge', '14'), 10: ('iconst_1', ''), 14: ('iconst_0', '')},
    'use': {9: ('invokestatic', 'hasCharge:'), 12: ('ifeq', '41'), 17: ('invokevirtual', 'startUsingItem:'), 21: ('getstatic', 'RAYGUN_START:'), 37: ('invokestatic', 'ACCompat.useConsume:'), 43: ('invokevirtual', 'findAmmo:'), 49: ('invokevirtual', 'isCreative:'), 59: ('ifne', '71'), 64: ('iconst_1', ''), 65: ('invokevirtual', 'ItemStack.shrink:'), 73: ('ifeq', '125'), 78: ('iconst_0', ''), 79: ('invokestatic', 'setCharge:'), 102: ('getstatic', 'RAYGUN_RELOAD:'), 145: ('getstatic', 'RAYGUN_EMPTY:'), 167: ('invokestatic', 'ACCompat.useFail:')},
    'findAmmo': {1: ('invokevirtual', 'isCreative:'), 4: ('ifeq', '11'), 7: ('getstatic', 'ItemStack.EMPTY:'), 18: ('invokevirtual', 'Inventory.getContainerSize:'), 21: ('if_icmpge', '53'), 29: ('invokevirtual', 'Inventory.getItem:'), 33: ('getstatic', 'AMMO:'), 37: ('invokeinterface', 'Predicate.test:'), 42: ('ifeq', '47'), 50: ('goto', '13'), 53: ('getstatic', 'ItemStack.EMPTY:')},
    'getUseAnimation': {0: ('getstatic', 'UseAnim.NONE:')},
    'getUseDuration': {0: ('ldc', 'int 72000')},
    'acInventoryTick': {15: ('invokevirtual', 'getUseItem:'), 19: ('invokevirtual', 'Object.equals:'), 22: ('ifeq', '29'), 30: ('istore', '5'), 33: ('invokestatic', 'getUseTime:'), 39: ('invokevirtual', 'isClientSide:'), 42: ('ifne', '146'), 46: ('getstatic', 'SOLAR:'), 49: ('invokestatic', 'ACCompat.enchantLevel:'), 52: ('ifle', '230'), 57: ('ifne', '230'), 61: ('invokestatic', 'getCharge:'), 68: ('ifle', '143'), 75: ('invokeinterface', 'nextFloat:'), 80: ('ldc', 'float 0.02f'), 83: ('ifge', '143'), 87: ('invokevirtual', 'blockPosition:'), 90: ('invokevirtual', 'BlockPos.above:'), 98: ('invokevirtual', 'canSeeSky:'), 101: ('ifeq', '143'), 105: ('invokevirtual', 'isDay:'), 108: ('ifeq', '143'), 115: ('invokevirtual', 'hasFixedTime:'), 118: ('ifne', '143'), 124: ('invokestatic', 'sunAboveHorizon:'), 127: ('ifeq', '143'), 133: ('iconst_1', ''), 134: ('isub', ''), 135: ('invokestatic', 'setCharge:'), 139: ('iconst_0', ''), 140: ('invokestatic', 'setUseTime:'), 154: ('ldc', 'PrevUseTime'), 161: ('ldc', 'UseTime'), 166: ('if_icmpeq', '180'), 177: ('invokevirtual', 'CompoundTag.putInt:'), 183: ('invokestatic', 'ACCompat.setTag:'), 188: ('ifeq', '209'), 194: ('ldc_w', 'float 5.0f'), 198: ('ifge', '209'), 205: ('iadd', ''), 206: ('invokestatic', 'setUseTime:'), 211: ('ifne', '230'), 219: ('ifle', '230'), 226: ('isub', ''), 227: ('invokestatic', 'setUseTime:')},
    'onUseTick': {140: ('invokestatic', 'hasCharge:'), 143: ('ifne', '210'), 169: ('invokevirtual', 'stopUsingItem:'), 209: ('return', ''), 214: ('ifeq', '322'), 246: ('getstatic', 'ENERGY_EFFICIENCY:'), 274: ('iflt', '322'), 282: ('ifne', '322'), 299: ('ifne', '322'), 313: ('sipush', '1000'), 316: ('invokestatic', 'Math.min:'), 319: ('invokestatic', 'setCharge:'), 875: ('invokevirtual', 'isClientSide:'), 878: ('ifne', '1160'), 885: ('isub', ''), 886: ('iconst_3', ''), 887: ('irem', ''), 888: ('ifne', '1160')},
    'setUseTime': {1: ('invokestatic', 'getOrCreateTag:'), 6: ('ldc', 'PrevUseTime'), 9: ('invokestatic', 'getUseTime:'), 12: ('invokevirtual', 'putInt:'), 16: ('ldc', 'UseTime'), 18: ('iload_1', ''), 19: ('invokevirtual', 'putInt:'), 24: ('invokestatic', 'setTag:')},
    'setRayPosition': {1: ('invokestatic', 'getOrCreateTag:'), 7: ('invokestatic', 'getRayPosition:'), 14: ('ldc_w', 'PrevRayX'), 27: ('ldc_w', 'PrevRayY'), 40: ('ldc_w', 'PrevRayZ'), 53: ('ldc_w', 'RayX'), 56: ('dload_1', ''), 62: ('ldc_w', 'RayY'), 65: ('dload_3', ''), 71: ('ldc_w', 'RayZ'), 74: ('dload', '5'), 82: ('invokestatic', 'setTag:')},
    'getUseTime': {1: ('invokestatic', 'getTag:'), 6: ('ifnull', '18'), 10: ('ldc', 'UseTime'), 12: ('invokestatic', 'getInt:'), 18: ('iconst_0', '')},
    'getCharge': {1: ('invokestatic', 'getTag:'), 6: ('ifnull', '19'), 10: ('ldc_w', 'ChargeUsed'), 13: ('invokestatic', 'getInt:'), 19: ('iconst_0', '')},
    'setCharge': {1: ('invokestatic', 'getOrCreateTag:'), 6: ('ldc_w', 'ChargeUsed'), 9: ('iload_1', ''), 10: ('invokevirtual', 'putInt:'), 15: ('invokestatic', 'setTag:')},
    'getRayPosition': {1: ('invokestatic', 'getTag:'), 6: ('ifnull', '48'), 10: ('ldc_w', 'RayX'), 13: ('invokevirtual', 'contains:'), 16: ('ifeq', '48'), 24: ('ldc_w', 'RayX'), 27: ('invokestatic', 'getDouble:'), 31: ('ldc_w', 'RayY'), 34: ('invokestatic', 'getDouble:'), 38: ('ldc_w', 'RayZ'), 41: ('invokestatic', 'getDouble:'), 44: ('invokespecial', 'Vec3."<init>":'), 48: ('getstatic', 'Vec3.ZERO:')},
    'getLerpedUseTime': {6: ('ifnull', '19'), 10: ('ldc', 'PrevUseTime'), 19: ('fconst_0', ''), 22: ('ifnull', '35'), 26: ('ldc', 'UseTime'), 35: ('fconst_0', ''), 43: ('fsub', ''), 44: ('fmul', ''), 45: ('fadd', '')},
    'getLerpedRayPosition': {6: ('ifnull', '113'), 10: ('ldc_w', 'PrevRayX'), 20: ('ldc_w', 'RayX'), 31: ('ldc_w', 'PrevRayY'), 42: ('ldc_w', 'RayY'), 53: ('ldc_w', 'PrevRayZ'), 64: ('ldc_w', 'RayZ'), 16: ('d2f', ''), 17: ('f2d', ''), 26: ('d2f', ''), 27: ('f2d', ''), 37: ('d2f', ''), 38: ('f2d', ''), 48: ('d2f', ''), 49: ('f2d', ''), 59: ('d2f', ''), 60: ('f2d', ''), 70: ('d2f', ''), 71: ('f2d', ''), 84: ('dsub', ''), 85: ('dmul', ''), 86: ('dadd', ''), 95: ('dsub', ''), 96: ('dmul', ''), 97: ('dadd', ''), 106: ('dsub', ''), 107: ('dmul', ''), 108: ('dadd', ''), 113: ('aconst_null', '')},
    'releaseUsing': {6: ('invokespecial', 'Item.releaseUsing:'), 10: ('invokevirtual', 'isClientSide:'), 13: ('ifeq', '31'), 25: ('invokespecial', 'UpdateItemTagMessage."<init>":'), 28: ('invokestatic', 'sendMSGToServer:'), 35: ('invokevirtual', 'clearSoundCacheFor:')},
    'isBarVisible': {1: ('invokestatic', 'getCharge:'), 4: ('ifeq', '11'), 7: ('iconst_1', ''), 11: ('iconst_0', '')},
    'getBarWidth': {0: ('ldc_w', 'float 13.0f'), 4: ('invokestatic', 'getCharge:'), 8: ('ldc_w', 'float 13.0f'), 11: ('fmul', ''), 12: ('ldc_w', 'float 1000.0f'), 15: ('fdiv', ''), 16: ('fsub', ''), 17: ('invokestatic', 'Math.round:')},
    'getBarColor': {1: ('invokestatic', 'getCharge:'), 5: ('ldc_w', 'float 1000.0f'), 8: ('fdiv', ''), 9: ('fconst_2', ''), 10: ('fmul', ''), 15: ('invokevirtual', 'getPlayerTime:'), 22: ('invokevirtual', 'getPartialTicks:'), 25: ('fadd', ''), 27: ('ldc_w', 'float 0.5f'), 33: ('fmul', ''), 35: ('invokestatic', 'Math.sin:'), 38: ('dadd', ''), 40: ('fmul', ''), 43: ('ldc_w', 'float 0.3f'), 48: ('ldc_w', 'float 0.6f'), 51: ('fmul', ''), 52: ('ldc_w', 'float 0.2f'), 55: ('fadd', ''), 56: ('fconst_1', ''), 57: ('invokestatic', 'Mth.hsvToRgb:')},
    'appendHoverText': {1: ('invokestatic', 'getCharge:'), 4: ('ifeq', '59'), 7: ('sipush', '1000'), 11: ('invokestatic', 'getCharge:'), 14: ('isub', ''), 23: ('ldc_w', 'item.alexscaves.raygun.charge'), 37: ('sipush', '1000'), 47: ('getstatic', 'ChatFormatting.GREEN:'), 53: ('invokeinterface', 'List.add:')},
    'shouldCauseReequipAnimation': {1: ('getstatic', 'ACItemRegistry.RAYGUN:'), 12: ('invokevirtual', 'ItemStack.is:'), 15: ('ifeq', '36'), 19: ('getstatic', 'ACItemRegistry.RAYGUN:'), 30: ('invokevirtual', 'ItemStack.is:'), 33: ('ifne', '40'), 36: ('iconst_1', ''), 40: ('iconst_0', '')},
    'lambda$static$0': {1: ('invokevirtual', 'ItemStack.getItem:'), 4: ('getstatic', 'ACBlockRegistry.URANIUM_ROD:'), 15: ('invokevirtual', 'Block.asItem:'), 18: ('if_acmpne', '25'), 21: ('iconst_1', ''), 25: ('iconst_0', '')},
}

# Explicit catalog dispositions prevent identity-only hashes being mistaken for
# semantic review. UI/delegates have their relevant behavior and N/A explained.
METHOD_FACTS = {
    'RaygunItem': ('ITEM_LIFECYCLE', 'Constructs Item.Properties.stacksTo(1); no durability property is requested by this constructor.'),
    'initializeClient': ('CLIENT_DELEGATE', 'Passes PROXY.getISTERProperties() as IClientItemExtensions to Consumer.accept; downstream rendering remains the bounded Gamma visual delegate.'),
    'getEnchantmentValue': ('ENCHANTING_PARAMETER', 'Returns 1.'),
    'isEnchantable': ('ENCHANTING_PREDICATE', 'Returns stack.getCount()==1.'),
    'hasCharge': ('CHARGE_PREDICATE', 'Returns getCharge(stack)<1000; ChargeUsed is expenditure, not remaining charge.'),
    'use': ('ACTIVATION_AND_AMMO', 'Loaded use starts using the hand, requests RAYGUN_START and useConsume; exhausted use finds ammo, shrinks one nonempty ammo stack, sets ChargeUsed=0 when ammo or Creative, requests reload/empty sound, then returns useFail even after reload. No immediate start on the reload branch.'),
    'findAmmo': ('AMMO_SELECTION', 'Creative returns EMPTY; otherwise scans inventory slots in increasing order and returns the first AMMO match or EMPTY.'),
    'getUseAnimation': ('UI_ONLY', 'Returns UseAnim.NONE; no damage/cost operation.'),
    'getUseDuration': ('USE_PARAMETER', 'Returns 72000 ticks.'),
    'acInventoryTick': ('INVENTORY_AND_SOLAR', 'Server Solar recovery requires level>0, idle stack, ChargeUsed>0, randomFloat<0.02, sky above holder, day, no fixed time and sunAboveHorizon; decrements expenditure by1 and writes UseTime0. Client copies changed PrevUseTime and increments UseTime while using below5 or decrements it while idle above0.'),
    'onUseTick': ('COMPOSED_NATIVE_PIPELINE', 'Replayed X-Ray/Gamma/Energy contracts cover warmup, endpoints, client cost, server AoE, filters, damage/status and selected visuals; replayed post-hit and hit-CFG probes preserve independent bounded outcome guards. Depletion stops using and returns before these branches.'),
    'setUseTime': ('RENDER_STATE_WRITE', 'Copies previous getUseTime into PrevUseTime then stores raw argument in UseTime through setTag; no clamp.'),
    'setRayPosition': ('RENDER_STATE_WRITE', 'Copies current getRayPosition into PrevRayX/Y/Z then stores raw argument doubles in RayX/Y/Z through setTag; no position authorization is established.'),
    'getUseTime': ('RENDER_STATE_READ', 'Reads UseTime via ACCompat.getInt or returns0 when tag absent.'),
    'getCharge': ('CHARGE_STATE_READ', 'Reads ChargeUsed via ACCompat.getInt or returns0 when tag absent.'),
    'setCharge': ('CHARGE_STATE_WRITE', 'Writes raw integer argument to ChargeUsed through setTag; this setter does not clamp or authorize it.'),
    'getRayPosition': ('RENDER_STATE_READ', 'Returns Vec3(RayX,RayY,RayZ) only with nonnull tag containing RayX, otherwise Vec3.ZERO; only RayX presence is checked.'),
    'getLerpedUseTime': ('UI_ONLY', 'Returns prev+partial*(current-prev) from PrevUseTime/UseTime, using0 defaults for absent tag; no clamp or damage operation.'),
    'getLerpedRayPosition': ('UI_ONLY', 'With nonnull tag, each previous/current double coordinate narrows through float then widens to double before prev+partial*(current-prev); absent tag returns null. No damage operation.'),
    'releaseUsing': ('RELEASE_AND_NETWORK_DELEGATE', 'Calls Item.releaseUsing, sends UpdateItemTagMessage only client-side and clears proxy sound cache; no own charge or UseTime reset.'),
    'isBarVisible': ('UI_ONLY', 'Returns getCharge()!=0; no damage/cost operation.'),
    'getBarWidth': ('UI_ONLY', 'Returns Math.round(13F-getCharge()*13F/1000F), with no own clamp.'),
    'getBarColor': ('UI_ONLY', 'HSV uses hue0.3, value1, saturation0.2+0.6*(0.5*(1+sin((playerTime+partialTicks)*(2*ChargeUsed/1000)))); no damage/cost operation.'),
    'appendHoverText': ('UI_ONLY', 'When ChargeUsed!=0, adds green translatable item.alexscaves.raygun.charge with remaining1000-ChargeUsed and max1000; no own clamp.'),
    'shouldCauseReequipAnimation': ('UI_ONLY', 'Returns false exactly when both old and new stack are RAYGUN; otherwise true. Third argument is unused; no damage/cost operation.'),
    'lambda$static$0': ('AMMO_PREDICATE', 'Tests ItemStack.getItem identity against URANIUM_ROD.get().asItem(); this is reload ammunition, not a declared durability repair ingredient.'),
}

ANVIL_PIVOTS = {7: ('instanceof', 'AlwaysCombinableOnAnvil'), 10: ('ifeq', '395'), 27: ('if_acmpne', '395'), 34: ('invokestatic', 'getEnchantmentsForCrafting:'), 40: ('ifne', '395'), 47: ('invokestatic', 'getEnchantmentsForCrafting:'), 53: ('ifne', '395'), 60: ('invokevirtual', 'ItemStack.copy:'), 85: ('iconst_1', ''), 86: ('istore', '5'), 163: ('if_icmpne', '173'), 169: ('iadd', ''), 177: ('invokestatic', 'Math.max:'), 231: ('invokestatic', 'Enchantment.areCompatible:'), 237: ('iconst_0', ''), 238: ('istore', '5'), 248: ('ifeq', '372'), 255: ('invokevirtual', 'getMaxLevel:'), 258: ('if_icmple', '268'), 273: ('invokevirtual', 'Mutable.set:'), 284: ('tableswitch', ''), 379: ('invokevirtual', 'setCost:'), 387: ('invokestatic', 'setEnchantments:'), 392: ('invokevirtual', 'setOutput:')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf8'), object_pairs_hook=unique_pairs)


def verify_resources(primary, tags):
    require(digest(primary) == PRIMARY_HASH, 'Raygun primary resource fingerprint drift')
    parsed = json.loads(primary, object_pairs_hook=unique_pairs)
    require(parsed == EXACT_PRIMARY, 'Raygun primary damage metadata drift')
    require(set(tags) == set(DIRECT_TAG_HASHES), 'Raygun direct damage tag roster drift')
    require({name: digest(raw) for name, raw in tags.items()} == DIRECT_TAG_HASHES, 'Raygun direct damage tag fingerprint drift')
    values = {name: json.loads(raw, object_pairs_hook=unique_pairs) for name, raw in tags.items()}
    require(all(value.get('replace') is False and 'alexscaves:raygun' in value['values'] for value in values.values()), 'Raygun direct default tag membership drift')
    return parsed, values


def verify_dispositions(methods, sealed_methods):
    require(set(METHOD_FACTS) == set(METHOD_PIVOTS) and len(METHOD_FACTS) == 26, 'Raygun disposition specification roster drift')
    require(len(methods) == len(sealed_methods) == 26, 'Raygun disposition native roster drift')
    by = {}
    for method in methods:
        name = name_of(method)
        require(name not in by, 'duplicate or overloaded Raygun disposition identity')
        by[name] = method
    require(set(by) == set(METHOD_FACTS), 'Raygun missing or extra method disposition')
    result = []
    for sealed in sealed_methods:
        name, descriptor = sealed['method'].split(' ', 1)
        method = by[name]
        require(method['descriptor'] == descriptor and digest_method(method) == sealed['parsed_method_sha256'], 'Raygun disposition whole-method identity drift: ' + name)
        edges, switches = method_census.branches(method)
        require(len(method['instructions']) == sealed['instructions'] and len(edges) == sealed['direct_branches'] and switches == sealed['switch_offsets'], 'Raygun disposition method census drift')
        pivots = gamma.check_pivots(method, METHOD_PIVOTS[name])
        role, fact = METHOD_FACTS[name]
        result.append({**sealed, 'disposition': role, 'facts': fact, 'pivots': pivots, 'evidence': 'WHOLE_BODY_IDENTITY_PLUS_BOUNDED_SEMANTIC_PIVOTS'})
    return result


def verify_initialization(source, javap_bin, jar):
    normalized, count = re.subn(r'(?m)^  static \{\};$', '  private static void nativeClinit();', source)
    require(count == 1, 'Raygun missing or duplicate static initializer')
    method = gamma.method_select(parse_methods(normalized), 'nativeClinit', '()V')
    pivots = gamma.check_pivots(method, {0: ('invokedynamic', '#2:test:'), 5: ('putstatic', 'AMMO:'), 8: ('return', '')})
    require(len(method['instructions']) == 3, 'Raygun static initializer instruction drift')
    result = subprocess.run([str(javap_bin), '-classpath', str(jar), '-v', '-p', OWNER[:-6].replace('/', '.')], capture_output=True, text=True, timeout=45, check=False)
    require(result.returncode == 0 and 0 < len(result.stdout) < 1000000, 'Raygun bootstrap extraction failed')
    blocks = re.findall(r'(?m)^  2: ([\s\S]*?)(?=\nInnerClasses:)', result.stdout)
    require(len(blocks) == 1 and 'REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:' in blocks[0] and 'REF_invokeStatic com/github/alexmodguy/alexscaves/server/item/RaygunItem.lambda$static$0:(Lnet/minecraft/world/item/ItemStack;)Z' in blocks[0], 'Raygun AMMO bootstrap drift')
    return {'scope': 'ADDITIONAL_STATIC_INITIALIZER_NOT_IN_26_METHOD_PARSER_CENSUS', 'instructions': 3, 'body_sha256': digest_method(method), 'pivots': pivots, 'bootstrap': {'index': 2, 'implementation': 'REF_invokeStatic RaygunItem.lambda$static$0:(Lnet/minecraft/world/item/ItemStack;)Z', 'field': 'AMMO'}}


def verify_anvil(source, marker_source):
    require(parse_methods(marker_source) == [], 'AlwaysCombinableOnAnvil marker gained a method')
    method = gamma.method_select(parse_methods(source), 'onUpdateAnvil', '(Lnet/neoforged/neoforge/event/AnvilUpdateEvent;)V')
    pivots = gamma.check_pivots(method, ANVIL_PIVOTS)
    # This external consumer is bounded to native entry/merge/output pivots.
    # Full digest is also frozen in the final canonical report.
    calls = [r['symbol'] for r in method['instructions'] if r['opcode'].startswith('invoke')]
    require(not any(token in symbol for symbol in calls for token in ('setCharge:', 'setUseTime:', 'setDamageValue:', 'shrink:')), 'anvil consumer gained repair/charge mutation')
    return {'scope': 'SELECTED_NATIVE_ANVIL_COMBINATION_CONSUMER_ONLY', 'owner': EVENTS, 'name': 'onUpdateAnvil', 'descriptor': method['descriptor'], 'body_sha256': digest_method(method), 'instructions': len(method['instructions']), 'pivots': pivots, 'marker_declared_methods': 0, 'facts': 'Marker plus same item identity and both enchantment sets nonempty gates a left-stack copy, enchantment merge capped at max level, event cost and output writes. Compatibility local5 is initialized true once before the outer loop; an incompatible pair sets it false and it is not reset for later enchantments. This method has no setCharge/setUseTime/setDamageValue/shrink call; no charge refill or uranium durability repair is inferred.', 'limits': {'complete_anvil_cfg': 'NOT_RECONSTRUCTED', 'actual_event_execution': 'NOT_TESTED'}}


def replay_composed(jar, javap_bin, prior):
    census = method_census.audit(jar, javap_bin)
    all_methods.verify(census, prior['EXACT-RAYGUN-ALL-METHODS-1.0.10.json'])
    reports = {}
    for module, name in ((charge_ammo, 'CHARGE-AMMO-FLOW'), (charge_cost, 'CHARGE-COST'), (post_hit, 'POST-HIT-GUARDS'), (hit_cfg, 'HIT-OUTCOMES-CFG')):
        report = module.audit(jar, javap_bin)
        filename = 'EXACT-RAYGUN-' + name + '-1.0.10.json'
        module.verify_snapshot(report, prior[filename])
        reports[filename] = report
    xreport = xray.audit(jar, javap_bin)
    xray.verify_seal(xreport, prior['EXACT-XRAY-CAUSAL-1.0.10.json'])
    # X-Ray replays the frozen full Gamma and Energy pipeline. Verify both
    # the frozen Gamma bytes and X-Ray's explicit composed report identity.
    require(xreport['composed_gamma_report_sha256'] == PRIOR_SEALS['EXACT-GAMMA-RAY-CAUSAL-1.0.10.json'], 'Raygun composed Gamma report drift')
    require(digest(canonical(xreport).encode('utf8')) == PRIOR_SEALS['EXACT-XRAY-CAUSAL-1.0.10.json'], 'Raygun composed X-Ray report drift')
    rreport = receiver.audit(jar, javap_bin)
    receiver.verify_sealed_report(rreport, prior['EXACT-RAYGUN-RECEIVER-1.0.10.json'])
    cfg = receiver_cfg.audit(jar, javap_bin, prior['EXACT-RAYGUN-RECEIVER-1.0.10.json'], prior['EXACT-RAYGUN-RECEIVER-IDENTITY-1.0.10.json'])
    receiver_cfg.verify_snapshot(cfg, prior['EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json'])
    reports['EXACT-RAYGUN-RECEIVER-1.0.10.json'] = receiver.snapshot_projection(rreport)
    reports['EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json'] = receiver_cfg.snapshot_projection(cfg)
    return census, xreport, {'prior_seal_sha256': PRIOR_SEALS, 'replayed_report_sha256': {name: digest(canonical(value).encode('utf8')) for name, value in reports.items()}, 'composed_xray_report_sha256': digest(canonical(xreport).encode('utf8')), 'composed_gamma_report_sha256': xreport['composed_gamma_report_sha256'], 'composed_energy_report_sha256': xreport['composed_energy_report_sha256'], 'historical_probe_scopes': {name: value['scope'] for name, value in reports.items()}, 'scope_rule': 'Historical discovery scopes remain unchanged; consolidated bounded semantic interpretation is additional evidence, not retrospective runtime promotion.'}


def audit(jar: Path, javap_bin: str):
    jar = Path(jar)
    require(jar.is_file() and sha_file(jar) == (ARTIFACT['sha1'], ARTIFACT['sha256'], ARTIFACT['size_bytes']), 'Raygun publisher artifact fingerprint drift')
    prior = {}
    for name, expected in PRIOR_SEALS.items():
        raw = (PROVIDER / name).read_bytes()
        require(digest(raw) == expected, 'Raygun prior independent seal drift: ' + name)
        prior[name] = json.loads(raw, object_pairs_hook=unique_pairs)
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), 'Raygun duplicate ZIP member')
        require(digest(arc.read(OWNER)) == CLASS_SHA256, 'Raygun compiled class fingerprint drift')
        require({name: digest(arc.read(name)) for name in EXTRA_CLASSES} == EXTRA_CLASSES, 'Raygun bounded anvil class fingerprint drift')
        tags = {}
        for name in names:
            if re.fullmatch(r'data/[^/]+/tags/damage_type/[^/]+\.json', name):
                raw = arc.read(name)
                parsed = json.loads(raw, object_pairs_hook=unique_pairs)
                if 'alexscaves:raygun' in parsed.get('values', []):
                    tags[name] = raw
        primary, tags_json = verify_resources(arc.read(PRIMARY), tags)
    census, xreport, composed = replay_composed(jar, javap_bin, prior)
    source = javap(javap_bin, jar, OWNER[:-6].replace('/', '.'))
    require('extends net.minecraft.world.item.Item implements' in source and 'AlwaysCombinableOnAnvil' in source and 'UpdatesStackTags' in source, 'Raygun declaration/delegate drift')
    dispositions = verify_dispositions(parse_methods(source), prior['EXACT-RAYGUN-ALL-METHODS-1.0.10.json']['methods'])
    init = verify_initialization(source, javap_bin, jar)
    anvil = verify_anvil(javap(javap_bin, jar, EVENTS[:-6].replace('/', '.')), javap(javap_bin, jar, ANVIL_MARKER[:-6].replace('/', '.')))
    gcontract = prior['EXACT-GAMMA-RAY-CAUSAL-1.0.10.json']['static_contract']
    return {
        'schema_version': 1, 'version': '1.0.10', 'damage_type': 'alexscaves:raygun',
        'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
        'artifact': ARTIFACT, 'class_path': OWNER, 'class_sha256': CLASS_SHA256,
        'primary_resource': {'path': PRIMARY, 'sha256': PRIMARY_HASH, 'json': primary},
        'direct_damage_type_tags': {'scope': 'EXACT_PUBLISHER_DIRECT_MEMBERSHIPS_ONLY', 'count': len(tags_json), 'resource_sha256': DIRECT_TAG_HASHES, 'json': tags_json, 'limits': 'Effective datapack tags and inherited/nested vanilla tag resolution NOT_VERIFIED.'},
        'census': {key: census[key] for key in ('declared_methods', 'instruction_total', 'direct_branch_total')},
        'method_dispositions': dispositions, 'static_initialization': init,
        'anvil_delegate': {'class_sha256': EXTRA_CLASSES, **anvil},
        'composed_evidence': composed,
        'static_contract': {
            'identity': {'damage_type': primary, 'source_factory': 'causeRaygunDamage(registryAccess,shooter) resolves RAYGUN and constructs DamageSourceRandomMessages(holder,shooter,1); constructor forwards holder+entity to DamageSource. Reused SHA-exact Gamma helper proof.', 'direct_default_tags': ['minecraft:bypasses_cooldown', 'minecraft:is_explosion', 'minecraft:is_projectile']},
            'behavior': {'activation': METHOD_FACTS['use'][1], 'depletion': 'hasCharge false: client sends item tag message, stops using, requests empty sound and returns; release calls superclass, sends client message and clears proxy sound cache.', 'inventory': METHOD_FACTS['acInventoryTick'][1], 'render_state': 'UseTime/PrevUseTime and Ray/PrevRay keys are separately inventoried; interpolation accessors are UI-only, not accepted-hit evidence.'},
            'parameters': {'max_charge_expenditure': 1000, 'duration_ticks': 72000, 'warmup_ticks': 15, 'range': '25F*(elapsed<15 ? elapsed/15F : 1F)', 'server_damage_gate': '!level.isClientSide() && (elapsed-15)%3==0; no extra elapsed>=15 guard', 'damage_request': gcontract['damage_request'], 'status_duration_ticks': 800, 'gamma_false_amplifier': 0, 'gamma_true_amplifier': 4},
            'targeting': {key: xreport['static_contract'][key] for key in ('full_endpoint', 'initial_endpoints', 'scan_aabb', 'scan_loop', 'scan_break', 'scan_first_segment', 'scan_no_hit', 'block_sturdy', 'entity_endpoint', 'impact_and_damage_separation', 'target_volume', 'native_pipeline_reference')},
            'costs': {'charge_meaning': 'ChargeUsed defaults0 and hasCharge iff<1000; raw setter is unclamped.', 'client_expenditure': 'Client only, warmup>=1 and elapsed%(2+floor(1.5F*EnergyEfficiencyLevel))==0 and noncreative: ChargeUsed=min(ChargeUsed+1,1000); this cadence is separate from server damage cadence.', 'reload': 'First inventory uranium-rod item, shrink1, reset expenditure0; Creative findAmmo EMPTY yet reset branch succeeds; reload attempt returns useFail.', 'solar': METHOD_FACTS['acInventoryTick'][1], 'anvil': anvil['facts']},
            'integration': {'gamma': gcontract, 'xray': {'range': xreport['static_contract']['range'], 'exclusion': xreport['static_contract']['exclusion'], 'damage_status': 'X-Ray changes endpoint/scan geometry; no separate damage/status bonus. Gamma toggles 1.5F/2F requests and amplifier0/4.'}, 'visual_consumers': prior['EXACT-GAMMA-RAY-CAUSAL-1.0.10.json']['visual_consumers'], 'network_boundary': {'senders': ['onUseTick exhausted client branch@165', 'releaseUsing client branch@28'], 'conditional_receiver': 'Historical native handle resolves packet entityId, requires LivingEntity, chooses matching main/offhand ItemStack item identity, checks UpdatesStackTags and nonnull incoming tag, then invokes default updateTagFromServer; default delegates ACCompat.setTag, which removes or sets DataComponents.CUSTOM_DATA.', 'claim': 'CONDITIONAL_CLIENT_INPUT_TAG_WRITE_ONLY', 'authorization': 'NOT_VERIFIED', 'sanitization': 'NOT_VERIFIED', 'replay_protection': 'NOT_VERIFIED', 'codec_and_delivery': 'NOT_VERIFIED'}},
            'validation': {'native_item_methods_dispositioned': 26, 'static_initializer_additional_instructions': 3, 'charge_ammo_subset': {'methods': 8, 'instructions': 168, 'direct_branches': 15}, 'onUseTick': {'instructions': 523, 'direct_branches': 57}, 'whole_provider_discovery': False, 'unaccounted_native_roots': 0, 'physical_qa': 'NOT_TESTED', 'mutating_hook': 'NOT_VERIFIED'},
        },
        'safety': SAFETY,
    }


def verify_seal(actual, expected):
    require(isinstance(expected, dict) and expected.get('claim_scope') == 'STATIC_TECHNICAL_CATALOG_ONLY' and expected.get('safety') == SAFETY, 'unsafe Raygun contract scope or safety drift')
    require(actual == expected, 'Raygun exact consolidated native contract seal drift')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--javap', required=True)
    parser.add_argument('--seal', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        expected = load(args.seal) if args.seal else None
        if expected is not None:
            verify_seal(expected, expected)
        report = audit(args.jar, args.javap)
        if expected is not None:
            verify_seal(report, expected)
        data = canonical(report)
        require(len(data.encode('utf8')) < 140000, 'Raygun bounded contract report budget exceeded')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding='utf8')
        print('PASS: SHA-exact Raygun 1.0.10 consolidated static contract')
        print('methods=26 instructions=1111 direct_branches=107 axes=7')
        print('report_sha256=' + digest(data.encode('utf8')))
        print('STATIC_TECHNICAL_CATALOG_ONLY NO_MUTATION NOT_VERIFIED NOT_TESTED')
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
