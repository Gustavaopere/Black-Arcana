#!/usr/bin/env python3
"""Read-only SHA-exact Galena / ACCompat 1.0.10 helper JVM causal checker.

Validates exact publisher method body digests and selected typed JVM boundaries.
Negative tests forge report-only instructions (not a new JAR) and re-seal digests;
NO_MUTATION, no assumption of Minecraft internals, and no perk certification.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

REPORT_SHA = 'ca395f3418979d8302363cf9db8d54c620572b16ebdc2ecacee5014fce0add64'
REPORT_BYTES = 26782
PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
CLASS_SHA = '333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b'
OWNER = 'com/github/alexmodguy/alexscaves/server/misc/ACCompat'
SCOPE = 'ALEXSCAVES_1010_GALENA_ACCOMPAT_HELPER_CAUSAL_STATIC_ONLY'
REPORT_SCOPE = 'GALENA_ACCOMPAT_HELPERS_JVM_DISCOVERY_NOT_CERTIFIED'
SOURCE_SHA = 'c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9'
EXPECTED = {'getCompound', 'getInt', 'getOrCreateTag', 'getTag', 'getUUID', 'hasUUID',
            'loadStack', 'putUUID', 'saveStack', 'setTag'}
STATES={'static_contract':'NOT_CERTIFIED','mutating_hook':'NOT_VERIFIED',
        'physical_qa':'NOT_TESTED','mutation':'NO_MUTATION',
        'perk_certification':'NOT_CERTIFIED','provider_universe_closed':False,
        'installed_dump_parity':'NOT_VERIFIED','semantic_magic_roots_delta':0}
MANDATORY = {
    'getCompound':[(2,'invokevirtual','CompoundTag.getCompound:')],
    'getInt':[(2,'invokevirtual','CompoundTag.getInt:')],
    'getOrCreateTag':[(1,'getstatic','DataComponents.CUSTOM_DATA:'),
        (4,'invokevirtual','ItemStack.get:'),(12,'ifnonnull',''),
        (15,'new','CompoundTag'),(26,'invokevirtual','CustomData.copyTag:')],
    'getTag':[(1,'getstatic','DataComponents.CUSTOM_DATA:'),
        (4,'invokevirtual','ItemStack.get:'),(12,'ifnonnull',''),
        (15,'aconst_null',''),(20,'invokevirtual','CustomData.copyTag:')],
    'getUUID':[(2,'invokevirtual','CompoundTag.getUUID:')],
    'hasUUID':[(2,'invokevirtual','CompoundTag.hasUUID:')],
    'loadStack':[(2,'invokestatic','ItemStack.parse:'),(5,'getstatic','ItemStack.EMPTY:'),
                 (8,'invokevirtual','Optional.orElse:')],
    'putUUID':[(3,'invokevirtual','CompoundTag.putUUID:')],
    'saveStack':[(2,'invokevirtual','ItemStack.save:'),(5,'checkcast','CompoundTag')],
    'setTag':[(1,'ifnonnull',''),(8,'invokevirtual','ItemStack.remove:'),
              (20,'invokestatic','CustomData.of:'),(23,'invokevirtual','ItemStack.set:')],
}

def require(pred,msg):
    if not pred: raise ValueError(msg)

def no_duplicates(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key '+k)
        d[k]=v
    return d

def sha(raw):return hashlib.sha256(raw).hexdigest()

def canonical_sha(ins):return sha((json.dumps(ins,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())

def load(path,size):
    raw=Path(path).read_bytes()
    require(0<len(raw)<=size,'file size exceeds bounded audit')
    return raw,json.loads(raw,object_pairs_hook=no_duplicates)

def check(report,manifest,raw,*,reseal=False):
    require(report['schema_version']==manifest['schema_version']==1,'schema drift')
    require(report['scope']==REPORT_SCOPE and manifest['scope']==SCOPE,'scope drift')
    ev=manifest['evidence']
    require(ev['report_bytes']==len(raw) and ev['report_sha256']==sha(raw),'report digest drift')
    require(reseal or (sha(raw)==REPORT_SHA and len(raw)==REPORT_BYTES),'official helper report hash drift')
    require(ev['source_workflow_run_id']==45077106620 and ev['source_artifact_id']==14775313807 and
            ev['caller_report_sha256']==SOURCE_SHA,'provenance drift')
    art=report['artifact']
    require(art==manifest['publisher'] and art['sha256']==PUBLISHER_SHA and
            art['size_bytes']==75279314 and art['version']=='1.0.10' and
            art['installed_dump_parity']=='NOT_VERIFIED','publisher identity drift')
    require(manifest['states']==STATES,'status drift')
    require(all(report[k]==STATES[k] for k in ['static_contract','mutating_hook','physical_qa',
            'mutation','provider_universe_closed','semantic_magic_roots_delta']),
            'provider safety drift')
    require(report['limits']['save_restart_recovery']=='NOT_TESTED' and
            report['limits']['minecraft_engine_helpers']=='NOT_VERIFIED',
            'engine/runtime limit drift')
    cls=report['class'];ident=manifest['class']
    require(ident=={'owner':OWNER,'sha256':CLASS_SHA,'declared_methods':200,'fields':3} and
            {k:cls[k] for k in ('owner','sha256','declared_methods','fields')}==ident,
            'exact ACCompat class identity drift')
    methods={(x['declaration']['name'],x['declaration']['descriptor']):x
             for x in cls['selected_methods']}
    require(len(methods)==len(cls['selected_methods'])==10,'native method roster ambiguity')
    specs=manifest['methods']
    require(len(specs)==10 and {s['name'] for s in specs}==EXPECTED and
            len({(s['name'],s['descriptor']) for s in specs})==10,
            'selected exact method roster drift')
    total=0
    for spec in specs:
        name,key=spec['name'],(spec['name'],spec['descriptor'])
        require(key in methods,'missing native method '+name)
        m=methods[key];d=m['declaration'];body=m['instructions']
        require(d['code_sha256']==spec['code_sha256'] and m['instruction_sha256']==
                spec['instruction_sha256']==canonical_sha(body) and
                m['instruction_count']==spec['instruction_count']==len(body),
                'native helper class Code/instruction SHA/count drift '+name)
        offsets=[p['offset'] for p in spec['pivots']]
        require(offsets==sorted(set(offsets)),'pivot roster unsorted or duplicated '+name)
        found={ins['offset']:ins for ins in body}
        require(len(found)==len(body),'duplicate JVM instruction offset '+name)
        for p in spec['pivots']:
            require(found.get(p['offset'])==p,
                    'causal JVM pivot differs '+name+'@'+str(p['offset']))
            total+=1
        for offset,op,token in MANDATORY[name]:
            row=found.get(offset)
            require(row is not None and row['opcode']==op and token in row['symbol'],
                    'causal JVM invariant differs '+name+'@'+str(offset))
    require(total==43,'causal JVM pivot count drift')
    source=report['caller_evidence']
    require(source['source_sha256']==SOURCE_SHA and source['source_bytes']==1780492,
            'Galena physical caller source changed')
    calls=source['typed_callsites']
    require(calls==manifest['typed_caller_sites'] and len(calls)==17,
            '17 exact typed item/entity callsite identities drift')
    require({x['callee_name'] for x in calls}==EXPECTED,'consumer helper roster mismatch')
    require(all(x['opcode']=='invokestatic' and x['callee_descriptor'].startswith('(')
                for x in calls),'caller bytecode type drift')
    require({(x['callee_name'],x['callee_descriptor']) for x in calls}==set(methods),
            'callee descriptors do not reconcile with caller method invocations')
    return total

def adversarial(report,manifest):
    cases=[('getCompound',2,'opcode'),('getInt',2,'opcode'),
           ('getOrCreateTag',12,'operand'),('getOrCreateTag',26,'opcode'),
           ('getTag',12,'operand'),('getTag',20,'opcode'),
           ('getUUID',2,'opcode'),('hasUUID',2,'opcode'),
           ('loadStack',2,'opcode'),('loadStack',5,'opcode'),('loadStack',8,'opcode'),
           ('putUUID',3,'opcode'),('saveStack',2,'opcode'),('saveStack',5,'opcode'),
           ('setTag',1,'operand'),('setTag',8,'opcode'),('setTag',20,'opcode'),
           ('setTag',23,'opcode')]
    for name,off,kind in cases:
        altered=copy.deepcopy(report);seal=copy.deepcopy(manifest)
        m=next(x for x in altered['class']['selected_methods'] if x['declaration']['name']==name)
        instruction=next(i for i in m['instructions'] if i['offset']==off)
        if kind=='opcode':
            require(instruction['opcode']!='nop','invalid adversarial opcode')
            instruction['opcode']='nop'
        else:
            require(instruction['operand'] not in ('','99999'),'invalid adversarial branch')
            instruction['operand']='99999'
        m['instruction_sha256']=canonical_sha(m['instructions'])
        next(s for s in seal['methods'] if s['name']==name)['instruction_sha256']=m['instruction_sha256']
        forged=json.dumps(altered,ensure_ascii=False,sort_keys=True).encode()
        seal['evidence']['report_sha256']=sha(forged)
        seal['evidence']['report_bytes']=len(forged)
        try:check(altered,seal,forged,reseal=True)
        except ValueError as exc:
            require('causal JVM' in str(exc),'negative test rejected for wrong reason: '+str(exc))
        else:raise AssertionError('forged JVM report accepted: '+name+'@'+str(off))
    print('PASS:',len(cases),'independent resealed report-only causal forgeries rejected')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--adversarial',action='store_true')
    args=p.parse_args()
    raw,r=load(args.report,80_000);_,m=load(args.manifest,40_000)
    pivots=check(r,m,raw)
    print('PASS: 10 publisher-native ACCompat methods,',pivots,
          'JVM pivots, 17 pinned caller sites; NO_MUTATION')
    if args.adversarial:adversarial(r,m)
    print('NOT_CERTIFIED NOT_VERIFIED NOT_TESTED')
