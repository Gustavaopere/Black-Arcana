#!/usr/bin/env python3
"""Bounded, fail-closed cross-provider entity ABI and lifecycle reference audit.

Only public JVM method names/descriptors and aggregate counters leave the
process. No third-party bytecode, method bodies, call order or assets are saved.
Static calls are NOT evidence of runtime activation, target caps or safe hooks.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

SPECS = (
    ("alshanex_familiars", "1.21.1_v4.0.3",
     "e5051c2385a426d05bf203ba8081a23d891f6686",
     "net.alshanex.alshanex_familiars.entity.misc.MegidoEntity"),
    ("irons_spellbooks", "1.21.1-3.16.3",
     "017fd8140c477f9ae602cf95594f1c23bef1d6e3",
     "io.redspace.ironsspellbooks.entity.spells.ball_lightning.BallLightning"),
)
HEADER = re.compile(r"^\s{2}(.+)\(([^;]*)\);\s*$")
DESC = re.compile(r"^\s*descriptor:\s*(\([^)]*\)[^\s]+)\s*$")
INSTR = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b(.*)$")
CALL = re.compile(r"//\s+(?:Method|InterfaceMethod)\s+([^:\s]+):(\([^)]*\)[^\s]+)")
RISK_WORDS = (
    "tick", "target", "hurt", "damage", "hit", "attack", "remove",
    "discard", "kill", "explode", "entity", "spawn", "pos", "radius",
    "range", "chain", "connection", "nearest", "collision", "nearby",
    "filter", "level", "server",
)


def _risk(name: str) -> bool:
    return any(word in name.lower() for word in RISK_WORDS)


def parse_class(stdout: str, fqcn: str) -> dict:
    methods: dict[tuple[str, str], list[tuple[str, str]]] = {}
    current = None
    descriptor = None
    in_code = False
    seen_names = set()

    def commit_header():
        nonlocal current, descriptor, in_code
        current = None
        descriptor = None
        in_code = False

    for line in stdout.splitlines():
        hdr = HEADER.fullmatch(line)
        if hdr:
            prefix = hdr.group(1).strip()
            name = prefix.split()[-1].split(".")[-1]
            if re.fullmatch(r"[A-Za-z_$][\w$]*", name):
                commit_header()
                current = name
            continue
        if line.strip() == "}":
            commit_header()
            continue
        if current is None:
            continue
        m = DESC.fullmatch(line)
        if m:
            descriptor = m.group(1)
            continue
        if line.strip() == "Code:":
            if descriptor is None:
                raise ValueError("code without descriptor for " + current)
            key = current, descriptor
            if key in methods:
                raise ValueError("duplicate method body " + current)
            methods[key] = []
            seen_names.add(current)
            in_code = True
            continue
        if in_code:
            match = INSTR.fullmatch(line)
            if match:
                methods[(current, descriptor)].append(
                    (match.group(1), match.group(2).strip())
                )

    if not methods or len(methods) > 150:
        raise ValueError("missing/oversize entity ABI " + fqcn)
    output = []
    risk_total = collections.Counter()
    for (method, desc), ops in sorted(methods.items()):
        if not ops or len(ops) > 14000:
            raise ValueError("missing/oversize method body " + method)
        grouped_calls = collections.Counter()
        interesting = collections.Counter()
        unresolved = 0
        for opcode, operand in ops:
            if not opcode.startswith("invoke"):
                continue
            ref = CALL.search(operand)
            if not ref:
                unresolved += 1
                continue
            symbol, call_desc = ref.groups()
            if "." in symbol:
                owner, target = symbol.rsplit(".", 1)
            else:
                owner, target = "UNQUALIFIED_OWNER", symbol
            target = target.strip('"')
            if len(owner) > 220 or len(target) > 110:
                raise ValueError("unbounded symbol")
            prefix = ("alshanex" if "alshanex" in owner else
                      "irons" if "ironsspellbooks" in owner else
                      "minecraft" if owner.startswith("net/minecraft/") else
                      "java" if owner.startswith("java/") else "other_or_unqualified")
            grouped_calls[prefix] += 1
            if _risk(target):
                interesting[(owner, target, call_desc)] += 1
                risk_total[target] += 1
        if len(interesting) > 110:
            raise ValueError("unbounded risk call sites")
        output.append({
            "declared_method": method,
            "descriptor": desc,
            "instruction_count": len(ops),
            "branch_op_count": sum(op.startswith("if") or op in (
                "goto", "goto_w", "lookupswitch", "tableswitch") for op, _ in ops),
            "allocation_op_count": sum(op in ("new", "anewarray",
                "newarray", "multianewarray") for op, _ in ops),
            "field_read_op_count": sum(op in ("getfield", "getstatic") for op, _ in ops),
            "direct_invocations_by_owner": dict(sorted(grouped_calls.items())),
            "unresolved_invoke_count": unresolved,
            "risk_related_direct_references": [
                {"symbol_owner": owner, "symbol_method": target,
                 "descriptor": sig, "call_sites": n}
                for (owner, target, sig), n in sorted(interesting.items())
            ],
        })
    if len(risk_total) > 150:
        raise ValueError("unbounded symbol inventory")
    return {
        "class_name": fqcn,
        "declared_method_bodies": len(output),
        "method_names_with_code": sorted(seen_names),
        "risk_symbol_name_counts": dict(sorted(risk_total.items())),
        "methods": output,
        "runtime_target_count": "NOT_VERIFIED",
        "damage_hit_count": "NOT_VERIFIED",
        "runtime_spawn_count": "NOT_VERIFIED",
        "execution_budget": "NOT_VERIFIED",
        "mutating_hook": "NOT_VERIFIED",
    }


def verify_and_inspect(path: Path, spec: tuple[str, str, str, str]):
    modid, version, expected_sha, fqcn = spec
    sha = hashlib.sha1()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1 << 20), b""):
            sha.update(part)
    if sha.hexdigest() != expected_sha:
        raise ValueError("SHA-1 mismatch before archive inspection: " + modid)
    with zipfile.ZipFile(path) as archive:
        resource = fqcn.replace(".", "/") + ".class"
        if archive.namelist().count(resource) != 1:
            raise ValueError("class identity mismatch: " + resource)
    proc = subprocess.run(
        ["javap", "-classpath", str(path), "-p", "-s", "-c", fqcn],
        capture_output=True, text=True, check=False, timeout=40
    )
    if proc.returncode:
        raise ValueError("javap exact class failure: " + modid)
    result = parse_class(proc.stdout, fqcn)
    result.update({"modid": modid, "version": version, "sha1": expected_sha})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alshanex", type=Path, required=True)
    parser.add_argument("--irons", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    providers = [
        verify_and_inspect(args.alshanex, SPECS[0]),
        verify_and_inspect(args.irons, SPECS[1]),
    ]
    report = {
        "schema_version": 1,
        "scope": "EXACT_TWO_PROVIDER_ENTITY_ABI_METADATA_ONLY",
        "third_party_code_or_assets_copied": False,
        "modpack_physical_qa": "NOT_TESTED",
        "cross_provider_mutation_hook": "NOT_VERIFIED",
        "providers": providers,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for p in providers:
        print("PASS", p["modid"], p["sha1"], "class", p["class_name"],
              "method bodies", p["declared_method_bodies"])
        print("METHOD_NAMES", p["modid"], ",".join(p["method_names_with_code"]))
        print("RISK_SYMBOL_COUNTS", p["modid"],
              json.dumps(p["risk_symbol_name_counts"], sort_keys=True))
    print("No disassembly, code, recipe bodies or third-party assets retained.")


if __name__ == "__main__":
    main()
