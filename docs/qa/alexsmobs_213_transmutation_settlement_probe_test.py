#!/usr/bin/env python3
"""Synthetic negative tests for exact settlement audit boundaries (not physical QA)."""
import copy
import unittest

from alexsmobs_213_transmutation_c2s_probe import (
    MENU, MESSAGE, TILE, SHA1, SHA256, SIZE, TransmuteProbeError, fingerprint,
)
from alexsmobs_213_transmutation_settlement_probe import (
    projected_method, settlement_sequence, reroll_lifecycle, select_method,
    validate_against_sealed_snapshot, verify_snapshot,
)


def op(n, opcode, operand="", symbol=""):
    return {"offset": n, "opcode": opcode, "operand": operand, "symbol": symbol}


def method(name, rows, descriptor="()V"):
    return {"header": "public void " + name + "();",
            "descriptor": descriptor, "instructions": rows}


def ordered_native_effects():
    return method("transmute", [
        op(0, "aload_1"),
        op(122, "invokevirtual", "#1", "Method net/minecraft/world/item/ItemStack.setCount:(I)V"),
        op(131, "invokevirtual", "#2", "Method net/minecraft/world/inventory/Slot.set:(Lnet/minecraft/world/item/ItemStack;)V"),
        op(138, "invokevirtual", "#3", "Method net/minecraft/world/entity/player/Player.giveExperienceLevels:(I)V"),
        op(149, "invokevirtual", "#4", "Method com/github/alexthe666/alexsmobs/tileentity/TileEntityTransmutationTable.postTransmute:(Lnet/minecraft/world/entity/player/Player;)V"),
        op(152, "return"),
    ])


def reroll_methods():
    return [
        method("postTransmute", [
            op(50, "invokevirtual", "#1", "Method TransmutationData.onTransmuteItem:()V"),
            op(79, "putfield", "#2", "Field totalTransmuteCount:I"),
            op(114, "invokevirtual", "#3", "Method setRerollPlayerUUID:(Ljava/util/UUID;)V"),
            op(117, "return"),
        ]),
        method("tick", [
            op(14, "ifnull", "87"),
            op(25, "invokevirtual", "#4", "Method net/minecraft/world/level/Level.getPlayerByUUID:(Ljava/util/UUID;)Lnet/minecraft/world/entity/player/Player;"),
            op(30, "ifnull", "82"),
            op(79, "invokevirtual", "#5", "Method randomizeResults:(Lnet/minecraft/world/entity/player/Player;)V"),
            op(82, "aload_0"),
            op(84, "putfield", "#6", "Field rerollPlayerUUID:Ljava/util/UUID;"),
            op(87, "return"),
        ]),
        method("loadAdditional", [op(0, "return")]),
        method("saveAdditional", [op(0, "return")]),
        method("randomizeResults", [
            op(3, "invokevirtual", "#7", "Method rollPossiblity:(I)V"),
            op(9, "invokevirtual", "#7", "Method rollPossiblity:(I)V"),
            op(15, "invokevirtual", "#7", "Method rollPossiblity:(I)V"),
            op(18, "return"),
        ]),
    ]


class SettlementProbeTests(unittest.TestCase):
    def test_expected_effect_order_remains_hard_gated(self):
        seq = settlement_sequence(ordered_native_effects())
        self.assertEqual(seq["observed_order"], [122, 131, 138, 149])
        self.assertEqual(seq["runtime_atomicity"], "NOT_TESTED")

    def test_missing_xp_debit_fails_closed(self):
        m = ordered_native_effects()
        m["instructions"] = [r for r in m["instructions"] if r["offset"] != 138]
        with self.assertRaises(TransmuteProbeError):
            settlement_sequence(m)

    def test_duplicate_xp_debit_fails_closed(self):
        m = ordered_native_effects()
        m["instructions"].insert(-1, op(
            146, "invokevirtual", "#5",
            "Method net/minecraft/world/entity/player/Player.giveExperienceLevels:(I)V",
        ))
        with self.assertRaises(TransmuteProbeError):
            settlement_sequence(m)

    def test_reverse_order_fails_closed(self):
        m = ordered_native_effects()
        m["instructions"][2]["offset"] = 118
        with self.assertRaises(TransmuteProbeError):
            settlement_sequence(m)

    def test_unrecognized_effect_offset_fails_closed(self):
        m = ordered_native_effects()
        m["instructions"][1]["offset"] = 121
        with self.assertRaises(TransmuteProbeError):
            settlement_sequence(m)

    def test_projection_tracks_absence_of_still_valid_call(self):
        p = projected_method(ordered_native_effects())
        self.assertFalse(p["direct_still_valid_call"])
        self.assertTrue(any(
            "Slot.set" in s["site"]["symbol"] for s in p["relevant_sites"]
        ))

    def test_projection_tracks_explicit_still_valid_call(self):
        m = method("check", [
            op(0, "aload_0"),
            op(1, "invokevirtual", "#4",
               "Method net/minecraft/world/inventory/AbstractContainerMenu.stillValid:()Z"),
            op(5, "ireturn"),
        ])
        self.assertTrue(projected_method(m)["direct_still_valid_call"])

    def test_nonexistent_branch_target_fails_closed(self):
        m = method("check", [
            op(0, "iconst_0"), op(1, "ifeq", "10"), op(4, "return"),
        ])
        with self.assertRaises(TransmuteProbeError):
            projected_method(m)

    def test_real_branch_target_keeps_context(self):
        m = method("check", [
            op(0, "iconst_0"), op(1, "ifeq", "4"), op(4, "return"),
        ])
        p = projected_method(m)
        self.assertEqual(p["branches"][0]["target"], 4)
        self.assertEqual(p["branches"][0]["preceding"]["opcode"], "iconst_0")

    def test_duplicate_bytecode_offset_is_rejected(self):
        m = method("check", [op(0, "nop"), op(0, "return")])
        with self.assertRaises(TransmuteProbeError):
            projected_method(m)

    def test_missing_method_not_silently_skipped(self):
        with self.assertRaises(TransmuteProbeError):
            select_method([method("saveAdditional", [op(0, "return")])],
                          "postTransmute")

    def test_sealed_predecessor_fingerprint_must_match(self):
        native = {
            MESSAGE: [method("read", [op(0, "return")])],
            MENU: [method("transmute", [op(0, "return")])],
            TILE: [method("postTransmute", [op(0, "return")])],
        }
        snapshot = {
            "artifact": {
                "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
            },
            "observations": {
                "classes": [
                    {"class_path": k,
                     "selected_methods": [
                         {"name": m["header"].split("(")[0].split()[-1],
                          "descriptor": m["descriptor"],
                          "body_sha256": fingerprint(m)}
                         for m in v
                     ]}
                    for k, v in native.items()
                ],
            },
        }
        self.assertTrue(validate_against_sealed_snapshot(native, snapshot))
        corrupted = copy.deepcopy(native)
        corrupted[MENU][0]["instructions"][0]["opcode"] = "aconst_null"
        with self.assertRaises(TransmuteProbeError):
            validate_against_sealed_snapshot(corrupted, snapshot)

    def test_deferred_reroll_branch_remains_fail_closed(self):
        observed = reroll_lifecycle(reroll_methods())
        self.assertTrue(observed["missing_player_branch_bypasses_randomize"])
        self.assertEqual(
            observed["anchors"]["tick_missing_player_skips_reroll"]["operand"], "82",
        )
        self.assertFalse(observed["serialization"][
            "saveAdditional_directly_references_reroll_uuid"
        ])

    def test_new_direct_nbt_persistence_requires_audit_revision(self):
        altered = reroll_methods()
        altered[3]["instructions"].append(
            op(2, "getfield", "#8", "Field rerollPlayerUUID:Ljava/util/UUID;")
        )
        with self.assertRaises(TransmuteProbeError):
            reroll_lifecycle(altered)

    def test_missing_player_branch_drift_requires_audit_revision(self):
        altered = reroll_methods()
        altered[1]["instructions"][2]["operand"] = "79"
        with self.assertRaises(TransmuteProbeError):
            reroll_lifecycle(altered)

    def test_immediate_reroll_changes_deferred_contract(self):
        altered = reroll_methods()
        altered[0]["instructions"].insert(
            1, op(53, "invokevirtual", "#9", "Method randomizeResults:()V")
        )
        with self.assertRaises(TransmuteProbeError):
            reroll_lifecycle(altered)

    def test_new_snapshot_must_match_exactly(self):
        before = {"scope": "read-only", "mutation": "NO_MUTATION"}
        verify_snapshot(before, copy.deepcopy(before))
        changed = copy.deepcopy(before)
        changed["mutation"] = "ALLOWED"
        with self.assertRaises(TransmuteProbeError):
            verify_snapshot(changed, before)


if __name__ == "__main__":
    unittest.main()
