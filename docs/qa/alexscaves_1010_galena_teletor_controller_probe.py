#!/usr/bin/env python3
"""Read-only exact publisher controller separation; no runtime execution."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs, SELECT_OPS
from alexscaves_1010_galena_motion_dataflow_probe import successors
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, bootstrap, MATH

P = "com/github/alexmodguy/alexscaves/server/entity/"
WEAPON = P + "item/MagneticWeaponEntity"
TELETOR = P + "living/TeletorEntity"
PIN = "a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071"
TICK = "eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699"
METHODS = {
    "tick": (744, "3478b6038fe3dad88fd11a2b7aeca49fc85a9ccadc1ad4e9fca089b423b8e9bc"),
    "getController": (34, "0b547d0cef5e0afa81b6dfbdb7f6215da923e21abc49ddb9a6be8cbc4d3199e2"),
    "getControllerUUID": (9, "fa91dcd8ea98ce6e8c942e529c1a254848e801d3e415ac78253d332227b81ad7"),
    "setControllerUUID": (7, "d14d79b5d9ecaee766923df03e2a29df3f489a75e771bace60ee9dc6857ba91a"),
}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutation":"NO_MUTATION",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "actual_owner_resolution":"NOT_VERIFIED","effective_combat":"NOT_VERIFIED"}

def bounded_refs(reader,body):
    require(len(body)<=1600,"method budget")
    offsets=sorted(body)
    result=[]
    for start in range(0,len(offsets),120):
        part=offsets[start:start+120]
        result.extend(refs(reader,{at:body[at] for at in part}))
    expected=[at for at in offsets if body[at][0] in SELECT_OPS]
    require([row["offset"] for row in result]==expected,"partitioned member coverage drift")
    return result

def project_method(reader,key,body,decl):
    members=bounded_refs(reader,body)
    if len(members)<=180:
        row=projection(reader,key,body,decl)
        require(row["typed_members"]==members,"projection census drift")
        return row
    # Do not truncate the method or relax the shared 180-member bound.
    # Resolve each partition using the existing strict CP decoder, then
    # reconstruct the complete normal-edge CFG over original instructions.
    require(not decl.get("exception_handlers",[]),"wide method exception CFG unsupported")
    edges=successors(body)
    offsets=sorted(body)
    branches=[]
    for i,at in enumerate(offsets):
        op,arg,sym=body[at]
        if not op.startswith(("if","goto")):
            continue
        prior=offsets[max(0,i-5):i]
        branches.append({"offset":at,"opcode":op,"target":int(arg),
                         "successors":edges[at],"prelude_offsets":prior,
                         "prelude_opcodes":[body[p][0] for p in prior]})
    require(len(branches)<=90,"wide branch budget")
    type_operands=[]
    for at,(op,arg,_) in sorted(body.items()):
        if op not in {"new","checkcast","instanceof","anewarray","multianewarray"}:
            continue
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        require(match is not None and reader.pool[int(match[1])][0]==7,"unresolved type operand")
        type_operands.append({"offset":at,"opcode":op,"owner":reader.resolve(int(match[1]))})
    return {"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
            "code_bytes":decl["code_size"],"instruction_count":len(body),
            "instruction_sha256":summarize(reader,key,body)["instruction_sha256"],
            "projection":"FULL_NORMAL_CFG_PARTITIONED_TYPED_MEMBERS",
            "partition_instruction_budget":120,
            "typed_members":members,"branches":branches,
            "exception_handler_count":0,
            "terminals":[{"offset":at,"opcode":body[at][0]} for at in offsets if not edges[at]],
            "numeric_operands":[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
                                for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)],
            "arithmetic":[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH],
            "strings":[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if sym.startswith("String ")],
            "local_accesses":[{"offset":at,"opcode":op,"operand":arg}
                              for at,(op,arg,_) in sorted(body.items())
                              if op.startswith(("aload","astore","iload","istore","fload","fstore","dload","dstore","lload","lstore")) or op=="iinc"],
            "bootstrap_links":bootstrap(reader,body),"type_operands":type_operands}

def select_sites(members, owner):
    return [m for m in members if m["owner"] == owner and
            m["opcode"] in {"invokevirtual","invokespecial","invokestatic","invokeinterface"}]

def self_test():
    a={"owner":TELETOR,"opcode":"invokevirtual","name":"getTarget","descriptor":"()V"}
    b={**a,"owner":WEAPON}; c={**a,"opcode":"getfield"}
    require(select_sites([a,b,c],TELETOR)==[a],"owner and opcode filter")
    require(select_sites([a,b,c],WEAPON)==[b],"separate weapon calls")
    require(select_sites([],TELETOR)==[],"empty input")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    class FixtureReader:
        pool=[None,(10,)]
        def resolve(self,index):
            require(index==1,"fixture index")
            return (10,"fixture/Owner",(12,"call","()V"))
    body={i*3:("invokevirtual","#1","") for i in range(181)}
    body[544]=("return","","")
    result=bounded_refs(FixtureReader(),body)
    require([r["offset"] for r in result]==[i*3 for i in range(181)],"wide site roster")
    require(bounded_refs(FixtureReader(),{})==[],"empty member roster")
    bad=dict(body);bad[543]=("invokevirtual","#2","")
    try:
        bounded_refs(FixtureReader(),bad)
    except Exception as exc:
        require("invalid JVM ref index" in str(exc),"wrong rejection")
    else:
        raise AssertionError("invalid member accepted")
    print("PASS: seven scope, typed-site and partition checks")

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate archive entry")
        readers={}; bodies={}; hashes={}
        for owner in (WEAPON,TELETOR):
            raw=z.read(owner+".class"); rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            readers[owner]=rd; hashes[owner]=digest(raw)
            bodies[owner]=disassemble(jar,javap,owner)
        require(hashes[WEAPON]==PIN,"weapon class drift")
        wr=readers[WEAPON]; weapon={}
        for name,(count,sha) in METHODS.items():
            ds=[d for d in wr.methods if d["name"]==name and "code_sha256" in d]
            require(len(ds)==1,"weapon declaration ambiguity "+name)
            d=ds[0]; key=(name,d["descriptor"]); body=bodies[WEAPON][key]
            require(len(body)==count and summarize(wr,key,body)["instruction_sha256"]==sha,"method identity "+name)
            if name=="tick":
                require(d["code_sha256"]==TICK and not d["exception_handlers"],"tick Code drift")
            weapon[name]=project_method(wr,key,body,d)
        sites=select_sites(weapon["tick"]["typed_members"],TELETOR)
        require({m["name"] for m in sites}>={"setWeaponUUID","getTarget","getWeaponPosition"},"expected typed Teletor calls missing")
        tr=readers[TELETOR]
        direct={(m["name"],m["descriptor"]) for m in sites}
        declarations={(d["name"],d["descriptor"]):d for d in tr.methods}
        require(len(declarations)==len(tr.methods),"ambiguous Teletor method")
        selected={k for k in direct if k in declarations}
        # Select native direct callers of weapon methods, plus methods accessing
        # fields named in the bodies of the directly referenced Teletor methods.
        field_names=set()
        for k in sorted(selected):
            if k in bodies[TELETOR]:
                field_names.update(m["name"] for m in bounded_refs(tr,bodies[TELETOR][k])
                                   if m["owner"]==TELETOR and m["opcode"] in {"getfield","putfield","getstatic","putstatic"})
        reverse=[]
        for k,body in sorted(bodies[TELETOR].items()):
            if not body: continue
            members=bounded_refs(tr,body)
            calls=select_sites(members,WEAPON)
            fields=[m for m in members if m["owner"]==TELETOR and m["name"] in field_names and m["opcode"] in {"getfield","putfield","getstatic","putstatic"}]
            if calls or fields:
                selected.add(k)
                reverse.append({"name":k[0],"descriptor":k[1],"weapon_calls":calls,"related_fields":fields})
        require(1<=len(selected)<=40,"Teletor selection budget")
        native=[]
        for k in sorted(selected):
            d=declarations[k]
            if "code_sha256" not in d:
                native.append({"name":k[0],"descriptor":k[1],"executable":False})
            else:
                require(k in bodies[TELETOR] and bodies[TELETOR][k],"selected body unavailable")
                native.append({"executable":True,**project_method(tr,k,bodies[TELETOR][k],d)})
        return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
                "class_hashes":hashes,"weapon_methods":weapon,"typed_teletor_calls":sites,
                "teletor_parent":tr.parent,"teletor_selected_fields":sorted(field_names),
                "direct_calls_without_local_declaration":[{"name":n,"descriptor":d} for n,d in sorted(direct-set(declarations))],
                "teletor_methods":native,"teletor_reverse_sites":reverse,"limits":LIMITS}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once report")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode()
        require(0<len(raw)<=2_500_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for k in ("class_hashes","typed_teletor_calls","teletor_parent","teletor_selected_fields","direct_calls_without_local_declaration","teletor_reverse_sites"):
            print(k.upper(),json.dumps(report[k],sort_keys=True))
        for owner,methods in ((WEAPON,report["weapon_methods"].values()),(TELETOR,report["teletor_methods"])):
            for m in methods:print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED")
