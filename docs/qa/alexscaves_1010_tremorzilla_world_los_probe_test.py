#!/usr/bin/env python3
"""Fail-closed synthetic regressions for read-only world/LOS inspection."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from alexscaves_1010_tremorzilla_world_los_probe import (
    TremorzillaWorldEvidenceError, compact_method, select_rows, extract,
    audit, limitations, verify_sealed_snapshot,
)


def ins(offset, op, symbol="", operand=""):
    return {"offset": offset, "opcode": op,
            "symbol": symbol, "operand": operand}


def method(name, rows, desc="()V"):
    return {"header": "public void " + name + "();",
            "descriptor": desc, "instructions": rows}


def fixture():
    result = [
        method("tickBreath", [
            ins(0, "invokevirtual", "Method TremorzillaEntity.breakBlocksAround:(LVec3;FZZF)Z"),
            ins(5, "invokevirtual", "Method TremorzillaEntity.hurtEntitiesAround:(LVec3;FFFZZZ)Z"),
            ins(8, "return")
        ]),
        method("canEntityBeHurtByBeam", [
            ins(0, "invokevirtual", "Method Level.clip:(LClipContext;)LHitResult;"),
            ins(4, "ireturn")
        ], "(LLivingEntity;LVec3;)Z"),
        method("breakBlocksAround", [
            ins(0, "invokevirtual", "Method Level.getBlockState:(LBlockPos;)LBlockState;"),
            ins(3, "ifeq", operand="12"),
            ins(6, "return")
        ], "(LVec3;FZZF)Z")
    ]
    result.extend(method("fillerMethod" + str(i), [ins(0, "return")])
                  for i in range(103))
    return result


class TremorzillaWorldContractTests(unittest.TestCase):
    def sealed_fixture(self):
        manifest = (Path(__file__).resolve().parents[2] /
                    "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                    "EXACT-TREMORZILLA-WORLD-LOS-1.0.10.json")
        seal = json.loads(manifest.read_text(encoding="utf-8"))
        report = {
            key: copy.deepcopy(seal[key]) for key in
            ("schema_version", "scope", "artifact", "class_path",
             "class_sha256", "method_count", "limits")
        }
        report["selected"] = {}
        for row in seal["method_signatures_and_digests"]:
            report["selected"][row["name"]] = [{
                "name": row["name"], "descriptor": row["descriptor"],
                "method_sha256": row["sha256"],
                "references": {"rows": [], "truncated": False},
                "constants": {"rows": [], "truncated": False},
                "branches": {"rows": [], "truncated": False},
            }]
        for anchor in seal["selected_abi_anchors"]:
            row = report["selected"][anchor["method"]][0]
            row[anchor["group"]]["rows"].append({
                "offset": anchor["offset"], "opcode": anchor["opcode"],
                "symbol": anchor.get("symbol_contains", ""),
                "operand": anchor.get("operand_equals", ""),
            })
        return report, seal

    def test_positive_exact_native_seal(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_sealed_snapshot(report, seal))

    def test_wrong_world_mutation_opcode_rejected(self):
        report, seal = self.sealed_fixture()
        row = next(r for r in report["selected"]["breakBlocksAround"][0]
                   ["references"]["rows"] if r["offset"] == 249)
        row["opcode"] = "getstatic"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "anchor mismatch"):
            verify_sealed_snapshot(report, seal)

    def test_false_griefing_authorization_rejected(self):
        report, seal = self.sealed_fixture()
        report["limits"]["world_protection_and_claims"] = "VERIFIED"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "promotion"):
            verify_sealed_snapshot(report, seal)

    def test_false_physical_qa_rejected(self):
        report, seal = self.sealed_fixture()
        seal["limits"]["physical_qa"] = "PASS"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "promotion"):
            verify_sealed_snapshot(report, seal)

    def test_hurt_method_sha_drift_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected"]["tickBreath"][0]["method_sha256"] = "0" * 64
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "digest drift"):
            verify_sealed_snapshot(report, seal)

    def test_truncated_anchor_evidence_rejected(self):
        report, seal = self.sealed_fixture()
        report["selected"]["tickBreath"][0]["references"]["truncated"] = True
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "truncated"):
            verify_sealed_snapshot(report, seal)

    def test_false_interpretation_rejected(self):
        report, seal = self.sealed_fixture()
        seal["interpretation"] = "PERK_READY"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "semantics"):
            verify_sealed_snapshot(report, seal)

    def test_positive_bounded_boundary_fixture(self):
        evidence = extract(fixture())
        self.assertEqual(len(evidence["tickBreath"]), 1)
        self.assertEqual(len(evidence["breakBlocksAround"]), 1)
        self.assertEqual(evidence["canEntityBeHurtByBeam"][0]
                         ["references"]["observed_count"], 1)

    def test_wrong_beam_call_is_rejected(self):
        methods = fixture()
        methods[0]["instructions"][0]["symbol"] = "Method unrelated.call:()V"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "required world/damage"):
            extract(methods)

    def test_missing_hurt_call_is_rejected(self):
        methods = fixture()
        methods[0]["instructions"][1]["symbol"] = "Method unrelated.call:()V"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "required world/damage"):
            extract(methods)

    def test_missing_los_call_is_rejected(self):
        methods = fixture()
        methods[1]["instructions"][0]["symbol"] = "Method unrelated.call:()V"
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "LOS raytrace"):
            extract(methods)

    def test_duplicate_method_signatures_rejected(self):
        methods = fixture()
        methods.append(copy.deepcopy(methods[2]))
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "duplicate method signature"):
            extract(methods)

    def test_duplicate_bytecode_offset_rejected(self):
        m = fixture()[2]
        m["instructions"].append(ins(3, "goto", operand="6"))
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "duplicate bytecode offset"):
            compact_method(m)

    def test_wrong_population_rejected(self):
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError,
                                    "method population"):
            extract(fixture()[:3])

    def test_no_world_hook_claim(self):
        self.assertEqual(limitations()["mutation"], "NO_MUTATION")
        self.assertEqual(limitations()["physical_qa"], "NOT_TESTED")
        self.assertEqual(limitations()["world_protection_and_claims"], "NOT_VERIFIED")

    def test_references_are_not_fabricated(self):
        m = method("breakBlocksAround", [
            ins(0, "getfield", "Field irrelevant.nonWorldField:I"),
            ins(3, "return"),
        ])
        result = compact_method(m)
        self.assertEqual(result["references"]["observed_count"], 0)

    def test_truncated_export_reports_true_total(self):
        rows = select_rows(list(range(10)), 3)
        self.assertEqual(rows["observed_count"], 10)
        self.assertEqual(rows["rows"], [0, 1, 2])
        self.assertTrue(rows["truncated"])

    def test_reference_budget_fails_closed(self):
        with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "export budget"):
            select_rows(list(range(701)), 20)

    def test_wrong_publisher_checksum_fails_before_zip(self):
        with patch("alexscaves_1010_tremorzilla_world_los_probe.sha_file",
                   return_value=("wrong", "hash", 0)):
            with self.assertRaisesRegex(TremorzillaWorldEvidenceError, "checksum"):
                audit("missing.jar", "javap")


if __name__ == "__main__":
    unittest.main()
