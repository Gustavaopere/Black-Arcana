#!/usr/bin/env python3
"""Fail-closed exact publisher JVM verifier of Galena return/drop lifecycle.

Checks eight caller methods and the ACCompat.spawnAtLocation direct helper, typed
branch/side-effect order, SHA pinning and adversarial report forgeries. NEVER
certifies world item spawns, item restitution, inventory transactions, engine
acceptance, mutating hooks or physical gameplay.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

OWNER='com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity'
ITEM='com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem'
HELPER='com/github/alexmodguy/alexscaves/server/misc/ACCompat'
REPORT_SHA='8cff541420b4bbca8820aa419ed73cf01478c4a881c7f6afa12e256f6a9ae916'
REPORT_SIZE=188299
PUBLISHER_SHA='36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
SOURCE_SHA='c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9'
HELPER_CLASS_SHA='333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b'
HELPER_CODE_SHA='505d89864837abd20cf36829273586fcff20e07d7cbe828010d73481e2311ed6'
EXPECTED_NAMES={
 'entity': {'tick','plopItem','getController','isOwnerWearingGauntlet',
            'getReturnProgress','directMovementTowards','getItemStack'},
 'item': {'onUseTick'},
 'helper': {'spawnAtLocation'},
}
STATES={'static_contract':'NOT_CERTIFIED','mutating_hook':'NOT_VERIFIED',
        'physical_qa':'NOT_TESTED','perk_certification':'NOT_CERTIFIED',
        'mutation':'NO_MUTATION','installed_dump_parity':'NOT_VERIFIED',
        'provider_universe_closed':False,'semantic_magic_roots_delta':0}
# Static opcode/branch anchors independent from the mutable manifest or report SHA.
# A verified branch is evidence of local intent, not proof of world acceptance.
GUARDS={
 'entity/tick': {
  37:('ifne','124',''),44:('ifne','65',''),51:('ifeq','73',''),
  62:('ifne','73',''),88:('if_icmpgt','101',''),98:('ifeq','124',''),
  105:('ifeq','117',''),109:('invokevirtual','','plopItem'),
  118:('getstatic','','RemovalReason.DISCARDED'),121:('invokevirtual','','remove:'),
  173:('ifeq','470',''),203:('invokevirtual','','TeletorEntity.setWeaponUUID'),
  474:('ifeq','1554',''),519:('invokevirtual','','isOwnerWearingGauntlet'),
  522:('ifne','529',''),530:('putfield','','comingBack'),
  544:('ifeq','1416',''),549:('putfield','','hadPlayerController'),
  1422:('ifge','1441',''),1431:('ldc_w','','float 0.2f'),
  1435:('invokestatic','','Math.min'),1438:('putfield','','returnProgress'),
  1445:('ifnull','1470',''),1462:('invokevirtual','','destroyBlockProgress'),
  1467:('putfield','','lastSelectedBlock'),
  1489:('ldc2_w','','double 1.4d'),1493:('ifge','1541',''),
  1497:('invokevirtual','','isRemoved'),1500:('ifne','1541',''),
  1507:('ifne','1537',''),1516:('invokevirtual','','Player.addItem'),
  1519:('ifeq','1537',''),1524:('putfield','','spawnedItem'),
  1531:('invokevirtual','','remove:'),1538:('invokevirtual','','plopItem'),
  1551:('invokevirtual','','directMovementTowards'),
  1568:('putfield','','playerUseCooldown'),
  1579:('invokevirtual','','move:'),1590:('invokevirtual','','Vec3.scale:'),
 },
 'entity/plopItem': {
  1:('getfield','','spawnedItem'),4:('ifne','29',''),
  9:('putfield','','spawnedItem'),17:('invokestatic','','ACCompat.spawnAtLocation'),
  22:('ifnull','29',''),26:('invokevirtual','','ItemEntity.setNoPickUpDelay'),
  30:('getstatic','','RemovalReason.DISCARDED'),33:('invokevirtual','','remove:'),
 },
 'entity/isOwnerWearingGauntlet': {
  1:('invokevirtual','','getController'),6:('instanceof','','LivingEntity'),
  9:('ifeq','56',''),18:('invokevirtual','','LivingEntity.getUseItem'),
  32:('invokevirtual','','ItemStack.is:'),35:('ifeq','56',''),
  38:('aload_1','',''),39:('invokevirtual','','LivingEntity.isAlive'),
  42:('ifeq','56',''),46:('getfield','','returnFlag'),49:('ifne','56',''),
  57:('ireturn','',''),
 },
 'entity/getReturnProgress': {
  1:('getfield','','prevReturnProgress'),5:('getfield','','returnProgress'),
  9:('getfield','','prevReturnProgress'),12:('fsub','',''),
  14:('fmul','',''),15:('fadd','',''),16:('freturn','',''),
 },
 'item/onUseTick': {
  186:('iload','7',''),188:('ifne','277',''),
  193:('invokevirtual','','ItemStack.copy'),201:('invokevirtual','','ItemStack.setCount'),
  216:('invokestatic','','ACCompat.createEntity'),
  228:('invokevirtual','','MagneticWeaponEntity.setItemStack'),
  252:('invokevirtual','','MagneticWeaponEntity.setControllerUUID'),
  258:('invokevirtual','','Level.addFreshEntity'),261:('pop','',''),
 },
 'helper/spawnAtLocation': {
  0:('aload_0','',''),1:('aload_1','',''),
  2:('invokevirtual','','Entity.spawnAtLocation'),5:('areturn','',''),
 },
}

def require(ok, reason):
    if not ok: raise ValueError(reason)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def canonical_sha(rows):return sha((json.dumps(rows,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode())

def pairs_no_duplicates(items):
    result={}
    for k,v in items:
        require(k not in result,'duplicate JSON key '+k)
        result[k]=v
    return result

def load(path,max_bytes):
    raw=Path(path).read_bytes()
    require(0<len(raw)<=max_bytes,'bounded file size violated')
    return raw,json.loads(raw,object_pairs_hook=pairs_no_duplicates)

def get_methods(report):
    require(set(report['callers'])=={OWNER,ITEM},'unexpected caller owners')
    methods={}
    for prefix,owner in (('entity',OWNER),('item',ITEM)):
        entries=report['callers'][owner]['methods']
        names=[m['declaration']['name'] for m in entries]
        require(len(set(names))==len(names) and set(names)==EXPECTED_NAMES[prefix],
                'unexpected method roster for '+prefix)
        for m in entries:methods[prefix+'/'+m['declaration']['name']]=m
    methods['helper/spawnAtLocation']=report['helper']['selected']
    require(set(methods)=={k for pre,names in EXPECTED_NAMES.items() for k in (pre+'/'+n for n in names)},
            'missing expected native method')
    return methods

def check(report,manifest,raw,*,resealed=False):
    require(report['schema']=='GALENA_RETURN_DROP_DISCOVERY_V1' and
            report['scope']=='SHA_EXACT_PUBLISHER_JVM_DISCOVERY_NOT_CERTIFIED' and
            manifest['schema']==1 and manifest['scope']=='ALEXSCAVES_1010_GALENA_RETURN_DROP_LIFECYCLE_STATIC_ONLY',
            'discovery schema or scope drift')
    ev=manifest['report']
    require(ev['sha256']==sha(raw) and ev['size_bytes']==len(raw),'report/manfiest digest mismatch')
    require(resealed or (sha(raw)==REPORT_SHA and len(raw)==REPORT_SIZE),'official source report identity drift')
    require(ev['source_caller_sha256']==SOURCE_SHA and ev['initial_workflow_run']==45080911861 and
            ev['initial_artifact_id']==14777325666,'evidence chain drift')
    require(report['caller_report']=={'sha256':SOURCE_SHA,'size_bytes':1780492},
            'underlying Galena source caller report drift')
    art=report['artifact']
    require(manifest['publisher']==art and art['sha256']==PUBLISHER_SHA and
            art['version']=='1.0.10' and art['size_bytes']==75279314 and
            art['installed_dump_parity']=='NOT_VERIFIED','publisher physical identity drift')
    for key,expect in STATES.items():
        if key in report:require(report[key]==expect,'discovery safety drift '+key)
    require(manifest['states']==STATES,'manifest safety drift')
    require(report['helper']['class_sha256']==manifest['classes']['helper']==HELPER_CLASS_SHA and
            report['helper']['methods_declared']==200,'helper class identity drift')
    require(manifest['classes']['entity']==report['callers'][OWNER]['class_sha256'] and
            manifest['classes']['item']==report['callers'][ITEM]['class_sha256'],
            'consumer class identity drift')
    require(manifest['helper_callers']==report['typed_helper_callers'] and
            len(report['typed_helper_callers'])==1,'missing/duplicated helper callsite')
    site=report['typed_helper_callers'][0]
    require(site['caller_owner']==OWNER and site['caller_method']=='plopItem' and
            site['offset']==17 and site['opcode']=='invokestatic' and
            site['callee_name']=='spawnAtLocation', 'helper callsite drift')
    methods=get_methods(report)
    require(set(manifest['methods'])==set(methods),'manifest method roster drift')
    total=0
    for name,m in methods.items():
        spec=manifest['methods'][name]
        require((m['declaration']['name'],m['declaration']['descriptor'])==
                (spec['name'],spec['descriptor']),'selected overload drift '+name)
        require(m['declaration']['code_sha256']==spec['code_sha256'] and
                m['instruction_sha256']==spec['instruction_sha256']==canonical_sha(m['instructions']) and
                m['instruction_count']==spec['instruction_count']==len(m['instructions']),
                'body integrity drift '+name)
        if name=='helper/spawnAtLocation':
            require(m['declaration']['code_sha256']==HELPER_CODE_SHA and
                    m['instruction_count']==4 and m['declaration']['exception_handlers']==[],
                    'helper direct-delegation body identity drift')
        rows={row['offset']:row for row in m['instructions']}
        require(len(rows)==len(m['instructions']),'duplicate native instruction offset '+name)
        pivots=spec['pivots'];offsets=[x['offset'] for x in pivots]
        require(offsets==sorted(set(offsets)) and len(pivots)>0 and
                all(rows.get(x['offset'])==x for x in pivots),
                'CAUSAL_PIVOT: missing, reordered or changed JVM pivot in '+name)
        require(set(GUARDS.get(name,{})).issubset(set(offsets)),
                'CAUSAL_PIVOT: guard missing from manifest '+name)
        for off,(op,operand,token) in GUARDS.get(name,{}).items():
            row=rows[off]
            require(row['opcode']==op and (not operand or row['operand']==operand) and
                    (not token or token in row['symbol']),
                    'CAUSAL_PIVOT: independently pinned JVM guard drift at '+name+':'+str(off))
        total+=len(pivots)
    # Ownership/restoration sequence: do not treat runtime outcomes as proven.
    tick=methods['entity/tick']['instructions']
    require([x['offset'] for x in tick if 'Player.addItem:' in x['symbol']]==[1516] and
            [x['offset'] for x in tick if 'plopItem:' in x['symbol']]==[109,1538],
            'CAUSAL_PIVOT: return callsite cardinality drift')
    plop=methods['entity/plopItem']['instructions']
    require([x['offset'] for x in plop if 'spawnAtLocation:' in x['symbol']]==[17] and
            plop[-1]['opcode']=='return','CAUSAL_PIVOT: fallback terminal-call drift')
    source=methods['item/onUseTick']['instructions']
    require([x['offset'] for x in source if 'Level.addFreshEntity:' in x['symbol']]==[258],
            'CAUSAL_PIVOT: spawn request roster drift')
    return total

def adversarial(report,manifest):
    tests={
      'entity/tick':[(37,'operand'),(44,'operand'),(51,'operand'),(62,'operand'),
        (88,'operand'),(98,'operand'),(105,'operand'),(109,'opcode'),(118,'opcode'),
        (121,'opcode'),(474,'operand'),(519,'opcode'),(522,'operand'),(530,'opcode'),
        (544,'operand'),(549,'opcode'),(1422,'operand'),(1431,'opcode'),(1438,'opcode'),
        (1445,'operand'),(1462,'opcode'),(1489,'opcode'),(1493,'operand'),
        (1497,'opcode'),(1500,'operand'),(1507,'operand'),(1516,'opcode'),
        (1519,'operand'),(1524,'opcode'),(1531,'opcode'),(1538,'opcode'),
        (1551,'opcode')],
      'entity/plopItem':[(1,'opcode'),(4,'operand'),(9,'opcode'),(17,'opcode'),
        (22,'operand'),(26,'opcode'),(30,'opcode'),(33,'opcode')],
      'entity/isOwnerWearingGauntlet':[(1,'opcode'),(6,'opcode'),(35,'operand'),
        (39,'opcode'),(42,'operand'),(49,'operand')],
      'entity/getReturnProgress':[(1,'opcode'),(12,'opcode'),(14,'opcode')],
      'item/onUseTick':[(188,'operand'),(193,'opcode'),(201,'opcode'),(216,'opcode'),
         (228,'opcode'),(252,'opcode'),(258,'opcode'),(261,'opcode')],
      'helper/spawnAtLocation':[(0,'opcode'),(1,'opcode'),(2,'opcode'),(5,'opcode')],
    }
    success=0
    for name,offsets in tests.items():
        for off,kind in offsets:
            rr=copy.deepcopy(report);mm=copy.deepcopy(manifest)
            method=get_methods(rr)[name]
            row=next(x for x in method['instructions'] if x['offset']==off)
            if kind=='opcode':require(row['opcode']!='nop','bad adversarial op');row['opcode']='nop'
            else:require(row['operand']!='99999','bad adversarial operand');row['operand']='99999'
            method['instruction_sha256']=canonical_sha(method['instructions'])
            mm['methods'][name]['instruction_sha256']=method['instruction_sha256']
            raw=(json.dumps(rr,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
            mm['report']['sha256']=sha(raw);mm['report']['size_bytes']=len(raw)
            try:check(rr,mm,raw,resealed=True)
            except ValueError as exc:
                require('CAUSAL_PIVOT:' in str(exc),
                        'forgery detected for wrong reason '+name+':'+str(off)+' '+str(exc))
            else:raise AssertionError('resealed adversarial JVM forgery accepted '+name+':'+str(off))
            success+=1
    print(f'PASS: {success} adversarial re-sealed JVM mutations rejected by causal anchors')
    return success

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',required=True,type=Path)
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--adversarial',action='store_true')
    a=p.parse_args()
    raw,r=load(a.report,300_000);_,m=load(a.manifest,140_000)
    count=check(r,m,raw)
    print('PASS: 9 SHA-exact methods,',count,'pinned JVM pivots; 1 exact helper typed callsite')
    if a.adversarial:adversarial(r,m)
    print('NO_MUTATION NOT_CERTIFIED NOT_TESTED')
