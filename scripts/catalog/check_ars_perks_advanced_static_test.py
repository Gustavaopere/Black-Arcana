#!/usr/bin/env python3
"""Four source-only Ars armor thread contracts: runtime QA is not implied."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

from check_perk_ready_indexes import inventory as catalog_inventory

REPO = Path(__file__).resolve().parents[2]
ARS = REPO / "wiki/modpack-catalog/providers/✅-ars-nouveau"
LEDGER = REPO / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
SOURCE = "baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157"
SHA = "02782d071ee5fab3b5c4b8ced67b7e1748277dfd"
FIELDS = frozenset({"identity","behavior","parameters","targeting","costs",
                    "integration","validation"})
CASES = {
 "undying": ("TotemPerk", "thread_undying", "getInitTag",
             "LivingDeathEvent", "SleepFinishedTimeEvent",
             "getHolderForPerk", "ARMOR_PERKS", "isActive=false"),
 "repairing": ("RepairingPerk", "thread_repairing",
               "BASE_ARMOR_REPAIR_RATE", "getGameTime()%200",
               "cap.removeMana(20)", "UNBREAKING",
               "EnchantersSword", "EnchantersShield"),
 "life-drain": ("VampiricPerk", "thread_life_drain",
                "SpellDamageEvent.Post", "PerkEvents.postSpellDamageEvent",
                "0.2f", "countForPerk", "getPerksFromLiving",
                "event.caster.heal"),
 "gliding": ("GlidingPerk", "thread_gliding", "PerkSlot.THREE",
              "EffectGlide.canGlide", "PlayerTickEvent.Pre",
              "ArsNouveau.caelusLoaded", "CaelusHandler.setFlying",
              "ElytraPlayerMixin", "addTransientModifier")
}
class FourArmorPerksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_text(encoding="utf8"))
        cls.objects = cls.data["objects"]
        cls.perks = (ARS/"perks/INDEX.md").read_text(encoding="utf8")
        cls.ars = (ARS/"INDEX.md").read_text(encoding="utf8")
        cls.global_index = (REPO/"wiki/modpack-catalog/providers/INDEX.md").read_text(encoding="utf8")

    def test_perks_have_distinct_source_only_release_provenance(self):
        for slug in CASES:
            with self.subTest(slug=slug):
                item = self.objects[f"✅-ars-nouveau/perks/{slug}.md"]
                self.assertEqual(item["status"], "COMPLETE_PERK_READY")
                self.assertEqual(item["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
                self.assertEqual(item["evidence_grade"], "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY")
                self.assertEqual(item["mutating_hook"], "NOT_VERIFIED")
                self.assertEqual(item["physical_qa"], "NOT_TESTED")
                self.assertEqual(item["artifact_sha1"], SHA)
                self.assertEqual(item["source_revision"], SOURCE)
                self.assertEqual(set(item["evidence"]), FIELDS)
                for ev in item["evidence"].values():
                    self.assertTrue((REPO/ev["path"]).is_file(), ev["path"])
                    self.assertGreater(len(ev["reason"]), 18)

    def test_individual_perk_consumers_are_documented(self):
        for slug,tokens in CASES.items():
            with self.subTest(slug=slug):
                page = (ARS/"perks"/f"{slug}.md").read_text(encoding="utf8")
                for token in tokens:
                    self.assertIn(token, page)
                for token in ("STATIC_TECHNICAL_CATALOG_ONLY", SOURCE, SHA,
                              "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED",
                              "WorldEffectPolicy"):
                    self.assertIn(token, page)

    def test_max_slot_is_not_aggregated_sum_or_selection_order(self):
        dossier = (ARS/"PERK-STATIC-LIFECYCLE-UNDYING-REPAIRING-DRAIN-GLIDING-5.13.1.md"
                  ).read_text(encoding="utf8")
        for token in ("PerkUtil.countForPerk", "máximo", "getHolderForPerk",
                      "última instância", "getPerksFromLiving",
                      "cada instância equipada", "não sua soma"):
            self.assertIn(token, dossier)
        life = (ARS/"perks/life-drain.md").read_text(encoding="utf8")
        self.assertIn("múltiplas tentativas de heal", life)
        death = (ARS/"perks/undying.md").read_text(encoding="utf8")
        self.assertIn("último correspondente iterado", death)

    def test_repair_mana_and_server_side_are_not_implied_safe(self):
        page = (ARS/"perks/repairing.md").read_text(encoding="utf8")
        for term in ("getGameTime()%200", "20 mana Ars",
                     "EnchantersSword.inventoryTick",
                     "EnchantersShield.inventoryTick",
                     "sem gate", "onAdded", "onRemoved",
                     "UNBREAKING"):
            self.assertIn(term,page)
        self.assertIn("sem gate",page)

    def test_glide_caelus_teardown_is_unverified(self):
        page = (ARS/"perks/gliding.md").read_text(encoding="utf8")
        for t in ("ElytraPlayerMixin.elytraOverride", "original ||",
                  "EffectGlide.canGlide", "CaelusHandler.setFlying",
                  "addTransientModifier", "apenas adiciona e não remove"):
            self.assertIn(t,page)

    def test_scope_and_indexes_match_certification_ledger(self):
        dossier = (ARS/"PERK-STATIC-LIFECYCLE-UNDYING-REPAIRING-DRAIN-GLIDING-5.13.1.md"
                  ).read_text(encoding="utf8")
        for term in (SOURCE, SHA, "119/138", "119/2075", "0/164",
                     "85 glyphs e 24 rituals", "não", "WorldEffectPolicy",
                     "mutating_hook=NOT_VERIFIED", "physical_qa=NOT_TESTED"):
            self.assertIn(term,dossier)
        n=sum(k.startswith("✅-ars-nouveau/perks/") for k in self.objects)
        a=sum(k.startswith("✅-ars-nouveau/") for k in self.objects)
        self.assertEqual(n,20)
        self.assertIn(f"{n}/20.",self.perks)
        self.assertIn(f"{a}/138.",self.ars)
        self.assertIn(f"{len(self.objects)}/{len(catalog_inventory()[2])}.",self.global_index)
        self.assertIn("0/164.",self.global_index)
        for slug in CASES:
            name = slug.replace("-", " ").title()
            self.assertIn(f"| ✅ | {name} |",self.perks)
            self.assertIn(f"| ✅ | {name} | [perks/{slug}.md]",self.ars)

if __name__ == "__main__":
    unittest.main()
