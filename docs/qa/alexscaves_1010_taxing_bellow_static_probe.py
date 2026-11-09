#!/usr/bin/env python3
"""Read-only SHA-exact publisher 1.0.10 Taxing Bellow reputation/cost audit.

Never reimplement provider behavior or execute original mod code. Verify
bytecode offsets, digests, branch targets and bounded symbolic windows only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ID = "alexscaves:taxing_bellow"
ENCH = "data/alexscaves/enchantment/taxing_bellow.json"
TAG = "data/alexscaves/tags/item/enchantable/magic_conch.json"
LANG = "assets/alexscaves/lang/en_us.json"
CONCH = BASE + "server/item/MagicConchItem.class"
DEEP = BASE + "server/entity/living/DeepOneBaseEntity.class"
WORLD = BASE + "server/level/storage/ACWorldData.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
CLASSES = {
    CONCH: "4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2",
    DEEP: "185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470",
    WORLD: "ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5",
    REG: "60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32",
}
ENCH_SHA = "275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1"
TAG_SHA = "730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8"
METHODS = {
    CONCH: ("use", "getUseDuration", "releaseUsing", "summonDeepOne"),
    DEEP: ("addReputation", "getReputationOf", "setReputationOf",
           "setSummonedBy", "copyTarget", "addAdditionalSaveData",
           "readAdditionalSaveData"),
    WORLD: ("getDeepOneReputation", "setDeepOneReputation"),
}
SEALED_DIGESTS = {
    (CONCH, "releaseUsing"): "f8a7f97d8a15e513a06cf81e0c4cb2fde5fad9a100b1a3187a9ab4f4f9dd7894",
    (CONCH, "summonDeepOne"): "c355ab39634de12bb46dd45a2286aca99dcacd1843c98c80d4fe6723fbdf6d25",
    (DEEP, "setSummonedBy"): "af63ee72cd7a7cb9c6b4e4c18a505acabe91c29cee1eea133b71ebf13138c4eb",
}
PIVOTS = {
    "releaseUsing": ("TAXING_BELLOW:", "enchantLevel:", "Math.min:", "ItemStack.setDamageValue:",
                     "hurtAndBreakUsedHand:", "isClientSide:", "addReputation:", "addCooldown:",
                     "LASTING_MORALE:", "CHARTING_CALL:", "summonDeepOne:"),
    "addReputation": ("getReputationOf:", "setReputationOf:", "fromReputation:",
                      "getPlayerByUUID:", "displayClientMessage:"),
    "getReputationOf": ("ACWorldData.get:", "getDeepOneReputation:", "isClientSide:"),
    "setReputationOf": ("ACWorldData.get:", "setDeepOneReputation:", "isClientSide:"),
    "summonDeepOne": ("setSummonedBy:", "addFreshEntity:", "copyTarget:"),
    "getDeepOneReputation": ("deepOneReputation", "Map.get:", "Map.getOrDefault:"),
    "setDeepOneReputation": ("deepOneReputation", "setDirty:", "Map.put:"),
    "addAdditionalSaveData": ("ConchSummoned", "ConchTime", "ConchUUID"),
    "readAdditionalSaveData": ("ConchSummoned", "ConchTime", "ConchUUID"),
}
OFFSETS = {
    "releaseUsing": (20,25,39,41,45,48,51,54,55,57,60,61,62,65,68,69,71,
                     74,77,86,90,93,96,101,104,107,114,267,322,377,
                     397,399,402,404,407,410,413,415,418,422,448,451),
    "addReputation": (2,5,8,9,19,23,28,39,43,48,51,64,67,75,100,103),
    "getReputationOf": (4,7,14,19,22,26,28,31,32,33),
    "setReputationOf": (4,7,14,19,22,25,28),
    "summonDeepOne": (234,268,278,281,290,293,297,300,302,303,304),
    "setSummonedBy": (2,7,10,15),
}


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def small(row: dict) -> dict:
    return {k:row[k] for k in ("offset","opcode","operand","symbol")}


def choose(methods: list[dict], name: str) -> dict:
    hits = [m for m in methods if name_of(m) == name]
    require(len(hits)==1,"missing or ambiguous " + name)
    m=hits[0]
    ins=m["instructions"]
    require(1 <= len(ins) <= 2000 and
            [r["offset"] for r in ins]==sorted(set(r["offset"] for r in ins)),
            "bad instruction census "+name)
    return m


def check(m: dict, rules: dict[int,tuple[str,str|None,str|None]]) -> None:
    rows = {r["offset"]:r for r in m["instructions"]}
    for offset,(opcode,symbol,operand) in rules.items():
        r=rows.get(offset)
        require(r is not None and r["opcode"]==opcode and
                (symbol is None or symbol in r["symbol"]) and
                (operand is None or operand==r["operand"]),
                "SHA-exact JVM CFG drift "+name_of(m)+" @"+str(offset))


def verify_cfg(consumers: dict[str,dict[str,dict]]) -> dict:
    release=consumers[CONCH]["releaseUsing"]
    check(release, {
        20:("invokevirtual","playSound:",None),
        39:("bipush",None,"25"),
        41:("if_icmple",None,"451"),
        45:("getstatic","TAXING_BELLOW:",None),
        48:("invokestatic","ACCompat.enchantLevel:",None),
        51:("ifle",None,"74"),
        55:("iconst_0",None,None),
        57:("invokevirtual","ItemStack.getDamageValue:",None),
        60:("iconst_1",None,None),
        61:("isub",None,None),
        62:("invokestatic","Math.min:",None),
        65:("invokevirtual","ItemStack.setDamageValue:",None),
        68:("iconst_1",None,None),
        69:("istore",None,"6"),
        71:("goto",None,"80"),
        74:("aload_1",None,None),
        77:("invokestatic","ACCompat.hurtAndBreakUsedHand:",None),
        90:("getstatic","LASTING_MORALE:",None),
        93:("invokestatic","ACCompat.enchantLevel:",None),
        96:("sipush",None,"400"),
        101:("istore",None,"8"),
        104:("invokevirtual","isClientSide:",None),
        107:("ifne",None,"418"),
        397:("iload",None,"6"),
        399:("ifeq",None,"418"),
        402:("aload",None,"10"),
        404:("ifnull",None,"418"),
        410:("invokevirtual","getUUID:",None),
        413:("bipush",None,"-2"),
        415:("invokevirtual","DeepOneBaseEntity.addReputation:",None),
        418:("aload_3",None,None),
        422:("ifeq",None,"451"),
        448:("invokestatic","ACCompat.addCooldown:",None),
        451:("return",None,None),
    })
    rep=consumers[DEEP]["addReputation"]
    check(rep,{
        2:("invokevirtual","getReputationOf:",None),
        8:("iadd",None,None),
        9:("invokestatic","DeepOneReaction.fromReputation:",None),
        19:("invokevirtual","setReputationOf:",None),
        28:("if_acmpeq",None,"103"),
        36:("invokevirtual","getPlayerByUUID:",None),
        43:("ifnull",None,"103"),
        100:("invokestatic","ACCompat.displayClientMessage:",None),
    })
    get=consumers[DEEP]["getReputationOf"]
    check(get,{
        4:("invokevirtual","isClientSide:",None),
        7:("ifne",None,"32"),
        14:("invokestatic","ACWorldData.get:",None),
        19:("ifnonnull",None,"26"),
        22:("iconst_0",None,None),
        28:("invokevirtual","ACWorldData.getDeepOneReputation:",None),
        32:("iconst_0",None,None),
    })
    set_=consumers[DEEP]["setReputationOf"]
    check(set_,{
        4:("invokevirtual","isClientSide:",None),
        7:("ifne",None,"28"),
        14:("invokestatic","ACWorldData.get:",None),
        19:("ifnull",None,"28"),
        25:("invokevirtual","ACWorldData.setDeepOneReputation:",None),
    })
    summon=consumers[CONCH]["summonDeepOne"]
    check(summon,{
        234:("invokevirtual","setSummonedBy:",None),
        278:("invokevirtual","checkSpawnObstruction:",None),
        281:("ifeq",None,"303"),
        290:("invokevirtual","Level.addFreshEntity:",None),
        293:("pop",None,None),
        297:("invokevirtual","copyTarget:",None),
        302:("areturn",None,None),
        303:("aconst_null",None,None),
    })
    # Persisted world-level reputation is the actual clamped consumer, not
    # the visual reaction nor the item-durability argument.
    world_get=consumers[WORLD]["getDeepOneReputation"]
    check(world_get,{
        9:("getfield","deepOneReputations:",None),
        13:("iconst_0",None,None),
        17:("invokeinterface","Map.getOrDefault:",None),
        28:("ireturn",None,None),
    })
    world_set=consumers[WORLD]["setDeepOneReputation"]
    check(world_set,{
        1:("getfield","deepOneReputations:",None),
        6:("bipush",None,"-100"),
        8:("bipush",None,"100"),
        10:("invokestatic","Mth.clamp:",None),
        16:("invokeinterface","Map.put:",None),
        22:("return",None,None),
    })
    return {
        "physical_JAR":"SHA_EXACT_1.0.10_ONLY",
        "enchantment":"TAXING_BELLOW_level_positive",
        "use_condition":"charge>25 elapsed ticks; cast sound precedes guard",
        "cost_branch":"replace wear1 by ItemStack.setDamageValue(Math.min(0, getDamageValue()-1)), then flag local6=true",
        "bound_min_warning":"if damage=0, argument=-1 to setDamageValue; effective engine damage semantics NOT_VERIFIED",
        "server_reputation_guard":"if !Level.isClientSide and flag6 and last_nonnull_summon_local10 != null",
        "reputation_operation":"last_nonnull_summon.addReputation(summoner.getUUID(), -2) once after summon loops",
        "reputation_storage":"DeepOneBaseEntity.addReputation reads current via getReputationOf, writes current-2 via setReputationOf -> ACWorldData when server and data available",
        "acceptance_warning":"summonDeepOne returns non-null after addFreshEntity without inspecting its boolean",
        "cooldown":"Lasting Morale time=1200+400*level, passed to Item cooldown only after loops if summoner Player; independent of Taxing Bellow",
        "physical_qa":"NOT_TESTED",
        "mutating_hook":"NOT_VERIFIED",
        "mutation":"NO_MUTATION",
    }


def proof(m: dict, name: str) -> dict:
    ins=m["instructions"]
    positions={v["offset"]:i for i,v in enumerate(ins)}
    result=[]
    for off in OFFSETS.get(name,()):
        require(off in positions, "method offset disappeared "+name+" @"+str(off))
        i=positions[off]
        result.append({"at":off,"window":[small(x) for x in ins[max(0,i-2):i+4]]})
    refs=[]
    for tok in PIVOTS.get(name,()):
        matches=[i for i,x in enumerate(ins) if tok in x["symbol"]]
        require(len(matches)<=60,"unbounded symbolic pivot "+name+" "+tok)
        refs.append({"token":tok,"count":len(matches),
                     "samples":[{"at":ins[i]["offset"],
                                 "window":[small(x) for x in ins[max(0,i-3):i+5]]}
                                for i in matches[:2]]})
    require(len(result)<=46,"offset window budget exceeded")
    return {"header":m["header"],"descriptor":m["descriptor"],
            "instruction_count":len(ins),"parsed_method_sha256":digest_method(m),
            "fixed_Cfg_windows":result,"bounded_symbolic_pivots":refs}


def audit(jar:Path,javap_bin:str)->dict:
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "incorrect physical 1.0.10 JAR fingerprint")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR entry")
        for p in (ENCH,TAG,LANG,*CLASSES):
            require(p in names,"missing resource/class "+p)
        data={p:z.read(p) for p in (ENCH,TAG,LANG,*CLASSES)}
        hashes={p:sha(raw) for p,raw in data.items()}
        require(hashes[ENCH]==ENCH_SHA and hashes[TAG]==TAG_SHA,
                "enchantment resource or item tag drift")
        require(all(hashes[c]==v for c,v in CLASSES.items()),
                "classfile drift from existing exact Magic Conch / Deep One contract")
        resource=json.loads(data[ENCH]); tag=json.loads(data[TAG]); lang=json.loads(data[LANG])
        require(resource.get("description",{}).get("translate")=="enchantment.alexscaves.taxing_bellow",
                "wrong enchantment descriptor")
        require(resource.get("supported_items")=="#alexscaves:enchantable/magic_conch" and
                "alexscaves:magic_conch" in tag.get("values",[]),"wrong Conch item tag")
        classes=[name for name in names if name.startswith(BASE) and name.endswith(".class")]
        require(1000<=len(classes)<=3000,"publisher JAR class census outside limits")
        direct=sorted(c for c in classes if b"TAXING_BELLOW" in z.read(c))
        require(REG in direct and CONCH in direct and len(direct)<=12,
                "unresolved direct TAXING_BELLOW compiled consumers")
    selections={}
    for owner,names in METHODS.items():
        parsed=parse_methods(javap(javap_bin,jar,owner[:-6].replace("/",".")))
        picks={name:choose(parsed,name) for name in names}
        for name,m in picks.items():
            seal=SEALED_DIGESTS.get((owner,name))
            if seal:
                require(digest_method(m)==seal,"drift from already sealed full JVM method "+name)
        selections[owner]=picks
    semantics=verify_cfg(selections)
    result={
        "schema_version":1,"claim_scope":"TAXING_BELLOW_SHA_EXACT_STATIC_ONLY",
        "artifact":{"size_bytes":SIZE,"sha1":SHA1,"sha256":SHA256},
        "enchantment":{"path":ENCH,"size_bytes":len(data[ENCH]),"sha256":hashes[ENCH],"json":resource},
        "tag":{"path":TAG,"sha256":hashes[TAG],"json":tag},
        "locale":{"path":LANG,"sha256":hashes[LANG],
                  "keys":{k:v for k,v in lang.items() if "taxing_bellow" in k}},
        "classes":{k:{"sha256":hashes[k],
                      "selected_methods":{n:proof(m,n) for n,m in selections.get(k,{}).items()}}
                   for k in CLASSES},
        "direct_references":{"examined_classfiles":len(classes),
                             "TAXING_BELLOW":direct},
        "verified_static_semantics":semantics,
        "limits":{"world_data_mutation_runtime":"NOT_TESTED",
                  "ItemStack.setDamageValue_negative_argument":"NOT_TESTED",
                  "enchantment_effect_in_real_server":"NOT_TESTED",
                  "physical_qa":"NOT_TESTED",
                  "mutating_hook":"NOT_VERIFIED",
                  "mutation":"NO_MUTATION",
                  "external_datapacks":"NOT_VERIFIED",
                  "whole_provider_closed":False}
    }
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=audit(args.jar,args.javap)
    canonical=json.dumps(result,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    require(len(canonical.encode("utf8"))<=100000,
            "taxing bellow bounded evidence volume exceeded")
    if args.seal:
        require(json.loads(args.seal.read_text(encoding="utf8"))==result,
                "sha-exact Taxing Bellow static seal mismatch")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("TAXING_BELLOW_REPORT="+canonical)
    print("TAXING_BELLOW_JAR_AUDIT_READONLY_NO_MUTATION")


if __name__=="__main__":
    main()
