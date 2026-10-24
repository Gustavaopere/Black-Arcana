#!/usr/bin/env python3
"""Synthetic mutation tests for exact provider getter evidence gate."""
import unittest
import winds_105_formula_contract as gate

def good():
    return {"provider":"wind_spellbooks","release":"1.0.5","sha1":gate.SHA1,
      "result":"PASS_INVENTORY_ONLY","method_count":4,
      "methods":{spell:{method:{"state":"EXACT_STRAIGHT_LINE_EXPRESSION",
        "expression_ast":ast} for method,ast in methods.items()}
        for spell,methods in gate.expected().items()}}

class ContractGateTests(unittest.TestCase):
    def test_exact_roster_accepts(self): self.assertEqual(4,gate.validate(good()))
    def test_rejects_unknown_sha(self):
        x=good();x['sha1']='0'*40
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_unresolved_getter(self):
        x=good();x['methods']['tornado']['getDuration']['state']='UNRESOLVED'
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_changed_constant(self):
        x=good();x['methods']['wind_jump']['getFloatDuration']['expression_ast']['left']['value']='101'
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_reordered_arguments(self):
        x=good();ast=x['methods']['almighty_push']['getDuration']['expression_ast']
        ast['left'],ast['right']=ast['right'],ast['left']
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_unknown_extra_getter(self):
        x=good();x['methods']['aeropic']['newMethod']={}
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_wrong_count(self):
        x=good();x['method_count']=3
        with self.assertRaises(gate.ContractError):gate.validate(x)

if __name__=='__main__':unittest.main()
