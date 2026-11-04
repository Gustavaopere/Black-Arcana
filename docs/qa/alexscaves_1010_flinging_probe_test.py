#!/usr/bin/env python3
"""Synthetic fail-closed checks for Flinging publisher read-only ABI discovery."""
import unittest
from alexscaves_1010_flinging_probe import (
    ITEM, WAVE, SCOPE, digest, require, select_methods, verify_launch
)

def ins(offset, symbol="", opcode="invokevirtual"):
    return {"offset":offset,"opcode":opcode,"operand":"","symbol":symbol}

def method(name, desc, instructions):
    return {"header":f"public void {name}();",
            "descriptor":desc,"instructions":instructions}

DESC="(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V"

class FlingingProbeTests(unittest.TestCase):
    def test_scope(self):
        self.assertIn("1010",SCOPE)
        self.assertEqual(len(digest(b"abc")),64)

    def test_no_release_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            verify_launch([])

    def test_missing_flinging_rejected(self):
        rows=[ins(i*3) for i in range(26)]
        rows[2]=ins(6,"Method enchantLevel:")
        rows[3]=ins(9,"Method setDeltaMovement:")
        rows[4]=ins(12,"Field TSUNAMI:")
        rows[5]=ins(15,"Method getEntitiesOfClass:")
        selected=select_methods([method("releaseUsing",DESC,rows)],ITEM)
        with self.assertRaisesRegex(ValueError,"FLINGING"):
            verify_launch(selected)

    def test_all_expected_launch_gates(self):
        rows=[ins(i*3) for i in range(28)]
        for idx,t in enumerate(("FLINGING:","enchantLevel:","setDeltaMovement:",
                                "TSUNAMI:","getEntitiesOfClass:"),2):
            rows[idx]=ins(idx*3,t)
        selected=select_methods([method("releaseUsing",DESC,rows)],ITEM)
        verify_launch(selected)
        self.assertEqual(selected[0]["pivots"][0]["positions"][0]["offset"],6)

    def test_unsorted_offsets_rejected(self):
        with self.assertRaisesRegex(ValueError,"unsorted"):
            select_methods([method("releaseUsing",DESC,
                        [ins(0),ins(4),ins(3)])],ITEM)

    def test_reject_excessive_method_population(self):
        with self.assertRaisesRegex(ValueError,"unbounded method"):
            select_methods([method("releaseUsing",DESC,
                           [ins(i) for i in range(2201)])],ITEM)

    def test_missing_launch_with_wave_method(self):
        selected=select_methods([method("tick","()V",
                                [ins(i) for i in range(8)])],WAVE)
        self.assertEqual(selected[0]["name"],"tick")
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            verify_launch(selected)

    def test_negative_gate(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
