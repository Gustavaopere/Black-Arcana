#!/usr/bin/env python3
"""Check the nine remaining packaged rituals and their bounded item consumers."""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

from alshanex_403_archmage_ritual_contract import (
    BASE, DRUID_SEAL, ITEM_REGISTRY, RECIPES as REPLAYED, RUNE, SOUL, audit_druid,
    inspect_class, inspect_recipe, item_factory,
)
from alshanex_403_exact_ritual_spell_abi import PREFIX, RITUALS
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require

SEAL = DRUID_SEAL.with_name('EXACT-4.0.3-REMAINING-RITUALS.json')
ALSHANEX = 'alshanex_familiars:'
IRONS = 'irons_spellbooks:'
MINECRAFT = 'minecraft:'
ARCANE = IRONS + 'arcane_essence'
DIVINE = IRONS + 'divine_soulshard'
LIB_PREFIX = 'net/alshanex/familiarslib/'
PET = LIB_PREFIX + 'entity/AbstractSpellCastingPet'
CONSUMABLES = LIB_PREFIX + 'util/consumables/'
MIRROR = 'item/TruthMirror'
ENTITY_REGISTRY = 'registry/EntityRegistry'


def inputs(*items, retained=None):
    return tuple((item, item != retained) for item in items)


RECIPES = {
    'frostling_shard': (SOUL, MINECRAFT + 'snowflake',
                      inputs(MINECRAFT + 'blue_ice', ARCANE, IRONS + 'ice_rune', IRONS + 'frozen_bone')),
    'hunter_shard': (SOUL, MINECRAFT + 'crit',
                    inputs(IRONS + 'hogskin', ARCANE, MINECRAFT + 'crossbow', MINECRAFT + 'rabbit_foot')),
    'lightning_mage_shard': (SOUL, IRONS + 'electricity',
                           inputs(IRONS + 'lightning_bottle', ARCANE, IRONS + 'lightning_rune',
                                  MINECRAFT + 'lightning_rod')),
    'magic_power_tier_2': (ALSHANEX + 'magic_power_tier_1', IRONS + 'cleanse',
                          inputs(MINECRAFT + 'ghast_tear', IRONS + 'cinder_essence',
                                 MINECRAFT + 'blaze_rod', IRONS + 'hogskin')),
    'magic_power_tier_3': (ALSHANEX + 'magic_power_tier_2', IRONS + 'cleanse',
                          inputs(DIVINE, MINECRAFT + 'end_crystal', MINECRAFT + 'end_rod',
                                 IRONS + 'dragonskin', retained=DIVINE)),
    'magic_resist_tier_2': (ALSHANEX + 'magic_resist_tier_1', IRONS + 'unstable_ender',
                           inputs(MINECRAFT + 'ghast_tear', IRONS + 'cinder_essence',
                                  MINECRAFT + 'warped_fungus', IRONS + 'hogskin')),
    'magic_resist_tier_3': (ALSHANEX + 'magic_resist_tier_2', IRONS + 'unstable_ender',
                           inputs(DIVINE, MINECRAFT + 'popped_chorus_fruit', MINECRAFT + 'crying_obsidian',
                                  IRONS + 'dragonskin', retained=DIVINE)),
    'summoner_shard': (SOUL, MINECRAFT + 'sculk_charge_pop',
                       inputs(IRONS + 'ruined_book', ARCANE, IRONS + 'eldritch_manuscript',
                              MINECRAFT + 'sculk_catalyst')),
    'truth_mirror': (IRONS + 'visibility_ring', MINECRAFT + 'enchanted_hit',
                     inputs(MINECRAFT + 'gold_ingot', IRONS + 'mithril_ingot',
                            IRONS + 'shriving_stone', IRONS + 'divine_pearl')),
}

# Framework offsets in ItemRegistry.<clinit>, invokedynamic index, holder field.
REGISTRY = {
    'frostling_shard': (772, 43, 'FROSTLING_RUNE'),
    'hunter_shard': (704, 39, 'HUNTER_RUNE'),
    'lightning_mage_shard': (738, 41, 'MAGE_RUNE'),
    'magic_power_tier_2': (1108, 62, 'MAGIC_POWER_TIER_2'),
    'magic_power_tier_3': (1125, 63, 'MAGIC_POWER_TIER_3'),
    'magic_resist_tier_2': (1159, 65, 'MAGIC_RESIST_TIER_2'),
    'magic_resist_tier_3': (1176, 66, 'MAGIC_RESIST_TIER_3'),
    'summoner_shard': (755, 42, 'SUMMONER_RUNE'),
    'truth_mirror': (904, 50, 'TRUTH_MIRROR'),
}
SHARDS = {
    'frostling_shard': ('FrostlingShard', 'FrostlingPetEntity', 'FROSTLING_PET'),
    'hunter_shard': ('HunterShard', 'HunterPetEntity', 'HUNTER_PET'),
    'lightning_mage_shard': ('MageShard', 'MagePetEntity', 'MAGE_PET'),
    'summoner_shard': ('SummonerShard', 'SummonerPetEntity', 'SUMMONER_PET'),
}
ENTITY_FIELDS = (
    (14, 'mage_pet', 'MAGE_PET'), (46, 'summoner_pet', 'SUMMONER_PET'),
    (78, 'hunter_pet', 'HUNTER_PET'), (110, 'illusionist_pet', 'ILLUSIONIST_PET'),
    (203, 'frostling_pet', 'FROSTLING_PET'),
)
FACTORIES = {
    'magic_power_tier_2': ('lambda$static$40', 'SPELL_POWER', 2, 'RARE'),
    'magic_power_tier_3': ('lambda$static$41', 'SPELL_POWER', 3, 'EPIC'),
    'magic_resist_tier_2': ('lambda$static$43', 'SPELL_RESIST', 2, 'RARE'),
    'magic_resist_tier_3': ('lambda$static$44', 'SPELL_RESIST', 3, 'EPIC'),
}
ITEM_DESC = '()Lnet/minecraft/world/item/Item;'
MIRROR_PIVOTS = {
    '<init>': [(14, 'iconst_1'), (15, 'Item$Properties.stacksTo:'),
               (18, 'iconst_3'), (19, 'Item$Properties.durability:')],
    'interactLivingEntity': [
        (18, 'Level.isClientSide:'), (26, 'getIsImpostor:'), (32, 'ifeq 482'),
        (37, 'getSummoner:'), (40, 'ifnonnull 233'),
        (103, 'Level.addFreshEntity:'), (106, 'pop'), (208, 'AbstractSpellCastingPet.remove:'),
        (227, 'triggerRevealAdvancement:'), (239, 'LivingEntity.is:'), (242, 'ifeq 482'),
        (315, 'IllusionistPetEntity.setOwnerUUID:'), (355, 'Level.addFreshEntity:'), (358, 'pop'),
        (460, 'AbstractSpellCastingPet.remove:'), (479, 'triggerRevealAdvancement:'),
        (485, 'EquipmentSlot.MAINHAND:'), (488, 'ItemStack.hurtAndBreak:'),
        (491, 'InteractionResult.SUCCESS:'), (495, 'InteractionResult.FAIL:'),
    ],
    'triggerRevealAdvancement': [(0, 'CriteriaTriggersRegistry.ILLUSIONIST_REVEAL_TRIGGER:')],
}
LIB_PIVOTS = {
    PET: {
        'getSummoner': [(9, 'getOwnerUUID:'), (12, 'OwnerHelper.getAndCacheOwner:')],
        'mobInteract': [(2, 'Player.getItemInHand:'), (64, 'AbstractFamiliarStorageBlockEntity.isOwner:'),
                        (87, 'FamiliarConsumableIntegration.handleConsumableInteraction:'),
                        (250, 'Level.isClientSide:'), (257, 'getOwnerUUID:'),
                        (316, 'FamiliarConsumableIntegration.handleConsumableInteraction:')],
    },
    CONSUMABLES + 'FamiliarConsumableIntegration': {
        'handleConsumableInteraction': [
            (17, 'Level.isClientSide:'), (41, 'FamiliarConsumableComponent.getLimit:'),
            (50, 'if_icmplt 113'), (119, 'getMaxUsableTier:'),
            (222, 'FamiliarConsumableComponent.getBonus:'),
            (234, 'Math.min:'), (247, 'ConsumableData.setValue:'),
            (259, 'FamiliarConsumableSystem.applyAttributeModifiers:'),
            (276, 'iconst_1'), (277, 'ItemStack.shrink:'),
        ],
        'getMaxUsableTier': [],
        'applyConsumableModifiers': [],
        'saveConsumableData': [],
        'loadConsumableData': [],
    },
    CONSUMABLES + 'FamiliarConsumableSystem': {
        'applyAttributeModifiers': [
            (124, 'AttributeRegistry.SPELL_POWER:'), (140, 'double 100.0d'),
            (155, 'ADD_MULTIPLIED_BASE:'), (167, 'AttributeInstance.addPermanentModifier:'),
            (185, 'AttributeRegistry.SPELL_RESIST:'), (201, 'double 100.0d'),
            (216, 'ADD_MULTIPLIED_BASE:'), (228, 'AttributeInstance.addPermanentModifier:'),
        ],
    },
    CONSUMABLES + 'FamiliarConsumableSystem$ConsumableData': {
        'getValue': [], 'setValue': [], 'saveToNBT': [], 'loadFromNBT': [],
    },
    CONSUMABLES + 'FamiliarConsumableComponent': {
        'getBonus': [], 'getLimit': [],
    },
    CONSUMABLES + 'FamiliarConsumableSystem$ConsumableType': {
        '<clinit>': [
            (106, 'String SPELL_POWER'), (119, 'iconst_5'), (123, 'bipush 15'),
            (136, 'bipush 30'), (141, 'bipush 45'), (149, 'Field SPELL_POWER:'),
            (156, 'String SPELL_RESIST'), (169, 'iconst_5'), (173, 'bipush 15'),
            (186, 'bipush 30'), (191, 'bipush 45'), (199, 'Field SPELL_RESIST:'),
        ],
        'getTierBonus': [], 'getTierLimit': [],
    },
}


def registry_contract(archive, jar, javap):
    pivots = {'<clinit>': []}
    for name, (offset, bootstrap, field) in REGISTRY.items():
        pivots['<clinit>'].extend([
            (offset, 'String ' + name), (offset + 3, f'InvokeDynamic #{bootstrap}:get:'),
            (offset + 8, 'DeferredRegister.register:'), (offset + 11, 'Field ' + field + ':'),
        ])
    for method, kind, tier, rarity in FACTORIES.values():
        pivots[method] = [
            (11, 'bipush 64'), (16, 'Rarity.' + rarity + ':'), (22, 'ComponentRegistry.FAMILIAR_CONSUMABLE:'),
            (37, 'ConsumableType.' + kind + ':'), (40, f'iconst_{tier}'), (44, 'Item$Properties.component:'),
        ]
    reader = ClassReader(archive.read(BASE + ITEM_REGISTRY + '.class'))
    bootstraps = reader.attributes['bootstrap_methods']
    factories = {}
    for name, (method, _, _, _) in FACTORIES.items():
        index = REGISTRY[name][1]
        factory = {'reference_kind': 6, 'reference': [10, BASE + ITEM_REGISTRY, [12, method, ITEM_DESC]]}
        require(factory in bootstraps[index]['arguments'], 'unexpected consumable factory: ' + name)
        factories[name] = {'bootstrap_index': index, 'method': method, 'descriptor': ITEM_DESC}
    return inspect_class(archive, jar, javap, BASE + ITEM_REGISTRY, set(pivots), pivots), factories


def audit(jar, library, javap):
    druid = canonical(audit_druid(jar, library, javap))
    require(druid == DRUID_SEAL.read_text(encoding='utf-8'), 'shared catalyst and automation seal drift')
    roster = sorted(set(REPLAYED) | set(RECIPES))
    require(roster == sorted(RITUALS) and REGISTRY.keys() == RECIPES.keys(), 'unexpected coverage roster')
    with zipfile.ZipFile(jar) as archive:
        found = sorted(name[len(PREFIX):-5] for name in archive.namelist()
                       if name.startswith(PREFIX) and name.endswith('.json'))
        require(found == roster, 'publisher ritual recipe roster drift')
        recipe_facts = {name: inspect_recipe(archive, name, spec) for name, spec in RECIPES.items()}
        registry, bindings = registry_contract(archive, jar, javap)
        classes = {BASE + ITEM_REGISTRY: registry, BASE + MIRROR: inspect_class(
            archive, jar, javap, BASE + MIRROR, set(MIRROR_PIVOTS), MIRROR_PIVOTS,
        )}
        entity_pivots = {'<clinit>': [
            pair for offset, name, field in ENTITY_FIELDS
            for pair in ((offset, 'String ' + name), (offset + 10, 'Field ' + field + ':'))
        ]}
        classes[BASE + ENTITY_REGISTRY] = inspect_class(
            archive, jar, javap, BASE + ENTITY_REGISTRY, {'<clinit>'}, entity_pivots,
        )
        bindings['truth_mirror'] = item_factory(archive, REGISTRY['truth_mirror'][1], MIRROR)
        for name, (shard, entity, entity_field) in SHARDS.items():
            owner = 'item/shards/' + shard
            pivots = {'spawnFamiliar': [
                (4, 'EntityRegistry.' + entity_field + ':'), (21, 'iconst_0'),
                (25, entity + '.setIsImpostor:'), (31, 'BlockPos.getCenter:'),
                (35, 'dconst_1'), (46, 'Player.getYRot:'), (49, 'fneg'),
                (50, entity + '.setYRot:'), (56, 'Level.addFreshEntity:'), (59, 'pop'),
            ]}
            contract = inspect_class(archive, jar, javap, BASE + owner, {'<init>', 'spawnFamiliar'}, pivots)
            require(contract['superclass'] == RUNE, 'shard superclass drift: ' + name)
            classes[BASE + owner] = contract
            bindings[name] = item_factory(archive, REGISTRY[name][1], owner)
    with zipfile.ZipFile(library) as archive:
        consumers = {name: inspect_class(archive, library, javap, name, set(pivots), pivots)
                     for name, pivots in LIB_PIVOTS.items()}
    return {'schema_version': 1, 'publisher_version': '4.0.3',
            'publisher_ritual_recipe_ids': roster, 'additional_ritual_recipes': recipe_facts,
            'shared_druid_seal': DRUID_SEAL.name, 'shared_druid_seal_sha256': digest(druid.encode('utf-8')),
            'output_item_bindings': bindings, 'provider_classes': classes, 'library_consumers': consumers,
            'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
            'mutation': 'NO_MUTATION', 'provider_universe_closed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, required=True)
    parser.add_argument('--familiarslib', type=Path, required=True)
    parser.add_argument('--javap', default='javap')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = canonical(audit(args.jar, args.familiarslib, args.javap))
    if args.verify:
        require(report == SEAL.read_text(encoding='utf-8'), 'Alshanex ritual seal drift')
    else:
        args.output.write_text(report, encoding='utf-8')
    print('PASS: 11/11 exact Alshanex publisher ritual contracts, including Archmage and Druid')


if __name__ == '__main__':
    main()
