#!/usr/bin/env python3
"""Fail-closed synthetic regression tests for Chomping Spirit static probe."""
import unittest
from alexscaves_1010_chomping_spirit_causal_probe import (
    SPEAR, SPIRIT, PIVOTS, exact_anchors, causal_pivots, local_nbt,
    selected, require, SAVE_KEYS, NON_SAVE_FIELDS
)
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges

def inst(offset,opcode="nop",operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}

def method(name,rows,desc="()V"):
    return {"header":"public void "+name+"()",
            "descriptor":desc,"instructions":rows}

class ChompingSpiritCausalProbeTests(unittest.TestCase):
    def test_previous_exact_anchors_match(self):
        rows=[inst(0,"aload_0"),inst(3,"nop"),inst(6,"return")]
        record={"name":"acHurtEnemy","descriptor":"()V","anchors":[rows[0],rows[2]]}
        self.assertEqual(exact_anchors(method("acHurtEnemy",rows),record,SPEAR),2)

    def test_previous_anchor_opcode_drift_fails_closed(self):
        rows=[inst(0,"aload_0"),inst(3,"return")]
        record={"name":"acHurtEnemy","descriptor":"()V",
                "anchors":[inst(0,"nop")]}
        with self.assertRaisesRegex(ValueError,"selected JVM anchor drift"):
            exact_anchors(method("acHurtEnemy",rows),record,SPEAR)

    def test_duplicate_previous_anchor_offset_fails_closed(self):
        rows=[inst(0,"aload_0"),inst(3,"return")]
        record={"name":"acHurtEnemy","descriptor":"()V",
                "anchors":[rows[0],rows[0]]}
        with self.assertRaisesRegex(ValueError,"duplicate parent JVM anchor"):
            exact_anchors(method("acHurtEnemy",rows),record,SPEAR)

    def test_native_spear_cost_anchor_pivot(self):
        method_name="acHurtEnemy"
        rows=[inst(0,"nop"),inst(6,"invokestatic",
                   symbol="Method ACCompat.hurtAndBreak:()V")]
        found=causal_pivots(method(method_name,rows),SPEAR)
        self.assertEqual(found[0]["offset"],6)

    def test_native_spear_cost_pivot_wrong_opcode_fails(self):
        rows=[inst(0,"nop"),inst(6,"invokevirtual",
                   symbol="Method ACCompat.hurtAndBreak:()V")]
        with self.assertRaisesRegex(ValueError,"causal pivot drift"):
            causal_pivots(method("acHurtEnemy",rows),SPEAR)

    def test_symbol_refs_bounded_and_clean(self):
        rows=[inst(0,"getstatic",symbol="Field ENCHANTMENT_LEVEL:I"),
              inst(3,"nop"),inst(4,"invokevirtual",symbol="Method get:()I")]
        self.assertEqual(len(selected(method("sample",rows))),2)
        self.assertTrue(all("header" not in row
                            for row in selected(method("sample",rows))))

    def _nbt_fixture(self, bad=False):
        out=[]
        for name in ("addAdditionalSaveData","readAdditionalSaveData"):
            rows=[inst(i,"nop") for i in range(15)]
            rows[1]=inst(1,"ldc_w",symbol="String UsingPlayerUUID")
            rows[5]=inst(5,"ldc_w",symbol="String DinosaurType")
            if bad:rows[9]=inst(9,"getfield",symbol="Field ENCHANTMENT_LEVEL:I")
            out.append(method(name,rows))
        return out

    def test_native_own_nbt_fields_only(self):
        result=local_nbt(self._nbt_fixture())
        self.assertEqual(set(result),{"addAdditionalSaveData",
                                      "readAdditionalSaveData"})
        self.assertEqual(result["addAdditionalSaveData"]["exact_own_nbt_keys"],
                         list(SAVE_KEYS))
        self.assertFalse(result["readAdditionalSaveData"]
                         ["enchantment_level_and_victim_id_in_own_overrides"])

    def test_own_nbt_future_level_write_requires_reaudit(self):
        with self.assertRaisesRegex(ValueError,"serializes other targeted field"):
            local_nbt(self._nbt_fixture(bad=True))

    def test_missing_owner_save_key_requires_reaudit(self):
        rows=self._nbt_fixture()
        rows[0]["instructions"][5]=inst(5,"nop")
        with self.assertRaisesRegex(ValueError,"missing own native NBT field"):
            local_nbt(rows)

    def test_direct_branch_target_out_of_method_rejected(self):
        with self.assertRaisesRegex(ValueError,"branch target"):
            branch_edges(method("tick",[inst(0,"ifeq","44"),
                                        inst(3,"return")]))

    def test_unverified_switch_table_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"unsupported switch"):
            branch_edges(method("tick",[inst(0,"tableswitch"),
                                        inst(20,"return")]))

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative control"):
            require(False,"negative control")

if __name__=="__main__":
    unittest.main()
