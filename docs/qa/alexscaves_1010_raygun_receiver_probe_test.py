#!/usr/bin/env python3
"""Synthetic fail-closed JVM identity/dispatch tests. No provider binary copied."""
import unittest
import copy
import json
from pathlib import Path
from alexscaves_1010_raygun_receiver_probe import (
    ANCHORS, HANDLE, PACKET, RAYGUN, UPDATES, ReceiverProbeError,
    anchor, bounded_method, class_declaration, method_by_sig, verify_sealed_report
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


    def sealed_fixture(self):
        root = Path(__file__).resolve().parents[2]
        path = (root / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
                / "EXACT-RAYGUN-RECEIVER-1.0.10.json")
        seal = json.loads(path.read_text(encoding="utf8"))
        rows = seal["class_identities"]
        report = {
            "schema_version": seal["schema_version"],
            "scope": seal["scope"], "artifact": seal["artifact"],
            "classes": [
                {**rows[0], "declaration": {
                    "direct_superclass_or_interface": seal["direct_raygun_superclass"],
                    "mentions_updates_interface": True
                }, "sender_methods": copy.deepcopy(seal["sender_methods"])},
                {**rows[1], "receiver": copy.deepcopy(seal["packet_receiver"])},
                {**rows[2], "declared_update_methods": [{
                    "declaration": seal["interface_update_method"]["declaration"],
                    "implementation": {**seal["interface_update_method"],
                                       "selected_references": [{
                                           "offset": 2, "opcode": "invokestatic",
                                           "symbol": "Method ACCompat.setTag:(LItemStack;LCompoundTag;)V"
                                       }]}
                }]},
                {**rows[3], "selected_set_tag": {
                    **seal["compat_set_tag"],
                    "selected_references": [
                        {"offset": row["offset"], "opcode": "invokevirtual",
                         "symbol": row["symbol_contains"]}
                        for row in seal["compat_custom_data_calls"]
                    ]
                }}
            ]
        }
        return report, seal

    def test_positive_exact_manifest_projection(self):
        report, seal = self.sealed_fixture()
        self.assertTrue(verify_sealed_report(report, seal))

    def test_sealed_raygun_interface_absent_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][0]["declaration"]["mentions_updates_interface"] = False
        with self.assertRaisesRegex(ReceiverProbeError, "sealed SHA-exact"):
            verify_sealed_report(report, seal)

    def test_default_method_override_drift_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][2]["declared_update_methods"][0]["declaration"] = (
            "public abstract void updateTagFromServer(...)"
        )
        with self.assertRaisesRegex(ReceiverProbeError, "sealed SHA-exact"):
            verify_sealed_report(report, seal)

    def test_set_tag_custom_data_write_drift_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][3]["selected_set_tag"]["selected_references"][-1]["symbol"] = (
            "Method OtherItem.write:(Ljava/lang/Object;)V"
        )
        with self.assertRaisesRegex(ReceiverProbeError, "write/read path drift"):
            verify_sealed_report(report, seal)

    def test_sealed_sender_method_hash_drift_rejected(self):
        report, seal = self.sealed_fixture()
        report["classes"][0]["sender_methods"][0]["parsed_method_sha256"] = "0" * 64
        with self.assertRaisesRegex(ReceiverProbeError, "sealed SHA-exact"):
            verify_sealed_report(report, seal)

    def test_receiver_snapshot_rejects_unknown_class(self):
        report, seal = self.sealed_fixture()
        report["classes"][3]["path"] = "Other.class"
        with self.assertRaisesRegex(ReceiverProbeError, "ordering/identity"):
            verify_sealed_report(report, seal)
if __name__ == "__main__":
    unittest.main()
