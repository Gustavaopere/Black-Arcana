#!/usr/bin/env python3
"""Bounded publisher capture, dispatch, representation and inventory bridge discovery."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze, SELECT_OPS
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, MATH, bootstrap
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P="com/github/alexmodguy/alexscaves/server/"
EVENT=P+"event/CommonEvents"
PLATFORM=P+"misc/ACPlatform"
COMPAT=P+"misc/ACCompat"
ACCESS=P+"misc/ACItemAccess"
BLOCK=P+"block/HologramProjectorBlock"
BE=P+"block/blockentity/HologramProjectorBlockEntity"
REG=P+"block/blockentity/ACBlockEntityRegistry"
ITEM=P+"item/HolocoderItem"
TARGETS={
    EVENT:{"acPlayerEntityInteract","playerEntityInteract","<init>"},
    PLATFORM:{"serializeEntity","entityItemHandler","setThrower"},
    COMPAT:{"markDisplayEntity","entityTypeFrom","getUUID","hasUUID","putUUID"},
    ACCESS:{"takeOne","size","stackInSlot"},
    BE:{"tick","getDisplayEntity","setEntity"},
}
SELECT={
    EVENT:{"acPlayerEntityInteract","playerEntityInteract","<init>"},
    PLATFORM:{"serializeEntity","entityItemHandler","setThrower"},
    COMPAT:{"markDisplayEntity","entityTypeFrom","getUUID","hasUUID","putUUID","getCompound","getTag","setTag","getOrCreateTag"},
    P+"entity/ai/GingerbreadManStealGoal":{"canStealFromEntityType","hasStealableInventory","stealOneFrom","canUse","canContinueToUse","tick","start","stop"},
    P+"entity/ai/GingerbreadManStoreStolenItemsGoal":{"canUse","canContinueToUse","tick","start","stop","getRandomArmor"},
}
ALL={BLOCK,ITEM,ACCESS}
PINS={
    EVENT:"d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43",
    COMPAT:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    PLATFORM:"662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6",
    BLOCK:"ec685ba2b8db000916105c2696f61372e7ee9f93893529bfe196c262dce465fe",
    BE:"5aaf4f2f96190d740a101f75c2603d2f3b1001a8c494eaa0594e6aebde308057",
    ITEM:"7d2697b694b97483ad592733fad8ad595de0fa0805de7a0396ac6cb4715dfd96",
}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "actual_dispatch_and_cancellation":"NOT_VERIFIED","actual_inventory_settlement":"NOT_VERIFIED",
        "runtime_loaded_bytes":"NOT_OBSERVED","effective_tags":"NOT_VERIFIED"}

class AnnotationReader(ClassReader):
    """Parse JVM annotation attributes only; never infer from pool strings."""
    def element(self,depth):
        require(depth<=12,"annotation recursion budget")
        tag=chr(self.number(1))
        if tag in "BCDFIJSZs":
            return {"tag":tag,"constant":self.resolve(self.number())}
        if tag=="e":
            return {"tag":tag,"type":self.resolve(self.number()),"constant":self.resolve(self.number())}
        if tag=="c":
            return {"tag":tag,"class":self.resolve(self.number())}
        if tag=="@":
            return {"tag":tag,"annotation":self.annotation(depth+1)}
        if tag=="[":
            n=self.number()
            require(n<=256,"annotation array budget")
            return {"tag":tag,"values":[self.element(depth+1) for _ in range(n)]}
        require(False,"unknown annotation element tag "+tag)

    def annotation(self,depth=0):
        require(depth<=12,"annotation recursion budget")
        desc=self.resolve(self.number())
        require(isinstance(desc,str) and desc.startswith("L") and desc.endswith(";"),"annotation descriptor")
        n=self.number()
        require(n<=128,"annotation pair budget")
        pairs={}
        for _ in range(n):
            name=self.resolve(self.number())
            require(name not in pairs,"duplicate annotation element")
            pairs[name]=self.element(depth+1)
        return {"descriptor":desc,"elements":pairs}

    def attrs(self):
        result={}
        for _ in range(self.number()):
            name,size=self.resolve(self.number()),self.number(4)
            end=self.pos+size
            require(end<=len(self.raw),"annotation attribute overrun")
            if name in ("RuntimeVisibleAnnotations","RuntimeInvisibleAnnotations"):
                require(name not in result,"duplicate annotations attribute")
                n=self.number()
                require(n<=128,"annotation count budget")
                result[name]=[self.annotation() for _ in range(n)]
                require(self.pos==end,"annotation attribute size mismatch")
            self.pos=end
        return result

def annotations(raw):
    rd=AnnotationReader(raw)
    return {"class":rd.attributes,"methods":[{"name":m["name"],"descriptor":m["descriptor"],
                **{k:v for k,v in m.items() if k in ("RuntimeVisibleAnnotations","RuntimeInvisibleAnnotations")}}
            for m in rd.methods if any(k in m for k in ("RuntimeVisibleAnnotations","RuntimeInvisibleAnnotations"))]}

def match_ref(ref):
    return isinstance(ref,list) and len(ref)==3 and ref[0] in (10,11) and ref[2][1] in TARGETS.get(ref[1],())

def candidate(reader):
    hits={}
    for i,e in enumerate(reader.pool):
        if e is None or e[0] not in (10,11,15):continue
        v=reader.resolve(i)
        ref=v["reference"] if isinstance(v,dict) else v
        if match_ref(ref):hits[i]=v
    return hits

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
        roster=sorted(x for x in paths if x.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"publisher roster")
        candidates={};implementers=[];parents={}
        for path in roster:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"publisher class identity")
            hits=candidate(rd)
            if hits:candidates[rd.name]=hits
            parents[rd.name]=(rd.parent,rd.interfaces)
        changed=True
        while changed:
            changed=False
            for owner,(parent,interfaces) in parents.items():
                if owner==ACCESS or owner in implementers:continue
                if ACCESS in interfaces or parent in implementers or any(i in implementers for i in interfaces):
                    implementers.append(owner);changed=True
        require(len(implementers)<=40,"inventory implementation budget")
        selected=sorted(set(candidates)|set(SELECT)|ALL|set(implementers))
        require(len(selected)<=100,"owner budget")
        owners={}
        dispatch_count=0
        for owner in selected:
            raw=z.read(owner+".class");rd=ClassReader(raw)
            require(owner not in PINS or digest(raw)==PINS[owner],"prior class drift "+owner)
            parsed=disassemble(jar,javap,owner)
            methods=[]
            for key,body in sorted(parsed.items()):
                if not body:continue
                offsets=sorted(body);sites=[]
                for pos,at in enumerate(offsets):
                    op,arg,sym=body[at]
                    cp=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if cp and int(cp[1]) in candidates.get(owner,{}):
                        sites.append({"offset":at,"opcode":op,"reference":candidates[owner][int(cp[1])],
                            "window":[{"offset":v,"opcode":body[v][0],"operand":body[v][1],"symbol":body[v][2]}
                                      for v in offsets[max(0,pos-8):pos+9]]})
                links=[v for v in bootstrap(rd,body) if any(h["name"] in TARGETS.get(h["owner"],()) for h in v["handles"])]
                for site in sites:
                    v=site["reference"]
                    if isinstance(v,list) and v[1]==EVENT and v[2][1]=="acPlayerEntityInteract":
                        dispatch_count+=1
                dispatch_count+=sum(1 for v in links for h in v["handles"] if h["owner"]==EVENT and h["name"]=="acPlayerEntityInteract")
                core=owner in ALL or owner in implementers or key[0] in SELECT.get(owner,())
                if not (core or sites or links):continue
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                members=sum(op in SELECT_OPS for op,_,_ in body.values())
                branches=sum(op.startswith("if") or op in ("goto","goto_w") for op,_,_ in body.values())
                terminals=sum(op.endswith("return") or op=="athrow" for op,_,_ in body.values())
                bounded=len(body)<=800 and members<=180 and branches<=90 and terminals<=30
                row={"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
                     "instruction_count":len(body),"instruction_sha256":summarize(rd,key,body)["instruction_sha256"],
                     "sites":sites,"target_bootstraps":links,"projection":"DIRECT_SITE_WINDOWS_ONLY"}
                if bounded:
                    row["semantics"]=project(rd,key,body,decl);row["projection"]="FULL_BOUNDED_SEMANTICS"
                elif core:
                    row["projection"]="CORE_BODY_OVER_BUDGET_NOT_CERTIFIED"
                methods.append(row)
            owners[owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,
                           "declarations":[{"name":d["name"],"descriptor":d["descriptor"],"code_sha256":d.get("code_sha256")} for d in rd.methods],
                           "fields":rd.fields,"methods":methods}
        require(dispatch_count==1,"previously observed capture dispatcher drift")
        reg=registry(z,jar,javap,REG,{BE})
        annotations_by_owner={owner:annotations(z.read(owner+".class")) for owner in selected if owner==EVENT or any(v["sites"] and any(isinstance(x["reference"],list) and x["reference"][1]==EVENT for x in v["sites"]) for v in owners[owner]["methods"])}
    report={"schema_version":2,"scope":"HOLOCODER_INGRESS_AND_INVENTORY_BRIDGE_DISCOVERY_ONLY",
            "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},"class_roster":1555,
            "event_dispatch_sites":dispatch_count,"inventory_access_implementers":sorted(implementers),
            "owners":owners,"block_entity_registry":reg,"annotations":annotations_by_owner,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=4000000,"report budget")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("xb") as f:f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(owners),"EVENT_SITES",dispatch_count)
    print("ACCESS_IMPLEMENTERS",json.dumps(sorted(implementers)))
    print("REGISTRY",json.dumps(reg,sort_keys=True))
    print("ANNOTATIONS",json.dumps(annotations_by_owner,sort_keys=True))
    for owner,row in owners.items():
        print("OWNER",owner,row["class_sha256"],row["interfaces"])
        for method in row["methods"]:
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION")

def self_test():
    require(match_ref([10,EVENT,[12,"acPlayerEntityInteract","()Z"]]),"event match")
    require(not match_ref([10,"foreign/CommonEvents",[12,"acPlayerEntityInteract","()Z"]]),"owner match")
    require(not match_ref([9,EVENT,[12,"acPlayerEntityInteract","Z"]]),"typed method match")
    require(match_ref([11,ACCESS,[12,"takeOne","(I)Ljava/lang/Object;"]]),"interface match")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    probe=object.__new__(AnnotationReader)
    probe.raw=bytes.fromhex("00010000")
    probe.pos=0
    probe.pool=[None,(1,"Lsample/Event;")]
    require(probe.annotation()=={"descriptor":"Lsample/Event;","elements":{}},"annotation parser")
    print("PASS: exact typed method and interface owner matching")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None,"jar/output required")
        inspect(a.jar,a.javap,a.output)
