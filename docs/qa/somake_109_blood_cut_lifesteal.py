#!/usr/bin/env python3
"""Somake Blood Cut exact 1.0.9: lifesteal setup callsite metadata gate.

Clean-room output only: no JVM method body, publisher code, JAR or classfile.
A call to a setter is not proof of an applied heal or a per-player mutation API.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_radius_irons_contract import sections, opcode_rows
from somake_109_blood_cut_refs import inspect as verify_classes

SPELL_CLASS="com.somake.somakespells.spells.blood.BloodCutSpell"
SETTING="SpellDamageSource.setLifestealPercent:"
DEFAULT_SOURCE="AbstractSpell.getDamageSource:"

def survey(rows: list[tuple[int,str,str,str]]) -> dict:
    if not 4 <= len(rows) <= 140:
        raise GateError("unexpected Blood Cut getDamageSource budget")
    offsets=[r[0] for r in rows]
    if offsets!=sorted(set(offsets)):
        raise GateError("invalid JVM instruction order")
    setter=[(i,c) for i,(_,op,_,c) in enumerate(rows)
            if op.startswith("invoke") and SETTING in c]
    source=[i for i,(_,op,_,c) in enumerate(rows)
            if op.startswith("invoke") and DEFAULT_SOURCE in c]
    if len(setter)!=1 or len(source)!=1:
        raise GateError("missing or ambiguous native damage-source/lifesteal callsite")
    setter_i,setter_ref=setter[0]
    if setter_i<=source[0]:
        raise GateError("setter must follow canonical damage source")
    if not re.search(r"setLifestealPercent:\(F\)",setter_ref):
        raise GateError("lifesteal setter typed float descriptor drift")
    if rows[-1][1]!="areturn":
        raise GateError("damage source expected to return object")
    numbers=[]
    for index,(pc,op,operand,comment) in enumerate(rows):
        if op in ("bipush","sipush") and re.fullmatch(r"-?\d+",operand):
            numbers.append({"kind":"int","index":index,"value":int(operand)})
        elif re.fullmatch(r"fconst_[0-2]",op):
            numbers.append({"kind":"float","index":index,"value":float(op[-1])})
        elif op.startswith("ldc"):
            m=re.search(r"\bfloat\s+(-?\d+(?:\.\d+)?)(?:f)?\b",comment)
            if m:
                numbers.append({"kind":"float","index":index,"value":float(m.group(1))})
    prev=rows[setter_i-1][1]
    strict_float=None
    if len(rows)==7:
        # Strict native-release fingerprint. The ldc directly before the setter
        # leaves a float literal on top of the JVM operand stack.
        if (source[0]!=3 or setter_i!=5 or prev!="ldc"
            or any(op.startswith(("if","goto")) for _,op,_,_ in rows)):
            raise GateError("native Blood Cut lifesteal operand topology drift")
        match=re.fullmatch(r"float 0\.15f",rows[setter_i-1][3])
        if not match:
            raise GateError("native Blood Cut 0.15f setter operand drift")
        strict_float=0.15
    return {
        "instruction_count":len(rows),
        "base_source_call_index":source[0],
        "lifesteal_setter_call_index":setter_i,
        "setter_typed_float_argument":True,
        "return_opcode":rows[-1][1],
        "immediate_argument_producer_opcode":prev,
        "certified_lifesteal_float_argument":strict_float,
        "literal_adjacent_to_setter":strict_float is not None,
        "float_numeric_literals":numbers[:15],
        "boundary":"Numbers and immediate opcodes are static callsite evidence, not the source's effective float operand or a healing result.",
    }

def inspect(jar:Path)->dict:
    jar=Path(jar)
    prior=verify_classes(jar)
    if prior["sha1"]!=SHA1 or jar.name!=FILENAME:
        raise GateError("wrong exact physical provider")
    p=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),SPELL_CLASS],
                     capture_output=True,text=True,timeout=40,check=False)
    if p.returncode or not 100 < len(p.stdout) < 1_500_000:
        raise GateError("could not examine native spell class")
    matches=[(d,opcode_rows(body)) for n,d,body in sections(p.stdout) if n=="getDamageSource"]
    if len(matches)!=1:
        raise GateError("missing/ambiguous getDamageSource method")
    descriptor,rows=matches[0]
    if not descriptor.startswith("(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/Entity;)"):
        raise GateError("getDamageSource method arguments changed")
    if not descriptor.endswith("SpellDamageSource;"):
        raise GateError("native damage source return descriptor changed")
    data=survey(rows)
    if data["certified_lifesteal_float_argument"]!=0.15:
        raise GateError("getDamageSource native exact 0.15f argument gate not certified")
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError("provider mutated during inspection")
    return {
        "status":"PASS_SHA_EXACT_BLOOD_CUT_LIFESTEAL_SETTER_TOPOLOGY",
        "provider":"somakespells","version":"1.0.9","sha1":SHA1,
        "spell_id":"somakespells:blood_cut","spell_class":SPELL_CLASS,
        "get_damage_source_descriptor":descriptor,"setter":data,
        "scope":"Native 0.15f setter float argument certified via adjacent ldc, not actual healing outcome or per-caster mutator hook."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    data=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("BLOOD_CUT_LIFESTEAL",data["status"],data["sha1"])
    print("LIFESTEAL_TOPOLOGY",json.dumps(data["setter"],sort_keys=True))
if __name__=="__main__":
    main()
