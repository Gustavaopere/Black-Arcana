#!/usr/bin/env python3
"""Replay the bounded Alshanex shard ritual contracts without running provider classes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

from alexscaves_1010_action_contract_audit import parse_javap
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, unique_pairs
from alshanex_403_exact_ritual_spell_abi import EXPECTED_SHA1, PREFIX, RITUAL_TYPE

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / 'wiki/modpack-catalog/providers/✅-alshanex-familiars/EXACT-4.0.3-ARCHMAGE-RITUAL.json'
PROVIDER = (21848062, EXPECTED_SHA1, 'ed006afb15a68bee9685ddac45c0f8bfc2a16e3a8a05004c6e1a3373f5f9a284')
LIBRARY = (341186, '7fa3f3116e35c12456425ae195924ced33fcc2eb',
           'bf53bc48bb220c268b2db3619c68d75dba15e140bbd2d3799dd85b9299a0e5a9')
BASE = 'net/alshanex/alshanex_familiars/'
RUNE = 'net/alshanex/familiarslib/item/AbstractRuneItem'
DRUID_SEAL = SEAL.with_name('EXACT-4.0.3-DRUID-RITUAL.json')
DRUID = 'item/shards/DruidShard'
ITEM_REGISTRY = 'registry/ItemRegistry'
SOUL = 'alshanex_familiars:pet_soul'
RECIPES = {
    'archmage_shard': (
        SOUL, 'minecraft:end_rod',
        (('irons_spellbooks:legendary_ink', True), ('irons_spellbooks:arcane_essence', True),
         ('irons_spellbooks:arcane_rune', True), ('irons_spellbooks:magic_cloth', True)),
    ),
    'druid_shard': (
        SOUL, 'minecraft:composter',
        (('irons_spellbooks:greater_oakskin_elixir', True), ('irons_spellbooks:arcane_essence', True),
         ('irons_spellbooks:nature_rune', True), ('minecraft:spore_blossom', False)),
    ),
}
CORE = 'block/entity/RitualCorePedestalEntity'
HELPER = 'util/rituals/RitualHelper'
AUTOMATOR = 'block/entity/RitualAutomatorBlockEntity'
MATCHER = 'recipe_types/RitualRecipeType'
SHARD = 'item/shards/ArchmageShard'
METHODS = {
    'block/RitualCorePedestal': {'useItemOn', 'dropItem', 'onRemove', 'getTicker'},
    'block/ArchmageStatue': {'useItemOn', 'dropItem', 'onRemove', 'newBlockEntity'},
    'block/ClericStatue': {'useItemOn', 'dropItem', 'onRemove', 'newBlockEntity'},
    'block/DruidStatue': {'useItemOn', 'dropItem', 'onRemove', 'newBlockEntity'},
    'block/HunterStatue': {'useItemOn', 'dropItem', 'onRemove', 'newBlockEntity'},
    'block/entity/FamiliarStatueEntity': {'getHeldItem', 'setHeldItem', 'loadAdditional', 'saveAdditional', 'drops', 'setChanged'},
    CORE: {'tick', 'setHeldItem', 'completeRitual', 'readNBT', 'writeNBT', 'drops'},
    HELPER: {'findMatchingRecipe', 'isValidRecipe', 'getResultForRecipe', 'isItemInRecipeRecipe',
             'getParticleForRecipe', 'clearItemsFromPedestals', 'getSurroundingPedestals',
             'getItemStacksFromPedestals', 'spawnParticlesAtPedestals', 'lambda$findMatchingRecipe$0'},
    MATCHER: {'matches', 'result', 'assemble', 'canCraftInDimensions', 'centralItem', 'inputs'},
    MATCHER + '$Serializer': {'codec', 'streamCodec', 'lambda$static$0', '<clinit>'},
    AUTOMATOR: {'tick', 'findCore', 'setRecipe', 'performCollection', 'performCleanup', 'performSupply',
                'removeNeed', 'extractItemForIngredient', 'isTargeted', 'spawnFlyingItem',
                'processFlyingItems', 'completeFlight', 'returnToStorageOrDrop', 'saveAdditional',
                'loadAdditional', 'lambda$tick$0'},
    'util/rituals/FlyingItem': {'<init>', 'tick', 'hasArrived', 'save', 'load'},
    ITEM_REGISTRY: {'<clinit>', 'lambda$static$1'},
    'registry/RecipeRegistry': {'<clinit>'},
    SHARD: {'<init>', 'spawnFamiliar'},
}
# JVM offsets for a small set of factual claims. The seal stores only method
# checksums/ABI and these anchors, without retaining the disassembly.
PROVIDER_PIVOTS = {
    CORE: {
        'tick': [(1, 'isClientSide:'), (38, 'isValidRecipe:'), (68, 'bipush 100'),
                 (87, 'bipush 10'), (136, 'bipush 100'), (145, 'completeRitual:')],
        'completeRitual': [(6, 'getResultForRecipe:'), (70, 'clearItemsFromPedestals:'),
                           (86, 'ItemStack."<init>":(Lnet/minecraft/world/level/ItemLike;)V'),
                           (89, 'setHeldItem:')],
    },
    HELPER: {
        'getSurroundingPedestals': [
            (7, 'iconst_2'), (8, 'BlockPos.north:'), (15, 'iconst_2'), (16, 'BlockPos.south:'),
            (23, 'iconst_2'), (24, 'BlockPos.east:'), (31, 'iconst_2'), (32, 'BlockPos.west:'),
        ],
        'findMatchingRecipe': [(87, 'Stream.findFirst:')],
        'clearItemsFromPedestals': [(143, 'RitualIngredient.consume:'), (228, 'FamiliarStatueEntity.setHeldItem:')],
    },
    AUTOMATOR: {
        'tick': [(32, 'bipush 10'), (124, 'BlockPos.below:'), (128, 'Level.getCapability:')],
        'lambda$tick$0': [(1, 'RecipeHolder.id:'), (8, 'ResourceLocation.equals:')],
        'findCore': [(8, 'bipush -10'), (12, 'bipush 10'), (17, 'bipush -5'),
                     (25, 'bipush -10'), (31, 'bipush 10')],
        'performCollection': [(20, 'isSameItemSameComponents:'), (30, 'setHeldItem:'),
                              (48, 'spawnFlyingItem:')],
        'spawnFlyingItem': [(11, 'bipush 20')],
        'completeFlight': [(12, 'returnToStorageOrDrop:'), (62, 'FamiliarStatueEntity.setHeldItem:'),
                           (100, 'RitualCorePedestalEntity.setHeldItem:')],
    },
    ITEM_REGISTRY: {'<clinit>': [(670, 'String archmage_shard'), (673, 'InvokeDynamic #37:get:'),
                               (678, 'DeferredRegister.register:'), (681, 'Field ARCHMAGE_RUNE:')]},
    SHARD: {'spawnFamiliar': [(4, 'EntityRegistry.ARCHMAGE_PET:'), (46, 'Player.getYRot:'),
                              (49, 'fneg'), (50, 'ArchmagePetEntity.setYRot:'),
                              (56, 'Level.addFreshEntity:'), (59, 'pop')]},
}
DRUID_PIVOTS = {
    HELPER: {'clearItemsFromPedestals': [(143, 'RitualIngredient.consume:'),
                                        (146, 'ifne 152'), (149, 'goto 119'),
                                        (228, 'FamiliarStatueEntity.setHeldItem:')]},
    AUTOMATOR: {'performCleanup': [(214, 'Ingredient.test:'), (231, 'ifne 267')],
                'performSupply': [(152, 'removeNeed:'), (207, 'removeNeed:')],
                'removeNeed': [(30, 'Ingredient.test:'), (38, 'List.remove:')]},
    ITEM_REGISTRY: {'<clinit>': [(687, 'String druid_shard'), (690, 'InvokeDynamic #38:get:'),
                               (695, 'DeferredRegister.register:'), (698, 'Field DRUID_RUNE:')]},
    DRUID: {'spawnFamiliar': [(4, 'EntityRegistry.DRUID_PET:'), (21, 'iconst_0'),
                             (25, 'DruidPetEntity.setIsImpostor:'), (31, 'BlockPos.getCenter:'),
                             (35, 'dconst_1'), (46, 'Player.getYRot:'), (49, 'fneg'),
                             (50, 'DruidPetEntity.setYRot:'), (56, 'Level.addFreshEntity:'), (59, 'pop')]},
}
LIBRARY_PIVOTS = {'useOn': [(24, 'iconst_1'), (25, 'ItemStack.shrink:'), (33, 'spawnFamiliar:'),
                            (52, 'triggerShardAdvancement:'), (55, 'InteractionResult.SUCCESS:')]}


def verify_artifact(path, expected):
    size, sha1, sha256 = expected
    require(path.stat().st_size == size, 'artifact size mismatch: ' + path.name)
    raw = path.read_bytes()
    require(hashlib.sha1(raw).hexdigest() == sha1 and digest(raw) == sha256,
            'artifact SHA mismatch: ' + path.name)
    return {'bytes': size, 'sha1': sha1, 'sha256': sha256}


def inspect_recipe(archive, ritual, specification):
    resource = PREFIX + ritual + '.json'
    raw = archive.read(resource)
    recipe = json.loads(raw, object_pairs_hook=unique_pairs)
    center, particle, inputs = specification
    result = 'alshanex_familiars:' + ritual
    require(set(recipe) == {'type', 'central_item', 'inputs', 'result', 'particle_type'}, 'recipe fields drift')
    require(recipe['type'] == RITUAL_TYPE and recipe['central_item'] == {'item': center},
            'recipe type or center drift')
    require(recipe['result'] == {'id': result} and recipe['particle_type'] == particle,
            'recipe output or particle drift')
    require(len(recipe['inputs']) == len(inputs), 'peripheral roster drift')
    for actual, (item, consume) in zip(recipe['inputs'], inputs, strict=True):
        require(set(actual) == {'ingredient', 'count', 'consume'}
                and actual['ingredient'] == {'item': item}
                and type(actual['count']) is int and actual['count'] == 1 and actual['consume'] is consume,
                'peripheral ingredient drift: ' + item)
    return {'resource': resource, 'resource_sha256': digest(raw), 'type': RITUAL_TYPE,
            'recipe_id': 'alshanex_familiars:ritual_recipes/' + ritual,
            'central_item': center,
            'peripheral_inputs': [{'item': item, 'count': 1, 'consume': consume} for item, consume in inputs],
            'result_item': result, 'result_count_explicit': False, 'result_components_explicit': False,
            'particle': particle}


def inspect_class(archive, jar, javap, owner, names, pivots):
    raw = archive.read(owner + '.class')
    reader = ClassReader(raw)
    require(reader.name == owner and reader.major == 65, 'class identity drift: ' + owner)
    output = subprocess.run([javap, '-classpath', str(jar), '-p', '-c', '-s', owner.replace('/', '.')],
                            capture_output=True, text=True, check=True, timeout=60)
    parsed = parse_javap(output.stdout, owner)
    selected = [m for m in reader.methods if m['name'] in names and 'code_sha256' in m]
    require({m['name'] for m in selected} == names, 'method roster drift: ' + owner)
    for method in selected:
        name = method['name']
        key = (name, method['descriptor'])
        require(key in parsed and parsed[key], 'disassembly missing: ' + name)
        body = parsed[key]
        method['instruction_count'] = len(body)
        anchors = pivots.get(name, ())
        if anchors:
            require(sum(m['name'] == name for m in selected) == 1, 'ambiguous anchored method: ' + name)
            method['anchors'] = []
        for offset, expected in anchors:
            opcode, operand, symbol = body.get(offset, ('', '', ''))
            require(' '.join((opcode, operand)).strip() == expected or expected in symbol,
                    f'bytecode anchor drift: {owner}.{name} @{offset} {expected}')
            method['anchors'].append({'offset': offset, 'fact': expected})
    return {'class_sha256': digest(raw), 'superclass': reader.parent, 'methods': selected}


def item_factory(archive, bootstrap_index, shard):
    reader = ClassReader(archive.read(BASE + ITEM_REGISTRY + '.class'))
    arguments = reader.attributes['bootstrap_methods'][bootstrap_index]['arguments']
    expected = {'reference_kind': 8, 'reference': [10, BASE + shard, [12, '<init>', '()V']]}
    require(expected in arguments, 'shard item factory drift: ' + shard)
    return {'bootstrap_index': bootstrap_index, 'constructor_owner': BASE + shard, 'descriptor': '()V'}


def audit(jar, library, javap):
    publisher = verify_artifact(jar, PROVIDER)
    dependency = verify_artifact(library, LIBRARY)
    with zipfile.ZipFile(jar) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate publisher ZIP path')
        recipe = inspect_recipe(archive, 'archmage_shard', RECIPES['archmage_shard'])
        factory = item_factory(archive, 37, SHARD)
        classes = {BASE + name: inspect_class(archive, jar, javap, BASE + name, names, PROVIDER_PIVOTS.get(name, {}))
                   for name, names in METHODS.items()}
    with zipfile.ZipFile(library) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate FamiliarsLib ZIP path')
        downstream = inspect_class(archive, library, javap, RUNE, {'useOn', 'triggerShardAdvancement'}, LIBRARY_PIVOTS)
    require(classes[BASE + SHARD]['superclass'] == RUNE, 'familiar shard superclass drift')
    return {'schema_version': 1, 'publisher_version': '4.0.3', 'publisher_artifact': publisher,
            'familiarslib_version': '1.7.1', 'familiarslib_artifact': dependency, 'recipe': recipe,
            'item_factory': factory,
            'provider_classes': classes, 'post_craft_library_class': {RUNE: downstream},
            'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
            'mutation': 'NO_MUTATION', 'provider_universe_closed': False}


def audit_druid(jar, library, javap):
    shared = canonical(audit(jar, library, javap))
    require(shared == SEAL.read_text(encoding='utf-8'), 'shared Archmage Shard seal drift')
    with zipfile.ZipFile(jar) as archive:
        recipe = inspect_recipe(archive, 'druid_shard', RECIPES['druid_shard'])
        factory = item_factory(archive, 38, DRUID)
        classes = {BASE + name: inspect_class(
            archive, jar, javap, BASE + name, set(pivots), pivots,
        ) for name, pivots in DRUID_PIVOTS.items()}
    require(classes[BASE + DRUID]['superclass'] == RUNE, 'Druid Shard superclass drift')
    return {'schema_version': 1, 'publisher_version': '4.0.3',
            'shared_ritual_seal': SEAL.name, 'shared_ritual_seal_sha256': digest(shared.encode('utf-8')),
            'recipe': recipe, 'item_factory': factory, 'provider_classes': classes,
            'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
            'mutation': 'NO_MUTATION', 'provider_universe_closed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, required=True)
    parser.add_argument('--familiarslib', type=Path, required=True)
    parser.add_argument('--javap', default='javap')
    parser.add_argument('--ritual', choices=tuple(RECIPES), default='archmage_shard')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--output', type=Path)
    args = parser.parse_args()
    inspect, seal = (audit_druid, DRUID_SEAL) if args.ritual == 'druid_shard' else (audit, SEAL)
    actual = canonical(inspect(args.jar, args.familiarslib, args.javap))
    if args.verify:
        require(actual == seal.read_text(encoding='utf-8'), args.ritual + ' seal drift')
    else:
        args.output.write_text(actual, encoding='utf-8')
    print(f'PASS: Alshanex 4.0.3 {args.ritual} manual and automated ritual contract')


if __name__ == '__main__':
    main()
