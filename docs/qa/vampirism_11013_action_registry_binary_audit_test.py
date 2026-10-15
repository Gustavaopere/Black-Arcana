#!/usr/bin/env python3
"""Read-only 1.10.13 player-action auditor regression suite."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=HERE/"vampirism_11013_action_registry_binary_audit.py"
spec=importlib.util.spec_from_file_location("vampirism11013audit",MOD)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class VampirismCompiledActionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory()
        java=HERE/"fixtures/VampirismActionRegistryFixture.java"
        subprocess.run(["javac","--release","21","-d",cls.folder.name,str(java)],
                       check=True,timeout=35,capture_output=True,text=True)
        result=subprocess.run(
            ["javap","-c","-p","-v","-classpath",cls.folder.name,"VampirismActionRegistryFixture"],
            check=True,timeout=30,capture_output=True,text=True)
        cls.compiled=result.stdout
        cls.expected={"bat":("BAT","BatVampireAction"),
                      "freeze":("FREEZE","FreezeVampireAction")}
    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_catalog_match_exact_source_19(self):
        audit.expected()
        self.assertEqual([14,3,2],[len(x) for x in audit.GROUPS.values()])
        ids={x for group in audit.GROUPS.values() for x in group}
        self.assertEqual(19,len(ids))
        doc=(ROOT/"wiki/modpack-catalog/providers/✅-vampirism/ACTION-CATALOG.md").read_text(encoding="utf8")
        got=set(re.findall(r"^\| \d+ \| \x60vampirism:([a-z0-9_]+)\x60",doc,re.M))
        got.update(re.findall(r"^- \x60vampirism:(lord_[a-z_]+)\x60$",doc,re.M))
        self.assertEqual(ids,got)

    def test_java21_exact_deferred_holder_lambda_linkage(self):
        self.assertEqual(self.expected,audit.parse_registry(self.compiled,self.expected))

    def test_missing_action_cannot_pass(self):
        with self.assertRaises(audit.AuditError):
            audit.parse_registry(self.compiled,{"bat":self.expected["bat"]})

    def test_mutated_constructor_lambda_fails_closed(self):
        prefix,boots=self.compiled.split("BootstrapMethods:",1)
        changed=boots.replace('REF_newInvokeSpecial FreezeVampireAction."<init>"',
                              'REF_newInvokeSpecial BatVampireAction."<init>"',1)
        self.assertNotEqual(boots,changed)
        with self.assertRaises(audit.AuditError):
            audit.parse_registry(prefix+"BootstrapMethods:"+changed,self.expected)

    def test_action_literal_change_fails_closed(self):
        changed=self.compiled.replace("// String bat","// String imposter",1)
        self.assertNotEqual(changed,self.compiled)
        with self.assertRaises(audit.AuditError):
            audit.parse_registry(changed,self.expected)

    def test_removed_bus_registration_rejected(self):
        bad=self.compiled.replace('Method DeferredRegister.register:(LIEventBus;)V',
                                  'Method NoRegistry.register:(LIEventBus;)V',1)
        self.assertNotEqual(bad,self.compiled)
        with self.assertRaises(audit.AuditError):
            audit.parse_registry(bad,self.expected)

    def test_wrong_publisher_path_fails_before_java(self):
        with self.assertRaises(audit.AuditError):
            audit.audit(Path("/tmp/not-the-installed-vampirism.jar"))

if __name__=="__main__":
    unittest.main()
