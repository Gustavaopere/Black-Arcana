#!/usr/bin/env python3
"""Replay repair boundary evidence without loading any game runtime."""
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SEAL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.json"


class RepairBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"))
        raw = Path(os.environ["AC_REPAIRABLE_BOUNDARY"]).read_bytes()
        cls.report = json.loads(raw)
        cls.raw = raw

    def test_report_and_safety(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), self.seal["boundary_report_sha256"])
        for key in ("scope", "mutation", "mutating_hook", "physical_qa"):
            self.assertEqual(self.report[key], self.seal[key])

    def test_native_delegates_and_bindings(self):
        self.assertEqual(self.report["native"]["spear"], self.seal["native"]["spear"])
        for owner, group in self.seal["native"]["bindings"].items():
            actual = self.report["native"]["bindings"][owner]
            self.assertEqual(actual["class_sha256"], group["class_sha256"])
            self.assertEqual(set(actual["fields"]), set(group["fields"]))
            for field, expected in group["fields"].items():
                record = actual["fields"][field]
                self.assertEqual(record["write"], expected["write"])
                self.assertIn("String " + expected["registration_name"], [s["symbol"] for s in record["context"]])

    def test_vanilla_method_identities(self):
        for owner, group in self.seal["vanilla"].items():
            actual = self.report["vanilla"]["classes"][owner]
            self.assertEqual(actual["class_sha256"], group["class_sha256"])
            self.assertEqual(actual["parent"], group["parent"])
            methods = {(m["named_method"], m["declaration"]["descriptor"]): m for m in actual["methods"]}
            self.assertEqual(len(methods), len(group["methods"]))
            for expected in group["methods"]:
                method = methods[(expected["name"], expected["descriptor"])]
                self.assertEqual(method["declaration"]["code_sha256"], expected["code_sha256"])
                self.assertEqual(method["instruction_sha256"], expected["instruction_sha256"])
                self.assertEqual(method["instruction_count"], expected["instruction_count"])

    def test_anvil_pivots(self):
        group = self.report["vanilla"]["classes"]["net.minecraft.world.inventory.AnvilMenu"]
        methods = {m["named_method"]: m for m in group["methods"]}
        create = {r["offset"]: r for r in methods["createResult"]["instructions"]}
        for offset, opcode in {172:"invokevirtual", 188:"iconst_4", 189:"idiv", 190:"invokestatic",
                               252:"invokevirtual", 255:"iinc", 268:"iconst_4", 269:"idiv",
                               275:"iinc", 284:"putfield"}.items():
            self.assertEqual(create[offset]["opcode"], opcode)
        take = {r["offset"]: r for r in methods["onTake"]["instructions"]}
        self.assertEqual(take[18]["opcode"], "ineg")
        self.assertEqual(take[76]["opcode"], "invokevirtual")
        self.assertEqual(take[127]["opcode"], "invokevirtual")

    def test_neoforge_method_and_patch_identities(self):
        for owner, group in self.seal["neoforge"]["classes"].items():
            actual = self.report["neoforge"]["classes"][owner]
            self.assertEqual(actual["present"], group["present"])
            if not group["present"]:
                continue
            self.assertEqual(actual["class_sha256"], group["class_sha256"])
            methods = {(m["declaration"]["name"], m["declaration"]["descriptor"]): m for m in actual["methods"]}
            self.assertEqual(len(methods), len(group["methods"]))
            for exp in group["methods"]:
                method = methods[(exp["name"], exp["descriptor"])]
                self.assertEqual(method["declaration"]["code_sha256"], exp["code_sha256"])
                self.assertEqual(method["instruction_sha256"], exp["instruction_sha256"])
        for path, group in self.seal["neoforge"]["patches"].items():
            actual = self.report["neoforge"]["patches"][path]
            self.assertEqual(actual["present"], group["present"])
            if group["present"]:
                self.assertEqual(actual["sha256"], group["sha256"])

    def test_certificate_matches_reports(self):
        directory = SEAL.parent
        cert = json.loads((directory / "EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
        native = json.loads((directory / "EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json").read_text(encoding="utf8"))
        self.assertEqual(cert["artifact"], native["artifact"])
        self.assertEqual(cert["direct_implementers"], native["direct_implementers"])
        self.assertEqual(cert["target_class_sha256"], native["target_class_sha256"])
        self.assertEqual(cert["native_report_sha256"], native["report_sha256"])
        self.assertEqual(cert["boundary_report_sha256"], self.seal["boundary_report_sha256"])
        self.assertEqual(cert["material_bindings"], self.seal["native"]["bindings"])
        self.assertEqual(set(cert["axes"]), {"identity", "behavior", "parameters", "targeting", "costs", "integration", "validation"})
        ledger = json.loads((ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text(encoding="utf8"))
        item = ledger["objects"]["✅-alexs-caves-continued/systems/repairable-item.md"]
        self.assertEqual(set(item["evidence"]), set(cert["axes"]))
        for field in ("claim_scope", "evidence_grade", "mutation", "mutating_hook", "physical_qa", "perk_certification", "runtime_dispatch", "provider_universe_closed"):
            self.assertEqual(item[field], cert["claims"][field])


if __name__ == "__main__":
    unittest.main()
