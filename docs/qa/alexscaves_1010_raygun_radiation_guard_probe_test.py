#!/usr/bin/env python3
"""Fail-closed synthetic tests for Raygun radiation-resistance boundaries."""
import copy
import json
import unittest

from alexscaves_1010_raygun_radiation_guard_probe import (
    AuditError, LIMITS, SCOPE, inspect_default_tag,
    probe_method, verify_seal,
)

def specimen():
    offsets=list(range(465))+[953]+list(range(1025,1162))
    ins=[{"offset":i,"opcode":"nop","operand":"","symbol":""} for i in offsets]
    by={x["offset"]:x for x in ins}
    declarations={
        1041:("invokestatic","#1","Method ACCompat.hurt:()Z"),
        1044:("ifeq","1051",""),
        1080:("getstatic","#2","Field ACTagRegistry.RESISTS_RADIATION:Lnet/minecraft/tags/TagKey;"),
        1085:("invokevirtual","#3","Method Holder$Reference.is:(Lnet/minecraft/tags/TagKey;)Z"),
        1088:("ifne","1157",""),
        1095:("getstatic","#4","Field ACEffectRegistry.IRRADIATED:Ljava/util/function/Supplier;"),
        1111:("sipush","800",""),1114:("iload","23",""),
        1116:("invokespecial","#5","Method MobEffectInstance.<init>:(LHolder;II)V"),
        1119:("invokevirtual","#6","Method LivingEntity.addEffect:(LMobEffectInstance;)Z"),
        1122:("ifeq","1157",""),
        1151:("invokespecial","#7","Method UpdateEffectVisualityEntityMessage.<init>:(IIII)V"),
        1154:("invokestatic","#8","Method AlexsCaves.sendMSGToAll:(Ljava/lang/Object;)V"),
        1157:("goto","953",""),
    }
    for at,(op,operand,sym) in declarations.items():
        by[at].update(opcode=op,operand=operand,symbol=sym)
    return {"header":"public void onUseTick(...)","descriptor":"(Ldummy;)V",
            "instructions":ins}

def sealed():
    return {"scope":SCOPE,"limits":copy.deepcopy(LIMITS),
            "radiation_guard_method":probe_method(specimen())}

class RadiationGuardTests(unittest.TestCase):
    def test_six_exact_marker_families_and_edges(self):
        r=probe_method(specimen())
        self.assertEqual(len(r["symbols_with_local_context"]),6)
        self.assertEqual(
            [x["name"] for x in r["symbols_with_local_context"]],
            ["resistance_tag","irradiated_effect","resistance_test",
             "native_hurt_request","status_request","visual_notification"],
        )
        self.assertEqual(
            [(x["offset"],x["taken_target"]) for x in r["selected_branch_edges"]],
            [(1044,1051),(1088,1157),(1122,1157),(1157,953)],
        )

    def test_mismatched_radiation_tag_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1080)["symbol"]="Field WRONG_TAG:Lx;"
        with self.assertRaisesRegex(AuditError,"missing radiation marker resistance_tag"):
            probe_method(m)

    def test_wrong_irradiated_effect_registry_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1095)["symbol"]="Field WRONG:Lx;"
        with self.assertRaisesRegex(AuditError,"missing radiation marker irradiated_effect"):
            probe_method(m)

    def test_resistance_guard_jump_drift_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1088)["operand"]="1154"
        with self.assertRaisesRegex(AuditError,"pinned radiation ABI drift"):
            probe_method(m)

    def test_effect_result_guard_jump_drift_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1122)["operand"]="1154"
        with self.assertRaisesRegex(AuditError,"pinned radiation ABI drift"):
            probe_method(m)

    def test_visual_message_drift_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1154)["symbol"]="Method unrelated:"
        with self.assertRaisesRegex(AuditError,"pinned radiation ABI drift"):
            probe_method(m)

    def test_duplicate_marker_rejected(self):
        m=specimen()
        next(x for x in m["instructions"] if x["offset"]==1078)["symbol"]="Field ACTagRegistry.RESISTS_RADIATION:Lx;"
        with self.assertRaisesRegex(AuditError,"ambiguous or missing radiation marker"):
            probe_method(m)

    def test_bad_jvm_offset_population_rejected(self):
        m=specimen();m["instructions"][3]["offset"]=2
        with self.assertRaisesRegex(AuditError,"duplicate or unordered JVM offsets"):
            probe_method(m)

    def test_publisher_tag_values_captured_not_as_runtime_truth(self):
        data={"values":["alexscaves:radgill","alexscaves:raycat"],
              "replace":False}
        out=inspect_default_tag(json.dumps(data).encode("utf8"))
        self.assertEqual(out["value_count"],2)
        self.assertFalse(out["replace_effective_default"])
        self.assertEqual(out["interpretation"],
                         "PUBLISHER_DEFAULT_NOT_EFFECTIVE_RUNTIME_REGISTRY")

    def test_bad_tag_type_rejected(self):
        with self.assertRaisesRegex(AuditError,"required tag value type"):
            inspect_default_tag(b'{"values":[{"id":"alexscaves:raycat"}]}')

    def test_duplicate_tag_values_rejected(self):
        with self.assertRaisesRegex(AuditError,"tag values or duplication"):
            inspect_default_tag(b'{"values":["alexscaves:raycat","alexscaves:raycat"]}')

    def test_seal_equal(self):
        x=sealed()
        self.assertTrue(verify_seal(x,copy.deepcopy(x)))

    def test_seal_drift_rejected(self):
        x=sealed();y=copy.deepcopy(x)
        y["radiation_guard_method"]["selected_branch_edges"][1]["taken_target"]=0
        with self.assertRaisesRegex(AuditError,"evidence drift"):
            verify_seal(x,y)

    def test_unsafe_seal_promotion_rejected(self):
        x=sealed();y=copy.deepcopy(x);y["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(AuditError,"unsafe limits"):
            verify_seal(x,y)

    def test_wrong_scope_rejected(self):
        x=sealed();y=copy.deepcopy(x);y["scope"]="WRONG"
        with self.assertRaisesRegex(AuditError,"wrong static guard"):
            verify_seal(x,y)

if __name__=="__main__":
    unittest.main()
