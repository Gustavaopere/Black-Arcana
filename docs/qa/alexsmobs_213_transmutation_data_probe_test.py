#!/usr/bin/env python3
"""Fail-closed synthetic tests for TransmutationData/NBT/display auditor."""
import copy
import hashlib
import json
import unittest

from alexsmobs_213_transmutation_c2s_probe import (
    SHA1, SHA256, SIZE, TransmuteProbeError,
)
from alexsmobs_213_transmutation_data_probe import (
    DATA, DISPLAY, COMPAT, TILE, MENU, EXPECTED_DATA,
    method_projection, prior_hashes, selected_methods, verify_lock,
)


def row(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode,
            "operand": operand, "symbol": symbol}


def method(name, rows, descriptor="()V"):
    return {"header": "public void " + name + "();",
            "descriptor": descriptor, "instructions": rows}


class TransmutationDataProbeTests(unittest.TestCase):
    def test_native_named_data_methods_required(self):
        m = [method(name, [row(0, "return")])
             for name in sorted(EXPECTED_DATA)]
        self.assertEqual(len(selected_methods(DATA, m)), len(EXPECTED_DATA))

    def test_missing_data_contract_fails_closed(self):
        m = [method(name, [row(0, "return")])
             for name in sorted(EXPECTED_DATA) if name != "getTotalWeight"]
        with self.assertRaises(TransmuteProbeError):
            selected_methods(DATA, m)

    def test_bounded_compat_methods(self):
        ms = [method("saveItem", [row(0, "return")]),
              method("getInt", [row(0, "return")]),
              method("unrelated", [row(0, "return")])]
        self.assertEqual(
            [x["header"] for x in selected_methods(COMPAT, ms)],
            [ms[0]["header"], ms[1]["header"]],
        )

    def test_relevant_tile_method_selection(self):
        ms = [method("loadAdditional", [row(0, "return")]),
              method("tick", [row(0, "return")]),
              method("other", [row(0, "return")])]
        self.assertEqual(len(selected_methods(TILE, ms)), 2)

    def test_display_methods_include_codec(self):
        ms = [method("read", [row(0, "return")]),
              method("write", [row(0, "return")])]
        self.assertEqual(len(selected_methods(DISPLAY, ms)), 2)

    def test_bytecode_refs_and_constants_are_bounded(self):
        m = method("fromNBT", [
            row(0, "ldc", "#10", "String TransmutationData"),
            row(2, "invokestatic", "#12",
                "Method com/github/alexthe666/alexsmobs/misc/AMCompat.getCompound:()V"),
            row(5, "return"),
        ])
        projected = method_projection(m)
        self.assertEqual(projected["literal_operators"][0]["offset"], 0)
        self.assertEqual(projected["relevant_refs"][0]["site"]["offset"], 0)
        self.assertEqual(projected["instruction_count"], 3)

    def test_branch_outside_method_fails_closed(self):
        m = method("getRandomItem", [
            row(0, "iconst_0"), row(1, "ifeq", "15"),
            row(4, "return"),
        ])
        with self.assertRaises(TransmuteProbeError):
            method_projection(m)

    def test_duplicate_jvm_offsets_fail_closed(self):
        m = method("onTransmuteItem", [
            row(0, "aload_0"), row(0, "return"),
        ])
        with self.assertRaises(TransmuteProbeError):
            method_projection(m)

    def test_direct_setchanged_is_a_callsite_not_durability_proof(self):
        m = method("saveAsNBT", [
            row(0, "aload_0"),
            row(1, "invokevirtual", "#1",
                "Method net/minecraft/world/level/block/entity/BlockEntity.setChanged:()V"),
            row(4, "return"),
        ])
        projected = method_projection(m)
        self.assertEqual(len(projected["native_set_changed_calls"]), 1)

    def test_math_operators_cover_weighted_sampling_sign_and_division(self):
        m = method("getRandomItem", [
            row(0, "dconst_0"),
            row(1, "dneg"),
            row(2, "ddiv"),
            row(3, "dreturn"),
        ])
        result = method_projection(m)
        self.assertEqual(
            [r["site"]["opcode"] for r in result["arithmetic_operators"]],
            ["dneg", "ddiv"],
        )

    def test_unbounded_math_operators_fail_closed(self):
        m = method("calculateAddWeight", [
            *[row(i, "dneg") for i in range(76)],
            row(76, "dreturn"),
        ])
        with self.assertRaises(TransmuteProbeError):
            method_projection(m)

    def test_prior_artifact_hash_identity_is_mandatory(self):
        x = {"artifact": {"sha1": SHA1, "sha256": SHA256,
                          "size_bytes": SIZE},
             "observations": {"classes": [
                 {"class_path": TILE, "class_sha256": "a" * 64},
                 {"class_path": MENU, "class_sha256": "b" * 64}
             ]}}
        self.assertEqual(prior_hashes(x)[TILE], "a" * 64)
        changed = copy.deepcopy(x)
        changed["artifact"]["size_bytes"] += 1
        with self.assertRaises(TransmuteProbeError):
            prior_hashes(changed)

    def test_digest_seal_rejects_other_report(self):
        report = {
            "artifact": {"sha256": SHA256},
            "classes": [{}, {}],
            "candidate_consumer_population": [{}],
            "limitations": {"mutation": "NO_MUTATION"},
        }
        b = (json.dumps(report, indent=2, ensure_ascii=False)
             + "\n").encode("utf-8")
        lock = {
            "publisher_sha256": SHA256,
            "report_sha256": hashlib.sha256(b).hexdigest(),
            "report_bytes": len(b),
            "class_count": 2,
            "candidate_consumer_count": 1,
            "mutation": "NO_MUTATION",
        }
        verify_lock(report, lock)
        wrong = copy.deepcopy(report)
        wrong["limitations"]["mutation"] = "MUTATION_PERMITTED"
        with self.assertRaises(TransmuteProbeError):
            verify_lock(wrong, lock)


if __name__ == "__main__":
    unittest.main()
