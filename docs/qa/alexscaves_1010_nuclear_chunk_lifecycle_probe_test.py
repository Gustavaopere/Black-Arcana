#!/usr/bin/env python3
"""Fail-closed synthetic regression tests for chunk-force ownership evidence."""
import json
import unittest

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_chunk_lifecycle_probe import (
    MAX_CANDIDATES, MAX_METHOD_INSNS, chosen_sites, method_sha, seal,
)


def instr(offset, symbol="", opcode="invokestatic"):
    return {"offset":offset,"opcode":opcode,"operand":"#7","symbol":symbol}


def method(*ins):
    return {"header":"public void sample()","descriptor":"()V","instructions":list(ins)}


class NuclearChunkLifecycleTests(unittest.TestCase):
    def test_exact_force_and_unforce_callsite_windows(self):
        m=method(instr(0,"Method ACPlatform.forceChunk:(...)V"),instr(3),
                 instr(6,"Method ACPlatform.forceChunk:(...)V"))
        sites=chosen_sites(m)
        self.assertEqual([x["at"] for x in sites],[0,6])
        self.assertEqual([x["offset"] for x in sites[0]["window"]],[0,3,6])

    def test_absence_of_symbol_does_not_invent_callsites(self):
        self.assertEqual(chosen_sites(method(instr(0,"Method Other.doSomething:()V"))),[])

    def test_duplicate_instruction_offset_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate chunk-lifecycle offset"):
            chosen_sites(method(instr(0),instr(0)))

    def test_bounded_method_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"instruction budget"):
            chosen_sites(method(*[instr(i) for i in range(MAX_METHOD_INSNS+1)]))

    def test_static_digest_identity_sensitive(self):
        a=method(instr(2,"Method ACPlatform.forceChunk:(...)V"))
        b=method(instr(3,"Method ACPlatform.forceChunk:(...)V"))
        self.assertNotEqual(method_sha(a),method_sha(b))

    def test_snapshot_projection_strips_context_not_anchor(self):
        doc={
            "schema_version":1,"scope":"unit","artifact":{},
            "nuclear_class_path":"a","nuclear_class_sha256":"sha",
            "nuclear_declared_method_roster":[],"candidate_class_count":1,
            "candidate_classes":[{
                "class_path":"a","class_sha256":"sha","method_count":1,
                "relevant_methods":[{
                    "name":"tick","descriptor":"()V","header":"void tick()",
                    "instruction_count":1,"parsed_method_sha256":"digest",
                    "sites":[{"at":7,"anchor":instr(7,"Method ACPlatform.forceChunk:(...)V"),
                              "window":[instr(5),instr(7)]}]
                }]
            }],
            "limitations":{"force_chunk_release_at_every_lifecycle_exit":"NOT_PROVEN"}
        }
        sealed=seal(doc)
        selected=sealed["candidate_classes"][0]["relevant_methods"][0]
        self.assertEqual(selected["site_anchors"][0]["offset"],7)
        self.assertNotIn("window",selected)
        self.assertLess(MAX_CANDIDATES,100)

    def test_duplicate_snapshot_keys_fail(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"scope":1,"scope":2}',object_pairs_hook=strict_pairs)


if __name__ == "__main__":
    unittest.main()
