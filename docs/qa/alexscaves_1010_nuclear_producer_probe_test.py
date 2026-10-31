#!/usr/bin/env python3
"""Fail-closed synthetic regression tests for NuclearExplosion producer audit."""
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_producer_probe import relevant_method, sealed


def ins(at, op="invokespecial", sym="Method NuclearExplosionEntity.<init>:()V"):
    return {"offset": at, "opcode": op, "operand": "#1", "symbol": sym}


def method(*instructions):
    return {"header": "public void test()", "descriptor": "()V",
            "instructions": list(instructions)}


class NuclearProducerTest(unittest.TestCase):
    def test_bounded_direct_constructor_reference(self):
        m = relevant_method(method(ins(0), ins(3, "return", "")))
        self.assertEqual(m["name"], "test")
        self.assertEqual(len(m["sites"]), 1)
        self.assertEqual(m["sites"][0]["at"], 0)

    def test_registry_field_reference(self):
        item = ins(5, "getstatic", "Field ACEntityRegistry.NUCLEAR_EXPLOSION:Ljava/util/function/Supplier;")
        m = relevant_method(method(item))
        self.assertEqual(m["sites"][0]["anchor"]["opcode"], "getstatic")

    def test_nonmatching_symbol_is_not_reported(self):
        self.assertIsNone(relevant_method(method(ins(0, "return", "Method Other.create:()V"))))

    def test_duplicate_offsets_fail_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate producer"):
            relevant_method(method(ins(2), ins(2)))

    def test_window_is_bounded(self):
        data = [ins(i * 3, "invokevirtual", "Method Other.ignored:()V") for i in range(30)]
        data[10] = ins(30)
        result = relevant_method(method(*data))
        self.assertLessEqual(len(result["sites"][0]["ins"]), 19)

    def test_seal_rejects_duplicate_sites(self):
        one = {"name": "test", "descriptor": "()V",
               "parsed_method_sha256": "a" * 64, "instruction_count": 1,
               "sites": [{"anchor": ins(1)}, {"anchor": ins(1)}]}
        scan = {"candidate_tokens": ["NuclearExplosionEntity"], "symbol_tokens": ["NuclearExplosionEntity"]}
        data = {"schema_version": 1, "scope": "TEST", "artifact": {}, "scan": scan,
                "candidate_classes": [], "classes_with_bytecode_references": [
                    {"class_path": "example.class", "class_sha256": "b" * 64, "selected_methods": [one]}
                ]}
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate producer site"):
            sealed(data)

    def test_strict_manifest_parser_rejects_duplicate_keys(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate snapshot key"):
            json.loads('{"scope":1,"scope":2}', object_pairs_hook=strict_pairs)



class ExactProducerSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NUCLEAR-PRODUCERS-1.0.10.json")
        cls.snapshot = json.loads(path.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)

    def test_publisher_identity_and_candidate_set(self):
        obj=self.snapshot
        self.assertEqual(obj["artifact"]["sha1"],
                         "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570")
        self.assertEqual(obj["artifact"]["size_bytes"],75279314)
        self.assertEqual(len(obj["candidate_classes"]),9)
        self.assertEqual(len(obj["classes_with_bytecode_references"]),6)

    def test_four_native_server_reference_producers(self):
        data = self.snapshot["classes_with_bytecode_references"]
        paths = {c["class_path"].rsplit("/",1)[-1]: c for c in data}
        expected = {
            "NuclearFurnaceBlockEntity.class":"destroyWhileCritical",
            "NuclearBombEntity.class":"explode",
            "NucleeperEntity.class":"explode",
            "SackOfSatingItem.class":"acInventoryTick",
        }
        for filename, method_name in expected.items():
            self.assertIn(filename,paths)
            methods = paths[filename]["selected_methods"]
            self.assertTrue(any(m["name"]==method_name for m in methods))
            self.assertTrue(any(any("NUCLEAR_EXPLOSION" in a["symbol"]
                                    for a in m["site_anchors"]) for m in methods))
        self.assertTrue(any("setIntentionalGameDesign" in a["symbol"]
                            for m in paths["SackOfSatingItem.class"]["selected_methods"]
                            for a in m["site_anchors"]))
        self.assertTrue(any("setNoGriefing" in a["symbol"]
                            for m in paths["NucleeperEntity.class"]["selected_methods"]
                            for a in m["site_anchors"]))

    def test_snapshot_reflects_distinct_client_renderer(self):
        names = {x["class_path"].rsplit("/",1)[-1]
                 for x in self.snapshot["classes_with_bytecode_references"]}
        self.assertIn("ClientProxy.class",names)
        self.assertNotIn("ACEntityRegistry.class",names)
        self.assertNotIn("MushroomCloudParticle.class",names)

if __name__ == "__main__":
    unittest.main()
