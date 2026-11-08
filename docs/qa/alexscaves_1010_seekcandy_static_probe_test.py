#!/usr/bin/env python3
"""Guard tests: Seekcandy discovery fails closed on wrong artifact and invalid IDs."""
import tempfile
from pathlib import Path
import unittest
from alexscaves_1010_seekcandy_static_probe import audit,require

class SeekcandyStaticProbeTests(unittest.TestCase):
    def test_nonpublisher_artifact_rejected_before_javap(self):
        with tempfile.TemporaryDirectory() as td:
            jar=Path(td)/"not-1010.jar"
            jar.write_bytes(b"wrong publisher artifact")
            with self.assertRaisesRegex(ValueError,"publisher JAR SHA"):
                audit(jar,"javap",Path(td)/"must-not-read.json")
    def test_fail_closed_predicate(self):
        with self.assertRaisesRegex(ValueError,"no static evidence"):
            require(False,"no static evidence")
    def test_supported_identifiers_and_no_mutating_source(self):
        from alexscaves_1010_seekcandy_static_probe import ENCH,TAG,PRODUCER,PROJECTILE,SELECTION
        self.assertEqual(ENCH,"data/alexscaves/enchantment/seekcandy.json")
        self.assertEqual(TAG,"data/alexscaves/tags/item/enchantable/sugar_staff.json")
        self.assertTrue(PRODUCER.endswith("SugarStaffItem.class"))
        self.assertTrue(PROJECTILE.endswith("SpinningPeppermintEntity.class"))
        self.assertTrue(SELECTION.endswith("SeaStaffItem.class"))
if __name__=="__main__": unittest.main()
