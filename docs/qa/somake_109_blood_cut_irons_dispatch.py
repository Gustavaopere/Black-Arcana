#!/usr/bin/env python3
"""SHA-exact Somake 1.0.9 Blood Cut / Iron's 3.16.3 overload evidence.

Clean-room: publish method identity, invocation descriptors and bounded opcode
census only. No JAR/classfile/method body/source code redistribution.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from somake_109_perk_method_probe import GateError, FILENAME, SHA1
from somake_109_radius_irons_contract import (
    IRON_API_FILENAME, IRON_API_SHA256, IRON_CLASS,
    validate_irons_api, sections, opcode_rows
)

CHILD="com.somake.somakespells.spells.blood.BloodCutSpell"
ENTITY="Lnet/minecraft/world/entity/Entity;"
SOURCE="Lio/redspace/ironsspellbooks/damage/SpellDamageSource;"
ONE="("+ENTITY+")"+SOURCE
TWO="("+ENTITY+ENTITY+")"+SOURCE


def survey_overload_family(base_methods,child_methods):
    def get_exact(methods,desc):
        found=[r for r in methods if r[0]=="getDamageSource" and r[1]==desc]
        if len(found)!=1:
            raise GateError("missing or ambiguous exact getDamageSource overload")
        rows=found[0][2]
        if not 2<=len(rows)<=140:
            raise GateError("unbounded or empty method")
        return rows
    parent=get_exact(base_methods,ONE)
    child=get_exact(child_methods,TWO)
    if parent[-1][1]!="areturn" or child[-1][1]!="areturn":
        raise GateError("source overload return opcode changed")
    def calls(rows):
        output=[]
        for i,(_,op,arg,comment) in enumerate(rows):
            if not op.startswith("invoke") or "getDamageSource:" not in comment:
                continue
            match=re.search(r"getDamageSource:(\([^)]*\)[A-Za-z0-9_/$;\[]+)",comment)
            if not match:raise GateError("untyped getDamageSource invocation")
            output.append({"index":i,"opcode":op,"descriptor":match.group(1),
                           "self_or_super_reference":"AbstractSpell" in comment or
                           comment.startswith("Method getDamageSource:")})
        return output
    calls_parent=calls(parent)
    calls_child=calls(child)
    return {
        "assurance":"OVERLOAD_DECLARATIONS_ONLY",
        "base_one_entity_descriptor":ONE,
        "child_two_entity_descriptor":TWO,
        "base_one_arg_instruction_count":len(parent),
        "child_two_arg_instruction_count":len(child),
        "base_one_arg_getDamageSource_calls":calls_parent,
        "child_two_arg_getDamageSource_calls":calls_child,
        "base_one_arg_invocation_opcodes":[op for _,op,_,_ in parent if op.startswith("invoke")][:30],
        "child_two_arg_invocation_opcodes":[op for _,op,_,_ in child if op.startswith("invoke")][:30],
        "base_one_arg_return_count":sum(op=="areturn" for _,op,_,_ in parent),
        "child_two_arg_return_count":sum(op=="areturn" for _,op,_,_ in child),
        "boundary":"Method declarations and typed callsite references only; virtual dispatch, healing and game-event results need separate gates."
    }


def certify_virtual_lifesteal_bridge(base_methods,child_methods):
    """Strict native JVM five-op parent dispatch and seven-op Somake override."""
    parent=[r[2] for r in base_methods if r[0]=="getDamageSource" and r[1]==ONE]
    child=[r[2] for r in child_methods if r[0]=="getDamageSource" and r[1]==TWO]
    if len(parent)!=1 or len(child)!=1:
        raise GateError("missing or ambiguous source overload pair")
    base=parent[0];over=child[0]
    if [op for _,op,_,_ in base]!=["aload_0","aload_1","aload_1",
                                    "invokevirtual","areturn"]:
        raise GateError("parent one-arg virtual forwarding opcode drift")
    if [op for _,op,_,_ in over]!=["aload_0","aload_1","aload_2",
                                    "invokespecial","ldc","invokevirtual","areturn"]:
        raise GateError("Blood Cut two-arg source/setter opcode drift")
    if ("getDamageSource:"+TWO not in base[3][3] or
            "getDamageSource:"+TWO not in over[3][3] or
            "AbstractSpell" not in over[3][3]):
        raise GateError("parent virtual and child super dispatch descriptor mismatch")
    if not re.fullmatch(r"float 0\.15f",over[4][3]):
        raise GateError("Blood Cut direct 0.15f setter operand drift")
    if ("SpellDamageSource.setLifestealPercent:(F)" not in over[5][3]
            or not over[5][3].startswith("Method ")):
        raise GateError("native setter method descriptor changed")
    return {
        "assurance":"SHA_EXACT_VIRTUAL_DISPATCH_WITH_015F_SETTER",
        "base_dispatch_opcode":"invokevirtual",
        "base_receiver_operand":"aload_0",
        "forwarded_second_entity_operand":"aload_1",
        "forwarded_first_entity_operand":"aload_1",
        "base_virtual_call_descriptor":TWO,
        "child_super_call_opcode":"invokespecial",
        "child_super_call_descriptor":TWO,
        "lifesteal_setter_argument":0.15,
        "setter_argument_type":"float",
        "setter_invocation_opcode":"invokevirtual",
        "child_return_opcode":"areturn",
        "interpretation":"On a BloodCutSpell receiver, the inherited 1-Entity method invokes the 2-Entity override with the same Entity in both argument positions; that override passes 0.15f to the SpellDamageSource lifesteal setter.",
        "limits":"Compiled virtual dispatch + nominal setter parameter only. Actual damage, heal percent of applied damage, caps, player owner and runtime execution are not certified."
    }


def javap(jar,cls):
    q=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),cls],
         capture_output=True,text=True,timeout=50,check=False)
    if q.returncode or not 100<len(q.stdout)<1_500_000:
        raise GateError("exact class javap unavailable")
    return q.stdout


def inspect(somake,irons):
    somake=Path(somake);irons=Path(irons)
    if somake.is_symlink() or not somake.is_file() or somake.name!=FILENAME:
        raise GateError("invalid Somake jar")
    if hashlib.sha1(somake.read_bytes()).hexdigest()!=SHA1:
        raise GateError("Somake SHA-1 mismatch")
    digest=validate_irons_api(irons)
    if digest!=IRON_API_SHA256:raise GateError("Iron's API SHA-256 mismatch")
    raw_parent=javap(irons,IRON_CLASS)
    raw_child=javap(somake,CHILD)
    parent=[(name,desc,opcode_rows(body)) for name,desc,body in sections(raw_parent) if name=="getDamageSource"]
    child=[(name,desc,opcode_rows(body)) for name,desc,body in sections(raw_child) if name=="getDamageSource"]
    result=survey_overload_family(parent,child)
    print("BLOOD_CUT_BASE_OPCODE_FINGERPRINT", [op for _,op,_,_ in parent[0][2]])
    print("BLOOD_CUT_CHILD_OPCODE_FINGERPRINT", [op for _,op,_,_ in child[0][2]])
    bridge=certify_virtual_lifesteal_bridge(parent,child)
    # Ensure the physical class's ancestry mentions the actual host class.
    header=" ".join(raw_child.splitlines()[:8])
    if "extends io.redspace.ironsspellbooks.api.spells.AbstractSpell" not in header:
        raise GateError("Somake spell superclass differs from host")
    if hashlib.sha1(somake.read_bytes()).hexdigest()!=SHA1 or hashlib.sha256(irons.read_bytes()).hexdigest()!=digest:
        raise GateError("binary modified during analysis")
    return {"status":"PASS_SHA_EXACT_SOMAKE_IRONS_VIRTUAL_LIFESTEAL_BRIDGE",
        "somake_sha1":SHA1,"irons_api_sha256":digest,
        "somake_version":"1.0.9","irons_version":"1.21.1-3.16.3",
        "base_class":IRON_CLASS,"child_class":CHILD,
        "class_ancestry":"direct AbstractSpell superclass proven",
        "overloads":result,
        "native_virtual_dispatch_and_setter":bridge,
        "limit":"No physical gameplay, applied healing or per-caster mutator certified."}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--somake",required=True,type=Path)
    p.add_argument("--irons-api",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    data=inspect(a.somake,a.irons_api)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("BLOOD_CUT_OVERLOAD",data["status"],data["somake_sha1"],data["irons_api_sha256"])
    print("BLOOD_CUT_OVERLOAD_METHODS",json.dumps(data["overloads"],sort_keys=True))
    print("BLOOD_CUT_VIRTUAL_LIFESTEAL",json.dumps(data["native_virtual_dispatch_and_setter"],sort_keys=True))
if __name__=="__main__":
    main()
