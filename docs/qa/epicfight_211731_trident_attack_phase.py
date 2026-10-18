#!/usr/bin/env python3
"""Bounded Epic Fight 21.17.3.1 compiled trident attack-phase property evidence.

Follows exact ordered property-key / float / ValueModifier factory / addProperty
callsite windows in three specific EpicFightSkills supplier lambdas. The
publisher artifact must match both fingerprints before any inspection.
This is NOT a JVM verifier, executed combat, effective damage or a perk hook.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unittest

from epicfight_211731_trident_causal import (
    EXPECTED_SHA1, EXPECTED_SHA256, blocks, instructions, inspect, javap,
)

REGISTRY = "yesman.epicfight.registry.entries.EpicFightSkills"
PROPERTY = re.compile(r"AttackPhaseProperty\.([A-Z_]+):")
VALUE_FACTORY = re.compile(r"ValueModifier\.(setter|adder|multiplier):")
STUN = re.compile(r"StunType\.([A-Z_]+):")
CONFIG = {
    "wrathful_lighting": {
        "lambda": "lambda$static$40(",
        "return_type": "WrathfulLightingSkill",
        "groups": 2,
        "properties": [
            ("MAX_STRIKES_MODIFIER", "setter", 1.0),
            ("DAMAGE_MODIFIER", "setter", 8.0),
            ("MAX_STRIKES_MODIFIER", "setter", 3.0),
            ("EXTRA_DAMAGE", None, None),
            ("ARMOR_NEGATION_MODIFIER", "adder", 100.0),
            ("STUN_TYPE", "KNOCKDOWN", None),
            ("SOURCE_TAG", "WEAPON_INNATE", None),
        ],
    },
    "tsunami": {
        "lambda": "lambda$static$42(",
        "return_type": "ConditionalWeaponInnateSkill",
        "groups": 1,
        "properties": [
            ("ARMOR_NEGATION_MODIFIER", "adder", 100.0),
            ("SOURCE_TAG", "WEAPON_INNATE", None),
            ("STUN_TYPE", "KNOCKDOWN", None),
        ],
    },
    "everlasting_allegiance": {
        "lambda": "lambda$static$43(",
        "return_type": "EverlastingAllegiance",
        "groups": 1,
        "properties": [
            ("ARMOR_NEGATION_MODIFIER", "adder", 30.0),
            ("DAMAGE_MODIFIER", "multiplier", 1.4),
            ("EXTRA_DAMAGE", None, None),
            ("SOURCE_TAG", "WEAPON_INNATE", None),
            ("STUN_TYPE", "HOLD", None),
        ],
    },
}


def literal(instruction):
    _, opcode, tail = instruction
    if opcode.startswith("fconst_"):
        return float(opcode.split("_")[-1])
    if opcode.startswith(("ldc",)) and (m := re.search(
            r"// float (-?\d+(?:\.\d+)?)f\b", tail)):
        return float(m.group(1))
    raise ValueError("expected single-precision float literal")


def exact_phase_property(method, kind):
    cfg = CONFIG[kind]
    selected = [code for name, code in blocks(method)
                if cfg["lambda"] in name and cfg["return_type"] in name]
    if len(selected) != 1:
        raise ValueError(f"{kind}: expected one exact supplier method, found {len(selected)}")
    ops = instructions(selected[0])
    if not ops or len(ops) > 170:
        raise ValueError(f"{kind}: missing or excessive opcode list")
    if any(op in ("goto", "tableswitch", "lookupswitch") or op.startswith("if")
           for _, op, _ in ops):
        raise ValueError(f"{kind}: unexpected branch in straight-line supplier")
    groups = sum("Builder.newProperty:" in tail and op.startswith("invoke")
                 for _, op, tail in ops)
    if groups != cfg["groups"]:
        raise ValueError(f"{kind}: property group count {groups} != {cfg['groups']}")
    if not any("Builder.build:" in tail and op.startswith("invoke")
               for _, op, tail in ops):
        raise ValueError(f"{kind}: missing builder build")
    if kind in ("wrathful_lighting", "tsunami") and not any(
            "Builder.setAnimations:" in t and op.startswith("invoke")
            for _, op, t in ops):
        raise ValueError(f"{kind}: no animation builder binding")

    property_positions = []
    for idx, (pc, op, tail) in enumerate(ops):
        if op == "getstatic" and (m := PROPERTY.search(tail)):
            property_positions.append((idx, m.group(1)))
    actual = [p for _, p in property_positions]
    wanted = [p for p, _, _ in cfg["properties"]]
    if actual != wanted:
        raise ValueError(f"{kind}: property sequence differs: {actual} != {wanted}")

    evidence = []
    for row, (prop, mode, numeric) in enumerate(cfg["properties"]):
        start = property_positions[row][0]
        end = property_positions[row+1][0] if row+1 < len(property_positions) else len(ops)
        span = ops[start:end]
        add = [i for i, (_, op, tail) in enumerate(span)
               if op.startswith("invoke") and "Builder.addProperty:" in tail]
        if len(add) != 1:
            raise ValueError(f"{kind}: {prop} requires one builder.addProperty call")
        if mode in {"setter", "adder", "multiplier"}:
            if len(span) < 4 or literal(span[1]) != numeric:
                raise ValueError(f"{kind}: {prop} float operand mismatch")
            if not (span[2][1] == "invokestatic" and
                    (m := VALUE_FACTORY.search(span[2][2])) and m.group(1) == mode):
                raise ValueError(f"{kind}: {prop} modifier factory mismatch")
            if add[0] != 3:
                raise ValueError(f"{kind}: {prop} operand not adjacent to addProperty")
        elif mode == "KNOCKDOWN" or mode == "HOLD":
            if len(span) < 3 or span[1][1] != "getstatic" or not (
                    (m := STUN.search(span[1][2])) and m.group(1) == mode):
                raise ValueError(f"{kind}: {prop} stun operand mismatch")
            if add[0] != 2:
                raise ValueError(f"{kind}: {prop} stun not directly bound")
        elif mode == "WEAPON_INNATE":
            if not any(op == "getstatic" and
                       "EpicFightDamageTypeTags.WEAPON_INNATE:" in tail
                       for _, op, tail in span[:add[0]]):
                raise ValueError(f"{kind}: {prop} tag missing before addProperty")
        elif prop == "EXTRA_DAMAGE":
            if add[0] == 0:
                raise ValueError(f"{kind}: no extra damage expression")
        else:
            raise ValueError(f"{kind}: unsupported expected property {prop}")
        evidence.append({"property": prop, "value_modifier": mode,
                         "numeric_operand": numeric, "key_pc": ops[start][0]})
    return evidence


def evaluate(compiled):
    evidence = {name: exact_phase_property(compiled, name) for name in CONFIG}
    return {
        "status": "PASS_BOUNDED_TRIDENT_ATTACK_PHASE_PROPERTIES",
        "evidence_class": "EXACT_PUBLISHER_COMPILED_SUPPLIER_PROPERTY_CALLSITES",
        "data": evidence,
        "limits": [
            "Property values are passed to the provider's builder; no runtime attacks or modifiers applied were tested.",
            "The three static supplier lambdas have return-type and numeric signatures; a separate registry/bootstrap linkage proof may be required.",
            "EXTRA_DAMAGE expressions and SOURCE_TAG set contents are not fully dataflow-verified.",
            "No evidence about actual target, hitbox, range, projectile size, skill resource debit, cooldown, damage or armor mitigation.",
        ],
    }


def synth(kind):
    cfg = CONFIG[kind]
    codes = []
    def append(opcode, comment=""):
        codes.append(f"      {len(codes)*4}: {opcode} #1 {comment}".rstrip())
    if kind in ("wrathful_lighting", "tsunami"):
        append("invokevirtual", "// Method Builder.setAnimations:()V")
    append("invokevirtual", "// Method Builder.newProperty:()V")
    for idx, (prop, mode, numeric) in enumerate(cfg["properties"]):
        if kind == "wrathful_lighting" and idx == 1:
            append("invokevirtual", "// Method Builder.newProperty:()V")
        append("getstatic", f"// Field AnimationProperty$AttackPhaseProperty.{prop}:LProperty;")
        if mode in ("setter", "adder", "multiplier"):
            if numeric == 1.0:
                append("fconst_1")
            else:
                append("ldc_w", f"// float {numeric}f")
            append("invokestatic", f"// InterfaceMethod ValueModifier.{mode}:(F)LValueModifier;")
        elif mode in ("KNOCKDOWN", "HOLD"):
            append("getstatic", f"// Field StunType.{mode}:LStunType;")
        elif mode == "WEAPON_INNATE":
            append("getstatic", "// Field EpicFightDamageTypeTags.WEAPON_INNATE:LTagKey;")
        else:
            append("getstatic", "// Field ExtraDamageInstance.SWEEPING_EDGE_ENCHANTMENT:LExtraDamage;")
        append("invokevirtual", "// Method Builder.addProperty:(LProperty;Ljava/lang/Object;)V")
    append("invokevirtual", "// Method Builder.build:()LSkill;")
    return "public class Fake {\n  private static yesman.epicfight.skill.weaponinnate." + cfg["return_type"] + " " + cfg["lambda"] + "net.minecraft.resources.ResourceLocation);\n    descriptor: ()V\n    Code:\n" + "\n".join(codes) + "\n}"


class Tests(unittest.TestCase):
    def test_three_positive_fixtures(self):
        for skill in CONFIG:
            with self.subTest(skill=skill):
                self.assertEqual(len(exact_phase_property(synth(skill), skill)),
                                 len(CONFIG[skill]["properties"]))

    def test_wrong_coefficient(self):
        with self.assertRaisesRegex(ValueError, "operand"):
            exact_phase_property(synth("wrathful_lighting").replace("float 8.0f", "float 9.0f"), "wrathful_lighting")

    def test_wrong_factory(self):
        with self.assertRaisesRegex(ValueError, "factory"):
            exact_phase_property(synth("everlasting_allegiance").replace("ValueModifier.multiplier", "ValueModifier.adder"),
                                 "everlasting_allegiance")

    def test_missing_property(self):
        with self.assertRaisesRegex(ValueError, "sequence"):
            exact_phase_property(synth("tsunami").replace("ARMOR_NEGATION_MODIFIER", "IMPACT_MODIFIER"), "tsunami")

    def test_wrong_stun(self):
        with self.assertRaisesRegex(ValueError, "stun"):
            exact_phase_property(synth("tsunami").replace("StunType.KNOCKDOWN", "StunType.HOLD"), "tsunami")

    def test_missing_tag(self):
        with self.assertRaisesRegex(ValueError, "tag"):
            exact_phase_property(synth("wrathful_lighting").replace("Tags.WEAPON_INNATE", "Tags.MELEE"), "wrathful_lighting")

    def test_missing_property_group(self):
        a = synth("wrathful_lighting").replace("Builder.newProperty", "Builder.otherProperty", 1)
        with self.assertRaisesRegex(ValueError, "group count"):
            exact_phase_property(a, "wrathful_lighting")

    def test_wrong_supplier(self):
        with self.assertRaisesRegex(ValueError, "supplier method"):
            exact_phase_property(synth("tsunami").replace("lambda$static$42", "lambda$static$41"), "tsunami")

    def test_fail_branch(self):
        a = synth("tsunami").replace("      0:", "      0: ifeq 9\n      1:")
        with self.assertRaisesRegex(ValueError, "branch"):
            exact_phase_property(a, "tsunami")

    def test_missing_builder_call(self):
        with self.assertRaisesRegex(ValueError, "build"):
            exact_phase_property(synth("tsunami").replace("Builder.build:", "Builder.missing:"), "tsunami")

    def test_missing_animation_binding(self):
        with self.assertRaisesRegex(ValueError, "animation"):
            exact_phase_property(synth("tsunami").replace("Builder.setAnimations:", "Builder.noAnimations:"), "tsunami")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--self-test", action="store_true")
    a.add_argument("--jar", type=Path)
    a.add_argument("--output", type=Path)
    opts = a.parse_args()
    if opts.self_test:
        r = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if r.wasSuccessful() else 1
    if not opts.jar or not opts.output:
        a.error("--jar and --output are required")
    try:
        # SHA checks, metadata, packaged configs and causal seams remain mandatory.
        previous = inspect(opts.jar)
        dis = javap(opts.jar, REGISTRY)
        result = evaluate(dis)
        result["prerequisite"] = previous["status"]
        result["sha1"] = previous["sha1"]
        result["sha256"] = previous["sha256"]
    except (OSError, ValueError) as e:
        result = {"status": "FAIL_CLOSED", "deviations": [str(e)]}
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": result["status"], "deviations": result.get("deviations", [])}))
    return 0 if result["status"] == "PASS_BOUNDED_TRIDENT_ATTACK_PHASE_PROPERTIES" else 2


if __name__ == "__main__":
    sys.exit(main())
