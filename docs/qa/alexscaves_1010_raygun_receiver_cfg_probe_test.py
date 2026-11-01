#!/usr/bin/env python3
"""Bounded synthetic CFG tests; not native gameplay or authorization tests."""
import copy
import unittest
from unittest.mock import patch
from alexscaves_1010_raygun_receiver_cfg_probe import (
    CfgProbeError, audit, dominating_offsets, inspect_handler, reachable,
    successors
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

    def test_wrong_publisher_rejected_before_archive(self):
        with patch("alexscaves_1010_raygun_receiver_cfg_probe.sha_file",
                   return_value=("wrong", "wrong", 0)):
            with self.assertRaisesRegex(CfgProbeError, "publisher"):
                audit("missing.jar", "javap", {}, {})


if __name__ == "__main__":
    unittest.main()
