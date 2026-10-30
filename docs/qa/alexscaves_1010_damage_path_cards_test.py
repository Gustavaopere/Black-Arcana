#!/usr/bin/env python3
"""Cross-check four exact-JAR method anchor groups against existing provider cards."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FOLDER = REPO / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAP = FOLDER / "EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json"
EXPECTED = {
    "ForsakenAttackGoal.class": ("forsaken-sonic-boom.md",),
    "DarkArrowEntity.class": ("dark-arrow.md",),
    "DesolateDaggerEntity.class": ("desolate-dagger.md",),
    "NuclearExplosionEntity.class": ("nuke.md", "intentional-game-design.md"),
}
STATIC_CONTRACTS = {
    "dark-arrow.md": ("## 4. Impacto, fórmula e filtros causais",
                      "EXACT-DREADBOW-CONTRACTS-1.0.10.json"),
    "desolate-dagger.md": ("## 4. Ataque, dano solicitado e Sated Blade",
                           "EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json"),
}

class DamagePathCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads(SNAP.read_text(encoding="utf-8"))

    def test_scope_keeps_qa_and_mutation_unverified(self):
        doc = self.e
        self.assertEqual(doc["scope"],
                         "SHA_EXACT_1010_SELECTED_DAMAGE_CALLSITE_INSTRUCTION_WINDOWS_ONLY")
        self.assertTrue(doc["limits"]["not_entire_provider"])
        self.assertFalse(doc["limits"]["complete_perk_ready"])
        self.assertFalse(doc["limits"]["provider_universe_closed"])
        self.assertEqual(doc["limits"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(doc["limits"]["physical_qa"], "NOT_TESTED")

    def test_all_four_classes_and_six_factory_windows(self):
        classes = self.e["selected_classes"]
        self.assertEqual(len(classes), 4)
        self.assertEqual(
            {x["class_path"].split("/")[-1] for x in classes},
            set(EXPECTED),
        )
        self.assertEqual(sum(len(m["factory_windows"])
                             for x in classes for m in x["methods"]), 6)

    def test_each_card_mentions_exact_bytecode_identity(self):
        for cls in self.e["selected_classes"]:
            suffix = cls["class_path"].split("/")[-1]
            for name in EXPECTED[suffix]:
                with self.subTest(cls=suffix, card=name):
                    card = (FOLDER / name).read_text(encoding="utf-8")
                    self.assertIn(cls["class_sha256"], card)
                    self.assertIn(cls["class_path"], card)
                    if name in STATIC_CONTRACTS:
                        heading, manifest = STATIC_CONTRACTS[name]
                        self.assertIn(heading, card)
                        self.assertIn(manifest, card)
                    else:
                        self.assertIn("## Aprofundamento de fluxo — 1.0.10", card)
                    for method in cls["methods"]:
                        self.assertIn(method["method_descriptor"], card)
                        for window in method["factory_windows"]:
                            self.assertIn(window["factory_name"], card)
                            self.assertIn(str(window["invocation_offset"]), card)
                    for token in ("NOT_VERIFIED", "NOT_TESTED"):
                        self.assertIn(token, card)
                    self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY" if name in STATIC_CONTRACTS else "NOT_CERTIFIED", card)

    def test_no_full_flow_claim(self):
        self.assertEqual(self.e["limits"]["control_flow_reachability"], "NOT_PROVEN")
        for cls in self.e["selected_classes"]:
            for method in cls["methods"]:
                self.assertEqual(method["method_semantics"], "NOT_PROVEN_FROM_ANCHORS")
                self.assertEqual(len(method["full_method_parsed_sha256"]), 64)
                self.assertTrue(method["branch_opcode_anchors"])

if __name__ == "__main__":
    unittest.main()
