#!/usr/bin/env python3
"""Read-only full-method roster / bounded control evidence for Astral Transferring.

All authority comes from the installed SHA-exact publisher JAR and the existing
exact resource/selected-window seal. No decompilation output or implementation
is redistributed. The result is evidence for interoperability, NOT a mutator
API, physical QA, complete CFG/exception analysis or provider-level closure.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,BASE,javap,parse_methods,sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

OWNER=BASE+"server/item/TotemOfPossessionItem.class"
OWNER_SHA256="bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e"
SOURCE_SEAL="EXACT-ASTRAL-TRANSFERRING-1.0.10.json"
TRANSFER_DESC="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"
SYMBOLIC={"getstatic","putstatic","getfield","putfield","invokevirtual",
          "invokestatic","invokespecial","invokeinterface"}
NUMERIC={"iconst_m1","iconst_0","iconst_1","iconst_2","iconst_3","iconst_4",
         "iconst_5","bipush","sipush","ldc","ldc_w","ldc2_w",
         "irem","fcmpl","fcmpg","iadd","isub","fmul"}
HIGH_VALUE=("BoundEntity","ControllingEntity","TotemPossessed",
            "ASTRAL_TRANSFERRING","RESISTS_TOTEM_OF_POSSESSION",
            "setPossessed","getControlledEntity","getBoundEntityUUID",
            "updateEntityIdFromServer","setTag","serializeEntity",
            "getPersistentData","getEntity","stopUsingItem",
            "releaseUsing","ACCompat","getHealth","setLastHurtByMob",
            "setTarget","getLook","LivingEntity.attack","Player.attack")
GUARDS={
    883:("iconst_4",""),884:("irem",""),885:("ifne","1081"),
    890:("invokevirtual","getHealth"),895:("invokevirtual","getHealth"),
    898:("fcmpl",""),899:("ifle","1081"),
    910:("getstatic","RESISTS_TOTEM_OF_POSSESSION"),
    916:("ifne","1081"),920:("getstatic","ASTRAL_TRANSFERRING"),
    923:("invokestatic","enchantLevel"),926:("ifle","1081"),
    932:("invokestatic","setPossessed"),943:("ldc_w","BoundEntityUUID"),
    951:("invokestatic","putUUID"),956:("invokestatic","serializeEntity"),
    987:("ldc_w","BoundEntityTag"),999:("invokestatic","setTag"),
    1048:("invokestatic","updateEntityIdFromServer")
}

def require(ok,reason):
    if not ok:raise ValueError(reason)

def digest(raw:bytes):
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    data={}
    for k,v in pairs:
        require(k not in data,"duplicate JSON key: "+k)
        data[k]=v
    return data

def exact_method(methods,name,desc=None):
    hits=[m for m in methods if name_of(m)==name and (desc is None or m["descriptor"]==desc)]
    require(len(hits)==1,"missing or ambiguous method "+name)
    return hits[0]

def instruction_order(method):
    xs=method["instructions"]
    offs=[x["offset"] for x in xs]
    require(len(xs)<=1200 and offs==sorted(set(offs)),"invalid or oversized JVM method")
    return xs

def branch_target(x):
    op=x["opcode"]
    if not (op.startswith("if") or op.startswith("goto") or op in ("jsr","jsr_w")):
        return None
    v=x["operand"].split()[0] if x["operand"] else ""
    return int(v) if v.lstrip("-").isdigit() else None

def method_summary(m):
    xs=instruction_order(m)
    branches=[]
    relevant=[]
    for x in xs:
        target=branch_target(x)
        if target is not None:
            branches.append({"offset":x["offset"],"opcode":x["opcode"],
                             "target":target,"is_back_edge":target<=x["offset"]})
        if x["opcode"] in SYMBOLIC and any(s in x["symbol"] for s in HIGH_VALUE):
            relevant.append({k:x[k] for k in ("offset","opcode","symbol")})
    require(len(branches)<=250 and len(relevant)<=180,"unbounded control summary")
    return {"name":name_of(m),"descriptor":m["descriptor"],
            "parsed_method_sha256":digest_method(m),
            "instruction_count":len(xs),"branch_count":len(branches),
            "branches":branches,"relevant_references":relevant}

def transfer_region(m):
    xs=instruction_order(m)
    by={x["offset"]:x for x in xs}
    require(len(xs)==478 and m["descriptor"]==TRANSFER_DESC,
            "unexpected native onUseTick definition")
    for offset,(opcode,token) in GUARDS.items():
        row=by.get(offset)
        require(row is not None and row["opcode"]==opcode and
                token in (row["operand"]+" "+row["symbol"]),
                "Astral transfer exact JVM pivot drift @"+str(offset))
    selected=[{"offset":x["offset"],"opcode":x["opcode"],
               "operand":x["operand"],"symbol":x["symbol"]}
              for x in xs if 700<=x["offset"]<=1100 and (
                  x["opcode"] in SYMBOLIC or x["opcode"] in NUMERIC or
                  branch_target(x) is not None)]
    require(45<=len(selected)<=225,"unexpected transfer region size")
    outgoing=[x for x in selected if x["opcode"].startswith("if") and
              x["operand"].split()[0].lstrip("-").isdigit()]
    require(any(x["offset"]==926 and int(x["operand"])==1081 for x in outgoing),
            "missing reject branch")
    return {"window":[700,1100],"pinned_instructions":len(selected),
            "anchors":selected,
            "claim":"SELECTED_COMPLETE_CONSUMER_METHOD_PLUS_LOCAL_BRANCH_OFFSETS_NOT_EXECUTED_CFG"}

def audit(jar:Path,javap_bin:str,seal:Path):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "installed publisher JAR SHA1/SHA256/size mismatch")
    old=json.loads(seal.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
    require(old["artifact"]=={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE}
            and old["consumer"]["instruction_count"]==478
            and old["owner"]["class"]==OWNER,
            "existing Astral publisher seal mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)) and OWNER in names,
                "duplicate ZIP entry / missing native class")
        class_sha=digest(z.read(OWNER))
        require(class_sha==OWNER_SHA256==old["owner"]["sha256"],
                "native Totem class fingerprint drift")
    methods=parse_methods(javap(javap_bin,jar,OWNER[:-6].replace("/",".")))
    require(len(methods)==old["owner"]["parsed_methods"]==22,
            "native declared Totem method roster changed")
    identities=[(name_of(m),m["descriptor"]) for m in methods]
    require(len(set(identities))==22,"duplicate native method descriptor")
    native=exact_method(methods,"onUseTick",TRANSFER_DESC)
    require(digest_method(native)==old["consumer"]["parsed_method_sha256"],
            "native consumer parse drift")
    summary=[method_summary(m) for m in methods]
    symbols={m["name"] for m in summary}
    for name in ("onUseTick","setPossessed","updateEntityIdFromServer",
                 "getBoundEntityUUID","use","releaseUsing","acHurtEnemy"):
        require(name in symbols,"missing Totem lifecycle method "+name)
    return {"schema_version":1,
            "scope":"ASTRAL_TRANSFER_NATIVE_TOTEM_22_METHOD_ROSTER_AND_CONTROL_EDGES",
            "artifact":old["artifact"],
            "owner":{"class":OWNER,"sha256":class_sha,"methods":len(methods)},
            "source_seal":{"path":str(seal).replace("\\","/"),
                           "consumer_digest":old["consumer"]["parsed_method_sha256"]},
            "methods":summary,
            "astral_transfer_region":transfer_region(native),
            "limits":{"executed_cfg_and_exception_paths":"NOT_RECONSTRUCTED",
                      "runtime_transformations":"NOT_VERIFIED",
                      "complete_world_state_and_prior_marker_cleanup":"NOT_VERIFIED",
                      "server_ownership_and_replay":"NOT_VERIFIED",
                      "effective_pack_datapacks":"NOT_VERIFIED",
                      "mutating_hook":"NOT_VERIFIED",
                      "physical_qa":"NOT_TESTED","certification":"PARTIAL",
                      "mutation":"NO_MUTATION"}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True,type=Path)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--seal",required=True,type=Path)
    ap.add_argument("--snapshot",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    data=audit(args.jar,args.javap,args.seal)
    if args.snapshot:
        saved=json.loads(args.snapshot.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        require(saved==data,"ASTRAL LIFECYCLE SEALED SNAPSHOT DRIFT")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("ASTRAL_LIFECYCLE_METHODS="+json.dumps([
          {"name":m["name"],"descriptor":m["descriptor"],
           "instructions":m["instruction_count"],"branches":m["branch_count"],
           "digest":m["parsed_method_sha256"]} for m in data["methods"]],
          separators=(",",":"),ensure_ascii=False))
    print("ASTRAL_LIFECYCLE_TRANSFER="+json.dumps(data["astral_transfer_region"],
          separators=(",",":"),ensure_ascii=False))
    print("ASTRAL_LIFECYCLE_SEAL","VERIFIED" if args.snapshot else "DISCOVERY",
          "METHODS",len(data["methods"]),"NO_MUTATION")
if __name__=="__main__":
    main()
