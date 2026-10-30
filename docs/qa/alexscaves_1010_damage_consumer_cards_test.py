#!/usr/bin/env python3
"""Cross-check exact 1.0.10 consumer evidence and scoped cards; no gameplay claim."""
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CARDS = BASE / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAPSHOT = CARDS / "EXACT-CONSUMERS-1.0.10.json"
STATIC_DAMAGE_TYPES = frozenset({"acid", "dark_arrow"})

class DamageConsumerCardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

    def test_exact_eleven_factories(self):
        rows = self.obj["owner"]["factory_methods"]
        self.assertEqual(11, len(rows))
        self.assertEqual(
            set(self.obj["damage_type_resource_ids"]),
            {r["damage_type_fields"][0]["field"].lower() for r in rows}
        )
        for r in rows:
            self.assertTrue(r["descriptor"].endswith(
                "Lnet/minecraft/world/damagesource/DamageSource;"))
            self.assertNotEqual(r["descriptor"], "()V")
            self.assertTrue(r["damage_source_constructor_sites"])

    def test_direct_calls_match_factory_descriptor(self):
        factories = {r["method"]: r["descriptor"]
                     for r in self.obj["owner"]["factory_methods"]}
        callers = self.obj["direct_calling_classes"]
        self.assertEqual(12, len(callers))
        self.assertEqual(len(callers), len({c["class"] for c in callers}))
        for class_record in callers:
            for call in class_record["direct_factory_calls"]:
                self.assertEqual(factories[call["factory_name"]],
                                 call["factory_descriptor"])
                self.assertEqual("invokestatic", call["opcode"])

    def test_every_card_documents_its_factory_and_direct_callers(self):
        by_id = {r["damage_type_fields"][0]["field"].lower(): r
                 for r in self.obj["owner"]["factory_methods"]}
        for id, factory in by_id.items():
            with self.subTest(id=id):
                text = (CARDS / (id.replace("_", "-") + ".md")).read_text(encoding="utf-8")
                self.assertIn(factory["method"], text)
                self.assertIn(factory["descriptor"], text)
                self.assertIn(self.obj["owner"]["sha256"], text)
                for c in self.obj["direct_calling_classes"]:
                    if any(x["factory_name"] == factory["method"]
                           for x in c["direct_factory_calls"]):
                        self.assertIn(c["class"], text)
                for absent in ("NOT_VERIFIED", "NOT_TESTED",
                               "NO_MUTATION"):
                    self.assertIn(absent, text)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if id in STATIC_DAMAGE_TYPES else "NOT_CERTIFIED", text)
        self.assertFalse(self.obj["limits"]["provider_universe_closed"])
        self.assertTrue(self.obj["limits"]["static_only"])

if __name__ == "__main__":
    unittest.main()
