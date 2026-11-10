#!/usr/bin/env python3
"""Read-only individual 1.0.10 Twilight Perfection enchantment contract census.

Verifies the exact publisher resource, neighboring exclusivity, native client
charge/release and damage callsites against the already audited SHA-exact
Dreadbow manifest. No vendor implementation is copied or mutated.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest, validate_structure
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file

BASE="com/github/alexmodguy/alexscaves/"
ITEM=BASE+"server/item/DreadbowItem.class"
ARROW=BASE+"server/entity/item/DarkArrowEntity.class"
REG=BASE+"server/enchantment/ACEnchantmentRegistry.class"
MSG=BASE+"server/message/UpdateItemTagMessage.class"
RENDER=BASE+"client/render/item/ACItemstackRenderer.class"
RESOURCE="data/alexscaves/enchantment/twilight_perfection.json"
RESOURCE_SHA="82a8e06c07b66be33a330bdbeb1bc867d03ce13a49ab2505fa06504fe5f044e1"
TAG="data/alexscaves/tags/item/enchantable/dreadbow.json"
LANG="assets/alexscaves/lang/en_us.json"
RELENTLESS="data/alexscaves/enchantment/relentless_darkness.json"
ALLOWED=frozenset(("description","supported_items","weight","max_level",
                  "min_cost","max_cost","anvil_cost","slots","effects","exclusive_set"))
# These are exact pivots inside the 1.0.10 compiler manifest, not claims about
# the full runtime CFG, damage acceptance or server-side tag authorization.
PIVOTS={
    (ITEM,"acInventoryTick"):{
        39:"isClientSide",42:"400",91:"getPerfectShotTicks",94:"122",
        99:"getPerfectShotTicks",103:"isub",104:"setPerfectShotTicks",
        119:"sendMSGToServer",140:"TWILIGHT_PERFECTION",143:"enchantLevel",
        149:"getMaxLoadTime",156:"256",163:"256",184:"setUseTime",
        189:"256",196:"236",203:"236",207:"iconst_4",210:"iconst_1",
        211:"isub",212:"iconst_3",214:"iadd",215:"setPerfectShotTicks",
        230:"sendMSGToServer",237:"iconst_0",238:"setPerfectShotTicks",
        253:"sendMSGToServer",300:"setUseTime",305:"setPerfectShotTicks"
    },
    (ITEM,"releaseUsing"):{
        14:"RELENTLESS_DARKNESS",20:"899",87:"TWILIGHT_PERFECTION",
        90:"enchantLevel",93:"107",97:"getPerfectShotTicks",100:"107",
        103:"iconst_1",107:"iconst_0",108:"istore",117:"899",
        402:"setShadowArrowDamage",407:"10",409:"setPerfectShot",
        421:"443",431:"ac$getBaseDamage",436:"2.0d",439:"dmul",
        440:"setBaseDamage",775:"addFreshEntity",874:"hurtAndBreakUsedHand"
    },
    (ITEM,"getPerfectShotTicks"):{10:"PerfectShotTicks"},
    (ITEM,"setPerfectShotTicks"):{6:"PerfectShotTicks"},
    (ARROW,"onHitEntity"):{
        11:"getShadowArrowDamage",17:"isPerfectShot",20:"29",25:"fconst_2",
        26:"fmul",37:"causeDarkArrowDamage",51:"93",59:"93",67:"93",
        74:"93",82:"ACCompat.hurt",85:"93"
    },
    (ARROW,"setPerfectShot"):{},
    (ARROW,"isPerfectShot"):{},
    (MSG,"handle"):{8:"getSender",15:"isClientSide",39:"entityId",
                     42:"getEntity",81:"ItemStack.is",113:"ItemStack.is",
                     143:"UpdatesStackTags",174:"updateTagFromServer"},
    (RENDER,"renderByItem"):{3191:"getPerfectShotTicks"},
}
MAX_ANCHORS=400

def require(ok,reason):
    if not ok:raise ValueError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,"duplicate publisher JSON key: "+k)
        out[k]=v
    return out

def selected_method(m, classpath, methodname):
    hits=[x for x in m["classes"][classpath]["methods"] if x["name"]==methodname]
    require(len(hits)==1,"missing/ambiguous native method "+methodname)
    return hits[0]

def verify_pivots(method,expected):
    by={x["offset"]:x for x in method["anchors"]}
    require(len(by)==len(method["anchors"]),"duplicate compiled anchor offsets")
    for offset,token in expected.items():
        row=by.get(offset)
        require(row is not None and token in
                (row["opcode"]+" "+row["operand"]+" "+row["symbol"]),
                "missing native Twilight Perfection pivot: "+str(offset))
    return len(expected)

def bounded_evidence(m,classpath,methodname):
    mm=selected_method(m,classpath,methodname)
    verified=verify_pivots(mm,PIVOTS[(classpath,methodname)])
    anchors=mm["anchors"]
    require(1<=len(anchors)<=MAX_ANCHORS,"unbounded method evidence")
    # Retain only a digest, inventory and the exact semantically pertinent
    # anchors: the canonical parent manifest already preserves other windows.
    bounded=[x for x in anchors if x["offset"] in PIVOTS[(classpath,methodname)]]
    return {"class_sha256":m["classes"][classpath]["sha256"],
            "method":methodname,"descriptor":mm["descriptor"],
            "parent_method_anchors_sha256":sha(json.dumps(anchors,sort_keys=True,
                separators=(",",":"),ensure_ascii=False).encode("utf8")),
            "parent_anchor_count":len(anchors),
            "verified_pivots":verified,
            "pivots":bounded}

def audit(jar:Path,parent_path:Path):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher artifact does not match installed SHA-exact 1.0.10")
    m=load_manifest(parent_path)
    validate_structure(m,profile="dreadbow")
    require(m["artifact_sha256"]==SHA256 and
            m["resources"].get(RESOURCE)==RESOURCE_SHA,
            "canonical Dreadbow authority does not match Twilight JSON")
    needed=(RESOURCE,TAG,LANG,RELENTLESS,ITEM,ARROW,REG,MSG,RENDER)
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP member")
        require(all(n in names for n in needed),"missing publisher resource/class")
        raw=z.read(RESOURCE)
        require(16<=len(raw)<=4096 and sha(raw)==RESOURCE_SHA,
                "Twilight Perfection JSON fingerprint drift")
        config=json.loads(raw,object_pairs_hook=strict_pairs)
        require(isinstance(config,dict) and
                set(config)<=ALLOWED and
                config.get("description")=={"translate":"enchantment.alexscaves.twilight_perfection"} and
                config.get("supported_items")=="#alexscaves:enchantable/dreadbow",
                "Twilight Perfection publisher JSON identity/schema drift")
        tag_raw=z.read(TAG)
        require(sha(tag_raw)==m["resources"][TAG],"Dreadbow item tag drift")
        tag=json.loads(tag_raw,object_pairs_hook=strict_pairs)
        require(tag=={"values":["alexscaves:dreadbow"]},"Dreadbow tag contents drift")
        langs=json.loads(z.read(LANG),object_pairs_hook=strict_pairs)
        translations={k:v for k,v in langs.items() if
                      k.startswith("enchantment.alexscaves.twilight_perfection")}
        other_raw=z.read(RELENTLESS)
        require(sha(other_raw)==m["resources"][RELENTLESS],
                "Relentless Darkness resource identity drift")
        other=json.loads(other_raw,object_pairs_hook=strict_pairs)
        exclusions=other.get("exclusive_set",[])
        require("alexscaves:twilight_perfection" in exclusions,
                "neighboring publisher exclusivity drift")
        hashes={p:sha(z.read(p)) for p in (ITEM,ARROW,REG,MSG,RENDER)}
        require(all(hashes[p]==m["classes"][p]["sha256"] for p in hashes),
                "compiled consumer/registry class digest drift")
    evidence=[bounded_evidence(m,p,name) for p,name in PIVOTS]
    return {
        "schema_version":1,
        "scope":"TWILIGHT_PERFECTION_SHA_EXACT_PUBLISHER_AND_NATIVE_BRANCH_CONTRACT",
        "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade":"SHA_EXACT_BINARY_BEHAVIOR",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "enchantment_id":"alexscaves:twilight_perfection",
        "resource":{"path":RESOURCE,"sha256":RESOURCE_SHA,
                    "size_bytes":len(raw),"json":config},
        "item_tag":{"path":TAG,"sha256":sha(tag_raw),"json":tag},
        "english_translations":translations,
        "neighbor_exclusion":{"path":RELENTLESS,"sha256":sha(other_raw),
                              "exclusive_set":exclusions},
        "class_hashes":hashes,
        "parent_manifest":{"path":str(parent_path).replace("\\","/"),
                           "artifact_sha256":m["artifact_sha256"]},
        "evidence":evidence,
        "limits":{"full_runtime_cfg":"NOT_RECONSTRUCTED",
                  "client_to_server_tag_authority":"NOT_VERIFIED",
                  "physical_damage_acceptance":"NOT_TESTED",
                  "datapack_enchantments":"NOT_VERIFIED",
                  "safe_mutating_hook":"NOT_VERIFIED",
                  "physical_qa":"NOT_TESTED",
                  "provider_universe_closed":False,
                  "mutation":"NO_MUTATION"}
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True,type=Path)
    ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--seal",type=Path)
    args=ap.parse_args()
    result=audit(args.jar,args.manifest)
    if args.seal:
        expected=json.loads(args.seal.read_text(encoding="utf8"),
                            object_pairs_hook=strict_pairs)
        require(result==expected,"Twilight Perfection individual seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf8")
    print("TWILIGHT_PUBLISHER_RESOURCE="+json.dumps(result["resource"],
          separators=(",",":"),ensure_ascii=False))
    print("TWILIGHT_PUBLISHER_TRANSLATIONS="+json.dumps(result["english_translations"],
          separators=(",",":"),ensure_ascii=False))
    print("TWILIGHT_PUBLISHER_EXCLUSIONS="+json.dumps(result["neighbor_exclusion"],
          separators=(",",":"),ensure_ascii=False))
    if not args.seal:
        print("TWILIGHT_DISCOVERY_JSON="+json.dumps(result,separators=(",",":"),
                                                   ensure_ascii=False))
    print("TWILIGHT_STATUS", "SEALED" if args.seal else "UNSEALED_DISCOVERY",
          "NATIVE_METHODS",len(result["evidence"]),"NO_MUTATION")

if __name__=="__main__":
    main()
