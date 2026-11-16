#!/usr/bin/env python3
"""Synthetic negative certification tests; no Minecraft gameplay assertion."""
import copy
import unittest

from alexscaves_1010_ferrous_haste_causal_audit import AuditError, branches
from alexscaves_1010_field_extension_causal_audit import (
    PIVOTS, load_cert, validate_individual_seal,
)

def fake_report(cert):
    return {
        "enchantment": cert["enchantment"],
        "claim_scope": cert["claim_scope"], "evidence_grade": cert["evidence_grade"],
        "artifact": copy.deepcopy(cert["artifact"]),
        "resources": copy.deepcopy(cert["resources"]),
        "resource_json": copy.deepcopy(cert["resource_json"]),
        "supported_item_tag": copy.deepcopy(cert["supported_item_tag"]),
        "class_sha256": copy.deepcopy(cert["class_sha256"]),
        "compiled_field_extension_token_owners":
            copy.deepcopy(cert["compiled_field_extension_token_owners"]),
        "census": copy.deepcopy(cert["census"]),
        "pivots": copy.deepcopy(cert["pivots"]),
        "safety": copy.deepcopy(cert["safety"]),
    }

class FieldExtensionStaticContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = load_cert()

    def test_native_static_contract_fixture(self):
        self.assertEqual(len(PIVOTS), len(self.cert["pivots"]))
        validate_individual_seal(fake_report(self.cert), self.cert)

    def test_wrong_version_or_publisher_rejected(self):
        s = copy.deepcopy(self.cert)
        s["version"] = "1.1.1"
        with self.assertRaisesRegex(AuditError, "identity drift"):
            validate_individual_seal(fake_report(self.cert), s)
        report = fake_report(self.cert)
        report["artifact"]["size_bytes"] -= 1
        with self.assertRaisesRegex(AuditError, "publisher artifact"):
            validate_individual_seal(report, self.cert)

    def test_wrong_resource_or_class_digest_rejected(self):
        report = fake_report(self.cert)
        report["resources"]["data/alexscaves/enchantment/field_extension.json"] = "0" * 64
        with self.assertRaisesRegex(AuditError, "resources"):
            validate_individual_seal(report, self.cert)
        report = fake_report(self.cert)
        key = next(iter(report["class_sha256"]))
        report["class_sha256"][key] = "0" * 64
        with self.assertRaisesRegex(AuditError, "class_sha256"):
            validate_individual_seal(report, self.cert)

    def test_unreviewed_token_owner_rejected(self):
        report = fake_report(self.cert)
        report["compiled_field_extension_token_owners"].append("other/Owner.class")
        with self.assertRaisesRegex(AuditError, "token_owners"):
            validate_individual_seal(report, self.cert)

    def test_full_method_hash_drift_rejected(self):
        report = fake_report(self.cert)
        report["census"]["method_census"][0]["parsed_method_sha256"] = "f" * 64
        with self.assertRaisesRegex(AuditError, "census"):
            validate_individual_seal(report, self.cert)

    def test_wrong_range_pivot_rejected(self):
        report = fake_report(self.cert)
        x = next(r for r in report["pivots"] if r["offset"] == 639)
        x["symbol"] = "float 6.0f"
        with self.assertRaisesRegex(AuditError, "pivots"):
            validate_individual_seal(report, self.cert)

    def test_unbounded_attack_route_rejected(self):
        report = fake_report(self.cert)
        x = next(r for r in report["pivots"] if r["offset"] == 683)
        x["operand"] = "928"
        with self.assertRaisesRegex(AuditError, "pivots"):
            validate_individual_seal(report, self.cert)

    def test_unsafe_hook_and_physical_promotion_rejected(self):
        for key, value in [
            ("mutating_hook", "VERIFIED"), ("physical_qa", "PASSED"),
            ("mutation", "ALLOW_MUTATION"), ("provider_universe_closed", True),
        ]:
            with self.subTest(key=key):
                s = copy.deepcopy(self.cert)
                s["safety"][key] = value
                with self.assertRaisesRegex(AuditError, "unsafe hook"):
                    validate_individual_seal(fake_report(s), s)

    def test_raw_branch_destination_drift_rejected(self):
        # Full JVM branch verification rejects a missing destination in a
        # deliberately tiny malformed method, independent of row count.
        method = {"instructions": [
            {"offset": 0, "opcode": "ifeq", "operand": "99", "symbol": ""},
            {"offset": 3, "opcode": "return", "operand": "", "symbol": ""},
        ]}
        with self.assertRaisesRegex(AuditError, "branch destination"):
            branches(method)

if __name__ == "__main__":
    unittest.main()
