#!/usr/bin/env python3
"""Synthetic budget, offset and integrity checks for 1.0.10 Nuclear probe."""
import unittest
import json
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError
from alexscaves_1010_nuclear_envelope_probe import selected_anchors, seal, TICK_OFFSETS
from alexscaves_1010_gumball_state_probe import strict_pairs


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
        entry={"name":"calculateDamage","descriptor":"(FF)F",
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



class SealedNuclearEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NUCLEAR-ENVELOPE-1.0.10.json")
        cls.snapshot = json.loads(path.read_text(encoding="utf8"),
                                  object_pairs_hook=strict_pairs)

    def test_exact_selected_methods_and_29_critical_offsets(self):
        snap = self.snapshot
        self.assertEqual(snap["selected_method_count"], 7)
        self.assertEqual(snap["declared_method_count"], 19)
        self.assertEqual(len(snap["methods"]), 7)
        tick = snap["methods"]["tick:()V"]
        self.assertEqual(tick["parsed_method_sha256"],
                         "64f9a412c81a25525edf5b9576d56cec8354f6963ef718a44e6179347fcd8a25")
        self.assertEqual([x["offset"] for x in tick["selected_offsets"]],
                         list(TICK_OFFSETS))
        self.assertEqual(tick["instruction_count"], 348)

    def test_damage_factories_are_separate_paths_before_hurt(self):
        tick = self.snapshot["methods"]["tick:()V"]["selected_offsets"]
        by_offset = {x["offset"]: x for x in tick}
        self.assertIn("causeIntentionalGameDesign", by_offset[605]["symbol"])
        self.assertIn("causeNukeDamage", by_offset[618]["symbol"])
        self.assertEqual(by_offset[595]["opcode"], "ifeq")
        self.assertEqual(by_offset[595]["operand"], "611")
        self.assertEqual(by_offset[608]["opcode"], "goto")
        self.assertEqual(by_offset[608]["operand"], "621")
        self.assertIn("LivingEntity.hurt", by_offset[623]["symbol"])
        self.assertEqual(by_offset[626]["opcode"], "pop")

    def test_duplicate_json_snapshot_key_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate snapshot key"):
            json.loads('{"scope":"a","scope":"b"}', object_pairs_hook=strict_pairs)

    def test_snapshot_mutation_does_not_equal_original(self):
        replica = json.loads(json.dumps(self.snapshot))
        replica["methods"]["tick:()V"]["selected_offsets"][0]["opcode"] = "return"
        self.assertNotEqual(replica, self.snapshot)


if __name__ == "__main__":
    unittest.main()
