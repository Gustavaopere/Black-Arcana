#!/usr/bin/env python3
"""Read-only, fail-closed symbolic callsite inventory for exact Megido 4.0.3.

Output contains method names/counts, NEVER third-party bytecode or source bodies.
A direct callsite in this class does not prove a successful gameplay effect,
consumer geometry, safe mutation hook, or runtime test result.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

EXPECTED_SHA1 = 'e5051c2385a426d05bf203ba8081a23d891f6686'
CLASS = 'net.alshanex.alshanex_familiars.spells.MegidoSpell'
OWNER = CLASS.replace('.', '/')
GETTERS = ('getRange', 'getRadius')
HEADER = re.compile(r'^\s{2}(?:public|private|protected)\s+[^;]+\s+([\w$]+)\([^;]*\);\s*$')
INSTRUCTION = re.compile(r'^\s*(\d+):\s+(\w+)\s*(.*?)\s*$')
METHOD_REF = re.compile(r'//\s+(?:Method|InterfaceMethod)\s+((?:[\w/$]+\.)?[\w$]+):([\w/$;\[()]*)\s*$')


def inspect_javap(stdout: str) -> dict:
    declarations: dict[str,list[str]] = {}
    calls: list[tuple[str,str,str]] = []
    current = None
    descriptor = None
    in_code = False
    methods_with_code: set[str] = set()

    for line in stdout.splitlines():
        h = HEADER.fullmatch(line)
        if h:
            current = h.group(1)
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
        s = line.strip()
        if s.startswith('descriptor:'):
            descriptor = s[len('descriptor:'):].strip()
            declarations.setdefault(current,[]).append(descriptor)
        elif s == 'Code:':
            in_code = descriptor is not None
            if in_code:
                methods_with_code.add(current)
        elif in_code:
            ins = INSTRUCTION.fullmatch(line)
            if not ins or not ins.group(2).startswith('invoke'):
                continue
            op, args = ins.group(2), ins.group(3)
            ref = METHOD_REF.search(args)
            if not ref:
                continue
            name_with_owner, target_desc = ref.groups()
            if '.' in name_with_owner:
                target_owner, name = name_with_owner.rsplit('.',1)
                if target_owner not in (OWNER,CLASS):
                    continue
            else:
                name = name_with_owner
            if name in GETTERS and target_desc == '()F':
                calls.append((current,name,op))

    for name in GETTERS:
        if declarations.get(name) != ['()F'] or name not in methods_with_code:
            raise ValueError('missing or duplicate exact getter '+name)
    if 'onCast' not in declarations or 'onCast' not in methods_with_code:
        raise ValueError('missing onCast implementation')
    if len(calls) > 256:
        raise ValueError('excessive getter reference inventory')

    results = {}
    for getter in GETTERS:
        matching = [c for c in calls if c[1] == getter]
        callers = sorted({c[0] for c in matching})
        results[getter] = {
            'status': 'SAME_CLASS_DIRECT_CALLS_FOUND' if matching else 'NO_SAME_CLASS_DIRECT_CALL_SEEN',
            'same_class_calls': len(matching),
            'direct_on_cast_calls': sum(1 for c in matching if c[0] == 'onCast'),
            'calling_methods': callers,
        }
    return results


def audit(jar: Path) -> dict:
    h=hashlib.sha1()
    with jar.open('rb') as f:
        for buf in iter(lambda: f.read(1024 * 1024), b''):
            h.update(buf)
    if h.hexdigest() != EXPECTED_SHA1:
        raise ValueError('SHA-1 mismatch: refuse bytecode inspection')
    p = subprocess.run(['javap','-classpath',str(jar),'-p','-s','-c',CLASS],
                       capture_output=True,text=True,check=False,timeout=30)
    if p.returncode:
        raise ValueError('javap exact class failed')
    return {
        'schema_version':1,
        'artifact_sha1':EXPECTED_SHA1,
        'provider_version':'1.21.1_v4.0.3',
        'class_name':CLASS,
        'scope':'SAME_CLASS_DIRECT_GETTER_CALLSITES_ONLY',
        'external_consumer_classes':'NOT_AUDITED',
        'effective_spell_geometry':'NOT_VERIFIED',
        'mutating_hook':'NOT_VERIFIED',
        'physical_qa':'NOT_TESTED',
        'getters':inspect_javap(p.stdout),
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    report=audit(a.jar)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    for name, result in report['getters'].items():
        print(name, result['status'], 'same-class=',result['same_class_calls'],
              'direct-onCast=',result['direct_on_cast_calls'],
              'callers=',','.join(result['calling_methods']))
    print('Only aggregate invocation metadata saved; no method bodies stored.')


if __name__ == '__main__':
    main()
