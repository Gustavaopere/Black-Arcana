#!/usr/bin/env python3
"""Synthetic SHA-exact bytecode numeric regression and sealed snapshot checks."""
import hashlib
import json
import unittest
from pathlib import Path
from alexscaves_1010_gumball_state_probe import GumballStateProbeError, strict_pairs
from alexscaves_1010_nuclear_numeric_probe import SPECS, verify_method

ROOT=Path(__file__).resolve().parents[2]
SNAP=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NUCLEAR-NUMERIC-1.0.10.json"


def mkmethod(insns):
    return {"header":"public float calculateDamage(float, float)",
            "descriptor":"(FF)F", "instructions":insns}


def instruction(offset,opcode="fconst_1",operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}


class NumericGuardTests(unittest.TestCase):
    def test_duplicate_compiled_offsets_rejected(self):
        m=mkmethod([instruction(1),instruction(1)])
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate numeric instruction"):
            verify_method(m,("0"*64,2))

    def test_method_digest_drift_rejected(self):
        m=mkmethod([instruction(0)])
        with self.assertRaisesRegex(GumballStateProbeError,"hash/length drift"):
            verify_method(m,("0"*64,1))

    def test_empty_or_wrong_method_length_rejected(self):
        m=mkmethod([instruction(0)])
        raw=json.dumps(m,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        with self.assertRaisesRegex(GumballStateProbeError,"hash/length drift"):
            verify_method(m,(hashlib.sha256(raw).hexdigest(),2))

    def test_jvm_offsets_identity_is_exact(self):
        m=mkmethod([instruction(0), instruction(1,"fmul")])
        sha=hashlib.sha256(json.dumps(m,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
        checked=verify_method(m,(sha,2))
        self.assertEqual(checked["instruction_count"],2)
        self.assertEqual(checked["instructions"][1]["opcode"],"fmul")

    def test_reject_duplicate_snapshot_json_keys(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"a":1,"a":2}',object_pairs_hook=strict_pairs)

    def test_three_method_specs_pin_prior_checksums(self):
        self.assertEqual(len(SPECS),3)
        self.assertEqual(sum(len(x["methods"]) for x in SPECS.values()),3)
        self.assertEqual(SPECS["server/entity/item/NuclearExplosionEntity.class"]["methods"][("calculateDamage","(FF)F")][1],26)

    @unittest.skipUnless(SNAP.exists(), "snapshot created after first publisher JAR CI")
    def test_exact_numeric_snapshot_structure(self):
        d=json.loads(SNAP.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        self.assertEqual(d["artifact"]["sha256"],"36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(len(d["classes"]),3)
        self.assertEqual([len(x["methods"]) for x in d["classes"]],[1,1,1])
        for cls in d["classes"]:
            relative=cls["class_path"].split("com/github/alexmodguy/alexscaves/")[1]
            self.assertEqual(cls["class_sha256"],SPECS[relative]["sha256"])
            for m in cls["methods"]:
                spec=SPECS[relative]["methods"][(m["name"],m["descriptor"])]
                self.assertEqual((m["sha256"],m["instruction_count"]),spec)
                self.assertEqual(len(m["instructions"]),spec[1])
        calc=d["classes"][0]["methods"][0]["instructions"]
        nuc=d["classes"][1]["methods"][0]["instructions"]
        bomb=d["classes"][2]["methods"][0]["instructions"]
        self.assertTrue(any("getSize:()F" in x["symbol"] for x in calc))
        self.assertTrue(any("RULE_MOBGRIEFING" in x["symbol"] for x in nuc))
        self.assertTrue(any("DoubleValue.get:()" in x["symbol"] for x in bomb))


if __name__=="__main__":
    unittest.main()
