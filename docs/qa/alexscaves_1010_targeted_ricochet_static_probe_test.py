#!/usr/bin/env python3
"""Negative and positive clean-room tests of Targeted Ricochet JVM audit."""
import unittest

from alexscaves_1010_targeted_ricochet_static_probe import (
    ID, ENCH, ENCH_SHA, TAG_SHA, GUM_SHA, SHOT_SHA,
    require, digest, anchors, check, certify,
)


def instr(off, opcode="nop", symbol="", operand=""):
    return {"offset":off,"opcode":opcode,"operand":operand,"symbol":symbol}


def method(name, rows):
    return {"header":name,"descriptor":"()V","instructions":rows}


class TargetedRicochetProofTests(unittest.TestCase):
    def test_registry_id(self):
        self.assertEqual(ID, "alexscaves:targeted_ricochet")
        self.assertEqual(ENCH, "data/alexscaves/enchantment/targeted_ricochet.json")

    def test_prior_sha_seals(self):
        for seal in (ENCH_SHA,TAG_SHA,GUM_SHA,SHOT_SHA):
            self.assertEqual(len(seal),64)
            self.assertTrue(all(c in "0123456789abcdef" for c in seal))

    def test_real_digest(self):
        self.assertEqual(digest(b"abc"),"ba7816bf8f01cfea414140de5dae2223b00361f20015ad")

    def test_fail_closed_helper(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            require(False,"expected")
        self.assertIsNone(require(True,"unused"))

    def test_bounded_anchor_output(self):
        m=method("bounceFromDirection",[instr(0),instr(5,"invokevirtual","targetsOnBounce:()Z"),instr(8)])
        a=anchors(m,[5])
        self.assertEqual(5,a[0]["offset"])
        self.assertEqual(3,len(a[0]["window"]))

    def test_missing_offset_fails(self):
        with self.assertRaisesRegex(ValueError,"JVM anchor missing"):
            anchors(method("onHit",[instr(0)]),[99])

    def test_target_branch_tamper_fails(self):
        m=method("test",[instr(0,"ifeq","","40")])
        check(m,{0:("ifeq",None,"40")})
        with self.assertRaisesRegex(ValueError,"CFG mismatch"):
            check(m,{0:("ifne",None,"40")})
        with self.assertRaisesRegex(ValueError,"CFG mismatch"):
            check(m,{0:("ifeq",None,"41")})

    def test_symbol_drift_fails(self):
        m=method("test",[instr(138,"getstatic","ACEnchantmentRegistry.TARGETED_RICOCHET:")])
        check(m,{138:("getstatic","TARGETED_RICOCHET",None)})
        with self.assertRaisesRegex(ValueError,"CFG mismatch"):
            check(m,{138:("getstatic","TRIPLE_SPLIT",None)})

    def test_certification_not_from_empty_methods(self):
        with self.assertRaises(Exception):
            certify(method("acInventoryTick",[]),{})


if __name__=="__main__":
    unittest.main()
