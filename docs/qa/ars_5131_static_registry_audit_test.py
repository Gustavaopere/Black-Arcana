#!/usr/bin/env python3
"""Fail-closed synthetic Java21 class registration tests; no upstream runtime copied."""
from pathlib import Path
import importlib.util
import subprocess
import tempfile
import unittest
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ars_binary',HERE/'ars_5131_static_registry_audit.py')
aud=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aud)
class ClassRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        subprocess.run(['javac','--release','21','-d',cls.tmp.name,str(HERE/'fixtures/ArsRegistrationFixture.java')],check=True,capture_output=True,text=True)
        r=subprocess.run(['javap','-c','-p','-classpath',cls.tmp.name,'ArsRegistrationFixture'],check=True,capture_output=True,text=True)
        cls.dis=r.stdout
        cls.spells=['MethodProjectile','EffectHarm']
        cls.rituals=['RitualFlight','RitualBinding']
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def parse(self,s=None,spells=None,rituals=None):
        return aud.parse(self.dis if s is None else s,
                         self.spells if spells is None else spells,
                         self.rituals if rituals is None else rituals,False)
    def test_manifest_exact_counts(self):
        aud.validate_manifest()
        self.assertEqual((85,24),(len(aud.SPELL_CLASSES),len(aud.RITUAL_CLASSES)))
    def test_real_java21_fixture_registers(self):
        result=self.parse()
        self.assertEqual(result['count_spell_parts'],2)
        self.assertEqual(result['count_rituals'],2)
    def test_misspelled_spell_owner_fails(self):
        with self.assertRaisesRegex(aud.AuditError,'spell-part callsite mismatch'):
            self.parse(spells=['MethodProjectile','EffectBogus'])
    def test_missing_ritual_fails(self):
        with self.assertRaisesRegex(aud.AuditError,'ritual callsite mismatch'):
            self.parse(rituals=['RitualFlight'])
    def test_wrong_holder_fails(self):
        changed=self.dis.replace('MethodProjectile.INSTANCE','OtherClass.INSTANCE',1)
        self.assertNotEqual(changed,self.dis)
        with self.assertRaisesRegex(aud.AuditError,'spell-part callsite mismatch'):
            self.parse(s=changed)
    def test_wrong_constructor_fails(self):
        changed=self.dis.replace('class RitualFlight','class OtherRitual',1)
        self.assertNotEqual(changed,self.dis)
        with self.assertRaises(aud.AuditError):self.parse(s=changed)
    def test_conditional_call_fails(self):
        # Explicit injected instruction in bounded registration region.
        needle=next(x for x in self.dis.splitlines() if 'getstatic' in x and 'EffectHarm.INSTANCE' in x)
        changed=self.dis.replace(needle, '       6: ifeq          20\n'+needle,1)
        with self.assertRaisesRegex(aud.AuditError,'conditional jump'):
            self.parse(s=changed)
    def test_exact_duplicate_publisher_legal_metadata_allowed(self):
        names=['META-INF/LICENSE.txt']*6+['META-INF/NOTICE.txt']*6+[
            'com/hollingsworth/arsnouveau/setup/registry/APIRegistry.class']
        result=aud.check_duplicate_members(names)
        self.assertEqual(result,{'META-INF/LICENSE.txt':6,'META-INF/NOTICE.txt':6})
    def test_duplicate_compiled_class_rejected(self):
        names=['META-INF/LICENSE.txt']*6+['META-INF/NOTICE.txt']*6+[
            'com/hollingsworth/arsnouveau/setup/registry/APIRegistry.class']*2
        with self.assertRaisesRegex(aud.AuditError,'outside exact legal metadata allowlist'):
            aud.check_duplicate_members(names)
    def test_unexpected_legal_metadata_count_rejected(self):
        with self.assertRaises(aud.AuditError):
            aud.check_duplicate_members(['META-INF/LICENSE.txt']*5+['META-INF/NOTICE.txt']*6)
    def test_wrong_hash_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/aud.FILENAME
            p.write_bytes(b'test')
            with self.assertRaisesRegex(aud.AuditError,'publisher size mismatch'):aud.audit(p)
    def test_duplicate_manifest_rejected(self):
        with self.assertRaisesRegex(aud.AuditError,'duplicate spell class'):
            aud.validate_manifest(['EffectHarm','EffectHarm'],[],False)
if __name__=='__main__':unittest.main()
