#!/usr/bin/env python3
"""Read-only exact NeoForge 21.1.248 grief-event bytecode seam.

Static API/event flow is not a proof of permission from any loaded claims mod.
No provider code or bytecode is reproduced in the emitted evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

VERSION = '21.1.248'
CLASSES = {
    'EventHooks': 'net/neoforged/neoforge/event/EventHooks.class',
    'EntityMobGriefingEvent': 'net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.class',
}
METHODS = {
    'EventHooks': {
        'canEntityGrief': '(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;)Z',
    },
    'EntityMobGriefingEvent': {
        '<init>': '(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;)V',
        'canGrief': '()Z',
        'setCanGrief': '(Z)V',
        'isMobGriefingEnabled': '()Z',
    },
}
RE_INSN = re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(.*))?$')
RE_METHOD = re.compile(r'^\s{2,}(?:public|private|protected)\s+.*\(.*\);\s*$')
MAX_JAR = 20_000_000  # fail closed for unexpected universal JAR size
MAX_REPORT = 28_000

class EvidenceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def parse_methods(data):
    """Parse selected javap signatures and instructions, without exporting bodies."""
    lines = data.splitlines()
    methods = []
    for i, line in enumerate(lines):
        if not RE_METHOD.match(line):
            continue
        descriptor = None
        start = None
        for k in range(i+1, min(i+6, len(lines))):
            if lines[k].strip().startswith('descriptor:'):
                descriptor = lines[k].split('descriptor:',1)[1].strip()
            if lines[k].strip() == 'Code:':
                start = k+1
                break
        if descriptor is None or start is None:
            continue
        instructions = []
        for line2 in lines[start:]:
            hit = RE_INSN.match(line2)
            if hit:
                operand = (hit.group(3) or '').strip()
                instructions.append({'offset': int(hit.group(1)), 'opcode': hit.group(2),
                                     'operand': operand.split('//',1)[0].strip(),
                                     'symbol': operand.split('//',1)[1].strip() if '//' in operand else ''})
            elif instructions and (line2.strip() == '' or RE_METHOD.match(line2)):
                break
        name = line.split('(',1)[0].strip().rsplit(' ',1)[-1].split('.')[-1]
        if name == 'EntityMobGriefingEvent':
            name = '<init>'
        methods.append({'name':name,'descriptor':descriptor,'instructions':instructions})
    return methods


def selected(methods, name, desc):
    matches = [m for m in methods if m['name']==name and m['descriptor']==desc]
    require(len(matches)==1, 'missing or ambiguous descriptor: '+name+desc)
    m=matches[0]
    ins=m['instructions']
    require(1 <= len(ins) <= 300, 'unexpected selected-method instruction population')
    offs=[i['offset'] for i in ins]
    require(offs==sorted(set(offs)), 'invalid offsets')
    return m


def sites(m):
    return [{'offset':i['offset'],'opcode':i['opcode'],'symbol':i['symbol']}
            for i in m['instructions'] if i['symbol'] and i['opcode'].startswith(('invoke','get','put','new'))]


def has(m, opcode_prefix, symbol):
    return any(i['opcode'].startswith(opcode_prefix) and symbol in i['symbol'] for i in m['instructions'])


def inspect_selected(owner, m):
    ins=m['instructions']
    name=m['name']
    if owner=='EventHooks':
        require(name=='canEntityGrief', 'unexpected EventHooks method')
        require(any(i['opcode'] in ('ifnull','ifnonnull') for i in ins), 'entity-null branch absent')
        for op, symbol in [('invoke','Level.getGameRules:'),('getstatic','GameRules.RULE_MOBGRIEFING:'),
                           ('invoke','GameRules.getBoolean:'),('new','EntityMobGriefingEvent'),
                           ('getstatic','NeoForge.EVENT_BUS:'),('invoke','post:'),
                           ('invoke','EntityMobGriefingEvent.canGrief:')]:
            require(has(m,op,symbol), 'missing grief branch/delegate: '+symbol)
        require(sum(i['opcode']=='ireturn' for i in ins)==2, 'unexpected grief return path count')
    elif name=='<init>':
        for op,symbol in [('invoke','EntityEvent."<init>":'),('invoke','Level.getGameRules:'),
                          ('getstatic','GameRules.RULE_MOBGRIEFING:'),('invoke','GameRules.getBoolean:'),
                          ('putfield','isMobGriefingEnabled:'),('putfield','canGrief:')]:
            require(has(m,op,symbol), 'missing event initialization: '+symbol)
    elif name=='canGrief':
        require(has(m,'getfield','canGrief:'), 'event getter not backed by canGrief field')
        require(ins[-1]['opcode']=='ireturn', 'event getter return changed')
    elif name=='setCanGrief':
        require(has(m,'putfield','canGrief:'), 'event setter does not write canGrief')
        require(ins[-1]['opcode']=='return', 'event setter return changed')
    elif name=='isMobGriefingEnabled':
        require(has(m,'getfield','isMobGriefingEnabled:'), 'gamerule getter changed')
        require(ins[-1]['opcode']=='ireturn', 'gamerule getter return changed')
    else:
        raise EvidenceError('unrecognized method')
    return {'name': name, 'descriptor':m['descriptor'], 'instruction_count':len(ins),
            'method_sha256':sha256(json.dumps(ins,sort_keys=True,separators=(',',':')).encode()),
            'selected_references':sites(m)[:24], 'reference_count':len(sites(m))}


def examine_jar(jar, javap):
    jar=Path(jar)
    require(jar.is_file() and 10_000 < jar.stat().st_size < MAX_JAR, 'unexpected or missing universal jar')
    filebytes=jar.read_bytes()
    require(zipfile.is_zipfile(jar), 'not a ZIP archive')
    records=[]
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)), 'duplicate ZIP members')
        for owner,path in CLASSES.items():
            require(path in names, 'missing class in exact NeoForge jar: '+owner)
            cls=path[:-6].replace('/','.')
            ret=subprocess.run([javap,'-classpath',str(jar),'-p','-s','-c',cls],
                               capture_output=True,text=True,timeout=45,check=False)
            require(ret.returncode==0, 'javap failed: '+owner+' '+ret.stderr[:300])
            parsed=parse_methods(ret.stdout)
            chosen=[inspect_selected(owner,selected(parsed,n,d)) for n,d in METHODS[owner].items()]
            records.append({'owner':owner,'class_path':path,'class_sha256':sha256(z.read(path)),
                            'selected_methods':chosen})
    report={'schema_version':1,'scope':'EXACT_NEOFORGE_211248_CAN_ENTITY_GRIEF_EVENT_BYTECODE',
            'artifact':{'coordinates':'net.neoforged:neoforge:21.1.248:universal',
                        'size_bytes':len(filebytes),'sha256':sha256(filebytes)},
            'classes':records,
            'interpretation':'STATIC_EVENT_DELEGATION_ONLY_NOT_CLAIM_AUTHORIZATION',
            'limits':{'modpack_loader_21_1_250':'NOT_INSPECTED_HERE',
                      'third_party_claim_listeners':'NOT_VERIFIED',
                      'black_arcana_world_effect_policy':'NOT_VERIFIED',
                      'mutating_hook':'NOT_VERIFIED',
                      'physical_qa':'NOT_TESTED',
                      'mutation':'NO_MUTATION',
                      'perk_certification':'NOT_CERTIFIED'}}
    require(len(json.dumps(report).encode())<MAX_REPORT,'report budget exceeded')
    return report


def verify_seal(report, seal):
    for key in ('schema_version','scope','artifact','interpretation','limits'):
        require(report.get(key)==seal.get(key), 'seal mismatch: '+key)
    require(len(report['classes'])==len(seal.get('classes',[]))==2,'class universe changed')
    for observed, required in zip(report['classes'],seal['classes']):
        for field in ('owner','class_path','class_sha256'):
            require(observed[field]==required[field], 'class seal drift: '+field)
        a,b=observed['selected_methods'],required['selected_methods']
        require(len(a)==len(b), 'selected method count drift')
        for m,n in zip(a,b):
            for field in ('name','descriptor','method_sha256','instruction_count'):
                require(m[field]==n[field], 'method seal drift: '+field)
            require(m['selected_references']==n['selected_references'], 'callsite seal drift')
    return True


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jar',required=True)
    parser.add_argument('--javap',default='javap')
    parser.add_argument('--output',required=True)
    parser.add_argument('--seal')
    args=parser.parse_args()
    try:
        report=examine_jar(args.jar,args.javap)
        if args.seal:
            seal=json.loads(Path(args.seal).read_text(encoding='utf-8'))
            verify_seal(report,seal)
        Path(args.output).parent.mkdir(parents=True,exist_ok=True)
        Path(args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print('PASS: exact NeoForge grief event static flow; sha256='+report['artifact']['sha256'])
        print('limits: NO_MUTATION; NOT_CERTIFIED; claims/QA NOT_VERIFIED')
    except (EvidenceError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1,'FAIL-CLOSED: '+str(exc)+'\n')

if __name__=='__main__':
    main()