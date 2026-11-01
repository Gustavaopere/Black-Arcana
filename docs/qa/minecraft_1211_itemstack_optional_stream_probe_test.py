#!/usr/bin/env python3
"""Synthetic fail-closed checks for official 1.21.1 vanilla codec evidence."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from minecraft_1211_itemstack_optional_stream_probe import (
    CLIENT_SHA1, MojangBoundaryError, audit, map_itemstack, parse_initializer,
    codec_class_from_initializer, named_vanilla_classes, verify_snapshot
)


MAPPING = """net.minecraft.world.item.ItemStack -> crp:
    public static final net.minecraft.network.codec.StreamCodec OPTIONAL_STREAM_CODEC -> h
    public static final net.minecraft.network.codec.StreamCodec STREAM_CODEC -> i
net.minecraft.world.item.Item -> abc:
    public static final int other -> e
"""
JAVAP = """Compiled from "ItemStack.java"
public final class crp {
  static {};
    descriptor: ()V
    Code:
       0: new           #15               // class crp$1
       3: dup
       4: invokespecial #18               // Method crp$1."<init>":()V
       7: putstatic     #20               // Field h:Lnet/minecraft/network/codec/StreamCodec;
      10: getstatic     #21               // Field i:Lnet/minecraft/network/codec/StreamCodec;
      13: putstatic     #22               // Field i:Lnet/minecraft/network/codec/StreamCodec;
}
"""


class ExactVanillaProbeTests(unittest.TestCase):
    def test_official_mapping_resolves_only_named_itemstack_field(self):
        self.assertEqual(map_itemstack(MAPPING)["class"], "crp")
        self.assertEqual(map_itemstack(MAPPING)["field"], "h")

    def test_missing_optional_field_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "did not resolve"):
            map_itemstack(MAPPING.replace("OPTIONAL_STREAM_CODEC", "SOME_OTHER"))

    def test_duplicate_mapped_field_rejected(self):
        lines = MAPPING.replace(
            "    public static final net.minecraft.network.codec.StreamCodec STREAM_CODEC -> i",
            "    public static final net.minecraft.network.codec.StreamCodec OPTIONAL_STREAM_CODEC -> i")
        with self.assertRaisesRegex(MojangBoundaryError, "duplicated"):
            map_itemstack(lines)

    def test_wrong_mapped_field_type_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "type drift"):
            map_itemstack(MAPPING.replace(
                "net.minecraft.network.codec.StreamCodec OPTIONAL_STREAM_CODEC",
                "java.lang.String OPTIONAL_STREAM_CODEC"))

    def test_bytecode_static_initializer_site(self):
        info = parse_initializer(JAVAP, "h")
        self.assertEqual(info["optional_codec_putstatic_offset"], 7)
        self.assertEqual([x["offset"] for x in info["selected_preassignment_abi"]],
                         [0, 4, 7])
        self.assertEqual(info["initializer_instruction_count"], 6)

    def test_optional_codec_class_resolves_pinned_constructor(self):
        observed = parse_initializer(JAVAP, "h")
        self.assertEqual(codec_class_from_initializer(observed), "crp$1")

    def test_ambiguous_inner_codec_constructor_rejected(self):
        observed = parse_initializer(JAVAP, "h")
        observed["selected_preassignment_abi"].append({
            "offset": 1, "opcode": "new", "symbol": "class crp$2"
        })
        with self.assertRaisesRegex(MojangBoundaryError, "ambiguous"):
            codec_class_from_initializer(observed)

    def test_missing_nearby_codec_constructor_rejected(self):
        observed = parse_initializer(JAVAP, "h")
        observed["selected_preassignment_abi"] = [
            x for x in observed["selected_preassignment_abi"] if x["opcode"] != "new"
        ]
        with self.assertRaisesRegex(MojangBoundaryError, "unresolved"):
            codec_class_from_initializer(observed)

    def test_official_mapping_resolves_codec_owner_roster(self):
        mapping = MAPPING + (
            "net.minecraft.network.RegistryFriendlyByteBuf -> wk:\n"
            "net.minecraft.core.Holder -> jm:\n"
            "net.minecraft.core.component.DataComponentPatch -> kn:\n"
        )
        names = named_vanilla_classes(mapping, ("wk", "jm", "kn"))
        self.assertEqual(names["kn"],
                         "net.minecraft.core.component.DataComponentPatch")

    def test_missing_mapped_codec_owner_fails(self):
        with self.assertRaisesRegex(MojangBoundaryError, "missing Mojang"):
            named_vanilla_classes(MAPPING, ("wk", "jm", "kn"))

    def test_missing_static_assignment_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "not unique"):
            parse_initializer(JAVAP.replace("Field h:", "Field x:"), "h")

    def test_ambiguous_static_assignment_rejected(self):
        text = JAVAP.replace("      10: getstatic", "      10: putstatic") \
                    .replace("Field i:", "Field h:")
        with self.assertRaisesRegex(MojangBoundaryError, "not unique"):
            parse_initializer(text, "h")

    def test_missing_class_initializer_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "static initializer"):
            parse_initializer(JAVAP.replace("static {};", "void notinit();"), "h")

    def test_duplicate_jvm_offset_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "duplicate JVM"):
            parse_initializer(JAVAP.replace("      10: getstatic", "       7: getstatic"), "h")

    def test_oversized_disassembly_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "oversized"):
            parse_initializer(JAVAP * 100000, "h")

    def test_bad_official_version_rejected_before_files(self):
        with self.assertRaisesRegex(MojangBoundaryError, "version metadata"):
            audit("missing.jar", "missing.map",
                  {"id": "1.21.2", "type": "release"}, "javap")

    def test_bad_client_metadata_hash_rejected(self):
        with self.assertRaisesRegex(MojangBoundaryError, "artifact SHA disagreement"):
            audit("missing.jar", "missing.map",
                  {"id": "1.21.1", "type": "release",
                   "downloads": {"client": {"sha1": "a" * 40}}}, "javap")

    def pinned_fixture(self):
        seal_path = (Path(__file__).resolve().parents[2] /
                     "wiki/modpack-catalog/providers/✅-alexs-caves-continued" /
                     "EXACT-MOJANG-1211-ITEMSTACK-STREAM-ABI.json")
        seal = json.loads(seal_path.read_text(encoding="utf8"))
        report = copy.deepcopy(seal)
        report["static_initializer"] = {
            "optional_codec_putstatic_offset": 127,
            "selected_preassignment_abi": [
                {"offset": 120, "opcode": "new", "symbol": "class cuq$1"},
                {"offset": 124, "opcode": "invokespecial",
                 "symbol": 'Method cuq$1."<init>":()V'},
                {"offset": 127, "opcode": "putstatic", "symbol": "Field h:Lyx;"}
            ]
        }
        impl = {
            "class_path": seal["codec_class_path"],
            "class_sha256": seal["codec_class_sha256"],
            "methods": []
        }
        for signature in seal["codec_method_signatures"]:
            refs = [
                {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}
                for row in seal["selected_vanilla_codec_abi"]
                if row["method"] == signature["name"]
                and row["descriptor"] == signature["descriptor"]
            ]
            impl["methods"].append({**signature, "selected_refs": refs})
        report["assigned_codec_implementation"] = impl
        return report, seal

    def test_exact_official_vanilla_snapshot(self):
        report, seal = self.pinned_fixture()
        self.assertTrue(verify_snapshot(report, seal))

    def test_codec_count_branch_drift_rejected(self):
        report, seal = self.pinned_fixture()
        decode = next(m for m in report["assigned_codec_implementation"]["methods"]
                      if m["descriptor"] == "(Lwk;)Lcuq;")
        decode["selected_refs"][1]["operand"] = "15"
        with self.assertRaisesRegex(MojangBoundaryError, "branch or delegate"):
            verify_snapshot(report, seal)

    def test_component_patch_delegate_drift_rejected(self):
        report, seal = self.pinned_fixture()
        decode = next(m for m in report["assigned_codec_implementation"]["methods"]
                      if m["descriptor"] == "(Lwk;)Lcuq;")
        decode["selected_refs"][4]["symbol"] = "Field OtherCodec.c:"
        with self.assertRaisesRegex(MojangBoundaryError, "branch or delegate"):
            verify_snapshot(report, seal)

    def test_wrong_vanilla_codec_binary_hash_rejected(self):
        report, seal = self.pinned_fixture()
        report["assigned_codec_implementation"]["class_sha256"] = "0" * 64
        with self.assertRaisesRegex(MojangBoundaryError, "anonymous ItemStack codec"):
            verify_snapshot(report, seal)

    def test_falsely_claimed_neoforge_validation_rejected(self):
        report, seal = self.pinned_fixture()
        report["limits"]["neoforge_21_1_248_merged_runtime"] = "VERIFIED"
        with self.assertRaisesRegex(MojangBoundaryError, "falsely promoted"):
            verify_snapshot(report, seal)

    def test_falsely_certified_codec_snapshot_rejected(self):
        report, seal = self.pinned_fixture()
        seal["limits"]["mutation"] = "ALLOW"
        with self.assertRaisesRegex(MojangBoundaryError, "snapshot"):
            verify_snapshot(report, seal)

    def test_wrong_downloaded_client_rejected(self):
        with patch("minecraft_1211_itemstack_optional_stream_probe.sha1_file",
                   return_value=("bad", 5)):
            with self.assertRaisesRegex(MojangBoundaryError, "client JAR identity"):
                audit("missing.jar", "missing.map", {
                    "id": "1.21.1", "type": "release",
                    "downloads": {
                        "client": {"sha1": CLIENT_SHA1, "size": 123},
                        "client_mappings": {"sha1": "f" * 40, "size": 10}
                    }
                }, "javap")


if __name__ == "__main__":
    unittest.main()
