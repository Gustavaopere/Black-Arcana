#!/usr/bin/env python3
"""Original synthetic typed assignment inventory for controller, fail-closed."""
import unittest
from somake_109_controller_fields import scan,field,token,prove_controller_field_lifecycle,certify_exact_controller_lifecycle_109,CONTROLLER
from somake_109_perk_method_probe import GateError
def fixture():
    body=[f"{i}: nop" for i in range(40)]
    body[11]="11: aload_0"
    body[12]="12: iload 6"
    body[13]="13: putfield #1 // Field witherDuration:I"
    body[18]="18: putfield #2 // Field witherAmplifier:I"
    body[21]="21: putfield #3 // Field impactDamage:F"
    body[30]="30: getfield #4 // Field activeTargetIds:Ljava/util/Set;"
    body[31]="31: invokeinterface #5, 2 // InterfaceMethod java/util/Set.add:(Ljava/lang/Object;)Z"
    return [("example","()V",body)]
class SurveyTests(unittest.TestCase):
    def test_typed_write_and_set_categories(self):
        r=scan(fixture())
        self.assertEqual("OBSERVED_CONTROLLER_FIELD_ASSIGNMENT_SURFACES_ONLY",r["status"],r)
        self.assertEqual(1,r["method_count"])
        self.assertEqual(["witherDuration","witherAmplifier","impactDamage","activeTargetIds"],
                         [z["field"] for z in r["methods"][0]["field_sites"]])
        self.assertEqual(1,len(r["methods"][0]["set_calls"]))
        self.assertIn("not a proven",r["boundary"])
    def test_no_wither_assignment_fails(self):
        rows=fixture();rows[0][2][13]="13: nop"
        self.assertEqual("NOT_PROVED",scan(rows)["status"])
    def test_wrong_release_type_is_not_silently_normalized(self):
        a=fixture();a[0][2][13]="13: putfield #1 // Field witherDuration:F"
        r=scan(a)
        self.assertEqual("F",r["methods"][0]["field_sites"][0]["descriptor"])
    def test_method_overflow_fails(self):
        self.assertEqual("NOT_PROVED",scan(fixture()*37)["status"])
    def test_instructions_not_included_verbatim(self):
        self.assertNotIn("raw_bytecode",str(scan(fixture())))
        self.assertNotIn("JAR_BYTES",str(scan(fixture())))

def lifecycle_fixture():
    def rows(n):return [f"{i}: nop" for i in range(n)]
    def put(ops,patch):
        for k,v in patch.items():ops[k]=f"{k}: {v}"
        return ops
    basic=put(rows(24),{
        4:"aload_0",5:"bipush 80",6:"putfield #1 // Field witherDuration:I",
        10:"aload_0",11:"bipush 8",12:"putfield #2 // Field maxTargets:I",
        13:"aload_0",14:"new #3 // class java/util/HashSet",15:"dup",
        16:'invokespecial #4 // Method java/util/HashSet."<init>":()V',
        17:"putfield #5 // Field activeTargetIds:Ljava/util/Set;",
    })
    specialized=put(rows(44),{
        23:"aload_0",24:"iconst_1",25:"iload 7",
        26:"invokestatic #6 // Method java/lang/Math.max:(II)I",
        27:"putfield #7 // Field maxTargets:I",
        28:"aload_0",29:"fload 8",30:"putfield #8 // Field impactDamage:F",
        31:"aload_0",32:"bipush 30",33:"iload 9",
        34:"invokestatic #6 // Method java/lang/Math.max:(II)I",
        35:"putfield #9 // Field witherDuration:I",
        36:"aload_0",37:"iconst_0",38:"iload 10",
        39:"invokestatic #6 // Method java/lang/Math.max:(II)I",
        40:"putfield #10 // Field witherAmplifier:I",
    })
    read=put(rows(52),{
        29:"aload_0",30:"aload_1",31:"ldc #11 // String ImpactDamage",
        32:"invokevirtual #12 // Method net/minecraft/nbt/CompoundTag.getFloat:(Ljava/lang/String;)F",
        33:"putfield #8 // Field impactDamage:F",
        34:"aload_0",35:"bipush 30",36:"aload_1",37:"ldc #13 // String WitherDuration",
        38:"invokevirtual #14 // Method net/minecraft/nbt/CompoundTag.getInt:(Ljava/lang/String;)I",
        39:"invokestatic #6 // Method java/lang/Math.max:(II)I",
        40:"putfield #9 // Field witherDuration:I",
        41:"aload_0",42:"iconst_0",43:"aload_1",44:"ldc #15 // String WitherAmplifier",
        45:"invokevirtual #14 // Method net/minecraft/nbt/CompoundTag.getInt:(Ljava/lang/String;)I",
        46:"invokestatic #6 // Method java/lang/Math.max:(II)I",
        47:"putfield #10 // Field witherAmplifier:I",
    })
    save=put(rows(45),{
        28:"getfield #8 // Field impactDamage:F",
        29:"invokevirtual #12 // Method net/minecraft/nbt/CompoundTag.putFloat:(Ljava/lang/String;F)V",
        33:"getfield #9 // Field witherDuration:I",
        34:"invokevirtual #14 // Method net/minecraft/nbt/CompoundTag.putInt:(Ljava/lang/String;I)V",
        38:"getfield #10 // Field witherAmplifier:I",
        39:"invokevirtual #14 // Method net/minecraft/nbt/CompoundTag.putInt:(Ljava/lang/String;I)V",
    })
    prune=put(rows(46),{
        34:"aload_2",35:"aload 4",
        36:"invokevirtual #16 // Method com/somake/somakespells/entity/FuneralBloomBudEntity.getTargetUuid:()Ljava/util/UUID;",
        37:"invokeinterface #17, 2 // InterfaceMethod java/util/Set.add:(Ljava/lang/Object;)Z",
        40:"aload_0",41:"getfield #5 // Field activeTargetIds:Ljava/util/Set;",
        42:"aload_2",
        43:"invokeinterface #18, 2 // InterfaceMethod java/util/Set.retainAll:(Ljava/util/Collection;)Z",
    })
    pred=put(rows(13),{
        0:"aload_0",1:"aload_1",2:"aload_2",
        3:"invokevirtual #19 // Method isValidTarget:(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",
        4:"ifeq 12",
        5:"aload_0",6:"getfield #5 // Field activeTargetIds:Ljava/util/Set;",
        7:"aload_2",8:"invokevirtual #20 // Method net/minecraft/world/entity/Entity.getUUID:()Ljava/util/UUID;",
        9:"invokeinterface #21, 2 // InterfaceMethod java/util/Set.contains:(Ljava/lang/Object;)Z",
        10:"ifne 12",
    })
    return [
        (CONTROLLER,"(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V",basic),
        (CONTROLLER,"(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V",specialized),
        ("readAdditionalSaveData","(Lnet/minecraft/nbt/CompoundTag;)V",read),
        ("addAdditionalSaveData","(Lnet/minecraft/nbt/CompoundTag;)V",save),
        ("pruneTargets","(Lnet/minecraft/server/level/ServerLevel;)V",prune),
        ("lambda$launchWave$0","(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z",pred),
    ]

class ControllerLifecycleNativeTests(unittest.TestCase):
    def test_constructor_nbt_and_uuid_membership_are_instance_scoped(self):
        p=prove_controller_field_lifecycle(lifecycle_fixture())
        self.assertEqual("PROVED_CONTROLLER_CONSTRUCTOR_NBT_AND_LOCAL_UUID_MEMBERSHIP_OPERATIONS",p["status"],p)
        self.assertEqual("Math.max_int(30,ctor_int_slot9)",p["specialized_wither_duration"])
        self.assertEqual("Math.max_int(0,ctor_int_slot10)",p["specialized_wither_amplifier"])
        self.assertIn("retainAll",p["prune"])
        self.assertIn("cross-controller dedup",p["boundary"])
        certify_exact_controller_lifecycle_109(p)
    def test_wrong_ctor_max_targets_floor_rejected(self):
        x=lifecycle_fixture();x[1][2][24]="24: iconst_0"
        self.assertEqual("NOT_PROVED",prove_controller_field_lifecycle(x)["status"])
    def test_nbt_restore_type_changed_rejected(self):
        x=lifecycle_fixture();x[2][2][32]="32: invokevirtual #12 // Method net/minecraft/nbt/CompoundTag.getInt:(Ljava/lang/String;)I"
        self.assertEqual("NOT_PROVED",prove_controller_field_lifecycle(x)["status"])
    def test_prune_retainAll_replaced_rejected(self):
        x=lifecycle_fixture();x[4][2][43]="43: invokeinterface #18, 2 // InterfaceMethod java/util/Set.addAll:(Ljava/util/Collection;)Z"
        self.assertEqual("NOT_PROVED",prove_controller_field_lifecycle(x)["status"])
    def test_predicate_uuid_source_drift_rejected(self):
        x=lifecycle_fixture();x[5][2][7]="7: aload_1"
        self.assertEqual("NOT_PROVED",prove_controller_field_lifecycle(x)["status"])
    def test_ambiguous_constructor_rejected(self):
        x=lifecycle_fixture();x.append(x[0])
        self.assertEqual("NOT_PROVED",prove_controller_field_lifecycle(x)["status"])
    def test_fingerprint_drift_rejected(self):
        p=prove_controller_field_lifecycle(lifecycle_fixture())
        for update in ({"prune":"global dedup"},{"boundary":"per-player mutator approved"},
                       {"specialized_wither_duration":"input"},{"active_target_set":"global"}):
            with self.subTest(update=update):
                with self.assertRaises(GateError):
                    certify_exact_controller_lifecycle_109(dict(p,**update))
if __name__=="__main__":
    unittest.main()

    unittest.main()
