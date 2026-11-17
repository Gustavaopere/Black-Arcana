#!/usr/bin/env python3
"""Energy Efficiency 1.0.10 individual static certificate and indexes."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
KEY="✅-alexs-caves-continued/enchantments/energy-efficiency.md"

class EnergyEfficiencyStaticCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((P/"EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json").read_text(encoding="utf8"))
        cls.ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        cls.card=(P/"enchantments/energy-efficiency.md").read_text(encoding="utf8")
        cls.cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8")
        cls.enchants=(P/"enchantments/INDEX.md").read_text(encoding="utf8")
        cls.provider=(P/"INDEX.md").read_text(encoding="utf8")
        cls.global_index=(ROOT/"wiki/modpack-catalog/providers/INDEX.md").read_text(encoding="utf8")

    def test_publisher_identity_and_complete_jvm_method(self):
        s=self.seal
        self.assertEqual(s["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["artifact"]["size_bytes"],75279314)
        self.assertEqual(s["artifact"]["sha256"],"36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(s["onUseTick_sha256"],"b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5")
        self.assertEqual(s["full_report_sha256"],"0bb9e77b51908adaf6b679f483c484d5b4da5169cd4cb440e0c7a31b9c6dcfb3")
        self.assertEqual(s["onUseTick_direct_branches"],57)
        self.assertEqual(set(s["method_sha256"]),{"onUseTick","hasCharge","getCharge","setCharge"})
        self.assertEqual(len(s["compiled_token_owners"]),2)
        self.assertEqual(s["resource_sha256"]["data/alexscaves/enchantment/energy_efficiency.json"],
                         "c5771a00e6dd2dd0a693369a110a943354b074dde27b9f3c9d1dcb4a8440cf3a")

    def test_consumption_is_bounded_client_path_not_server_settlement(self):
        s=self.seal
        charge=s["energy_consumption_contract"]
        self.assertEqual(charge["side"],"CLIENT_BRANCH_IN_THIS_METHOD")
        self.assertEqual(charge["periods_0_to_3"],{"0":2,"1":3,"2":5,"3":6})
        self.assertEqual(charge["warmup_ticks"],15)
        self.assertTrue(charge["negative_level_minus_one_zero_divisor"])
        self.assertEqual(charge["client_update_message_authorization"],"NOT_VERIFIED")
        self.assertEqual(s["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(s["limits"]["physical_qa"],"NOT_TESTED")
        self.assertEqual(s["limits"]["network_authorization"],"NOT_VERIFIED")

    def test_seven_axis_certificate_and_no_execution_claims(self):
        cert=self.ledger["objects"][KEY]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),{
            "identity","behavior","parameters","targeting","costs","integration","validation"})
        for k,x in cert["evidence"].items():
            self.assertEqual(x["path"],"wiki/modpack-catalog/providers/"+KEY)
            self.assertGreater(len(x["reason"]),60,k)

    def test_card_distinguishes_publisher_math_client_server_and_qa(self):
        for x in ("contrato técnico estático individual certificado","523 instruções JVM",
                  "57 branches","15 ticks","2/3/5/6","isClientSide",
                  "NO_MUTATION","NOT_TESTED","NOT_VERIFIED","L=-1",
                  "0bb9e77b51908adaf6b679f483c484d5b4da5169cd4cb440e0c7a31b9c6dcfb3"):
            self.assertIn(x,self.card)

    def test_all_indexes_derive_from_ledger_and_alphabetical_row(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts/catalog"))
        import check_perk_ready_indexes as canonical
        provider_cards = [card for card in P.rglob("*.md")
                          if canonical.is_card(card)]
        global_cards = [card for card in canonical.PROVIDERS.rglob("*.md")
                        if canonical.is_card(card)]
        keys=self.ledger["objects"]
        all_count=sum(canonical.certified(card, self.ledger) for card in global_cards)
        provider_count=sum(canonical.certified(card, self.ledger) for card in provider_cards)
        enchant_count=sum(k.startswith("✅-alexs-caves-continued/enchantments/") for k in keys)
        self.assertGreaterEqual(all_count,209)
        self.assertGreaterEqual(provider_count,71)
        self.assertGreaterEqual(enchant_count,43)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {all_count}/{len(global_cards)}",self.global_index)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {provider_count}/{len(provider_cards)}",self.provider)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {enchant_count}/51",self.enchants)
        self.assertIn(f"individual_full_enchantment_dossiers={enchant_count}/51",self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-enchant_count}/51",self.cross)
        self.assertIn("| ✅ | Energy Efficiency |",self.enchants)
        self.assertIn("| ✅ | Energy Efficiency |",self.provider)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:energy_efficiency",self.cross)
        self.assertIn("Providers com catálogo concluído: 4/164",self.global_index)
        self.assertIn("Mods com escopo integral certificado: 0/164",self.global_index)

if __name__=="__main__":
    unittest.main()
