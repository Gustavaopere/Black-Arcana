#!/usr/bin/env python3
"""Read-only Galena Gauntlet persistence/controller synchronization JVM audit.

Source is the SHA-verified Alex's Caves Continued publisher 1.0.10 discovery
report. No runtime changes, mutating perks, or physical persistence claims.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

PUBLISHER_SHA="36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
CLASS_SHA="a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071"
SOURCE_SHA="c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9"
OWNER="com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
SCOPE="ALEXSCAVES_1010_GALENA_GAUNTLET_PERSISTENCE_SYNC_CONTROLLER_STATIC_ONLY"
METHODS={"<clinit>","<init>","defineSynchedData","addAdditionalSaveData",
         "readAdditionalSaveData","getController","getControllerUUID","setControllerUUID",
         "getItemStack","setItemStack","getTarget","tick"}
FIELDS={"ITEMSTACK","CONTROLLER_UUID","CONTROLLER_ID","TARGET_ID","IDLING",
        "prevStrikeProgress","strikeProgress","prevReturnProgress","returnProgress",
        "playerUseCooldown","comingBack","destroyBlockProgress","lastSelectedBlock",
        "totalMiningTime","hadPlayerController","spawnedItem","returnFlag"}
STATES={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION", "provider_universe_closed":False,
        "installed_dump_parity":"NOT_VERIFIED","perk_certification":"NOT_CERTIFIED",
        "semantic_magic_roots_delta":0}

def require(condition,msg):
    if not condition: raise ValueError(msg)

def no_dups(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,"duplicate JSON key "+k)
        out[k]=v
    return out

def read(path,maxbytes):
    raw=Path(path).read_bytes()
    require(0<len(raw)<=maxbytes,"bounded input violated")
    return raw,json.loads(raw,object_pairs_hook=no_dups)

def sha(data):return hashlib.sha256(data).hexdigest()

def canonical_sha(data):
    return sha((json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf8"))

def check(report,manifest,raw,*,test_reseal=False):
    require(manifest['schema_version']==report['schema_version']==1,"schema drift")
    require(manifest['scope']==SCOPE and report['scope']=="GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED","scope drift")
    ev=manifest['evidence']
    require(ev['report_sha256']==sha(raw) and ev['report_bytes']==len(raw),"report digest drift")
    require(test_reseal or (ev['report_sha256']==SOURCE_SHA and ev['report_bytes']==1780492),"official report drift")
    require(ev['source_workflow_run_id']==45071358036 and ev['source_artifact_id']==14773961125,
            "official provenance drift")
    p=report['artifact'];m=manifest['publisher']
    require(p==m and p['sha256']==PUBLISHER_SHA and p['size_bytes']==75279314 and
            p['version']=="1.0.10" and p['installed_dump_parity']=="NOT_VERIFIED",
            "publisher identity drift")
    require(report['mutation']=="NO_MUTATION" and report['mutating_hook']=="NOT_VERIFIED" and
            report['physical_qa']=="NOT_TESTED" and report['provider_universe_closed'] is False and
            report['semantic_magic_roots_certified_delta']==0,"source safety drift")
    require(manifest['states']==STATES,"status drift")
    targets=report['entity_native']['targets']
    require(set(targets)=={OWNER},"class discovery scope drift")
    entity=targets[OWNER]; mc=manifest['class']
    require(entity['class_sha256']==mc['sha256']==CLASS_SHA,"class SHA drift")
    require(len(entity['methods'])==mc['executables']==24 and len(entity['fields'])==17,
            "class method/field census drift")
    require(entity['fields']==mc['fields'] and {f['name'] for f in entity['fields']}==FIELDS,
            "typed accessor/field roster drift")
    require(report['entity_native']['class_entries_scanned']==1555,"class roster scanning drift")
    methods={(x['declaration']['name'],x['declaration']['descriptor']):x for x in entity['methods']}
    require(len(methods)==len(entity['methods']),"ambiguous overloaded method")
    specs=mc and manifest['methods']
    require(len(specs)==len(METHODS) and {s['name'] for s in specs}==METHODS,"selected method roster drift")
    require(len({(s['name'],s['descriptor']) for s in specs})==len(specs),"ambiguous requested method")
    pivots=0
    for s in specs:
        key=(s['name'],s['descriptor']); require(key in methods,"missing method "+s['name'])
        method=methods[key];body=method['instructions']
        require(method['declaration']['code_sha256']==s['code_sha256'],"Code SHA drift "+s['name'])
        require(method['instruction_count']==s['instruction_count']==len(body),"instruction count drift "+s['name'])
        require(method['instruction_sha256']==s['instruction_sha256']==canonical_sha(body),
                "instruction SHA drift "+s['name'])
        expected=s['pivots']; offsets=[p['offset'] for p in expected]
        require(offsets==sorted(set(offsets)) and len(expected)>=3,"pivot ordering/coverage drift "+s['name'])
        observed={row['offset']:row for row in body}
        require(len(observed)==len(body),"duplicate offset "+s['name'])
        for p in expected:
            row=observed.get(p['offset'])
            require(row is not None,"causal JVM missing offset "+s['name']+"@"+str(p['offset']))
            require(row['opcode']==p['opcode'],"causal JVM opcode drift "+s['name']+"@"+str(p['offset']))
            if 'operand' in p:
                require(row['operand']==p['operand'],"causal JVM branch operand drift "+s['name']+"@"+str(p['offset']))
            if 'contains' in p:
                require(p['contains'] in row['symbol'],"causal JVM typed-symbol drift "+s['name']+"@"+str(p['offset']))
            pivots+=1
    require(pivots==126,"expected 126 independent controller/sync/persistence JVM anchors")
    return pivots

def adversarial(report,manifest,raw):
    baseline=check(report,manifest,raw)
    entity=report['entity_native']['targets'][OWNER]
    tests=[('<init>',8,'opcode'),('<clinit>',13,'opcode'),('defineSynchedData',45,'opcode'),
           ('addAdditionalSaveData',7,'operand'),('addAdditionalSaveData',25,'opcode'),
           ('readAdditionalSaveData',7,'operand'),('readAdditionalSaveData',35,'opcode'),
           ('getController',7,'operand'),('getController',31,'opcode'),
           ('getControllerUUID',14,'opcode'),('setControllerUUID',8,'opcode'),
           ('getItemStack',7,'opcode'),('setItemStack',8,'opcode'),('getTarget',19,'operand'),
           ('tick',213,'operand'),('tick',490,'opcode')]
    for name,offset,variant in tests:
        forged=copy.deepcopy(report);seal=copy.deepcopy(manifest)
        body=next(x for x in forged['entity_native']['targets'][OWNER]['methods']
                  if x['declaration']['name']==name)
        instruction=next(x for x in body['instructions'] if x['offset']==offset)
        if variant=='opcode':
            require(instruction['opcode']!='nop',"invalid test")
            instruction['opcode']='nop'
        else:
            require(instruction['operand']!='',"invalid branch test")
            instruction['operand']='99999'
        new_sha=canonical_sha(body['instructions'])
        body['instruction_sha256']=new_sha
        next(x for x in seal['methods'] if x['name']==name)['instruction_sha256']=new_sha
        new_raw=json.dumps(forged,ensure_ascii=False,sort_keys=True).encode('utf8')
        seal['evidence']['report_sha256']=sha(new_raw)
        seal['evidence']['report_bytes']=len(new_raw)
        try:
            check(forged,seal,new_raw,test_reseal=True)
        except ValueError as exc:
            require('causal JVM' in str(exc),"adversarial test failed for wrong reason: "+repr(exc))
        else:
            raise AssertionError(f'causal mutation accepted {name}@{offset}')
        print('PASS_FORGED_JVM_REJECTED',name,offset,variant)
    print('PASS: original',baseline,'JVM anchors and',len(tests),'resealed causal forgeries rejected')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--adversarial',action='store_true')
    args=parser.parse_args()
    raw,r=read(args.report,2_100_000)
    _,m=read(args.manifest,80_000)
    n=check(r,m,raw)
    print('PASS: exact publisher and entity identity; 17 fields, 24 class methods,',len(m['methods']),'methods,',n,'JVM pivots')
    print('PASS: NBT stack/UUID guards, server/client controller ID, SynchedEntityData initialization and tick callsites')
    if args.adversarial:adversarial(r,m,raw)
    print('NO_MUTATION NOT_CERTIFIED NOT_TESTED')
