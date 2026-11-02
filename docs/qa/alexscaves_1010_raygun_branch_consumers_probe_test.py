#!/usr/bin/env python3
"""Synthetic fail-closed tests: no Raygun gameplay is simulated."""
import copy
import unittest
from alexscaves_1010_raygun_branch_consumers_probe import (
    AuditError, LIMITS, REGIONS, SCOPE, inspect_selected, verify_seal,
)

def synthetic():
    offsets=sorted(set(
        list(range(460))+
        [569,570,571,574,575,578,580,600,619,625,633,635,640,643,647,
         650,657,660,665,668,669]+
        list(range(920,963))+
        list(range(1080,1123))+
        list(range(1125,1162))
    ))
    ins=[{"offset":i,"opcode":"nop","operand":"","symbol":""} for i in offsets]
    by={x["offset"]:x for x in ins}
    for off,opcode,operand,symbol in [
        (569,"iload","9",""),(571,"ifeq","669",""),
        (575,"invokevirtual","#1","Method LivingEntity.getBoundingBox:()Lx;"),
        (640,"invokestatic","#2","Method ProjectileUtil.getEntityHitResult:()Lx;"),
        (647,"ifnull","657",""),(922,"iload","18",""),
        (924,"ifeq","931",""),(927,"iconst_4","",""),
        (931,"iconst_0","",""),(932,"istore","23",""),
        (943,"invokevirtual","#3","Method Level.getEntities:()Ljava/util/List;"),
        (950,"iload","23",""),
        (1111,"sipush","800",""),
        (1114,"iload","23",""),
        (1116,"invokespecial","#5","Method MobEffectInstance.<init>:()V"),
        (1119,"invokevirtual","#6","Method LivingEntity.addEffect:()Z"),
        (1138,"iload","18",""),
        (1140,"ifeq","1147",""),(1143,"iconst_4","",""),
        (1147,"iconst_0","",""),
        (1151,"invokespecial","#4",
         "Method UpdateEffectVisualityEntityMessage.<init>:()V"),
        (1154,"invokestatic","#7","Method AlexsCaves.sendMSGToAll:()V")
    ]:
        by[off].update(opcode=opcode,operand=operand,symbol=symbol)
    return {"header":"public void onUseTick(...)",
            "descriptor":"(Ldummy;)V","instructions":ins}

def example():
    return {"scope":SCOPE,"limits":copy.deepcopy(LIMITS),
            "observations":inspect_selected(synthetic())}

class SelectedBranchConsumersTests(unittest.TestCase):
    def test_four_bounded_regions(self):
        v=inspect_selected(synthetic())
        self.assertEqual([x["name"] for x in v["regions"]],
                         [r[0] for r in REGIONS])
        self.assertEqual(len(v["regions"]),4)
        self.assertTrue(all(x["instruction_count"]<=95 for x in v["regions"]))

    def test_xray_branch_and_trace_invocation(self):
        x=inspect_selected(synthetic())["regions"][0]
        self.assertTrue(any(b["offset"]==571 and b["taken_target"]==669
                            for b in x["branch_edges"]))
        self.assertTrue(any("ProjectileUtil.getEntityHitResult:"
                            in a["symbol"] for a in x["method_calls"]))

    def test_gamma_selector_received_by_local23(self):
        v=inspect_selected(synthetic())
        x=v["regions"][1]
        self.assertTrue(any(t["offset"]==927 and t["opcode"]=="iconst_4"
                            for t in x["numeric_operands"]))
        self.assertTrue(any(t["offset"]==932 and t["opcode"]=="istore"
                            for t in x["selected_local_accesses"]))
        self.assertEqual([t["access"] for t in v["selected_slot23_accesses"]],
                         ["WRITE","READ"])

    def test_gamma_effect_request_uses_local23_and_duration(self):
        result=inspect_selected(synthetic())
        region=result["regions"][2]
        self.assertTrue(any(x["offset"]==1111 and x["operand"]=="800"
                            for x in region["numeric_operands"]))
        self.assertTrue(any(x["offset"]==1114 and x["opcode"]=="iload"
                            for x in region["selected_local_accesses"]))
        self.assertTrue(any("MobEffectInstance." in x["symbol"]
                            for x in region["method_calls"]))
        self.assertTrue(any("LivingEntity.addEffect:" in x["symbol"]
                            for x in region["method_calls"]))

    def test_visual_region_has_only_compiled_observation(self):
        v=inspect_selected(synthetic())
        self.assertTrue(any("UpdateEffectVisualityEntityMessage"
                            in m["symbol"] for m in v["regions"][3]["method_calls"]))
        self.assertIn("NOT_COMPLETE_CFG",v["interpretation"])

    def test_pinned_exact_method_drift_rejected(self):
        m=synthetic()
        next(x for x in m["instructions"] if x["offset"]==640)["symbol"]="unrelated"
        with self.assertRaisesRegex(AuditError,"pinned Raygun consumer"):
            inspect_selected(m)

    def test_missing_pinned_offset_fails(self):
        m=synthetic()
        m["instructions"]=[x for x in m["instructions"] if x["offset"]!=924]
        with self.assertRaisesRegex(AuditError,"missing pinned JVM"):
            inspect_selected(m)

    def test_missing_referenced_branch_target_fails(self):
        m=synthetic()
        x=next(x for x in m["instructions"] if x["offset"]==600)
        x["opcode"]="ifeq";x["operand"]="99999"
        with self.assertRaisesRegex(AuditError,"outside JVM instructions"):
            inspect_selected(m)

    def test_invalid_branch_operand_fails(self):
        m=synthetic()
        x=next(x for x in m["instructions"] if x["offset"]==600)
        x["opcode"]="ifeq";x["operand"]="abc"
        with self.assertRaisesRegex(AuditError,"unknown direct branch"):
            inspect_selected(m)

    def test_duplicate_jvm_instruction_fails(self):
        m=synthetic()
        m["instructions"][10]["offset"]=9
        with self.assertRaisesRegex(AuditError,"duplicate or nonmonotonic"):
            inspect_selected(m)

    def test_missing_selected_slot23_write_fails(self):
        m=synthetic()
        next(x for x in m["instructions"] if x["offset"]==932)["operand"]="24"
        with self.assertRaisesRegex(AuditError,"pinned Raygun consumer"):
            inspect_selected(m)

    def test_manifest_exact(self):
        v=example()
        self.assertTrue(verify_seal(v,copy.deepcopy(v)))

    def test_manifest_mutation_rejected(self):
        v=example()
        other=copy.deepcopy(v);other["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(AuditError,"unsafe manifest"):
            verify_seal(v,other)

    def test_manifest_delta_rejected(self):
        v=example()
        other=copy.deepcopy(v)
        other["observations"]["selected_slot23_accesses"][0]["offset"]=999
        with self.assertRaisesRegex(AuditError,"consumer seam drift"):
            verify_seal(v,other)

    def test_manifest_scope_rejected(self):
        v=example()
        other=copy.deepcopy(v);other["scope"]="WRONG"
        with self.assertRaisesRegex(AuditError,"wrong manifest scope"):
            verify_seal(v,other)

if __name__=="__main__":
    unittest.main()
