#!/usr/bin/env python3
"""Synthetic tests for observed JVM call owner/opcode vs unproven dispatch."""
import unittest
import winds_105_aeropic_recast_invokes as audit
import winds_105_spell_metadata as binary

BASE = """public class net.raptorzizi.wind_spellbooks.effect.AeropicEffect {
  public void applyEffectTick(net.minecraft.world.entity.LivingEntity, int);
    Code:
       2: invokevirtual #17 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
       5: invokevirtual #19 // Method io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.addRecast:(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z
  public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);
    Code:
       1: invokevirtual #17 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I
  public void onEffectRemoved(net.minecraft.world.entity.LivingEntity, int);
    Code:
       1: invokevirtual #22 // Method io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.decrementRecastCount:(Ljava/lang/String;)V
}"""

class EffectCallsiteTests(unittest.TestCase):
    def test_exact_two_method_symbol_provenance(self):
        found=audit.scan(BASE)
        self.assertEqual({"applyEffectTick","onEffectAdded"},set(found))
        self.assertEqual("invokevirtual",found["applyEffectTick"]["invocation_opcode"])
        self.assertEqual("NOT_PROVEN",found["onEffectAdded"]["dynamic_receiver_type"])
        self.assertEqual(1,len(found["applyEffectTick"]["related_call_symbols_in_same_method"]))
        self.assertEqual(2,audit.verify(binary.EXPECTED_SHA1,found)["call_site_total"])

    def test_host_api_not_certified_by_provider(self):
        report=audit.verify(binary.EXPECTED_SHA1,audit.scan(BASE))
        self.assertEqual("NOT_VERIFIED",report["host_JAR_abi"])
        self.assertEqual("NOT_PROVEN",report["safe_mutating_hook"])

    def test_wrong_recast_owner_not_credited(self):
        other=BASE.replace("api/spells/AbstractSpell.getRecastCount","other/Spell.getRecastCount")
        with self.assertRaisesRegex(audit.EvidenceError,"one explicit"):
            audit.scan(other)

    def test_changed_descriptor_not_credited(self):
        other=BASE.replace("(ILnet/minecraft/world/entity/LivingEntity;)I","(I)I")
        with self.assertRaisesRegex(audit.EvidenceError,"one explicit"):
            audit.scan(other)

    def test_missing_effect_added_call_rejected(self):
        rows=BASE.splitlines()
        at=next(i for i,line in enumerate(rows) if "onEffectAdded(" in line)
        rows.pop(at+2)
        with self.assertRaisesRegex(audit.EvidenceError,"one explicit"):
            audit.scan("\n".join(rows))

    def test_duplicate_calls_in_one_method_rejected(self):
        rows=BASE.splitlines()
        at=next(i for i,line in enumerate(rows) if "getRecastCount" in line)
        rows.insert(at+1,rows[at].replace("2:", "3:"))
        with self.assertRaisesRegex(audit.EvidenceError,"one explicit"):
            audit.scan("\n".join(rows))

    def test_overloaded_caller_rejected(self):
        rows=BASE.replace("  public void onEffectRemoved(",
                          "  public void onEffectAdded(java.lang.String);\n    Code:\n       0: return\n  public void onEffectRemoved(")
        with self.assertRaisesRegex(audit.EvidenceError,"duplicate/overloaded"):
            audit.scan(rows)

    def test_missing_method_rejected(self):
        rows=BASE.replace("  public void onEffectAdded(", "  public void renamed(")
        with self.assertRaisesRegex(audit.EvidenceError,"missing exact"):
            audit.scan(rows)

    def test_wrong_sha_rejected(self):
        with self.assertRaisesRegex(audit.EvidenceError,"non-frozen"):
            audit.verify("0"*40,audit.scan(BASE))

    def test_call_from_non_recast_method_not_counted(self):
        rows=BASE.replace(
            "       1: invokevirtual #22 // Method io/redspace/ironsspellbooks/capabilities",
            "       1: invokevirtual #17 // Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I\n       2: invokevirtual #22 // Method io/redspace/ironsspellbooks/capabilities"
        )
        self.assertEqual(2,audit.verify(binary.EXPECTED_SHA1,audit.scan(rows))["call_site_total"])

if __name__=="__main__":
    unittest.main()
