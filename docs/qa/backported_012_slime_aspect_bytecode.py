#!/usr/bin/env python3
"""Bounded SHA-matched publisher bytecode audit for Backported Spellbooks Slime Aspect.

This proves selected classfile operations and reference order, not physical
movement, final attributes, source-build identity or a provider mutation hook.
No third-party bytecode is checked into this repository.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

from backported_012_perk_consumer_bytecode import hash_and_zip, javap, blocks, unique

CLASSES = {
    "spell": "net.redreaper.backported_spellbooks.spells.nature.AspectOfTheSlimeSpell",
    "effect": "net.redreaper.backported_spellbooks.effect.SlimeAspectMobEffect",
    "registry": "net.redreaper.backported_spellbooks.init.ModMobEffects",
}

def ordered(ops, expected, label):
    last = -1
    found = []
    for opcode, token in expected:
        candidates = [pc for pc, op, tail in ops
                      if pc > last and op == opcode and token in tail]
        if not candidates:
            raise ValueError(f"{label}: missing {opcode}/{token!r} after pc={last}")
        last = candidates[0]
        found.append(last)
    return found

def count(ops, name, required, label):
    pcs = [pc for pc, op, tail in ops
           if op.startswith("invoke") and name in tail]
    if len(pcs) != required:
        raise ValueError(f"{label}: call {name} count={len(pcs)} expected={required}")
    return pcs

def verify_cast(ops):
    pcs = ordered(ops, [
        ("getstatic", "ModMobEffects.SLIME_ASPECT:"),
        ("invokevirtual", "getSpellPower:"),
        ("ldc", "float 20.0f"),
        ("fmul", ""),
        ("f2i", ""),
        ("isub", ""),
        ("invokespecial", "MobEffectInstance."),
        ("invokevirtual", "LivingEntity.addEffect:"),
        ("invokespecial", "onCast:")
    ], "AspectOfTheSlimeSpell.onCast")
    count(ops, "LivingEntity.addEffect:", 1, "slime cast self buff")
    if any("DamageSources.applyDamage:" in tail for _,_,tail in ops):
        raise ValueError("SLIME_CAST_UNEXPECTED_DAMAGE_CALL")
    return {"effect_application_order_pcs": pcs,
            "duration_operand": "(int)(getSpellPower * 20.0f)",
            "amplifier_operand": "integer subtraction; exact operand checked by source, level-1 not fully proved in this gate",
            "target": "LivingEntity argument of onCast; self-only in source",
            "damage": "no direct DamageSources.applyDamage call in onCast"}

def verify_registry(dis):
    if "String slime_aspect" not in dis:
        raise ValueError("SLIME_REGISTRY_ID_MISSING")
    candidates = [(h, ops) for h, ops in blocks(dis)
                  if all(any(x in tail for _,_,tail in ops)
                         for x in ("ModAttributes.BOUNCINESS:",
                                   "Attributes.JUMP_STRENGTH:",
                                   "ModAttributes.AIR_DRAG_MODIFIER:"))]
    if len(candidates) != 1:
        raise ValueError(f"SLIME_MODIFIER_FACTORY_MISSING_OR_AMBIGUOUS count={len(candidates)}")
    header, ops = candidates[0]
    checks = [
        ("getstatic", "ModAttributes.BOUNCINESS:"),
        ("ldc2_w", "double 0.5d"),
        ("getstatic", "Operation.ADD_VALUE:"),
        ("invokevirtual", "addAttributeModifier:"),
        ("getstatic", "Attributes.JUMP_STRENGTH:"),
        ("ldc2_w", "double 0.15000000596046448d"),
        ("getstatic", "Operation.ADD_MULTIPLIED_TOTAL:"),
        ("invokevirtual", "addAttributeModifier:"),
        ("getstatic", "ModAttributes.AIR_DRAG_MODIFIER:"),
        ("ldc2_w", "double -0.10000000149011612d"),
        ("getstatic", "Operation.ADD_MULTIPLIED_TOTAL:"),
        ("invokevirtual", "addAttributeModifier:")
    ]
    pcs = ordered(ops, checks, "ModMobEffects slime modifier supplier")
    if count(ops, "addAttributeModifier:", 3, "slime modifier supplier") != pcs[3::4]:
        raise ValueError("SLIME_MODIFIER_EXTRA_OR_REORDERED_CALLS")
    if not any(op == "new" and "SlimeAspectMobEffect" in tail for _,op,tail in ops):
        raise ValueError("SLIME_EFFECT_CONSTRUCTOR_MISSING")
    return {"factory_header":header, "modifier_order_pcs":pcs,
            "float_to_double_conversion": "compiled modifiers call the double-taking addAttributeModifier, with float32 rounding observable as 0.15000000596046448d and -0.10000000149011612d",
            "attributes":[
                {"name":"BOUNCINESS","operation":"ADD_VALUE","coefficient":0.5},
                {"name":"JUMP_STRENGTH","operation":"ADD_MULTIPLIED_TOTAL","coefficient":0.15},
                {"name":"AIR_DRAG_MODIFIER","operation":"ADD_MULTIPLIED_TOTAL","coefficient":-0.10}],
            "limit":"source-aligned lambda factory; loaded effect attributes and bootstrap linking not exercised"}

def inspect(dis):
    if set(dis) != set(CLASSES):
        raise ValueError("REQUIRED_CLASS_SET_MISSING")
    return {
        "status": "PASS_BACKPORTED_012_SLIME_BOUNDED_BYTECODE",
        "evidence_class": "EXACT_PUBLISHER_COMPILED_CALLSITES_ONLY",
        "spell": verify_cast(unique(dis["spell"], "onCast")),
        "registry": verify_registry(dis["registry"]),
        "limitations": [
            "No measured mobility, attribute values, effect duration or live player.",
            "No host Iron's 3.16.3 / VanillaBackport attribute consumer tested.",
            "No complete control-flow proof, registry bootstrap linkage, or public perk hook.",
            "No Black Arcana/RPG Skill Tree adapter or Mastery event tested."
        ]
    }

class Tests(unittest.TestCase):
    @staticmethod
    def fixture(*items):
        return [(n * 4, op, tail) for n,(op,tail) in enumerate(items)]

    def test_order_accepts_three_attributes(self):
        x=self.fixture(*[
            ("getstatic","ModAttributes.BOUNCINESS:"),("ldc2_w","double 0.5d"),
            ("getstatic","Operation.ADD_VALUE:"),("invokevirtual","addAttributeModifier:"),
            ("getstatic","Attributes.JUMP_STRENGTH:"),("ldc2_w","double 0.15000000596046448d"),
            ("getstatic","Operation.ADD_MULTIPLIED_TOTAL:"),("invokevirtual","addAttributeModifier:"),
            ("getstatic","ModAttributes.AIR_DRAG_MODIFIER:"),("ldc2_w","double -0.10000000149011612d"),
            ("getstatic","Operation.ADD_MULTIPLIED_TOTAL:"),("invokevirtual","addAttributeModifier:")
        ])
        self.assertEqual(count(x,"addAttributeModifier:",3,"fixture"),[12,28,44])

    def test_wrong_bounce_coefficient_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.fixture(("ldc2_w","double 0.4000000059604645d")),
                    [("ldc2_w","double 0.5d")],"bounce")

    def test_wrong_jump_modifier_mode_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.fixture(("getstatic","Operation.ADD_VALUE:")),
                    [("getstatic","Operation.ADD_MULTIPLIED_TOTAL:")],"jump")

    def test_wrong_air_drag_sign_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.fixture(("ldc2_w","double 0.10000000149011612d")),
                    [("ldc2_w","double -0.10000000149011612d")],"air drag")

    def test_duplicate_modifier_call_rejected(self):
        with self.assertRaisesRegex(ValueError,"count"):
            count(self.fixture(*[("invokevirtual","addAttributeModifier:")]*4),
                  "addAttributeModifier:",3,"modifiers")

    def test_cast_missing_duration_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.fixture(("ldc","float 19.0f")),
                    [("ldc","float 20.0f")],"duration")

    def test_class_set_rejected(self):
        with self.assertRaisesRegex(ValueError,"REQUIRED_CLASS_SET_MISSING"):
            inspect({})

    def test_missing_method_rejected(self):
        with self.assertRaisesRegex(ValueError,"METHOD_MISSING_OR_AMBIGUOUS"):
            unique("class Empty{}", "onCast")

    def test_bad_publisher_hash_rejected(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.jar"
            p.write_bytes(b"wrong bytes")
            with self.assertRaisesRegex(ValueError,"JAR_SHA_MISMATCH"):
                hash_and_zip(p)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        ok=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if ok.wasSuccessful() else 1
    if not a.jar or not a.output:
        p.error("--jar and --output required")
    try:
        sha1=hash_and_zip(a.jar)
        with zipfile.ZipFile(a.jar) as jar:
            entries=set(jar.namelist())
        for name in CLASSES.values():
            if name.replace(".","/")+".class" not in entries:
                raise ValueError("JAR_CLASS_MISSING: "+name)
        result=inspect({k:javap(a.jar,v) for k,v in CLASSES.items()})
        result["publisher_sha1"]=sha1
        result["deviations"]=[]
    except (OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        result={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"deviations":result["deviations"]}))
    return 0 if result["status"]=="PASS_BACKPORTED_012_SLIME_BOUNDED_BYTECODE" else 2

if __name__ == "__main__":
    sys.exit(main())
