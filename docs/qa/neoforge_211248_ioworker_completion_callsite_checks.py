#!/usr/bin/env python3
"""Fail-closed checks for exact NeoForge 21.1.248 IO worker completion callsites."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

SCOPE='NEOFORGE_211248_IOWORKER_COMPLETION_CALLSITE_CENSUS_DISTRIBUTED_ONLY'
GOLDEN_SHA='54411e230dbf04fe72faedae3b96e513524739a4592d1c56646d48e797cc1725'
STATES={
 'shutdown_execution':'NOT_TESTED','worker_completion_at_server_stop':'NOT_VERIFIED',
 'modlauncher_classes':'NOT_OBSERVED','real_disk_durability':'NOT_TESTED',
 'modpack_physical_qa':'NOT_TESTED','static_contract':'NOT_CERTIFIED',
 'mutating_hook':'NOT_VERIFIED','mutation':'NO_MUTATION',
 'provider_universe_closed':False,'semantic_magic_roots_delta':0}
EXPECTED={
 'net/minecraft/server/level/ServerLevel':('save','(Lnet/minecraft/util/ProgressListener;ZZ)V',94,1324),
 'net/minecraft/util/worldupdate/WorldUpgrader':('work','()V',74,213)}
def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        assert k not in out,('duplicate JSON key',k)
        out[k]=v
    return out
def load(path,limit):
    raw=Path(path).read_bytes()
    assert 0<len(raw)<=limit,'JSON size bound exceeded'
    return raw,json.loads(raw,object_pairs_hook=unique_pairs)
def canonical_sha(obj):
    return hashlib.sha256((json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
def pivot(m,off,opcode,symbol='',operand=None):
    rows=[x for x in m['instructions'] if x['offset']==off]
    assert len(rows)==1,('JVM offset missing',m['declaration']['name'],off)
    x=rows[0]
    assert x['opcode']==opcode,('JVM opcode drift',m['declaration']['name'],off,x['opcode'])
    assert symbol in x['symbol'],('JVM symbol drift',m['declaration']['name'],off)
    if operand is not None:
        assert x['operand']==operand,('JVM operand drift',m['declaration']['name'],off)
    return x
def check(report,manifest):
    raw,r=load(report,420000);_,w=load(manifest,16000)
    assert w['evidence']['run_id']==45062154362
    assert w['evidence']['artifact_id']==14770385280
    assert w['evidence']['report_bytes']==len(raw)
    assert w['evidence']['report_sha256']==hashlib.sha256(raw).hexdigest()
    # Manifest SHA binds the report; negative fixtures deliberately re-seal altered reports.
    assert r['schema_version']==w['schema_version']==1
    assert r['scope']==w['scope']==SCOPE
    assert r['target']==w['target']=={'owner':'net/neoforged/neoforge/common/IOUtilities','name':'waitUntilIOWorkerComplete','descriptor':'()V'}
    assert r['distribution']==w['distribution']
    assert r['distribution']['neoforge_version']=='21.1.248'
    assert r['distribution']['neoforge_server_sha256']=='1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359'
    assert r['distribution']['minecraft_srg_sha256']=='26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71'
    assert r['distribution']['installer_sha256']=='68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c'
    assert r['conclusion_boundary']==('direct invocations and separate method-handle candidates in three official distributed JARs; no exhaustive modloader/third-party classpath claim')
    assert w['states']==STATES
    for k,v in STATES.items():
        assert r[k]==v,('state drift',k)
    assert len(r['archives'])==len(w['archives'])==3
    assert [x['source_archive'] for x in r['archives']]==['NEOFORGE_OVERLAY','INSTALLED_MINECRAFT_SRG','NEOFORGE_UNIVERSAL']
    seen=[]
    for n,(a,s) in enumerate(zip(r['archives'],w['archives'])):
        for k in ('source_archive','jar_sha256','jar_size_bytes','class_entries_scanned','class_roster_sha256','candidates','method_handles_not_direct_calls'):
            assert a[k]==s[k],('archive census drift',a['source_archive'],k)
        assert a['method_handles_not_direct_calls']==[]
        assert a['class_entries_scanned']==[1603,6148,1492][n]
        assert a['jar_size_bytes']==[5675624,14246609,3551268][n]
        assert len(a['direct_invoke_sites'])==len(s['direct_invoke_sites'])==[2,0,0][n]
        assert len(a['candidates'])==[2,0,0][n]
        if n:
            continue
        assert [x['owner'] for x in a['candidates']]==list(EXPECTED)
        assert [x['owner'] for x in a['direct_invoke_sites']]==list(EXPECTED)
        for call,sw in zip(a['direct_invoke_sites'],s['direct_invoke_sites']):
            owner=call['owner'];assert sw['owner']==owner
            name,desc,off,cp=EXPECTED[owner]
            method=call['method'];decl=method['declaration']
            assert (decl['name'],decl['descriptor'])==(name,desc)
            assert call['source_archive']=='NEOFORGE_OVERLAY'
            assert call['class_sha256']==sw['class_sha256']==next(x['class_sha256'] for x in a['candidates'] if x['owner']==owner)
            assert decl['code_sha256']==sw['code_sha256']
            assert method['instruction_sha256']==sw['instruction_sha256']==canonical_sha(method['instructions'])
            assert method['instruction_count']==sw['instruction_count']==len(method['instructions'])
            assert call['callsites']==sw['callsites']==[{'offset':off,'opcode':'invokestatic','cp_index':cp,'symbol':'Method net/neoforged/neoforge/common/IOUtilities.waitUntilIOWorkerComplete:()V'}]
            assert not decl['exception_handlers']
            pivot(method,off,'invokestatic','waitUntilIOWorkerComplete:',f'#{cp}')
            seen.append(owner)
            if owner.endswith('ServerLevel'):
                pivot(method,7,'ifne','','97')
                pivot(method,27,'invokevirtual','saveLevelData:')
                pivot(method,49,'invokevirtual','ServerChunkCache.save:')
                pivot(method,73,'getstatic','NeoForge.EVENT_BUS:')
                pivot(method,84,'invokeinterface','IEventBus.post:')
                pivot(method,90,'iload_2')
                pivot(method,91,'ifeq','','97')
                pivot(method,97,'return')
            else:
                pivot(method,71,'invokevirtual','DimensionDataStorage.save:')
                pivot(method,74,'invokestatic','waitUntilIOWorkerComplete:')
                pivot(method,103,'putfield','finished:Z')
    assert len(seen)==2
    print('PASS: exact 9243-class IO-worker completion callsites and JVM branch pivots')
    print('REPORT_SHA256',hashlib.sha256(raw).hexdigest())
    print('NO_MUTATION NOT_CERTIFIED NOT_TESTED NOT_MODLAUNCHER')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    a=p.parse_args();check(a.report,a.manifest)
