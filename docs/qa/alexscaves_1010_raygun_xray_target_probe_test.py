#!/usr/bin/env python3
"""Synthetic fail-closed Raygun X_RAY tracing tests; no game runtime exercised."""
import copy
import unittest
from alexscaves_1010_raygun_xray_target_probe import (
    EXACT_DESCRIPTOR, PIVOTS, ProbeError, LIMITS, SCOPE,
    select_windows, verify_seal, digest_method,
)

ANCHOR_SYMBOLS={
    44:"Field ACEnchantmentRegistry.X_RAY:Holder;",
    69:"Method ProjectileUtil.getHitResultOnViewVector:()V",
    640:"Method ProjectileUtil.getEntityHitResult:()V",
    943:"Method net/minecraft/world/level/Level.getEntities:()V",
    1026:"Method ACDamageTypes.causeRaygunDamage:()V",
    1041:"Method ACCompat.hurt:()Z",
}
def specimen():
    offs=list(range(0,241))+[640,943,1026,1041]
    ins=[{"offset":o,"opcode":"nop","operand":"","symbol":""} for o in offs]
    for x in ins:
        if x["offset"] in ANCHOR_SYMBOLS:
            x["opcode"]="invokestatic" if x["offset"]!=44 else "getstatic"
            x["symbol"]=ANCHOR_SYMBOLS[x["offset"]]
    ins[43]["opcode"]="ifne";ins[43]["operand"]="69"
    return {"header":"public void onUseTick(net.minecraft.world.level.Level,net.minecraft.world.entity.LivingEntity,net.minecraft.world.item.ItemStack,int)",
            "descriptor":EXACT_DESCRIPTOR,"instructions":ins}

def report():
    return {"scope":SCOPE,"limits":copy.deepcopy(LIMITS),
            "selected":select_windows(specimen())}

class ExactRaygunTargetTests(unittest.TestCase):
    def test_known_pivots_have_explanation_and_bounded_windows(self):
        s=select_windows(specimen())
        self.assertEqual(len(s["windows"]),6)
        self.assertEqual([x["name"] for x in s["windows"]],list(PIVOTS))
        self.assertTrue(all(len(x["window"])<=19 for x in s["windows"]))
        self.assertEqual(len(s["reference_markers"]),6)
        self.assertEqual(s["interpretation"],
                         "BOUNDED_JVM_WINDOWS_NOT_COMPLETE_CFG_OR_RANGE_CERTIFICATION")

    def test_selected_xray_branch_is_visible_as_observation(self):
        s=select_windows(specimen())
        branches=[b for group in s["branch_neighborhoods"] if
                  group["pivot"]=="xray_enchantment" for b in group["branches"]]
        self.assertTrue(any(b["opcode"]=="ifne" for b in branches))

    def test_missing_pinned_xray_rejected(self):
        m=specimen()
        m["instructions"][44]["symbol"]="Field UNRELATED:Holder;"
        with self.assertRaisesRegex(ProbeError,"X_RAY field"):
            select_windows(m)

    def test_pinned_selector_callsite_drift_rejected(self):
        m=specimen()
        row=next(x for x in m["instructions"] if x["offset"]==640)
        row["symbol"]="Method unrelated:()V"
        with self.assertRaisesRegex(ProbeError,"entity trace"):
            select_windows(m)

    def test_pinned_damage_factory_drift_rejected(self):
        m=specimen()
        row=next(x for x in m["instructions"] if x["offset"]==1026)
        row["symbol"]="Method unrelated:()V"
        with self.assertRaisesRegex(ProbeError,"damage source"):
            select_windows(m)

    def test_duplicate_instruction_offsets_rejected(self):
        m=specimen()
        m["instructions"][10]["offset"]=9
        with self.assertRaisesRegex(ProbeError,"duplicate or unordered"):
            select_windows(m)

    def test_incomplete_instruction_population_rejected(self):
        m=specimen();m["instructions"]=m["instructions"][:50]
        with self.assertRaisesRegex(ProbeError,"instruction population"):
            select_windows(m)

    def test_seal_exactly_matches_selected_windows(self):
        a=report()
        self.assertTrue(verify_seal(a,copy.deepcopy(a)))
        bad=copy.deepcopy(a)
        bad["selected"]["windows"][0]["window"][0]["operand"]="mutated"
        with self.assertRaisesRegex(ProbeError,"evidence drift"):
            verify_seal(a,bad)

    def test_seal_rejects_unsafe_status_promotion(self):
        a=report()
        bad=copy.deepcopy(a);bad["limits"]["mutation"]="ALLOWED"
        with self.assertRaisesRegex(ProbeError,"unsafe limit"):
            verify_seal(a,bad)

    def test_seal_rejects_wrong_scope(self):
        a=report()
        bad=copy.deepcopy(a);bad["scope"]="UNVERIFIED"
        with self.assertRaisesRegex(ProbeError,"incorrect sealed scope"):
            verify_seal(a,bad)

    def test_digest_is_sensitive_to_operand_changes(self):
        before=specimen();after=copy.deepcopy(before)
        after["instructions"][43]["operand"]="1026"
        self.assertNotEqual(digest_method(before),digest_method(after))

if __name__=="__main__":
    unittest.main()
