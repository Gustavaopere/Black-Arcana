#!/usr/bin/env python3
"""Read-only exact Resistor Shield presentation and sound consumer discovery."""
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import SELECT_OPS
from alexscaves_1010_four_items_downstream_250_probe import projection
ROOT="com/github/alexmodguy/alexscaves/"
ITEM=ROOT+"server/item/ResistorShieldItem"
SOUND=ROOT+"client/sound/ResistorShieldSound"
EVENT=ROOT+"client/event/ClientEvents"
RENDER=ROOT+"client/render/item/ACItemstackRenderer"
CLIENT=ROOT+"client/ClientProxy"
COMMON=ROOT+"server/CommonProxy"
ALL={ITEM,SOUND}
SELECT={EVENT:{"onPoseHand"},RENDER:{"renderByItem"},CLIENT:{"playWorldSound","clearSoundCacheFor"},COMMON:{"playWorldSound","clearSoundCacheFor"}}
WINDOWS={(EVENT,"onPoseHand"),(RENDER,"renderByItem"),(CLIENT,"playWorldSound")}
NATIVE={"<init>":[12,"b998827c74b378bf4ceab37241709c2f1bca3defee255f9d8099150db2c99d16"],"acExtraRepairMaterials":[15,"b1c165d8b02b3531e59afa61434eb1da01506822154ef3a4d9db9cc34f60812e"],"acInventoryTick":[79,"3cec5ec860390c581f2795f6c2f128c2c1507593934eb6b40db608bf6d182b20"],"appendHoverText":[8,"f1d51a225066a01d40e4007c660f90f54ee87aca37278015cb3b8cdfc2cf79e5"],"getEnchantmentValue":[2,"d943c5fe0bd38038ce70963c73b8759ba3d76c8c00d31c1a2141268dc4e0ee0a"],"getLerpedSwitchTime":[29,"2b596a6e1fd948380b3afa27536d03e15147b74b1ce2626edac364e1dd4680bd"],"getLerpedUseTime":[29,"3bf9be409b9b6d5cb4414c966a0cd27b7b5f5bb89650c7edf4ccaee672d91845"],"getSwitchTime":[11,"dd7de29ec565120099306b77dee7d87f2ddb4fb9d7951584ffceb803cfb3e5e2"],"getUseTime":[11,"fe8cd54d443d0f8217dfcab40bcfafd4d1e89b31203423840e1301b11b1ec087"],"initializeClient":[6,"3a6c2d33865c1d1707dcbd93e1f9e0bd3bd706c9817ddb988b4e0589ebb14cf4"],"isEnchantable":[8,"9cd84b0255be269f2bf50fce0095c14fa5d484831fd35063e71f4c9814aa6b4f"],"isScarlet":[11,"0120856259e8808d6984bbf32e027806ce18b55f48b968a4d8cc0cd31466f25a"],"isValidRepairItem":[13,"56ef4089abe5ca807759ea066eaab7be291dd520d357c2fab2a6de913f3fa597"],"onUseTick":[276,"91abe64167b12b90bbdb14a3792f2c25a273444303ca928df0ae378d5ed7f117"],"releaseUsing":[10,"060b90ea58c4220856ab82b2a6ed4cb7e6948aba77ef9ed69a1c7f756835355b"],"setPolarity":[11,"99cf6b8ca3b1854f35ccacb7a6134c2334a8ba796748e389dcbff0648c6f3106"],"setSwitchTime":[16,"8230f61088a45eebc80b500e579737bc42824385ecb633ee3799fc8fb5284d5a"],"setUseTime":[16,"14cdd83df5a99a5b39d424d15ab530141740c1e17afe79b2b7edc7938cc27701"],"shouldCauseReequipAnimation":[16,"3e00d35cc9b87936c41e5bc8d92b876c67d1df83ae7e0bef4a637ec674f56c60"],"use":[26,"ecdff4ab3bec4f7f57b488a358d7dc40ff72e2570625bbb81496b1929a060c8a"]}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","scope":"STATIC_DISCOVERY_ONLY"}
def selected(owner,name):
    return owner in ALL or name in SELECT.get(owner,set())
def window(rd,key,body,d):
    offsets=sorted(body)
    require(len(offsets)<=10000,"shared method budget")
    sites=[]
    for i,at in enumerate(offsets):
        op,arg,_=body[at]
        if op not in SELECT_OPS and op not in {"new","instanceof","checkcast"}:continue
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        require(match is not None,"typed operand")
        cp=int(match[1]);ref=rd.resolve(cp);tag=rd.pool[cp][0]
        target=ref[1] if tag in (9,10,11) else ref if tag==7 else None
        if target not in {ITEM,SOUND}:continue
        sites.append({"offset":at,"opcode":op,"reference":ref,"window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-12):i+13]]})
    require(0<len(sites)<=80,"typed consumer sites "+rd.name+"."+key[0])
    return {"name":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],"instruction_sha256":summarize(rd,key,body)["instruction_sha256"],"instruction_count":len(body),"projection":"RESISTOR_TYPED_WINDOWS_ONLY","sites":sites}
def inspect(jar,javap):
    verify_artifact(jar)
    out={};seen={}
    with ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)) and sum(x.endswith(".class") for x in paths)==1555,"publisher roster")
        for owner in sorted(ALL|set(SELECT)):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            require(owner!=ITEM or digest(raw)=="ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741","native class pin")
            decls=[d for d in rd.methods if selected(owner,d["name"])]
            require(0<len(decls)<=40 and SELECT.get(owner,set())<={d["name"] for d in decls},"owner scope "+owner)
            parsed=disassemble(jar,javap,owner);rows=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                require("code_sha256" in d and key in parsed and bool(parsed[key]),"body absent "+str(key))
                body=parsed[key]
                if owner==ITEM:
                    require(key[0] in NATIVE and key[0] not in seen,"native roster")
                    fp=[len(body),summarize(rd,key,body)["instruction_sha256"]]
                    require(fp==NATIVE[key[0]],"native instruction pin "+key[0]);seen[key[0]]=fp
                if (owner,key[0]) in WINDOWS:row=window(rd,key,body,d)
                else:
                    require(len(body)<=1600,"full projection budget")
                    row=projection(rd,key,body,d);row["projection"]="FULL_BOUNDED_SEMANTICS"
                row["executable"]=True;rows.append(row)
            out[owner]={"class_sha256":digest(raw),"methods":rows}
    require(seen==NATIVE,"all 20 native pins")
    require({"isValidItem","tickVolume"}<={m["name"] for m in out[SOUND]["methods"]},"sound methods")
    require(sum(len(x["methods"]) for x in out.values())<=100,"report method budget")
    return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size":SIZE},"classes":out,"limits":LIMITS}
def self_test():
    require(len(NATIVE)==20,"native roster")
    require(selected(ITEM,"onUseTick"),"native")
    require(selected(SOUND,"tickVolume"),"sound")
    require(selected(RENDER,"renderByItem"),"renderer")
    require(not selected(RENDER,"unrelated"),"bounded")
    require(not selected("foreign/ResistorShieldItem","onUseTick"),"owner")
    require((CLIENT,"playWorldSound") in WINDOWS,"dispatcher")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS eight scope checks")
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(),"write once")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode()
        require(len(raw)<=4000000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row["class_sha256"],"METHODS",len(row["methods"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
