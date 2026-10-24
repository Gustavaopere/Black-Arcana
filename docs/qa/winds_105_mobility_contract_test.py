#!/usr/bin/env python3
"""Positive/negative tests for SHA-exact five-getter document integrity."""
import unittest

import winds_105_mobility_contract as gate

def valid():
    return {
        "result": "PASS_EXACT_FIVE_METHOD_LOCAL_AST",
        "provider": "wind_spellbooks", "release": "1.0.5",
        "sha1": gate.EXPECTED_SHA1, "getter_count": 5,
        "methods": {spell: {getter: {
            "state": "EXACT_STRAIGHT_LINE_EXPRESSION", "expression_ast": ast
        } for getter, ast in methods.items()} for spell, methods in gate.expected().items()},
    }

class ContractTests(unittest.TestCase):
    def test_accepts_five_exact_asts(self):
        self.assertEqual(5, gate.validate(valid()))

    def test_rejects_changed_sha(self):
        d=valid();d["sha1"]="0"*40
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_new_method(self):
        d=valid();d["methods"]["wind_jump"]["unknown_method"]={}
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_missing_method(self):
        d=valid();d["methods"]["tailwind"].pop("getPercentJump")
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_unknown_instruction_evidence(self):
        d=valid();d["methods"]["iron_slash"]["getDistance"]["state"]="UNRESOLVED"
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_swapped_operands(self):
        d=valid();ast=d["methods"]["almighty_push"]["getRange"]["expression_ast"]
        ast["left"], ast["right"] = ast["right"], ast["left"]
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_changed_float_literal(self):
        d=valid();ast=d["methods"]["tailwind"]["getPercentAirSpeed"]["expression_ast"]
        ast["right"]["value"] = "99.0"
        with self.assertRaises(gate.ContractError): gate.validate(d)

    def test_rejects_missing_provider_metadata(self):
        d=valid();d.pop("release")
        with self.assertRaises(gate.ContractError): gate.validate(d)

if __name__ == "__main__":
    unittest.main()
