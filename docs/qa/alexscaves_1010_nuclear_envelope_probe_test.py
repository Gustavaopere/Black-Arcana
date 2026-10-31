#!/usr/bin/env python3
"""Synthetic budget, offset and integrity checks for 1.0.10 Nuclear probe."""
import unittest

from alexscaves_1010_gumball_state_probe import GumballStateProbeError
from alexscaves_1010_nuclear_envelope_probe import selected_anchors, seal, TICK_OFFSETS


def method(ins):
    return {"header":"public void tick()","descriptor":"()V",
            "instructions":ins}


def instruction(n, opcode="iconst_0"):
    return {"offset":n,"opcode":opcode,"operand":"","symbol":""}


class NuclearEnvelopeTests(unittest.TestCase):
    def test_fail_closed_missing_fixed_window(self):
        with self.assertRaisesRegex(GumballStateProbeError,"offset missing"):
            selected_anchors(method([instruction(0)]), (17,))

    def test_duplicate_bytecode_offset(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate Nuclear"):
            selected_anchors(method([instruction(1), instruction(1)]), (1,))

    def test_selected_numeric_constant_and_window(self):
        actual=selected_anchors(method([instruction(0),instruction(1,"ifeq"),
                                        instruction(3,"invokestatic"),
                                        instruction(6,"return")]),(0,3))
        self.assertEqual(actual["instruction_count"],4)
        self.assertEqual(len(actual["windows"]),2)
        self.assertEqual(actual["constants"][0]["offset"],0)
        self.assertEqual(actual["branches"][0]["opcode"],"ifeq")

    def test_too_many_windows(self):
        with self.assertRaisesRegex(GumballStateProbeError, "too many Nuclear windows"):
            selected_anchors(method([instruction(0)]), (0,)*31)

    def test_snapshot_requires_unique_selected_method(self):
        entry={"name":"tick","descriptor":"()V",
               "parsed_method_sha256":"a"*64,"instruction_count":2,
               "symbols":[],"branches":[],"constants":[],
               "windows":[]}
        evidence={"schema_version":1,"scope":"TEST","artifact":{},
                  "class_path":"example","class_sha256":"b"*64,
                  "declared_methods":[{}],"selected_methods":[entry,entry]}
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate Nuclear selected"):
            seal(evidence)

    def test_tick_pinned_anchor_population_is_bounded(self):
        self.assertEqual(len(TICK_OFFSETS),29)
        self.assertEqual(len(TICK_OFFSETS),len(set(TICK_OFFSETS)))


if __name__ == "__main__":
    unittest.main()
