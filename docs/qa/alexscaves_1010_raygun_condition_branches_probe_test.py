#!/usr/bin/env python3
"""Synthetic negative tests for selected 1.0.10 Raygun JVM branches."""
import copy
import unittest
from alexscaves_1010_raygun_condition_branches_probe import (
    AuditError, DESC, LIMITS, READS, SCOPE, check_seal, selected_branches,
)

def specimen():
    indices=list(range(0,432))+[569,570,571,922,923,924,1029,1031,1034,
                                1038,1041,1138,1139,1140]
    ins=[{"offset":i,"opcode":"nop","operand":"","symbol":""}
         for i in indices]
    m={x["offset"]:x for x in ins}
    for off in READS["xray_local9"]:
        m[off].update(opcode="iload",operand="9")
    for off in READS["gamma_local18"]:
        m[off].update(opcode="iload",operand="18")
    for off in (106,123,570,368,403,923,1031,1139):
        m[off].update(opcode="ifeq",operand="1041")
    m[47].update(opcode="invokestatic",
                 symbol="Method ACCompat.enchantLevel:()I")
    m[332].update(opcode="getstatic",symbol="Field Registry.GAMMA_RAY:Key;")
    m[58].update(opcode="istore",operand="9")
    m[346].update(opcode="istore",operand="18")
    m[69].update(opcode="invokestatic",
                 symbol="Method ProjectileUtil.getHitResultOnViewVector:()V")
    m[1041].update(opcode="invokestatic",symbol="Method ACCompat.hurt:()Z")
    return {"header":"public void onUseTick(...)","descriptor":DESC,
            "instructions":ins}
def make_report():
    return {"scope":SCOPE,"limits":copy.deepcopy(LIMITS),
            "branch_observations":selected_branches(specimen())}

class BranchAuditTests(unittest.TestCase):
    def test_eight_reads_and_conditional_fallthroughs(self):
        o=selected_branches(specimen())
        reads=[x for group in o["selected_local_consumers"] for x in group["uses"]]
        self.assertEqual(len(reads),8)
        self.assertEqual([x["offset"] for x in reads],
                         [105,122,569,367,402,922,1029,1138])
        self.assertEqual(reads[0]["immediate_conditional"]["taken_target"],1041)
        self.assertEqual(reads[0]["immediate_conditional"]["fallthrough_target"],107)
        self.assertEqual(len(o["selected_producer_and_effect_anchors"]),6)

    def test_optional_nonconditional_neighbor_remains_unknown(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==106)["opcode"]="nop"
        r=selected_branches(m)
        self.assertIsNone(r["selected_local_consumers"][0]["uses"][0]["immediate_conditional"])

    def test_no_xray_slot_fails_closed(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==105)["operand"]="18"
        with self.assertRaisesRegex(AuditError,"slot identity drift"):
            selected_branches(m)

    def test_no_gamma_slot_fails_closed(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==1029)["operand"]="9"
        with self.assertRaisesRegex(AuditError,"slot identity drift"):
            selected_branches(m)

    def test_branch_target_not_an_instruction_fails(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==106)["operand"]="99999"
        with self.assertRaisesRegex(AuditError,"outside method"):
            selected_branches(m)

    def test_invalid_branch_operand_fails(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==123)["operand"]="not_an_offset"
        with self.assertRaisesRegex(AuditError,"unsupported conditional"):
            selected_branches(m)

    def test_disordered_or_repeated_offset_fails(self):
        m=specimen();m["instructions"][8]["offset"]=7
        with self.assertRaisesRegex(AuditError,"invalid Raygun JVM offsets"):
            selected_branches(m)

    def test_missing_enchant_registry_anchor_fails(self):
        m=specimen();next(x for x in m["instructions"] if x["offset"]==332)["symbol"]="Field OTHER:"
        with self.assertRaisesRegex(AuditError,"symbolic anchor drift"):
            selected_branches(m)

    def test_seal_matches_exact_same_evidence(self):
        a=make_report()
        self.assertTrue(check_seal(a,copy.deepcopy(a)))

    def test_seal_rejects_evidence_drift(self):
        a=make_report();b=copy.deepcopy(a)
        b["branch_observations"]["selected_local_consumers"][0]["uses"][0]["immediate_conditional"]["taken_target"]=999
        with self.assertRaisesRegex(AuditError,"ABI drift"):
            check_seal(a,b)

    def test_seal_rejects_unsafe_mutation(self):
        a=make_report();b=copy.deepcopy(a);b["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(AuditError,"safety-gate drift"):
            check_seal(a,b)

    def test_seal_rejects_wrong_scope(self):
        a=make_report();b=copy.deepcopy(a);b["scope"]="WRONG"
        with self.assertRaisesRegex(AuditError,"wrong evidence scope"):
            check_seal(a,b)

if __name__=="__main__":
    unittest.main()
