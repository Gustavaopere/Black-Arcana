#!/usr/bin/env python3
"""Negative boundary checks and opt-in twice-run official-artifact CLI audit."""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import alexscaves_1010_armor_material_audit as shared
import alexscaves_1010_destroyed_item_engine_reference as audit


def body(method):
    return {r['offset']: (r['opcode'], r['operand'], r['symbol']) for r in method['instructions']}


class BoundaryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = audit.load_seal(audit.SEAL)
        cls.bridges = {b['owner']: body(b['method']) for b in cls.seal['universal_default_bridges']}

    def reject_report_change(self, edit):
        changed = copy.deepcopy(self.seal)
        edit(changed)
        with self.assertRaises(audit.AuditError):
            audit.compare_seal(changed, self.seal)

    def reject_bridge_change(self, owner, offset, value):
        changed = copy.deepcopy(self.bridges[owner])
        changed[offset] = value
        with self.assertRaises(audit.AuditError):
            audit.bridge_pivots(owner, changed)

    def patches(self):
        """Only selected active lines are needed to exercise the patch contract."""
        selected = {p['entry']: [line['text'] for line in p['selected_patch_lines']]
            for p in self.seal['userdev_source_patches']}
        for name in (audit.ITEM_PATCH, audit.STACK_PATCH):
            selected[name].insert(0, '-public class OldDeclaration {')
        return {name: ('\n'.join(lines) + '\n').encode() for name, lines in selected.items()}

    def test_unchanged_shared_parsers_are_reused(self):
        self.assertIs(audit.ClassReader, shared.ClassReader)
        self.assertIs(audit.parse_javap, shared.parse_javap)

    def test_exact_seal_keeps_only_two_defaults_and_three_source_patches(self):
        audit.validate_report(self.seal)
        self.assertEqual(len(self.seal['universal_default_bridges']), 2)
        self.assertEqual(len(self.seal['userdev_source_patches']), 3)
        for owner, instructions in self.bridges.items():
            audit.bridge_pivots(owner, instructions)
        audit.patch_pivots(self.patches())

    def test_item_bridge_preserves_virtual_one_argument_dispatch(self):
        self.reject_bridge_change(audit.ITEM, 7, ('invokespecial', '#256',
            'Method net/minecraft/world/item/Item.onDestroyed:' + audit.ONE_ARG))
        self.reject_bridge_change(audit.ITEM, 7, ('invokevirtual', '#256',
            'Method net/minecraft/world/item/Item.onDestroyed:' + audit.CALLBACK[1]))

    def test_stack_bridge_preserves_source_and_item_receiver(self):
        self.reject_bridge_change(audit.STACK, 10, ('aload_1', '', ''))
        self.reject_bridge_change(audit.STACK, 6, ('invokevirtual', '#9',
            'Method net/minecraft/world/item/ItemStack.copy:()Lnet/minecraft/world/item/ItemStack;'))
        self.reject_bridge_change(audit.STACK, 11, ('invokevirtual', '#256',
            'Method net/minecraft/world/item/Item.onDestroyed:' + audit.ONE_ARG))

    def test_bridge_cannot_add_guard_or_remove_return(self):
        self.reject_bridge_change(audit.ITEM, 9, ('ifeq', '10', ''))
        changed = copy.deepcopy(self.bridges[audit.STACK])
        del changed[14]
        with self.assertRaises(audit.AuditError):
            audit.bridge_pivots(audit.STACK, changed)

    def test_extension_name_in_comment_is_not_an_active_declaration(self):
        patches = self.patches()
        patches[audit.ITEM_PATCH] = patches[audit.ITEM_PATCH].replace(b'+public class Item', b'+// public class Item')
        with self.assertRaises(audit.AuditError):
            audit.patch_pivots(patches)

    def test_stack_must_actively_implement_stack_extension(self):
        patches = self.patches()
        patches[audit.STACK_PATCH] = patches[audit.STACK_PATCH].replace(b'IItemStackExtension', b'IItemExtension')
        with self.assertRaises(audit.AuditError):
            audit.patch_pivots(patches)

    def test_dispatch_requires_damage_source_and_health_gate(self):
        for old, new in ((b'onDestroyed(this, p_32013_)', b'onDestroyed(this)'),
                (b'if (this.health <= 0)', b'if (this.health > 0)')):
            patches = self.patches()
            patches[audit.ENTITY_PATCH] = patches[audit.ENTITY_PATCH].replace(old, new)
            with self.assertRaises(audit.AuditError):
                audit.patch_pivots(patches)

    def test_discard_cannot_move_before_callback(self):
        patches = self.patches()
        patches[audit.ENTITY_PATCH] = patches[audit.ENTITY_PATCH].replace(
            b'+                this.getItem().onDestroyed(this, p_32013_);\n                 this.discard();',
            b'                 this.discard();\n+                this.getItem().onDestroyed(this, p_32013_);')
        with self.assertRaises(audit.AuditError):
            audit.patch_pivots(patches)

    def test_source_patch_context_cannot_be_presented_as_full_engine_binary(self):
        self.reject_report_change(lambda r: r['validation'].__setitem__('derived_minecraft_jar_required', True))
        self.reject_report_change(lambda r: r['validation'].__setitem__('engine_build_or_launch_performed', True))
        self.assertIn('not a complete ItemEntity.hurt binary body', self.seal['external_boundary']['limitations'])

    def test_runtime_and_perk_status_cannot_be_promoted(self):
        for key, value in (('installed_transformed_execution', 'VERIFIED'), ('actual_gameplay_outcomes', 'VERIFIED'),
                ('physical_qa', 'PASS'), ('mutating_hook', 'VERIFIED'), ('perk_certification', 'CERTIFIED'),
                ('provider_universe_closed', True), ('semantic_magic_roots_delta', 1)):
            self.reject_report_change(lambda r, k=key, v=value: r['claims'].__setitem__(k, v))

    def test_method_cannot_be_abstract_or_drop_code_hash(self):
        self.reject_report_change(lambda r: r['universal_default_bridges'][0]['method'].__setitem__('access', 1025))
        self.reject_report_change(lambda r: r['universal_default_bridges'][1]['method'].__setitem__('code_sha256', '0'*64))

    def test_duplicate_instruction_offsets_are_rejected(self):
        def duplicate(report):
            method = report['universal_default_bridges'][0]['method']
            method['instructions'].append(copy.deepcopy(method['instructions'][0]))
            method['instruction_count'] += 1
            method['instruction_sha256'] = audit.digest(audit.canonical(method['instructions']).encode())
        self.reject_report_change(duplicate)

    def test_wrong_artifact_rejected_before_disassembly(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'wrong.jar'
            path.write_bytes(b'not NeoForge')
            with self.assertRaisesRegex(audit.AuditError, 'size mismatch'):
                audit.verify_artifact(path, 'universal')
            with path.open('wb') as handle:
                handle.truncate(audit.ARTIFACTS['userdev']['size_bytes'])
            with self.assertRaisesRegex(audit.AuditError, 'digest mismatch'):
                audit.verify_artifact(path, 'userdev')

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'duplicate.json'
            path.write_text('{"schema":1,"schema":1}')
            with self.assertRaises(audit.AuditError):
                audit.load_seal(path)

    def test_cli_requires_all_explicit_physical_inputs(self):
        result = subprocess.run([sys.executable, audit.__file__], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--universal', result.stderr)

    def test_cli_cannot_overwrite_seal_artifact_or_shared_parser(self):
        for path in (audit.SEAL, Path(audit.__file__), Path(shared.__file__),
                Path(sys.modules[audit.parse_javap.__module__].__file__), Path('missing-universal.jar')):
            result = subprocess.run([sys.executable, audit.__file__, '--universal', 'missing-universal.jar',
                '--userdev', 'missing-userdev.jar', '--javap', 'missing-javap', '--output', str(path)],
                capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('overwrite', result.stderr)


@unittest.skipUnless(all(os.environ.get(name) for name in
    ('AC_DESTROYED_ENGINE_UNIVERSAL', 'AC_DESTROYED_ENGINE_USERDEV', 'AC_DESTROYED_ENGINE_JAVAP')),
    'set AC_DESTROYED_ENGINE_UNIVERSAL/USERDEV/JAVAP for official-artifact CLI reproduction')
class PhysicalArtifactCLI(unittest.TestCase):
    def test_twice_run_is_identical_and_preserves_inputs(self):
        universal = Path(os.environ['AC_DESTROYED_ENGINE_UNIVERSAL'])
        userdev = Path(os.environ['AC_DESTROYED_ENGINE_USERDEV'])
        javap = Path(os.environ['AC_DESTROYED_ENGINE_JAVAP'])
        protected = {p: p.read_bytes() for p in (audit.SEAL, Path(audit.__file__), Path(shared.__file__),
            Path(sys.modules[audit.parse_javap.__module__].__file__))}
        before = {p: (p.stat().st_size, p.stat().st_mtime_ns) for p in (universal, userdev)}
        with tempfile.TemporaryDirectory() as folder:
            outputs = [Path(folder) / name for name in ('one.json', 'two.json')]
            for output in outputs:
                result = subprocess.run([sys.executable, audit.__file__, '--universal', str(universal),
                    '--userdev', str(userdev), '--javap', str(javap), '--output', str(output)],
                    capture_output=True, text=True, timeout=180)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            self.assertEqual(outputs[0].read_bytes(), protected[audit.SEAL])
        for path, raw in protected.items():
            self.assertEqual(path.read_bytes(), raw)
        for kind, path in (('universal', universal), ('userdev', userdev)):
            self.assertEqual((path.stat().st_size, path.stat().st_mtime_ns), before[path])
            audit.verify_artifact(path, kind)


if __name__ == '__main__':
    unittest.main()
