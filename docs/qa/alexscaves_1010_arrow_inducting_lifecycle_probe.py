#!/usr/bin/env python3
"""Read-only SHA-exact lifecycle census for Arrow Inducting (1.0.10).

Method fingerprints, direct JVM callsites and branch offsets, not vendor code,
runtime behavior, a complete CFG, a mutating hook or physical acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, sha_file, javap, parse_methods)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

EVENT=BASE+"server/event/CommonEvents.class"
ARROW=BASE+"server/entity/item/SeekingArrowEntity.class"
RESOURCE="data/alexscaves/enchantment/arrow_inducting.json"
EXPECTED={EVENT:("d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43",34),
          ARROW:("1102754436829c3dcadb1450d6ab15efb354a3f4e58a2a262a78c5013d7f0e25",12)}
EVENT_HASH="3b6a9d9699a101ff2c4aa61dc08308857a1480fdd11f711c5ce04e2638244368"
TICK_HASH="eb936d76c3fbdcf1be042312dd7dba664af91244529443c7806aa6a4a2c7e152"
RESOURCE_HASH="80d52e42318ad732b32ba6118dea8f5b315b8d2d702da32d202ff95246a973e5"

def require(ok,reason):
    if not ok: raise ValueError(reason)

def compact(row):
    return {k:row[k] for k in ("offset","opcode","operand","symbol")}

def summarize(method):
    ins=method["instructions"]
    offsets=[x["offset"] for x in ins]
    require(len(ins)<=1200 and offsets==sorted(set(offsets)),
            "bad bounds, order, or duplicate JVM offsets")
    refs=[compact(x) for x in ins if x["opcode"].startswith("invoke") or
          x["opcode"] in ("getfield","putfield","getstatic","putstatic")]
    branches=[compact(x) for x in ins if x["opcode"].startswith("if") or
              x["opcode"] in ("goto","goto_w")]
    nums=[compact(x) for x in ins if x["opcode"].startswith(
          ("iconst_","fconst_","dconst_","lconst_")) or
          x["opcode"] in ("bipush","sipush","ldc","ldc_w","ldc2_w")]
    require(len(refs)<=180 and len(branches)<=180 and len(nums)<=180,
            "unbounded JVM evidence")
    return {"name":name_of(method),"header":method["header"],
            "descriptor":method["descriptor"],"instruction_count":len(ins),
            "method_sha256":digest_method(method),
            "refs":refs,"branch_edges":branches,"numeric_operands":nums}

def select(methods,path):
    if path==EVENT:
        matches=[m for m in methods if any("ARROW_INDUCTING:" in x["symbol"]
                 for x in m["instructions"])]
        require(len(matches)==1 and name_of(matches[0])=="acLivingAttack",
                "missing or ambiguous event consumer")
        require(digest_method(matches[0])==EVENT_HASH, "event digest changed")
        return matches
    matches=[m for m in methods if name_of(m)=="tick" and m["descriptor"]=="()V"]
    require(len(matches)==1,"missing or ambiguous arrow tick")
    require(digest_method(matches[0])==TICK_HASH,"arrow tick digest changed")
    return sorted(methods,key=lambda m:(name_of(m),m["descriptor"],m["header"]))

def audit(jar,javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"wrong physical JAR")
    result={"schema_version":1,
        "scope":"EXACT_ARROW_INDUCTING_EVENT_AND_SEEKING_ARROW_LIFECYCLE_DISCOVERY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "resource_sha256":RESOURCE_HASH,"classes":{},
        "limits":{"complete_cfg":"NOT_RECONSTRUCTED","inherited_methods":"NOT_AUDITED",
                  "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                  "perk_certification":"NOT_CERTIFIED","mutation":"NO_MUTATION"}}
    with zipfile.ZipFile(jar) as z:
        require(len(set(z.namelist()))==len(z.namelist()),"duplicate ZIP members")
        require(hashlib.sha256(z.read(RESOURCE)).hexdigest()==RESOURCE_HASH,
                "resource identity mismatch")
        for path in (EVENT,ARROW):
            expected_sha,count=EXPECTED[path]
            require(hashlib.sha256(z.read(path)).hexdigest()==expected_sha,
                    "class identity mismatch: "+path)
            ms=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
            require(len(ms)==count,"method roster count drift: "+path)
            result["classes"][path]={"class_sha256":expected_sha,
                "parsed_method_count":count,
                "methods":[summarize(m) for m in select(ms,path)]}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--seal",type=Path)
    a=p.parse_args()
    data=audit(a.jar,a.javap)
    if a.seal:
        require(data==json.loads(a.seal.read_text(encoding="utf8")),
                "lifecycle manifest drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",
                            encoding="utf8")
    for path,block in data["classes"].items():
        print("CLASS",path,block["class_sha256"],block["parsed_method_count"])
        for m in block["methods"]:
            print("METHOD",m["name"],m["descriptor"],m["instruction_count"],m["method_sha256"])
            for row in m["refs"]:
                if any(t in row["symbol"] for t in (
                     "getOwner:", "setOwner:", "onHit", "hurt:", "discard:",
                     "addAdditionalSaveData:", "readAdditionalSaveData:",
                     "defineSynchedData:", "getArcTowardsID:", "setArcTowardsID:",
                     "setDeltaMovement:", "getEntities:", "getEntity:")):
                    print("REF",m["name"],row["offset"],row["symbol"])
    print("STATUS EXACT_JAR_DISCOVERY_NO_MUTATION")

if __name__=="__main__":
    main()
