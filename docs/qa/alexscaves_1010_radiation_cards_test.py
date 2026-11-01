#!/usr/bin/env python3
"""Radiation damage-type static-only profile: source families remain independent."""
import copy
import hashlib
import unittest
from pathlib import Path
import alexscaves_1010_action_contract_audit as audit

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
RADIATION = PROVIDER / "EXACT-RADIATION-CONTRACT-1.0.10.json"
EFFECTS = PROVIDER / "EXACT-EFFECT-CONTRACTS-1.0.10.json"
LEDGER = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
CARD = "damage-types/radiation.md"
EFFECT_CARD = "effects/irradiated.md"
CLASS = "com/github/alexmodguy/alexscaves/server/potion/IrradiatedEffect.class"
FACTORY = "com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class"

class RadiationScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.damage = audit.load_manifest(RADIATION)
        cls.effects = audit.load_manifest(EFFECTS)
        cls.ledger = audit.load_manifest(LEDGER)

    def test_one_literal_card_and_separate_effect_certification(self):
        self.assertEqual(set(self.damage["cards"]), {CARD})
        self.assertEqual(set(self.damage["contract_evidence"]), {CARD})
        self.assertEqual(set(self.effects["cards"]), audit.EFFECTS)
        self.assertEqual(set(audit.RADIATION), {CARD})
        self.assertEqual(audit.profile_spec("radiation")[1], audit.RADIATION)
        self.assertEqual("RADIATION_DAMAGE_CONTRACT", self.damage["catalog_family"])
        self.assertEqual("COMPLETE_PERK_READY",
            self.ledger["objects"][PROVIDER.name + "/" + CARD]["status"])
        self.assertEqual("COMPLETE_PERK_READY",
            self.ledger["objects"][PROVIDER.name + "/" + EFFECT_CARD]["status"])

    def test_sealed_card_and_selected_native_anchors(self):
        audit.validate_structure(self.damage, profile="radiation")
        audit.validate_cards(self.damage, PROVIDER, profile="radiation")
        self.assertEqual(hashlib.sha256((PROVIDER / CARD).read_bytes()).hexdigest(),
                         self.damage["cards"][CARD])
        self.assertIn(CLASS, self.damage["contract_evidence"][CARD]["classes"])
        self.assertIn(FACTORY, self.damage["contract_evidence"][CARD]["classes"])
        factory = {(m["name"], m["descriptor"]) for m in self.damage["classes"][FACTORY]["methods"]}
        self.assertIn(("causeRadiationDamage",
            "(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;"), factory)
        tick = {(m["name"], m["descriptor"]) for m in self.damage["classes"][CLASS]["methods"]}
        self.assertIn(("tick", "(Lnet/minecraft/world/entity/LivingEntity;I)V"), tick)
        self.assertIn(("shouldTick", "(II)Z"), tick)

    def test_damage_contract_is_derived_exact_subset_of_existing_effect_evidence(self):
        e = self.effects["effect_evidence"][EFFECT_CARD]
        self.assertEqual(self.damage["contract_evidence"][CARD]["classes"], e["classes"])
        self.assertEqual(self.damage["contract_evidence"][CARD]["resources"], e["resources"])
        for p, value in self.damage["classes"].items():
            self.assertEqual(value, self.effects["classes"][p])
        for p, value in self.damage["resources"].items():
            self.assertEqual(value, self.effects["resources"][p])
        self.assertFalse(self.damage["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", self.damage["mutating_hook"])
        self.assertEqual("NOT_TESTED", self.damage["physical_qa"])

    def test_card_scope_mutation_rejected(self):
        doc = copy.deepcopy(self.damage)
        doc["cards"]["effects/irradiated.md"] = doc["cards"][CARD]
        with self.assertRaises(audit.AuditError):
            audit.validate_structure(doc, profile="radiation")

    def test_producer_class_removal_rejected(self):
        doc = copy.deepcopy(self.damage)
        doc["contract_evidence"][CARD]["classes"].remove(CLASS)
        doc["classes"].pop(CLASS)
        with self.assertRaises(AssertionError):
            self.assertEqual(doc["contract_evidence"][CARD]["classes"],
                             self.effects["effect_evidence"][EFFECT_CARD]["classes"])

    def test_stale_card_sha_rejected(self):
        doc = copy.deepcopy(self.damage)
        doc["cards"][CARD] = "0" * 64
        with self.assertRaises(audit.AuditError):
            audit.validate_cards(doc, PROVIDER, profile="radiation")

    def test_ledger_has_seven_complete_axes_and_no_runtime_claims(self):
        cert = self.ledger["objects"][PROVIDER.name + "/" + CARD]
        self.assertEqual(set(cert["evidence"]),
                         {"identity", "behavior", "parameters", "targeting",
                          "costs", "integration", "validation"})
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", cert["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", cert["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", cert["mutating_hook"])
        self.assertEqual("NOT_TESTED", cert["physical_qa"])
        self.assertTrue(all(x["path"] == str(PROVIDER.relative_to(ROOT) / CARD)
                            and len(x["reason"].strip()) > 20
                            for x in cert["evidence"].values()))

if __name__ == "__main__":
    unittest.main()
