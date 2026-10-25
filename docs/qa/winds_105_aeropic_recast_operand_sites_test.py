#!/usr/bin/env python3
"""Synthetic guardrails for two call-adjacent Aeropic invoke sites."""
import unittest
import winds_105_aeropic_recast_operand_sites as audit
import winds_105_spell_metadata as physical

SAMPLE = """public class net.raptorzizi.wind_spellbooks.effect.AeropicEffect {
  public boolean applyEffectTick(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: getstatic #1 // Field OTHER:Ljava/lang/Object;
      3: invokevirtual #5 // Method registry/Holder.get:()Ljava/lang/Object;
      6: checkcast #6 // class io/redspace/ironsspellbooks/api/spells/AbstractSpell
      9: iload_2
      10: aload_1
      11: invokevirtual #7 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
      14: istore_3
      15: aload_0
      16: invokestatic #8 // Method other/Use.accept:(Ljava/lang/Object;)V
  public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: aload_1
      1: invokevirtual #7 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
      4: pop
  public void onEffectRemoved(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: return
}"""

class OperandSitesTests(unittest.TestCase):
    def test_two_sites_have_bounded_symbol_context(self):
        row=audit.summarize(audit.parse_methods(SAMPLE))
        self.assertEqual("invokevirtual",row["applyEffectTick"]["invocation_opcode"])
        self.assertEqual("istore_3",row["applyEffectTick"]["immediately_after_opcode"])
        self.assertIn("registry/Holder.get:()Ljava/lang/Object;",row["applyEffectTick"]["prelude_method_refs"])
        self.assertEqual("NOT_TRACED",row["applyEffectTick"]["receiver_object"])
    def test_wrong_owner_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"exactly one"):
            audit.summarize(audit.parse_methods(SAMPLE.replace("api/spells/AbstractSpell.getRecastCount", "other/Other.getRecastCount")))
    def test_wrong_descriptor_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"exactly one"):
            audit.summarize(audit.parse_methods(SAMPLE.replace("(ILnet/minecraft/world/entity/LivingEntity;)I", "(I)I")))
    def test_wrong_invoke_opcode_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"wrong recast call opcode"):
            audit.summarize(audit.parse_methods(SAMPLE.replace("invokevirtual #7", "invokestatic #7", 1)))
    def test_missing_caller_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"missing exact"):
            audit.parse_methods(SAMPLE.replace("onEffectAdded", "someOtherMethod"))
    def test_duplicate_call_in_method_rejected(self):
        extra="      12: invokevirtual #7 // Method " + audit.RECAST + "\n"
        with self.assertRaisesRegex(audit.EvidenceError,"exactly one"):
            audit.summarize(audit.parse_methods(SAMPLE.replace("      14: istore_3", extra+"      14: istore_3")))
    def test_branched_precondition_is_not_dispatch_proof(self):
        text=SAMPLE.replace("      3: invokevirtual", "      2: ifeq 14\n      3: invokevirtual")
        row=audit.summarize(audit.parse_methods(text))
        self.assertEqual(1,row["applyEffectTick"]["prelude_branch_opcode_count"])
        self.assertEqual("NOT_TRACED",row["applyEffectTick"]["return_value_dataflow"])
    def test_wrong_sha_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"wrong Wind release"):
            audit.validate_frozen("0"*40,audit.summarize(audit.parse_methods(SAMPLE)))
    def test_unordered_offsets_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"invalid or unbounded"):
            audit.parse_methods(SAMPLE.replace("      10: aload_1", "      5: aload_1"))
    def test_no_raw_bytecode_in_evidence(self):
        row=audit.validate_frozen(physical.EXPECTED_SHA1, audit.summarize(audit.parse_methods(SAMPLE)))
        self.assertTrue(row["bytecode_context_not_published"])
        self.assertNotIn("instructions",row["call_sites"]["applyEffectTick"])

if __name__ == "__main__":
    unittest.main()
