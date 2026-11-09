#!/usr/bin/env python3
"""Fail-closed tests for exact-JVM Taxing Bellow producer/reputation contract."""
import unittest

from alexscaves_1010_taxing_bellow_static_probe import (
    ID, ENCH, ENCH_SHA, TAG_SHA, CLASSES,
    check, choose, require, proof, sha,
)


def row(off,op="nop",symbol="",operand=""):
    return {"offset":off,"opcode":op,"symbol":symbol,"operand":operand}


def method(name,ins):
    return {"header":"public void "+name+"();","descriptor":"()V","instructions":ins}


class TaxingBellowStaticTests(unittest.TestCase):
    def test_identity_and_hash_seals(self):
        self.assertEqual(ID,"alexscaves:taxing_bellow")
        self.assertEqual(ENCH,"data/alexscaves/enchantment/taxing_bellow.json")
        for value in (ENCH_SHA,TAG_SHA,*CLASSES.values()):
            self.assertEqual(len(value),64)
            self.assertTrue(all(c in "0123456789abcdef" for c in value))

    def test_known_sha(self):
        self.assertEqual(sha(b"abc"),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"expected"):
            require(False,"expected")
        self.assertIsNone(require(True,"unused"))

    def test_consumer_method_uniqueness(self):
        self.assertEqual(choose([method("releaseUsing", [row(0)])],"releaseUsing")["header"],"public void releaseUsing();")
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            choose([method("releaseUsing",[row(0)]),method("releaseUsing",[row(0)])],"releaseUsing")

    def test_missing_method_fails(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            choose([method("use",[row(0)])],"releaseUsing")

    def test_negative_reputation_literal_is_frozen(self):
        m=method("test",[row(413,"bipush","","-2")])
        check(m,{413:("bipush",None,"-2")})
        with self.assertRaisesRegex(ValueError,"CFG drift"):
            check(m,{413:("bipush",None,"-3")})

    def test_math_min_is_not_math_max(self):
        m=method("test",[row(62,"invokestatic","Method java/lang/Math.min:(II)I")])
        check(m,{62:("invokestatic","Math.min:",None)})
        with self.assertRaisesRegex(ValueError,"CFG drift"):
            check(m,{62:("invokestatic","Math.max:",None)})

    def test_branch_target_change_fails(self):
        m=method("test",[row(399,"ifeq","","418")])
        check(m,{399:("ifeq",None,"418")})
        with self.assertRaisesRegex(ValueError,"CFG drift"):
            check(m,{399:("ifeq",None,"419")})

    def test_named_method_ref_mismatch_fails(self):
        m=method("test",[row(415,"invokevirtual","DeepOneBaseEntity.addReputation:")])
        check(m,{415:("invokevirtual","addReputation:",None)})
        with self.assertRaisesRegex(ValueError,"CFG drift"):
            check(m,{415:("invokevirtual","setReputationOf:",None)})

    def test_proof_refuses_absent_offsets(self):
        with self.assertRaisesRegex(ValueError,"offset disappeared"):
            proof(method("releaseUsing",[row(0)]),"releaseUsing")


if __name__=="__main__":
    unittest.main()
