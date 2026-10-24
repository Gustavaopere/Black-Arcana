#!/usr/bin/env python3
"""Independent synthetic tests of exact-JAR call-edge evidence boundaries."""
from copy import deepcopy
import unittest

import winds_105_getter_consumer_edges as edges
import winds_105_spell_metadata as binary

def fixture():
    spells = {}
    for spell, class_name in binary.ROSTER.items():
        methods = {
            "public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity);":
                {"invoked_symbols": [], "read_fields": [], "written_fields": []},
            "public java.util.List getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);":
                {"invoked_symbols": [], "read_fields": [], "written_fields": []},
        }
        for getter, desc in edges.GETTERS.get(spell, {}).items():
            ret = "float" if desc.endswith("F") else "int"
            methods[f"public {ret} {getter}(int);"] = {
                "invoked_symbols": [], "read_fields": [], "written_fields": [],
            }
            for caller in edges.EXPECTED_CALLERS[spell][getter]:
                if caller == "getJumpHeight":
                    methods.setdefault(
                        "public float getJumpHeight(int);",
                        {"invoked_symbols": [], "read_fields": [], "written_fields": []},
                    )
                key = next(header for header in methods if f" {caller}(" in header)
                methods[key]["invoked_symbols"].append(getter + ":" + desc)
        for field, symbols in edges.ON_CAST_OBSERVATIONS.get(spell, {}).items():
            methods[next(h for h in methods if " onCast(" in h)][field].extend(symbols)
        spells[spell] = {"class": binary.BASE + class_name, "methods": methods}
    return {
        "result": "PASS", "sha1": binary.EXPECTED_SHA1, "provider": "wind_spellbooks",
        "class_count": 7, "spells": spells,
    }

class GetterEdgesTests(unittest.TestCase):
    def test_exact_roster_and_distinct_call_classes(self):
        out = edges.analyze(fixture())
        self.assertEqual("PASS_SHA_EXACT_DIRECT_CALL_EDGE_INVENTORY", out["result"])
        self.assertEqual(9, out["getters_checked"])
        self.assertEqual(6, out["spells_in_scope"])
        self.assertFalse(out["spells"]["tailwind"]["getters"]["getPercentJump"]["on_cast_direct_call"])
        self.assertTrue(out["spells"]["tornado"]["getters"]["getDuration"]["on_cast_direct_call"])
        self.assertEqual("NOT_PROVEN", out["spells"]["tornado"]["getters"]["getDuration"]["effective_consumer_argument_flow"])

    def test_wrong_sha_is_not_evidence(self):
        d=fixture();d["sha1"]="0"*40
        with self.assertRaisesRegex(edges.EvidenceError, "unverified"):
            edges.analyze(d)

    def test_direct_on_cast_call_deleted_rejected(self):
        d=fixture()
        oncast=next(x for x in d["spells"]["tornado"]["methods"] if " onCast(" in x)
        sym="getDuration:(I)I"
        d["spells"]["tornado"]["methods"][oncast]["invoked_symbols"].remove(sym)
        with self.assertRaisesRegex(edges.EvidenceError, "direct caller drift"):
            edges.analyze(d)

    def test_unexpected_direct_on_cast_call_rejected(self):
        d=fixture()
        oncast=next(x for x in d["spells"]["tailwind"]["methods"] if " onCast(" in x)
        d["spells"]["tailwind"]["methods"][oncast]["invoked_symbols"].append(
            "getPercentJump:(I)F"
        )
        with self.assertRaisesRegex(edges.EvidenceError, "direct caller drift"):
            edges.analyze(d)

    def test_missing_sink_is_not_proven(self):
        d=fixture()
        oncast=next(x for x in d["spells"]["almighty_push"]["methods"] if " onCast(" in x)
        d["spells"]["almighty_push"]["methods"][oncast]["written_fields"]=[]
        with self.assertRaisesRegex(edges.EvidenceError, "missing onCast symbol"):
            edges.analyze(d)

    def test_same_method_is_not_a_value_flow_claim(self):
        out=edges.analyze(fixture())
        self.assertEqual("SAME_METHOD_ONLY_NOT_GETTER_TO_SINK_DATAFLOW",
                         out["spells"]["almighty_push"]["copresent_sink_relationship"])
        self.assertIn("onCast", out["spells"]["almighty_push"]["getters"]["getRange"]["direct_callers"])

    def test_duplicate_method_name_fails_closed(self):
        d=fixture()
        d["spells"]["tailwind"]["methods"]["private void onCast(java.lang.String);"]={
            "invoked_symbols": [], "read_fields": [], "written_fields": []
        }
        with self.assertRaisesRegex(edges.EvidenceError, "ambiguous overloaded"):
            edges.analyze(d)

    def test_modlist_spell_roster_cannot_drift(self):
        d=fixture();d["spells"].pop("wind_blade")
        with self.assertRaisesRegex(edges.EvidenceError, "unexpected spell class roster"):
            edges.analyze(d)

    def test_no_auto_promotion_of_external_callers(self):
        d=fixture()
        oncast=next(h for h in d["spells"]["aeropic"]["methods"] if " onCast(" in h)
        d["spells"]["aeropic"]["methods"][oncast]["invoked_symbols"].append(
            "other/package/Spell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I"
        )
        out=edges.analyze(d)
        self.assertEqual(["getUniqueInfo"],out["spells"]["aeropic"]["getters"]["getRecastCount"]["direct_callers"])

if __name__=="__main__":
    unittest.main()
