#!/usr/bin/env python3
"""Synthetic Java21 compiled registry identity fixtures."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location("malum_182_rite_registry_binary_audit",HERE/"malum_182_rite_registry_binary_audit.py")
aud=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aud)
class MalumRiteAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work=tempfile.TemporaryDirectory()
        subprocess.run(["javac","--release","21","-d",cls.work.name,str(HERE/"fixtures/MalumRiteRegistryFixture.java")],check=True,timeout=25,capture_output=True,text=True)
        cp=subprocess.run(["javap","-c","-p","-v","-classpath",cls.work.name,"MalumRiteRegistryFixture"],check=True,timeout=25,capture_output=True,text=True)
        cls.bytecode=cp.stdout
        cls.identity={"undirected_rite":"UNDIRECTED_RITE","unchained_rite":"UNCHAINED_RITE"}
    @classmethod
    def tearDownClass(cls):
        cls.work.cleanup()
    def parse(self,text=None,manifest=None):
        return aud.parse_registry(text or self.bytecode,self.identity if manifest is None else manifest,"MalumRiteRegistryFixture")
    def test_26_unique_rites_manifest(self):
        aud.validate_manifest()
        self.assertEqual(26,len(aud.RITES))
        self.assertEqual("RITE_OF_RAISING",aud.RITES["rite_of_rending"])
        self.assertNotIn("undirected_rite_effect",aud.RITES)
    def test_exact_literal_registry_and_factory(self):
        self.assertEqual({k:v["holder"] for k,v in self.parse().items()},self.identity)
    def test_missing_register_fails(self):
        with self.assertRaisesRegex(aud.AuditError,"compiled identities differ"):
            self.parse(manifest={"undirected_rite":"UNDIRECTED_RITE"})
    def test_forged_id_fails(self):
        x=self.bytecode.replace("// String undirected_rite","// String forged_rite",1)
        with self.assertRaises(aud.AuditError):self.parse(x)
    def test_wrong_holder_fails(self):
        x=self.bytecode.replace("Field UNDIRECTED_RITE:LRiteHolder","Field FAKE_RITE:LRiteHolder",1)
        with self.assertRaisesRegex(aud.AuditError,"holder mismatch"):self.parse(x)
    def test_foreign_lambda_fails(self):
        a,b=self.bytecode.split("BootstrapMethods:",1)
        c=b.replace("REF_invokeStatic MalumRiteRegistryFixture.lambda$static$1:","REF_invokeStatic ForeignRegistry.lambda$static$1:",1)
        self.assertNotEqual(c,b)
        with self.assertRaisesRegex(aud.AuditError,"lambda does not belong"):self.parse(a+"BootstrapMethods:"+c)
    def test_wrong_publisher_hash_fails(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/aud.FILENAME
            path.write_bytes(b"not physical jar")
            with self.assertRaisesRegex(aud.AuditError,"physically SHA1-equal"):aud.audit(path)
if __name__=="__main__":
    unittest.main()
