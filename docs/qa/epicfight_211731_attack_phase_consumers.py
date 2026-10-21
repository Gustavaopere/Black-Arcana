#!/usr/bin/env python3
"""Read-only exact-publisher Epic Fight AttackPhase property consumer probe.

Checks method-bounded compiler references, numeric armor calculation markers
and ordered ResultCalculator opcodes. SHA-gates exact Epic Fight 21.17.3.1.
This is NOT gameplay, proof of active mixin injection, a generalized Java
dataflow verifier, effective HP damage, or permission to implement an adapter.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from epicfight_211731_trident_causal import inspect as inspect_publisher, blocks, instructions, javap
from epicfight_211731_trident_attack_phase import evaluate as evaluate_phase

CLASSES = {
    "calculator": "yesman.epicfight.api.utils.math.ValueModifier$ResultCalculator",
    "adder": "yesman.epicfight.api.utils.math.ValueModifier$Adder",
    "multiplier": "yesman.epicfight.api.utils.math.ValueModifier$Multiplier",
    "setter": "yesman.epicfight.api.utils.math.ValueModifier$Setter",
    "attack": "yesman.epicfight.api.animation.types.AttackAnimation",
    "source": "yesman.epicfight.world.damagesource.EpicFightDamageSource",
    "armor_mixin": "yesman.epicfight.mixin.common.MixinLivingEntity",
}


def method(disasm: str, method_name: str, signature_prefix: str = ""):
    selected = [(name, code) for name, code in blocks(disasm)
                if method_name + "(" in name and
                (not signature_prefix or
                 method_name + "(" + signature_prefix in name)]
    if len(selected) != 1:
        raise ValueError(f"expected exactly one {method_name}({signature_prefix}): {len(selected)}")
    ops = instructions(selected[0][1])
    if not ops or len(ops) > 160:
        raise ValueError(f"invalid instruction count in {method_name}")
    return ops


def steps(ops, expectations, label):
    """Strict forward-only reference order, with opcode and resolved marker."""
    last = -1
    locations = []
    for opcode, marker in expectations:
        matches = [pc for pc, op, tail in ops
                   if pc > last and op == opcode and marker in tail]
        if not matches:
            raise ValueError(f"{label}: missing ordered {opcode} {marker!r} after {last}")
        last = matches[0]
        locations.append(last)
    return locations


def inspect_consumers(dis: dict[str, str]) -> dict:
    if set(dis) != set(CLASSES):
        raise ValueError("incomplete exact class set")
    checks = {}

    checks["calculator_result"] = steps(method(dis["calculator"], "getResult", "float"),
        [("invokestatic", "Float.isNaN"),
         ("getfield", "Field set:"), ("getfield", "Field add:"),
         ("fadd", ""), ("getfield", "Field multiply:"),
         ("fmul", ""), ("freturn", "")], "calculator_result")

    checks["adder_attach"] = steps(method(dis["adder"], "attach"),
        [("getfield", "ResultCalculator.add:"), ("fadd", ""),
         ("putfield", "ResultCalculator.add:")], "adder")
    checks["multiplier_attach"] = steps(method(dis["multiplier"], "attach"),
        [("getfield", "ResultCalculator.multiply:"), ("fmul", ""),
         ("putfield", "ResultCalculator.multiply:")], "multiplier")
    setter = method(dis["setter"], "attach")
    checks["setter_attach"] = steps(setter,
        [("invokestatic", "Float.isNaN"), ("invokestatic", "Math.min"),
         ("putfield", "ResultCalculator.set:")], "setter")
    if len([1 for _, op, tail in setter if op == "putfield" and "ResultCalculator.set:" in tail]) != 2:
        raise ValueError("setter: exact two write paths absent")

    checks["max_strikes"] = steps(method(dis["attack"], "getMaxStrikes"),
        [("getstatic", "MAX_STRIKES_MODIFIER:"), ("invokevirtual", "getProperty:"),
         ("invokevirtual", "Optional.map:"),
         ("invokevirtual", "LivingEntityPatch.getMaxStrikes:")],
        "max_strikes")

    checks["phase_damage_source"] = steps(method(dis["attack"], "getEpicFightDamageSource",
                                       "net.minecraft.world.damagesource.DamageSource"),
        [("getstatic", "DAMAGE_MODIFIER:"), ("invokevirtual", "getProperty:"),
         ("invokevirtual", "Optional.ifPresent:"),
         ("getstatic", "ARMOR_NEGATION_MODIFIER:"), ("invokevirtual", "getProperty:"),
         ("invokevirtual", "Optional.ifPresent:"),
         ("getstatic", "STUN_TYPE:"), ("invokevirtual", "getProperty:"),
         ("invokevirtual", "Optional.ifPresent:"),
         ("getstatic", "SOURCE_TAG:"), ("invokevirtual", "getProperty:"),
         ("invokevirtual", "Optional.ifPresent:")],
        "phase_damage_source")

    checks["attach_damage"] = steps(method(dis["source"], "attachDamageModifier"),
        [("getfield", "modifiedDamageCalculator:"), ("invokevirtual", "ResultCalculator.attach:")],
        "attach_damage")
    checks["attach_armor_negation"] = steps(method(dis["source"], "attachArmorNegationModifier"),
        [("getfield", "modifiedArmorNegationCalculator:"),
         ("invokevirtual", "ResultCalculator.attach:")], "attach_armor_negation")
    checks["calculate_damage"] = steps(method(dis["source"], "calculateDamageAgainst"),
        [("getfield", "modifiedDamageCalculator:"),
         ("invokevirtual", "ResultCalculator.getResult:"),
         ("getfield", "extraDamages:")], "calculate_damage")
    checks["calculate_armor_negation"] = steps(method(dis["source"], "calculateArmorNegation"),
        [("getfield", "modifiedArmorNegationCalculator:"),
         ("getfield", "baseArmorNegation:"),
         ("invokevirtual", "ResultCalculator.getResult:")], "calculate_armor_negation")

    armor = method(dis["armor_mixin"], "epicfight$getDamageAfterArmorAbsorb")
    checks["armor_absorption_hook"] = steps(armor,
        [("instanceof", "EpicFightDamageSource"),
         ("getstatic", "DamageTypeTags.BYPASSES_ARMOR:"),
         ("invokevirtual", "EpicFightDamageSource.calculateArmorNegation:"),
         ("ldc", "float 0.01f"),
         ("fmul", ""), ("fconst_1", ""),
         ("invokestatic", "Math.min:"), ("fmul", ""),
         ("invokestatic", "CombatRules.getDamageAfterAbsorb:"),
         ("fadd", ""), ("invokevirtual", "CallbackInfoReturnable.setReturnValue:"),
         ("invokevirtual", "CallbackInfoReturnable.cancel:")],
        "armor_absorption_hook")
    if not any(op == "ifne" for _, op, _ in armor):
        raise ValueError("mixin: missing bypass-armor guard jump")
    return {
        "status": "PASS_BOUNDED_EPICFIGHT_ATTACK_PHASE_CONSUMERS",
        "scope": "PUBLISHER_COMPILED_CONSUMER_METHOD_OPCODE_REFERENCES",
        "checks": {k: {"ordered_opcode_offsets": v} for k, v in checks.items()},
        "interpretation": [
            "ResultCalculator getResult applies (set if finite else base + adder) times multiplier, in that order.",
            "Adder, Multiplier and Setter attach into independent ResultCalculator accumulator fields; Setter has a Math.min merge path.",
            "AttackAnimation looks up phase properties; EpicFightDamageSource stores and computes bounded modifiers.",
            "MixinLivingEntity armor reduction branch uses 0.01f, Math.min(.,1), CombatRules.getDamageAfterAbsorb and sums the remaining armorable damage.",
        ],
        "limitations": [
            "No assertion that the mixin was applied to the Minecraft target class in a loaded game.",
            "Only bounded opcode/reference ordering; not a general control-flow or JVM dataflow proof.",
            "No active player, hit, target, cooldown, projectile AOE or realized post-mitigation HP damage measured.",
            "AttackAnimation Optional.ifPresent method handles not proven to dispatch each exact callback in this check.",
            "Provider effects and RPG progression remain provider-owned; no adapter authorized.",
        ],
    }


class Tests(unittest.TestCase):
    def test_order_control(self):
        self.assertEqual(steps([(0, "getstatic", "Field DAMAGE_MODIFIER:"),
                               (3, "invokevirtual", "Method getProperty:"),
                               (6, "invokevirtual", "Optional.ifPresent:")],
                              [("getstatic", "DAMAGE_MODIFIER:"),
                               ("invokevirtual", "getProperty:"),
                               ("invokevirtual", "ifPresent:")], "control"), [0, 3, 6])

    def test_drift_key_fails(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            steps([(0, "getstatic", "Field OTHER:")],
                  [("getstatic", "DAMAGE_MODIFIER:")], "key")

    def test_drift_order_fails(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            steps([(0, "fmul", ""), (3, "fadd", "")],
                  [("fadd", ""), ("fmul", "")], "order")

    def test_wrong_opcode_fails(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            steps([(0, "fsub", "")], [("fadd", "")], "opcode")

    def test_missing_method_fails(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            method("public class X {}", "calculateArmorNegation")

    def test_duplicate_method_fails(self):
        body = ("public class X {\n  public void calculateArmorNegation();\n"
                "    descriptor: ()V\n    Code:\n      0: return\n"
                "  public void calculateArmorNegation();\n"
                "    descriptor: ()V\n    Code:\n      1: return\n}")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            method(body, "calculateArmorNegation")

    def test_missing_class_fails(self):
        with self.assertRaisesRegex(ValueError, "class set"):
            inspect_consumers({})

    def test_wrong_local_path_after_absorb_fails(self):
        seq = [(0,"invokestatic","CombatRules.getDamageAfterAbsorb:"),
               (2,"fsub",""),(4,"invokevirtual","CallbackInfoReturnable.setReturnValue:")]
        with self.assertRaisesRegex(ValueError, "missing"):
            steps(seq,[("invokestatic","CombatRules.getDamageAfterAbsorb:"),
                       ("fadd",""),("invokevirtual","setReturnValue:")],"absorb")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--jar", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if args.self_test:
        r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if r.wasSuccessful() else 1
    if not args.jar or not args.output:
        p.error("--jar and --output required")
    try:
        # Authenticates publisher SHA1/SHA256, exact registry and original trident JSON.
        prior = inspect_publisher(args.jar)
        phase = evaluate_phase(javap(args.jar, "yesman.epicfight.registry.entries.EpicFightSkills"))
        result = inspect_consumers({k: javap(args.jar, c) for k, c in CLASSES.items()})
        result["publisher_sha1"] = prior["sha1"]
        result["publisher_sha256"] = prior["sha256"]
        result["prerequisites"] = [prior["status"], phase["status"]]
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        result = {"status": "FAIL_CLOSED", "deviations": [str(e)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "deviations": result.get("deviations", [])}))
    return 0 if result["status"] == "PASS_BOUNDED_EPICFIGHT_ATTACK_PHASE_CONSUMERS" else 2


if __name__ == "__main__":
    sys.exit(main())
