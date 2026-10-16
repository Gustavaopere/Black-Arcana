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
    # Registry sentinel epicfight:empty is excluded deliberately: it is an internal
    # Skill.EMPTY identity, not an independently configured JSON skill resource.
    "combo_attacks": {},
    "knockdown_wakeup": {"consumption": 6.0},
    "sweeping_edge": {"consumption": 24.0},
    "dancing_edge": {"consumption": 30.0},
    "the_guillotine": {"consumption": 24.0},
    "heartpiercer": {"consumption": 40.0},
    "steel_whirlwind": {"consumption": 60.0},
    "battojutsu": {"consumption": 30.0},
    "rushing_tempo": {"consumption": 25.0, "max_stacks": 3},
    "relentless_combo": {"consumption": 20.0},
    "sharp_stab": {"consumption": 30.0},
    "liechtenauer": {"consumption": 40.0, "max_duration": 240, "return_duration": 60},
    "eviscerate": {"consumption": 25.0, "damage_cap": 20.0},
    "blade_rush": {"consumption": 25.0, "max_stacks": 4},
    "battojutsu_passive": {"consumption": 5.0},
    "guard": {"penalizer": 0.6},
    "adaptive_skin": {"damage_resistance": 0.15, "max_resistance_stack": 3},
    "meteor_slam": {},
    "revelation": {"max_duration": 20, "block_stacks": 3, "parry_stacks": 6, "dodge_stacks": 8, "default_revelation_stacks": 20},
    "demolition_leap": {"consumption": 0.6},
    "phantom_ascent": {"extra_jumps": 1, "jump_power": 0.6},
    "grasping_spire": {"consumption": 40.0},
    "parrying": {"penalizer": 0.6, "parry_window": 8},
    "impact_guard": {"penalizer": 0.6, "superior_penalizer": 0.2, "damage_reducer": 0.2},
    "swordmaster": {"speed_bonus": 30},
    "forbidden_strength": {},
    "technician": {},
    "berserker": {"speed_bonus": 0.5, "damage_bonus": 0.3},
    "stamina_pillager": {"regen_rate": 30},
    "death_harvest": {},
    "endurance": {"consumption": 12.0, "max_duration": 160, "stamina_ratio": 0.3},
    "hypervitality": {"consumption": 6.0, "max_stacks": 1},
    "adrenaline_fiend": {},
    "catharsis": {"regen_bonus": 0.5},
    "emergency_escape": {"consumption": 5.0},
    "bonebreaker": {"damage_bonus": 0.1, "max_damage_bonus_stacks": 8},
    "vengeance": {"damage_bonus": 0.3, "max_duration": 200},
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
    "technician": {
        "epicfight:stamina_regen": ("add_value", 0.4),
    },
    "berserker": {
        "epicfight:stamina": ("add_value", 6.0),
    },
    "stamina_pillager": {
        "minecraft:generic.attack_damage": ("add_multiplied_total", 0.1),
        "epicfight:stamina": ("add_value", 3.0),
    },
    "death_harvest": {
        "minecraft:generic.attack_damage": ("add_multiplied_total", 0.15),
    },
    "endurance": {
        "minecraft:generic.max_health": ("add_value", 2.0),
        "epicfight:stamina": ("add_value", 4.0),
    },
    "hypervitality": {
        "epicfight:stamina": ("add_value", 2.0),
        "minecraft:generic.max_health": ("add_value", 4.0),
    },
    "emergency_escape": {
        "epicfight:stamina_regen": ("add_value", 0.3),
    },
}
# These are legacy-shaped records in some packaged JSONs. Their presence/values are
# evidence ONLY of serialized data, not proof that AttributeModifier.MAP_CODEC
# parses/applies the records (they lack a modern "id" key).
# tuple: (attribute, operation, amount, name, uuid) exact JSON fields.
EXPECTED_LEGACY_MODIFIERS = {
    "adaptive_skin": [
        ("minecraft:generic.max_health", "addition", 6.0, "adaptive_skin_skill_stat", "e9cd15f0-72cc-474b-bfee-66276d06157d"),
    ],
    "adrenaline_fiend": [
        ("minecraft:generic.attack_speed", "multiply_total", 0.1, "adrenaline_skill_stat", "678cff5d-dc70-492d-b960-f01241d1a0f9"),
        ("minecraft:generic.attack_damage", "multiply_total", 0.075, "adrenaline_skill_stat", "678cff5d-dc70-492d-b960-f01241d1a0f9"),
    ],
    "catharsis": [
        ("epicfight:stamina_regen", "addition", 0.15, "bloodlust_skill_stat", "0c6efd18-199e-48a6-aa1b-51a1c1f9f613"),
        ("minecraft:generic.attack_damage", "multiply_total", 0.1, "bloodlust_skill_stat", "0c6efd18-199e-48a6-aa1b-51a1c1f9f613"),
    ],
    "bonebreaker": [
        ("minecraft:generic.attack_speed", "multiply_total", 0.15, "bonebreaker_skill_stat", "06212e76-6dbe-4d4b-a875-562829bb6db4"),
    ],
    "vengeance": [
        ("minecraft:generic.max_health", "addition", 3.0, "vengeance_skill_stat", "bcb1f110-c987-412e-9e40-5831c62eba2e"),
        ("minecraft:generic.attack_damage", "multiply_total", 0.075, "vengeance_skill_stat", "bcb1f110-c987-412e-9e40-5831c62eba2e"),
    ],
}
# Entity-type limits are declarative packaged datapack values, not an active
# loaded registry or a promise every referenced addon entity is present.
EXPECTED_MAPS = {
    "revelation": {
        "minecraft:cave_spider": 10,
        "minecraft:drowned": 10,
        "minecraft:enderman": 30,
        "minecraft:husk": 10,
        "minecraft:iron_golem": 30,
        "minecraft:piglin": 10,
        "minecraft:piglin_brute": 20,
        "minecraft:zombified_piglin": 10,
        "minecraft:pillager": 10,
        "minecraft:player": 30,
        "minecraft:skeleton": 10,
        "minecraft:spider": 10,
        "minecraft:stray": 10,
        "minecraft:vindicator": 10,
        "minecraft:wither_skeleton": 20,
        "minecraft:zombie": 10,
        "minecraft:zombie_villager": 10,
        "epicfight:wither_skeleton_minion": 10,
    },
}
# These are *symbol-presence* checks in compiled classfiles, not behavioral/ABI proof.
CLASS_SYMBOLS = {
    "yesman.epicfight.skill.Skill":
        ("EMPTY", "loadDatapackParameters("),
    "yesman.epicfight.skill.common.ComboAttacks":
        ("MIN_SPRINT_TICKS_FOR_DASH", "executeOnServer(", "checkConsumption("),
    "yesman.epicfight.skill.dodge.KnockdownWakeupSkill":
        ("gatherArguments(", "isExecutableState("),
    "yesman.epicfight.skill.weaponinnate.SimpleWeaponInnateSkill":
        ("registerPropertiesToAnimation(", "executeOnServer("),
    "yesman.epicfight.skill.weaponinnate.GuillotineAxeSkill":
        ("DELIVER_DAMAGE_PRE", "setExecute"),
    "yesman.epicfight.skill.weaponinnate.SteelWhirlwindSkill":
        ("getAllowedMaxChargingTicks(", "onStopHolding("),
    "yesman.epicfight.skill.weaponinnate.BattojutsuSkill":
        ("playSkillAnimation(", "SHEATH"),
    "yesman.epicfight.skill.weaponinnate.RushingTempoSkill":
        ("comboAnimation", "checkExecuteCondition("),
    "yesman.epicfight.skill.weaponinnate.LiechtenauerSkill":
        ("returnDuration", "KILL_ENTITY", "TAKE_DAMAGE_INCOME"),
    "yesman.epicfight.skill.weaponinnate.EviscerateSkill":
        ("damageCap", "reserveAnimation", "getDamageCap("),
    "yesman.epicfight.skill.weaponinnate.BladeRushSkill":
        ("INSTABILITY", "DELIVER_DAMAGE_POST", "checkExecuteCondition("),
    "yesman.epicfight.skill.weapon_passive.BattojutsuPassive":
        ("SHEATH", "USE_ITEM", "getCooldownRegenPerSecond("),
    "yesman.epicfight.skill.passive.AdaptiveSkinSkill":
        ("damageResistance", "maxResistanceStack", "RESISTING_DAMAGE_TYPE", "TAKE_DAMAGE_PRE"),
    "yesman.epicfight.skill.identity.MeteorSlamSkill":
        ("minDistance", "CAST_SKILL", "FALL_DISTANCE", "PROTECT_NEXT_FALL"),
    "yesman.epicfight.skill.identity.RevelationSkill":
        ("maxRevelationStacks", "checkStackAndActivate(", "ON_DODGE", "TAKE_DAMAGE_INCOME"),
    "yesman.epicfight.skill.mover.DemolitionLeapSkill":
        ("holdTick(", "getAllowedMaxChargingTicks(", "PROTECT_NEXT_FALL"),
    "yesman.epicfight.skill.mover.PhantomAscentSkill":
        ("extraJumps", "jumpPower", "JUMP_COUNT", "TAKE_DAMAGE_INCOME"),
    "yesman.epicfight.skill.weaponinnate.GraspingSpireSkill":
        ("LAST_HIT_COUNT", "DELIVER_DAMAGE_POST", "registerPropertiesToAnimation("),
    "yesman.epicfight.skill.guard.GuardSkill":
        ("penalizer", "TAKE_DAMAGE_INCOME", "guard("),
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
    "yesman.epicfight.skill.passive.TechnicianSkill":
        ("onInitiate(", "ON_DODGE"),
    "yesman.epicfight.skill.passive.BerserkerSkill":
        ("speedBonus", "damageBonus", "MODIFY_ATTACK_SPEED", "MODIFY_ATTACK_DAMAGE"),
    "yesman.epicfight.skill.passive.StaminaPillagerSkill":
        ("regenRate", "KILL_ENTITY"),
    "yesman.epicfight.skill.passive.DeathHarvestSkill":
        ("onInitiate(", "WEAPON_INNATE", "DeathHarvestOrb"),
    "yesman.epicfight.skill.passive.EnduranceSkill":
        ("staminaRatio", "TAKE_DAMAGE_PRE", "setMaxStunShield"),
    "yesman.epicfight.skill.passive.HyperVitalitySkill":
        ("CONSUME_SKILL", "CANCEL_SKILL"),
    "yesman.epicfight.skill.passive.AdrenalineFiendSkill":
        ("KILL_ENTITY", "START_ACTION"),
    "yesman.epicfight.skill.passive.CatharsisSkill":
        ("regenBonus", "ON_DODGE"),
    "yesman.epicfight.skill.passive.EmergencyEscapeSkill":
        ("CAST_SKILL", "CONSUME_SKILL", "setStateExecutable"),
    "yesman.epicfight.skill.passive.BonebreakerSkill":
        ("DELIVER_DAMAGE_PRE", "MODIFY_ATTACK_DAMAGE", "maxDamageBonusStacks"),
    "yesman.epicfight.skill.passive.VengeanceSkill":
        ("TAKE_DAMAGE_PRE", "DELIVER_DAMAGE_PRE", "KILL_ENTITY"),
    "yesman.epicfight.world.entity.DeathHarvestOrb":
        ("tick(", "setConsumptionSynchronize"),
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
        legacy_expected = EXPECTED_LEGACY_MODIFIERS.get(skill, [])
        if legacy_expected:
            modifiers = data.get("attribute_modifiers")
            if not isinstance(modifiers, list) or len(modifiers) != len(legacy_expected):
                failures.append(f"{skill}: expected {len(legacy_expected)} legacy-shaped modifiers")
            else:
                exact = []
                for modifier in modifiers:
                    if not isinstance(modifier, dict):
                        failures.append(f"{skill}: non-object legacy modifier")
                        continue
                    if "id" in modifier:
                        failures.append(f"{skill}: legacy raw modifier unexpectedly contains modern id")
                    exact.append(tuple(modifier.get(k) for k in
                                       ("attribute", "operation", "amount", "name", "uuid")))
                if sorted(map(repr, exact)) != sorted(map(repr, legacy_expected)):
                    failures.append(f"{skill}: legacy raw modifier fields drift")
            checked["legacy_modifier_schema"] = "RAW_ONLY_NOT_PROVEN_LOADED"
            checked["legacy_modifiers_raw_count"] = len(modifiers) if isinstance(modifiers, list) else None
        if skill in EXPECTED_MAPS:
            actual_map = data.get("max_revelations")
            expected_map = EXPECTED_MAPS[skill]
            if not isinstance(actual_map, dict) or actual_map != expected_map:
                failures.append(f"{skill}: max_revelations entity-type limits drift")
            checked["entity_type_limit_entries"] = len(actual_map) if isinstance(actual_map, dict) else None
            checked["entity_type_limit_schema"] = "PACKAGED_RAW_NOT_LOADED_REGISTRY"
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
        "registered_core_skill_ids_classified": 43,
        "unconfigured_empty_sentinel": "epicfight:empty",
        "exact_classfiles_symbol_checked": len(classes),
        "legacy_modifier_skill_ids_raw_only": sorted(EXPECTED_LEGACY_MODIFIERS),
        "entity_limit_map_ids_raw_only": sorted(EXPECTED_MAPS),
        "parameter_evidence": params,
        "symbol_evidence": classes,
        "deviations": failures,
        "result": "PASS_STATIC_LIMITED" if not failures else "FAIL_CLOSED",
        "limits": [
            "Matching symbol strings does not prove instruction equivalence or hook ordering.",
            "Matching packaged JSON does not prove actual world datapack/config values.",
            "Legacy-shaped name/uuid attribute_modifiers are raw data only; loader compatibility unproven.",
            "Entity-type map keys are packaged raw only; registry and addon presence not verified.",
            "No runtime loading, skill activation, damage, stamina consumption, Mastery, or optional adapter tested.",
            "No external JAR or proprietary class contents are redistributed.",
            "EpicFightSkills EMPTY is an internal sentinel and not a 43rd skill_parameters JSON resource.",
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
        for skill, modifiers in EXPECTED_LEGACY_MODIFIERS.items():
            docs[skill]["attribute_modifiers"] = [
                dict(zip(("attribute", "operation", "amount", "name", "uuid"), modifier))
                for modifier in modifiers
            ]
        for skill, entity_map in EXPECTED_MAPS.items():
            docs[skill]["max_revelations"] = dict(entity_map)
        return docs

    def test_synthetic_expected_values(self):
        actual, errors = compare_parameters(self.sample())
        self.assertEqual(len(actual), 42)
        self.assertEqual(errors, [])

    def test_compiled_invocation_symbol_fragments(self):
        self.assertIn("setExecute", CLASS_SYMBOLS["yesman.epicfight.skill.weaponinnate.GuillotineAxeSkill"])
        self.assertIn("reserveAnimation", CLASS_SYMBOLS["yesman.epicfight.skill.weaponinnate.EviscerateSkill"])
        self.assertNotIn("setExecute(", CLASS_SYMBOLS["yesman.epicfight.skill.weaponinnate.GuillotineAxeSkill"])
        self.assertNotIn("reserveAnimation(", CLASS_SYMBOLS["yesman.epicfight.skill.weaponinnate.EviscerateSkill"])

    def test_empty_sentinel_is_not_a_missing_json_skill(self):
        self.assertNotIn("empty", EXPECTED_FIELDS)
        self.assertIn("yesman.epicfight.skill.Skill", CLASS_SYMBOLS)
        self.assertIn("EMPTY", CLASS_SYMBOLS["yesman.epicfight.skill.Skill"])

    def test_missing_combo_resource_fails_closed(self):
        docs = self.sample()
        del docs["combo_attacks"]
        self.assertTrue(any("combo_attacks" in e for e in compare_parameters(docs)[1]))

    def test_liechtenauer_return_duration_drift(self):
        docs = self.sample()
        docs["liechtenauer"]["return_duration"] = 59
        self.assertTrue(any("return_duration" in e for e in compare_parameters(docs)[1]))

    def test_blade_rush_stack_drift(self):
        docs = self.sample()
        docs["blade_rush"]["max_stacks"] = 3
        self.assertTrue(any("max_stacks" in e for e in compare_parameters(docs)[1]))

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

    def test_revelation_type_limits_drift_fails_closed(self):
        docs = self.sample()
        docs["revelation"]["max_revelations"]["minecraft:player"] = 999
        self.assertTrue(any("max_revelations" in x for x in compare_parameters(docs)[1]))

    def test_revelation_missing_limit_fails_closed(self):
        docs = self.sample()
        del docs["revelation"]["max_revelations"]["minecraft:player"]
        self.assertTrue(any("max_revelations" in x for x in compare_parameters(docs)[1]))

    def test_adaptive_legacy_attribute_not_promoted(self):
        docs = self.sample()
        entries, failures = compare_parameters(docs)
        self.assertEqual(failures, [])
        item = next(x for x in entries if x["id"] == "epicfight:adaptive_skin")
        self.assertEqual(item["publisher_values"]["legacy_modifier_schema"], "RAW_ONLY_NOT_PROVEN_LOADED")

    def test_legacy_raw_schema_preserved_not_promoted(self):
        evidence, failures = compare_parameters(self.sample())
        self.assertEqual(failures, [])
        item = next(x for x in evidence if x["id"] == "epicfight:adrenaline_fiend")
        self.assertEqual(item["publisher_values"]["legacy_modifier_schema"], "RAW_ONLY_NOT_PROVEN_LOADED")

    def test_legacy_modifier_drift_fails_closed(self):
        docs = self.sample()
        docs["vengeance"]["attribute_modifiers"][0]["operation"] = "add_value"
        self.assertTrue(any("vengeance" in e for e in compare_parameters(docs)[1]))

    def test_legacy_modifier_migration_requires_reaudit(self):
        docs = self.sample()
        docs["bonebreaker"]["attribute_modifiers"][0]["id"] = "epicfight:bonebreaker"
        self.assertTrue(any("modern id" in e for e in compare_parameters(docs)[1]))

    def test_legacy_modifier_missing_fails_closed(self):
        docs = self.sample()
        docs["catharsis"]["attribute_modifiers"] = []
        self.assertTrue(any("catharsis" in e for e in compare_parameters(docs)[1]))

    def test_hooks_are_in_nested_compiled_classes(self):
        entity = "yesman.epicfight.api.event.EpicFightEventHooks$Entity"
        player = "yesman.epicfight.api.event.EpicFightEventHooks$Player"
        self.assertIn("MODIFY_ATTACK_SPEED", CLASS_SYMBOLS[entity])
        self.assertIn("TAKE_DAMAGE_INCOME", CLASS_SYMBOLS[entity])
        self.assertIn("CONSUME_SKILL", CLASS_SYMBOLS[player])
        self.assertNotIn("yesman.epicfight.api.event.EpicFightEventHooks", CLASS_SYMBOLS)

    def test_missing_nested_class_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "fixture.jar"
            with zipfile.ZipFile(path, "w") as z:
                for name, value in self.sample().items():
                    z.writestr(PARAMETER_PREFIX + name + ".json", json.dumps(value))
                for name in CLASS_SYMBOLS:
                    if name.endswith("$Player"):
                        continue
                    z.writestr(name.replace(".", "/") + ".class", b"synthetic-class-placeholder")
            _docs, errors = read_jar_parameters(path)
            self.assertTrue(any("EpicFightEventHooks$Player.class" in e for e in errors))


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
