#!/usr/bin/env python3
"""Synthetic provenance-boundary and fail-closed tests for exact Wind effect audit."""
import unittest

import winds_105_effect_boundaries as effect
import winds_105_spell_metadata as binary

def methods(*, read=(), names=("onCast",)):
    return {f"public void {name}();": {
        "read_fields": list(read), "written_fields": [],
        "invoked_symbols": [], "numeric_opcodes": [],
        "branch_opcodes": [], "literal_operands": []} for name in names}

def sample():
    classes = {binary.BASE + cls: methods() for cls in binary.ROSTER.values()}
    class_name = "net.raptorzizi.wind_spellbooks.effect.TailwindEffect"
    classes[class_name] = methods(names=("applyEffectTick","getAttributeModifiers"))
    sp = {}
    for spell, class_name in binary.ROSTER.items():
        field = effect.ENTRY_SPELLS.get(spell)
        fields = [] if field is None else [
            "net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry."
            + field + ":Lnet/neoforged/neoforge/registries/DeferredHolder;"
        ]
        sp[spell] = {"methods": methods(read=fields)}
    return (
        {"result":"PASS","sha1":binary.EXPECTED_SHA1,
         "class_count":7,"provider":"wind_spellbooks","spells":sp},
        classes,sorted(classes),
    )

class BoundariesTest(unittest.TestCase):
    def test_expected_registry_facts_and_named_candidate(self):
        doc,classes,universe=sample()
        out=effect.summarize(doc,classes,universe)
        self.assertEqual("PASS_SHA_EXACT_EFFECT_CANDIDATE_SYMBOL_AUDIT",out["result"])
        self.assertEqual(8,out["classes_inspected"])
        self.assertEqual("TAILWIND",out["entry_spell_field_refs"]["tailwind"]["referenced_provider_effect_registry_field"])
        self.assertFalse(out["entry_spell_field_refs"]["aeropic"]["effect_class_or_instance_proven"])
        candidate=out["candidate_classes"]["net.raptorzizi.wind_spellbooks.effect.TailwindEffect"]
        self.assertEqual("NOT_PROVEN",candidate["runtime_effect_settlement"])
        self.assertTrue(any("applyEffectTick" in n for n in candidate["candidate_methods"]))

    def test_missing_effect_field_fails_closed(self):
        doc,classes,universe=sample()
        doc["spells"]["tailwind"]["methods"]=methods()
        with self.assertRaisesRegex(effect.EvidenceError,"missing exact spell"):
            effect.summarize(doc,classes,universe)

    def test_missing_acrobatics_field_fails_closed(self):
        doc,classes,universe=sample()
        doc["spells"]["aeropic"]["methods"]=methods()
        with self.assertRaisesRegex(effect.EvidenceError,"ACROBATICS"):
            effect.summarize(doc,classes,universe)

    def test_wrong_sha_fails_closed(self):
        doc,classes,universe=sample()
        doc["sha1"]="0"*40
        with self.assertRaisesRegex(effect.EvidenceError,"SHA-verified"):
            effect.summarize(doc,classes,universe)

    def test_incomplete_provider_class_universe_fails(self):
        doc,classes,universe=sample()
        del classes[universe[0]]
        with self.assertRaisesRegex(effect.EvidenceError,"incomplete"):
            effect.summarize(doc,classes,universe)

    def test_declaration_name_alone_is_not_registration(self):
        one=effect.classify("net.raptorzizi.wind_spellbooks.effects.AcrobaticsEffect",
                            methods(names=("tick",)))
        self.assertTrue(one["class_name_candidate"])
        self.assertEqual("CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY",one["classification"])
        self.assertEqual({},one["effect_registry_references"])

    def test_reference_without_effect_name_is_explicit(self):
        row=effect.classify("net.raptorzizi.wind_spellbooks.SpellThing",methods(
            read=["com/example/Registry.TAILWIND:Ljava/lang/Object;"]))
        self.assertFalse(row["class_name_candidate"])
        self.assertEqual(["TAILWIND"],next(iter(row["effect_registry_references"].values())))

    def test_unrelated_class_is_excluded(self):
        self.assertIsNone(effect.classify("net.raptorzizi.wind_spellbooks.Foo",methods()))

    def test_no_candidate_rejected(self):
        doc,classes,universe=sample()
        classes={name: methods() for name in universe}
        # Class name still contains Effect, so a positive candidate remains.
        self.assertGreaterEqual(effect.summarize(doc,classes,universe)["candidate_class_count"],1)

    def test_duplicate_universe_rejected(self):
        doc,classes,universe=sample()
        with self.assertRaisesRegex(effect.EvidenceError,"non-canonical"):
            effect.summarize(doc,classes,universe+[universe[-1]])

if __name__=="__main__":
    unittest.main()
