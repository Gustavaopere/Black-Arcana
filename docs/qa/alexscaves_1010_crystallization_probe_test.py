#!/usr/bin/env python3
"""Negative, deterministic, fail-closed tests for bounded Crystallization probe."""
import unittest

from alexscaves_1010_crystallization_probe import (
    exact_method, evidence, find_tag, check_resources, require,
)

def inst(offset, opcode="nop", symbol=""):
    return {"offset":offset, "opcode":opcode, "operand":"", "symbol":symbol}

def method(name="use", desc="()V", instructions=None):
    return {"header":"public void "+name+"();","descriptor":desc,
            "instructions":instructions or [inst(0),inst(3)]}

class CrystallizationProbeTest(unittest.TestCase):
    def test_rejects_missing_method(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            exact_method([], "use")

    def test_rejects_duplicate_method(self):
        m=method()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            exact_method([m,m], "use")

    def test_rejects_disordered_bytecode(self):
        with self.assertRaisesRegex(ValueError, "unsorted"):
            exact_method([method(instructions=[inst(10),inst(8)])], "use")

    def test_rejects_broken_sha_contract(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            require(False,"negative")

    def test_rejects_ambiguous_tag_namespace(self):
        files={"data/alexscaves/tags/item/enchantable/galena_gauntlet.json",
               "data/alexscaves/tags/items/enchantable/galena_gauntlet.json"}
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            find_tag(files,"enchantable/galena_gauntlet.json")

    def test_rejects_missing_crystallization_tag(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            find_tag(set(),"galena_gauntlet_crystallization_items.json")

    def test_rejects_missing_native_consumer(self):
        m=method(instructions=[inst(x*2) for x in range(20)])
        with self.assertRaisesRegex(ValueError,"critical compiled pivot"):
            evidence(m,"use")

    def test_rejects_malformed_resource_semantics(self):
        resources={
            "enchantment":{"json":{"description":{"translate":"enchantment.alexscaves.crystallization"},
                                    "supported_items":"#alexscaves:enchantable/galena_gauntlet","max_level":1}},
            "gauntlet":{"json":{"values":["alexscaves:galena_gauntlet"]}},
            "crystallization":{"json":{"values":["minecraft:diamond"]}},
            "ferromagnetic":{"json":{"values":["minecraft:iron_sword"]}},
        }
        with self.assertRaisesRegex(ValueError,"ferromagnetic subset"):
            check_resources(resources)

    def test_validates_critical_pivot_presence(self):
        rows=[inst(0),inst(2,"getstatic","Field ACEnchantmentRegistry.CRYSTALLIZATION:Ljava/lang/Object;"),
              inst(4,"getstatic","Field ACTagRegistry.GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:Ljava/lang/Object;"),
              inst(6,"getstatic","Field ACTagRegistry.MAGNETIC_ITEMS:Ljava/lang/Object;"),
              inst(8)]
        self.assertEqual(len(evidence(method(instructions=rows),"use")["pivot_windows"]),3)

if __name__=="__main__":
    unittest.main()
