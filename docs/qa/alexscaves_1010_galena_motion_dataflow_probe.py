#!/usr/bin/env python3
"""Bounded normal-edge reaching-definition audit for MagneticWeaponEntity.tick."""
from __future__ import annotations
import argparse
import json
import re
from collections import deque
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_movement_probe import OWNER, PIN, METHODS, window
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs
from alexscaves_1010_nuclear_explosion_effect_probe import numeric

TICK_CODE = "eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699"
LIMITS = {"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
          "mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"effective_motion":"NOT_VERIFIED",
          "branch_feasibility":"NOT_PROVEN"}

def local_write(op, operand):
    if op in {"iinc","iinc_w"}:
        return {int(operand.split(",")[0].strip())}
    match=re.fullmatch(r"([ailfd])store(?:_(\d+)|_w)?",op)
    if not match:
        return set()
    slot=int(match[2] if match[2] is not None else operand.strip())
    return {slot,slot+1} if match[1] in {"l","d"} else {slot}

def successors(body):
    offsets=sorted(body)
    edges={}
    for i,at in enumerate(offsets):
        op,arg,_=body[at]
        following=offsets[i+1:i+2]
        require(op not in {"tableswitch","lookupswitch","jsr","jsr_w","ret","ret_w"},
                "unsupported control flow "+op)
        if op.startswith("if"):
            require(bool(following),"conditional at method end")
            targets=[int(arg),*following]
        elif op in {"goto","goto_w"}:
            targets=[int(arg)]
        elif op.endswith("return") or op=="athrow":
            targets=[]
        else:
            require(bool(following),"fallthrough beyond method")
            targets=following
        require(all(t in body for t in targets),"invalid CFG target")
        edges[at]=sorted(set(targets))
    return edges

def reaching(body,slot):
    edges=successors(body)
    start=min(body)
    incoming={start:{-1}}
    work=deque([start])
    while work:
        at=work.popleft()
        out={at} if slot in local_write(*body[at][:2]) else incoming[at]
        for dest in edges[at]:
            prior=incoming.get(dest,set())
            merged=prior|out
            if merged!=prior:
                incoming[dest]=merged
                work.append(dest)
    return incoming,edges

def self_test():
    # Two mutually exclusive branches define different values at the join.
    b={0:("ifeq","4",""),1:("fstore","6",""),2:("goto","5",""),
       4:("fstore","6",""),5:("fload","6",""),6:("return","","")}
    require(reaching(b,6)[0][5]=={1,4},"branch union")
    # An intervening write kills both prior definitions.
    b[5]=("fstore","6","")
    require(reaching(b,6)[0][6]=={5},"definition kill")
    # Double/long stores overwrite two local slots; dead code contributes none.
    b={0:("goto","3",""),1:("fstore","6",""),2:("goto","4",""),
       3:("dstore","5",""),4:("return","","")}
    require(reaching(b,6)[0][4]=={3} and 1 not in reaching(b,6)[0],"wide overwrite and dead code")
    b={0:("fstore","6",""),1:("ifeq","4",""),2:("fstore","6",""),
       3:("goto","1",""),4:("return","","")}
    require(reaching(b,6)[0][4]=={0,2},"loop fixed point")
    require(local_write("iinc","6, 1")=={6} and local_write("astore_2","")=={2},"local operand forms")
    print("PASS: five reaching-definition and operand checks")

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        require(len(z.namelist())==len(set(z.namelist())),"duplicate publisher entries")
        raw=z.read(OWNER+".class")
        rd=ClassReader(raw)
        require(rd.name==OWNER and rd.major==65 and digest(raw)==PIN[OWNER],"class pin")
        d=next(x for x in rd.methods if (x["name"],x["descriptor"])==("tick","()V"))
        require(d["code_sha256"]==TICK_CODE and not d["exception_handlers"],"Code/exception table pin")
        body=disassemble(jar,javap,OWNER)[("tick","()V")]
        count,sha=METHODS["tick"]
        require(len(body)==count and summarize(rd,("tick","()V"),body)["instruction_sha256"]==sha,"instruction pin")
        require(body[1547][:2]==("aload","5") and body[1549][:2]==("fload","6"),"final local reads")
        require(refs(rd,{1551:body[1551]})[0]["name"]=="directMovementTowards","final call")
        offsets=sorted(body)
        data={}
        for slot,read in ((5,1547),(6,1549)):
            incoming,edges=reaching(body,slot)
            defs=[]
            require(read in incoming and -1 not in incoming[read],"uninitialized final slot")
            for at in offsets:
                if slot not in local_write(*body[at][:2]):
                    continue
                local=window(offsets,at,24,6)
                sub={i:body[i] for i in local}
                defs.append({"offset":at,"opcode":body[at][0],"operand":body[at][1],
                             "reachable":at in incoming,"reaches_final_read":at in incoming[read],
                             "typed_members":refs(rd,sub),
                             "window":[{"offset":i,"opcode":body[i][0],
                                         "operand":body[i][1] if numeric(body[i][0],body[i][2]) or
                                         body[i][0].startswith(("aload","astore","fload","fstore","iload","istore","dload","dstore","if","goto")) else "",
                                         "numeric_symbol":body[i][2] if numeric(body[i][0],body[i][2]) else ""} for i in local]})
            require(0<len(defs)<=32,"slot write budget")
            data[str(slot)]={"final_read_offset":read,"reaching_definitions":sorted(incoming[read]),
                            "definitions":defs}
        branches=[{"offset":i,"opcode":body[i][0],"successors":edges[i]} for i in offsets
                  if body[i][0].startswith(("if","goto"))]
    return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
            "class_sha256":PIN[OWNER],"code_sha256":TICK_CODE,"instruction_sha256":sha,
            "instructions":count,"normal_edge_branch_sites":branches,
            "final_call_offset":1551,"slots":data,"limits":LIMITS}

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
        require(a.jar and a.output and not a.output.exists(),"write-once report")
        result=inspect(a.jar,a.javap)
        raw=canonical(result).encode()
        require(len(raw)<=1_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:
            f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for slot,row in result["slots"].items():
            print("SLOT",slot,json.dumps(row,sort_keys=True))
        print("BRANCHES",json.dumps(result["normal_edge_branch_sites"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
