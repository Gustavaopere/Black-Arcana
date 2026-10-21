#!/usr/bin/env python3
"""Own synthetic fixtures for clean-room Somake funeral spell handoff."""
import unittest
from somake_109_funeral_spell_handoff import spell_scout,meaning,certify_spell_cast_getters_109,GETTERS,EXPECTED,CONTROL,SPELL_ONCAST_DESC,CTOR_DESC
C="(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/LivingEntity;)V"
def specimen():
    rows=[f"{i}: nop" for i in range(145)]
    rows[19]="19: aload 3"
    rows[40]="40: invokestatic #4 // Method java/lang/Math.max:(II)I"
    rows[95]="95: invokevirtual #1 // Method getWitherDuration:(ILnet/minecraft/world/entity/LivingEntity;)I"
    rows[110]='110: invokespecial #2 // Method com/somake/somakespells/entity/FuneralBloomControllerEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V'
    return [("onCast",C,rows)]
class ScoutTests(unittest.TestCase):
    def test_detects_single_constructor_and_window(self):
        p=spell_scout(specimen())
        self.assertEqual("OBSERVED_CONTROLLER_CAST_HANDBACK_OPERANDS_ONLY",p["status"],p)
        self.assertEqual([110],[c["ctor_site"] for c in p["methods"][0]["constructor_calls"]])
        self.assertIn("no per-level values",p["boundary"])
    def test_missing_site_is_not_proved(self):
        self.assertEqual("NOT_PROVED",spell_scout([("x","()V",["0: nop"])] )["status"])
    def test_double_path_is_not_proved(self):
        self.assertEqual("NOT_PROVED",spell_scout(specimen()*2)["status"])
    def test_window_is_bounded(self):
        p=spell_scout(specimen())
        self.assertLessEqual(len(p["methods"][0]["constructor_calls"][0]["operand_window"]),93)
    def test_typed_field_without_source_code(self):
        r=(43,"getfield","", "Field witherDuration:I")
        self.assertEqual("witherDuration",meaning(2,r)["field"])
        self.assertNotIn("provider_source",meaning(2,r))

def original_synthetic_contract():
    def method_call(index,name,desc):
        cls=("java/lang/Math" if name=="max" or name=="min" else
             "net/minecraft/util/Mth" if name=="clamp" else "com/example/OriginalSpell")
        return f"{index}: invokevirtual #1 // Method {cls}.{name}:{desc}"
    synthetic=[]
    for name,desc in GETTERS.items():
        length,nums,refs=EXPECTED[name]
        body=[f"{i}: nop" for i in range(length)]
        for i,op in CONTROL[name].items():
            body[i]=f"{i}: {op}"
        for i,num in nums.items():
            if isinstance(num,int):
                op=(f"iconst_{num}" if 0<=num<=5 else
                    f"bipush {num}" if -128<=num<=127 else f"sipush {num}")
            else:op=f"ldc_w #1 // float {num}f"
            body[i]=f"{i}: {op}"
        for i,(member,call_desc) in refs.items():
            body[i]=method_call(i,member,call_desc)
        if name=="getRadius":
            body[1]="1: ifnonnull 4"
            body[3]="3: goto 9"
        if name=="getWitherAmplifier":
            body[2]="2: if_icmplt 5"
            body[4]="4: goto 6"
        synthetic.append((name,desc,body))
    c=[f"{i}: nop" for i in range(81)]
    c[8]="8: ldc2_w #1 // double 32.0d"
    c[14]="14: invokestatic #2 // Method com/example/OriginalSpell.raycastForEntity:()V"
    c[19]="19: invokestatic #3 // Method com/example/OriginalSpell.groundPosition:()V"
    c[21]="21: new #4 // class com/somake/somakespells/entity/FuneralBloomControllerEntity"
    c[22]="22: dup"
    for i,slot in {23:1,24:3,25:0,26:2,52:8,53:8,54:7,56:1,57:8}.items():
        c[i]=f"{i}: aload_{slot}" if slot<4 else f"{i}: aload {slot}"
    for first,last in ((25,26),(29,30),(32,33),(35,36),(38,39),(41,42),(45,46),(48,49)):
        c[first]=f"{first}: aload_0"
        c[last]=f"{last}: iload_2"
    c[27]="27: aload_3"
    c[43]="43: aload_3"
    calls={28:("getRadius",GETTERS["getRadius"]),31:("getDuration",GETTERS["getDuration"]),
           34:("getWaveInterval",GETTERS["getWaveInterval"]),
           37:("getTelegraphTicks",GETTERS["getTelegraphTicks"]),
           40:("getMaxTargets",GETTERS["getMaxTargets"]),
           44:("getImpactDamage",GETTERS["getImpactDamage"]),
           47:("getWitherDuration",GETTERS["getWitherDuration"]),
           50:("getWitherAmplifier",GETTERS["getWitherAmplifier"])}
    for i,(member,desc) in calls.items():
        c[i]=f"{i}: invokevirtual #6 // Method com/example/OriginalSpell.{member}:{desc}"
    c[51]=f'51: invokespecial #7 // Method com/somake/somakespells/entity/FuneralBloomControllerEntity."<init>":{CTOR_DESC}'
    c[55]="55: invokevirtual #8 // Method com/somake/somakespells/entity/FuneralBloomControllerEntity.setPos:(Lnet/minecraft/world/phys/Vec3;)V"
    c[58]="58: invokevirtual #9 // Method net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z"
    c[59]="59: pop"
    synthetic.append(("onCast",SPELL_ONCAST_DESC,c))
    return synthetic

class ExactCompiledCastGateTests(unittest.TestCase):
    def test_original_fixture_source_pins_eight_getters(self):
        p=certify_spell_cast_getters_109(original_synthetic_contract())
        self.assertEqual("PROVED_SOMAKE_FUNERAL_NATIVE_GETTER_FORMULAS_AND_CAST_TO_CONTROLLER",p["status"],p)
        self.assertEqual(81,p["on_cast_instructions"])
        self.assertEqual(8,len(p["getter_details"]))
        self.assertIn("perks",p["boundary"])
    def test_caster_spell_power_multiplier_drift_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="getImpactDamage":rows[5]="5: ldc_w #1 // float 1.75f"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_wither_amplifier_jump_drift_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="getWitherAmplifier":rows[2]="2: if_icmplt 6"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_raw_level_telegraph_integer_division_drift_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="getTelegraphTicks":rows[4]="4: irem"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_incorrect_controller_ctor_order_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="onCast":rows[47]="47: nop"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_wrong_cast_actor_getter_input_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="onCast":rows[43]="43: aload_4"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_wrong_cast_level_getter_input_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="onCast":rows[46]="46: iload_4"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_cast_spawn_boolean_drift_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="onCast":rows[59]="59: nop"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
    def test_cast_raycast_range_drift_fails(self):
        f=original_synthetic_contract()
        for n,d,rows in f:
            if n=="onCast":rows[8]="8: ldc2_w #1 // double 48.0d"
        self.assertEqual("NOT_PROVED",certify_spell_cast_getters_109(f)["status"])
if __name__=="__main__":unittest.main()
