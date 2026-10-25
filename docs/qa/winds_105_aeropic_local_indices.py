#!/usr/bin/env python3
"""Exact-JAR Aeropic local-index probe. Evidence only, no runtime changes."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path

import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as prior
import winds_105_aeropic_supplier_receiver_slice as parser
import winds_105_aeropic_stack_slice as stack

INSTRUCTION = re.compile(r"^\s*(\d+):\s+([a-z][\w]*)\b(.*)$")
LOCAL_UNSUFFIXED = frozenset(
    prefix + direction
    for prefix in ("a", "i", "f", "d", "l")
    for direction in ("load", "store")
)
OPERAND = re.compile(r"^\s+([0-9]+)(?=\s|$)")
MAX_INDEX = 65535
MAX_ROWS = 10000

class ProbeError(ValueError):
    pass

def normalize(text: str) -> dict[str, dict]:
    """Annotate noncompact javap locals only in a separate symbolic probe.

    aload_4 is a synthetic token representing javap 'aload 4', not a claim
    that the classfile used the JVM compact opcode.
    """
    originals = parser.methods_from_javap(text)
    records = {name: {"rows": [], "unsuffixed": 0, "local_load_store": 0}
               for name in prior.EXPECTED_CALLER_METHODS}
    method = None
    for line in text.splitlines():
        if parser.DECL.match(line):
            name = line.strip().split("(", 1)[0].rsplit(" ", 1)[-1]
            method = name if name in records else None
            continue
        if line.startswith("  static {};"):
            method = None
            continue
        if method is None:
            continue
        match = INSTRUCTION.match(line)
        if match is None:
            continue
        offset, op, raw_operand = match.groups()
        record = records[method]
        index = len(record["rows"])
        if index >= MAX_ROWS or index >= len(originals[method]):
            raise ProbeError("instruction population drift")
        canonical = originals[method][index]
        if canonical["offset"] != int(offset) or canonical["opcode"] != op:
            raise ProbeError("instruction order or opcode drift")
        patched = dict(canonical)
        if op in LOCAL_UNSUFFIXED:
            local = OPERAND.match(raw_operand)
            if local is None:
                raise ProbeError("unparseable explicit JVM local index in " + method)
            numeric = int(local.group(1))
            if numeric > MAX_INDEX:
                raise ProbeError("JVM local index exceeds unsigned u2")
            patched["opcode"] = op + "_" + str(numeric)
            record["unsuffixed"] += 1
        if op in LOCAL_UNSUFFIXED or any(
            re.fullmatch(prefix + r"_(?:0|1|2|3)", op)
            for prefix in LOCAL_UNSUFFIXED
        ):
            record["local_load_store"] += 1
        record["rows"].append(patched)
    for name, record in records.items():
        if len(record["rows"]) != len(originals[name]):
            raise ProbeError("partial or missing method instruction population: " + name)
    return records

def report(sha1: str, text: str) -> dict:
    if sha1 != physical.EXPECTED_SHA1:
        raise ProbeError("official Wind 1.0.5 SHA identity mismatch")
    parsed = normalize(text)
    methods = {}
    for name in prior.EXPECTED_CALLER_METHODS:
        row = parsed[name]
        candidate = stack.classify(row["rows"], name)
        methods[name] = {
            "method": name,
            "unsuffixed_load_store_indices_parsed": row["unsuffixed"],
            "all_load_store_instructions": row["local_load_store"],
            "operand_index_state": "EXACT_EXPLICIT_INDICES_OR_COMPACT_SUFFIX",
            "compiled_receiver_probe": candidate["compiled_receiver_source"],
            "probe_non_proof_reason": candidate["non_proof_reason"],
            "binary_candidate_requires_manual_review": True,
            "dynamic_override_executed": "NOT_PROVEN",
            "return_value_to_PlayerRecasts": "NOT_PROVEN",
            "safe_mutating_hook": "NOT_PROVEN",
        }
    return {
        "result": "PASS_EXACT_JAR_AEROPIC_LOCAL_INDEX_PROBE",
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "sha1": sha1,
        "call_sites": methods,
        "original_negative_contract_unchanged": True,
        "installed_host_checksum": "NOT_VERIFIED",
        "runtime_dispatch": "NOT_PROVEN",
        "physical_gameplay": "NOT_TESTED",
        "safe_mutating_hook": "NOT_PROVEN",
        "published_provider_bytecode": False,
    }

def audit(jar: Path) -> dict:
    identity = physical.audit(jar)
    try:
        proc = subprocess.run(
            ["javap", "-c", "-p", "-classpath", str(jar), prior.EFFECT],
            capture_output=True, text=True, check=True, timeout=30,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ProbeError("frozen Wind AeropicEffect javap failed") from exc
    return report(identity["sha1"], proc.stdout)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    try:
        result = audit(args.jar)
        status = 0
    except (ProbeError, parser.SliceError, stack.SliceError,
            physical.AuditError, ValueError, KeyError, TypeError, OSError) as exc:
        result = {"result": "FAIL_CLOSED", "reason": str(exc)}
        status = 1
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf8")
    print(payload)
    return status

if __name__ == "__main__":
    raise SystemExit(main())
