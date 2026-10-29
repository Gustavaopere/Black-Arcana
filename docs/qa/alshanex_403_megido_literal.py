#!/usr/bin/env python3
"""Fail-closed exact Alshanex 4.0.3 Megido numeric probe.

javap output is transient; the report contains only two numeric results or
NOT_VERIFIED, never disassembly, code bodies or assets.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

EXPECTED='e5051c2385a426d05bf203ba8081a23d891f6686'
CLASS='net.alshanex.alshanex_familiars.spells.MegidoSpell'
GETTERS=('getRange', 'getRadius')
HEADER=re.compile(r'^\s{2}(?:public|private|protected)\s+float\s+(getRadius|getRange)\(\);\s*$')
OPCODE=re.compile(r'^\s*(\d+):\s+([a-z][\w]*)\s*(.*?)\s*$')
FLOAT=re.compile(r'^#\d+\s+// float\s+(-?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)[fF]?\s*$')


def literal(instructions):
    if len(instructions)!=2 or instructions[0][0]!=0 or instructions[1][1]!='freturn':
        return None
    _,op,arg=instructions[0]
    if op in ('fconst_0','fconst_1','fconst_2') and not arg:
        return float(op[-1])
    if op in ('ldc','ldc_w'):
        found=FLOAT.fullmatch(arg)
        if found:
            value=float(found.group(1))
            if math.isfinite(value):
                return value
    return None


def inspect_javap(stdout):
    methods={}
    current=None
    descriptor=False
    code=False
    instructions=[]

    def finish():
        nonlocal current,descriptor,code,instructions
        if current and descriptor and code:
            if current in methods:
                raise ValueError('ambiguous duplicate getter '+current)
            value=literal(instructions)
            methods[current]={'status':'EXACT_DIRECT_FLOAT_LITERAL' if value is not None else 'DYNAMIC_NOT_VERIFIED','value':value}
        current=None
        descriptor=False
        code=False
        instructions=[]

    for line in stdout.splitlines()+['']:
        header=HEADER.fullmatch(line)
        if header:
            finish()
            current=header.group(1)
            continue
        if current is None:
            continue
        trimmed=line.strip()
        if trimmed.startswith('descriptor:'):
            descriptor=trimmed=='descriptor: ()F'
        elif trimmed=='Code:':
            code=descriptor
        elif not trimmed or trimmed.startswith('}'):
            finish()
        elif code:
            match=OPCODE.fullmatch(line)
            if match:
                instructions.append((int(match.group(1)),match.group(2),match.group(3).strip()))
            else:
                code=False
    for name in GETTERS:
        if name not in methods:
            raise ValueError('missing exact ()F getter '+name)
    return {k:methods[k] for k in GETTERS}


def audit(jar):
    h=hashlib.sha1()
    with Path(jar).open('rb') as fd:
        for part in iter(lambda: fd.read(1024*1024),b''):
            h.update(part)
    if h.hexdigest()!=EXPECTED:
        raise ValueError('SHA-1 mismatch before inspection')
    proc=subprocess.run(['javap','-classpath',str(jar),'-p','-s','-c',CLASS],
                        capture_output=True,text=True,check=False,timeout=30)
    if proc.returncode:
        raise ValueError('javap exact class failed')
    return {'schema_version':1,'artifact_sha1':EXPECTED,'provider_version':'1.21.1_v4.0.3',
            'class_name':CLASS,'scope':'TWO_DIRECT_FLOAT_GETTER_RETURNS_ONLY',
            'mutating_hook':'NOT_VERIFIED','physical_qa':'NOT_TESTED',
            'getters':inspect_javap(proc.stdout)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=audit(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf8')
    for k,v in result['getters'].items():
        print(k+': '+v['status']+' '+str(v['value']))
    print('No disassembly or third-party implementation retained.')


if __name__=='__main__':
    main()
