#!/usr/bin/env python3
"""TDD guard: Java21 compiled owner switch → constructor lambda identity."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
PROOF=HERE/"reliquified_artifacts_108_owner_link_audit.py"
spec=importlib.util.spec_from_file_location("reart_owner_proof",PROOF)
proof=importlib.util.module_from_spec(spec)
spec.loader.exec_module(proof)

class ExactOwnerLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        fixture=HERE/"fixtures/ReArtOwnerFixture.java"
        subprocess.run(["javac","--release","21","-d",cls.temp.name,str(fixture)],check=True,timeout=30)
        output=subprocess.run(["javap","-c","-p","-v","-classpath",cls.temp.name,"ReArtOwnerFixture"],check=True,text=True,capture_output=True,timeout=30)
        cls.bytecode=output.stdout
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_compiled_lambda_handle_to_exact_owner(self):
        bootstrap=proof.bootstrap_ctors(self.bytecode)
        mapping=proof.switch_mapping(self.bytecode,"redirectWearableItem",bootstrap)
        self.assertEqual({
            "plastic_drinking_hat":"HatItem",
            "novelty_drinking_hat":"HatItem",
            "snorkel":"ToolItem"
        },mapping)
        self.assertEqual({"eternal_steak":"FoodItem"},
                         proof.switch_mapping(self.bytecode,"redirectRegister",bootstrap))

    def test_hashcode_tableswitch_is_distinct_from_case_tableswitch(self):
        method=proof.code_of_method(self.bytecode,"compactHash")
        self.assertEqual(2,method.count("tableswitch"))
        actual=proof.switch_mapping(self.bytecode,"compactHash",
                                    proof.bootstrap_ctors(self.bytecode))
        self.assertEqual({"owner_45":"HatItem","owner_46":"ToolItem",
                          "owner_47":"FoodItem"},actual)

    def test_wrong_constructor_is_not_explained_away_by_matching_owner_literals(self):
        boot=proof.bootstrap_ctors(self.bytecode)
        mapping=proof.switch_mapping(self.bytecode,"redirectWearableItem",boot)
        expected=dict(mapping)
        expected["snorkel"]="HatItem"
        self.assertNotEqual(expected,mapping)
        with self.assertRaises(proof.AuditError):
            proof.require_exact_owner_classes(mapping,expected)

    def test_missing_or_modified_discriminator_fails_closed(self):
        edited=self.bytecode.replace("// String snorkel","// String forged_key",1)
        with self.assertRaises(proof.AuditError):
            proof.switch_mapping(edited,"redirectWearableItem",proof.bootstrap_ctors(edited),
                                 expected_owners={"plastic_drinking_hat","novelty_drinking_hat","snorkel"})

    def test_bootstrap_constructor_mutation_fails(self):
        prefix,bootstrap=self.bytecode.split("BootstrapMethods:",1)
        corrupt=prefix+"BootstrapMethods:"+bootstrap.replace("REF_newInvokeSpecial ReArtOwnerFixture$HatItem.","REF_invokeVirtual ReArtOwnerFixture$HatItem.",1)
        with self.assertRaises(proof.AuditError):
            proof.switch_mapping(corrupt,"redirectWearableItem",proof.bootstrap_ctors(corrupt))

    def test_real_inventory_owner_cardinality(self):
        existing=proof.load_source_owner_classes(
            (HERE.parent.parent/"wiki/modpack-catalog/providers/✅-reliquified-artifacts/ABILITY-INVENTORY-1.0.8.md").read_text(encoding="utf8")
        )
        self.assertEqual(48,len(existing))
        self.assertEqual(47,len(set(existing.values())))
        self.assertEqual("DrinkingHatItem",existing["novelty_drinking_hat"])

if __name__=="__main__":
    unittest.main()
