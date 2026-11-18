#!/usr/bin/env python3
"""Native semantic negatives and exact-JAR CLI reproduction; no gameplay."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import alexscaves_1010_destroyed_item_contract_audit as audit


def bodies(seal):
    return {owner:{(m['name'],m['descriptor']):{r['offset']:(r['opcode'],r['operand'],r['symbol'])
        for r in m['instructions']} for m in methods} for owner,methods in seal['native_methods'].items()}


class NativeContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=audit.load_seal(audit.SEAL)
        cls.parsed=bodies(cls.seal)

    def reject_pivot(self,owner,name,offset,opcode=None,operand=None,symbol=None):
        parsed=copy.deepcopy(self.parsed)
        key=next(key for key in parsed[owner] if key[0]==name)
        old=parsed[owner][key][offset]
        parsed[owner][key][offset]=(old[0] if opcode is None else opcode,
            old[1] if operand is None else operand,old[2] if symbol is None else symbol)
        with self.assertRaises(audit.AuditError):
            audit.native_pivots(parsed)

    def reject_seal_change(self,edit):
        changed=copy.deepcopy(self.seal)
        edit(changed)
        with self.assertRaises(audit.AuditError):
            audit.compare_seal(changed,self.seal)

    def test_valid_seal_reconciles_complete_callback_and_native_pivots(self):
        audit.validate_report(self.seal)
        audit.native_pivots(self.parsed)
        callback=next(m for m in self.seal['native_methods'][audit.IMPLEMENTER] if m['name']=='onDestroyed')
        self.assertEqual(callback['code_size'],170)
        self.assertEqual(callback['exception_handlers'],[])
        self.assertEqual(callback['instructions'][-1]['offset'],169)
        self.assertEqual(callback['branches'],[
            {'offset':10,'opcode':'ifne','target':169},{'offset':17,'opcode':'ifne','target':169}])
        declaration=self.seal['native_methods'][audit.TARGET]
        self.assertEqual(len(declaration),1)
        self.assertEqual(declaration[0]['coverage'],'ABSTRACT_DECLARATION')
        self.assertIsNone(declaration[0]['code_size'])

    def test_superclass_call_must_precede_guards(self):
        self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',3,opcode='invokevirtual')

    def test_superclass_descriptor_cannot_collapse_to_one_argument(self):
        self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',3,
            symbol='Method '+audit.PARENT+'.onDestroyed:'+audit.ONE_ARG)

    def test_missing_native_constructor_fails(self):
        parsed=copy.deepcopy(self.parsed)
        del parsed[audit.IMPLEMENTER]['<init>',audit.CTOR]
        with self.assertRaises(audit.AuditError):
            audit.native_pivots(parsed)

    def test_creative_and_removed_guard_polarity_and_target(self):
        for offset,change in [(10,{'opcode':'ifeq'}),(10,{'operand':'20'}),
                              (17,{'opcode':'ifeq'}),(17,{'operand':'20'})]:
            with self.subTest(offset=offset,change=change):
                self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',offset,**change)

    def test_discard_cannot_be_replaced_with_stack_decrement(self):
        self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',21,
            symbol='Method net/minecraft/world/item/ItemStack.shrink:(I)V')

    def test_cloud_status_payload_and_lifetime_are_distinct(self):
        for offset,change in [(88,{'operand':'12000'}),(104,{'operand':'9600'}),
            (91,{'opcode':'iconst_0'}),(111,{'opcode':'iconst_1'}),
            (99,{'opcode':'fconst_1'}),(64,{'symbol':'int 7853583'})]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',offset,**change)

    def test_numeric_operand_check_is_exact_not_substring(self):
        self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',88,operand='96000')

    def test_cloud_particle_and_status_supplier_targets(self):
        for offset in (49,74):
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',offset,symbol='Field OTHER:Ljava/util/function/Supplier;')

    def test_cloud_shrink_uses_negative_radius_over_duration(self):
        for offset,opcode in [(120,'fconst_0'),(125,'nop'),(126,'fmul')]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',offset,opcode=opcode)

    def test_cloud_submission_boolean_remains_ignored(self):
        self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',138,opcode='istore_2')

    def test_explosion_null_source_y_offset_strength_and_block_interaction(self):
        for offset,change in [(143,{'opcode':'aload_1'}),(152,{'symbol':'double 1.0d'}),
            (155,{'opcode':'dsub'}),(160,{'symbol':'float 1.9f'}),
            (162,{'symbol':'Field net/minecraft/world/level/Level$ExplosionInteraction.NONE:Lnet/minecraft/world/level/Level$ExplosionInteraction;'})]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IMPLEMENTER,'onDestroyed',offset,**change)

    def test_callback_cannot_acquire_new_side_guard(self):
        parsed=copy.deepcopy(self.parsed)
        parsed[audit.IMPLEMENTER]['onDestroyed',audit.TWO_ARG][170]=('invokevirtual','#1','Method Level.isClientSide:()Z')
        with self.assertRaises(audit.AuditError):
            audit.native_pivots(parsed)

    def test_inherited_inventory_chance_is_stored_as_field(self):
        self.reject_pivot(audit.PARENT,'<init>',8,symbol='Field OTHER:F')

    def test_inventory_rng_and_multiplier_are_separate_from_callback(self):
        for offset,change in [(52,{'opcode':'fadd'}),(62,{'symbol':'float 3.0f'}),
            (94,{'symbol':'InterfaceMethod RandomSource.nextDouble:()D'}),
            (105,{'opcode':'ifle'}),(126,{'operand':'9600'})]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.PARENT,'acInventoryTick',offset,**change)

    def test_relocated_one_argument_callback_keeps_container_condition(self):
        self.reject_pivot(audit.CITADEL,'onDestroyed',12,opcode='ifne')

    def test_cloud_color_native_bridge_keeps_empty_effect_list(self):
        self.reject_pivot(audit.COMPAT,'setCloudColor',15,symbol='InterfaceMethod java/util/List.copyOf:(Ljava/util/Collection;)Ljava/util/List;')

    def test_native_effect_bridge_keeps_mob_effect_registry(self):
        self.reject_pivot(audit.COMPAT,'effect',0,symbol='Field BuiltInRegistries.ITEM:Lnet/minecraft/core/Registry;')

    def test_status_schedule_keeps_amplifier_positive_divisor_and_phase(self):
        for offset,change in [(1,{'opcode':'ifge'}),(6,{'operand':'100'}),
            (10,{'opcode':'imul'}),(19,{'opcode':'idiv'}),(23,{'opcode':'if_icmpeq'})]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IRRADIATED,'shouldTick',offset,**change)

    def test_status_tick_raycat_rng_hazmat_and_damage_requests(self):
        for offset,change in [(8,{'symbol':'float 0.5f'}),(33,{'symbol':'float 0.8f'}),
            (42,{'opcode':'ifeq'}),(59,{'symbol':'float 0.2f'}),(63,{'opcode':'ifle'}),
            (82,{'opcode':'ireturn'})]:
            with self.subTest(offset=offset):
                self.reject_pivot(audit.IRRADIATED,'tick',offset,**change)

    def test_hazmat_identity_and_damage_registry_operands(self):
        self.reject_pivot(audit.HAZMAT,'getWornAmount',9,symbol='Field ACItemRegistry.OTHER:Ljava/util/function/Supplier;')
        self.reject_pivot(audit.DAMAGE,'causeRadiationDamage',19,symbol='Field ACID:Lnet/minecraft/resources/ResourceKey;')

    def test_positive_and_negative_factory_selection(self):
        audit.factory_pivots(self.parsed[audit.REGISTRY])
        r=self.seal['registration_bridge']
        self.assertEqual(r['destroyed_selector'],5)
        self.assertEqual([row['name'] for row in r['positive_registrations']],['waste_drum'])
        self.assertEqual([row['name'] for row in r['negative_registrations']],
            ['radrock_uranium_ore','block_of_uranium','unrefined_waste'])
        self.assertEqual(r['explicit_three_argument_registration_count'],43)
        self.assertEqual(r['selector_switch']['5'],87)
        self.assertEqual(r['selector_switch']['4'],80)

    def test_factory_cannot_swap_radioactive_and_destroyed_classes_or_chances(self):
        for name,offset,change in [
            ('lambda$getBlockSupplier$441',0,{'symbol':'class '+audit.PARENT}),
            ('lambda$getBlockSupplier$441',8,{'symbol':'float 0.001f'}),
            ('lambda$getBlockSupplier$440',0,{'symbol':'class '+audit.IMPLEMENTER}),
            ('lambda$getBlockSupplier$440',8,{'symbol':'float 0.01f'}),
            ('getBlockSupplier',88,{'symbol':'InvokeDynamic #7:get:'+audit.FACTORY})]:
            with self.subTest(name=name,offset=offset):
                methods=copy.deepcopy(self.parsed[audit.REGISTRY])
                body=audit.named(methods,name)
                old=body[offset]
                body[offset]=(old[0],old[1],change['symbol'])
                with self.assertRaises(audit.AuditError):
                    audit.factory_pivots(methods)

    def test_supplier_bootstrap_cannot_point_at_wrong_factory(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.attributes={'bootstrap_methods':[{} for _ in range(9)]}
        bootstrap=copy.deepcopy(self.seal['registration_bridge']['supplier_bootstraps'][1])
        bootstrap.pop('index')
        reader.attributes['bootstrap_methods'][8]=bootstrap
        audit.bootstrap_target(reader,8,audit.REGISTRY,'lambda$getBlockSupplier$441')
        ref=next(arg for arg in bootstrap['arguments'] if isinstance(arg,dict))
        ref['reference'][2][1]='lambda$getBlockSupplier$440'
        with self.assertRaises(audit.AuditError):
            audit.bootstrap_target(reader,8,audit.REGISTRY,'lambda$getBlockSupplier$441')

    def test_switch_parser_rejects_swapped_cases(self):
        raw='private static java.util.function.Supplier<X> getBlockSupplier(int, java.util.function.Supplier<X>);\n'
        raw+=' descriptor: '+audit.FACTORY+'\n Code:\n 0: iload_0\n 1: tableswitch { // 1 to 9\n'
        switch=self.seal['registration_bridge']['selector_switch']
        cases=''.join(f' {key}: {target}\n' for key,target in switch.items())+' }\n'
        self.assertEqual(audit.parse_factory_switch(raw+cases),switch)
        with self.assertRaises(audit.AuditError):
            audit.parse_factory_switch(raw+cases.replace('5: 87','5: 80'))

    def test_missing_factory_switch_case_rejected(self):
        with self.assertRaises(audit.AuditError):
            audit.parse_factory_switch('')

    def test_all_global_declarations_and_member_reference_rosters(self):
        c=self.seal['typed_reference_census']
        self.assertEqual(len(c['on_destroyed_declarations']),3)
        self.assertEqual(len(c['on_destroyed_member_references']),1)
        self.assertEqual(c['inherited_implementers_within_publisher'],[])
        self.assertEqual(c['direct_implementers'],[audit.IMPLEMENTER])

    def test_census_rejects_missing_overload_or_new_member_caller(self):
        for key,edit in [('on_destroyed_declarations',lambda rows:rows.pop()),
            ('on_destroyed_member_references',lambda rows:rows.append(copy.deepcopy(rows[0]))),
            ('inherited_implementers_within_publisher',lambda rows:rows.append('external/Invented'))]:
            with self.subTest(key=key):
                census=copy.deepcopy(self.seal['typed_reference_census'])
                edit(census[key])
                with self.assertRaises(audit.AuditError):
                    audit.validate_census(census)

    def test_typed_census_rejects_plain_string_false_positive(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,audit.TARGET),(8,1)]
        reader.fields=[];reader.methods=[]
        self.assertEqual(reader.typed_refs(audit.TARGET),[])
        reader.pool.append((7,1))
        self.assertEqual(reader.typed_refs(audit.TARGET),[{'kind':'class_constant','index':3}])

    def test_typed_census_captures_descriptor_and_hierarchy_is_recursive(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,'unused')]
        reader.fields=[];reader.methods=[{'name':'accept','descriptor':'(L'+audit.TARGET+';)V'}]
        self.assertEqual(reader.typed_refs(audit.TARGET)[0]['kind'],'method_declaration')
        hierarchy={'sub':{'parent':audit.IMPLEMENTER,'interfaces':[]},
            audit.IMPLEMENTER:{'parent':None,'interfaces':[audit.TARGET]}}
        self.assertTrue(audit.assignable('sub',hierarchy))
        self.assertFalse(audit.assignable('unavailable',hierarchy))
        with self.assertRaises(audit.AuditError):
            audit.assignable('cycle',{'cycle':{'parent':'cycle','interfaces':[]}})

    def test_claims_cannot_promote_gameplay_hooks_provider_or_roots(self):
        for key,value in [('physical_qa','TESTED'),('mutating_hook','VERIFIED'),
            ('provider_universe_closed',True),('semantic_magic_roots_delta',1),
            ('mutation','MUTATED')]:
            with self.subTest(key=key):
                self.reject_seal_change(lambda r:r['claims'].__setitem__(key,value))

    def test_seal_cannot_reassign_uranium_to_destroyed_factory(self):
        self.reject_seal_change(lambda r:r['registration_bridge'].__setitem__('destroyed_selector',4))

    def test_full_body_integrity_and_super_causal_bound_cannot_be_dropped(self):
        self.reject_seal_change(lambda r:r['native_methods'][audit.IMPLEMENTER][1]['instructions'].pop())
        self.reject_seal_change(lambda r:r['callback_semantics']['upstream_call'].__setitem__('causal_bound','guaranteed'))

    def test_duplicate_json_keys_and_truncated_class_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'duplicate.json'
            path.write_text('{"claims":{},"claims":{}}')
            with self.assertRaises(audit.AuditError):
                audit.load_seal(path)
        with self.assertRaises(audit.AuditError):
            audit.ClassReader(b'\xca\xfe\xba\xbe\x00')

    def test_artifact_identity_rejects_wrong_size_and_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.jar';path.write_bytes(b'wrong')
            with self.assertRaisesRegex(audit.AuditError,'size mismatch'):
                audit.verify_artifact(path)
            with path.open('wb') as handle:
                handle.truncate(audit.SIZE)
            with self.assertRaisesRegex(audit.AuditError,'digest mismatch'):
                audit.verify_artifact(path)

    def test_cli_requires_explicit_physical_inputs(self):
        proc=subprocess.run([sys.executable,str(Path(audit.__file__))],capture_output=True,text=True)
        self.assertNotEqual(proc.returncode,0)
        self.assertIn('--jar',proc.stderr)

    def test_cli_protects_seal_helpers_and_old_probe(self):
        protected=[audit.SEAL,Path(audit.__file__),Path(audit.__file__).with_name('alexscaves_1010_destroyed_item_probe.py'),
            Path(audit.__file__).with_name('alexscaves_1010_armor_material_audit.py'),
            Path(audit.__file__).with_name('alexscaves_1010_action_contract_audit.py')]
        for output in protected:
            with self.subTest(output=output.name):
                proc=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar','absent.jar',
                    '--javap','absent','--output',str(output)],capture_output=True,text=True)
                self.assertNotEqual(proc.returncode,0)
                self.assertIn('overwrite',proc.stderr)


@unittest.skipUnless(os.environ.get('AC_DESTROYED_ITEM_JAR'),
    'set AC_DESTROYED_ITEM_JAR and AC_DESTROYED_ITEM_JAVAP for exact physical-binary CLI reproduction')
class PhysicalBinaryCLI(unittest.TestCase):
    def test_twice_run_cli_is_identical_and_preserves_inputs(self):
        jar=Path(os.environ['AC_DESTROYED_ITEM_JAR'])
        javap=Path(os.environ['AC_DESTROYED_ITEM_JAVAP'])
        files=[audit.SEAL,Path(audit.__file__),
            Path(audit.__file__).with_name('alexscaves_1010_destroyed_item_probe.py'),
            Path(audit.__file__).with_name('alexscaves_1010_armor_material_audit.py'),
            Path(audit.__file__).with_name('alexscaves_1010_action_contract_audit.py')]
        before={path:path.read_bytes() for path in files}
        audit.verify_artifact(jar)
        with tempfile.TemporaryDirectory() as folder:
            outputs=[]
            for index in range(2):
                output=Path(folder)/f'evidence-{index}.json'
                proc=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar',str(jar),
                    '--javap',str(javap),'--seal',str(audit.SEAL),'--output',str(output)],
                    capture_output=True,text=True,timeout=180)
                self.assertEqual(proc.returncode,0,proc.stderr)
                outputs.append(output.read_bytes())
            self.assertEqual(outputs[0],outputs[1])
            self.assertEqual(outputs[0],before[audit.SEAL])
        for path,raw in before.items():
            self.assertEqual(path.read_bytes(),raw,path.name)
        audit.verify_artifact(jar)


if __name__=='__main__':
    unittest.main()
