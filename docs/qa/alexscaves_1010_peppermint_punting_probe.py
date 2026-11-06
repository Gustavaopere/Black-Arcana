#!/usr/bin/env python3
"""Read-only publisher 1.0.10 Peppermint Punting JSON discovery.

The installed-version resource is inspected under exact JAR SHA checks, with
the pre-existing Multiple Mint manifest as an independent resource/class
fingerprint. This probe does not export provider code or certify a hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, sha_file

PUNTING = "data/alexscaves/enchantment/peppermint_punting.json"
LANG = "assets/alexscaves/lang/en_us.json"
TAG = "data/alexscaves/tags/item/enchantable/sugar_staff.json"
EXPECTED_RESOURCE = "ebe5a66b3d69d1d4384149959893712a7458ed9acfcc9064fa58fd16e8ba412b"
PREFIX = "com/github/alexmodguy/alexscaves/"
ITEM = PREFIX + "server/item/SugarStaffItem.class"
ENTITY = PREFIX + "server/entity/item/SpinningPeppermintEntity.class"
ALLOWED_KEYS = frozenset(("description","supported_items","weight","max_level","min_cost","max_cost","anvil_cost","slots","exclusive_set","effects"))

def require(test, problem):
    if not test: raise ValueError(problem)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def audit(jar:Path, manifest:Path):
    require(jar.name=="alexscaves-1.0.10.jar" and jar.is_file(), "unexpected publisher jar")
    require(sha_file(jar)==(SHA1,SHA256,SIZE), "publisher artifact checksum mismatch")
    reference=json.loads(manifest.read_text(encoding="utf-8"))
    require(reference["version"]=="1.0.10" and
            reference["artifact_sha256"]==SHA256 and
            reference["claim_scope"]=="STATIC_TECHNICAL_CATALOG_ONLY" and
            reference["evidence_grade"]=="SHA_EXACT_BINARY_BEHAVIOR", "reference contract drift")
    require(reference["resources"].get(PUNTING)==EXPECTED_RESOURCE, "reference resource hash drift")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate publisher ZIP path")
        require(all(x in names for x in (PUNTING,LANG,TAG,ITEM,ENTITY)), "missing Punting dependency")
        raw=z.read(PUNTING)
        require(len(raw)<=4096 and sha(raw)==EXPECTED_RESOURCE, "Punting resource hash/size drift")
        config=json.loads(raw)
        require(isinstance(config,dict) and
                config.get("description")=={"translate":"enchantment.alexscaves.peppermint_punting"} and
                config.get("supported_items")=="#alexscaves:enchantable/sugar_staff" and
                set(config).issubset(ALLOWED_KEYS), "unexpected publisher Punting JSON schema")
        languages=json.loads(z.read(LANG))
        translations={key:value for key,value in languages.items()
            if key.startswith("enchantment.alexscaves.peppermint_punting")}
        tag=json.loads(z.read(TAG))
        require(tag=={"values":["alexscaves:sugar_staff"]}, "sugar staff tag drift")
        require(sha(z.read(TAG))==reference["resources"][TAG],"tag SHA drift")
        classes={p:sha(z.read(p)) for p in (ITEM,ENTITY)}
        for path,digest in classes.items():
            require(digest==reference["classes"][path]["sha256"], "class fingerprint drift "+path)
    use=[m for m in reference["classes"][ITEM]["methods"] if m["name"]=="use"]
    require(len(use)==1, "expected one Sugar Staff use")
    anchors={a["offset"]:a for a in use[0]["anchors"]}
    pivots={262:"PEPPERMINT_PUNTING",265:"enchantLevel",274:"setStraight",295:"setYRot",
            302:"setSpinSpeed",305:"20",315:"setStraight",332:"setYRot",
            339:"setSpinSpeed",349:"SEEKCANDY",372:"setSpinSpeed",375:"50",
            405:"setStartAngle",418:"addFreshEntity",461:"addCooldown"}
    for offset,needle in pivots.items():
        row=anchors.get(offset)
        require(row is not None and needle in
                (row["symbol"]+" "+row["operand"]),f"missing Punting bytecode pivot {offset} {needle}")
    report={"scope":"SHA_EXACT_1010_PUNTING_JSON_AND_REUSED_MULTIPLE_MINT_CONSUMER",
            "identity":"alexscaves:peppermint_punting",
            "artifact":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
            "resource":{"path":PUNTING,"sha256":EXPECTED_RESOURCE,"size_bytes":len(raw),"json":config},
            "english_translations":translations,
            "item_tag":{"path":TAG,"sha256":sha(z.read(TAG)) if False else reference["resources"][TAG],"json":tag},
            "class_hashes":classes,"bytecode_pivots":pivots,
            "limits":{"runtime_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION"}}
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    obj=audit(args.jar,args.manifest)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("EXACT_PUNTING_CONFIG="+json.dumps(obj["resource"],sort_keys=True,ensure_ascii=False))
    print("EXACT_PUNTING_DESCRIPTIONS="+json.dumps(obj["english_translations"],ensure_ascii=False,sort_keys=True))
    print("EXACT_PUNTING_REUSE_VALIDATED="+str(len(obj["bytecode_pivots"]))+" Punting pivots; no mutation")
if __name__=="__main__": main()
