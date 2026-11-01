#!/usr/bin/env python3
"""Synthetic negative controls for SHA-exact Raygun class audit."""
import unittest
import copy

from alexscaves_1010_raygun_control_probe import (
    CLASS, CLASS_SHA256, FACTORY_OFFSET, RaygunProbeError,
    is_focus, selected_report, validate_impact_method, check_snapshot
)


def instr(offset, opcode, symbol=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol, "operand": ""}


def method(name, instructions, descriptor="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"):
    return {"header": "public void " + name + "()", "descriptor": descriptor,
            "instructions": instructions}


class RaygunControlProbeTest(unittest.TestCase):
    def impact(self):
        return method("onUseTick", [
            instr(0, "aload_0"),
            instr(FACTORY_OFFSET, "invokestatic",
                  "Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.causeRaygunDamage:(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;"),
            instr(1030, "return")
        ])

    def test_sha_exact_class_identifiers_are_pinned(self):
        self.assertTrue(CLASS.endswith("/RaygunItem.class"))
        self.assertEqual(len(CLASS_SHA256), 64)

    def test_expected_callsite_is_recovered(self):
        info = validate_impact_method(self.impact())
        self.assertEqual(info["offset"], FACTORY_OFFSET)
        self.assertEqual(info["opcode"], "invokestatic")

    def test_missing_or_wrong_offset_rejected(self):
        bad = self.impact()
        bad["instructions"][1]["offset"] = 1025
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_wrong_factory_rejected(self):
        bad = self.impact()
        bad["instructions"][1]["symbol"] = "Method causeNukeDamage:()V"
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_client_or_virtual_call_not_mistaken_for_factory(self):
        bad = self.impact()
        bad["instructions"][1]["opcode"] = "invokevirtual"
        with self.assertRaisesRegex(RaygunProbeError, "missing/moved"):
            validate_impact_method(bad)

    def test_duplicate_on_use_tick_fails_closed(self):
        with self.assertRaisesRegex(RaygunProbeError, "duplicate declared"):
            selected_report([self.impact(), self.impact()])

    def test_bounded_report_contains_selected_window(self):
        res = selected_report([self.impact(), method("other", [instr(0, "return")])])
        self.assertEqual(res["method_count"], 1)
        self.assertEqual(res["selected_methods"][0]["selected_windows"][0]["at"], FACTORY_OFFSET)
        self.assertTrue(is_focus(self.impact()))
        self.assertFalse(is_focus(method("unrelated", [instr(0, "return")])))

    def test_no_impact_method_fails_closed(self):
        with self.assertRaisesRegex(RaygunProbeError, "one exact"):
            selected_report([method("use", [instr(0, "return")])])

    def test_bad_descriptor_is_rejected(self):
        bad = self.impact()
        bad["descriptor"] = "()I"
        with self.assertRaisesRegex(RaygunProbeError, "unexpected"):
            validate_impact_method(bad)


    def pinned_pair(self):
        report = {
            "schema_version": 1, "scope": "static", "artifact": {"sha1": "1"},
            "class_path": CLASS, "class_sha256": CLASS_SHA256,
            "declared_method_count": 1, "method_count": 1,
            "selected_methods": [{
                "name": "onUseTick", "descriptor": "()V", "parsed_method_sha256": "abcd",
                "symbolic_references": [{
                    "offset": FACTORY_OFFSET, "opcode": "invokestatic",
                    "symbol": "Method causeRaygunDamage:()V", "operand": ""
                }],
                "numeric_constants": [], "branches": []
            }]
        }
        snapshot = {k: report[k] for k in (
            "schema_version", "scope", "artifact", "class_path", "class_sha256",
            "declared_method_count", "method_count"
        )}
        snapshot.update({
            "selected_method_digests": {"onUseTick ()V": "abcd"},
            "anchors": [{
                "method": "onUseTick", "offset": FACTORY_OFFSET,
                "kind": "symbolic_references", "opcode": "invokestatic",
                "symbol_contains": "causeRaygunDamage:"
            }]
        })
        return report, snapshot

    def test_sealed_hash_and_anchor_match(self):
        self.assertTrue(check_snapshot(*self.pinned_pair()))

    def test_sealed_anchor_mutation_rejected(self):
        report, snapshot = self.pinned_pair()
        report["selected_methods"][0]["symbolic_references"][0]["offset"] -= 1
        with self.assertRaisesRegex(RaygunProbeError, "missing or duplicate"):
            check_snapshot(report, snapshot)

    def test_sealed_digest_drift_rejected(self):
        report, snapshot = self.pinned_pair()
        snapshot["selected_method_digests"]["onUseTick ()V"] = "other"
        with self.assertRaisesRegex(RaygunProbeError, "digest drift"):
            check_snapshot(report, snapshot)

    def test_duplicate_anchor_rejected(self):
        report, snapshot = self.pinned_pair()
        snapshot["anchors"].append(copy.deepcopy(snapshot["anchors"][0]))
        with self.assertRaisesRegex(RaygunProbeError, "duplicate sealed"):
            check_snapshot(report, snapshot)

    def test_metadata_drift_rejected(self):
        report, snapshot = self.pinned_pair()
        report["class_sha256"] = "bad"
        with self.assertRaisesRegex(RaygunProbeError, "metadata drift"):
            check_snapshot(report, snapshot)



if __name__ == "__main__":
    unittest.main()
