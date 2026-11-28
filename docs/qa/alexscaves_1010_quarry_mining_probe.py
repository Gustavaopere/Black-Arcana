#!/usr/bin/env python3
"""Read-only, pinned quarry mining causal census; no runtime or certificate claim."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble

P="com/github/alexmodguy/alexscaves/server/"
Q=P+"entity/item/QuarrySmasherEntity"
B=P+"block/blockentity/QuarryBlockEntity"
I=P+"item/QuarrySmasherItem"
ER=P+"entity/ACEntityRegistry"
IR=P+"item/ACItemRegistry"
ROSTER_SHA="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
PINS={Q:"6691eb5f3ca50fd3d0c700e7b2464994778efa812e5336f59802c328a73d352a",
      B:"d28351c04247eadf0218b6514ce6c7e4aeea4d11ad37cccb88626e9c2c9e9e99",
      I:"bf8fe4f6404e3d46f085bc708eb6a260f598cab0fc0a1dec0806bf066fd790d4"}
CODE_PINS={(Q,"tick","()V"):"ac9dbb5d0dc0eaa8bfa5733b1499c6bd34b6c6d8fa313bf609dcce9e7aa3b399",
           (Q,"findTarget","()Lnet/minecraft/core/BlockPos;"):"e6829ab1cc348066542bf19168397365ba10e62b74bce7b07de2e5e21582fdce",
           (IR,"lambda$static$16","()Lnet/minecraft/world/item/Item;"):"8eedb42718de2b1062ad616449d83c8b6577741845712c901bd1fbb73a7c70f6"}
LIMITS={"static_contract":"NOT_CERTIFIED","mutation":"NO_MUTATION","physical_qa":"NOT_TESTED",
        "runtime_loaded_bytes":"NOT_OBSERVED","semantic_magic_roots_delta":0}
# Restrict full bodies to provider-owned quarry classes, not every unrelated method.
def primary(owner):
    return owner.startswith(P) and owner.rsplit("/",1)[-1].startswith("Quarry")

def matched_member(v):
    return isinstance(v,list) and len(v)==3 and v[0] in (9,10,11) and (
        v[1] in (Q,B) or (v[1] in (ER,IR) and v[2][1]=="QUARRY_SMASHER"))

def method_record(rd,key,body):
    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
    require("code_sha256" in decl and 0<len(body)<=3000,"method body budget "+str(key))
    # Report typed operands, branch targets, constants and ordered local/arithmetic events.
    # No source transcription or third-party implementation copied into catalog.
    instructions=[]
    for at,(op,arg,symbol) in sorted(body.items()):
        m=re.match(r"#(\d+)(?:\s|,|$)",arg)
        resolved=rd.resolve(int(m[1])) if m else None
        instructions.append({"offset":at,"opcode":op,"operand":arg,
                             "constant":resolved,"symbol":symbol if m else ""})
    return {"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
            "instruction_count":len(body),"instruction_sha256":digest(canonical(instructions).encode()),
            "instructions":instructions}

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist();roster=sorted(n for n in names if n.endswith(".class"))
        require(len(names)==len(set(names)) and len(roster)==1555,"publisher roster")
        require(digest(("\n".join(roster)+"\n").encode())==ROSTER_SHA,"roster hash")
        classes={};census={};pins=set();codes=set()
        for path in roster:
            raw=z.read(path);rd=ClassReader(raw);owner=rd.name
            require(owner+".class"==path and rd.major==65,"class identity "+path)
            if owner in PINS:
                require(digest(raw)==PINS[owner],"class pin "+owner);pins.add(owner)
            refs={i:rd.resolve(i) for i,v in enumerate(rd.pool) if v and v[0] in (9,10,11) and matched_member(rd.resolve(i))}
            selected=primary(owner) or owner in (IR,ER)
            if not selected and not refs:continue
            parsed=disassemble(jar,javap,owner)
            methods=[];sites=[]
            for key,body in sorted(parsed.items()):
                if not body:continue
                if primary(owner) or (owner==IR and key[0]=="lambda$static$16") or (owner==ER and key[0]=="lambda$static$10"):
                    m=method_record(rd,key,body)
                    pin=(owner,*key)
                    if pin in CODE_PINS:
                        require(m["code_sha256"]==CODE_PINS[pin],"Code pin "+str(pin));codes.add(pin)
                    if pin==(Q,"tick","()V"):require(m["instruction_count"]==580,"prior deferred tick count")
                    methods.append(m)
                hits=[]
                for at,(op,arg,_) in sorted(body.items()):
                    m=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if m and int(m[1]) in refs:
                        hits.append({"offset":at,"opcode":op,"member":refs[int(m[1])]})
                if hits:
                    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                    sites.append({"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],"sites":hits})
            if methods:
                if primary(owner):
                    require({(m["name"],m["descriptor"]) for m in methods}==
                            {(d["name"],d["descriptor"]) for d in rd.methods if "code_sha256" in d},
                            "executable roster "+owner)
                classes[owner]={"class_sha256":digest(raw),"parent":rd.parent,
                                "fields":rd.fields,"methods":methods}
            if refs:
                census[owner]={"class_sha256":digest(raw),"constant_pool_candidates":list(refs.values()),"direct_sites":sites}
        require(pins==set(PINS) and codes==set(CODE_PINS),"prior pins covered")
        require(3<=len(classes)<=25 and 1<=len(census)<=100,"scope budget")
        return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
                "roster_sha256":ROSTER_SHA,"classes":classes,"direct_consumer_census":census,"limits":LIMITS}
def self_test():
    require(primary(Q) and primary(B) and not primary("net/minecraft/Quarry"),"owner filter")
    require(matched_member([10,Q,[12,"tick","()V"]]),"member filter")
    require(not matched_member([9,IR,[12,"OTHER","Ljava/util/function/Supplier;"]]),"negative filter")
    require(LIMITS["mutation"]=="NO_MUTATION","scope")
    print("PASS owner and typed member filters")
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once output")
        result=inspect(a.jar,a.javap);raw=canonical(result).encode()
        require(len(raw)<=8_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row["class_sha256"],"METHODS",len(row["methods"]))
            for m in row["methods"]:print("METHOD",json.dumps({"owner":owner,**m},sort_keys=True))
        for owner,row in result["direct_consumer_census"].items():
            print("CONSUMERS",json.dumps({"owner":owner,**row},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
