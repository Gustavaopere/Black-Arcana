#!/usr/bin/env python3
"""Negative synthetic regression checks; they are NOT physical Minecraft tests."""
import copy
import hashlib
import json
import unittest

from alexsmobs_213_transmutation_c2s_probe import (
    SHA1, SHA256, SIZE, TransmuteProbeError,
)
from alexsmobs_213_table_block_lifecycle_probe import (
    BLOCK, MENU, TILE, INPUT_CONTAINER, INPUT_SLOT,
    choose, project, exact_edge, native_owner_path, sealed_classfiles, verify_lock,
)


def ins(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode,
            "operand": operand, "symbol": symbol}


def method(name, rows, descriptor="()V"):
    return {"header": "public void " + name + "();",
            "descriptor": descriptor, "instructions": rows}


class TableBlockProbeTests(unittest.TestCase):
    def test_block_open_method_is_selected_without_guessing_native_name(self):
        m = [method("useWithoutItem", [ins(0, "return")]),
             method("getTicker", [ins(0, "areturn")])]
        self.assertEqual(choose(BLOCK, m), m)

    def test_menu_selects_only_relevant_native_methods(self):
        m = [method("transmute", [ins(0, "return")]),
             method("removed", [ins(0, "return")]),
             method("notRelevant", [ins(0, "return")])]
        self.assertEqual(len(choose(MENU, m)), 2)

    def test_tile_selects_saved_data_callbacks(self):
        m = [method("loadAdditional", [ins(0, "return")]),
             method("postTransmute", [ins(0, "return")]),
             method("getRandomItem", [ins(0, "return")])]
        self.assertEqual(len(choose(TILE, m)), 2)

    def test_subclass_slot_is_not_dropped(self):
        m = [method("mayPlace", [ins(0, "ireturn")])]
        self.assertEqual(choose(INPUT_SLOT, m), m)
        self.assertEqual(choose(INPUT_CONTAINER, m), m)

    def test_project_maps_server_menu_open_and_tile_dirty_separately(self):
        m = method("useWithoutItem", [
            ins(0, "aload_0"),
            ins(1, "invokevirtual", "#2",
                "Method net/minecraft/server/level/ServerPlayer.openMenu:(Lnet/minecraft/world/MenuProvider;)Ljava/util/OptionalInt;"),
            ins(4, "invokevirtual", "#3",
                "Method net/minecraft/world/level/block/entity/BlockEntity.setChanged:()V"),
            ins(7, "return"),
        ])
        p = project(m)
        self.assertEqual(len(p["open_menu_calls"]), 1)
        self.assertEqual(len(p["native_set_changed_calls"]), 1)
        self.assertEqual(p["native_block_updates"], [])

    def test_menu_still_validity_reference_is_not_boolean_certification(self):
        m = method("use", [
            ins(0, "aload_0"),
            ins(1, "invokevirtual", "#2",
                "Method net/minecraft/world/inventory/AbstractContainerMenu.stillValid:()Z"),
            ins(4, "ireturn"),
        ])
        p = project(m)
        self.assertEqual(len(p["direct_validity_calls"]), 1)

    def test_missing_branch_target_fails_closed(self):
        m = method("getTicker", [
            ins(0, "iconst_0"), ins(1, "ifeq", "99"),
            ins(4, "areturn"),
        ])
        with self.assertRaises(TransmuteProbeError):
            project(m)

    def test_valid_branch_target_tracks_opcode(self):
        m = method("getTicker", [
            ins(0, "iconst_0"), ins(1, "ifeq", "4"),
            ins(4, "areturn"),
        ])
        x = project(m)["branches"][0]
        self.assertEqual((x["site"], x["target"]), (1, 4))

    def test_duplicate_jvm_offset_fails_closed(self):
        with self.assertRaises(TransmuteProbeError):
            project(method("openMenu", [
                ins(0, "aload_0"), ins(0, "return")
            ]))

    def test_prior_seal_requires_exclusive_exact_publisher(self):
        previous = {
            "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "observations": {"classes": [
                {"class_path": MENU, "class_sha256": "a" * 64},
                {"class_path": TILE, "class_sha256": "b" * 64},
            ]},
        }
        self.assertEqual(sealed_classfiles(previous)[MENU], "a" * 64)
        changed = copy.deepcopy(previous)
        changed["artifact"]["size_bytes"] += 1
        with self.assertRaises(TransmuteProbeError):
            sealed_classfiles(changed)


    def test_broadcast_uses_native_owner_method_not_shared_context_guess(self):
        m = project(method("amUse", [
            ins(83, "invokestatic", "#7",
                "Method com/github/alexthe666/alexsmobs/AlexsMobs.sendMSGToAll:(Ljava/lang/Object;)V"),
            ins(86, "areturn"),
        ]))
        site = exact_edge(m, 83, "invokestatic", "sendMSGToAll:")
        self.assertEqual(site["offset"], 83)

    def test_explosion_strength_literal_operators_recorded(self):
        m = project(method("explodeOnDestroy", [
            ins(0, "fconst_2"),
            ins(1, "iconst_0"),
            ins(2, "return"),
        ]))
        self.assertEqual([r["opcode"] for r in m["literal_operators"]],
                         ["fconst_2", "iconst_0"])

    def test_incorrect_owner_opcode_or_offset_fails_closed(self):
        m = project(method("amUse", [
            ins(0, "invokevirtual", "#1", "Method Player.openMenu:()V"),
            ins(3, "return"),
        ]))
        with self.assertRaises(TransmuteProbeError):
            exact_edge(m, 0, "invokestatic", "Player.openMenu:")
        with self.assertRaises(TransmuteProbeError):
            exact_edge(m, 19, "invokevirtual", "Player.openMenu:")

    def test_owner_path_missing_required_method_fails_closed(self):
        by = {BLOCK: {"selected_methods": []}}
        with self.assertRaises(TransmuteProbeError):
            native_owner_path(by)

    def test_mutation_lock_rejected_and_digest_checked(self):
        report = {
            "artifact": {"sha256": SHA256},
            "classes": [{}, {}, {}, {}, {}],
            "binary_consumer_candidates": [{}],
            "static_signals": {"block_direct_dirty_calls": 0},
            "exact_owner_path": {"sample": "STATIC"},
            "limitations": {"mutation": "NO_MUTATION"},
        }
        raw = (json.dumps(report, indent=2, ensure_ascii=False)
               + "\n").encode()
        lock = {
            "report_sha256": hashlib.sha256(raw).hexdigest(),
            "report_bytes": len(raw),
            "publisher_sha256": SHA256,
            "class_count": 5, "candidate_count": 1,
            "static_signals": {"block_direct_dirty_calls": 0},
            "owner_path_sha256": hashlib.sha256(
                json.dumps(report["exact_owner_path"], sort_keys=True,
                           ensure_ascii=False).encode("utf-8")
            ).hexdigest(),
            "mutation": "NO_MUTATION",
        }
        verify_lock(report, lock)
        mismatch = copy.deepcopy(lock)
        mismatch["static_signals"]["block_direct_dirty_calls"] = 1
        with self.assertRaises(TransmuteProbeError):
            verify_lock(report, mismatch)
        changed = copy.deepcopy(report)
        changed["limitations"]["mutation"] = "MUTATION"
        with self.assertRaises(TransmuteProbeError):
            verify_lock(changed, lock)


if __name__ == "__main__":
    unittest.main()
