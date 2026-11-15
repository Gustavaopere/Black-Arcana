#!/usr/bin/env python3
"""Safety and version-drift negatives for the native Raygun charge discovery."""
import copy
import json
import unittest
from alexscaves_1010_energy_efficiency_probe import (
    RES, TAG, CLASS, CLASS_REG, LIMITS, PIVOTS, EXACT_ENCHANTMENT, EXACT_TAG,
    verify_config, check_pivots, verified_normal_levels, windows, method_select, unique_pairs,
)
class EnergyEfficiencyDiscoveryTests(unittest.TestCase):
    def test_scope_is_read_only_and_exact(self):
        self.assertEqual(RES,"data/alexscaves/enchantment/energy_efficiency.json")
        self.assertEqual(TAG,"data/alexscaves/tags/item/enchantable/raygun.json")
        self.assertIn("RaygunItem.class",CLASS)
        self.assertIn("ACEnchantmentRegistry.class",CLASS_REG)
        self.assertEqual(LIMITS["individual_static_certificate"],"STATIC_TECHNICAL_CATALOG_ONLY")
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

    def test_exact_publisher_metadata_and_tag_are_closed(self):
        verify_config(EXACT_ENCHANTMENT,EXACT_TAG)
        changed=copy.deepcopy(EXACT_ENCHANTMENT)
        changed["max_level"]=4
        with self.assertRaisesRegex(ValueError,"metadata"):
            verify_config(changed,EXACT_TAG)
        changed=copy.deepcopy(EXACT_TAG)
        changed["values"]=["minecraft:stick"]
        with self.assertRaisesRegex(ValueError,"tag"):
            verify_config(EXACT_ENCHANTMENT,changed)

    def test_verified_normal_divisor_and_negative_level_risk(self):
        self.assertEqual(verified_normal_levels(),{"0":2,"1":3,"2":5,"3":6})
        import math
        self.assertEqual(2+math.floor(-1*1.5),0)
        self.assertGreaterEqual(min(999+1,1000),999)
        self.assertEqual(min(1000+1,1000),1000)

    def test_exact_local_stack_pivot_drift_or_duplicate_token_rejected(self):
        rows=[{"offset":offset,"opcode":op,
               "operand":fragment if fragment.replace(" ","").isdecimal() else "",
               "symbol":fragment}
              for offset,(op,fragment) in sorted(PIVOTS.items())]
        if rows[0]["offset"]!=0:
            rows.insert(0,{"offset":0,"opcode":"aload_0","operand":"","symbol":""})
        check_pivots({"instructions":rows})
        wrong=copy.deepcopy(rows)
        for r in wrong:
            if r["offset"]==281:
                r["opcode"]="idiv"
        with self.assertRaisesRegex(ValueError,"pivot drift"):
            check_pivots({"instructions":wrong})
        duplicated=copy.deepcopy(rows)
        duplicated.append({"offset":1500,"opcode":"getstatic","operand":"",
                           "symbol":"ACEnchantmentRegistry.ENERGY_EFFICIENCY:"})
        with self.assertRaisesRegex(ValueError,"reference population"):
            check_pivots({"instructions":duplicated})

if __name__=="__main__":
    unittest.main()
