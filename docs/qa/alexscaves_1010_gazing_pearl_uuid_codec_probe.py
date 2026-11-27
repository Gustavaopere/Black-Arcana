#!/usr/bin/env python3
"""Read-only exact Alex's Caves Continued 1.0.10 UUID codec discovery.

Publisher JAR SHA checked. Trace ACWorldData UUID save/load typed invocations
into ACCompat UUID helpers and their direct typed consumers. No Java bodies,
NBT files, Minecraft execution, mutation or physical/ModLauncher QA.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble

COMPAT='com/github/alexmodguy/alexscaves/server/misc/ACCompat'
WORLD='com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData'
WORLD_SHA='ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5'
NAMES={'putUUID','getUUID'}
MAX_CLASS_BYTES=2_000_000
MAX_CLASSES=2000
MAX_CALLERS=150
MAX_INSNS=6500


def signed_refs(reader, target, names):
    refs={}
    for i,e in enumerate(reader.pool):
        if e is None or e[0] not in (10,11):
            continue
        _,owner,name_type=reader.resolve(i)
        _,name,desc=name_type
        if owner==target and name in names:
            refs[i]={'owner':owner,'name':name,'descriptor':desc,
                     'cp_index':i,'kind':'Methodref' if e[0]==10 else 'InterfaceMethodref'}
    return refs


def method_calls(reader,body,refs):
    sites=[]
    for offset,(opcode,operand,_symbol) in sorted(body.items()):
        if not opcode.startswith('invoke') or opcode=='invokedynamic':
            continue
        tok=operand.split()[0].removeprefix('#') if operand.split() else ''
        if tok.isdecimal() and int(tok) in refs:
            sites.append({'offset':offset,'opcode':opcode,**refs[int(tok)]})
    require(len(sites)<=80,'bounded callsite budget')
    return sites


def all_invokes(reader,body):
    refs={}
    for i,e in enumerate(reader.pool):
        if e is None or e[0] not in (10,11):
            continue
        _,owner,pair=reader.resolve(i)
        _,name,desc=pair
        refs[i]={'owner':owner,'name':name,'descriptor':desc,
                 'cp_index':i,'kind':'Methodref' if e[0]==10 else 'InterfaceMethodref'}
    return method_calls(reader,body,refs)


def count_branches(body):
    return {'conditional':sum(op.startswith('if') for op,_,_ in body.values()),
            'unconditional':sum(op in ('goto','goto_w') for op,_,_ in body.values()),
            'switch':sum(op in ('tableswitch','lookupswitch') for op,_,_ in body.values()),
            'returns':sum(op.endswith('return') for op,_,_ in body.values())}


def audit(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as archive:
        files=archive.namelist()
        require(len(files)==len(set(files)),'duplicate publisher ZIP members')
        class_files=sorted(p for p in files if p.endswith('.class'))
        require(len(class_files)==1555 and len(class_files)<=MAX_CLASSES,
                'publisher class inventory changed')
        compat_bytes=archive.read(COMPAT+'.class')
        world_bytes=archive.read(WORLD+'.class')
        require(digest(world_bytes)==WORLD_SHA and
                64<len(compat_bytes)<MAX_CLASS_BYTES,'publisher identity drift')
        rd=ClassReader(compat_bytes)
        rw=ClassReader(world_bytes)
        require(rd.name==COMPAT and rw.name==WORLD and
                rd.major==rw.major==65,'Java 21 class identities changed')
        uuid_decl=[m for m in rd.methods if m['name'] in NAMES]
        require(len(uuid_decl)==2 and {m['name'] for m in uuid_decl}==NAMES,
                'expected exactly two declared ACCompat UUID wrappers')
        wrapper_bodies=disassemble(jar,javap,COMPAT)
        wrappers=[]
        for decl in sorted(uuid_decl,key=lambda m:m['name']):
            key=(decl['name'],decl['descriptor'])
            require(key in wrapper_bodies and 'code_sha256' in decl,
                    'UUID wrapper has no Code')
            body=wrapper_bodies[key]
            require(0<len(body)<=MAX_INSNS,'unbounded UUID wrapper')
            wrappers.append({'name':key[0],'descriptor':key[1],
                             'code_sha256':decl['code_sha256'],
                             'class_sha256':digest(compat_bytes),
                             'instructions':len(body),
                             'branch_shape':count_branches(body),
                             'direct_invocations':all_invokes(rd,body),
                             'returns_boolean_or_uuid':key[1].split(')')[-1]})
        refs={}
        for name in class_files:
            raw=archive.read(name)
            require(64<len(raw)<MAX_CLASS_BYTES and raw[:4]==b'\xca\xfe\xba\xbe',
                    'malformed bounded JAR member')
            cr=ClassReader(raw)
            require(cr.name+'.class'==name and cr.major==65,'class path identity mismatch')
            matches=signed_refs(cr,COMPAT,NAMES)
            if matches:
                refs[cr.name]={'sha256':digest(raw),'typed_references':matches}
        require(WORLD in refs and len(refs)<=MAX_CALLERS,
                'no ACWorldData UUID dependency or excessive callers')
        consumer_roster=[]
        for owner,entry in sorted(refs.items()):
            reader=ClassReader(archive.read(owner+'.class'))
            members=disassemble(jar,javap,owner)
            callers=[]
            for (name,desc),body in sorted(members.items()):
                sites=method_calls(reader,body,entry['typed_references'])
                if sites:
                    decl=[m for m in reader.methods
                          if m['name']==name and m['descriptor']==desc]
                    require(len(decl)==1 and 'code_sha256' in decl[0],
                            'declared consumer missing JVM Code')
                    callers.append({'method':name,'descriptor':desc,
                                    'code_sha256':decl[0]['code_sha256'],
                                    'callsite_count':len(sites),'sites':sites})
            consumer_roster.append({'owner':owner,'sha256':entry['sha256'],
                                    'callers':callers})
        world=next(x for x in consumer_roster if x['owner']==WORLD)
        require(any(c['method']=='acSave' and any(s['name']=='putUUID' and
                    s['offset']==78 for s in c['sites']) for c in world['callers']),
                'known exact DeepOneReputations save site changed')
        require(any(c['method']=='load' and any(s['name']=='getUUID'
                    for s in c['sites']) for c in world['callers']),
                'DeepOneReputations restore UUID read no longer linked')
    return {'schema':1,'scope':'GAZING_PEARL_1010_ACCOMPAT_UUID_CODEC_DISCOVERY_ONLY',
            'artifact':{'publisher_filename':'alexscaves-1.0.10-neoforge+1.21.1.jar',
                        'publisher_sha256':digest(jar.read_bytes()),
                        'publisher_bytes':jar.stat().st_size,
                        'physical_install_copy_verified':False},
            'compat':{'owner':COMPAT,'sha256':digest(compat_bytes),
                      'declared_methods':len(rd.methods),'uuid_wrappers':wrappers},
            'world':{'owner':WORLD,'sha256':digest(world_bytes),
                     'caller_count':len(world['callers'])},
            'direct_consumer_census':consumer_roster,
            'limits':{'installed_copy':'NOT_VERIFIED','engine_uuid_payload_tag_type':'NOT_VERIFIED',
                      'modlauncher_runtime':'NOT_OBSERVED','actual_save_restart':'NOT_TESTED',
                      'static_contract':'NOT_CERTIFIED','mutating_hook':'NOT_VERIFIED',
                      'physical_qa':'NOT_TESTED','mutation':'NO_MUTATION',
                      'provider_universe_closed':False,'semantic_magic_roots_delta':0}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--javap',default='javap')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    require(args.output.suffix=='.json' and not args.output.exists(),'write-once report')
    result=audit(args.jar,args.javap)
    data=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    require(0<len(data)<180_000,'report size budget')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(data)
    print('REPORT_SHA256',hashlib.sha256(data).hexdigest(),'BYTES',len(data))
    print('COMPAT_SHA256',result['compat']['sha256'])
    for row in result['compat']['uuid_wrappers']:
        print('UUID_WRAPPER',row['name'],row['descriptor'],row['code_sha256'],
              'INSTRUCTIONS',row['instructions'])
        for c in row['direct_invocations']:
            print('WRAPPER_CALL',row['name'],c['offset'],c['owner'],c['name'],c['descriptor'])
    for row in result['direct_consumer_census']:
        print('CONSUMER',row['owner'],'SHA256',row['sha256'])
        for method in row['callers']:
            for site in method['sites']:
                print('CALLSITE',row['owner'],method['method'],site['offset'],site['name'])
    print('NO_MUTATION UUID_CODEC_DISCOVERY_ONLY NO_PHYSICAL_QA')

if __name__=='__main__':main()
