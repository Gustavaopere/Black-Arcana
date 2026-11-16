#!/usr/bin/env python3
"""Synthetic negative regressions for Ferrous Haste full-method static seal.

This is only a deterministic contract fixture; it is NOT Minecraft gameplay QA.
The physical JAR replay is a separate CI step.
"""
import copy
import json
import unittest

from alexscaves_1010_ferrous_haste_causal_audit import (
    ROOT, AuditError, branches, load_history, row, strict_pairs,
    validate_individual_seal,
)


def report_fixture(seal):
    census = seal["full_method_census"]
    core = [{
        "owner": m["owner"], "name": m["name"],
        "descriptor": m["descriptor"],
        "instructions": m["instructions"],
        "body_sha256": m["parsed_method_sha256"],
        "direct_branches": 0, "switch_offsets": [],
    } for m in census["prior_sha_locked_methods"]]
    switch = [m for m in core if m["name"] == "getDigSpeed"]
    assert len(switch) == 1
    switch[0]["switch_offsets"] = [77]
    return {
        "enchantment": seal["enchantment"],
        "claim_scope": seal["claim_scope"],
        "evidence_grade": seal["evidence_grade"],
        "artifact": copy.deepcopy(seal["artifact"]),
        "compiled_ferrous_haste_token_owners":
            list(seal["compiled_ferrous_haste_token_owners"]),
        "methods_checked": census["methods_checked"],
        "instructions_checked": census["instructions_checked"],
        "direct_branches_checked": census["direct_branches_checked"],
        "dig_speed_switch_targets": copy.deepcopy(census["fatigue_switch"]["cases"]),
        "switches": switch,
        "method_census": core,
        "safety": {
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
        },
    }


class FerrousHasteCausalCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(
            (ROOT / "EXACT-FERROUS-HASTE-CAUSAL-1.0.10.json").read_text(
                encoding="utf8"), object_pairs_hook=strict_pairs)

    def test_static_baseline_contract(self):
        s = self.seal
        prior = load_history()
        self.assertEqual(s["artifact"], prior["artifact"])
        self.assertEqual(s["version"], "1.0.10")
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["full_method_census"]["methods_checked"], 13)
        self.assertEqual(s["full_method_census"]["instructions_checked"], 1387)
        self.assertEqual(s["full_method_census"]["direct_branches_checked"], 147)
        self.assertEqual(s["full_method_census"]["fatigue_switch"]["cases"],
                         [["0","108"], ["1","116"], ["2","124"], ["3","132"],
                          ["default","132"]])
        self.assertEqual(s["safety"]["mutation"], "NO_MUTATION")
        self.assertEqual(s["safety"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(s["safety"]["physical_qa"], "NOT_TESTED")
        validate_individual_seal(report_fixture(s), cert=s)

    def test_method_digest_tamper_rejected(self):
        report = report_fixture(self.seal)
        report["method_census"][0]["body_sha256"] = "f" * 64
        with self.assertRaisesRegex(AuditError, "full method body"):
            validate_individual_seal(report, cert=self.seal)

    def test_stale_publisher_rejected(self):
        report = report_fixture(self.seal)
        report["artifact"]["size_bytes"] -= 1
        with self.assertRaisesRegex(AuditError, "publisher identity"):
            validate_individual_seal(report, cert=self.seal)

    def test_wrong_native_token_owner_rejected(self):
        report = report_fixture(self.seal)
        report["compiled_ferrous_haste_token_owners"].append("com/evil/Other.class")
        with self.assertRaisesRegex(AuditError, "token consumers"):
            validate_individual_seal(report, cert=self.seal)

    def test_wrong_switch_or_missing_branch_rejected(self):
        report = report_fixture(self.seal)
        report["dig_speed_switch_targets"][0][1] = "999"
        with self.assertRaisesRegex(AuditError, "switch cases"):
            validate_individual_seal(report, cert=self.seal)
        method = {"instructions": [
            {"offset": 0, "opcode": "ifeq", "operand": "99", "symbol": ""},
            {"offset": 3, "opcode": "return", "operand": "", "symbol": ""},
        ]}
        with self.assertRaisesRegex(AuditError, "branch destination"):
            branches(method)

    def test_runtime_hook_and_physical_qa_not_promotable(self):
        s = copy.deepcopy(self.seal)
        s["safety"]["mutating_hook"] = "VERIFIED"
        with self.assertRaisesRegex(AuditError, "unsafe mutation hook"):
            validate_individual_seal(report_fixture(self.seal), cert=s)
        s = copy.deepcopy(self.seal)
        s["safety"]["physical_qa"] = "PASSED"
        with self.assertRaisesRegex(AuditError, "physical QA"):
            validate_individual_seal(report_fixture(self.seal), cert=s)

    def test_reject_unclosed_world_proof(self):
        s = copy.deepcopy(self.seal)
        s["safety"]["provider_universe_closed"] = True
        with self.assertRaisesRegex(AuditError, "provider universe"):
            validate_individual_seal(report_fixture(self.seal), cert=s)

    def test_duplicate_json_and_opcode_drift(self):
        with self.assertRaisesRegex(AuditError, "duplicate JSON"):
            json.loads('{"tag":1,"tag":2}',object_pairs_hook=strict_pairs)
        with self.assertRaisesRegex(AuditError, "unexpected opcode"):
            row({"instructions":[{"offset":5,"opcode":"ireturn",
                                  "operand":"","symbol":""}]},5,"ifne")


if __name__ == "__main__":
    unittest.main()
