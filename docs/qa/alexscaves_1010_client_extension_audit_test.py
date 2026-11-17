#!/usr/bin/env python3
"""Native negative regressions and opt-in exact-JAR CLI reproduction; no gameplay."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import alexscaves_1010_armor_material_audit as shared
import alexscaves_1010_client_extension_audit as audit


def body(method):
    return {row['offset']:(row['opcode'],row['operand'],row['symbol']) for row in method['instructions']}


class NativeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=audit.load_seal(audit.SEAL)
        cls.outputs={owner:{(method['name'],method['descriptor']):body(method) for method in methods}
            for owner,methods in cls.seal['native_methods'].items()}

    def reject_report_change(self,edit):
        changed=copy.deepcopy(self.seal)
        edit(changed)
        with self.assertRaises(audit.AuditError):
            audit.compare_seal(changed,self.seal)

    def reject_output_pivot(self,owner,name,offset,opcode=None,operand=None,symbol=None):
        outputs=copy.deepcopy(self.outputs)
        key=next(key for key in outputs[owner] if key[0]==name)
        old=outputs[owner][key][offset]
        outputs[owner][key][offset]=(old[0] if opcode is None else opcode,
            old[1] if operand is None else operand,old[2] if symbol is None else symbol)
        with self.assertRaises(audit.AuditError):
            audit.output_pivots(outputs)

    def test_unchanged_shared_parsers_are_reused(self):
        self.assertIs(audit.ClassReader,shared.ClassReader)
        self.assertIs(audit.parse_javap,shared.parse_javap)

    def test_seal_has_complete_callback_and_finite_output_bodies(self):
        audit.validate_report(self.seal)
        audit.output_pivots(self.outputs)
        self.assertEqual(len(self.seal['callbacks']),19)
        for callback in self.seal['callbacks']:
            method=callback['method']
            self.assertEqual(method['instruction_count'],6)
            self.assertEqual(method['code_size'],16)
            self.assertEqual(method['exception_handlers'],[])
            audit.callback_pivots(callback['owner'],body(method))
        self.assertEqual(set(self.outputs),set(audit.SELECTED))
        for owner,methods in self.outputs.items():
            self.assertEqual(set(methods),audit.SELECTED[owner])

    def test_abstract_declaration_is_not_an_executable_body(self):
        interface=self.seal['interface_contract']
        self.assertFalse(interface['executable_code'])
        self.assertEqual(interface['declared_methods'],[{'access':1025,'name':audit.CALLBACK[0],'descriptor':audit.CALLBACK[1]}])
        self.assertEqual(interface['generic_signature'],audit.GENERIC)
        self.reject_report_change(lambda r:r['interface_contract'].__setitem__('executable_code',True))

    def test_callback_getter_groups_are_twelve_six_one(self):
        native=[r for r in self.seal['callbacks'] if r['owner']!=audit.CITADEL_ITEM]
        self.assertEqual(sum(r['proxy_getter']=='getISTERProperties' for r in native),12)
        self.assertEqual(sum(r['proxy_getter']=='getArmorProperties' for r in native),6)
        relocated=next(r for r in self.seal['callbacks'] if r['owner']==audit.CITADEL_ITEM)
        self.assertEqual(relocated['proxy_getter_owner'],audit.CITADEL_PROXY)
        self.assertEqual(relocated['proxy_field_owner'],audit.PREFIX+'citadel/Citadel')

    def test_callback_consumer_receiver_is_original_parameter(self):
        callback=self.seal['callbacks'][0]
        changed=body(callback['method']);changed[0]=('aload_0','','')
        with self.assertRaises(audit.AuditError):
            audit.callback_pivots(callback['owner'],changed)

    def test_callback_requires_typed_proxy_getter(self):
        callback=self.seal['callbacks'][0]
        changed=body(callback['method']);changed[4]=('invokevirtual','#22','Method other.getISTERProperties:()Ljava/lang/Object;')
        with self.assertRaises(audit.AuditError):
            audit.callback_pivots(callback['owner'],changed)

    def test_callback_requires_extension_cast(self):
        callback=self.seal['callbacks'][0]
        changed=body(callback['method']);changed[7]=('checkcast','#28','class java/lang/Object')
        with self.assertRaises(audit.AuditError):
            audit.callback_pivots(callback['owner'],changed)

    def test_callback_requires_consumer_accept_descriptor(self):
        callback=self.seal['callbacks'][0]
        changed=body(callback['method']);changed[10]=('invokeinterface','#30, 2','InterfaceMethod java/util/function/Consumer.accept:()V')
        with self.assertRaises(audit.AuditError):
            audit.callback_pivots(callback['owner'],changed)

    def test_callback_cannot_add_a_second_call_or_guard(self):
        callback=self.seal['callbacks'][0]
        changed=body(callback['method']);changed[14]=('ifeq','15','')
        with self.assertRaises(audit.AuditError):
            audit.callback_pivots(callback['owner'],changed)

    def test_native_proxy_property_allocations_and_field_lifetime(self):
        self.reject_output_pivot(audit.CLIENT,'<init>',5,opcode='aconst_null')
        self.reject_output_pivot(audit.CLIENT,'getArmorProperties',1,symbol='Field other:Ljava/lang/Object;')

    def test_common_proxy_null_is_not_client_success(self):
        self.reject_output_pivot(audit.COMMON,'getISTERProperties',0,opcode='aload_0')
        self.reject_output_pivot(audit.CITADEL_PROXY,'getISTERProperties',0,opcode='aload_0')

    def test_native_renderer_is_new_per_getter(self):
        self.reject_output_pivot(audit.ITEM_PROPERTIES,'getCustomRenderer',0,opcode='getstatic')
        self.reject_output_pivot(audit.ITEM_PROPERTIES,'getCustomRenderer',4,symbol='Method other."<init>":()V')

    def test_citadel_properties_are_new_and_renderer_is_stored(self):
        self.reject_output_pivot(audit.CITADEL_CLIENT,'getISTERProperties',0,opcode='getstatic')
        self.reject_output_pivot(audit.CITADEL_PROPERTIES,'<init>',12,symbol='Field another:Ljava/lang/Object;')
        self.reject_output_pivot(audit.CITADEL_PROPERTIES,'getCustomRenderer',1,opcode='new')

    def test_armor_slot_argument_cannot_be_used(self):
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'getHumanoidArmorModel',2,operand='3')
        self.reject_report_change(lambda r:r['extension_outputs'].__setitem__('slot_argument_used',True))

    def test_armor_initializer_gate_and_flag_order(self):
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'getACArmorModelBase',3,opcode='ifeq')
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'initializeModels',0,opcode='iconst_0')
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'initializeModels',17,symbol='Method EntityModelSet.other:()V')

    def test_six_armor_model_branches_and_fallback_are_exact(self):
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'getACArmorModelBase',16,operand='37')
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'getACArmorModelBase',89,symbol='Field PRIMORDIAL_ARMOR_MODEL:Ljava/lang/Object;')
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'getACArmorModelBase',93,opcode='aconst_null')
        self.assertEqual(len(self.seal['extension_outputs']['armor_model_roster']),6)

    def test_armor_animation_null_guard_and_finite_delegation(self):
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'applyACArmorAnimations',1,opcode='ifnull')
        self.reject_output_pivot(audit.ARMOR_PROPERTIES,'applyACArmorAnimations',56,symbol='Method HazmatArmorModel.withAnimations:()V')

    def test_twenty_typed_owners_and_twenty_three_declarations_are_not_callers(self):
        census=self.seal['typed_reference_census']
        self.assertEqual(census['class_entries_scanned'],1555)
        self.assertEqual(len(census['target_owners']),20)
        self.assertEqual(len(census['initialize_client_declarations']),23)
        self.assertEqual(census['initialize_client_member_references'],[])
        self.assertEqual(census['registration_event_typed_owners'],[])
        self.reject_report_change(lambda r:r['typed_reference_census']['initialize_client_member_references'].append({'owner':'invented'}))
        self.reject_report_change(lambda r:r['typed_reference_census']['registration_event_typed_owners'].append('invented'))

    def test_inherited_spears_resolve_to_existing_body(self):
        hierarchy=self.seal['typed_reference_census']['assignability_census']
        self.assertEqual(len(hierarchy['direct_implementers']),19)
        self.assertEqual(len(hierarchy['inherited_implementers']),3)
        self.assertEqual(len(hierarchy['concrete_assignable']),22)
        self.assertEqual({r['owner'] for r in hierarchy['inherited_implementers']},set(audit.INHERITED))
        self.assertTrue(all(r['callback_declaring_owner']==audit.ITEM+'SpearItem' and r['declared_callbacks']==[] for r in hierarchy['inherited_implementers']))
        self.assertTrue(set(audit.INHERITED)<=set(self.seal['class_sha256']))
        self.assertTrue(set(audit.INHERITED).isdisjoint(r['owner'] for r in self.seal['callbacks']))
        self.reject_report_change(lambda r:r['typed_reference_census']['assignability_census']['inherited_implementers'][0].__setitem__('callback_declaring_owner','invented'))

    def test_memberref_scan_rejects_utf8_name_and_declaration_false_positives(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,'initializeClient'),(8,1)]
        reader.methods=[{'name':'initializeClient','descriptor':audit.CALLBACK[1]}]
        self.assertEqual(audit.initialize_member_references(reader),[])

    def test_memberref_scan_covers_external_owner_and_arbitrary_descriptor(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,'external/Item'),(7,1),(1,'initializeClient'),(1,'()V'),(12,(3,4)),(10,(2,5)),(11,(2,5))]
        refs=audit.initialize_member_references(reader)
        self.assertEqual(len(refs),2)
        self.assertEqual({r['kind'] for r in refs},{'method_reference','interface_method_reference'})
        self.assertTrue(all(r['receiver_owner']=='external/Item' and r['descriptor']=='()V' for r in refs))

    def test_no_runtime_or_provider_promotion(self):
        for key,value in (('physical_qa','PASS'),('mutating_hook','VERIFIED'),('perk_certification','CERTIFIED'),
                ('provider_universe_closed',True),('semantic_magic_roots_delta',1)):
            self.reject_report_change(lambda r,k=key,v=value:r['claims'].__setitem__(k,v))
        self.reject_report_change(lambda r:r['registration_boundary'].__setitem__('registration_execution','VERIFIED'))

    def test_property_outputs_cannot_be_silently_expanded(self):
        self.reject_report_change(lambda r:r['native_methods'][audit.ARMOR_PROPERTIES].append({'name':'renderCustomArmor','descriptor':'()V'}))

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'duplicate.json';path.write_text('{"schema_version":1,"schema_version":1}')
            with self.assertRaises(audit.AuditError):
                audit.load_seal(path)

    def test_wrong_artifact_rejected_before_disassembly(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.jar';path.write_bytes(b'not publisher')
            with self.assertRaisesRegex(audit.AuditError,'size mismatch'):
                audit.verify_artifact(path)
            with path.open('wb') as handle:
                handle.truncate(audit.SIZE)
            with self.assertRaisesRegex(audit.AuditError,'digest mismatch'):
                audit.verify_artifact(path)

    def test_cli_requires_explicit_inputs(self):
        result=subprocess.run([sys.executable,str(Path(audit.__file__))],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('--jar',result.stderr)

    def test_cli_cannot_overwrite_canonical_or_shared_inputs(self):
        for path in (audit.SEAL,Path(audit.__file__),Path(shared.__file__),
                Path(sys.modules[audit.parse_javap.__module__].__file__),Path('absent.jar'),Path('absent')):
            result=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar','absent.jar','--javap','absent',
                '--output',str(path)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('overwrite',result.stderr)


@unittest.skipUnless(os.environ.get('AC_CLIENT_EXTENSION_JAR') and os.environ.get('AC_CLIENT_EXTENSION_JAVAP'),
    'set AC_CLIENT_EXTENSION_JAR and AC_CLIENT_EXTENSION_JAVAP for physical-binary CLI reproduction')
class PhysicalBinaryCLI(unittest.TestCase):
    def test_twice_run_cli_is_identical_and_preserves_inputs(self):
        jar=Path(os.environ['AC_CLIENT_EXTENSION_JAR'])
        javap=Path(os.environ['AC_CLIENT_EXTENSION_JAVAP'])
        protected={path:path.read_bytes() for path in (audit.SEAL,Path(audit.__file__),Path(shared.__file__))}
        before_stat=jar.stat()
        audit.verify_artifact(jar)
        with tempfile.TemporaryDirectory() as folder:
            paths=[Path(folder)/'one.json',Path(folder)/'two.json']
            for path in paths:
                result=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar',str(jar),'--javap',str(javap),
                    '--output',str(path)],capture_output=True,text=True,timeout=180)
                self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(paths[0].read_bytes(),paths[1].read_bytes())
            self.assertEqual(paths[0].read_bytes(),protected[audit.SEAL])
        for path,raw in protected.items():
            self.assertEqual(path.read_bytes(),raw)
        self.assertEqual((jar.stat().st_size,jar.stat().st_mtime_ns),(before_stat.st_size,before_stat.st_mtime_ns))
        audit.verify_artifact(jar)


if __name__=='__main__':
    unittest.main()
