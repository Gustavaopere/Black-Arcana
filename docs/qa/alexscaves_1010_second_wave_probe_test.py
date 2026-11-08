#!/usr/bin/env python3
"""Fail-closed tests for Second Wave exact publisher catalog discovery."""
import tempfile
from pathlib import Path
import unittest
from alexscaves_1010_second_wave_probe import audit,require,snapshot

class SecondWaveProbeTests(unittest.TestCase):
    def test_wrong_publisher_jar_is_rejected_before_javap(self):
        with tempfile.TemporaryDirectory() as temp:
            fake=Path(temp)/"not-a-jar.jar"
            fake.write_bytes(b"not the exact publisher JAR")
            with self.assertRaisesRegex(ValueError,"wrong publisher"):
                audit(fake,"javap",Path(temp)/"not-read.json")
    def test_missing_or_ambiguous_release_is_not_a_valid_contract(self):
        with self.assertRaisesRegex(ValueError,"releaseUsing instruction population"):
            snapshot({"descriptor":"()V","instructions":[]})
    def test_fail_closed_condition(self):
        with self.assertRaisesRegex(ValueError,"no proof"):
            require(False,"no proof")

if __name__=="__main__":
    unittest.main()
