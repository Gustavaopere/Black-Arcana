#!/usr/bin/env python3
"""Mutation regressions for the independent binary Aeropic evidence contract."""
import copy
import unittest
import winds_105_aeropic_local_indices_contract as c

VALID = {
    **c.FIXED,
    "call_sites": {
        method: {
            **row,
            "method": method,
            "operand_index_state": "EXACT_EXPLICIT_INDICES_OR_COMPACT_SUFFIX",
            "binary_candidate_requires_manual_review": True,
            "dynamic_override_executed": "NOT_PROVEN",
            "return_value_to_PlayerRecasts": "NOT_PROVEN",
            "safe_mutating_hook": "NOT_PROVEN",
        }
        for method, row in c.EXPECTED.items()
    },
}

class AeropicLocalIndexContractTests(unittest.TestCase):
    def test_independent_fixture(self):
        self.assertEqual(2, c.validate(copy.deepcopy(VALID)))

    def test_binary_identity_cannot_change(self):
        data = copy.deepcopy(VALID)
        data["sha1"] = "0" * 40
        with self.assertRaisesRegex(c.ContractError, "sha1"):
            c.validate(data)

    def test_callsite_population_cannot_change(self):
        data = copy.deepcopy(VALID)
        data["call_sites"].pop("applyEffectTick")
        with self.assertRaisesRegex(c.ContractError, "exactly two"):
            c.validate(data)

    def test_compiled_positive_cannot_be_inferred_or_removed(self):
        for value in ("NOT_PROVEN", "PROVEN_RUNTIME_OVERRIDE"):
            data = copy.deepcopy(VALID)
            data["call_sites"]["onEffectAdded"]["compiled_receiver_probe"] = value
            with self.assertRaisesRegex(c.ContractError, "compiled provenance"):
                c.validate(data)

    def test_negative_apply_effect_tick_remains_negative(self):
        data = copy.deepcopy(VALID)
        data["call_sites"]["applyEffectTick"]["compiled_receiver_probe"] = \
            "COMPILED_SUPPLIER_GET_CAST_RECEIVER"
        with self.assertRaisesRegex(c.ContractError, "compiled provenance"):
            c.validate(data)

    def test_exact_observed_local_counts(self):
        data = copy.deepcopy(VALID)
        data["call_sites"]["onEffectAdded"]["unsuffixed_load_store_indices_parsed"] = 7
        with self.assertRaisesRegex(c.ContractError, "compiled provenance"):
            c.validate(data)

    def test_control_flow_reason_frozen(self):
        data = copy.deepcopy(VALID)
        data["call_sites"]["applyEffectTick"]["probe_non_proof_reason"] = None
        with self.assertRaisesRegex(c.ContractError, "compiled provenance"):
            c.validate(data)

    def test_never_promote_dynamic_dispatch(self):
        data = copy.deepcopy(VALID)
        data["call_sites"]["onEffectAdded"]["dynamic_override_executed"] = "PROVEN"
        with self.assertRaisesRegex(c.ContractError, "unsafe authority"):
            c.validate(data)

    def test_never_promote_consumer(self):
        data = copy.deepcopy(VALID)
        data["call_sites"]["onEffectAdded"]["return_value_to_PlayerRecasts"] = "PROVEN"
        with self.assertRaisesRegex(c.ContractError, "unsafe authority"):
            c.validate(data)

    def test_never_promote_mutating_hook(self):
        data = copy.deepcopy(VALID)
        data["safe_mutating_hook"] = "PROVEN"
        with self.assertRaisesRegex(c.ContractError, "authority"):
            c.validate(data)

if __name__ == "__main__":
    unittest.main()
