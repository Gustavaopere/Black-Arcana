#!/usr/bin/env python3
"""Adversarial probes: re-seal reports and require causal JVM opcode rejection."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
from tempfile import TemporaryDirectory
CASES=(('server-save-skip',0,7),('server-save-data',0,27),('server-save-event',0,84),('server-wait-boolean',0,91),('server-wait-call',0,94),('upgrader-storage-save',1,71),('upgrader-wait-call',1,74),('upgrader-finished',1,103))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('report','manifest','checker'):p.add_argument('--'+name,required=True,type=Path)
 a=p.parse_args()
 r=json.loads(a.report.read_text());w=json.loads(a.manifest.read_text())
 with TemporaryDirectory() as td:
  for name,idx,offset in CASES:
   report=copy.deepcopy(r);seal=copy.deepcopy(w)
   method=report['archives'][0]['direct_invoke_sites'][idx]['method']
   ins=[x for x in method['instructions'] if x['offset']==offset]
   assert len(ins)==1 and ins[0]['opcode']!='nop',name
   ins[0]['opcode']='nop'
   digest=hashlib.sha256((json.dumps(method['instructions'],sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
   method['instruction_sha256']=digest
   seal['archives'][0]['direct_invoke_sites'][idx]['instruction_sha256']=digest
   forged=json.dumps(report,sort_keys=True,ensure_ascii=False).encode()
   seal['evidence']['report_bytes']=len(forged)
   seal['evidence']['report_sha256']=hashlib.sha256(forged).hexdigest()
   ra=Path(td)/(name+'.json');sa=Path(td)/(name+'-seal.json')
   ra.write_bytes(forged);sa.write_text(json.dumps(seal,ensure_ascii=False))
   out=subprocess.run((sys.executable,str(a.checker),'--report',str(ra),'--manifest',str(sa)),capture_output=True,text=True)
   assert out.returncode!=0 and 'JVM opcode drift' in out.stderr,(name,out.stderr[-600:])
   print('PASS_FORGED_JVM_REJECTED',name)
 print('PASS: all 8 forged guards/calls rejected via JVM opcode drift')
if __name__=='__main__':main()
