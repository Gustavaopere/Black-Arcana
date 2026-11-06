#!/usr/bin/env python3
"""Fail-closed, read-only Rapid Possession 1.0.10 publisher-JAR probe.

Reuses the 8-action Totem technical manifest; validates specific native
movement calculation in compiled code, without copying provider code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1,SHA256,SIZE,sha_file
from alexscaves_1010_action_contract_audit import load_manifest,validate_structure,parse_javap

RESOURCE="data/alexscaves/enchantment/rapid_possession.json"
RESOURCE_SHA="449eda001a6bb6507ef4e43cc18e601659d970e8bd7d43967aff32dfed07288a"
TAG="data/alexscaves/tags/item/enchantable/totem_of_possession.json"
LANG="assets/alexscaves/lang/en_us.json"
OWNER="com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class"
HELPER="com/github/alexmodguy/alexscaves/server/misc/ACCompat.class"
CONFIG="com/github/alexmodguy/alexscaves/server/config/ACServerConfig.class"
METHOD=("onUseTick","(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V")

def require(v,why):
    if not v: raise ValueError(why)

def digest(v):
    return hashlib.sha256(v).hexdigest()

def audit(jar,manifest_path,javap):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher Alex's Caves Continued JAR != 1.0.10 SHA-exact")
    d=load_manifest(manifest_path)
    validate_structure(d,profile="actions")
    require(d["artifact_sha256"]==SHA256 and d["resources"][RESOURCE]==RESOURCE_SHA,
            "8-action manifest/resource drift")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)), "duplicate ZIP member")
        require(all(p in names for p in (RESOURCE,TAG,LANG,OWNER,HELPER,CONFIG)),
                "missing publisher source for Rapid Possession")
        raw=z.read(RESOURCE)
        require(len(raw)<4096 and digest(raw)==RESOURCE_SHA, "Rapid Possession JSON SHA")
        j=json.loads(raw)
        require(isinstance(j,dict) and
                j.get("description")=={"translate":"enchantment.alexscaves.rapid_possession"} and
                j.get("supported_items")=="#alexscaves:enchantable/totem_of_possession" and
                j.get("max_level")==3, "wrong Rapid Possession JSON identity/level")
        tag=json.loads(z.read(TAG))
        require(tag=={"values":["alexscaves:totem_of_possession"]},
                "wrong exact item tag")
        require(digest(z.read(TAG))==d["resources"][TAG],"item tag SHA drift")
        en=json.loads(z.read(LANG))
        names={key:value for key,value in en.items() if
               key.startswith("enchantment.alexscaves.rapid_possession")}
        classes={p:digest(z.read(p)) for p in (OWNER,HELPER,CONFIG)}
        require(all(classes[p]==d["classes"][p]["sha256"] for p in classes),
                "native Totem/Compat/Config classes changed")
    command=[str(javap),"-classpath",str(jar),"-p","-s","-c",
             OWNER[:-6].replace("/",".")]
    proc=subprocess.run(command,capture_output=True,text=True,timeout=45)
    require(proc.returncode==0 and len(proc.stdout)<1000000,
            "javap failed to read exact Totem class")
    methods=parse_javap(proc.stdout,OWNER)
    require(METHOD in methods,"missing exact onUseTick signature")
    native=methods[METHOD]
    parent=[m for m in d["classes"][OWNER]["methods"]
            if (m["name"],m["descriptor"])==METHOD]
    require(len(parent)==1,"missing inherited Totem method")
    for anchor in parent[0]["anchors"]:
        row=native.get(anchor["offset"])
        require(row is not None and tuple(row)==
                (anchor["opcode"],anchor["operand"],anchor["symbol"]),
                "inherited Totem JVM anchor changed: "+str(anchor["offset"]))
    native_rows=[{"offset":off,"opcode":op,"operand":operand,"symbol":sym}
                 for off,(op,operand,sym) in sorted(native.items())]
    speed=[a for a in native_rows if 310<=a["offset"]<=344]
    require(any("RAPID_POSSESSION" in a["symbol"] for a in speed) and
            any("float 1.25f" in a["symbol"] for a in speed) and
            any("float 0.35f" in a["symbol"] for a in speed) and
            any(a["opcode"]=="fmul" for a in speed) and
            any(a["opcode"]=="fadd" for a in speed),
            "no exact 1.25+0.35*L calculation in Totem native method")
    require(any(a["offset"]==310 and "float 32.0f" in a["symbol"] for a in native_rows),
            "different native view-ray command factor")
    selected=[a for a in native_rows if (275<=a["offset"]<=356 or
               391<=a["offset"]<=406 or 582<=a["offset"]<=651)]
    require(30<=len(selected)<=135,"unexpected selected JVM pivot count")
    return {
       "scope":"RAPID_POSSESSION_SHA_EXACT_RESOURCE_AND_TOTEM_MOVEMENT",
       "identity":"alexscaves:rapid_possession",
       "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
       "resource":{"path":RESOURCE,"sha256":RESOURCE_SHA,"size_bytes":len(raw),"json":j},
       "item_tag":{"path":TAG,"sha256":d["resources"][TAG],"json":tag},
       "english_translations":names,"class_hashes":classes,
       "method":{"owner":OWNER,"name":METHOD[0],"descriptor":METHOD[1]},
       "selected_anchors":selected,
       "limits":{"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                 "mutation":"NO_MUTATION","provider_universe_closed":False}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--javap",type=Path,default=Path("javap"))
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    out=audit(a.jar,a.manifest,a.javap)
    if a.seal: verify_seal(out,a.seal,a.manifest)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("RAPID_RESOURCE="+json.dumps(out["resource"],sort_keys=True,ensure_ascii=False))
    print("RAPID_EN="+json.dumps(out["english_translations"],sort_keys=True,ensure_ascii=False))
    print("RAPID_TAG="+json.dumps(out["item_tag"],sort_keys=True,ensure_ascii=False))
    print("RAPID_SPEED_JVM="+json.dumps([a for a in out["selected_anchors"]
             if 310<=a["offset"]<=345],sort_keys=True,ensure_ascii=False))
    print("RAPID_PROBE_PASS"+(" AND SEAL_VALID" if a.seal else " DISCOVERY_ONLY"))
if __name__=="__main__":main()
