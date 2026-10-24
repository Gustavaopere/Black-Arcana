#!/usr/bin/env python3
"""Independent SHA-pinned regression gate for five exact Wind 1.0.5 float getter ASTs.

This compares metadata, not game behavior or permission to mutate external spells.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_SHA1 = "8744886899bc245ae147a44baa2b183689cec7da"

def level():
    return {"kind": "parameter", "slot": 1}

def lit(value: str):
    return {"kind": "literal", "value": value}

def cast(opcode: str, value: dict):
    return {"kind": "cast", "opcode": opcode, "value": value}

def operation(opcode: str, operator: str, left: dict, right: dict):
    return {"kind": "binary", "opcode": opcode, "operator": operator, "left": left, "right": right}

def expected() -> dict:
    """Canonical ASTs as published by exact-JAR CI #40126898432."""
    return {
        "almighty_push": {
            "getRange": operation("fadd", "+", lit("3.0"),
                operation("fmul", "*", cast("i2f", level()), lit("0.5"))),
        },
        "iron_slash": {
            "getDistance": operation("fadd", "+", lit("10.0"),
                operation("fmul", "*", cast("i2f", level()), lit("2"))),
        },
        "tailwind": {
            "getPercentAirSpeed": operation("fmul", "*",
                operation("fmul", "*", cast("i2f", level()), lit("0.15")),
                lit("100.0")),
            "getPercentJump": operation("fmul", "*",
                operation("fadd", "+", lit("0.5"),
                    operation("fmul", "*", lit("0.3"),
                        cast("i2f", operation("isub", "-", level(), lit("1"))))),
                lit("100.0")),
        },
        "wind_jump": {
            "getJumpStrength": cast("d2f", operation("dadd", "+", lit("0.2"),
                operation("dmul", "*", cast("i2d", level()), lit("0.05")))),
        },
    }

class ContractError(ValueError):
    pass

def validate(document: dict) -> int:
    if not isinstance(document, dict):
        raise ContractError("not a JSON object")
    if document.get("sha1") != EXPECTED_SHA1 or document.get("provider") != "wind_spellbooks":
        raise ContractError("provider binary identity mismatch")
    if document.get("result") != "PASS_EXACT_FIVE_METHOD_LOCAL_AST" or document.get("release") != "1.0.5":
        raise ContractError("exact-JAR analysis not successful")
    want = expected()
    got = document.get("methods")
    if document.get("getter_count") != 5 or not isinstance(got, dict) or set(got) != set(want):
        raise ContractError("unexpected spell roster or count")
    for spell, entries in want.items():
        found = got[spell]
        if not isinstance(found, dict) or set(found) != set(entries):
            raise ContractError("wrong method roster for " + spell)
        for name, ast in entries.items():
            row = found[name]
            if not isinstance(row, dict) or row.get("state") != "EXACT_STRAIGHT_LINE_EXPRESSION":
                raise ContractError("unresolved method " + spell + "." + name)
            if row.get("expression_ast") != ast:
                raise ContractError("binary AST differs at " + spell + "." + name)
    return 5

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ValueError, OSError, TypeError) as exc:
        print("FAIL_CLOSED: " + str(exc))
        return 1
    print(f"PASS: {result}/5 SHA-pinned JVM getter ASTs, NO runtime or perk approval")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
