#!/usr/bin/env python3
"""SHA-exact, read-only JVM audit of Galena Gauntlet mining and block effects.

Pins the Alex's Caves Continued 1.0.10 publisher discovery report, including
server-only destruction, progress arithmetic, a ShulkerBox split and downstream
side effects. This NEVER asserts that Level.destroyBlock guarantees permission,
actual drops, experience, world safety, enchantment application or a valid perk.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

SOURCE_SHA = 'c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9'
PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
CLASS_SHA = 'a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071'
OWNER = 'com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity'
SCOPE = 'ALEXSCAVES_1010_GALENA_GAUNTLET_MINING_BLOCK_WORLD_EFFECT_STATIC_ONLY'
SOURCE_SCOPE = 'GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED'
STATES = {
    'static_contract': 'NOT_CERTIFIED', 'mutating_hook': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'mutation': 'NO_MUTATION',
    'provider_universe_closed': False, 'installed_dump_parity': 'NOT_VERIFIED',
    'perk_certification': 'NOT_CERTIFIED', 'semantic_magic_roots_delta': 0,
}
LIMITS = [
    'Level.destroyBlock success vs external protection hooks not audited',
    'Block.playerDestroy may execute despite local destroyBlock failure',
    'ShulkerBox branch awards statistics regardless of local destroyBlock return',
    'no real server world permission/claim tests performed',
    'no actual item loss/XP or event acceptance established',
]
# Independently pinned CFG/control-flow pivots; manifest has all 222 typed anchors.
GUARDS = {
    37: ('ifne', '124', ''), 522: ('ifne', '529', ''),
    544: ('ifeq', '1416', ''), 659: ('invokestatic', '', 'getHitResultOnViewVector'),
    669: ('ifeq', '802', ''), 867: ('ifeq', '928', ''),
    893: ('ifge', '903', ''), 918: ('ifne', '928', ''),
    930: ('ifnull', '1413', ''), 949: ('ifne', '987', ''),
    973: ('invokevirtual', '', 'Level.destroyBlockProgress'),
    984: ('putfield', '', 'destroyBlockProgress'),
    1013: ('invokevirtual', '', 'BlockState.getDestroySpeed'),
    1025: ('invokevirtual', '', 'getDigSpeed'),
    1034: ('ifle', '1413', ''), 1118: ('fdiv', '', ''),
    1124: ('bipush', '8', ''), 1129: ('bipush', '10', ''),
    1132: ('fdiv', '', ''), 1143: ('putfield', '', 'destroyBlockProgress'),
    1168: ('invokevirtual', '', 'destroyBlockProgress'),
    1177: ('iflt', '1413', ''), 1184: ('invokevirtual', '', 'Level.isClientSide'),
    1187: ('ifne', '1413', ''), 1192: ('invokevirtual', '', 'damageItem'),
    1213: ('invokevirtual', '', 'ItemStack.mineBlock'),
    1221: ('invokestatic', '', 'ACCompat.enchantLevel'),
    1231: ('invokestatic', '', 'ACCompat.enchantLevel'),
    1257: ('invokevirtual', '', 'BlockState.getExpDrop'),
    1269: ('invokestatic', '', 'EventHooks.onPlayerDestroyItem'),
    1277: ('instanceof', '', 'ShulkerBoxBlock'),
    1280: ('ifeq', '1322', ''),
    1290: ('invokevirtual', '', 'Level.destroyBlock'),
    1293: ('istore', '20', ''),
    1308: ('invokevirtual', '', 'Player.awardStat'),
    1316: ('invokevirtual', '', 'Player.causeFoodExhaustion'),
    1319: ('goto', '1363', ''),
    1329: ('invokevirtual', '', 'Level.destroyBlock'),
    1332: ('istore', '20', ''),
    1360: ('invokevirtual', '', 'Block.playerDestroy'),
    1363: ('iload', '20', ''), 1365: ('ifeq', '1408', ''),
    1368: ('iload', '19', ''), 1370: ('ifle', '1408', ''),
    1381: ('instanceof', '', 'ServerLevel'), 1384: ('ifeq', '1408', ''),
    1405: ('invokevirtual', '', 'Block.popExperience'),
    1410: ('putfield', '', 'destroyBlockProgress'),
    1462: ('invokevirtual', '', 'destroyBlockProgress'),
}

def require(ok: bool, label: str) -> None:
    if not ok:
        raise ValueError(label)

def reject_duplicates(items):
    out = {}
    for k,v in items:
        require(k not in out, 'duplicate JSON key '+k)
        out[k] = v
    return out

def read(path: Path, max_bytes: int):
    raw = path.read_bytes()
    require(0 < len(raw) <= max_bytes, 'bounded input violated')
    return raw,json.loads(raw, object_pairs_hook=reject_duplicates)

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canonical_sha(rows) -> str:
    return sha((json.dumps(rows, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode('utf-8'))

def method_map(report):
    targets = report['entity_native']['targets']
    require(set(targets)=={OWNER}, 'unexpected native class targets')
    methods = targets[OWNER]['methods']
    mapped = {(m['declaration']['name'],m['declaration']['descriptor']):m for m in methods}
    require(len(mapped)==len(methods)==24,'ambiguous method roster')
    return mapped

def check(report,manifest,raw,*,resealed=False):
    require(report['schema_version']==manifest['schema_version']==1,'schema drift')
    require(report['scope']==SOURCE_SCOPE and manifest['scope']==SCOPE,'scope drift')
    evidence=manifest['evidence']
    require(evidence['report_sha256']==sha(raw) and evidence['report_bytes']==len(raw),'report evidence drift')
    require(resealed or (sha(raw)==SOURCE_SHA and len(raw)==1780492),'publisher discovery report differs')
    require(evidence['source_workflow_run_id']==45071358036 and evidence['source_artifact_id']==14773961125,
            'provenance run/artifact drift')
    p=report['artifact']
    require(manifest['publisher']==p and p['sha256']==PUBLISHER_SHA and
            p['size_bytes']==75279314 and p['version']=='1.0.10' and
            p['installed_dump_parity']=='NOT_VERIFIED','publisher identity drift')
    require(report['mutating_hook']=='NOT_VERIFIED' and report['physical_qa']=='NOT_TESTED' and
            report['mutation']=='NO_MUTATION' and report['provider_universe_closed'] is False and
            report['semantic_magic_roots_certified_delta']==0,'source safety drift')
    require(manifest['states']==STATES and manifest['known_limits']==LIMITS,'status or limitation drift')
    entity=report['entity_native']['targets'][OWNER]; ident=manifest['class']
    require(ident=={'owner':OWNER,'sha256':CLASS_SHA,'methods':24,'fields':17},'class identity manifest drift')
    require(entity['class_sha256']==CLASS_SHA and len(entity['fields'])==17 and
            report['entity_native']['class_entries_scanned']==1555,'publisher class identity drift')
    methods=method_map(report)
    spec=manifest['tick']
    require(spec['descriptor']=='()V','tick descriptor changed')
    tick=methods[('tick','()V')]; body=tick['instructions']
    require(spec['code_sha256']==tick['declaration']['code_sha256']==
            'eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699',
            'native tick code SHA drift')
    require(spec['instruction_sha256']==tick['instruction_sha256']==canonical_sha(body),
            'native tick instruction SHA drift')
    require(spec['instructions']==tick['instruction_count']==len(body)==744,'tick body length drift')
    actual={x['offset']:x for x in body}
    require(len(actual)==len(body),'duplicate native JVM offsets')
    anchors=spec['pivots']
    offsets=[p['offset'] for p in anchors]
    require(len(anchors)==222 and offsets==sorted(set(offsets)) and set(GUARDS)<=set(offsets),
            '222 anchored offsets missing, duplicated or reordered')
    for p in anchors:
        require(actual.get(p['offset'])==p,'causal JVM anchor drift at '+str(p['offset']))
    for off,(opcode,operand,needle) in GUARDS.items():
        obs=actual[off]
        require(obs['opcode']==opcode and (not operand or obs['operand']==operand) and
                (not needle or needle in obs['symbol']),
                'causal JVM fixed guard drift at '+str(off))
    # Audited callers: direct side effects must remain exactly the observed set.
    symbols=[(x['offset'],x['symbol']) for x in body]
    must={
        'Level.destroyBlock:':(1290,1329),
        'Level.destroyBlockProgress:':(973,1168,1462),
        'ItemStack.mineBlock:':(1213,),
        'Block.playerDestroy:':(1360,),
        'Player.awardStat:':(1308,),
        'Block.popExperience:':(1405,),
        'EventHooks.onPlayerDestroyItem:':(1269,),
    }
    for name,expected in must.items():
        found=tuple(offset for offset,symbol in symbols if name in symbol)
        require(found==expected,'causal JVM callsite roster drift: '+name)
    # A call after a boolean store but before testing it is NOT success-gated locally.
    require(all(x['opcode'] not in ('iload','iload_0','iload_1','iload_2','iload_3') or
                x.get('operand')!='20' for x in body if 1293<x['offset']<1308),
            'Shulker statistics success guard changed')
    require(all(x['opcode']!='iload' or x.get('operand')!='20' for x in body if 1332<x['offset']<1360),
            'ordinary Block.playerDestroy success guard changed')
    # Pin previously audited callees but do not treat this as a new certification.
    callee=manifest['dependency_methods']
    require(len(callee)==2 and {m['name'] for m in callee}=={'getDigSpeed','damageItem'},
            'dependency method roster drift')
    for dep in callee:
        key=(dep['name'],dep['descriptor']); require(key in methods,'missing dependency method')
        m=methods[key]
        require(dep['code_sha256']==m['declaration']['code_sha256'] and
                dep['instruction_sha256']==m['instruction_sha256']==canonical_sha(m['instructions']) and
                dep['instructions']==m['instruction_count']==len(m['instructions']),
                'dependency sha/descriptor drift '+dep['name'])
    return len(anchors)

def adversarial(report,manifest):
    tests=[
        (37,'operand'),(522,'operand'),(544,'operand'),(659,'opcode'),
        (669,'operand'),(867,'operand'),(893,'operand'),(918,'operand'),
        (930,'operand'),(973,'opcode'),(1013,'opcode'),(1025,'opcode'),
        (1034,'operand'),(1118,'opcode'),(1124,'operand'),(1129,'operand'),
        (1143,'opcode'),(1168,'opcode'),(1177,'operand'),(1187,'operand'),
        (1192,'opcode'),(1213,'opcode'),(1257,'opcode'),(1269,'opcode'),
        (1277,'opcode'),(1280,'operand'),(1290,'opcode'),(1308,'opcode'),
        (1329,'opcode'),(1360,'opcode'),(1365,'operand'),(1370,'operand'),
        (1384,'operand'),(1405,'opcode'),(1462,'opcode'),
    ]
    for offset,kind in tests:
        rr=copy.deepcopy(report);mm=copy.deepcopy(manifest)
        t=method_map(rr)[('tick','()V')]
        ins=next(x for x in t['instructions'] if x['offset']==offset)
        if kind=='opcode':
            require(ins['opcode']!='nop','adversarial input invalid')
            ins['opcode']='nop'
        else:
            require(ins['operand'] not in ('','99999'),'adversarial operand invalid')
            ins['operand']='99999'
        # Re-seal the forged report and instruction list to prove causal anchor
        # rejection rather than merely a trivial cryptographic mismatch.
        t['instruction_sha256']=canonical_sha(t['instructions'])
        mm['tick']['instruction_sha256']=t['instruction_sha256']
        forged_raw=json.dumps(rr,ensure_ascii=False,sort_keys=True).encode('utf-8')
        mm['evidence']['report_bytes']=len(forged_raw)
        mm['evidence']['report_sha256']=sha(forged_raw)
        try:
            check(rr,mm,forged_raw,resealed=True)
        except ValueError as exc:
            require('causal JVM' in str(exc),f'negative test rejected for wrong reason {offset}: {exc}')
        else:
            raise AssertionError(f'resealed forged causal JVM step accepted @ {offset}')
    print(f'PASS: {len(tests)} independent resealed adversarial opcode/branch/operand changes rejected')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--adversarial',action='store_true')
    args=parser.parse_args()
    raw,r=read(args.report,2_100_000)
    _,m=read(args.manifest,90_000)
    pinned=check(r,m,raw)
    print(f'PASS: publisher SHA-exact; 744-instruction tick, {pinned} typed JVM anchors, 2 exact callees')
    print('PASS: server-only destruction; Shulker split; no local success guard on stats/playerDestroy; XP guarded')
    if args.adversarial:adversarial(r,m)
    print('NO_MUTATION NOT_CERTIFIED NOT_TESTED')
