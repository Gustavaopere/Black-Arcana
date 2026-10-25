#!/usr/bin/env python3
"""Fail-closed regressions for twenty Ars Nouveau 5.13.1 Effect static dossiers.

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
    "harm": ("glyph_harm", "EffectHarm",
             ("MobEffects.POISON", "IDamageEffect.attemptDamage", "Duration Down")),
    "explosion": ("glyph_explosion", "EffectExplosion",
                  ("ANExplosion", "onExplosionStart", "DESTROY_WITH_DECAY", "4096")),
    "lightning": ("glyph_lightning", "EffectLightning",
                  ("LightningEntity", "EntityStruckByLightningEvent", "wetBonus", "EnergyStorage")),
    "freeze": ("glyph_freeze", "EffectFreeze",
               ("calcAOEBlocks", "Frosted Ice", "ShapersFocus", "Sensitive")),
    "ignite": ("glyph_ignite", "EffectIgnite",
               ("setRemainingFireTicks", "MAGIC_FIRE", "destroyRespectsClaim")),
    "blink": ("glyph_blink", "EffectBlink",
              ("TELEPORTING_NOT_SUPPORTED", "blinkForward", "getForward", "WarpScrollData")),
    "leap": ("glyph_leap", "EffectLeap",
             ("force_ground", "setDeltaMovement", "RotatingTurretTile", "Sensitive")),
    "launch": ("glyph_launch", "EffectLaunch",
               ("setDeltaMovement", "0,48", "ShapersFocus", "Sensitive")),
    "pull": ("glyph_pull", "EffectPull",
             ("ParticleUtil.inRange", "shooter.position", "canBlockBeHarvested", "Sensitive")),
    "snare": ("glyph_snare", "EffectSnare",
              ("groundBlock(true)", "SNARE_EFFECT", "IPotionEffect", "setDeltaMovement(0,0,0)")),
    "invisibility": ("glyph_invisibility", "EffectInvisibility",
                     ("MobEffects.INVISIBILITY", "applyConfigPotion", "false", "30", "8")),
    "wither": ("glyph_wither", "EffectWither",
               ("MobEffects.WITHER", "IPotionEffect", "Amplify", "30", "8")),
    "hex": ("glyph_hex", "EffectHex",
            ("ModPotions.HEX_EFFECT", "getBookDescription", "IPotionEffect", "4 Amplify")),
    "bounce": ("glyph_bounce", "EffectBounce",
               ("BOUNCE_EFFECT", "getPotionAugments", "setDeltaMovement")),
    "dispel": ("glyph_dispel", "EffectDispel",
               ("DispelEvent.Pre", "DispelEvent.Post", "IDispellable", "DISPEL_DENY", "DISPEL_ALLOW")),
}


class StaticContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = json.loads(MANIFEST.read_text(encoding="utf-8"))["objects"]
        cls.index = (ARS / "glyphs/effects/INDEX.md").read_text(encoding="utf-8")
        cls.root_index = (REPO / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf-8"
        )

    def test_twenty_distinct_effect_identities(self):
        self.assertEqual(20, len(CASES))
        self.assertEqual(20, len({v[0] for v in CASES.values()}))
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

    def test_twenty_evidence_paths_exist_in_checkout(self):
        for name in CASES:
            cert = self.cert["✅-ars-nouveau/glyphs/effects/" + name + ".md"]
            for field, evidence in cert["evidence"].items():
                with self.subTest(effect=name, field=field):
                    self.assertIsInstance(evidence.get("path"), str)
                    self.assertIsInstance(evidence.get("reason"), str)
                    self.assertGreater(len(evidence["reason"]), 18)
                    self.assertTrue((REPO / evidence["path"]).is_file())

    def test_all_parent_indexes_use_green_only_for_the_twenty(self):
        nested = [ARS / "glyphs/effects/INDEX.md",
                  ARS / "glyphs/INDEX.md", ARS / "INDEX.md"]
        for parent in nested:
            page = parent.read_text(encoding="utf-8")
            for slug in CASES:
                label = slug.replace("-", " ").title()
                with self.subTest(index=parent.name, effect=slug):
                    self.assertIn("| ✅ | " + label + " |", page)

    def test_counter_without_provider_wide_promotion(self):
        self.assertIn("Homologadas para perks (somente fichas detectadas): 35/67.",
                      self.index)
        # Other Ars families can gain independent certifications without
        # changing the number of Effect cards reviewed by this test suite.
        self.assertIn(
            f"Fichas com contrato técnico estático certificado: {len(self.cert)}/2075.",
            self.root_index,
        )
        self.assertIn("Mods com escopo integral certificado: 0/164.", self.root_index)
        self.assertGreaterEqual(len(self.cert), 53)

    def test_dossier_avoids_unproved_runtime_claims(self):
        page = GATE.read_text(encoding="utf-8")
        for token in ("5/67", SOURCE, SHA1, "NOT_VERIFIED", "NOT_TESTED",
                      "isInvertedHealAndHarm", "canGlide", "75"):
            self.assertIn(token, page)


    def test_damage_world_dossier_keeps_dynamic_consumers_outside_simple_spell(self):
        page = (ARS / "EFFECT-STATIC-DAMAGE-WORLD-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("10/67", "28/2.075", SOURCE, SHA1, "Poison em vez de dano",
                     "ANExplosion", "LightningEntity", "ShapersFocus",
                     "NOT_VERIFIED", "NOT_TESTED"):
            self.assertIn(term, page)
        # Static catalog never certifies gameplay, real QA, or provider-wide completion.
        self.assertNotIn("✅ 164/164", page)

    def test_damage_world_cards_keep_runtime_fail_closed_and_separate_paths(self):
        examples = {
            "harm": ("em vez de", "SpellDamageEvent.Pre"),
            "explosion": ("DESTROY_WITH_DECAY", "onExplosionDetonate"),
            "lightning": ("hitEntities", "restaurar", "SHOCKED_EFFECT"),
            "freeze": ("seis direções", "MOVEMENT_SLOWDOWN"),
            "ignite": ("destroyRespectsClaim", "setRemainingFireTicks"),
        }
        for slug, facts in examples.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                for fact in facts:
                    self.assertIn(fact, card)
                self.assertIn("mutating_hook=NOT_VERIFIED", card)
                self.assertIn("physical_qa=NOT_TESTED", card)


    def test_mobility_dossier_keeps_separate_vector_and_teleport_paths(self):
        page = (ARS / "EFFECT-STATIC-MOBILITY-CONTROL-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for token in ("15/67", "33/2.075", SOURCE, SHA1, "Blink",
                      "Leap", "Launch", "Pull", "Snare",
                      "substitui", "soma", "NOT_VERIFIED", "NOT_TESTED"):
            self.assertIn(token, page)
        self.assertNotIn("✅ 164/164", page)

    def test_mobility_cards_distinguish_mutation_and_applicability(self):
        examples = {
            "blink": ("getForward", "scroll", "canOcclude", "teleportTo"),
            "leap": ("force_ground", "max(0", "RotatingTurretTile", "setDeltaMovement"),
            "launch": ("0,48", "0,8", "setDeltaMovement", "Sensitive"),
            "pull": ("0,05", "shooter.position", "normal da face", "canBlockBeHarvested"),
            "snare": ("groundBlock(true)", "SNARE_EFFECT", "IPotionEffect",
                      "EntityHitResult"),
        }
        for slug, facts in examples.items():
            with self.subTest(effect=slug):
                card = (ARS / "glyphs/effects" / (slug + ".md")).read_text(
                    encoding="utf-8")
                for fact in facts:
                    self.assertIn(fact, card)
                self.assertIn("mutating_hook", card)
                self.assertIn("NOT_VERIFIED", card)
                self.assertIn("NOT_TESTED", card)


    def test_dossier_separates_status_callback_from_real_downstream_behavior(self):
        page = (ARS / "EFFECT-STATIC-STATUS-DISPEL-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("20/67", "38/2075", SOURCE, SHA1, "Invisibility", "Wither",
                     "Hex", "Bounce", "Dispel", "ICancellableEvent",
                     "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED"):
            self.assertIn(term, page)

    def test_dispel_public_event_is_not_approval_of_spell_mutation(self):
        dispel = (ARS / "glyphs/effects/dispel.md").read_text(encoding="utf-8")
        for term in ("DispelEvent.Pre", "DispelEvent.Post", "ICancellableEvent",
                     "EffectCures.MILK", "DISPEL_DENY", "DISPEL_ALLOW",
                     "EntityHitResult", "BlockEntity", "isCanceled",
                     "Post", "mutating_hook=NOT_VERIFIED",
                     "physical_qa=NOT_TESTED"):
            self.assertIn(term, dispel)
        self.assertIn("sem Post", dispel)
        self.assertIn("não prova", dispel)

    def test_status_cards_name_downstream_and_deduplicate_event_ticks(self):
        requirements = {
            "invisibility": ("showParticles", "false", "MobEffects.INVISIBILITY"),
            "wither": ("MobEffects.WITHER", "IPotionEffect", "30", "8"),
            "hex": ("HEX_EFFECT", "getBookDescription()", "não", "4 Amplify"),
            "bounce": ("BOUNCE_EFFECT", "setDeltaMovement", "downstream"),
        }
        for name, words in requirements.items():
            with self.subTest(effect=name):
                card = (ARS / "glyphs/effects" / (name + ".md")).read_text(
                    encoding="utf-8")
                for term in words:
                    self.assertIn(term, card)
                self.assertIn("mutating_hook=NOT_VERIFIED", card)
                self.assertIn("physical_qa=NOT_TESTED", card)


if __name__ == "__main__":
    unittest.main()
