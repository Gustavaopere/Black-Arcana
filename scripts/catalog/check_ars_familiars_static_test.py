#!/usr/bin/env python3
"""Static source-only contract QA for six Ars Nouveau 5.13.1 familiars.

The already-verified 109 compiled glyph+ritual IDs DO NOT cover familiar class
identity or method bytecode. These tests are documentation checks, not modpack QA.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARS = REPO / "wiki/modpack-catalog/providers/✅-ars-nouveau"
LEDGER = REPO / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
SHA1 = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
FIELDS = {"identity", "behavior", "parameters", "targeting", "costs",
          "integration", "validation"}
EXPECTED = {
    "amethyst-golem": (
        "AmethystFamiliarHolder", "FamiliarAmethystGolem",
        "ENTITY_FAMILIAR_BOOKWYRM", "FAMILIAR_AMETHYST_GOLEM",
        "LivingKnockBackEvent", "LivingDamageEvent.Post", "GEMS_AMETHYST",
        "3600", "player.equals(getOwner())"),
    "bookwyrm": (
        "FamiliarBookwyrm", "new AABB(owner.getOnPos()).inflate(5.0)",
        "ItemEntityPickupEvent.Pre", "PlayerXpEvent.PickupXp",
        "PreventRemoteMovement", "insertStack", "PlayerMainInvWrapper",
        "getOwnerID().equals(i.getOwner())", "giveExperiencePoints"),
    "drygmy": (
        "FamiliarDrygmy", "SpellModifierEvent",
        "spellResolveEvent", "modifierEvent", "addDamageModifier(2.0f)",
        "ELEMENTAL_EARTH", "LOOTING_EFFECT", "600",
        "LootingLevelEvent"),
    "starbuncle": (
        "FamiliarStarbuncle", "MOVEMENT_SPEED", "600", "amplifier",
        "NUGGETS_GOLD", "RitualScrying.grantScrying", "3600",
        "player.equals(getOwner())"),
    "whirlisprig": (
        "FamiliarWhirlisprig", "ENTITY_FAMILIAR_SYLPH",
        "FAMILIAR_WHIRLISPRIG", "SpellCostCalcEvent",
        "part.getCastingCost()*0.5", "event.currentCost",
        "LivingEntityUseItemEvent.Finish", "saturationLevel",
        "não checa explicitamente"),
    "wixie": (
        "FamiliarWixie", "getAllPotionRecipes", "PotionUtil.applyContents",
        "Potions.WATER", "Potions.AWKWARD", "MobEffectEvent.Added",
        "effect.duration += effect.duration/5", "DebuffTargetGoal",
        "debuffCooldown=150", "não checa owner"),
}

class FamiliarStaticCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.objects = cls.manifest["objects"]
        cls.provider = (ARS / "INDEX.md").read_text(encoding="utf-8")
        cls.directory = (ARS / "familiars/INDEX.md").read_text(encoding="utf-8")
        cls.global_index = (
            REPO / "wiki/modpack-catalog/providers/INDEX.md"
        ).read_text(encoding="utf-8")

    def test_six_source_only_certificates_and_seven_local_evidences(self):
        self.assertEqual(6, len(EXPECTED))
        for slug in EXPECTED:
            with self.subTest(familiar=slug):
                key = f"✅-ars-nouveau/familiars/{slug}.md"
                item = self.objects[key]
                self.assertEqual("COMPLETE_PERK_READY", item["status"])
                self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY",
                                 item["claim_scope"])
                self.assertEqual("PINNED_SOURCE_WITH_RELEASE_SHA_ONLY",
                                 item["evidence_grade"])
                self.assertEqual("5.13.1", item["version"])
                self.assertEqual(SHA1, item["artifact_sha1"])
                self.assertEqual(SOURCE, item["source_revision"])
                self.assertEqual("NOT_VERIFIED", item["mutating_hook"])
                self.assertEqual("NOT_TESTED", item["physical_qa"])
                self.assertEqual(FIELDS, set(item["evidence"]))
                for evidence in item["evidence"].values():
                    self.assertTrue(
                        (REPO / evidence["path"]).is_file(),
                        evidence["path"])
                    self.assertGreater(len(evidence["reason"]), 18)

    def test_card_consumer_tokens_and_fail_closed_limits(self):
        for slug, tokens in EXPECTED.items():
            with self.subTest(familiar=slug):
                content = (ARS / "familiars" / f"{slug}.md"
                           ).read_text(encoding="utf-8")
                for token in tokens:
                    self.assertIn(token, content)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY", content)
                self.assertIn("mutating_hook=NOT_VERIFIED", content)
                self.assertIn("physical_qa=NOT_TESTED", content)
                self.assertIn(SOURCE, content)
                self.assertIn(SHA1, content)
                self.assertIn("WorldEffectPolicy", content)

    def test_golem_type_mismatch_is_not_binary_verification(self):
        content = (ARS / "familiars/amethyst-golem.md").read_text(
            encoding="utf-8")
        self.assertIn("ENTITY_FAMILIAR_BOOKWYRM", content)
        self.assertIn("FAMILIAR_AMETHYST_GOLEM", content)
        self.assertIn("NÃO está verificado", content)
        self.assertIn("Falhar fechado", content)

    def test_drygmy_double_dispatch_is_not_certified_plus_four(self):
        content = (ARS / "familiars/drygmy.md").read_text(
            encoding="utf-8")
        for token in ("spellResolveEvent", "modifierEvent",
                      "SpellModifierEvent", "onModifier",
                      "não certificar +4", "comentado"):
            self.assertIn(token, content)

    def test_wixie_potions_and_combat_cooldown_not_client_proven(self):
        content = (ARS / "familiars/wixie.md").read_text(encoding="utf-8")
        for token in ("MobEffectEvent.Added", "debuffCooldown",
                      "não é serializado explicitamente",
                      "Potions.AWKWARD", "Potions.WATER",
                      "não checa owner", "150"):
            self.assertIn(token, content)

    def test_dossier_disclaims_binary_identity_and_real_qa(self):
        dossier = (ARS / "FAMILIAR-STATIC-SIX-5.13.1.md").read_text(
            encoding="utf-8")
        for token in (SOURCE, SHA1, "115/138", "115/2075", "0/164",
                      "85 glyphs e 24 rituais", "NÃO os seis familiares",
                      "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY",
                      "FamiliarSummonEvent", "WeakHashMap",
                      "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                      "physical_qa=NOT_TESTED", "06.05", "09"):
            self.assertIn(token, dossier)

    def test_indexes_count_certificates_without_closing_provider(self):
        self.assertIn("6/6.", self.directory)
        self.assertIn("contratos técnicos estáticos", self.directory)
        self.assertIn("0/164.", self.global_index)
        fam_count = sum(k.startswith("✅-ars-nouveau/familiars/")
                        for k in self.objects)
        ars_count = sum(k.startswith("✅-ars-nouveau/")
                        for k in self.objects)
        self.assertEqual(6, fam_count)
        self.assertIn(f"{fam_count}/6.", self.directory)
        self.assertIn(f"{ars_count}/138.", self.provider)
        self.assertIn(f"{len(self.objects)}/2075.", self.global_index)
        self.assertNotIn("100% certificado com escopo fechado", self.provider)
        for slug in EXPECTED:
            label = slug.replace("-", " ").title()
            self.assertIn(f"| ✅ | {label} |", self.directory)
            self.assertIn(f"| ✅ | {label} | [familiars/{slug}.md]",
                          self.provider)

if __name__ == "__main__":
    unittest.main()
