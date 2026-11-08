#!/usr/bin/env python3
"""Synthetic fail-closed tests for the exact Straight Hook discovery probe."""
import unittest

from alexscaves_1010_straight_hook_static_probe import (
    HOOK, ITEM, HOOK_SHA, ITEM_SHA, TAG_SHA, window, require, digest, certify_compiled_branches,
)


def ins(offset: int, symbol: str = "", opcode: str = "nop") -> dict:
    return {"offset": offset, "opcode": opcode, "operand": "", "symbol": symbol}


def method(rows: list[dict]) -> dict:
    return {"instructions": rows}


class TestStraightHookProbe(unittest.TestCase):
    def test_identity_constants_are_sha256(self):
        for value in (HOOK_SHA, ITEM_SHA, TAG_SHA):
            self.assertEqual(len(value), 64)
            self.assertTrue(all(ch in "0123456789abcdef" for ch in value))

    def test_distinct_hook_and_item(self):
        self.assertNotEqual(HOOK, ITEM)

    def test_hash_is_real_sha256(self):
        self.assertEqual(digest(b"abc"),
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_straight_enchantment_pivot(self):
        result = window(method([ins(0), ins(3, "Field STRAIGHT_HOOK:"), ins(6)]),
                        "STRAIGHT_HOOK")
        self.assertEqual(1, len(result))
        self.assertEqual(3, result[0]["offset"])

    def test_gravity_state_pivot(self):
        result = window(method([ins(0), ins(3, "Field RESISTS_GRAVITY:"),
                                ins(6, "Method setNoGravity:")]), "RESISTS_GRAVITY")
        self.assertEqual([3], [row["offset"] for row in result])

    def test_short_gravity_method_includes_return_branch(self):
        rows = [ins(i, "Field RESISTS_GRAVITY:" if i == 11 else "",
                    "getstatic" if i == 11 else "nop") for i in range(20)]
        evidence = window(method(rows), "RESISTS_GRAVITY")
        self.assertEqual(20, len(evidence[0]["instructions"]))
        self.assertEqual(19, evidence[0]["instructions"][-1]["offset"])

    def test_no_pivot_is_not_fake_evidence(self):
        self.assertEqual([], window(method([ins(1), ins(2)]), "STRAIGHT_HOOK"))

    def test_evidence_is_bounded(self):
        entries = [ins(i, "STRAIGHT_HOOK") for i in range(60)]
        with self.assertRaisesRegex(ValueError, "unbounded JVM pivot"):
            window(method(entries), "STRAIGHT_HOOK")


    def test_exact_gravity_cfg_rejects_changed_branch(self):
        offsets = [0, 1, 4, 7, 8, 11, 14, 17, 20, 23, 26, 27,
                   30, 33, 36, 37, 40, 41, 44, 47]
        code = {i: ins(i) for i in offsets}
        checks = {
            1: ("invokevirtual", "isReeling:()Z", ""),
            4: ("ifne", "", "40"),
            11: ("getstatic", "RESISTS_GRAVITY", ""),
            23: ("ifeq", "", "44"),
            30: ("invokevirtual", "horizontalDistance:()D", ""),
            33: ("ldc2_w", "double 0.05000000074505806d", "#607"),
            37: ("ifle", "", "44"),
            40: ("dconst_0", "", ""),
            41: ("goto", "", "47"),
            44: ("ldc2_w", "double 0.07999999821186066d", "#609"),
            47: ("dreturn", "", ""),
        }
        for i, (op, sym, operand) in checks.items():
            code[i].update(opcode=op, symbol=sym, operand=operand)
        ctor = [
            {"offset": i, "opcode": op, "symbol": sym, "operand": operand}
            for i, op, sym, operand in (
                (437, "getstatic", "STRAIGHT_HOOK", ""),
                (440, "invokestatic", "ACCompat.enchantLevel:", ""),
                (443, "ifle", "", "460"),
                (450, "getstatic", "RESISTS_GRAVITY", ""),
                (453, "iconst_1", "", ""),
                (457, "invokevirtual", "SynchedEntityData.set:", ""))
        ]
        data = {"bounded_pivot_witnesses": [
            {"name": "getDefaultGravity", "descriptor": "()D", "instructions": 20,
             "parsed_sha256": "aa", "windows": [
                 {"pivot": "RESISTS_GRAVITY", "instructions": [code[i] for i in offsets]}]},
            {"name": "CandyCaneHookEntity", "descriptor":
             "(Lnet/minecraft/world/item/ItemStack;)V",
             "windows": [{"pivot": "STRAIGHT_HOOK", "instructions": ctor}]}
        ]}
        self.assertEqual("0.07999999821186066",
                         certify_compiled_branches(data)["otherwise_return_gravity"])
        code[37]["operand"] = "40"
        with self.assertRaisesRegex(ValueError, "gravity CFG mismatch"):
            certify_compiled_branches(data)

    def test_require_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "test failure"):
            require(False, "test failure")

    def test_true_require_is_noop(self):
        self.assertIsNone(require(True, "should not fail"))


if __name__ == "__main__":
    unittest.main()
