#!/usr/bin/env python3
"""Exact-distribution, fail-closed checks for bounded NBT Tag.write JVM discovery.

The checks enforce SHA-pinned provenance and causal JVM offsets, not world
persistence, a live transformed runtime, or an authorized mutation boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE = "NEOFORGE_211248_NBT_TAG_WRITERS_DISTRIBUTED_DISCOVERY_ONLY"
GOLDEN_REPORT_SHA = "c80b30aaac9a243f83af59c581800bb565653adc7fc7d1ada4a6b14546667351"
GOLDEN_REPORT_BYTES = 71642
CLASS_SHA = {
    "net/minecraft/nbt/Tag":"2e5fb1c98da5019e49f1b6805daf7564f980d83cc1ae0bfc3d8723f336a546ca",
    "net/minecraft/nbt/CompoundTag":"93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6",
    "net/minecraft/nbt/ListTag":"b9f4d0b453362a71e82e05af6190509694c781e688feee51fe9b6e74f38abb84",
    "net/minecraft/nbt/IntTag":"0245c8d0134ebd88f1b484c90f72c7a3ace51ae858bde385e0436439d3c95077",
    "net/minecraft/nbt/IntArrayTag":"8894d67d9f0e9c27b2df9971c685b7cd3dc0696d1c3b2c295fd180773f222088",
    "net/minecraft/nbt/StringTag":"4c177a1d925f5645ece0d34ab51a438ec247b02f9ddc805945db49ea8d5be110",
}
DISTRIBUTION = {
    "minecraft_version":"1.21.1",
    "neoforge_version":"21.1.248",
    "installer_sha256":"68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c",
    "neoforge_server_sha256":"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",
    "neoforge_server_bytes":5675624,
    "minecraft_srg_sha256":"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",
    "minecraft_srg_bytes":14246609,
    "modlauncher_loaded_bytes":"NOT_OBSERVED",
}
STATES = {
    "static_contract":"NOT_CERTIFIED", "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED", "mutation":"NO_MUTATION",
    "provider_universe_closed":False, "semantic_magic_roots_delta":0,
}
LIMITS = {
    "all_tag_implementations_audited":False,
    "live_modlauncher":"NOT_OBSERVED",
    "installed_modpack_parity":"NOT_VERIFIED",
    "filesystem_write_or_restart":"NOT_TESTED",
    "actual_nbt_reload":"NOT_TESTED",
    "shutdown_wait_callsite":"NOT_VERIFIED",
}
WRITE="(Ljava/io/DataOutput;)V"
NAMED="(Ljava/lang/String;Lnet/minecraft/nbt/Tag;Ljava/io/DataOutput;)V"

def unique_object(pairs):
    data = {}
    for k,v in pairs:
        assert k not in data, ("duplicate JSON key",k)
        data[k] = v
    return data

def load(path,max_bytes):
    raw = Path(path).read_bytes()
    assert 0 < len(raw) <= max_bytes, "JSON evidence exceeds bound"
    return raw, json.loads(raw, object_pairs_hook=unique_object)

def canonical_sha(obj):
    return hashlib.sha256((json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)+"\n").encode()).hexdigest()

def get_method(row,name,desc):
    methods=[m for m in row['selected_methods'] if m['declaration']['name']==name and m['declaration']['descriptor']==desc]
    assert len(methods)==1,("ambiguous JVM method",row['owner'],name,desc)
    return methods[0]

def pivot(row,name,desc,offset,opcode,symbol="",operand=None):
    m=get_method(row,name,desc)
    matches=[i for i in m['instructions'] if i['offset']==offset]
    assert len(matches)==1,("JVM offset missing",row['owner'],name,offset)
    i=matches[0]
    assert i['opcode']==opcode,("JVM opcode drift",row['owner'],name,offset)
    assert symbol in i['symbol'],("JVM symbol drift",row['owner'],name,offset)
    if operand is not None:
        assert i['operand']==operand,("JVM operand drift",row['owner'],name,offset)
    return i

def check(report_path, seal_path):
    raw,r=load(report_path,750_000)
    _,seal=load(seal_path,25_000)
    assert r['schema_version']==seal['schema_version']==1
    assert r['scope']==seal['scope']==SCOPE
    assert seal['evidence']['run_id']==45058410553
    assert seal['evidence']['artifact_id']==14768342779
    # Negative tests may re-seal forged evidence to prove opcode checks run.
    assert len(raw)==seal['evidence']['report_bytes']
    assert hashlib.sha256(raw).hexdigest()==seal['evidence']['report_sha256']
    assert seal['evidence']['report_bytes']==GOLDEN_REPORT_BYTES or seal['evidence']['report_sha256']!=GOLDEN_REPORT_SHA
    assert r['distribution']==seal['distribution']==DISTRIBUTION
    assert seal['states']==STATES
    for k,v in STATES.items():
        assert r[k]==v,("state drift",k)
    assert seal['limits']==LIMITS
    for k,v in LIMITS.items():
        assert r[k]==v,("limit drift",k)
    assert r['context']==(
        "NbtIo.writeUnnamedTag -> Tag.write virtual dispatch; this probe audits a bounded set of exact concrete NBT writers and the Tag interface")
    assert len(r['classes'])==len(seal['classes'])==len(CLASS_SHA)
    assert [x['owner'] for x in r['classes']]==list(CLASS_SHA)
    by_owner={}
    for row,exp in zip(r['classes'],seal['classes']):
        owner=row['owner']
        assert exp['owner']==owner
        assert row['class_major']==exp['class_major']==65
        assert row['class_sha256']==exp['class_sha256']==CLASS_SHA[owner]
        assert row['source_archive']==exp['source_archive']
        assert row['parent']==exp['parent']
        assert row['declared_method_count']==exp['declared_method_count']==len(row['roster'])
        assert canonical_sha(row['roster'])==exp['roster_sha256']
        assert row['fields']==exp['fields']
        assert row['non_executable_selected']==exp['non_executable_selected']
        assert len(row['selected_methods'])==len(exp['methods'])
        for m,w in zip(row['selected_methods'],exp['methods']):
            d=m['declaration']
            assert (d['name'],d['descriptor'])==(w['name'],w['descriptor'])
            assert d['code_sha256']==w['code_sha256']
            assert d.get('exception_handlers',[])==w['exception_handlers']==[]
            assert m['instruction_sha256']==w['instruction_sha256']==canonical_sha(m['instructions'])
            assert m['instruction_count']==w['instruction_count']==len(m['instructions'])
            offsets=[x['offset'] for x in m['instructions']]
            assert offsets==sorted(set(offsets))
        by_owner[owner.split('/')[-1]]=row
    tag=by_owner['Tag']
    assert tag['selected_methods']==[]
    assert tag['non_executable_selected']==[
        {'access':1025,'descriptor':'()B','name':'getId'},
        {'access':1025,'descriptor':WRITE,'name':'write'},
    ]
    c=by_owner['CompoundTag']; l=by_owner['ListTag']; i=by_owner['IntTag']; a=by_owner['IntArrayTag']; s=by_owner['StringTag']
    # Core compound semantics: each key/value pair dispatched, then END (0).
    pivot(c,'write',WRITE,4,'invokeinterface','Map.keySet:')
    pivot(c,'write',WRITE,16,'invokeinterface','Iterator.hasNext:')
    pivot(c,'write',WRITE,53,'invokestatic','writeNamedTag:')
    pivot(c,'write',WRITE,60,'iconst_0')
    pivot(c,'write',WRITE,61,'invokeinterface','DataOutput.writeByte:')
    # Write entry type, optional UTF key, then virtual Tag.write value.
    pivot(c,'writeNamedTag',NAMED,2,'invokeinterface','Tag.getId:')
    pivot(c,'writeNamedTag',NAMED,7,'invokeinterface','DataOutput.writeByte:')
    pivot(c,'writeNamedTag',NAMED,18,'ifeq','', '35')
    pivot(c,'writeNamedTag',NAMED,23,'invokeinterface','DataOutput.writeUTF:')
    pivot(c,'writeNamedTag',NAMED,30,'invokeinterface','Tag.write:')
    # List type from first element or END for empty, size, each virtual value.
    pivot(l,'write',WRITE,9,'ifeq','', '20')
    pivot(l,'write',WRITE,14,'putfield','type:B')
    pivot(l,'write',WRITE,34,'invokeinterface','Tag.getId:')
    pivot(l,'write',WRITE,39,'putfield','type:B')
    pivot(l,'write',WRITE,47,'invokeinterface','DataOutput.writeByte:')
    pivot(l,'write',WRITE,62,'invokeinterface','DataOutput.writeInt:')
    pivot(l,'write',WRITE,98,'invokeinterface','Tag.write:')
    # Persistent 32-bit values, UUID-array representation and UTF payloads.
    pivot(i,'write',WRITE,5,'invokeinterface','DataOutput.writeInt:')
    pivot(a,'write',WRITE,5,'arraylength')
    pivot(a,'write',WRITE,6,'invokeinterface','DataOutput.writeInt:')
    pivot(a,'write',WRITE,37,'invokeinterface','DataOutput.writeInt:')
    pivot(s,'write',WRITE,5,'invokeinterface','DataOutput.writeUTF:')
    for name in ('CompoundTag','ListTag','IntTag','IntArrayTag','StringTag'):
        assert get_method(by_owner[name],'write',WRITE)['instruction_count']>0
    print('PASS: exact NeoForge 21.1.248 CompoundTag/ListTag/int/UTF serializer JVM pivots')
    print('REPORT_SHA256',hashlib.sha256(raw).hexdigest())
    print('NO_MUTATION NOT_CERTIFIED NOT_TESTED NOT_MODLAUNCHER')

if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--report',type=Path,required=True)
    cli.add_argument('--manifest',type=Path,required=True)
    a=cli.parse_args()
    check(a.report,a.manifest)
