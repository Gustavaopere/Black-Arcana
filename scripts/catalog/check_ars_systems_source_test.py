#!/usr/bin/env python3
"""Source-pinned Ars Nouveau 5.13.1 system docs (not runtime or binary QA).

Do not turn the 109 glyph+ritual binary ID checks into evidence for mana,
armor providers or learned glyph persistence. Supports later certification.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARS = ROOT / "wiki/modpack-catalog/providers/✅-ars-nouveau"
DOCS = ARS / "systems"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
SHA1 = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
CASES = {
    "perk-slot-providers": (
        "APIRegistry", "PerkRegistry.registerPerkProvider",
        "ArmorPerkHolder.getSlotsForTier", "slotsForTier.get(getTier())",
        "PerkSlot.ONE/TWO/THREE", "getPerkInstances",
        "30*(perkHolder.getTier()+1)", "MANA_REGEN_BONUS",
        "getHolderForPerk", "WorldEffectPolicy",
    ),
    "player-mana": (
        "IManaCap", "ManaCapEvents.playerOnTick", "ManaUtil.calcMaxMana",
        "ManaUtil.getManaRegen", "AttachmentsRegistry.MANA_ATTACHMENT",
        "current", "book_tier", "reserved", "MaxManaCalcEvent.setReserve",
        "Mth.clamp(0,newReserve,1)", "SpellCostCalcEvent.Pre",
        "SpellCostCalcEvent.Post", "CastResolveType.SUCCESS",
        "TileCaster", "getRealMax()", "WorldEffectPolicy",
    ),
    "spellbooks-glyph-learning": (
        "Glyph.use", "SpellBook.use", "getKnownGlyphs",
        "ANPlayerData.serializeNBT", "ANPlayerData", "GlyphRecipeProvider",
        "GlyphRegistry.getSpellPart(id)", "unlockGlyph",
        "Config.isGlyphEnabled", "27", "55", "160",
        "hasInfiniteMaterials", "WorldEffectPolicy",
    ),
}


class ArsSystemsSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
             ).read_text(encoding="utf8"))
        cls.index = (DOCS / "INDEX.md").read_text(encoding="utf8")
        cls.dossier = (ARS / "SYSTEM-STATIC-SOURCE-THREE-5.13.1.md"
                       ).read_text(encoding="utf8")

    def test_source_provenance_and_three_technical_system_cards(self):
        for slug, terms in CASES.items():
            with self.subTest(system=slug):
                path = DOCS / (slug + ".md")
                text = path.read_text(encoding="utf8")
                for t in terms:
                    self.assertIn(t, text)
                for t in (SOURCE, SHA1, "mutating_hook=NOT_VERIFIED",
                          "physical_qa=NOT_TESTED"):
                    self.assertIn(t, text)
                self.assertNotIn("SHA_EXACT_BINARY_BEHAVIOR", text)

    def test_mana_events_costs_and_reserve_do_not_claim_transactionality(self):
        page = (DOCS / "player-mana.md").read_text(encoding="utf8")
        for t in ("REGEN_INTERVAL", "getResolveCost", "getExpendedCost",
                  "Math.max(0,event.currentCost)", "getCurrentMana",
                  "getMaxMana", "SpellCostCalcEvent.Pre",
                  "SpellCostCalcEvent.Post", "não há igualdade/atomicidade garantida",
                  "newReserve>1", "FamiliarEvents.maxManaCalc",
                  "removeMana"):
            self.assertIn(t, page)
        self.assertIn("não defeito demonstrado no JAR", page)

    def test_glyph_learning_is_distinct_from_mana_and_recipe_xp(self):
        page = (DOCS / "spellbooks-glyph-learning.md").read_text(
            encoding="utf8")
        for t in ("SpellTier.CREATIVE", "GlyphRegistry",
                  "iMana.getGlyphBonus()", "cap.getKnownGlyphs()",
                  "GlyphRecipeProvider.getExpFromTier", "27", "55", "160",
                  "deserializeNBT", "null",
                  "Mastery RPG", "addon", "server"):
            self.assertIn(t, page)

    def test_armor_provider_is_not_rpg_perk_tree(self):
        page = (DOCS / "perk-slot-providers.md").read_text(
            encoding="utf8")
        for t in ("12 providers", "BATTLEMAGE_*", "ARCANIST_*",
                  "SORCERER_*", "máximo"):
            self.assertIn(t, page)
        self.assertIn("getTier()", page)
        self.assertIn("não faz bounds check explícito", page)
        self.assertIn("ADD_VALUE", page)

    def test_dossier_keeps_systems_uncertified_until_manifest_update(self):
        for t in (SOURCE, SHA1, "109 registros = 85 glyphs + 24 rituais",
                  "NÃO certificado no manifesto", "SpellCostCalcEvent.Pre",
                  "SpellCostCalcEvent.Post", "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY",
                  "WorldEffectPolicy", "mutating_hook=NOT_VERIFIED",
                  "physical_qa=NOT_TESTED", "06.05/09"):
            self.assertIn(t, self.dossier)
        obj = self.ledger["objects"]
        for slug in CASES:
            key = f"✅-ars-nouveau/systems/{slug}.md"
            certified = key in obj
            if certified:
                self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY",
                                 obj[key]["claim_scope"])
                self.assertEqual("PINNED_SOURCE_WITH_RELEASE_SHA_ONLY",
                                 obj[key]["evidence_grade"])
            label = slug.replace("-", " ").title()
            marker = "✅" if certified else "⚠️"
            self.assertIn(f"| {marker} | {label} |", self.index)

if __name__ == "__main__":
    unittest.main()
