#!/usr/bin/env python3
"""Narrow symbolic JVM stack proof for Ars Hex 5.0.4b perk attribute modifiers.

Read-only: checks operand origin, arithmetic, modifier constructor arguments and
withModifierAdded destinations. Rejects unsupported instructions / branches.
This is not a runtime test and does not authorize a Black Arcana adapter.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unittest

from ars_hex_504b_perk_bytecode import CLASSES, inspect_jar, javap, method_block


INSN = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")
DOUBLE = re.compile(r"//\s+double\s+(-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)d?\b")
ATTRS = {
    "SOUL_WARD_CAPACITY", "SOUL_WARD_INTEGRITY",
    "MAGIC_PROFICIENCY", "SPIRIT_SPOILS",
}
OPERATIONS = {"ADD_VALUE", "ADD_MULTIPLIED_BASE"}


class UnsupportedBytecode(ValueError):
    pass


def parse(block: str) -> list[tuple[int, str, str]]:
    out = []
    for line in block.splitlines():
        if (m := INSN.match(line)):
            out.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    if not out or len(out) > 80 or len({pc for pc, _, _ in out}) != len(out):
        raise ValueError("invalid, excessive or duplicate bytecode instructions")
    return out


def double_value(tail: str) -> float:
    m = DOUBLE.search(tail)
    if not m:
        raise UnsupportedBytecode("expected a numeric double literal")
    return float(m.group(1))


def field_symbol(tail: str) -> str:
    if "// Field " not in tail:
        raise UnsupportedBytecode("getstatic missing resolved Field comment")
    symbol = tail.split("// Field ", 1)[1].split(":", 1)[0].split(".")[-1]
    if symbol in ATTRS | OPERATIONS | {"INSTANCE"}:
        return symbol
    raise UnsupportedBytecode("unexpected static field: " + symbol)


def symbolic_perk_method(block: str) -> list[dict]:
    ops = parse(block)
    stack = []
    changes: list[dict] = []
    result = None
    for index, (pc, opcode, tail) in enumerate(ops):
        if opcode == "aload_1":
            stack.append(("receiver",))
        elif opcode == "aload" and tail.split(" ", 1)[0] == "4":
            stack.append(("slot_group",))
        elif opcode == "iload_3":
            stack.append(("slotValue",))
        elif opcode == "iconst_2":
            stack.append(("int", 2))
        elif opcode in {"ldc2_w", "ldc_w", "ldc"}:
            stack.append(("double", double_value(tail)))
        elif opcode == "i2d":
            v = stack.pop()
            stack.append(("as_double", v))
        elif opcode in {"imul", "dmul"}:
            b = stack.pop()
            a = stack.pop()
            stack.append((opcode, a, b))
        elif opcode == "getstatic":
            stack.append(("field", field_symbol(tail)))
        elif opcode == "new":
            if "AttributeModifier" not in tail:
                raise UnsupportedBytecode(f"unexpected new at {pc}")
            stack.append({"type": "AttributeModifier", "constructor": None})
        elif opcode == "dup":
            if not stack or not isinstance(stack[-1], dict):
                raise UnsupportedBytecode("dup only supported for pending AttributeModifier")
            stack.append(stack[-1])
        elif opcode == "invokevirtual" and "getRegistryName:" in tail:
            instance = stack.pop()
            if instance != ("field", "INSTANCE"):
                raise ValueError("modifier id did not originate from perk INSTANCE")
            stack.append(("registry_id",))
        elif opcode == "invokespecial" and 'AttributeModifier."<init>":' in tail:
            operation = stack.pop()
            amount = stack.pop()
            modifier_id = stack.pop()
            obj = stack.pop()
            if (not isinstance(obj, dict) or obj["constructor"] is not None
                    or modifier_id != ("registry_id",) or operation[0] != "field"
                    or operation[1] not in OPERATIONS):
                raise ValueError("unexpected AttributeModifier constructor operand origin")
            obj["constructor"] = {"amount": amount, "operation": operation[1]}
        elif opcode == "invokevirtual" and "withModifierAdded:" in tail:
            group = stack.pop()
            obj = stack.pop()
            attribute = stack.pop()
            base = stack.pop()
            if (group != ("slot_group",) or not isinstance(obj, dict)
                    or obj["constructor"] is None
                    or attribute[0] != "field" or attribute[1] not in ATTRS
                    or base[0] not in {"receiver", "modifiers"}):
                raise ValueError("unexpected withModifierAdded operand origin")
            item = {"attribute": attribute[1],
                    "amount_expr": obj["constructor"]["amount"],
                    "operation": obj["constructor"]["operation"]}
            changes.append(item)
            stack.append(("modifiers", len(changes)))
        elif opcode == "areturn" and index == len(ops) - 1:
            result = stack.pop()
            if stack or result != ("modifiers", len(changes)):
                raise ValueError("unexpected perk return value or stack residue")
        else:
            raise UnsupportedBytecode(f"unsupported opcode or control flow {opcode} at {pc}")
    if result is None:
        raise ValueError("no terminal areturn")
    return changes


EXPECTED = {
    "soul_ward": [
        {"attribute": "SOUL_WARD_CAPACITY", "amount_expr": ("as_double", ("imul", ("int", 2), ("slotValue",))), "operation": "ADD_VALUE"},
        {"attribute": "SOUL_WARD_INTEGRITY", "amount_expr": ("dmul", ("double", 0.5), ("as_double", ("slotValue",))), "operation": "ADD_MULTIPLIED_BASE"},
    ],
    "magic_proficiency": [
        {"attribute": "MAGIC_PROFICIENCY", "amount_expr": ("dmul", ("double", 0.1), ("as_double", ("slotValue",))), "operation": "ADD_MULTIPLIED_BASE"},
    ],
    "spirit_spoils": [
        {"attribute": "SPIRIT_SPOILS", "amount_expr": ("as_double", ("slotValue",)), "operation": "ADD_VALUE"},
    ],
}


def audit_perk_disassemblies(dis: dict[str, str]) -> dict:
    if set(dis) != set(EXPECTED):
        raise ValueError("missing or unexpected perk class")
    observed = {}
    for name, expected in EXPECTED.items():
        compiled = symbolic_perk_method(method_block(dis[name], "applyAttributeModifiers"))
        if compiled != expected:
            raise ValueError(f"{name}: expected modifier dataflow differs: {compiled!r}")
        observed[name] = {"modifiers": [{"attribute": x["attribute"],
                                        "operation": x["operation"],
                                        "source_expression": str(x["amount_expr"])}
                                       for x in compiled],
                          "bounded_symbolic_dataflow": True}
    return {
        "status": "PASS_BOUNDED_PERK_DATAFLOW",
        "scope": "EXACT_METHOD_STACK_FLOW_FOR_THREE_PERK_CLASSES_ONLY",
        "perks": observed,
        "limitations": [
            "The whitelist rejects unsupported bytecode rather than inferring behavior.",
            "The symbolic stack is bounded to modifier construction and direct return, not a full JVM/CFG verifier.",
            "No equipment state or AttributeInstance was read in a loaded Minecraft server.",
            "No Minecraft damage, Malum Soul Ward/spirit output, or RPG progression was observed.",
        ],
    }


def test_method(lines: list[str]) -> str:
    return ("public class Dummy {\n"
            "  public ItemAttributeModifiers applyAttributeModifiers();\n"
            "    descriptor: ()LItemAttributeModifiers;\n"
            "    Code:\n" + "\n".join(
                f"      {i*4}: {line}" for i, line in enumerate(lines)) + "\n}")


SIMPLE = [
    "aload_1",
    "getstatic #1 // Field com/foo/Attributes.MAGIC_PROFICIENCY:LAttribute;",
    "new #2 // class net/minecraft/world/entity/ai/attributes/AttributeModifier",
    "dup",
    "getstatic #3 // Field INSTANCE:LPerk;",
    "invokevirtual #4 // Method getRegistryName:()LResourceLocation;",
    "ldc2_w #5 // double 0.1d",
    "iload_3",
    "i2d",
    "dmul",
    "getstatic #6 // Field net/minecraft/world/entity/ai/attributes/AttributeModifier$Operation.ADD_MULTIPLIED_BASE:LOperation;",
    "invokespecial #7 // Method net/minecraft/world/entity/ai/attributes/AttributeModifier.\"<init>\":(LResourceLocation;DLOperation;)V",
    "aload 4",
    "invokevirtual #8 // Method net/minecraft/world/item/component/ItemAttributeModifiers.withModifierAdded:(LAttribute;LAttributeModifier;LEquipmentSlotGroup;)LItemAttributeModifiers;",
    "areturn",
]


class Tests(unittest.TestCase):
    def test_pass_valid_modifier_stack(self):
        r = symbolic_perk_method(test_method(SIMPLE))
        self.assertEqual(r, EXPECTED["magic_proficiency"])

    def test_fail_numeric_drift(self):
        s = [x.replace("double 0.1d", "double 0.2d") for x in SIMPLE]
        self.assertNotEqual(symbolic_perk_method(test_method(s)), EXPECTED["magic_proficiency"])

    def test_fail_attribute_swap(self):
        s = [x.replace("MAGIC_PROFICIENCY", "SPIRIT_SPOILS") for x in SIMPLE]
        self.assertNotEqual(symbolic_perk_method(test_method(s)), EXPECTED["magic_proficiency"])

    def test_fail_operation_swap(self):
        s = [x.replace("ADD_MULTIPLIED_BASE", "ADD_VALUE") for x in SIMPLE]
        self.assertNotEqual(symbolic_perk_method(test_method(s)), EXPECTED["magic_proficiency"])

    def test_fail_slot_origin(self):
        s = [x.replace("iload_3", "iload_2") for x in SIMPLE]
        with self.assertRaises(UnsupportedBytecode):
            symbolic_perk_method(test_method(s))

    def test_fail_missing_conversion(self):
        s = [x for x in SIMPLE if x != "i2d"]
        self.assertNotEqual(symbolic_perk_method(test_method(s)), EXPECTED["magic_proficiency"])

    def test_fail_unexpected_branch(self):
        s = SIMPLE[:-1] + ["goto 100", "areturn"]
        with self.assertRaises(UnsupportedBytecode):
            symbolic_perk_method(test_method(s))

    def test_fail_wrong_constructor_origin(self):
        s = [x.replace("getRegistryName:", "differentName:") for x in SIMPLE]
        with self.assertRaises(UnsupportedBytecode):
            symbolic_perk_method(test_method(s))

    def test_fail_wrong_equipment_slot(self):
        s = [x.replace("aload 4", "aload_1") for x in SIMPLE]
        with self.assertRaises(ValueError):
            symbolic_perk_method(test_method(s))

    def test_fail_trailing_extra_instruction(self):
        s = SIMPLE + ["nop"]
        with self.assertRaises(UnsupportedBytecode):
            symbolic_perk_method(test_method(s))

    def test_fail_no_areturn(self):
        with self.assertRaises(ValueError):
            symbolic_perk_method(test_method(SIMPLE[:-1]))

    def test_fail_missing_class(self):
        with self.assertRaises(ValueError):
            audit_perk_disassemblies({"magic_proficiency": test_method(SIMPLE)})


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
        root = inspect_jar(args.jar)
        dis = {key: javap(args.jar, CLASSES[key]) for key in EXPECTED}
        report = audit_perk_disassemblies(dis)
        report["publisher_sha1"] = root["publisher_sha1"]
        report["publisher_sha256"] = root["publisher_sha256"]
        report["publisher_bytes"] = root["publisher_bytes"]
    except (OSError, ValueError) as exc:
        report = {"status": "FAIL_CLOSED", "evidence_class": "NO_BOUNDED_PERK_FLOW_PROOF",
                  "deviations": [str(exc)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "deviations": report.get("deviations", [])}))
    return 0 if report["status"] == "PASS_BOUNDED_PERK_DATAFLOW" else 2


if __name__ == "__main__":
    sys.exit(main())
