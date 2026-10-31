#!/usr/bin/env python3
"""Fail-closed synthetic regression tests for NuclearExplosion producer audit."""
import json
import unittest

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


if __name__ == "__main__":
    unittest.main()
