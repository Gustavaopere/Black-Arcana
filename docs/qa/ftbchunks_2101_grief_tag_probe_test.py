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
       4: invokevirtual  #2  // Method net/minecraft/world/entity/Entity.getType:()Lnet/minecraft/world/entity/EntityType;
       7: getstatic  #3  // Field FTBChunksTags$Entities.ENTITY_MOB_GRIEFING_BLACKLIST_TAG:Lnet/minecraft/tags/TagKey;
      10: invokevirtual  #4  // Method net/minecraft/world/entity/EntityType.is:(Lnet/minecraft/tags/TagKey;)Z
      13: ifeq  63
      17: invokevirtual  #5  // Method net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.getEntity:()Lnet/minecraft/world/entity/Entity;
      20: invokevirtual  #6  // Method net/minecraft/world/entity/Entity.level:()Lnet/minecraft/world/level/Level;
      23: invokevirtual  #7  // Method net/minecraft/world/level/Level.isClientSide:()Z
      26: ifne  63
      29: invokestatic  #8  // Method ClaimedChunkManagerImpl.getInstance:()Ldev/ftb/mods/ftbchunks/data/ClaimedChunkManagerImpl;
      32: new  #9  // class dev/ftb/mods/ftblibrary/math/ChunkDimPos
      37: invokevirtual  #10  // Method EntityMobGriefingEvent.getEntity:()Lnet/minecraft/world/entity/Entity;
      40: invokespecial  #11  // Method ChunkDimPos."<init>":(Lnet/minecraft/world/entity/Entity;)V
      43: invokevirtual  #12  // Method ClaimedChunkManagerImpl.getChunk:()Ldev/ftb/mods/ftbchunks/data/ClaimedChunkImpl;
      48: ifnull  63
      52: invokevirtual  #13  // Method ClaimedChunkImpl.allowMobGriefing:()Z
      55: ifne  63
      56: aload_1
      57: iconst_0
      60: invokevirtual  #14  // Method EntityMobGriefingEvent.setCanGrief:(Z)V
      63: return

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

    def test_denial_sets_false_in_selected_handler(self):
        method=parse_methods(BODY)[0]
        self.assertEqual(analyze_method(method)["setter_argument"],
                         "EXACT_ICONST_0_BEFORE_SET_CAN_GRIEF")

    def test_changed_denial_true_rejected(self):
        method=parse_methods(BODY.replace("iconst_0", "iconst_1"))[0]
        with self.assertRaisesRegex(EvidenceError,"literal false"):
            analyze_method(method)

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
            with patch("ftbchunks_2101_grief_tag_probe.subprocess.run",
                       side_effect=fake_javap):
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
