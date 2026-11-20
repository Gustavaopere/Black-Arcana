#!/usr/bin/env python3
"""Reject unsupported Alex Meal claims and reproduce the exact item certificate."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from alexscaves_1010_armor_material_audit import AuditError, load_seal
from alexscaves_1010_alex_meal_item_certification import (
    AXES, CLAIMS, PREREQUISITES, PROVIDER, ROOT, SEAL, prerequisites, validate_contract,
)


class AlexMealCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = load_seal(SEAL)
        cls.prior = prerequisites()

    def reject(self, change):
        data = copy.deepcopy(self.seal)
        change(data)
        with self.assertRaises(AuditError):
            validate_contract(data, self.prior)

    def test_complete_certificate(self):
        validate_contract(self.seal, self.prior)
        self.assertEqual(len(self.seal['native']['methods']), 2)

    def test_claims_are_static_and_fail_closed(self):
        for key, value in {'runtime_dispatch': 'VERIFIED', 'mutating_hook': 'VERIFIED',
                           'physical_qa': 'TESTED', 'perk_certification': 'CERTIFIED',
                           'provider_universe_closed': True, 'mutation': 'MUTATE',
                           'semantic_magic_roots_delta': 1}.items():
            with self.subTest(key=key):
                self.reject(lambda data, k=key, v=value: data['claims'].update({k: v}))
        self.assertEqual(self.seal['claims'], CLAIMS)

    def test_downstream_effect_acceptance_cannot_be_promoted(self):
        self.reject(lambda data: data['boundaries'].update(effect_application_acceptance='VERIFIED'))

    def test_prerequisites_cannot_be_replaced_by_mutable_or_missing_versions(self):
        self.assertEqual(self.seal['prerequisites'], PREREQUISITES)
        self.reject(lambda data: data['prerequisites'].update({next(iter(PREREQUISITES)): 'main'}))

    def test_complete_own_method_surface_cannot_be_shortened(self):
        self.reject(lambda data: data['native']['methods'].pop())

    def test_unobserved_override_cannot_hide_in_the_interface_surface(self):
        self.reject(lambda data: data['native']['declarations'].append({'name': 'finishUsingItem'}))

    def test_constructor_cannot_be_relabelled_as_instant_consumption(self):
        self.reject(lambda data: data['native']['methods'][0]['instructions'][0].update(opcode='return'))

    def test_registry_id_and_factory_are_not_inferred_from_class_name(self):
        self.reject(lambda data: data['registry_binding'].update(resource_location='alexscaves:alex_meal_item'))
        self.reject(lambda data: data['registry_binding']['factory'].update(name='lambda$static$195'))

    def test_rainbow_is_an_alias_not_a_new_rarity(self):
        self.assertEqual(self.seal['rarity_alias']['value']['name'], 'EPIC')
        self.reject(lambda data: data['rarity_alias']['value'].update(name='RAINBOW'))

    def test_nutrition_and_saturation_are_separate_inputs(self):
        self.reject(lambda data: data['food_profile'].update(nutrition=400))
        self.reject(lambda data: data['food_profile']['saturation_modifier'].update(value=400))

    def test_bowl_does_not_imply_fast_or_always_edible(self):
        self.assertEqual(self.seal['food_profile']['flags'], ['bowl'])
        self.reject(lambda data: data['food_profile']['flags'].append('alwaysEat'))

    def test_effect_identity_duration_probability_and_order_are_fixed(self):
        for field, value in [('field_name', 'DAMAGE_BOOST'), ('duration_ticks', 48000)]:
            with self.subTest(field=field):
                self.reject(lambda data, k=field, v=value: data['food_profile']['effects'][0].update({k: v}))
        self.reject(lambda data: data['food_profile']['effects'][1]['probability'].update(value=0.5))
        self.reject(lambda data: data['food_profile']['effects'].reverse())

    def test_recipe_keeps_both_crumb_entries(self):
        self.reject(lambda data: data['native']['resources']['data/alexscaves/recipe/alex_meal.json']['json']['ingredients'].pop())

    def test_provider_tooltip_is_not_replaced_with_an_invented_effect_description(self):
        self.reject(lambda data: data['translations']['assets/alexscaves/lang/en_us.json']['strings'].update(
            {'item.alexscaves.alex_meal.desc': 'Heals 40 health'}))

    def test_new_item_is_not_a_new_spell_root(self):
        self.reject(lambda data: data.update(semantic_magic_roots_delta=1))


class AlexMealPublishedRecord(unittest.TestCase):
    def test_ledger_has_local_seven_axis_evidence_with_independent_states(self):
        ledger = json.loads((ROOT/'wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json').read_text())
        entry = ledger['objects'][PROVIDER.name+'/items/alex-meal.md']
        self.assertEqual(entry['status'], 'COMPLETE_PERK_READY')
        self.assertEqual(entry['claim_scope'], 'STATIC_TECHNICAL_CATALOG_ONLY')
        self.assertEqual(entry['evidence_grade'], 'SHA_EXACT_BINARY_BEHAVIOR')
        self.assertEqual(set(entry['evidence']), set(AXES))
        for evidence in entry['evidence'].values():
            self.assertTrue((ROOT/evidence['path']).is_file())
            self.assertTrue(evidence['reason'])
        for key in ('mutation', 'runtime_dispatch', 'mutating_hook', 'physical_qa',
                    'perk_certification', 'provider_universe_closed'):
            self.assertEqual(entry[key], CLAIMS[key])
        self.assertNotIn(PROVIDER.name, ledger['providers'])

    def test_alphabetical_prefix_is_contiguous_and_item_is_not_an_extra_api_support(self):
        inventory = json.loads((PROVIDER/'INTEGRATION-SCOPE-INVENTORY-1.0.10.json').read_text())
        support = inventory['integration_support_inventory']
        prefix = support['reviewed_prefix']
        roster = inventory['remaining_family_inventory']['item_outer_classes']
        self.assertEqual([row['class'] for row in prefix], roster[:len(prefix)])
        entry = next(row for row in prefix if row['class']=='server/item/AlexMealItem')
        self.assertEqual(entry['card'], 'items/alex-meal.md')
        self.assertEqual(entry['semantic_magic_roots_added'], 0)
        self.assertEqual(support['next_alphabetical_uncovered_scope'], roster[len(prefix)])
        self.assertEqual(inventory['next_alphabetical_uncovered_scope'], roster[len(prefix)])
        self.assertIn('items/alex-meal.md', inventory['family_catalog_status']['item_contracts']['cards'])
        self.assertNotIn('items/alex-meal.md', inventory['family_catalog_status']['integration_support']['cards'])
        self.assertFalse(inventory['whole_provider_catalog_closed'])

    def test_item_index_distinguishes_static_contract_hooks_and_qa(self):
        text = (PROVIDER/'items/INDEX.md').read_text()
        row = next(line for line in text.splitlines() if '[ficha/alex-meal.md](alex-meal.md)' in line)
        self.assertTrue(row.startswith('| ✅ |'))
        self.assertIn('✅ certificado', row)
        self.assertIn('⚠️ não verificado', row)
        self.assertIn('⚠️ não testado', row)


@unittest.skipUnless(os.environ.get('AC_MEAL_JAR') and os.environ.get('AC_MEAL_JAVAP'),
                     'exact publisher/JDK paths required; mandatory in certificate CI')
class AlexMealBinaryReplay(unittest.TestCase):
    def cli(self, output, jar=None, seal=SEAL):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('alexscaves_1010_alex_meal_item_certification.py')),
                               '--jar', str(jar or os.environ['AC_MEAL_JAR']), '--javap', os.environ['AC_MEAL_JAVAP'],
                               '--seal', str(seal), '--output', str(output)], capture_output=True, text=True, timeout=150)

    def test_two_binary_cli_runs_reproduce_seal_and_preserve_inputs(self):
        paths = [Path(os.environ['AC_MEAL_JAR']), Path(os.environ['AC_MEAL_JAVAP']), SEAL,
                 *(PROVIDER/name for name in PREREQUISITES)]
        before = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
        with tempfile.TemporaryDirectory() as temporary:
            a, b = Path(temporary)/'first.json', Path(temporary)/'second.json'
            for output in (a, b):
                proc = self.cli(output)
                self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(json.loads(a.read_text()), load_seal(SEAL))
        self.assertEqual(before, {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths})

    def test_wrong_publisher_cannot_produce_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            jar, output = Path(temporary)/'wrong.jar', Path(temporary)/'out.json'
            jar.write_bytes(b'wrong publisher')
            self.assertNotEqual(self.cli(output, jar=jar).returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(jar.read_bytes(), b'wrong publisher')

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'existing.json'
            output.write_text('preserve evidence')
            self.assertNotEqual(self.cli(output).returncode, 0)
            self.assertEqual(output.read_text(), 'preserve evidence')


if __name__ == '__main__':
    unittest.main()
