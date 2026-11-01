#!/usr/bin/env python3
"""Read-only, bounded compiled 1.0.10 Tremorzilla beam damage seam.
No gameplay execution, complete CFG, copied source, or mutating hook claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file

CLASS = 'com/github/alexmodguy/alexscaves/server/entity/living/TremorzillaEntity.class'
CLASS_SHA = 'e1ac60a8005f9414dde1d25a92a2110df65cef145c3225e9c2557c96672fe8dc'
FACTORY = 'ACDamageTypes.causeTremorzillaBeamDamage:'
HURT = 'hurtEntitiesAround'
DESCRIPTOR = '(Lnet/minecraft/world/phys/Vec3;FFFZZZ)Z'
FACTORY_OFFSET = 76
RELATED = re.compile(r'(beam|laser|ray|shoot|charge|attack|hurt|roar|explode|destroy|nuke|tick|animation)', re.I)
REF_OPS = {'invokevirtual', 'invokestatic', 'invokeinterface', 'invokespecial',
           'getfield', 'putfield', 'getstatic', 'putstatic', 'instanceof', 'checkcast'}
NUM_OPS = {'ldc', 'ldc_w', 'ldc2_w', 'bipush', 'sipush'}
BRANCH_OPS = {'goto', 'goto_w', 'tableswitch', 'lookupswitch'}
MAX_EXPORT = 190000


class BeamProbeError(ValueError):
    pass


def method_name(method):
    return method['header'].split('(', 1)[0].split()[-1].rsplit('.', 1)[-1]


def method_digest(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def bounded(rows, limit):
    return {'observed_total': len(rows), 'exported': rows[:limit],
            'truncated': len(rows) > limit}


def window(method, bci, *, before=12, after=16):
    insns = method['instructions']
    matches = [i for i, op in enumerate(insns) if op['offset'] == bci]
    if len(matches) != 1:
        raise BeamProbeError('ambiguous/missing exact bytecode offset')
    k = matches[0]
    return {'offset': bci, 'instruction_window': insns[max(0, k-before):k+after+1]}


def verify_factory(method):
    if method_name(method) != HURT or method['descriptor'] != DESCRIPTOR:
        raise BeamProbeError('wrong damage consumer JVM method or descriptor')
    found = [i for i in method['instructions'] if i['offset'] == FACTORY_OFFSET]
    if len(found) != 1 or found[0]['opcode'] != 'invokestatic' or FACTORY not in found[0]['symbol']:
        raise BeamProbeError('missing exact beam damage factory invocation')
    return {'name': HURT, 'descriptor': DESCRIPTOR, 'bytecode_offset': FACTORY_OFFSET,
            'opcode': found[0]['opcode'], 'factory_symbol': found[0]['symbol']}


def inspect(methods):
    names = [(method_name(m), m['descriptor']) for m in methods]
    if len(names) != len(set(names)):
        raise BeamProbeError('duplicate parsed method signature')
    found = [m for m in methods if method_name(m) == HURT and m['descriptor'] == DESCRIPTOR]
    if len(found) != 1:
        raise BeamProbeError('missing/ambiguous beam damage consumer')
    hurt = found[0]
    ins = hurt['instructions']
    if not 1 <= len(ins) <= 6500 or len({i['offset'] for i in ins}) != len(ins):
        raise BeamProbeError('invalid or duplicated target instructions')
    anchor = verify_factory(hurt)
    refs = [i for i in ins if i['opcode'] in REF_OPS]
    nums = [i for i in ins if i['opcode'] in NUM_OPS or i['opcode'].startswith(
        ('iconst_', 'fconst_', 'dconst_', 'lconst_'))]
    branches = [i for i in ins if i['opcode'].startswith('if') or i['opcode'] in BRANCH_OPS]
    owner_callers = []
    beam_related = []
    for method in methods:
        n = method_name(method)
        calls = [i for i in method['instructions']
                 if i['opcode'].startswith('invoke') and
                 (HURT + ':' in i['symbol'])]
        if calls:
            owner_callers.append({
                'method': n, 'descriptor': method['descriptor'],
                'parsed_method_sha256': method_digest(method),
                'sites': [window(method, op['offset'], before=5, after=9) for op in calls[:8]],
                'site_count': len(calls)
            })
        if RELATED.search(n) and method['instructions']:
            beam_related.append({
                'method': n, 'descriptor': method['descriptor'],
                'instruction_count': len(method['instructions']),
                'parsed_method_sha256': method_digest(method),
                'beam_symbols': bounded([
                    {'offset': i['offset'], 'opcode': i['opcode'], 'symbol': i['symbol']}
                    for i in method['instructions'] if i['opcode'] in REF_OPS and
                    re.search(r'(beam|laser|ray|shoot|charge|attack|hurt|target|entity|explode|destroy|fire|level|particle)', i['symbol'], re.I)
                ], 35)
            })
    if len(owner_callers) > 70 or len(beam_related) > 110:
        raise BeamProbeError('selected caller/related method roster exceeds bound')
    return {
        'declared_method_count': len(methods),
        'damage_factory_anchor': anchor,
        'damage_method': {
            'method': HURT, 'descriptor': DESCRIPTOR,
            'parsed_method_sha256': method_digest(hurt),
            'instruction_count': len(ins),
            'references': bounded(refs, 120), 'numeric_constants': bounded(nums, 100),
            'branches': bounded(branches, 130),
            'factory_window': window(hurt, FACTORY_OFFSET),
            'hurt_call_windows': [window(hurt, i['offset'], before=7, after=10)
                                  for i in ins if i['opcode'].startswith('invoke')
                                  and re.search(r'(ACCompat.hurt|LivingEntity.hurt|Entity.hurt)', i['symbol'])][:12],
            'exact_damage_and_target_filters': 'INSPECTION_REQUIRED'
        },
        'local_hurtEntitiesAround_callers': owner_callers,
        'related_method_roster': beam_related
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise BeamProbeError('publisher JAR SHA/size mismatch')
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise BeamProbeError('duplicate ZIP member')
        if hashlib.sha256(archive.read(CLASS)).hexdigest() != CLASS_SHA:
            raise BeamProbeError('TremorzillaEntity class SHA changed')
    compiled = javap(javap_bin, jar, CLASS[:-6].replace('/', '.'))
    methods = parse_methods(compiled)
    result = {
        'schema_version': 1,
        'scope': 'SHA_EXACT_1010_TREMORZILLA_BEAM_SELECTED_JVM_CONSUMER_AND_CALLERS_ONLY',
        'artifact': {'sha1': SHA1, 'sha256': SHA256, 'size_bytes': SIZE},
        'class_path': CLASS,
        'class_sha256': CLASS_SHA,
        **inspect(methods),
        'limits': {
            'complete_method_body_exported': False,
            'full_control_flow_graph': 'NOT_RECONSTRUCTED',
            'final_effective_damage_or_PvP': 'NOT_CERTIFIED',
            'native_mutating_hook': 'NOT_VERIFIED',
            'physical_qa': 'NOT_TESTED',
            'provider_universe_closed': False
        }
    }
    if len(json.dumps(result, ensure_ascii=False).encode()) > MAX_EXPORT:
        raise BeamProbeError('bounded interoperability report size exceeded')
    return result


def verify_sealed_snapshot(report, seal):
    """Reject identity, method, caller, opcode and numeric drift; no runtime claims."""
    for field in ('schema_version', 'scope', 'artifact', 'class_path',
                  'class_sha256', 'declared_method_count', 'damage_factory_anchor'):
        if report.get(field) != seal.get(field):
            raise BeamProbeError('SHA-exact sealed identity drift: ' + field)
    observed = {
        (m['method'], m['descriptor']): m['parsed_method_sha256']
        for m in report['related_method_roster']
    }
    target = report['damage_method']
    observed[(target['method'], target['descriptor'])] = target['parsed_method_sha256']
    for m in report['local_hurtEntitiesAround_callers']:
        key = (m['method'], m['descriptor'])
        if key in observed and observed[key] != m['parsed_method_sha256']:
            raise BeamProbeError('related/caller duplicate method digest mismatch')
        observed[key] = m['parsed_method_sha256']
    desired = seal.get('selected_method_digests')
    if not isinstance(desired, list) or not 1 <= len(desired) <= 30:
        raise BeamProbeError('invalid selected method seal size')
    keys = [(m['name'], m['descriptor']) for m in desired]
    if len(keys) != len(set(keys)):
        raise BeamProbeError('duplicate sealed JVM method identity')
    for m in desired:
        if (not re.fullmatch(r'[0-9a-f]{64}', m['sha256']) or
                observed.get((m['name'], m['descriptor'])) != m['sha256']):
            raise BeamProbeError('sealed method digest/descriptor drift: ' + m['name'])
    recorded = {}
    for c in report['local_hurtEntitiesAround_callers']:
        k = (c['method'], c['descriptor'])
        if k in recorded:
            raise BeamProbeError('duplicate local caller')
        recorded[k] = [s['offset'] for s in c['sites']]
        if c['site_count'] != len(recorded[k]):
            raise BeamProbeError('truncated local hurt caller sites')
    required = seal.get('local_callers')
    if not isinstance(required, list) or len(required) > 30:
        raise BeamProbeError('invalid local caller seal')
    expected = {(c['method'], c['descriptor']): c['sites'] for c in required}
    if len(expected) != len(required) or expected != recorded:
        raise BeamProbeError('local native producer/callsite drift')
    anchors = seal.get('method_anchors')
    if not isinstance(anchors, list) or not 1 <= len(anchors) <= 70:
        raise BeamProbeError('invalid sealed opcode anchor budget')
    seen = set()
    for anchor in anchors:
        key = (anchor['group'], anchor['offset'])
        if key in seen:
            raise BeamProbeError('duplicate sealed opcode anchor')
        seen.add(key)
        if anchor['group'] not in ('references', 'numeric_constants', 'branches'):
            raise BeamProbeError('unexpected sealed opcode group')
        # Never treat truncated evidence as comprehensive.
        group = target[anchor['group']]
        if group['truncated']:
            raise BeamProbeError('sealed group is truncated')
        hits = [x for x in group['exported'] if x['offset'] == anchor['offset']]
        if len(hits) != 1 or hits[0]['opcode'] != anchor['opcode']:
            raise BeamProbeError('sealed opcode anchor drift')
        row = hits[0]
        if anchor.get('symbol_contains') and anchor['symbol_contains'] not in row['symbol']:
            raise BeamProbeError('sealed symbol anchor drift')
        if 'operand_equals' in anchor and row['operand'] != anchor['operand_equals']:
            raise BeamProbeError('sealed numeric/branch operand drift')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jar', type=Path, required=True)
    ap.add_argument('--javap', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    args = ap.parse_args()
    result = audit(args.jar, args.javap)
    seal = json.loads(args.manifest.read_text(encoding='utf-8'))
    verify_sealed_snapshot(result, seal)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n',
                           encoding='utf-8')
    print('exact_beam_method_count=' + str(result['declared_method_count']) +
          ' local_callers=' + str(len(result['local_hurtEntitiesAround_callers'])) +
          '; STATIC_ONLY; NO_RUNTIME_CERTIFICATION')


if __name__ == '__main__':
    main()
