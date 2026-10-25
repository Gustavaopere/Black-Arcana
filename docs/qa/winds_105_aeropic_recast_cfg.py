#!/usr/bin/env python3
"""SHA-gated Aeropic recast control-flow topology, NOT a receiver dataflow proof.

Build normal control-flow edges from exact javap offsets; never serialize
bytecode, offsets or graph. Unsupported control flow and exception handlers
disable dominator conclusions. No mutation or gameplay claims.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from collections import deque
from pathlib import Path

import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as invokes
import winds_105_aeropic_supplier_receiver_slice as parser

METHODS = invokes.EXPECTED_CALLER_METHODS
SOURCE = parser.SPELL_SUPPLIER
RECAST = invokes.RECAST
LIMIT = 10000
TERMINALS = frozenset({"return", "areturn", "ireturn", "lreturn", "dreturn", "freturn", "athrow"})
BRANCH_UNSUPPORTED = frozenset({"tableswitch", "lookupswitch", "jsr", "jsr_w", "ret"})
JUMP = frozenset({"goto", "goto_w"})

class ControlFlowError(ValueError):
    pass

def exception_methods(text: str) -> set[str]:
    """Conservatively flag any selected method with a javap exception table."""
    found: set[str] = set()
    current = None
    for line in text.splitlines():
        if parser.DECL.match(line):
            name = line.strip().split("(", 1)[0].rsplit(" ", 1)[-1]
            current = name if name in METHODS else None
        elif line.startswith("  static {};"):
            current = None
        elif current is not None and line.strip() == "Exception table:":
            found.add(current)
    return found

def reachable(edges: dict[int, set[int]], start: int) -> set[int]:
    seen: set[int] = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        if len(seen) > LIMIT:
            raise ControlFlowError("CFG node budget exceeded")
        queue.extend(edges.get(node, ()))
    return seen

def classify(rows: list[dict], name: str, *, exception_table: bool = False) -> dict:
    if not rows or len(rows) > LIMIT:
        raise ControlFlowError("empty or over-limit method: " + name)
    offsets = [row["offset"] for row in rows]
    if offsets != sorted(set(offsets)):
        raise ControlFlowError("non-monotonic or duplicated instruction offsets")
    at = [i for i, row in enumerate(rows) if row.get("symbol") == RECAST
          and row["opcode"].startswith("invoke")]
    if len(at) != 1 or rows[at[0]]["opcode"] != "invokevirtual":
        raise ControlFlowError("recast site opcode or population drift")
    source_ids = [i for i, row in enumerate(rows)
                  if row["opcode"] == "getstatic" and row.get("symbol") == SOURCE]
    offset_to_id = {offset: i for i, offset in enumerate(offsets)}
    edges: dict[int, set[int]] = {i: set() for i in range(len(rows))}
    failures: set[str] = set()
    branch_count = 0
    for i, row in enumerate(rows):
        op = row["opcode"]
        if op in BRANCH_UNSUPPORTED:
            failures.add("UNSUPPORTED_COMPLEX_CONTROL_FLOW")
            continue
        if op in TERMINALS:
            continue
        if row.get("branch"):
            branch_count += 1
            target = row.get("branch_target")
            if target not in offset_to_id:
                failures.add("UNRESOLVED_OR_INVALID_JUMP_TARGET")
            else:
                edges[i].add(offset_to_id[target])
            if op in JUMP:
                continue
            if not op.startswith("if"):
                failures.add("UNSUPPORTED_BRANCH_OPCODE")
                continue
        if i + 1 < len(rows):
            edges[i].add(i + 1)
        else:
            failures.add("NON_TERMINAL_FALLTHROUGH_AT_METHOD_END")
    if exception_table:
        failures.add("UNMODELED_EXCEPTION_HANDLER_EDGES")
    entry = reachable(edges, 0)
    reverse: dict[int, set[int]] = {i: set() for i in edges}
    for src, targets in edges.items():
        for dst in targets:
            reverse[dst].add(src)
    target = at[0]
    reaches_target = reachable(reverse, target)
    relevant = entry & reaches_target
    preds = {n: reverse[n] & entry for n in entry}
    joins = sum(1 for n in relevant if len(preds[n] & relevant) > 1)
    dominance = set()
    if not failures and target in entry:
        dom = {n: ({n} if n == 0 else set(entry)) for n in entry}
        for _ in range(len(entry)):
            changed = False
            for node in sorted(entry - {0}):
                predset = preds[node]
                intersection = set.intersection(*(dom[p] for p in predset)) if predset else set()
                next_dom = intersection | {node}
                if next_dom != dom[node]:
                    dom[node] = next_dom
                    changed = True
            if not changed:
                break
        else:
            failures.add("DOMINATOR_FIXED_POINT_NOT_CONVERGED")
        if not failures:
            dominance = dom[target]
    return {
        "method": name,
        "instruction_count": len(rows),
        "conditional_and_direct_jump_count": branch_count,
        "normal_entry_reachable_instructions": len(entry),
        "normal_routes_reaching_recast_instructions": len(relevant),
        "normal_route_join_instruction_count": joins,
        "supplier_field_reads_total": len(source_ids),
        "supplier_field_reads_on_some_normal_route": len(set(source_ids) & relevant),
        "supplier_field_reads_dominating_recast": (len(set(source_ids) & dominance)
                                                  if not failures else None),
        "recast_reachable_on_normal_cfg": target in entry if not failures else None,
        "cfg_evidence_grade": ("BOUNDED_NORMAL_CFG_TOPOLOGY_ONLY" if not failures
                               else "FAIL_CLOSED_INCOMPLETE_CFG"),
        "non_proof_reasons": sorted(failures),
        "compiled_receiver_source": "NOT_PROVEN_BY_CFG_TOPOLOGY",
        "return_value_to_PlayerRecasts": "NOT_PROVEN",
        "dynamic_override_executed": "NOT_PROVEN",
        "safe_mutating_hook": "NOT_PROVEN",
    }

def inspect(sha1: str, javap: str) -> dict:
    if sha1 != physical.EXPECTED_SHA1:
        raise ControlFlowError("publisher SHA mismatch")
    selected = parser.methods_from_javap(javap)
    exceptions = exception_methods(javap)
    return {
        "result": "PASS_SHA_EXACT_AEROPIC_NORMAL_CFG_TOPOLOGY_AUDIT",
        "provider": "wind_spellbooks", "release": "1.0.5", "sha1": sha1,
        "call_sites": {name: classify(selected[name], name,
                                      exception_table=name in exceptions) for name in METHODS},
        "scope": "NORMAL_CFG_GEOMETRY_NOT_OPERAND_STACK_PROOF",
        "bytecode_or_offsets_redistributed": False,
        "installed_host_checksum": "NOT_VERIFIED",
        "runtime_receiver_class": "NOT_PROVEN",
        "safe_mutating_hook": "NOT_PROVEN",
        "physical_gameplay": "NOT_TESTED",
    }

def audit(jar: Path) -> dict:
    proof = physical.audit(jar)
    try:
        run = subprocess.run(["javap", "-c", "-p", "-classpath", str(jar), invokes.EFFECT],
                             capture_output=True, text=True, check=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
        raise ControlFlowError("javap inspection failed") from exc
    return inspect(proof["sha1"], run.stdout)

def main() -> int:
    cmd = argparse.ArgumentParser()
    cmd.add_argument("--jar", required=True, type=Path)
    cmd.add_argument("--output", type=Path)
    args = cmd.parse_args()
    try:
        result = audit(args.jar)
        status = 0
    except (ControlFlowError, parser.SliceError, physical.AuditError,
            OSError, ValueError, TypeError, KeyError) as exc:
        result = {"result": "FAIL_CLOSED", "reason": str(exc)}
        status = 1
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf8")
    print(encoded)
    return status

if __name__ == "__main__":
    raise SystemExit(main())
