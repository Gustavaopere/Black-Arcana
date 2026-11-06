#!/usr/bin/env python3
"""Fail-closed synthetic regressions for exact Sea Swing static catalog evidence."""
import copy
import unittest
from alexscaves_1010_sea_swing_static_probe import (
    ITEM, WAVE, check_dependency, compiled_static_boundaries, select_full
)


def ins(offset, opcode="aload_0", symbol="", operand=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol, "operand": operand}


class SeaSwingStaticAuditTests(unittest.TestCase):
    def test_required_own_method_is_mandatory(self):
        with self.assertRaisesRegex(ValueError, "missing exact"):
            select_full([], ("attackEntities",))

    def test_wrong_publisher_fingerprint_is_rejected(self):
        discovery = {"scope": "UNSEALED_SEA_SWING_1010_JVM_DISCOVERY",
                     "artifact": {"sha1": "a", "sha256": "b"},
                     "class_sha256": {}, "enchantment": {},
                     "consumers": []}
        computed = {"artifact": {"sha1": "a", "sha256": "evil"},
                    "class_sha256": {}, "enchantment": {}, "methods": {}}
        with self.assertRaisesRegex(ValueError, "provenance mismatch"):
            check_dependency(discovery, computed)

    def test_prior_window_drift_is_rejected(self):
        owner = ITEM
        anchor = ins(17, "getstatic", "SEA_SWING")
        discovery = {"scope": "UNSEALED_SEA_SWING_1010_JVM_DISCOVERY",
                     "artifact": {"sha1": "a", "sha256": "b"},
                     "class_sha256": {}, "enchantment": {},
                     "consumers": [{"owner": owner, "methods": [{
                         "name": "acHurtEnemy", "parsed_method_sha256": "match",
                         "instruction_count": 1,
                         "pivots": [{"windows": [[anchor]]}]}]}]}
        computed = {"artifact": {"sha1": "a", "sha256": "b"},
                    "class_sha256": {}, "enchantment": {},
                    "methods": {owner: {"acHurtEnemy": {
                        "parsed_method_sha256": "match", "instruction_count": 1,
                        "instructions": [ins(17, "getstatic", "OTHER")]}}}}
        with self.assertRaisesRegex(ValueError, "window drift"):
            check_dependency(discovery, computed)

    def test_full_binary_guard_and_hurt_return_are_separate(self):
        item = [
            ins(17, "getstatic", "SEA_SWING"),
            ins(23, "ifle", operand="97"),
            ins(59, "iconst_5"),
            ins(93, "invokevirtual", "addFreshEntity"),
            ins(96, "pop"),
        ]
        damage = [
            ins(4, "ldc2_w", "double 0.5d"),
            ins(13, "invokevirtual", "AABB.inflate"),
            ins(26, "invokevirtual", "mobProjectile"),
            ins(123, "invokevirtual", "LivingEntity.hurt"),
            ins(126, "pop"),
            ins(169, "invokestatic", "knockback"),
        ]
        tick = [
            ins(13, "invokevirtual", "getWaitingTicks"),
            ins(44, "return"),
            ins(527, "invokevirtual", "attackEntities"),
            ins(575, "invokevirtual", "getLifespan"),
        ]
        doc = {"methods": {
            ITEM: {"acHurtEnemy": {"instructions": item}},
            WAVE: {"attackEntities": {"instructions": damage},
                   "tick": {"instructions": tick}},
        }}
        compiled_static_boundaries(doc)
        tampered = copy.deepcopy(doc)
        tampered["methods"][WAVE]["attackEntities"]["instructions"][4]["opcode"] = "ifeq"
        with self.assertRaisesRegex(ValueError, "damage acceptance boundary"):
            compiled_static_boundaries(tampered)


if __name__ == "__main__":
    unittest.main()
