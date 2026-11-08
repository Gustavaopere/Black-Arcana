#!/usr/bin/env python3
"""SHA-exact, bounded read-only Second Wave producer discovery (1.0.10).
No copying of provider implementation. A static catalog fact is not a mutating hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from alexscaves_1010_damage_consumer_probe import BASE,SHA1,SHA256,SIZE,javap,parse_methods,sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ITEM=BASE+"server/item/OrtholanceItem.class"
WAVE=BASE+"server/entity/item/WaveEntity.class"
REG=BASE+"server/enchantment/ACEnchantmentRegistry.class"
FILENAME="data/alexscaves/enchantment/second_wave.json"
TAG="data/alexscaves/tags/item/enchantable/ortholance.json"
LANG="assets/alexscaves/lang/en_us.json"
PRIOR="wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-FLINGING-1.0.10.json"
SCOPE="SECOND_WAVE_1010_BOUNDED_READONLY_DISCOVERY"
PIVOTS=(460,463,466,469,474,477,482,486,489)
STEP=5
MAX_SNAP=90000
MAX_INS=600

def require(x,message):
    if not x: raise ValueError(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def snapshot(method):
    offsets=[i["offset"] for i in method["instructions"]]
    require(len(method["instructions"])==435 and offsets==sorted(set(offsets)),
            "releaseUsing instruction population/offset drift")
    ins=method["instructions"]
    require(digest_method(method)=="00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae",
            "releaseUsing method drift vs Flinging")
    require(sum("SECOND_WAVE" in x["symbol"] for x in ins)==1,
            "unexpected Second Wave registry references")
    offset_lookup={x["offset"]:i for i,x in enumerate(ins)}
    require(all(p in offset_lookup for p in PIVOTS),"Second Wave JVM pivots missing")
    windows=[]
    for p in PIVOTS:
        pos=offset_lookup[p]
        windows.append({"pivot":p,"instructions":ins[max(0,pos-STEP):min(len(ins),pos+STEP+1)]})
    # The release method has external consumers; emit bounded callsites within
    # the Second Wave segment, not the original third-party implementation.
    block=[x for x in ins if 459<=x["offset"]<705]
    selected=[x for x in block if x["opcode"].startswith("if") or
              x["opcode"] in ("goto","invokestatic","invokevirtual","invokeinterface","invokespecial") or
              x["opcode"].startswith(("iconst_","fconst_","dconst_","bipush","sipush","ldc"))]
    require(15<len(selected)<180,"unexpected Second Wave method block census")
    return {
        "descriptor":method["descriptor"],
        "instruction_count":len(ins),
        "method_sha256":digest_method(method),
        "block_offset_range":[459,705],
        "selected_block_operands":selected,
        "pivot_windows":windows,
    }

def audit(jar,javap_bin,prior):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"wrong publisher 1.0.10 JAR fingerprint")
    prior_raw=prior.read_bytes()
    require(1000<len(prior_raw)<250000,"prior Flinging manifest not bounded")
    old=json.loads(prior_raw)
    require(old["artifact"]=={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "baseline Flinging artifact drift")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR member")
        sha_classes={}
        for owner in (ITEM,WAVE,REG):
            require(owner in names,"missing provider class")
            sha_classes[owner]=digest(z.read(owner))
        require(sha_classes==old["class_sha256"],"class SHA drift from Flinging")
        require(FILENAME in names and TAG in names and LANG in names,
                "missing enchantment/tag/locale resources")
        enc=z.read(FILENAME)
        tag=z.read(TAG)
        locale=z.read(LANG)
        require(len(enc)<3000 and len(tag)<5000 and len(locale)<300000,
                "resource size outside selected bounds")
        enc_json=json.loads(enc)
        tag_json=json.loads(tag)
        dictionary=json.loads(locale)
    method_candidates=parse_methods(javap(javap_bin,jar,ITEM[:-6].replace("/",".")))
    relevant=[m for m in method_candidates if name_of(m)=="releaseUsing"]
    require(len(relevant)==1,"missing/ambiguous Ortholance.releaseUsing")
    method=relevant[0]
    contract=snapshot(method)
    original=[x for c in old["consumers"] if c["owner"]==ITEM
              for x in c["selected_methods"] if x["name"]=="releaseUsing"]
    require(len(original)==1 and original[0]["parsed_method_sha256"]==contract["method_sha256"],
            "release method from previously sealed artifact diverged")
    by_offset={i["offset"]:i for i in method["instructions"]}
    for p in original[0]["pivots"]:
        for position in p["positions"]:
            for instruction in position["instructions"]:
                require(by_offset.get(instruction["offset"])==instruction,
                        "pinned Flinging window changed")
    require(enc_json["description"]["translate"]=="enchantment.alexscaves.second_wave",
            "enchantment ID translation differs")
    texts={k:v for k,v in dictionary.items() if k.startswith("enchantment.alexscaves.second_wave")}
    require("enchantment.alexscaves.second_wave" in texts,"missing official name")
    evidence={
      "schema_version":1,"scope":SCOPE,"artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
      "prior_flinging_manifest_sha256":digest(prior_raw),
      "class_sha256":sha_classes,
      "enchantment":{"id":"alexscaves:second_wave","path":FILENAME,"json":enc_json,
                     "size_bytes":len(enc),"sha256":digest(enc)},
      "item_tag":{"path":TAG,"json":tag_json,"sha256":digest(tag)},
      "localization":{"path":LANG,"file_sha256":digest(locale),"selected":texts},
      "release_using":contract,
      "limits":{"hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                "spawn_acceptance":"NOT_VERIFIED","damage_acceptance":"NOT_TESTED",
                "runtime_server_event_guards":"NOT_CERTIFIED",
                "mutation":"NO_MUTATION","contract":"PARTIAL"},
    }
    require(len(json.dumps(evidence))<MAX_SNAP,"discovery snapshot budget exceeded")
    return evidence

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--prior",type=Path,default=Path(PRIOR))
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=audit(args.jar,args.javap,args.prior)
    if args.seal:
        require(result==json.loads(args.seal.read_text(encoding="utf8")),
                "second-wave exact discovery seal changed")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("SECOND_WAVE_DISCOVERY_JSON="+json.dumps(result,ensure_ascii=False,separators=(",",":")))
    print("SECOND_WAVE_STATUS=PARTIAL_READONLY_NO_MUTATION")
if __name__=="__main__":
    main()
