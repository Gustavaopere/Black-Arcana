#!/usr/bin/env python3
"""Clean-room, SHA-exact Aeropic recast call-adjacent operand provenance.

Only bounded counts and referenced JVM symbol names are emitted. Adjacent
symbols are not stack provenance, actual receiver, return consumer or gameplay.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path
import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as previous

EFFECT = previous.EFFECT
RECAST = previous.RECAST
METHODS = previous.EXPECTED_CALLER_METHODS
METHOD_DECL = re.compile(r"^  (?:public|protected|private) [^\n]*\([^;]*\);$")
INSTRUCTION = re.compile(r"^\s*(\d+):\s+([a-z][a-z_0-9]*)\b(.*)$")
METHOD_REF = re.compile(r"^(?:Method|InterfaceMethod)\s+(\S+)$")
FIELD_REF = re.compile(r"^Field\s+(\S+)$")
CLASS_REF = re.compile(r"^class\s+(\S+)$")
WINDOW_BEFORE = 24
WINDOW_AFTER = 12

class EvidenceError(ValueError):
    pass

def _info(opcode: str, operand_comment: str) -> dict:
    result = {"opcode": opcode}
    if opcode.startswith("invoke") and (m := METHOD_REF.match(operand_comment)):
        result["invoked_symbol"] = m.group(1)
    elif opcode in {"getstatic", "putstatic", "getfield", "putfield"} and (m := FIELD_REF.match(operand_comment)):
        result["field_symbol"] = m.group(1)
    elif opcode in {"new", "checkcast", "instanceof", "anewarray"} and (m := CLASS_REF.match(operand_comment)):
        result["class_symbol"] = m.group(1)
    return result

def parse_methods(text: str) -> dict[str, list[dict]]:
    """Parse javap's method boundaries. Never publish instructions/offsets."""
    methods: dict[str, list[dict]] = {}
    current = None
    last_offset = -1
    for line in text.splitlines():
        if METHOD_DECL.match(line):
            name = line.strip().split("(", 1)[0].rsplit(" ", 1)[-1]
            current = name if name in METHODS else None
            if current:
                if current in methods:
                    raise EvidenceError("duplicate/overloaded selected method " + current)
                methods[current] = []
                last_offset = -1
            continue
        if line.startswith("  static {};"):
            current = None
            continue
        if current is None:
            continue
        if not (m := INSTRUCTION.match(line)):
            continue
        offset, opcode, tail = m.groups()
        pos = int(offset)
        if pos <= last_offset or len(methods[current]) > 10000:
            raise EvidenceError("invalid or unbounded method bytecode " + current)
        last_offset = pos
        comment = tail.split("//", 1)[1].strip() if "//" in tail else ""
        entry = _info(opcode, comment)
        if opcode.startswith("invoke") and entry.get("invoked_symbol") == RECAST:
            entry["recast_site"] = True
        methods[current].append(entry)
    if set(methods) != set(METHODS):
        raise EvidenceError("missing exact method population")
    return methods

def summarize(methods: dict[str, list[dict]]) -> dict:
    if set(methods) != set(METHODS):
        raise EvidenceError("unexpected method population")
    calls = {}
    for method in METHODS:
        opcodes = methods[method]
        indices = [i for i, row in enumerate(opcodes) if row.get("recast_site")]
        if len(indices) != 1:
            raise EvidenceError("expected exactly one AbstractSpell recast call in "+method)
        i = indices[0]
        call = opcodes[i]
        if call["opcode"] != "invokevirtual":
            raise EvidenceError("wrong recast call opcode: "+method)
        before = opcodes[max(0, i-WINDOW_BEFORE):i]
        after = opcodes[i+1:i+1+WINDOW_AFTER]
        related=lambda rows, key: sorted(set(row[key] for row in rows if key in row))
        calls[method] = {
            "invocation_opcode": "invokevirtual",
            "owner_and_descriptor": RECAST,
            "instructions_examined_before": len(before),
            "instructions_examined_after": len(after),
            "immediately_prior_opcode": before[-1]["opcode"] if before else None,
            "immediately_after_opcode": after[0]["opcode"] if after else None,
            "prelude_method_refs": related(before, "invoked_symbol"),
            "prelude_field_refs": related(before, "field_symbol"),
            "prelude_class_refs": related(before, "class_symbol"),
            "following_method_refs": related(after, "invoked_symbol"),
            "following_field_refs": related(after, "field_symbol"),
            "following_class_refs": related(after, "class_symbol"),
            "prelude_branch_opcode_count": sum(1 for x in before if x["opcode"].startswith(("if", "goto", "tableswitch", "lookupswitch"))),
            "receiver_object":"NOT_TRACED",
            "return_value_dataflow":"NOT_TRACED",
            "runtime_override_dispatch":"NOT_PROVEN",
            "scope":"ADJACENT_SYMBOLS_NOT_JVM_STACK_DATAFLOW",
        }
    return calls

def validate_frozen(sha1: str, calls: dict) -> dict:
    if sha1 != physical.EXPECTED_SHA1 or set(calls) != set(METHODS):
        raise EvidenceError("wrong Wind release or callsite population")
    return {"result":"PASS_SHA_EXACT_RECAST_OPERAND_ADJACENCY_ONLY",
            "release":"1.0.5", "provider":"wind_spellbooks", "sha1":sha1,
            "effect_class":EFFECT, "call_sites":calls, "calls_observed":2,
            "bytecode_context_not_published":True,
            "exact_host_3163_published_ABI":"VERIFIED_SEPARATE_PR_891_NOT_RECEIVER_PROOF",
            "installed_host_binary_identity":"NOT_VERIFIED",
            "receiver_concrete_type":"NOT_TRACED",
            "getRecastCount_return_consumer":"NOT_TRACED",
            "safe_mutating_hook":"NOT_PROVEN",
            "physical_gameplay_validation":"NOT_TESTED"}

def audit(jar: Path) -> dict:
    identity=physical.audit(jar)
    try:
        run=subprocess.run(["javap", "-c", "-p", "-classpath", str(jar), EFFECT],
                           capture_output=True, text=True, timeout=30, check=True)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise EvidenceError("javap failed for exact effect class") from exc
    return validate_frozen(identity["sha1"], summarize(parse_methods(run.stdout)))

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--output", type=Path)
    args=p.parse_args()
    try:
        result=audit(args.jar)
        code=0
    except (EvidenceError, physical.AuditError, OSError, ValueError, TypeError, KeyError) as exc:
        result={"result":"FAIL_CLOSED", "reason":str(exc)}
        code=1
    data=json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf8")
    print(data)
    return code

if __name__ == "__main__":
    raise SystemExit(main())
