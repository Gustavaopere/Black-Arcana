#!/usr/bin/env python3
"""Deterministic fail-closed tests for Sea Swing publisher discovery."""
import unittest

from alexscaves_1010_sea_swing_probe import verify_producer


def method(name, *needles):
    return {"name": name, "pivots": [{"needle": needle} for needle in needles]}


class SeaSwingProducerTests(unittest.TestCase):
    def test_accepts_one_mapped_producer(self):
        producer = method("hurtEnemy", "SEA_SWING:", "enchantLevel:",
                          "setLifespan:", "addFreshEntity:")
        self.assertEqual(verify_producer([producer]), "hurtEnemy")

    def test_refuses_identity_only_reference(self):
        with self.assertRaisesRegex(ValueError, "not uniquely located"):
            verify_producer([method("hurtEnemy", "SEA_SWING:", "enchantLevel:")])

    def test_refuses_two_producers(self):
        producer = method("acHurtEnemy", "SEA_SWING:", "enchantLevel:",
                          "setLifespan:", "addFreshEntity:")
        with self.assertRaisesRegex(ValueError, "not uniquely located"):
            verify_producer([producer, method("hurtEnemy", "SEA_SWING:",
                                             "enchantLevel:", "setLifespan:",
                                             "addFreshEntity:")])

    def test_ignores_unrelated_launch_method(self):
        wave = method("releaseUsing", "SEA_SWING:", "enchantLevel:",
                      "setLifespan:", "addFreshEntity:")
        with self.assertRaisesRegex(ValueError, "not uniquely located"):
            verify_producer([wave])


if __name__ == "__main__":
    unittest.main()
