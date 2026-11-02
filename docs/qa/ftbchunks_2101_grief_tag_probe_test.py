#!/usr/bin/env python3
"""Synthetic fail-closed FTB evidence tests; not gameplay or claim QA."""
from __future__ import annotations
import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from ftbchunks_2101_grief_tag_probe import (
    CLASS_SUFFIX, TAG_PATH, METHOD_DESC, EvidenceError,
    audit, analyze_method, validate_tag, verify_seal,
)
from neoforge_211248_grief_event_probe import parse_methods

BODY = """  private void mobGriefing(net.neoforged.neoforge.event.entity.EntityMobGriefingEvent);
    descriptor: (Lnet/neoforged/neoforge/event/entity/EntityMobGriefingEvent;)V
    Code:
       0: aload_1
       1: invokevirtual  #1  // Method net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.getEntity:()Lnet/minecraft/world/entity/Entity;
       4: getstatic  #2  // Field FTBChunksTags$Entities.ENTITY_MOB_GRIEFING_BLACKLIST_TAG:Lnet/minecraft/tags/TagKey;
       7: invokevirtual  #3  // Method net/minecraft/world/entity/Entity.is:(Lnet/minecraft/tags/TagKey;)Z
      10: ifeq  55
      13: new  #4  // class dev/ftb/mods/ftbchunks/data/ChunkDimPos
      16: invokevirtual  #5  // Method ClaimedChunkManagerImpl.getChunk:()V
      19: invokevirtual  #6  // Method ClaimedChunkImpl.allowMobGriefing:()Z
      22: invokevirtual  #7  // Method EntityMobGriefingEvent.setCanGrief:(Z)V
      25: return

"""
CLASS = "dev/ftb/mods/ftbchunks/neoforge/NeoEventListeners.class"


def tmp_jar(path, values=None, include_class=True, include_tag=True):
    with zipfile.ZipFile(path,"w") as z:
        if include_class:
            z.writestr(CLASS, b"\xca\xfe\xba\xbe"+b"EntityMobGriefingEvent"+bytes(12000))
        if include_tag:
            z.writestr(TAG_PATH,json.dumps({"replace":False,
                        "values":values if values is not None else ["minecraft:enderman"]}))


def fake_javap(args,**kwargs):
    return CompletedProcess(args,0,BODY,"")


class ExactFtbSynthetic(unittest.TestCase):
    def test_tag_defaults_report_only_jar_local_membership(self):
        item=validate_tag(b'{"values":["minecraft:enderman"],"replace":false}')
        self.assertEqual(item["declared_values"],["minecraft:enderman"])
        self.assertFalse(item["replace"])
        self.assertIn("datapacks",item["note"])

    def test_duplicate_tag_values_rejected(self):
        with self.assertRaisesRegex(EvidenceError,"duplicate"):
            validate_tag(b'{"values":["minecraft:enderman","minecraft:enderman"]}')

    def test_bad_tag_value_rejected(self):
        with self.assertRaisesRegex(EvidenceError,"unsupported"):
            validate_tag(b'{"values":[{"unexpected":"minecraft:enderman"}]}')

    def test_selected_jvm_method_parsing(self):
        methods=parse_methods(BODY)
        self.assertEqual(len(methods),1)
        self.assertEqual(methods[0]["descriptor"],METHOD_DESC)
        report=analyze_method(methods[0])
        self.assertTrue(report["symbolic_presence"]["event_set_can_grief"])
        self.assertTrue(report["symbolic_presence"]["tag_registry_reference"])
        self.assertEqual(report["limit"],"SYMBOLS_OBSERVED_ONLY_NOT_COMPLETE_CFG")

    def test_wrong_version_name_rejected(self):
        with self.assertRaisesRegex(EvidenceError,"wrong FTB"):
            audit("ftb-chunks-neoforge-2101.1.21.jar","javap")

    def test_missing_default_tag_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ftb-chunks-neoforge-2101.1.22.jar"
            tmp_jar(p,include_tag=False)
            with self.assertRaisesRegex(EvidenceError,"blacklist tag"):
                audit(p,"javap")

    def test_ambiguous_class_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ftb-chunks-neoforge-2101.1.22.jar"
            tmp_jar(p)
            with zipfile.ZipFile(p,"a") as z:
                z.writestr("extra"+CLASS_SUFFIX,b"EntityMobGriefingEvent"+bytes(12000))
            with self.assertRaisesRegex(EvidenceError,"ambiguous"):
                audit(p,"javap")

    def test_valid_synthetic_evidence_and_seal_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ftb-chunks-neoforge-2101.1.22.jar"
            tmp_jar(p)
            with patch("ftbchunks_2101_grief_tag_probe.subprocess.run",
                       side_effect=fake_javap):
                report=audit(p,"javap")
            self.assertEqual(report["limits"]["mutation"],"NO_MUTATION")
            self.assertTrue(verify_seal(report,copy.deepcopy(report)))
            bad=copy.deepcopy(report)
            bad["default_entity_tag"]["declared_values"].append("alexscaves:tremorzilla")
            with self.assertRaisesRegex(EvidenceError,"seal drift"):
                verify_seal(report,bad)

    def test_missing_selected_handler_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ftb-chunks-neoforge-2101.1.22.jar"
            tmp_jar(p)
            def absent(args,**kwargs):
                return CompletedProcess(args,0,BODY.replace("mobGriefing","other"),"")
            with patch("ftbchunks_2101_grief_tag_probe.subprocess.run",side_effect=absent):
                with self.assertRaisesRegex(EvidenceError,"handler"):
                    audit(p,"javap")


if __name__=="__main__":
    unittest.main()
