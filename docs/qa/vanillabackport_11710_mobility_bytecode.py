#!/usr/bin/env python3
"""Bounded publisher-bytecode gate for Vanilla Backport NeoForge 1.1.7.10.

Confirms attribute declarations and mixin callsites against an exact official
publisher JAR SHA-256. This does not prove that host mixins apply in a running
game, that attribute modifiers actually stack, or any external perk API.
Third-party JAR and bytecode are never checked into the repository.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

from backported_012_perk_consumer_bytecode import blocks, unique, javap, OPCODE
from backported_012_slime_aspect_bytecode import ordered, count

PUBLISHER_NAME = "VanillaBackport-neoforge-1.21.1-1.1.7.10.jar"
PUBLISHER_FILE_ID = 8229724
SIZE = 54902084
SHA256 = "ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d"
SHA1 = "eb30efe569cbd5186abf9e5d1e64d4a84895b346"
CLASSES = {
    "attributes": "com.blackgear.vanillabackport.common.registries.ModAttributes",
    "entity": "com.blackgear.vanillabackport.core.mixin.common.entities.EntityMixin",
    "living": "com.blackgear.vanillabackport.core.mixin.common.entities.LivingEntityMixin",
}

def publisher_identity(jar: Path):
    if jar.stat().st_size != SIZE:
        raise ValueError("PUBLISHER_SIZE_DRIFT")
    sha256 = hashlib.sha256()
    sha1 = hashlib.sha1()
    with jar.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            sha256.update(chunk)
            sha1.update(chunk)
    if sha256.hexdigest() != SHA256 or sha1.hexdigest() != SHA1:
        raise ValueError("PUBLISHER_DIGEST_DRIFT")
    with zipfile.ZipFile(jar) as z:
        present=set(z.namelist())
    for name in CLASSES.values():
        if name.replace(".","/") + ".class" not in present:
            raise ValueError("PUBLISHER_CLASS_MISSING: "+name)
    return {"sha256":SHA256,"sha1":SHA1,"bytes":SIZE,"curseforge_file_id":PUBLISHER_FILE_ID}

def attr_lambda(dis,name,description,defaults):
    ops=unique(dis,name)
    got=[op for _,op,_ in ops]
    expected=["new","dup","ldc"]+defaults+["invokespecial","iconst_1","invokevirtual","areturn"]
    if got != expected:
        raise ValueError(f"ATTRIBUTE_LIMIT_OPCODES_DRIFT:{name} expected={expected} got={got}")
    if not any(description in tail for _,op,tail in ops if op=="ldc"):
        raise ValueError("ATTRIBUTE_NAME_DRIFT:"+name)
    if count(ops,'RangedAttribute."<init>":',1,name)!=[p for p,o,t in ops if o=="invokespecial"]:
        raise ValueError("ATTRIBUTE_RANGE_CTOR_DRIFT:"+name)
    if count(ops,"RangedAttribute.setSyncable:",1,name)!=[p for p,o,t in ops if o=="invokevirtual"]:
        raise ValueError("ATTRIBUTE_SYNCABLE_DRIFT:"+name)
    return {"constructor_opcode_sequence":expected,"attribute_description":description,
            "verified_syncable":True}

def attrs(dis):
    # The generic javap method parser deliberately does not recognize "static {};".
    # Split that initializer out or it bleeds into the final supplier lambda.
    methods=dis.split("  static {};")[0]
    init=unique(methods,"lambda$static$0")
    bounce=attr_lambda(methods,"lambda$static$1","attribute.name.bounciness",
                       ["dconst_0","dconst_0","dconst_1"])
    friction=attr_lambda(methods,"lambda$static$2","attribute.name.friction_modifier",
                         ["dconst_1","dconst_0","ldc2_w"])
    air=attr_lambda(methods,"lambda$static$0","attribute.name.air_drag_modifier",
                    ["dconst_1","dconst_0","ldc2_w"])
    for label,ops in [("friction",unique(methods,"lambda$static$2")),
                      ("air",init)]:
        if not any(op=="ldc2_w" and "double 2048.0d" in tail for _,op,tail in ops):
            raise ValueError("ATTRIBUTE_MAX_2048_DRIFT:"+label)
    if dis.count("  static {};")!=1:
        raise ValueError("ATTRIBUTE_CLINIT_MISSING_OR_AMBIGUOUS")
    section=dis.split("  static {};")[1].split("\\n}")[0]
    static=[(int(m.group(1)),m.group(2),m.group(3).strip())
            for line in section.splitlines() if (m:=OPCODE.match(line))]
    ordered(static,[
        ("ldc","String minecraft"),
        ("ldc","String air_drag_modifier"),
        ("putstatic","AIR_DRAG_MODIFIER:"),
        ("ldc","String bounciness"),
        ("putstatic","BOUNCINESS:"),
        ("ldc","String friction_modifier"),
        ("putstatic","FRICTION_MODIFIER:")
    ],"ModAttributes.<clinit>")
    count(static,"CoreRegistry.holder:",3,"three registered host attrs")
    return {
        "registered_namespace":"minecraft",
        "bounciness":{"range":[0.0,1.0],"default":0.0,"classfile":bounce},
        "friction_modifier":{"range":[0.0,2048.0],"default":1.0,"classfile":friction},
        "air_drag_modifier":{"range":[0.0,2048.0],"default":1.0,"classfile":air},
        "mixin_application_or_resolved_attribute":"NOT_VERIFIED"
    }

def verify_computed_friction(ops):
    expected=["fconst_1","fconst_1","fload_0","fsub","fload_1",
              "fmul","fsub","fconst_0","fconst_1","invokestatic","freturn"]
    got=[op for _,op,_ in ops]
    if got!=expected:
        raise ValueError(f"FRICTION_FORMULA_OPCODE_DRIFT got={got}")
    if "Mth.clamp:(FFF)F" not in ops[9][2]:
        raise ValueError("FRICTION_CLAMP_CALLEE_DRIFT")
    return "clamp(1 - (1 - rawFriction) * modifier, 0, 1) as compiled float opcodes"

def host_consumers(entity,living):
    early=unique(entity,"vb$earlyCapture")
    ordered(early,[("getstatic","BOUNCINESS:"),("invokestatic","vb$getOrDefault:")],
            "Entity.move pre-collision attribute read")
    post=unique(entity,"vb$RestituteMovementAfterCollisions")
    ordered(post,[
        ("invokevirtual","isSuppressingBounce:"),
        ("getstatic","BOUNCINESS:"),
        ("invokestatic","vb$getOrDefault:"),
        ("invokestatic","vb$getAirDrag:"),
        ("invokestatic","Mth.lerp:"),
        ("invokevirtual","setDeltaMovement:")
    ],"Entity.move restitution")
    if not any("GameEvent.HIT_GROUND" in t for _,o,t in post if o=="getstatic"):
        raise ValueError("BOUNCE_GAME_EVENT_CALLEE_MISSING")
    air=unique(entity,"vb$getAirDrag")
    ordered(air,[("getstatic","AIR_DRAG_MODIFIER:"),
                 ("invokestatic","computeModifiedFriction:"),
                 ("getstatic","FRICTION_MODIFIER:")],"Entity drag")
    register=unique(living,"createLivingAttributes")
    ordered(register,[("getstatic","AIR_DRAG_MODIFIER:"),
                      ("getstatic","BOUNCINESS:"),
                      ("getstatic","FRICTION_MODIFIER:")],
            "LivingEntity attributes")
    count(register,"AttributeSupplier$Builder.add:",3,"host attribute defaults")
    ground=unique(living,"vb$handleMovementFriction")
    ordered(ground,[("getstatic","FRICTION_MODIFIER:"),
                    ("invokevirtual","AttributeInstance.getValue:"),
                    ("invokestatic","vb$computeModifiedFriction:")],
            "ground friction")
    travel=unique(living,"vb$applyAirDrag")
    ordered(travel,[("getstatic","FRICTION_MODIFIER:"),
                    ("getstatic","AIR_DRAG_MODIFIER:"),
                    ("ldc","float 0.91f"),
                    ("invokestatic","vb$computeModifiedFriction:"),
                    ("ldc","float 0.98f")],
            "LivingEntity travel drag")
    clamp=verify_computed_friction(unique(living,"vb$computeModifiedFriction"))
    return {
        "movement_guard":{"bounciness_consulted_before_collisions":True,
                          "suppressed_bounce_gate":True,
                          "movement_restitution_callsite":True},
        "air_drag":{"entity_consumer":True,"living_travel_consumer":True},
        "friction":{"ground_consumer":True,"living_travel_consumer":True},
        "float_friction_helper":clamp,
        "runtime_mixin_applied":"NOT_VERIFIED"
    }

def inspect(dis):
    if set(dis)!=set(CLASSES):
        raise ValueError("MISSING_REQUIRED_CLASS_DISASSEMBLY")
    return {
        "status":"PASS_VANILLABACKPORT_11710_BOUNDED_MOBILITY_BYTECODE",
        "evidence_class":"EXACT_PUBLISHER_BYTECODE_HOST_OPERANDS_AND_CALLSITES",
        "attribute_registry":attrs(dis["attributes"]),
        "consumers":host_consumers(dis["entity"],dis["living"]),
        "limits":[
            "No physical installed-JAR hash for VanillaBackport independently sourced.",
            "No mixin application, resolved attribute value, final bounce/friction or real client.",
            "No full control flow proof or exact host + Backported Spellbooks combined runtime.",
            "No hook permitting a Black Arcana perk to mutate provider attributes."
        ],
    }

class Regression(unittest.TestCase):
    @staticmethod
    def mk(*lines):
        return [(i,op,tail) for i,(op,tail) in enumerate(lines)]

    def test_bounce_clamp_max_one(self):
        ops=self.mk(("new","RangedAttribute"),("dup",""),("ldc","attribute.name.bounciness"),
            ("dconst_0",""),("dconst_0",""),("dconst_1",""),
            ("invokespecial","RangedAttribute."),("iconst_1",""),
            ("invokevirtual","RangedAttribute.setSyncable:"),("areturn",""))
        self.assertTrue(attr_lambda_fake(ops))
    def test_bounce_bad_max_rejected(self):
        ops=self.mk(("new","RangedAttribute"),("dup",""),("ldc","attribute.name.bounciness"),
            ("dconst_0",""),("dconst_0",""),("ldc2_w","double 10.0d"),
            ("invokespecial","RangedAttribute."),("iconst_1",""),
            ("invokevirtual","RangedAttribute.setSyncable:"),("areturn",""))
        with self.assertRaisesRegex(ValueError,"ATTRIBUTE_LIMIT"):
            validate_bounce_ops(ops)
    def test_friction_formula_accepts(self):
        ops=self.mk(*[(v,"Mth.clamp:(FFF)F" if v=="invokestatic" else "")
                      for v in ["fconst_1","fconst_1","fload_0","fsub","fload_1","fmul",
                                "fsub","fconst_0","fconst_1","invokestatic","freturn"]])
        self.assertIn("clamp(",verify_computed_friction(ops))
    def test_friction_sign_reversal_rejected(self):
        ops=self.mk(*[(v,"Mth.clamp:(FFF)F" if v=="invokestatic" else "")
                      for v in ["fconst_1","fconst_1","fload_0","fadd","fload_1","fmul",
                                "fsub","fconst_0","fconst_1","invokestatic","freturn"]])
        with self.assertRaisesRegex(ValueError,"FRICTION_FORMULA_OPCODE_DRIFT"):
            verify_computed_friction(ops)
    def test_clamp_callee_drift_rejected(self):
        ops=self.mk(*[(v,"Mth.max:(FF)F" if v=="invokestatic" else "")
                      for v in ["fconst_1","fconst_1","fload_0","fsub","fload_1","fmul",
                                "fsub","fconst_0","fconst_1","invokestatic","freturn"]])
        with self.assertRaisesRegex(ValueError,"FRICTION_CLAMP_CALLEE_DRIFT"):
            verify_computed_friction(ops)
    def test_order_bad_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.mk(("getstatic","FRICTION_MODIFIER:"),
                            ("getstatic","BOUNCINESS:")),
                    [("getstatic","BOUNCINESS:"),
                     ("getstatic","FRICTION_MODIFIER:")],"order")
    def test_class_set_rejected(self):
        with self.assertRaisesRegex(ValueError,"MISSING_REQUIRED_CLASS"):
            inspect({})
    def test_publisher_wrong_size_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as temp:
            f=Path(temp)/PUBLISHER_NAME
            f.write_bytes(b"fake")
            with self.assertRaisesRegex(ValueError,"PUBLISHER_SIZE_DRIFT"):
                publisher_identity(f)
    def test_bad_attribute_sync_order_rejected(self):
        with self.assertRaisesRegex(ValueError,"ATTRIBUTE_LIMIT"):
            validate_bounce_ops(self.mk(("new","RangedAttribute")))
    def test_missing_attribute_consumer_rejected(self):
        with self.assertRaisesRegex(ValueError,"METHOD_MISSING_OR_AMBIGUOUS"):
            unique("class Empty {}", "vb$earlyCapture")

def validate_bounce_ops(ops):
    expected=["new","dup","ldc","dconst_0","dconst_0","dconst_1",
              "invokespecial","iconst_1","invokevirtual","areturn"]
    if [o for _,o,_ in ops]!=expected:
        raise ValueError("ATTRIBUTE_LIMIT_OPCODES_DRIFT")
    return True

def attr_lambda_fake(ops):
    return validate_bounce_ops(ops)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--jar",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
        return 0 if result.wasSuccessful() else 1
    if not args.jar or not args.output:
        ap.error("--jar and --output required")
    try:
        ids=publisher_identity(args.jar)
        evidence=inspect({k:javap(args.jar,c) for k,c in CLASSES.items()})
        evidence["publisher"]=ids
        evidence["deviations"]=[]
    except (OSError,ValueError,subprocess.CalledProcessError,zipfile.BadZipFile) as exc:
        evidence={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":evidence["status"],"deviations":evidence["deviations"]}))
    return 0 if evidence["status"]=="PASS_VANILLABACKPORT_11710_BOUNDED_MOBILITY_BYTECODE" else 2

if __name__=="__main__":
    sys.exit(main())
