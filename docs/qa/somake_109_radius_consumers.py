#!/usr/bin/env python3
"""Somake 1.0.9 radius consumer *references*, not inferred value propagation.

SHA-pinned, bounded javap method-level callsites for three exact classfiles.
No provider implementation, bytecode, classes, or JARs exported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_cast_refs import SYMBOL
from somake_109_funeral_bud_probe import isolate_named_methods

CLASSES={
    "spell":"com.somake.somakespells.spells.blood.FuneralBloomSpell",
    "controller":"com.somake.somakespells.entity.FuneralBloomControllerEntity",
    "bud":"com.somake.somakespells.entity.FuneralBloomBudEntity",
}
METHODS={
    "spell":("onCast","getRadius"),
    "controller":("tick","launchWave"),
    "bud":("tick","impact"),
}
KEYS={
    "radius":("getRadius:", "getRadius("),
    "spawn_controller":("FuneralBloomControllerEntity.",),
    "wave":("launchWave:", "FuneralBloomBudEntity."),
    "aabb":("AABB.inflate:", "getBoundingBox:", "AABB.<init>:"),
    "query":("getEntitiesOfClass:", "getEntities:", "distanceToSqr:"),
    "damage":("DamageSources.applyDamage:", "LivingEntity.hurt:", "getImpactDamage:"),
    "heal":("SpellHealEvent", "LivingEntity.heal:", "getHealing:"),
    "owner":("getOwner:", "getCaster:", "isAlliedTo:"),
}
MAX_TEXT=1_400_000
MAX_METHODS=180
MAX_METHOD_INSTRUCTIONS=2800
MAX_SYMBOLS_PER_METHOD=110
MAX_SYMBOL_LEN=900

def wave_radius_aabb_shape(body:list[str])->dict:
    """Return bounded callsite topology only; never infer values by co-occurrence."""
    rows=opcode_rows(body)
    if len(rows)>250:raise GateError("oversized Funeral Bloom wave method")
    radius=[];inflates=[]
    for i,(_,op,_,symbol) in enumerate(rows):
        if op in ("invokevirtual","invokespecial"):
            if symbol in (
                "Method getRadius:()F",
                "Method com/somake/somakespells/entity/FuneralBloomControllerEntity.getRadius:()F"):
                radius.append(i)
            if symbol=="Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;":
                inflates.append(i)
    if not radius or not inflates:
        return {"status":"NOT_PROVED","reason":"radius_or_inflate_not_found",
                "radius_call_count":len(radius),"inflate_call_count":len(inflates)}
    pairs=[(r,a) for r in radius for a in inflates if r<a]
    branch=sum(op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch")
               for _,op,_,_ in rows)
    if not pairs:
        return {"status":"NOT_PROVED","reason":"radius_does_not_precede_inflate",
                "radius_call_count":len(radius),"inflate_call_count":len(inflates)}
    r,a=min(pairs,key=lambda pair:pair[1]-pair[0])
    between=rows[r+1:a]
    callnames=sorted(set(symbol for _,op,_,symbol in between if op.startswith("invoke")))
    if len(callnames)>30:return {"status":"NOT_PROVED","reason":"intervening_method_symbol_budget"}
    return {
        "status":"STRUCTURAL_ONLY_NO_AABB_OPERAND_PROVENANCE",
        "radius_call_count":len(radius),
        "inflate_call_count":len(inflates),
        "radius_before_inflate":True,
        "instruction_count":len(rows),
        "f2d_instruction_count":sum(op=="f2d" for _,op,_,_ in rows),
        "branch_instruction_count":branch,
        "invokedynamic_instruction_count":sum(op=="invokedynamic" for _,op,_,_ in rows),
        "nearest_radius_to_inflate_instruction_gap":a-r-1,
        "intervening_method_symbols":callnames,
        "intervening_branch_instruction_count":sum(
            op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch")
            for _,op,_,_ in between),
        "intervening_float_to_double_count":sum(op=="f2d" for _,op,_,_ in between),
        "intervening_double_arithmetic_count":sum(op in
            ("dadd","dsub","dmul","ddiv","dneg","drem") for _,op,_,_ in between),
        "boundary":"Callsite order and opcode counts only; AABB DDD operand stack and world hitbox NOT proved."
    }

def calls_in_method(body:list[str])->dict:
    """Only bytecode callsite comments; fields are separately counted."""
    if len(body)>4500:raise GateError("oversized method section")
    records=[]
    fields=[]
    dynamic_invokes=0
    opcount=0
    for line in body:
        before,sep,after=line.partition("//")
        match=re.match(r"^\s*\d+:\s+([a-z][a-z0-9_]*)(?:\s+.*?)?$",before)
        if match:
            opcount+=1
            if opcount>MAX_METHOD_INSTRUCTIONS:raise GateError("oversized method")
            op=match.group(1)
            if op.startswith("invoke") and not sep:
                raise GateError("invocation missing JVM symbol")
            if not sep:continue
            comment=after.strip()
            if len(comment)>MAX_SYMBOL_LEN:raise GateError("symbol oversized")
            sm=SYMBOL.match(comment)
            if op=="invokedynamic":
                if not re.match(r"^InvokeDynamic\s+#\d+:[^ ]+",comment):
                    raise GateError("invalid invokedynamic bootstrap descriptor")
                dynamic_invokes+=1
            elif op.startswith("invoke"):
                if not sm or sm.group(1) not in ("Method","InterfaceMethod"):
                    raise GateError("invocation missing JVM symbol for "+op)
                records.append(sm.group(2))
            elif op in ("getfield","putfield","getstatic","putstatic"):
                if sm and sm.group(1)=="Field":
                    fields.append(sm.group(2))
    if len(records)>MAX_SYMBOLS_PER_METHOD:raise GateError("unbounded callsites")
    return {
        "instruction_count":opcount,
        "invoke_count":len(records),
        "invokedynamic_count":dynamic_invokes,
        "callsite_symbols":sorted(set(records)),
        "field_symbols":sorted(set(fields))[:40],
        "classified":{category:sorted(set(x for x in records if any(k in x for k in keywords)))
                      for category,keywords in KEYS.items()},
    }

def analyze_javap(text:str, label:str)->dict:
    if not text or len(text)>MAX_TEXT:raise GateError("oversized class output")
    declared=sections(isolate_named_methods(text))
    if len(declared)>MAX_METHODS:raise GateError("too many class methods")
    selected={}
    for name,desc,body in declared:
        if name not in METHODS[label]:continue
        key=name+desc
        if key in selected:raise GateError("duplicate selected signature")
        selected[key]=calls_in_method(body)
    for target in METHODS[label]:
        if not any(k.startswith(target+"(") for k in selected):
            raise GateError("missing focused method: "+label+"."+target)
    if len(selected)>14:raise GateError("excessive method overloads")
    report={"fqcn":CLASSES[label],"selected_methods":selected}
    if label=="controller":
        candidates=[body for name,desc,body in declared
                    if name=="launchWave" and desc=="(Lnet/minecraft/server/level/ServerLevel;)V"]
        if len(candidates)!=1:raise GateError("missing exact launchWave descriptor")
        report["wave_radius_aabb_shape"]=wave_radius_aabb_shape(candidates[0])
    return report

def certify_exact_consumer_surface(outcome:dict)->None:
    """Ensure exact version callsite relations do not silently change."""
    def single(label,method):
        methods=outcome[label]["selected_methods"]
        found=[row for key,row in methods.items() if key.startswith(method+"(")]
        if len(found)!=1:raise GateError("missing/ambiguous "+label+"."+method)
        return found[0]
    spell=single("spell","onCast")
    tick=single("controller","tick")
    wave=single("controller","launchWave")
    impact=single("bud","impact")
    def require(record,category,match,label):
        symbols=record["classified"][category]
        if not any(match in x for x in symbols):
            raise GateError("exact downstream callsite missing: "+label)
    require(spell,"radius","getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F","spell getter")
    require(spell,"spawn_controller",'''FuneralBloomControllerEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V''',"controller constructor")
    require(tick,"radius","getRadius:()F","controller.tick radius access")
    require(tick,"wave","launchWave:(Lnet/minecraft/server/level/ServerLevel;)V","controller wave dispatch")
    require(wave,"radius","getRadius:()F","wave radius access")
    require(wave,"aabb","AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;","wave AABB")
    require(wave,"query","getEntitiesOfClass:","wave targeting")
    require(wave,"wave",'''FuneralBloomBudEntity."<init>":''',"bud creation")
    require(impact,"aabb","AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;","impact AABB")
    require(impact,"query","getEntitiesOfClass:","impact target query")
    require(impact,"damage","DamageSources.applyDamage:","impact damage")
    require(impact,"heal","SpellHealEvent","impact heal event")
    if impact["classified"]["radius"]:
        raise GateError("unanticipated direct getRadius in bud impact")
    if spell["invokedynamic_count"]<1 or wave["invokedynamic_count"]<1:
        raise GateError("dynamic invocation fingerprint changed")

def inspect(jar:Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME or not 100<jar.stat().st_size<20_000_000:
        raise GateError("wrong Somake file")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:raise GateError("Somake release mismatch")
    with zipfile.ZipFile(jar) as z:
        members=z.namelist()
        if len(members)!=len(set(members)):raise GateError("duplicate zip members")
        meta=z.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("publisher modid mismatch")
        for cls in CLASSES.values():
            if cls.replace(".","/")+".class" not in members:raise GateError("missing class")
    outcome={}
    for label,cls in CLASSES.items():
        process=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),cls],
                               capture_output=True,text=True,timeout=50,check=False)
        if process.returncode or len(process.stdout)>MAX_TEXT:
            raise GateError("javap failed or exceeded budget: "+label)
        result=analyze_javap(process.stdout,label)
        outcome[label]=result
        for method,metrics in result["selected_methods"].items():
            print("SOMAKE_RADIUS_CONSUMER",label,method,
                  "ops",metrics["instruction_count"],
                  "invokes",metrics["invoke_count"],"dynamic",metrics["invokedynamic_count"],
                  "classified",json.dumps(metrics["classified"],sort_keys=True),
                  "fields",json.dumps(metrics["field_symbols"]))
    certify_exact_consumer_surface(outcome)
    print("SOMAKE_WAVE_RADIUS_AABB_SHAPE",json.dumps(outcome["controller"]["wave_radius_aabb_shape"],sort_keys=True))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("JAR changed")
    return {"status":"PASS_SHA_EXACT_METHOD_SYMBOL_DISCOVERY_ONLY",
            "publisher_sha1":digest,"version":"1.0.9","mod_id":"somakespells",
            "scope":outcome,
            "limits":[
                "Method-level callsite and exact descriptors are pinned but NOT constructor-argument mapping or value propagation.",
                "Without dataflow, a radius getter call does NOT prove it is the radius of an AABB or projectile.",
                "No loaded modpack, live player, Survival, client or multiplayer evidence.",
                "No provider JAR, classfile, bytecode or implementation exported.",
                "No provider-native mutation or RPG perk adapter approved."
            ]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    data=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_RADIUS_CONSUMER_GATE",data["status"],data["publisher_sha1"])
if __name__=="__main__":
    main()
