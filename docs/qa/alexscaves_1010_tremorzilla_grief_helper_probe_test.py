#!/usr/bin/env python3
"""Synthetic fail-closed tests; do not substitute for publisher JAR verification."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch

from alexscaves_1010_tremorzilla_grief_helper_probe import (
    ANCHORS, CLASSES, SELECTION, GriefHelperEvidenceError,
    selected, window, inspect, bounded, audit,
)


def op(offset, opcode, symbol="", operand=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol, "operand": operand}


def method(name, desc, rows):
    return {"header": "public static boolean " + name + "(...);",
            "descriptor": desc, "instructions": rows}


def tremor():
    descriptor = SELECTION["TremorzillaEntity"]["breakBlocksAround"]
    rows = [op(0, "aload_0")]
    rows += [op(offset, opcode, "Method " + symbol) for offset, opcode, symbol in ANCHORS]
    rows.append(op(352, "ireturn"))
    return method("breakBlocksAround", descriptor, rows)


class GriefHelperTests(unittest.TestCase):
    def test_expected_classes_unique(self):
        self.assertEqual(len(CLASSES), len(set(CLASSES.values())))
        self.assertTrue(all(x.endswith(".class") for x in CLASSES.values()))

    def test_positive_method_selection(self):
        m = tremor()
        self.assertIs(selected([m], "TremorzillaEntity", "breakBlocksAround",
                               m["descriptor"]), m)

    def test_wrong_descriptor_rejected(self):
        m = tremor()
        with self.assertRaisesRegex(GriefHelperEvidenceError, "missing/ambiguous"):
            selected([m], "TremorzillaEntity", "breakBlocksAround", "()V")

    def test_duplicate_method_rejected(self):
        m = tremor()
        with self.assertRaisesRegex(GriefHelperEvidenceError, "missing/ambiguous"):
            selected([m, copy.deepcopy(m)], "TremorzillaEntity",
                     "breakBlocksAround", m["descriptor"])

    def test_empty_bytecode_fails_closed(self):
        m = tremor()
        m["instructions"] = []
        with self.assertRaisesRegex(GriefHelperEvidenceError, "empty"):
            selected([m], "TremorzillaEntity", "breakBlocksAround",
                     m["descriptor"])

    def test_duplicate_instruction_rejected(self):
        m = tremor()
        m["instructions"].append(op(12, "return"))
        with self.assertRaisesRegex(GriefHelperEvidenceError, "unordered"):
            selected([m], "TremorzillaEntity", "breakBlocksAround",
                     m["descriptor"])

    def test_positive_exact_guard_and_world_calls(self):
        evidence = inspect(tremor(), "TremorzillaEntity")
        self.assertEqual(evidence["name"], "breakBlocksAround")
        self.assertEqual(evidence["references"]["total"], len(ANCHORS))
        self.assertEqual(len(evidence["selected_windows"]), 2)

    def test_world_callsite_opcode_drift_fails_closed(self):
        m = tremor()
        m["instructions"][3]["opcode"] = "invokeinterface"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "callsite drift"):
            inspect(m, "TremorzillaEntity")

    def test_world_callsite_owner_drift_fails_closed(self):
        m = tremor()
        m["instructions"][1]["symbol"] = "Method wrong.canEntityGrief:()Z"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "callsite drift"):
            inspect(m, "TremorzillaEntity")

    def test_window_rejects_missing_or_duplicate_offsets(self):
        m = tremor()
        with self.assertRaisesRegex(GriefHelperEvidenceError, "window site"):
            window(m["instructions"], 999)
        m["instructions"].append(op(12, "return"))
        with self.assertRaisesRegex(GriefHelperEvidenceError, "window site"):
            window(m["instructions"], 12)

    def test_bounded_rows_disclose_truncation(self):
        rows = bounded([1, 2, 3], 2)
        self.assertTrue(rows["truncated"])
        self.assertEqual(rows["total"], 3)
        self.assertEqual(rows["rows"], [1, 2])

    def test_bounded_rows_refuse_oversize(self):
        with self.assertRaisesRegex(GriefHelperEvidenceError, "maximum"):
            bounded(list(range(1101)), 300)

    def test_publisher_sha_failure_before_zip_open(self):
        with patch("alexscaves_1010_tremorzilla_grief_helper_probe.sha_file",
                   return_value=("bad", "digest", 0)):
            with self.assertRaisesRegex(GriefHelperEvidenceError, "checksum"):
                audit("no-jar.jar", "javap")

    def test_helper_method_outputs_read_only_evidence(self):
        m = method("canEntityGrief", SELECTION["ACPlatform"]["canEntityGrief"],
                   [op(0, "invokevirtual", "Method GameRules.getBoolean:()Z"),
                    op(3, "ifeq", operand="8"), op(6, "iconst_1"),
                    op(7, "ireturn"), op(8, "iconst_0"),
                    op(9, "ireturn")])
        evidence = inspect(m, "ACPlatform")
        self.assertEqual(evidence["branches_and_returns"]["total"], 3)
        self.assertEqual(evidence["references"]["total"], 1)
        self.assertEqual(len(evidence["method_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
