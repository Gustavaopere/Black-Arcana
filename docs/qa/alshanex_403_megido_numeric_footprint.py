#!/usr/bin/env python3
"""Exact-JAR, clean-room numerical method dependency footprints for Megido.

Never publishes decompiled code, method bodies, bytecode, op sequences or
upstream resources. A structural footprint is not a gameplay formula.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SHA1 = "e5051c2385a426d05bf203ba8081a23d891f6686"
CLASS = "net.alshanex.alshanex_familiars.spells.MegidoSpell"
METHODS = {
    "getDamage": "(ILnet/minecraft/world/entity/LivingEntity;)F",
    "getMaxConnections": "(ILnet/minecraft/world/entity/LivingEntity;)I",
}
HEADER = re.compile(r"^\s{2}(?:(?:public|private|protected)\s+)[^;]*?\b([a-zA-Z_$][\w$]*)\([^;]*\);\s*$")
OPCODE = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b(.*)$")
REF = re.compile(r"//\s+(?:InterfaceMethod|Method)\s+([^:\s]+):(\([^)]*\)[^\s]+)")
FLOAT_ARITH = {"fadd", "fsub", "fmul", "fdiv", "frem", "fneg"}
INT_ARITH = {"iadd", "isub", "imul", "idiv", "irem", "ineg"}
CONVERSIONS = {"f2d", "f2i", "f2l", "d2f", "i2f", "l2f", "i2d", "d2i"}
CONSTANTS = {"ldc", "ldc_w", "bipush", "sipush", "aconst_null"}


def group_owner(owner):
    if owner.startswith(("net/alshanex/", "net.alshanex.")):
        return "provider_alshanex"
    if owner.startswith(("io/redspace/ironsspellbooks/", "io.redspace.ironsspellbooks.")):
        return "irons_spellbooks"
    if owner.startswith(("net/minecraft/", "net.minecraft.")):
        return "minecraft"
    if owner.startswith(("java/", "javax/", "java.", "javax.")):
        return "java"
    if owner == "":
        return "current_class_implicit"
    return "other_external_or_unknown"


def inspect(stdout):
    entries = {}
    method = None
    signature = None
    collecting = False

    for line in stdout.splitlines():
        header = HEADER.fullmatch(line)
        if header:
            method = header.group(1)
            signature = None
            collecting = False
            continue
        if line.strip() == "}":
            method = None
            signature = None
            collecting = False
            continue
        if method not in METHODS:
            continue
        stripped = line.strip()
        if stripped.startswith("descriptor:"):
            signature = stripped.split("descriptor:", 1)[1].strip()
            continue
        if stripped == "Code:":
            if signature != METHODS[method]:
                raise ValueError("method descriptor drift: " + method)
            if method in entries:
                raise ValueError("duplicate method body: " + method)
            entries[method] = []
            collecting = True
            continue
        if collecting:
            m = OPCODE.match(line)
            if m:
                entries[method].append((m.group(1), m.group(2).strip()))

    result = {}
    for method, expected in METHODS.items():
        if method not in entries or not entries[method]:
            raise ValueError("missing exact method body: " + method)
        instructions = entries[method]
        if len(instructions) > 4096:
            raise ValueError("oversized body: " + method)
        calls = {}
        unknown_invokes = 0
        for op, arg in instructions:
            if op.startswith("invoke"):
                match = REF.search(arg)
                if not match:
                    unknown_invokes += 1
                    continue
                symbol, descriptor = match.groups()
                if "." in symbol:
                    owner, target = symbol.rsplit(".", 1)
                else:
                    owner, target = "", symbol
                group = group_owner(owner)
                calls[group] = calls.get(group, 0) + 1
        float_arithmetic = sum(op in FLOAT_ARITH for op, _ in instructions)
        int_arithmetic = sum(op in INT_ARITH for op, _ in instructions)
        conversions = sum(op in CONVERSIONS for op, _ in instructions)
        branches = sum(op.startswith("if") or op in ("goto", "goto_w", "tableswitch", "lookupswitch") for op, _ in instructions)
        field_reads = sum(op in ("getfield", "getstatic") for op, _ in instructions)
        field_writes = sum(op in ("putfield", "putstatic") for op, _ in instructions)
        level_load = sum(op == "iload_1" or (op == "iload" and arg == "1") for op, arg in instructions)
        caster_load = sum(op == "aload_2" or (op == "aload" and arg == "2") for op, arg in instructions)
        constants = sum(op.startswith(("fconst_", "iconst_", "dconst_", "lconst_")) or op in CONSTANTS for op, _ in instructions)
        result[method] = {
            "descriptor": expected,
            "instruction_count": len(instructions),
            "float_arithmetic_op_count": float_arithmetic,
            "int_arithmetic_op_count": int_arithmetic,
            "primitive_conversion_op_count": conversions,
            "branch_op_count": branches,
            "field_read_op_count": field_reads,
            "field_write_op_count": field_writes,
            "numeric_or_null_constant_load_count": constants,
            "level_parameter_local_load_op_count": level_load,
            "caster_parameter_local_load_op_count": caster_load,
            "direct_invocation_owner_group_counts": dict(sorted(calls.items())),
            "unresolved_invocation_ref_count": unknown_invokes,
            "numeric_formula": "NOT_VERIFIED",
            "return_value_semantics": "NOT_VERIFIED",
        }
    return result


def audit(jar: Path):
    digest = hashlib.sha1()
    with jar.open("rb") as fd:
        for chunk in iter(lambda: fd.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != SHA1:
        raise ValueError("JAR SHA-1 mismatch before bytecode inspection")
    proc = subprocess.run(
        ["javap", "-classpath", str(jar), "-p", "-s", "-c", CLASS],
        capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode:
        raise ValueError("javap failed for exact Megido class")
    return {
        "schema_version": 1,
        "provider": "alshanex_familiars",
        "version": "1.21.1_v4.0.3",
        "artifact_sha1": SHA1,
        "scope": "EXACT_MEGIDO_NUMERICAL_METHOD_OP_CATEGORY_COUNTS",
        "third_party_code_copied": False,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "methods": inspect(proc.stdout)
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = audit(a.jar)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for name, detail in report["methods"].items():
        print(name + " " + json.dumps({k: v for k, v in detail.items() if k not in ("descriptor",)}, sort_keys=True))
    print("No third-party method body, bytecode or source copied.")


if __name__ == "__main__":
    main()
