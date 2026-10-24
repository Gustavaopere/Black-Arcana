#!/usr/bin/env python3
"""Independent synthetic callsite attribution and non-promotion checks."""
import unittest

import winds_105_cross_class_getter_calls as cross
import winds_105_getter_consumer_edges as edges
import winds_105_spell_metadata as binary

def sample():
    result = {}
    all_owners = []
    for spell, callers in edges.EXPECTED_CALLERS.items():
        fqcn = binary.BASE + binary.ROSTER[spell]
        code = ["public class " + fqcn + " {"]
        mapping = {}
        for getter, methods in callers.items():
            for method in methods:
                mapping.setdefault(method, []).append((getter, edges.GETTERS[spell][getter]))
        for name, getter_rows in mapping.items():
            code += ["  public void "+name+"();", "    Code:"]
            for i, (getter, descriptor) in enumerate(getter_rows):
                code.append(f"       {i}: invokevirtual #12 // Method {getter}:{descriptor}")
            code += ["       50: return"]
        code += ["}"]
        result[fqcn] = "\n".join(code)
        all_owners.append(fqcn)
    other = "net.raptorzizi.wind_spellbooks.effects.TailwindEffect"
    result[other] = "public class TailwindEffect {\n  public void apply();\n    Code:\n       0: return\n}"
    return result

class CrossClassCallTests(unittest.TestCase):
    def test_own_class_shorthand_resolves_only_in_own_class(self):
        own = binary.BASE + "TailwindSpell"
        body = "public class TailwindSpell {\n  public void method();\n    Code:\n       0: invokevirtual #12 // Method getPercentJump:(I)F\n}"
        got = cross.inspect_class(own, body)
        self.assertEqual(1,len(got))
        self.assertEqual("tailwind",got[0]["callee_spell"])
        self.assertEqual("JAVAP_OWN_CLASS_SHORTHAND",got[0]["owner_attribution"])
        other = cross.inspect_class("net.raptorzizi.wind_spellbooks.effects.Effect",body)
        self.assertEqual([],other)

    def test_external_explicit_owner_detected(self):
        other="net.raptorzizi.wind_spellbooks.effects.WindEffect"
        fqref="net/raptorzizi/wind_spellbooks/spells/wind/TailwindSpell.getPercentJump:(I)F"
        body="public class WindEffect {\n  public void tick();\n    Code:\n       0: invokevirtual #20 // Method "+fqref+"\n}"
        got=cross.inspect_class(other,body)
        self.assertEqual(1,len(got))
        self.assertEqual(other,got[0]["caller_class"])
        self.assertEqual("JAVAP_EXPLICIT_CLASS_OWNER",got[0]["owner_attribution"])

    def test_no_promotion_from_same_method_effects(self):
        d=sample()
        result=cross.summarize(d,sorted(d))
        self.assertEqual(9,result["getters_scoped"])
        self.assertEqual(0,result["out_of_declaring_spell_invokes"])
        self.assertEqual("NOT_PROVEN",result["selected_getters"]["tornado"]["getDuration"]["runtime_getter_to_sink_flow"])

    def test_add_external_reference_measured_separately(self):
        d=sample()
        key="net.raptorzizi.wind_spellbooks.effects.TailwindEffect"
        d[key]=d[key].replace("0: return","0: invokevirtual #20 // Method net/raptorzizi/wind_spellbooks/spells/wind/TailwindSpell.getPercentJump:(I)F")
        got=cross.summarize(d,sorted(d))
        self.assertEqual(1,got["out_of_declaring_spell_invokes"])
        self.assertEqual(1,got["selected_getters"]["tailwind"]["getPercentJump"]["calls_outside_declaring_spell_class"])

    def test_missing_known_caller_is_fail_closed(self):
        d=sample()
        key=binary.BASE+"AeropicSpell"
        d[key]=d[key].replace("getRecastCount:","unrelated:")
        with self.assertRaises(cross.AuditError):
            cross.summarize(d,sorted(d))

    def test_wrong_descriptor_is_not_credited(self):
        key=binary.BASE+"TailwindSpell"
        body="  public void foo();\n    Code:\n       0: invokevirtual #5 // Method getPercentJump:(II)F"
        self.assertEqual([],cross.inspect_class(key,body))

    def test_unknown_owner_does_not_credit_target(self):
        key="net.raptorzizi.wind_spellbooks.effects.Effect"
        b="  public void tick();\n    Code:\n       0: invokevirtual #5 // Method other/Spell.getPercentJump:(I)F"
        self.assertEqual([],cross.inspect_class(key,b))

    def test_non_invoke_symbol_is_not_a_call(self):
        key=binary.BASE+"TailwindSpell"
        b="  public void foo();\n    Code:\n       0: getfield #12 // Field getPercentJump:(I)F"
        self.assertEqual([],cross.inspect_class(key,b))

    def test_reject_incomplete_class_universe(self):
        d=sample()
        with self.assertRaisesRegex(cross.AuditError,"incomplete provider class"):
            cross.summarize(d,sorted(d)[:-1])

    def test_code_without_header_is_not_attributable(self):
        with self.assertRaisesRegex(cross.AuditError,"no method header"):
            cross.inspect_class(binary.BASE+"TailwindSpell","    Code:\n       0: invokevirtual #1 // Method getPercentJump:(I)F")

if __name__=="__main__":
    unittest.main()
