#!/usr/bin/env python3
"""Synthetic fail-closed ABI tests, not proof of native explosion behavior."""
import copy
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from ftbchunks_2101_explosion_seam_probe import (
    CLASS_PATH, EXPLOSION_DESCRIPTOR, EvidenceError, LIMITS,
    inspect, selected_summary, verify_seal,
)
from neoforge_211248_grief_event_probe import parse_methods

PRIMARY = """  private void explosionDetonate(net.neoforged.neoforge.event.level.ExplosionEvent$Detonate);
    descriptor: (Lnet/neoforged/neoforge/event/level/ExplosionEvent$Detonate;)V
    Code:
       0: aload_1
       1: invokevirtual  #1  // Method ExplosionEvent$Detonate.getAffectedBlocks:()Ljava/util/List;
       4: invokevirtual  #2  // Method ClaimedChunkManagerImpl.getChunk:()LClaimedChunkImpl;
       7: invokevirtual  #3  // Method ClaimedChunkImpl.allowExplosions:()Z
      10: ifne  20
      13: invokeinterface  #4  // InterfaceMethod java/util/List.clear:()V
      20: return

"""
LAMBDA = """  private static void lambda$explosionDetonate$0(java.util.List);
    descriptor: (Ljava/util/List;)V
    Code:
       0: aload_0
       1: invokevirtual  #5  // Method ExplosionEvent$Detonate.getAffectedEntities:()Ljava/util/List;
       4: return

"""

def mock_java(output):
    def run(args,**kwargs):
        return CompletedProcess(args,0,output,"")
    return run

def fixture(jar,cls=b"\xca\xfe\xba\xbe"+bytes(12000)):
    with zipfile.ZipFile(jar,"w") as archive:
        archive.writestr(CLASS_PATH,cls)
    return hashlib.sha256(jar.read_bytes()).hexdigest(), hashlib.sha256(cls).hexdigest()

class ExplosionAbiTests(unittest.TestCase):
    def run_synthetic(self,bytecode=PRIMARY+LAMBDA,duplicate=False):
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/"ftb-chunks-neoforge-2101.1.22.jar"
            artifact_hash,class_hash=fixture(jar)
            import ftbchunks_2101_explosion_seam_probe as mod
            with patch.object(mod,"ARTIFACT_SHA256",artifact_hash),\
                 patch.object(mod,"CLASS_SHA256",class_hash),\
                 patch.object(mod.subprocess,"run",side_effect=mock_java(bytecode)):
                return inspect(jar,"javap")

    def test_selected_method_and_lambda(self):
        result=self.run_synthetic()
        self.assertEqual(result["primary_handler_name"],"explosionDetonate")
        self.assertEqual(len(result["selected_methods"]),2)
        self.assertTrue(result["observed_symbolic_anchors"]["explosion_affected_blocks"])
        self.assertTrue(result["observed_symbolic_anchors"]["explosion_affected_entities"])
        self.assertTrue(result["observed_symbolic_anchors"]["allow_explosions_check"])
        self.assertEqual(result["limits"],LIMITS)
        self.assertTrue(verify_seal(result,copy.deepcopy(result)))

    def test_missing_handler_is_explicitly_noncertified(self):
        result=self.run_synthetic(LAMBDA)
        self.assertEqual(result["handler_status"],
                         "NO_EXACT_SIGNATURE_IN_BOUNDED_CLASS_SCAN")
        self.assertIsNone(result["primary_handler_name"])
        self.assertEqual(result["limits"]["perk_certification"],"NOT_CERTIFIED")

    def test_duplicate_handler_fails_closed(self):
        with self.assertRaisesRegex(EvidenceError,"ambiguous exact"):
            self.run_synthetic(PRIMARY+PRIMARY)

    def test_changed_handler_descriptor_is_explicitly_noncertified(self):
        result=self.run_synthetic(PRIMARY.replace(EXPLOSION_DESCRIPTOR,"()V")+LAMBDA)
        self.assertEqual(result["handler_status"],
                         "NO_EXACT_SIGNATURE_IN_BOUNDED_CLASS_SCAN")
        self.assertIsNone(result["primary_handler_name"])

    def test_seal_detects_callsite_drift(self):
        result=self.run_synthetic()
        tampered=copy.deepcopy(result)
        tampered["selected_methods"][0]["references"][0]["symbol"]="Method unrelated:()V"
        with self.assertRaisesRegex(EvidenceError,"ABI drift"):
            verify_seal(result,tampered)

    def test_seal_rejects_perk_promotion(self):
        result=self.run_synthetic()
        tampered=copy.deepcopy(result)
        tampered["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(EvidenceError,"unsafe"):
            verify_seal(result,tampered)

    def test_zip_hash_drift_rejected(self):
        import ftbchunks_2101_explosion_seam_probe as mod
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/"ftb-chunks-neoforge-2101.1.22.jar"
            fixture(jar)
            with self.assertRaisesRegex(EvidenceError,"publisher JAR hash drift"):
                inspect(jar,"javap")

    def test_unordered_offsets_fails_closed(self):
        m=parse_methods(PRIMARY)[0]
        m["instructions"][0]["offset"]=100
        with self.assertRaisesRegex(EvidenceError,"duplicate JVM offsets"):
            selected_summary(m)

    def test_wrong_jar_name_fails_closed(self):
        with self.assertRaisesRegex(EvidenceError,"wrong FTB"):
            inspect("wrong.jar","javap")

if __name__=="__main__":
    unittest.main()
