#!/usr/bin/env python3
"""Galena weapon return/fallback and ACCompat.spawnAtLocation: exact publisher JVM discovery.

Read-only inspection for interop; no hooks, Minecraft settlement, world mutation, or
physical gameplay. Caller bytecode is independently reconstructed from publisher.
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
CALLEE = ('spawnAtLocation',
          '(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/item/ItemEntity;')
METHODS = {
    ITEM: {'onUseTick'},
    ENTITY: {'tick', 'plopItem', 'getController', 'isOwnerWearingGauntlet',
             'getReturnProgress', 'directMovementTowards', 'getItemStack'},
}
CLASSES = {
    ITEM: '5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0',
    ENTITY: 'a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071',
}


def caller_snapshot(path: Path):
    raw = path.read_bytes()
    require(len(raw) == 1780492 and digest(raw) == CALLER_SHA,
            'canonical Galena discovery report identity drift')
    doc = json.loads(raw)
    require(doc['artifact']['sha256'] == SHA256 and doc['mutation'] == 'NO_MUTATION'
            and doc['physical_qa'] == 'NOT_TESTED', 'caller provenance/safety drift')
    out = {}
    refs = []
    for section, owner in (('native', ITEM), ('entity_native', ENTITY)):
        targets = doc[section]['targets']
        require(set(targets) == {owner}, 'caller owner roster drift')
        card = targets[owner]
        require(card['class_sha256'] == CLASSES[owner], 'caller class drift')
        methods = [m for m in card['methods'] if m['declaration']['name'] in METHODS[owner]]
        require({m['declaration']['name'] for m in methods} == METHODS[owner]
                and len(methods) == len(METHODS[owner]), 'caller return-method roster drift')
        for method in methods:
            for ins in method['instructions']:
                if ins['symbol'] == 'Method ' + OWNER + '.' + CALLEE[0] + ':' + CALLEE[1]:
                    require(ins['opcode'] == 'invokestatic', 'callee invocation-kind drift')
                    refs.append({'caller_owner': owner, 'caller_method': method['declaration']['name'],
                                 'caller_descriptor': method['declaration']['descriptor'],
                                 'offset': ins['offset'], 'opcode': ins['opcode'],
                                 'callee_name': CALLEE[0], 'callee_descriptor': CALLEE[1]})
        out[owner] = {'class_sha256': card['class_sha256'], 'methods': sorted(
            methods, key=lambda m: (m['declaration']['name'], m['declaration']['descriptor']))}
    require(len(refs) == 1 and refs[0]['caller_owner'] == ENTITY
            and refs[0]['caller_method'] == 'plopItem' and refs[0]['offset'] == 17,
            'ACCompat.spawnAtLocation exact Galena caller mismatch')
    return out, refs


def probe(jar: Path, javap: str, caller_report: Path, output: Path):
    verify_artifact(jar)
    require(output.suffix == '.json' and not output.exists(), 'write-once report destination')
    callers, refs = caller_snapshot(caller_report)
    with ZipFile(jar) as archive:
        entries = archive.namelist()
        require(len(entries) == len(set(entries)), 'duplicate ZIP path')
        require(sum(x.endswith('.class') for x in entries) == 1555, 'class roster drift')
        for owner,card in callers.items():
            raw = archive.read(owner + '.class')
            require(digest(raw) == card['class_sha256'], 'caller physical class drift')
        raw = archive.read(OWNER + '.class')
        reader = ClassReader(raw)
        require(reader.name == OWNER and reader.major == 65, 'ACCompat identity drift')
        matching = [d for d in reader.methods if (d['name'], d['descriptor']) == CALLEE]
        require(len(matching) == 1 and 'code_sha256' in matching[0],
                'missing ACCompat exact spawn helper implementation')
        disasm = disassemble(jar, javap, OWNER)
        require(CALLEE in disasm, 'javap missed exact spawn helper')
        method = summarize(reader, CALLEE, disasm[CALLEE])
        report = {
            'schema': 'GALENA_RETURN_DROP_DISCOVERY_V1',
            'scope': 'SHA_EXACT_PUBLISHER_JVM_DISCOVERY_NOT_CERTIFIED',
            'artifact': {'filename': 'alexscaves-1.0.10-neoforge+1.21.1.jar',
                         'version': '1.0.10', 'sha1': SHA1, 'sha256': SHA256,
                         'size_bytes': SIZE, 'installed_dump_parity': 'NOT_VERIFIED'},
            'caller_report': {'sha256': CALLER_SHA, 'size_bytes': 1780492},
            'callers': callers, 'helper': {'owner': OWNER, 'class_sha256': digest(raw),
                 'methods_declared': len(reader.methods), 'fields_declared': len(reader.fields),
                 'selected': method},
            'typed_helper_callers': refs,
            'limits': {'engine_Player_addItem': 'NOT_VERIFIED',
                'engine_Level_addFreshEntity': 'NOT_VERIFIED',
                'engine_Entity_remove': 'NOT_VERIFIED',
                'engine_ACCompat_spawnAtLocation_settlement': 'JVM_REQUESTS_ONLY',
                'world_drops': 'NOT_TESTED', 'save_reload': 'NOT_TESTED'},
            'static_contract': 'NOT_CERTIFIED', 'mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
            'mutation': 'NO_MUTATION', 'provider_universe_closed': False,
            'semantic_magic_roots_delta': 0,
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding='utf8')
    print('REPORT', digest(output.read_bytes()), output.stat().st_size)
    print('HELPER_CLASS', report['helper']['class_sha256'], 'METHODS', len(reader.methods))
    print('SPAWN_HELPER', CALLEE, 'INS', method['instruction_count'],
          'CODE_SHA', method['declaration']['code_sha256'])
    for ins in method['instructions']:
        print('SPAWN_JVM', ins['offset'], ins['opcode'], ins['operand'], ins['symbol'])
    print('EXACT_CONSUMER', refs)
    print('DISCOVERY_ONLY NO_MUTATION NO_PERK_CERTIFICATION')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for k in ('jar','caller-report','output'):
        parser.add_argument('--'+k, type=Path, required=True)
    parser.add_argument('--javap',default='javap')
    a = parser.parse_args()
    probe(a.jar,a.javap,a.caller_report,a.output)
