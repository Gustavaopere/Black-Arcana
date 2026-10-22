#!/usr/bin/env python3
"""Exact WOM catalog/ABI reference checks, without loading either mod.

This is a project-specific static audit, not an adapter or generic parser library.
Only facts/offsets are emitted. No publisher disassembly or JAR is redistributed.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-weapons-of-miracles'
MANIFEST = PROVIDER / 'skills/individual-skill-cards-2.0.178.json'
REGISTRY = 'reascer.wom.gameasset.WOMSkills'
WOM_HASHES = ('b507eb376778cfd1cbecec2841c38891b26a7349',
              '0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc', 20941584)
EPIC_HASHES = ('fb199b7bbea2fc402da28ab586e73f47e32f8fc0',
               '8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526', 8578288)
DECL = re.compile(r'^  ((?:public|protected|private)[^\n]*\([^\n]*;)\n    descriptor: (\S+)\n(.*?)(?=^  \S|^\}|\Z)', re.M | re.S)
INSTRUCTION = re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$', re.M)
ABSENT = {'avatar_of_might', 'herrscher_passive', 'lunar_echo_passive',
          'napoleon_passive', 'evil_tachi_passive', 'unbreakable_passive'}
EMPTY = {'ruine_passive', 'torment_passive', 'solar_passive'}


def methods(text: str) -> dict[tuple[str, str], str]:
    result = {}
    for match in DECL.finditer(text):
        signature, descriptor, body = match.groups()
        name = re.search(r'([^\s(]+)\(', signature)[1]
        key = (name, descriptor)
        if key in result:
            raise ValueError(f'duplicate method {key}')
        result[key] = body
    return result


def instructions(body: str) -> dict[int, tuple[str, str]]:
    result = {}
    for match in INSTRUCTION.finditer(body):
        pc, opcode, tail = match.groups()
        pc = int(pc)
        if pc in result:
            raise ValueError('duplicate instruction offset')
        result[pc] = (opcode, tail.strip())
    return result


def equal_json(actual, expected) -> bool:
    """Allow JSON integer/float numeric equality, but never bool == 0/1."""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return actual == expected
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(equal_json(actual[k], expected[k]) for k in actual)
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(equal_json(a, b) for a, b in zip(actual, expected))
    return actual == expected


def registry_links(verbose: str, cards: list[dict]) -> dict:
    if '\n  static {};\n' not in verbose or '\nBootstrapMethods:\n' not in verbose:
        raise ValueError('registry static initializer or BootstrapMethods absent')
    body = verbose.split('\n  static {};\n', 1)[1].split('\n}', 1)[0]
    insn = list(instructions(body).items())
    boots = verbose.split('\nBootstrapMethods:\n', 1)[1].split('\nInnerClasses:', 1)[0]
    stanzas = {}
    headers = list(re.finditer(r'^  (\d+):\s+#\d+\s+REF_invokeStatic[^\n]*', boots, re.M))
    for i, match in enumerate(headers):
        stanzas[int(match[1])] = boots[match.start():headers[i + 1].start() if i + 1 < len(headers) else len(boots)]
    ids = []
    for i, (pc, (opcode, tail)) in enumerate(insn):
        match = re.search(r'// String ([a-z0-9_]+)$', tail)
        if opcode not in ('ldc', 'ldc_w') or not match:
            continue
        # The namespace literal "wom" is not followed by register.
        if i + 2 < len(insn) and 'DeferredRegister.register:' in insn[i + 2][1][1]:
            ids.append(match[1])
    wanted = [c['id'].split(':', 1)[1] for c in cards]
    if len(ids) != len(set(ids)) or set(ids) != set(wanted):
        raise ValueError('registry ID set mismatch/duplicate')
    suppliers = methods(verbose)
    result = {}
    for card in cards:
        id = card['id'].split(':', 1)[1]
        spots = [i for i, (_, (op, tail)) in enumerate(insn)
                 if op in ('ldc', 'ldc_w') and re.search(r'// String ' + re.escape(id) + r'$', tail)]
        if len(spots) != 1 or spots[0] + 3 >= len(insn):
            raise ValueError(f'{id}: ID binding absent/truncated')
        i = spots[0]
        dynamic, register, holder = [insn[i + k][1] for k in (1, 2, 3)]
        boot = re.search(r'// InvokeDynamic #(\d+):apply:', dynamic[1])
        if dynamic[0] != 'invokedynamic' or not boot:
            raise ValueError(f'{id}: supplier invokedynamic missing')
        stanza = stanzas.get(int(boot[1]), '')
        cls = card['implementation_class'].replace('.', '/')
        descriptor = '(Lnet/minecraft/resources/ResourceLocation;)L' + cls + ';'
        target = REGISTRY.replace('.', '/') + '.' + card['supplier'] + ':' + descriptor
        if 'LambdaMetafactory.metafactory:' not in stanza or 'REF_invokeStatic ' + target not in stanza:
            raise ValueError(f'{id}: wrong supplier/class bootstrap')
        if (card['supplier'], descriptor) not in suppliers:
            raise ValueError(f'{id}: typed supplier declaration absent')
        if register[0] != 'invokevirtual' or 'DeferredRegister.register:' not in register[1]:
            raise ValueError(f'{id}: register call absent')
        if holder[0] != 'putstatic' or '// Field ' + card['registry_field'] + ':' not in holder[1]:
            raise ValueError(f'{id}: wrong holder')
        generic = 'DeferredHolder<yesman.epicfight.skill.Skill, ' + card['implementation_class'] + '> ' + card['registry_field'] + ';'
        if generic not in verbose:
            raise ValueError(f'{id}: holder declared type mismatch')
        result[card['id']] = {'bootstrap_index': int(boot[1]), 'supplier': card['supplier'],
                              'id_pc': insn[i][0], 'class': card['implementation_class']}
    return result


def assert_references(text: str, card: dict) -> int:
    header = f"public class {card['implementation_class']} extends {card['superclass']}"
    if header not in text:
        raise ValueError(f"{card['id']}: concrete superclass mismatch")
    all_methods = methods(text)
    count = 0
    for method in card['methods']:
        key = (method['name'], method['descriptor'])
        if key not in all_methods:
            raise ValueError(f"{card['id']}: method/descriptor absent: {key}")
        insn = instructions(all_methods[key])
        for ref in method['references']:
            op, tail = insn.get(ref['pc'], ('', ''))
            actual = re.search(r'// (?:Method|InterfaceMethod|Field) (.*)$', tail)
            if not actual or actual[1] != ref['reference'] or not op.startswith(('invoke', 'get', 'put')):
                raise ValueError(f"{card['id']}: method-bounded reference differs at {key}@{ref['pc']}")
            count += 1
    return count


def literal_fields(text: str, cls: str) -> dict:
    candidates = [b for (n, _), b in methods(text).items() if n == cls]
    if len(candidates) != 1:
        raise ValueError('constructor ambiguity')
    insn = list(instructions(candidates[0]).values())
    result = {}
    for i, (op, tail) in enumerate(insn):
        if op != 'putfield' or i == 0:
            continue
        field = re.search(r'// Field (\S+)$', tail)
        prevop, prevtail = insn[i - 1]
        value = None
        if match := re.search(r'// (float|double|int|long) (-?[\d.]+)[fdl]?$', prevtail):
            value = float(match[2]) if match[1] in ('float', 'double') else int(match[2])
        elif match := re.fullmatch(r'[fi]const_(m1|\d+)', prevop):
            value = -1 if match[1] == 'm1' else int(match[1])
        elif prevop in ('bipush', 'sipush'):
            value = int(prevtail)
        if field and value is not None:
            result[field[1]] = value
    return result


def builder_resource(supplier: str, concrete: str) -> str:
    """Follow the bounded factory choices used by this exact registrar."""
    resource = 'NONE'
    if '.createDodgeBuilder:' in supplier:
        resource = 'STAMINA'
    elif '.createWeaponInnateBuilder:' in supplier or '.createConditionalWeaponInnateBuilder:' in supplier:
        resource = 'WEAPON_CHARGE'
    elif '.createCounterAttackBuilder:' in supplier:
        factories = [body for (name, _), body in methods(concrete).items()
                     if name == 'createCounterAttackBuilder']
        if len(factories) != 1 or 'GuardSkill.createGuardBuilder:' not in factories[0]:
            raise ValueError('custom guard factory not resolved')
        resource = 'STAMINA'
    elif '.createRavangerForceBuilder:' in supplier:
        factories = [body for (name, _), body in methods(concrete).items()
                     if name == 'createRavangerForceBuilder']
        if len(factories) != 1 or 'Skill$Resource.STAMINA:' not in factories[0]:
            raise ValueError('custom dodge resource not resolved')
        resource = 'STAMINA'
    elif '.createBuilder:' not in supplier:
        raise ValueError('unrecognized builder factory')
    overrides = re.findall(r'// Field [^\n]*Skill\$Resource\.([A-Z_]+):', supplier)
    if overrides:
        if len(overrides) != 1 or '.setResource:' not in supplier:
            raise ValueError('ambiguous supplier resource override')
        resource = overrides[0]
    return resource


# Very narrow operand/reference windows. These check the documented operands at
# selected call sites, not arbitrary constants anywhere in a class or CFG truth.
OPERANDS = {
    'time_travel': ('executeOnServer', {27: 'float 12.0f', 29: 'PlayerPatch.consumeForSkill:'}),
    'avatar_of_might': ('lambda$onInitiate$0', {117: 'float 12.0f', 119: 'PlayerPatch.consumeForSkill:', 420: 'double 20.0d', 423: 'double 20.0d', 426: 'double 20.0d', 429: 'AABB.ofSize:'}),
    'voodoo_magic': ('updateContainer', {407: 'float -1.5f', 409: 'PlayerPatch.consumeForSkill:'}),
    'heart_shield': ('updateContainer', {153: 'WOMSkillDataKeys.MAX_SHIELD:', 156: '20', 161: 'SkillDataManager.setDataSync:', 211: 'AttributeModifier$Operation.ADD_VALUE:', 214: 'AttributeModifier."<init>":'}),
    'vampirize': ('lambda$onInitiate$0', {11: 'DealDamageEvent$Post.getModifiedDamage:', 14: 'float 0.2f', 17: 'Player.heal:'}),
    'spider_techniques': ('loadDatapackParameters', {2: 'Skill.loadDatapackParameters:', 6: 'float 0.2f', 8: 'Field consumption:F'}),
    'perfect_bulwark': ('updateContainer', {847: 'double 20.0d', 850: 'double 20.0d', 853: 'double 20.0d', 856: 'AABB.ofSize:'}),
    'proximity_exploiter': ('updateContainer', {28: 'double 20.0d', 31: 'double 20.0d', 34: 'double 20.0d', 37: 'AABB.ofSize:'}),
    'demonic_ascension': ('updateContainer', {4238: 'double 50.0d', 4241: 'double 50.0d', 4244: 'double 50.0d', 4247: 'AABB.ofSize:'}),
    'charybdis': ('executeOnServer', {5: 'Skill$Resource.STAMINA:', 9: 'Field consumption:F', 12: 'PlayerPatch.consumeForSkill:'}),
}


def check_operands(text: str, method: str, expected: dict[int, str]):
    bodies = [b for (name, _), b in methods(text).items() if name == method]
    if len(bodies) != 1:
        raise ValueError('operand method ambiguous/absent')
    insn = instructions(bodies[0])
    for pc, fragment in expected.items():
        if fragment not in insn.get(pc, ('', ''))[1]:
            raise ValueError(f'{method}@{pc}: operand/reference differs')


def javap(jar: Path, classes: list[str], executable: str, verbose=False) -> str:
    result = subprocess.run([executable, '-p', '-s', '-c', '-constants', *(['-v'] if verbose else []),
                             '-classpath', str(jar), *classes], capture_output=True, text=True,
                            timeout=60, check=False)
    if result.returncode:
        raise ValueError(f'javap failed: {result.stderr[:500]}')
    return result.stdout


def check_hash(path: Path, expected: tuple):
    raw = path.read_bytes()
    actual = (hashlib.sha1(raw).hexdigest(), hashlib.sha256(raw).hexdigest(), len(raw))
    if actual != expected:
        raise ValueError('artifact fingerprint mismatch; fail closed')


def validate_cards(manifest: dict, provider: Path):
    cards = manifest['cards']
    if len(cards) != 64 or len({c['id'] for c in cards}) != 64 or len({c['card_path'] for c in cards}) != 64:
        raise ValueError('expected exactly 64 unique IDs and dedicated paths')
    if collections.Counter(c['semantic_disposition'] for c in cards) != {'COUNTED_EXACT': 12, 'CONDITIONAL': 1, 'EXCLUDED': 51}:
        raise ValueError('semantic accounting changed')
    if next(c for c in cards if c['id'] == 'wom:flash_mutilation')['semantic_disposition'] != 'CONDITIONAL':
        raise ValueError('Nova reachability was not closed')
    for c in cards:
        path = (provider / c['card_path']).resolve()
        if provider.resolve() not in path.parents or not path.is_file():
            raise ValueError('card missing/outside provider')
        content = path.read_text()
        for required in [c['id'], c['implementation_class'], c['registry_field'], c['supplier'],
                         'Parâmetros empacotados e consumidor', 'Campos que uma perk pode precisar',
                         'Dano / cura / tipo', 'Alcance / alvo / área', 'Projétil / hitbox / tamanho',
                         'Tempo / duração / cooldown', 'Custo / recurso / refund', 'PENDING']:
            if required not in content:
                raise ValueError(f"{c['id']}: card lacks {required}")
        for m in c['methods']:
            if 'lambda$' not in m['name'] and m['descriptor'] not in content:
                raise ValueError(f"{c['id']}: public method descriptor not in card")
        for key, value in (c['packaged_parameters'] or {}).items():
            if '`' + key + '`' not in content or json.dumps(value, ensure_ascii=False, separators=(',', ':')) not in content:
                raise ValueError(f"{c['id']}: parameter not represented in card")


def audit(jar: Path, epic: Path, executable: str) -> dict:
    check_hash(jar, WOM_HASHES)
    check_hash(epic, EPIC_HASHES)
    manifest = json.loads(MANIFEST.read_text())
    validate_cards(manifest, PROVIDER)
    cards = manifest['cards']
    verbose = javap(jar, [REGISTRY], executable, verbose=True)
    links = registry_links(verbose, cards)
    with zipfile.ZipFile(jar) as archive:
        prefix = 'data/wom/skill_parameters/'
        actual = {name[len(prefix):-5]: json.loads(archive.read(name)) for name in archive.namelist()
                  if name.startswith(prefix) and name.endswith('.json')}
        expected = {c['id'].split(':')[1]: c['packaged_parameters'] for c in cards if c['parameter_path'] is not None}
        if len(actual) != 58 or not equal_json(actual, expected):
            raise ValueError('exact packaged parameter set/values differ')
        absent = {c['id'].split(':')[1] for c in cards if c['parameter_path'] is None}
        if absent != ABSENT or {key for key, value in actual.items() if value == {}} != EMPTY:
            raise ValueError('missing-vs-empty parameter distinction differs')
        for c in cards:
            id = c['id'].split(':')[1]
            if c['parameter_path'] != (prefix + id + '.json' if id in actual else None):
                raise ValueError('parameter path mismatch')
    bulk = javap(jar, [c['implementation_class'] for c in cards], executable)
    sections = {}
    for section in re.split(r'(?=Compiled from)', bulk):
        match = re.search(r'^public class ([\w.]+) ', section, re.M)
        if match:
            sections[match[1]] = section
    if len(sections) != 64:
        raise ValueError('concrete class inventory differs')
    reference_count = 0
    supplier_methods = methods(verbose)
    for c in cards:
        text = sections[c['implementation_class']]
        reference_count += assert_references(text, c)
        fields = literal_fields(text, c['implementation_class'])
        expected_fields = {f['field']: f['value'] for f in c['constructor_literal_fields']}
        if not equal_json(fields, expected_fields):
            raise ValueError(f"{c['id']}: constructor literal assignments differ")
        supplier_descriptor = '(Lnet/minecraft/resources/ResourceLocation;)L' + c['implementation_class'].replace('.', '/') + ';'
        supplier = supplier_methods[(c['supplier'], supplier_descriptor)]
        if builder_resource(supplier, text) != c['builder_resource']:
            raise ValueError(f"{c['id']}: declared builder resource differs")
        id = c['id'].split(':')[1]
        if id in OPERANDS:
            method, operands = OPERANDS[id]
            check_operands(text, method, operands)
    # Host checks pin loader consumers and builder defaults separately. They do
    # not claim the loader actually ran in the deployed pack.
    bases = javap(epic, ['yesman.epicfight.skill.Skill', 'yesman.epicfight.skill.SkillBuilder',
                        'yesman.epicfight.skill.dodge.DodgeSkill', 'yesman.epicfight.skill.guard.GuardSkill',
                        'yesman.epicfight.skill.weaponinnate.WeaponInnateSkill',
                        'yesman.epicfight.skill.weaponinnate.ConditionalWeaponInnateSkill'], executable)
    base_sections = {}
    for section in re.split(r'(?=Compiled from)', bases):
        match = re.search(r'^public (?:abstract )?class ([\w.]+)', section, re.M)
        if match:
            base_sections[match[1]] = section
    skill = methods(base_sections['yesman.epicfight.skill.Skill'])
    loader = skill[('loadDatapackParameters', '(Lnet/minecraft/nbt/CompoundTag;)V')]
    for fragment in ['String consumption', 'String max_duration', 'String max_stacks', 'Field consumption:F',
                     'Field maxDuration:I', 'Field maxStackSize:I', 'Map.clear:', 'ATTRIBUTE_ENTRY_CODEC:',
                     'Codec.parse:', 'Optional.ifPresent:']:
        if fragment not in loader:
            raise ValueError('host loader consumer differs')
    if 'String xp_requirement' in loader:
        raise ValueError('unexpected xp consumer in base loader')
    for cls, fragment in [('SkillBuilder', 'Skill$Resource.NONE:'), ('dodge.DodgeSkill', 'Skill$Resource.STAMINA:'),
                          ('guard.GuardSkill', 'String penalizer'), ('guard.GuardSkill', 'Skill$Resource.STAMINA:'),
                          ('weaponinnate.WeaponInnateSkill', 'Skill$Resource.WEAPON_CHARGE:'),
                          ('weaponinnate.ConditionalWeaponInnateSkill', 'Skill$Resource.WEAPON_CHARGE:')]:
        if fragment not in base_sections['yesman.epicfight.skill.' + cls]:
            raise ValueError('host builder/guard contract differs')
    return {'result': 'PASS_EXACT_STATIC_CATALOG', 'provider': 'wom', 'version': '2.0.178',
            'wom_sha1': WOM_HASHES[0], 'wom_sha256': WOM_HASHES[1], 'epic_sha1': EPIC_HASHES[0],
            'epic_sha256': EPIC_HASHES[1], 'registry_links': links, 'dedicated_cards': 64,
            'parameter_files': 58, 'parameterless_ids': sorted(ABSENT), 'empty_parameter_objects': sorted(EMPTY),
            'method_descriptors_checked': sum(len(c['methods']) for c in cards),
            'method_bounded_references_checked': reference_count, 'operand_cases': len(OPERANDS),
            'declared_builder_resources_checked': 64,
            'runtime_acceptance': 'PENDING', 'downstream_and_mutators': 'PARTIAL_NOT_CERTIFIED',
            'limits': ['Static artifact identity, registry/bootstrap linkage, parameter and selected method-reference/operand checks only.',
                       'Not full control-flow, complete downstream reconstruction or per-player mutation API proof.',
                       'No provider execution, deployed config, connected player, final damage/cost, PvP/claims or full-pack QA.',
                       'No third-party implementation bodies, assets or JARs are emitted.']}


class Tests(unittest.TestCase):
    def test_builder_override_does_not_inherit_wrong_resource(self):
        supplier = ('// Method fixture/Satsujin.createBuilder:()V\n'
                    '// Field yesman/epicfight/skill/Skill$Resource.COOLDOWN:LResource;\n'
                    '// Method fixture/Builder.setResource:()V\n')
        self.assertEqual(builder_resource(supplier, ''), 'COOLDOWN')
        with self.assertRaisesRegex(ValueError, 'unrecognized builder'):
            builder_resource('// Method future/NewFactory.createUnknown:()V', '')

    def test_json_bool_is_not_numeric_cost(self):
        self.assertFalse(equal_json({'consumption': True}, {'consumption': 1}))
        self.assertTrue(equal_json({'consumption': 1.0}, {'consumption': 1}))

    def test_json_absent_empty_zero_are_different(self):
        self.assertFalse(equal_json(None, {}))
        self.assertFalse(equal_json({}, {'consumption': 0}))
        self.assertFalse(equal_json({'max_stacks': 1}, {'max_stacks': 1, 'extra': 2}))

    def test_method_boundary_prevents_neighbor_reference(self):
        text = ('public class fixture.Skill extends fixture.Base {\n'
                '  public void target();\n    descriptor: ()V\n    Code:\n       0: return\n\n'
                '  private void neighbor();\n    descriptor: ()V\n    Code:\n'
                '       0: invokevirtual #1 // Method fixture/Event.getAmount:()F\n       3: return\n}\n')
        card = {'id': 'fixture:skill', 'implementation_class': 'fixture.Skill', 'superclass': 'fixture.Base',
                'methods': [{'name': 'target', 'descriptor': '()V', 'references': [{'pc': 0, 'reference': 'fixture/Event.getAmount:()F'}]}]}
        with self.assertRaisesRegex(ValueError, 'method-bounded reference'):
            assert_references(text, card)

    def test_method_descriptor_is_part_of_identity(self):
        text = '  public void target(int);\n    descriptor: (I)V\n    Code:\n       0: return\n}\n'
        self.assertNotIn(('target', '()V'), methods(text))
        self.assertIn(('target', '(I)V'), methods(text))

    def test_operand_must_match_same_offset(self):
        text = '  public void target();\n    descriptor: ()V\n    Code:\n       0: ldc #1 // float 12.0f\n       2: return\n}\n'
        check_operands(text, 'target', {0: 'float 12.0f'})
        with self.assertRaisesRegex(ValueError, 'operand/reference differs'):
            check_operands(text, 'target', {2: 'float 12.0f'})

    @staticmethod
    def fixture():
        card = {'id': 'wom:sample', 'registry_field': 'SAMPLE', 'implementation_class': 'fixture.Sample',
                'supplier': 'lambda$static$0'}
        text = ('public class reascer.wom.gameasset.WOMSkills {\n'
                '  public static final DeferredHolder<yesman.epicfight.skill.Skill, fixture.Sample> SAMPLE;\n'
                '  private static fixture.Sample lambda$static$0(net.minecraft.resources.ResourceLocation);\n'
                '    descriptor: (Lnet/minecraft/resources/ResourceLocation;)Lfixture/Sample;\n'
                '    Code:\n       0: areturn\n\n  static {};\n    descriptor: ()V\n    Code:\n'
                '       0: ldc #1 // String sample\n'
                '       2: invokedynamic #2, 0 // InvokeDynamic #7:apply:()Ljava/util/function/Function;\n'
                '       7: invokevirtual #3 // Method net/neoforged/neoforge/registries/DeferredRegister.register:()V\n'
                '      10: putstatic #4 // Field SAMPLE:Lnet/neoforged/neoforge/registries/DeferredHolder;\n'
                '      13: return\n}\nBootstrapMethods:\n'
                '  7: #5 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:()V\n'
                '    Method arguments:\n'
                '      #6 REF_invokeStatic reascer/wom/gameasset/WOMSkills.lambda$static$0:(Lnet/minecraft/resources/ResourceLocation;)Lfixture/Sample;\n'
                'InnerClasses:\n')
        return text, card

    def test_registry_typed_bootstrap_control(self):
        text, card = self.fixture()
        self.assertEqual(registry_links(text, [card])['wom:sample']['bootstrap_index'], 7)

    def test_registry_wrong_holder_is_rejected(self):
        text, card = self.fixture()
        with self.assertRaisesRegex(ValueError, 'wrong holder'):
            registry_links(text.replace('// Field SAMPLE:', '// Field OTHER:'), [card])

    def test_registry_wrong_supplier_is_rejected(self):
        text, card = self.fixture()
        with self.assertRaisesRegex(ValueError, 'supplier/class bootstrap'):
            registry_links(text.replace('REF_invokeStatic reascer/wom/gameasset/WOMSkills.lambda$static$0:',
                                        'REF_invokeStatic reascer/wom/gameasset/WOMSkills.lambda$static$1:'), [card])

    def test_registry_missing_bootstrap_is_rejected(self):
        text, card = self.fixture()
        with self.assertRaisesRegex(ValueError, 'BootstrapMethods absent'):
            registry_links(text.split('\nBootstrapMethods:')[0], [card])

    def test_registry_wrong_return_type_is_rejected(self):
        text, card = self.fixture()
        with self.assertRaisesRegex(ValueError, 'supplier/class bootstrap'):
            registry_links(text.replace('REF_invokeStatic reascer/wom/gameasset/WOMSkills.lambda$static$0:(Lnet/minecraft/resources/ResourceLocation;)Lfixture/Sample;',
                                        'REF_invokeStatic reascer/wom/gameasset/WOMSkills.lambda$static$0:(Lnet/minecraft/resources/ResourceLocation;)Lfixture/Wrong;'), [card])

    def test_duplicate_instruction_offsets_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate instruction'):
            instructions('0: return\n0: areturn\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path)
    parser.add_argument('--epic-jar', type=Path)
    parser.add_argument('--javap', default='javap')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=[__file__], exit=True)
    if not args.jar or not args.epic_jar:
        parser.error('--jar and --epic-jar are required')
    try:
        report = audit(args.jar, args.epic_jar, args.javap)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        report = {'result': 'FAIL_CLOSED', 'error': str(exc), 'runtime_acceptance': 'PENDING'}
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(json.dumps({k: v for k, v in report.items() if k != 'registry_links'}, ensure_ascii=False))
    return 0 if report['result'] == 'PASS_EXACT_STATIC_CATALOG' else 1


if __name__ == '__main__':
    raise SystemExit(main())
