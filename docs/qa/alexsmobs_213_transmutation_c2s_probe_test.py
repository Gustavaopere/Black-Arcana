#!/usr/bin/env python3
"""Synthetic fail-closed proof boundaries for 2.1.13 transmutation audit."""
import copy
import unittest

from alexsmobs_213_transmutation_c2s_probe import (
    MESSAGE, MENU, TILE, MAX_REFS_PER, TransmuteProbeError,
    projection, project_method, parse_class_initializer, verify_snapshot,
)


def instruction(offset, opcode, operand="", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": operand,
            "symbol": symbol}


def method(name, rows, descriptor="()V"):
    return {"header": "public void " + name + "();",
            "descriptor": descriptor, "instructions": rows}


def test_methods():
    return {
        MESSAGE: [
            method("handle", [
                instruction(0,"aload_0"),
                instruction(1,"getfield","#17","Field playerId:I"),
                instruction(4,"invokevirtual","#20","Method ServerPlayer.getEntity:()V"),
                instruction(7,"invokevirtual","#21",
                            "Method MenuTransmutationTable.transmute:(I)V"),
                instruction(10,"return"),
            ]),
            method("read", [instruction(0,"return")]),
        ],
        MENU: [
            method("clickMenuButton", [
                instruction(0,"invokevirtual","#1","Method Player.getId:()I"),
                instruction(3,"new","#2","class MessageTransmuteFromMenu"),
                instruction(6,"return"),
            ]),
            method("transmute", [
                instruction(0,"getstatic","#5","Field AMConfig.transmutingExperienceCost:I"),
                instruction(3,"invokevirtual","#6","Method Player.giveExperienceLevels:(I)V"),
                instruction(6,"return"),
            ]),
        ],
        TILE: [
            method("getPossibility", [
                instruction(0,"invokestatic","#8","Method Mth.clamp:(III)I"),
                instruction(3,"areturn"),
            ]),
            method("postTransmute", [
                instruction(0,"invokevirtual","#9","Method TileEntityTransmutationTable.setChanged:()V"),
                instruction(3,"return"),
            ]),
        ],
    }


class TransmutationC2STests(unittest.TestCase):
    def test_three_class_projection_with_sender_and_settlement(self):
        r=projection(test_methods())
        self.assertEqual(len(r["classes"]),3)
        self.assertEqual(r["classes"][0]["class_path"],MESSAGE)
        self.assertGreaterEqual(r["bounded_reference_count"],4)

    def test_contract_refs_not_all_jvm_invocations(self):
        m=method("handle",[
            instruction(0,"invokestatic","#1","Method MyClass.debug:()V"),
            instruction(3,"getfield","#2","Field playerId:I"),
            instruction(6,"return")])
        o=project_method(m)
        self.assertEqual(len(o["selected_refs"]),1)
        self.assertEqual(o["selected_refs"][0]["site"]["offset"],3)

    def test_critical_window_contains_branch_context(self):
        m=method("handle",[
            instruction(0,"aload_0"),
            instruction(1,"getfield","#2","Field playerId:I"),
            instruction(4,"ifeq","15"),
            instruction(7,"invokevirtual","#3","Method Menu.transmute:(I)V"),
            instruction(10,"return"),
            instruction(15,"return"),
        ])
        o=project_method(m)
        w=o["critical_windows"][0]
        self.assertEqual(w["anchor"],7)
        self.assertIn("ifeq",[r["opcode"] for r in w["operators"]])
        self.assertEqual(o["branches"][0]["target"],15)

    def test_duplicate_offsets_fail_closed(self):
        with self.assertRaisesRegex(TransmuteProbeError,"duplicate/non-monotonic"):
            project_method(method("handle",[
                instruction(0,"return"),instruction(0,"return")]))

    def test_reordered_offsets_fail_closed(self):
        with self.assertRaisesRegex(TransmuteProbeError,"duplicate/non-monotonic"):
            project_method(method("handle",[
                instruction(5,"return"),instruction(0,"return")]))

    def test_unparseable_branch_is_rejected(self):
        with self.assertRaisesRegex(TransmuteProbeError,"unparseable"):
            project_method(method("handle",[
                instruction(0,"ifeq","NaN"),instruction(3,"return")]))

    def test_empty_receiver_body_is_rejected(self):
        with self.assertRaisesRegex(TransmuteProbeError,"invalid/oversize"):
            project_method(method("handle",[]))

    def test_overlong_reference_list_rejected(self):
        calls=[instruction(i*3,"getfield","#8","Field playerId:I")
               for i in range(MAX_REFS_PER+1)]
        with self.assertRaisesRegex(TransmuteProbeError,"unbounded C2S"):
            project_method(method("handle",calls))

    def test_missing_menu_settlement_rejected(self):
        d=test_methods()
        d[MENU]=d[MENU][0:1]
        with self.assertRaisesRegex(TransmuteProbeError,"sender/settlement missing"):
            projection(d)

    def test_missing_tile_reader_rejected(self):
        d=test_methods()
        d[TILE]=d[TILE][1:]
        with self.assertRaisesRegex(TransmuteProbeError,"reader/post-settlement missing"):
            projection(d)

    def test_duplicate_descriptor_rejected(self):
        d=test_methods()
        d[MESSAGE].append(copy.deepcopy(d[MESSAGE][0]))
        with self.assertRaisesRegex(TransmuteProbeError,"duplicate JVM"):
            projection(d)

    def test_missing_message_rejected(self):
        d=test_methods()
        del d[MESSAGE]
        with self.assertRaisesRegex(TransmuteProbeError,"missing transmutation class"):
            projection(d)

    def test_class_initializer_parser_preserves_bytecode_registration(self):
        body=("Compiled from \"Registration.java\"\n"
              "public class Example {\n"
              "  static {};\n"
              "    descriptor: ()V\n"
              "    Code:\n"
              "       0: ldc_w #10 // class MessageTransmuteFromMenu\n"
              "       3: return\n"
              "}\n")
        m=parse_class_initializer(body)
        self.assertIsNotNone(m)
        self.assertEqual(len(m["instructions"]),2)
        self.assertEqual(m["instructions"][0]["opcode"],"ldc_w")

    def test_class_initializer_parser_returns_none_without_static_code(self):
        self.assertIsNone(parse_class_initializer("public class A {\n}\n"))

    def test_snapshot_rejects_changed_authorization(self):
        a={"limits":{"mutation":"NO_MUTATION","sender":"NOT_VERIFIED"}}
        b=copy.deepcopy(a);b["limits"]["sender"]="VERIFIED"
        self.assertIs(verify_snapshot(a,a),a)
        with self.assertRaisesRegex(TransmuteProbeError,"snapshot drift"):
            verify_snapshot(a,b)


if __name__ == "__main__":
    unittest.main()
