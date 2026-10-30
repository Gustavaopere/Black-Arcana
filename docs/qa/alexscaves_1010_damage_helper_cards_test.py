#!/usr/bin/env python3
"""Regression of five documented selected helper APIs against sealed JAR evidence."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
MANIFEST = FOLDER / "EXACT-DAMAGE-HELPERS-1.0.10.json"
CARDS = {
    "getSonicDamageAgainst": "forsaken-sonic-boom.md",
    "getShadowArrowDamage": "dark-arrow.md",
    "isPerfectShot": "dark-arrow.md",
    "hurt": "desolate-dagger.md",
    "enchantLevel": "desolate-dagger.md",
}
STATIC_CARDS = frozenset({"dark-arrow.md", "desolate-dagger.md"})

class HelperCardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.methods = {
            m["name"]: (c, m)
            for c in cls.obj["classes"]
            for m in c["methods"]
        }

    def test_exact_scoped_population(self):
        self.assertEqual(len(self.obj["classes"]), 3)
        self.assertEqual(set(self.methods), set(CARDS))
        self.assertEqual(self.obj["scope"],
                         "EXACT_ALEXSCAVES_1010_SELECTED_DAMAGE_HELPER_ABI_ONLY")
        self.assertFalse(self.obj["limitations"]["complete_perk_ready"])
        self.assertFalse(self.obj["limitations"]["provider_universe_closed"])
        self.assertEqual(self.obj["limitations"]["mutating_hook"], "NOT_VERIFIED")

    def test_sonic_tag_and_both_return_constants(self):
        _, method = self.methods["getSonicDamageAgainst"]
        literals = [x["symbol"] for x in method["numeric_constants"]]
        self.assertIn("float 45.0f", literals)
        self.assertIn("float 4.0f", literals)
        self.assertTrue(any("WEAK_TO_FORSAKEN_SONIC_ATTACK" in x["symbol"]
                            for x in method["invoked_methods_and_fields"]))

    def test_wrapper_delegation_not_new_settlement(self):
        _, method = self.methods["hurt"]
        self.assertEqual(len(method["invoked_methods_and_fields"]), 1)
        self.assertIn("Entity.hurt:", method["invoked_methods_and_fields"][0]["symbol"])
        self.assertEqual(len(method["branch_opcodes"]), 0)

    def test_enchantment_level_and_zero_fallback(self):
        _, method = self.methods["enchantLevel"]
        symbols = "\n".join(x["symbol"] for x in method["invoked_methods_and_fields"])
        self.assertIn("ItemStack.getEnchantments", symbols)
        self.assertIn("Holder.is", symbols)
        self.assertIn("getIntValue", symbols)
        self.assertTrue(any(x["opcode"] == "iconst_0" for x in method["numeric_constants"]))

    def test_arrow_getters_are_synced_accessors(self):
        for name, field in (("getShadowArrowDamage", "SHADOW_ARROW_DAMAGE"),
                            ("isPerfectShot", "PERFECT_SHOT")):
            _, method = self.methods[name]
            self.assertTrue(any(field in x["symbol"]
                                for x in method["invoked_methods_and_fields"]))
            self.assertTrue(any("SynchedEntityData.get" in x["symbol"]
                                for x in method["invoked_methods_and_fields"]))

    def test_docs_have_exact_signatures_and_unverified_contracts(self):
        for name, path in CARDS.items():
            cls, m = self.methods[name]
            with self.subTest(name=name):
                card = (FOLDER / path).read_text(encoding="utf8")
                self.assertIn(m["descriptor"], card)
                self.assertIn(m["parsed_method_sha256"], card)
                self.assertIn(cls["class_sha256"], card)
                for token in ("NOT_VERIFIED", "NOT_TESTED",
                              "NO_MUTATION"):
                    self.assertIn(token, card)
                self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if path in STATIC_CARDS else "NOT_CERTIFIED", card)

if __name__ == "__main__":
    unittest.main()
