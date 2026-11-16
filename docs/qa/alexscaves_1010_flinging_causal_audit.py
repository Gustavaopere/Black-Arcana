#!/usr/bin/env python3
"""Read-only full-method Flinging contract on publisher Alex's Caves 1.0.10.

A bounded disassembly census, not a game simulation, runtime adapter or safe
mutation hook. Historical selected-window evidence remains immutable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, METHOD_LINE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_flinging_probe import audit as historical_audit

ROOT = Path(__file__).resolve().parents[2] / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
BASE = 'com/github/alexmodguy/alexscaves/'
ITEM = BASE + 'server/item/OrtholanceItem.class'
WAVE = BASE + 'server/entity/item/WaveEntity.class'
COMPAT = BASE + 'server/misc/ACCompat.class'
REGISTRY = BASE + 'server/enchantment/ACEnchantmentRegistry.class'
ENCHANT = 'data/alexscaves/enchantment/flinging.json'
TAG = 'data/alexscaves/tags/item/enchantable/ortholance.json'
SEAL = ROOT / 'EXACT-FLINGING-CAUSAL-1.0.10.json'
HISTORY = ROOT / 'EXACT-FLINGING-1.0.10.json'
COMPAT_NAMES = {
    'enchantLevel', 'hurtAndBreakUsedHand', 'hurtAndBreak', 'slotOf',
    'attackDamageBonus', 'lambda$attackDamageBonus$2', 'itemAttributes',
    'useFail', 'useConsume',
}
SELECTIONS = {
    ITEM: None,  # all thirteen declared item methods, including adjacent melee
    WAVE: None,  # all twenty-eight wave methods, including owner/NBT/defaults
    COMPAT: COMPAT_NAMES,
    REGISTRY: {'key', '__class_init__'},
}
RESOURCE_PATHS = (
    ENCHANT, TAG,
    'data/alexscaves/enchantment/tsunami.json',
    'data/alexscaves/enchantment/second_wave.json',
    'data/minecraft/tags/enchantment/in_enchanting_table.json',
    'data/minecraft/tags/enchantment/non_treasure.json',
    'data/minecraft/tags/enchantment/on_random_loot.json',
    'data/minecraft/tags/enchantment/tradeable.json',
    'assets/alexscaves/lang/en_us.json',
    'assets/alexscaves/lang/pt_br.json',
)
EXPECTED_JSON = {
    'description': {'translate': 'enchantment.alexscaves.flinging'},
    'supported_items': '#alexscaves:enchantable/ortholance',
    'weight': 10, 'max_level': 3,
    'min_cost': {'base': 1, 'per_level_above_first': 8},
    'max_cost': {'base': 41, 'per_level_above_first': 10},
    'anvil_cost': 1, 'slots': ['mainhand'],
}
SAFETY = {
    'mutating_hook': 'NOT_VERIFIED', 'physical_qa': 'NOT_TESTED',
    'mutation': 'NO_MUTATION', 'provider_universe_closed': False,
    'effective_displacement': 'NOT_TESTED',
    'accepted_damage_or_spawn': 'NOT_CERTIFIED',
    'pvp_claims_external_callbacks': 'NOT_VERIFIED',
    'runtime_packet_authority': 'NOT_CERTIFIED',
    'datapacks_effective': 'NOT_VERIFIED',
    'mastery_proc_credit': 'NOT_CERTIFIED',
}
CONTRACT = {
    'charge': 'C=clamp(72000-useTime,0,60); only C>0 changes requested velocity',
    'impulse': 'f=0.1F*C+0.1F*F; V9=oldDelta+normalize(view)*(f,0.15F*f,f)',
    'vertical': 'requestedDelta=V9+(0,(onGround?0.2F:0)+0.1F*F,0)',
    'server_gate': 'C>=10 and !isClientSide gate waves, wear and AABB hit iteration; final movement has no local side gate',
    'cost': 'one hurtAndBreakUsedHand(stack,1,actor) request in server C>=10 branch; no separate Flinging debit',
    'geometry': 'B=C/5 integer normal; B=5 with Tsunami; AABB(P,P+V9*B).inflate(1D), before final vertical bonus',
    'target': 'LivingEntity candidates; reject actor-allied, self and failed hasLineOfSight; hurt return discarded; stopRiding follows',
    'damage': 'mobAttack(actor), float attackDamageBonus(stack); F has no independent damage coefficient',
    'waves': 'normal 2*B spawn requests; Second Wave adds 2*max(1,B-1) delayed requests only in normal branch; Tsunami one and skips Second Wave; addFreshEntity return discarded',
    'persistence': 'Wave stores Owner UUID and Lifespan; waiting/scale/yaw/slam and activeWaveTicks not saved by own NBT overrides',
    'ownership': 'Wave owner reference+UUID; getOwner server lookup resolves only LivingEntity; tick/attackEntities use raw owner with no getOwner call; not guaranteed postreload recovery or credit/dedup receipt',
    'cooldown': 'getUseDuration=72000; no dedicated Flinging cooldown set in complete item bodies; external lifecycle unverified',
}
# Semantic pivots are fixed separately from the mutable certificate file.
PIVOT_SPECS = {('com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class', 'OrtholanceItem'): [(13,
                                                                                            'new',
                                                                                            'class '
                                                                                            'net/minecraft/world/entity/ai/attributes/AttributeModifier'),
                                                                                           (16, 'dup', '')],
 ('com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class', 'getUseDuration'): [(0, 'ldc', 'int 72000'),
                                                                                           (2, 'ireturn', '')],
 ('com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class', 'releaseUsing'): [(3,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'getUseDuration:(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I'),
                                                                                         (8, 'isub', ''),
                                                                                         (10, 'bipush', '60'),
                                                                                         (12,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'net/minecraft/util/Mth.clamp:(III)I'),
                                                                                         (18,
                                                                                          'getstatic',
                                                                                          'Field '
                                                                                          'com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.FLINGING:Lnet/minecraft/resources/ResourceKey;'),
                                                                                         (21,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'com/github/alexmodguy/alexscaves/server/misc/ACCompat.enchantLevel:(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I'),
                                                                                         (43, 'iload', '5'),
                                                                                         (45, 'ifle', '869'),
                                                                                         (48, 'ldc', 'float 0.1f'),
                                                                                         (53, 'fmul', ''),
                                                                                         (54, 'iload', '6'),
                                                                                         (57, 'ldc', 'float 0.1f'),
                                                                                         (59, 'fmul', ''),
                                                                                         (60, 'fadd', ''),
                                                                                         (64,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.getDeltaMovement:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (69,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.getViewVector:(F)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (72,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.normalize:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (75, 'fload', '8'),
                                                                                         (80, 'ldc', 'float 0.15f'),
                                                                                         (82, 'fmul', ''),
                                                                                         (87,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.multiply:(DDD)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (90,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.add:(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (93, 'astore', '9'),
                                                                                         (95, 'iload', '5'),
                                                                                         (97, 'bipush', '10'),
                                                                                         (99, 'if_icmplt', '836'),
                                                                                         (103,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/level/Level.isClientSide:()Z'),
                                                                                         (106, 'ifne', '836'),
                                                                                         (135,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'com/github/alexmodguy/alexscaves/server/misc/ACCompat.hurtAndBreakUsedHand:(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;)V'),
                                                                                         (138, 'iload', '5'),
                                                                                         (140, 'iconst_5', ''),
                                                                                         (141, 'idiv', ''),
                                                                                         (142, 'istore', '10'),
                                                                                         (146, 'ifeq', '247'),
                                                                                         (149, 'iconst_5', ''),
                                                                                         (150, 'istore', '10'),
                                                                                         (240,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                         (243, 'pop', ''),
                                                                                         (244, 'goto', '705'),
                                                                                         (460,
                                                                                          'getstatic',
                                                                                          'Field '
                                                                                          'com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.SECOND_WAVE:Lnet/minecraft/resources/ResourceKey;'),
                                                                                         (463,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'com/github/alexmodguy/alexscaves/server/misc/ACCompat.enchantLevel:(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I'),
                                                                                         (466, 'ifle', '705'),
                                                                                         (469, 'iconst_1', ''),
                                                                                         (470, 'iload', '10'),
                                                                                         (472, 'iconst_1', ''),
                                                                                         (473, 'isub', ''),
                                                                                         (474,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'java/lang/Math.max:(II)I'),
                                                                                         (477, 'istore', '11'),
                                                                                         (484, 'iload', '11'),
                                                                                         (486, 'if_icmpge', '705'),
                                                                                         (610,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                         (613, 'pop', ''),
                                                                                         (695,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                         (698, 'pop', ''),
                                                                                         (705,
                                                                                          'new',
                                                                                          'class '
                                                                                          'net/minecraft/world/phys/AABB'),
                                                                                         (710,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.position:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (714,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.position:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (717, 'aload', '9'),
                                                                                         (719, 'iload', '10'),
                                                                                         (721, 'i2d', ''),
                                                                                         (722,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.scale:(D)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (725,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.add:(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (728,
                                                                                          'invokespecial',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/AABB."<init>":(Lnet/minecraft/world/phys/Vec3;Lnet/minecraft/world/phys/Vec3;)V'),
                                                                                         (731, 'dconst_1', ''),
                                                                                         (732,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/AABB.inflate:(D)Lnet/minecraft/world/phys/AABB;'),
                                                                                         (742,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/damagesource/DamageSources.mobAttack:(Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/damagesource/DamageSource;'),
                                                                                         (748,
                                                                                          'invokestatic',
                                                                                          'Method '
                                                                                          'com/github/alexmodguy/alexscaves/server/misc/ACCompat.attackDamageBonus:(Lnet/minecraft/world/item/ItemStack;)D'),
                                                                                         (758,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/level/Level.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;)Ljava/util/List;'),
                                                                                         (793,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                         (796, 'ifne', '833'),
                                                                                         (802,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.equals:(Ljava/lang/Object;)Z'),
                                                                                         (805, 'ifne', '833'),
                                                                                         (811,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.hasLineOfSight:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                         (814, 'ifeq', '833'),
                                                                                         (824,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.hurt:(Lnet/minecraft/world/damagesource/DamageSource;F)Z'),
                                                                                         (827, 'pop', ''),
                                                                                         (830,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.stopRiding:()V'),
                                                                                         (841,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.onGround:()Z'),
                                                                                         (844, 'ifeq', '853'),
                                                                                         (847, 'ldc_w', 'float 0.2f'),
                                                                                         (850, 'goto', '854'),
                                                                                         (853, 'fconst_0', ''),
                                                                                         (854, 'iload', '6'),
                                                                                         (857, 'ldc', 'float 0.1f'),
                                                                                         (859, 'fmul', ''),
                                                                                         (860, 'fadd', ''),
                                                                                         (863,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/phys/Vec3.add:(DDD)Lnet/minecraft/world/phys/Vec3;'),
                                                                                         (866,
                                                                                          'invokevirtual',
                                                                                          'Method '
                                                                                          'net/minecraft/world/entity/LivingEntity.setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V')],
 ('com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class', 'use'): [(9,
                                                                                 'invokevirtual',
                                                                                 'Method '
                                                                                 'net/minecraft/world/item/ItemStack.getDamageValue:()I'),
                                                                                (14,
                                                                                 'invokevirtual',
                                                                                 'Method '
                                                                                 'net/minecraft/world/item/ItemStack.getMaxDamage:()I'),
                                                                                (17, 'iconst_1', ''),
                                                                                (18, 'isub', ''),
                                                                                (19, 'if_icmplt', '28'),
                                                                                (24,
                                                                                 'invokestatic',
                                                                                 'Method '
                                                                                 'com/github/alexmodguy/alexscaves/server/misc/ACCompat.useFail:(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/InteractionResultHolder;'),
                                                                                (30,
                                                                                 'invokevirtual',
                                                                                 'Method '
                                                                                 'net/minecraft/world/entity/player/Player.startUsingItem:(Lnet/minecraft/world/InteractionHand;)V'),
                                                                                (35,
                                                                                 'invokestatic',
                                                                                 'Method '
                                                                                 'com/github/alexmodguy/alexscaves/server/misc/ACCompat.useConsume:(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/InteractionResultHolder;')],
 ('com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class', 'mineBlock'): [(0, 'aload_3', ''),
                                                                                      (1, 'aload_2', ''),
                                                                                      (2, 'aload', '4'),
                                                                                      (4,
                                                                                       'invokevirtual',
                                                                                       'Method '
                                                                                       'net/minecraft/world/level/block/state/BlockState.getDestroySpeed:(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;)F'),
                                                                                      (7, 'f2d', ''),
                                                                                      (8, 'dconst_0', ''),
                                                                                      (9, 'dcmpl', ''),
                                                                                      (10, 'ifeq', '23'),
                                                                                      (13, 'aload_1', ''),
                                                                                      (14, 'iconst_2', ''),
                                                                                      (15, 'aload', '5'),
                                                                                      (17,
                                                                                       'getstatic',
                                                                                       'Field '
                                                                                       'net/minecraft/world/entity/EquipmentSlot.MAINHAND:Lnet/minecraft/world/entity/EquipmentSlot;'),
                                                                                      (20,
                                                                                       'invokestatic',
                                                                                       'Method '
                                                                                       'com/github/alexmodguy/alexscaves/server/misc/ACCompat.hurtAndBreak:(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/EquipmentSlot;)V'),
                                                                                      (23, 'iconst_1', ''),
                                                                                      (24, 'ireturn', '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'setOwner'): [(0, 'aload_0', ''),
                                                                                        (1, 'aload_1', ''),
                                                                                        (2,
                                                                                         'putfield',
                                                                                         'Field '
                                                                                         'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                        (5, 'aload_0', ''),
                                                                                        (6, 'aload_1', ''),
                                                                                        (7, 'ifnonnull', '14'),
                                                                                        (10, 'aconst_null', ''),
                                                                                        (11, 'goto', '18'),
                                                                                        (14, 'aload_1', ''),
                                                                                        (15,
                                                                                         'invokevirtual',
                                                                                         'Method '
                                                                                         'net/minecraft/world/entity/LivingEntity.getUUID:()Ljava/util/UUID;'),
                                                                                        (18,
                                                                                         'putfield',
                                                                                         'Field '
                                                                                         'ownerUUID:Ljava/util/UUID;'),
                                                                                        (21, 'return', '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'getOwner'): [(1,
                                                                                         'getfield',
                                                                                         'Field '
                                                                                         'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                        (4, 'ifnonnull', '54'),
                                                                                        (8,
                                                                                         'getfield',
                                                                                         'Field '
                                                                                         'ownerUUID:Ljava/util/UUID;'),
                                                                                        (11, 'ifnull', '54'),
                                                                                        (15,
                                                                                         'invokevirtual',
                                                                                         'Method '
                                                                                         'level:()Lnet/minecraft/world/level/Level;'),
                                                                                        (21, 'ifeq', '54'),
                                                                                        (25,
                                                                                         'invokevirtual',
                                                                                         'Method '
                                                                                         'level:()Lnet/minecraft/world/level/Level;'),
                                                                                        (32,
                                                                                         'getfield',
                                                                                         'Field '
                                                                                         'ownerUUID:Ljava/util/UUID;'),
                                                                                        (35,
                                                                                         'invokevirtual',
                                                                                         'Method '
                                                                                         'net/minecraft/server/level/ServerLevel.getEntity:(Ljava/util/UUID;)Lnet/minecraft/world/entity/Entity;'),
                                                                                        (43, 'ifeq', '54'),
                                                                                        (51,
                                                                                         'putfield',
                                                                                         'Field '
                                                                                         'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                        (55,
                                                                                         'getfield',
                                                                                         'Field '
                                                                                         'owner:Lnet/minecraft/world/entity/LivingEntity;')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'defineSynchedData'): [(1,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'SLAMMING:Lnet/minecraft/network/syncher/EntityDataAccessor;'),
                                                                                                 (4, 'iconst_0', ''),
                                                                                                 (13,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'LIFESPAN:Lnet/minecraft/network/syncher/EntityDataAccessor;'),
                                                                                                 (16, 'bipush', '10'),
                                                                                                 (26,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'WAITING_TICKS:Lnet/minecraft/network/syncher/EntityDataAccessor;'),
                                                                                                 (29, 'iconst_0', ''),
                                                                                                 (38,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'Y_ROT:Lnet/minecraft/network/syncher/EntityDataAccessor;'),
                                                                                                 (41, 'fconst_0', ''),
                                                                                                 (50,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'WAVE_SCALE:Lnet/minecraft/network/syncher/EntityDataAccessor;'),
                                                                                                 (53, 'fconst_1', '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'readAdditionalSaveData'): [(0,
                                                                                                       'aload_1',
                                                                                                       ''),
                                                                                                      (1,
                                                                                                       'ldc',
                                                                                                       'String Owner'),
                                                                                                      (3,
                                                                                                       'invokestatic',
                                                                                                       'Method '
                                                                                                       'com/github/alexmodguy/alexscaves/server/misc/ACCompat.hasUUID:(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)Z'),
                                                                                                      (6, 'ifeq', '19'),
                                                                                                      (9,
                                                                                                       'aload_0',
                                                                                                       ''),
                                                                                                      (10,
                                                                                                       'aload_1',
                                                                                                       ''),
                                                                                                      (11,
                                                                                                       'ldc',
                                                                                                       'String Owner'),
                                                                                                      (13,
                                                                                                       'invokestatic',
                                                                                                       'Method '
                                                                                                       'com/github/alexmodguy/alexscaves/server/misc/ACCompat.getUUID:(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)Ljava/util/UUID;'),
                                                                                                      (16,
                                                                                                       'putfield',
                                                                                                       'Field '
                                                                                                       'ownerUUID:Ljava/util/UUID;'),
                                                                                                      (19,
                                                                                                       'aload_1',
                                                                                                       ''),
                                                                                                      (20,
                                                                                                       'ldc',
                                                                                                       'String '
                                                                                                       'Lifespan'),
                                                                                                      (22,
                                                                                                       'invokevirtual',
                                                                                                       'Method '
                                                                                                       'net/minecraft/nbt/CompoundTag.contains:(Ljava/lang/String;)Z'),
                                                                                                      (25,
                                                                                                       'ifeq',
                                                                                                       '38'),
                                                                                                      (28,
                                                                                                       'aload_0',
                                                                                                       ''),
                                                                                                      (29,
                                                                                                       'aload_1',
                                                                                                       ''),
                                                                                                      (30,
                                                                                                       'ldc',
                                                                                                       'String '
                                                                                                       'Lifespan'),
                                                                                                      (32,
                                                                                                       'invokestatic',
                                                                                                       'Method '
                                                                                                       'com/github/alexmodguy/alexscaves/server/misc/ACCompat.getInt:(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)I'),
                                                                                                      (35,
                                                                                                       'invokevirtual',
                                                                                                       'Method '
                                                                                                       'setLifespan:(I)V'),
                                                                                                      (38,
                                                                                                       'return',
                                                                                                       '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'addAdditionalSaveData'): [(0, 'aload_0', ''),
                                                                                                     (1,
                                                                                                      'getfield',
                                                                                                      'Field '
                                                                                                      'ownerUUID:Ljava/util/UUID;'),
                                                                                                     (4,
                                                                                                      'ifnull',
                                                                                                      '17'),
                                                                                                     (7, 'aload_1', ''),
                                                                                                     (8,
                                                                                                      'ldc',
                                                                                                      'String Owner'),
                                                                                                     (10,
                                                                                                      'aload_0',
                                                                                                      ''),
                                                                                                     (11,
                                                                                                      'getfield',
                                                                                                      'Field '
                                                                                                      'ownerUUID:Ljava/util/UUID;'),
                                                                                                     (14,
                                                                                                      'invokestatic',
                                                                                                      'Method '
                                                                                                      'com/github/alexmodguy/alexscaves/server/misc/ACCompat.putUUID:(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;Ljava/util/UUID;)V'),
                                                                                                     (17,
                                                                                                      'aload_1',
                                                                                                      ''),
                                                                                                     (18,
                                                                                                      'ldc',
                                                                                                      'String '
                                                                                                      'Lifespan'),
                                                                                                     (20,
                                                                                                      'aload_0',
                                                                                                      ''),
                                                                                                     (21,
                                                                                                      'invokevirtual',
                                                                                                      'Method '
                                                                                                      'getLifespan:()I'),
                                                                                                     (24,
                                                                                                      'invokevirtual',
                                                                                                      'Method '
                                                                                                      'net/minecraft/nbt/CompoundTag.putInt:(Ljava/lang/String;I)V'),
                                                                                                     (27,
                                                                                                      'return',
                                                                                                      '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'tick'): [(1,
                                                                                     'invokespecial',
                                                                                     'Method '
                                                                                     'net/minecraft/world/entity/Entity.tick:()V'),
                                                                                    (6,
                                                                                     'getfield',
                                                                                     'Field slamProgress:F'),
                                                                                    (9,
                                                                                     'putfield',
                                                                                     'Field prevSlamProgress:F'),
                                                                                    (13,
                                                                                     'invokevirtual',
                                                                                     'Method getWaitingTicks:()I'),
                                                                                    (16, 'ifle', '45'),
                                                                                    (20,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'level:()Lnet/minecraft/world/level/Level;'),
                                                                                    (23,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/level/Level.isClientSide:()Z'),
                                                                                    (26, 'ifne', '39'),
                                                                                    (31,
                                                                                     'invokevirtual',
                                                                                     'Method getWaitingTicks:()I'),
                                                                                    (36,
                                                                                     'invokevirtual',
                                                                                     'Method setWaitingTicks:(I)V'),
                                                                                    (41,
                                                                                     'invokevirtual',
                                                                                     'Method setInvisible:(Z)V'),
                                                                                    (46,
                                                                                     'invokevirtual',
                                                                                     'Method isInvisible:()Z'),
                                                                                    (49, 'ifeq', '57'),
                                                                                    (54,
                                                                                     'invokevirtual',
                                                                                     'Method setInvisible:(Z)V'),
                                                                                    (58,
                                                                                     'invokevirtual',
                                                                                     'Method isSlamming:()Z'),
                                                                                    (61, 'ifeq', '84'),
                                                                                    (65,
                                                                                     'getfield',
                                                                                     'Field slamProgress:F'),
                                                                                    (71, 'ifge', '84'),
                                                                                    (76,
                                                                                     'getfield',
                                                                                     'Field slamProgress:F'),
                                                                                    (81,
                                                                                     'putfield',
                                                                                     'Field slamProgress:F'),
                                                                                    (85,
                                                                                     'invokevirtual',
                                                                                     'Method isSlamming:()Z'),
                                                                                    (88, 'ifeq', '105'),
                                                                                    (92,
                                                                                     'getfield',
                                                                                     'Field slamProgress:F'),
                                                                                    (98, 'ifne', '105'),
                                                                                    (102,
                                                                                     'invokevirtual',
                                                                                     'Method discard:()V'),
                                                                                    (106,
                                                                                     'invokevirtual',
                                                                                     'Method isNoGravity:()Z'),
                                                                                    (109, 'ifne', '135'),
                                                                                    (113,
                                                                                     'invokestatic',
                                                                                     'Method '
                                                                                     'com/github/alexmodguy/alexscaves/server/misc/ACCompat.isInWaterOrBubble:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                    (116, 'ifne', '135'),
                                                                                    (121,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'getDeltaMovement:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (129,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.add:(DDD)Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (132,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V'),
                                                                                    (136,
                                                                                     'getfield',
                                                                                     'Field activeWaveTicks:I'),
                                                                                    (144,
                                                                                     'invokestatic',
                                                                                     'Method java/lang/Math.min:(FF)F'),
                                                                                    (162,
                                                                                     'invokespecial',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3."<init>":(DDD)V'),
                                                                                    (166,
                                                                                     'invokevirtual',
                                                                                     'Method getYRot:()F'),
                                                                                    (171,
                                                                                     'invokestatic',
                                                                                     'Method '
                                                                                     'java/lang/Math.toRadians:(D)D'),
                                                                                    (175,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.yRot:(F)Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (180,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'level:()Lnet/minecraft/world/level/Level;'),
                                                                                    (183,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/level/Level.isClientSide:()Z'),
                                                                                    (186, 'ifeq', '486'),
                                                                                    (190, 'getfield', 'Field lSteps:I'),
                                                                                    (193, 'ifle', '321'),
                                                                                    (197,
                                                                                     'invokevirtual',
                                                                                     'Method getX:()D'),
                                                                                    (201, 'getfield', 'Field lx:D'),
                                                                                    (205,
                                                                                     'invokevirtual',
                                                                                     'Method getX:()D'),
                                                                                    (210, 'getfield', 'Field lSteps:I'),
                                                                                    (218,
                                                                                     'invokevirtual',
                                                                                     'Method getY:()D'),
                                                                                    (222, 'getfield', 'Field ly:D'),
                                                                                    (226,
                                                                                     'invokevirtual',
                                                                                     'Method getY:()D'),
                                                                                    (231, 'getfield', 'Field lSteps:I'),
                                                                                    (240,
                                                                                     'invokevirtual',
                                                                                     'Method getZ:()D'),
                                                                                    (244, 'getfield', 'Field lz:D'),
                                                                                    (248,
                                                                                     'invokevirtual',
                                                                                     'Method getZ:()D'),
                                                                                    (253, 'getfield', 'Field lSteps:I'),
                                                                                    (263, 'getfield', 'Field lyr:D'),
                                                                                    (267,
                                                                                     'invokestatic',
                                                                                     'Method '
                                                                                     'net/minecraft/util/Mth.wrapDegrees:(F)F'),
                                                                                    (270,
                                                                                     'invokevirtual',
                                                                                     'Method setYRot:(F)V'),
                                                                                    (275,
                                                                                     'invokevirtual',
                                                                                     'Method getXRot:()F'),
                                                                                    (279, 'getfield', 'Field lxr:D'),
                                                                                    (283,
                                                                                     'invokevirtual',
                                                                                     'Method getXRot:()F'),
                                                                                    (290, 'getfield', 'Field lSteps:I'),
                                                                                    (296,
                                                                                     'invokevirtual',
                                                                                     'Method setXRot:(F)V'),
                                                                                    (301, 'getfield', 'Field lSteps:I'),
                                                                                    (306, 'putfield', 'Field lSteps:I'),
                                                                                    (315,
                                                                                     'invokevirtual',
                                                                                     'Method setPos:(DDD)V'),
                                                                                    (322,
                                                                                     'invokevirtual',
                                                                                     'Method reapplyPosition:()V'),
                                                                                    (330,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (334, 'ifge', '483'),
                                                                                    (343, 'if_icmpgt', '477'),
                                                                                    (358,
                                                                                     'getfield',
                                                                                     'Field '
                                                                                     'random:Lnet/minecraft/util/RandomSource;'),
                                                                                    (361,
                                                                                     'invokeinterface',
                                                                                     'InterfaceMethod '
                                                                                     'net/minecraft/util/RandomSource.nextFloat:()F'),
                                                                                    (382,
                                                                                     'getfield',
                                                                                     'Field '
                                                                                     'random:Lnet/minecraft/util/RandomSource;'),
                                                                                    (385,
                                                                                     'invokeinterface',
                                                                                     'InterfaceMethod '
                                                                                     'net/minecraft/util/RandomSource.nextFloat:()F'),
                                                                                    (396,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (410,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (414,
                                                                                     'getstatic',
                                                                                     'Field '
                                                                                     'com/github/alexmodguy/alexscaves/client/particle/ACParticleRegistry.WATER_FOAM:Ljava/util/function/Supplier;'),
                                                                                    (417,
                                                                                     'invokeinterface',
                                                                                     'InterfaceMethod '
                                                                                     'java/util/function/Supplier.get:()Ljava/lang/Object;'),
                                                                                    (425,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'spawnParticleAt:(FFFLnet/minecraft/core/particles/ParticleOptions;)V'),
                                                                                    (433,
                                                                                     'getfield',
                                                                                     'Field '
                                                                                     'random:Lnet/minecraft/util/RandomSource;'),
                                                                                    (436,
                                                                                     'invokeinterface',
                                                                                     'InterfaceMethod '
                                                                                     'net/minecraft/util/RandomSource.nextFloat:()F'),
                                                                                    (447,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (461,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (465,
                                                                                     'getstatic',
                                                                                     'Field '
                                                                                     'net/minecraft/core/particles/ParticleTypes.SPLASH:Lnet/minecraft/core/particles/SimpleParticleType;'),
                                                                                    (468,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'spawnParticleAt:(FFFLnet/minecraft/core/particles/ParticleOptions;)V'),
                                                                                    (487,
                                                                                     'invokevirtual',
                                                                                     'Method reapplyPosition:()V'),
                                                                                    (492,
                                                                                     'invokevirtual',
                                                                                     'Method getYRot:()F'),
                                                                                    (496,
                                                                                     'invokevirtual',
                                                                                     'Method getXRot:()F'),
                                                                                    (499,
                                                                                     'invokevirtual',
                                                                                     'Method setRot:(FF)V'),
                                                                                    (503,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'level:()Lnet/minecraft/world/level/Level;'),
                                                                                    (506,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/level/Level.isClientSide:()Z'),
                                                                                    (509, 'ifne', '530'),
                                                                                    (515,
                                                                                     'invokevirtual',
                                                                                     'Method getSlamAmount:(F)F'),
                                                                                    (523,
                                                                                     'invokevirtual',
                                                                                     'Method getWaveScale:()F'),
                                                                                    (527,
                                                                                     'invokevirtual',
                                                                                     'Method attackEntities:(F)V'),
                                                                                    (531,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'getDeltaMovement:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (537,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.scale:(D)Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (541,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.add:(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (546,
                                                                                     'getstatic',
                                                                                     'Field '
                                                                                     'net/minecraft/world/entity/MoverType.SELF:Lnet/minecraft/world/entity/MoverType;'),
                                                                                    (550,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'move:(Lnet/minecraft/world/entity/MoverType;Lnet/minecraft/world/phys/Vec3;)V'),
                                                                                    (564,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.multiply:(DDD)Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (567,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V'),
                                                                                    (571,
                                                                                     'getfield',
                                                                                     'Field activeWaveTicks:I'),
                                                                                    (575,
                                                                                     'invokevirtual',
                                                                                     'Method getLifespan:()I'),
                                                                                    (578, 'if_icmpgt', '604'),
                                                                                    (582,
                                                                                     'getfield',
                                                                                     'Field activeWaveTicks:I'),
                                                                                    (587, 'if_icmple', '609'),
                                                                                    (591,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'getDeltaMovement:()Lnet/minecraft/world/phys/Vec3;'),
                                                                                    (594,
                                                                                     'invokevirtual',
                                                                                     'Method '
                                                                                     'net/minecraft/world/phys/Vec3.horizontalDistance:()D'),
                                                                                    (601, 'ifge', '609'),
                                                                                    (606,
                                                                                     'invokevirtual',
                                                                                     'Method setSlamming:(Z)V'),
                                                                                    (611,
                                                                                     'getfield',
                                                                                     'Field activeWaveTicks:I'),
                                                                                    (616,
                                                                                     'putfield',
                                                                                     'Field activeWaveTicks:I')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'attackEntities'): [(0, 'aload_0', ''),
                                                                                              (1,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'getBoundingBox:()Lnet/minecraft/world/phys/AABB;'),
                                                                                              (4,
                                                                                               'ldc2_w',
                                                                                               'double 0.5d'),
                                                                                              (7,
                                                                                               'ldc2_w',
                                                                                               'double 0.5d'),
                                                                                              (10,
                                                                                               'ldc2_w',
                                                                                               'double 0.5d'),
                                                                                              (13,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;'),
                                                                                              (16, 'astore_2', ''),
                                                                                              (17, 'aload_0', ''),
                                                                                              (18,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'damageSources:()Lnet/minecraft/world/damagesource/DamageSources;'),
                                                                                              (21, 'aload_0', ''),
                                                                                              (22, 'aload_0', ''),
                                                                                              (23,
                                                                                               'getfield',
                                                                                               'Field '
                                                                                               'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                              (26,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/damagesource/DamageSources.mobProjectile:(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/damagesource/DamageSource;'),
                                                                                              (29, 'astore_3', ''),
                                                                                              (30, 'aload_0', ''),
                                                                                              (31,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'level:()Lnet/minecraft/world/level/Level;'),
                                                                                              (34,
                                                                                               'ldc',
                                                                                               'class '
                                                                                               'net/minecraft/world/entity/LivingEntity'),
                                                                                              (36, 'aload_2', ''),
                                                                                              (37,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/level/Level.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;)Ljava/util/List;'),
                                                                                              (40,
                                                                                               'invokeinterface',
                                                                                               'InterfaceMethod '
                                                                                               'java/util/List.iterator:()Ljava/util/Iterator;'),
                                                                                              (45, 'astore', '4'),
                                                                                              (47, 'aload', '4'),
                                                                                              (49,
                                                                                               'invokeinterface',
                                                                                               'InterfaceMethod '
                                                                                               'java/util/Iterator.hasNext:()Z'),
                                                                                              (54, 'ifeq', '175'),
                                                                                              (57, 'aload', '4'),
                                                                                              (59,
                                                                                               'invokeinterface',
                                                                                               'InterfaceMethod '
                                                                                               'java/util/Iterator.next:()Ljava/lang/Object;'),
                                                                                              (64,
                                                                                               'checkcast',
                                                                                               'class '
                                                                                               'net/minecraft/world/entity/LivingEntity'),
                                                                                              (67, 'astore', '5'),
                                                                                              (69, 'aload_0', ''),
                                                                                              (70, 'aload', '5'),
                                                                                              (72,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                              (75, 'ifne', '172'),
                                                                                              (78, 'aload', '5'),
                                                                                              (80,
                                                                                               'instanceof',
                                                                                               'class '
                                                                                               'com/github/alexmodguy/alexscaves/server/entity/living/DeepOneBaseEntity'),
                                                                                              (83, 'ifne', '172'),
                                                                                              (86, 'aload_0', ''),
                                                                                              (87,
                                                                                               'getfield',
                                                                                               'Field '
                                                                                               'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                              (90, 'ifnull', '117'),
                                                                                              (93, 'aload_0', ''),
                                                                                              (94,
                                                                                               'getfield',
                                                                                               'Field '
                                                                                               'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                              (97, 'aload', '5'),
                                                                                              (99,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/entity/LivingEntity.equals:(Ljava/lang/Object;)Z'),
                                                                                              (102, 'ifne', '172'),
                                                                                              (105, 'aload_0', ''),
                                                                                              (106,
                                                                                               'getfield',
                                                                                               'Field '
                                                                                               'owner:Lnet/minecraft/world/entity/LivingEntity;'),
                                                                                              (109, 'aload', '5'),
                                                                                              (111,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z'),
                                                                                              (114, 'ifne', '172'),
                                                                                              (117, 'aload', '5'),
                                                                                              (119, 'aload_3', ''),
                                                                                              (120, 'fload_1', ''),
                                                                                              (121, 'fconst_1', ''),
                                                                                              (122, 'fadd', ''),
                                                                                              (123,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'net/minecraft/world/entity/LivingEntity.hurt:(Lnet/minecraft/world/damagesource/DamageSource;F)Z'),
                                                                                              (126, 'pop', ''),
                                                                                              (127, 'aload_0', ''),
                                                                                              (128, 'iconst_1', ''),
                                                                                              (129,
                                                                                               'invokevirtual',
                                                                                               'Method '
                                                                                               'setSlamming:(Z)V'),
                                                                                              (132, 'aload', '5'),
                                                                                              (134,
                                                                                               'ldc2_w',
                                                                                               'double 0.1d'),
                                                                                              (137,
                                                                                               'ldc2_w',
                                                                                               'double 0.5d'),
                                                                                              (140, 'fload_1', ''),
                                                                                              (141, 'f2d', ''),
                                                                                              (142, 'dmul', ''),
                                                                                              (143, 'dadd', ''),
                                                                                              (144, 'aload_0', ''),
                                                                                              (145,
                                                                                               'invokevirtual',
                                                                                               'Method getYRot:()F'),
                                                                                              (148,
                                                                                               'ldc_w',
                                                                                               'float 0.017453292f'),
                                                                                              (151, 'fmul', ''),
                                                                                              (152,
                                                                                               'invokestatic',
                                                                                               'Method '
                                                                                               'net/minecraft/util/Mth.sin:(F)F'),
                                                                                              (155, 'f2d', ''),
                                                                                              (156, 'aload_0', ''),
                                                                                              (157,
                                                                                               'invokevirtual',
                                                                                               'Method getYRot:()F'),
                                                                                              (160,
                                                                                               'ldc_w',
                                                                                               'float 0.017453292f'),
                                                                                              (163, 'fmul', ''),
                                                                                              (164,
                                                                                               'invokestatic',
                                                                                               'Method '
                                                                                               'net/minecraft/util/Mth.cos:(F)F'),
                                                                                              (167, 'fneg', ''),
                                                                                              (168, 'f2d', ''),
                                                                                              (169,
                                                                                               'invokestatic',
                                                                                               'Method '
                                                                                               'com/github/alexmodguy/alexscaves/server/misc/ACCompat.knockback:(Lnet/minecraft/world/entity/LivingEntity;DDD)V'),
                                                                                              (172, 'goto', '47'),
                                                                                              (175, 'return', '')],
 ('com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class', 'getDimensions'): [(0, 'aload_0', ''),
                                                                                             (1, 'aload_1', ''),
                                                                                             (2,
                                                                                              'invokespecial',
                                                                                              'Method '
                                                                                              'net/minecraft/world/entity/Entity.getDimensions:(Lnet/minecraft/world/entity/Pose;)Lnet/minecraft/world/entity/EntityDimensions;'),
                                                                                             (5, 'aload_0', ''),
                                                                                             (6,
                                                                                              'invokevirtual',
                                                                                              'Method '
                                                                                              'getWaveScale:()F'),
                                                                                             (9,
                                                                                              'invokevirtual',
                                                                                              'Method '
                                                                                              'net/minecraft/world/entity/EntityDimensions.scale:(F)Lnet/minecraft/world/entity/EntityDimensions;'),
                                                                                             (12, 'areturn', '')],
 ('com/github/alexmodguy/alexscaves/server/misc/ACCompat.class', 'hurtAndBreakUsedHand'): [(0, 'aload_0', ''),
                                                                                           (1, 'iload_1', ''),
                                                                                           (2, 'aload_2', ''),
                                                                                           (3, 'aload_2', ''),
                                                                                           (4,
                                                                                            'invokevirtual',
                                                                                            'Method '
                                                                                            'net/minecraft/world/entity/LivingEntity.getUsedItemHand:()Lnet/minecraft/world/InteractionHand;'),
                                                                                           (7,
                                                                                            'invokestatic',
                                                                                            'Method '
                                                                                            'slotOf:(Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/entity/EquipmentSlot;'),
                                                                                           (10,
                                                                                            'invokevirtual',
                                                                                            'Method '
                                                                                            'net/minecraft/world/item/ItemStack.hurtAndBreak:(ILnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/EquipmentSlot;)V'),
                                                                                           (13, 'return', '')],
 ('com/github/alexmodguy/alexscaves/server/misc/ACCompat.class', 'slotOf'): [(0, 'aload_0', ''),
                                                                             (1,
                                                                              'getstatic',
                                                                              'Field '
                                                                              'net/minecraft/world/InteractionHand.MAIN_HAND:Lnet/minecraft/world/InteractionHand;'),
                                                                             (4, 'if_acmpne', '13'),
                                                                             (7,
                                                                              'getstatic',
                                                                              'Field '
                                                                              'net/minecraft/world/entity/EquipmentSlot.MAINHAND:Lnet/minecraft/world/entity/EquipmentSlot;'),
                                                                             (10, 'goto', '16'),
                                                                             (13,
                                                                              'getstatic',
                                                                              'Field '
                                                                              'net/minecraft/world/entity/EquipmentSlot.OFFHAND:Lnet/minecraft/world/entity/EquipmentSlot;'),
                                                                             (16, 'areturn', '')],
 ('com/github/alexmodguy/alexscaves/server/misc/ACCompat.class', 'enchantLevel'): [(1,
                                                                                    'invokevirtual',
                                                                                    'Method '
                                                                                    'net/minecraft/world/item/ItemStack.getEnchantments:()Lnet/minecraft/world/item/enchantment/ItemEnchantments;'),
                                                                                   (4,
                                                                                    'invokevirtual',
                                                                                    'Method '
                                                                                    'net/minecraft/world/item/enchantment/ItemEnchantments.entrySet:()Ljava/util/Set;'),
                                                                                   (7,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'java/util/Set.iterator:()Ljava/util/Iterator;'),
                                                                                   (14,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'java/util/Iterator.hasNext:()Z'),
                                                                                   (19, 'ifeq', '60'),
                                                                                   (23,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'java/util/Iterator.next:()Ljava/lang/Object;'),
                                                                                   (33,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'it/unimi/dsi/fastutil/objects/Object2IntMap$Entry.getKey:()Ljava/lang/Object;'),
                                                                                   (42,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'net/minecraft/core/Holder.is:(Lnet/minecraft/resources/ResourceKey;)Z'),
                                                                                   (47, 'ifeq', '57'),
                                                                                   (51,
                                                                                    'invokeinterface',
                                                                                    'InterfaceMethod '
                                                                                    'it/unimi/dsi/fastutil/objects/Object2IntMap$Entry.getIntValue:()I')],
 ('com/github/alexmodguy/alexscaves/server/misc/ACCompat.class', 'attackDamageBonus'): [(0, 'iconst_1', ''),
                                                                                        (1, 'newarray', 'double'),
                                                                                        (3, 'astore_1', ''),
                                                                                        (4, 'aload_0', ''),
                                                                                        (5,
                                                                                         'getstatic',
                                                                                         'Field '
                                                                                         'net/minecraft/world/entity/EquipmentSlot.MAINHAND:Lnet/minecraft/world/entity/EquipmentSlot;'),
                                                                                        (8, 'aload_1', ''),
                                                                                        (9,
                                                                                         'invokedynamic',
                                                                                         'InvokeDynamic '
                                                                                         '#2:accept:([D)Ljava/util/function/BiConsumer;'),
                                                                                        (14,
                                                                                         'invokevirtual',
                                                                                         'Method '
                                                                                         'net/minecraft/world/item/ItemStack.forEachModifier:(Lnet/minecraft/world/entity/EquipmentSlot;Ljava/util/function/BiConsumer;)V'),
                                                                                        (17, 'aload_1', ''),
                                                                                        (18, 'iconst_0', ''),
                                                                                        (19, 'daload', ''),
                                                                                        (20, 'dreturn', '')],
 ('com/github/alexmodguy/alexscaves/server/misc/ACCompat.class', 'lambda$attackDamageBonus$2'): [(0, 'aload_1', ''),
                                                                                                 (1,
                                                                                                  'invokeinterface',
                                                                                                  'InterfaceMethod '
                                                                                                  'net/minecraft/core/Holder.value:()Ljava/lang/Object;'),
                                                                                                 (6,
                                                                                                  'getstatic',
                                                                                                  'Field '
                                                                                                  'net/minecraft/world/entity/ai/attributes/Attributes.ATTACK_DAMAGE:Lnet/minecraft/core/Holder;'),
                                                                                                 (9,
                                                                                                  'invokeinterface',
                                                                                                  'InterfaceMethod '
                                                                                                  'net/minecraft/core/Holder.value:()Ljava/lang/Object;'),
                                                                                                 (14,
                                                                                                  'if_acmpne',
                                                                                                  '27'),
                                                                                                 (17, 'aload_0', ''),
                                                                                                 (18, 'iconst_0', ''),
                                                                                                 (19, 'dup2', ''),
                                                                                                 (20, 'daload', ''),
                                                                                                 (21, 'aload_2', ''),
                                                                                                 (22,
                                                                                                  'invokevirtual',
                                                                                                  'Method '
                                                                                                  'net/minecraft/world/entity/ai/attributes/AttributeModifier.amount:()D'),
                                                                                                 (25, 'dadd', ''),
                                                                                                 (26, 'dastore', ''),
                                                                                                 (27, 'return', '')],
 ('com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class', 'key'): [(0,
                                                                                               'getstatic',
                                                                                               'Field '
                                                                                               'net/minecraft/core/registries/Registries.ENCHANTMENT:Lnet/minecraft/resources/ResourceKey;'),
                                                                                              (3,
                                                                                               'ldc',
                                                                                               'String alexscaves'),
                                                                                              (5, 'aload_0', ''),
                                                                                              (6,
                                                                                               'invokestatic',
                                                                                               'Method '
                                                                                               'net/minecraft/resources/ResourceLocation.fromNamespaceAndPath:(Ljava/lang/String;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;'),
                                                                                              (9,
                                                                                               'invokestatic',
                                                                                               'Method '
                                                                                               'net/minecraft/resources/ResourceKey.create:(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/resources/ResourceLocation;)Lnet/minecraft/resources/ResourceKey;'),
                                                                                              (12, 'areturn', '')],
 ('com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class', '__class_init__'): [(221,
                                                                                                          'ldc_w',
                                                                                                          'String '
                                                                                                          'flinging'),
                                                                                                         (227,
                                                                                                          'putstatic',
                                                                                                          'Field '
                                                                                                          'FLINGING:Lnet/minecraft/resources/ResourceKey;')]}

class AuditError(ValueError):
    """An exact-artifact or bounded-contract verification failed."""


def require(ok, reason):
    if not ok:
        raise AuditError(reason)


def strict_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key ' + key)
        out[key] = value
    return out


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized_text(raw):
    return raw.replace('  static {};', '  private static void __class_init__();')


def method_sections(raw):
    answer = {}
    current, lines = None, []
    for line in normalized_text(raw).splitlines():
        match = METHOD_LINE.match(line)
        if match and '(' in match.group(1):
            if current is not None:
                require(current not in answer, 'duplicate textual method header')
                answer[current] = '\n'.join(lines)
            current, lines = match.group(1).strip(), [line]
        elif current is not None:
            lines.append(line)
    if current is not None:
        require(current not in answer, 'duplicate final textual method header')
        answer[current] = '\n'.join(lines)
    return answer


def exception_table(section):
    if 'Exception table:' not in section:
        return []
    rest = section.split('Exception table:', 1)[1]
    rows = []
    for line in rest.splitlines():
        if not line.strip() or line.strip() == 'from    to  target type':
            continue
        match = re.fullmatch(r'\s*(\d+)\s+(\d+)\s+(\d+)\s+(.+?)\s*', line)
        if not match:
            break
        rows.append({'from': int(match[1]), 'to': int(match[2]),
                     'target': int(match[3]), 'type': match[4]})
    require(rows, 'unparsed declared JVM exception table')
    require(len(rows) <= 32, 'unbounded exception table')
    return rows


def branch_edges(method):
    ins = method['instructions']
    offsets = [r['offset'] for r in ins]
    require(0 < len(ins) <= 1000, 'unbounded/empty full method')
    require(offsets == sorted(set(offsets)), 'duplicate/unsorted JVM offsets')
    known = set(offsets)
    edges = []
    for r in ins:
        op = r['opcode']
        require(op not in {'tableswitch', 'lookupswitch', 'jsr', 'jsr_w', 'ret'},
                'unverified switch/subroutine in selected method')
        if op.startswith('if') or op in {'goto', 'goto_w'}:
            require(re.fullmatch(r'\d+', r['operand']) is not None,
                    'unparsed branch target @' + str(r['offset']))
            target = int(r['operand'])
            require(target in known, 'branch target outside method @' + str(r['offset']))
            edges.append([r['offset'], target])
    return edges


def native_index(raw):
    out = {}
    for m in parse_methods(normalized_text(raw)):
        ident = (name_of(m), m['descriptor'])
        require(ident not in out, 'ambiguous JVM identity ' + str(ident))
        out[ident] = m
    return out


def checked_pivots(native):
    result = []
    for (owner, name), entries in PIVOT_SPECS.items():
        found = [m for (o, n, _), m in native.items() if o == owner and n == name]
        require(len(found) == 1, 'missing/ambiguous semantic method ' + name)
        method = found[0]
        rows = {r['offset']: r for r in method['instructions']}
        for at, op, token in entries:
            require(at in rows, 'missing semantic pivot @' + str(at))
            r = rows[at]
            require(r['opcode'] == op, 'semantic opcode drift ' + name + '@' + str(at))
            require(token in r['operand'] + ' ' + r['symbol'],
                    'semantic symbol/value drift ' + name + '@' + str(at))
            result.append({'owner': owner, 'name': name,
                           **{k: r[k] for k in ('offset', 'opcode', 'operand', 'symbol')}})
    require(0 < len(result) <= 512, 'unbounded semantic pivot roster')
    return result


def extract(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE), 'publisher SHA1/SHA256/size drift')
    old = json.loads(HISTORY.read_text(encoding='utf8'), object_pairs_hook=strict_pairs)
    require(historical_audit(jar, javap_bin) == old, 'immutable historical Flinging seal drift')
    resources, decoded = {}, {}
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate JAR members')
        class_sha = {p: digest(z.read(p)) for p in SELECTIONS}
        require(all(class_sha[p] == h for p, h in old['class_sha256'].items()),
                'historical class identity drift')
        token_owners = sorted(p for p in names if p.startswith(BASE)
                              and p.endswith('.class') and b'FLINGING' in z.read(p))
        require(token_owners == sorted([ITEM, REGISTRY]), 'new FLINGING token owner')
        for p in RESOURCE_PATHS:
            raw = z.read(p)
            require(0 < len(raw) <= 1_000_000, 'oversized/empty JSON resource')
            data = json.loads(raw, object_pairs_hook=strict_pairs)
            require(isinstance(data, dict), 'non-object JSON resource')
            resources[p] = {'sha256': digest(raw), 'size_bytes': len(raw)}
            decoded[p] = data
        enchant_paths = sorted(p for p in names if p.startswith('data/alexscaves/enchantment/') and p.endswith('.json'))
        require(len(enchant_paths) == 51, 'publisher enchantment universe drift')
        enchant_census = []
        reverse = []
        for p in enchant_paths:
            raw = z.read(p); d = json.loads(raw, object_pairs_hook=strict_pairs)
            exclusions = d.get('exclusive_set', [])
            require(isinstance(exclusions, (list, str)), 'unrecognized exclusivity structure')
            if 'alexscaves:flinging' in exclusions:
                reverse.append(p)
            enchant_census.append({'path': p, 'sha256': digest(raw), 'exclusive_set': exclusions})
        require(reverse == [], 'new reverse Flinging exclusivity declaration')
    require(decoded[ENCHANT] == EXPECTED_JSON, 'Flinging declarative values drift')
    require(decoded[TAG] == {'values': ['alexscaves:ortholance']}, 'supported item tag drift')
    acquire = {p: 'alexscaves:flinging' in decoded[p].get('values', [])
               for p in RESOURCE_PATHS if p.startswith('data/minecraft/tags/enchantment/')}
    require(all(acquire.values()), 'publisher acquisition-tag membership drift')
    keys = ['enchantment.alexscaves.flinging', 'enchantment.alexscaves.flinging.desc']
    locales = {p: {k: decoded[p].get(k) for k in keys}
               for p in RESOURCE_PATHS if '/lang/' in p}
    native, census, populations = {}, [], {}
    for owner, selected in SELECTIONS.items():
        raw = javap(javap_bin, jar, owner[:-6].replace('/', '.'))
        methods, sections = native_index(raw), method_sections(raw)
        populations[owner] = len(methods)
        picked = [(ident, m) for ident, m in methods.items()
                  if selected is None or ident[0] in selected]
        if selected is not None:
            require({ident[0] for ident, _ in picked} == selected, 'missing selected native method')
        require(len(picked) <= 32, 'unbounded selected owner method roster')
        for (name, desc), m in picked:
            require(m['header'] in sections, 'missing method textual extent')
            edges = branch_edges(m)
            handlers = exception_table(sections[m['header']])
            require(not handlers, 'unverified exception handler in chosen exact body')
            native[(owner, name, desc)] = m
            census.append({'owner': owner, 'name': name, 'descriptor': desc,
                           'instructions': len(m['instructions']), 'body_sha256': digest_method(m),
                           'direct_branches': len(edges), 'branch_edges': edges,
                           'switch_offsets': [], 'exception_table': handlers})
    require(len(census) <= 64 and sum(x['instructions'] for x in census) <= 5000,
            'unbounded full native census')
    pivots = checked_pivots(native)
    verbose = subprocess.run(
        [str(javap_bin), '-classpath', str(jar), '-v', '-p', COMPAT[:-6].replace('/', '.')],
        capture_output=True, text=True, timeout=45, check=True,
    ).stdout
    require(len(verbose) < 3_500_000, 'unbounded verbose compatibility class')
    bootstrap = re.search(r'(?m)^  2: #.*?(?=\n  \d+: #|\nInnerClasses:|\Z)', verbose, re.S)
    require(bootstrap is not None, 'attackDamageBonus bootstrap #2 missing')
    binding = bootstrap.group(0)
    require('LambdaMetafactory.metafactory:' in binding and
            'ACCompat.lambda$attackDamageBonus$2:([DLnet/minecraft/core/Holder;Lnet/minecraft/world/entity/ai/attributes/AttributeModifier;)V' in binding,
            'attackDamageBonus callback bootstrap drift')
    report = {
        'version': '1.0.10', 'enchantment': 'alexscaves:flinging',
        'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY',
        'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
        'artifact': {'sha1': SHA1, 'sha256': SHA256, 'size_bytes': SIZE},
        'legacy_seal': HISTORY.name,
        'legacy_seal_sha256': digest(HISTORY.read_bytes()),
        'class_sha256': class_sha, 'resources': resources,
        'resource_json': decoded[ENCHANT], 'supported_item_tag': decoded[TAG],
        'publisher_acquisition_tags': acquire, 'locales': locales,
        'publisher_enchantment_census': enchant_census,
        'reverse_exclusive_set': reverse,
        'compiled_flinging_token_owners': token_owners,
        'owner_method_populations': populations,
        'methods_checked': len(census),
        'instructions_checked': sum(x['instructions'] for x in census),
        'direct_branches_checked': sum(x['direct_branches'] for x in census),
        'method_census': census, 'pivots': pivots,
        'bootstrap_bindings': [{'owner': COMPAT, 'index': 2, 'callback': 'lambda$attackDamageBonus$2', 'section_sha256': digest(binding.encode())}],
        'safety': dict(SAFETY), 'contract': dict(CONTRACT),
    }
    return report


def validate_individual_seal(report, cert=None):
    cert = (json.loads(SEAL.read_text(encoding='utf8'), object_pairs_hook=strict_pairs)
            if cert is None else cert)
    require(report.get('claim_scope') == cert.get('claim_scope') == 'STATIC_TECHNICAL_CATALOG_ONLY', 'static claim scope drift')
    require(report.get('version') == cert.get('version') == '1.0.10' and
            report.get('enchantment') == cert.get('enchantment') == 'alexscaves:flinging', 'individual identity drift')
    require(report.get('evidence_grade') == cert.get('evidence_grade') == 'SHA_EXACT_BINARY_BEHAVIOR', 'individual evidence grade drift')
    require(report.get('artifact') == cert.get('artifact') == {'sha1': SHA1, 'sha256': SHA256, 'size_bytes': SIZE}, 'individual artifact identity drift')
    require((cert.get('methods_checked'), cert.get('instructions_checked'), cert.get('direct_branches_checked')) == (55, 1662, 75), 'individual native census drift')
    require(len(cert.get('method_census', [])) == 55 and len(cert.get('pivots', [])) == 442 and len(cert.get('resources', {})) == 10, 'individual evidence population drift')
    require(cert.get('compiled_flinging_token_owners') == sorted([ITEM, REGISTRY]), 'individual literal owner roster drift')
    require(cert.get('resource_json') == EXPECTED_JSON and cert.get('supported_item_tag') == {'values': ['alexscaves:ortholance']}, 'individual resource identity drift')

    require(report.get('safety') == cert.get('safety') == SAFETY, 'unsafe validation-state promotion')
    require(report.get('contract') == cert.get('contract') == CONTRACT, 'causal contract drift')
    require(report == cert, 'Flinging exact full-method causal seal drift')
    return cert


def audit(jar, javap_bin, cert_path=SEAL):
    report = extract(jar, javap_bin)
    cert = json.loads(Path(cert_path).read_text(encoding='utf8'), object_pairs_hook=strict_pairs)
    validate_individual_seal(report, cert)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--javap', default='javap')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--seal', type=Path, default=SEAL)
    args = parser.parse_args()
    report = audit(args.jar, args.javap, args.seal)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({k: report[k] for k in ('enchantment', 'methods_checked', 'instructions_checked', 'direct_branches_checked', 'safety')}, ensure_ascii=False))

if __name__ == '__main__':
    main()
