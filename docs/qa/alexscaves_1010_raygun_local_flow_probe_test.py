#!/usr/bin/env python3
"""Synthetic fail-closed local-slot evidence regression tests."""
import copy
import unittest
import alexscaves_1010_raygun_local_flow_probe as probe

def synthetic():
    ins=[{"offset":k,"opcode":"nop","operand":"","symbol":""}
         for k in range(0,450)]
    ins.extend([
        {"offset":1029,"opcode":"iload","operand":"18","symbol":""},
        {"offset":1041,"opcode":"invokestatic","operand":"#10",
         "symbol":"Method ACCompat.hurt:()Z"}
    ])
    writes={22:("fstore","7"),38:("fload","7"),
            41:("fstore","8"),44:("getstatic","#1"),
            58:("istore","9"),64:("iload","9"),
            67:("fload","8"),320:("istore","18")}
    for offset,(op,operand) in writes.items():
        ins[offset]["opcode"]=op
        ins[offset]["operand"]=operand
        if offset==44:
            ins[offset]["symbol"]="Field ACEnchantmentRegistry.X_RAY:Lnet/minecraft/resources/ResourceKey;"
    return {"header":"public void onUseTick(...)","descriptor":probe.DESC,
            "instructions":ins}
def record():
    return {"scope":probe.SCOPE,"limits":copy.deepcopy(probe.LIMITS),
            "local_access_census":probe.census(synthetic())}

class LocalFlowTests(unittest.TestCase):
    def test_exact_slot_accesses_are_distinct(self):
        d=probe.census(synthetic())
        self.assertEqual(set(d["selected_slots"]),{"7","8","9","18"})
        self.assertEqual([d["selected_slots"][k]["access_count"]
                          for k in ("7","8","9","18")],[2,2,2,2])
        self.assertEqual(len(d["critical_windows"]),6)
        self.assertEqual(len(d["selected_write_windows"]),4)
        self.assertEqual(d["interpretation"],
            "SLOT_ACCESS_AND_NEARBY_INSTRUCTIONS_ONLY_NOT_REACHING_DEFINITIONS")

    def test_only_targeted_local_index(self):
        self.assertEqual(probe.local_access({"opcode":"iload","operand":"18",
                                            "symbol":"","offset":1}),(18,"READ"))
        self.assertEqual(probe.local_access({"opcode":"iinc","operand":"9, 1",
                                            "symbol":"","offset":1}),(9,"READ_WRITE"))
        self.assertEqual(probe.local_access({"opcode":"fstore","operand":"7",
                                            "symbol":"","offset":1}),(7,"WRITE"))
        self.assertIsNone(probe.local_access({"opcode":"ldc_w","operand":"7",
                                              "symbol":"","offset":1}))

    def test_implicit_jvm_local_indexes_supported(self):
        self.assertEqual(probe.local_access({"opcode":"aload_3","operand":"",
                                            "symbol":"","offset":1}),(3,"READ"))

    def test_missing_xray_anchor_fails(self):
        m=synthetic()
        m["instructions"][44]["symbol"]="Field OTHER:Lx;"
        with self.assertRaisesRegex(probe.AuditError,"critical Raygun"):
            probe.census(m)

    def test_missing_local_18_read_fails(self):
        m=synthetic()
        m["instructions"][-2]["operand"]="17"
        with self.assertRaisesRegex(probe.AuditError,"critical Raygun"):
            probe.census(m)

    def test_duplicate_offsets_fail(self):
        m=synthetic()
        m["instructions"][12]["offset"]=11
        with self.assertRaisesRegex(probe.AuditError,"duplicates"):
            probe.census(m)

    def test_wrong_local_population_fails(self):
        m=synthetic()
        m["instructions"]=m["instructions"][:300]
        with self.assertRaisesRegex(probe.AuditError,"instruction count"):
            probe.census(m)

    def test_missing_local_operand_fails_closed(self):
        with self.assertRaisesRegex(probe.AuditError,"variable index"):
            probe.local_access({"opcode":"fstore","operand":"n/a",
                                "symbol":"","offset":1})

    def test_manifest_exact_match(self):
        a=record()
        self.assertTrue(probe.verify_seal(a,copy.deepcopy(a)))

    def test_manifest_drift_fails(self):
        a=record();b=copy.deepcopy(a)
        b["local_access_census"]["selected_slots"]["18"]["accesses"][0]["offset"]=999
        with self.assertRaisesRegex(probe.AuditError,"evidence drift"):
            probe.verify_seal(a,b)

    def test_manifest_mutation_promotion_fails(self):
        a=record();b=copy.deepcopy(a)
        b["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(probe.AuditError,"seal safety"):
            probe.verify_seal(a,b)

    def test_manifest_wrong_scope_fails(self):
        a=record();b=copy.deepcopy(a)
        b["scope"]="WRONG"
        with self.assertRaisesRegex(probe.AuditError,"wrong seal scope"):
            probe.verify_seal(a,b)

if __name__=="__main__":unittest.main()
