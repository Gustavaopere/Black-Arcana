#!/usr/bin/env python3
"""Mutation tests for reviewed exact-JAR CFG results, never gameplay claims."""
import copy
import unittest
import winds_105_aeropic_recast_cfg_contract as contract

VALID = {
    **contract.TOP,
    "call_sites": {
        name: {"method": name, **counts, **contract.SAFE_ROW}
        for name, counts in contract.ROWS.items()
    }
}

class CFGContractTests(unittest.TestCase):
    def change(self, method, key, value):
        doc = copy.deepcopy(VALID)
        doc["call_sites"][method][key] = value
        with self.assertRaisesRegex(contract.ContractError, "drift"):
            contract.validate(doc)

    def test_good_exact_fixture(self):
        self.assertEqual(2, contract.validate(copy.deepcopy(VALID)))

    def test_wrong_binary_sha(self):
        doc = copy.deepcopy(VALID)
        doc["sha1"] = "0"*40
        with self.assertRaisesRegex(contract.ContractError, "sha1"):
            contract.validate(doc)

    def test_missing_callsite(self):
        doc = copy.deepcopy(VALID)
        doc["call_sites"].pop("onEffectAdded")
        with self.assertRaisesRegex(contract.ContractError, "two"):
            contract.validate(doc)

    def test_modified_branch_count(self):
        self.change("applyEffectTick", "conditional_and_direct_jump_count", 21)

    def test_modified_join_count(self):
        self.change("applyEffectTick", "normal_route_join_instruction_count", 4)

    def test_modified_dominator_count(self):
        self.change("applyEffectTick", "supplier_field_reads_dominating_recast", 3)

    def test_modified_supplier_read_count(self):
        self.change("applyEffectTick", "supplier_field_reads_total", 2)

    def test_modified_instructions_on_route(self):
        self.change("applyEffectTick", "normal_routes_reaching_recast_instructions", 221)

    def test_no_runtime_receiver_promotion(self):
        doc = copy.deepcopy(VALID)
        doc["runtime_receiver_class"] = "AeropicSpell"
        with self.assertRaisesRegex(contract.ContractError, "drift"):
            contract.validate(doc)

    def test_no_operand_source_promotion(self):
        self.change("applyEffectTick", "compiled_receiver_source", "PROVEN")

    def test_no_player_recasts_dataflow_promotion(self):
        self.change("applyEffectTick", "return_value_to_PlayerRecasts", "PROVEN")

    def test_no_safe_mutating_hook_promotion(self):
        self.change("onEffectAdded", "safe_mutating_hook", "PROVEN")

    def test_non_proof_reasons_cannot_silently_change(self):
        self.change("applyEffectTick", "non_proof_reasons", ["NOT_PROVEN"])

    def test_cfg_grade_cannot_be_overstated(self):
        self.change("applyEffectTick", "cfg_evidence_grade", "FULL_JVM_DATAFLOW")

    def test_number_bool_coercion_is_rejected(self):
        self.change("onEffectAdded", "recast_reachable_on_normal_cfg", 1)

if __name__ == "__main__":
    unittest.main()
