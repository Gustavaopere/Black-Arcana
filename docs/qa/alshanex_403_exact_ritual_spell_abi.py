#!/usr/bin/env python3
"""Fail-closed, bounded identity/schema/ABI inspection of Alshanex 4.0.3.

No JAR bytes, recipe JSON, disassembly, method bodies, assets or item recipes
are copied into output. Factual metadata only, to aid clean-room integration.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

EXPECTED_SHA1 = 'e5051c2385a426d05bf203ba8081a23d891f6686'
PREFIX = 'data/alshanex_familiars/recipe/ritual_recipes/'
SPELL_PREFIX = 'net/alshanex/alshanex_familiars/spells/'
RITUAL_TYPE = 'alshanex_familiars:ritual_recipe'
RITUALS = (
    'archmage_shard', 'druid_shard', 'frostling_shard', 'hunter_shard',
    'lightning_mage_shard', 'magic_power_tier_2', 'magic_power_tier_3',
    'magic_resist_tier_2', 'magic_resist_tier_3', 'summoner_shard',
    'truth_mirror',
)
SPELLS = {
    'summon_shadows': 'ShadowSummonSpell',
    'ice_age': 'IceAgeSpell',
    'ice_chamber': 'IceChamberSpell',
    'megido': 'MegidoSpell',
    'fire_fist': 'HikenSpell',
    'end_mayhem': 'EndMayhemSpell',
    'switcheroo': 'SwitcherooSpell',
}

class AuditError(ValueError):
    pass


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _kind(value):
    if value is None:
        return 'absent'
    if isinstance(value, dict):
        return 'object'
    if isinstance(value, list):
        return 'array'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, (int, float)):
        return 'number'
    if isinstance(value, str):
        return 'string'
    return 'other'


def _result_id(result):
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ('id', 'item', 'name'):
            val = result.get(key)
            if isinstance(val, str):
                return val
    raise AuditError('missing factual recipe result ID')


def inspect_zip(z):
    paths = set(z.namelist())
    actual = sorted(p[len(PREFIX):-5] for p in paths if p.startswith(PREFIX) and p.endswith('.json'))
    if actual != sorted(RITUALS):
        raise AuditError(f'ritual path inventory drift: {actual!r}')
    ritual_summary = []
    for name in RITUALS:
        path = PREFIX + name + '.json'
        obj = json.loads(z.read(path).decode('utf-8'), object_pairs_hook=_unique)
        if not isinstance(obj, dict) or obj.get('type') != RITUAL_TYPE:
            raise AuditError(f'ritual type mismatch: {name}')
        result = _result_id(obj.get('result'))
        expected = 'alshanex_familiars:' + name
        if result != expected:
            raise AuditError(f'ritual result identity drift for {name}: {result}')
        inputs = obj.get('inputs')
        # Do not invent defaults, or pretend a non-array is four pedestal slots.
        input_summary = []
        if isinstance(inputs, list):
            for entry in inputs:
                if not isinstance(entry, dict):
                    input_summary.append({'kind': _kind(entry)})
                else:
                    input_summary.append({
                        'kind': 'object',
                        'keys': sorted(entry.keys()),
                        'count_explicit': 'count' in entry,
                        'consume_explicit': 'consume' in entry,
                        'consume_false': entry.get('consume') is False,
                        'ingredient_kind': _kind(entry.get('ingredient')),
                    })
        output = obj['result']
        ritual_summary.append({
            'id': 'alshanex_familiars:' + name,
            'resource_path': path,
            'result_id': result,
            'top_level_keys': sorted(obj),
            'central_item_kind': _kind(obj.get('central_item')),
            'inputs_kind': _kind(inputs),
            'inputs_count': len(inputs) if isinstance(inputs, list) else None,
            'input_shapes': input_summary,
            'result_kind': _kind(output),
            'result_keys': sorted(output) if isinstance(output, dict) else [],
            'result_count_explicit': isinstance(output, dict) and 'count' in output,
            'particle_type_kind': _kind(obj.get('particle_type')),
        })
    for sid, cname in SPELLS.items():
        expected = SPELL_PREFIX + cname + '.class'
        if expected not in paths:
            raise AuditError(f'missing registered spell class {sid}: {expected}')
    return ritual_summary


def parse_javap_abi(stdout: str, class_name: str):
    """Return *only* method names and JVM descriptors, never bytecode."""
    result = []
    last_name = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.endswith(';') and '(' in stripped and not stripped.startswith('descriptor:'):
            match = re.search(r'([A-Za-z_$][\w$]*)\s*\(', stripped)
            last_name = match.group(1) if match else None
        elif stripped.startswith('descriptor:') and last_name is not None:
            descriptor = stripped[len('descriptor:'):].strip()
            if not re.fullmatch(r'\([\w/;$\[ZBCDFIJSV]*\)[\w/;$\[ZBCDFIJSV]+', descriptor):
                raise AuditError(f'invalid JVM method descriptor: {descriptor}')
            result.append({'name': last_name, 'descriptor': descriptor})
            last_name = None
    if not result:
        raise AuditError(f'no ABI methods found for {class_name}')
    return result


def audit(jar_path: Path):
    h = hashlib.sha1()
    with jar_path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    if h.hexdigest() != EXPECTED_SHA1:
        raise AuditError('SHA-1 mismatch: refusing to inspect any archive content')
    with zipfile.ZipFile(jar_path) as z:
        rituals = inspect_zip(z)
    spells = []
    for spell_id, cls in SPELLS.items():
        fqcn = 'net.alshanex.alshanex_familiars.spells.' + cls
        proc = subprocess.run(['javap', '-classpath', str(jar_path), '-p', '-s', fqcn], capture_output=True, text=True, timeout=30, check=False)
        if proc.returncode:
            raise AuditError(f'javap failed for {cls}: {proc.returncode}')
        methods = parse_javap_abi(proc.stdout, cls)
        spells.append({'spell_id': 'alshanex_familiars:' + spell_id, 'class_name': fqcn,
                       'declared_method_abi': methods})
    return {
        'schema_version': 1,
        'scope': 'EXACT_JAR_FINGERPRINTED_METADATA_AND_ABI_ONLY',
        'artifact_version': '1.21.1_v4.0.3',
        'artifact_sha1': EXPECTED_SHA1,
        'identity_inventory': {'spells': len(spells), 'rituals': len(rituals)},
        'source_code_or_method_bodies_extracted': False,
        'physical_runtime_qa': 'NOT_TESTED',
        'mutating_provider_hook': 'NOT_VERIFIED',
        'ritual_resources': rituals,
        'spell_class_abi': spells,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jar', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('PASS: exactly pinned Alshanex 4.0.3; 7 spell ABI classes; 11 ritual schema summaries')
    print('ritual shape counts:', [(r['id'].split(':')[1], r['inputs_count'], r['central_item_kind']) for r in report['ritual_resources']])
    print('spell method ABI names:', [(s['spell_id'].split(':')[1], [m['name'] for m in s['declared_method_abi']]) for s in report['spell_class_abi']])


if __name__ == '__main__':
    main()
