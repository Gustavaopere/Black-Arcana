#!/usr/bin/env python3
"""Flinging static semantics and live catalog accounting regressions.

These checks protect distinct native gates, volume construction, ignored
settlement results and documentary scope. They do not execute Minecraft.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
ITEM = "com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class"
LEGACY_DIGEST = "bfd013357139a53a42408905470a152e8d82d67aec7c081f946dec1e1d48209b"


class FlingingStaticCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / "EXACT-FLINGING-CAUSAL-1.0.10.json").read_text())
        cls.legacy_bytes = (PROVIDER / "EXACT-FLINGING-1.0.10.json").read_bytes()
        cls.legacy = json.loads(cls.legacy_bytes)
        cls.card = (PROVIDER / "enchantments/flinging.md").read_text()
        cls.proof = (PROVIDER / "EXACT-FLINGING-CAUSAL-1.0.10.md").read_text()

    def pivots(self, name="releaseUsing", owner=ITEM):
        rows = [r for r in self.seal["pivots"] if r["owner"] == owner and r["name"] == name]
        self.assertTrue(rows, (owner, name))
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

    def test_publisher_and_historical_evidence_are_not_relabelled(self):
        self.assertEqual(hashlib.sha256(self.legacy_bytes).hexdigest(), LEGACY_DIGEST)
        self.assertEqual(self.legacy["enchantment"]["id"], "alexscaves:flinging")
        self.assertEqual(self.seal["artifact"], self.legacy["artifact"])
        self.assertEqual(self.seal["artifact"]["sha1"], "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570")
        self.assertEqual(self.seal["version"], "1.0.10")
        self.assertEqual(self.seal["enchantment"], "alexscaves:flinging")
        self.assertEqual(self.seal["class_sha256"][ITEM], self.legacy["class_sha256"][ITEM])

    def test_declarative_costs_do_not_become_cast_costs(self):
        e = self.seal["resource_json"]
        self.assertEqual(e, self.legacy["enchantment"]["json"])
        self.assertEqual(e["max_level"], 3)
        self.assertEqual(e["weight"], 10)
        self.assertEqual(e["anvil_cost"], 1)
        self.assertEqual(e["min_cost"], {"base": 1, "per_level_above_first": 8})
        self.assertEqual(e["max_cost"], {"base": 41, "per_level_above_first": 10})
        self.assertEqual(e["slots"], ["mainhand"])
        self.assertNotIn("exclusive_set", e)
        self.assertEqual(self.seal["supported_item_tag"]["values"], ["alexscaves:ortholance"])

    def test_full_census_and_damage_callback_remain_explicit(self):
        methods = self.seal["method_census"]
        identities = {(m["owner"], m["name"], m["descriptor"]) for m in methods}
        self.assertEqual(len(identities), len(methods))
        self.assertEqual(self.seal["methods_checked"], len(methods))
        self.assertEqual(self.seal["instructions_checked"], sum(m["instructions"] for m in methods))
        self.assertEqual(self.seal["direct_branches_checked"], sum(m["direct_branches"] for m in methods))
        for owner in (ITEM, ITEM.replace("server/item/OrtholanceItem.class", "server/entity/item/WaveEntity.class")):
            selected = [m for m in methods if m["owner"] == owner]
            self.assertEqual(len(selected), self.seal["owner_method_populations"][owner])
        for m in methods:
            self.assertEqual(m["direct_branches"], len(m["branch_edges"]))
            self.assertEqual(m["exception_table"], [])
            self.assertEqual(m["switch_offsets"], [])
        binding = next(b for b in self.seal["bootstrap_bindings"] if b["callback"] == "lambda$attackDamageBonus$2")
        self.assertEqual(binding["index"], 2)
        self.assertRegex(binding["section_sha256"], r"^[0-9a-f]{64}$")

    def test_zero_charge_returns_before_movement_and_server_settlement(self):
        p = self.pivots()
        for offset, opcode, token in ((3, "invokevirtual", "getUseDuration"),
                                      (8, "isub", ""), (10, "bipush", "60"),
                                      (12, "invokestatic", "Mth.clamp"),
                                      (18, "getstatic", "FLINGING"),
                                      (21, "invokestatic", "enchantLevel"),
                                      (45, "ifle", "869")):
            self.assert_row(p, offset, opcode, token)
        methods = [m for m in self.seal["method_census"] if m["owner"] == ITEM and m["name"] == "releaseUsing"]
        self.assertEqual(len(methods), 1)
        self.assertEqual(methods[0]["instructions"], 435)
        self.assertEqual(methods[0]["body_sha256"], "00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae")

    def test_short_charge_and_client_paths_still_reach_motion(self):
        p = self.pivots()
        self.assert_row(p, 99, "if_icmplt", "836")
        self.assert_row(p, 103, "invokevirtual", "isClientSide")
        self.assert_row(p, 106, "ifne", "836")
        self.assert_row(p, 135, "invokestatic", "hurtAndBreakUsedHand")
        self.assert_row(p, 866, "invokevirtual", "setDeltaMovement")

    def test_flinging_motion_preserves_prior_velocity_and_vertical_separation(self):
        p = self.pivots()
        for offset, token in ((48, "float 0.1f"), (57, "float 0.1f"),
                              (64, "getDeltaMovement"), (69, "getViewVector"),
                              (72, "normalize"), (80, "float 0.15f"),
                              (87, "Vec3.multiply"), (90, "Vec3.add"),
                              (841, "onGround"), (847, "float 0.2f"),
                              (857, "float 0.1f"), (863, "Vec3.add")):
            self.assert_row(p, offset, token=token)
        self.assert_row(p, 93, "astore", "9")
        self.assert_row(p, 844, "ifeq", "853")
        self.assert_row(p, 854, "iload", "6")

    def test_attack_box_uses_pre_lift_vector_and_charge_dependent_multiplier(self):
        p = self.pivots()
        for offset, opcode, token in ((138, "iload", "5"), (140, "iconst_5", ""),
                                      (141, "idiv", ""), (142, "istore", "10"),
                                      (149, "iconst_5", ""), (150, "istore", "10"),
                                      (705, "new", "AABB"),
                                      (710, "invokevirtual", "position"),
                                      (714, "invokevirtual", "position"),
                                      (717, "aload", "9"), (719, "iload", "10"),
                                      (721, "i2d", ""),
                                      (722, "invokevirtual", "Vec3.scale"),
                                      (725, "invokevirtual", "Vec3.add"),
                                      (728, "invokespecial", "AABB"),
                                      (731, "dconst_1", ""),
                                      (732, "invokevirtual", "AABB.inflate")):
            self.assert_row(p, offset, opcode, token)

    def test_tsunami_bypasses_normal_and_second_wave_emissions(self):
        p = self.pivots()
        self.assert_row(p, 146, "ifeq", "247")
        self.assert_row(p, 240, "invokevirtual", "addFreshEntity")
        self.assert_row(p, 243, "pop")
        self.assert_row(p, 244, "goto", "705")
        self.assert_row(p, 460, "getstatic", "SECOND_WAVE")
        self.assert_row(p, 466, "ifle", "705")
        for offset, opcode, token in ((469, "iconst_1", ""),
                                      (470, "iload", "10"),
                                      (472, "iconst_1", ""),
                                      (473, "isub", ""),
                                      (474, "invokestatic", "Math.max"),
                                      (477, "istore", "11"),
                                      (484, "iload", "11"),
                                      (486, "if_icmpge", "705")):
            self.assert_row(p, offset, opcode, token)
        for call, ignored in ((610, 613), (695, 698)):
            self.assert_row(p, call, "invokevirtual", "addFreshEntity")
            self.assert_row(p, ignored, "pop")

    def test_direct_damage_and_dismount_do_not_share_acceptance_receipt(self):
        p = self.pivots()
        for offset, token in ((742, "mobAttack"), (748, "attackDamageBonus"),
                              (758, "getEntitiesOfClass"), (793, "isAlliedTo"),
                              (802, "equals"), (811, "hasLineOfSight"),
                              (824, "LivingEntity.hurt"), (830, "stopRiding")):
            self.assert_row(p, offset, token=token)
        self.assert_row(p, 796, "ifne", "833")
        self.assert_row(p, 805, "ifne", "833")
        self.assert_row(p, 814, "ifeq", "833")
        self.assert_row(p, 827, "pop")

    def test_static_certificate_keeps_hooks_and_physical_qa_unapproved(self):
        self.assertEqual(self.seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(self.seal["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        for key, value in (("mutating_hook", "NOT_VERIFIED"),
                           ("physical_qa", "NOT_TESTED"),
                           ("mutation", "NO_MUTATION"),
                           ("provider_universe_closed", False)):
            self.assertEqual(self.seal["safety"][key], value)
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cert = ledger["objects"][PROVIDER.name + "/enchantments/flinging.md"]
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"], "NOT_TESTED")
        self.assertEqual(set(cert["evidence"]), {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"})
        for axis in cert["evidence"].values():
            self.assertTrue((ROOT / axis["path"]).is_file())
            self.assertTrue(axis["reason"].strip())

    def test_card_and_proof_link_both_historical_and_causal_evidence(self):
        for text in (self.card, self.proof):
            self.assertIn("EXACT-FLINGING-1.0.10.json", text)
            self.assertIn("EXACT-FLINGING-CAUSAL-1.0.10.json", text)
            self.assertIn("NOT_VERIFIED", text)
            self.assertIn("NOT_TESTED", text)
            self.assertIn("NO_MUTATION", text)
            self.assertIn("1.1.1", text)
        self.assertIn("STATIC_TECHNICAL_CATALOG_ONLY", self.card)
        self.assertIn("flinging_causal_audit.py", self.proof)

    def test_enchantment_inventory_matches_current_ledger(self):
        inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        prefix = PROVIDER.name + "/enchantments/"
        cards = sorted(key.removeprefix(PROVIDER.name + "/")
                       for key, cert in ledger["objects"].items()
                       if key.startswith(prefix) and cert["status"] == "COMPLETE_PERK_READY")
        family = inventory["family_catalog_status"]["enchantments"]
        self.assertEqual(family["cards"], cards)
        self.assertEqual(family["documented_static_contracts"], len(cards))
        observed = inventory["remaining_family_inventory"]["enchantment_ids"]
        certified_ids = {Path(path).stem.replace("-", "_") for path in cards}
        partial = sorted(set(observed) - certified_ids)
        existing = list((PROVIDER / "enchantments").glob("*.md"))
        existing = [p for p in existing if p.name not in {"INDEX.md", "README.md"}]
        self.assertEqual(family["individual_dossiers"], len(existing))
        self.assertEqual(family["partial_dossiers"], len(partial))
        self.assertEqual(len(existing), len(observed))
        self.assertFalse(inventory["whole_provider_catalog_closed"])

    def test_crosswalk_counts_and_next_partial_are_derived_from_certificates(self):
        inventory = json.loads((PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        prefix = PROVIDER.name + "/enchantments/"
        cert_ids = {Path(key).stem.replace("-", "_") for key, cert in ledger["objects"].items()
                    if key.startswith(prefix) and cert["status"] == "COMPLETE_PERK_READY"}
        observed = set(inventory["remaining_family_inventory"]["enchantment_ids"])
        remaining = sorted(observed - cert_ids)
        text = (PROVIDER / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        pairs = dict(re.findall(r"^(individual_[a-z_]+)=(\d+/\d+)$", text, flags=re.M))
        self.assertEqual(pairs["individual_full_enchantment_dossiers"], f"{len(cert_ids)}/{len(observed)}")
        self.assertEqual(pairs["individual_partial_enchantment_dossiers"], f"{len(remaining)}/{len(observed)}")
        self.assertEqual(pairs["individual_existing_enchantment_dossiers"], f"{len(observed)}/{len(observed)}")
        if remaining:
            next_work = text.split("O próximo trabalho", 1)[1].split("A fila global", 1)[0]
            self.assertIn("`alexscaves:" + remaining[0] + "`", next_work)
            self.assertNotIn("`alexscaves:flinging`", next_work)


if __name__ == "__main__":
    unittest.main()
