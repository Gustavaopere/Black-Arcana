#!/usr/bin/env python3
"""Check exact 1.21.1 vanilla target *declarations* against official Mojang mappings.

This does not prove NeoForge's patched runtime, callsite ordinal/index,
loaded mixin transformation, physical Minecraft server or player behavior.
No Mojang mapping contents are checked into this repo or uploaded to artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
import unittest

MC_VERSION = "1.21.1"
MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
TARGETS = {
    "net.minecraft.world.entity.Entity": [
        ("move","void",("net.minecraft.world.entity.MoverType","net.minecraft.world.phys.Vec3")),
        ("collide","net.minecraft.world.phys.Vec3",("net.minecraft.world.phys.Vec3",)),
        ("tryCheckInsideBlocks","void",()),
        ("setDeltaMovement","void",("double","double","double"))
    ],
    "net.minecraft.world.entity.LivingEntity": [
        ("travel","void",("net.minecraft.world.phys.Vec3",)),
        ("createLivingAttributes","net.minecraft.world.entity.ai.attributes.AttributeSupplier$Builder",()),
        ("handleRelativeFrictionAndCalculateMovement","net.minecraft.world.phys.Vec3",
         ("net.minecraft.world.phys.Vec3","float"))
    ],
    "net.minecraft.world.entity.ai.attributes.RangedAttribute": []
}
# Original ProGuard mapping methods appear as:
#     45:47:void move(net.minecraft.world.entity.MoverType,net.minecraft.world.phys.Vec3) -> a
# or:
#     void someMethod() -> a
# The class lines are fully qualified named classes with no indentation.
CLASS = re.compile(r"^([\w.$]+) -> [\w.$]+:$")
METHOD = re.compile(r"^(?:(?:\d+:\d+:)+)?(\S+)\s+([\w$<>]+)\(([^)]*)\)\s+->\s+\S+$")

def official_get(url: str, cap: int=25000000):
    if not url.startswith(("https://piston-meta.mojang.com/", "https://piston-data.mojang.com/")):
        raise ValueError("UNTRUSTED_MOJANG_DOWNLOAD_URL")
    req=Request(url,headers={"User-Agent":"BlackArcanaProviderTargetAudit/1.0"})
    with urlopen(req, timeout=55) as r:
        payload=r.read(cap+1)
    if len(payload)>cap:
        raise ValueError("MOJANG_DOWNLOAD_SIZE_LIMIT")
    return payload

def official_version_downloads():
    idx=json.loads(official_get(MANIFEST,5000000))
    matches=[v for v in idx["versions"] if v.get("id")==MC_VERSION and v.get("type")=="release"]
    if len(matches)!=1:
        raise ValueError("OFFICIAL_MINECRAFT_VERSION_NOT_UNIQUE")
    entry=matches[0]
    raw=official_get(entry["url"],300000)
    if hashlib.sha1(raw).hexdigest()!=entry["sha1"]:
        raise ValueError("VERSION_METADATA_SHA1_MISMATCH")
    meta=json.loads(raw)
    if meta["id"]!=MC_VERSION:
        raise ValueError("VERSION_JSON_ID_DRIFT")
    return {"releaseTime":meta.get("releaseTime"),"json_sha1":entry["sha1"],
            "downloads":meta["downloads"]}

def mapping_class_methods(data: str, wanted: set[str]):
    result={k:set() for k in wanted}
    seen=set()
    current=None
    for line in data.splitlines():
        top=CLASS.fullmatch(line)
        if top:
            current=top.group(1) if top.group(1) in wanted else None
            if current is not None: seen.add(current)
            continue
        if current is None or not line.startswith("    "):
            continue
        body=line.strip()
        match=METHOD.fullmatch(body)
        if not match: continue
        ret,name,raw_args=match.groups()
        args=tuple(raw_args.split(",")) if raw_args else ()
        result[current].add((name,ret,args))
    return result,seen

def validate_mappings(mapping: str, side: str):
    actual,seen=mapping_class_methods(mapping,set(TARGETS))
    missing_classes=sorted(set(TARGETS)-seen)
    if missing_classes:
        raise ValueError(f"{side.upper()}_TARGET_CLASSES_MISSING: {missing_classes}")
    proofs=[]
    for clazz,methods in TARGETS.items():
        for method in methods:
            if method not in actual[clazz]:
                raise ValueError(f"{side.upper()}_METHOD_DECLARATION_MISSING: {clazz}::{method}")
            proofs.append({"class":clazz,"method":method[0],"return":method[1],
                           "parameters":list(method[2]),"method_declared_in_official_mappings":True})
    return {"side":side,"class_count":len(seen),"method_count":len(proofs),
            "mapped_target_declarations":proofs,
            "limits":"mapping source names/parameters only; no target bytecode invocation counts"}

def verify(downloads: dict):
    report={"status":"PASS_MINECRAFT_1211_OFFICIAL_TARGET_MAPPINGS",
            "evidence_class":"OFFICIAL_VERSION_PINNED_NAMED_METHOD_DECLARATIONS",
            "minecraft_version":MC_VERSION,
            "version_json_sha1":downloads["json_sha1"],
            "releaseTime":downloads["releaseTime"],
            "mappings":{},"deviations":[]}
    for side in ("server","client"):
        item=downloads["downloads"][side+"_mappings"]
        body=official_get(item["url"],15000000)
        actual_hash=hashlib.sha1(body).hexdigest()
        if actual_hash!=item["sha1"]:
            raise ValueError("OFFICIAL_MOJANG_MAPPING_HASH_DRIFT:"+side)
        parsed=validate_mappings(body.decode("utf-8"),side)
        report["mappings"][side]={"official_sha1":actual_hash,"bytes":len(body),
                                  "evidence":parsed}
    report["limitations"]=[
        "Official Mojang mappings are NOT a NeoForge 21.1.250 patched target jar.",
        "No guarantee of Mixin matching @At target, invocation cardinality, or ordinal=3.",
        "RangedAttribute constructor is not mapped as an ordinary method; class only.",
        "No client boot, player movement, loaded mixin, physical profile hash or perk adapter.",
        "Only class + named method descriptors on published 1.21.1 mappings are proven."
    ]
    return report

class Regression(unittest.TestCase):
    def setUp(self):
        self.mappings=(
            "net.minecraft.world.entity.Entity -> a:\n"
            "    1:2:void move(net.minecraft.world.entity.MoverType,net.minecraft.world.phys.Vec3) -> a\n"
            "    1:2:net.minecraft.world.phys.Vec3 collide(net.minecraft.world.phys.Vec3) -> b\n"
            "    void tryCheckInsideBlocks() -> c\n"
            "    void setDeltaMovement(double,double,double) -> d\n"
            "net.minecraft.world.entity.LivingEntity -> b:\n"
            "    void travel(net.minecraft.world.phys.Vec3) -> a\n"
            "    net.minecraft.world.entity.ai.attributes.AttributeSupplier$Builder createLivingAttributes() -> b\n"
            "    net.minecraft.world.phys.Vec3 handleRelativeFrictionAndCalculateMovement(net.minecraft.world.phys.Vec3,float) -> c\n"
            "net.minecraft.world.entity.ai.attributes.RangedAttribute -> c:\n"
        )
    def test_matching_methods(self):
        r=validate_mappings(self.mappings,"server")
        self.assertEqual(r["method_count"],7)
    def test_class_missing_rejected(self):
        s=self.mappings.replace("net.minecraft.world.entity.ai.attributes.RangedAttribute -> c:\n","")
        with self.assertRaisesRegex(ValueError,"TARGET_CLASSES_MISSING"):
            validate_mappings(s,"server")
    def test_method_removed_rejected(self):
        s=self.mappings.replace("    void tryCheckInsideBlocks() -> c\n","")
        with self.assertRaisesRegex(ValueError,"METHOD_DECLARATION_MISSING"):
            validate_mappings(s,"server")
    def test_wrong_parameter_type_rejected(self):
        s=self.mappings.replace("setDeltaMovement(double,double,double)","setDeltaMovement(float,float,float)")
        with self.assertRaisesRegex(ValueError,"METHOD_DECLARATION_MISSING"):
            validate_mappings(s,"server")
    def test_wrong_return_type_rejected(self):
        s=self.mappings.replace("void travel(","boolean travel(")
        with self.assertRaisesRegex(ValueError,"METHOD_DECLARATION_MISSING"):
            validate_mappings(s,"server")
    def test_method_unindented_rejected(self):
        s=self.mappings.replace("    void tryCheckInsideBlocks()","void tryCheckInsideBlocks()")
        with self.assertRaisesRegex(ValueError,"METHOD_DECLARATION_MISSING"):
            validate_mappings(s,"server")
    def test_untrusted_url_rejected(self):
        with self.assertRaisesRegex(ValueError,"UNTRUSTED_MOJANG_DOWNLOAD_URL"):
            official_get("https://www.example.com/not-a-mapping")
    def test_static_synthetic_drift(self):
        with self.assertRaisesRegex(ValueError,"METHOD_DECLARATION_MISSING"):
            validate_mappings(self.mappings.replace("createLivingAttributes()","other()"),"client")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:
        ok=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
        return 0 if ok.wasSuccessful() else 1
    if args.output is None: p.error("--output required")
    try:
        report=verify(official_version_downloads())
    except (ValueError,KeyError,OSError,UnicodeError) as error:
        report={"status":"FAIL_CLOSED","deviations":[str(error)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"]}))
    return 0 if report["status"]=="PASS_MINECRAFT_1211_OFFICIAL_TARGET_MAPPINGS" else 2

if __name__=="__main__":
    sys.exit(main())
