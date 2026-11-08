#!/usr/bin/env python3
"""Discover and seal exact publisher 1.0.10 Sightless control gates and consumers.

Read-only clean-room interoperability evidence. Delimit each selected method by
full-JVM digest, resource and class hashes; emit only sparse decisive instructions.
This does NOT certify mutation, safety of a hook, or physical acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, sha_file, javap, parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ENCH = "data/alexscaves/enchantment/sightless.json"
TAG = "data/alexscaves/tags/item/enchantable/totem_of_possession.json"
LANG_EN = "assets/alexscaves/lang/en_us.json"
LANG_PT = "assets/alexscaves/lang/pt_br.json"
PRIOR = "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TECHNICAL-CONTRACTS-1.0.10.json"
ASTRAL = "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ASTRAL-TRANSFERRING-1.0.10.json"
OWNER = BASE + "server/item/TotemOfPossessionItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
COMPAT = BASE + "server/misc/ACCompat.class"
CONSUMER_METHODS = (
    "use", "onUseTick", "releaseUsing", "getControlledEntity",
    "isEntityLookingAt", "isBound", "resetBound",
    "getBoundEntityUUID", "updateEntityIdFromServer",
    "setPossessed", "getUseDuration",
)
SCAN_TERMS = (
    "SIGHTLESS", "isEntityLookingAt", "getControlledEntity", "setGlowingTag",
    "getDamageValue", "getMaxDamage", "setDamageValue",
    "stopUsingItem", "startUsingItem", "shrink:",
    "isClientSide", "isBound", "getControlledEntity",
    "getBoundEntityUUID", "resetBound", "UpdateItemTagMessage",
    "sendMSGToServer", "getNavigation", "moveTo:", "getUseDuration",
    "hasLineOfSight", "distanceTo", "getViewVector",
    "dot:", "isCreative", "ControllingEntityID", "BoundEntityUUID",
    "totemOfPossessionPlayers", "TOTEM_OF_POSSESSION_USE",
)
MAX_BUDGET = 100000

def require(cond,why):
    if not cond: raise ValueError(why)

def digest(blob):
    return hashlib.sha256(blob).hexdigest()

def find_method(methods,name):
    matches=[m for m in methods if name_of(m)==name]
    require(len(matches)==1,"method missing or ambiguous: "+name)
    m=matches[0]
    require(0<len(m["instructions"])<=2500,"invalid method size: "+name)
    return m

def compact(row):
    return {k:row[k] for k in ("offset","opcode","operand","symbol")}

def evidence(jar,java_bin,prior_path,astral_path):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"publisher jar mismatch")
    baseline=json.loads(prior_path.read_text(encoding="utf-8"))
    astral=json.loads(astral_path.read_text(encoding="utf-8"))
    require(baseline["artifact_sha256"]==SHA256 and baseline["version"]=="1.0.10" and
            baseline["resources"][ENCH]=="1e7d093a0d459e2e6a29b40cd625b4fb1f990285343b53e4421c8f3727b2ecb9",
            "prior resource publisher pin drift")
    require(astral["consumer"]["parsed_method_sha256"]==
            "4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39",
            "independent Totem onUseTick fingerprint drift")
    with zipfile.ZipFile(jar) as z:
        members=z.namelist()
        require(len(members)==len(set(members)),"duplicate archive path")
        require(all(p in members for p in (ENCH,TAG,LANG_EN,LANG_PT,OWNER,REG,COMPAT)),
                "missing publisher resources or classes")
        classes=sorted(p for p in members if p.startswith(BASE) and p.endswith(".class"))
        require(100<=len(classes)<=3000,"provider class census outside budget")
        hits=[p for p in classes if b"SIGHTLESS" in z.read(p)]
        require(OWNER in hits and REG in hits and len(hits)<=15,"unexpected Sightless direct consumer census")
        resource={p:{"sha256":digest(z.read(p)),"size_bytes":len(z.read(p))}
                  for p in (ENCH,TAG,LANG_EN,LANG_PT)}
        require(resource[ENCH]["sha256"]==baseline["resources"][ENCH],"resource mismatched")
        require(resource[TAG]["sha256"]==baseline["resources"][TAG],"tag mismatched")
        cfg=json.loads(z.read(ENCH));tag=json.loads(z.read(TAG))
        en=json.loads(z.read(LANG_EN));pt=json.loads(z.read(LANG_PT))
        translations={lang:{k:v for k,v in obj.items() if
                             k.startswith("enchantment.alexscaves.sightless")}
                      for lang,obj in (("en_us",en),("pt_br",pt))}
        hashes={p:digest(z.read(p)) for p in (OWNER,REG,COMPAT)}
        require(hashes[OWNER]==baseline["classes"][OWNER]["sha256"],"Totem binary drift")
        require(hashes[COMPAT]==baseline["classes"][COMPAT]["sha256"],"ACCompat binary drift")
    methodset=parse_methods(javap(java_bin,jar,OWNER[:-6].replace("/",".")))
    refs=baseline["classes"][OWNER]["methods"]
    selected={}
    for name in CONSUMER_METHODS:
        m=find_method(methodset,name)
        anchors=[a for r in refs if r["name"]==name and r["descriptor"]==m["descriptor"]
                 for a in r["anchors"]]
        ins=m["instructions"]
        by={x["offset"]:x for x in ins}
        for a in anchors:
            row=by.get(a["offset"])
            require(row is not None and row["opcode"]==a["opcode"] and
                    " ".join(row["operand"].split())==" ".join(a["operand"].split()) and
                    row["symbol"]==a["symbol"],
                    "prior proven method anchor mismatch "+name+" @"+str(a["offset"]))
        found=[i for i,row in enumerate(ins) if any(t in row["symbol"] for t in SCAN_TERMS)]
        chosen=set()
        for i in found[:40]:
            chosen.update(range(max(0,i-3),min(len(ins),i+4)))
        # preserve up to 6 first and last opcodes for entry/return structure
        chosen.update(range(min(6,len(ins))))
        chosen.update(range(max(0,len(ins)-6),len(ins)))
        # The 5D gaze helper is an angular/distance/LOS predicate, not
        # a five-block range. Retain only decisive numerical JVM operations
        # and their immediate operands to prove the exact installed formula.
        if name=="isEntityLookingAt":
            for i,row in enumerate(ins):
                if row["opcode"] in ("ddiv","dsub","dadd","dmul","dcmpl","dcmpg"):
                    chosen.update(range(max(0,i-2),min(len(ins),i+3)))
        windows=[compact(ins[i]) for i in sorted(chosen)]
        require(len(windows)<=340,"producer evidence too wide: "+name)
        selected[name]={"descriptor":m["descriptor"],"instructions_total":len(ins),
                        "method_sha256":digest_method(m),"reused_anchors":len(anchors),
                        "symbolic_hits":[{"offset":ins[i]["offset"],"symbol":ins[i]["symbol"]}
                                         for i in found[:60]],
                        "bounded_instructions":windows}
    require(selected["onUseTick"]["method_sha256"]==
            astral["consumer"]["parsed_method_sha256"],
            "Totem tick differs from independently reviewed 1.0.10 Astral contract")
    out={
      "schema_version":1,"scope":"EXACT_1010_SIGHTLESS_READONLY_DISCOVERY",
      "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
      "prior_sha256":digest(prior_path.read_bytes()),
      "astral_sha256":digest(astral_path.read_bytes()),
      "class_sha256":hashes,
      "class_census":{"scanned":len(classes),"sightless_token_hits":hits},
      "enchantment":{"path":ENCH,**resource[ENCH],"json":cfg},
      "item_tag":{"path":TAG,**resource[TAG],"json":tag},
      "translations":translations,
      "locale_hashes":{"en_us":resource[LANG_EN],"pt_br":resource[LANG_PT]},
      "methods":selected,
      "limits":{"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                "provider_closed":False,"mutation":"NO_MUTATION",
                "runtime_damage_or_mana":"NOT_CLAIMED",
                "loaded_datapack":"NOT_VERIFIED"},
    }
    require(len(json.dumps(out))<=MAX_BUDGET,"discovery exceeds clean-room bound")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--prior",type=Path,default=Path(PRIOR))
    p.add_argument("--astral",type=Path,default=Path(ASTRAL))
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    out=evidence(a.jar,a.javap,a.prior,a.astral)
    # Expose bounded read-only evidence even on a seal mismatch so reviewers
    # can diagnose the exact drift; the process still fails closed.
    print("SIGHTLESS_DISCOVERY_JSON="+json.dumps(out,ensure_ascii=False,separators=(",",":")))
    if a.seal:
        require(json.loads(a.seal.read_text(encoding="utf-8"))==out,
                "publisher Sightless immutable static seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("SIGHTLESS_STATIC_STATUS=READONLY_NO_MUTATION")
if __name__=="__main__": main()
