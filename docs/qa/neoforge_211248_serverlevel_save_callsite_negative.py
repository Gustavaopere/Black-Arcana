#!/usr/bin/env python3
"""Re-seal forged JVM pivots; require independent causal opcode rejection."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

TESTS = (
  ("shutdown-nosave-clear", "saveallchunks", 0, "stopServer", 117),
  ("shutdown-flag-1", "saveallchunks", 0, "stopServer", 221),
  ("shutdown-wait-flag", "saveallchunks", 0, "stopServer", 222),
  ("shutdown-override-flag", "saveallchunks", 0, "stopServer", 223),
  ("shutdown-save-call", "saveallchunks", 0, "stopServer", 224),
  ("save-flush-forward", "serverlevel_save", 0, "saveAllChunks", 64),
  ("save-nosave-filter", "serverlevel_save", 0, "saveAllChunks", 73),
  ("worldgen-skip-flag", "serverlevel_save", 2, "lambda$acceptChunkResult$5", 6),
  ("manual-save-forward", "saveallchunks", 0, "saveEverything", 16),
)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("serverlevel-report","saveallchunks-report","manifest","checker"):
        p.add_argument("--"+name,required=True,type=Path)
    a=p.parse_args()
    raw={"serverlevel_save":json.loads(a.serverlevel_report.read_text()),
         "saveallchunks":json.loads(a.saveallchunks_report.read_text())}
    seal=json.loads(a.manifest.read_text())
    with TemporaryDirectory() as td:
        for case,key,archive_idx,method_name,offset in TESTS:
            r=copy.deepcopy(raw)
            m=copy.deepcopy(seal)
            items=r[key]["archives"][archive_idx]["direct_invoke_sites"]
            candidate=[x for x in items if x["method"]["declaration"]["name"]==method_name]
            assert len(candidate)==1,case
            body=candidate[0]["method"]
            rows=[x for x in body["instructions"] if x["offset"]==offset]
            assert len(rows)==1 and rows[0]["opcode"]!="nop",case
            rows[0]["opcode"]="nop"
            replacement=hashlib.sha256((json.dumps(body["instructions"],sort_keys=True,
                                           ensure_ascii=False,indent=2)+"\n").encode()).hexdigest()
            body["instruction_sha256"]=replacement
            sealed=[x for x in m["methods"] if x["report"]==key and x["archive"]==archive_idx
                    and x["name"]==method_name]
            assert len(sealed)==1,case
            sealed[0]["instruction_sha256"]=replacement
            output=json.dumps(r[key],sort_keys=True,ensure_ascii=False).encode()
            m["evidence"][key]["bytes"]=len(output)
            m["evidence"][key]["sha256"]=hashlib.sha256(output).hexdigest()
            p1=Path(td)/"serverlevel.json"
            p2=Path(td)/"saveallchunks.json"
            pm=Path(td)/"seal.json"
            p1.write_bytes(output if key=="serverlevel_save" else a.serverlevel_report.read_bytes())
            p2.write_bytes(output if key=="saveallchunks" else a.saveallchunks_report.read_bytes())
            pm.write_text(json.dumps(m,sort_keys=True,ensure_ascii=False))
            proc=subprocess.run((sys.executable,str(a.checker),
                     "--serverlevel-report",str(p1),"--saveallchunks-report",str(p2),
                     "--manifest",str(pm)),capture_output=True,text=True)
            assert proc.returncode!=0 and "JVM opcode drift" in proc.stderr,(case,proc.stderr[-900:])
            print("PASS_FORGED_JVM_REJECTED",case)
    print("PASS: 9/9 forged shutdown/boolean/caller pivots rejected via causal JVM opcode drift")

if __name__=="__main__":
    main()
