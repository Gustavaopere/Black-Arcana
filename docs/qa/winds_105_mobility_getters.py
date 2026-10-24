#!/usr/bin/env python3
"""Verify exact Wind's Spellbooks 1.0.5 pure float getters, clean-room.

The previous SHA-pinned JVM scalar analyzer is authoritative for instruction support.
This file only chooses five additional getters and fails closed on any ambiguity.
Expressions are method-local mathematical provenance, never gameplay/hook claims.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import winds_105_getter_formulas as scalar
import winds_105_spell_metadata as metadata

# (method, exact method parameters, JVM return opcode)
SELECTED = {
    "almighty_push": (("getRange", "(int, net.minecraft.world.entity.LivingEntity)", "freturn"),),
    "iron_slash": (("getDistance", "(int, net.minecraft.world.entity.LivingEntity)", "freturn"),),
    "tailwind": (
        ("getPercentAirSpeed", "(int)", "freturn"),
        ("getPercentJump", "(int)", "freturn"),
    ),
    "wind_jump": (("getJumpStrength", "(int, net.minecraft.world.entity.LivingEntity)", "freturn"),),
}

class InspectionError(ValueError):
    pass

def inspect_compiled_methods(disassembly_by_spell: dict[str, str]) -> dict:
    """Require five exact, unambiguous methods to yield a full numeric AST."""
    if set(disassembly_by_spell) != set(SELECTED):
        raise InspectionError("missing or unexpected spell disassembly")
    methods = {}
    for spell_id, roster in SELECTED.items():
        results = {}
        for method_name, parameters, return_op in roster:
            try:
                opcodes = scalar.extract_method_instructions(
                    disassembly_by_spell[spell_id], method_name + parameters + ";"
                )
                row = scalar.analyze(opcodes, return_op)
            except scalar.Unsupported as exc:
                raise InspectionError(
                    f"UNRESOLVED {spell_id}.{method_name}: {exc}"
                ) from exc
            if row["state"] != "EXACT_STRAIGHT_LINE_EXPRESSION":
                raise InspectionError(f"unsupported evidence state for {spell_id}.{method_name}")
            results[method_name] = row
        methods[spell_id] = results
    count = sum(len(steps) for steps in methods.values())
    if count != 5:
        raise InspectionError("wrong five-getter population")
    return methods

def audit(jar: Path) -> dict:
    # The previous exact SHA-1, regular-file, class roster and ZIP guard run first.
    binary = metadata.audit(jar)
    disassemblies = {}
    for spell_id in SELECTED:
        fqcn = metadata.BASE + metadata.ROSTER[spell_id]
        try:
            result = subprocess.run(
                ["javap", "-c", "-p", "-classpath", str(jar), fqcn],
                capture_output=True, text=True, check=True, timeout=20,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
            raise InspectionError(f"JVM inspection failed for {spell_id}") from exc
        disassemblies[spell_id] = result.stdout
    return {
        "result": "PASS_EXACT_FIVE_METHOD_LOCAL_AST",
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "sha1": binary["sha1"],
        "getter_count": 5,
        "methods": inspect_compiled_methods(disassemblies),
        "limits": [
            "no inferred calls, no control-flow approximation and no code reproduction",
            "JVM method-local expressions only; no units, bounds, config or effective gameplay",
            "no approved RPG Skill Tree perk mutation, no Black Arcana provider adapter",
        ],
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = audit(args.jar)
        exit_code = 0
    except (InspectionError, metadata.AuditError, OSError, ValueError) as exc:
        data = {"result": "FAIL_CLOSED", "reason": str(exc)}
        exit_code = 1
    rendered = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return exit_code

if __name__ == "__main__":
    raise SystemExit(main())
