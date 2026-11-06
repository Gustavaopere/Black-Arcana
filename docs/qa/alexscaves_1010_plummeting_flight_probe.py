#!/usr/bin/env python3
"""Fail-closed SHA-exact plummeting_flight discovery; no provider code exported.

The native Extinction Spear + Dinosaur Spirit classfiles are ALREADY sealed by
the 1.0.10 Spirit Dinosaur contract. This independent inspector reads only the
enchantment resource, text and item tag from the exact publisher artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, sha_file
from alexscaves_1010_action_contract_audit import load_manifest, validate_structure

P = "data/alexscaves/enchantment/plummeting_flight.json"
TAG = "data/alexscaves/tags/item/enchantable/extinction_spear.json"
LANG = "assets/alexscaves/lang/en_us.json"
PT = "assets/alexscaves/lang/pt_br.json"
CLASS_PREFIX = "com/github/alexmodguy/alexscaves/"
CLASSES = (
    CLASS_PREFIX + "server/entity/item/ExtinctionSpearEntity.class",
    CLASS_PREFIX + "server/entity/item/DinosaurSpiritEntity.class",
    CLASS_PREFIX + "server/item/ExtinctionSpearItem.class",
    CLASS_PREFIX + "server/enchantment/ACEnchantmentRegistry.class",
)
JSON_SHA = "163b032e37c716f0ef172a37b739a6d61340dab7c629c070698f8543999ec830"
MAX_JSON_BYTES = 4096

def require(test:bool, reason:str):
    if not test: raise ValueError(reason)

def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def audit(jar:Path, reference:Path)->dict:
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher 1.0.10 JAR size/SHA mismatch")
    manifest=load_manifest(reference)
    validate_structure(manifest,profile="spirit_dinosaur")
    require(manifest["artifact_sha256"]==SHA256 and
            manifest["resources"][P]==JSON_SHA, "reused Spirit manifest drift")
    with zipfile.ZipFile(jar) as z:
        filenames=z.namelist()
        require(len(filenames)==len(set(filenames)), "duplicate ZIP members")
        require(all(p in filenames for p in (P,TAG,LANG,PT,*CLASSES)),
                "missing publisher Punting dependency".replace("Punting","Plummeting"))
        raw=z.read(P)
        require(len(raw)<=MAX_JSON_BYTES and sha(raw)==JSON_SHA,
                "plummeting_flight resource SHA drift")
        config=json.loads(raw)
        require(isinstance(config,dict) and
                config.get("description")=={"translate":"enchantment.alexscaves.plummeting_flight"} and
                config.get("supported_items")=="#alexscaves:enchantable/extinction_spear",
                "incorrect JSON identity/tag")
        tagdata=json.loads(z.read(TAG))
        require(tagdata=={"values":["alexscaves:extinction_spear"]},
                "publisher item tag mismatch")
        require(sha(z.read(TAG))==manifest["resources"][TAG],
                "SHA drift in extinction_spear tag")
        lang=json.loads(z.read(LANG))
        pt=json.loads(z.read(PT))
        desc={k:v for k,v in lang.items() if
              k.startswith("enchantment.alexscaves.plummeting_flight")}
        pt_desc={k:v for k,v in pt.items() if
                 k.startswith("enchantment.alexscaves.plummeting_flight")}
        class_hashes={c:sha(z.read(c)) for c in CLASSES}
        require(all(class_hashes[c]==manifest["classes"][c]["sha256"] for c in CLASSES),
                "native producer/consumer class SHA drift")
    required={
        CLASSES[0]:("onHitEntity",),
        CLASSES[1]:("tickSubterranodon","getEnchantmentLevel","setEnchantmentLevel",
                     "getAttackingEntity","getUsingPlayer","tick","defineSynchedData",
                     "readAdditionalSaveData","addAdditionalSaveData"),
    }
    for c, names in required.items():
        methods={m["name"] for m in manifest["classes"][c]["methods"]}
        require(set(names)<=methods, "missing Plummeting native chain: "+c)
    report={
        "scope":"PLUMMETING_FLIGHT_SHA_EXACT_RESOURCE_AND_REUSED_SPIRIT_CONSUMER",
        "identity":"alexscaves:plummeting_flight",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "resource":{"path":P,"sha256":JSON_SHA,"size_bytes":len(raw),"json":config},
        "item_tag":{"path":TAG,"sha256":manifest["resources"][TAG],"json":tagdata},
        "english_translations":desc,
        "portuguese_translations":pt_desc,
        "class_hashes":class_hashes,
        "limits":{"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                  "mutation":"NO_MUTATION","provider_universe_closed":False}
    }
    return report

def verify_seal(report:dict, path:Path, manifest_path:Path):
    """Verify exact publisher JSON and already certified native JVM anchors."""
    seal=json.loads(path.read_text(encoding="utf-8"))
    require(seal["schema_version"]==1 and
            seal["catalog_family"]=="PLUMMETING_FLIGHT_ENCHANTMENT_CONTRACT" and
            seal["claim_scope"]=="STATIC_TECHNICAL_CATALOG_ONLY" and
            seal["evidence_grade"]=="SHA_EXACT_BINARY_BEHAVIOR" and
            seal["mutating_hook"]=="NOT_VERIFIED" and
            seal["physical_qa"]=="NOT_TESTED" and
            seal["mutation"]=="NO_MUTATION" and
            seal["provider_universe_closed"] is False,
            "invalid static completion scope")
    require(seal["artifact"]==report["artifact"],"artifact drift")
    for name in ("resource","item_tag","english_translations","portuguese_translations","class_hashes"):
        require(seal[name]==report[name],"exact-JAR "+name+" drift")
    parent=load_manifest(manifest_path)
    validate_structure(parent,profile="spirit_dinosaur")
    require(seal["reused_binary_manifest"]=={
        "path":"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json",
        "version":"1.0.10","family":"SPIRIT_DINOSAUR_DAMAGE_CONTRACT",
        "evidence_grade":"SHA_EXACT_BINARY_BEHAVIOR","artifact_sha256":SHA256},
        "noncanonical bytecode source")
    seen=set()
    anchors=seal["anchors"]
    require(300<=len(anchors)<=450 and
            seal["limits"]["sealed_pivots"]==len(anchors),"insufficient/oversize anchors")
    for a in anchors:
        require(set(a)=={"class","method","descriptor","offset","opcode","operand","symbol"},
                "invalid bytecode pivot")
        cl=a["class"]
        require(cl in seal["class_hashes"] and
                parent["classes"][cl]["sha256"]==seal["class_hashes"][cl],
                "class SHA mismatch")
        methods=[m for m in parent["classes"][cl]["methods"] if
                 m["name"]==a["method"] and m["descriptor"]==a["descriptor"]]
        require(len(methods)==1, "ambiguous JVM signature")
        row=[x for x in methods[0]["anchors"] if x["offset"]==a["offset"]]
        require(len(row)==1 and
                all(row[0][k]==a[k] for k in ("offset","opcode","operand","symbol")),
                "JVM anchor changed")
        identity=(cl,a["method"],a["descriptor"],a["offset"])
        require(identity not in seen,"duplicate JVM anchor")
        seen.add(identity)
    expected="wiki/modpack-catalog/providers/✅-alexs-caves-continued/enchantments/plummeting-flight.md"
    card=seal["card"]
    require(card["path"]==expected and
            sha((Path(__file__).resolve().parents[2]/expected).read_bytes())==
            card["sha256"],"document hash drift")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--manifest",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seal",type=Path)
    args=parser.parse_args()
    result=audit(args.jar,args.manifest)
    if args.seal:
        verify_seal(result,args.seal,args.manifest)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("PLUMMETING_RESOURCE="+json.dumps(result["resource"],ensure_ascii=False,sort_keys=True))
    print("PLUMMETING_ENGLISH="+json.dumps(result["english_translations"],ensure_ascii=False))
    print("PLUMMETING_PTBR="+json.dumps(result["portuguese_translations"],ensure_ascii=False))
    print("PLUMMETING_SHA_EXACT_RESOURCE_VALIDATED"+
          (" AND IMMUTABLE SEAL VERIFIED" if args.seal else " (discovery only)"))
if __name__=="__main__":
    main()
