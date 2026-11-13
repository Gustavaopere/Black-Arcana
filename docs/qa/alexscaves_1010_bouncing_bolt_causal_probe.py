#!/usr/bin/env python3
"""SHA-exact read-only Sea Staff / Water Bolt ricochet causal audit, release 1.0.10.

Inspects all declared methods of the two audited classes, including constructors
and save/load, plus complete (parsed) branch edges in three direct consumers.
Output is a bounded symbolic-interoperability manifest, never vendor code or a
runtime mutation/physical QA claim. Parent sealed binary is hard authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_bouncing_bolt_probe import SEA_STAFF,WATER_BOLT,SELECTORS,require
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file,javap,parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

WATCH=("ricochet","Ricochet","Bouncing","getOwner","isAlliedTo",
       "getEntitiesOfClass","getArcingTowards","setArcingTowards",
       "addFreshEntity","hurt","damageMobs","onHitEntity","onHitBlock",
       "Bubbling","seekAmount","dieIn","readAdditionalSaveData",
       "addAdditionalSaveData","setDeltaMovement","copyPosition",
       "onProjectileImpact","setOwner","canHitEntity","getTarget",
       "EntityType","getPersistentData","getSynchedData","tickCount",
       "getItemInHand","TRIPLE_SPLASH","ENVELOPING_BUBBLE",
       "SOAK_SEEKING","BOUNCING_BOLT")
BRANCH_PREFIX=("if","goto")
BRANCH_UNSUPPORTED={"tableswitch","lookupswitch","jsr","jsr_w","ret"}
SYM_PREFIX=("invoke","getfield","putfield","getstatic","putstatic")
NUMERICS={"ldc","ldc_w","ldc2_w","bipush","sipush","fconst_0","fconst_1",
          "fconst_2","dconst_0","dconst_1","iconst_m1","iconst_0","iconst_1",
          "iconst_2","iconst_3","iconst_4","iconst_5"}
TARGET_NAMES=("use","damageMobs","onRicochetHit")
REQUIRED={
    "use":{299:("getstatic","BOUNCING_BOLT"),
           302:("invokestatic","enchantLevel"),
           305:("ifle","314"),
           310:("iconst_1",""),
           311:("putfield","ricochet")},
    "damageMobs":{139:("invokestatic","hurt"),
                  142:("ifeq","216"),
                  220:("getfield","ricochet"),
                  223:("ifeq","242"),
                  233:("putfield","ricochet"),
                  239:("invokevirtual","onRicochetHit")},
    "onRicochetHit":{1:("invokevirtual","getOwner"),
                    9:("ldc2_w","32.0"),
                    12:("ldc2_w","32.0"),
                    15:("ldc2_w","32.0"),
                    32:("invokevirtual","getEntitiesOfClass"),
                    119:("ldc2_w","3.0"),
                    156:("ifnull","270"),
                    163:("ifeq","270"),
                    182:("invokespecial","WaterBoltEntity"),
                    190:("invokevirtual","copyPosition"),
                    200:("invokevirtual","setArcingTowards"),
                    209:("ldc","0.3"),
                    248:("invokevirtual","setDeltaMovement"),
                    254:("invokevirtual","isBubbling"),
                    257:("invokevirtual","setBubbling"),
                    266:("invokevirtual","addFreshEntity")}
}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,"duplicate JSON field "+k)
        out[k]=v
    return out

def validate_method(method):
    instructions=method["instructions"]
    offsets=[r["offset"] for r in instructions]
    require(1<=len(instructions)<=1900 and offsets==sorted(set(offsets)),
            "unsorted, duplicate or oversized JVM method")
    return instructions

def edges(method):
    rows=validate_method(method)
    valid={r["offset"] for r in rows}
    out=[]
    for i,r in enumerate(rows):
        opcode=r["opcode"]
        require(opcode not in BRANCH_UNSUPPORTED,"unsupported JVM control primitive")
        if not opcode.startswith(BRANCH_PREFIX): continue
        word=r["operand"].split()[0] if r["operand"] else ""
        require(word.lstrip("-").isdigit(),"unknown JVM branch target")
        target=int(word)
        require(target in valid,"JVM branch destination absent")
        entry={"offset":r["offset"],"opcode":opcode,
               "target":target,"back_edge":target<=r["offset"]}
        if opcode.startswith("if"):
            require(i+1<len(rows),"conditional branch ends method")
            entry["fallthrough"]=rows[i+1]["offset"]
        out.append(entry)
    require(len(out)<=180,"too many branches in consumer")
    return out

def exact_pivots(m,name):
    rows=validate_method(m)
    by={x["offset"]:x for x in rows}
    out=[]
    for offset,(opcode,needle) in REQUIRED[name].items():
        row=by.get(offset)
        require(row and row["opcode"]==opcode and
                needle in (row["operand"]+" "+row["symbol"]),
                "Bouncing Bolt causal pivot drift "+name+" @"+str(offset))
        out.append({k:row[k] for k in ("offset","opcode","operand","symbol")})
    return out

def roster(methods):
    out=[]
    identities=set()
    for method in methods:
        name=name_of(method)
        key=(name,method["descriptor"])
        require(key not in identities,"duplicate method identity")
        identities.add(key)
        rows=validate_method(method)
        relevant=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
                  for r in rows if r["opcode"].startswith(SYM_PREFIX) and
                  any(token.lower() in r["symbol"].lower() for token in WATCH)]
        require(len(relevant)<=135,"too many class references")
        out.append({"name":name,"descriptor":method["descriptor"],
                    "instruction_count":len(rows),
                    "parsed_method_sha256":digest_method(method),
                    "relevant_symbolic_refs":relevant})
    require(2<=len(out)<=90,"unexpected complete class method count")
    return out

def full_consumer(method,owner):
    name=name_of(method)
    rows=validate_method(method)
    symbols=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
             for r in rows if r["opcode"].startswith(SYM_PREFIX)]
    values=[{k:r[k] for k in ("offset","opcode","operand","symbol")}
            for r in rows if r["opcode"] in NUMERICS]
    require(len(symbols)<=260 and len(values)<=190,"unbounded consumer symbols")
    return {"owner":owner,"name":name,"descriptor":method["descriptor"],
            "parsed_method_sha256":digest_method(method),
            "instruction_count":len(rows),
            "all_branch_edges":edges(method),
            "all_symbolic_calls_and_fields":symbols,
            "all_literal_operands":values,
            "verified_pivots":exact_pivots(method,name)}

def audit(jar:Path,manifest:Path,javap_bin:str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher JAR SHA1/SHA256/size drift")
    parent=json.loads(manifest.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
    require(parent["artifact"]=={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE}
            and parent["enchantment"]["id"]=="alexscaves:bouncing_bolt"
            and len(parent["consumers"])==3,"wrong parent publisher manifest")
    expected={row["path"]:row["sha256"] for row in parent["classes"]}
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP entries")
        actual={klass:digest(z.read(klass)) for klass in (SEA_STAFF,WATER_BOLT)}
    require(actual==expected,"publisher class SHA mismatch")
    all_methods={}
    rosters={}
    for klass in (SEA_STAFF,WATER_BOLT):
        methods=parse_methods(javap(javap_bin,jar,klass[:-6].replace("/",".")))
        rosters[klass]=roster(methods)
        all_methods[klass]=methods
    selected=[]
    for old in parent["consumers"]:
        owner=old["owner"]
        name=old["method"]["name"]
        desc=old["method"]["descriptor"]
        require(owner in all_methods and name in TARGET_NAMES,"unexpected parent method")
        found=[m for m in all_methods[owner] if
               name_of(m)==name and m["descriptor"]==desc]
        require(len(found)==1,"ambiguous/missing parent consumer")
        m=found[0]
        require(digest_method(m)==old["method"]["parsed_method_sha256"] and
                len(m["instructions"])==old["method"]["instruction_count"],
                "parent method parse drift")
        selected.append(full_consumer(m,owner))
    require(len(selected)==3 and {x["name"] for x in selected}==set(TARGET_NAMES),
            "native causal consumer set drift")
    # Deny any undeclared field writers/consumers if outside the audited classes;
    # this is an intra-class roster only, not a cross-JAR universe proof.
    return {"schema_version":1,
            "scope":"BOUNCING_BOLT_NATIVE_RICOCHET_FULL_METHOD_BRANCHES_AND_CLASS_ROSTERS",
            "authority":"EXACT_PUBLISHER_1.0.10_READ_ONLY",
            "artifact":parent["artifact"],
            "parent_manifest_sha256":digest(manifest.read_bytes()),
            "classes":[{"path":p,"sha256":actual[p],
                        "declared_method_count":len(rosters[p]),
                        "methods":rosters[p]} for p in (SEA_STAFF,WATER_BOLT)],
            "consumers":selected,
            "limits":{"full_interprocedural_cfg_and_exceptions":"NOT_RECONSTRUCTED",
                      "external_mixin_and_cross_jar_consumers":"NOT_VERIFIED",
                      "live_damage_acceptance":"NOT_VERIFIED",
                      "child_spawn_success":"NOT_TESTED",
                      "owner_reload_persistence":"NOT_VERIFIED",
                      "actual_datapacks_and_pvp_claims":"NOT_VERIFIED",
                      "mutating_hook":"NOT_VERIFIED",
                      "physical_qa":"NOT_TESTED",
                      "certification":"PARTIAL",
                      "mutation":"NO_MUTATION"}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--snapshot",type=Path)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--javap",default="javap")
    args=ap.parse_args()
    data=audit(args.jar,args.manifest,args.javap)
    if args.snapshot:
        saved=json.loads(args.snapshot.read_text(encoding="utf8"),
                         object_pairs_hook=strict_pairs)
        require(saved==data,"Bouncing Bolt causal snapshot drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf8")
    if not args.snapshot:
        print("BOUNCING_BOLT_CAUSAL_JSON="+json.dumps(data,separators=(",",":"),
                                                    ensure_ascii=False))
    print("BOUNCING_BOLT_CAUSAL_STATUS",
          "SEALED" if args.snapshot else "DISCOVERY",
          "CONSUMERS",len(data["consumers"]),
          "METHODS",sum(x["declared_method_count"] for x in data["classes"]),
          "NO_MUTATION")
if __name__=="__main__":
    main()
