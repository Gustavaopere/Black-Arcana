#!/usr/bin/env python3
"""Fail-closed synthetic regressions for read-only world/LOS inspection."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch

from alexscaves_1010_tremorzilla_world_los_probe import (
    TremorzillaWorldEvidenceError, compact_method, select_rows, extract,
    audit, limitations,
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
