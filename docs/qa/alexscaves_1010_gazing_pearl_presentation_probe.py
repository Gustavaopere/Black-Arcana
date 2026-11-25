#!/usr/bin/env python3
"""Read-only publisher-exact Gazing Pearl acquisition and presentation links."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P="com/github/alexmodguy/alexscaves/"
ITEM=P+"server/item/GazingPearlItem"
REG=P+"server/item/ACItemRegistry"
CLIENT=P+"client/ClientProxy"
PIN="2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07"
ITEM_ID="alexscaves:gazing_pearl"
BANDS=("aggressive","stalking","neutral","helpful")
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
        "provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "effective_loot_and_trades":"NOT_VERIFIED","client_render":"NOT_TESTED",
        "loaded_translations":"NOT_VERIFIED"}

def hits(obj,targets,path=()):
    result=[]
    if isinstance(obj,str):
        if obj in targets:
            result.append({"path":list(path),"kind":"VALUE","token":obj})
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            result.extend(hits(v,targets,(*path,i)))
    elif isinstance(obj,dict):
        for k,v in sorted(obj.items()):
            if k in targets:
                result.append({"path":[*path,k],"kind":"KEY","token":k})
            result.extend(hits(v,targets,(*path,k)))
    return result

def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,"duplicate JSON key")
        out[key]=value
    return out

def read_resources(z,keys):
    paths=sorted(n for n in z.namelist() if n.startswith(("assets/","data/")) and n.endswith(".json"))
    require(len(paths)<=20000,"resource census budget")
    total=0; errors=[]; matches={}; languages={}
    for path in paths:
        raw=z.read(path);total+=len(raw)
        require(len(raw)<=4_000_000 and total<=100_000_000,"resource size budget")
        try: obj=json.loads(raw.decode("utf8"),object_pairs_hook=unique)
        except (UnicodeError,ValueError) as e:
            errors.append({"path":path,"reason":type(e).__name__});continue
        found=hits(obj,{ITEM_ID,"item.alexscaves.gazing_pearl",*keys})
        if found:
            require(len(found)<=200,"resource hit budget")
            row={"sha256":digest(raw),"bytes":len(raw),"hits":found}
            if path.startswith("data/") and len(raw)<=16000:
                # Ephemeral evidence for exact relevant declarative resources,
                # not runtime or an installed/effective registry snapshot.
                row["data_json"]=obj
            matches[path]=row
        if "/lang/" in path and isinstance(obj,dict):
            local={}
            for key in sorted({"item.alexscaves.gazing_pearl",*keys}):
                if key in obj:
                    require(isinstance(obj[key],str),"translation value type")
                    local[key]={"utf8_sha256":digest(obj[key].encode("utf8")),"characters":len(obj[key])}
            if local:languages[path]={"sha256":digest(raw),"keys":local}
    return {"paths_scanned":len(paths),"bytes_scanned":total,"parse_errors":errors,
            "matches":matches,"language_keys":languages}

def candidate_refs(rd):
    result={}
    for i,e in enumerate(rd.pool):
        if e is None:continue
        if e[0]==7 and rd.resolve(i)==ITEM:
            result[i]={"kind":"CLASS","owner":ITEM}
        elif e[0] in (9,10,11):
            tag,owner,sig=rd.resolve(i)
            if owner==ITEM or (tag==9 and owner==REG and sig[1]=="GAZING_PEARL"):
                result[i]={"kind":"MEMBER","tag":tag,"owner":owner,"name":sig[1],"descriptor":sig[2]}
    return result

def linked_methods(rd,bodies,candidates):
    direct={}; links={}
    for k,body in sorted(bodies.items()):
        sites=[]
        for at,(op,arg,_) in sorted(body.items()):
            cp=re.match(r"#(\d+)(?:\s|,|$)",arg)
            if cp and int(cp[1]) in candidates:
                sites.append({"offset":at,"opcode":op,"cp_index":int(cp[1]),**candidates[int(cp[1])]})
        handles=bootstrap(rd,body)
        for h in handles:
            for ref in h["handles"]:
                if ref["owner"]==ITEM:
                    sites.append({"offset":h["offset"],"opcode":"invokedynamic","kind":"BOOTSTRAP_HANDLE",**ref})
        if sites:direct[k]=sites
        links[k]=handles
    # Propagate only through explicitly observed local bootstrap handles,
    # not through generic call graphs or assumed runtime registration.
    selected=set(direct)
    for _ in range(len(bodies)+1):
        new=selected|{k for k,hs in links.items() if any(r["owner"]==rd.name and (r["name"],r["descriptor"]) in selected for h in hs for r in h["handles"])}
        if new==selected:break
        selected=new
    require(len(selected)<=70,"candidate methods budget")
    result=[]
    for k in sorted(selected):
        body=bodies[k]; offsets=sorted(body)
        sites=list(direct.get(k,[]))
        for h in links[k]:
            for ref in h["handles"]:
                if ref["owner"]==rd.name and (ref["name"],ref["descriptor"]) in selected:
                    sites.append({"offset":h["offset"],"opcode":"invokedynamic","kind":"LOCAL_BOOTSTRAP_HANDLE",**ref})
        require(1<=len(sites)<=100,"linked sites budget")
        decl=next(m for m in rd.methods if (m["name"],m["descriptor"])==k)
        row={"name":k[0],"descriptor":k[1],"code_sha256":decl["code_sha256"],
             "instruction_sha256":summarize(rd,k,body)["instruction_sha256"],
             "instruction_count":len(body),"sites":sites,"windows":[]}
        for at in sorted({x["offset"] for x in sites}):
            i=offsets.index(at); window=offsets[max(0,i-12):i+13]; sub={j:body[j] for j in window}
            row["windows"].append({"site":at,"typed_members":refs(rd,sub),
               "operands":[{"offset":j,"opcode":op,"operand":arg,"symbol":sym if numeric(op,sym) or sym.startswith("String ") else ""}
                           for j,(op,arg,sym) in sorted(sub.items())
                           if numeric(op,sym) or sym.startswith("String ") or op.startswith(("if","goto","aload","astore","iload","istore","ireturn","areturn"))]})
        if len(body)<=120:
            row["projection"]="FULL_SMALL_BODY"
            row["semantic"]=projection(rd,k,body,decl)
        else:row["projection"]="LINKED_WINDOWS_ONLY"
        result.append(row)
    return result

def tooltip(z,jar,javap):
    raw=z.read(ITEM+".class");rd=ClassReader(raw)
    require(rd.name==ITEM and rd.major==65 and digest(raw)==PIN,"item class pin")
    parsed=disassemble(jar,javap,ITEM)
    key=next(k for k in parsed if k[0]=="appendHoverText")
    body=parsed[key];d=next(x for x in rd.methods if (x["name"],x["descriptor"])==key)
    require(len(body)==38 and summarize(rd,key,body)["instruction_sha256"]=="41a8d00ebb184327784103f4fb98e9b14dc7949da9e6096d0e27a499340e9886","tooltip instruction pin")
    op,arg,_=body[48];require(op=="invokedynamic","tooltip concat site")
    cp=re.match(r"#(\d+)(?:\s|,|$)",arg);require(cp is not None,"concat index")
    tag,index,_=rd.resolve(int(cp[1]));require(tag==18,"concat tag")
    b=rd.attributes["bootstrap_methods"][index]
    templates=[x for x in b["arguments"] if isinstance(x,str) and x.count(chr(1))==1 and chr(2) not in x]
    require(len(templates)==1,"tooltip recipe unsupported")
    keys=[templates[0].replace(chr(1),band) for band in BANDS]
    return {"concat_offset":48,"bootstrap_index":index,"bootstrap":b,"keys":keys,
            "method":projection(rd,key,body,d)}

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist();roster=sorted(n for n in names if n.endswith(".class"))
        require(len(names)==len(set(names)) and len(roster)==1555,"publisher roster")
        owners={}
        for path in roster:
            raw=z.read(path);rd=ClassReader(raw)
            require(rd.name+".class"==path and rd.major==65,"class identity")
            cp=candidate_refs(rd)
            if cp:
                bodies=disassemble(jar,javap,rd.name)
                owners[rd.name]={"sha256":digest(raw),"cp_references":cp,
                    "methods":linked_methods(rd,bodies,cp)}
        require({ITEM,REG,CLIENT}<=set(owners) and len(owners)<=60,"consumer roster")
        t=tooltip(z,jar,javap)
        reg=registry(z,jar,javap,REG,{ITEM})
        require(reg["bootstrap_links"],"registry linkage absent")
        resource=read_resources(z,t["keys"])
    return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
            "class_entries_scanned":len(roster),"consumers":owners,"tooltip":t,
            "registration":reg,"resources":resource,"limits":LIMITS}

def self_test():
    x={"id":ITEM_ID,"nested":[{"name":ITEM_ID+"x"},{ITEM_ID:"other"}]}
    require(hits(x,{ITEM_ID})==[{"path":["id"],"kind":"VALUE","token":ITEM_ID},
              {"path":["nested",1,ITEM_ID],"kind":"KEY","token":ITEM_ID}],"exact decoded matches")
    require(hits("prefix"+ITEM_ID,{ITEM_ID})==[],"no substring matches")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","scope")
    print("PASS: three resource and scope checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--jar",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once report")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode()
        require(0<len(raw)<=2_500_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        print("TOOLTIP",json.dumps(report["tooltip"],sort_keys=True))
        print("REGISTRATION",json.dumps(report["registration"],sort_keys=True))
        print("RESOURCES",json.dumps(report["resources"],sort_keys=True))
        for owner,row in report["consumers"].items():
            print("OWNER",owner,row["sha256"])
            for m in row["methods"]:
                print("LINKED",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED")
