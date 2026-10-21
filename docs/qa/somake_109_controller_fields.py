#!/usr/bin/env python3
"""SHA-exact clean-room controller-field provenance survey for Somake 1.0.9.

Metadata limited to method descriptors, field operations, typed numeric/local
operand windows and Set call categories. No JAR, classfiles, method bodies,
source, third-party assets or unrestricted disassembly leave the CI runner.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows
from somake_109_bud_wither_construction import (
    CONTROLLER,BUD,certify_wither_constructor_handoff,
    certify_exact_wither_handoff_109,
)
from somake_109_bud_operand_provenance import operand_contract,certify_exact_bud_operand_contract_109
from somake_109_wave_maxtargets import prove_wave_list_cap,certify_exact_wave_list_cap_109,prove_wave_loop_spawn_sites,certify_exact_wave_loop_109

FIELDS={"witherDuration","witherAmplifier","impactDamage","activeTargetIds"}
MAX_TEXT=1_500_000
def field(row):
    _,op,_,comment=row
    if op not in ("putfield","getfield","getstatic","putstatic"):return None
    m=re.search(r"\bField (?:[\w/$]+\.)?([\w$]+):([^\s]+)",comment)
    return (m.group(1),m.group(2)) if m else None

def token(i,row):
    _,op,operand,comment=row
    item={"index":i,"op":op}
    m=re.match(r"^([a-z]+)(?:load|store)_([0-9]+)$",op)
    if m:item["slot"]=int(m.group(2))
    elif op in ("aload","astore","iload","istore","fload","fstore","dload","dstore"):
        if operand.isdecimal():item["slot"]=int(operand)
    elif op=="iinc":
        m=re.fullmatch(r"(\d+),\s*(-?\d+)",operand)
        if m:item["slot"]=int(m.group(1));item["increment"]=int(m.group(2))
    elif op.startswith("iconst_"):item["constant"]=op.removeprefix("iconst_")
    elif op in ("bipush","sipush") and operand.lstrip("-").isdigit():item["constant"]=int(operand)
    elif op.startswith("ldc"):
        m=re.search(r"\b(?:float|double|int|long) ([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",comment)
        if m:item["constant"]=m.group(1)
    f=field(row)
    if f:item["field"],item["descriptor"]=f
    if op.startswith("invoke"):
        m=re.search(r"(?:Method|InterfaceMethod) ([^:]+):(\([^ ]*\)[^ ]+)",comment)
        if m:
            item["call"]=m.group(1).rsplit(".",1)[-1].replace('"',"")[:85]
            item["descriptor"]=m.group(2)[:150]
            if m.group(1).startswith("java/util/Set.") or ".Set." in m.group(1):item["family"]="set"
            if "FuneralBloom" in m.group(1):item["family"]="funeral_bloom"
    return item

def scan(methods):
    found=[]
    for name,desc,body in methods:
        rows=opcode_rows(body)
        targets=[(i,f[0],f[1],op) for i,(pc,op,operand,comment) in enumerate(rows)
                 if (f:=field(rows[i])) is not None and f[0] in FIELDS]
        if not targets:continue
        if len(targets)>45:return {"status":"NOT_PROVED","reason":"too_many_field_operations"}
        blocks=[]
        for i,fn,fd,operation in targets:
            blocks.append({
                "site":i,"field":fn,"descriptor":fd,"operation":operation,
                "window":[token(j,rows[j]) for j in range(max(0,i-8),min(len(rows),i+5))]
            })
        set_calls=[token(i,row) for i,row in enumerate(rows)
                   if row[1].startswith("invoke") and ("java/util/Set." in row[3]
                   or "java/util/Collection." in row[3] or "getUUID:()" in row[3])]
        found.append({
            "name":name,"descriptor":desc,"instruction_count":len(rows),
            "field_sites":blocks,"set_calls":set_calls[:25],
        })
    if len(found)>36:return {"status":"NOT_PROVED","reason":"too_many_methods"}
    if not any(any(z["field"]=="witherDuration" and z["operation"]=="putfield" for z in m["field_sites"]) for m in found):
        return {"status":"NOT_PROVED","reason":"no_wither_duration_write"}
    return {
        "status":"OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY",
        "methods":found,"method_count":len(found),
        "boundary":"Presence and typed operands only; not a proven spell-level formula, persisted ownership, cross-bud dedup or per-player adapter",
    }

def inspect(jar:Path):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("untrusted filename/size")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("wrong publisher SHA")
    with zipfile.ZipFile(jar) as a:
        names=a.namelist()
        if len(names)!=len(set(names)) or any(c.replace(".","/")+".class" not in names for c in (CONTROLLER,BUD)):
            raise GateError("class not in exact JAR or ZIP duplicate")
        meta=a.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("wrong mod ID")
    def methods(cls):
        p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),cls],
                         capture_output=True,text=True,timeout=60,check=False)
        if p.returncode or not p.stdout or len(p.stdout)>MAX_TEXT:raise GateError("bounded javap failed")
        return sections(p.stdout)
    controller=methods(CONTROLLER);bud=methods(BUD)
    certify_exact_bud_operand_contract_109(operand_contract(bud))
    certify_exact_wave_list_cap_109(prove_wave_list_cap(controller))
    certify_exact_wave_loop_109(prove_wave_loop_spawn_sites(controller))
    certify_exact_wither_handoff_109(certify_wither_constructor_handoff(bud,controller))
    proof=scan(controller)
    if proof["status"]!="OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY":
        raise GateError("controller source observation failed:"+proof.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("artifact altered")
    return {"mod_id":"somakespells","version":"1.0.9","sha1":digest,"survey":proof}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_CONTROLLER_FIELD_SURVEY",json.dumps(result["survey"],sort_keys=True))
    print("SOMAKE_CONTROLLER_FIELD_SHA",result["sha1"])

if __name__=="__main__":
    main()
