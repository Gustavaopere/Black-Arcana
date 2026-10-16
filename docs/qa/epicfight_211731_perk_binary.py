#!/usr/bin/env python3
"""Fail-closed static evidence for publisher Epic Fight 21.17.3.1; no mod runtime."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import unittest
import zipfile

EXPECTED_SHA1 = "fb199b7bbea2fc402da28ab586e73f47e32f8fc0"
EXPECTED_SHA256 = "8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526"
PARAMETER_PREFIX = "data/epicfight/skill_parameters/"
EXPECTED_FIELDS = {
    "parrying": {"penalizer": 0.6, "parry_window": 8},
    "impact_guard": {"penalizer": 0.6, "superior_penalizer": 0.2, "damage_reducer": 0.2},
    "swordmaster": {"speed_bonus": 30},
    "forbidden_strength": {},
    "roll": {"consumption": 4.0},
    "step": {"consumption": 3.0},
    "wrathful_lighting": {"consumption": 50.0},
    "tsunami": {"consumption": 50.0},
    "everlasting_allegiance": {"consumption": 40.0},
}
EXPECTED_ATTRIBUTE_MODIFIERS = {
    "swordmaster": {
        "epicfight:stamina_regen": ("add_value", 0.2),
        "epicfight:stamina": ("add_value", 2.0),
    },
    "forbidden_strength": {
        "minecraft:generic.attack_damage": ("add_multiplied_total", 0.05),
        "minecraft:generic.max_health": ("add_value", 4.0),
    },
}
# These are *symbol-presence* checks in compiled classfiles, not behavioral/ABI proof.
CLASS_SYMBOLS = {
    "yesman.epicfight.skill.guard.ParryingSkill":
        ("parryWindow", "loadDatapackParameters(", "guard("),
    "yesman.epicfight.skill.guard.ImpactGuardSkill":
        ("damageReducer", "dealEvent(", "isAdvancedBlockableDamageSource("),
    "yesman.epicfight.skill.passive.SwordmasterSkill":
        ("speedBonus", "onInitiate(", "MODIFY_ATTACK_SPEED"),
    "yesman.epicfight.skill.passive.ForbiddenStrengthSkill":
        ("onInitiate(", "CONSUME_SKILL", "STAMINA", "HEALTH"),
    "yesman.epicfight.skill.dodge.DodgeSkill":
        ("gatherArguments(", "executeOnServer(", "isExecutableState("),
    "yesman.epicfight.skill.weaponinnate.WrathfulLightingSkill":
        ("registerPropertiesToAnimation(",),
    "yesman.epicfight.skill.weaponinnate.EverlastingAllegiance":
        ("checkExecuteCondition(", "executeOnServer(", "recalledBySkill"),
    "yesman.epicfight.registry.entries.EpicFightMovesets":
        ("TSUNAMI", "WRATHFUL_LIGHTING", "EVERLASTING_ALLEGIANCE"),
    "yesman.epicfight.registry.entries.EpicFightSkills":
        ("wrathful_lighting", "tsunami", "everlasting_allegiance"),
    "yesman.epicfight.api.event.EpicFightEventHooks$Entity":
        ("MODIFY_ATTACK_SPEED", "TAKE_DAMAGE_INCOME"),
    "yesman.epicfight.api.event.EpicFightEventHooks$Player":
        ("CONSUME_SKILL",),
    "yesman.epicfight.skill.SkillContainer":
        ("requestCasting(", "CONSUME_SKILL"),
}


def compare_parameters(documents: dict[str, object]) -> tuple[list[dict], list[str]]:
    """Return inspected JSON facts and discrepancies; absent or changed data is never assumed."""
    evidence = []
    failures = []
    for skill, expected in EXPECTED_FIELDS.items():
        data = documents.get(skill)
        if not isinstance(data, dict):
            failures.append(f"{skill}: missing or non-object JSON")
            continue
        checked = {}
        for key, want in expected.items():
            got = data.get(key)
            checked[key] = got
            if isinstance(got, bool) or not isinstance(got, (int, float)) or got != want:
                failures.append(f"{skill}.{key}: expected {want!r}, got {got!r}")
        for attr, (want_operation, want_amount) in EXPECTED_ATTRIBUTE_MODIFIERS.get(skill, {}).items():
            modifiers = data.get("attribute_modifiers")
            if not isinstance(modifiers, list):
                failures.append(f"{skill}: missing attribute_modifiers")
                continue
            matches = [m for m in modifiers if isinstance(m, dict) and m.get("attribute") == attr]
            if len(matches) != 1:
                failures.append(f"{skill}: expected exactly one modifier for {attr}, got {len(matches)}")
                continue
            m = matches[0]
            checked["modifier:" + attr] = {"operation": m.get("operation"), "amount": m.get("amount")}
            if m.get("operation") != want_operation or isinstance(m.get("amount"), bool) or m.get("amount") != want_amount:
                failures.append(f"{skill}: modifier {attr} differs: {m!r}")
        evidence.append({"id": "epicfight:" + skill, "source_adjacent_expected": expected,
                         "publisher_values": checked, "resource_path": PARAMETER_PREFIX + skill + ".json"})
    return evidence, failures


def read_jar_parameters(jar: pathlib.Path) -> tuple[dict[str, object], list[str]]:
    documents: dict[str, object] = {}
    failures = []
    with zipfile.ZipFile(jar) as z:
        entries = set(z.namelist())
        for skill in EXPECTED_FIELDS:
            name = PARAMETER_PREFIX + skill + ".json"
            if name not in entries:
                failures.append(f"missing resource: {name}")
                continue
            try:
                documents[skill] = json.loads(z.read(name).decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as e:
                failures.append(f"invalid JSON: {name}: {type(e).__name__}")
        for cls in CLASS_SYMBOLS:
            path = cls.replace(".", "/") + ".class"
            if path not in entries:
                failures.append(f"missing class: {path}")
    return documents, failures


def inspect_symbols(jar: pathlib.Path) -> tuple[list[dict], list[str]]:
    details = []
    failures = []
    for cls, names in CLASS_SYMBOLS.items():
        try:
            proc = subprocess.run(
                ["javap", "-classpath", str(jar), "-p", "-c", "-constants", cls],
                capture_output=True, text=True, timeout=90, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as e:
            failures.append(f"javap failed for {cls}: {type(e).__name__}")
            continue
        if proc.returncode:
            failures.append(f"javap exit {proc.returncode} for {cls}: {proc.stderr[:180]}")
            continue
        symbols = {symbol: symbol in proc.stdout for symbol in names}
        details.append({"class": cls, "symbols": symbols})
        for symbol, present in symbols.items():
            if not present:
                failures.append(f"{cls}: missing compiled symbol {symbol!r}")
    return details, failures


def audit(jar: pathlib.Path) -> dict:
    raw = jar.read_bytes()
    sha1 = hashlib.sha1(raw).hexdigest()
    sha256 = hashlib.sha256(raw).hexdigest()
    if sha1 != EXPECTED_SHA1 or sha256 != EXPECTED_SHA256:
        raise ValueError(f"publisher/physical fingerprint mismatch: sha1={sha1}, sha256={sha256}")
    docs, failures = read_jar_parameters(jar)
    params, drift = compare_parameters(docs)
    failures += drift
    classes, absent = inspect_symbols(jar)
    failures += absent
    return {
        "scope": "STATIC_BINARY_ONLY_NOT_GAMEPLAY_OR_PROVIDER_LOADED",
        "provider": "epicfight",
        "physical_version": "21.17.3.1",
        "publisher": "CurseForge 405076 / 8175609",
        "sha1": sha1, "sha256": sha256, "bytes": len(raw),
        "source_adjacent_pin": "Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf",
        "exact_json_parameter_files_inspected": len(params),
        "exact_classfiles_symbol_checked": len(classes),
        "parameter_evidence": params,
        "symbol_evidence": classes,
        "deviations": failures,
        "result": "PASS_STATIC_LIMITED" if not failures else "FAIL_CLOSED",
        "limits": [
            "Matching symbol strings does not prove instruction equivalence or hook ordering.",
            "Matching packaged JSON does not prove actual world datapack/config values.",
            "No runtime loading, skill activation, damage, stamina consumption, Mastery, or optional adapter tested.",
            "No external JAR or proprietary class contents are redistributed.",
        ],
    }


class ContractSelfTest(unittest.TestCase):
    def sample(self):
        docs = {k: dict(v) for k, v in EXPECTED_FIELDS.items()}
        for skill, mods in EXPECTED_ATTRIBUTE_MODIFIERS.items():
            docs[skill]["attribute_modifiers"] = [
                {"attribute": attr, "operation": op, "amount": amount}
                for attr, (op, amount) in mods.items()
            ]
        return docs

    def test_synthetic_expected_values(self):
        actual, errors = compare_parameters(self.sample())
        self.assertEqual(len(actual), 9)
        self.assertEqual(errors, [])

    def test_missing_skill_fails_closed(self):
        docs = self.sample()
        del docs["tsunami"]
        self.assertTrue(any("tsunami" in e for e in compare_parameters(docs)[1]))

    def test_parameter_drift_fails_closed(self):
        docs = self.sample()
        docs["parrying"]["parry_window"] = 9
        self.assertTrue(any("parry_window" in e for e in compare_parameters(docs)[1]))

    def test_modifier_drift_fails_closed(self):
        docs = self.sample()
        docs["swordmaster"]["attribute_modifiers"][0]["amount"] = 1.2
        self.assertTrue(any("stamina_regen" in e for e in compare_parameters(docs)[1]))

    def test_missing_modifier_fails_closed(self):
        docs = self.sample()
        docs["forbidden_strength"]["attribute_modifiers"] = []
        self.assertTrue(any("attack_damage" in e for e in compare_parameters(docs)[1]))

    def test_type_bool_cannot_equal_one(self):
        docs = self.sample()
        docs["parrying"]["parry_window"] = True
        self.assertTrue(any("parry_window" in e for e in compare_parameters(docs)[1]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractSelfTest)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if result.wasSuccessful() else 1
    if args.jar is None or args.output is None:
        parser.error("--jar and --output are required except for --self-test")
    try:
        result = audit(args.jar)
    except (OSError, zipfile.BadZipFile, ValueError) as e:
        result = {"result": "FAIL_CLOSED", "deviations": [f"{type(e).__name__}: {e}"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], "parameters": result.get("exact_json_parameter_files_inspected"),
                      "classfiles": result.get("exact_classfiles_symbol_checked"),
                      "deviations": result["deviations"]}, indent=2, ensure_ascii=False))
    return 0 if result["result"] == "PASS_STATIC_LIMITED" else 1


if __name__ == "__main__":
    sys.exit(main())
