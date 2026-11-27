#!/usr/bin/env python3
"""Read-only exact Jelly Bean potion producer and consumption boundaries."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection, identified, verify_universal, ARTIFACTS

P = "com/github/alexmodguy/alexscaves/server/"
M = "net/minecraft/"
N = "net/neoforged/neoforge/"
J = P+"item/JellyBeanItem"
G = P+"entity/living/GummyBearEntity"
C = P+"misc/ACCompat"
ER = P+"potion/ACEffectRegistry"
IR = P+"item/ACItemRegistry"
FOOD = P+"item/ACFoods"
PC = M+"world/item/alchemy/PotionContents"
L = M+"world/entity/LivingEntity"
PINS = {
    J:"9842c28cd2eff05621a23be37ce5917ca88a19bf0bd99f0da9b5a5cc62a4355f",
    G:"46c685cfbe9273430ce95d8eda27a75b086978dd3e3a216b83e3d485ba1c2191",
    C:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    ER:"f60c1a6704c39eecace6522db8a36ed3219ed13a329f0c56c368737533c51d82",
    IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
    L:"52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
}
CODE_PINS={
    (J,"finishUsingItem"):"285ba91b3197410e4ea9e455598f972ce7a7c2be1d1febc8aa9702959b493e18",
    (G,"createJellybean"):"32a3e91f97ff7fb2d1d43eca02dfdf79a41ad80bca76b93f80578165307788cd",
    (ER,"createJellybean"):"5726e6ef99a36f1d369980be69c04f1105182ca41f3e9c68bd6378f032626b18",
    (C,"potionEffects"):"cfb23f71a3385db6d2a487c4d733f5fdc6fec2e9be5177807a28c82c6610e704",
    (C,"applyInstantenousEffect"):"061e7ceb46bd78233f4e56ba3a28a9fa1eb1561754dd2e2fe2db2a143446cf1a",
    (IR,"lambda$static$198"):"546da6af37d6cc4834693c322a2cd13c1852123744a3bd55006b0bee3fd5ed63",
}
SELECT={
    IR:{"lambda$static$198"},
    G:{"createJellybean","addAdditionalSaveData","readAdditionalSaveData"},
    ER:{"createJellybean"},
    C:{"contentsOf","potionStack","potionEffects","potionColor","rawEffect","applyInstantenousEffect","getOrCreateTag","setTag"},
    P+"misc/ACPlatform":{"attributeModifiers","formatDuration"},
    M+"world/item/PotionItem":{"<init>","use","getUseAnimation","getUseDuration","finishUsingItem","getDefaultInstance"},
    M+"world/item/ItemUtils":{"startUsingInstantly"},
    M+"world/item/ItemStack":{"finishUsingItem","use","consume","shrink","grow"},
    PC:{"<init>","getAllEffects","getColor","withPotion","withEffect","forEachEffect","hasEffects"},
    M+"world/item/alchemy/Potion":{"getEffects"},
    M+"world/effect/MobEffect":{"applyInstantenousEffect","isInstantenous","getAttributeModifiers","addAttributeModifiers"},
    M+"world/effect/MobEffectInstance":{"<init>","update","getDuration","getAmplifier","endsWithin"},
    L:{"startUsingItem","completeUsingItem","addEffect","canBeAffected","onEffectAdded","onEffectUpdated"},
    N+"event/EventHooks":{"onItemUseStart","onItemUseTick","onItemUseFinish"},
    N+"common/CommonHooks":{"canMobEffectBeApplied"},
    M+"world/item/component/CustomData":{"of","copyTag"},
    M+"world/food/FoodData":{"eat"},
}
REQUIRED={
    J:{"<init>","finishUsingItem","getUseDuration","getBeanColor"},
    G:{"createJellybean"},
    ER:{"createJellybean"},
    C:{"contentsOf","potionStack","potionEffects","applyInstantenousEffect"},
    IR:{"lambda$static$198"},
    PC:{"getAllEffects"},
    L:{"completeUsingItem","addEffect"},
    M+"world/item/PotionItem":{"use"},
    M+"world/item/ItemStack":{"finishUsingItem"},
    N+"event/EventHooks":{"onItemUseFinish"},
    N+"common/CommonHooks":{"canMobEffectBeApplied"},
}
LIMITS={"static_contract":"NOT_CERTIFIED","mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","runtime_loaded_bytes":"NOT_OBSERVED",
        "provider_universe_closed":False,"semantic_magic_roots_delta":0}
MEMBER_KINDS={"field_reference","method_reference","interface_method_reference"}
OPS={"getstatic","putstatic","getfield","putfield","invokestatic","invokevirtual","invokespecial","invokeinterface","ldc","ldc_w","new","checkcast","instanceof"}

def matched_indices(rd):
    typed=rd.typed_refs(J)
    typed.extend(x for target in (IR,FOOD) for x in rd.typed_refs(target)
                 if x.get("kind")=="field_reference" and x.get("name")=="JELLY_BEAN")
    typed.extend(x for x in rd.typed_refs(G) if x.get("name") in {"digestingEffect","createJellybean"})
    typed.extend(x for x in rd.typed_refs(ER) if x.get("name")=="createJellybean")
    literals=[i for i,v in enumerate(rd.pool) if v and v[0]==8 and rd.resolve(i)=="Rainbow"]
    cp={x["index"] for x in typed if "index" in x and x["kind"] in MEMBER_KINDS|{"class_constant"}}
    return typed,literals,cp|set(literals)

def consumers(mod,jar,javap,paths):
    out=[]
    for path in paths:
        raw=mod.read(path)
        rd=ClassReader(raw)
        require(rd.name+".class"==path and rd.major==65,"publisher class identity")
        typed,literals,indices=matched_indices(rd)
        if not typed and not literals:
            continue
        require(len(out)<60,"consumer owner budget")
        methods=[]
        if indices:
            decls={(d["name"],d["descriptor"]):d for d in rd.methods}
            for key,body in sorted(disassemble(jar,javap,rd.name).items()):
                offsets=sorted(body)
                hits=[]
                for i,at in enumerate(offsets):
                    op,arg,_=body[at]
                    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if op not in OPS or not match or int(match[1]) not in indices:
                        continue
                    window=offsets[max(0,i-8):i+9]
                    hits.append({"offset":at,"opcode":op,"constant":rd.resolve(int(match[1])),
                                 "context":[{"offset":q,"opcode":body[q][0],"symbol":body[q][2]} for q in window]})
                if hits:
                    require(key in decls and len(hits)<=100,"consumer site budget")
                    methods.append({"name":key[0],"descriptor":key[1],"code_sha256":decls[key]["code_sha256"],"sites":hits})
        out.append({"owner":rd.name,"class_sha256":digest(raw),"typed_references":typed,
                    "rainbow_string_constant_indices":literals,"instruction_sites":methods})
    require(any(row["owner"]==G for row in out),"gummy producer census")
    return {"scope":"EXACT_TYPED_AND_STRING_CANDIDATES_WITH_LOCAL_SITES_NOT_DYNAMIC_DISPATCH",
            "class_entries_scanned":len(paths),"owners":out}

def inspect(a):
    verify_artifact(a.publisher)
    verify_universal(a.universal,"universal")
    require(not a.output.exists(),"write-once report")
    artifact={"publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
              "neoforge_version":"21.1.250",
              "installer":identified(a.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
              "server":identified(a.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
              "srg":identified(a.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
              "universal":ARTIFACTS["universal"]}
    with ZipFile(a.server) as ov,ZipFile(a.universal) as uni,ZipFile(a.srg) as mc,ZipFile(a.publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive path")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        paths=sorted(p for p in mod.namelist() if p.endswith(".class"))
        require(len(paths)==1555 and digest(("\n".join(paths)+"\n").encode())=="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed","publisher roster")
        cs=consumers(mod,a.publisher,a.javap,paths)
        cp=":".join(map(str,(a.server,a.universal,a.srg,a.publisher)))
        classes={}
        for owner in sorted({J}|set(SELECT)):
            found=[(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False}
                continue
            source,z=found[0]
            raw=z.read(owner+".class")
            rd=ClassReader(raw)
            sha=digest(raw)
            require(rd.name==owner and rd.major==65 and (owner not in PINS or sha==PINS[owner]),"class identity "+owner)
            if owner==J:
                require(rd.parent==M+"world/item/PotionItem" and len(rd.methods)==9,"JellyBeanItem roster")
            decls=[d for d in rd.methods if owner==J or d["name"] in SELECT.get(owner,set())]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required declaration "+owner)
            require(len(decls)<=100,"method budget")
            for (o,name),expected in CODE_PINS.items():
                if o==owner:
                    require(any(d["name"]==name and d.get("code_sha256")==expected for d in decls),"Code pin "+owner+"."+name)
            parsed=disassemble(cp,a.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"body absent "+owner+str(key))
                print("PROJECTING",owner,*key,flush=True)
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner==J:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d}=={k for k,v in parsed.items() if v},"complete JellyBeanItem body roster")
            classes[owner]={"present":True,"source":source,"class_sha256":sha,"parent":rd.parent,
                            "interfaces":rd.interfaces,"declarations":rd.methods,"fields":rd.fields,"methods":methods}
        resources={}
        candidates=sorted(p for p in mod.namelist() if p.endswith(".json") and ("jelly_bean" in p.rsplit("/",1)[-1] or "jellybean" in p.rsplit("/",1)[-1]))
        require(len(candidates)<=40,"resource budget")
        for path in candidates:
            raw=mod.read(path)
            require(len(raw)<=100000,"resource byte budget")
            resources[path]={"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}
    report={"schema_version":1,"scope":"JELLY_BEAN_POTION_DISCOVERY_ONLY","artifact":artifact,"classes":classes,
            "publisher_consumers":cs,"resources":resources,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=10000000,"report budget")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("xb") as f:
        f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,row in classes.items():
        print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
        for method in row.get("methods",[]):
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("PUBLISHER_CONSUMERS",json.dumps(cs,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS)<={J}|set(SELECT),"pins scoped")
    require(all(o==J or n in SELECT[o] for o,n in CODE_PINS),"Code pin scope")
    require(REQUIRED[C]>={"contentsOf","potionStack"},"component boundaries")
    require(REQUIRED[L]>={"addEffect","completeUsingItem"},"settlement boundaries")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: discovery scope and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"all inputs required")
        inspect(a)
