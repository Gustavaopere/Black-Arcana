#!/usr/bin/env python3
"""Fail-closed static control-flow signature for the Ars Hex scythe mana discount.

Proof scope: exactly one SHA-verified published classfile method, direct
Necromancy-selected iteration, 0.2 * getCastingCost sum and ceil return.
Not proof of mana settlement, player activation, or final host expense.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unittest

from ars_hex_504b_perk_bytecode import CLASSES, inspect_jar, javap, method_block


INSTRUCTION = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")
EXPECTED = (
    "dconst_0 dstore_3 aload_2 invokevirtual invokeinterface astore "
    "aload invokeinterface ifeq aload invokeinterface checkcast astore "
    "getstatic aload invokevirtual ifeq dload_3 ldc2_w aload invokevirtual "
    "i2d dmul dadd dstore_3 goto dload_3 invokestatic ireturn"
).split()
EXPECTED_PCS = (0, 1, 2, 3, 6, 11, 13, 15, 20, 23, 25, 30, 33, 35,
                38, 40, 43, 46, 47, 50, 52, 55, 56, 57, 58, 59, 62, 63, 66)


def parse(block: str):
    lines = []
    for line in block.splitlines():
        if (m := INSTRUCTION.match(line)):
            lines.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    return lines


def contains(line, token: str) -> bool:
    return token in line[2].split("//", 1)[-1]


def local_slot(line, op: str, slot: int):
    if line[1] != op or not re.match(rf"^{slot}(?:\s|$)", line[2]):
        raise ValueError(f"unexpected {op} local slot at pc={line[0]}")


def branch(line, op: str, target: int):
    if line[1] != op or not re.match(rf"^{target}(?:\s|$)", line[2]):
        raise ValueError(f"unexpected control flow at pc={line[0]} ({op}->{target})")


def audit_discount(block: str):
    rows = parse(block)
    if tuple(pc for pc, _, _ in rows) != EXPECTED_PCS:
        raise ValueError("scythe method program counters differ from bounded publisher fingerprint")
    if [op for _, op, _ in rows] != EXPECTED:
        raise ValueError("scythe method opcode structure differs from bounded signature")
    line = {x[0]: x for x in rows}
    for pc, label in ((3, "unsafeList"), (6, "iterator"), (15, "hasNext"),
                      (25, "next"), (30, "AbstractSpellPart"),
                      (35, "NECROMANCY"), (40, "isPartOfSchool"),
                      (47, "double 0.2d"), (52, "getCastingCost"), (63, "ceil")):
        if not contains(line[pc], label):
            raise ValueError(f"pc={pc} missing required compiled marker {label}")
    for pc, op, slot in ((11, "astore", 5), (13, "aload", 5),
                         (23, "aload", 5), (33, "astore", 6),
                         (38, "aload", 6), (50, "aload", 6)):
        local_slot(line[pc], op, slot)
    branch(line[20], "ifeq", 62)     # after foreach
    branch(line[43], "ifeq", 59)     # non-Necromancy continues foreach
    branch(line[59], "goto", 13)     # loop back to hasNext
    return {
        "status": "PASS_BOUNDED_SCYTHE_DISCOUNT_FLOW",
        "scope": "PUBLISHER_BINARY_ONE_METHOD_WITH_FIXED_OFFSETS_BRANCHES_AND_LOCALS",
        "observations": {
            "initial_accumulator": "double 0.0, local3",
            "iteration": "Spell.unsafeList() -> Iterator; loop local5; part local6",
            "condition": "SpellSchools.NECROMANCY.isPartOfSchool(part)",
            "accumulation": "local3 += 0.2d * (double) part.getCastingCost()",
            "result": "Mth.ceil(local3)",
        },
        "limits": [
            "An exact fixed-offset signature is not a complete JVM control-flow or type verifier.",
            "The signature shows how getManaDiscount calculates a value; not whether the host ever calls it.",
            "Does not prove actual mana debit, configuration, performance, equipment eligibility or gameplay.",
        ],
    }


REFERENCE_COMMENTS = {
    3: "// Method com/hollingsworth/arsnouveau/api/spell/Spell.unsafeList:()Ljava/util/List;",
    6: "// InterfaceMethod java/util/List.iterator:()Ljava/util/Iterator;",
    15: "// InterfaceMethod java/util/Iterator.hasNext:()Z",
    25: "// InterfaceMethod java/util/Iterator.next:()Ljava/lang/Object;",
    30: "// class com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart",
    35: "// Field com/hollingsworth/arsnouveau/api/spell/SpellSchools.NECROMANCY:LSpellSchool;",
    40: "// Method com/hollingsworth/arsnouveau/api/spell/SpellSchool.isPartOfSchool:(LAbstractSpellPart;)Z",
    47: "// double 0.2d",
    52: "// Method com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.getCastingCost:()I",
    63: "// Method net/minecraft/util/Mth.ceil:(D)I",
}
LOCALS = {11: "5", 13: "5", 23: "5", 33: "6", 38: "6", 50: "6"}
BRANCHES = {20: "62", 43: "59", 59: "13"}


def fixture() -> str:
    result = ["public class Scythe {", "  public int getManaDiscount();",
              "    descriptor: ()I", "    Code:"]
    for pc, op in zip(EXPECTED_PCS, EXPECTED):
        operand = LOCALS.get(pc, BRANCHES.get(pc, ""))
        comment = REFERENCE_COMMENTS.get(pc, "")
        result.append(f"      {pc}: {op} {operand} {comment}".rstrip())
    return "\n".join(result + ["}"])


class Tests(unittest.TestCase):
    def test_control(self):
        self.assertEqual(audit_discount(fixture())["status"], "PASS_BOUNDED_SCYTHE_DISCOUNT_FLOW")

    def test_missing_method(self):
        with self.assertRaises(ValueError):
            audit_discount("public class X { }")

    def test_coefficient_drift(self):
        with self.assertRaisesRegex(ValueError, "0.2"):
            audit_discount(fixture().replace("double 0.2d", "double 0.3d"))

    def test_wrong_necromancy_condition(self):
        with self.assertRaisesRegex(ValueError, "NECROMANCY"):
            audit_discount(fixture().replace("SpellSchools.NECROMANCY", "SpellSchools.FIRE"))

    def test_wrong_casting_cost_source(self):
        with self.assertRaisesRegex(ValueError, "getCastingCost"):
            audit_discount(fixture().replace("getCastingCost", "getOtherCost"))

    def test_wrong_branch_target(self):
        with self.assertRaisesRegex(ValueError, "control flow"):
            audit_discount(fixture().replace("43: ifeq 59", "43: ifeq 62"))

    def test_wrong_local(self):
        with self.assertRaisesRegex(ValueError, "local slot"):
            audit_discount(fixture().replace("50: aload 6", "50: aload 5"))

    def test_missing_addition(self):
        with self.assertRaisesRegex(ValueError, "opcode structure"):
            audit_discount(fixture().replace("57: dadd", "57: dsub"))

    def test_wrong_ceil(self):
        with self.assertRaisesRegex(ValueError, "ceil"):
            audit_discount(fixture().replace("Mth.ceil", "Mth.floor"))

    def test_unexpected_extra_opcode(self):
        with self.assertRaisesRegex(ValueError, "program counters"):
            audit_discount(fixture().replace("66: ireturn", "65: nop\n      66: ireturn"))

    def test_missing_loop_return(self):
        with self.assertRaisesRegex(ValueError, "control flow"):
            audit_discount(fixture().replace("59: goto 13", "59: goto 23"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    if not args.jar or not args.output:
        parser.error("--jar and --output required")
    try:
        base = inspect_jar(args.jar)
        block = method_block(javap(args.jar, CLASSES["scythe"]), "getManaDiscount")
        report = audit_discount(block)
        report["publisher_sha1"] = base["publisher_sha1"]
        report["publisher_sha256"] = base["publisher_sha256"]
        report["publisher_bytes"] = base["publisher_bytes"]
    except (OSError, ValueError) as exc:
        report = {"status": "FAIL_CLOSED", "deviations": [str(exc)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "deviations": report.get("deviations", [])}))
    return 0 if report["status"] == "PASS_BOUNDED_SCYTHE_DISCOUNT_FLOW" else 2


if __name__ == "__main__":
    sys.exit(main())
