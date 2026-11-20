#!/usr/bin/env python3
"""Guard the public registry crosswalk and its bounded static certificate."""
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
CARD = "systems/item-registry.md"
TARGET = "com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
AXES = {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"}


def table_rows(text, first_cell_pattern):
    result = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5 or not re.fullmatch(first_cell_pattern, cells[0]):
            continue
        first = cells[0].strip("`")
        if first in result:
            raise AssertionError("Duplicated table identity: " + first)
        result[first] = cells
    return result


class ItemRegistryPublishedContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json").read_text())
        cls.native = cls.seal["native"]
        cls.card = (PROVIDER / CARD).read_text()
        cls.proof = (PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.md").read_text()
        cls.ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cls.inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        cls.bindings = table_rows(cls.card, r"`[A-Z0-9_]+`")
        cls.eggs = table_rows(cls.card, r"`alexscaves:spawn_egg_[a-z_]+`")

    def test_every_named_binding_is_individualized_in_alphabetical_order(self):
        self.assertEqual(set(self.bindings), {entry["field"] for entry in self.native["bindings"]})
        self.assertEqual(len(self.bindings), 188)
        self.assertEqual(list(self.bindings), sorted(self.bindings))

    def test_binding_ids_and_full_factory_handles_match_native_arguments(self):
        for entry in self.native["bindings"]:
            with self.subTest(field=entry["field"]):
                cells = self.bindings[entry["field"]]
                factory = entry["factory"]
                self.assertEqual(cells[1].strip("`"), entry["resource_location"])
                self.assertEqual(cells[2].strip("`"),
                                 factory["owner"] + "." + factory["name"] + ":" + factory["descriptor"])
                self.assertTrue(cells[3].strip("`— "), "construction identity must be stated")
                self.assertEqual(cells[4].strip("`"), factory["code_sha256"])
                self.assertEqual(factory["reference_kind"], 6)

    def test_each_extra_spawn_egg_has_its_own_alphabetical_row(self):
        self.assertEqual(set(self.eggs), {entry["resource_location"] for entry in self.native["spawn_egg_registrations"]})
        self.assertEqual(len(self.eggs), 43)
        self.assertEqual(list(self.eggs), sorted(self.eggs))

    def test_egg_entity_colors_group_and_call_offsets_remain_distinct(self):
        for entry in self.native["spawn_egg_registrations"]:
            with self.subTest(egg=entry["resource_location"]):
                cells = self.eggs[entry["resource_location"]]
                supplier, group = entry["entity_supplier"], entry["creative_tab"]
                self.assertEqual(cells[1].strip("`"),
                                 supplier["owner"] + "." + supplier["name"] + ":" + supplier["descriptor"])
                self.assertEqual([int(value.strip("` ")) for value in cells[2].split("/")],
                                 [entry["primary_color"], entry["secondary_color"]])
                self.assertEqual(cells[3].strip("`"), group["owner"] + "." + group["name"] + ":" + group["descriptor"])
                self.assertEqual(int(cells[4]), entry["call_offset"])
                self.assertEqual(entry["path"], "spawn_egg_" + entry["base_name"])

    def test_static_request_count_does_not_stop_at_supplier_field_count(self):
        ids = [entry["resource_location"] for entry in self.native["bindings"] + self.native["spawn_egg_registrations"]]
        self.assertEqual(len(ids), 231)
        self.assertEqual(len(set(ids)), 231)
        self.assertEqual(self.native["counts"]["literal_registration_requests"], 231)
        self.assertEqual(self.native["counts"]["registry_fields"], 200)
        self.assertEqual(self.seal["claims"]["semantic_magic_roots_delta"], 0)

    def test_callback_cost_and_spawn_acceptance_are_not_conflated(self):
        callback = self.native["local_callback_contracts"][TARGET + "$7"]
        self.assertEqual(callback["stack_cost_request"], 1)
        self.assertEqual(callback["ordered_requests"], ["addFreshEntity", "playSound", "gameEvent", "shrink"])
        self.assertEqual(callback["add_fresh_entity_result"], "DISCARDED_BOOLEAN")
        self.assertEqual(callback["cost_guard"], "NONE_IF_PRIOR_CALLS_RETURN_NORMALLY")
        self.assertIn("shrink(1)", self.card)
        self.assertIn("booleano", self.card)
        self.assertTrue("continuação normal" in self.card,
                        "The exception versus normal-return boundary must be explicit")
        self.assertIn("pipeline", self.proof)

    def test_player_factories_and_dispenser_factories_are_separate_boundaries(self):
        callbacks = self.native["local_callback_contracts"]
        self.assertEqual(len(callbacks), 13)
        for index in range(1, 7):
            callback = callbacks[TARGET + "$" + str(index)]
            self.assertEqual(callback["constructor_arguments"], ["level", "position.x", "position.y", "position.z"])
            self.assertFalse(callback["spawn_request"])
            self.assertIsNone(callback["stack_cost_request"])
        players = [callback for name, callback in callbacks.items() if name.startswith(TARGET + ".lambda$")]
        self.assertEqual(len(players), 6)
        self.assertTrue(all(callback["constructor_arguments"] == ["player.level()", "player"] for callback in players))
        self.assertIn("Player", self.card)

    def test_certificate_requires_seven_local_evidence_axes(self):
        entry = self.ledger["objects"][PROVIDER.name + "/" + CARD]
        self.assertEqual(entry["status"], "COMPLETE_PERK_READY")
        self.assertEqual(entry["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(entry["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(entry["artifact_sha1"], self.seal["artifact"]["sha1"])
        self.assertEqual(entry["version"], "1.0.10")
        self.assertEqual(set(entry["evidence"]), AXES)
        self.assertEqual(set(self.seal["axes"]), AXES)
        for axis, evidence in entry["evidence"].items():
            self.assertTrue((ROOT / evidence["path"]).is_file(), axis)
            self.assertTrue(evidence["reason"].strip(), axis)
            self.assertIn("`" + axis + "`", self.proof)

    def test_documentation_success_does_not_promote_hooks_runtime_or_universe(self):
        entry = self.ledger["objects"][PROVIDER.name + "/" + CARD]
        for name, value in {"mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
                            "physical_qa": "NOT_TESTED", "runtime_dispatch": "NOT_VERIFIED",
                            "perk_certification": "NOT_CERTIFIED", "provider_universe_closed": False}.items():
            self.assertEqual(entry[name], value, name)
            self.assertEqual(self.seal["claims"][name], value, name)
        self.assertNotIn(PROVIDER.name, self.ledger["providers"])
        self.assertFalse(self.inventory["whole_provider_catalog_closed"])
        for text in (self.card, self.proof):
            for token in ("NOT_VERIFIED", "NOT_TESTED", "NOT_CERTIFIED", "NO_MUTATION", "OPEN"):
                self.assertIn(token, text)
            self.assertNotIn("@@", text, "unfinished documentary placeholder")

    def test_alphabetical_prefix_stays_contiguous_with_zero_new_roots(self):
        support = self.inventory["integration_support_inventory"]
        roster = self.inventory["remaining_family_inventory"]["item_outer_classes"]
        prefix = support["reviewed_prefix"]
        self.assertEqual([row["class"] for row in prefix], roster[:len(prefix)])
        row = next(row for row in prefix if row["class"] == "server/item/ACItemRegistry")
        self.assertEqual(row["card"], CARD)
        self.assertEqual(row["disposition"], "INDIVIDUAL_STATIC_CONTRACT_CERTIFIED")
        self.assertEqual(row["additional_cards"], 1)
        self.assertEqual(row["semantic_magic_roots_added"], 0)
        self.assertFalse(support["family_universe_closed"])
        self.assertEqual(support["next_alphabetical_uncovered_scope"],
                         roster[len(prefix)] if len(prefix) < len(roster) else None)

    def test_index_keeps_certification_hooks_and_qa_separate(self):
        index = (PROVIDER / "systems/INDEX.md").read_text()
        row = next(line for line in index.splitlines() if "[ficha/item-registry.md](item-registry.md)" in line)
        self.assertTrue(row.startswith("| ✅ |"))
        self.assertIn("✅ certificado", row)
        self.assertIn("⚠️ não verificado", row)
        self.assertIn("⚠️ não testado", row)
        self.assertIn("universo integral do provider continua não verificado", index)


if __name__ == "__main__":
    unittest.main()
