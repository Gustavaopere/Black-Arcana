#!/usr/bin/env python3
"""Bounded classfile annotation contract for Vanilla Backport NeoForge 1.1.7.10.

Inspect exact publisher JAR via javap -p -v and compare the compiled @Mixin,
@Inject, @ModifyArg, @ModifyReturnValue, and @WrapOperation metadata.
This is NOT a Mixin transformer/bootstrap test, target bytecode verifier,
physical multiplayer observation, or authorization for external perk mutation.
Third-party JAR/classfile/source is neither copied nor distributed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from zipfile import BadZipFile

from backported_012_perk_consumer_bytecode import METHOD, javap, unique
from vanillabackport_11710_mobility_bytecode import publisher_identity
from vanillabackport_11710_mixin_manifest import verify_archive as verify_manifest_archive

CLASSES = {
    "entity":"com.blackgear.vanillabackport.core.mixin.common.entities.EntityMixin",
    "living":"com.blackgear.vanillabackport.core.mixin.common.entities.LivingEntityMixin",
    "ranged":"com.blackgear.vanillabackport.core.mixin.common.attributes.RangedAttributeMixin",
}

TARGETS = {
    "entity":"Lnet/minecraft/world/entity/Entity;",
    "living":"Lnet/minecraft/world/entity/LivingEntity;",
    "ranged":"Lnet/minecraft/world/entity/ai/attributes/RangedAttribute;",
}
ANNOTATIONS = {
    "Inject":"org.spongepowered.asm.mixin.injection.Inject",
    "WrapOperation":"com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation",
    "ModifyReturnValue":"com.llamalad7.mixinextras.injector.ModifyReturnValue",
    "ModifyArg":"org.spongepowered.asm.mixin.injection.ModifyArg",
}

MOVE = "move(Lnet/minecraft/world/entity/MoverType;Lnet/minecraft/world/phys/Vec3;)V"
TRAVEL = "travel(Lnet/minecraft/world/phys/Vec3;)V"

METHODS = {
    "entity":[
        {
            "name":"vb$earlyCapture", "kind":"Inject", "target_method":MOVE,
            "at":"HEAD"
        },
        {
            "name":"vb$capture", "kind":"WrapOperation", "target_method":MOVE,
            "at":"INVOKE",
            "call_target":"Lnet/minecraft/world/entity/Entity;collide(Lnet/minecraft/world/phys/Vec3;)Lnet/minecraft/world/phys/Vec3;"
        },
        {
            "name":"vb$RestituteMovementAfterCollisions", "kind":"Inject", "target_method":MOVE,
            "at":"INVOKE",
            "call_target":"Lnet/minecraft/world/entity/Entity;tryCheckInsideBlocks()V"
        }
    ],
    "living":[
        {
            "name":"createLivingAttributes", "kind":"ModifyReturnValue",
            "target_method":"createLivingAttributes()Lnet/minecraft/world/entity/ai/attributes/AttributeSupplier$Builder;",
            "at":"RETURN"
        },
        {
            "name":"vb$handleMovementFriction", "kind":"ModifyArg", "target_method":TRAVEL,
            "at":"INVOKE",
            "call_target":"Lnet/minecraft/world/entity/LivingEntity;handleRelativeFrictionAndCalculateMovement(Lnet/minecraft/world/phys/Vec3;F)Lnet/minecraft/world/phys/Vec3;",
            "index":1
        },
        {
            "name":"vb$applyAirDrag", "kind":"WrapOperation", "target_method":TRAVEL,
            "at":"INVOKE",
            "call_target":"Lnet/minecraft/world/entity/LivingEntity;setDeltaMovement(DDD)V",
            "ordinal":3
        }
    ],
    "ranged":[
        {
            "name":"vb$fixKnockbackResistanceRange", "kind":"Inject",
            "target_method":"<init>(Ljava/lang/String;DDD)V",
            "at":"TAIL"
        }
    ]
}

def class_annotations(dis:str, label:str):
    # javap class-level RuntimeInvisibleAnnotations comes AFTER the closing
    # class brace. Constant pool entries do not count as annotation evidence.
    parts=dis.rsplit("\n}\n",1)
    if len(parts)!=2:
        raise ValueError("MIXIN_CLASS_TRAILER_MISSING:"+label)
    tail=parts[-1]
    if "RuntimeInvisibleAnnotations:" not in tail:
        raise ValueError("MIXIN_CLASS_ANNOTATION_SECTION_MISSING:"+label)
    pattern="org.spongepowered.asm.mixin.Mixin("
    if tail.count(pattern)!=1:
        raise ValueError("MIXIN_CLASS_ANNOTATION_CARDINALITY:"+label)
    literal="value=[class "+TARGETS[label]+"]"
    if literal not in tail:
        raise ValueError("MIXIN_CLASS_TARGET_DRIFT:"+label)
    return {"kind":"Mixin","target_descriptor":TARGETS[label],
            "retention":"RuntimeInvisibleAnnotations", "verified_in_classfile":True}

def get_method_annotation(dis:str, name:str):
    lines=dis.splitlines()
    headers=[i for i,line in enumerate(lines)
             if METHOD.match(line) and re.search(r"\s"+re.escape(name)+r"\(",line)]
    if len(headers)!=1:
        raise ValueError(f"INJECTION_METHOD_NOT_UNIQUE:{name}:count={len(headers)}")
    first=headers[0]
    end=next((j for j in range(first+1,len(lines))
              if METHOD.match(lines[j]) or lines[j]=="}"),len(lines))
    body="\n".join(lines[first:end])
    # Only the method's annotation list can establish the contract. Stop
    # before the following class member, never match constant-pool literals.
    if "    RuntimeVisibleAnnotations:\n" not in body:
        raise ValueError("INJECTION_METHOD_ANNOTATIONS_MISSING:"+name)
    annotation=body.split("    RuntimeVisibleAnnotations:\n",1)[1]
    # RuntimeVisibleAnnotations is emitted at method end, followed by
    # MethodParameters or RuntimeInvisibleAnnotations on some toolchains.
    for trailer in ["\n    MethodParameters:","\n    RuntimeInvisibleAnnotations:",
                    "\n    RuntimeInvisibleTypeAnnotations:"]:
        annotation=annotation.split(trailer,1)[0]
    return annotation

def check_spec(annotation:str,spec:dict):
    name=spec["name"]
    kind=spec["kind"]
    parent=ANNOTATIONS[kind]+"("
    if annotation.count(parent)!=1:
        raise ValueError(f"INJECTION_KIND_CARDINALITY:{name}:{kind}")
    for other_kind,other in ANNOTATIONS.items():
        if other_kind!=kind and other+"(" in annotation:
            raise ValueError("INJECTION_UNEXPECTED_EXTRA_ANNOTATION:"+name)

    target_method='method=["'+spec["target_method"]+'"]'
    if target_method not in annotation:
        raise ValueError("INJECTION_TARGET_METHOD_DRIFT:"+name)
    required_at='value="'+spec["at"]+'"'
    if "org.spongepowered.asm.mixin.injection.At(" not in annotation or required_at not in annotation:
        raise ValueError("INJECTION_AT_POINT_DRIFT:"+name)
    if spec.get("call_target") is not None:
        expected_call='target="'+spec["call_target"]+'"'
        if expected_call not in annotation:
            raise ValueError("INJECTION_INVOKE_TARGET_DRIFT:"+name)
    elif 'target="' in annotation:
        raise ValueError("INJECTION_UNEXPECTED_INVOKE_TARGET:"+name)

    if "ordinal" in spec:
        if not re.search(r"(?m)^\s+ordinal="+str(spec["ordinal"])+r"\s*$",annotation):
            raise ValueError("INJECTION_ORDINAL_DRIFT:"+name)
    elif re.search(r"(?m)^\s+ordinal=",annotation):
        raise ValueError("INJECTION_UNEXPECTED_ORDINAL:"+name)

    if "index" in spec:
        if not re.search(r"(?m)^\s+index="+str(spec["index"])+r"\s*$",annotation):
            raise ValueError("INJECTION_ARGUMENT_INDEX_DRIFT:"+name)
    elif re.search(r"(?m)^\s+index=",annotation):
        raise ValueError("INJECTION_UNEXPECTED_ARGUMENT_INDEX:"+name)

    return {
        "handler":name, "kind":kind,
        "target_method":spec["target_method"],
        "at":spec["at"], "invoke_target":spec.get("call_target"),
        "ordinal":spec.get("ordinal"), "index":spec.get("index"),
        "classfile_annotation_verified":True, "injection_applied":"NOT_VERIFIED"
    }

def analyze_verbose(dis:dict):
    if set(dis)!=set(CLASSES):
        raise ValueError("VERBOSE_REQUIRED_CLASS_SET_DRIFT")
    result={}
    for label,body in dis.items():
        result[label]={
            "mixin":class_annotations(body,label),
            "injections":[
                check_spec(get_method_annotation(body, spec["name"]),spec)
                for spec in METHODS[label]
            ]
        }

    # The RangedAttribute mixin targets a knockback-resistance constructor.
    # Do not pretend its presence implements bounciness attribute clamping.
    return {
        "status":"PASS_VANILLABACKPORT_11710_COMPILED_MIXIN_INJECTION_DECLARATIONS",
        "evidence_class":"EXACT_PUBLISHER_VERBOSE_CLASSFILE_INJECTION_ANNOTATIONS",
        "classes":result,
        "scoped_handler_count":sum(len(v) for v in METHODS.values()),
        "ranged_attribute_note":"ctor inject TAIL; knockback-resistance source behavior, not bounciness limit proof",
        "limitations":[
            "No actual Mixin application, target method existence in patched host, ordinal resolution or invocation count proved.",
            "No NeoForge runtime, Minecraft client/server, loaded modpack or user physical JAR hash compared.",
            "No generated external provider setter/perk adapter; consumer source and compiled annotations are read-only."
        ],
        "deviations":[]
    }

class InjectionRegression(unittest.TestCase):
    @staticmethod
    def annotation(spec):
        kind=ANNOTATIONS[spec["kind"]]
        method=spec["target_method"]
        at=spec["at"]
        call=spec.get("call_target")
        target=('\n    target="'+call+'"' if call else "")
        ordtxt=('\n    ordinal='+str(spec["ordinal"]) if "ordinal" in spec else "")
        indtxt=('\n  index='+str(spec["index"]) if "index" in spec else "")
        return (kind+'(\n  method=["'+method+'"]\n'
                +'  at=[@org.spongepowered.asm.mixin.injection.At(\n    value="'+at+'"'
                +target+ordtxt+'\n  )]'+indtxt+'\n)')

    def test_all_spec_synthetic_annotations(self):
        self.assertEqual(sum(len(x) for x in METHODS.values()),7)
        for group in METHODS.values():
            for s in group:
                self.assertTrue(check_spec(self.annotation(s),s)["classfile_annotation_verified"])

    def test_wrong_method_rejected(self):
        s=METHODS["entity"][0]
        with self.assertRaisesRegex(ValueError,"INJECTION_TARGET_METHOD_DRIFT"):
            check_spec(self.annotation(s).replace("move(","run("),s)

    def test_wrong_injection_type_rejected(self):
        s=METHODS["entity"][1]
        with self.assertRaisesRegex(ValueError,"INJECTION_KIND_CARDINALITY"):
            check_spec(self.annotation(s).replace("WrapOperation(","Inject("),s)

    def test_wrong_head_at_rejected(self):
        s=METHODS["entity"][0]
        with self.assertRaisesRegex(ValueError,"INJECTION_AT_POINT_DRIFT"):
            check_spec(self.annotation(s).replace('value="HEAD"','value="TAIL"'),s)

    def test_wrong_invoke_target_rejected(self):
        s=METHODS["entity"][2]
        with self.assertRaisesRegex(ValueError,"INJECTION_INVOKE_TARGET_DRIFT"):
            check_spec(self.annotation(s).replace("tryCheckInsideBlocks()V","move()V"),s)

    def test_missing_ordinal_rejected(self):
        s=METHODS["living"][2]
        with self.assertRaisesRegex(ValueError,"INJECTION_ORDINAL_DRIFT"):
            check_spec(self.annotation(s).replace("ordinal=3","ordinal=2"),s)

    def test_missing_argument_index_rejected(self):
        s=METHODS["living"][1]
        with self.assertRaisesRegex(ValueError,"INJECTION_ARGUMENT_INDEX_DRIFT"):
            check_spec(self.annotation(s).replace("index=1","index=0"),s)

    def test_wrong_mixin_class_target_rejected(self):
        desc="org.spongepowered.asm.mixin.Mixin(\n  value=[class Lnet/minecraft/world/entity/Player;]\n)"
        with self.assertRaisesRegex(ValueError,"MIXIN_CLASS_TARGET_DRIFT"):
            class_annotations("header\n}\nRuntimeInvisibleAnnotations:\n"+desc,"entity")

    def test_cloned_annotations_rejected(self):
        s=METHODS["entity"][0]
        with self.assertRaisesRegex(ValueError,"INJECTION_KIND_CARDINALITY"):
            check_spec(self.annotation(s)+"\n"+self.annotation(s),s)

    def test_unexpected_ordinal_rejected(self):
        s=METHODS["entity"][0]
        with self.assertRaisesRegex(ValueError,"INJECTION_UNEXPECTED_ORDINAL"):
            check_spec(self.annotation(s).replace('value="HEAD"','value="HEAD"\n ordinal=3'),s)

    def test_missing_class_set_rejected(self):
        with self.assertRaisesRegex(ValueError,"VERBOSE_REQUIRED_CLASS_SET_DRIFT"):
            analyze_verbose({})

    def test_wrong_file_identity_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d:
            p=Path(d)/"not-the-publisher.jar"
            p.write_bytes(b"not a JAR")
            with self.assertRaisesRegex(ValueError,"PUBLISHER_SIZE_DRIFT"):
                publisher_identity(p)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--jar",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(InjectionRegression))
        return 0 if result.wasSuccessful() else 1
    if args.jar is None or args.output is None:
        ap.error("--jar and --output are required")
    try:
        exact=publisher_identity(args.jar)
        manifest=verify_manifest_archive(args.jar)
        if manifest["status"]!="PASS_VANILLABACKPORT_11710_MIXIN_MANIFEST_BOUNDARY":
            raise ValueError("MANIFEST_PRECONDITION_MISSING")
        dis={}
        for key,clazz in CLASSES.items():
            dis[key]=subprocess.run(
                ["javap","-p","-v","-classpath",str(args.jar),clazz],
                check=True,capture_output=True,text=True).stdout
        report=analyze_verbose(dis)
        report["publisher"]=exact
        report["manifest_status"]=manifest["status"]
    except (OSError, ValueError, subprocess.CalledProcessError, BadZipFile) as exc:
        report={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"]}))
    return 0 if report["status"]=="PASS_VANILLABACKPORT_11710_COMPILED_MIXIN_INJECTION_DECLARATIONS" else 2

if __name__=="__main__":
    sys.exit(main())
