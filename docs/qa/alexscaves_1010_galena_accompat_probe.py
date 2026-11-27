#!/usr/bin/env python3
"""Read-only exact Alex's Caves Continued 1.0.10 ACCompat bridge discovery.

Targeted consumer methods are chosen by typed Galena publisher JVM callsites.
No decompiled source, mod runtime or world mutation is used. This discovery does
not certify the delegated Minecraft/NeoForge engine behavior.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

OWNER = 'com/github/alexmodguy/alexscaves/server/misc/ACCompat'
ITEM = 'com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem'
ENTITY = 'com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity'
CALLER_SHA = 'c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9'
NAMES = frozenset({'saveStack', 'loadStack', 'putUUID', 'getUUID',
    'hasUUID', 'getCompound', 'getOrCreateTag', 'getTag', 'setTag', 'getInt'})


def source_census(path: Path):
    raw = path.read_bytes()
    require(len(raw) == 1780492 and digest(raw) == CALLER_SHA,
            'Galena caller report must match the previously verified publisher SHA')
    obj = json.loads(raw)
    require(obj['artifact']['sha256'] == SHA256 and obj['artifact']['size_bytes'] == SIZE,
            'Galena caller JAR identity drift')
    require(obj['mutation'] == 'NO_MUTATION' and obj['physical_qa'] == 'NOT_TESTED',
            'Galena caller safety state drift')
    refs = []
    for key, owner in (('native', ITEM), ('entity_native', ENTITY)):
        card = obj[key]['targets']
        require(set(card) == {owner}, 'caller class roster mismatch')
        for method in card[owner]['methods']:
            d = method['declaration']
            for ins in method['instructions']:
                prefix = 'Method ' + OWNER + '.'
                sym = ins['symbol']
                if ins['opcode'] != 'invokestatic' or not sym.startswith(prefix):
                    continue
                n, sep, desc = sym[len(prefix):].partition(':')
                require(sep and desc.startswith('('), 'bad JVM invocation descriptor')
                if n in NAMES:
                    refs.append({'caller_owner': owner, 'caller_name': d['name'],
                        'caller_descriptor': d['descriptor'], 'offset': ins['offset'],
                        'opcode': ins['opcode'], 'callee_name': n,
                        'callee_descriptor': desc})
    seen_names = {s['callee_name'] for s in refs}
    require(seen_names == NAMES, 'ACCompat helper set does not match prior Galena consumers')
    pairs = sorted({(s['callee_name'], s['callee_descriptor']) for s in refs})
    require(len(pairs) == len(NAMES), 'unexpected ACCompat overload in exact consumers')
    return refs, pairs


def probe(jar: Path, javap: str, caller_report: Path, output: Path):
    verify_artifact(jar)
    require(not output.exists() and output.suffix == '.json', 'write-once JSON output required')
    refs, pairs = source_census(caller_report)
    with ZipFile(jar) as z:
        paths = z.namelist()
        require(len(set(paths)) == len(paths), 'duplicate ZIP entries')
        require(sum(p.endswith('.class') for p in paths) == 1555, 'JAR class count drift')
        raw = z.read(OWNER + '.class')
        rd = ClassReader(raw)
        require(rd.name == OWNER and rd.major == 65,
                'ACCompat class identity or classfile version changed')
        method_decls = {(m['name'], m['descriptor']): m for m in rd.methods}
        require(len(method_decls) == len(rd.methods), 'ambiguous helper declarations')
        require(all(k in method_decls and 'code_sha256' in method_decls[k] for k in pairs),
                'a targeted ACCompat helper has no method body')
        methods = disassemble(jar, javap, OWNER)
        require(all(k in methods for k in pairs), 'JVM disassembly misses helper body')
        selected = [summarize(rd, key, methods[key]) for key in pairs]
        require(len(selected) == 10, 'selected method roster drift')
        out = {
            'schema_version': 1,
            'scope': 'GALENA_ACCOMPAT_HELPERS_JVM_DISCOVERY_NOT_CERTIFIED',
            'artifact': {'filename': 'alexscaves-1.0.10-neoforge+1.21.1.jar',
                'version': '1.0.10', 'sha1': SHA1, 'sha256': SHA256,
                'size_bytes': SIZE, 'installed_dump_parity': 'NOT_VERIFIED'},
            'class': {'owner': OWNER, 'sha256': digest(raw),
                'declared_methods': len(rd.methods), 'fields': len(rd.fields),
                'selected_methods': selected},
            'caller_evidence': {'source_sha256': CALLER_SHA, 'source_bytes': 1780492,
                'typed_callsites': refs},
            'limits': {'minecraft_engine_helpers': 'NOT_VERIFIED',
                'neoforge_engine_hooks': 'NOT_VERIFIED',
                'save_restart_recovery': 'NOT_TESTED',
                'dimension_transfer': 'NOT_TESTED'},
            'static_contract': 'NOT_CERTIFIED', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'mutation': 'NO_MUTATION',
            'provider_universe_closed': False, 'semantic_magic_roots_delta': 0,
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(out), encoding='utf-8')
    print('REPORT_SHA256', digest(output.read_bytes()), 'BYTES', output.stat().st_size)
    print('CLASS_SHA256', out['class']['sha256'], 'DECLARED_METHODS', len(rd.methods))
    print('GALLERY_CALLSITES', len(refs), 'TARGET_HELPERS', len(selected))
    for m in selected:
        d = m['declaration']
        print('METHOD', d['name'], d['descriptor'], 'INS', m['instruction_count'],
              'CODE_SHA', d['code_sha256'], 'INSTRUCTION_SHA', m['instruction_sha256'])
        for ins in m['instructions']:
            if ins['opcode'].startswith(('invoke','if','get','put')) or ins['opcode'] in {
                'ldc','ldc_w','bipush','sipush','aconst_null','areturn','ireturn','new','checkcast'}:
                print('PIVOT',d['name'],ins['offset'],ins['opcode'],ins['operand'],ins['symbol'][:130])
    print('DISCOVERY_ONLY NO_MUTATION NO_PERK_CERTIFICATION')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jar',type=Path,required=True)
    ap.add_argument('--caller-report',type=Path,required=True)
    ap.add_argument('--javap',default='javap')
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    probe(a.jar,a.javap,a.caller_report,a.output)
