#!/usr/bin/env python3
"""Read-only Alex's Caves 1.0.10 Precise Volley evidence from the publisher JAR.

Reuses the fully audited Dreadbow + Dark Arrow manifest. No bytecode or
proprietary code exported; only bounded identity, data and class fingerprints.
"""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
from alexscaves_1010_action_contract_audit import load_manifest, validate_structure
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file

RESOURCE = "data/alexscaves/enchantment/precise_volley.json"
HASH = "59efc44222dcd59530e13a50cb413a2db0c875213ced1a2ac9de2ef982615f53"
TAG = "data/alexscaves/tags/item/enchantable/dreadbow.json"
LANG = "assets/alexscaves/lang/en_us.json"
PRE = "com/github/alexmodguy/alexscaves/"
ITEM = PRE+"server/item/DreadbowItem.class"
ARROW = PRE+"server/entity/item/DarkArrowEntity.class"
REG = PRE+"server/enchantment/ACEnchantmentRegistry.class"
ALLOWED = frozenset(("description","supported_items","weight","max_level",
                     "min_cost","max_cost","anvil_cost","slots","effects","exclusive_set"))

def require(ok,reason):
    if not ok: raise ValueError(reason)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def audit(jar:Path,manifest_path:Path):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher JAR identity is not SHA-exact 1.0.10")
    m=load_manifest(manifest_path)
    validate_structure(m,profile="dreadbow")
    require(m["artifact_sha256"]==SHA256 and
            m["resources"][RESOURCE]==HASH,"Dreadbow parent manifest or resource drift")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate publisher zip path")
        require(all(p in names for p in (RESOURCE,TAG,LANG,ITEM,ARROW,REG)),
                "missing Precise Volley publisher dependency")
        raw=z.read(RESOURCE)
        require(len(raw)<=4096 and digest(raw)==HASH,
                "precise_volley resource fingerprint mismatch")
        config=json.loads(raw)
        require(isinstance(config,dict) and set(config)<=ALLOWED and
                config.get("description")=={"translate":"enchantment.alexscaves.precise_volley"} and
                config.get("supported_items")=="#alexscaves:enchantable/dreadbow",
                "unexpected Precise Volley JSON identity/schema")
        tag=json.loads(z.read(TAG))
        require(tag=={"values":["alexscaves:dreadbow"]},
                "Dreadbow item tag drift")
        require(digest(z.read(TAG))==m["resources"][TAG],
                "publisher item tag SHA mismatch")
        lang=json.loads(z.read(LANG))
        strings={k:v for k,v in lang.items() if
                 k.startswith("enchantment.alexscaves.precise_volley")}
        classes={p:digest(z.read(p)) for p in (ITEM,ARROW,REG)}
        require(all(classes[p]==m["classes"][p]["sha256"] for p in classes),
                "native compiled class mismatch")
    use=[z for z in m["classes"][ITEM]["methods"] if z["name"]=="releaseUsing"]
    require(len(use)==1,"releaseUsing overload mismatch")
    offsets={x["offset"]:x for x in use[0]["anchors"]}
    pivots={14:"RELENTLESS_DARKNESS",20:"899",43:"PRECISE_VOLLEY",46:"enchantLevel",
            49:"56",52:"iconst_1",56:"iconst_0",57:"istore",
            390:"iload",392:"399",395:"fconst_2",399:"3.0f",
            402:"setShadowArrowDamage",665:"672",668:"fconst_0",
            775:"addFreshEntity",874:"hurtAndBreakUsedHand"}
    for offset,needle in pivots.items():
        a=offsets.get(offset)
        require(a is not None and needle in
                (a["opcode"]+" "+a["operand"]+" "+a["symbol"]),
                "missing native Precise Volley pivot "+str(offset))
    hit=[z for z in m["classes"][ARROW]["methods"] if z["name"]=="onHitEntity"]
    require(len(hit)==1 and
            any(x["offset"]==82 and "ACCompat.hurt" in x["symbol"] for x in hit[0]["anchors"]),
            "missing actual Dark Arrow damage settlement")
    return {"scope":"PRECISE_VOLLEY_SHA_EXACT_RESOURCE_AND_REUSED_DREADBOW_CONSUMERS",
            "identity":"alexscaves:precise_volley",
            "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "resource":{"path":RESOURCE,"sha256":HASH,"size_bytes":len(raw),"json":config},
            "item_tag":{"path":TAG,"sha256":m["resources"][TAG],"json":tag},
            "english_translations":strings,"class_hashes":classes,
            "pivots_checked":pivots,
            "limits":{"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                      "mutation":"NO_MUTATION","provider_universe_closed":False}}

def verify_seal(evidence:dict, seal_path:Path, manifest_path:Path):
    s=json.loads(seal_path.read_text(encoding="utf-8"))
    require(s["schema_version"]==1 and
            s["catalog_family"]=="PRECISE_VOLLEY_ENCHANTMENT_CONTRACT" and
            s["claim_scope"]=="STATIC_TECHNICAL_CATALOG_ONLY" and
            s["evidence_grade"]=="SHA_EXACT_BINARY_BEHAVIOR" and
            s["mutating_hook"]=="NOT_VERIFIED" and
            s["physical_qa"]=="NOT_TESTED" and
            s["mutation"]=="NO_MUTATION" and
            s["provider_universe_closed"] is False,
            "unsafe Precise Volley seal scope")
    for key in ("artifact","resource","item_tag","english_translations","class_hashes"):
        require(s[key]==evidence[key],"Precise Volley exact publisher "+key+" drift")
    parent=load_manifest(manifest_path)
    validate_structure(parent,profile="dreadbow")
    require(s["reused_binary_manifest"]=={
        "path":"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json",
        "version":"1.0.10","family":"DREADBOW_AND_DARK_ARROW",
        "evidence_grade":"SHA_EXACT_BINARY_BEHAVIOR","artifact_sha256":SHA256},
        "noncanonical Dreadbow authority")
    anchors=s["anchors"]
    require(145<=len(anchors)<=280 and
            s["limits"]["sealed_pivots"]==len(anchors),
            "Precise Volley bounded pivots missing")
    seen=set()
    for row in anchors:
        require(set(row)=={"class","method","descriptor","offset","opcode","operand","symbol"},
                "unverified anchor fields")
        cl=row["class"]
        require(cl in s["class_hashes"] and
                parent["classes"][cl]["sha256"]==s["class_hashes"][cl],
                "native class hash drift")
        method=[m for m in parent["classes"][cl]["methods"]
                if m["name"]==row["method"] and m["descriptor"]==row["descriptor"]]
        require(len(method)==1,"ambiguous native method")
        candidate=[a for a in method[0]["anchors"] if a["offset"]==row["offset"]]
        require(len(candidate)==1 and
                all(candidate[0][k]==row[k] for k in ("offset","opcode","operand","symbol")),
                "Precise Volley JVM offset/opcode drift")
        ident=(cl,row["method"],row["descriptor"],row["offset"])
        require(ident not in seen,"duplicate native anchor")
        seen.add(ident)
    expected="wiki/modpack-catalog/providers/✅-alexs-caves-continued/enchantments/precise-volley.md"
    require(s["card"]["path"]==expected and
            digest((Path(__file__).resolve().parents[2]/expected).read_bytes())==
            s["card"]["sha256"],"Precise Volley dossier hash mismatch")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--seal",type=Path)
    a=p.parse_args()
    evidence=audit(a.jar,a.manifest)
    if a.seal: verify_seal(evidence,a.seal,a.manifest)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PRECISE_RESOURCE="+json.dumps(evidence["resource"],sort_keys=True,ensure_ascii=False))
    print("PRECISE_TRANSLATIONS="+json.dumps(evidence["english_translations"],sort_keys=True,ensure_ascii=False))
    print("PRECISE_ITEM_TAG="+json.dumps(evidence["item_tag"],sort_keys=True))
    print("PRECISE_SHA_EXACT_RESOURCE_VALIDATED"+(" AND SEAL VALID" if a.seal else " DISCOVERY"))

if __name__=="__main__":main()
