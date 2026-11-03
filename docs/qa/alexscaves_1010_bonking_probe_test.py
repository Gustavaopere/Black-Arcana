#!/usr/bin/env python3
"""Synthetic negative tests for Bonking read-only exact publisher probe."""
import unittest
from alexscaves_1010_bonking_probe import choose_event,inspect_mixin,require

def ins(index,symbol="",opcode="getstatic"):
    return {"offset":index,"opcode":opcode,"operand":"","symbol":symbol}

def method(name,items,desc="(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V"):
    return {"header":"public void "+name+"();","descriptor":desc,"instructions":items}

def valid():
    xs=[ins(i*3,"","nop") for i in range(120)]
    xs[20]=ins(60,"Field ACEnchantmentRegistry.BONKING:Ljava/lang/Object;")
    xs[22]=ins(66,"InterfaceMethod EntityDropChanceAccessor.ac_getEquipmentDropChance:()F")
    xs[24]=ins(72,"InterfaceMethod EntityDropChanceAccessor.ac_setDropChance:(F)V")
    xs[26]=ins(78,"InterfaceMethod EntityDropChanceAccessor.ac_dropCustomDeathLoot:()V")
    return method("livingDie",xs)

class BonkingProbeTests(unittest.TestCase):
    def test_accepts_unique_selected_consumer(self):
        self.assertEqual(choose_event([valid()])["header"],"public void livingDie();")

    def test_no_bonking_guard_is_rejected(self):
        m=valid()
        m["instructions"][20]=ins(60,"")
        with self.assertRaisesRegex(ValueError,"Bonking"):
            choose_event([m])

    def test_duplicate_guard_rejected(self):
        m=valid()
        m["instructions"][27]=ins(81,"Field ACEnchantmentRegistry.BONKING:Ljava/lang/Object;")
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            choose_event([m])

    def test_loot_bridge_missing_rejected(self):
        m=valid()
        m["instructions"][26]=ins(78,"")
        with self.assertRaisesRegex(ValueError,"loot bridge"):
            choose_event([m])

    def test_unsorted_offsets_rejected(self):
        m=valid()
        m["instructions"][24]=ins(61,"InterfaceMethod EntityDropChanceAccessor.ac_setDropChance:(F)V")
        with self.assertRaisesRegex(ValueError,"unordered"):
            choose_event([m])

    def test_missing_mixin_method_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            inspect_mixin([method("foo",[])])

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
