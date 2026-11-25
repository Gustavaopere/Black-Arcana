#!/usr/bin/env python3
"""Read-only exact publisher controller separation; no runtime execution."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs

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
    print("PASS: four scope and typed-site checks")

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
            weapon[name]=projection(wr,key,body,d)
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
                field_names.update(m["name"] for m in refs(tr,bodies[TELETOR][k])
                                   if m["owner"]==TELETOR and m["opcode"] in {"getfield","putfield","getstatic","putstatic"})
        reverse=[]
        for k,body in sorted(bodies[TELETOR].items()):
            if not body: continue
            members=refs(tr,body)
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
                native.append({"executable":True,**projection(tr,k,bodies[TELETOR][k],d)})
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
