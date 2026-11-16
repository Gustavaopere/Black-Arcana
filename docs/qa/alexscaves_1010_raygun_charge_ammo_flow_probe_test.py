#!/usr/bin/env python3
"""Read-only Raygun 1.0.10 charging/ammo JVM evidence synthetic regressions."""
import unittest

from alexscaves_1010_raygun_charge_ammo_flow_probe import method_site
from alexscaves_1010_ferrous_haste_causal_audit import AuditError

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
        self.assertEqual([r["offset"] for r in obs["selected_references_and_constants"]],[0,3])

    def test_unknown_target_fails_closed(self):
        with self.assertRaisesRegex(AuditError,"missing branch destination"):
            method_site(method([ins(0,"ifeq","999"),ins(3,"return")]))

    def test_duplicate_offsets_rejected(self):
        with self.assertRaisesRegex(AuditError,"invalid method instruction order"):
            method_site(method([ins(0,"return"),ins(0,"return")]))

    def test_empty_method_rejected(self):
        with self.assertRaisesRegex(AuditError,"empty method"):
            method_site(method([]))

    def test_switch_instruction_rejected(self):
        with self.assertRaisesRegex(AuditError,"unexpected JVM switch"):
            method_site(method([ins(0,"tableswitch","{"),ins(3,"return")]))

    def test_selected_sites_are_bounded(self):
        with self.assertRaisesRegex(AuditError,"budget exceeded"):
            method_site(method([ins(i*3,"invokestatic","#1","Method Example.x:()V")
                                for i in range(86)]))

if __name__ == "__main__":
    unittest.main()
