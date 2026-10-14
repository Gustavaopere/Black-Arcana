#!/usr/bin/env python3
"""Read-only, exact-SHA Werewolves 2.0.3.3 Vampirism action registration audit.

Checks compiled static registration callsites only; does not load Minecraft,
claim normal action reachability, or run the modpack.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import zipfile
from pathlib import Path

FILENAME = "Werewolves-1.21-2.0.3.3.jar"
SHA1 = "12a400d50c6e2afdcd96caf73cb80d37877147c8"
MODID = "werewolves"
CLASS = "de.teamlapen.werewolves.core.ModActions"
EVIDENCE = "EXACT_SHA_STATIC_VAMPIRISM_ACTION_CALLS_NOT_REACHABILITY"
EXPECTED = (
    ("human_form", "HUMAN_FORM"),
    ("beast_form", "BEAST_FORM"),
    ("survival_form", "SURVIVAL_FORM"),
    ("howling", "HOWLING"),
    ("rage", "RAGE"),
    ("sense", "SENSE"),
    ("fear", "FEAR"),
    ("leap", "LEAP"),
    ("hide_name", "HIDE_NAME"),
)
# From the source-based semantic ledger: Leap is counted via the skill/input
# route despite hidden selector UI; Hide Name is presentation-only and excluded.
# This classification is NOT proven by javap or any in-game observation.
EXCLUDED_FROM_STRICT_SEMANTIC = ("hide_name",)
INSTRUCTION = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]+)\b")
FIELD = re.compile(r"^\s*public static final [^\n]*DeferredHolder[^\n]*\s+([A-Z][A-Z0-9_]*);$", re.M)
ID = re.compile(r"^[a-z][a-z0-9_]*$")


class AuditError(Exception):
    pass


def parse(disassembly: str) -> tuple[list[tuple[str, str]], list[str]]:
    if disassembly.count("  static {};") != 1:
        raise AuditError("ModActions initializer missing or ambiguous")
    head, body = disassembly.split("  static {};", 1)
    declared = FIELD.findall(head)
    instructions = []
    for line in body.splitlines():
        prefix, _, comment = line.partition("//")
        match = INSTRUCTION.match(prefix)
        if match:
            instructions.append((match.group(1), comment.strip()))
    pairs = []
    for i in range(len(instructions) - 4):
        (pre, pc), (op0, c0), (op1, c1), (op2, c2), (op3, c3) = instructions[i:i+5]
        if not (pre == "getstatic" and "ACTIONS:" in pc
                and op0 in ("ldc", "ldc_w") and c0.startswith("String ")
                and op1 == "invokedynamic"
                and op2 in ("invokevirtual", "invokeinterface")
                and "DeferredRegister.register:" in c2
                and "(Ljava/lang/String;Ljava/util/function/Supplier;)" in c2
                and op3 == "putstatic" and "Field " in c3):
            continue
        spell_id = c0[len("String "):]
        match = re.search(r"\bField (?:[^\s:]+\.)?([A-Z][A-Z0-9_]*):", c3)
        if not match or not ID.fullmatch(spell_id):
            raise AuditError("invalid action ID or field in compiled registration")
        pairs.append((spell_id, match.group(1)))
    return pairs, declared


def reconcile(disassembly: str, expected=EXPECTED) -> dict:
    if len(expected) != len(set(expected)) or any(
        not ID.fullmatch(id) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", field)
        for id, field in expected
    ):
        raise AuditError("invalid independent source-expected pair specification")
    pairs, declared = parse(disassembly)
    listed, actual = set(expected), set(pairs)
    deviation = {
        "missing": sorted(f"{a}:{b}" for a, b in listed - actual),
        "unexpected": sorted(f"{a}:{b}" for a, b in actual - listed),
        "duplicate_callsites": len(pairs) != len(actual),
        "duplicate_fields": len(declared) != len(set(declared)),
        "undeclared_registered_fields": sorted({f for _, f in pairs} - set(declared)),
        "unregistered_declared_fields": sorted(set(declared) - {f for _, f in pairs}),
        "unexpected_callsite_count": len(pairs) != len(expected),
    }
    return {
        "result": "PASS" if not any(deviation.values()) else "UNPROVEN_OR_MISMATCH",
        "registered_expected": len(expected),
        "registered_observed": len(pairs),
        "distinct_observed": len({id for id, _ in pairs}),
        "deviations": {k: value for k, value in deviation.items() if value},
        "excluded_from_semantic_count_source_classification": list(EXCLUDED_FROM_STRICT_SEMANTIC),
        "semantic_reachability_verified_by_binary": False,
    }


def audit(jar: Path, *, expected_sha1=SHA1, expected=EXPECTED, javap="javap") -> dict:
    if jar.is_symlink() or not jar.is_file() or jar.name != FILENAME:
        raise AuditError("JAR missing, symlinked, or filename mismatched")
    before = jar.stat()
    stat_signature = lambda s: (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size < 32*1024*1024:
        raise AuditError("invalid JAR size or type")
    binary = jar.read_bytes()
    if stat_signature(jar.stat()) != stat_signature(before):
        raise AuditError("JAR modified while reading")
    sha1, sha256 = hashlib.sha1(binary).hexdigest(), hashlib.sha256(binary).hexdigest()
    if sha1 != expected_sha1:
        raise AuditError(f"publisher/physical SHA-1 mismatch (observed {sha1})")
    try:
        with zipfile.ZipFile(io.BytesIO(binary)) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or CLASS.replace(".", "/")+".class" not in names:
                raise AuditError("duplicate ZIP entries or ModActions class absent")
            try:
                meta = z.read("META-INF/neoforge.mods.toml")
            except KeyError as ex:
                raise AuditError("NeoForge metadata absent") from ex
            if len(meta) > 256_000 or not re.search(rb'\bmodId\s*=\s*["\x27]werewolves["\x27]', meta):
                raise AuditError("NeoForge mod ID mismatch")
    except (zipfile.BadZipFile, RuntimeError) as ex:
        raise AuditError("invalid JAR ZIP") from ex
    try:
        p = subprocess.run([javap, "-c", "-p", "-classpath", str(jar.resolve()), CLASS],
                           capture_output=True, text=True, check=False, timeout=35)
    except (OSError, subprocess.TimeoutExpired) as ex:
        raise AuditError("javap unavailable/timeout") from ex
    if p.returncode or len(p.stdout) > 2*1024*1024:
        raise AuditError("javap failed/output too large")
    if stat_signature(jar.stat()) != stat_signature(before) or hashlib.sha256(jar.read_bytes()).hexdigest() != sha256:
        raise AuditError("JAR changed during bytecode inspection")
    report = reconcile(p.stdout, expected)
    return {
        "evidence_class": EVIDENCE,
        "provider": MODID, "version": "2.0.3.3",
        "filename": FILENAME, "size_bytes": len(binary),
        "sha1": sha1, "sha256": sha256,
        "result": report["result"], "registry": report,
        "not_proven": [
            "Vampirism action registry loaded in actual NeoForge modpack",
            "eight normally reachable semantic identities",
            "Werewolf forms, infection, bite, health and transformation time",
            "action grants, cooldowns, server authority, config and Survival",
            "Vampirism progression or RPG Skill Tree adapter",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        doc = audit(args.jar)
        rc = 0 if doc["result"] == "PASS" else 1
    except (AuditError, OSError, UnicodeError) as ex:
        doc = {"evidence_class": "UNVERIFIED", "result": "FAIL_CLOSED", "reason": str(ex)}
        rc = 1
    value = json.dumps(doc, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(value + "\n", encoding="utf-8")
    print(value)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
