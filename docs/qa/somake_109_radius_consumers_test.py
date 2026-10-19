#!/usr/bin/env python3
"""Bounded radius consumer symbolic inventory regression tests."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_radius_consumers import analyze_javap,calls_in_method,certify_exact_consumer_surface,KEYS

def synthetic(more_oncast:str=""):
    return """public class FuneralBloomSpell {
  public void onCast();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #2 // Method getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F
       4: new #3 // class com/somake/somakespells/entity/FuneralBloomControllerEntity
       7: invokespecial #4 // Method com/somake/somakespells/entity/FuneralBloomControllerEntity."<init>":()V
"""+more_oncast+"""      10: return
  public float getRadius(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: fconst_1
       1: freturn
}
"""

class ConsumerProbeTests(unittest.TestCase):
    def test_distinct_radius_and_constructor_symbols(self):
        o=analyze_javap(synthetic(),"spell")
        methods=o["selected_methods"]
        oncast=methods["onCast()V"]
        self.assertEqual(2,oncast["invoke_count"])
        self.assertEqual(1,len(oncast["classified"]["radius"]))
        self.assertEqual(1,len(oncast["classified"]["spawn_controller"]))
        self.assertNotIn("AABB.inflate",str(oncast["classified"]["aabb"]))

    def test_missing_focus_method_fails_closed(self):
        with self.assertRaises(GateError):
            analyze_javap(synthetic().replace("public float getRadius","public float other"),"spell")

    def test_oversized_symbol_rejected(self):
        with self.assertRaises(GateError):
            calls_in_method(["0: invokevirtual #1 // Method "+("x"*901)])

    def test_malformed_invoke_rejected(self):
        with self.assertRaises(GateError):
            calls_in_method(["0: invokestatic #10"])

    def test_bounded_branch_not_confused_with_callsite(self):
        d=calls_in_method(["0: aload_0","1: ifnonnull 7",
                           "4: invokevirtual #2 // Method getRadius:(I)F",
                           "7: return"])
        self.assertEqual(1,d["invoke_count"])
        self.assertEqual(4,d["instruction_count"])

    def test_invokedynamic_is_tracked_but_not_attributed_to_method(self):
        d=calls_in_method([
            "0: invokedynamic #10, 0 // InvokeDynamic #0:run:()Ljava/lang/Runnable;",
            "5: return"])
        self.assertEqual(1,d["invokedynamic_count"])
        self.assertEqual(0,d["invoke_count"])
        self.assertEqual([],d["callsite_symbols"])

    def test_malformed_invokedynamic_fails_closed(self):
        with self.assertRaises(GateError):
            calls_in_method(["0: invokedynamic #10 // InvokeDynamic malformed"])

    def test_field_not_counted_as_method(self):
        d=calls_in_method(["0: getfield #1 // Field com/Example.radius:F",
                           "3: invokevirtual #2 // Method getRadius:(I)F","6: freturn"])
        self.assertEqual(1,d["invoke_count"])
        self.assertEqual(1,len(d["field_symbols"]))

    def test_snapshot_missing_causal_surface_fails_closed(self):
        def record(*, radius=(), spawn=(), wave=(), aabb=(), query=(),
                   damage=(), heal=(), dyn=1):
            classified={k:[] for k in KEYS}
            for k,values in (("radius",radius),("spawn_controller",spawn),
                             ("wave",wave),("aabb",aabb),("query",query),
                             ("damage",damage),("heal",heal)):
                classified[k]=list(values)
            return {"classified":classified,"invokedynamic_count":dyn}
        outcome={
           "spell":{"selected_methods":{"onCast()V":record(
               radius=["getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F"],
               spawn=['com/somake/somakespells/entity/FuneralBloomControllerEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V'])}},
           "controller":{"selected_methods":{
               "tick()V":record(radius=["getRadius:()F"],
                                wave=["launchWave:(Lnet/minecraft/server/level/ServerLevel;)V"]),
               "launchWave()V":record(radius=["getRadius:()F"],
                    wave=['FuneralBloomBudEntity."<init>":(Lnet/minecraft/world/level/Level;)V'],
                    aabb=["AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"],
                    query=["ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;)Ljava/util/List;"]) }},
           "bud":{"selected_methods":{
               "impact()V":record(aabb=["AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"],
                 query=["ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;)Ljava/util/List;"],
                 damage=["DamageSources.applyDamage:(...)Z"],
                 heal=['SpellHealEvent."<init>":(...)V'])}}}
        certify_exact_consumer_surface(outcome)
        outcome["controller"]["selected_methods"]["launchWave()V"]["classified"]["radius"]=[]
        with self.assertRaises(GateError):
            certify_exact_consumer_surface(outcome)

    def test_bud_direct_radius_is_not_inferred_from_aabb(self):
        d=calls_in_method(["0: invokevirtual #1 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
                           "2: invokevirtual #2 // Method ServerLevel.getEntitiesOfClass:()Ljava/util/List;"])
        self.assertTrue(d["classified"]["aabb"])
        self.assertEqual([],d["classified"]["radius"])

    def test_no_inference_from_same_method_cooccurrence(self):
        d=analyze_javap(synthetic(),"spell")["selected_methods"]["onCast()V"]
        self.assertTrue(d["classified"]["radius"])
        self.assertTrue(d["classified"]["spawn_controller"])
        # Only callsites; no asserted constructor operand mapping.
        self.assertNotIn("argument_binding",d)
        self.assertNotIn("causal_radius",d)

if __name__=="__main__":
    unittest.main()
