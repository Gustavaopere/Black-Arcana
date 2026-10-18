#!/usr/bin/env python3
"""Fail-closed bounded callsite audit on exact NeoForge 21.1.250 server patch.

Distinguishes patched Entity/LivingEntity classes from the mapped Minecraft SRG
base used to supply RangedAttribute. Never claims Mixin transform/runtime proof.
No Mojang/NeoForge JAR or proprietary code redistributed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import unittest
import zipfile

from minecraft_1211_vanilla_target_callsites import (
    exact_method, matched_calls, javap_class
)

NEOFORGE_VERSION="21.1.250"
MINECRAFT_VERSION="1.21.1"
INSTALLER_SHA256="0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60"
PATCHED_SHA256="1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359"
BASE_SRG_SHA256="26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71"
INSTALLER="neoforge-21.1.250-installer.jar"
PATCHED="libraries/net/neoforged/neoforge/21.1.250/neoforge-21.1.250-server.jar"
SRG="libraries/net/minecraft/server/1.21.1-20240808.144430/server-1.21.1-20240808.144430-srg.jar"
ENTITY="net.minecraft.world.entity.Entity"
LIVING="net.minecraft.world.entity.LivingEntity"
RANGED="net.minecraft.world.entity.ai.attributes.RangedAttribute"
VEC="net.minecraft.world.phys.Vec3"
ENTRIES={
    PATCHED: {"net/minecraft/world/entity/Entity.class",
              "net/minecraft/world/entity/LivingEntity.class"},
    SRG: {"net/minecraft/world/entity/ai/attributes/RangedAttribute.class"}
}

def exact_hash(path:Path, expected:str):
    if not path.is_file():
        raise ValueError("EXACT_NEOFORGE_ARTIFACT_MISSING:"+path.name)
    sha=hashlib.sha256()
    with path.open("rb") as stream:
        for buf in iter(lambda:stream.read(1048576),b""):
            sha.update(buf)
    if sha.hexdigest()!=expected:
        raise ValueError("NEOFORGE_211250_SHA256_DRIFT:"+path.name)
    return {"sha256":sha.hexdigest(),"bytes":path.stat().st_size}

def package_identity(root:Path):
    found={}
    for name,expected in ((INSTALLER,INSTALLER_SHA256),
                          (PATCHED,PATCHED_SHA256),(SRG,BASE_SRG_SHA256)):
        path=root/name
        found[name]=exact_hash(path,expected)
        if name in ENTRIES:
            with zipfile.ZipFile(path) as zipfile_obj:
                names=set(zipfile_obj.namelist())
            missing=ENTRIES[name]-names
            if missing: raise ValueError("NEOFORGE_REQUIRED_CLASS_MISSING:"+str(sorted(missing)))
    # Required split: patched overlays two movement classes while RangedAttribute
    # comes from mapped base. Never treat SRG base alone as NeoForge-patched.
    with zipfile.ZipFile(root/PATCHED) as z:
        if "net/minecraft/world/entity/ai/attributes/RangedAttribute.class" in set(z.namelist()):
            raise ValueError("PATCHED_RANGE_CLASS_COMPOSITION_CHANGED")
    return found

def inspect(root:Path):
    hashes=package_identity(root)
    patched=root/PATCHED
    base=root/SRG
    ent=javap_class(patched,ENTITY)
    living=javap_class(patched,LIVING)
    ranged=javap_class(base,RANGED)
    move=exact_method(ent,"move","(Lnet/minecraft/world/entity/MoverType;Lnet/minecraft/world/phys/Vec3;)V")
    travel=exact_method(living,"travel","(Lnet/minecraft/world/phys/Vec3;)V")
    ctor=exact_method(ranged,"RangedAttribute","(Ljava/lang/String;DDD)V")

    calls=[
        {"edge":"NeoForge patched Entity.move -> collide",
         "callsites":matched_calls(move,"collide",
             "(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;",
             {ENTITY})},
        {"edge":"NeoForge patched Entity.move -> tryCheckInsideBlocks",
         "callsites":matched_calls(move,"tryCheckInsideBlocks","()V",{ENTITY})},
        {"edge":"NeoForge patched LivingEntity.travel -> handleRelativeFrictionAndCalculateMovement",
         "callsites":matched_calls(travel,"handleRelativeFrictionAndCalculateMovement",
             "(Lnet/minecraft/world/phys/Vec3;F)Lnet/minecraft/world/phys/Vec3;",
             {LIVING})},
        {"edge":"NeoForge patched LivingEntity.travel -> setDeltaMovement(DDD)",
         "callsites":matched_calls(travel,"setDeltaMovement","(DDD)V",
             {ENTITY,LIVING})},
    ]
    for index,spec in enumerate(calls):
        expected=4 if index==3 else 1
        if len(spec["callsites"])!=expected:
            raise ValueError("NEOFORGE_211250_PATCHED_CALLSITE_DRIFT:"+
                             spec["edge"]+":found="+str(len(spec["callsites"]))+
                             ":expected="+str(expected))
        spec["count"]=expected
    fourth_pc=calls[3]["callsites"][3]["pc"]
    return {
        "status":"PASS_NEOFORGE_211250_PATCHED_SERVER_TARGET_CALLSITES",
        "evidence_class":"EXACT_INSTALLER_GENERATED_PATCHED_SERVER_BYTECODE_ONLY",
        "minecraft_version":MINECRAFT_VERSION,
        "neoforge_version":NEOFORGE_VERSION,
        "exact_sha256":hashes,
        "artifact_composition":{
            "patched_entity_living_jar":PATCHED,
            "mapped_base_ranged_attribute_jar":SRG
        },
        "invocation_edges":calls,
        "ordinal3":{
            "target":"LivingEntity.travel -> setDeltaMovement(DDD)V",
            "zero_based_ordinal":3,
            "patched_server_fourth_pc":fourth_pc,
            "patched_server_callsite_count":4,
            "limit":"pre-application of optional modpack mixins; ordinal may change after other transformers"
        },
        "ranged_attribute_constructor":{
            "class_source":SRG,
            "descriptor":"(Ljava/lang/String;DDD)V",
            "classfile_verified":True,
            "lines_in_javap_method":len(ctor)
        },
        "limitations":[
            "This is server-patched NeoForge 21.1.250 classfile, not full modpack runtime.",
            "Does not prove Vanilla Backport 1.1.7.10 Mixin was applied.",
            "Does not prove ordering of other mods' Mixin transformations or actual target callback fire.",
            "Does not prove CLIENT NeoForge patch classfiles or connected multiplayer behaviour.",
            "Does not authorize RPG perk hook, player attribute mutation or Mastery awards."
        ],
        "deviations":[]
    }

class Regression(unittest.TestCase):
    def test_exact_hash_wrong_file_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/INSTALLER
            p.write_bytes(b"wrong binary")
            with self.assertRaisesRegex(ValueError,"NEOFORGE_211250_SHA256_DRIFT"):
                exact_hash(p,INSTALLER_SHA256)
    def test_absent_artifact_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"EXACT_NEOFORGE_ARTIFACT_MISSING"):
                package_identity(Path(tmp))
    def test_exact_single_move_call(self):
        lines=["   117: invokevirtual #44  // Method net/minecraft/world/entity/Entity.collide:(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;"]
        got=matched_calls(lines,"collide",
          "(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;",{ENTITY})
        self.assertEqual(len(got),1)
    def test_other_owner_not_counted(self):
        lines=["   117: invokevirtual #44  // Method some/other/Class.collide:(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;"]
        got=matched_calls(lines,"collide",
          "(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;",{ENTITY})
        self.assertEqual(len(got),0)
    def test_fourth_pc_synthetic(self):
        lines=[f"   {i*10}: invokevirtual #13  // Method net/minecraft/world/entity/LivingEntity.setDeltaMovement:(DDD)V" for i in range(4)]
        calls=matched_calls(lines,"setDeltaMovement","(DDD)V",{ENTITY,LIVING})
        self.assertEqual(len(calls),4)
        self.assertEqual(calls[3]["pc"],30)
    def test_wrong_overload_rejected(self):
        lines=["   8: invokevirtual #13  // Method net/minecraft/world/entity/LivingEntity.setDeltaMovement:(Lnet/minecraft/world/phys/Vec3;)V"]
        self.assertEqual(len(matched_calls(lines,"setDeltaMovement","(DDD)V",{ENTITY,LIVING})),0)
    def test_nonexistent_constructor_rejected(self):
        with self.assertRaisesRegex(ValueError,"TARGET_METHOD_DECLARATION_NOT_UNIQUE"):
            exact_method("class RangedAttribute {\n}\n","RangedAttribute","(Ljava/lang/String;DDD)V")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
        return 0 if result.wasSuccessful() else 1
    if not args.root or not args.output:
        p.error("--root and --output required")
    try:
        report=inspect(args.root)
    except (OSError,ValueError,zipfile.BadZipFile,subprocess.CalledProcessError) as exc:
        report={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"],
                      "calls":[[v["edge"],len(v["callsites"])] for v in report.get("invocation_edges",[])],
                      "ordinal3":report.get("ordinal3")}))
    return 0 if report["status"]=="PASS_NEOFORGE_211250_PATCHED_SERVER_TARGET_CALLSITES" else 2

if __name__=="__main__":
    sys.exit(main())
