#!/usr/bin/env python3
"""Independent synthetic regressions; never assert a provider-runtime result."""
import unittest
import winds_105_spell_metadata as physical
import winds_105_aeropic_local_indices as probe

SAMPLE = """public class TestEffect {
  public boolean applyEffectTick(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: aload_0
      1: iload_2
      2: aload_1
      3: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
      6: ireturn
  public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: getstatic #11 // Field net/raptorzizi/wind_spellbooks/registries/ModSpellRegistry.ACROBATICS_SPELL:Ljava/util/function/Supplier;
      3: invokeinterface #15, 1 // InterfaceMethod java/util/function/Supplier.get:()Ljava/lang/Object;
      8: checkcast #16 // class io/redspace/ironsspellbooks/api/spells/AbstractSpell
     11: astore 4
     13: aload 4
     15: iload 2
     17: aload 1
     19: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
     22: return
}"""

class LocalIndexProbeTests(unittest.TestCase):
    def run_probe(self, text=SAMPLE):
        return probe.report(physical.EXPECTED_SHA1, text)["call_sites"]["onEffectAdded"]

    def test_explicit_index_receiver_is_a_compiled_candidate_only(self):
        row = self.run_probe()
        self.assertEqual(4, row["unsuffixed_load_store_indices_parsed"])
        self.assertEqual("COMPILED_SUPPLIER_GET_CAST_RECEIVER", row["compiled_receiver_probe"])
        self.assertEqual("NOT_PROVEN", row["safe_mutating_hook"])
        self.assertEqual("NOT_PROVEN", row["dynamic_override_executed"])
        self.assertTrue(row["binary_candidate_requires_manual_review"])

    def test_wrong_local_never_aliases(self):
        row = self.run_probe(SAMPLE.replace("13: aload 4", "13: aload 5"))
        self.assertEqual("NOT_PROVEN", row["compiled_receiver_probe"])

    def test_missing_local_index_is_rejected(self):
        with self.assertRaisesRegex(probe.ProbeError, "unparseable"):
            self.run_probe(SAMPLE.replace("13: aload 4", "13: aload // malformed"))

    def test_negative_local_index_is_rejected(self):
        with self.assertRaisesRegex(probe.ProbeError, "unparseable"):
            self.run_probe(SAMPLE.replace("13: aload 4", "13: aload -1"))

    def test_invalid_u2_local_index_is_rejected(self):
        with self.assertRaisesRegex(probe.ProbeError, "exceeds unsigned"):
            self.run_probe(SAMPLE.replace("13: aload 4", "13: aload 65536"))

    def test_wrong_supplier_field_fails_closed(self):
        row = self.run_probe(SAMPLE.replace("ACROBATICS_SPELL", "WRONG_SPELL"))
        self.assertEqual("NOT_PROVEN", row["compiled_receiver_probe"])

    def test_wrong_supplier_method_fails_closed(self):
        row = self.run_probe(SAMPLE.replace("Supplier.get:", "Supplier.peek:"))
        self.assertEqual("NOT_PROVEN", row["compiled_receiver_probe"])

    def test_overwriting_source_local_fails_closed(self):
        text = SAMPLE.replace("     13: aload 4",
            "     12: aconst_null\n     13: astore 4\n     14: aload 4")
        self.assertEqual("NOT_PROVEN", self.run_probe(text)["compiled_receiver_probe"])

    def test_branch_in_expression_fails_closed(self):
        text = SAMPLE.replace("     13: aload 4",
            "     12: ifnonnull 17\n     13: aload 4")
        self.assertEqual("NOT_PROVEN", self.run_probe(text)["compiled_receiver_probe"])

    def test_exact_jar_identity_required(self):
        with self.assertRaisesRegex(probe.ProbeError, "SHA"):
            probe.report("0" * 40, SAMPLE)

    def test_duplicate_caller_rejected(self):
        text = SAMPLE.replace("  public void onEffectAdded(",
            "  public void onEffectAdded(java.lang.String);\n    Code:\n"
            "      0: return\n  public void onEffectAdded(")
        with self.assertRaisesRegex(ValueError, "overloaded"):
            self.run_probe(text)

    def test_no_gameplay_or_perk_promotion(self):
        doc = probe.report(physical.EXPECTED_SHA1, SAMPLE)
        self.assertTrue(doc["original_negative_contract_unchanged"])
        self.assertFalse(doc["published_provider_bytecode"])
        self.assertEqual("NOT_PROVEN", doc["runtime_dispatch"])
        for row in doc["call_sites"].values():
            self.assertEqual("NOT_PROVEN", row["return_value_to_PlayerRecasts"])
            self.assertEqual("NOT_PROVEN", row["safe_mutating_hook"])

if __name__ == "__main__":
    unittest.main()
