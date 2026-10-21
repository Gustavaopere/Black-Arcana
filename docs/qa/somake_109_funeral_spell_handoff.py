#!/usr/bin/env python3
"""Somake 1.0.9 Funeral Bloom spell-to-controller argument provenance survey.

Clean-room, SHA-exact, bounded metadata only. No publisher code, bytecode,
JAR, classfiles, full disassembly or protected assets are exported.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows
from somake_109_controller_fields import CONTROLLER,BUD,prove_controller_field_lifecycle,certify_exact_controller_lifecycle_109
from somake_109_bud_wither_construction import certify_wither_constructor_handoff,certify_exact_wither_handoff_109

MAX_JAVAP=1_500_000
def meaning(i,row):
    _,op,argument,comment=row
    o={"i":i,"op":op}
    m=re.fullmatch(r"[afid](?:load|store)_([0-9]+)",op)
    if m:o["slot"]=int(m.group(1))
    elif op in ("aload","astore","iload","istore","fload","fstore","dload","dstore") and argument.isdecimal():o["slot"]=int(argument)
    elif op=="iinc":
        mm=re.fullmatch(r"(\d+),\s*(-?\d+)",argument)
        if mm:o["slot"]=int(mm.group(1));o["increment"]=int(mm.group(2))
    elif op in ("bipush","sipush") and argument.lstrip("-").isdecimal():o["number"]=int(argument)
    elif op.startswith("iconst_"):o["number"]=op.split("_")[-1]
    elif op.startswith("fconst_"):o["number"]=op.split("_")[-1]
    elif op.startswith("ldc"):
        mm=re.search(r"\b(?:float|double|int|long)\s+([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",comment)
        if mm:o["number"]=mm.group(1)
    if op in ("getfield","putfield","getstatic","putstatic"):
        mm=re.search(r"\bField (?:[\w/$]+\.)?([\w$]+):([^\s]+)",comment)
        if mm:o["field"]=mm.group(1);o["type"]=mm.group(2)[:90]
    elif op.startswith("invoke"):
        mm=re.search(r"(?:Method|InterfaceMethod) ([^:]+):(\([^ ]*\)[^\s]+)",comment)
        if mm:
            o["call"]=mm.group(1).rsplit(".",1)[-1].replace('"',"")[:90]
            o["descriptor"]=mm.group(2)[:170]
            if "FuneralBloom" in mm.group(1):o["family"]="funeral_bloom"
            elif "Math." in mm.group(1) or "Mth." in mm.group(1):o["family"]="numeric_math"
    elif op=="new":
        mm=re.search(r"\bclass ([\w/$]+)",comment)
        if mm:o["class_name"]=mm.group(1).rsplit("/",1)[-1][:90]
    return o

def spell_scout(methods):
    result=[]
    for name,desc,body in methods:
        rows=opcode_rows(body)
        ctor_sites=[i for i,(_,op,_,comment) in enumerate(rows) if
                    op=="invokespecial" and "FuneralBloomControllerEntity." in comment and '"<init>"' in comment]
        if not ctor_sites:continue
        if len(ctor_sites)>4 or len(rows)>1800:return {"status":"NOT_PROVED","reason":"oversized_or_ambiguous_spell_ctor"}
        references=[i for i,r in enumerate(rows) if r[1].startswith("invoke") and
                    any(needle in r[3] for needle in ("getWitherDuration","getWitherAmplifier",
                         "getImpactDamage","getMaxTargets","getRadius","getSpellPower","getDuration","getWaveInterval"))]
        slices=[{"ctor_site":i,"ctor_symbol":meaning(i,rows[i]),
                 "operand_window":[meaning(j,rows[j]) for j in range(max(0,i-84),min(len(rows),i+9))]}
                for i in ctor_sites]
        result.append({"method":name,"descriptor":desc,"instruction_count":len(rows),
                       "constructor_calls":slices,
                       "getter_calls":[meaning(i,rows[i]) for i in references[:28]],
                       "branch_count":sum(r[1].startswith(("if","goto")) for r in rows)})
    if len(result)!=1:return {"status":"NOT_PROVED","reason":"expected_exactly_one_spell_controller_constructor_path","paths":len(result)}
    return {"status":"OBSERVED_CONTROLLER_CAST_HANDBACK_OPERANDS_ONLY",
            "methods":result,
            "boundary":"Spell-side typed callsite survey only; no per-level values, caster identity, damage settlement, player perk API or physical game proof certified"}

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("Somake JAR invalid filename/type")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("Somake 1.0.9 publisher SHA mismatch")
    with zipfile.ZipFile(jar) as f:
        names=f.namelist()
        if len(names)!=len(set(names)):raise GateError("duplicate member")
        required=[c.replace(".","/")+".class" for c in (CONTROLLER,BUD)]
        if any(c not in names for c in required):raise GateError("missing controller/bud class")
        spell_names=[n for n in names if n.endswith("/FuneralBloomSpell.class")]
        if len(spell_names)!=1:raise GateError("unique spell class not found")
        meta=f.read("META-INF/neoforge.mods.toml")
        if len(meta)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("mod ID mismatch")
        spell=spell_names[0][:-6].replace("/",".")
    def disasm(cls):
        p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),cls],
                         capture_output=True,text=True,timeout=60,check=False)
        if p.returncode or not p.stdout or len(p.stdout)>MAX_JAVAP:raise GateError("javap failed")
        return sections(p.stdout)
    controller=disasm(CONTROLLER);bud=disasm(BUD)
    certify_exact_controller_lifecycle_109(prove_controller_field_lifecycle(controller))
    certify_exact_wither_handoff_109(certify_wither_constructor_handoff(bud,controller))
    result=spell_scout(disasm(spell))
    if result["status"]!="OBSERVED_CONTROLLER_CAST_HANDBACK_OPERANDS_ONLY":
        raise GateError("spell controller handoff remains not proved:"+result.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("publisher artifact changed")
    return {"mod_id":"somakespells","version":"1.0.9","sha1":digest,
            "spell_compiled_class":spell,"spell_constructor_scout":result}
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args();data=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_FUNERAL_SPELL_CLASS",data["spell_compiled_class"])
    print("SOMAKE_FUNERAL_SPELL_SCOUT",json.dumps(data["spell_constructor_scout"],sort_keys=True))
    print("SOMAKE_FUNERAL_SPELL_SHA",data["sha1"])
if __name__=="__main__":
    main()
