#!/usr/bin/env python3
"""Negative synthetic parsing gates for exact Arrow Inducting probe."""
import unittest
from alexscaves_1010_arrow_inducting_probe import check_resource,choose,summarize,CONSUMER,PROJECTILE

def instruction(offset,opcode,symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":"","symbol":symbol}

def meth(name,refs):
    return {"header":"public void "+name+"();","descriptor":"()V","instructions":refs}

class ArrowInductingProbeTests(unittest.TestCase):
    def test_resource_requires_enchantment_fields(self):
        self.assertEqual(check_resource(b'{"description":"x","supported_items":"#tag","max_level":1,"weight":2}')["max_level"],1)
        with self.assertRaisesRegex(ValueError,"required"):
            check_resource(b'{"description":"x"}')

    def test_rejects_ambiguous_consumer(self):
        m=meth("foo",[instruction(0,"getstatic","Field ACEnchantmentRegistry.ARROW_INDUCTING:Ljava/lang/Object;")])
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            choose([m,m],CONSUMER)

    def test_rejects_missing_consumer(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            choose([meth("foo",[instruction(0,"return")])],CONSUMER)

    def test_rejects_missing_projectile_target_setter(self):
        m=meth("tick",[instruction(0,"invokevirtual","Method getOwner:()V")])
        with self.assertRaisesRegex(ValueError,"target state"):
            summarize(m,PROJECTILE)

    def test_rejects_duplicate_offsets(self):
        m=meth("foo",[instruction(0,"getstatic","Field ACEnchantmentRegistry.ARROW_INDUCTING:Ljava/lang/Object;"),
                      instruction(0,"new","class SeekingArrowEntity")])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            summarize(m,CONSUMER)

if __name__ == "__main__":
    unittest.main()
