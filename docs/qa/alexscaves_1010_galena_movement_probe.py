#!/usr/bin/env python3
"""Read-only Galena movement and registration projection, no runtime execution."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs
from alexscaves_1010_nuclear_explosion_effect_probe import numeric
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P = "com/github/alexmodguy/alexscaves/server/"
OWNER = P+"entity/item/MagneticWeaponEntity"
REG = P+"entity/ACEntityRegistry"
PIN = {
    OWNER: "a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071",
    REG: "7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072",
}
METHODS = {
    "directMovementTowards": (68, "2fe8f43c0e6a95bcca0297681830a315dded40b7003a46587e3681692a74ef04"),
    "getControllerHandPos": (59, "bdb7b25bdcbcf0f25722e10d23a95dff5475b928bbc3848e6b72a3ed6f524b07"),
    "getReturnProgress": (11, "02075318d60a3308f162b572846186f66aedb832a6c05423006b02620bab856b"),
    "getStrikeProgress": (11, "da0516824a0780e9bf984df062e2667d8d475b3b8f97d88fca5fc2d5fe4b7eba"),
    "isIdling": (7, "1208b41ebe7cf954271681ed59918a48344dfb4507181b98d53e4a2d965ed561"),
    "<init>": (23, "a2ed23d6da65e74725d089cbe4a67808b3ebabf363c32562f17c23efc562f66c"),
    "tick": (744, "3478b6038fe3dad88fd11a2b7aeca49fc85a9ccadc1ad4e9fca089b423b8e9bc"),
}
LIMITS = {"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "physical_qa":"NOT_TESTED","mutating_hook":"NOT_VERIFIED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "effective_motion":"NOT_VERIFIED","effective_collision":"NOT_VERIFIED"}

def window(offsets, at, before=24, after=3):
    require(at in offsets and 0<=before<=32 and 0<=after<=8,"invalid window")
    i=offsets.index(at)
    return offsets[max(0,i-before):i+after+1]

def inspect(jar, javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        require(len(z.namelist())==len(set(z.namelist())),"duplicate publisher entries")
        readers={}
        bodies={}
        for owner,sha in PIN.items():
            raw=z.read(owner+".class")
            rd=ClassReader(raw)
            require(digest(raw)==sha and rd.name==owner and rd.major==65,"class identity")
            readers[owner]=rd
            bodies[owner]=disassemble(jar,javap,owner)
        rd=readers[OWNER]
        out={}
        for name,(count,sha) in METHODS.items():
            ds=[d for d in rd.methods if d["name"]==name and "code_sha256" in d]
            require(len(ds)==1,"method declaration not unique "+name)
            decl=ds[0]; key=(name,decl["descriptor"]); body=bodies[OWNER][key]
            prior=summarize(rd,key,body)
            require(len(body)==count and prior["instruction_sha256"]==sha,"prior instruction identity "+name)
            if name!="tick":
                out[name]=projection(rd,key,body,decl)
                out[name]["opcode_offsets"]=[{"offset":at,"opcode":op,"local_or_constant":arg if numeric(op,sym) or op.startswith(("aload","astore","fload","fstore","dload","dstore","iload","istore")) else ""}
                    for at,(op,arg,sym) in sorted(body.items())]
                continue
            # Tick has a larger roster; select only windows around movement
            # calls, not an incomplete projection labeled as full-body coverage.
            sites=[]
            for at,(op,arg,sym) in sorted(body.items()):
                if op not in {"invokevirtual","invokespecial","invokestatic","invokeinterface"}:
                    continue
                single=refs(rd,{at:body[at]})[0]
                if single["name"] not in {"directMovementTowards","getControllerHandPos","setDeltaMovement","move"}:
                    continue
                offsets=window(sorted(body),at)
                sub={p:body[p] for p in offsets}
                sites.append({"call":single,"typed_members":refs(rd,sub),
                    "opcodes":[{"offset":p,"opcode":body[p][0],"operand":body[p][1] if numeric(body[p][0],body[p][2]) or body[p][0].startswith(("aload","astore","fload","fstore","dload","dstore","iload","istore","if","goto")) else "",
                    "numeric_symbol":body[p][2] if numeric(body[p][0],body[p][2]) else ""} for p in offsets]})
            require(any(s["call"]["name"]=="directMovementTowards" for s in sites) and len(sites)<=32,"movement call roster")
            out[name]={"descriptor":key[1],"code_sha256":decl["code_sha256"],
                       "instruction_sha256":sha,"instruction_count":count,
                       "projection":"MOVEMENT_WINDOWS_ONLY","sites":sites}
        reg=registry(z,jar,javap,REG,{OWNER})
        require(reg["class_sha256"]==PIN[REG] and reg["bootstrap_links"],"registration linkage absent")
        regmethods=[]
        rr=readers[REG]
        for x in reg["nested_factories"]:
            key=(x["method"],x["descriptor"])
            decl=next(d for d in rr.methods if (d["name"],d["descriptor"])==key)
            regmethods.append(projection(rr,key,bodies[REG][key],decl))
        require(bool(regmethods) and len(regmethods)<=8,"factory roster")
    return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
            "class_pins":PIN,"methods":out,"registration":reg,"factory_methods":regmethods,"limits":LIMITS}

def self_test():
    require(window([1,2,3],1)==[1,2,3],"left boundary")
    require(window([1,2,3],3,1,0)==[2,3],"right boundary")
    require(window([1,2,3],2,0,0)==[2],"single pivot")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","scope")
    print("PASS: four window and scope checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once exact report")
        report=inspect(a.jar,a.javap)
        raw=canonical(report).encode()
        require(len(raw)<=1_500_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as out:
            out.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for name,row in report["methods"].items():
            print("MOTION",json.dumps({"name":name,**row},sort_keys=True))
        print("REGISTRY",json.dumps(report["registration"],sort_keys=True))
        for row in report["factory_methods"]:
            print("FACTORY",json.dumps(row,sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
