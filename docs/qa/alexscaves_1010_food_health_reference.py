#!/usr/bin/env python3
"""FoodProperties construction and consumption: official bounded references.

Uses hash-checked vanilla 1.21.1 client and separate NeoForge 21.1.250
universal/userdev. No installed transformation or gameplay execution.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_enchantable_item_boundary import download, CLIENT_SHA1
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_engine
from minecraft_1211_mojang_mixin_target_mappings import CLASS, METHOD, official_version_downloads
from minecraft_1211_vanilla_target_callsites import jvm_type

PRIOR="e6453ae5631a104314f67c9d9e337cced60da511e56f226b2b13fb4f39054a77"
FOOD="net.minecraft.world.food.FoodProperties"
BUILDER=FOOD+"$Builder"
EFFECT=FOOD+"$PossibleEffect"
LIVING="net.minecraft.world.entity.LivingEntity"
PLAYER="net.minecraft.world.entity.player.Player"
FOODDATA="net.minecraft.world.food.FoodData"
TARGETS={
    LIVING:{"getHealth","setHealth","getMaxHealth","heal","getEffect","hasEffect","addEffect"},
    "net.minecraft.world.item.ItemUtils":{"startUsingInstantly"},
    "net.minecraft.world.item.PotionItem":{"use","getUseDuration","finishUsingItem","getUseAnimation"},
    "net.minecraft.world.item.alchemy.PotionContents":{"getAllEffects","forEachEffect","getColor"},
    "net.minecraft.world.effect.MobEffect":{"applyInstantenousEffect","isInstantenous"},
    "net.minecraft.world.effect.MobEffectInstance":{"<init>","getAmplifier","getDuration","getEffect"},
}


def vanilla(tmp,javap):
    metadata=official_version_downloads()
    d=metadata["downloads"]
    require(d["client"]["sha1"]==CLIENT_SHA1,"unexpected vanilla version")
    jar=tmp/"client.jar"; mapping=tmp/"client.txt"
    identity={"metadata_sha1":metadata["json_sha1"],
              "client":download(jar,d["client"],35000000),
              "client_mappings":download(mapping,d["client_mappings"],15000000)}
    require(identity["client"]["sha256"]=="499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99","client hash drift")
    require(identity["client_mappings"]["sha256"]=="140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec","mappings drift")
    lines=mapping.read_text(encoding="utf8").splitlines(); named={}; own=None
    candidates=[]
    for line in lines:
        if CLASS.fullmatch(line):
            own,obf=line[:-1].split(" -> ")
            named[own]=obf
            continue
        m=METHOD.fullmatch(line.strip()) if own in TARGETS else None
        if m and m.group(2) in TARGETS[own]:
            ret,name,args=m.groups()
            candidates.append((own,name,ret,tuple(args.split(",")) if args else (),line.strip().rsplit(" -> ",1)[1]))
    def dt(t):
        dims=0
        while t.endswith("[]"): dims+=1;t=t[:-2]
        known=named if t in named else {t:t}
        return "["*dims+jvm_type(t,known)
    ref_targets=set()
    refs={}
    result={}
    reverse={o.replace(".","/"):n for n,o in named.items()}
    with zipfile.ZipFile(jar) as z:
        for owner in TARGETS:
            obf=named[owner].replace(".","/")
            rd=ClassReader(z.read(obf+".class"))
            require(rd.name==obf and rd.major==65,"class identity drift")
            parsed=disassemble(jar,javap,obf)
            seen=set()
            methods=[]
            refs[owner]=[]
            for own,name,ret,args,m in candidates:
                if own!=owner:continue
                k=(m,"("+"".join(dt(t) for t in args)+")"+dt(ret))
                if k in seen:continue
                seen.add(k)
                require(k in parsed,"mapped method absent: "+str((owner,name,k)))
                body=parsed[k]
                require(len(body)<=350,"body over bound")
                methods.append({"named_method":name,"named_args":list(args),**summarize(rd,k,body)})
                for off,(op,operand,symbol) in sorted(body.items()):
                    if not (op.startswith("invoke") or op in ("getstatic","putstatic","getfield","putfield")):continue
                    cp=re.match(r"#(\d+)",operand)
                    if not cp:continue
                    r=rd.resolve(int(cp.group(1)))
                    if isinstance(r,list) and r[0] in (9,10,11):
                        refs[owner].append({"method":name,"descriptor":k[1],"offset":off,"member":r})
                        if r[1] in reverse:ref_targets.add(reverse[r[1]])
            result[owner]={"obfuscated_owner":obf,"class_sha256":digest(z.read(obf+".class")),"methods":methods}
    for own,names in TARGETS.items():
        require(any(m["named_method"] in names for m in result[own]["methods"]),"mapped surface missing "+own)
    field_re=re.compile(r"^(\S+)\s+([\w$]+)\s+->\s+(\S+)$")
    member_map={}
    for line in lines:
        if CLASS.fullmatch(line):
            own,obf=line[:-1].split(" -> ");continue
        if own not in ref_targets:continue
        method=METHOD.fullmatch(line.strip());field=field_re.fullmatch(line.strip())
        if method:
            ret,name,args=method.groups()
            desc="("+"".join(dt(t) for t in args.split(",") if t)+")"+dt(ret)
            mapped=line.strip().rsplit(" -> ",1)[1]
        elif field:
            ret,name,mapped=field.groups();desc=dt(ret)
        else:continue
        member_map.setdefault((named[own].replace(".","/"),mapped,desc),[]).append(own+"."+name)
    for items in refs.values():
        for r in items:
            _,owner,sig=r["member"]
            r["named_candidates"]=sorted(set(member_map.get((owner,sig[1],sig[2]),[])))
    return {"identity":identity,"classes":result,"references":refs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--javap",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();require(not a.output.exists(),"write once")
    tmp=a.output.parent/(a.output.stem+"-download");tmp.mkdir(exist_ok=False)
    report={"schema":"FOOD_HEALTH_REFERENCE_V1","scope":"OFFICIAL_VANILLA_REFERENCE_ONLY","vanilla":vanilla(tmp,a.javap),"mutation":"NO_MUTATION","physical_qa":"NOT_TESTED"}
    a.output.write_text(canonical(report),encoding="utf8")
    print("HEALTH_REFERENCE_SHA256",digest(a.output.read_bytes()),"BYTES",len(a.output.read_bytes()))
    for owner,data in report["vanilla"]["classes"].items():
        print("VANILLA_OWNER",owner,data["obfuscated_owner"],data["class_sha256"])
        for m in data["methods"]:
            refs={r["offset"]:r["named_candidates"] for r in report["vanilla"]["references"][owner] if r["method"]==m["named_method"] and r["descriptor"]==m["declaration"]["descriptor"]}
            print("VANILLA_METHOD",owner,m["named_method"],json.dumps(m["declaration"],sort_keys=True))
            for row in m["instructions"]:print(" ",row["offset"],row["opcode"],row["operand"],row["symbol"]," | ".join(refs.get(row["offset"],[])))
if __name__=="__main__":main()
