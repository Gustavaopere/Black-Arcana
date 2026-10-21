#!/usr/bin/env python3
"""Fail-closed Epic Fight 21.17.3.1 trident-innate causal-boundary probe.

Read-only inspection of the exact SHA-1 + SHA-256 publisher JAR. Proves three
packaged JSON cost declarations plus bounded compiled control/call signatures.
Does not infer the cost unit, attack-phase attributes, damage, runtime success,
actual skill selection or permission to inject a Black Arcana perk adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import zipfile

EXPECTED_SHA1 = "fb199b7bbea2fc402da28ab586e73f47e32f8fc0"
EXPECTED_SHA256 = "8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526"
PARAM_PREFIX = "data/epicfight/skill_parameters/"
CONSUMPTION = {"wrathful_lighting": 50.0, "tsunami": 50.0, "everlasting_allegiance": 40.0}
CLASSES = {
    "selector": "yesman.epicfight.registry.entries.EpicFightMovesets",
    "skill_registry": "yesman.epicfight.registry.entries.EpicFightSkills",
    "wrathful": "yesman.epicfight.skill.weaponinnate.WrathfulLightingSkill",
    "conditional": "yesman.epicfight.skill.weaponinnate.ConditionalWeaponInnateSkill",
    "recall": "yesman.epicfight.skill.weaponinnate.EverlastingAllegiance",
}
METHOD = re.compile(r"^  (?:public|protected|private|static)\b.*\([^)]*\)(?: throws .+)?;$")
INSN = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")


def blocks(disassembly: str):
    lines = disassembly.splitlines()
    result = []
    for i, line in enumerate(lines):
        if not METHOD.match(line):
            continue
        end = next((j for j in range(i + 1, len(lines))
                    if METHOD.match(lines[j]) or lines[j] == "}"), len(lines))
        body = "\n".join(lines[i:end])
        if "Code:" in body:
            result.append((line.strip(), body))
    return result


def instructions(body: str):
    found = []
    for line in body.splitlines():
        if m := INSN.match(line):
            found.append((int(m.group(1)), m.group(2), m.group(3)))
    return found


def choose(items, required: tuple[str, ...], label: str):
    matching = [(name, code) for name, code in items if all(term in code for term in required)]
    if len(matching) != 1:
        raise ValueError(f"{label}: expected one method with {required}, got {len(matching)}")
    name, code = matching[0]
    ops = instructions(code)
    if not ops:
        raise ValueError(f"{label}: empty compiled body")
    return {"declaration": name, "code": code, "ops": ops}


def ordered_markers(method, markers: tuple[str, ...], label: str):
    ops = method["ops"]
    offsets = []
    last = -1
    for marker in markers:
        found = [(pc, op) for pc, op, comment in ops if pc > last and marker in comment]
        if not found:
            raise ValueError(f"{label}: no forward compiled marker {marker}")
        pc, _ = found[0]
        offsets.append(pc)
        last = pc
    return offsets


def study(dis: dict[str, str], jsons: dict[str, dict]):
    if set(dis) != set(CLASSES):
        raise ValueError("required class set missing or extra")
    if set(jsons) != set(CONSUMPTION):
        raise ValueError("missing or extra trident skill JSON")
    for skill, expected in CONSUMPTION.items():
        obj = jsons[skill]
        if not isinstance(obj, dict) or type(obj.get("consumption")) not in (float, int):
            raise ValueError(f"{skill}: missing or invalid consumption")
        if float(obj["consumption"]) != expected:
            raise ValueError(f"{skill}: publisher consumption drift")
    methods = {key: blocks(value) for key, value in dis.items()}
    selector = choose(methods["selector"],
        ("RIPTIDE", "CHANNELING", "LOYALTY", "TSUNAMI", "WRATHFUL_LIGHTING",
         "EVERLASTING_ALLEGIANCE", "GRASPING_SPIRE"), "trident_moveset_selector")
    offsets = ordered_markers(selector, ("RIPTIDE", "TSUNAMI", "CHANNELING",
        "WRATHFUL_LIGHTING", "LOYALTY", "EVERLASTING_ALLEGIANCE", "GRASPING_SPIRE"),
        "trident_moveset_selector")

    condition = choose(methods["skill_registry"], ("isInWaterOrRain",),
                       "tsunami_water_rain_condition")
    if "iconst_1" not in condition["code"] or "iconst_0" not in condition["code"]:
        raise ValueError("Tsunami water/rain selector does not expose both binary outcomes")
    reg = choose(methods["skill_registry"], ("TSUNAMI_REINFORCED", "TSUNAMI"),
                 "tsunami_animation_registration")
    if "setAnimations" not in reg["code"]:
        raise ValueError("Tsunami missing animation selection registration")

    wrathful = choose(methods["wrathful"], ("addProperties",),
                      "wrathful_phase_property_registration")
    adds = [(pc, op) for pc, op, comment in wrathful["ops"]
            if op.startswith("invoke") and "addProperties" in comment]
    if len(adds) != 2:
        raise ValueError(f"Wrathful Lightning expected two property sets per phase, observed {len(adds)}")
    conditional = choose(methods["conditional"],
                         ("getAnimationInCondition", "playAnimationSynchronized"),
                         "conditional_animation_selection")
    ordered_markers(conditional, ("getAnimationInCondition", "playAnimationSynchronized"),
                    "conditional_animation_selection")

    # Isolate the named method: the trident ID key also occurs in other lifecycle methods.
    gates = [(name, code) for name, code in methods["recall"]
             if "checkExecuteCondition(" in name]
    recall_gate = choose(gates, ("THROWN_TRIDENT_ENTITY_ID",), "recall_gate")
    if not any(op == "iflt" or op == "ifge" for _, op, _ in recall_gate["ops"]):
        raise ValueError("Everlasting Allegiance gate lacks signed entity-ID boundary")
    recall = choose(methods["recall"],
        ("recalledBySkill", "playAnimationSynchronized", "cancelOnServer"),
        "recall_server_settlement")
    if "executeOnServer(" not in recall["declaration"]:
        raise ValueError("recall call chain not in executeOnServer")
    sequence = ordered_markers(recall,
        ("recalledBySkill", "playAnimationSynchronized", "cancelOnServer"),
        "recall_server_settlement")
    return {
        "status": "PASS_BOUNDED_TRIDENT_CAUSAL_REFERENCES",
        "evidence_class": "EXACT_PUBLISHER_JSON_AND_COMPILED_METHOD_SEAMS",
        "consumption_declared_no_unit_inferred": CONSUMPTION,
        "trident_selector_offsets": offsets,
        "tsunami": {"water_or_rain_predicate_present": True,
                    "two_outcomes": True,
                    "normal_and_reinforced_animation_refs": True},
        "wrathful": {"add_properties_invocations_in_method": len(adds)},
        "recall": {"trident_id_check_method_present": True,
                   "server_recall_animation_cancel_offsets": sequence},
        "limitations": [
            "The bytecode probe checks method boundaries, ordered references and selected markers; it is not a complete CFG or live activation.",
            "No value for range, hitbox, target cap, damage total, cooldown, projectile scale or cost unit is proven by these checks.",
            "AttackPhaseProperty values of source-adjacent 21.17.3 are NOT promoted to exact 21.17.3.1 compiled dataflow.",
            "Runtime selected skill, hit, thunder, water/rain variant, trident recall, charge debit and Mastery are not measured.",
            "No third-party code or JAR is copied to the Black Arcana source tree.",
        ],
    }


def javap(jar: Path, class_name: str):
    p = subprocess.run(["javap", "-p", "-c", "-s", "-classpath", str(jar), class_name],
                       text=True, capture_output=True, timeout=45, check=False)
    if p.returncode or "Code:" not in p.stdout:
        raise ValueError(f"javap failed for {class_name}: {p.stderr[:180]}")
    return p.stdout


def inspect(jar: Path):
    blob = jar.read_bytes()
    if hashlib.sha1(blob).hexdigest() != EXPECTED_SHA1:
        raise ValueError("publisher SHA1 differs")
    if hashlib.sha256(blob).hexdigest() != EXPECTED_SHA256:
        raise ValueError("publisher SHA256 differs")
    with zipfile.ZipFile(jar) as z:
        names = set(z.namelist())
        for class_name in CLASSES.values():
            target = class_name.replace(".", "/") + ".class"
            if target not in names:
                raise ValueError("classfile missing: " + target)
        js = {}
        for skill in CONSUMPTION:
            file = PARAM_PREFIX + skill + ".json"
            if file not in names:
                raise ValueError("skill config missing: " + file)
            js[skill] = json.loads(z.read(file))
    result = study({k: javap(jar, name) for k, name in CLASSES.items()}, js)
    result["sha1"] = hashlib.sha1(blob).hexdigest()
    result["sha256"] = hashlib.sha256(blob).hexdigest()
    result["jar_bytes"] = len(blob)
    return result


def sample_method(name, *markers):
    return ("public class Fixture {\n"
            "  private static void " + name + "();\n    descriptor: ()V\n    Code:\n" +
            "\n".join(f"      {i*4}: " + ("invokevirtual" if i%2 else "getstatic") +
                      f" #1 // Field {marker}" for i, marker in enumerate(markers)) + "\n}")


class Tests(unittest.TestCase):
    def test_blocks_only_code_methods(self):
        self.assertEqual(len(blocks(sample_method("demo", "RIPTIDE"))), 1)

    def test_absent_required_method_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "expected one"):
            choose(blocks(sample_method("one", "NOT_MATCH")), ("RIPTIDE",), "test")

    def test_duplicate_method_fail_closed(self):
        a = blocks(sample_method("one", "RIPTIDE"))
        with self.assertRaisesRegex(ValueError, "got 2"):
            choose(a + a, ("RIPTIDE",), "duplicate")

    def test_ordered_markers_positive(self):
        b = choose(blocks(sample_method("one", "RIPTIDE", "TSUNAMI")),
                   ("RIPTIDE",), "x")
        self.assertEqual(ordered_markers(b, ("RIPTIDE", "TSUNAMI"), "x"), [0, 4])

    def test_reversed_selector_fail_closed(self):
        b = choose(blocks(sample_method("one", "TSUNAMI", "RIPTIDE")),
                   ("RIPTIDE",), "x")
        with self.assertRaises(ValueError):
            ordered_markers(b, ("RIPTIDE", "TSUNAMI"), "x")

    def test_recall_missing_cancel_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "expected one"):
            choose(blocks(sample_method("executeOnServer", "recalledBySkill")),
                   ("recalledBySkill", "cancelOnServer"), "recall")

    def test_exact_json_cost_drift_fail_closed(self):
        js = {name: {"consumption": cost} for name, cost in CONSUMPTION.items()}
        js["tsunami"]["consumption"] = 500
        d = {name: "" for name in CLASSES}
        with self.assertRaisesRegex(ValueError, "consumption drift"):
            study(d, js)

    def test_invalid_json_bool_fail_closed(self):
        js = {name: {"consumption": cost} for name, cost in CONSUMPTION.items()}
        js["tsunami"]["consumption"] = True
        d = {name: "" for name in CLASSES}
        with self.assertRaisesRegex(ValueError, "invalid consumption"):
            study(d, js)

    def test_required_class_missing_fail_closed(self):
        js = {name: {"consumption": cost} for name, cost in CONSUMPTION.items()}
        with self.assertRaisesRegex(ValueError, "class set"):
            study({}, js)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--jar", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    if a.self_test:
        r = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if r.wasSuccessful() else 1
    if not a.jar or not a.output:
        p.error("--jar and --output required")
    try:
        result = inspect(a.jar)
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired,
            json.JSONDecodeError) as e:
        result = {"status": "FAIL_CLOSED", "deviations": [str(e)]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "deviations": result.get("deviations", [])}))
    return 0 if result["status"] == "PASS_BOUNDED_TRIDENT_CAUSAL_REFERENCES" else 2


if __name__ == "__main__":
    sys.exit(main())
