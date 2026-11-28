#!/usr/bin/env python3
"""Moth Dust exact publisher and distributed targeting/settlement discovery.
No gameplay execution, external hook promotion or provider code reuse.
"""
import argparse,json,re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader,canonical,digest,require,verify_artifact,SHA1,SHA256,SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection,identified,verify_universal,ARTIFACTS
P="com/github/alexmodguy/alexscaves/server/"
M="net/minecraft/"
N="net/neoforged/neoforge/"
I=P+"item/MothDustItem"
IR=P+"item/ACItemRegistry"
ID="alexscaves:moth_dust"
TAG="data/alexscaves/tags/entity_type/moth_dust_enrages.json"
PINS={I:"ce046ddfe30a9c860570332b04b63b619ad29d3f87b170b935b7b2dbd3db3faf",IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"}
CODE={(I,"<init>"):"8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c",
      (I,"getUseAnimation"):"dfb9aff16602b7340870ab7fc902b22294f662e441389a5a6c3b983791acee04",
      (I,"use"):"be2d1d78173630b6745f5890c9ac0bcee6fe32c2fb3906c8d416cb45bca71be5",
      (I,"releaseUsing"):"5f73541a31cf91fb222b685ee4eb456b7ffc2b91c19c29420a1311880f2f99fe",
      (I,"getUseDuration"):"b8aee7c99ad68ca4f9bded1dd23b0ec788cfe9329b0d036d54e7e6c95cb79b51",
      (I,"getPowerForTime"):"171bb48bcef90c7751d8b427a556bc04c5896001df0fcc9eab39585c8ab9af69",
      (IR,"lambda$static$122"):"20fac1a05d60f7390148c4a90e14a151511ba918fb57388a09b978b7dbcd4948"}
SELECT={
    IR:{"lambda$static$122"},P+"misc/ACCompat":{"useConsume"},
    M+"world/entity/projectile/ProjectileUtil":{"getHitResultOnViewVector","getHitResult","getEntityHitResult"},
    M+"world/entity/Entity":{"canBeHitByProjectile","isAlliedTo","isPassengerOfSameVehicle","getEyePosition","getViewVector","pick","is"},
    M+"world/entity/LivingEntity":{"canBeSeenAsEnemy","startUsingItem","releaseUsingItem","stopUsingItem","getUseItemRemainingTicks","getTicksUsingItem","setLastHurtByMob","getLastHurtByMob","getLastHurtByMobTimestamp","tick","canAttack"},
    M+"world/entity/Mob":{"setTarget","getTarget","canAttack","serverAiStep"},
    M+"world/entity/player/Player":{"isCreative","canBeSeenAsEnemy","canHarmPlayer"},
    M+"world/entity/ai/goal/target/TargetGoal":{"canContinueToUse","start","stop","canAttack"},
    M+"world/entity/ai/goal/target/HurtByTargetGoal":{"canUse","start","alertOthers","alertOther"},
    M+"world/entity/ai/targeting/TargetingConditions":{"test"},
    M+"world/item/ItemStack":{"releaseUsing","getUseDuration","shrink"},
    M+"world/item/Item":{"releaseUsing","use","getUseDuration"},
    M+"world/level/Level":{"getEntities"},
    M+"world/phys/AABB":{"<init>","clip","contains","intersects","inflate","expandTowards"},
    M+"world/level/ClipContext":{"<init>","getBlockShape","getFluidShape"},
    M+"world/level/BlockGetter":{"clip"},
    M+"server/network/ServerGamePacketListenerImpl":{"handlePlayerAction","handleUseItem"},
    M+"server/level/ServerPlayerGameMode":{"useItem"},
    N+"common/CommonHooks":{"onLivingChangeTarget","onItemUseStart","onItemUseStop"},
    N+"event/EventHooks":{"onLivingChangeTarget","onItemUseStart","onItemUseStop","onItemUseTick","onItemUseFinish"},
}
REQUIRED={IR:{"lambda$static$122"},M+"world/entity/projectile/ProjectileUtil":{"getHitResultOnViewVector","getEntityHitResult"},M+"world/entity/Mob":{"setTarget"},M+"world/entity/LivingEntity":{"setLastHurtByMob","releaseUsingItem"},M+"world/item/ItemStack":{"releaseUsing","shrink"}}
AI={"setTarget","getTarget","setLastHurtByMob","canAttack","canBeSeenAsEnemy","registerGoals","customServerAiStep","aiStep","tick","hurt","canBeHitByProjectile","isAlliedTo","addAdditionalSaveData","readAdditionalSaveData"}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED","actual_target_acceptance":"NOT_VERIFIED"}
def hits(v,path=()):
    if isinstance(v,dict):
        for k,x in sorted(v.items()):
            if k==ID:yield [list(path+(k,)),"KEY"]
            yield from hits(x,path+(k,))
    elif isinstance(v,list):
        for j,x in enumerate(v):yield from hits(x,path+(j,))
    elif v==ID:yield [list(path),"VALUE"]
def inspect(a):
    verify_artifact(a.publisher);verify_universal(a.universal,"universal")
    artifact={"publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},"installer":identified(a.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),"server":identified(a.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),"srg":identified(a.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),"universal":ARTIFACTS["universal"],"neoforge_version":"21.1.250"}
    require(not a.output.exists(),"write once")
    with ZipFile(a.server) as ov,ZipFile(a.universal) as un,ZipFile(a.srg) as mc,ZipFile(a.publisher) as mod:
        archives=[("OVERLAY",ov),("UNIVERSAL",un),("SRG",mc),("PUBLISHER",mod)]
        require(all(len(z.namelist())==len(set(z.namelist())) for _,z in archives),"duplicate entries")
        index=[(n,z,set(z.namelist())) for n,z in archives]
        cp=":".join(map(str,(a.server,a.universal,a.srg,a.publisher)))
        roster=sorted(p for p in mod.namelist() if p.endswith(".class"))
        require(len(roster)==1555 and digest(("\n".join(roster)+"\n").encode())=="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed","roster")
        rawtag=mod.read(TAG)
        require(digest(rawtag)=="5d7807c49608ec6c6250dd376c42519d74a317dd4f844b7b6382568eb8c8a402","tag pin")
        tag=json.loads(rawtag)
        require(isinstance(tag["values"],list),"tag values")
        names={v.split(":")[-1].replace("_","").lower()+"entity" for v in tag["values"] if isinstance(v,str) and not v.startswith("#")}
        # Class-name matches are candidates, not proven registry bindings.
        candidates=[];ai=[];fields=[]
        for path in roster:
            rd=ClassReader(mod.read(path));require(rd.name+".class"==path and rd.major==65,"publisher identity")
            refs=[v for v in rd.typed_refs(IR) if v["kind"]=="field_reference" and v["name"]=="MOTH_DUST"]
            typed=rd.typed_refs(I)
            if refs or typed:candidates.append({"owner":rd.name,"field_refs":refs,"typed_refs":typed})
            if rd.name.rsplit("/",1)[-1].lower() in names:ai.append(rd.name)
            if refs:
                parsed=disassemble(cp,a.javap,rd.name);ids={v["index"] for v in refs}
                for key,body in sorted(parsed.items()):
                    for at,(op,arg,sym) in sorted(body.items()):
                        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                        if match and int(match[1]) in ids:
                            decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                            fields.append({"owner":rd.name,"method":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],"offset":at,"opcode":op,"symbol":sym})
        require(len(candidates)<=100 and len(fields)<=100 and len(ai)<=20,"publisher candidate budget")
        classes={}
        for owner in sorted(set(SELECT)|{I}|set(ai)):
            found=[(n,z) for n,z,paths in index if owner+".class" in paths]
            if not found:
                require(owner not in REQUIRED and owner!=I,"required owner "+owner)
                classes[owner]={"present":False};continue
            source,z=found[0];raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            require(owner not in PINS or digest(raw)==PINS[owner],"class pin "+owner)
            select=SELECT.get(owner,AI if owner in ai else set())
            decls=[d for d in rd.methods if owner==I or d["name"] in select]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required method "+owner)
            require(len(decls)<=100,"method budget "+owner)
            parsed=disassemble(cp,a.javap,owner);methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"]);pin=CODE.get((owner,key[0]))
                require(pin is None or d.get("code_sha256")==pin,"Code pin "+owner+str(key))
                if "code_sha256" not in d:methods.append({"name":key[0],"descriptor":key[1],"executable":False});continue
                require(key in parsed and 0<len(parsed[key])<=5000,"body budget "+owner+str(key))
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            classes[owner]={"present":True,"source":source,"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"declarations":rd.methods,"methods":methods}
        resources={}
        paths=sorted(p for p in mod.namelist() if p.startswith("data/") and p.endswith(".json"))
        require(len(paths)<=5000,"resource budget")
        for p in paths:
            raw=mod.read(p);require(len(raw)<=2000000,"resource size")
            obj=json.loads(raw);refs=list(hits(obj))
            if refs or p==TAG or p.rsplit("/",1)[-1]=="moth_dust.json":resources[p]={"sha256":digest(raw),"bytes":len(raw),"refs":refs,"data":obj}
        require(len(resources)<=100,"resource hits")
        require(digest(mod.read("assets/alexscaves/models/item/moth_dust.json"))=="293ac1ab9c1db699f5e385954e7f773e2d899347f0351a1cf4bb7e428d06c4e0","model pin")
    report={"schema":1,"artifact":artifact,"classes":classes,"publisher_candidates":candidates,"field_sites":fields,"tag_class_name_candidates":ai,"data_json_count":len(paths),"resources":resources,"limits":LIMITS}
    data=canonical(report).encode();require(len(data)<=15000000,"report budget")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("xb") as f:f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,v in classes.items():
        print("OWNER",owner,v.get("source"),v.get("class_sha256"),"METHODS",len(v.get("methods",[])))
        for m in v.get("methods",[]):print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
    print("FIELD_SITES",json.dumps(fields,sort_keys=True));print("TAG_CLASS_NAME_CANDIDATES",json.dumps(ai,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True));print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
def self_test():
    require(list(hits({ID:1,"x":[ID,ID+"_other"]}))==[[[ID],"KEY"],[["x",0],"VALUE"]],"exact filter")
    require(len(CODE)==7 and LIMITS["mutation"]=="NO_MUTATION","policy and pins")
    print("PASS exact identity and policy")
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"inputs")
        inspect(a)
