#!/usr/bin/env python3
"""Read-only causal audit of Charting Call in exact Alex's Caves 1.0.10.

Reconciles the already pinned Charting Call manifest with the exact publisher
JAR, enumerates both involved class method rosters, validates direct JVM branch
destinations (including switch cases), and proves the call order/bound formulas
without copying provider code or asserting physical gameplay outcomes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_charting_call_probe import (
    CONCH, DEEP_ONE, CLASSES, SELECTORS, HASHES, ENCHANTMENTS,
    require, find_method,
)
from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges, method_switch_tables

REQUIRED = {
    "releaseUsing": {
        41: ("if_icmple", "451"), 62: ("invokestatic", "Math.min:"),
        104: ("invokevirtual", "isClientSide:"),
        107: ("ifne", "418"),
        111: ("getstatic", "CHARTING_CALL:"),
        114: ("invokestatic", "enchantLevel:"),
        126: ("invokeinterface", "RandomSource.nextInt:"),
        138: ("invokeinterface", "RandomSource.nextInt:"),
        150: ("invokeinterface", "RandomSource.nextInt:"),
        160: ("ifle", "223"),
        172: ("invokestatic", "Math.max:"),
        175: ("invokeinterface", "RandomSource.nextInt:"),
        192: ("invokestatic", "Math.max:"),
        195: ("invokeinterface", "RandomSource.nextInt:"),
        212: ("invokestatic", "Math.max:"),
        215: ("invokeinterface", "RandomSource.nextInt:"),
        267: ("invokevirtual", "summonDeepOne:"),
        322: ("invokevirtual", "summonDeepOne:"),
        377: ("invokevirtual", "summonDeepOne:"),
        415: ("invokevirtual", "addReputation:"),
        448: ("invokestatic", "addCooldown:"),
    },
    "summonDeepOne": {
        234: ("invokevirtual", "setSummonedBy:"),
        268: ("invokestatic", "finalizeSpawn:"),
        278: ("invokevirtual", "checkSpawnObstruction:"),
        290: ("invokevirtual", "addFreshEntity:"),
        297: ("invokevirtual", "copyTarget:"),
    },
    "setSummonedBy": {
        15: ("invokevirtual", "setSummonTime:"),
    },
    "tick": {
        227: ("invokevirtual", "isClientSide:"),
        240: ("invokevirtual", "setSummonTime:"),
        311: ("invokevirtual", "remove:"),
    },
}
# Full 1.0.10 JVM opcodes for the three level>0 bounded-RNG expressions.
RNG = {
    "deep_one": {
        167: "iload", 169: "iconst_1", 170: "isub",
        171: "iconst_2", 172: "invokestatic", 175: "invokeinterface",
        180: "iadd", 181: "istore"
    },
    "knight": {
        187: "iload", 189: "iconst_2", 190: "isub",
        191: "iconst_0", 192: "invokestatic", 195: "invokeinterface",
        200: "iadd", 201: "istore"
    },
    "mage": {
        207: "iload", 209: "iconst_3", 210: "isub",
        211: "iconst_0", 212: "invokestatic", 215: "invokeinterface",
        220: "iadd", 221: "istore"
    },
}
NBT_METHODS=("addAdditionalSaveData","readAdditionalSaveData")
RELATED={
    CONCH:("use","getUseDuration"),
    DEEP_ONE:("copyTarget","isAlliedTo","getReactionTo",*NBT_METHODS),
}
MONITOR=("ConchSummoned","ConchUUID","ConchTime",
         "addFreshEntity","getLastHurtMob","getLastHurtByMob",
         "summonerUUID","summonTime","setSummonTime","getSummonTime",
         "isAlliedTo","getUUID","isClientSide","setSummonedBy",
         "getTarget","getOwner","copyTarget","isEffectiveAi")

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def unique_pairs(pairs):
    out={}
    for key,val in pairs:
        require(key not in out,"duplicate JSON key "+key)
        out[key]=val
    return out

def strict_method(method):
    rows=method["instructions"]
    offsets=[r["offset"] for r in rows]
    require(1<=len(rows)<=3000 and offsets==sorted(set(offsets)),
            "unsorted, duplicate or out-of-range JVM offsets")
    return rows

def exact_pivots(method,name):
    positions={i["offset"]:i for i in strict_method(method)}
    out=[]
    for offset,(opcode,token) in REQUIRED[name].items():
        row=positions.get(offset)
        require(row is not None and row["opcode"]==opcode and
                token in (row["opcode"]+" "+row["operand"]+" "+row["symbol"]),
                "Charting Call causal pivot drift: "+name+" @"+str(offset))
        out.append({k:row[k] for k in ("offset","opcode","operand","symbol")})
    return out

def rng_bounds(method):
    positions={i["offset"]:i for i in strict_method(method)}
    output={}
    for family,points in RNG.items():
        xs=[]
        for offset,opcode in points.items():
            row=positions.get(offset)
            require(row is not None and row["opcode"]==opcode,
                    "Charting Call bounded RNG opcode drift "+family+" @"+str(offset))
            xs.append({k:row[k] for k in ("offset","opcode","operand","symbol")})
        require("Math.max:" in xs[4]["symbol"] and
                "RandomSource.nextInt:" in xs[5]["symbol"],
                "missing max-to-nextInt adjacency")
        output[family]=xs
    return output

def bounded_nbt(methods):
    result={}
    for method_name in NBT_METHODS:
        rows=[m for m in methods if name_of(m)==method_name]
        require(len(rows)==1,"missing or duplicate Deep One NBT method")
        method=rows[0]
        symbols=" ".join(row["symbol"] for row in strict_method(method))
        require(all(x in symbols for x in ("ConchSummoned","ConchUUID","ConchTime")),
                "missing native Conch summon save/load key")
        refs=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
              for r in method["instructions"] if r["opcode"].startswith(
                  ("invoke","getfield","putfield","getstatic")) and
                  any(w.lower() in r["symbol"].lower() for w in MONITOR)]
        require(len(refs)<=90,"too many NBT references")
        result[method_name]={"instruction_count":len(method["instructions"]),
                             "parsed_method_sha256":digest_method(method),
                             "required_nbt_keys":["ConchSummoned","ConchUUID","ConchTime"],
                             "selected_refs":refs}
    return result

def method_roster(methods):
    out=[]
    keys=set()
    for method in methods:
        name=name_of(method)
        key=(name,method["descriptor"])
        require(key not in keys,"duplicate method descriptor in owner class")
        keys.add(key)
        rows=strict_method(method)
        out.append({"name":name,"descriptor":method["descriptor"],
                    "instruction_count":len(rows),
                    "parsed_method_sha256":digest_method(method)})
    require(2<=len(out)<=350,"unexpected owner method roster length")
    return out

def additional(methods,names):
    result=[]
    for name in names:
        hits=[m for m in methods if name_of(m)==name]
        require(len(hits)==1,"missing/ambiguous native related method "+name)
        method=hits[0]
        rows=strict_method(method)
        selected=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
                  for r in rows if r["opcode"].startswith(
                      ("invoke","getfield","putfield","getstatic")) and
                      any(w.lower() in r["symbol"].lower() for w in MONITOR)]
        require(len(selected)<=125,"unbounded selected related method refs")
        result.append({"name":name,"descriptor":method["descriptor"],
                       "instruction_count":len(rows),
                       "parsed_method_sha256":digest_method(method),
                       "selected_refs":selected})
    return result

def native_consumer(method,owner,javap_text):
    name=name_of(method)
    rows=strict_method(method)
    switches=method_switch_tables(method,javap_text)
    edges=branch_edges(method,switches)
    symbols=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
             for r in rows if r["opcode"].startswith(
                 ("invoke","getfield","putfield","getstatic"))]
    require(len(symbols)<=300,"unbounded direct JVM symbolic refs")
    result={"owner":owner,"name":name,"descriptor":method["descriptor"],
            "instruction_count":len(rows),
            "parsed_method_sha256":digest_method(method),
            "direct_branch_edges":edges,
            "verified_switch_tables":switches,
            "symbolic_call_and_field_refs":symbols,
            "verified_causal_pivots":exact_pivots(method,name)}
    if name=="releaseUsing":
        result["verified_rng_bound_sequences"]=rng_bounds(method)
    return result

def audit(jar:Path,parent_path:Path,javap_bin:str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "wrong publisher artifact SHA1/SHA256/size")
    parent_bytes=parent_path.read_bytes()
    parent=json.loads(parent_bytes,object_pairs_hook=unique_pairs)
    require(parent["artifact"]=={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "pinned parent artifact drift")
    require(parent["resource_evidence"]["charting_call"]["json"]["max_level"]==4,
            "wrong Charting Call max level")
    require({x["path"]:x["sha256"] for x in parent["owner_classes"]}==CLASSES,
            "wrong classfile roster in parent seal")
    require({k:x["sha256"] for k,x in parent["resource_evidence"].items()}==HASHES,
            "wrong publisher resource roster in parent seal")
    with zipfile.ZipFile(jar) as z:
        members=z.namelist()
        require(len(members)==len(set(members)),
                "duplicate native publisher JAR entries")
        require(all(digest(z.read(owner))==sha for owner,sha in CLASSES.items()),
                "parent classfile SHA-256 changed")
        direct_token=sorted(p for p in members if p.endswith(".class") and
                            b"CHARTING_CALL" in z.read(p))
    require(1<=len(direct_token)<=12 and CONCH in direct_token,
            "unexpected cross-owner CHARTING_CALL class-token discovery")
    rosters=[]
    methods={}
    raw={}
    for owner in (CONCH,DEEP_ONE):
        raw[owner]=javap(javap_bin,jar,owner[:-6].replace("/","."))
        methods[owner]=parse_methods(raw[owner])
        entries=method_roster(methods[owner])
        rosters.append({"path":owner,"sha256":CLASSES[owner],
                        "declared_method_count":len(entries),
                        "methods":entries})
    core=[]
    for old in parent["selected_consumers"]:
        owner=old["owner"]
        name=old["method"]["name"]
        desc=old["method"]["descriptor"]
        require(owner in methods and name in REQUIRED,
                "unexpected parent causal consumer")
        m=find_method(methods[owner],name,desc)
        require(digest_method(m)==old["method"]["parsed_method_sha256"] and
                len(m["instructions"])==old["method"]["instruction_count"],
                "parent selected method digest drift")
        core.append(native_consumer(m,owner,raw[owner]))
    require(len(core)==4 and {r["name"] for r in core}==set(REQUIRED),
            "missing unique root consumer")
    extras=[]
    for owner,names in RELATED.items():
        extras.append({"owner":owner,"methods":additional(methods[owner],names)})
    save_load=bounded_nbt(methods[DEEP_ONE])
    # The native RNG derives zero-allowing Math.max(...,0) bounds for Knights
    # and Mages. This statically proves the argument, NOT exception behavior.
    return {
        "schema_version":1,
        "scope":"CHARTING_CALL_NATIVE_JVM_DIRECT_BRANCHES_RNG_AND_OWNER_STATE",
        "authority":"EXACT_PUBLISHER_1.0.10_READ_ONLY",
        "artifact":parent["artifact"],
        "parent_manifest_sha256":digest(parent_bytes),
        "direct_class_token_CHARTING_CALL":direct_token,
        "owner_method_rosters":rosters,
        "core_consumers":core,
        "related_native_methods":extras,
        "summon_nbt_overrides":save_load,
        "limits":{
            "full_interprocedural_exception_flow":"NOT_RECONSTRUCTED",
            "RandomSource_nextInt_zero_runtime_result":"NOT_TESTED",
            "actual_spawn_insertion_and_reputation":"NOT_TESTED",
            "other_jar_mixins_and_datapacks":"NOT_VERIFIED",
            "server_client_physical_qa":"NOT_TESTED",
            "provider_universe_closed":False,
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "certification":"STATIC_TECHNICAL_CATALOG_ONLY",
        },
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--parent",type=Path,required=True)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--snapshot",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=audit(args.jar,args.parent,args.javap)
    if args.snapshot:
        old=json.loads(args.snapshot.read_bytes(),object_pairs_hook=unique_pairs)
        require(result==old,"Charting Call causal snapshot drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf8")
    print("CHARTING_CALL_CAUSAL="+json.dumps(result,ensure_ascii=False,
                                             separators=(",",":")))
if __name__=="__main__":
    main()
