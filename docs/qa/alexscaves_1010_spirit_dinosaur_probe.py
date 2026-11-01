#!/usr/bin/env python3
"""Bounded SHA-exact Spirit Dinosaur damage emitters probe; no runtime claims."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file

ROOT = 'com/github/alexmodguy/alexscaves/server/entity/item/'
CLASSES = {
    ROOT + 'DinosaurSpiritEntity.class': {
        'sha': 'c4f6bbf7dab4aeeb2abd5b8cd227759d2ea1692115d1b3d14b62598a0b3900d7',
        'method': 'tickTremorsaurus', 'descriptor': '(Lnet/minecraft/world/entity/player/Player;)V', 'offset': 131},
    ROOT + 'ExtinctionSpearEntity.class': {
        'sha': '084a315c5a63dabc8c6ff1bc91ad008b0b2374e4d7f953bf3692c77394093774',
        'method': 'onHitEntity', 'descriptor': '(Lnet/minecraft/world/phys/EntityHitResult;)V', 'offset': 58}
}
INTERESTING = re.compile(r'(tick|owner|attack|target|hit|hurt|save|spawn|shoot|spirit|dinosaur|remove|discard|damage|summon|player|spear|readAdditional|defineSynched)', re.I)
SYMBOLS = {'getfield', 'putfield', 'getstatic', 'putstatic', 'invokevirtual', 'invokestatic', 'invokespecial', 'invokeinterface', 'invokedynamic', 'instanceof', 'checkcast'}
NUMERIC = {'bipush', 'sipush', 'ldc', 'ldc_w', 'ldc2_w'}
BRANCH = {'goto', 'goto_w', 'tableswitch', 'lookupswitch'}
MAX_REPORT_BYTES = 340000

class SpiritProbeError(ValueError):
    pass

def name_of(m):
    return m['header'].split('(', 1)[0].split()[-1].rsplit('.', 1)[-1]

def compact(i):
    return {k: i[k] for k in ('offset', 'opcode', 'operand', 'symbol')}

def caller_anchor(m, identity):
    matches = [i for i in m['instructions'] if i['offset'] == identity['offset']]
    if (name_of(m) != identity['method'] or m['descriptor'] != identity['descriptor']
        or len(matches) != 1 or matches[0]['opcode'] != 'invokestatic'
        or 'ACDamageTypes.causeSpiritDinosaurDamage:' not in matches[0]['symbol']):
        raise SpiritProbeError('exact Spirit Dinosaur factory caller drift')
    return {'method': identity['method'], 'descriptor': identity['descriptor'],
            'offset': identity['offset'], 'opcode': matches[0]['opcode'],
            'factory_symbol': matches[0]['symbol']}

def summarize(m, offsets):
    seq = m['instructions']
    if not 1 <= len(seq) <= 6500 or len({i['offset'] for i in seq}) != len(seq):
        raise SpiritProbeError('invalid bounded JVM instruction count/offsets')
    groups = {'references': [], 'numeric_constants': [], 'branches': []}
    for i in seq:
        opcode = i['opcode']
        group = ('references' if opcode in SYMBOLS else
                 'numeric_constants' if opcode in NUMERIC or opcode.startswith(('iconst_', 'fconst_', 'lconst_', 'dconst_')) else
                 'branches' if opcode.startswith('if') or opcode in BRANCH else None)
        if group:
            groups[group].append(compact(i))
    if len(groups['references']) > 300 or len(groups['numeric_constants']) > 160 or len(groups['branches']) > 200:
        raise SpiritProbeError('bounded instruction group overflow')
    places = {i['offset']: p for p, i in enumerate(seq)}
    windows = []
    for off in offsets:
        if off not in places:
            raise SpiritProbeError('exact selected offset missing')
        pos = places[off]
        windows.append({'offset': off, 'instructions': [compact(x) for x in seq[max(0,pos-9):pos+10]]})
    return {
        'name': name_of(m), 'descriptor': m['descriptor'],
        'instruction_count': len(seq),
        'parsed_method_sha256': hashlib.sha256(json.dumps(m, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest(),
        **groups, 'selected_windows': windows,
        'damage_accepted_or_counted': 'NOT_VERIFIED'
    }

def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise SpiritProbeError('exact publisher JAR digest/size drift')
    selected_classes = []
    with zipfile.ZipFile(jar) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise SpiritProbeError('duplicate ZIP entries')
        for path, wanted in CLASSES.items():
            data = z.read(path)
            if hashlib.sha256(data).hexdigest() != wanted['sha']:
                raise SpiritProbeError('exact caller class SHA mismatch')
            methods = parse_methods(javap(javap_bin, jar, path[:-6].replace('/', '.')))
            identities = [(name_of(m), m['descriptor']) for m in methods]
            if len(identities) != len(set(identities)):
                raise SpiritProbeError('duplicate declared JVM method')
            roots = [m for m in methods if name_of(m) == wanted['method'] and m['descriptor'] == wanted['descriptor']]
            if len(roots) != 1:
                raise SpiritProbeError('ambiguous/missing exact caller')
            factory = caller_anchor(roots[0], wanted)
            selected = [m for m in methods if m['instructions'] and (m is roots[0] or INTERESTING.search(name_of(m)))]
            if not 1 <= len(selected) <= 60:
                raise SpiritProbeError('selected methods over budget')
            selected_classes.append({
                'class_path': path, 'class_sha256': wanted['sha'],
                'declared_method_count': len(methods),
                'selected_method_count': len(selected),
                'damage_factory_callsite': factory,
                'selected_methods': [summarize(m, [wanted['offset']] if m is roots[0] else []) for m in selected]
            })
    result = {
        'schema_version': 1,
        'scope': 'SHA_EXACT_1010_SPIRIT_DINOSAUR_TWO_DAMAGE_CALLERS_SELECTED_METHODS_ONLY',
        'artifact': {'sha1': SHA1, 'sha256': SHA256, 'size_bytes': SIZE},
        'classes': selected_classes,
        'limits': {
            'full_provider_code_exported': False,
            'runtime_damage_acceptance': 'NOT_VERIFIED',
            'full_control_flow_and_exception_edges': 'NOT_RECONSTRUCTED',
            'projectile_ownership_and_PvP': 'NOT_CERTIFIED',
            'mutating_hook': 'NOT_VERIFIED', 'physical_qa': 'NOT_TESTED',
            'provider_universe_closed': False
        }
    }
    if len(json.dumps(result, ensure_ascii=False).encode()) > MAX_REPORT_BYTES:
        raise SpiritProbeError('bounded report size exceeded')
    return result


def check_sealed_manifest(report, manifest):
    """Fail closed on exact two-class identities, method hashes and selected anchors."""
    for key in ('schema_version', 'scope', 'artifact'):
        if report.get(key) != manifest.get(key):
            raise SpiritProbeError('sealed identity mismatch: ' + key)
    expected_classes = manifest.get('classes')
    if not isinstance(expected_classes, list) or len(expected_classes) != len(CLASSES):
        raise SpiritProbeError('sealed class roster mismatch')
    actual = {c['class_path']: c for c in report['classes']}
    if len(actual) != len(CLASSES):
        raise SpiritProbeError('duplicate or missing class result')
    for sealed in expected_classes:
        path = sealed['class_path']
        if path not in actual or path not in CLASSES:
            raise SpiritProbeError('unknown/missing sealed class')
        observed = actual[path]
        for key in ('class_sha256', 'declared_method_count'):
            if observed[key] != sealed[key]:
                raise SpiritProbeError('sealed class identity drift: ' + key)
        methods = {}
        for m in observed['selected_methods']:
            methods.setdefault(m['name'], []).append(m)
        for name, digest in sealed['selected_method_digests'].items():
            if not isinstance(digest, str) or len(digest) != 64:
                raise SpiritProbeError('invalid SHA-256 digest seal')
            found = methods.get(name, [])
            if len(found) != 1 or found[0]['parsed_method_sha256'] != digest:
                raise SpiritProbeError('sealed selected method digest drift: ' + name)
        anchors = sealed['anchors']
        if not 1 <= len(anchors) <= 40:
            raise SpiritProbeError('sealed anchor budget exceeded')
        seen = set()
        for anchor in anchors:
            key = (anchor['method'], anchor['kind'], anchor['offset'])
            if key in seen:
                raise SpiritProbeError('duplicate sealed control anchor')
            seen.add(key)
            found = methods.get(anchor['method'], [])
            if len(found) != 1:
                raise SpiritProbeError('missing/ambiguous sealed anchor method')
            rows = found[0].get(anchor['kind'])
            if not isinstance(rows, list):
                raise SpiritProbeError('invalid sealed control group')
            matches = [row for row in rows if row['offset'] == anchor['offset']]
            if len(matches) != 1 or matches[0]['opcode'] != anchor['opcode']:
                raise SpiritProbeError('missing/changed sealed control opcode')
            if anchor.get('symbol_contains') and anchor['symbol_contains'] not in matches[0]['symbol']:
                raise SpiritProbeError('sealed symbolic operand drift')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--javap', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    manifest = json.loads(args.manifest.read_text(encoding='utf8'))
    check_sealed_manifest(report, manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf8')
    print('selected_spirit_dinosaur_methods=' + str(sum(x['selected_method_count'] for x in report['classes'])) + '; static_only')

if __name__ == '__main__':
    main()
