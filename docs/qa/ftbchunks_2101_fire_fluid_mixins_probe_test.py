#!/usr/bin/env python3
"""Synthetic fail-closed fire/fluid mixin evidence tests, no gameplay testing."""
import copy
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import ftbchunks_2101_fire_fluid_mixins_probe as mod
from ftbchunks_2101_blockstate_mixin_probe_test import make_class

def write_fixture(path,classes, *, config=None, omit_class=None):
    if config is None:
        config={"package":"dev.ftb.mods.ftbchunks.core.mixin",
                "mixins":["FireBlockMixin","FlowingFluidMixin"]}
    config_data=json.dumps(config).encode()
    with zipfile.ZipFile(path,"w") as z:
        z.writestr(mod.CONFIG,config_data)
        for n,b in classes.items():
            if n!=omit_class:
                z.writestr(mod.CLASSES[n]["path"],b)
        z.writestr("padding.bin",b"x"*14500)
    return hashlib.sha256(path.read_bytes()).hexdigest(),hashlib.sha256(config_data).hexdigest()

class FireFluidMixinsTests(unittest.TestCase):
    def setUp(self):
        self.fake_classes={n:make_class() for n in mod.CLASSES}

    def fixture(self, *, config=None, classes=None, omit_class=None):
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/mod.JAR_NAME
            data=classes or self.fake_classes
            artifact_hash,config_hash=write_fixture(jar,data,config=config,
                                                   omit_class=omit_class)
            patched={n:{"path":mod.CLASSES[n]["path"],
                        "sha256":hashlib.sha256(data[n]).hexdigest()}
                     for n in data}
            with patch.object(mod,"CLASSES",patched),\
                 patch.object(mod,"JAR_SHA256",artifact_hash),\
                 patch.object(mod,"CONFIG_SHA256",config_hash):
                return mod.analyze_jar(jar)

    def test_two_selected_class_annotations(self):
        result=self.fixture()
        self.assertEqual(result["schema_version"],1)
        self.assertEqual(len(result["mixins"]),2)
        self.assertEqual([m["name"] for m in result["mixins"]],
                         ["FireBlockMixin","FlowingFluidMixin"])
        self.assertEqual([m["method_count"] for m in result["mixins"]],[1,1])
        self.assertEqual([m["method_annotation_count"] for m in result["mixins"]],[1,1])
        self.assertEqual(result["limits"]["mutation"],"NO_MUTATION")
        self.assertTrue(mod.verify_seal(result,copy.deepcopy(result)))

    def test_missing_fluid_class_rejected(self):
        with self.assertRaisesRegex(mod.AuditError,"missing exact"):
            self.fixture(omit_class="FlowingFluidMixin")

    def test_missing_fluid_declaration_rejected(self):
        config={"package":mod.SOURCE,"mixins":["FireBlockMixin"]}
        with self.assertRaisesRegex(mod.AuditError,"missing or duplicate"):
            self.fixture(config=config)

    def test_duplicate_fire_declaration_rejected(self):
        config={"package":mod.SOURCE,
                "mixins":["FireBlockMixin","FireBlockMixin","FlowingFluidMixin"]}
        with self.assertRaisesRegex(mod.AuditError,"missing or duplicate"):
            self.fixture(config=config)

    def test_wrong_package_rejected(self):
        config={"package":"unrelated.namespace","mixins":list(mod.CLASSES)}
        with self.assertRaisesRegex(mod.AuditError,"package"):
            self.fixture(config=config)

    def test_bad_jvm_classfile_rejected(self):
        classes=dict(self.fake_classes)
        classes["FireBlockMixin"]=b"invalid"
        with self.assertRaisesRegex(mod.AuditError,"JVM magic"):
            self.fixture(classes=classes)

    def test_missing_mixin_annotation_rejected(self):
        classes=dict(self.fake_classes)
        classes["FireBlockMixin"]=make_class(annotated=False)
        with self.assertRaisesRegex(mod.AuditError,"missing declared @Mixin"):
            self.fixture(classes=classes)

    def test_exact_publisher_hash_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar=Path(tmp)/mod.JAR_NAME
            write_fixture(jar,self.fake_classes)
            with self.assertRaisesRegex(mod.AuditError,"publisher exact artifact"):
                mod.analyze_jar(jar)

    def test_wrong_name_rejected(self):
        with self.assertRaisesRegex(mod.AuditError,"wrong FTB"):
            mod.analyze_jar("unrelated.jar")

    def test_manifest_drift_rejected(self):
        report=self.fixture()
        changed=copy.deepcopy(report)
        changed["mixins"][0]["annotation_types"]=[]
        with self.assertRaisesRegex(mod.AuditError,"ABI evidence drift"):
            mod.verify_seal(report,changed)

    def test_unsafe_manifest_status_rejected(self):
        report=self.fixture()
        changed=copy.deepcopy(report)
        changed["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(mod.AuditError,"safety limits"):
            mod.verify_seal(report,changed)

    def test_wrong_seal_scope_rejected(self):
        report=self.fixture()
        bad=copy.deepcopy(report);bad["scope"]="UNRELATED"
        with self.assertRaisesRegex(mod.AuditError,"scope"):
            mod.verify_seal(report,bad)

if __name__=="__main__":
    unittest.main()
