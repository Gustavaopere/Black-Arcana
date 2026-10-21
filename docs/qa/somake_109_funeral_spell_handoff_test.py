#!/usr/bin/env python3
"""Own synthetic fixtures for clean-room Somake funeral spell handoff."""
import unittest
from somake_109_funeral_spell_handoff import spell_scout,meaning
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
if __name__=="__main__":unittest.main()
