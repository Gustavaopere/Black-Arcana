#!/usr/bin/env python3
"""Read-only destroyed-item boundary from official NeoForge 21.1.250 artifacts.

Only two universal-JAR default methods and three userdev source patches are
projected. This does not build Minecraft or execute an installed transformed game.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, canonical, digest, load_seal, parse_javap, require, rows)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json'
VERSION = '21.1.250'
BASE_URL = 'https://maven.neoforged.net/releases/net/neoforged/neoforge/' + VERSION + '/'
ARTIFACTS = {
    'universal': {'filename': 'neoforge-21.1.250-universal.jar', 'size_bytes': 3551255,
        'sha1': '214c5293c8599b0aaadfdbfa92453ba23918a219',
        'sha256': '1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956'},
    'userdev': {'filename': 'neoforge-21.1.250-userdev.jar', 'size_bytes': 3983248,
        'sha1': '45f4a0daf3ecd5864338cb5ab7368afbee02e529',
        'sha256': 'deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372'}}
EXTENSION = 'net/neoforged/neoforge/common/extensions/'
ITEM, STACK = EXTENSION + 'IItemExtension', EXTENSION + 'IItemStackExtension'
ENTITY_TYPE = 'Lnet/minecraft/world/entity/item/ItemEntity;'
SOURCE_TYPE = 'Lnet/minecraft/world/damagesource/DamageSource;'
CALLBACK = ('onDestroyed', '(' + ENTITY_TYPE + SOURCE_TYPE + ')V')
ONE_ARG = '(' + ENTITY_TYPE + ')V'
CLASS_HASHES = {ITEM: 'd65a413962ab6bf6cf8c33119b010dd16fcf482c114b8ae8abe5c59da951b088',
    STACK: '244993a9cd1a5e99507c88a0a8e1d65b6ef997d44bd73ab696a510ccf2d0397e'}
CODE_HASHES = {ITEM: '5329be910501a1f43935664ae16d2d9968d734c3eb063130a2ece881a1cc508a',
    STACK: 'daec92ef22fe14d788a69e103bb2d2a03bff3357748764a77ce93bdcf159271c'}
PATCH_ROOT = 'patches/net/minecraft/'
ITEM_PATCH = PATCH_ROOT + 'world/item/Item.java.patch'
STACK_PATCH = PATCH_ROOT + 'world/item/ItemStack.java.patch'
ENTITY_PATCH = PATCH_ROOT + 'world/entity/item/ItemEntity.java.patch'
PATCH_HASHES = {
    ITEM_PATCH: '6d16f90d962de67d1de56f92fdf7a8c8067296a87c7c20f7e48691b15ced706f',
    STACK_PATCH: '5e910db862cc11662067e5ffbd2a792197d2eb618ce76f4281ee6fb5998c8c7d',
    ENTITY_PATCH: '6c48c1cacf8fa9b7afcb61f8b541782a6a5d0b48a4d32ae2868f1e2fe637e489'}
CLAIMS = {'evidence_grade': 'PINNED_USERDEV_PATCH_PLUS_UNIVERSAL_BYTECODE_REFERENCE',
    'claim_scope': 'STATIC_DESTROYED_ITEM_EXTERNAL_BOUNDARY_ONLY',
    'minecraft_version': '1.21.1', 'neoforge_version': VERSION,
    'matches_physical_ledger_loader_version': True,
    'installed_transformed_execution': 'NOT_VERIFIED', 'actual_gameplay_outcomes': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'mutating_hook': 'NOT_VERIFIED', 'perk_certification': 'NOT_CERTIFIED',
    'mutation': 'NO_MUTATION', 'provider_universe_closed': False, 'semantic_magic_roots_delta': 0}
BOUNDARY = {
    'item_entity_dispatch': 'The official userdev patch replaces the one-argument call with ItemStack.onDestroyed(this, damageSource) inside health <= 0 and before discard().',
    'stack_bridge': 'IItemStackExtension default invokes self().getItem().onDestroyed(itemEntity, damageSource) virtually.',
    'item_bridge': 'IItemExtension default invokes self().onDestroyed(itemEntity) virtually, preserving one-argument subclass dispatch.',
    'superclass_resolution': 'Conditional reference derivation: combining the separate publisher native seal with the standard external BlockItem-to-Item hierarchy and Item implementing IItemExtension supplies the inherited two-argument default when no class in the superclass chain declares that descriptor. JVM class-method resolution includes maximally specific superinterface defaults. The external BlockItem hierarchy itself is not projected by these three source patches.',
    'resolution_reference': 'https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html#jvms-5.4.3.3',
    'limitations': 'Userdev patch context is not a complete ItemEntity.hurt binary body. No derived Minecraft JAR is required. Installed transformations, modpack execution, cloud application, victims, explosion outcomes and gameplay safety remain unverified.'}


def artifact_identity(kind):
    return {**ARTIFACTS[kind], 'official_url': BASE_URL + ARTIFACTS[kind]['filename'],
        'official_sha256_url': BASE_URL + ARTIFACTS[kind]['filename'] + '.sha256'}


def verify_artifact(path, kind):
    expected = ARTIFACTS[kind]
    require(path.stat().st_size == expected['size_bytes'], kind + ' artifact size mismatch')
    raw = path.read_bytes()
    require(digest(raw) == expected['sha256'] and hashlib.sha1(raw).hexdigest() == expected['sha1'],
        kind + ' artifact digest mismatch')


def bridge_pivots(owner, body):
    """Require the complete short bridge, including receiver, arguments and call kind."""
    item_self = 'InterfaceMethod self:()Lnet/minecraft/world/item/Item;'
    stack_self = 'InterfaceMethod self:()Lnet/minecraft/world/item/ItemStack;'
    expected = ({0: ('aload_0', '', ''), 1: ('invokeinterface', '#3, 1', item_self),
        6: ('aload_1', '', ''), 7: ('invokevirtual', '#256', 'Method net/minecraft/world/item/Item.onDestroyed:' + ONE_ARG),
        10: ('return', '', '')} if owner == ITEM else {
        0: ('aload_0', '', ''), 1: ('invokeinterface', '#3, 1', stack_self),
        6: ('invokevirtual', '#9', 'Method net/minecraft/world/item/ItemStack.getItem:()Lnet/minecraft/world/item/Item;'),
        9: ('aload_1', '', ''), 10: ('aload_2', '', ''),
        11: ('invokevirtual', '#256', 'Method net/minecraft/world/item/Item.onDestroyed:' + CALLBACK[1]),
        14: ('return', '', '')})
    require(owner in (ITEM, STACK) and body == expected, 'destroyed-item default bridge drift: ' + owner)


def patch_pivots(entries):
    """Match active unified-diff additions and the callback's surrounding hunk."""
    require(set(entries) == set(PATCH_HASHES), 'finite source patch roster drift')
    lines = {name: raw.decode('utf8').splitlines() for name, raw in entries.items()}
    additions = {
        ITEM_PATCH: '+public class Item implements FeatureElement, ItemLike, net.neoforged.neoforge.common.extensions.IItemExtension {',
        STACK_PATCH: '+public final class ItemStack implements DataComponentHolder, net.neoforged.neoforge.common.MutableDataComponentHolder, net.neoforged.neoforge.common.extensions.IItemStackExtension {'}
    contracts = []
    for name, addition in additions.items():
        require(lines[name].count(addition) == 1, 'extension declaration patch drift: ' + name)
        index = lines[name].index(addition)
        require(index > 0 and lines[name][index-1].startswith('-public '), 'extension declaration is not a replacement')
        contracts.append({'entry': name, 'assertion': 'active class declaration adds extension interface',
            'selected_patch_lines': [{'line': index+1, 'text': addition}]})
    dispatch = [
        '@@ -282,7 +_,7 @@',
        '             this.health = (int)((float)this.health - p_32014_);',
        '             this.gameEvent(GameEvent.ENTITY_DAMAGE, p_32013_.getEntity());',
        '             if (this.health <= 0) {',
        '-                this.getItem().onDestroyed(this);',
        '+                this.getItem().onDestroyed(this, p_32013_);',
        '                 this.discard();',
        '             }']
    entity_lines = lines[ENTITY_PATCH]
    matches = [i for i in range(len(entity_lines)-len(dispatch)+1)
        if entity_lines[i:i+len(dispatch)] == dispatch]
    require(len(matches) == 1, 'health-gated two-argument dispatch-before-discard patch drift')
    start = matches[0]
    contracts.append({'entry': ENTITY_PATCH,
        'assertion': 'health <= 0 calls two-argument stack callback before discard',
        'selected_patch_lines': [{'line': start+i+1, 'text': line} for i, line in enumerate(dispatch)]})
    return contracts


def build_report(universal, userdev, javap):
    verify_artifact(universal, 'universal')
    verify_artifact(userdev, 'userdev')
    bridges = []
    with zipfile.ZipFile(universal) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate universal ZIP members')
        for owner in (ITEM, STACK):
            raw = archive.read(owner + '.class')
            require(digest(raw) == CLASS_HASHES[owner], 'extension class hash drift: ' + owner)
            parsed = ClassReader(raw)
            require(parsed.name == owner and parsed.access == 1537 and parsed.major == 65 and
                parsed.parent == 'java/lang/Object' and parsed.interfaces == [], 'extension declaration drift')
            selected = [m for m in parsed.methods if (m['name'], m['descriptor']) == CALLBACK]
            require(len(selected) == 1 and selected[0]['access'] == 1 and
                selected[0].get('code_sha256') == CODE_HASHES[owner] and
                selected[0].get('exception_handlers') == [], 'default method declaration/code drift')
            result = subprocess.run([str(javap), '-classpath', str(universal), '-p', '-c', '-s', owner.replace('/', '.')],
                capture_output=True, text=True, timeout=60)
            require(result.returncode == 0, 'javap failed: ' + result.stderr[:300])
            methods = parse_javap(result.stdout, owner)
            require(CALLBACK in methods, 'default callback body missing')
            body = methods[CALLBACK]
            bridge_pivots(owner, body)
            instructions = rows(body)
            bridges.append({'owner': owner, 'class_sha256': digest(raw), 'class_access': parsed.access,
                'class_major': parsed.major, 'parent': parsed.parent, 'interfaces': parsed.interfaces,
                'method': {**selected[0], 'instruction_count': len(instructions), 'instructions': instructions,
                    'instruction_sha256': digest(canonical(instructions).encode())}})
    with zipfile.ZipFile(userdev) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'duplicate userdev ZIP members')
        entries = {name: archive.read(name) for name in PATCH_HASHES}
        require(all(digest(raw) == PATCH_HASHES[name] for name, raw in entries.items()), 'source patch entry hash drift')
        patches = [{**contract, 'sha256': digest(entries[contract['entry']]),
            'size_bytes': len(entries[contract['entry']])} for contract in patch_pivots(entries)]
    return {'schema': 'AC_DESTROYED_ITEM_ENGINE_REFERENCE_V1', 'claims': CLAIMS,
        'artifacts': {kind: artifact_identity(kind) for kind in ARTIFACTS},
        'universal_default_bridges': bridges, 'userdev_source_patches': patches,
        'external_boundary': BOUNDARY,
        'validation': {'required_inputs': ['official universal JAR', 'official userdev JAR', 'JDK 21 javap'],
            'derived_minecraft_jar_required': False, 'engine_build_or_launch_performed': False,
            'comparison': 'Exact artifact and selected entry/code hashes; complete two bridge instruction bodies; active interface-declaration additions and health-gated callback-before-discard patch context; mandatory deterministic seal comparison.'}}


def validate_report(report):
    require(report.get('schema') == 'AC_DESTROYED_ITEM_ENGINE_REFERENCE_V1', 'invalid engine-reference schema')
    require(report.get('claims') == CLAIMS, 'reference claim ceiling drift')
    require(report.get('artifacts') == {kind: artifact_identity(kind) for kind in ARTIFACTS}, 'artifact reference identity drift')
    require(report.get('external_boundary') == BOUNDARY, 'external boundary scope drift')
    bridges = report['universal_default_bridges']
    require([b['owner'] for b in bridges] == [ITEM, STACK], 'finite bridge roster drift')
    for bridge in bridges:
        owner, method = bridge['owner'], bridge['method']
        require(bridge['class_sha256'] == CLASS_HASHES[owner] and bridge['class_access'] == 1537 and
            bridge['class_major'] == 65 and bridge['parent'] == 'java/lang/Object' and bridge['interfaces'] == [], 'report extension declaration drift')
        require((method['name'], method['descriptor']) == CALLBACK and method['access'] == 1 and
            method['code_sha256'] == CODE_HASHES[owner] and method['code_size'] == (11 if owner == ITEM else 15) and
            method['max_stack'] == (2 if owner == ITEM else 3) and method['max_locals'] == 3 and
            method['exception_handlers'] == [], 'report default callback declaration drift')
        instructions = method['instructions']
        require(method['instruction_count'] == len(instructions) and
            method['instruction_sha256'] == digest(canonical(instructions).encode()), 'bridge instruction digest drift')
        body = {r['offset']: (r['opcode'], r['operand'], r['symbol']) for r in instructions}
        require(len(body) == len(instructions), 'duplicate bridge instruction offset')
        bridge_pivots(owner, body)
    patches = report['userdev_source_patches']
    require([p['entry'] for p in patches] == [ITEM_PATCH, STACK_PATCH, ENTITY_PATCH] and
        all(p['sha256'] == PATCH_HASHES[p['entry']] for p in patches), 'source patch seal roster/hash drift')
    require(report['validation']['derived_minecraft_jar_required'] is False and
        report['validation']['engine_build_or_launch_performed'] is False, 'engine execution ceiling drift')


def compare_seal(report, expected):
    validate_report(expected)
    validate_report(report)
    require(report == expected, 'destroyed-item engine reference seal mismatch')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--universal', type=Path, required=True)
    parser.add_argument('--userdev', type=Path, required=True)
    parser.add_argument('--javap', type=Path, required=True)
    parser.add_argument('--seal', type=Path, default=SEAL)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.output:
            protected = {p.resolve() for p in (args.universal, args.userdev, args.javap, args.seal, SEAL,
                Path(__file__), Path(sys.modules[ClassReader.__module__].__file__),
                Path(sys.modules[parse_javap.__module__].__file__))}
            require(args.output.resolve() not in protected, 'output would overwrite an input/probe')
        expected = load_seal(args.seal)
        validate_report(expected)
        report = build_report(args.universal, args.userdev, args.javap)
        compare_seal(report, expected)
        payload = canonical(report)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding='utf8')
        else:
            sys.stdout.write(payload)
        return 0
    except (AuditError, ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile, KeyError, TypeError) as error:
        print('destroyed-item engine reference audit failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
