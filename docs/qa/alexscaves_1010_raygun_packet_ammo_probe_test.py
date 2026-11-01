#!/usr/bin/env python3
"""Synthetic fail-closed tests for SHA-exact Raygun C2S/ammo evidence."""
import copy
import unittest

from alexscaves_1010_raygun_packet_ammo_probe import (
    PacketAmmoProbeError, PACKET, RAYGUN, SENDERS,
    select, snapshot_projection, validate_sender
)


def instr(n, op, sym=""):
    return {"offset": n, "opcode": op, "symbol": sym, "operand": ""}


def method(name, instructions, desc="()V"):
    return {"header": "public void " + name + "()", "descriptor": desc,
            "instructions": instructions}


def sender(name):
    a, b = SENDERS[name]
    return method(name, [
        instr(0, "aload_0"),
        instr(a, "invokespecial",
              'Method com/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage."<init>":(ILnet/minecraft/world/item/ItemStack;)V'),
        instr(b, "invokestatic",
              "Method com/github/alexmodguy/alexscaves/AlexsCaves.sendMSGToServer:(Ljava/lang/Object;)V"),
        instr(249, "invokevirtual", "Method helper:()V") if name == "onUseTick" else instr(30, "return"),
        instr(1026, "invokestatic", "Method causeRaygunDamage:()V") if name == "onUseTick" else instr(31, "return")
    ])


class PacketAmmoSeamTests(unittest.TestCase):
    def test_expected_compiled_class_paths(self):
        self.assertTrue(RAYGUN.endswith("/RaygunItem.class"))
        self.assertTrue(PACKET.endswith("/UpdateItemTagMessage.class"))

    def test_two_actual_sender_methods(self):
        self.assertEqual(set(SENDERS), {"onUseTick", "releaseUsing"})
        self.assertEqual(validate_sender(sender("onUseTick"), (162,165))["sender_offset"], 165)
        self.assertEqual(validate_sender(sender("releaseUsing"), (25,28))["constructor_offset"], 25)

    def test_missing_constructor_is_rejected(self):
        m = sender("onUseTick")
        m["instructions"][1]["opcode"] = "invokevirtual"
        with self.assertRaisesRegex(PacketAmmoProbeError, "constructor"):
            validate_sender(m, (162,165))

    def test_changed_packet_owner_is_rejected(self):
        m = sender("onUseTick")
        m["instructions"][1]["symbol"] = 'Method OtherMessage."<init>":()V'
        with self.assertRaisesRegex(PacketAmmoProbeError, "constructor"):
            validate_sender(m, (162,165))

    def test_missing_server_dispatch_rejected(self):
        m = sender("releaseUsing")
        m["instructions"][2]["symbol"] = "Method sendMSGToClient:(Ljava/lang/Object;)V"
        with self.assertRaisesRegex(PacketAmmoProbeError, "dispatch"):
            validate_sender(m, (25,28))

    def test_duplicate_bytecode_offset_rejected(self):
        m = sender("releaseUsing")
        m["instructions"].append(instr(25, "return"))
        with self.assertRaisesRegex(PacketAmmoProbeError, "duplicate JVM"):
            validate_sender(m, (25,28))

    def test_packet_roster_requires_selected_methods(self):
        with self.assertRaisesRegex(PacketAmmoProbeError, "incomplete sender/ammo"):
            select([sender("onUseTick"), sender("releaseUsing")], set(SENDERS), raygun=True)

    def test_metadata_snapshot_drift(self):
        meta = {
            "schema_version": 1, "scope": "bounded",
            "artifact": {"sha1": "a"}, "classes": [],
            "senders": [{"method": "onUseTick", "constructor_offset": 162, "sender_offset": 165}],
        }
        first = snapshot_projection(meta)
        changed = copy.deepcopy(meta)
        changed["scope"] = "unverified"
        self.assertNotEqual(first, snapshot_projection(changed))

    def test_snapshot_projection_excludes_runtime_claim(self):
        report = {
            "schema_version": 1, "scope": "bounded",
            "artifact": {"sha1": "a"},
            "classes": [{"class_path": RAYGUN, "class_sha256": "hash",
                         "declared_method_count": 1, "selected_methods": [
                             {"name": "use", "descriptor": "()V", "instruction_count": 1,
                              "parsed_method_sha256": "x", "symbolic_references": [
                                  {"offset": 1, "symbol": "example"}]}
                         ]}],
            "senders": [],
            "limits": {"mutating_hook": "NOT_VERIFIED"}
        }
        out = snapshot_projection(report)
        self.assertNotIn("limits", out)
        self.assertNotIn("symbolic_references", out["classes"][0]["selected_methods"][0])


if __name__ == "__main__":
    unittest.main()
