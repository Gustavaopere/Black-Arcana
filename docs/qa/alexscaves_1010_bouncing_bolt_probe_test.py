#!/usr/bin/env python3
"""Synthetic fail-closed regressions for SHA-exact Bouncing Bolt probe."""
import unittest
from alexscaves_1010_bouncing_bolt_probe import (
    select, selected_evidence, require,
    SELECTORS, SEA_STAFF, WATER_BOLT
)

def ins(i,opcode="nop",symbol=""):
    return {"offset":i,"opcode":opcode,"operand":"","symbol":symbol}

def method(name,descriptor,items):
    return {"header":"public void "+name+"();","descriptor":descriptor,
            "instructions":items}

class BouncingBoltProbeTests(unittest.TestCase):
    def test_unique_use_selection(self):
        desc=SELECTORS[SEA_STAFF][0][1]
        rows=[ins(i*2) for i in range(22)]
        self.assertEqual(select([method("use",desc,rows)],"use",desc)["descriptor"],desc)

    def test_duplicate_use_rejected(self):
        desc=SELECTORS[SEA_STAFF][0][1]
        m=method("use",desc,[ins(i*2) for i in range(22)])
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            select([m,m],"use",desc)

    def test_unsorted_offsets_rejected(self):
        desc=SELECTORS[SEA_STAFF][0][1]
        rows=[ins(i*2) for i in range(22)]
        rows[13]=ins(5)
        with self.assertRaisesRegex(ValueError,"unsorted"):
            select([method("use",desc,rows)],"use",desc)

    def test_missing_bouncing_guard_rejected(self):
        desc=SELECTORS[SEA_STAFF][0][1]
        rows=[ins(i*2+270) for i in range(22)]
        with self.assertRaisesRegex(ValueError,"Bouncing Bolt"):
            selected_evidence(method("use",desc,rows),"use",270,335)

    def test_missing_ricochet_handoff_rejected(self):
        rows=[ins(i*2+100) for i in range(22)]
        with self.assertRaisesRegex(ValueError,"ricochet handoff"):
            selected_evidence(method("damageMobs","()V",rows),"damageMobs",95,275)

    def test_missing_child_spawn_rejected(self):
        rows=[ins(i*2) for i in range(22)]
        rows[4]=ins(8,"invokevirtual","Method getEntities:()V")
        with self.assertRaisesRegex(ValueError,"child spawn"):
            selected_evidence(
                method("onRicochetHit",SELECTORS[WATER_BOLT][1][1],rows),
                "onRicochetHit",0,275)

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
