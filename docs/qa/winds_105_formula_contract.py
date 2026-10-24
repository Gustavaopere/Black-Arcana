#!/usr/bin/env python3
"""Pinned binary evidence contract: reject silent drift of four approved getter ASTs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SHA1 = "8744886899bc245ae147a44baa2b183689cec7da"

def arg(): return {"kind":"parameter","slot":1}
def lit(x): return {"kind":"literal","value":str(x)}
def op(name, symbol, x, y):
    return {"kind":"binary","opcode":name,"operator":symbol,"left":x,"right":y}

def expected() -> dict:
    return {
        "aeropic":{"getRecastCount":{"kind":"jdk_math_max_int","left":lit(0),
            "right":op("isub","-",arg(),lit(1))}},
        "almighty_push":{"getDuration":op("iadd","+",lit(25),
            op("imul","*",arg(),lit(3)))},
        "tornado":{"getDuration":op("imul","*",lit(15),
            op("iadd","+",lit(5),op("imul","*",arg(),lit(2))))},
        "wind_jump":{"getFloatDuration":op("imul","*",lit(100),arg())},
    }

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    if doc.get("sha1") != SHA1 or doc.get("provider") != "wind_spellbooks":
        raise ContractError("provider artifact identity mismatch")
    if doc.get("result") != "PASS_INVENTORY_ONLY" or doc.get("release") != "1.0.5":
        raise ContractError("artifact not a successful exact-JAR inventory")
    want=expected()
    if doc.get("method_count") != 4 or not isinstance(doc.get("methods"),dict):
        raise ContractError("non-exact four-getter roster")
    if set(doc["methods"]) != set(want):
        raise ContractError("missing or unexpected spell getter")
    for spell, methods in want.items():
        actual=doc["methods"][spell]
        if not isinstance(actual,dict) or set(actual)!=set(methods):
            raise ContractError("missing or unexpected getter of " + spell)
        for name,ast in methods.items():
            row=actual[name]
            if not isinstance(row,dict) or row.get("state")!="EXACT_STRAIGHT_LINE_EXPRESSION":
                raise ContractError("unresolved getter " + spell + "." + name)
            if row.get("expression_ast") != ast:
                raise ContractError("formula AST diverged: " + spell + "." + name)
    return 4

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--json",type=Path,required=True)
    args=ap.parse_args()
    try:
        checked=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ContractError,ValueError,OSError,TypeError) as exc:
        print("FAIL_CLOSED: " + str(exc))
        return 1
    print(f"PASS: {checked}/4 exact getter ASTs match SHA-frozen reference; NO gameplay/perk claims")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
