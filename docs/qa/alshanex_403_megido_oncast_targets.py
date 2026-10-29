#!/usr/bin/env python3
"""SHA-pinned symbolic invocation inventory for Megido.onCast (clean-room).

Produces public ABI identifiers and aggregate operation counts, never body
instructions or control-flow order. It cannot certify target count, CPU budget
or a safe mutating hook from this class alone.
"""
import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

SHA1 = "e5051c2385a426d05bf203ba8081a23d891f6686"
CLASS = "net.alshanex.alshanex_familiars.spells.MegidoSpell"
HEADER = re.compile(r"^\s{2}(?:public|private|protected)\s+[^;]*\b([A-Za-z_$][\w$]*)\([^;]*\);\s*$")
INSTR = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b(.*)$")
REF = re.compile(r"//\s+(?:Method|InterfaceMethod)\s+([^:\s]+):(\([^)]*\)\S+)")
GETTERS = {"getRange", "getRadius", "getDamage", "getMaxConnections"}
SIGNATURE_TARGETS = {"getMaxConnections", "getRange", "getRadius", "getDamage", "<init>",
                     "setDamage", "setPos", "addFreshEntity", "getTarget"}


def inventory(javap_text):
    current = None
    descriptor = None
    bodies = {}
    signatures = {}
    for line in javap_text.splitlines():
        m = HEADER.fullmatch(line)
        if m:
            current = m.group(1)
            descriptor = None
            continue
        if line.strip() == "}":
            current = None
            continue
        if current is None:
            continue
        text = line.strip()
        if text.startswith("descriptor:"):
            descriptor = text[len("descriptor:"):].strip()
            signatures.setdefault(current, []).append(descriptor)
        elif text == "Code:" and descriptor is not None:
            if current in bodies:
                raise ValueError("duplicate method body: " + current)
            bodies[current] = []
        elif current in bodies:
            m = INSTR.fullmatch(line)
            if m:
                bodies[current].append((m.group(1), m.group(2).strip()))

    if "onCast" not in bodies or len(signatures.get("onCast", [])) != 1:
        raise ValueError("onCast declaration/code missing or ambiguous")
    for g in GETTERS:
        if g not in bodies or len(signatures.get(g, [])) != 1:
            raise ValueError("missing or duplicate getter: " + g)
    ops = bodies["onCast"]
    if not ops or len(ops) > 6000:
        raise ValueError("invalid/oversized onCast body")

    calls = collections.Counter()
    signatures_used = collections.Counter()
    unresolved = 0
    for op, arg in ops:
        if not op.startswith("invoke"):
            continue
        ref = REF.search(arg)
        if ref is None:
            unresolved += 1
            continue
        fullname, descriptor = ref.groups()
        if "." in fullname:
            owner, name = fullname.rsplit(".", 1)
        else:
            owner, name = "UNQUALIFIED_OWNER", fullname
        if "/" in name or len(name) > 100 or len(owner) > 200:
            raise ValueError("malformed call reference")
        calls[(owner, name)] += 1
        if name.strip('"') in SIGNATURE_TARGETS:
            signatures_used[(owner, name.strip('"'), descriptor)] += 1
    if len(calls) > 100 or unresolved > 200:
        raise ValueError("too many call targets")

    branch = sum(op.startswith("if") or op in ("goto", "goto_w", "tableswitch", "lookupswitch") for op, _ in ops)
    backedge = sum(op in ("goto", "goto_w") for op, _ in ops)
    alloc = sum(op in ("new", "anewarray", "newarray", "multianewarray") for op, _ in ops)
    direct = [{"symbol_owner": o, "symbol_method": m, "count": n}
              for (o, m), n in sorted(calls.items())]
    targeted_signatures = [{"owner": o, "method": m, "jvm_descriptor": d, "count": n}
                  for (o, m, d), n in sorted(signatures_used.items())]
    return {
        "on_cast_abi": signatures["onCast"][0],
        "on_cast_instruction_count": len(ops),
        "on_cast_branch_instruction_count": branch,
        "on_cast_goto_instruction_count": backedge,
        "on_cast_allocation_instruction_count": alloc,
        "unresolved_invoke_count": unresolved,
        "direct_method_references": direct,
        "targeted_jvm_signatures": targeted_signatures,
        "external_target_processing_effect": "NOT_VERIFIED",
        "selected_target_count": "NOT_VERIFIED",
        "execution_bound": "NOT_VERIFIED",
        "mutation_hook": "NOT_VERIFIED",
    }


def audit(jar):
    digest = hashlib.sha1()
    with jar.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    if digest.hexdigest() != SHA1:
        raise ValueError("JAR SHA-1 mismatch: refusing bytecode inspection")
    proc = subprocess.run(["javap", "-classpath", str(jar), "-p", "-s", "-c", CLASS],
                          capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode:
        raise ValueError("javap cannot resolve exact class")
    return {"schema_version": 1, "provider": "alshanex_familiars", "version": "4.0.3",
            "sha1": SHA1, "clean_room": "SYMBOL_REFERENCES_ONLY",
            "physical_qa": "NOT_TESTED", "on_cast": inventory(proc.stdout)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    contract = report["on_cast"]
    print("PASS: exact SHA1-matched JAR inspected; symbolic call metadata only")
    print("count:", contract["on_cast_instruction_count"], "branches:", contract["on_cast_branch_instruction_count"],
          "goto:", contract["on_cast_goto_instruction_count"], "allocations:", contract["on_cast_allocation_instruction_count"])
    for row in contract["direct_method_references"]:
        print("SYMBOL", row["symbol_owner"], row["symbol_method"], row["count"])
    for row in contract["targeted_jvm_signatures"]:
        print("ABI", row["owner"], row["method"], row["jvm_descriptor"], row["count"])
    print("No disassembly, third-party method body, or assets saved")


if __name__ == "__main__":
    main()
