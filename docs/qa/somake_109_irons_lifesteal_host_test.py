#!/usr/bin/env python3
"""Synthetic binary string markers, no publisher JAR contents or code."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_irons_lifesteal_host import find_lifesteal_class_names

class HostSymbolIndexTests(unittest.TestCase):
    def test_identifies_owner_and_consumer_from_marker(self):
        rows=[
          ("io/redspace/ironsspellbooks/damage/SpellDamageSource.class",
           b"XgetLifestealPercentY"),
          ("io/redspace/ironsspellbooks/events/SpellDamageEvents.class",
           b"GET_LIFESTEAL_PERCENT"),
          ("example/Unrelated.class",b"damage only"),
        ]
        self.assertEqual(
          ["io.redspace.ironsspellbooks.damage.SpellDamageSource",
           "io.redspace.ironsspellbooks.events.SpellDamageEvents"],
          find_lifesteal_class_names(rows))

    def test_duplicate_archive_class_member_rejected(self):
        rows=[("example/A.class",b"lifesteal"),("example/A.class",b"lifesteal")]
        with self.assertRaises(GateError):
            find_lifesteal_class_names(rows)

    def test_suspicious_class_member_rejected(self):
        with self.assertRaises(GateError):
            find_lifesteal_class_names([("../escape.class",b"lifesteal")])

    def test_marker_absence_must_fail_closed(self):
        with self.assertRaises(GateError):
            find_lifesteal_class_names([("example/A.class",b"unrelated")])

if __name__=="__main__":
    unittest.main()
