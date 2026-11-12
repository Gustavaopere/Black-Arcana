#!/usr/bin/env python3
"""Astral Transferring exact 22-method manifest remains partial/fail-closed."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL=P/"EXACT-ASTRAL-TRANSFERRING-LIFECYCLE-1.0.10.json"
OLD=P/"EXACT-ASTRAL-TRANSFERRING-1.0.10.json"
CARD=P/"enchantments/astral-transferring.md"
CROSS=P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md"
LEDGER=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SEAL.read_text(encoding="utf8"))
        cls.old=json.loads(OLD.read_text(encoding="utf8"))
    def test_full_native_roster_and_consumer_digest(self):
        d=self.d
        self.assertEqual(d["owner"]["methods"],22)
        self.assertEqual(len(d["methods"]),22)
        self.assertEqual(d["owner"]["sha256"],self.old["owner"]["sha256"])
        a=next(x for x in d["methods"] if x["name"]=="onUseTick")
        self.assertEqual((a["instruction_count"],a["branch_count"]),(478,59))
        self.assertEqual(a["parsed_method_sha256"],self.old["consumer"]["parsed_method_sha256"])
        self.assertEqual(d["astral_transfer_region"]["pinned_instructions"],69)
    def test_candidate_loop_and_branch_gates_are_literal(self):
        d=self.d
        a=next(x for x in d["methods"] if x["name"]=="onUseTick")
        self.assertIn({"offset":1081,"opcode":"goto","target":766,"is_back_edge":True},a["branches"])
        pins={x["offset"]:x for x in d["astral_transfer_region"]["anchors"]}
        for pos in (883,884,885,890,895,898,899,910,916,920,923,
                    926,931,932,943,951,956,987,999,1048,1081):
            self.assertIn(pos,pins)
        self.assertEqual(pins[931]["opcode"],"iconst_1")
        self.assertIn("setPossessed",pins[932]["symbol"])
        calls=[x["offset"] for x in pins.values()
               if 929<=x["offset"]<=1051 and "setPossessed:" in x["symbol"]]
        self.assertEqual(calls,[932])
    def test_owner_uses_client_id_or_server_uuid(self):
        m=next(x for x in self.d["methods"] if x["name"]=="getControlledEntity")
        self.assertEqual(m["instruction_count"],44)
        self.assertTrue(any("Level.getEntity:(I)" in x["symbol"]
                            for x in m["relevant_references"]))
        self.assertTrue(any("ServerLevel.getEntity:(Ljava/util/UUID;)" in x["symbol"]
                            for x in m["relevant_references"]))
    def test_historical_partial_and_current_static_certificate_never_mutate(self):
        key="✅-alexs-caves-continued/enchantments/astral-transferring.md"
        objects=json.loads(LEDGER.read_text(encoding="utf8"))["objects"]
        cert=objects[key]
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})
        for k,v in (("certification","PARTIAL"),("mutating_hook","NOT_VERIFIED"),
                    ("physical_qa","NOT_TESTED"),("mutation","NO_MUTATION")):
            self.assertEqual(self.d["limits"][k],v)
        card=CARD.read_text(encoding="utf8")
        self.assertIn("EXACT-ASTRAL-TRANSFERRING-LIFECYCLE-1.0.10.json",card)
        self.assertIn("EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json",card)
        self.assertIn("NO_MUTATION",card)
        self.assertIn("| ✅ | `alexscaves:astral_transferring`",
                      CROSS.read_text(encoding="utf8"))
if __name__=="__main__":
    unittest.main()
