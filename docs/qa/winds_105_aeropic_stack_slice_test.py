#!/usr/bin/env python3
"""Abstract stack regression: do not confuse JVM owner, class cast and runtime."""
import unittest
import winds_105_aeropic_stack_slice as stack
import winds_105_aeropic_supplier_receiver_slice as parser

def example(extra="",prefix="",post=""):
    return f"""public class TestEffect {{
  public boolean applyEffectTick(net.minecraft.world.entity.LivingEntity, int);
    Code:
      0: aload_0
      1: iload_2
      2: aload_1
      3: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
      6: ireturn
  public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);
    Code:
{prefix}     10: getstatic #11 // Field net/raptorzizi/wind_spellbooks/registries/ModSpellRegistry.ACROBATICS_SPELL:Ljava/util/function/Supplier;
     13: invokeinterface #15, 1 // InterfaceMethod java/util/function/Supplier.get:()Ljava/lang/Object;
     18: checkcast #16 // class io/redspace/ironsspellbooks/api/spells/AbstractSpell
{extra}     27: iload_2
     28: aload_1
     29: invokevirtual #2 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
{post}     32: return
}}"""

def classified(code):
    return {name:stack.classify(rows,name) for name,rows
            in parser.methods_from_javap(code).items()}

class StackSliceTests(unittest.TestCase):
    def test_simple_straight_line_path(self):
        doc=classified(example())
        self.assertEqual("COMPILED_SUPPLIER_GET_CAST_RECEIVER",
                         doc["onEffectAdded"]["compiled_receiver_source"])
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["runtime_receiver_concrete_class"])
        self.assertEqual("NOT_PROVEN",doc["applyEffectTick"]["compiled_receiver_source"])
    def test_intervening_safe_invocation_and_dup(self):
        more="""     20: dup
     21: invokevirtual #9 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getSpellId:()Ljava/lang/String;
     24: pop
"""
        doc=classified(example(extra=more))
        self.assertEqual("COMPILED_SUPPLIER_GET_CAST_RECEIVER",
                         doc["onEffectAdded"]["compiled_receiver_source"])
    def test_mismatched_supplier_ref_rejected(self):
        doc=classified(example().replace("Supplier.get:","Supplier.other:"))
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["compiled_receiver_source"])
    def test_wrong_checkcast_rejected(self):
        doc=classified(example().replace("class io/redspace/ironsspellbooks/api/spells/AbstractSpell",
                                          "class java/lang/Object"))
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["compiled_receiver_source"])
    def test_external_branch_into_expression_rejected(self):
        branch="      0: goto 18\n"
        doc=classified(example(prefix=branch))
        self.assertEqual("EXTERNAL_CONTROL_FLOW_ENTRY_OR_UNRESOLVED_SWITCH",
                         doc["onEffectAdded"]["non_proof_reason"])
    def test_branch_inside_candidate_block_rejected(self):
        branch="     19: ifnull 27\n"
        doc=classified(example(extra=branch))
        self.assertIn(doc["onEffectAdded"]["non_proof_reason"],
                      {"EXTERNAL_CONTROL_FLOW_ENTRY_OR_UNRESOLVED_SWITCH",
                       "FAIL_CLOSED_control flow or return in candidate stack slice"})
    def test_unsupported_stack_instruction_blocks_proof(self):
        doc=classified(example(extra="     22: dup_x1\n"))
        self.assertIn("unsupported",doc["onEffectAdded"]["non_proof_reason"])
    def test_recast_call_opcode_changed_fails_closed(self):
        with self.assertRaisesRegex(stack.SliceError,"invocation opcode"):
            classified(example().replace("29: invokevirtual", "29: invokestatic"))
    def test_receiver_swapped_to_other_field_not_proven(self):
        doc=classified(example().replace("ACROBATICS_SPELL", "WRONG_SPELL"))
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["compiled_receiver_source"])
    def test_unrelated_return_cannot_be_confirmed(self):
        doc=classified(example(post="     30: iadd\n"))
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["return_value_to_PlayerRecasts"])
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["safe_perk_mutator"])
    def test_descriptor_scanner_rejects_invalid_types(self):
        with self.assertRaises(stack.SliceError):
            stack.descriptor("(X)I")
        self.assertEqual((2,True),stack.descriptor("(ILnet/minecraft/world/entity/LivingEntity;)I"))
    def test_fallback_when_no_supplier_field(self):
        doc=classified(example().replace("getstatic #11", "aload_0 #11"))
        self.assertEqual("NOT_PROVEN",doc["onEffectAdded"]["compiled_receiver_source"])

if __name__=="__main__":
    unittest.main()
