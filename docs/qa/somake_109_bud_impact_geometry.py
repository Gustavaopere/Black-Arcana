#!/usr/bin/env python3
"""SHA-exact clean-room Somake 1.0.9 Funeral Bloom Bud impact geometry scout.

Only derived topological facts and bounded typed operand windows are emitted.
Provider source, bytecode, full disassembly, JAR and assets are never exported.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, zipfile
from pathlib import Path
from collections import Counter
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows

CLASS="com.somake.somakespells.entity.FuneralBloomBudEntity"
DESC="(Lnet/minecraft/server/level/ServerLevel;)V"
MAX_TEXT=1_400_000

def category(op,symbol):
    if not op.startswith("invoke"):return ""
    if "AABB.inflate:(DDD)" in symbol:return "aabb_inflate_DDD"
    if "getBoundingBox:()" in symbol:return "get_bounding_box"
    if "getEntitiesOfClass:" in symbol:return "query_living_entities"
    if "DamageSources.applyDamage:" in symbol:return "apply_damage"
    if "SpellHealEvent" in symbol:return "spell_heal_event"
    if ".heal:" in symbol:return "heal"
    if "MobEffects.WITHER" in symbol:return "wither"
    if ".addEffect:" in symbol:return "add_effect"
    if ".push:" in symbol:return "push"
    if "isAlliedTo:" in symbol:return "is_allied"
    if "getOwner:" in symbol:return "get_owner"
    if "getCaster:" in symbol:return "get_caster"
    if "getImpactDamage:" in symbol:return "get_impact_damage"
    if "getEntities:" in symbol:return "query_entities"
    m=re.search(r"(?:Method|InterfaceMethod) (?:[^ .]+\.)?([A-Za-z_$][A-Za-z0-9_$]*):\(",symbol)
    return "other_"+m.group(1) if m else "unknown"

def literal_tag(op,comment):
    if op.startswith(("ldc","bipush","sipush")):
        m=re.search(r"(?:double|float|int)\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)",comment)
        if m:return "bounded_numeric_constant:"+m.group(1)[:40]
        return "symbolic_literal"
    if re.fullmatch(r"[dfi]const_[0-5]",op):return op
    return ""

def impact_scout(declared):
    members=[body for name,desc,body in declared if name=="impact" and desc==DESC]
    if len(members)!=1:return {"status":"NOT_PROVED","reason":"missing_or_ambiguous_impact_method"}
    rows=opcode_rows(members[0])
    if len(rows)!=279:return {"status":"NOT_PROVED","reason":"unexpected_impact_instruction_count","instruction_count":len(rows)}
    calls=[{"index":i,"kind":category(op,comment)}
           for i,(_,op,_,comment) in enumerate(rows) if op.startswith("invoke")]
    grouped={tag:[item["index"] for item in calls if item["kind"]==tag]
             for tag in ("get_bounding_box","aabb_inflate_DDD","query_living_entities",
                         "apply_damage","spell_heal_event","heal","is_allied","get_owner",
                         "get_impact_damage","push","add_effect")}
    if len(grouped["aabb_inflate_DDD"])!=1 or not grouped["query_living_entities"]:
        return {"status":"NOT_PROVED","reason":"missing_nonunique_box_or_query",
                "inflates":len(grouped["aabb_inflate_DDD"]),"queries":len(grouped["query_living_entities"])}
    def window(site,back=14,ahead=9):
        start=max(0,site-back);end=min(len(rows),site+ahead+1)
        return [{"index":i,"opcode":rows[i][1],
                 "typed_value":literal_tag(rows[i][1],rows[i][3]),
                 "call":category(rows[i][1],rows[i][3]) if rows[i][1].startswith("invoke") else "",
                 "local_slot":(rows[i][2] if rows[i][1] in ("aload","astore","fload","fstore","dload","dstore","iload","istore") else "")}
                for i in range(start,end)]
    branches=[]
    position={pc:i for i,(pc,_,_,_) in enumerate(rows)}
    for i,(_,op,arg,_) in enumerate(rows):
        if not (op.startswith(("if","goto"))):continue
        dest=arg.split(" ",1)[0] if arg else ""
        if not dest.isdecimal() or int(dest) not in position:
            return {"status":"NOT_PROVED","reason":"unresolved_impact_branch"}
        branches.append({"index":i,"op":op,"target_index":position[int(dest)]})
    return {
       "status":"OBSERVED_BUD_IMPACT_TOPOLOGY_ONLY",
       "instruction_count":len(rows),
       "calls_by_category":grouped,
       "calls_order":calls[:90],
       "conditional_count":sum(b["op"].startswith("if") for b in branches),
       "branch_indices":branches[:45],
       "aabb_window":window(grouped["aabb_inflate_DDD"][0]),
       "query_windows":[window(i,6,5) for i in grouped["query_living_entities"][:2]],
       "damage_windows":[window(i,8,5) for i in grouped["apply_damage"][:2]],
       "opcode_histogram":dict(sorted(Counter(op for _,op,_,_ in rows).items())),
       "boundary":"Observed shapes only. Box operand values, query identity, damage/heal branches, procs and hooks not proved",
    }

def inspect(jar):
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("Somake publisher filename/size invalid")
    sha=hashlib.sha1(jar.read_bytes()).hexdigest()
    if sha!=SHA1:raise GateError("publisher SHA mismatch")
    with zipfile.ZipFile(jar) as archive:
        names=archive.namelist()
        if len(set(names))!=len(names) or CLASS.replace(".","/")+".class" not in names:
            raise GateError("missing class or duplicate ZIP member")
        toml=archive.read("META-INF/neoforge.mods.toml")
        if len(toml)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",toml):
            raise GateError("mod id mismatch")
    j=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),CLASS],
          capture_output=True,text=True,timeout=60,check=False)
    if j.returncode or not j.stdout or len(j.stdout)>MAX_TEXT:
        raise GateError("javap failed or output exceeded budget")
    x=impact_scout(sections(j.stdout))
    if x.get("status")!="OBSERVED_BUD_IMPACT_TOPOLOGY_ONLY":
        raise GateError("impact topology unproved:"+x.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=sha:
        raise GateError("source artifact changed during inspection")
    return {"status":"SHA_EXACT_BUD_IMPACT_SCOUT","mod_id":"somakespells",
            "version":"1.0.9","sha1":sha,"impact":x,
            "limitations":"static topology only, no gameplay or provider per-player setter"}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jar",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_BUD_IMPACT_SCOUT",json.dumps(result["impact"],sort_keys=True))
    print("SOMAKE_BUD_IMPACT_SHA",result["sha1"])
if __name__=="__main__":
    main()
