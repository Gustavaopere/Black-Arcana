#!/usr/bin/env python3
"""Read-only SHA-exact Seekcandy 1.0.10 static producer/consumer certification probe.

Produces a bounded interoperability manifest, not a copy of third-party code.
Full selected method hashes + 1.0.10 classfile hashes certify methods;
the already sealed Multiple Mint anchor corpus verifies individual offsets.
No gameplay/accepted damage or mutable API is inferred.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ENCH = "data/alexscaves/enchantment/seekcandy.json"
LANG = "assets/alexscaves/lang/en_us.json"
TAG = "data/alexscaves/tags/item/enchantable/sugar_staff.json"
REFERENCE = "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json"
CARD = "wiki/modpack-catalog/providers/✅-alexs-caves-continued/enchantments/seekcandy.md"
EXPECTED_ENCH_SHA = "7e564925928b90368d9042f1b722f89464bfbd708abf69ced0d785b5871f0a74"
PRODUCER = BASE + "server/item/SugarStaffItem.class"
SELECTION = BASE + "server/item/SeaStaffItem.class"
PROJECTILE = BASE + "server/entity/item/SpinningPeppermintEntity.class"
REGISTRY = BASE + "server/enchantment/ACEnchantmentRegistry.class"
COMPAT = BASE + "server/misc/ACCompat.class"
METHODS = {
    PRODUCER: ("use",),
    SELECTION: ("getClosestLookingAtEntityFor",),
    PROJECTILE: (
        "tick", "hurtEntities", "getOwner", "setOwner",
        "getSeekingEntityId", "setSeekingEntityId",
        "addAdditionalSaveData", "readAdditionalSaveData",
        "defineSynchedData", "getSpinSpeed", "setSpinSpeed", 
        "getSpinRadius", "setSpinRadius", "isStraight", "setStraight",
        "getSpinAroundPosition", "setSpinAroundPosition", "getLifespan",
        "setLifespan",
    ),
    COMPAT: ("enchantLevel", "addCooldown", "hurtAndBreakUsedHand", "hurt"),
}
FOCUS = {
    PRODUCER: {"use": (8, 11, 30, 35, 37, 186, 192, 195, 262, 268, 342, 344, 349, 352, 355,
                       362, 365, 370, 372, 375, 377, 381, 383, 389, 405, 412, 418, 421, 461, 468)},
    SELECTION: {"getClosestLookingAtEntityFor": (5, 24, 30, 33, 40, 47, 50, 78, 87, 95,
                                      104, 156, 159, 174, 220, 229, 238, 247, 259, 266, 270, 275)},
    PROJECTILE: {
        "tick": (65, 71, 245, 253, 262, 323, 327, 355, 358, 361, 362, 377, 380, 384,
                 393, 403, 408, 413, 418, 435, 440, 453, 456, 465, 469, 479, 596, 624, 733, 737),
        "hurtEntities": (1, 14, 27, 65, 72, 84, 91, 106, 109, 120, 137, 143, 145,
                         148, 151, 155, 178, 184, 189, 192, 193, 197, 200),
        "readAdditionalSaveData": (5, 15, 29, 37, 47, 61, 65, 91, 103, 113, 117,
                                   120, 134, 145, 156, 167, 170),
        "addAdditionalSaveData": (1, 12, 22, 26, 30, 37, 40, 50, 61, 72, 83,
                                  94, 105, 116, 127, 134, 137),
        "defineSynchedData": (1, 12, 24, 36, 48, 60, 74, 77, 84),
        "getOwner": (1, 8, 18, 35, 51, 55),
        "setOwner": (2, 15, 18),
        "getSeekingEntityId": (4, 7),
        "setSeekingEntityId": (4, 11),
    },
}
SCOPE = "EXACT_SEEKCANDY_1010_READONLY_STATIC_CONTRACT"
MAX_OUT = 90000

def require(ok, message):
    if not ok: raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def selected_methods(javap_bin, jar, cls, wanted, reference):
    raw = javap(javap_bin, jar, cls[:-6].replace("/", "."))
    all_methods = parse_methods(raw)
    report = {}
    references = reference["classes"][cls]["methods"]
    for method_name in wanted:
        found = [m for m in all_methods if name_of(m) == method_name]
        require(len(found) == 1, "missing/overloaded method "+cls+"."+method_name)
        m = found[0]
        require(m["descriptor"] and 1 <= len(m["instructions"]) <= 2500,
                "method descriptor/instruction limits "+method_name)
        recorded = [x for x in references if x["name"] == method_name and
                    x["descriptor"] == m["descriptor"]]
        # New methods absent from Multiple Mint are valid only when no pre-existing
        # same-name ABI was expected. Their digest remains explicitly pinned.
        require(len(recorded) <= 1, "duplicate inherited reference ABI "+method_name)
        if recorded:
            by_offset = {x["offset"]: x for x in m["instructions"]}
            require(len(by_offset) == len(m["instructions"]), "duplicate bytecode offsets")
            for anchor in recorded[0]["anchors"]:
                got = by_offset.get(anchor["offset"])
                valid = got is not None and got["offset"] == anchor["offset"] and (
                    got["opcode"] == anchor["opcode"] and
                    " ".join(got["operand"].split()) ==
                    " ".join(anchor["operand"].split()) and
                    got["symbol"] == anchor["symbol"])
                require(valid,
                        "SHA-exact inherited 1.0.10 method anchor mismatch: "+
                        cls+"."+method_name+" @"+str(anchor["offset"])+
                        " expected="+repr(anchor)+" received="+repr(got))
        focus = FOCUS.get(cls, {}).get(method_name, ())
        found_offsets = {x["offset"]: x for x in m["instructions"]}
        require(all(o in found_offsets for o in focus),
                "required Seekcandy bytecode flow pivot missing "+method_name)
        report[method_name] = {
            "descriptor": m["descriptor"],
            "instruction_count": len(m["instructions"]),
            "parsed_method_sha256": digest_method(m),
            "reused_manifest_anchor_count": len(recorded[0]["anchors"]) if recorded else 0,
            "flow_pivots": [{key: found_offsets[o][key] for key in
                            ("offset","opcode","operand","symbol")} for o in focus],
        }
    return report

def audit(jar, javap_bin, prior_file):
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher JAR SHA or size drift")
    reference = json.loads(prior_file.read_text(encoding="utf-8"))
    require(reference["version"] == "1.0.10" and reference["artifact_sha256"] == SHA256
            and reference["evidence_grade"] == "SHA_EXACT_BINARY_BEHAVIOR",
            "Multiple Mint 1.0.10 exact reference contract drift")
    require(reference["resources"][ENCH] == EXPECTED_ENCH_SHA,
            "Seekcandy resource hash differs from certified prior")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP members")
        members = sorted(p for p in names if p.startswith(BASE) and p.endswith(".class"))
        require(100 <= len(members) <= 2500, "unbounded provider class universe")
        require(all(x in names for x in (ENCH, LANG, TAG, *METHODS.keys(), REGISTRY)),
                "selected provider binaries/resources absent")
        hits = [path for path in members if b"SEEKCANDY" in z.read(path)]
        require(1 <= len(hits) <= 15 and PRODUCER in hits and REGISTRY in hits,
                "missing/out of bound direct Seekcandy registry consumers")
        class_sha = {p: sha(z.read(p)) for p in (*METHODS, REGISTRY)}
        require(all(reference["classes"][p]["sha256"] == value for p,value in class_sha.items()),
                "classfile drift from same-JAR inherited manifest")
        raw_ench, raw_lang, raw_tag = z.read(ENCH), z.read(LANG), z.read(TAG)
        require(0 < len(raw_ench) < 4096 and sha(raw_ench) == EXPECTED_ENCH_SHA,
                "Seekcandy JSON blob drift")
        require(len(raw_lang) < 300000 and sha(raw_lang) == reference["resources"][LANG],
                "locale mismatch")
        require(len(raw_tag) < 4096 and sha(raw_tag) == reference["resources"][TAG],
                "sugar staff tag mismatch")
        enc = json.loads(raw_ench)
        locale = json.loads(raw_lang)
        tag = json.loads(raw_tag)
    require(enc.get("description") == {"translate":"enchantment.alexscaves.seekcandy"},
            "Seekcandy translation key drift")
    require(enc.get("supported_items") == "#alexscaves:enchantable/sugar_staff",
            "Seekcandy supported items changed")
    require(tag == {"values":["alexscaves:sugar_staff"]},
            "Seekcandy item family changed")
    translations = {k:v for k,v in locale.items() if
                    k.startswith("enchantment.alexscaves.seekcandy")}
    require("enchantment.alexscaves.seekcandy" in translations,
            "Seekcandy localization missing")
    paths = {cl:selected_methods(javap_bin, jar, cl, names, reference)
             for cl,names in METHODS.items()}
    evidence = {
        "schema_version":1, "scope":SCOPE,
        "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
        "evidence_grade":"SHA_EXACT_BINARY_BEHAVIOR",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "prior_exact_manifest_sha256":sha(prior_file.read_bytes()),
        "provider_class_census":{"scanned":len(members),
                                 "direct_seekcandy_class_hits":hits},
        "class_sha256":class_sha,
        "enchantment":{"id":"alexscaves:seekcandy","path":ENCH,
                       "sha256":sha(raw_ench),"size_bytes":len(raw_ench),"json":enc},
        "item_tag":{"path":TAG,"sha256":sha(raw_tag),"json":tag},
        "locale":{"path":LANG,"sha256":sha(raw_lang),"translations":translations},
        "selected_methods":paths,
        "limits":{"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                  "effective_damage":"NOT_TESTED","accepted_spawn":"NOT_TESTED",
                  "loaded_datapack":"NOT_VERIFIED","provider_universe_closed":False,
                  "mutation":"NO_MUTATION"},
    }
    require(len(json.dumps(evidence)) <= MAX_OUT,"over-budget selected JVM evidence")
    return evidence

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--jar",type=Path,required=True)
    cli.add_argument("--javap",default="javap")
    cli.add_argument("--prior",type=Path,default=Path(REFERENCE))
    cli.add_argument("--seal",type=Path)
    cli.add_argument("--output",type=Path)
    args=cli.parse_args()
    actual=audit(args.jar,args.javap,args.prior)
    if args.seal:
        require(json.loads(args.seal.read_text(encoding="utf-8")) == actual,
                "Seekcandy 1.0.10 static digest/flow seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(actual,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf-8")
    print("SEEKCANDY_STATIC_JSON="+json.dumps(actual,ensure_ascii=False,separators=(",",":")))
    print("SEEKCANDY_STATUS=STATIC_EXACT_READONLY_NO_MUTATION")
if __name__=="__main__": main()
