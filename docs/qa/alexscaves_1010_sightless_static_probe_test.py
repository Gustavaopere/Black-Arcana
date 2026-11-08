#!/usr/bin/env python3
"""Sightless static discovery fail-closed tests; no provider mutation."""
import tempfile
from pathlib import Path
import unittest
from alexscaves_1010_sightless_static_probe import evidence, require, ENCH, OWNER, TAG
class SightlessProbeGuards(unittest.TestCase):
    def test_unpinned_jar_rejected_before_javap(self):
        with tempfile.TemporaryDirectory() as temp:
            jar=Path(temp)/"invalid.jar"
            jar.write_bytes(b"not the published JAR")
            with self.assertRaisesRegex(ValueError,"publisher jar mismatch"):
                evidence(jar,"javap",Path(temp)/"unused.json",Path(temp)/"unused-astral.json")
    def test_fail_closed_assertion(self):
        with self.assertRaisesRegex(ValueError,"requires evidence"):
            require(False,"requires evidence")
    def test_identifiers_are_pinned(self):
        self.assertEqual(ENCH,"data/alexscaves/enchantment/sightless.json")
        self.assertTrue(OWNER.endswith("TotemOfPossessionItem.class"))
        self.assertEqual(TAG,"data/alexscaves/tags/item/enchantable/totem_of_possession.json")
if __name__=="__main__": unittest.main()
