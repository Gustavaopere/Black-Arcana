#!/usr/bin/env python3
"""Read-only Somake 1.0.9 FuneralBloomBud constructor/Wither provenance scout.

Output is bounded *derived metadata* only, not provider bytecode, source,
classfile, JAR, disassembly, or assets. This is not per-player API approval.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows
from somake_109_bud_operand_provenance import operand_contract,certify_exact_bud_operand_contract_109
from somake_109_wave_maxtargets import (
    prove_wave_list_cap,certify_exact_wave_list_cap_109,
    prove_wave_loop_spawn_sites,certify_exact_wave_loop_109,
)
BUD="com.somake.somakespells.entity.FuneralBloomBudEntity"
CONTROLLER="com.somake.somakespells.entity.FuneralBloomControllerEntity"
LAUNCH_DESC="(Lnet/minecraft/server/level/ServerLevel;)V"
MAX_DISASM=1_500_000
WATCH={"witherDuration","witherAmplifier","impactDamage","getWitherDuration","getWitherAmplifier",
       "getImpactDamage","activeTargetIds","FuneralBloomBudEntity"}

def san(i,row):
    _,op,args,comment=row
    out={"i":i,"op":op}
    m=re.fullmatch(r"([a-z]+)(?:load|store)_([0-9]+)",op)
    if m:out["slot"]=int(m.group(2))
    elif op in ("aload","astore","iload","istore","fload","fstore","dload","dstore") and args.isdecimal():
        out["slot"]=int(args)
    elif op=="iinc":
        m=re.fullmatch(r"(\d+),\s*(-?\d+)",args)
        if m:out.update(slot=int(m.group(1)),increment=int(m.group(2)))
    elif op.startswith("iconst_"):out["literal"]=op.split("_")[-1]
    elif op in ("bipush","sipush") and args.lstrip("-").isdigit():out["literal"]=int(args)
    elif op.startswith("ldc"):
        m=re.search(r"\b(?:float|double|int|long)\s+([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",comment)
        if m:out["literal"]=m.group(1)
    if op in ("putfield","getfield","getstatic","putstatic"):
        m=re.search(r"\bField (?:[\w/$]+\.)?([A-Za-z0-9_$]+):([^\s]+)",comment)
        if m:out.update(field=m.group(1),descriptor=m.group(2))
    elif op.startswith("invoke"):
        m=re.search(r"(?:Method|InterfaceMethod) ([^:]+):(\([^ ]*\)[^ ]+)",comment)
        if m:
            out["call"]=m.group(1).rsplit(".",1)[-1].replace('"',"")
            out["descriptor"]=m.group(2)
            if "FuneralBloomBudEntity" in m.group(1):out["owner"]="Bud"
            elif "FuneralBloomControllerEntity" in m.group(1):out["owner"]="Controller"
    return out

def ctor_scout(bud,controller):
    constructors=[(n,d,b) for n,d,b in bud if n.rsplit(".",1)[-1]=="FuneralBloomBudEntity"]
    wave=[(n,d,b) for n,d,b in controller if n=="launchWave" and d==LAUNCH_DESC]
    if not 1<=len(constructors)<=6 or len(wave)!=1:
        return {"status":"NOT_PROVED","reason":"constructor_or_wave_missing_or_ambiguous",
                "constructor_count":len(constructors),"wave_count":len(wave)}
    wrows=opcode_rows(wave[0][2])
    if len(wrows)!=196:return {"status":"NOT_PROVED","reason":"wave_shape_drift"}
    ctor_sites=[i for i,r in enumerate(wrows) if r[1]=="invokespecial"
                and "FuneralBloomBudEntity" in r[3] and '"<init>"' in r[3]]
    if ctor_sites!=[93]:return {"status":"NOT_PROVED","reason":"bud_instantiation_drift","count":len(ctor_sites)}
    wave_window=[san(i,wrows[i]) for i in range(73,106)]
    ctor_proofs=[]
    for name,desc,body in constructors:
        rows=opcode_rows(body)
        if len(rows)>275:raise GateError("constructor unexpectedly large")
        mutations=[(i,san(i,r)) for i,r in enumerate(rows)
                   if r[1] in ("putfield","invokevirtual","invokespecial") and
                   any(w in r[3] for w in WATCH)]
        sites=[i for i,item in mutations]
        blocks=[]
        for i in sites[:18]:
            blocks.append({"site":i,"around":[san(j,rows[j]) for j in range(max(0,i-7),min(len(rows),i+3))]})
        ctor_proofs.append({
            "jvm_descriptor":desc,"instruction_count":len(rows),
            "field_write_sites":[item for i,item in mutations if item["op"]=="putfield"],
            "watched_sites":[{"i":i,"kind":d.get("call",d.get("field","other"))} for i,d in mutations],
            "bounded_operand_windows":blocks,
        })
    return {"status":"OBSERVED_CONSTRUCTOR_AND_WAVE_ARGUMENT_WINDOWS_ONLY",
            "constructor_count":len(constructors),
            "constructors":ctor_proofs,
            "wave_bud_ctor_index":93,
            "wave_bud_ctor_descriptor":san(93,wrows[93]).get("descriptor","unknown"),
            "wave_argument_window":wave_window,
            "boundary":"No assignment chain or cross-bud dedup certified by callsite cooccurrence. No gameplay or per-player mutator proved."}

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong artifact")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("publisher SHA-1 mismatch")
    with zipfile.ZipFile(jar) as f:
        names=f.namelist()
        if len(names)!=len(set(names)) or any(cls.replace(".","/")+".class" not in names for cls in (BUD,CONTROLLER)):
            raise GateError("missing class/ZIP duplication")
        meta=f.read("META-INF/neoforge.mods.toml")
        if len(meta)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("wrong mod ID")
    def methods(name):
        p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),name],
                         capture_output=True,text=True,timeout=60,check=False)
        if p.returncode or not p.stdout or len(p.stdout)>MAX_DISASM:
            raise GateError("bounded javap failed")
        return sections(p.stdout)
    bud=methods(BUD);wave=methods(CONTROLLER)
    certify_exact_bud_operand_contract_109(operand_contract(bud))
    certify_exact_wave_list_cap_109(prove_wave_list_cap(wave))
    certify_exact_wave_loop_109(prove_wave_loop_spawn_sites(wave))
    result=ctor_scout(bud,wave)
    if result["status"]!="OBSERVED_CONSTRUCTOR_AND_WAVE_ARGUMENT_WINDOWS_ONLY":
        raise GateError("constructor/launch wave topology NOT_PROVED:"+result.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=sha:raise GateError("artifact changed")
    return {"mod_id":"somakespells","version":"1.0.9","sha1":sha,
            "constructor_and_wave":result,"scope":"CLEAN_ROOM_METADATA_ONLY"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    out=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_BUD_CTOR_WAVE_SCOUT",json.dumps(out["constructor_and_wave"],sort_keys=True))
    print("SOMAKE_BUD_CTOR_SHA",out["sha1"])
if __name__=="__main__":
    main()
