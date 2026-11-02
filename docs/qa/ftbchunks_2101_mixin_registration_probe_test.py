#!/usr/bin/env python3
"""Synthetic negative fixtures for an exact publisher read-only metadata probe."""
import copy
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

import ftbchunks_2101_mixin_registration_probe as mod

MIX = "dev/ftb/mods/ftbchunks/mixin/ExplosionAwareMixin.class"
JVM = """  public static void explosionDetonate(net.minecraft.world.level.Level a, net.minecraft.world.level.Explosion b, java.util.List c);
    descriptor: (Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/Explosion;Ljava/util/List;)V
    Code:
       0: return

"""
CALL = """  public void caller();
    descriptor: ()V
    Code:
       0: invokestatic  #1  // Method dev/ftb/mods/ftbchunks/FTBChunks.explosionDetonate:(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/Explosion;Ljava/util/List;)V
       3: return

"""

def fake_jar(path, *, config=None, meta=None, include_class=True, mixin_bytes=b"MIXIN"):
    config = config if config is not None else {
        "package":"dev.ftb.mods.ftbchunks.mixin",
        "compatibilityLevel":"JAVA_21","mixins":["ExplosionAwareMixin"],
        "client":[],"injectors":{"defaultRequire":1}
    }
    meta = meta if meta is not None else (
        '[[mixins]]\nconfig = "ftbchunks-common.mixins.json"\n'
        '[[mods]]\nmodId = "ftbchunks"\n'
    )
    with zipfile.ZipFile(path,"w") as z:
        z.writestr(mod.CONFIG,json.dumps(config))
        z.writestr(mod.TOML,meta)
        if include_class:
            z.writestr(mod.OWNER,b"\xca\xfe\xba\xbe"+b"explosionDetonate"+bytes(12800))
        z.writestr(MIX,mixin_bytes)
        z.writestr("other/DirectCaller.class",b"explosionDetonate"+bytes(600))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fake_java(args,**kwargs):
    target=args[-1]
    if "DirectCaller" in target:
        return CompletedProcess(args,0,CALL,"")
    return CompletedProcess(args,0,JVM,"")

class MixinRegistrationTests(unittest.TestCase):
    def run_fixture(self,config=None,meta=None,include_class=True,mixin_bytes=b"Explosion"):
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/mod.JAR_NAME
            digest=fake_jar(jar,config=config,meta=meta,
                            include_class=include_class,mixin_bytes=mixin_bytes)
            with patch.object(mod,"JAR_SHA256",digest),\
                 patch.object(mod.subprocess,"run",side_effect=fake_java):
                return mod.extract_jar(jar,"javap")

    def test_declared_mixin_and_jvm_reference_are_separate(self):
        r=self.run_fixture()
        self.assertEqual(r["metadata"]["declared_mixin_population"],1)
        self.assertEqual(r["direct_jvm_invocation_site_count"],1)
        self.assertEqual(r["limits"]["runtime_mixin_application"],"NOT_OBSERVED")
        self.assertEqual(r["limits"]["mutation"],"NO_MUTATION")
        self.assertTrue(mod.verify_seal(r,copy.deepcopy(r)))

    def test_absent_direct_invocation_remains_explicit(self):
        with patch("ftbchunks_2101_mixin_registration_probe.parse_methods") as parser:
            # Only the declaring method appears in synthetic javap output.
            from neoforge_211248_grief_event_probe import parse_methods as original
            parser.side_effect=lambda output: original(JVM)
            r=self.run_fixture()
        self.assertEqual(r["direct_jvm_invocation_site_count"],0)
        self.assertEqual(r["limits"]["native_explosion_dispatch"],"NOT_VERIFIED")

    def test_missing_mod_registration_rejected(self):
        with self.assertRaisesRegex(mod.EvidenceError,"register selected mixin"):
            self.run_fixture(meta='[[mods]]\nmodId = "ftbchunks"\n')

    def test_missing_modid_rejected(self):
        with self.assertRaisesRegex(mod.EvidenceError,"mod ID"):
            self.run_fixture(meta='[[mixins]]\nconfig = "ftbchunks-common.mixins.json"\n')

    def test_wrong_jar_digest_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/mod.JAR_NAME
            fake_jar(jar)
            with self.assertRaisesRegex(mod.EvidenceError,"SHA-256 drift"):
                mod.extract_jar(jar,"javap")

    def test_missing_declared_class_rejected(self):
        config={"package":"dev.ftb.mods.ftbchunks.mixin","mixins":["NotPresent"]}
        with self.assertRaisesRegex(mod.EvidenceError,"declared mixin class absent"):
            self.run_fixture(config=config)

    def test_duplicate_entries_rejected(self):
        config={"package":"dev.ftb.mods.ftbchunks.mixin",
                "mixins":["ExplosionAwareMixin","ExplosionAwareMixin"]}
        with self.assertRaisesRegex(mod.EvidenceError,"duplicate mixin"):
            self.run_fixture(config=config)

    def test_unsafe_seal_rejected(self):
        report=self.run_fixture()
        bad=copy.deepcopy(report)
        bad["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(mod.EvidenceError,"unsafe"):
            mod.verify_seal(report,bad)

    def test_tampered_mixin_hash_rejected(self):
        report=self.run_fixture()
        bad=copy.deepcopy(report)
        bad["mixins"][0]["class_sha256"]="0"*64
        with self.assertRaisesRegex(mod.EvidenceError,"seal drift"):
            mod.verify_seal(report,bad)

    def test_untrusted_package_input_rejected(self):
        config={"package":"../../foo","mixins":["ExplosionAwareMixin"]}
        with self.assertRaisesRegex(mod.EvidenceError,"invalid mixin package"):
            self.run_fixture(config=config)

if __name__=="__main__":
    unittest.main()
