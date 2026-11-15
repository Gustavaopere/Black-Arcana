#!/usr/bin/env python3
"""Safety and version-drift negatives for the native Raygun charge discovery."""
import copy
import json
import unittest
from alexscaves_1010_energy_efficiency_probe import (
    RES, TAG, CLASS, CLASS_REG, LIMITS, windows, method_select, unique_pairs,
)
class EnergyEfficiencyDiscoveryTests(unittest.TestCase):
    def test_scope_is_read_only_and_exact(self):
        self.assertEqual(RES,"data/alexscaves/enchantment/energy_efficiency.json")
        self.assertEqual(TAG,"data/alexscaves/tags/item/enchantable/raygun.json")
        self.assertIn("RaygunItem.class",CLASS)
        self.assertIn("ACEnchantmentRegistry.class",CLASS_REG)
        self.assertEqual(LIMITS["individual_static_certificate"],"PENDING_JVM_CAUSAL_SEAL")
        self.assertEqual(LIMITS["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(LIMITS["physical_qa"],"NOT_TESTED")
        self.assertEqual(LIMITS["mutation"],"NO_MUTATION")

    def test_duplicate_publisher_keys_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate JSON key"):
            json.loads('{"max_level":3,"max_level":1}',object_pairs_hook=unique_pairs)

    def test_method_identity_exact(self):
        method={"header":"public void onUseTick(...)", "descriptor":"()V",
                "instructions":[]}
        self.assertIs(method_select([method],"onUseTick","()V"),method)
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            method_select([method,method],"onUseTick","()V")
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            method_select([method],"onUseTick","(I)V")

    def test_window_requires_exact_order_and_rejects_aliases(self):
        rows=[{"offset":180+i,"opcode":"nop","operand":"","symbol":""}
              for i in range(35)]
        self.assertEqual(len(windows(rows)),35)
        with self.assertRaisesRegex(ValueError,"ordering"):
            windows(rows+[copy.deepcopy(rows[0])])
        with self.assertRaisesRegex(ValueError,"population"):
            windows(rows[:4])
if __name__=="__main__":
    unittest.main()
