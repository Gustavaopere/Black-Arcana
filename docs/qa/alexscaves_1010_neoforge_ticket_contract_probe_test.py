#!/usr/bin/env python3
"""Synthetic fail-closed regression tests for exact NeoForge ticket contract."""
import hashlib
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_neoforge_ticket_contract_probe import (
    NEOFORGE_VERSION, NEO_CLASSES, evidence, mhash, seal,
)

def i(offset, symbol="", opcode="invokevirtual"):
    return {"offset":offset,"opcode":opcode,"operand":"#123","symbol":symbol}

def m(*ins):
    return {"header":"public void synthetic()","descriptor":"()V","instructions":list(ins)}

class NeoTicketSyntheticTests(unittest.TestCase):
    def test_expected_version_exact(self):
        self.assertEqual(NEOFORGE_VERSION,"21.1.248")
        self.assertIn("TicketController.class",NEO_CLASSES)
        self.assertIn("ForcedChunkManager.class",NEO_CLASSES)

    def test_bytecode_offset_duplication_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate JVM offset"):
            evidence(m(i(1),i(1)))

    def test_selected_boolean_argument_window(self):
        obj=evidence(m(i(0,"Method Other.a:()V"),i(1,"Method TicketController.forceChunk:()Z")))
        self.assertEqual(obj["total_cue_sites"],1)
        self.assertFalse(obj["anchors_truncated"])
        self.assertEqual(obj["anchors"][0]["at"],1)
        self.assertEqual([x["offset"] for x in obj["anchors"][0]["window"]],[0,1])

    def test_nonmatching_method_has_no_sites(self):
        obj=evidence(m(i(7,"Method java/lang/Math.max:(II)I")))
        self.assertEqual(obj["anchors"],[])

    def test_method_sha_changes_with_offset(self):
        self.assertNotEqual(mhash(m(i(1))),mhash(m(i(2))))

    def test_snapshot_key_duplicate_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"version":1,"version":2}',object_pairs_hook=strict_pairs)

    def test_seal_drops_context_without_dropping_anchor(self):
        x={"schema_version":1,"scope":"test","publisher":{},"neo":{},
           "provider_adapter_static_sha256":"x","provider_force_ticket_calls":[],
           "neoforge_class_count":1,"neoforge_classes":[{
                "class_path":"TicketController.class","class_sha256":"sha",
                "declared_method_count":1,"method_roster":[],
                "selected_methods":[{
                    "name":"forceChunk","descriptor":"()Z",
                    "instructions":4,"method_sha256":"m","total_cue_sites":1,
                    "anchors_truncated":False,
                    "anchors":[{"at":4,"instruction":i(4,"Method forceChunk:()Z"),
                                "window":[i(3),i(4),i(5)]}]
                }]
           }],"limits":{"allow_mutation":False}}
        s=seal(x)
        method=s["neoforge_classes"][0]["selected_methods"][0]
        self.assertEqual([v["offset"] for v in method["site_anchors"]],[4])
        self.assertNotIn("window",method)

if __name__=="__main__":
    unittest.main()
