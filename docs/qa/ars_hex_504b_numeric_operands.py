#!/usr/bin/env python3
"""Read-only fail-closed bounded numeric operand verification for Ars Hex 5.0.4b.

Requires the independently SHA-1-gated published provider JAR. Reports exact
constant-load and arithmetic opcodes *inside* specific compiled methods.
Neither constant presence nor instruction order establishes operand provenance,
branch reachability, final player attributes, or resource settlement.
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
DOUBLE = re.compile(r"//\s+double\s+(-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)d?\b")


def instructions(block: str) -> list[dict]:
    result = []
    for line in block.splitlines():
        m = INSTRUCTION.match(line)
        if m:
            value = None
            comment = DOUBLE.search(m.group(3))
            if comment is not None and m.group(2) in {"ldc", "ldc_w", "ldc2_w"}:
                value = float(comment.group(1))
            result.append({"pc": int(m.group(1)), "opcode": m.group(2), "float": value})
    if not result:
        raise ValueError("no bytecode instructions in target method")
    return result


def examine(dis: dict[str, str]) -> dict:
    if set(dis) != {"soul_ward", "magic_proficiency", "spirit_spoils", "scythe"}:
        raise ValueError("required disassemblies not complete")
    methods = {key: method_block(dis[key], "getManaDiscount" if key == "scythe" else "applyAttributeModifiers")
               for key in dis}
    rows = {}
    for key, expected in (("soul_ward", (0.5,)), ("magic_proficiency", (0.1,)),
                          ("spirit_spoils", ()), ("scythe", (0.2,))):
        ops = instructions(methods[key])
        constants = sorted(set(item["float"] for item in ops if item["float"] is not None))
        missing = [value for value in expected if value not in constants]
        if missing:
            raise ValueError(f"{key}: compiled double constants missing {missing}, found {constants}")
        if key == "soul_ward" and not any(item["opcode"] == "iconst_2" for item in ops):
            raise ValueError("soul_ward: constant 2 iconst_2 missing")
        if key in {"soul_ward", "magic_proficiency", "scythe"} and not any(
                item["opcode"] in ("dmul", "fmul") for item in ops):
            raise ValueError(f"{key}: multiplication opcode missing")
        if key in {"soul_ward", "magic_proficiency", "spirit_spoils"} and not any(
                item["opcode"] in ("iload_3", "iload") and
                (item["opcode"] == "iload_3" or re.search(r"\biload\s+3\b", methods[key]))
                for item in ops):
            raise ValueError(f"{key}: local slotValue index 3 load missing")
        rows[key] = {
            "expected_compiled_constants": list(expected) + ([2] if key == "soul_ward" else []),
            "expected_constant_loads_present": True,
            "arithmetic_opcode_present": key != "spirit_spoils",
            "slot_value_load_index_3_present": key != "scythe",
            "proof_scope": "BOUNDED_CONSTANT_LOADS_AND_OPCODES_NOT_DATAFLOW",
        }
    return {
        "status": "PASS_BOUNDED_NUMERIC_OPERANDS",
        "evidence_class": "PUBLISHER_BINARY_CONSTANT_PRESENCE",
        "classes": rows,
        "limitations": [
            "No def-use or control-flow graph; presence of constants and opcodes does not prove formula semantics.",
            "A source-pinned coefficient can occur in the same method without feeding the expected final attribute.",
            "No live equipped ServerPlayer or hostile hit/mana settlement executed.",
        ],
    }


class Tests(unittest.TestCase):
    def setUp(self):
        self.dis = {
            "soul_ward": self.perk(["iconst_2", "iload_3", "imul",
                                    "ldc2_w #4 // double 0.5d", "dmul"]),
            "magic_proficiency": self.perk(["iload_3", "ldc2_w #5 // double 0.1d", "dmul"]),
            "spirit_spoils": self.perk(["iload_3", "i2d"]),
            "scythe": self.discount(["ldc2_w #6 // double 0.2d", "dmul"]),
        }

    @staticmethod
    def perk(ops: list[str]) -> str:
        return "public class Foo {\n  public void applyAttributeModifiers();\n    descriptor: ()V\n    Code:\n" + "\n".join(
            f"      {i}: {text}" for i, text in enumerate(ops)) + "\n}"

    @staticmethod
    def discount(ops: list[str]) -> str:
        return "public class Foo {\n  public int getManaDiscount();\n    descriptor: ()I\n    Code:\n" + "\n".join(
            f"      {i}: {text}" for i, text in enumerate(ops)) + "\n}"

    def test_positive_compiled_operands(self):
        self.assertEqual(examine(self.dis)["status"], "PASS_BOUNDED_NUMERIC_OPERANDS")

    def test_missing_method_is_failure(self):
        self.dis["scythe"] = self.dis["scythe"].replace("getManaDiscount", "notOurMethod")
        with self.assertRaises(ValueError):
            examine(self.dis)

    def test_missing_ward_two_is_failure(self):
        self.dis["soul_ward"] = self.dis["soul_ward"].replace("iconst_2", "iconst_1")
        with self.assertRaisesRegex(ValueError, "constant 2"):
            examine(self.dis)

    def test_missing_ward_half_is_failure(self):
        self.dis["soul_ward"] = self.dis["soul_ward"].replace("0.5d", "0.4d")
        with self.assertRaisesRegex(ValueError, "0.5"):
            examine(self.dis)

    def test_missing_magic_tenth_is_failure(self):
        self.dis["magic_proficiency"] = self.dis["magic_proficiency"].replace("0.1d", "0.2d")
        with self.assertRaisesRegex(ValueError, "0.1"):
            examine(self.dis)

    def test_missing_scythe_fifth_is_failure(self):
        self.dis["scythe"] = self.dis["scythe"].replace("0.2d", "0.3d")
        with self.assertRaisesRegex(ValueError, "0.2"):
            examine(self.dis)

    def test_absent_multiplication_is_failure(self):
        self.dis["magic_proficiency"] = self.dis["magic_proficiency"].replace("dmul", "dadd")
        with self.assertRaisesRegex(ValueError, "multiplication"):
            examine(self.dis)

    def test_missing_slot_value_is_failure(self):
        self.dis["spirit_spoils"] = self.dis["spirit_spoils"].replace("iload_3", "iload_2")
        with self.assertRaisesRegex(ValueError, "slotValue"):
            examine(self.dis)

    def test_no_double_comment_false_positive(self):
        self.dis["scythe"] = self.dis["scythe"].replace("ldc2_w #6 // double 0.2d",
                                                        "ldc2_w #6 // String 0.2d")
        with self.assertRaisesRegex(ValueError, "0.2"):
            examine(self.dis)

    def test_missing_class_fail_closed(self):
        self.dis.pop("spirit_spoils")
        with self.assertRaisesRegex(ValueError, "not complete"):
            examine(self.dis)

    def test_missing_instruction_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "no bytecode"):
            instructions("    Code:\n       nonsense\n")

    def test_decimals_support_exponent(self):
        op = instructions("      2: ldc2_w #7 // double 1.0E-1d")
        self.assertEqual(op[0]["float"], 0.1)


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
        base = inspect_jar(args.jar)  # independently pins SHA, metadata and original causal references
        dis = {key: javap(args.jar, CLASSES[key]) for key in
               ("soul_ward", "magic_proficiency", "spirit_spoils", "scythe")}
        report = examine(dis)
        report["publisher_sha1"] = base["publisher_sha1"]
        report["publisher_sha256"] = base["publisher_sha256"]
        report["publisher_bytes"] = base["publisher_bytes"]
        report["prerequisite_status"] = base["status"]
    except (OSError, ValueError) as exc:
        report = {"status": "FAIL_CLOSED", "evidence_class": "NO_NEW_BINARY_PROOF",
                  "deviations": [str(exc)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "deviations": report.get("deviations", [])}))
    return 0 if report["status"] == "PASS_BOUNDED_NUMERIC_OPERANDS" else 2


if __name__ == "__main__":
    sys.exit(main())
