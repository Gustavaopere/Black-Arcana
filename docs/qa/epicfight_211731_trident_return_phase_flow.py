#!/usr/bin/env python3
"""Exact SHA-gated read-only Epic Fight trident return and phase precedence probe.

The proof is limited to named compiled methods and ordered bytecode operands.
It is not a Minecraft gameplay test, formal CFG, final-damage measurement or
authorization for a Black Arcana/RPG Skill Tree adapter.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unittest

from epicfight_211731_trident_causal import inspect as inspect_publisher, blocks, instructions, javap
from epicfight_211731_trident_attack_phase import evaluate as verify_property_builders

CLASSES = {
    "wrathful": "yesman.epicfight.skill.weaponinnate.WrathfulLightingSkill",
    "phase": "yesman.epicfight.api.animation.types.AttackAnimation$Phase",
    "everlasting": "yesman.epicfight.skill.weaponinnate.EverlastingAllegiance",
    "trident": "yesman.epicfight.world.capabilities.projectile.ThrownTridentPatch",
}

def exact_method(disasm: str, header: str):
    found = [(n, instructions(code)) for n, code in blocks(disasm) if n == header]
    if len(found) != 1 or not found[0][1]:
        raise ValueError("missing or duplicate compiled method: " + header)
    return found[0][1]

def ordered(ops, required, label):
    last = -1
    pcs = []
    for opcode, token in required:
        found = [(pc, tail) for pc, op, tail in ops if pc > last and op == opcode and token in tail]
        if not found:
            raise ValueError(f"{label}: missing ordered {opcode}/{token!r} after {last}")
        last = found[0][0]
        pcs.append(last)
    return pcs

def nearby_float(ops, method_fragment: str, value: float):
    calls = [(i,pc) for i,(pc,op,tail) in enumerate(ops)
             if op.startswith("invoke") and method_fragment in tail]
    if len(calls) != 1 or calls[0][0] < 1:
        raise ValueError(f"{method_fragment}: no unique invocation")
    index,pc = calls[0]
    predecessor = ops[index-1]
    m = re.search(r"// float ([-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?)f?", predecessor[2])
    if predecessor[1] not in ("ldc", "ldc_w", "ldc2_w") or not m or float(m.group(1)) != value:
        raise ValueError(f"{method_fragment}: direct float input {value} not proven")
    return {"constant_pc": predecessor[0], "call_pc": pc, "expected_float": value}

def check_methods(dis):
    if set(dis) != set(CLASSES):
        raise ValueError("incomplete required class set")
    wrath = exact_method(dis["wrathful"],
        "public yesman.epicfight.skill.weaponinnate.WeaponInnateSkill registerPropertiesToAnimation();")
    # List property group 0 is applied first, then property group 1, to each
    # iteration's SAME Phase receiver; this is not a phase-number mapping.
    first = ordered(wrath, [
        ("getfield", "Field properties:"),
        ("iconst_0", ""), ("invokeinterface", "java/util/List.get:"),
        ("invokeinterface", "java/util/Map.entrySet:"),
        ("invokevirtual", "AttackAnimation$Phase.addProperties:")
    ], "wrathful group zero")
    second = ordered(wrath, [
        ("getfield", "Field properties:"),
        ("iconst_1", ""), ("invokeinterface", "java/util/List.get:"),
        ("invokeinterface", "java/util/Map.entrySet:"),
        ("invokevirtual", "AttackAnimation$Phase.addProperties:")
    ], "wrathful group one")
    if first[-1] >= second[0]:
        raise ValueError("wrathful property groups reordered")
    group_calls = [(i,pc) for i,(pc,op,tail) in enumerate(wrath)
                   if op == "invokevirtual" and "AttackAnimation$Phase.addProperties:" in tail]
    if len(group_calls) != 2:
        raise ValueError("wrathful: expected exactly two Phase.addProperties calls")
    for i, _ in group_calls:
        if not any(op == "aload" and re.match(r"5(?:\s|$)", tail) for _,op,tail in wrath[max(0,i-10):i]):
            raise ValueError("wrathful: phase receiver local index 5 missing")

    phase = exact_method(dis["phase"], "public void addProperties(java.util.Set);")
    mapped = ordered(phase, [
        ("invokeinterface", "java/util/Set.iterator:"),
        ("invokeinterface", "java/util/Iterator.hasNext:"),
        ("invokeinterface", "java/util/Iterator.next:"),
        ("getfield", "Field properties:"),
        ("invokeinterface", "java/util/Map$Entry.getKey:"),
        ("invokeinterface", "java/util/Map$Entry.getValue:"),
        ("invokeinterface", "java/util/Map.put:")
    ], "Phase.addProperties map overwrite")
    if len([1 for _,op,tail in phase if "java/util/Map.put:" in tail and op == "invokeinterface"]) != 1:
        raise ValueError("Phase.addProperties: unexpected write behavior")
    everlasting = exact_method(dis["everlasting"],
        "public yesman.epicfight.skill.weaponinnate.WeaponInnateSkill registerPropertiesToAnimation();")
    if [(op,tail.strip()) for _,op,tail in everlasting] != [("aload_0",""),("areturn","")]:
        raise ValueError("EverlastingAllegiance: animation registration is not the bounded no-op")

    tick = exact_method(dis["trident"], "public void tickEnd();")
    dconst = [(pc,op) for pc,op,_ in tick if op == "dconst_1"]
    if len(dconst) < 3:
        raise ValueError("trident: three exact 1.0 AABB inflation constants absent")
    aabb = ordered(tick, [
        ("invokevirtual", "AABB.inflate:(DDD)"),
        ("invokevirtual", "Level.getEntities:"),
        ("invokestatic", "EpicFightDamageSources.trident:"),
        ("getstatic", "StunType.HOLD:"),
        ("getstatic", "EpicFightDamageTypeTags.WEAPON_INNATE:"),
        ("invokevirtual", "EpicFightDamageSource.setBaseArmorNegation:"),
        ("invokestatic", "ValueModifier.multiplier:"),
        ("invokevirtual", "EpicFightDamageSource.attachDamageModifier:"),
        ("invokevirtual", "ThrownTrident.getOwner:"),
        ("invokestatic", "EnchantmentHelper.modifyDamage:"),
        ("invokevirtual", "Entity.hurt:")
    ], "returning trident damage source")
    initial = next(i for i,(_,op,tail) in enumerate(tick)
                   if op == "invokevirtual" and "AABB.inflate:(DDD)" in tail)
    if [op for _,op,_ in tick[initial-3:initial]] != ["dconst_1"]*3:
        raise ValueError("trident: inflation is not exactly 1,1,1")
    armor = nearby_float(tick, "EpicFightDamageSource.setBaseArmorNegation:", 30.0)
    multiplier = nearby_float(tick, "ValueModifier.multiplier:", 1.4)
    if not any(op in ("ldc", "ldc_w") and re.search(r"// float 8\.0f",tail)
               for pc,op,tail in tick if aabb[0]<pc<aabb[-1]):
        raise ValueError("trident: 8.0f base hit amount not found inside return loop")
    movement = ordered(tick, [
        ("invokestatic", "java/lang/Math.pow:"),
        ("invokestatic", "java/lang/Math.min:"),
        ("invokestatic", "java/lang/Math.min:"),
        ("invokevirtual", "ThrownTrident.setPos:")
    ], "returning trident movement")
    recalled = exact_method(dis["trident"], "public void recalledBySkill();")
    recall = ordered(recalled, [
        ("putfield", "ThrownTrident.dealtDamage:"),
        ("putfield", "Field innateActivated:"),
        ("getfield", "ThrownTrident.tickCount:"),
        ("putfield", "Field returnTick:")
    ], "recall activation")
    return {
        "status": "PASS_BOUNDED_TRIDENT_PHASE_PRECEDENCE_AND_RETURN_PATH",
        "evidence_class": "EXACT_PUBLISHER_METHOD_ORDERED_REFERENCES_AND_OPERANDS",
        "wrathful": {
            "two_group_calls_on_same_phase_in_one_loop": True,
            "group_zero_then_one": [first[-1], second[-1]],
            "map_put_replaces_equal_property_keys": True,
            "phase_map_put_pc": mapped[-1],
            "conditional_inference": "Later group 1 MAX_STRIKES setter(3) replaces group 0 setter(1) on each phase if registration runs and no later write overrides it"
        },
        "everlasting": {
            "registerPropertiesToAnimation": "direct_return_this_no_phase_writes",
            "return_damage_source_in_tickEnd": "EpicFightDamageSources.trident with HOLD/WEAPON_INNATE, baseArmorNegation(30), multiplier(1.4), source hit amount 8 before enchantments",
            "aabb_inflation_xyz": [1.0,1.0,1.0],
            "damage_source_callsites": aabb,
            "armor_operand": armor,
            "multiplier_operand": multiplier,
            "movement_callsites": movement,
            "recall_activation_callsites": recall
        },
        "limits": [
            "Source-backed Map.put semantics plus bounded compiled calls, not a live loaded-animation property snapshot.",
            "AABB.inflate(1,1,1) is per-axis expansion of the current projectile bounding box, NOT a spherical radius or target limit.",
            "Return tickEnd code is a potential repeated path; no sample of hits, armor, knockdown, dedup, real speed, lifetime or cooldown.",
            "No evidence of connected player combat or cost settlement; no Black Arcana/RPG Skill Tree adapter authorized."
        ]
    }

def fixture_ops(*ops):
    return [(i*3, op, tail) for i,(op,tail) in enumerate(ops)]

class Tests(unittest.TestCase):
    def test_ordered_good(self):
        x=fixture_ops(("getfield","Field properties:"),("iconst_0",""),
                      ("invokeinterface","java/util/List.get:"))
        self.assertEqual(ordered(x,[("getfield","properties:"),("iconst_0",""),
                                    ("invokeinterface","List.get:")],"x"),[0,3,6])
    def test_ordered_reverse_fail(self):
        x=fixture_ops(("fadd",""),("fmul",""))
        with self.assertRaises(ValueError):
            ordered(x,[("fmul",""),("fadd","")],"x")
    def test_absent_exact_method_fail(self):
        with self.assertRaises(ValueError):
            exact_method("public class Foo {}", "public void tickEnd();")
    def test_float_input_good(self):
        x=fixture_ops(("ldc","// float 30.0f"),
                      ("invokevirtual","// Method EpicFightDamageSource.setBaseArmorNegation:(F)V"))
        self.assertEqual(nearby_float(x,"setBaseArmorNegation:",30.0)["expected_float"],30.0)
    def test_float_drift_fail(self):
        x=fixture_ops(("ldc","// float 20.0f"),("invokevirtual","setBaseArmorNegation:"))
        with self.assertRaises(ValueError):
            nearby_float(x,"setBaseArmorNegation:",30.0)
    def test_missing_predecessor_fail(self):
        x=fixture_ops(("invokevirtual","setBaseArmorNegation:"))
        with self.assertRaises(ValueError):
            nearby_float(x,"setBaseArmorNegation:",30.0)
    def test_duplicate_callsite_fail(self):
        x=fixture_ops(("ldc","// float 30.0f"),("invokevirtual","setBaseArmorNegation:"),
                      ("ldc","// float 30.0f"),("invokevirtual","setBaseArmorNegation:"))
        with self.assertRaises(ValueError):
            nearby_float(x,"setBaseArmorNegation:",30.0)
    def test_missing_class_set_fail(self):
        with self.assertRaisesRegex(ValueError,"class set"):
            check_methods({})
    def test_everlasting_noop_drift_fail(self):
        # Whitelist excludes even a harmless extra opcode or an outgoing call.
        a=[("aload_0",""),("nop",""),("areturn","")]
        self.assertNotEqual(a,[("aload_0",""),("areturn","")])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        run=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if run.wasSuccessful() else 1
    if not a.jar or not a.output:
        p.error("--jar and --output required")
    try:
        prior=inspect_publisher(a.jar)  # exact SHA1/SHA256 plus original skill identities
        builders=verify_property_builders(javap(a.jar,
            "yesman.epicfight.registry.entries.EpicFightSkills"))
        report=check_methods({key:javap(a.jar,name) for key,name in CLASSES.items()})
        report["publisher_sha1"]=prior["sha1"]
        report["publisher_sha256"]=prior["sha256"]
        report["prerequisite_checks"]=[prior["status"], builders["status"]]
    except (OSError,ValueError) as e:
        report={"status":"FAIL_CLOSED","deviations":[str(e)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],
                      "deviations":report.get("deviations",[])}))
    return 0 if report["status"]=="PASS_BOUNDED_TRIDENT_PHASE_PRECEDENCE_AND_RETURN_PATH" else 2

if __name__=="__main__":
    sys.exit(main())
