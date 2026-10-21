#!/usr/bin/env python3
"""Original synthetic typed assignment inventory for controller, fail-closed."""
import unittest
from somake_109_controller_fields import scan,field,token
def fixture():
    body=[f"{i}: nop" for i in range(40)]
    body[11]="11: aload_0"
    body[12]="12: iload 6"
    body[13]="13: putfield #1 // Field witherDuration:I"
    body[18]="18: putfield #2 // Field witherAmplifier:I"
    body[21]="21: putfield #3 // Field impactDamage:F"
    body[30]="30: getfield #4 // Field activeTargetIds:Ljava/util/Set;"
    body[31]="31: invokeinterface #5, 2 // InterfaceMethod java/util/Set.add:(Ljava/lang/Object;)Z"
    return [("example","()V",body)]
class SurveyTests(unittest.TestCase):
    def test_typed_write_and_set_categories(self):
        r=scan(fixture())
        self.assertEqual("OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY",r["status"],r)
        self.assertEqual(1,r["method_count"])
        self.assertEqual(["witherDuration","witherAmplifier","impactDamage","activeTargetIds"],
                         [z["field"] for z in r["methods"][0]["field_sites"]])
        self.assertEqual(1,len(r["methods"][0]["set_calls"]))
        self.assertIn("not a proven",r["boundary"])
    def test_no_wither_assignment_fails(self):
        rows=fixture();rows[0][2][13]="13: nop"
        self.assertEqual("NOT_PROVED",scan(rows)["status"])
    def test_wrong_release_type_is_not_silently_normalized(self):
        a=fixture();a[0][2][13]="13: putfield #1 // Field witherDuration:F"
        r=scan(a)
        self.assertEqual("F",r["methods"][0]["field_sites"][0]["descriptor"])
    def test_method_overflow_fails(self):
        self.assertEqual("NOT_PROVED",scan(fixture()*37)["status"])
    def test_instructions_not_included_verbatim(self):
        self.assertNotIn("raw_bytecode",str(scan(fixture())))
        self.assertNotIn("JAR_BYTES",str(scan(fixture())))
if __name__=="__main__":
    unittest.main()
