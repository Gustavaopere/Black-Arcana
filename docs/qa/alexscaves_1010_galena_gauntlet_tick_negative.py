#!/usr/bin/env python3
"""Reseal 15 forged Galena JVM opcode pivots and require causal rejection."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

CASES=(
    ("teletor-distinction","tick",170),
    ("owner-using-gauntlet","tick",544),
    ("use-item-check","tick",593),
    ("base-range","tick",552),
    ("ferrous-haste-provider","tick",608),
    ("field-extension-provider","tick",626),
    ("range-factor","tick",639),
    ("raycast","tick",659),
    ("entity-strike","tick",771),
    ("haste-cooldown","tick",780),
    ("default-random-cooldown","tick",790),
    ("block-destroy-request","tick",1290),
    ("player-inventory-return","tick",1516),
    ("returned-drop","plopItem",17),
    ("target-absent-sentinel","getTarget",19),
)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--checker",type=Path,required=True)
    args=ap.parse_args()
    original=json.loads(args.report.read_text(encoding="utf8"))
    seal=json.loads(args.manifest.read_text(encoding="utf8"))
    target="com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
    with TemporaryDirectory() as temp:
        for name,method,offset in CASES:
            r=copy.deepcopy(original)
            s=copy.deepcopy(seal)
            candidate=[m for m in r["entity_native"]["targets"][target]["methods"]
                       if m["declaration"]["name"]==method]
            expected=[m for m in s["methods"] if m["name"]==method]
            assert len(candidate)==len(expected)==1,name
            body=candidate[0]
            rows=[i for i in body["instructions"] if i["offset"]==offset]
            assert len(rows)==1 and rows[0]["opcode"]!="nop",name
            rows[0]["opcode"]="nop"
            instr_raw=(json.dumps(body["instructions"],sort_keys=True,
                    ensure_ascii=False,indent=2)+"\n").encode("utf8")
            digest=hashlib.sha256(instr_raw).hexdigest()
            body["instruction_sha256"]=digest
            expected[0]["instruction_sha256"]=digest
            report_raw=json.dumps(r,sort_keys=True,ensure_ascii=False).encode("utf8")
            s["evidence"]["report_sha256"]=hashlib.sha256(report_raw).hexdigest()
            s["evidence"]["report_bytes"]=len(report_raw)
            rpath=Path(temp)/(name+"-report.json")
            spath=Path(temp)/(name+"-seal.json")
            rpath.write_bytes(report_raw)
            spath.write_text(json.dumps(s,ensure_ascii=False),encoding="utf8")
            p=subprocess.run((sys.executable,str(args.checker),
                             "--report",str(rpath),"--manifest",str(spath)),
                             capture_output=True,text=True,timeout=15)
            assert p.returncode!=0 and "JVM opcode drift" in p.stderr,(name,p.stderr[-700:])
            print("PASS_FORGED_JVM_REJECTED",name)
    print("PASS: 15/15 forged JVM behavior pivots rejected by causal opcode validation")

if __name__=="__main__":
    main()
