#!/usr/bin/env python3
"""Read-only exact resource acquisition, tag binding and registry argument audit."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, MATH, bootstrap

P="com/github/alexmodguy/alexscaves/server/"
REG=P+"entity/ACEntityRegistry"
FACTORY="lambda$static$43"
IDS={"alexscaves:holocoder","alexscaves:hot_chocolate_bottle","alexscaves:ink_bomb","alexscaves:glow_ink_bomb"}
TAG="gingerbread_man_steals"
TAG_FIELD="GINGERBREAD_MAN_STEALS"
PREFIX="data/alexscaves/"
LOOT={
    PREFIX+"loot_table/chests/licowitch_tower.json":(15,"alexscaves:hot_chocolate_bottle","0d9f0a4837eb424eab1be3e2a1e95acd760e2a9e26b8650b4e53d8507ef67f60"),
    PREFIX+"loot_table/gameplay/deep_one_barter.json":(12,"alexscaves:ink_bomb","eb208ca3660daed76aaf13dfeba2cdef15bbce90ae3d2c235ecb63a4480042ac"),
    PREFIX+"loot_table/gameplay/deep_one_knight_barter.json":(14,"alexscaves:ink_bomb","57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818"),
    PREFIX+"loot_table/gameplay/deep_one_mage_barter.json":(14,"alexscaves:glow_ink_bomb","18682ca468355f61eda02c903fdb9c0dfbda88094c5caf343b1ae5ef437c44eb"),
}
TAG_PATH=PREFIX+"tags/item/"+TAG+".json"
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "effective_loot_tags":"NOT_VERIFIED","runtime_loaded_bytes":"NOT_OBSERVED"}

def load(z,path,pin):
    raw=z.read(path)
    require(digest(raw)==pin and len(raw)<1000000,"resource identity "+path)
    return {"sha256":pin,"bytes":len(raw)},json.loads(raw.decode("utf8"))

def loot_projection(obj,index,item):
    require(isinstance(obj,dict) and isinstance(obj.get("pools"),list),"loot object")
    pool=obj["pools"][0]
    entries=pool["entries"]
    chosen=entries[index]
    require(chosen.get("name")==item,"exact item slot")
    # The declared weights are not effective probabilities: conditions,
    # luck/quality, functions and global modifiers may alter selection.
    return {"type":obj.get("type"),"pool_count":len(obj["pools"]),"pool_index":0,
            "rolls":pool.get("rolls"),"bonus_rolls":pool.get("bonus_rolls"),
            "pool_conditions":pool.get("conditions",[]),"pool_functions":pool.get("functions",[]),
            "table_functions":obj.get("functions",[]),"entry_index":index,
            "selected_entry":{k:chosen[k] for k in ("type","name","weight","quality","conditions","functions") if k in chosen},
            "pool_entry_weights":[{"index":i,"type":e.get("type"),"name":e.get("name"),
                "weight":e.get("weight"),"quality":e.get("quality"),"conditions_present":bool(e.get("conditions")),
                "nested_children":bool(e.get("children"))} for i,e in enumerate(entries)]}

def hit(rd,i):
    entry=rd.pool[i]
    if entry is None:return False
    if entry[0]==8:return rd.resolve(i) in {TAG,"alexscaves:"+TAG}
    if entry[0]!=9:return False
    tag,owner,sig=rd.resolve(i)
    return sig[1]==TAG_FIELD and owner.startswith(P)

def project(rd,key,body,decl):
    result=analyze(rd,body,decl)
    result["instruction_sha256"]=summarize(rd,key,body)["instruction_sha256"]
    result["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
        for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
    result["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
    result["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if sym.startswith("String ")]
    result["bootstrap_links"]=bootstrap(rd,body)
    return result

def inspect(jar,javap,output):
    verify_artifact(jar)
    require(not output.exists(),"write-once report")
    with ZipFile(jar) as z:
        paths=z.namelist()
        roster=sorted(n for n in paths if n.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"roster drift")
        resources={}
        for path,(index,item,pin) in sorted(LOOT.items()):
            identity,obj=load(z,path,pin)
            resources[path]={**identity,"projection":loot_projection(obj,index,item)}
        identity,obj=load(z,TAG_PATH,"59c2591008e62e6bb91011202fa7aa2200fd950f9da55d309dbf0bea243682f8")
        require(obj.get("values",[])[5]=="alexscaves:hot_chocolate_bottle","tag slot drift")
        resources[TAG_PATH]={**identity,"projection":{"replace":obj.get("replace"),"values":obj["values"]}}
        candidates={}
        for path in roster:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"owner identity")
            hits={i:rd.resolve(i) for i in range(1,len(rd.pool)) if hit(rd,i)}
            if hits:candidates[rd.name]=hits
        require(1<=len(candidates)<=30,"tag candidate budget")
        owners={}
        for owner,hits in sorted(candidates.items()):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            methods=[]
            for key,body in sorted(disassemble(jar,javap,owner).items()):
                offsets=sorted(body);sites=[]
                for at,(op,arg,sym) in sorted(body.items()):
                    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if match and int(match[1]) in hits:
                        i=offsets.index(at)
                        sites.append({"offset":at,"opcode":op,"constant":hits[int(match[1])],
                            "window":[{"offset":v,"opcode":body[v][0],"operand":body[v][1],"symbol":body[v][2]}
                                      for v in offsets[max(0,i-8):i+9]]})
                if not sites:continue
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                row={"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
                     "instruction_count":len(body),"sites":sites,"projection":"DIRECT_SITE_WINDOWS_ONLY"}
                if key[0]!="<clinit>" and len(body)<=450:
                    row["semantics"]=project(rd,key,body,decl);row["projection"]="FULL_BOUNDED_SEMANTICS"
                methods.append(row)
            owners[owner]={"class_sha256":digest(raw),"fields":rd.fields,"methods":methods}
        raw=z.read(REG+".class")
        require(digest(raw)=="7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072","registry drift")
        rd=ClassReader(raw);bodies=disassemble(jar,javap,REG)
        keys=[k for k in bodies if k[0]==FACTORY]
        require(len(keys)==1,"factory identity")
        key=keys[0];decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
        factory=project(rd,key,bodies[key],decl)
        require(factory["instruction_sha256"]=="ebf33e4001e4ec0b07ee29546558633e3a3be800512e1ad12a68ebfdf2c28d51","factory projection drift")
    report={"schema_version":1,"scope":"FOUR_ITEMS_ACQUISITION_TAG_AND_REGISTRY_DISCOVERY",
            "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},"class_roster":1555,
            "resources":resources,"tag_candidates":owners,"ink_entity_factory":factory,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=1500000,"report size budget")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("xb") as f:f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"TAG_OWNERS",len(owners))
    print("RESOURCE_PROJECTION",json.dumps(resources,sort_keys=True))
    for owner,row in owners.items():print("TAG_OWNER",owner,json.dumps(row,sort_keys=True))
    print("INK_ENTITY_FACTORY",json.dumps(factory,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION")

def self_test():
    sample={"pools":[{"entries":[{"name":"alexscaves:ink_bomb","weight":3,"conditions":[{"condition":"test"}]}]}]}
    require(loot_projection(sample,0,"alexscaves:ink_bomb")["selected_entry"]["weight"]==3,"weight projection")
    require(loot_projection(sample,0,"alexscaves:ink_bomb")["pool_entry_weights"][0]["conditions_present"],"conditions retained")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: projection and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None,"jar/output required")
        inspect(a.jar,a.javap,a.output)
