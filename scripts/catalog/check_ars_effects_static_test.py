#!/usr/bin/env python3
"""Fail-closed regressions for five Ars Nouveau 5.13.1 Effect static dossiers.

No code execution, loaded provider API, runtime effect or perk behavior is
implied by these tests; exact release binary registration remains separately
verified by the Ars 109-ID workflow.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARS = REPO / "wiki/modpack-catalog/providers/✅-ars-nouveau"
MANIFEST = REPO / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
GATE = ARS / "EFFECT-STATIC-FIRST-FIVE-5.13.1.md"
RELEASE = "5.13.1"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
SHA1 = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
EVIDENCE = frozenset({"identity", "behavior", "parameters", "targeting",
                      "costs", "integration", "validation"})
CASES = {
    "heal": ("glyph_heal", "EffectHeal",
             ("causeFoodExhaustion(2.5f)", "Player", "DamageTypes.MAGIC", "attemptDamage")),
    "slowfall": ("glyph_slowfall", "EffectSlowfall",
                 ("MobEffects.SLOW_FALLING", "IPotionEffect", "30", "8")),
    "glide": ("glyph_glide", "EffectGlide",
              ("GlidingPerk", "ModPotions.GLIDE_EFFECT", "180", "120", "30/8")),
    "sense-magic": ("glyph_sense_magic", "EffectSenseMagic",
                    ("IPedestalMachine", "MAGIC_FIND_EFFECT", "75", "60")),
    "knockback": ("glyph_gust", "EffectKnockback",
                  ("KNOCKBACK_RESISTANCE", "EnchantedFallingBlock", "Sensitive", "Extract")),
}


class StaticContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = json.loads(MANIFEST.read_text(encoding="utf-8"))["objects"]
        cls.index = (ARS / "glyphs/effects/INDEX.md").read_text(encoding="utf-8")
        cls.root_index = (REPO / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf-8"
        )

    def test_five_distinct_effect_identities(self):
        self.assertEqual(5, len(CASES))
        self.assertEqual(5, len({v[0] for v in CASES.values()}))
        for slug, (identity, class_name, facts) in CASES.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                self.assertIn("ars_nouveau:" + identity, card)
                self.assertIn(class_name, card)
                for fact in facts:
                    self.assertIn(fact, card)

    def test_certifications_are_static_and_runtime_fail_closed(self):
        for name in CASES:
            with self.subTest(effect=name):
                key = "✅-ars-nouveau/glyphs/effects/" + name + ".md"
                data = self.cert[key]
                self.assertEqual("COMPLETE_PERK_READY", data["status"])
                self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", data["claim_scope"])
                self.assertEqual("PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY",
                                 data["evidence_grade"])
                self.assertEqual(SOURCE, data["source_revision"])
                self.assertEqual(RELEASE, data["version"])
                self.assertEqual(SHA1, data["artifact_sha1"])
                self.assertEqual("NOT_VERIFIED", data["mutating_hook"])
                self.assertEqual("NOT_TESTED", data["physical_qa"])
                self.assertEqual(EVIDENCE, set(data["evidence"]))

    def test_five_evidence_paths_exist_in_checkout(self):
        for name in CASES:
            cert = self.cert["✅-ars-nouveau/glyphs/effects/" + name + ".md"]
            for field, evidence in cert["evidence"].items():
                with self.subTest(effect=name, field=field):
                    self.assertIsInstance(evidence.get("path"), str)
                    self.assertIsInstance(evidence.get("reason"), str)
                    self.assertGreater(len(evidence["reason"]), 18)
                    self.assertTrue((REPO / evidence["path"]).is_file())

    def test_all_parent_indexes_use_green_only_for_the_five(self):
        nested = [ARS / "glyphs/effects/INDEX.md",
                  ARS / "glyphs/INDEX.md", ARS / "INDEX.md"]
        for parent in nested:
            page = parent.read_text(encoding="utf-8")
            for slug in CASES:
                label = slug.replace("-", " ").title()
                with self.subTest(index=parent.name, effect=slug):
                    self.assertIn("| ✅ | " + label + " |", page)

    def test_counter_without_provider_wide_promotion(self):
        self.assertIn("Homologadas para perks (somente fichas detectadas): 5/67.",
                      self.index)
        self.assertIn("Fichas com contrato técnico estático certificado: 23/2075.",
                      self.root_index)
        self.assertIn("Mods com escopo integral certificado: 0/164.", self.root_index)
        self.assertEqual(23, len(self.cert))

    def test_dossier_avoids_unproved_runtime_claims(self):
        page = GATE.read_text(encoding="utf-8")
        for token in ("5/67", SOURCE, SHA1, "NOT_VERIFIED", "NOT_TESTED",
                      "isInvertedHealAndHarm", "canGlide", "75"):
            self.assertIn(token, page)


if __name__ == "__main__":
    unittest.main()
