#!/usr/bin/env python3
"""Synthetic fail-closed tests for the Arrow Inducting causal anchor census."""
import unittest
from alexscaves_1010_arrow_causal_flow_probe import (
    project,EVENT,ARROW,SHA1,SHA256,SIZE)

def sample(name,descriptor="()V"):
    return {"name":name,"descriptor":descriptor,
            "method_sha256":"f"*64,"instruction_count":3,
            "refs":[{"offset":1,"opcode":"invokevirtual","operand":"#1","symbol":"Method foo:()V"}],
            "branch_edges":[{"offset":2,"opcode":"ifeq","operand":"12","symbol":""}],
            "numeric_operands":[{"offset":0,"opcode":"iconst_1","operand":"","symbol":""}]}

def fixture():
    methods=[sample("SeekingArrowEntity",f"({i})V") for i in range(11)]+[sample("tick")]
    return {"artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "classes":{EVENT:{"class_sha256":"a"*64,"parsed_method_count":34,
                              "methods":[sample("acLivingAttack")]},
                       ARROW:{"class_sha256":"b"*64,"parsed_method_count":12,
                              "methods":methods}}}

class Tests(unittest.TestCase):
    def test_bounded_projection_and_states(self):
        data=project(fixture())
        self.assertEqual(len(data["classes"][ARROW]["inspected_methods"]),12)
        self.assertEqual(data["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(data["limits"]["perk_certification"],"NOT_CERTIFIED")
    def test_missing_method_fails_closed(self):
        source=fixture()
        source["classes"][ARROW]["methods"].pop()
        with self.assertRaisesRegex(ValueError,"inventory drift"):
            project(source)
    def test_duplicate_signature_fails_closed(self):
        source=fixture()
        source["classes"][ARROW]["methods"][2]=source["classes"][ARROW]["methods"][1]
        with self.assertRaisesRegex(ValueError,"duplicate JVM"):
            project(source)
    def test_unsorted_refs_fail_closed(self):
        source=fixture()
        source["classes"][EVENT]["methods"][0]["refs"]=[
            {"offset":5,"opcode":"invokevirtual","operand":"#1","symbol":"Method x:()V"},
            {"offset":1,"opcode":"invokevirtual","operand":"#2","symbol":"Method y:()V"}]
        with self.assertRaisesRegex(ValueError,"unsorted"):
            project(source)
    def test_wrong_jar_fails_closed(self):
        source=fixture()
        source["artifact"]["sha1"]="0"*40
        with self.assertRaisesRegex(ValueError,"artifact identity"):
            project(source)
    def test_unbounded_references_fail_closed(self):
        source=fixture()
        source["classes"][EVENT]["methods"][0]["refs"]=[
            {"offset":i,"opcode":"invokevirtual","operand":"#1","symbol":"Method x:()V"}
            for i in range(181)]
        with self.assertRaisesRegex(ValueError,"unbounded"):
            project(source)

if __name__=="__main__":
    unittest.main()
