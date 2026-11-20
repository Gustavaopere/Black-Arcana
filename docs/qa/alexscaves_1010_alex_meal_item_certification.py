#!/usr/bin/env python3
"""Compose the exact Alex Meal item evidence with existing static food contracts.

No game classes are loaded. The reference engine and recipe lifecycle remain
separate from accepted gameplay, effective datapacks and safe perk mutations.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import zipfile

from alexscaves_1010_armor_material_audit import canonical, digest, load_seal, require
from alexscaves_1010_alex_meal_item_probe import inspect, TARGET, REGISTRY

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-ALEX-MEAL-ITEM-CERTIFICATION-1.0.10.json'
ORIGINAL = 'EXACT-ALEX-MEAL-ITEM-CONTRACT-1.0.10.json'
FOODS = 'EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json'
FOOD_REFERENCE = 'EXACT-FOODS-CONTRACT-1.0.10.json'
BUILDER = 'EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json'
REGISTRY_SEAL = 'EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json'
PREREQUISITES = {
    ORIGINAL: '289818396893334a8a281dcbed1e10ec93c04b776523641716d3d934c87008c0',
    FOODS: 'ab59a8181ea70648053efb15b8fd132f0c6fd3f9f683c7ea72729e0ef0e5c876',
    FOOD_REFERENCE: '391b4c8d56e364a234af03d34dc5b4fcb900176e116037c9b8363516566c4bef',
    BUILDER: '504735467770d52d75c99e7081bfb2a962e5dde0dfa32d884dfdab2e85a6473c',
    REGISTRY_SEAL: '0223cf52d1eaf653488346012d6bd80a74ab2219e3a31126aa0bee18f06a88f7',
}
CLAIMS = {
    'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY',
    'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
    'static_technical_contract': 'CERTIFIED_STATIC_7_AXES',
    'runtime_dispatch': 'NOT_VERIFIED', 'mutating_hook': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
    'mutation': 'NO_MUTATION', 'provider_universe_closed': False,
    'semantic_magic_roots_delta': 0,
}
AXES = {
    'identity': 'Exact publisher 1.0.10 hashes, concrete item class and complete two-method surface, registry argument flow and packaged recipe/model; source 1.1.1 is not the behavior authority.',
    'behavior': 'Constructor attaches the ALEX_MEAL food properties, rarity alias and stack limit; tooltip appends translated styled text before super. No own consumption override; inherited consumption is a pinned external reference.',
    'parameters': 'Nutrition 40, binary32 saturation modifier 5, nominal 400 saturation before reference clamps, stack limit 1, bowl conversion, CONFUSION 200 ticks and BAD_OMEN 48000 ticks at probability 1. Reference use duration 32 ticks and amplifier zero are separately scoped.',
    'targeting': 'Food consumer is the receiving entity in the external reference. No own attack, target query, range, area, projectile, summon or direct damage behavior. Downstream vanilla effects are not certified by this item.',
    'costs': 'Own methods do not settle resources. The inherited reference requests consume(1,entity), preserves infinite materials and handles bowl conversion; actual overrides, component composition and transactions remain unverified.',
    'integration': 'Composes existing FoodBuilder, Foods and registry contracts without mutating global FoodProperties or suppliers. Use events and getFoodProperties are reference surfaces, not approved per-player hooks or Mastery settlement.',
    'validation': 'Reproduces the original exact report, checks immutable prerequisite seals, complete item/factory bodies and resources, and records selected translation strings. Negative controls and two real read-only CLI runs guard the finite claim.',
}
BOUNDARIES = {
    'original_evidence': 'STATIC_CONTRACT_CANDIDATE_NOT_IN_LEDGER_PRESERVED',
    'inherited_consumption': 'COMPOSITION_OF_PINNED_OFFICIAL_REFERENCES',
    'effect_application_acceptance': 'NOT_VERIFIED',
    'downstream_effect_lifecycle': 'NOT_CERTIFIED_BY_THIS_ITEM',
    'effective_datapack_and_components': 'NOT_VERIFIED',
    'registry_execution': 'NOT_VERIFIED',
    'per_player_mutation_and_progression': 'NOT_CERTIFIED',
}
RECIPE_ITEMS = Counter({'alexscaves:gingerbread_crumbs': 2, 'minecraft:baked_potato': 1,
                        'minecraft:carrot': 1, 'minecraft:honey_bottle': 1,
                        'minecraft:cooked_beef': 1, 'minecraft:bowl': 1})


def prerequisites(provider=PROVIDER):
    data = {}
    for name, expected in PREREQUISITES.items():
        path = provider / name
        require(digest(path.read_bytes()) == expected, 'prerequisite seal drift: ' + name)
        data[name] = load_seal(path)
    return data


def original_report(native, prior):
    return {'scope': 'DISCOVERY_NOT_CERTIFIED', 'artifact': prior[ORIGINAL]['artifact'],
            'native': native, 'mutation': 'NO_MUTATION', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'provider_universe_closed': False}


def method(native, name):
    found = [entry for entry in native['methods'] if entry['declaration']['name'] == name]
    require(len(found) == 1, 'missing or duplicated method ' + name)
    return found[0]


def pivot(body, offset, opcode, symbol):
    row = next((row for row in body['instructions'] if row['offset'] == offset), None)
    require(row is not None and row['opcode'] == opcode and symbol in row['symbol'],
            'causal pivot drift at ' + str(offset))


def validate_contract(data, prior=None):
    prior = prior or prerequisites()
    require(data['claims'] == CLAIMS and data['axes'] == AXES and data['boundaries'] == BOUNDARIES,
            'claim or authority boundary drift')
    require(data['prerequisites'] == PREREQUISITES, 'prerequisite identity drift')
    require(data['artifact'] == prior[ORIGINAL]['artifact'], 'artifact identity drift')
    native = data['native']
    report_sha = digest(canonical(original_report(native, prior)).encode())
    require(report_sha == prior[ORIGINAL]['native_report_sha256'] == data['original_report_sha256'],
            'original exact report not reproduced')
    require(native['class_entries_scanned'] == 1555 and native['parent'] == 'net/minecraft/world/item/Item',
            'class/parent census drift')
    require(native['fields'] == [] and native['interfaces'] == [] and native['descendants'] == [],
            'new state, interface or native subclass')
    require(len(native['declarations']) == 2 and len(native['methods']) == 2,
            'complete own-method surface drift')
    ctor, tooltip = method(native, '<init>'), method(native, 'appendHoverText')
    require((ctor['instruction_count'], tooltip['instruction_count']) == (12, 16), 'body coverage drift')
    pivot(ctor, 8, 'getstatic', 'ACFoods.ALEX_MEAL:')
    pivot(ctor, 11, 'invokestatic', 'ACFoodBuilder.food:')
    pivot(ctor, 14, 'getstatic', 'ACItemRegistry.RARITY_RAINBOW:')
    pivot(ctor, 17, 'invokevirtual', 'Item$Properties.rarity:')
    require(next(row for row in ctor['instructions'] if row['offset'] == 20)['opcode'] == 'iconst_1',
            'stack-limit argument drift')
    pivot(ctor, 21, 'invokevirtual', 'Item$Properties.stacksTo:(I)')
    pivot(ctor, 24, 'invokespecial', 'Item."<init>":')
    pivot(tooltip, 1, 'ldc', 'String item.alexscaves.alex_meal.desc')
    pivot(tooltip, 6, 'getstatic', 'ChatFormatting.GRAY:')
    pivot(tooltip, 12, 'getstatic', 'ChatFormatting.ITALIC:')
    pivot(tooltip, 18, 'invokeinterface', 'List.add:')
    pivot(tooltip, 30, 'invokespecial', 'Item.appendHoverText:')
    binding = next(row for row in prior[REGISTRY_SEAL]['native']['bindings'] if row['field'] == 'ALEX_MEAL')
    require(data['registry_binding'] == binding and binding['resource_location'] == 'alexscaves:alex_meal',
            'causal registry binding drift')
    rarity = prior[REGISTRY_SEAL]['native']['support_field_initializers']['RARITY_RAINBOW']
    require(data['rarity_alias'] == rarity and rarity['value']['name'] == 'EPIC' and
            rarity['value']['owner'] == 'net/minecraft/world/item/Rarity', 'rarity alias drift')
    factory = native['factory']
    require(factory['declaration']['name'] == binding['factory']['name'] and
            factory['declaration']['descriptor'] == binding['factory']['descriptor'] and
            factory['declaration']['code_sha256'] == binding['factory']['code_sha256'] and
            factory['instruction_sha256'] == binding['factory']['instruction_sha256'], 'factory identity drift')
    require([row['opcode'] for row in factory['instructions']] == ['new', 'dup', 'invokespecial', 'areturn'],
            'factory shape drift')
    pivot(factory, 4, 'invokespecial', TARGET + '."<init>":()V')
    food = prior[FOODS]['native']['field_profiles']['ALEX_MEAL']
    require(data['food_profile'] == food and food['nutrition'] == 40 and
            food['saturation_modifier'] == {'bits_hex': '40a00000', 'value': 5.0} and
            food['flags'] == ['bowl'], 'food parameters drift')
    require([(e['field_name'], e['duration_ticks'], e['probability']) for e in food['effects']] ==
            [('CONFUSION', 200, {'bits_hex': '3f800000', 'value': 1.0}),
             ('BAD_OMEN', 48000, {'bits_hex': '3f800000', 'value': 1.0})], 'effect identity/order/probability drift')
    require(data['reference_reports'] == {
        'food': prior[FOOD_REFERENCE]['reports'], 'builder': prior[BUILDER]['reports']}, 'reference provenance drift')
    recipe = native['resources']['data/alexscaves/recipe/alex_meal.json']['json']
    require(recipe['type'] == 'minecraft:crafting_shapeless' and
            recipe['result'] == {'id': 'alexscaves:alex_meal'} and
            Counter(row['item'] for row in recipe['ingredients']) == RECIPE_ITEMS, 'recipe identity drift')
    translations = data['translations']
    require(translations['assets/alexscaves/lang/en_us.json']['strings'] == {
        'item.alexscaves.alex_meal': 'Alex Meal',
        'item.alexscaves.alex_meal.desc': 'You really live like this?'}, 'provider text drift')
    require(data['semantic_magic_roots_delta'] == 0, 'food is not a new spell root')


def inspect_contract(jar, javap):
    prior = prerequisites()
    native = inspect(jar, javap)
    translations = {}
    with zipfile.ZipFile(jar) as archive:
        for name in ('assets/alexscaves/lang/en_us.json', 'assets/alexscaves/lang/pt_br.json'):
            if name not in archive.namelist():
                continue
            raw = archive.read(name)
            strings = json.loads(raw)
            translations[name] = {'sha256': digest(raw), 'size_bytes': len(raw),
                                  'strings': {key: strings[key] for key in
                                              ('item.alexscaves.alex_meal', 'item.alexscaves.alex_meal.desc')
                                              if key in strings}}
    result = {'schema': 'AC_ALEX_MEAL_ITEM_CERTIFICATION_V1', 'artifact': prior[ORIGINAL]['artifact'],
              'claims': CLAIMS, 'axes': AXES, 'boundaries': BOUNDARIES, 'prerequisites': PREREQUISITES,
              'original_report_sha256': digest(canonical(original_report(native, prior)).encode()),
              'native': native, 'registry_binding': next(row for row in prior[REGISTRY_SEAL]['native']['bindings']
                                                       if row['field'] == 'ALEX_MEAL'),
              'rarity_alias': prior[REGISTRY_SEAL]['native']['support_field_initializers']['RARITY_RAINBOW'],
              'food_profile': prior[FOODS]['native']['field_profiles']['ALEX_MEAL'],
              'reference_reports': {'food': prior[FOOD_REFERENCE]['reports'], 'builder': prior[BUILDER]['reports']},
              'translations': translations, 'semantic_magic_roots_delta': 0}
    validate_contract(result, prior)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('jar', 'javap', 'seal', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and args.output.suffix == '.json', 'new JSON output required')
    sealed = load_seal(args.seal)
    validate_contract(sealed)
    actual = inspect_contract(args.jar, args.javap)
    require(actual == sealed, 'exact native certification seal mismatch')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical(actual), encoding='utf8')
    print('CERTIFICATION_SHA256', digest(args.output.read_bytes()))
    print('ALEX_MEAL_STATIC_CONTRACT_ONLY NO_MUTATION')


if __name__ == '__main__':
    main()
