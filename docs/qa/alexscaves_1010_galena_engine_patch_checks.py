#!/usr/bin/env python3
"""Fail-closed NeoForge 21.1.250 official patch-footprint verifier.

No decompiled vanilla source, world mutation, runtime launch, or inference from
absence of a patch to absence of a transformer. Report-only forgeries are tested
against independently committed line/hash/hunk anchors.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re
from pathlib import Path

REPORT_SHA = '7cb488b63c2abafcf17c839661ac7ff05a367fca84c497c174dea5017ded6411'
REPORT_SIZE = 10185
USERDEV_SHA = 'deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372'
PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
HELPER_SHA = 'ca395f3418979d8302363cf9db8d54c620572b16ebdc2ecacee5014fce0add64'
REPORT_SCOPE = 'GALENA_1010_NEOFORGE_211250_NBT_PATCH_FOOTPRINT_ONLY'
SEAL_SCOPE = 'GALENA_1010_NEOFORGE_211250_NBT_PATCH_FOOTPRINT_SEAL_STATIC_ONLY'
PATHS = {
 'ItemStack': 'patches/net/minecraft/world/item/ItemStack.java.patch',
 'CustomData': 'patches/net/minecraft/world/item/component/CustomData.java.patch',
 'CompoundTag': 'patches/net/minecraft/nbt/CompoundTag.java.patch',
}
PATCH_HASHES = {
 'ItemStack': '5e910db862cc11662067e5ffbd2a792197d2eb618ce76f4281ee6fb5998c8c7d',
 'CompoundTag': '6d4eb62dc6dddb7dd58b02fc1dfe5e76e6ca4634c5ae03bed2875a05c69abe02',
}
LIMITS = {'mutation':'NO_MUTATION','mutating_hook':'NOT_VERIFIED',
          'physical_qa':'NOT_TESTED','static_contract':'NOT_CERTIFIED',
          'provider_universe_closed':False,'vanilla_method_body':'NOT_VERIFIED',
          'installed_transformed_game':'NOT_VERIFIED',
          'userdev_patch_absence_implies_no_runtime_modification':False}

def require(ok, why):
 if not ok: raise ValueError(why)

def unique(pairs):
 out={}
 for k,v in pairs:
  require(k not in out,'duplicate JSON key: '+k)
  out[k]=v
 return out

def sha(raw): return hashlib.sha256(raw).hexdigest()

def load(path, cap):
 raw=Path(path).read_bytes()
 require(0<len(raw)<=cap,'invalid file size')
 return raw,json.loads(raw,object_pairs_hook=unique)

def assert_targets(t):
 require(set(t)==set(PATHS),'target roster drift')
 for n,p in t.items():
  require(p['path']==PATHS[n], 'path changed: '+n)
  require(isinstance(p['present'],bool), 'patch presence wrong type: '+n)
  if not p['present']:
   require(n=='CustomData' and p=={'path':PATHS[n],'present':False}, 'unexpected absence')
   continue
  require(n in PATCH_HASHES and p['sha256']==PATCH_HASHES[n], 'patch SHA drift: '+n)
  require(len(p['matches'])<=1200, 'unbounded symbol-hit count: '+n)
  require(p['hunk_count']==len(p['hunk_line_numbers'])>0 and
          p['hunk_line_numbers']==sorted(set(p['hunk_line_numbers'])), 'hunk roster drift')
  require(all(1<=v<=p['total_lines'] for v in p['hunk_line_numbers']), 'invalid hunk line')
  require(len(p['matches'])==sum(p['matched_counts_by_kind'].values()), 'match counter drift')
  require(set(p['matched_counts_by_kind'])=={'ADD','DELETE','CONTEXT'},'unknown diff kinds')
  lines=[x['line'] for x in p['matches']]
  require(lines==sorted(set(lines)), 'duplicate/out-of-order matched lines')
  for x in p['matches']:
   require(1<=x['line']<=p['total_lines'] and x['kind'] in ('ADD','DELETE','CONTEXT') and
           bool(re.fullmatch(r'[a-f0-9]{64}',x['line_sha256'])) and
           isinstance(x['bytes'],int) and x['bytes']>0 and
           x['tokens']==sorted(set(x['tokens'])) and
           all(re.fullmatch(r'[a-z_]+',y) for y in x['tokens']), 'invalid patch line')
  for kind in ('ADD','DELETE','CONTEXT'):
   require(p['matched_counts_by_kind'][kind]==sum(x['kind']==kind for x in p['matches']),
           'counts no longer match classified lines')
 require(t['ItemStack']['hunk_count']==20 and len(t['ItemStack']['matches'])==25 and
         t['ItemStack']['matched_counts_by_kind']=={'ADD':3,'CONTEXT':16,'DELETE':6},
         'ItemStack footprint drift')
 require(t['CompoundTag']['hunk_count']==3 and len(t['CompoundTag']['matches'])==4 and
         t['CompoundTag']['matched_counts_by_kind']=={'ADD':1,'CONTEXT':3,'DELETE':0},
         'CompoundTag footprint drift')
 require(not t['CustomData']['present'], 'CustomData direct patch unexpectedly present')
 require(not any('parse' in x['tokens'] or 'save' in x['tokens']
                 for x in t['ItemStack']['matches']), 'parse/save token footprint changed')

def validate(report,manifest,raw,strict_outer=True):
 require(report.get('schema_version')==manifest.get('schema_version')==1,'schema drift')
 require(report.get('scope')==REPORT_SCOPE and manifest.get('scope')==SEAL_SCOPE,'scope drift')
 evidence=manifest['evidence']
 require(evidence['source_workflow_run_id']==45078806235 and evidence['source_artifact_id']==14776063917 and
         evidence['source_branch_head']=='2ed0a9f6c58900669795d7e65842d80ba6f25968', 'report provenance drift')
 require(evidence['report_bytes']==REPORT_SIZE and evidence['report_sha256']==REPORT_SHA, 'fixed report identity drift')
 if strict_outer:
  require(len(raw)==REPORT_SIZE and sha(raw)==REPORT_SHA,'real report bytes do not match exact CI artifact')
 ref=report['reference']
 require(ref==manifest['expected_reference'] and ref['userdev_sha256']==USERDEV_SHA and
         ref['userdev_size']==3983248 and ref['alexscaves_publisher_sha256']==PUBLISHER_SHA and
         ref['accompat_helper_report_sha256']==HELPER_SHA and ref['neoforge']=='21.1.250' and
         ref['minecraft']=='1.21.1', 'artifact or caller chain changed')
 archive=report['archive']
 require(archive==manifest['expected_archive'] and archive['entry_count']==963 and
         archive['minecraft_patch_count']==753 and
         archive['minecraft_patch_path_roster_sha256']=='22046c708c5774e479f335fcef95a0c526670fbc9dde01fc29281c94102a640f', 'source patch census drift')
 t=report['targets'];assert_targets(t)
 assert_targets(manifest['expected_targets'])
 require(t==manifest['expected_targets'], 'specific patch hit/line/hunk/hash drift')
 limits=report['limitations']
 require(limits==manifest['expected_limits'] and
         all(limits[k]==v for k,v in LIMITS.items()), 'safety ceilings changed')
 conclusions=manifest['conclusions']
 require(conclusions['ItemStack_patch_count']==20 and
         conclusions['ItemStack_exact_add_delete_context_matches']=={'ADD':3,'DELETE':6,'CONTEXT':16} and
         conclusions['ItemStack_parse_or_save_literal_match_count']==0 and
         conclusions['CustomData_patch_present'] is False and
         conclusions['CompoundTag_patch_count']==3 and
         conclusions['installed_dump_parity']=='NOT_VERIFIED' and
         conclusions['semantic_magic_roots_certified_delta']==0 and
         conclusions['world_effect_policy_hook']=='NOT_VERIFIED' and
         all(conclusions[k]==limits[k] for k in ('mutation','static_contract','physical_qa','mutating_hook')),
         'unsafe claim or unsupported promotion')

def adversarial(report,manifest,raw):
 # Re-seal the modified report's *outer* hash by disabling only that outer check.
 # Pinned inner per-line and official patch digests still must reject each forgery.
 forged=[]
 def add(label,change):
  copy_report=copy.deepcopy(report);change(copy_report);forged.append((label,copy_report))
 for i in range(len(report['targets']['ItemStack']['matches'])):
  def mutate(r,index=i):
   row=r['targets']['ItemStack']['matches'][index]
   row['line_sha256']='0'*64 if row['line_sha256']!='0'*64 else '1'*64
  add('ItemStack line-hash '+str(i),mutate)
 for i in range(len(report['targets']['CompoundTag']['matches'])):
  def mutate(r,index=i):
   row=r['targets']['CompoundTag']['matches'][index]
   row['tokens']=['save'] if row['tokens']!=['save'] else ['codec']
  add('CompoundTag symbol '+str(i),mutate)
 add('ItemStack kind',lambda r:r['targets']['ItemStack']['matches'][0].__setitem__('kind','ADD'))
 add('ItemStack hunk',lambda r:r['targets']['ItemStack'].__setitem__('hunk_count',19))
 add('CompoundTag sha',lambda r:r['targets']['CompoundTag'].__setitem__('sha256','0'*64))
 add('CustomData falsely present',lambda r:r['targets']['CustomData'].__setitem__('present',True))
 add('archive count',lambda r:r['archive'].__setitem__('minecraft_patch_count',754))
 add('wrong reference',lambda r:r['reference'].__setitem__('userdev_sha256','0'*64))
 add('unsafe mutator promotion',lambda r:r['limitations'].__setitem__('mutating_hook','VERIFIED'))
 add('unsafe physical promotion',lambda r:r['limitations'].__setitem__('physical_qa','PASSED'))
 for label,forgery in forged:
  try: validate(forgery,manifest,raw,strict_outer=False)
  except (ValueError,AssertionError,KeyError,TypeError): pass
  else: raise AssertionError('adversarial patch report accepted: '+label)
 print(f'PASS: {len(forged)} independent report forgeries rejected after bypassing outer report digest')

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--report',type=Path,required=True)
 ap.add_argument('--manifest',type=Path,required=True)
 ap.add_argument('--adversarial',action='store_true')
 args=ap.parse_args()
 raw,report=load(args.report,2_000_000)
 _,manifest=load(args.manifest,2_000_000)
 validate(report,manifest,raw)
 if args.adversarial: adversarial(report,manifest,raw)
 print('PASS: official userdev SHA, 753 patches, two exact target files, 29 matched lines, immutable limits; NO_MUTATION')

if __name__=='__main__': main()
