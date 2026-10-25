#!/usr/bin/env python3
"""Fail-closed, static-only Ars 5.13.1 source-pinned ritual evidence regression.

No client, runtime, Source transaction, classfile method equality, or external
perk bridge is exercised. The exact binary ID checks are a separate CI job.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-ars-nouveau"
MANIFEST = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
SHA1 = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
FIELDS = {"identity", "behavior", "parameters", "targeting",
          "costs", "integration", "validation"}
CASES = {
    "sunrise": ("ritual_sunrise", "RitualSunrise",
                ("ClientboundSetTimePacket", "100", "18", "server.overworld")),
    "moonfall": ("ritual_moonfall", "RitualMoonfall",
                 ("NIGHT_TIME", "13000", "ClientboundSetTimePacket", "18")),
    "fertility": ("ritual_fertility", "RitualBreed",
                  ("200", "20", "BREED_BLACKLIST", "setNeedsSource(true)", "500")),
    "flight": ("ritual_flight", "RitualFlight",
               ("RangeEffectRitual", "1200", "200", "60", "PacketUpdateFlight")),
    "scrying": ("ritual_scrying", "RitualScrying",
                ("TagScryer", "SingleBlockScryer", "an_scryer",
                 "6000", "18000", "setFinished()")),
    "gravity": ("ritual_gravity", "RitualGravity",
                ("GRAVITY_EFFECT", "RangeEffectRitual", "renewThreshold", "1200")),
    "restoration": ("ritual_restoration", "RitualHealing",
                    ("ZombieVillager.startConverting", "ANFakePlayer", "playerAttack", "10.0f")),
    "warping": ("ritual_warping", "RitualWarp",
                 ("canTeleportWithDim", "teleportTo", "WarpScroll", "progress>=3")),
    "containment": ("ritual_containment", "RitualMobCapture",
                    ("JAR_WHITELIST", "JAR_BLACKLIST", "MobJarTile", "UNLOADED_TO_CHUNK")),
    "harvest": ("ritual_harvest", "RitualHarvest",
                 ("InventoryManager.insertStack", "MAGE_BLOOM_CROP", "HARVEST_STEMS", "200")),
    "binding": ("ritual_binding", "RitualBinding",
                ("FamiliarRegistry", "RemovalReason.DISCARDED", "getOutputItem()",
                 "AABB", "AbstractRitual.getSourceCost()")),
    "awakening": ("ritual_awakening", "RitualAwakening",
                  ("BOOKWYRM_CHARM", "WritableBookItem", "withinManhattan",
                   "DFSBlockstates", "BUDDING_AMETHYST")),
}


class ArsRitualStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.json = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.index = (PROVIDER / "rituals/INDEX.md").read_text(encoding="utf-8")
        cls.top = (ROOT / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf-8")
        cls.ars = (PROVIDER / "INDEX.md").read_text(encoding="utf-8")
        cls.dossier = (PROVIDER / "RITUAL-STATIC-FIRST-FIVE-5.13.1.md").read_text(
            encoding="utf-8")

    def test_twelve_unique_binary_pinned_ritual_identities(self):
        self.assertEqual(12, len(CASES))
        self.assertEqual(12, len({item[0] for item in CASES.values()}))
        for slug, (ritual_id, classname, facts) in CASES.items():
            with self.subTest(slug=slug):
                body = (PROVIDER / "rituals" / (slug + ".md")).read_text(
                    encoding="utf-8")
                self.assertIn("ars_nouveau:" + ritual_id, body)
                self.assertIn(classname, body)
                for fact in facts:
                    self.assertIn(fact, body)

    def test_only_static_contracts_are_green(self):
        for slug in CASES:
            with self.subTest(ritual=slug):
                key = "✅-ars-nouveau/rituals/" + slug + ".md"
                cert = self.json["objects"][key]
                self.assertEqual("COMPLETE_PERK_READY", cert["status"])
                self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY",
                                 cert["claim_scope"])
                self.assertEqual("PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY",
                                 cert["evidence_grade"])
                self.assertEqual(SOURCE, cert["source_revision"])
                self.assertEqual(SHA1, cert["artifact_sha1"])
                self.assertEqual("NOT_VERIFIED", cert["mutating_hook"])
                self.assertEqual("NOT_TESTED", cert["physical_qa"])
                self.assertEqual(FIELDS, set(cert["evidence"]))

    def test_evidence_has_real_checked_out_paths(self):
        for slug in CASES:
            evidences = self.json["objects"][
                "✅-ars-nouveau/rituals/" + slug + ".md"]["evidence"]
            for field, proof in evidences.items():
                with self.subTest(slug=slug, field=field):
                    self.assertTrue((ROOT / proof["path"]).is_file())
                    self.assertGreater(len(proof["reason"]), 24)

    def test_numerators_and_parent_statuses(self):
        # Check true independent counters against manifest; adding Effects in
        # another PR must never invalidate already proven Rituals.
        objs = self.json["objects"]
        ritual_count = sum(key.startswith("✅-ars-nouveau/rituals/") for key in objs)
        ars_count = sum(key.startswith("✅-ars-nouveau/") for key in objs)
        self.assertGreaterEqual(ritual_count, 12)
        self.assertGreaterEqual(ars_count, 65)
        self.assertIn(f"Homologadas para perks (somente fichas detectadas): {ritual_count}/24.", self.index)
        self.assertIn(f"Homologadas para perks (somente fichas detectadas): {ars_count}/138.", self.ars)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {len(objs)}/2075.", self.top)
        self.assertIn(f"Mods com escopo integral certificado: {len(self.json['providers'])}/164.", self.top)
        for slug in CASES:
            label = slug.capitalize()
            # Same display name may exist in Glyphs/Effects and in Rituals.
            row_index = next(
                line for line in self.index.splitlines()
                if line.startswith("| ✅ | " + label + " | ")
                and line.endswith("](" + slug + ".md) |")
            )
            row_root = next(
                line for line in self.ars.splitlines()
                if line.startswith("| ✅ | " + label + " | ")
                and line.endswith("](rituals/" + slug + ".md) |")
            )
            self.assertIn(slug + ".md", row_index)
            self.assertIn("rituals/" + slug + ".md", row_root)

    def test_local_ritual_execution_is_not_spell_cooldown_or_mana(self):
        for slug in CASES:
            body = (PROVIDER / "rituals" / (slug + ".md")).read_text(
                encoding="utf-8")
            self.assertIn("mutating_hook=NOT_VERIFIED", body)
            self.assertIn("physical_qa=NOT_TESTED", body)
            self.assertIn("Source", body)
            self.assertIn("não", body.lower())

    def test_inherited_source_zero_does_not_mean_free_activation(self):
        for slug in ("sunrise", "moonfall", "scrying", "warping"):
            card = (PROVIDER / "rituals" / (slug + ".md")).read_text(
                encoding="utf-8")
            self.assertIn("AbstractRitual.getSourceCost()", card)
            self.assertIn("0", card)
        self.assertIn("não equivale a ritual grátis", self.dossier.lower())

    def test_risky_global_time_rituals_do_not_assume_fixed_wall_duration(self):
        for slug in ("sunrise", "moonfall"):
            text = (PROVIDER / "rituals" / (slug + ".md")).read_text(
                encoding="utf-8")
            self.assertIn("incrementProgress()", text)
            self.assertIn("20", text)
            self.assertIn("não", text.lower())

    def test_scrying_completion_without_valid_scryer_is_not_success(self):
        text = (PROVIDER / "rituals/scrying.md").read_text(
            encoding="utf-8")
        self.assertIn("apenas Manipulation Essence", text)
        self.assertIn("setFinished()", text)
        self.assertIn("scryer", text)
        self.assertIn("an_scryer", text)

    def test_dossier_is_static_and_does_not_promote_runtime_stages(self):
        for token in ("5/24", SHA1, SOURCE, "NOT_VERIFIED", "NOT_TESTED",
                      "Source", "ClientboundSetTimePacket", "6000",
                      "18000", "0/164", "06.05"):
            self.assertIn(token, self.dossier)


    def test_second_five_rituals_have_distinct_spatial_and_settlement_gates(self):
        page = (PROVIDER / "RITUAL-STATIC-SECOND-FIVE-5.13.1.md").read_text(
            encoding="utf-8")
        for term in ("10/24", "63/2075", SOURCE, SHA1, "RitualGravity",
                     "Gravity", "Restoration", "Warping", "Containment",
                     "Harvest", "WorldEffectPolicy", "NOT_VERIFIED", "NOT_TESTED",
                     "Stage 06.05"):
            self.assertIn(term, page)

    def test_source_world_capture_and_storage_hazards_are_fail_closed(self):
        required = {
            "gravity": ("renewInterval", "renewThreshold", "não inferir",
                        "RangeEffectRitual", "200 Source"),
            "restoration": ("didWorkOnce", "ANFakePlayer", "10.0f",
                            "setNeedsSource(true)"),
            "warping": ("canTeleportWithDim", "teleportTo(double,double,double)",
                        "getConsumedItems().get(0)", "BlockPos"),
            "containment": ("343", "AABB", "JAR_WHITELIST",
                            "UNLOADED_TO_CHUNK", "setNeedsSource(true)"),
            "harvest": ("243", "Y+2", "MAGE_BLOOM_CROP",
                        "InventoryManager.insertStack", "destroyRespectsClaim"),
        }
        for slug, facts in required.items():
            with self.subTest(ritual=slug):
                card = (PROVIDER / "rituals" / (slug + ".md")).read_text(
                    encoding="utf-8")
                for token in facts:
                    self.assertIn(token, card)
                self.assertIn("mutating_hook=NOT_VERIFIED", card)
                self.assertIn("physical_qa=NOT_TESTED", card)

    def test_same_named_effect_is_not_certified_by_ritual(self):
        self.assertIn(
            "| ⚠️ | Harvest | [glyphs/effects/harvest.md](glyphs/effects/harvest.md) |",
            self.ars)
        self.assertIn(
            "| ✅ | Harvest | [rituals/harvest.md](rituals/harvest.md) |",
            self.ars)


    def test_binding_familiar_holder_collision_cannot_be_assumed_unique(self):
        binding = (PROVIDER / "rituals/binding.md").read_text(encoding="utf8")
        for token in ("getGameTime()%20==0", "getProgress()>=3",
                      "FamiliarRegistry.getFamiliarHolderMap()", "Não há `break`",
                      "getOutputItem()", "8 blocos", "DISCARDED",
                      "0 Source", "mutating_hook=NOT_VERIFIED"):
            self.assertIn(token, binding)
        self.assertIn("não equivale a ritual grátis", binding.lower())

    def test_awakening_modes_world_mutation_and_book_consumption_are_separate(self):
        awakening = (PROVIDER / "rituals/awakening.md").read_text(encoding="utf8")
        for token in ("WritableBookItem", "getProgress()>5",
                      "BOOKWYRM_CHARM", "numBookwyrms", "350", ">=50",
                      "Blazing", "Flourishing", "Vexing", "Cascading",
                      "ANFakePlayer", "BUDDING_AMETHYST",
                      "getSourceCost()=0", "destroyRespectsClaim",
                      "mutating_hook=NOT_VERIFIED"):
            self.assertIn(token, awakening)
        self.assertIn("não equivale", awakening)

    def test_third_ritual_dossier_retains_source_and_fail_closed_claims(self):
        dossier = (PROVIDER / "RITUAL-STATIC-THIRD-TWO-5.13.1.md").read_text(
            encoding="utf8")
        for token in ("12/24", SOURCE, SHA1, "Binding", "Awakening",
                      "FamiliarRegistry", "BOOKWYRM_CHARM", "getSourceCost()=0",
                      "NOT_VERIFIED", "NOT_TESTED", "WorldEffectPolicy",
                      "Stage 06.05", "Stage 09"):
            self.assertIn(token, dossier)


if __name__ == "__main__":
    unittest.main()
