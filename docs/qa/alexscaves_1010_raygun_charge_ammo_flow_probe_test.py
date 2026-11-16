#!/usr/bin/env python3
"""Read-only Raygun 1.0.10 charging/ammo JVM evidence synthetic regressions."""
import unittest

from alexscaves_1010_raygun_charge_ammo_flow_probe import method_site, verify_snapshot
from alexscaves_1010_ferrous_haste_causal_audit import AuditError
from alexscaves_1010_raygun_method_census_probe import CensusError

def ins(offset, opcode, operand="", symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}

def method(rows):
    return {"header":"public void test();","descriptor":"()V","instructions":rows}

class ChargeAmmoJVMRegression(unittest.TestCase):
    def test_captures_symbolic_sites_and_normal_branch_targets(self):
        m=method([
            ins(0,"getstatic","#1","Field RaygunItem.AMMO:Ljava/util/function/Predicate;"),
            ins(3,"invokevirtual","#2","Method ItemStack.shrink:(I)V"),
            ins(6,"ifeq","11"),ins(9,"return"),ins(11,"return"),
        ])
        obs=method_site(m)
        self.assertEqual(obs["direct_branch_edges"],[[6,11]])
        self.assertEqual(obs["branch_context"][0]["opcode"], "ifeq")
        self.assertEqual(obs["branch_context"][0]["fallthrough"], 9)
        self.assertEqual([x["opcode"] for x in obs["branch_context"][0]["stack_predecessors"][-2:]], ["getstatic", "invokevirtual"])
        self.assertEqual([r["offset"] for r in obs["selected_references_and_constants"]],[0,3])

    def test_unknown_target_fails_closed(self):
        with self.assertRaisesRegex(AuditError,"missing branch destination"):
            method_site(method([ins(0,"ifeq","999"),ins(3,"return")]))

    def test_duplicate_offsets_rejected(self):
        with self.assertRaisesRegex(CensusError,"invalid method instruction order"):
            method_site(method([ins(0,"return"),ins(0,"return")]))

    def test_empty_method_rejected(self):
        with self.assertRaisesRegex(CensusError,"empty method"):
            method_site(method([]))

    def test_switch_instruction_rejected(self):
        with self.assertRaisesRegex(CensusError,"unexpected JVM switch"):
            method_site(method([ins(0,"tableswitch","{"),ins(3,"return")]))

    def test_selected_sites_are_bounded(self):
        with self.assertRaisesRegex(CensusError,"budget exceeded"):
            method_site(method([ins(i*3,"invokestatic","#1","Method Example.x:()V")
                                for i in range(86)]))

    def test_snapshot_rejects_tampered_branch_destination(self):
        observed = method_site(method([
            ins(0,"ifeq","5"),ins(3,"return"),ins(5,"return")
        ]))
        report = {"selected_methods":[observed],"safety":{"mutation":"NO_MUTATION"}}
        copy_method = dict(observed)
        copy_method["direct_branch_edges"] = [[0,3]]
        frozen = {"selected_methods":[copy_method],"safety":{"mutation":"NO_MUTATION"}}
        from alexscaves_1010_raygun_method_census_probe import CensusError
        with self.assertRaisesRegex(CensusError,"branch seal drift"):
            verify_snapshot(report, frozen)

    def test_snapshot_accepts_identical_evidence(self):
        report = {"selected_methods":[],"safety":{"mutation":"NO_MUTATION"}}
        self.assertIs(verify_snapshot(report, report), report)

if __name__ == "__main__":
    unittest.main()
