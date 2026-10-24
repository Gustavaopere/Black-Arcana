#!/usr/bin/env python3
"""Synthetic proof obligations for static ABI and registry symbol boundaries."""
from copy import deepcopy
import unittest

import winds_105_effect_registry_dispatch as mod

def declarations():
    result={}
    for short,full in mod.CLASSES.items():
        if short=="aeropic_spell":
            result[short]={
                "class_declaration":f"public class {full} extends io.redspace.ironsspellbooks.api.spells.AbstractSpell {{",
                "immediate_superclass_token":"io.redspace.ironsspellbooks.api.spells.AbstractSpell",
                "recast_declarations":[{"declaration":"public int getRecastCount(int, net.minecraft.world.entity.LivingEntity);",
                                        "descriptor":mod.GET_RECAST}],
                "method_signature_count":3,
                "semantics":"JAVAP_DECLARATIONS_ONLY",
            }
        else:
            result[short]={
                "class_declaration":f"public class {full} {{",
                "immediate_superclass_token":None,
                "recast_declarations":[],
                "method_signature_count":2,
                "semantics":"JAVAP_DECLARATIONS_ONLY",
            }
    return result

def symbols():
    return ["io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:"+mod.GET_RECAST]

REGISTRY_SAMPLE="""public class Test {
  static {};
    Code:
       0: ldc #5 // String tailwind
       2: invokedynamic #12,  0 // InvokeDynamic #0:get:()Ljava/util/function/Supplier;
       5: invokestatic #7 // Method net/neoforged/neoforge/registries/DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredHolder;
       7: putstatic #3 // Field TAILWIND:Lnet/neoforged/neoforge/registries/DeferredHolder;
       9: return
  private static net.minecraft.world.effect.MobEffect lambda$static$0();
    Code:
       0: new #2 // class net/raptorzizi/wind_spellbooks/effect/TailwindEffect
       2: invokespecial #6 // Method net/raptorzizi/wind_spellbooks/effect/TailwindEffect."<init>":()V
       5: areturn
}"""

class RegistryDispatchTests(unittest.TestCase):
    def test_javap_method_abi(self):
        cls="""public class net.raptorzizi.wind_spellbooks.spells.wind.AeropicSpell extends io.redspace.ironsspellbooks.api.spells.AbstractSpell {
  public int getRecastCount(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)I
  public void onCast();
    descriptor: ()V
}"""
        out=mod.declaration_inventory(cls)
        self.assertEqual("io.redspace.ironsspellbooks.api.spells.AbstractSpell",out["immediate_superclass_token"])
        self.assertEqual(mod.GET_RECAST,out["recast_declarations"][0]["descriptor"])

    def test_registry_sites_are_unbound_candidates(self):
        rows=mod.registry_symbols(REGISTRY_SAMPLE)
        self.assertEqual("NOT_PROVEN",rows["registration_field_to_instance_binding"])
        self.assertEqual("NOT_PROVEN",rows["invokedynamic_bootstrap_resolution"])
        clinit=rows["candidate_methods"]["static {};"]
        self.assertEqual(["tailwind"],clinit["relevant_string_constants"])
        factory=next(v for k,v in rows["candidate_methods"].items() if "lambda$static$0(" in k)
        self.assertEqual(["net/raptorzizi/wind_spellbooks/effect/TailwindEffect"],factory["effect_constructor_candidates"])

    def test_same_signature_not_dispatch_proof(self):
        row=mod.summarize(declarations(),REGISTRY_SAMPLE,symbols())
        self.assertTrue(row["aeropic_virtual_recast"]["signature_compatible"])
        self.assertEqual("NOT_PROVEN",row["aeropic_virtual_recast"]["runtime_dispatch_to_spell_override"])
        self.assertEqual("NOT_PROVEN",row["aeropic_virtual_recast"]["receiver_instance"])

    def test_reject_missing_override_descriptor(self):
        rows=declarations()
        rows["aeropic_spell"]["recast_declarations"]=[]
        with self.assertRaisesRegex(mod.AuditError,"descriptor mismatch"):
            mod.summarize(rows,REGISTRY_SAMPLE,symbols())

    def test_reject_wrong_abi(self):
        rows=declarations()
        rows["aeropic_spell"]["recast_declarations"][0]["descriptor"]="(I)I"
        with self.assertRaisesRegex(mod.AuditError,"descriptor mismatch"):
            mod.summarize(rows,REGISTRY_SAMPLE,symbols())

    def test_reject_missing_base_call(self):
        with self.assertRaisesRegex(mod.AuditError,"base method"):
            mod.summarize(declarations(),REGISTRY_SAMPLE,[])

    def test_no_registration_inference_from_new_constructor(self):
        row=mod.registry_symbols(REGISTRY_SAMPLE)
        self.assertEqual("SYMBOLIC_JVM_REGISTRY_SITES_ONLY",row["semantics"])
        self.assertNotIn("PROVEN",str(row["registration_field_to_instance_binding"]).replace("NOT_PROVEN",""))

    def test_reject_partial_javap_class(self):
        with self.assertRaisesRegex(mod.AuditError,"class header"):
            mod.declaration_inventory("  public void onCast();\n    descriptor: ()V")

    def test_reject_partial_class_roster(self):
        rows=declarations();rows.pop("tailwind_effect")
        with self.assertRaisesRegex(mod.AuditError,"incomplete class"):
            mod.summarize(rows,REGISTRY_SAMPLE,symbols())

if __name__=="__main__":
    unittest.main()
