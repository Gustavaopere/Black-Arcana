#!/usr/bin/env python3
"""Semantic negative controls and opt-in exact-binary ACFoods reproduction."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from alexscaves_1010_armor_material_audit import AuditError, digest, load_seal
from alexscaves_1010_foods_contract_audit import (
    CLAIMS, EFFECT_DESC, PREREQUISITES, PROVIDER, SEAL, SOUNDS, f32_value,
    prerequisites, validate_bridge, validate_contract,
)

SCRIPT = Path(__file__).with_name("alexscaves_1010_foods_contract_audit.py")


class FoodsSemanticRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prior = prerequisites()
        cls.seal = load_seal(SEAL)

    def rejected(self, change):
        altered = copy.deepcopy(self.seal)
        change(altered)
        with self.assertRaises(AuditError):
            validate_contract(altered, self.prior)

    def test_full_contract_is_internally_closed(self):
        validate_contract(self.seal, self.prior)
        self.assertEqual(len(self.seal["native"]["field_profiles"]), 63)
        self.assertEqual(len(self.seal["native"]["supplier_profiles"]), 46)

    def test_float32_bits_are_not_decimal_display_values(self):
        value = f32_value(0.1)
        self.assertEqual(value["bits_hex"], "3dcccccd")
        self.assertEqual(value["value"], 0.10000000149011612)
        self.assertNotEqual(value["value"], 0.1)
        self.assertEqual(f32_value(0.01)["bits_hex"], "3c23d70a")

    def test_missing_preset_rejected(self):
        self.rejected(lambda d: d["native"]["field_profiles"].pop("ALEX_MEAL"))

    def test_unobserved_preset_rejected(self):
        self.rejected(lambda d: d["native"]["field_profiles"].update(NEW_FOOD={}))

    def test_nutrition_drift_rejected(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["ALEX_MEAL"].update(nutrition=20))

    def test_decimal_rounding_cannot_replace_binary32_operand(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["BIOME_TREAT"]["saturation_modifier"].update(value=0.1))

    def test_binary32_bit_drift_rejected(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["BIOME_TREAT"]["saturation_modifier"].update(bits_hex="3dccccce"))

    def test_effect_probability_drift_rejected(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["RADGILL_COOKED"]["effects"][0].update(probability=f32_value(1)))

    def test_two_effect_order_is_not_interchangeable(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["ALEX_MEAL"]["effects"].reverse())

    def test_payload_supplier_cannot_be_substituted(self):
        self.rejected(lambda d: d["native"]["field_profiles"]["RADGILL"]["effects"][0].update(supplier="lambda$static$3"))

    def test_effect_duration_drift_rejected(self):
        self.rejected(lambda d: d["native"]["supplier_profiles"]["lambda$static$45"].update(duration_ticks=200))

    def test_implicit_amplifier_cannot_be_promoted(self):
        self.rejected(lambda d: d["native"]["supplier_profiles"]["lambda$static$45"].update(amplifier_argument=0))

    def test_sound_fields_are_concrete_and_finite(self):
        for field, (offset, name) in SOUNDS.items():
            sound = self.seal["native"]["field_profiles"][field]["sound"]
            self.assertEqual((sound["offset"], sound["field"]), (offset, name))
        self.rejected(lambda d: d["native"]["field_profiles"]["SOYLENT_GREEN"]["sound"].update(field="undefined"))

    def test_initializer_coverage_cannot_be_shortened(self):
        self.rejected(lambda d: d["native"].update(initializer_instruction_count=605))

    def test_missing_supplier_body_rejected(self):
        self.rejected(lambda d: d["native"]["methods"].pop())

    def test_added_guard_cannot_hide_in_existing_supplier(self):
        def change(d):
            body = next(m for m in d["native"]["methods"] if m["declaration"]["descriptor"] == EFFECT_DESC)
            body["instructions"][0]["opcode"] = "ifeq"
        self.rejected(change)

    def test_partial_body_cannot_keep_original_hash(self):
        self.rejected(lambda d: d["native"]["methods"][0]["instructions"].pop())

    def test_external_consumer_missing_site_rejected(self):
        def change(d):
            next(iter(d["native"]["direct_field_read_boundary"].values()))["methods"][0]["sites"].pop()
        self.rejected(change)

    def test_external_write_is_not_treated_as_original_read(self):
        def change(d):
            next(iter(d["native"]["direct_field_read_boundary"].values()))["methods"][0]["sites"][0]["opcode"] = "putstatic"
        self.rejected(change)

    def test_holder_bridge_must_use_builtin_registry(self):
        altered = copy.deepcopy(self.seal["native"]["effect_holder_bridge"]["method"])
        altered["instructions"][2]["symbol"] = "InterfaceMethod example/Registry.applyEffect:()V"
        with self.assertRaises(AuditError):
            validate_bridge(altered)

    def test_readonly_dependency_seals_are_pinned(self):
        self.assertEqual({name: digest((PROVIDER / name).read_bytes()) for name in PREREQUISITES}, PREREQUISITES)
        self.rejected(lambda d: d["prerequisites"]["seal_sha256"].update({next(iter(PREREQUISITES)): "0" * 64}))

    def test_mutation_runtime_qa_perk_and_universe_claims_fail_closed(self):
        for key, value in {"mutating_hook": "VERIFIED", "physical_qa": "TESTED",
                           "perk_certification": "CERTIFIED", "runtime_dispatch": "VERIFIED",
                           "provider_universe_closed": True, "semantic_magic_roots_delta": 63,
                           "mutation": "MUTATE"}.items():
            with self.subTest(key=key):
                self.rejected(lambda d, k=key, v=value: d["claims"].update({k: v}))
        self.assertEqual(self.seal["claims"], CLAIMS)

    def test_complete_food_and_effect_execution_cannot_be_claimed(self):
        self.rejected(lambda d: d["boundaries"].update(complete_food_item_or_block_behavior="CERTIFIED"))
        self.rejected(lambda d: d["boundaries"].update(effect_application_acceptance="VERIFIED"))


@unittest.skipUnless(os.environ.get("AC_FOODS_JAR") and os.environ.get("AC_FOODS_JAVAP"),
                     "opt-in exact publisher/JDK21 paths; mandatory in contract CI")
class FoodsBinaryReproduction(unittest.TestCase):
    def run_cli(self, jar, output, *, expected=0):
        cmd = [sys.executable, str(SCRIPT), "--jar", str(jar), "--javap", os.environ["AC_FOODS_JAVAP"],
               "--seal", str(SEAL), "--output", str(output)]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=150)
        if expected == 0:
            self.assertEqual(proc.returncode, 0, proc.stderr[-4000:])
        else:
            self.assertNotEqual(proc.returncode, 0)
        return proc

    def test_twice_run_exact_binary_cli_preserves_all_inputs(self):
        jar = Path(os.environ["AC_FOODS_JAR"])
        paths = [jar, Path(os.environ["AC_FOODS_JAVAP"]), SEAL,
                 *(PROVIDER / name for name in PREREQUISITES)]
        before = {p: digest(p.read_bytes()) for p in paths}
        with tempfile.TemporaryDirectory() as raw:
            first, second = (Path(raw) / name for name in ("first.json", "second.json"))
            self.run_cli(jar, first)
            self.run_cli(jar, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(json.loads(first.read_text()), load_seal(SEAL))
        self.assertEqual(before, {p: digest(p.read_bytes()) for p in paths})

    def test_wrong_artifact_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as raw:
            jar, output = Path(raw) / "wrong.jar", Path(raw) / "output.json"
            jar.write_bytes(b"not the publisher")
            before = jar.read_bytes()
            self.run_cli(jar, output, expected=1)
            self.assertFalse(output.exists())
            self.assertEqual(jar.read_bytes(), before)

    def test_existing_report_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "output.json"
            output.write_text("preserve this evidence")
            self.run_cli(Path(os.environ["AC_FOODS_JAR"]), output, expected=1)
            self.assertEqual(output.read_text(), "preserve this evidence")


if __name__ == "__main__":
    unittest.main()
