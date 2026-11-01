#!/usr/bin/env python3
"""Synthetic fail-closed JVM identity/dispatch tests. No provider binary copied."""
import unittest
from alexscaves_1010_raygun_receiver_probe import (
    ANCHORS, HANDLE, PACKET, RAYGUN, UPDATES, ReceiverProbeError,
    anchor, bounded_method, class_declaration, method_by_sig
)

def op(offset, opcode, sym=""):
    return {"offset": offset, "opcode": opcode, "operand": "", "symbol": sym}

def method(name="handle", desc=HANDLE):
    return {"header": "public void " + name + "()",
            "descriptor": desc,
            "instructions": [
                op(0, "aload_0"),
                op(8, "invokeinterface", "InterfaceMethod ACNetworkContext.getSender:()LServerPlayer;"),
                op(15, "invokeinterface", "InterfaceMethod ACNetworkContext.isClientSide:()Z"),
                op(42, "invokevirtual", "Method Level.getEntity:(I)LEntity;"),
                op(78, "invokevirtual", "Method ItemStack.getItem:()LItem;"),
                op(81, "invokevirtual", "Method ItemStack.is:(LItem;)Z"),
                op(113, "invokevirtual", "Method ItemStack.is:(LItem;)Z"),
                op(158, "invokestatic", "Method ACCompat.getTag:(LItemStack;)LCompoundTag;"),
                op(171, "invokestatic", "Method ACCompat.getTag:(LItemStack;)LCompoundTag;"),
                op(174, "invokeinterface", "InterfaceMethod UpdatesStackTags.updateTagFromServer:(LEntity;LItemStack;LCompoundTag;)V"),
                op(177, "return")
            ]}

class ReceiverDispatchTests(unittest.TestCase):
    def test_expected_classfile_roster(self):
        self.assertEqual(len({RAYGUN, PACKET, UPDATES}), 3)
        self.assertTrue(UPDATES.endswith("/UpdatesStackTags.class"))

    def test_receiving_handler_signature(self):
        m = method()
        self.assertIs(method_by_sig([m], "handle", HANDLE), m)

    def test_wrong_receiver_signature_rejected(self):
        with self.assertRaisesRegex(ReceiverProbeError, "missing/ambiguous"):
            method_by_sig([method(desc="()V")], "handle", HANDLE)

    def test_duplicate_receiver_method_rejected(self):
        with self.assertRaisesRegex(ReceiverProbeError, "missing/ambiguous"):
            method_by_sig([method(), method()], "handle", HANDLE)

    def test_duplicate_bytecode_offset_rejected(self):
        m = method()
        m["instructions"].append(op(174, "return"))
        with self.assertRaisesRegex(ReceiverProbeError, "duplicate JVM offsets"):
            method_by_sig([m], "handle", HANDLE)

    def test_positive_packet_receiver_anchors(self):
        m = method()
        for offset, (opcode, name) in ANCHORS["handle"].items():
            self.assertEqual(anchor(m, offset, opcode, name)["offset"], offset)

    def test_changed_receiver_interface_rejected(self):
        m = method()
        m["instructions"][-2]["symbol"] = "InterfaceMethod Other.updateTagFromServer:()V"
        with self.assertRaisesRegex(ReceiverProbeError, "callsite drift"):
            anchor(m, 174, "invokeinterface", "UpdatesStackTags.updateTagFromServer:")

    def test_changed_network_sender_rejected(self):
        m = method()
        m["instructions"][1]["symbol"] = "Method ACNetworkContext.getClientId:()I"
        with self.assertRaisesRegex(ReceiverProbeError, "callsite drift"):
            anchor(m, 8, "invokeinterface", "ACNetworkContext.getSender:")

    def test_method_export_limited(self):
        m = method()
        info = bounded_method(m, [174])
        self.assertEqual(info["selected_windows"][0]["at"], 174)
        self.assertEqual(len(info["parsed_method_sha256"]), 64)

    def test_bounded_method_missing_offset_rejected(self):
        with self.assertRaisesRegex(ReceiverProbeError, "window offset"):
            bounded_method(method(), [999])

    def test_detect_direct_updates_interface(self):
        output = ("Compiled from \"Fake.java\"\npublic class com.github.alexmodguy.alexscaves.server.item.RaygunItem "
                  "extends net.minecraft.world.item.Item implements "
                  "com.github.alexmodguy.alexscaves.server.item.UpdatesStackTags {\n}\n")
        parsed = class_declaration(output, RAYGUN)
        self.assertTrue(parsed["mentions_updates_interface"])
        self.assertEqual(parsed["direct_superclass_or_interface"], "net.minecraft.world.item.Item")

    def test_do_not_infer_updates_from_class_name(self):
        output = ("public class com.github.alexmodguy.alexscaves.server.item.RaygunItem "
                  "extends net.minecraft.world.item.Item {\n}\n")
        self.assertFalse(class_declaration(output, RAYGUN)["mentions_updates_interface"])

    def test_ambiguous_class_declaration_rejected(self):
        output = ("public class com.github.alexmodguy.alexscaves.server.item.RaygunItem {\n" * 2)
        with self.assertRaisesRegex(ReceiverProbeError, "ambiguous"):
            class_declaration(output, RAYGUN)

if __name__ == "__main__":
    unittest.main()
