#!/usr/bin/env python3
"""Synthetic strict slice and uncertainty tests, no third-party code."""
import unittest
import winds_105_aeropic_supplier_receiver_slice as s
import winds_105_spell_metadata as physical

FIRST = """public class net.raptorzizi.wind_spellbooks.effect.AeropicEffect {
  public boolean applyEffectTick(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: aload_0
      1: iload_2
      2: aload_1
      3: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
      6: bipush 10
      8: imul
      9: ireturn
  public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: aload_1
      1: ifnull 39
      4: getstatic #11 // Field net/raptorzizi/wind_spellbooks/registries/ModSpellRegistry.ACROBATICS_SPELL:Ljava/util/function/Supplier;
      7: invokeinterface #13,  1 // InterfaceMethod java/util/function/Supplier.get:()Ljava/lang/Object;
     12: checkcast #15 // class io/redspace/ironsspellbooks/api/spells/AbstractSpell
     15: iload_2
     16: aload_1
     17: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
     20: iconst_1
     21: iadd
     22: istore_3
     39: return
}"""

class RecastSliceTests(unittest.TestCase):
    def test_straight_line_receiver_producer(self):
        out=s.examine(s.methods_from_javap(FIRST))
        self.assertEqual("COMPILED_ACROBATICS_SPELL_SUPPLIER_GET_CAST_TO_ABSTRACTSPELL",
                         out["onEffectAdded"]["static_receiver_origin"])
        self.assertEqual("PLUS_ONE_DIRECTLY_AFTER_CALL",
                         out["onEffectAdded"]["immediate_result_arithmetic"])
        self.assertEqual("NOT_PROVEN",out["onEffectAdded"]["receiver_runtime_type"])
        self.assertEqual("NOT_PROVEN",out["applyEffectTick"]["static_receiver_origin"])
    def test_wrong_field_rejected_as_proof(self):
        out=s.examine(s.methods_from_javap(FIRST.replace("ModSpellRegistry.ACROBATICS_SPELL","ModSpellRegistry.OTHER")))
        self.assertEqual("NOT_PROVEN",out["onEffectAdded"]["static_receiver_origin"])
    def test_wrong_supplier_method_rejected_as_proof(self):
        out=s.examine(s.methods_from_javap(FIRST.replace("Supplier.get:","Supplier.other:")))
        self.assertEqual("NOT_PROVEN",out["onEffectAdded"]["static_receiver_origin"])
    def test_wrong_checkcast_rejected_as_proof(self):
        out=s.examine(s.methods_from_javap(FIRST.replace("class io/redspace/ironsspellbooks/api/spells/AbstractSpell",
                                                        "class java/lang/Object")))
        self.assertEqual("NOT_PROVEN",out["onEffectAdded"]["static_receiver_origin"])
    def test_non_adjacent_extra_opcode_blocks_proof(self):
        text=FIRST.replace("     15: iload_2","     14: pop\n     15: iload_2")
        out=s.examine(s.methods_from_javap(text))
        self.assertEqual("NOT_PROVEN",out["onEffectAdded"]["static_receiver_origin"])
    def test_branch_into_middle_blocks_proof(self):
        text=FIRST.replace("1: ifnull 39","1: ifnull 15")
        out=s.examine(s.methods_from_javap(text))
        self.assertEqual("CONTROL_FLOW_ENTRY_OR_UNRESOLVED_SWITCH_PREVENTS_PROOF",
                         out["onEffectAdded"]["non_proof_reason"])
    def test_wrong_caller_descriptor_blocks_count(self):
        with self.assertRaisesRegex(s.SliceError,"recast invocation count"):
            s.examine(s.methods_from_javap(FIRST.replace(
                "(ILnet/minecraft/world/entity/LivingEntity;)I", "(I)I")))
    def test_invokeinterface_at_call_rejected(self):
        txt=FIRST.replace("17: invokevirtual", "17: invokeinterface")
        with self.assertRaisesRegex(s.SliceError,"invocation opcode drift"):
            s.examine(s.methods_from_javap(txt))
    def test_duplicate_selected_overload_rejected(self):
        txt=FIRST.replace("  public void onEffectAdded(",
                          "  public void onEffectAdded(java.lang.String);\n    Code:\n      0: return\n  public void onEffectAdded(")
        with self.assertRaisesRegex(s.SliceError,"overloaded"):
            s.methods_from_javap(txt)
    def test_immutable_release_sha_required(self):
        with self.assertRaisesRegex(s.SliceError,"wrong binary"):
            s.report("0"*40,s.examine(s.methods_from_javap(FIRST)))
        ok=s.report(physical.EXPECTED_SHA1,s.examine(s.methods_from_javap(FIRST)))
        self.assertFalse(ok["sender_jvm_bytecode_redistributed"])
    def test_return_consumer_never_claimed(self):
        rows=s.examine(s.methods_from_javap(FIRST))
        self.assertEqual("NOT_PROVEN",rows["onEffectAdded"]["recast_state_value_flow"])
        self.assertEqual("NOT_PROVEN",rows["onEffectAdded"]["safe_mutating_hook"])

if __name__=="__main__":
    unittest.main()
