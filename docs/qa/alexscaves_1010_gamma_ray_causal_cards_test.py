#!/usr/bin/env python3
"""Gamma Ray native gates and live catalog accounting, without gameplay claims."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
ITEM = "com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
LEGACY = {
    "EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json": "9a8ea7a6287598b317b016d3002bee474faa513ffbe537464d0d6db9683af0f8",
    "EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json": "fa135a619a12d3a615d11a5a604ab9c796f7247f3bb4e48df1e4e5adee17728e",
    "EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json": "a499370fe6bea484e7ac1d0d2afcf74a170495c913c151f73239253067f82a68",
}


class GammaRayStaticCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / "EXACT-GAMMA-RAY-CAUSAL-1.0.10.json").read_text())
        cls.card = (PROVIDER / "enchantments/gamma-ray.md").read_text()
        cls.proof = (PROVIDER / "EXACT-GAMMA-RAY-CAUSAL-1.0.10.md").read_text()

    def pivots(self):
        rows = [r for r in self.seal["pivots"] if r["owner"] == ITEM and r["name"] == "onUseTick"]
        self.assertTrue(rows)
        offsets = [r["offset"] for r in rows]
        self.assertEqual(len(offsets), len(set(offsets)))
        return {r["offset"]: r for r in rows}

    def assert_row(self, rows, offset, opcode=None, token=None):
        self.assertIn(offset, rows)
        r = rows[offset]
        if opcode is not None:
            self.assertEqual(r["opcode"], opcode, offset)
        if token is not None:
            self.assertIn(token, r["operand"] + " " + r["symbol"], offset)

    def test_exact_publisher_and_previous_partial_scopes_are_preserved(self):
        self.assertEqual(self.seal["version"], "1.0.10")
        self.assertEqual(self.seal["enchantment"], "alexscaves:gamma_ray")
        self.assertEqual(self.seal["artifact"], {
            "sha1": "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570",
            "sha256": "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
            "size_bytes": 75279314,
        })
        self.assertEqual(self.seal["class_sha256"][ITEM],
                         "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c")
        for name, digest in LEGACY.items():
            self.assertEqual(hashlib.sha256((PROVIDER / name).read_bytes()).hexdigest(), digest)

    def test_declarative_limits_and_reverse_exclusion_are_not_invented(self):
        e = self.seal["resource_json"]
        self.assertEqual(e["description"]["translate"], "enchantment.alexscaves.gamma_ray")
        self.assertEqual(e["supported_items"], "#alexscaves:enchantable/raygun")
        self.assertEqual(e["max_level"], 1)
        self.assertEqual(e["weight"], 2)
        self.assertEqual(e["anvil_cost"], 4)
        self.assertEqual(e["min_cost"], {"base": 1, "per_level_above_first": 18})
        self.assertEqual(e["max_cost"], {"base": 41, "per_level_above_first": 10})
        self.assertEqual(e["slots"], ["mainhand"])
        self.assertNotIn("exclusive_set", e)
        self.assertEqual(self.seal["x_ray_resource_json"]["exclusive_set"], ["alexscaves:gamma_ray"])
        self.assertEqual(self.seal["supported_item_tag"]["values"], ["alexscaves:raygun"])

    def test_full_on_use_tick_body_is_not_an_isolated_slot_reference(self):
        methods = self.seal["census"]["method_census"]
        found = [m for m in methods if m["owner"] == ITEM and m["name"] == "onUseTick"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["instructions"], 523)
        self.assertEqual(found[0]["body_sha256"],
                         "b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5")
        self.assertEqual(found[0]["direct_branches"], 57)
        p = self.pivots()
        for offset, opcode, token in ((332, "getstatic", "GAMMA_RAY"),
                                      (335, "invokestatic", "enchantLevel"),
                                      (338, "ifle", "345"), (341, "iconst_1", ""),
                                      (342, "goto", "346"), (345, "iconst_0", ""),
                                      (346, "istore", "18")):
            self.assert_row(p, offset, opcode, token)
        for offset in (367, 402, 922, 1029, 1138):
            self.assert_row(p, offset, "iload", "18")

    def test_server_damage_cadence_has_no_additional_fifteen_tick_warmup(self):
        p = self.pivots()
        for offset, opcode, token in ((875, "invokevirtual", "isClientSide"),
                                      (878, "ifne", "1160"),
                                      (881, "iload", "5"), (883, "iload", "6"),
                                      (885, "isub", ""), (886, "iconst_3", ""),
                                      (887, "irem", ""), (888, "ifne", "1160")):
            self.assert_row(p, offset, opcode, token)
        # This is an opportunity under Java's zero-remainder predicate, not
        # proof that a given elapsed callback, hit or accepted damage occurs.
        self.assertEqual([n for n in range(16) if (n - 15) % 3 == 0],
                         [0, 3, 6, 9, 12, 15])
        self.assertIn("(elapsed", self.card)

    def test_damage_request_and_amplifier_are_boolean_variants(self):
        p = self.pivots()
        for offset, opcode, token in ((924, "ifeq", "931"),
                                      (927, "iconst_4", ""), (928, "goto", "932"),
                                      (931, "iconst_0", ""), (932, "istore", "23"),
                                      (1031, "ifeq", "1038"),
                                      (1034, "fconst_2", ""), (1035, "goto", "1041"),
                                      (1038, "ldc_w", "float 1.5f"),
                                      (1041, "invokestatic", "ACCompat.hurt")):
            self.assert_row(p, offset, opcode, token)

    def test_tremorzilla_is_an_explicit_exception_to_accepted_hurt(self):
        p = self.pivots()
        for offset, opcode, token in ((1013, "instanceof", "TremorzillaEntity"),
                                      (1016, "ifne", "1047"),
                                      (1044, "ifeq", "1051"),
                                      (1047, "iconst_1", ""), (1048, "goto", "1052"),
                                      (1051, "iconst_0", ""), (1052, "istore", "26"),
                                      (1054, "iload", "26"), (1056, "ifeq", "1157")):
            self.assert_row(p, offset, opcode, token)

    def test_resistance_effect_acceptance_and_visual_delivery_are_distinct(self):
        p = self.pivots()
        for offset, opcode, token in ((1082, "getstatic", "RESISTS_RADIATION"),
                                      (1085, "invokevirtual", "Holder$Reference.is"),
                                      (1088, "ifne", "1157"),
                                      (1111, "sipush", "800"),
                                      (1114, "iload", "23"),
                                      (1116, "invokespecial", "MobEffectInstance"),
                                      (1119, "invokevirtual", "LivingEntity.addEffect"),
                                      (1122, "ifeq", "1157"),
                                      (1140, "ifeq", "1147"),
                                      (1143, "iconst_4", ""), (1144, "goto", "1148"),
                                      (1147, "iconst_0", ""), (1148, "sipush", "800"),
                                      (1151, "invokespecial", "UpdateEffectVisualityEntityMessage"),
                                      (1154, "invokestatic", "sendMSGToAll")):
            self.assert_row(p, offset, opcode, token)

    def test_target_volume_and_filters_do_not_become_gamma_range_bonus(self):
        p = self.pivots()
        for offset, opcode, token in ((891, "new", "AABB"), (895, "aload", "14"),
                                      (897, "ldc2_w", "double -1.0d"),
                                      (906, "invokevirtual", "Vec3.add"),
                                      (909, "aload", "14"), (911, "dconst_1", ""),
                                      (914, "invokevirtual", "Vec3.add"),
                                      (917, "invokespecial", "AABB"),
                                      (943, "invokevirtual", "Level.getEntities"),
                                      (978, "invokevirtual", "Entity.is:"),
                                      (981, "ifne", "1157"),
                                      (987, "invokevirtual", "isAlliedTo"),
                                      (990, "ifne", "1157"),
                                      (996, "invokevirtual", "isAlliedTo"),
                                      (999, "ifne", "1157"),
                                      (1005, "invokevirtual", "isPassengerOfSameVehicle"),
                                      (1008, "ifne", "1157")):
            self.assert_row(p, offset, opcode, token)

    def test_direct_damage_authorship_does_not_certify_periodic_credit(self):
        p = self.pivots()
        self.assert_row(p, 1025, "aload_2")
        self.assert_row(p, 1026, "invokestatic", "causeRaygunDamage")
        for text in (self.card, self.proof):
            self.assertIn("Irradiated", text)
            self.assertIn("Mastery", text)
            self.assertIn("effects/irradiated.md", text)

    def test_static_seven_axes_do_not_promote_hooks_network_or_physical_qa(self):
        self.assertEqual(self.seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(self.seal["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        for key, value in (("mutating_hook", "NOT_VERIFIED"), ("physical_qa", "NOT_TESTED"),
                           ("mutation", "NO_MUTATION"), ("provider_universe_closed", False)):
            self.assertEqual(self.seal["safety"][key], value)
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert = ledger["objects"][PROVIDER.name + "/enchantments/gamma-ray.md"]
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(cert["evidence"]), {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"})
        for evidence in cert["evidence"].values():
            self.assertTrue((ROOT / evidence["path"]).is_file())
            self.assertTrue(evidence["reason"].strip())

    def test_card_and_proof_keep_prior_scopes_and_pending_execution_separate(self):
        for text in (self.card, self.proof):
            for token in ("EXACT-GAMMA-RAY-CAUSAL-1.0.10.json", "EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json",
                          "STATIC_TECHNICAL_CATALOG_ONLY", "NOT_VERIFIED", "NOT_TESTED", "NO_MUTATION", "1.1.1"):
                self.assertIn(token, text)
        self.assertIn("gamma_ray_causal_audit.py", self.proof)

    def test_enchantment_inventory_matches_current_ledger(self):
        inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        prefix = PROVIDER.name + "/enchantments/"
        cards = sorted(key.removeprefix(PROVIDER.name + "/") for key, cert in ledger["objects"].items()
                       if key.startswith(prefix) and cert["status"] == "COMPLETE_PERK_READY")
        family = inventory["family_catalog_status"]["enchantments"]
        self.assertEqual(family["cards"], cards)
        self.assertEqual(family["documented_static_contracts"], len(cards))
        observed = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        partial = observed - {Path(path).stem.replace("-", "_") for path in cards}
        self.assertEqual(family["partial_dossiers"], len(partial))
        existing = [p for p in (PROVIDER / "enchantments").glob("*.md") if p.name not in {"INDEX.md", "README.md"}]
        self.assertEqual(family["individual_dossiers"], len(existing))
        self.assertEqual(len(existing), len(observed))
        self.assertFalse(inventory["whole_provider_catalog_closed"])

    def test_crosswalk_counts_and_next_partial_are_derived_dynamically(self):
        inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        prefix = PROVIDER.name + "/enchantments/"
        cert_ids = {Path(key).stem.replace("-", "_") for key, cert in ledger["objects"].items()
                    if key.startswith(prefix) and cert["status"] == "COMPLETE_PERK_READY"}
        observed = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        remaining = sorted(observed - cert_ids)
        text = (PROVIDER / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        pairs = dict(re.findall(r"^(individual_[a-z_]+)=(\d+/\d+)$", text, re.M))
        self.assertEqual(pairs["individual_full_enchantment_dossiers"], f"{len(cert_ids)}/{len(observed)}")
        self.assertEqual(pairs["individual_partial_enchantment_dossiers"], f"{len(remaining)}/{len(observed)}")
        self.assertEqual(pairs["individual_existing_enchantment_dossiers"], f"{len(observed)}/{len(observed)}")
        if remaining:
            queue = text.split("O próximo trabalho", 1)[1].split("A fila global", 1)[0]
            self.assertIn("`alexscaves:" + remaining[0] + "`", queue)
        row = next(line for line in text.splitlines() if "| `alexscaves:gamma_ray` |" in line)
        self.assertTrue(row.startswith("| ✅ |"))


if __name__ == "__main__":
    unittest.main()
