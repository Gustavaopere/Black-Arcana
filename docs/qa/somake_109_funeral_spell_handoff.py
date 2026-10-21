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


GETTERS={
 "getRadius":"(ILnet/minecraft/world/entity/LivingEntity;)F",
 "getDuration":"(I)I",
 "getWaveInterval":"(I)I",
 "getTelegraphTicks":"(I)I",
 "getMaxTargets":"(I)I",
 "getImpactDamage":"(ILnet/minecraft/world/entity/LivingEntity;)F",
 "getWitherDuration":"(I)I",
 "getWitherAmplifier":"(I)I",
}
def getter_scout(methods):
    evidence=[]
    for name,desc in GETTERS.items():
        found=[opcode_rows(body) for n,d,body in methods if n==name and d==desc]
        if len(found)!=1:return {"status":"NOT_PROVED","reason":"missing_ambiguous_getter","method":name}
        rows=found[0]
        if not 1<=len(rows)<=110:return {"status":"NOT_PROVED","reason":"getter_instruction_budget","method":name,"count":len(rows)}
        evidence.append({"getter":name,"descriptor":desc,"instruction_count":len(rows),
                         "typed_ops":[meaning(i,row) for i,row in enumerate(rows)]})
    return {"status":"OBSERVED_8_EXACT_GETTER_BODIES_TYPED_ONLY","getters":evidence,
            "boundary":"Getter numeric operand survey; effective stats, cast-side caster provenance, downstream gameplay and per-player hook not proved"}


SPELL_ONCAST_DESC="(Lnet/minecraft/world/level/Level;ILnet/minecraft/world/entity/LivingEntity;Lio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/magic/MagicData;)V"
CTOR_DESC="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V"
EXPECTED={
 "getRadius":(28,{10:9.5,13:0.82,21:0.65,24:10.0,25:15.0},
              {5:("getSchoolType","()Lio/redspace/ironsspellbooks/api/spells/SchoolType;"),
               7:("getPowerFor","(Lnet/minecraft/world/entity/LivingEntity;)D"),
               20:("max","(FF)F"),26:("clamp","(FFF)F")}),
 "getDuration":(11,{0:240,7:20},{4:("clamp","(III)I")}),
 "getWaveInterval":(7,{0:18},{4:("clamp","(III)I")}),
 "getTelegraphTicks":(8,{0:9,1:13},{6:("max","(II)I")}),
 "getMaxTargets":(7,{0:4},{4:("clamp","(III)I")}),
 "getImpactDamage":(9,{0:1.5,5:0.75},
                    {4:("getSpellPower","(ILnet/minecraft/world/entity/Entity;)F")}),
 "getWitherDuration":(9,{0:60,5:12},{4:("clamp","(III)I")}),
 "getWitherAmplifier":(7,{1:5},{}),
}
CONTROL={
 "getRadius":{0:"aload_2",1:"ifnonnull",2:"fconst_1",3:"goto",
              4:"aload_0",6:"aload_2",8:"d2f",9:"fstore_3",
              11:"iload_1",12:"i2f",14:"fmul",15:"fadd",
              16:"fconst_0",17:"fload_3",18:"fconst_1",19:"fsub",
              22:"fmul",23:"fadd",27:"freturn"},
 "getDuration":{1:"iload_1",2:"iconst_1",3:"iconst_5",5:"iconst_1",6:"isub",
                8:"imul",9:"iadd",10:"ireturn"},
 "getWaveInterval":{1:"iload_1",2:"iconst_1",3:"iconst_5",5:"isub",6:"ireturn"},
 "getTelegraphTicks":{2:"iload_1",3:"iconst_2",4:"idiv",5:"isub",7:"ireturn"},
 "getMaxTargets":{1:"iload_1",2:"iconst_1",3:"iconst_5",5:"iadd",6:"ireturn"},
 "getImpactDamage":{1:"aload_0",2:"iload_1",3:"aload_2",6:"fmul",7:"fadd",8:"freturn"},
 "getWitherDuration":{1:"iload_1",2:"iconst_1",3:"iconst_5",6:"imul",7:"iadd",8:"ireturn"},
 "getWitherAmplifier":{0:"iload_1",2:"if_icmplt",3:"iconst_1",4:"goto",5:"iconst_0",6:"ireturn"},
}
def _target(rows,index):
    s=rows[index][2].split(" ",1)[0]
    pc={n:i for i,(n,_,_,_) in enumerate(rows)}
    return pc.get(int(s)) if s.isdecimal() else None

def certify_spell_cast_getters_109(methods):
    """Certify source-pinned native operand calls and formulas, not outcomes."""
    def fail(reason):return {"status":"NOT_PROVED","reason":reason}
    if len([1 for n,d,b in methods if n=="onCast" and d==SPELL_ONCAST_DESC])!=1:
        return fail("onCast_signature_drift")
    cast=opcode_rows(next(b for n,d,b in methods if n=="onCast" and d==SPELL_ONCAST_DESC))
    if len(cast)!=81 or any(op.startswith(("if","goto")) for _,op,_,_ in cast):
        return fail("onCast_control_shape_drift")
    if not (meaning(21,cast[21]).get("class_name")=="FuneralBloomControllerEntity"
            and cast[22][1]=="dup"
            and [meaning(i,cast[i]).get("slot") for i in (23,24,25,26)]==[1,3,0,2]
            and meaning(51,cast[51]).get("descriptor")==CTOR_DESC
            and cast[51][1]=="invokespecial"
            and "FuneralBloomControllerEntity" in cast[51][3]
            and [meaning(i,cast[i]).get("slot") for i in (52,53,54,56,57)]==[8,8,7,1,8]
            and meaning(55,cast[55]).get("call")=="setPos"
            and meaning(58,cast[58]).get("call")=="addFreshEntity"
            and cast[59][1]=="pop"):
        return fail("native_ctor_position_or_spawn_discard_drift")
    calls={28:("getRadius","(ILnet/minecraft/world/entity/LivingEntity;)F"),
           31:("getDuration","(I)I"),
           34:("getWaveInterval","(I)I"),
           37:("getTelegraphTicks","(I)I"),
           40:("getMaxTargets","(I)I"),
           44:("getImpactDamage","(ILnet/minecraft/world/entity/LivingEntity;)F"),
           47:("getWitherDuration","(I)I"),
           50:("getWitherAmplifier","(I)I")}
    for index,(name,desc) in calls.items():
        t=meaning(index,cast[index])
        if t.get("call")!=name or t.get("descriptor")!=desc:
            return fail("getter_call_order_or_signature_drift_"+name)
    if not (meaning(8,cast[8]).get("number")=="32.0"
            and meaning(14,cast[14]).get("call")=="raycastForEntity"
            and meaning(19,cast[19]).get("call")=="groundPosition"):
        # the caster raycast is a separate concern; never infer entity acquisition.
        return fail("target_raycast_source_drift")
    getter_details=[]
    for name,desc in GETTERS.items():
        records=[opcode_rows(body) for n,d,body in methods if n==name and d==desc]
        if len(records)!=1:return fail("getter_missing_or_ambiguous_"+name)
        rows=records[0];length,numbers,refs=EXPECTED[name]
        if len(rows)!=length:return fail("getter_instruction_count_drift_"+name)
        for i,op in CONTROL[name].items():
            if rows[i][1]!=op:return fail("getter_opcode_drift_"+name)
        for i,v in numbers.items():
            n=meaning(i,rows[i]).get("number")
            if n is None or float(n)!=float(v):return fail("getter_literal_drift_"+name)
        for i,(member,methoddesc) in refs.items():
            t=meaning(i,rows[i])
            if t.get("call")!=member or t.get("descriptor")!=methoddesc:
                return fail("getter_invocation_drift_"+name)
        getter_details.append({"name":name,"instructions":length,
                               "bounded_literals":{str(i):v for i,v in numbers.items()}})
    if not (_target(opcode_rows(next(b for n,d,b in methods if n=="getRadius" and d==GETTERS["getRadius"])),1)==4
            and _target(opcode_rows(next(b for n,d,b in methods if n=="getRadius" and d==GETTERS["getRadius"])),3)==9
            and _target(opcode_rows(next(b for n,d,b in methods if n=="getWitherAmplifier" and d==GETTERS["getWitherAmplifier"])),2)==5
            and _target(opcode_rows(next(b for n,d,b in methods if n=="getWitherAmplifier" and d==GETTERS["getWitherAmplifier"])),4)==6):
        return fail("null_power_or_amp_jump_drift")
    return {
       "status":"PROVED_SOMAKE_FUNERAL_NATIVE_GETTER_FORMULAS_AND_CAST_TO_CONTROLLER",
       "on_cast_instructions":81,"controller_ctor_index":51,
       "spell_getters_in_order":[x[0] for x in calls.values()],
       "radius":"clamp_f32(9.5f+float32(level)*0.82f+max_f32(0,schoolPower(caster_or_1)-1)*0.65f,10f,15f)",
       "duration":"240+20*(clamp_int(level,1,5)-1)",
       "wave_interval":"18-clamp_int(level,1,5)",
       "telegraph_ticks":"max_int(9,13-trunc_div_int(level,2))",
       "max_targets":"4+clamp_int(level,1,5)",
       "impact_damage":"1.5f+getSpellPower(level,caster)*0.75f",
       "wither_duration":"60+12*clamp_int(level,1,5)",
       "wither_amplifier":"1_if_level_ge_5_else_0",
       "controller_spawn":"setPos(groundPosition(rayCast_location))_then_addFreshEntity_boolean_discarded",
       "getter_details":getter_details,
       "boundary":"Native getter inputs/cast path only; no effective gameplay damage/Wither, successful world spawn, caster perks or hook mutator approved"
    }

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
    spell_methods=disasm(spell)
    result=spell_scout(spell_methods)
    proof=certify_spell_cast_getters_109(spell_methods)
    print("SOMAKE_FUNERAL_CAST_GETTER_GATE_PROOF",json.dumps(proof,sort_keys=True))
    if proof["status"]!="PROVED_SOMAKE_FUNERAL_NATIVE_GETTER_FORMULAS_AND_CAST_TO_CONTROLLER":
        raise GateError("native spell getter/cast argument gate: "+proof.get("reason","unknown"))
    getter_result=getter_scout(spell_methods)
    print("SOMAKE_FUNERAL_GETTER_SCOUT",json.dumps(getter_result,sort_keys=True))
    if getter_result["status"]!="OBSERVED_8_EXACT_GETTER_BODIES_TYPED_ONLY":
        raise GateError("native getter corpus ambiguous")
    if result["status"]!="OBSERVED_CONTROLLER_CAST_HANDBACK_OPERANDS_ONLY":
        raise GateError("spell controller handoff remains not proved:"+result.get("reason","unknown"))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:raise GateError("publisher artifact changed")
    return {"mod_id":"somakespells","version":"1.0.9","sha1":digest,
            "spell_compiled_class":spell,"spell_constructor_scout":result,"native_getter_scout":getter_result,"cast_getter_gate":proof}
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
