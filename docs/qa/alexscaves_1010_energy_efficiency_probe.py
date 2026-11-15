#!/usr/bin/env python3
"""SHA-exact Energy Efficiency 1.0.10 Raygun consumption discovery.

Read-only physical JAR audit; this discovery stage MUST NOT certify static
behavior or allow mutating hooks until the JVM branch and stack proof is sealed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_raygun_local_flow_probe import (
    CLASS, CLASS_SHA256, DESC, METHOD_SHA256, digest_method,
)
from alexscaves_1010_bouncy_ball_causal_probe import (
    branch_edges, method_switch_tables,
)

RES="data/alexscaves/enchantment/energy_efficiency.json"
TAG="data/alexscaves/tags/item/enchantable/raygun.json"
CLASS_REG="com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class"
CLASS_REG_SHA="60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32"
RESOURCE_SHAS={RES:"c5771a00e6dd2dd0a693369a110a943354b074dde27b9f3c9d1dcb4a8440cf3a",TAG:"8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d"}
CANONICAL_METHODS={
    "onUseTick":DESC,
    "hasCharge":"(Lnet/minecraft/world/item/ItemStack;)Z",
    "getCharge":"(Lnet/minecraft/world/item/ItemStack;)I",
    "setCharge":"(Lnet/minecraft/world/item/ItemStack;I)V",
}
PARENT_HASHES={
    "onUseTick":METHOD_SHA256,
    "hasCharge":"0b89217b97ca4f3d1c155c01b4170d1f0cb9141e4ee854ccf0c72892cd3b1db7",
    "getCharge":"c69c154524dbe4b4e46ed589438f7548cc39658305072a59b7c6a7dc9ec25baa",
    "setCharge":"cedf012dbfb8edf1ca2171c57001dc8937f2982e3755a156da058a74d260993e",
}
LIMITS={
    "individual_static_certificate":"STATIC_TECHNICAL_CATALOG_ONLY",
    "artifact":"EXACT_PUBLISHER_1.0.10",
    "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "effective_world_state":"NOT_TESTED",
    "network_authorization":"NOT_VERIFIED",
    "effective_charge_settlement":"NOT_TESTED",
}


# Selected causal gates are examined as a contiguous operand path. Full-method
# parser digest and full direct CFG separately pin all remaining instructions.
PIVOTS={
    3:("invokevirtual","getUseDuration:"),
    6:("iload","4"),8:("isub",""),9:("istore","5"),
    11:("bipush","15"),19:("if_icmpge","32"),
    22:("iload","5"),24:("i2f",""),25:("iload","6"),
    27:("i2f",""),28:("fdiv",""),29:("goto","33"),
    32:("fconst_1",""),33:("fstore","7"),
    139:("aload_3",""),140:("invokestatic","hasCharge:"),
    143:("ifne","210"),147:("invokevirtual","Level.isClientSide:"),
    150:("ifeq","168"),153:("new","UpdateItemTagMessage"),
    165:("invokestatic","sendMSGToServer:"),
    169:("invokevirtual","stopUsingItem:"),
    209:("return",""),
    211:("invokevirtual","Level.isClientSide:"),
    214:("ifeq","322"),
    246:("getstatic","ACEnchantmentRegistry.ENERGY_EFFICIENCY:"),
    249:("invokestatic","ACCompat.enchantLevel:"),
    252:("istore","15"),254:("iconst_2",""),
    255:("iload","15"),257:("i2f",""),
    258:("ldc_w","float 1.5f"),261:("fmul",""),
    262:("f2d",""),263:("invokestatic","Math.floor:"),
    266:("d2i",""),267:("iadd",""),268:("istore","16"),
    270:("fload","7"),272:("fconst_1",""),
    273:("fcmpl",""),274:("iflt","322"),
    277:("iload","5"),279:("iload","16"),
    281:("irem",""),282:("ifne","322"),
    285:("aload_2",""),286:("instanceof","Player"),
    289:("ifeq","302"),293:("checkcast","Player"),
    296:("invokevirtual","Player.isCreative:"),
    299:("ifne","322"),
    302:("aload_3",""),303:("invokestatic","getCharge:"),
    306:("istore","17"),309:("iload","17"),
    311:("iconst_1",""),312:("iadd",""),
    313:("sipush","1000"),
    316:("invokestatic","Math.min:"),
    319:("invokestatic","setCharge:"),
}
EXACT_ENCHANTMENT={
    "description":{"translate":"enchantment.alexscaves.energy_efficiency"},
    "supported_items":"#alexscaves:enchantable/raygun",
    "weight":10,
    "max_level":3,
    "min_cost":{"base":1,"per_level_above_first":5},
    "max_cost":{"base":41,"per_level_above_first":10},
    "anvil_cost":1,
    "slots":["mainhand"],
}
EXACT_TAG={"values":["alexscaves:raygun"]}

def verify_config(meta,tag):
    require(meta==EXACT_ENCHANTMENT and tag==EXACT_TAG,
            "publisher 1.0.10 Energy Efficiency metadata or item tag drift")

def check_pivots(method):
    by={i["offset"]:i for i in method["instructions"]}
    require(len(by)==len(method["instructions"]),"duplicate JVM offsets")
    for offset,(op,fragment) in PIVOTS.items():
        row=by.get(offset)
        require(row is not None and row["opcode"]==op and
                fragment in (row["operand"]+" "+row["symbol"]),
                "energy charge JVM causal pivot drift at offset "+str(offset))
    owners=[i["offset"] for i in method["instructions"]
            if "ACEnchantmentRegistry.ENERGY_EFFICIENCY:" in i["symbol"]]
    require(owners==[246],"unexpected Energy Efficiency reference population")

def verified_normal_levels():
    """Mathematical projection of the exact bytecode, not measured gameplay."""
    import math
    return {str(L):2+math.floor(float(L)*1.5) for L in range(4)}

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)

def unique_pairs(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,"duplicate JSON key "+k)
        result[k]=v
    return result

def digest(payload: bytes):
    return hashlib.sha256(payload).hexdigest()

def method_select(methods, name, desc):
    hits=[m for m in methods if m["descriptor"]==desc and
          re.search(r"\b"+re.escape(name)+r"\(",m["header"])]
    require(len(hits)==1,"missing/ambiguous native method "+name)
    return hits[0]

def windows(rows, start=180, end=365):
    """Bounded exact raw JVM instructions, not source code or game execution."""
    result=[{key:r[key] for key in ("offset","opcode","operand","symbol")}
            for r in rows if start<=r["offset"]<=end]
    require(25<len(result)<160,"unexpected charge-region instruction population")
    offsets=[r["offset"] for r in result]
    require(offsets==sorted(set(offsets)),"bad exact JVM offset ordering")
    return result

def audit(jar: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher 1.0.10 JAR fingerprint drift")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP member")
        required=[RES,TAG,CLASS,CLASS_REG]
        for name in required:
            require(name in names,"missing 1.0.10 provider resource: "+name)
        require(digest(arc.read(CLASS))==CLASS_SHA256 and
                digest(arc.read(CLASS_REG))==CLASS_REG_SHA,
                "publisher Raygun/registry compiled class drift")
        metadata=json.loads(arc.read(RES),object_pairs_hook=unique_pairs)
        tag=json.loads(arc.read(TAG),object_pairs_hook=unique_pairs)
        resource_hashes={name:digest(arc.read(name)) for name in (RES,TAG)}
        require(resource_hashes==RESOURCE_SHAS,"publisher resource hashes drift")
        verify_config(metadata,tag)
        token_owners=sorted(name for name in names
                           if name.startswith("com/github/alexmodguy/alexscaves/")
                           and name.endswith(".class")
                           and b"ENERGY_EFFICIENCY" in arc.read(name))
        require(token_owners==sorted([CLASS,CLASS_REG]),
                "unexpected compiled ENERGY_EFFICIENCY token owners")
    source=javap(javap_bin,jar,CLASS[:-6].replace("/","."))
    declared=parse_methods(source)
    require(len(declared)==26,"native Raygun declared method count drift")
    selected={}
    for name,desc in CANONICAL_METHODS.items():
        method=method_select(declared,name,desc)
        require(digest_method(method)==PARENT_HASHES[name],
                "prior exact Raygun JVM method identity mismatch: "+name)
        selected[name]=method
    on_tick=selected["onUseTick"]
    ins=on_tick["instructions"]
    require(len(ins)==523,"native Raygun onUseTick instruction count drift")
    refs=[r for r in ins if "ACEnchantmentRegistry.ENERGY_EFFICIENCY:" in r["symbol"]]
    require(len(refs)==1 and refs[0]["offset"]==246 and refs[0]["opcode"]=="getstatic",
            "unexpected Energy Efficiency lookup location")
    branches=branch_edges(on_tick,method_switch_tables(on_tick,source))
    require(len(branches)==57,"unexpected Raygun direct branch population")
    check_pivots(on_tick)
    charge_window=windows(ins)
    return {
        "schema_version":1,
        "scope":"READ_ONLY_ENERGY_EFFICIENCY_1010_CHARGE_REGION_DISCOVERY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class":{"path":CLASS,"sha256":CLASS_SHA256},
        "resources":resource_hashes,
        "resource_data":{"enchantment":metadata,"raygun_item_tag":tag},
        "token_owners":token_owners,
        "declared_methods":len(declared),
        "native_methods":{name:{"descriptor":CANONICAL_METHODS[name],
            "method_sha256":digest_method(m),"instructions":len(m["instructions"])}
            for name,m in selected.items()},
        "onUseTick_direct_branches":len(branches),
        "energy_consumption_contract":{
            "side":"CLIENT_BRANCH_IN_THIS_METHOD",
            "use_ticks_local":"getUseDuration(stack,null)-remainingUseTicks",
            "warmup_ticks":15,
            "period_formula":"2+floor(1.5*enchantLevel)",
            "periods_0_to_3":verified_normal_levels(),
            "event_guard":"use_ticks/15 >= 1; use_ticks % period == 0; noncreative Player or non-Player",
            "write":"setCharge(stack, min(getCharge(stack)+1, 1000))",
            "negative_level_minus_one_zero_divisor":True,
            "client_update_message_authorization":"NOT_VERIFIED",
        },
        "onUseTick_charge_window":charge_window,
        "onUseTick_entry_window":[{k:r[k] for k in ("offset","opcode","operand","symbol")} for r in ins if r["offset"]<=85],
        "onUseTick_precharge_window":[{k:r[k] for k in ("offset","opcode","operand","symbol")} for r in ins if 132<=r["offset"]<=216],
        "limits":LIMITS,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--seal",type=Path)
    a=p.parse_args()
    result=audit(a.jar,a.javap)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    if a.seal:
        sealed=json.loads(a.seal.read_text(encoding="utf8"),object_pairs_hook=unique_pairs)
        expected={
            "schema_version":1,"claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
            "artifact":result["artifact"],"class":result["class"],
            "resource_sha256":result["resources"],
            "compiled_token_owners":result["token_owners"],
            "onUseTick_sha256":result["native_methods"]["onUseTick"]["method_sha256"],
            "method_sha256":{name:item["method_sha256"] for name,item in result["native_methods"].items()},
            "onUseTick_direct_branches":result["onUseTick_direct_branches"],
            "energy_consumption_contract":result["energy_consumption_contract"],
            "full_report_sha256":digest(data.encode("utf8")),
            "limits":result["limits"],
        }
        require(sealed==expected,"individual Energy Efficiency SHA seal drift")
    a.output.write_text(data,encoding="utf8")
    print("ENERGY_EFFICIENCY_PUBLISHER_EXPLORATION")
    print("metadata="+json.dumps(result["resource_data"],sort_keys=True))
    print("resource_hashes="+json.dumps(result["resources"],sort_keys=True))
    print("token_owners="+json.dumps(result["token_owners"]))
    print("onUseTick_branches="+str(result["onUseTick_direct_branches"]))
    for label in ("onUseTick_entry_window","onUseTick_precharge_window","onUseTick_charge_window"):
        print("JVM_WINDOW="+label)
        for row in result[label]:
            print("@%d %s %s %s"%(row["offset"],row["opcode"],row["operand"],row["symbol"]))
    print("report_sha256="+digest(data.encode("utf8")))
    print("STATIC_ONLY_NO_MUTATION NOT_TESTED")

if __name__=="__main__":
    main()
