#!/usr/bin/env python3
"""Positive/negative direct field provenance fixtures; no provider bytecode."""
import unittest
import subprocess
import tempfile
from pathlib import Path
from somake_109_perk_method_probe import GateError
from somake_109_controller_radius_bridge import (
  FQCN,CONSTRUCTOR_DESC,FLOAT_SLOTS,GETTER_DESC,
  analyze,local_id,direct_float_getter,constructor_direct_assignments,getter_structural_shape,synced_entity_float_getter,synced_radius_constructor_setter,synced_accessor_method_inventory,direct_synched_radius_setter,direct_constructor_setter_call
)

def specimen(getter=None,slot=3):
    getter=getter or [
        "0: aload_0",
        "1: getfield #10 // Field radius:F",
        "4: freturn",
    ]
    return (
       "public class "+FQCN+" {\n"
       "  public "+FQCN+"(net.minecraft.world.level.Level,net.minecraft.world.entity.LivingEntity,float,int,int,int,int,float,int,int);\n"
       "    descriptor: "+CONSTRUCTOR_DESC+"\n"
       "    Code:\n"
       "       0: aload_0\n"
       "       1: invokespecial #1 // Method java/lang/Object.\"<init>\":()V\n"
       "       4: aload_0\n"
       "       5: fload "+str(slot)+"\n"
       "       7: putfield #10 // Field radius:F\n"
       "      10: return\n"
       "  public float getRadius();\n"
       "    descriptor: "+GETTER_DESC+"\n"
       "    Code:\n"
       +"".join("      "+s+"\n" for s in getter)
       +"}\n"
    )

class RadiusBridgeTests(unittest.TestCase):
    def test_direct_float_arg3_maps_to_exact_radius_field(self):
        result=analyze(specimen())
        self.assertEqual("PROVED_DIRECT_INSTANCE_FLOAT_GETTER",result["getter"]["status"])
        binding=result["constructor_to_getter"]
        self.assertEqual("PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING",binding["status"])
        self.assertEqual(3,binding["jvm_local_slot"])
        self.assertEqual(1,binding["float_ordinal"])

    def test_second_float_slot_maps_without_guess(self):
        result=analyze(specimen(slot=8))
        self.assertEqual(8,result["constructor_to_getter"]["jvm_local_slot"])
        self.assertEqual(2,result["constructor_to_getter"]["float_ordinal"])

    def test_non_direct_getter_remains_unproved_but_yields_bounded_shape(self):
        modified=["0: aload_0","1: getfield #10 // Field radius:F",
                  "4: fconst_1","5: fadd","6: freturn"]
        record=analyze(specimen(getter=modified))
        self.assertEqual("NOT_PROVED",record["getter"]["status"])
        shape=record["getter_structure"]
        self.assertEqual(5,shape["instruction_count"])
        self.assertEqual(["radius"],shape["float_field_names_read"])
        self.assertEqual(1,shape["float_arithmetic_and_conversion_instructions"])
        self.assertEqual("STRUCTURAL_ONLY_NO_ARGUMENT_PROVENANCE",shape["proof_status"])

    def test_bounded_getter_calls_are_symbols_not_proven_arguments(self):
        shape=getter_structural_shape([
            "0: aload_0",
            "1: invokevirtual #2 // Method getBaseRadius:()F",
            "4: freturn"])
        self.assertEqual(["getBaseRadius:()F"],shape["invoked_method_symbols"])
        self.assertEqual([],shape["float_field_names_read"])
        self.assertNotIn("constructor_argument",shape)

    def test_full_sync_float_getter_is_proved_without_constructor_guess(self):
        body=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: invokevirtual #4 // Method net/minecraft/network/syncher/SynchedEntityData.get:(Lnet/minecraft/network/syncher/EntityDataAccessor;)Ljava/lang/Object;",
           "10: checkcast #5 // class java/lang/Float",
           "13: invokevirtual #6 // Method java/lang/Float.floatValue:()F",
           "16: freturn"]
        record=analyze(specimen(getter=body))
        self.assertEqual("NOT_PROVED",record["getter"]["status"])
        self.assertEqual("PROVED_EXACT_SYNCED_ENTITY_DATA_FLOAT_GETTER",
                         record["synced_data_getter"]["status"])
        self.assertEqual("DATA_RADIUS",record["synced_data_getter"]["accessor_field"])
        self.assertEqual("NOT_PROVED",record["constructor_to_getter"]["status"])

    def test_sync_getter_requires_float_cast_and_unbox(self):
        body=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: invokevirtual #4 // Method net/minecraft/network/syncher/SynchedEntityData.get:(Lnet/minecraft/network/syncher/EntityDataAccessor;)Ljava/lang/Object;",
           "10: checkcast #5 // class java/lang/Double",
           "13: invokevirtual #6 // Method java/lang/Float.floatValue:()F",
           "16: freturn"]
        proof=synced_entity_float_getter(body)
        self.assertEqual("NOT_PROVED",proof["status"])

    def test_foreign_synched_accessor_is_refused(self):
        body=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field external/mod/OtherController.DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: invokevirtual #4 // Method net/minecraft/network/syncher/SynchedEntityData.get:(Lnet/minecraft/network/syncher/EntityDataAccessor;)Ljava/lang/Object;",
           "10: checkcast #5 // class java/lang/Float",
           "13: invokevirtual #6 // Method java/lang/Float.floatValue:()F",
           "16: freturn"]
        self.assertEqual("NOT_PROVED",synced_entity_float_getter(body)["status"])

    def test_getter_invocation_without_symbol_rejected(self):
        with self.assertRaises(GateError):
            getter_structural_shape(["0: aload_0","1: invokevirtual #2","4: freturn"])

    def test_getter_with_operation_is_not_certified_direct(self):
        getter=["0: aload_0","1: getfield #10 // Field radius:F",
                "4: fconst_1","5: fadd","6: freturn"]
        x=analyze(specimen(getter=getter))
        self.assertEqual("NOT_PROVED",x["getter"]["status"])
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_field_conflict_rejected(self):
        x=analyze(specimen().replace("putfield #10 // Field radius:F",
                                     "putfield #10 // Field impactDamage:F"))
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_foreign_field_owner_is_never_claimed_as_controller_radius(self):
        foreign="external/mod/OtherEntity.radius:F"
        x=analyze(specimen().replace("Field radius:F", "Field "+foreign))
        self.assertEqual("NOT_PROVED",x["getter"]["status"])

    def test_foreign_constructor_field_write_does_not_bind_local_getter(self):
        x=analyze(specimen().replace("putfield #10 // Field radius:F",
            "putfield #10 // Field external/mod/OtherEntity.radius:F"))
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_unknown_local_source_not_guessed(self):
        x=analyze(specimen(slot=4))
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_descriptor_mismatch_rejected(self):
        with self.assertRaises(GateError):
            analyze(specimen().replace(CONSTRUCTOR_DESC,"(IF)V",1))

    def test_duplicate_field_writes_fail_closed(self):
        body=["0: aload_0","1: fload_3","2: putfield #1 // Field radius:F",
              "5: aload_0","6: fload 8","8: putfield #1 // Field radius:F","11: return"]
        x=constructor_direct_assignments(body,"radius")
        self.assertEqual("NOT_PROVED",x["status"])
        self.assertEqual(2,x["field_write_count"])

    def test_synched_setter_maps_only_direct_boxed_constructor_float(self):
        setter=[
          "0: aload_0",
          "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
          "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
          "7: fload_3",
          "8: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
          "11: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
          "14: return"]
        x=synced_radius_constructor_setter(setter,"DATA_RADIUS")
        self.assertEqual("PROVED_DIRECT_CONSTRUCTOR_FLOAT_TO_SYNCED_RADIUS",x["status"])
        self.assertEqual(3,x["jvm_local_slot"])
        second=[s.replace("fload_3","fload 8") for s in setter]
        self.assertEqual(8,synced_radius_constructor_setter(second,"DATA_RADIUS")["jvm_local_slot"])

    def test_synched_setter_rejects_transformations_and_branch(self):
        setter=[
          "0: aload_0",
          "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
          "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
          "7: fload_3","8: fconst_1","9: fadd",
          "10: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
          "13: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
          "16: return"]
        self.assertEqual("NOT_PROVED",synced_radius_constructor_setter(setter,"DATA_RADIUS")["status"])
        guarded=setter.copy()
        guarded[0]="0: ifnonnull 16"
        self.assertEqual("NOT_PROVED",synced_radius_constructor_setter(guarded,"DATA_RADIUS")["status"])

    def test_synched_setter_rejects_wrong_accessor_and_duplicate(self):
        setter=[
          "0: aload_0",
          "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
          "4: getstatic #3 // Field OTHER_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
          "7: fload_3",
          "8: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
          "11: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
          "14: return"]
        self.assertEqual("NOT_PROVED",synced_radius_constructor_setter(setter,"DATA_RADIUS")["status"])
        shifted=[line.replace(str(offset)+":",str(offset+20)+":",1)
                 for line,offset in zip(setter[:-1],[0,1,4,7,8,11])]
        duplicated=[*setter[:-1],*shifted,"34: return"]
        self.assertEqual("NOT_PROVED",synced_radius_constructor_setter(duplicated,"OTHER_RADIUS")["status"])

    def test_exact_seven_opcode_float_setter_proves_accessor_but_not_caller(self):
        body=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: fload_1",
           "8: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
           "11: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
           "14: return"]
        record=direct_synched_radius_setter(body,"DATA_RADIUS")
        self.assertEqual("PROVED_DIRECT_FLOAT_SETTER_TO_SYNCED_RADIUS",record["status"],record)
        self.assertEqual(1,record["setter_parameter_local_slot"])
        self.assertNotIn("constructor_argument",record)

    def test_sync_setter_rejects_wrong_float_source(self):
        body=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: fload_2",
           "8: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
           "11: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
           "14: return"]
        self.assertEqual("NOT_PROVED",direct_synched_radius_setter(body,"DATA_RADIUS")["status"])

    def test_constructor_direct_setter_argument_requires_adjacent_same_caster(self):
        body=["0: aload_0","1: fload_3",
              "2: invokevirtual #8 // Method setRadius:(F)V",
              "5: return"]
        proof=direct_constructor_setter_call(body)
        self.assertEqual("PROVED_DIRECT_CTOR_FLOAT_ARGUMENT_TO_SETTER",proof["status"])
        self.assertEqual(3,proof["jvm_local_slot"])
        second=[x.replace("fload_3","fload 8") for x in body]
        self.assertEqual(8,direct_constructor_setter_call(second)["jvm_local_slot"])

    def test_constructor_indirect_or_conditional_setter_cannot_be_certified(self):
        bad=["0: aload_0","1: fload_3","2: fconst_1","3: fadd",
             "4: invokevirtual #8 // Method setRadius:(F)V","7: return"]
        self.assertEqual("NOT_PROVED",direct_constructor_setter_call(bad)["status"])
        branch=["0: aload_0","1: ifnull 9",
                "4: fload_3","5: invokevirtual #8 // Method setRadius:(F)V",
                "9: return"]
        self.assertEqual("NOT_PROVED",direct_constructor_setter_call(branch)["status"])

    def test_accessor_method_inventory_discovers_but_does_not_prove_setter(self):
        method=[
           "0: aload_0",
           "1: getfield #2 // Field entityData:Lnet/minecraft/network/syncher/SynchedEntityData;",
           "4: getstatic #3 // Field DATA_RADIUS:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "7: fload_1",
           "8: invokestatic #4 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;",
           "11: invokevirtual #5 // Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V",
           "14: return"]
        result=synced_accessor_method_inventory([("setRadius","(F)V",method)],"DATA_RADIUS")
        self.assertEqual(1,result["methods_examined"])
        item=result["methods_with_relevant_symbols"][0]
        self.assertEqual("setRadius",item["method"])
        self.assertEqual([1],item["float_local_load_slots"])
        self.assertEqual(1,item["direct_getstatic_accessor_count"])
        self.assertEqual("STRUCTURAL_METHOD_REFERENCE_DISCOVERY_ONLY",result["status"])
        self.assertNotIn("constructor_parameter",item)

    def test_accessor_inventory_does_not_conflate_different_getstatic_accessor(self):
        body=[
           "0: getstatic #3 // Field DATA_OTHER:Lnet/minecraft/network/syncher/EntityDataAccessor;",
           "3: return"]
        result=synced_accessor_method_inventory([("whatever","()V",body)],"DATA_RADIUS")
        self.assertEqual([],result["methods_with_relevant_symbols"])

    def test_compiled_java21_constructor_field_getter(self):
        """Compiler output exercises real javap field comments and local slots."""
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            classes=root/"classes"
            files={
                "net/minecraft/world/level/Level.java":
                    "package net.minecraft.world.level; public class Level {}\n",
                "net/minecraft/world/entity/LivingEntity.java":
                    "package net.minecraft.world.entity; public class LivingEntity {}\n",
                "com/somake/somakespells/entity/FuneralBloomControllerEntity.java":
                    "package com.somake.somakespells.entity;\n"
                    "import net.minecraft.world.level.Level;\n"
                    "import net.minecraft.world.entity.LivingEntity;\n"
                    "public class FuneralBloomControllerEntity {\n"
                    " private final float radius;\n"
                    " private final float impactDamage;\n"
                    " public FuneralBloomControllerEntity(Level level, LivingEntity caster,"
                    " float radius,int a,int b,int c,int d,float impactDamage,int e,int f) {\n"
                    "   this.radius=radius;\n"
                    "   this.impactDamage=impactDamage;\n"
                    " }\n"
                    " public float getRadius() {return this.radius;}\n"
                    "}\n",
            }
            sources=[]
            for rel,source in files.items():
                path=root/rel
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(source)
                sources.append(str(path))
            comp=subprocess.run(["javac","-d",str(classes),*sources],
                                text=True,capture_output=True)
            self.assertEqual(0,comp.returncode,comp.stderr)
            scan=subprocess.run(["javap","-p","-c","-s","-classpath",str(classes),FQCN],
                                text=True,capture_output=True)
            self.assertEqual(0,scan.returncode,scan.stderr)
            result=analyze(scan.stdout)
            self.assertEqual("PROVED_DIRECT_INSTANCE_FLOAT_GETTER",
                             result["getter"]["status"],result)
            proof=result["constructor_to_getter"]
            self.assertEqual("PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING",
                             proof["status"],proof)
            self.assertEqual(3,proof["jvm_local_slot"])
            self.assertEqual(1,proof["float_ordinal"])

    def test_conditional_assignment_never_certifies_constructor_bridge(self):
        body=["0: aload_1","1: ifnull 11",
              "4: aload_0","5: fload_3",
              "6: putfield #1 // Field radius:F","9: goto 11",
              "11: return"]
        result=constructor_direct_assignments(body,"radius")
        self.assertEqual("NOT_PROVED",result["status"])
        self.assertEqual("constructor_contains_conditional_or_unsupported_control_flow",
                         result["reason"])

    def test_early_return_rejected_even_with_a_direct_store(self):
        body=["0: return","1: aload_0","2: fload_3",
              "3: putfield #1 // Field radius:F","6: return"]
        result=constructor_direct_assignments(body,"radius")
        self.assertEqual("NOT_PROVED",result["status"])
        self.assertEqual("constructor_has_nonterminal_or_ambiguous_return",result["reason"])

    def test_strict_load_slot_parser(self):
        self.assertEqual(0,local_id("aload_0","","aload"))
        self.assertEqual(8,local_id("fload","8","fload"))
        self.assertIsNone(local_id("dload_2","","fload"))

if __name__=="__main__":unittest.main()
