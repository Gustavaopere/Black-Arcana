#!/usr/bin/env python3
"""Clean-room Java21 fixtures: exact Bloodlines IAction identities and fail-closed gates."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("bloodlines309binary",HERE/"bloodlines_309_action_binary_audit.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class Bloodlines309PhysicalActionAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory()
        parts=[
            "import java.util.function.Supplier;",
            "interface IEventBus {}",
            "class VampirismRegistries { static class Keys { static final Object ACTION = new Object(); } }",
            'class BloodlinesConstants { static final String MODID = "bloodlines"; }',
            "class DeferredRegister {",
            "  static DeferredRegister create(Object key,String namespace){return new DeferredRegister();}",
            "  Object register(String key,Supplier<?> supplier){return supplier.get();}",
            "  void register(IEventBus bus) {}",
            "}",
        ]
        for holder,ctor in audit.MANIFEST.values():
            parts.append(f"class {ctor} {{ public {ctor}(){{}} }}")
        parts.append("class BloodlineActions {")
        parts.append(" static final DeferredRegister ACTIONS=DeferredRegister.create(VampirismRegistries.Keys.ACTION,BloodlinesConstants.MODID);")
        for key,(holder,ctor) in audit.MANIFEST.items():
            parts.append(f' static final Object {holder}=ACTIONS.register("{key}",{ctor}::new);')
        parts.append("}")
        parts.extend([
            "public class Bloodlines {",
            "  public Bloodlines(IEventBus bus){ BloodlineActions.ACTIONS.register(bus); }",
            "}",
        ])
        filename=Path(cls.folder.name)/"Bloodlines.java"
        filename.write_text("\n".join(parts)+"\n",encoding="utf8")
        subprocess.run(["javac","--release","21","-d",cls.folder.name,str(filename)],
                       check=True,capture_output=True,text=True,timeout=30)
        def inspect(classname):
            result=subprocess.run(["javap","-v","-c","-p","-classpath",cls.folder.name,classname],
                                  capture_output=True,text=True,check=True,timeout=25)
            return result.stdout
        cls.registry=inspect("BloodlineActions")
        cls.mod_entry=inspect("Bloodlines")
    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_manifest_29_registry_28_semantic_one_excluded(self):
        audit.validate_manifest()
        self.assertEqual(29,len(audit.MANIFEST))
        self.assertIn("gravebound_crit_action",audit.MANIFEST)
        provider=(HERE.parents[1]/"wiki/modpack-catalog/providers/✅-bloodlines/ACTION-CARDS-3.0.9.md").read_text(encoding="utf8")
        for name in audit.MANIFEST:
            self.assertIn("bloodlines:"+name,provider)
        self.assertIn("EXCLUDED",provider)
    def test_real_java21_compiled_full_register_lambdas(self):
        self.assertEqual(audit.MANIFEST,audit.inspect_registry(self.registry))
    def test_real_java21_mod_constructor_register_bridge(self):
        audit.verify_main_bus(self.mod_entry,synthetic_local_bus=True)
    def test_modified_compiled_supplier_ctor_fails(self):
        first="GraveboundCritStrikeAction"
        second="GraveboundMistFormAction"
        prefix,section=self.registry.split("BootstrapMethods:",1)
        edited=section.replace("REF_newInvokeSpecial "+first+".", "REF_newInvokeSpecial "+second+".",1)
        self.assertNotEqual(section,edited)
        with self.assertRaises(audit.AuditError):
            audit.inspect_registry(prefix+"BootstrapMethods:"+edited)
    def test_modified_compiled_id_fails(self):
        changed=self.registry.replace("// String noble_celerity_action","// String synthetic_impersonator",1)
        self.assertNotEqual(changed,self.registry)
        with self.assertRaises(audit.AuditError):
            audit.inspect_registry(changed)
    def test_mod_bus_connection_fails_when_method_changed(self):
        modified=self.mod_entry.replace("DeferredRegister.register:(LIEventBus;)V",
                                        "ForeignRegistry.register:(LIEventBus;)V",1)
        self.assertNotEqual(modified,self.mod_entry)
        with self.assertRaises(audit.AuditError):
            audit.verify_main_bus(modified,synthetic_local_bus=True)
    def test_invalid_sha_never_reaches_classfile(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/audit.JAR_NAME
            path.write_bytes(b"not a publisher jar")
            with self.assertRaises(audit.AuditError):
                audit.audit(path)

if __name__=="__main__":
    unittest.main()
