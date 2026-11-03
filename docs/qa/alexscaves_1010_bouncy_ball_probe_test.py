#!/usr/bin/env python3
"""Synthetic fail-closed regression tests for Bouncy Ball exact probe."""
import unittest
from alexscaves_1010_bouncy_ball_probe import (
    method,select_native,require,SELECTION,SHOT,BALL
)

def ins(offset,op="nop",symbol=""):
    return {"offset":offset,"opcode":op,"operand":"","symbol":symbol}

def m(name,desc,insns):
    return {"header":"public void "+name+"();","descriptor":desc,
            "instructions":insns}

class BouncyBallProbeTests(unittest.TestCase):
    def test_selects_unique_shot_method(self):
        name,desc,_,_=SELECTION[SHOT][0]
        obj=m(name,desc,[ins(i*2) for i in range(25)])
        self.assertEqual(method([obj],name,desc)["descriptor"],desc)

    def test_rejects_missing_method(self):
        name,desc,_,_=SELECTION[SHOT][0]
        with self.assertRaisesRegex(ValueError,"missing"):
            method([],name,desc)

    def test_rejects_duplicate_method(self):
        name,desc,_,_=SELECTION[SHOT][0]
        obj=m(name,desc,[ins(i*2) for i in range(25)])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            method([obj,obj],name,desc)

    def test_rejects_unsorted_offsets(self):
        name,desc,_,_=SELECTION[SHOT][0]
        rows=[ins(i*2) for i in range(25)]
        rows[9]=ins(3)
        with self.assertRaisesRegex(ValueError,"unsorted"):
            method([m(name,desc,rows)],name,desc)

    def test_rejects_missing_bouncy_ball(self):
        name,desc,_,_=SELECTION[SHOT][0]
        with self.assertRaisesRegex(ValueError,"Bouncy Ball"):
            select_native(m(name,desc,[ins(i*2) for i in range(25)]),name,None,())

    def test_rejects_unverified_anchor(self):
        name,desc,_,_=SELECTION[SHOT][0]
        rows=[ins(i*2) for i in range(25)]
        with self.assertRaisesRegex(ValueError,"anchor missing"):
            select_native(m(name,desc,rows),name,None,(1000,))

    def test_rejects_missing_bounce_consumer(self):
        name,desc,_,_=SELECTION[BALL][0]
        with self.assertRaisesRegex(ValueError,"bounce consumer"):
            select_native(m(name,desc,[ins(i*2) for i in range(25)]),name,None,())

    def test_rejects_wrong_method_digest(self):
        with self.assertRaisesRegex(ValueError,"drift"):
            select_native(m("getMaximumBounces","()I",[ins(i*2) for i in range(25)]),
                          "getMaximumBounces","invalid-hash",())

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
