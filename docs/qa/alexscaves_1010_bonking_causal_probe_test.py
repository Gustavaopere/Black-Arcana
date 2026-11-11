#!/usr/bin/env python3
"""Fail-closed synthetic structural checks for SHA-exact Bonking causal audit."""
import unittest
from alexscaves_1010_bonking_causal_probe import (
    branch_edges,extract_exception_table,validate_pivots,select_consumer,
    strict_pairs
)
def i(offset,opcode,operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}
def method(rows):
    return {"header":"public void livingDie();",
            "descriptor":"(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V",
            "instructions":rows}
class Tests(unittest.TestCase):
    def test_branch_edges_and_fallthrough(self):
        data=branch_edges(method([i(0,"ifeq","4"),i(3,"goto","0"),i(4,"return")]))
        self.assertEqual(data[0]["fallthrough"],3)
        self.assertTrue(data[1]["back_edge"])
        self.assertEqual(data[1]["target"],0)
    def test_unresolved_target_fails(self):
        with self.assertRaisesRegex(ValueError,"invalid JVM branch target"):
            branch_edges(method([i(0,"goto","999"),i(3,"return")]))
    def test_unsupported_switch_fails(self):
        with self.assertRaisesRegex(ValueError,"unsupported"):
            branch_edges(method([i(0,"tableswitch","{}"),i(4,"return")]))
    def test_exact_pivot_missing_fails(self):
        with self.assertRaisesRegex(ValueError,"Bonking pivot"):
            validate_pivots(method([i(167,"getstatic",symbol="BONKING")]))
    def test_exception_parser_handles_javap_table(self):
        raw=("  public void livingDie(net.neoforged.neoforge.event.entity.living.LivingDeathEvent);\n"
             "    descriptor: (Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V\n"
             "    Code:\n"
             "       0: return\n"
             "      Exception table:\n"
             "         from    to  target type\n"
             "             0     1     2   any\n"
             "  public void another();\n")
        x=extract_exception_table(raw,"livingDie")
        self.assertEqual(x["declared_exception_handlers"],1)
        self.assertEqual(x["entries"][0]["handler"],2)
    def test_no_exception_table_is_not_physical_proof(self):
        raw=("  public void livingDie(net.neoforged.neoforge.event.entity.living.LivingDeathEvent);\n"
             "    descriptor: ()V\n"
             "    Code:\n"
             "       0: return\n"
             "  public void another();\n")
        self.assertEqual(extract_exception_table(raw,"livingDie")["declared_exception_handlers"],0)
    def test_strict_duplicate_json_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            strict_pairs([("limit","a"),("limit","b")])
    def test_does_not_accept_truncated_handler(self):
        with self.assertRaises(ValueError):
            select_consumer([method([i(0,"return")])])
if __name__=="__main__":
    unittest.main()
