#!/usr/bin/env python3
"""Bounded read-only causal projection of publisher NuclearExplosionEntity.

Only symbolic members, control-flow pivots, numeric operands and config
declarations are recorded; no third-party implementation is copied.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze

PREFIX = "com/github/alexmodguy/alexscaves/server/"
OWNER = PREFIX + "entity/item/NuclearExplosionEntity"
OWNER_SHA = "d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912"
CONFIG = PREFIX + "config/ACServerConfig"
LIMITS = {
    "world_safety":"BLOCKED", "physical_qa":"NOT_TESTED",
    "static_contract":"NOT_CERTIFIED", "mutating_hook":"NOT_VERIFIED",
    "effective_config":"NOT_VERIFIED", "actual_damage":"NOT_VERIFIED",
    "actual_world_changes":"NOT_VERIFIED", "runtime_loaded_bytes":"NOT_OBSERVED",
    "mutation":"NO_MUTATION", "semantic_magic_roots_delta":0,
    "provider_universe_closed":False,
}
MEMBERS = {"invokevirtual","invokeinterface","invokespecial","invokestatic",
           "getfield","getstatic","putfield","putstatic"}
MATH = {"iadd","isub","imul","idiv","irem","ineg","ishl","ishr",
        "fadd","fsub","fmul","fdiv","frem","fneg","fcmpg","fcmpl",
        "dadd","dsub","dmul","ddiv","drem","dneg","dcmpg","dcmpl",
        "ladd","lsub","lmul","ldiv","lrem","lcmp","i2f","i2d","f2i",
        "f2d","d2i","d2f","i2l","l2i"}


def numeric(op, sym):
    return op.startswith(("iconst_","fconst_","dconst_","lconst_")) or op in {"bipush","sipush"} or (op.startswith("ldc") and sym.startswith(("int ","float ","double ","long ")))


def context(body, offset, before=8, after=2):
    offsets = sorted(body)
    i = offsets.index(offset)
    selected = []
    for at in offsets[max(0,i-before):i+after+1]:
        op, arg, sym = body[at]
        if op in MEMBERS or numeric(op,sym) or op in MATH or sym.startswith("String "):
            selected.append({"offset":at,"opcode":op,"operand":arg,"symbol":sym})
    return selected


def bootstrap(reader, body):
    result = []
    for at,(op,arg,_) in sorted(body.items()):
        if op != "invokedynamic":
            continue
        match = re.fullmatch(r"#(\d+)(?:\s*,\s*\d+)?",arg)
        require(match is not None,"unresolved bootstrap operand")
        tag,index,_ = reader.resolve(int(match.group(1)))
        require(tag == 18,"not invoke dynamic")
        args = reader.attributes["bootstrap_methods"][index]["arguments"]
        handles = []
        for a in args:
            ref = a.get("reference") if isinstance(a,dict) else None
            if isinstance(ref,list) and len(ref)==3 and ref[0] in (10,11):
                handles.append({"kind":a["reference_kind"],"owner":ref[1],
                                "name":ref[2][1],"descriptor":ref[2][2]})
        result.append({"offset":at,"bootstrap_index":index,"handles":handles})
    return result


def inspect(jar,javap,output):
    verify_artifact(jar)
    require(not output.exists(),"write-once report required")
    with ZipFile(jar) as z:
        require(len(z.namelist())==len(set(z.namelist())),"duplicate jar entries")
        raw=z.read(OWNER+".class")
        require(digest(raw)==OWNER_SHA,"exact explosion owner drift")
        reader=ClassReader(raw)
        require(reader.name==OWNER and reader.major==65,"owner identity drift")
        bodies=disassemble(jar,javap,OWNER)
        expected={(m["name"],m["descriptor"]) for m in reader.methods if "code_sha256" in m}
        require(0<len(expected)<=80 and expected=={k for k,v in bodies.items() if v},"executable census mismatch")
        methods=[]
        fields=set()
        for k in sorted(expected):
            body=bodies[k]
            d=next(m for m in reader.methods if (m["name"],m["descriptor"])==k)
            row=analyze(reader,body,d)
            row["instruction_sha256"]=summarize(reader,k,body)["instruction_sha256"]
            row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym} for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
            row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
            row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op.startswith("ldc") and sym.startswith("String ")]
            row["bootstrap_links"]=bootstrap(reader,body)
            row["effect_contexts"]=[{"call":v,"context":context(body,v["offset"])} for v in row["typed_members"] if any(cue in v["name"].lower() for cue in ("hurt","damage","effect","setblock","destroy","explode","push","aabb","inflate","getentities","setdelta","forcechunk","setsize","getsize","getdistance","distanceto","random","grief","resistance"))]
            for v in row["typed_members"]:
                if v["owner"]==CONFIG and v["opcode"]=="getfield":
                    fields.add(v["name"])
            methods.append(row)
        # Bomb upstream size modifier was independently observed in PR #1182.
        fields.add("nukeExplosionSizeModifier")
        config_raw=z.read(CONFIG+".class")
        config=ClassReader(config_raw)
        require(config.name==CONFIG and config.major==65,"config owner drift")
        found={f["name"] for f in config.fields}
        require(fields.issubset(found),"config field identity unresolved")
        cfg=[]
        for key,body in sorted(disassemble(jar,javap,CONFIG).items()):
            for at,(op,arg,sym) in sorted(body.items()):
                if op!="putfield":
                    continue
                match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                require(match is not None,"unresolved config field")
                tag,owner,sig=config.resolve(int(match.group(1)))
                if tag==9 and owner==CONFIG and sig[1] in fields:
                    cfg.append({"field":sig[1],"descriptor":sig[2],"method":key[0],"offset":at,"context":context(body,at,18,0)})
        require(fields=={x["field"] for x in cfg},"config writes not fully found")
    report={"schema_version":1,"scope":"NUCLEAR_EXPLOSION_PUBLISHER_EFFECT_DISCOVERY_ONLY",
            "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "owner":OWNER,"class_sha256":OWNER_SHA,"methods":methods,
            "config":{"owner":CONFIG,"class_sha256":digest(config_raw),"fields":sorted(fields),"writes":cfg},
            "limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=900000,"report budget")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("xb") as f:
        f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"METHODS",len(methods))
    print("CONFIG",json.dumps(report["config"],sort_keys=True))
    for row in methods:
        print("SEMANTIC",json.dumps(row,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")


def self_test():
    for op,sym,expected in (("iconst_0","",True),("ldc","float 2.0f",True),
                            ("ldc","String 2.0f",False),("invokevirtual","",False),
                            ("sipush","",True)):
        require(numeric(op,sym)==expected,"numeric projection mismatch")
    require(LIMITS["static_contract"]=="NOT_CERTIFIED","policy drift")
    print("PASS: five numeric projection cases")


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
        require(a.jar is not None and a.output is not None,"jar/output required")
        inspect(a.jar,a.javap,a.output)
