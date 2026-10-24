#!/usr/bin/env python3
"""No-provider synthetic regression tests for the exact mobility getter gate."""
import unittest

import winds_105_mobility_getters as mobility

def samples():
    out = {}
    for spell, methods in mobility.SELECTED.items():
        chunks = ["public class demo.Spell {"]
        for name, params, ret in methods:
            chunks.extend([
                f"  public float {name}{params};",
                "    Code:",
                "       0: iload_1",
                "       1: i2f",
                "       2: fconst_2",
                "       3: fmul",
                "       4: " + ret,
            ])
        chunks.append("}")
        out[spell] = "\n".join(chunks)
    return out

class MobilityGetterTests(unittest.TestCase):
    def test_exact_five_selected_float_asts(self):
        data = mobility.inspect_compiled_methods(samples())
        self.assertEqual(5, sum(map(len, data.values())))
        for rows in data.values():
            for item in rows.values():
                self.assertEqual("EXACT_STRAIGHT_LINE_EXPRESSION", item["state"])
                self.assertEqual("fmul", item["expression_ast"]["opcode"])

    def test_missing_method_fails_closed(self):
        data=samples()
        data["iron_slash"]=data["iron_slash"].replace("getDistance", "getOther")
        with self.assertRaisesRegex(mobility.InspectionError, "UNRESOLVED"):
            mobility.inspect_compiled_methods(data)

    def test_unknown_method_body_fails_closed(self):
        data=samples()
        data["wind_jump"]=data["wind_jump"].replace("3: fmul","3: invokevirtual #99 // Method demo.Spell.unsafe:()F")
        with self.assertRaisesRegex(mobility.InspectionError, "unsupported opcode"):
            mobility.inspect_compiled_methods(data)

    def test_guarded_method_fails_closed(self):
        data=samples()
        data["tailwind"]=data["tailwind"].replace("3: fmul", "3: ifeq 5")
        with self.assertRaisesRegex(mobility.InspectionError, "unsupported opcode"):
            mobility.inspect_compiled_methods(data)

    def test_bad_stack_fails_closed(self):
        data=samples()
        data["almighty_push"]=data["almighty_push"].replace("3: fmul", "3: fconst_1")
        with self.assertRaisesRegex(mobility.InspectionError, "invalid final stack height"):
            mobility.inspect_compiled_methods(data)

    def test_unexpected_spell_is_not_permitted(self):
        data=samples()
        data["foreign_magic"]="public class demo.NotTrusted {}"
        with self.assertRaisesRegex(mobility.InspectionError, "unexpected spell"):
            mobility.inspect_compiled_methods(data)

    def test_exact_roster_is_five_methods_not_spells(self):
        self.assertEqual(4, len(mobility.SELECTED))
        self.assertEqual(5, sum(map(len, mobility.SELECTED.values())))
        self.assertNotIn("tornado", mobility.SELECTED)

if __name__ == "__main__":
    unittest.main()
