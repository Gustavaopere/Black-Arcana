#!/usr/bin/env python3
"""Keep the public food parameter table and certification within the sealed scope."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
CARD = "systems/foods.md"
AXES = {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"}


class FoodsPublishedContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.discovery = json.loads((PROVIDER / "EXACT-FOODS-DISCOVERY-1.0.10.json").read_text())
        cls.contract = json.loads((PROVIDER / "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json").read_text())
        cls.card = (PROVIDER / CARD).read_text()
        cls.proof = (PROVIDER / "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.md").read_text()
        cls.ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cls.inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        cls.table = {}
        for line in cls.card.splitlines():
            if re.match(r"^\| `[A-Z_]+` \|", line):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if len(cells) != 7:
                    raise AssertionError("Invalid preset row: " + line)
                field = cells[0].strip("`")
                if field in cls.table:
                    raise AssertionError("Duplicated preset: " + field)
                cls.table[field] = cells

    def test_every_preset_has_its_own_parameter_row(self):
        self.assertEqual(set(self.table), {f["field"] for f in self.discovery["fields"]})
        self.assertEqual(len(self.table), 63)
        self.assertEqual(list(self.table), sorted(self.table))
        for f in self.discovery["fields"]:
            with self.subTest(field=f["field"]):
                cells = self.table[f["field"]]
                self.assertEqual(int(cells[1]), f["nutrition"])
                self.assertEqual(float(cells[2]), f["saturation_modifier"])
                self.assertEqual(int(cells[5]), f["write_offset"])

    def test_declared_flags_are_not_lost_or_invented(self):
        for f in self.discovery["fields"]:
            expected = []
            for flag in f["flags"]:
                name = flag["name"]
                if name == "sound":
                    name += ":" + flag["argument"].split("SoundEvents.", 1)[1].split(":", 1)[0]
                expected.append(name)
            actual = self.table[f["field"]][3]
            self.assertEqual(actual, ", ".join(expected) if expected else "—", f["field"])

    def test_each_effect_keeps_its_holder_probability_ticks_and_supplier(self):
        suppliers = self.discovery["suppliers"]
        for f in self.discovery["fields"]:
            expected = []
            for effect in f["effects"]:
                supplier = suppliers[effect["supplier"]]
                field = supplier["field"].rsplit(".", 1)[-1]
                expected.append(f"`{field}` · {effect['probability'] * 100:g}% · {supplier['ticks']} t · `{effect['supplier']}`")
            self.assertEqual(self.table[f["field"]][4], "; ".join(expected) if expected else "—", f["field"])
        self.assertEqual(sum(bool(f["effects"]) for f in self.discovery["fields"]), 45)
        self.assertEqual(sum(len(f["effects"]) for f in self.discovery["fields"]), 46)

    def test_sites_are_a_reference_census_and_not_a_registry_identity(self):
        counts = Counter(s["field"] for methods in self.discovery["consumers"].values()
                         for method in methods for s in method["sites"])
        self.assertEqual(sum(counts.values()), 121)
        self.assertEqual(len(self.discovery["consumers"]), 8)
        for field, count in counts.items():
            self.assertEqual(int(self.table[field][6]), count, field)
        self.assertIn("não constituem prova de IDs de registry", self.card)
        self.assertIn("não a execução aceita do registro ou do consumo", self.card)

    def test_certificate_requires_all_seven_local_evidence_axes(self):
        entry = self.ledger["objects"][PROVIDER.name + "/" + CARD]
        self.assertEqual(entry["status"], "COMPLETE_PERK_READY")
        self.assertEqual(entry["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(entry["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(entry["artifact_sha1"], self.discovery["artifact"]["sha1"])
        self.assertEqual(entry["version"], "1.0.10")
        self.assertEqual(set(entry["evidence"]), AXES)
        self.assertEqual(set(self.contract["axes"]), AXES)
        for axis, evidence in entry["evidence"].items():
            self.assertTrue((ROOT / evidence["path"]).is_file(), axis)
            self.assertTrue(evidence["reason"].strip(), axis)
            self.assertIn("`" + axis + "`", self.proof)

    def test_static_success_does_not_promote_runtime_hooks_or_provider(self):
        entry = self.ledger["objects"][PROVIDER.name + "/" + CARD]
        expected = {"mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
                    "physical_qa": "NOT_TESTED", "runtime_dispatch": "NOT_VERIFIED",
                    "perk_certification": "NOT_CERTIFIED", "provider_universe_closed": False}
        for key, value in expected.items():
            self.assertEqual(entry[key], value, key)
            self.assertEqual(self.contract["claims"][key], value, key)
        self.assertNotIn(PROVIDER.name, self.ledger["providers"])
        self.assertFalse(self.inventory["whole_provider_catalog_closed"])
        for text in (self.card, self.proof):
            for token in ("NOT_VERIFIED", "NOT_TESTED", "NOT_CERTIFIED", "NO_MUTATION", "OPEN"):
                self.assertIn(token, text)

    def test_prefix_is_contiguous_and_does_not_create_magic_roots(self):
        support = self.inventory["integration_support_inventory"]
        roster = self.inventory["remaining_family_inventory"]["item_outer_classes"]
        prefix = support["reviewed_prefix"]
        self.assertEqual([p["class"] for p in prefix], roster[:len(prefix)])
        row = next(p for p in prefix if p["class"] == "server/item/ACFoods")
        self.assertEqual(row["card"], CARD)
        self.assertEqual(row["disposition"], "INDIVIDUAL_STATIC_CONTRACT_CERTIFIED")
        self.assertEqual(row["additional_cards"], 1)
        self.assertEqual(row["semantic_magic_roots_added"], 0)
        self.assertFalse(support["family_universe_closed"])
        self.assertEqual(support["next_alphabetical_uncovered_scope"],
                         roster[len(prefix)] if len(prefix) < len(roster) else None)

    def test_child_index_reports_certification_with_separate_hook_and_qa(self):
        index = (PROVIDER / "systems/INDEX.md").read_text()
        row = next(line for line in index.splitlines() if "[ficha/foods.md](foods.md)" in line)
        self.assertTrue(row.startswith("| ✅ |"))
        self.assertIn("✅ certificado", row)
        self.assertIn("⚠️ não verificado", row)
        self.assertIn("⚠️ não testado", row)
        self.assertIn("universo integral do provider continua não verificado", index)


if __name__ == "__main__":
    unittest.main()
