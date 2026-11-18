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
    BUILDER:{"<init>","nutrition","saturationModifier","alwaysEdible","fast","usingConvertsTo","effect","build"},
    FOOD:{"<init>","saturationByModifier","eatDurationTicks","nutrition","saturation","canAlwaysEat","eatSeconds","effects","usingConvertsTo"},
    EFFECT:{"<init>","effect","probability"},
    LIVING:{"eat","addEatEffect","addEatEffects"},
    PLAYER:{"eat"},
    FOODDATA:{"eat","add","addInternal"},
    "net.minecraft.world.food.FoodConstants":{"saturationByModifier"},
    "net.minecraft.world.item.Item":{"use","getUseDuration","finishUsingItem"},
    "net.minecraft.world.item.ItemStack":{"consume"},
}
EXPECTED_BUILDER=TARGETS[BUILDER]-{"<init>"}


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
    require(EXPECTED_BUILDER<={m["named_method"] for m in result[BUILDER]["methods"]},"builder method missing")
    for own in (LIVING,PLAYER,FOODDATA):
        require(any(m["named_method"]=="eat" for m in result[own]["methods"]),"eat consumer missing")
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


def neo(universal,userdev,javap):
    verify_engine(universal,"universal");verify_engine(userdev,"userdev")
    owner="net/neoforged/neoforge/event/EventHooks"
    with zipfile.ZipFile(universal) as z:
        raw=z.read(owner+".class")
        rd=ClassReader(raw)
        parsed=disassemble(universal,javap,owner)
        methods=[summarize(rd,k,b) for k,b in sorted(parsed.items()) if k[0] in {"onItemUseFinish","onItemUseStart","onItemUseTick","onItemUseStop"}]
        require(any(m["declaration"]["name"]=="onItemUseFinish" for m in methods),"event hook missing")
    with zipfile.ZipFile(userdev) as z:
        path="patches/net/minecraft/world/food/FoodProperties.java.patch";raw_patch=z.read(path)
        # No entire external patch is emitted; finite selected lines around the
        # two PossibleEffect constructors, supplier and copy boundary.
        lines=raw_patch.decode("utf8").splitlines()
        anchors=[i for i,l in enumerate(lines) if "PossibleEffect(" in l or "effectSupplier" in l or "Supplier<MobEffectInstance>" in l or "effect()" in l]
        idx={j for i in anchors for j in range(max(0,i-2),min(len(lines),i+3))}
        patch={"entry":path,"sha256":digest(raw_patch),"lines":[{"line":i+1,"text":lines[i]} for i in sorted(idx)]}
    return {"owner":owner,"class_sha256":digest(raw),"methods":methods,"food_patch":patch}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("native-report","universal","userdev","javap","output"):
        p.add_argument("--"+n,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists() and a.output.suffix==".json","new JSON required")
    require(digest(a.native_report.read_bytes())==PRIOR,"native report drift")
    tmp=a.output.parent/"mojang-downloads";tmp.mkdir(exist_ok=False)
    result={"schema":"AC_FOOD_BUILDER_REFERENCE_V1","native_sha256":PRIOR,
            "scope":"REFERENCE_ONLY_NOT_INSTALLED_EXECUTION","vanilla":vanilla(tmp,a.javap),
            "neoforge":neo(a.universal,a.userdev,a.javap),
            "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}
    a.output.write_text(canonical(result),encoding="utf8")
    print("REFERENCE_SHA256",digest(a.output.read_bytes()))
    print("MOJANG",json.dumps(result["vanilla"]["identity"]))
    for owner,data in result["vanilla"]["classes"].items():
        print("VANILLA_OWNER",owner,data["obfuscated_owner"],data["class_sha256"])
        for m in data["methods"]:
            print("VANILLA_METHOD",m["named_method"],json.dumps(m["named_args"]),json.dumps(m["declaration"]))
            refs={r["offset"]:r["named_candidates"] for r in result["vanilla"]["references"][owner] if r["method"]==m["named_method"] and r["descriptor"]==m["declaration"]["descriptor"]}
            for r in m["instructions"]:
                print(" ",r["offset"],r["opcode"],r["operand"],r["symbol"]," | ".join(refs.get(r["offset"],[])))
    for m in result["neoforge"]["methods"]:
        print("NEO_METHOD",m["declaration"]["name"],json.dumps(m["declaration"]))
        for r in m["instructions"]:print(" ",r["offset"],r["opcode"],r["operand"],r["symbol"])
    print("FOOD_PATCH",json.dumps(result["neoforge"]["food_patch"]))
    print("END_FOOD_REFERENCE NO_MUTATION")

if __name__=="__main__":
    main()
