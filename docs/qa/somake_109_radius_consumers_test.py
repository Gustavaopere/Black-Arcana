#!/usr/bin/env python3
"""Bounded radius consumer symbolic inventory regression tests."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_radius_consumers import analyze_javap,calls_in_method,certify_exact_consumer_surface,KEYS,wave_radius_aabb_shape,prove_wave_inflate_operands,certify_exact_wave_aabb_109,wave_query_aabb_link,certify_exact_wave_query_109

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

class WaveRadiusAabbShapeTests(unittest.TestCase):
    @staticmethod
    def specimen():
        return [
            "0: aload_0",
            "1: invokevirtual #1 // Method getRadius:()F",
            "4: f2d",
            "5: dstore_2",
            "6: aload_0",
            "7: invokevirtual #2 // Method getBoundingBox:()Lnet/minecraft/world/phys/AABB;",
            "10: dload_2",
            "11: dconst_1",
            "12: dload_2",
            "13: invokevirtual #3 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
            "16: pop",
            "17: return",
        ]

    def test_bounded_ordered_calls_are_observed_without_inventing_dataflow(self):
        p=wave_radius_aabb_shape(self.specimen())
        self.assertEqual("STRUCTURAL_ONLY_NO_AABB_OPERAND_PROVENANCE",p["status"])
        self.assertEqual(1,p["radius_call_count"])
        self.assertEqual(1,p["inflate_call_count"])
        self.assertTrue(p["radius_before_inflate"])
        self.assertEqual(12,p["instruction_count"])
        self.assertEqual(1,p["f2d_instruction_count"])
        self.assertEqual(0,p["branch_instruction_count"])
        self.assertNotIn("aabb_radius_proved",p)

    def test_inflate_without_getter_never_becomes_radius_proof(self):
        rows=[x for x in self.specimen() if "getRadius:()F" not in x]
        p=wave_radius_aabb_shape(rows)
        self.assertEqual("NOT_PROVED",p["status"])

    def test_inverted_order_never_becomes_radius_proof(self):
        original=self.specimen()
        radius=[x for x in original if "getRadius:()F" in x][0]
        rows=[x for x in original if "getRadius:()F" not in x]
        rows.insert(-1,radius)
        rows=[str(3*i)+":"+line.split(":",1)[1] for i,line in enumerate(rows)]
        p=wave_radius_aabb_shape(rows)
        self.assertEqual("NOT_PROVED",p["status"])

class WaveInflateCausalOperandTests(unittest.TestCase):
    @staticmethod
    def triple_radius():
        body=["0: aload_0",
              "1: invokevirtual #1 // Method getBoundingBox:()Lnet/minecraft/world/phys/AABB;"]
        pc=4
        for i in range(3):
            body.extend([
                f"{pc}: aload_0",
                f"{pc+1}: invokevirtual #2 // Method getRadius:()F",
                f"{pc+4}: f2d"
            ])
            pc+=5
        body.extend([
            f"{pc}: invokevirtual #3 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
            f"{pc+3}: areturn"])
        return body

    @staticmethod
    def xz_radius_y_literal():
        return [
            "0: aload_0",
            "1: invokevirtual #1 // Method getBoundingBox:()Lnet/minecraft/world/phys/AABB;",
            "4: aload_0",
            "5: invokevirtual #2 // Method getRadius:()F",
            "8: f2d",
            "9: ldc2_w #3 // double 2.0d",
            "12: aload_0",
            "13: invokevirtual #2 // Method getRadius:()F",
            "16: f2d",
            "17: invokevirtual #4 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
            "20: areturn"
        ]

    def test_xz_radius_with_literal_y_requires_exact_stack(self):
        x=prove_wave_inflate_operands(self.xz_radius_y_literal())
        self.assertEqual("PROVED_AABB_XZ_CONTROLLER_RADIUS_Y_LITERAL_DOUBLE",x["status"],x)
        self.assertEqual(["X","Z"],x["radius_axes"])
        self.assertEqual("2.0",x["vertical_double_literal"])
        self.assertNotIn("entity_selection_proved",x)

    def test_xz_y_expression_or_malformed_constant_fails_closed(self):
        rows=self.xz_radius_y_literal()
        rows[5]=rows[5].replace("double 2.0d","float 2.0f")
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(rows)["status"])
        rows=self.xz_radius_y_literal()
        rows[5]=rows[5].replace("ldc2_w #3 // double 2.0d",
            "invokestatic #3 // Method getVerticalArea:()D")
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(rows)["status"])

    def test_xz_radius_caller_must_be_this(self):
        rows=self.xz_radius_y_literal()
        rows[6]=rows[6].replace("aload_0","aload_1")
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(rows)["status"])

    def test_xyz_arguments_are_all_local_controller_radius_for_exact_pattern(self):
        result=prove_wave_inflate_operands(self.triple_radius())
        self.assertEqual("PROVED_THREE_AABB_INFLATE_ARGUMENTS_FROM_CONTROLLER_RADIUS",result["status"],result)
        self.assertEqual(["X","Y","Z"],result["axes"])
        self.assertEqual("F_TO_D",result["conversion"])
        self.assertNotIn("world_hit_targets_proved",result)

    def test_only_two_radius_arguments_fail_closed(self):
        body=self.triple_radius()
        body[9]=body[9].replace("getRadius:()F","otherFloat:()F")
        result=prove_wave_inflate_operands(body)
        self.assertEqual("NOT_PROVED",result["status"])

    def test_foreign_method_and_arithmetic_fail_closed(self):
        body=self.triple_radius()
        body[3]=body[3].replace("Method getRadius:()F",
            "Method external/mod/Other.getRadius:()F")
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(body)["status"])
        body=self.triple_radius()
        body[4]=body[4].replace("f2d","fadd")
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(body)["status"])

    def test_external_branch_into_argument_sequence_fail_closed(self):
        body=self.triple_radius()
        body.insert(0,"0: goto 10")
        body=[str(i*5)+":"+r.split(":",1)[1] for i,r in enumerate(body)]
        # Make the branch target hit the second instruction of the AABB argument slice.
        body[0]="0: goto 20"
        self.assertEqual("NOT_PROVED",prove_wave_inflate_operands(body)["status"])

class Exact109WaveCertificationGateTests(unittest.TestCase):
    def test_exact_release_105_vertical_and_two_radius_axes_required(self):
        expected={
            "status":"PROVED_AABB_XZ_CONTROLLER_RADIUS_Y_LITERAL_DOUBLE",
            "radius_axes":["X","Z"],
            "vertical_double_literal":"10.5",
            "source_call_count":2,
            "conversion":"F_TO_D",
            "source_method":"FuneralBloomControllerEntity.getRadius:()F",
            "aabb_method_descriptor":"(DDD)Lnet/minecraft/world/phys/AABB;",
            "method_instruction_count":196,
        }
        certify_exact_wave_aabb_109(expected)
        for change in (
            {"vertical_double_literal":"11.0"},
            {"radius_axes":["X","Y","Z"]},
            {"source_call_count":3},
            {"status":"NOT_PROVED"},
            {"method_instruction_count":195},
        ):
            sample=dict(expected,**change)
            with self.subTest(change=change):
                with self.assertRaises(GateError):
                    certify_exact_wave_aabb_109(sample)

class WaveQueryAabbCausalityTests(unittest.TestCase):
    @staticmethod
    def direct_query():
        return [
            "0: aload_1",
            "1: ldc #2 // class net/minecraft/world/entity/LivingEntity",
            "3: aload_0",
            "4: invokevirtual #3 // Method getBoundingBox:()Lnet/minecraft/world/phys/AABB;",
            "7: dconst_1",
            "8: dconst_1",
            "9: dconst_1",
            "10: invokevirtual #4 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
            "13: invokedynamic #5, 0 // InvokeDynamic #0:test:()Ljava/util/function/Predicate;",
            "18: invokevirtual #6 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
            "21: pop",
            "22: return",
        ]

    def test_direct_inflate_return_used_by_exact_entity_query(self):
        p=wave_query_aabb_link(self.direct_query())
        self.assertEqual("PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY",p["status"],p)
        self.assertEqual(1,p["inflate_call_count"])
        self.assertEqual(1,p["entity_query_call_count"])
        self.assertEqual(1,p["between_instruction_count"])
        self.assertEqual("direct_stack",p["aabb_transport"])
        self.assertNotIn("filter_semantics_proved",p)

    @staticmethod
    def stored_then_loaded():
        return [
            "0: aload_0",
            "1: invokevirtual #1 // Method getBoundingBox:()Lnet/minecraft/world/phys/AABB;",
            "4: dconst_1",
            "5: dconst_1",
            "6: dconst_1",
            "7: invokevirtual #2 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;",
            "10: astore_3",
            "11: new #3 // class java/util/ArrayList",
            "14: dup",
            "15: aload_1",
            "16: ldc #4 // class net/minecraft/world/entity/LivingEntity",
            "18: aload_3",
            "19: aload_0",
            "20: aload_2",
            "21: invokedynamic #5, 0 // InvokeDynamic #0:test:(Lcom/somake/somakespells/entity/FuneralBloomControllerEntity;Lnet/minecraft/world/entity/LivingEntity;)Ljava/util/function/Predicate;",
            "26: invokevirtual #6 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
            "29: invokespecial #7 // Method java/util/ArrayList.\"<init>\":(Ljava/util/Collection;)V",
            "32: areturn",
        ]

    def test_stored_aabb_reloaded_as_query_argument(self):
        p=wave_query_aabb_link(self.stored_then_loaded())
        self.assertEqual("PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY",p["status"],p)
        self.assertEqual("via_local_3",p["aabb_transport"])
        self.assertEqual(9,p["between_instruction_count"])
        self.assertEqual("unknown_predicate_body",p["predicate_semantics"])

    def test_slot_overwrite_is_not_proven(self):
        rows=self.stored_then_loaded()
        rows[11]=rows[11].replace("aload_3","aload_2")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])
        rows=self.stored_then_loaded()
        rows[6]=rows[6].replace("astore_3","astore_2")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])

    def test_lambda_signature_and_box_type_must_match(self):
        rows=self.stored_then_loaded()
        rows[14]=rows[14].replace("java/util/function/Predicate","java/util/function/Function")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])
        rows=self.stored_then_loaded()
        rows[10]=rows[10].replace("LivingEntity","Other")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])

    def test_unrelated_query_or_stored_box_must_fail_closed(self):
        rows=self.direct_query()
        rows[9]=rows[9].replace("getEntitiesOfClass","getEntities")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])
        rows=self.direct_query()
        rows.insert(8,"12: astore_3")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])

    def test_missing_predicate_or_duplicate_query_must_fail_closed(self):
        rows=self.direct_query()
        rows[8]=rows[8].replace("invokedynamic","nop")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])
        rows=self.direct_query()
        rows.append("25: invokevirtual #6 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;")
        self.assertEqual("NOT_PROVED",wave_query_aabb_link(rows)["status"])

class ExactWaveQueryPhysicalGateTests(unittest.TestCase):
    @staticmethod
    def expected():
        return {
            "status":"PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY",
            "inflate_call_count":1,
            "entity_query_call_count":1,
            "aabb_transport":"via_local_3",
            "between_instruction_count":9,
            "query_descriptor":"(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
            "predicate_semantics":"unknown_predicate_body",
            "instruction_count":196,
        }

    def test_exact_wave_slot3_query_proof_is_hard_gated(self):
        original=self.expected()
        certify_exact_wave_query_109(original)
        for edits in (
            {"aabb_transport":"via_local_2"},
            {"between_instruction_count":8},
            {"status":"NOT_PROVED"},
            {"entity_query_call_count":2},
            {"query_descriptor":"(Ljava/lang/Class;)Ljava/util/List;"},
            {"predicate_semantics":"proved_filters"},
            {"instruction_count":195},
        ):
            with self.subTest(edits=edits):
                with self.assertRaises(GateError):
                    certify_exact_wave_query_109(dict(original,**edits))

if __name__=="__main__":
    unittest.main()
