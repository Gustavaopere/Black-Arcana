#!/usr/bin/env python3
"""Synthetic and negative regression tests: bounded Raygun 1.0.10 charge sites."""
import copy
import unittest

from alexscaves_1010_raygun_charge_cost_probe import (
    METHODS, MAX_SITES_PER_METHOD, projection, selected_sites,
    selected_instruction_window, verify_snapshot,
)
from alexscaves_1010_raygun_hit_outcomes_cfg_probe import FlowError

def ins(offset, opcode, operand="", symbol=""):
    return {"offset":offset, "opcode":opcode, "operand":operand, "symbol":symbol}

def method(name, rows):
    return {"header":"public void "+name+"();",
            "descriptor":"()V", "instructions":rows}

def roster():
    methods=[]
    for name in METHODS:
        if name=="onUseTick":
            rows=[ins(0,"return"),ins(246,"getstatic","#9",
                      "Field ACEnchantmentRegistry.ENERGY_EFFICIENCY:Ljava/lang/Object;"),
                  ins(249,"invokestatic","#10","Method ACCompat.enchantLevel:()I"),
                  ins(252,"return")]
        else:
            rows=[ins(0,"return")]
        methods.append(method(name,rows))
    return methods

class RaygunChargeCostTests(unittest.TestCase):
    def test_exact_method_projection_carries_energy_efficiency(self):
        result=projection(roster())
        self.assertEqual(len(result["selected_methods"]),len(METHODS))
        self.assertEqual(result["charge_related_site_count"],1)
        self.assertEqual(result["selected_methods"][0]["charge_related_references"][0]["offset"],246)

    def test_bounded_site_window_carries_predecessor_and_successor(self):
        m=method("x",[ins(0,"iload_1"),ins(1,"iconst_1"),
                      ins(2,"invokestatic","#1","Method Sample.setCharge:(I)V"),
                      ins(5,"return")])
        items=selected_sites(m)
        self.assertEqual(len(items),1)
        self.assertEqual(items[0]["site"]["offset"],2)
        self.assertEqual([x["offset"] for x in items[0]["before"]],[0,1])
        self.assertEqual(items[0]["after"][0]["opcode"],"return")

    def test_unrelated_invocations_do_not_become_charge_evidence(self):
        m=method("x",[ins(0,"invokestatic","#3","Method Sample.render:()V"),ins(3,"return")])
        self.assertEqual(selected_sites(m),[])

    def test_duplicate_offsets_are_rejected(self):
        with self.assertRaisesRegex(FlowError,"duplicate/invalid"):
            selected_sites(method("x",[ins(0,"return"),ins(0,"return")]))

    def test_reordered_offsets_are_rejected(self):
        with self.assertRaisesRegex(FlowError,"duplicate/invalid"):
            selected_sites(method("x",[ins(3,"return"),ins(1,"return")]))

    def test_empty_method_is_rejected(self):
        with self.assertRaisesRegex(FlowError,"duplicate/invalid"):
            selected_sites(method("x",[]))

    def test_too_many_charge_sites_fails_closed(self):
        rows=[ins(i*3,"invokestatic","#1","Method RaygunItem.getCharge:()I")
              for i in range(MAX_SITES_PER_METHOD+1)]
        with self.assertRaisesRegex(FlowError,"unbounded charge-related"):
            selected_sites(method("x",rows))

    def test_window_selection_keeps_arithmetic_and_branches(self):
        rows=[ins(226,"fload","7"),ins(229,"fmul"),ins(230,"ifne","244"),
              ins(233,"return")]
        result=selected_instruction_window(method("x",rows),222,240)
        self.assertEqual([x["opcode"] for x in result],["fload","fmul","ifne"])

    def test_window_rejects_unbounded_ranges(self):
        with self.assertRaisesRegex(FlowError,"unbounded charge window"):
            selected_instruction_window(method("x",[ins(0,"return")]),0,1000)

    def test_snapshot_rejects_changed_charge_cost(self):
        a={"scope":"test","charge":2,"limits":{"mutation":"NO_MUTATION"}}
        b=copy.deepcopy(a)
        b["charge"]=200
        with self.assertRaisesRegex(FlowError,"charge cost snapshot drift"):
            verify_snapshot(a,b)
        self.assertIs(verify_snapshot(a,a),a)

    def test_missing_energy_efficiency_anchor_is_rejected(self):
        r=roster()
        r[0]["instructions"][1]["symbol"]="Field Other.EFFICIENCY:Ljava/lang/Object;"
        with self.assertRaisesRegex(FlowError,"Energy Efficiency native anchor drift"):
            projection(r)

    def test_duplicate_method_name_is_rejected(self):
        r=roster()+[roster()[0]]
        with self.assertRaisesRegex(FlowError,"ambiguous overloaded charge method"):
            projection(r)

if __name__ == "__main__":
    unittest.main()
