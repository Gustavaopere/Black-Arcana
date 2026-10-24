#!/usr/bin/env python3
"""Synthetic RED/GREEN for compiled clinit->supplier->factory->holder claims."""
import unittest

import winds_105_bootstrap_registry_trace as trace

def fixture():
    return """public class demo.Registry {
  static {};
    descriptor: ()V
    flags: (0x0008) ACC_STATIC
    Code:
      stack=3, locals=0, args_size=0
         0: getstatic     #10 // Field MOB_EFFECTS:Lnet/neoforged/neoforge/registries/DeferredRegister;
         3: ldc           #11 // String aeropic
         5: invokedynamic #12,  0 // InvokeDynamic #0:get:()Ljava/util/function/Supplier;
        10: invokevirtual #13 // Method net/neoforged/neoforge/registries/DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredHolder;
        13: putstatic     #14 // Field ACROBATICS:Lnet/neoforged/neoforge/registries/DeferredHolder;
        16: getstatic     #10 // Field MOB_EFFECTS:Lnet/neoforged/neoforge/registries/DeferredRegister;
        19: ldc           #15 // String tailwind
        21: invokedynamic #16,  0 // InvokeDynamic #1:get:()Ljava/util/function/Supplier;
        26: invokevirtual #13 // Method net/neoforged/neoforge/registries/DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredHolder;
        29: putstatic     #17 // Field TAILWIND:Lnet/neoforged/neoforge/registries/DeferredHolder;
        32: return
}
BootstrapMethods:
  0: #24 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #70 ()Ljava/lang/Object;
      #71 REF_invokeStatic net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry.lambda$static$0:()Lnet/minecraft/world/effect/MobEffect;
      #72 ()Lnet/minecraft/world/effect/MobEffect;
  1: #24 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #70 ()Ljava/lang/Object;
      #73 REF_invokeStatic net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry.lambda$static$1:()Lnet/raptorzizi/wind_spellbooks/effect/TailwindEffect;
      #74 ()Lnet/raptorzizi/wind_spellbooks/effect/TailwindEffect;
InnerClasses:
"""

def factories():
    return {
        "private static Object lambda$static$0();":{
            "effect_constructor_candidates":[
                "net/raptorzizi/wind_spellbooks/effect/AeropicEffect"]},
        "private static Object lambda$static$1();":{
            "effect_constructor_candidates":[
                "net/raptorzizi/wind_spellbooks/effect/TailwindEffect"]},
    }

class BootstrapRegistryTest(unittest.TestCase):
    def test_two_exact_compiled_registration_edges(self):
        data=trace.trace(fixture(),factories())
        self.assertEqual("PASS_COMPILED_REGISTRATION_EDGES",data["result"])
        self.assertEqual({"ACROBATICS","TAILWIND"},set(data["registration_edges"]))
        self.assertEqual(0,data["registration_edges"]["ACROBATICS"]["supplier_bootstrap_site"])
        self.assertEqual("PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP",
                         data["registration_edges"]["TAILWIND"]["compiled_supplier_to_holder"])
        self.assertEqual("NOT_TESTED",data["registration_edges"]["TAILWIND"]["runtime_instance_registration"])

    def test_missing_bootstrap_is_fail_closed(self):
        with self.assertRaisesRegex(trace.TraceError,"BootstrapMethods"):
            trace.trace(fixture().replace("BootstrapMethods:","OtherMethods:"),factories())

    def test_wrong_factory_bootstrap_is_fail_closed(self):
        txt=fixture().replace("ModMobEffectRegistry.lambda$static$1:",
                              "ModMobEffectRegistry.lambda$static$0:")
        with self.assertRaisesRegex(trace.TraceError,"bootstrap target"):
            trace.trace(txt,factories())

    def test_swapped_holder_is_fail_closed(self):
        txt=fixture().replace("Field ACROBATICS:Lnet/neoforged/neoforge/registries/DeferredHolder;",
                              "Field WRONG:Lnet/neoforged/neoforge/registries/DeferredHolder;")
        with self.assertRaisesRegex(trace.TraceError,"holder and registration key"):
            trace.trace(txt,factories())

    def test_wrong_registry_owner_type_is_fail_closed(self):
        txt=fixture().replace("Field MOB_EFFECTS:Lnet/neoforged/neoforge/registries/DeferredRegister;",
                              "Field MOB_EFFECTS:Ljava/lang/Object;")
        with self.assertRaisesRegex(trace.TraceError,"receiver type"):
            trace.trace(txt,factories())

    def test_extra_instruction_breaks_bounded_stack_proof(self):
        txt=fixture().replace(
            "         5: invokedynamic",
            "         4: pop\n         5: invokedynamic")
        with self.assertRaisesRegex(trace.TraceError,"supplier callsite"):
            trace.trace(txt,factories())

    def test_missing_exact_factory_is_fail_closed(self):
        d=factories()
        d["private static Object lambda$static$0();"]["effect_constructor_candidates"]=[]
        with self.assertRaisesRegex(trace.TraceError,"factory has no exact"):
            trace.trace(fixture(),d)

    def test_duplicate_registration_key_is_fail_closed(self):
        txt=fixture().replace("String tailwind","String aeropic")
        with self.assertRaisesRegex(trace.TraceError,"registration key population"):
            trace.trace(txt,factories())

    def test_non_supplier_invokedynamic_is_fail_closed(self):
        txt=fixture().replace("InvokeDynamic #1:get:()Ljava/util/function/Supplier;",
                              "InvokeDynamic #1:call:()Ljava/util/function/Runnable;")
        with self.assertRaisesRegex(trace.TraceError,"recognized Supplier"):
            trace.trace(txt,factories())

    def test_missing_factory_method_handle_argument_fails(self):
        txt=fixture().replace(
            "REF_invokeStatic net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry.lambda$static$0:",
            "REF_invokeStatic other/Untrusted.unknown:")
        with self.assertRaisesRegex(trace.TraceError,"absent Supplier"):
            trace.trace(txt,factories())

    def test_non_metafactory_handle_rejected(self):
        txt=fixture().replace(
            "REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:",
            "REF_invokeStatic other/Unknown.boot:",1)
        with self.assertRaisesRegex(trace.TraceError,"unrecognized bootstrap"):
            trace.trace(txt,factories())

    def test_symbol_count_distinct_bootstraps(self):
        b=trace.bootstrap_invokers(fixture())
        self.assertEqual(2,len(b))
        self.assertEqual(11,len(trace.method_instr(fixture())))

if __name__=="__main__":
    unittest.main()
