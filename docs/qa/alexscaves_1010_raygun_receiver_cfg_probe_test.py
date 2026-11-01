#!/usr/bin/env python3
"""Bounded synthetic CFG tests; not native gameplay or authorization tests."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from alexscaves_1010_raygun_receiver_cfg_probe import (
    CfgProbeError, audit, dominating_offsets, inspect_handler, reachable,
    successors, verify_snapshot
)


def ins(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand, "symbol": symbol}


class ReceiverCfgTests(unittest.TestCase):
    def example(self):
        # Sequential program; conditional bypass to return; no exception edges.
        return [
            ins(0, "aload_0"),
            ins(1, "ifnull", "15"),
            ins(4, "getfield", "#6", "Field packet.entityId:I"),
            ins(7, "invokestatic", "#9", "Method Level.getEntity:(I)LEntity;"),
            ins(10, "invokeinterface", "#10", "UpdatesStackTags.updateTagFromServer:()V"),
            ins(15, "return")
        ]

    def test_normal_cfg_conditional_paths(self):
        edges, branches = successors(self.example())
        self.assertEqual(edges[1], [15, 4])
        self.assertEqual(branches[0]["fallthrough"], 4)
        self.assertEqual(reachable(edges, 0), {0, 1, 4, 7, 10, 15})
        self.assertEqual(dominating_offsets(edges, 0, 10), [0, 1, 4, 7, 10])

    def test_dominance_does_not_infer_entity_ownership(self):
        data = self.example()
        edges, _ = successors(data)
        dominate = dominating_offsets(edges, 0, 10)
        # An entity lookup dominating a call does NOT imply sender == entity.
        self.assertIn(7, dominate)
        self.assertNotIn(15, dominate)

    def test_missing_sink_rejected(self):
        nodes = self.example()
        edges, _ = successors(nodes)
        with self.assertRaisesRegex(CfgProbeError, "unreachable"):
            dominating_offsets(edges, 0, 999)

    def test_branch_to_non_instruction_rejected(self):
        nodes = self.example()
        nodes[1]["operand"] = "13"
        with self.assertRaisesRegex(CfgProbeError, "branch target"):
            successors(nodes)

    def test_malformed_branch_target_rejected(self):
        nodes = self.example()
        nodes[1]["operand"] = "unresolved"
        with self.assertRaisesRegex(CfgProbeError, "invalid JVM branch"):
            successors(nodes)

    def test_duplicate_jvm_offsets_rejected(self):
        nodes = self.example()
        nodes.append(copy.deepcopy(nodes[0]))
        with self.assertRaisesRegex(CfgProbeError, "duplicate JVM"):
            successors(nodes)

    def test_out_of_order_offsets_rejected(self):
        nodes = self.example()
        nodes[0], nodes[1] = nodes[1], nodes[0]
        with self.assertRaisesRegex(CfgProbeError, "offset order"):
            successors(nodes)

    def test_explicit_return_has_no_fallthrough(self):
        edges, _ = successors(self.example())
        self.assertEqual(edges[15], [])

    def manifest_fixture(self):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                "EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json")
        sealed = json.loads(path.read_text(encoding="utf8"))
        report = copy.deepcopy(sealed)
        report["handler"]["selected_call_and_field_refs"] = (
            copy.deepcopy(sealed["pivotal_native_sites"]))
        report["handler"]["normal_cfg_dominators_of_update_dispatch"] = (
            sealed["required_normal_cfg_dominators"])
        return report, sealed

    def test_sha_exact_sealed_projection_positive(self):
        report, sealed = self.manifest_fixture()
        self.assertTrue(verify_snapshot(report, sealed))

    def test_entity_id_field_drift_rejected(self):
        report, sealed = self.manifest_fixture()
        report["handler"]["selected_call_and_field_refs"][2]["symbol"] = "Field otherId:I"
        with self.assertRaisesRegex(CfgProbeError, "pivotal native"):
            verify_snapshot(report, sealed)

    def test_item_source_type_substitution_rejected(self):
        report, sealed = self.manifest_fixture()
        report["handler"]["selected_call_and_field_refs"][5]["symbol"] = "Field otherStack:I"
        with self.assertRaisesRegex(CfgProbeError, "pivotal native"):
            verify_snapshot(report, sealed)

    def test_branch_target_snapshot_drift_rejected(self):
        report, sealed = self.manifest_fixture()
        report["handler"]["normal_cfg_branches"][1]["branch_target"] = 176
        with self.assertRaisesRegex(CfgProbeError, "snapshot drift"):
            verify_snapshot(report, sealed)

    def test_unjustified_hook_or_qa_promotion_rejected(self):
        report, sealed = self.manifest_fixture()
        altered = copy.deepcopy(sealed)
        altered["limits"]["mutation"] = "ALLOW"
        with self.assertRaisesRegex(CfgProbeError, "snapshot drift"):
            verify_snapshot(report, altered)

    def test_alternative_hand_branch_must_not_be_declared_dominant(self):
        report, sealed = self.manifest_fixture()
        report["handler"]["normal_cfg_dominators_of_update_dispatch"].append(113)
        with self.assertRaisesRegex(CfgProbeError, "alternative"):
            verify_snapshot(report, sealed)

    def test_wrong_publisher_rejected_before_archive(self):
        with patch("alexscaves_1010_raygun_receiver_cfg_probe.sha_file",
                   return_value=("wrong", "wrong", 0)):
            with self.assertRaisesRegex(CfgProbeError, "publisher"):
                audit("missing.jar", "javap", {}, {})


if __name__ == "__main__":
    unittest.main()
