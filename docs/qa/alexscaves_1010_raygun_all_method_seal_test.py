#!/usr/bin/env python3
"""Synthetic negative tests for the immutable Raygun JAR method fingerprint."""
import copy
import unittest

from alexscaves_1010_raygun_method_census_probe import CensusError
from alexscaves_1010_raygun_all_method_seal import (
    ARTIFACT, OWNER, CLASS_SHA256, LIMITS, PRIOR_SCOPE, projection, verify,
)

def fixture():
    rows=[]
    for i in range(26):
        count=523 if i==0 else 564 if i==1 else 1
        rows.append({
            "method": ("onUseTick ()V" if i==0 else f"m{i} ()V"),
            "instructions": count,
            "parsed_method_sha256": f"{i+1:064x}",
            "direct_branches": 107 if i==0 else 0,
            "switch_offsets": [],
        })
    return {
        "schema_version":1, "scope": PRIOR_SCOPE, "artifact": ARTIFACT,
        "class_path":OWNER, "class_sha256":CLASS_SHA256,
        "declared_methods":26, "historically_sealed_methods":8,
        "newly_surveyed_unsealed_methods":18,
        "instruction_total":1111, "direct_branch_total":107,
        "methods":rows,
        "safety":{
            "discovery_only":True, "static_perk_contract":"NOT_CERTIFIED",
            "full_method_roster_unsealed":True, "packet_sender_binding":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED", "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
        },
    }

class RaygunSealTests(unittest.TestCase):
    def test_fixture_seals_only_static_method_fingerprints(self):
        original=fixture()
        seal=projection(original)
        self.assertEqual(verify(original,seal),seal)
        self.assertEqual(seal["limits"],LIMITS)

    def test_missing_method_rejected(self):
        r=fixture()
        r["methods"].pop()
        with self.assertRaisesRegex(CensusError,"incomplete method"):
            projection(r)

    def test_duplicate_method_rejected(self):
        r=fixture()
        r["methods"][2]["method"]=r["methods"][1]["method"]
        with self.assertRaisesRegex(CensusError,"duplicated"):
            projection(r)

    def test_unknown_method_digest_rejected(self):
        r=fixture()
        r["methods"][2]["parsed_method_sha256"]="x"*64
        with self.assertRaisesRegex(CensusError,"fingerprint"):
            projection(r)

    def test_total_instruction_drift_rejected(self):
        r=fixture()
        r["methods"][1]["instructions"]-=1
        with self.assertRaisesRegex(CensusError,"population totals"):
            projection(r)

    def test_jvm_branch_excess_rejected(self):
        r=fixture()
        r["methods"][2]["direct_branches"]=2
        with self.assertRaisesRegex(CensusError,"branch count"):
            projection(r)

    def test_altered_snapshot_rejected(self):
        r=fixture()
        seal=projection(r)
        seal["methods"][4]["parsed_method_sha256"]="f"*64
        with self.assertRaisesRegex(CensusError,"fingerprint seal drift"):
            verify(r,seal)

    def test_unsafe_hook_promotion_rejected(self):
        r=fixture()
        r["safety"]["mutating_hook"]="VERIFIED"
        with self.assertRaisesRegex(CensusError,"improperly promoted"):
            projection(r)

    def test_unsafe_physical_promotion_rejected(self):
        r=fixture()
        r["safety"]["physical_qa"]="PASSED"
        with self.assertRaisesRegex(CensusError,"improperly promoted"):
            projection(r)

if __name__=="__main__":
    unittest.main()
