#!/usr/bin/env python3
"""Clean-room, SHA-exact raycast predicate proof for Somake Funeral Bloom 1.0.9.

Only bounded derived JVM metadata is emitted. No class/JAR/bytecode contents,
publisher code, decompilation, or assets are retained in reports.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME,SHA1,GateError
from somake_109_radius_irons_contract import sections,opcode_rows
from somake_109_funeral_spell_handoff import (
    certify_spell_cast_getters_109,SPELL_ONCAST_DESC,meaning,
)
from somake_109_controller_fields import (
    CONTROLLER,prove_controller_field_lifecycle,certify_exact_controller_lifecycle_109,
)
from somake_109_bud_wither_construction import (
    BUD,certify_wither_constructor_handoff,certify_exact_wither_handoff_109,
)
SPELL="com.somake.somakespells.spells.blood.FuneralBloomSpell"
MAX_JAVAP=1_500_000

def survey(methods):
    oncast=[opcode_rows(b) for n,d,b in methods if n=="onCast" and d==SPELL_ONCAST_DESC]
    if len(oncast)!=1 or len(oncast[0])!=81:
        return {"status":"NOT_PROVED","reason":"native_oncast_drift"}
    rows=oncast[0]
    if rows[13][1]!="invokedynamic" or "test:" not in rows[13][3]:
        return {"status":"NOT_PROVED","reason":"missing_predicate_factory"}
    candidates=[]
    for name,desc,body in methods:
        if not name.startswith("lambda$onCast$"):continue
        r=opcode_rows(body)
        if len(r)>80:return {"status":"NOT_PROVED","reason":"unbounded_predicate"}
        offsets={pc:i for i,(pc,_,_,_) in enumerate(r)}
        tokens=[]
        for i,row in enumerate(r):
            t=meaning(i,row)
            if row[1] in ("instanceof","checkcast","getstatic"):
                m=re.search(r"class ([A-Za-z0-9_/$]+)",row[3])
                if m:t["class"]=m.group(1).rsplit("/",1)[-1]
                mm=re.search(r"Field ([^:]+):([^\s]+)",row[3])
                if mm:t["field"]=mm.group(1).rsplit(".",1)[-1];t["type"]=mm.group(2)[:100]
            if row[1].startswith(("if","goto")):
                w=row[2].split(" ",1)[0] if row[2] else ""
                t["target_index"]=offsets.get(int(w)) if w.isdecimal() else None
            tokens.append(t)
        candidates.append({"name":name,"descriptor":desc,"instruction_count":len(r),"ops":tokens})
    if not 1<=len(candidates)<=4:
        return {"status":"NOT_PROVED","reason":"unexpected_lambda_count","count":len(candidates)}
    return {"status":"OBSERVED_RAYCAST_LAMBDA_TYPED_SHAPES",
            "predicate_factory_index":13,
            "predicate_factory":rows[13][3].split(":",1)[0][:100],
            "oncast_instruction_count":81,
            "candidate_lambdas":candidates,
            "boundary":"Native lambda branch/call shape only; entity passed to raycast, policy, final raycast target and hooks remain unproven"}


def certify_constant_false_predicate(methods):
    """Exact native JVM body; not proof of linkage or raycast fallback."""
    matched=[opcode_rows(b) for n,d,b in methods if
             n=="lambda$onCast$0" and d=="(Lnet/minecraft/world/entity/Entity;)Z"]
    if len(matched)!=1:return {"status":"NOT_PROVED","reason":"lambda_signature_missing_or_ambiguous"}
    r=matched[0]
    siblings=[(n,d) for n,d,b in methods if n.startswith("lambda$onCast$")]
    if len(siblings)!=1:return {"status":"NOT_PROVED","reason":"unexpected_oncast_lambda_set"}
    if len(r)!=2 or r[0][1]!="iconst_0" or r[1][1]!="ireturn":
        return {"status":"NOT_PROVED","reason":"predicate_body_not_constant_false"}
    casts=[opcode_rows(b) for n,d,b in methods if n=="onCast" and d==SPELL_ONCAST_DESC]
    if len(casts)!=1 or len(casts[0])!=81:
        return {"status":"NOT_PROVED","reason":"onCast_shape_drift"}
    cast=casts[0]
    if cast[13][1]!="invokedynamic" or "InvokeDynamic #0:test:()Ljava/util/function/Predicate;" not in cast[13][3]:
        return {"status":"NOT_PROVED","reason":"onCast_predicate_factory_signature_drift"}
    if cast[14][1]!="invokestatic" or "raycastForEntity:" not in cast[14][3]:
        return {"status":"NOT_PROVED","reason":"raycast_function_unproven"}
    return {"status":"PROVED_ONCAST_UNLINKED_LAMBDA_CONSTANT_FALSE",
            "lambda_name":"lambda$onCast$0",
            "lambda_descriptor":"(Lnet/minecraft/world/entity/Entity;)Z",
            "lambda_instruction_count":2,"lambda_boolean_result":False,
            "invokedynamic_index":13,"invokedynamic_bootstrap_index":0,
            "raycast_call_index":14,
            "boundary":"Actual invokedynamic bootstrap linkage, raycastForEntity library behavior, final target and world-position fallback require separate evidence"}

def bootstrap_scout(verbose_text):
    marker="\nBootstrapMethods:"
    pos=verbose_text.find(marker)
    if pos<0:return {"status":"NOT_PROVED","reason":"bootstrap_table_missing"}
    part=verbose_text[pos+len(marker):]
    part=part[:part.find("\nInnerClasses:")] if "\nInnerClasses:" in part else part[:20000]
    if len(part)>20000:return {"status":"NOT_PROVED","reason":"bootstrap_data_oversized"}
    entries=re.split(r"(?m)^\s{2}(\d+):\s+",part)
    # The parser deliberately never returns third-party method bodies.
    found=[]
    for i in range(1,len(entries),2):
        number=int(entries[i]);block=entries[i+1][:3500]
        found.append({"index":number,
                      "lambda_metafactory":("LambdaMetafactory.metafactory" in block.splitlines()[0]),
                      "funeral_lambda_handle":bool(re.search(
                         r"REF_invokeStatic\s+[\w/$]+FuneralBloomSpell\.lambda\$onCast\$0:"
                         r"\(Lnet/minecraft/world/entity/Entity;\)Z",block)),
                      "predicate_method_shape":("(Lnet/minecraft/world/entity/Entity;)Z" in block)})
    return {"status":"OBSERVED_BOOTSTRAP_METHOD_REFERENCES","bootstrap_entries":found[:20],
            "boundary":"Symbolic bootstrap references only; no proof of raycastForEntity external implementation"}

def inspect(jar:Path):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("invalid Somake publisher file")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("Somake official SHA mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or any(k.replace(".","/")+".class" not in names for k in (SPELL,BUD,CONTROLLER)):
            raise GateError("missing class or duplicate ZIP member")
        meta=z.read("META-INF/neoforge.mods.toml")
        if len(meta)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("Somake modID invalid")
    def methods(c):
        p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),c],
                         capture_output=True,text=True,timeout=60,check=False)
        if p.returncode or not p.stdout or len(p.stdout)>MAX_JAVAP:
            raise GateError("bounded javap failed")
        return sections(p.stdout)
    spell,controller,bud=methods(SPELL),methods(CONTROLLER),methods(BUD)
    prior=certify_spell_cast_getters_109(spell)
    if prior["status"]!="PROVED_SOMAKE_FUNERAL_NATIVE_GETTER_FORMULAS_AND_CAST_TO_CONTROLLER":
        raise GateError("previous cast gate drift")
    certify_exact_controller_lifecycle_109(prove_controller_field_lifecycle(controller))
    certify_exact_wither_handoff_109(certify_wither_constructor_handoff(bud,controller))
    result=survey(spell)
    false_body=certify_constant_false_predicate(spell)
    print("SOMAKE_RAYCAST_FALSE_LAMBDA_PROOF",json.dumps(false_body,sort_keys=True))
    if false_body["status"]!="PROVED_ONCAST_UNLINKED_LAMBDA_CONSTANT_FALSE":
        raise GateError("lambda false body changed:"+false_body.get("reason","unknown"))
    verbose=subprocess.run(["javap","-p","-v","-classpath",str(jar.resolve()),SPELL],
                           capture_output=True,text=True,timeout=60,check=False)
    if verbose.returncode or not verbose.stdout or len(verbose.stdout)>MAX_JAVAP:
        raise GateError("bounded verbose javap unavailable")
    bootstrap=bootstrap_scout(verbose.stdout)
    print("SOMAKE_RAYCAST_BOOTSTRAP_SCOUT",json.dumps(bootstrap,sort_keys=True))
    if result["status"]!="OBSERVED_RAYCAST_LAMBDA_TYPED_SHAPES":
        raise GateError("native lambda shape unknown:"+result.get("reason",""))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=sha:raise GateError("artifact changed during inspection")
    return {"sha1":sha,"version":"1.0.9","mod_id":"somakespells","raycast_lambda":result,"false_lambda":false_body,"bootstrap":bootstrap}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    args=a.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_RAYCAST_LAMBDA_SCOUT",json.dumps(result["raycast_lambda"],sort_keys=True))
    print("SOMAKE_RAYCAST_LAMBDA_SHA",result["sha1"])
if __name__=="__main__":
    main()
