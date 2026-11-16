#!/usr/bin/env python3
"""Fail-closed synthetic checks for Tremorzilla 1.0.10 damage type evidence."""
import copy
import unittest

from alexscaves_1010_tremorzilla_beam_static_audit import (
    DAMAGE_ANCHORS, CALLERS, EXPECTED, anchors, pairs, merge_rosters
)

def fake_rows(anchors):
    return {"instructions":[{"offset":offset,
                             "opcode":value[0],
                             "operand":value[1],
                             "symbol":value[2] or "fake"}
                            for offset,value in anchors.items()]}

class TremorzillaBeamStaticTests(unittest.TestCase):
    def test_contract_shape(self):
        self.assertEqual(len(EXPECTED),12)
        self.assertEqual(len(DAMAGE_ANCHORS),22)
        self.assertEqual(sum(len(x) for x in CALLERS.values()),10)

    def test_strict_pairs(self):
        with self.assertRaisesRegex(ValueError,"duplicate JSON"):
            pairs([("a",1),("a",2)])

    def test_bad_factory_opcode_rejected(self):
        rows=fake_rows(DAMAGE_ANCHORS)
        row=next(x for x in rows["instructions"] if x["offset"]==76)
        row["opcode"]="invokevirtual"
        with self.assertRaisesRegex(ValueError,"@76"):
            anchors(rows,DAMAGE_ANCHORS,triples=True)

    def test_wrong_damage_branch_rejected(self):
        rows=fake_rows(DAMAGE_ANCHORS)
        next(x for x in rows["instructions"] if x["offset"]==240)["operand"]="351"
        with self.assertRaisesRegex(ValueError,"@240"):
            anchors(rows,DAMAGE_ANCHORS,triples=True)

    def test_wrong_irradiated_duration_rejected(self):
        rows=fake_rows(DAMAGE_ANCHORS)
        next(x for x in rows["instructions"] if x["offset"]==341)["operand"]="800"
        with self.assertRaisesRegex(ValueError,"@341"):
            anchors(rows,DAMAGE_ANCHORS,triples=True)

    def test_missing_historical_method_rejected(self):
        beam={"selected_method_digests":[{"name":"hurtEntitiesAround",
           "descriptor":"()V","sha256":"a"*64}]}
        with self.assertRaisesRegex(ValueError,"incomplete"):
            merge_rosters(beam,{"method_signatures_and_digests":[]},
                          {"methods":[]})

    def test_conflicting_method_digest_rejected(self):
        beam={"selected_method_digests":[{"name":"tickBreath",
           "descriptor":"()V","sha256":"a"*64}]}
        world={"method_signatures_and_digests":[{"name":"tickBreath",
           "descriptor":"()V","sha256":"b"*64}]}
        with self.assertRaisesRegex(ValueError,"contradictory"):
            merge_rosters(beam,world,{"methods":[]})

if __name__=="__main__":
    unittest.main()
