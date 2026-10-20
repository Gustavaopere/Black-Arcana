#!/usr/bin/env python3
"""Bounded radius consumer symbolic inventory regression tests."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_radius_consumers import analyze_javap,calls_in_method,certify_exact_consumer_surface,KEYS,wave_radius_aabb_shape,prove_wave_inflate_operands,certify_exact_wave_aabb_109,wave_query_aabb_link,certify_exact_wave_query_109,lambda_selection_candidate_inventory,wave_predicate_bootstrap_binding,certify_exact_wave_predicate_109,wave_predicate_branch_topology,certify_exact_wave_boolean_109,native_isvalidtarget_surface,wave_max_targets_surface,certify_exact_native_selection_109,native_isvalidtarget_branch_edges,native_isvalidtarget_early_guards

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


class WavePredicateHelperInventoryTests(unittest.TestCase):
    @staticmethod
    def candidate():
        return [(
            "lambda$launchWave$0",
            "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            ["0: aload_0",
             "1: aload_1",
             "2: invokevirtual #1 // Method isValidTarget:(Lnet/minecraft/world/entity/LivingEntity;)Z",
             "5: ifeq 11",
             "8: iconst_1",
             "9: ireturn",
             "11: iconst_0",
             "12: ireturn"]
        )]

    def test_observe_predicate_candidate_without_proving_bootstrap_binding(self):
        p=lambda_selection_candidate_inventory(self.candidate())
        self.assertEqual("PREDICATE_HELPER_CANDIDATES_ONLY",p["status"],p)
        self.assertEqual(1,p["candidate_count"])
        one=p["candidates"][0]
        self.assertEqual("lambda$launchWave$0",one["method"])
        self.assertEqual(8,one["instruction_count"])
        self.assertTrue(one["mentions_isValidTarget"])
        self.assertEqual(1,one["conditional_branch_count"])
        self.assertEqual("BOOTSTRAP_BINDING_NOT_PROVED",p["boundary"])

    def test_non_wave_lambda_and_missing_candidate_fail_closed(self):
        p=lambda_selection_candidate_inventory([(
            "lambda$impact$0","()Z",["0: iconst_1","1: ireturn"])])
        self.assertEqual("NOT_PROVED",p["status"])

    def test_ambiguous_duplicate_candidate_is_rejected(self):
        with self.assertRaises(GateError):
            lambda_selection_candidate_inventory(self.candidate()+self.candidate())

    def test_unbounded_candidate_method_is_rejected(self):
        oversized=[("lambda$launchWave$0","()Z",
                   [f"{i}: nop" for i in range(251)])]
        with self.assertRaises(GateError):
            lambda_selection_candidate_inventory(oversized)


class WavePredicateBootstrapBindingTests(unittest.TestCase):
    @staticmethod
    def inventory():
        return lambda_selection_candidate_inventory(WavePredicateHelperInventoryTests.candidate())

    @staticmethod
    def caller():
        return [
            "0: aload_0",
            "1: aload_2",
            "2: invokedynamic #6, 0 // InvokeDynamic #0:test:(Lcom/somake/somakespells/entity/FuneralBloomControllerEntity;Lnet/minecraft/world/entity/LivingEntity;)Ljava/util/function/Predicate;",
            "7: pop",
            "8: return",
        ]

    @staticmethod
    def bootstrap():
        return (
            "BootstrapMethods:\n"
            "  0: #314 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(...)\n"
            "    Method arguments:\n"
            "      #1 (Ljava/lang/Object;)Z\n"
            "      #2 REF_invokeVirtual com/somake/somakespells/entity/FuneralBloomControllerEntity.lambda$launchWave$0:(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z\n"
            "      #3 (Ljava/lang/Object;)Z\n"
            "  1: #315 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(...)\n"
            "    Method arguments:\n"
            "      #8 REF_invokeStatic com/somake/somakespells/entity/FuneralBloomControllerEntity.lambda$launchWave$1:(Lnet/minecraft/world/entity/LivingEntity;)D\n"
            "InnerClasses:\n"
        )

    def test_exact_bootstrap_zero_links_predicate_to_boolean_wave_helper(self):
        p=wave_predicate_bootstrap_binding(self.bootstrap(),self.caller(),self.inventory())
        self.assertEqual("PROVED_QUERY_PREDICATE_BOOTSTRAP_TO_LAUNCHWAVE_LAMBDA0",p["status"],p)
        self.assertEqual("lambda$launchWave$0",p["implementation_method"])
        self.assertEqual(0,p["bootstrap_index"])
        self.assertEqual("BODY_BRANCH_OUTCOMES_NOT_PROVED",p["boundary"])

    def test_static_method_handle_is_not_the_physical_predicate_binding(self):
        self.assertEqual("NOT_PROVED",wave_predicate_bootstrap_binding(
            self.bootstrap().replace("REF_invokeVirtual com/somake/somakespells/entity/FuneralBloomControllerEntity.lambda$launchWave$0",
                                     "REF_invokeStatic com/somake/somakespells/entity/FuneralBloomControllerEntity.lambda$launchWave$0"),
            self.caller(),self.inventory())["status"])

    def test_wrong_bootstrap_or_nonpredicate_caller_fails_closed(self):
        self.assertEqual("NOT_PROVED",wave_predicate_bootstrap_binding(
            self.bootstrap().replace("lambda$launchWave$0","lambda$launchWave$9"),
            self.caller(),self.inventory())["status"])
        self.assertEqual("NOT_PROVED",wave_predicate_bootstrap_binding(
            self.bootstrap(),[x.replace("#0:test:","#1:test:") for x in self.caller()],
            self.inventory())["status"])

    def test_malformed_and_duplicate_bootstrap_implementation_fails_closed(self):
        self.assertEqual("NOT_PROVED",wave_predicate_bootstrap_binding(
            "no bootstrap",self.caller(),self.inventory())["status"])
        extra="      #4 REF_invokeStatic com/somake/somakespells/entity/FuneralBloomControllerEntity.lambda$launchWave$0:(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z\n"
        self.assertEqual("NOT_PROVED",wave_predicate_bootstrap_binding(
            self.bootstrap().replace("  1: #315",extra+"  1: #315"),self.caller(),self.inventory())["status"])

class ExactWavePredicate109GateTests(unittest.TestCase):
    @staticmethod
    def exact_inventory():
        return {
            "status":"PREDICATE_HELPER_CANDIDATES_ONLY",
            "candidate_count":2,
            "candidates":[
                {"method":"lambda$launchWave$0",
                 "descriptor":"(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
                 "instruction_count":15,"conditional_branch_count":2,
                 "mentions_isValidTarget":True,"mentions_activeTargetIds":True},
                {"method":"lambda$launchWave$1",
                 "descriptor":"(Lnet/minecraft/world/entity/LivingEntity;)D",
                 "instruction_count":4,"conditional_branch_count":0,
                 "mentions_isValidTarget":False,"mentions_activeTargetIds":False},
            ],
        }

    @staticmethod
    def exact_link():
        return {
            "status":"PROVED_QUERY_PREDICATE_BOOTSTRAP_TO_LAUNCHWAVE_LAMBDA0",
            "bootstrap_index":0,
            "implementation_method":"lambda$launchWave$0",
            "implementation_descriptor":"(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            "helper_instruction_count":15,
            "helper_conditional_branch_count":2,
            "references_isValidTarget":True,
            "references_activeTargetIds":True,
            "boundary":"BODY_BRANCH_OUTCOMES_NOT_PROVED",
        }

    def test_physical_gate_rejects_link_or_helper_drift(self):
        link=self.exact_link()
        inventory=self.exact_inventory()
        certify_exact_wave_predicate_109(link,inventory)
        for k,v in (("bootstrap_index",1),("implementation_method","lambda$launchWave$1"),
                    ("references_isValidTarget",False),("references_activeTargetIds",False),
                    ("helper_instruction_count",14),("boundary","FILTER_OUTCOMES_PROVED"),
                    ("status","NOT_PROVED")):
            with self.subTest(k=k):
                with self.assertRaises(GateError):
                    certify_exact_wave_predicate_109(dict(link,**{k:v}),inventory)
        with self.assertRaises(GateError):
            certify_exact_wave_predicate_109(link,dict(inventory,candidate_count=1))
        bad=self.exact_inventory()
        bad["candidates"][1]["instruction_count"]=5
        with self.assertRaises(GateError):
            certify_exact_wave_predicate_109(link,bad)

class WavePredicateBranchTopologyTests(unittest.TestCase):
    @staticmethod
    def compiled_like_boolean_body():
        return [(
            "lambda$launchWave$0",
            "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            [
                "0: aload_0",
                "1: aload_1",
                "2: aload_2",
                "3: invokevirtual #1 // Method isValidTarget:(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
                "6: ifeq 30",
                "9: aload_0",
                "10: getfield #2 // Field activeTargetIds:Ljava/util/Set;",
                "13: aload_2",
                "14: invokevirtual #3 // Method net/minecraft/world/entity/LivingEntity.getUUID:()Ljava/util/UUID;",
                "17: invokeinterface #4, 2 // InterfaceMethod java/util/Set.contains:(Ljava/lang/Object;)Z",
                "22: ifne 30",
                "25: iconst_1",
                "26: goto 31",
                "30: iconst_0",
                "31: ireturn",
            ],
        )]

    def test_boolean_helper_call_order_and_branch_topology_are_visible(self):
        p=wave_predicate_branch_topology(self.compiled_like_boolean_body())
        self.assertEqual("PROVED_WAVE_PREDICATE_VALID_AND_NOT_ACTIVE",p["status"],p)
        self.assertEqual(["isValidTarget","getUUID","Set.contains"],p["ordered_checks"])
        self.assertEqual(["ifeq","ifne"],p["conditional_opcodes"])
        self.assertEqual(15,p["instruction_count"])
        self.assertEqual(1,p["boolean_return_count"])
        self.assertEqual(["boolean_0","boolean_0"],p["conditional_destination_kinds"])
        self.assertEqual(["true_only_if_valid","false_if_active_uuid"],p["semantic_guards"])
        self.assertIn("actual captured role/teams/PvP",p["boundary"])

    def test_missing_or_duplicate_boolean_helper_fails_closed(self):
        self.assertEqual("NOT_PROVED",wave_predicate_branch_topology([])["status"])
        with self.assertRaises(GateError):
            wave_predicate_branch_topology(
                self.compiled_like_boolean_body()*2)

    def test_ambiguous_call_order_does_not_certify_predicate_checks(self):
        c=self.compiled_like_boolean_body()
        rows=c[0][2].copy()
        rows[3]=rows[3].replace("isValidTarget","notAValidTarget")
        value=wave_predicate_branch_topology([(c[0][0],c[0][1],rows)])
        self.assertEqual("NOT_PROVED",value["status"])

    def test_inverted_membership_branch_or_false_target_fails_closed(self):
        n,desc,rows=self.compiled_like_boolean_body()[0]
        change=rows.copy()
        change[10]=change[10].replace("ifne 30","ifeq 30")
        self.assertEqual("NOT_PROVED",wave_predicate_branch_topology([(n,desc,change)])["status"])
        change=rows.copy()
        change[4]=change[4].replace("ifeq 30","ifeq 25")
        self.assertEqual("NOT_PROVED",wave_predicate_branch_topology([(n,desc,change)])["status"])

    def test_field_and_membership_owner_replacement_fail_closed(self):
        n,desc,rows=self.compiled_like_boolean_body()[0]
        change=rows.copy()
        change[6]=change[6].replace("activeTargetIds","otherSet")
        self.assertEqual("NOT_PROVED",wave_predicate_branch_topology([(n,desc,change)])["status"])
        change=rows.copy()
        change[9]=change[9].replace("java/util/Set.contains","external/FakeSet.contains")
        self.assertEqual("NOT_PROVED",wave_predicate_branch_topology([(n,desc,change)])["status"])

    def test_invalid_branch_target_fails_closed(self):
        c=self.compiled_like_boolean_body()
        rows=c[0][2].copy()
        rows[4]=rows[4].replace("ifeq 30","ifeq 999")
        result=wave_predicate_branch_topology([(c[0][0],c[0][1],rows)])
        self.assertEqual("NOT_PROVED",result["status"])

class Exact109PredicateBooleanGateTests(unittest.TestCase):
    def test_exact_valid_and_unseen_predicate_gate_rejects_mutations(self):
        proof=wave_predicate_branch_topology(WavePredicateBranchTopologyTests.compiled_like_boolean_body())
        self.assertEqual("PROVED_WAVE_PREDICATE_VALID_AND_NOT_ACTIVE",proof["status"])
        certify_exact_wave_boolean_109(proof)
        for change in (
            {"status":"NOT_PROVED"},
            {"conditional_opcodes":["ifne","ifne"]},
            {"conditional_destination_kinds":["boolean_0","boolean_1"]},
            {"boolean_return_count":2},
            {"semantic_guards":["true_only_if_valid","false_if_new_uuid"]},
            {"ordered_checks":["Set.contains","getUUID","isValidTarget"]},
            {"instruction_count":14},
            {"return_constant_categories":["0","1"]},
            {"boolean_call_adjacent_to_branch":[False,True]},
        ):
            with self.subTest(change=change):
                with self.assertRaises(GateError):
                    certify_exact_wave_boolean_109(dict(proof,**change))

class NativeIsValidTargetSurfaceTests(unittest.TestCase):
    @staticmethod
    def sample():
        return [(
            "isValidTarget",
            "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            [
                "0: aload_1",
                "1: invokevirtual #1 // Method net/minecraft/world/entity/LivingEntity.isAlive:()Z",
                "4: ifeq 19",
                "7: aload_1",
                "8: aload_2",
                "9: invokevirtual #2 // Method net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z",
                "12: ifne 19",
                "15: iconst_1",
                "16: ireturn",
                "19: iconst_0",
                "20: ireturn",
            ]
        )]

    def test_exact_method_shape_is_reported_without_inferred_filter_semantics(self):
        p=native_isvalidtarget_surface(self.sample())
        self.assertEqual("ISVALIDTARGET_MEMBER_SHAPE_ONLY",p["status"],p)
        self.assertEqual(11,p["instruction_count"])
        self.assertEqual(["ifeq","ifne"],p["conditional_opcodes"])
        self.assertEqual(2,p["boolean_return_count"])
        self.assertEqual(2,p["invoke_count"])
        self.assertEqual("FILTER_OUTCOMES_NOT_PROVED",p["boundary"])
        self.assertNotIn("passes_allies",p)

    def test_missing_member_fails_closed(self):
        p=native_isvalidtarget_surface([])
        self.assertEqual("NOT_PROVED",p["status"])

    def test_duplicate_and_unbounded_member_are_rejected(self):
        with self.assertRaises(GateError):
            native_isvalidtarget_surface(self.sample()+self.sample())
        name,desc,body=self.sample()[0]
        with self.assertRaises(GateError):
            native_isvalidtarget_surface([(name,desc,
                [f"{i}: nop" for i in range(351)])])

    def test_nonboolean_signature_does_not_claim_filter(self):
        name,desc,body=self.sample()[0]
        p=native_isvalidtarget_surface([(name,desc.replace(")Z",")I"),body)])
        self.assertEqual("NOT_PROVED",p["status"])

class WaveMaxTargetsSurfaceTests(unittest.TestCase):
    @staticmethod
    def sample():
        return [
            "0: aload_0",
            "1: getfield #1 // Field maxTargets:I",
            "4: istore_2",
            "5: new #2 // class com/somake/somakespells/entity/FuneralBloomBudEntity",
            "8: dup",
            '9: invokespecial #3 // Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":()V',
            "12: return",
        ]

    def test_field_and_bud_callsite_inventory_is_structural_only(self):
        p=wave_max_targets_surface(self.sample())
        self.assertEqual("MAXTARGETS_AND_BUD_COSITES_ONLY",p["status"],p)
        self.assertEqual(1,p["max_targets_field_read_count"])
        self.assertEqual(1,p["bud_ctor_call_count"])
        self.assertEqual(7,p["instruction_count"])
        self.assertEqual("TARGET_COUNT_CAP_NOT_PROVED",p["boundary"])
        self.assertNotIn("cap_enforced",p)

    def test_missing_max_targets_read_is_fail_closed(self):
        body=[s.replace("maxTargets","unrelatedField") for s in self.sample()]
        self.assertEqual("NOT_PROVED",wave_max_targets_surface(body)["status"])

    def test_missing_bud_constructor_is_fail_closed(self):
        body=[s.replace("FuneralBloomBudEntity.", "OtherEntity.") for s in self.sample()]
        self.assertEqual("NOT_PROVED",wave_max_targets_surface(body)["status"])

class Exact109NativeSelectionShapeTests(unittest.TestCase):
    @staticmethod
    def native():
        return {
            "status":"ISVALIDTARGET_MEMBER_SHAPE_ONLY",
            "descriptor":"(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            "instruction_count":41,
            "conditional_opcodes":["ifeq","ifne","if_acmpne","ifnull","ifeq","ifgt"],
            "boolean_return_count":3,
            "invoke_count":9,
            "field_read_count":0,
            "field_write_count":0,
            "callsite_symbols":[
                "getRadius:()F","getX:()D","getZ:()D",
                "net/minecraft/world/entity/LivingEntity.distanceToSqr:(DDD)D",
                "net/minecraft/world/entity/LivingEntity.getY:()D",
                "net/minecraft/world/entity/LivingEntity.isAlive:()Z",
                "net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z",
                "net/minecraft/world/entity/LivingEntity.isSpectator:()Z",
            ],
            "boundary":"FILTER_OUTCOMES_NOT_PROVED",
        }

    @staticmethod
    def cap():
        return {
            "status":"MAXTARGETS_AND_BUD_COSITES_ONLY",
            "instruction_count":196,
            "max_targets_field_read_count":2,
            "bud_ctor_call_count":1,
            "first_max_targets_read_before_first_bud_ctor":True,
            "first_read_to_ctor_instruction_gap":49,
            "conditional_branch_count":4,
            "boundary":"TARGET_COUNT_CAP_NOT_PROVED",
        }

    def test_exact_release_requires_native_method_and_cap_fingerprint(self):
        native,cap=self.native(),self.cap()
        certify_exact_native_selection_109(native,cap)
        for change in (
            {"status":"NOT_PROVED"},
            {"instruction_count":40},
            {"conditional_opcodes":["ifeq","ifne"]},
            {"boolean_return_count":2},
            {"invoke_count":8},
            {"field_read_count":1},
            {"callsite_symbols":native["callsite_symbols"][:-1]},
            {"boundary":"ALL_TARGETING_PROVED"},
        ):
            with self.subTest(native_change=change):
                with self.assertRaises(GateError):
                    certify_exact_native_selection_109(dict(native,**change),cap)
        for change in (
            {"max_targets_field_read_count":1},
            {"bud_ctor_call_count":2},
            {"first_read_to_ctor_instruction_gap":48},
            {"first_max_targets_read_before_first_bud_ctor":False},
            {"boundary":"TARGET_COUNT_CAP_PROVED"},
        ):
            with self.subTest(cap_change=change):
                with self.assertRaises(GateError):
                    certify_exact_native_selection_109(native,dict(cap,**change))

class NativeIsValidTargetBranchEdgesTests(unittest.TestCase):
    @staticmethod
    def method():
        return [(
            "isValidTarget",
            "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            [
                "0: aload_1",
                "1: invokevirtual #1 // Method net/minecraft/world/entity/LivingEntity.isAlive:()Z",
                "4: ifeq 16",
                "7: aload_2",
                "8: invokevirtual #2 // Method net/minecraft/world/entity/LivingEntity.isSpectator:()Z",
                "11: ifne 16",
                "14: iconst_1",
                "15: ireturn",
                "16: iconst_0",
                "17: ireturn",
            ],
        )]

    def test_bounded_branches_resolve_targets_without_claiming_gameplay(self):
        p=native_isvalidtarget_branch_edges(self.method())
        self.assertEqual("ISVALIDTARGET_BRANCH_EDGES_ONLY",p["status"],p)
        self.assertEqual(10,p["instruction_count"])
        self.assertEqual(2,p["branch_count"])
        self.assertEqual(["ifeq","ifne"],[b["opcode"] for b in p["branch_edges"]])
        self.assertEqual([8,8],[b["target_index"] for b in p["branch_edges"]])
        self.assertEqual(["constant_zero","constant_zero"],
                         [b["destination_kind"] for b in p["branch_edges"]])
        self.assertEqual("PATH_PREDICATES_AND_ENTITY_ROLES_NOT_PROVED",p["boundary"])
        self.assertNotIn("accepts_player",p)

    def test_unresolvable_branch_target_is_fail_closed(self):
        method=self.method()
        name,desc,rows=method[0]
        rows=rows.copy()
        rows[2]=rows[2].replace("ifeq 16","ifeq 999")
        self.assertEqual("NOT_PROVED",native_isvalidtarget_branch_edges([(name,desc,rows)])["status"])

    def test_ambiguous_or_oversized_method_is_rejected(self):
        with self.assertRaises(GateError):
            native_isvalidtarget_branch_edges(self.method()*2)
        name,desc,_=self.method()[0]
        with self.assertRaises(GateError):
            native_isvalidtarget_branch_edges([(name,desc,[f"{i}: nop" for i in range(90)])])

class NativeIsValidTargetEarlyGuardsTests(unittest.TestCase):
    @staticmethod
    def body():
        return [(
            "isValidTarget",
            "(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
            [
                "0: aload_2",
                "1: invokevirtual #1 // Method net/minecraft/world/entity/LivingEntity.isAlive:()Z",
                "4: ifeq 17",
                "7: aload_2",
                "8: invokevirtual #2 // Method net/minecraft/world/entity/LivingEntity.isSpectator:()Z",
                "11: ifne 17",
                "14: aload_2",
                "15: aload_1",
                "16: if_acmpne 19",
                "17: iconst_0",
                "18: ireturn",
                "19: aload_1",
                "20: iconst_1",
                "21: ireturn",
            ],
        )]

    def test_first_arg_must_be_alive_not_spectator_and_different_from_second(self):
        p=native_isvalidtarget_early_guards(self.body())
        self.assertEqual("PROVED_NATIVE_EARLY_ALIVE_NOT_SPECTATOR_NOT_IDENTICAL",p["status"],p)
        self.assertEqual(2,p["examined_jvm_local"])
        self.assertEqual(1,p["compared_jvm_local"])
        self.assertEqual(["ifeq","ifne","if_acmpne"],p["branch_ops"])
        self.assertEqual("DIRECT_ZERO_RETURN_ON_THREE_REJECTIONS",p["rejection_mode"])
        self.assertNotIn("owner_is_caster",p)

    def test_inverted_spectator_branch_rejected(self):
        n,d,body=self.body()[0]
        rows=body.copy()
        rows[5]=rows[5].replace("ifne 17","ifeq 17")
        self.assertEqual("NOT_PROVED",native_isvalidtarget_early_guards([(n,d,rows)])["status"])

    def test_self_comparison_and_false_return_must_remain_exact(self):
        n,d,body=self.body()[0]
        rows=body.copy()
        rows[7]=rows[7].replace("aload_1","aload_2")
        self.assertEqual("NOT_PROVED",native_isvalidtarget_early_guards([(n,d,rows)])["status"])
        rows=body.copy()
        rows[9]=rows[9].replace("iconst_0","iconst_1")
        self.assertEqual("NOT_PROVED",native_isvalidtarget_early_guards([(n,d,rows)])["status"])

    def test_ambiguous_method_rejected(self):
        with self.assertRaises(GateError):
            native_isvalidtarget_early_guards(self.body()*2)

if __name__=="__main__":
    unittest.main()
