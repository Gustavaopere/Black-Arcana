#!/usr/bin/env python3
"""Negative native regressions plus opt-in exact-JAR CLI idempotence (not gameplay)."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import alexscaves_1010_armor_material_audit as audit


class NativeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = audit.load_seal(audit.SEAL)
        cls.material = {(m['name'],m['descriptor']):{row['offset']:(row['opcode'],row['operand'],row['symbol'])
            for row in m['instructions']} for m in cls.seal['native_methods'][audit.MATERIAL]}

    def mutate_pivot(self, name, offset, opcode=None, operand=None, symbol=None, descriptor=None):
        methods=copy.deepcopy(self.material)
        keys=[key for key in methods if key[0]==name and (descriptor is None or key[1]==descriptor)]
        self.assertEqual(len(keys),1)
        old=methods[keys[0]][offset]
        methods[keys[0]][offset]=(old[0] if opcode is None else opcode,
            old[1] if operand is None else operand,old[2] if symbol is None else symbol)
        with self.assertRaises(audit.AuditError):
            audit.material_pivots(methods)

    def reject_report_change(self, edit):
        report=copy.deepcopy(self.seal)
        edit(report)
        with self.assertRaises(audit.AuditError):
            audit.compare_seal(report,self.seal)

    def test_complete_ten_method_declarations_and_bodies(self):
        audit.validate_report(self.seal)
        audit.material_pivots(self.material)
        self.assertEqual(len(self.material),10)
        self.assertEqual(sum(k[0]=='<init>' for k in self.material),2)
        self.assertEqual(len(self.seal['native_methods'][audit.MARKER]),0)
        for record in self.seal['native_methods'][audit.MATERIAL]:
            self.assertEqual(record['instruction_count'],len(record['instructions']))
            self.assertEqual(record['instruction_sha256'],audit.digest(audit.canonical(record['instructions']).encode()))
            self.assertEqual(record['exception_handlers'],[])

    def test_missing_overloaded_constructor_fails(self):
        methods=copy.deepcopy(self.material)
        del methods['<init>',audit.LONG_CTOR]
        with self.assertRaises(audit.AuditError):
            audit.material_pivots(methods)

    def test_clinit_cannot_be_folded_into_constructor(self):
        methods=copy.deepcopy(self.material)
        del methods['<clinit>','()V']
        with self.assertRaises(audit.AuditError):
            audit.material_pivots(methods)

    def test_short_constructor_zero_knockback_operand(self):
        self.mutate_pivot('<init>',10,opcode='fconst_1',descriptor=audit.SHORT_CTOR)

    def test_long_constructor_retains_raw_array(self):
        self.mutate_pivot('<init>',25,opcode='aconst_null',descriptor=audit.LONG_CTOR)

    def test_vanilla_enum_length_guard_target(self):
        self.mutate_pivot('vanilla',42,operand='73')

    def test_vanilla_enum_guard_opcode(self):
        self.mutate_pivot('vanilla',42,opcode='if_icmplt')

    def test_vanilla_material_enchantability_argument(self):
        self.mutate_pivot('vanilla',79,symbol='Field durability:I')

    def test_vanilla_sound_holder_bridge(self):
        self.mutate_pivot('vanilla',86,symbol='Method other.soundHolder:()V')

    def test_vanilla_empty_layer_list(self):
        self.mutate_pivot('vanilla',95,symbol='Method java/util/List.copyOf:()Ljava/util/List;')

    def test_vanilla_holder_is_direct(self):
        self.mutate_pivot('vanilla',109,symbol='Method Holder.reference:()V')

    def test_properties_multiplication(self):
        self.mutate_pivot('properties',13,opcode='iadd')

    def test_properties_array_index(self):
        self.mutate_pivot('properties',8,opcode='aaload')

    def test_defense_array_index(self):
        self.mutate_pivot('defense',8,opcode='arraylength')

    def test_null_repair_uses_empty(self):
        self.mutate_pivot('getRepairIngredient',7,symbol='Field Ingredient.OTHER:Ljava/lang/Object;')

    def test_null_repair_branch(self):
        self.mutate_pivot('getRepairIngredient',4,opcode='ifnull')

    def test_repair_setter_keeps_raw_argument(self):
        self.mutate_pivot('setRepairMaterial',1,opcode='aconst_null')

    def test_static_max_damage_constants(self):
        self.mutate_pivot('<clinit>',15,operand='15')

    def test_new_defense_guard_would_change_claim(self):
        methods=copy.deepcopy(self.material)
        key=next(k for k in methods if k[0]=='defense')
        methods[key][10]=('ifeq','9','')
        with self.assertRaises(audit.AuditError):
            audit.material_pivots(methods)

    def test_manifest_cannot_promote_physical_qa(self):
        self.reject_report_change(lambda r:r['claims'].__setitem__('physical_qa','TESTED'))

    def test_manifest_cannot_close_provider(self):
        self.reject_report_change(lambda r:r['claims'].__setitem__('provider_universe_closed',True))

    def test_manifest_cannot_invent_magic_root(self):
        self.reject_report_change(lambda r:r['claims'].__setitem__('semantic_magic_roots_delta',1))

    def test_manifest_repair_supplier_cannot_be_frozen(self):
        self.reject_report_change(lambda r:r.__setitem__('material_supplier_bootstrap',[]))

    def test_manifest_literal_material_parameter_drift(self):
        self.reject_report_change(lambda r:r['material_definitions'][0].__setitem__('durability_multiplier',21))

    def test_marker_cannot_acquire_dispatch(self):
        self.reject_report_change(lambda r:r['marker'].__setitem__('typed_dispatch_references',['invented']))

    def test_actual_dispatch_interface_must_stay_distinct(self):
        self.reject_report_change(lambda r:r['marker']['actual_tick_dispatch'].__setitem__('receiver_interface',audit.MARKER))

    def test_whole_jar_typed_census_not_raw_search(self):
        self.assertEqual(self.seal['typed_reference_census']['class_entries_scanned'],1555)
        owners={r['owner'] for r in self.seal['typed_reference_census']['targets'][audit.MATERIAL]}
        self.assertEqual(owners,{audit.MATERIAL,audit.REGISTRY,*audit.CONSUMERS})
        marker=self.seal['typed_reference_census']['targets'][audit.MARKER]
        self.assertEqual({r['owner'] for r in marker},{audit.MARKER,audit.CONSUMERS[0]})
        self.assertEqual(sum(r['implements_directly'] for r in marker),1)

    def test_typed_census_rejects_string_false_positive(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,audit.MATERIAL),(8,1)]  # Literal string, not class/descriptor.
        reader.fields=[];reader.methods=[]
        self.assertEqual(reader.typed_refs(audit.MATERIAL),[])
        reader.pool.append((7,1))
        self.assertEqual(reader.typed_refs(audit.MATERIAL),[{'kind':'class_constant','index':3}])

    def test_typed_census_includes_declared_descriptors(self):
        reader=audit.ClassReader.__new__(audit.ClassReader)
        reader.pool=[None,(1,'unused')]
        reader.fields=[{'name':'material','descriptor':'L'+audit.MATERIAL+';'}];reader.methods=[]
        self.assertEqual(reader.typed_refs(audit.MATERIAL),[{'kind':'field_declaration',
            'name':'material','descriptor':'L'+audit.MATERIAL+';'}])

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'duplicate.json';path.write_text('{"schema_version":1,"schema_version":1}')
            with self.assertRaises(audit.AuditError):
                audit.load_seal(path)

    def test_truncated_class_rejected(self):
        with self.assertRaises(audit.AuditError):
            audit.ClassReader(b'\xca\xfe\xba\xbe\x00')

    def test_artifact_size_rejected_before_disassembly(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.jar';path.write_bytes(b'not publisher')
            with self.assertRaisesRegex(audit.AuditError,'size mismatch'):
                audit.verify_artifact(path)

    def test_artifact_digest_rejected_at_exact_size(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.jar'
            with path.open('wb') as handle:
                handle.truncate(audit.SIZE)
            with self.assertRaisesRegex(audit.AuditError,'digest mismatch'):
                audit.verify_artifact(path)

    def test_cli_requires_explicit_physical_inputs(self):
        result=subprocess.run([sys.executable,str(Path(audit.__file__))],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('--jar',result.stderr)

    def test_cli_rejects_overwriting_seal(self):
        result=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar','absent.jar','--javap','absent',
            '--output',str(audit.SEAL)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('overwrite',result.stderr)


@unittest.skipUnless(os.environ.get('AC_ARMOR_JAR'),'set AC_ARMOR_JAR and AC_ARMOR_JAVAP for physical-binary CLI reproduction')
class PhysicalBinaryCLI(unittest.TestCase):
    def test_twice_run_cli_is_identical_and_preserves_inputs(self):
        jar=Path(os.environ['AC_ARMOR_JAR'])
        javap=Path(os.environ['AC_ARMOR_JAVAP'])
        seal_before=audit.SEAL.read_bytes()
        source_before=Path(audit.__file__).read_bytes()
        jar_size_before=jar.stat().st_size
        audit.verify_artifact(jar)
        with tempfile.TemporaryDirectory() as folder:
            outputs=[]
            for index in range(2):
                output=Path(folder)/f'evidence-{index}.json'
                result=subprocess.run([sys.executable,str(Path(audit.__file__)),'--jar',str(jar),'--javap',str(javap),
                    '--seal',str(audit.SEAL),'--output',str(output)],capture_output=True,text=True,timeout=180)
                self.assertEqual(result.returncode,0,result.stderr)
                outputs.append(output.read_bytes())
            self.assertEqual(outputs[0],outputs[1])
            self.assertEqual(outputs[0],seal_before)
        self.assertEqual(audit.SEAL.read_bytes(),seal_before)
        self.assertEqual(Path(audit.__file__).read_bytes(),source_before)
        self.assertEqual(jar.stat().st_size,jar_size_before)
        audit.verify_artifact(jar)


if __name__=='__main__':
    unittest.main()
