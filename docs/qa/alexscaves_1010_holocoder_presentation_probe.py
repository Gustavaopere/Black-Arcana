#!/usr/bin/env python3
"""Bounded read-only Holocoder presentation and state bridge audit.
Publisher exact 1.0.10; no launch, client render, effect or runtime mutation.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

ROOT = "com/github/alexmodguy/alexscaves/"
RENDER = ROOT+"client/render/blockentity/HologramProjectorBlockRenderer"
SOUND = ROOT+"client/sound/HologramProjectorSound"
NOTOR = ROOT+"client/render/entity/NotorRenderer"
CLIENT = ROOT+"client/ClientProxy"
COMMON = ROOT+"server/CommonProxy"
BE = ROOT+"server/block/blockentity/HologramProjectorBlockEntity"
BLOCK = ROOT+"server/block/HologramProjectorBlock"
ITEM = ROOT+"server/item/HolocoderItem"
COMPAT = ROOT+"server/misc/ACCompat"
PLATFORM = ROOT+"server/misc/ACPlatform"
TYPES = ROOT+"client/render/ACRenderTypes"
POST = ROOT+"citadel/client/shader/PostEffectRegistry"
ALL = {RENDER,SOUND,ITEM,BE}
SELECT = {
    NOTOR: {"renderEntityInHologram"},
    CLIENT: {"playWorldSound","clearSoundCacheFor"},
    COMMON: {"playWorldSound","clearSoundCacheFor"},
    BLOCK: {"acUse","useItemOn"},
    COMPAT: {"itemResult","markDisplayEntity","getCompound","entityTypeFrom"},
    PLATFORM: {"encapsulating"},
    TYPES: {"getHologramLights"},
    POST: {"renderEffectForNextTick"},
}
PINS = {
    "com/github/alexmodguy/alexscaves/client/render/blockentity/HologramProjectorBlockRenderer": "fcbaf584c8029aa88028aa290943f445eba7a848c062994e8cabaac61102b025",
    "com/github/alexmodguy/alexscaves/client/sound/HologramProjectorSound": "9d1df43aaaaba9f60b0b0f2192265a6dd1f024a20e185771627e13ebc7a17c7c",
    "com/github/alexmodguy/alexscaves/server/block/HologramProjectorBlock": "ec685ba2b8db000916105c2696f61372e7ee9f93893529bfe196c262dce465fe",
    "com/github/alexmodguy/alexscaves/server/block/blockentity/HologramProjectorBlockEntity": "5aaf4f2f96190d740a101f75c2603d2f3b1001a8c494eaa0594e6aebde308057",
    "com/github/alexmodguy/alexscaves/server/item/HolocoderItem": "7d2697b694b97483ad592733fad8ad595de0fa0805de7a0396ac6cb4715dfd96",
    "com/github/alexmodguy/alexscaves/server/misc/ACCompat": "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    "com/github/alexmodguy/alexscaves/server/misc/ACPlatform": "662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6",
}
KNOWN = {
    ("com/github/alexmodguy/alexscaves/client/render/blockentity/HologramProjectorBlockRenderer", "renderAt", "(Lcom/github/alexmodguy/alexscaves/server/block/blockentity/HologramProjectorBlockEntity;FLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;)V"): "d54930b7a54fb9939a56e4276508a1d638b9560a29620a9f9bfdf2cb9777e04d",
    ("com/github/alexmodguy/alexscaves/client/sound/HologramProjectorSound", "canPlaySound", "()Z"): "5dbc3ba2682a5750e1b237b55068b3a9a04f72c36758a73611387323781c515d",
    ("com/github/alexmodguy/alexscaves/server/item/HolocoderItem", "<init>", "(Lnet/minecraft/world/item/Item$Properties;)V"): "405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d",
    ("com/github/alexmodguy/alexscaves/server/item/HolocoderItem", "appendHoverText", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item$TooltipContext;Ljava/util/List;Lnet/minecraft/world/item/TooltipFlag;)V"): "81b704b643ff1a74bb86ccab2e49d277f0fa103cf76a1adc37d5cfe4b89b738b",
    ("com/github/alexmodguy/alexscaves/server/item/HolocoderItem", "getBoundEntityUUID", "(Lnet/minecraft/world/item/ItemStack;)Ljava/util/UUID;"): "8311a7a2d391c44a11448265c9d667ffc563b3f2d821df19c7ff244fa5a7216e",
    ("com/github/alexmodguy/alexscaves/server/item/HolocoderItem", "isBound", "(Lnet/minecraft/world/item/ItemStack;)Z"): "52dc62c4339e96eb94f2717e55ebd3e232681716b04287d6b04ce8735bb63542",
}
REQUIRED = {
    RENDER: {"renderAt","renderPlayerHologram","shineOriginVertex","shineLeftCornerVertex","shineRightCornerVertex"},
    SOUND: {"canPlaySound","tick"},
    ITEM: {"getBoundEntityUUID","isBound","appendHoverText"},
    BE: {"setEntity","getDisplayEntity","markUpdated","setRemoved","getRenderBoundingBox"},
    NOTOR: {"renderEntityInHologram"},
    BLOCK: {"acUse","useItemOn"},
    COMPAT: {"itemResult","markDisplayEntity"},
    PLATFORM: {"encapsulating"},
    TYPES: {"getHologramLights"},
    POST: {"renderEffectForNextTick"},
}
LIMITS = {"scope":"STATIC_DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "runtime_loaded_bytes":"NOT_OBSERVED","actual_render_and_audio":"NOT_TESTED"}

def selected(owner, declaration):
    return owner in ALL or declaration["name"] in SELECT.get(owner,set())

def inspect(jar,javap):
    verify_artifact(jar)
    out={}; seen=set()
    with ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)) and sum(x.endswith(".class") for x in paths)==1555,"publisher roster")
        for owner in sorted(ALL|set(SELECT)):
            require(owner+".class" in paths,"missing publisher owner "+owner)
            raw=z.read(owner+".class"); rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"owner identity")
            require(owner not in PINS or digest(raw)==PINS[owner],"prior class drift "+owner)
            declarations=[d for d in rd.methods if selected(owner,d)]
            require(len(declarations)<=45,"owner budget "+owner)
            parsed=disassemble(jar,javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"]); full=(owner,*key)
                if "code_sha256" not in d:
                    require(full not in KNOWN,"prior body absent")
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"body not parsed "+str(full))
                if full in KNOWN:
                    require(d["code_sha256"]==KNOWN[full],"prior Code drift "+str(full));seen.add(full)
                row=projection(rd,key,parsed[key],d)
                row["exception_handlers"]=d["exception_handlers"]; row["executable"]=True
                methods.append(row)
            require(REQUIRED.get(owner,set())<={x["name"] for x in methods if x["executable"]},"missing executable body "+owner)
            out[owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,
                        "declared_signatures":[[d["name"],d["descriptor"]] for d in rd.methods],"methods":methods}
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(len(out[ITEM]["declared_signatures"])==4 and len(out[BE]["declared_signatures"])==20,"native roster drift")
    require(sum(len(x["methods"]) for x in out.values())<=120,"total method budget")
    def call(owner,method,offset,target,name,desc):
        require(any(m["name"]==method and m.get("executable") and
                    any((x["offset"],x["owner"],x["name"],x["descriptor"])==(offset,target,name,desc)
                        for x in m["typed_members"]) for m in out[owner]["methods"]),
                "typed presentation callsite drift "+method+" "+name)
    call(RENDER,"renderAt",666,RENDER,"renderPlayerHologram","(Ljava/util/UUID;FLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;I)V")
    call(RENDER,"renderAt",754,NOTOR,"renderEntityInHologram","(Lnet/minecraft/world/entity/Entity;DDDFFLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;I)V")
    call(BE,"tick",131,COMMON,"playWorldSound","(Ljava/lang/Object;B)V")
    call(BE,"setRemoved",4,COMMON,"clearSoundCacheFor","(Lnet/minecraft/world/level/block/entity/BlockEntity;)V")
    return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size":SIZE},"classes":out,"limits":LIMITS}

def self_test():
    require(selected(RENDER,{"name":"renderPlayerHologram"}),"renderer scope")
    require(selected(SOUND,{"name":"tick"}),"sound scope")
    require(selected(BE,{"name":"setRemoved"}),"lifecycle scope")
    require(selected(NOTOR,{"name":"renderEntityInHologram"}),"typed consumer")
    require(not selected(NOTOR,{"name":"unrelated"}),"not whole mob renderer")
    require(not selected("foreign/NotorRenderer",{"name":"renderEntityInHologram"}),"owner boundary")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: seven scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(),"exact input and write-once output")
        report=inspect(a.jar,a.javap); raw=canonical(report).encode()
        require(len(raw)<=4_000_000,"report byte budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row["class_sha256"],"METHODS",len(row["methods"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
