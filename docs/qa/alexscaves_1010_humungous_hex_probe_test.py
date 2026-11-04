#!/usr/bin/env python3
"""Synthetic fail-closed tests for exact Humungous Hex discovery."""
import unittest
from alexscaves_1010_humungous_hex_probe import (
    EXPECTED, ITEM, HEX, ENCHANT, summarize, require, sha,
)

def m(rows, name="use"):
    return {"header":f"public void {name}();", "descriptor":"()V",
            "instructions":rows}

def row(offset, symbol=""):
    return {"offset":offset,"opcode":"invokevirtual","operand":"#1","symbol":symbol}

class HumungousHexDiscoveryTests(unittest.TestCase):
    def test_literal_exact_members(self):
        self.assertIn("SugarStaffItem.class",ITEM)
        self.assertIn("SugarStaffHexEntity.class",HEX)
        self.assertIn("humungous_hex.json",ENCHANT)
        self.assertEqual(len(EXPECTED),5)
        self.assertTrue(all(len(x)==64 for x in EXPECTED.values()))
    def test_bounded_windows_and_digest(self):
        s=summarize(m([row(0,"getHexScale:()F"),row(3),row(4,"setHexScale:(F)V")]))
        self.assertEqual(s["name"],"use")
        self.assertEqual(s["instruction_count"],3)
        self.assertEqual(s["matched_window_count"],2)
        self.assertEqual(len(s["parsed_method_sha256"]),64)
        self.assertEqual(s["selected_windows"][0]["at"],0)
    def test_unsorted_and_duplicate_offsets_fail_closed(self):
        for invalid in ([row(3),row(0)],[row(0),row(0)]):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError,"invalid or duplicate"):
                    summarize(m(invalid))
    def test_unbounded_method_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"unbounded"):
            summarize(m([row(i) for i in range(1801)]))
    def test_digest_and_guard(self):
        self.assertEqual(sha(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        with self.assertRaisesRegex(ValueError,"fail-closed"):
            require(False,"fail-closed")
if __name__=="__main__":
    unittest.main()
