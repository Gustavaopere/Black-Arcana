#!/usr/bin/env python3
"""Exact Alshanex Megido: bounded first-use observation after getter calls.

Read-only evidence: exact SHA before javap; no third-party bytecode, assets,
control-flow reconstruction, or decompiled methods stored or published.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

EXPECTED = 'e5051c2385a426d05bf203ba8081a23d891f6686'
CLASS = 'net.alshanex.alshanex_familiars.spells.MegidoSpell'
OWNER = CLASS.replace('.', '/')
GETTERS = ('getRange', 'getRadius')
OTHER = ('getDamage', 'getMaxConnections')
METHOD = re.compile(r'^\s{2}(?:public|protected|private)\s+[^;]*\b([A-Za-z_$][\w$]*)\([^;]*\);\s*$')
OP = re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)\s*(.*?)\s*$')
REF = re.compile(r'//\s+(?:InterfaceMethod|Method)\s+([^:]+):(\([^)]*\)[^ \t]+)')
FLOAT_OPS = {'fadd', 'fsub', 'fmul', 'fdiv', 'frem', 'fcmpg', 'fcmpl'}


def parse_calls(stdout: str) -> dict:
    declarations: dict[str, set[str]] = {}
    methods: dict[str, list[tuple[str, str]]] = {}
    current = None
    descriptor = None
    in_code = False
    for line in stdout.splitlines():
        header = METHOD.fullmatch(line)
        if header:
            current = header.group(1)
            descriptor = None
            in_code = False
            continue
        if line.strip() == '}':
            current = None
            descriptor = None
            in_code = False
            continue
        if current is None:
            continue
        stripped = line.strip()
        if stripped.startswith('descriptor:'):
            descriptor = stripped[len('descriptor:'):].strip()
            declarations.setdefault(current, set()).add(descriptor)
        elif stripped == 'Code:':
            in_code = descriptor is not None
            if in_code:
                methods.setdefault(current, [])
        elif in_code:
            m = OP.fullmatch(line)
            if m:
                methods[current].append((m.group(2), m.group(3).strip()))

    if declarations.get('getRange') != {'()F'} or declarations.get('getRadius') != {'()F'}:
        raise ValueError('getter ABI drift')
    if len(declarations.get('onCast', set())) != 1 or 'onCast' not in methods:
        raise ValueError('onCast ABI or code missing')
    for name in OTHER:
        if name not in declarations:
            raise ValueError('missing declared method ' + name)

    def self_target(arg):
        match = REF.search(arg)
        if not match:
            return None
        symbol, desc = match.groups()
        if '.' in symbol:
            owner, name = symbol.rsplit('.', 1)
            if owner not in (OWNER, CLASS):
                return None
        else:
            name = symbol
        if desc not in declarations.get(name, set()):
            return None
        return name, desc

    def immediate(opcode):
        if opcode in ('f2d', 'f2i', 'f2l'):
            return 'FLOAT_PRIMITIVE_CONVERSION'
        if opcode == 'freturn':
            return 'FLOAT_RETURN'
        if opcode.startswith('fstore'):
            return 'STORED_TO_LOCAL'
        if opcode in FLOAT_OPS:
            return 'FLOAT_ARITHMETIC_OR_COMPARISON'
        if opcode in ('dup', 'dup_x1', 'dup_x2', 'dup2'):
            return 'STACK_DUPLICATION'
        return 'NEXT_INSTRUCTION_NOT_PROVEN_CONSUMER'

    instructions = methods['onCast']
    getter_sites = {g: [] for g in GETTERS}
    other_counts = {x: 0 for x in OTHER}
    for i, (opcode, arg) in enumerate(instructions):
        if not opcode.startswith('invoke'):
            continue
        target = self_target(arg)
        if not target:
            continue
        name, _ = target
        if name in getter_sites:
            if i + 1 >= len(instructions):
                raise ValueError('getter call without following instruction')
            next_op = instructions[i+1][0]
            getter_sites[name].append({'first_following_category': immediate(next_op)})
        elif name in other_counts:
            other_counts[name] += 1
    if any(len(getter_sites[g]) != 1 for g in GETTERS):
        raise ValueError('expected exactly one direct onCast getter call per getter')
    if len(instructions) > 5000 or any(n > 256 for n in other_counts.values()):
        raise ValueError('unexpectedly large method contract')
    return {
        'getters': {
            g: {'direct_on_cast_call_count': len(getter_sites[g]),
                'first_following_category': getter_sites[g][0]['first_following_category'],
                'full_value_flow': 'NOT_VERIFIED'} for g in GETTERS
        },
        'other_declared_methods_directly_called_from_on_cast': {
            k: {'count': v, 'status': 'SAME_CLASS_DIRECT_CALLS_FOUND' if v else 'NO_SAME_CLASS_DIRECT_CALL_SEEN'}
            for k, v in other_counts.items()
        }
    }


def audit(path: Path) -> dict:
    digest = hashlib.sha1()
    with path.open('rb') as fd:
        for data in iter(lambda: fd.read(1024 * 1024), b''):
            digest.update(data)
    if digest.hexdigest() != EXPECTED:
        raise ValueError('JAR SHA-1 mismatch before bytecode inspection')
    proc = subprocess.run(['javap', '-classpath', str(path), '-p', '-s', '-c', CLASS],
                          capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode:
        raise ValueError('javap unable to inspect exact class')
    return {
        'schema_version': 1,
        'provider': 'alshanex_familiars',
        'artifact_version': '4.0.3',
        'artifact_sha1': EXPECTED,
        'scope': 'SAME_CLASS_ONCAST_CALL_AND_IMMEDIATE_OPCODE_CATEGORY_ONLY',
        'reported_code_or_disassembly': False,
        'world_runtime_qa': 'NOT_TESTED',
        'mutating_hook': 'NOT_VERIFIED',
        'results': parse_calls(proc.stdout),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jar', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = audit(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('PASS: exact 4.0.3 bounded onCast first-use categories')
    for k, v in result['results']['getters'].items():
        print(k, v['first_following_category'])
    for k, v in result['results']['other_declared_methods_directly_called_from_on_cast'].items():
        print(k, 'direct onCast calls', v['count'])


if __name__ == '__main__':
    main()
