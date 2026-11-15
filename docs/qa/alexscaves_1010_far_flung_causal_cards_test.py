#!/usr/bin/env python3
"""Synthetic fail-closed tests for the Far Flung 1.0.10 individual seal.

No claim of a physical gameplay test or a mutating provider hook.
"""
import copy
import json
import unittest

from alexscaves_1010_far_flung_causal_audit import (
    BASE, EXTRA_METHODS, HOOK, ITEM, PROVIDER, FarFlungAuditError,
    direct_branch_count, load_history, row, unique_pairs,
    validate_individual_seal,
)


def synthetic_report(seal):
    census = seal["individual_method_census"]
    core = [
        {
            "owner": item["owner"], "method": item["name"],
            "descriptor": item["descriptor"],
            "instructions": item["instruction_count"],
            "full_parsed_method_sha256": item["parsed_method_sha256"],
        }
        for item in census["core_sha_locked_methods"]
    ]
    other = [
        {
            "owner": owner, "method": name, "descriptor": "()V",
            "instructions": count,
            "full_parsed_method_sha256": "0" * 64,
        }
        for owner, entries in census["supplemental_full_class_sha_locked_methods"].items()
        for name, count in entries.items()
    ]
    return {
        "enchantment": seal["enchantment"], "release": seal["version"],
        "claim_scope": seal["claim_scope"],
        "evidence_grade": seal["evidence_grade"],
        "methods_checked": census["expected_methods_checked"],
        "instructions_checked": census["expected_instructions_checked"],
        "direct_branches_checked": census["expected_direct_branches_checked"],
        "compiled_far_flung_owners": list(seal["compiled_far_flung_token_owners"]),
        "method_census": core + other,
        "limits": {
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
        },
    }


class FarFlungStaticCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(
            (PROVIDER / "EXACT-FAR-FLUNG-CAUSAL-1.0.10.json").read_text(
                encoding="utf8"), object_pairs_hook=unique_pairs)

    def test_history_and_exact_individual_contract(self):
        s = self.seal
        previous = load_history()
        self.assertEqual(previous["enchantment"]["id"], "alexscaves:far_flung")
        self.assertEqual(previous["enchantment"]["json"]["max_level"], 3)
        self.assertEqual(previous["enchantment"]["json"]["slots"], ["mainhand"])
        self.assertEqual(s["version"], "1.0.10")
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(s["artifact"], previous["artifact"])
        self.assertEqual(s["launch"]["levels"], {"0": 0.5, "1": 0.7, "2": 0.9, "3": 1.1})
        self.assertEqual(s["safety"]["mutation"], "NO_MUTATION")
        self.assertEqual(s["safety"]["physical_qa"], "NOT_TESTED")
        self.assertEqual(s["safety"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(s["individual_method_census"]["expected_methods_checked"], 27)
        self.assertEqual(s["individual_method_census"]["expected_instructions_checked"], 1600)
        self.assertEqual(s["individual_method_census"]["expected_direct_branches_checked"], 182)
        self.assertEqual(len(s["individual_method_census"]["core_sha_locked_methods"]), 17)
        self.assertEqual(sum(map(len,
                s["individual_method_census"]["supplemental_full_class_sha_locked_methods"].values())), 10)
        self.assertEqual(set(EXTRA_METHODS), {ITEM, HOOK})
        validate_individual_seal(synthetic_report(s), seal_override=s)

    def test_wrong_method_digest_rejected(self):
        report = synthetic_report(self.seal)
        report["method_census"][0]["full_parsed_method_sha256"] = "f" * 64
        with self.assertRaisesRegex(FarFlungAuditError, "full body drift"):
            validate_individual_seal(report, seal_override=self.seal)

    def test_unclosed_runtime_mutation_rejected(self):
        s = copy.deepcopy(self.seal)
        s["safety"]["mutating_hook"] = "VERIFIED_CONTRACT"
        with self.assertRaisesRegex(FarFlungAuditError, "hook promoted"):
            validate_individual_seal(synthetic_report(self.seal), seal_override=s)
        s = copy.deepcopy(self.seal)
        s["safety"]["physical_qa"] = "PHYSICALLY_VERIFIED"
        with self.assertRaisesRegex(FarFlungAuditError, "physical QA promoted"):
            validate_individual_seal(synthetic_report(self.seal), seal_override=s)

    def test_provider_universe_not_falsely_closed(self):
        s = copy.deepcopy(self.seal)
        s["safety"]["provider_universe_closed"] = True
        with self.assertRaisesRegex(FarFlungAuditError, "provider universe"):
            validate_individual_seal(synthetic_report(self.seal), seal_override=s)

    def test_causal_counts_and_native_owners_fail_closed(self):
        report = synthetic_report(self.seal)
        report["direct_branches_checked"] = 181
        with self.assertRaisesRegex(FarFlungAuditError, "census"):
            validate_individual_seal(report, seal_override=self.seal)
        report = synthetic_report(self.seal)
        report["compiled_far_flung_owners"].append(BASE + "server/Unexpected.class")
        with self.assertRaisesRegex(FarFlungAuditError, "native consumer"):
            validate_individual_seal(report, seal_override=self.seal)

    def test_bad_adjacent_method_roster_fails_closed(self):
        report = synthetic_report(self.seal)
        report["method_census"][-1]["instructions"] -= 1
        with self.assertRaisesRegex(FarFlungAuditError, "adjacent"):
            validate_individual_seal(report, seal_override=self.seal)

    def test_branch_target_drift_rejected(self):
        method = {"instructions": [
            {"offset": 0, "opcode": "ifne", "operand": "99", "symbol": ""},
            {"offset": 3, "opcode": "return", "operand": "", "symbol": ""},
        ]}
        with self.assertRaisesRegex(FarFlungAuditError, "branch target"):
            direct_branch_count(method)
        with self.assertRaisesRegex(FarFlungAuditError, "opcode drift"):
            row(method, 0, "ifeq")
        with self.assertRaisesRegex(FarFlungAuditError, "duplicate"):
            row({"instructions": [
                {"offset": 0, "opcode": "nop", "symbol": "", "operand": ""},
                {"offset": 0, "opcode": "nop", "symbol": "", "operand": ""},
            ]}, 0)

    def test_duplicate_json_rejected(self):
        with self.assertRaisesRegex(FarFlungAuditError, "duplicate publisher"):
            json.loads('{"max_level":3,"max_level":4}', object_pairs_hook=unique_pairs)


if __name__ == "__main__":
    unittest.main()
