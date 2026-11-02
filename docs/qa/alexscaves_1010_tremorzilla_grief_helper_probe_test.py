#!/usr/bin/env python3
"""Synthetic fail-closed tests; do not substitute for publisher JAR verification."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch

from alexscaves_1010_tremorzilla_grief_helper_probe import (
    ANCHORS, CLASSES, SELECTION, GriefHelperEvidenceError,
    selected, window, inspect, bounded, audit, verify_sealed_snapshot,
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

    def sealed_fixture(self):
        from pathlib import Path
        import json
        manifest_path = (Path(__file__).resolve().parents[2] /
                         "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                         "EXACT-TREMORZILLA-GRIEF-HELPERS-1.0.10.json")
        seal = json.loads(manifest_path.read_text(encoding="utf-8"))
        report = {k: copy.deepcopy(seal[k]) for k in
                  ("schema_version", "scope", "artifact", "limits")}
        classes = {}
        for m in seal["selected_methods"]:
            cls = classes.setdefault(m["owner"], {
                "owner": m["owner"], "class_path": m["class_path"],
                "class_sha256": m["class_sha256"],
                "declared_method_count": m["declared_method_count"],
                "selected_methods": [],
            })
            cls["selected_methods"].append({
                "name": m["name"], "descriptor": m["descriptor"],
                "method_sha256": m["method_sha256"],
                "instruction_count": m["instruction_count"],
                "references": {"rows": [], "truncated": False},
                "branches_and_returns": {"rows": [], "truncated": False},
                "selected_windows": [],
            })
        report["classes"] = list(classes.values())
        for a in seal["selected_abi_anchors"]:
            c = classes[a["owner"]]
            m = next(row for row in c["selected_methods"] if row["name"] == a["name"])
            instruction = {
                "offset": a["offset"], "opcode": a["opcode"],
                "operand": a.get("operand_equals", ""),
                "symbol": a.get("symbol_contains", "")
            }
            if a["owner"] == "TremorzillaEntity":
                m["selected_windows"].append({
                    "site": a["offset"], "nearby_instructions": [instruction]
                })
            else:
                group = ("references" if a["opcode"].startswith(("invoke", "get"))
                         else "branches_and_returns")
                m[group]["rows"].append(instruction)
        return report, seal

    def test_exact_positive_sealed_helper_fixture(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_sealed_snapshot(report, seal))

    def test_eventhooks_delegate_replaced_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][0]["selected_methods"][0]["references"]["rows"][0][
            "symbol"] = "Method unrelated.canEntityGrief:()Z"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "callsite/branch"):
            verify_sealed_snapshot(report, seal)

    def test_early_return_target_changed_rejected(self):
        report, seal = self.sealed_fixture()
        t = report["classes"][2]["selected_methods"][0]["selected_windows"]
        row = next(w["nearby_instructions"][0] for w in t if w["site"] == 15)
        row["operand"] = "30"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "callsite/branch"):
            verify_sealed_snapshot(report, seal)

    def test_early_return_opcode_changed_rejected(self):
        report, seal = self.sealed_fixture()
        t = report["classes"][2]["selected_methods"][0]["selected_windows"]
        row = next(w["nearby_instructions"][0] for w in t if w["site"] == 29)
        row["opcode"] = "areturn"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "callsite/branch"):
            verify_sealed_snapshot(report, seal)

    def test_class_sha_changed_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][0]["class_sha256"] = "0" * 64
        with self.assertRaisesRegex(GriefHelperEvidenceError, "metadata drift"):
            verify_sealed_snapshot(report, seal)

    def test_method_sha_changed_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][1]["selected_methods"][0]["method_sha256"] = "0" * 64
        with self.assertRaisesRegex(GriefHelperEvidenceError, "method hash drift"):
            verify_sealed_snapshot(report, seal)

    def test_false_claims_verification_rejected(self):
        report, seal = self.sealed_fixture()
        report["limits"]["loaded_modpack_claims"] = "VERIFIED"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "promotion"):
            verify_sealed_snapshot(report, seal)

    def test_false_physical_qa_rejected(self):
        report, seal = self.sealed_fixture()
        report["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "promotion"):
            verify_sealed_snapshot(report, seal)

    def test_truncated_native_helper_evidence_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][0]["selected_methods"][0]["references"]["truncated"] = True
        with self.assertRaisesRegex(GriefHelperEvidenceError, "truncated"):
            verify_sealed_snapshot(report, seal)

    def test_unreviewed_permission_interpretation_rejected(self):
        report, seal = self.sealed_fixture()
        seal["interpretation"] = "CLAIMS_CERTIFIED"
        with self.assertRaisesRegex(GriefHelperEvidenceError, "permission inference"):
            verify_sealed_snapshot(report, seal)

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
