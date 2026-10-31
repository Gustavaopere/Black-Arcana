#!/usr/bin/env python3
"""Regression tests for fail-closed NuclearExplosion target/world evidence."""
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_target_world_probe import (
    HIGHLIGHTS, TICK_COUNT, TICK_SHA, compact, digest, scan_method, seal, window,
)


def instruction(at, opcode="fconst_0", symbol=""):
    return {"offset":at, "opcode":opcode, "operand":"", "symbol":symbol}


def method(*ins, name="tick"):
    return {"header":"public void "+name+"()", "descriptor":"()V", "instructions":list(ins)}


class NuclearWorldContractTests(unittest.TestCase):
    def test_selected_offset_is_bytecode_exact(self):
        selected=window(method(instruction(0),instruction(5),instruction(10)),5)
        self.assertEqual(selected["at"],5)
        self.assertEqual([x["offset"] for x in selected["ins"]],[0,5,10])

    def test_missing_offset_fails_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError,"missing/duplicate"):
            window(method(instruction(0)),4)

    def test_duplicate_offset_fails_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate target/world"):
            scan_method(method(instruction(1),instruction(1)))

    def test_critical_branch_and_field_collection(self):
        m=scan_method(method(
            instruction(0,"getstatic","Field Registry.NO_GRIEFING:Z"),
            instruction(2,"ifeq"),
            instruction(7,"ldc","float 1.0f"),
            instruction(9,"invokevirtual","Method Level.getBlockState:()V"), name="synthetic"))
        self.assertEqual([x["offset"] for x in m["references"]],[0,9])
        self.assertEqual([x["offset"] for x in m["branches"]],[2])
        self.assertEqual([x["offset"] for x in m["constants"]],[7])

    def test_excess_tick_method_budget(self):
        long_method=method(*[instruction(i) for i in range(451)])
        with self.assertRaisesRegex(GumballStateProbeError,"budget"):
            scan_method(long_method)

    def test_prior_sha_and_instruction_count_pinned(self):
        self.assertEqual(TICK_COUNT,348)
        self.assertEqual(TICK_SHA,"64f9a412c81a25525edf5b9576d56cec8354f6963ef718a44e6179347fcd8a25")
        self.assertLessEqual(len(HIGHLIGHTS),25)
        self.assertEqual(len(set(HIGHLIGHTS)),len(HIGHLIGHTS))

    def test_seal_strips_context_windows(self):
        doc={
            "schema_version":1,"scope":"SYNTHETIC","artifact":{},
            "class_path":"path","class_sha256":"sha",
            "declared_method_count":1,"selected_methods":{
                "tick:()V":{"instruction_count":1,"parsed_method_sha256":"abc",
                    "references":[],"branches":[],"constants":[],
                    "windows":[{"at":7,"ins":[compact(instruction(6)),compact(instruction(7)),
                                             compact(instruction(8))]}]}
            },"limitations":{"physical_qa":"NOT_TESTED"}
        }
        result=seal(doc)
        self.assertEqual([x["offset"] for x in
                         result["selected_methods"]["tick:()V"]["windows"][0]["ins"]],[7])

    def test_snapshot_duplicate_key_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"offset":1,"offset":3}',object_pairs_hook=strict_pairs)


if __name__=="__main__":
    unittest.main()
