#!/usr/bin/env python3
"""Reject re-sealed fake NBT writer traces on the actual causal JVM opcodes."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

CASES = (
    ('compound-map','CompoundTag','write','(Ljava/io/DataOutput;)V',4),
    ('compound-named','CompoundTag','write','(Ljava/io/DataOutput;)V',53),
    ('end-byte','CompoundTag','write','(Ljava/io/DataOutput;)V',61),
    ('entry-type','CompoundTag','writeNamedTag','(Ljava/lang/String;Lnet/minecraft/nbt/Tag;Ljava/io/DataOutput;)V',7),
    ('entry-utf','CompoundTag','writeNamedTag','(Ljava/lang/String;Lnet/minecraft/nbt/Tag;Ljava/io/DataOutput;)V',23),
    ('entry-value','CompoundTag','writeNamedTag','(Ljava/lang/String;Lnet/minecraft/nbt/Tag;Ljava/io/DataOutput;)V',30),
    ('list-type','ListTag','write','(Ljava/io/DataOutput;)V',47),
    ('list-count','ListTag','write','(Ljava/io/DataOutput;)V',62),
    ('int-payload','IntTag','write','(Ljava/io/DataOutput;)V',5),
    ('intarray-element','IntArrayTag','write','(Ljava/io/DataOutput;)V',37),
    ('string-payload','StringTag','write','(Ljava/io/DataOutput;)V',5),
)

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--report',type=Path,required=True)
    cli.add_argument('--manifest',type=Path,required=True)
    cli.add_argument('--checker',type=Path,required=True)
    a=cli.parse_args()
    src=json.loads(a.report.read_text()); seal=json.loads(a.manifest.read_text())
    with TemporaryDirectory() as td:
        for name,owner,method,descriptor,offset in CASES:
            r=copy.deepcopy(src); s=copy.deepcopy(seal)
            matched=[(k,x) for k,x in enumerate(r['classes']) if x['owner'].endswith('/'+owner)]
            assert len(matched)==1,name
            k,row=matched[0]
            targets=[(j,m) for j,m in enumerate(row['selected_methods'])
                     if m['declaration']['name']==method and m['declaration']['descriptor']==descriptor]
            assert len(targets)==1,name
            j,m=targets[0]
            instr=[x for x in m['instructions'] if x['offset']==offset]
            assert len(instr)==1 and instr[0]['opcode']!='nop',name
            instr[0]['opcode']='nop'
            sha=hashlib.sha256((json.dumps(m['instructions'],sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()).hexdigest()
            m['instruction_sha256']=sha
            s['classes'][k]['methods'][j]['instruction_sha256']=sha
            raw=json.dumps(r,sort_keys=True,ensure_ascii=False).encode()
            s['evidence']['report_bytes']=len(raw)
            s['evidence']['report_sha256']=hashlib.sha256(raw).hexdigest()
            report=Path(td)/'fake.json'; manifest=Path(td)/'fake-seal.json'
            report.write_bytes(raw); manifest.write_text(json.dumps(s,ensure_ascii=False))
            proc=subprocess.run((sys.executable,str(a.checker),'--report',str(report),'--manifest',str(manifest)),
                                capture_output=True,text=True,check=False)
            assert proc.returncode!=0 and 'JVM opcode drift' in proc.stderr,(name,proc.stderr[-600:])
            print('PASS_FORGED_OPCODE_REJECTED',name)
    print('PASS: all 11 forged JVM pivots rejected for the correct causal reason')

if __name__=='__main__':
    main()
