#!/usr/bin/env python3
"""Exact-JAR clean-room scalar dataflow evidence, with fail-closed JVM handling.

Not a decompiler or runtime emulator: symbolic stack analysis of specifically selected
methods; publishes no bytecode/disassembly or third-party executable contents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

import winds_105_spell_metadata as base

# Deliberate, finite target list; never auto-upgrade a magic catalog from names.
TARGETS = {
    "aeropic": [("getRecastCount", "(int, net.minecraft.world.entity.LivingEntity)", "ireturn")],
    "almighty_push": [("getDuration", "(int)", "ireturn")],
    "tornado": [("getDuration", "(int)", "ireturn")],
    "wind_jump": [("getFloatDuration", "(int, net.minecraft.world.entity.LivingEntity)", "ireturn")],
}
INSTRUCTION = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")
METHOD = re.compile(r"^  (?:public|private|protected) .+\([^;]*\);$")
MATH_MAX = re.compile(r"^Method java/lang/Math\.max:\(II\)I$")
CONSTANT = re.compile(r"^(?:Float|Double|int|long) (-?\d+(?:\.\d+)?)(?:[fdl])?$", re.I)
LOAD = re.compile(r"^([aifdl])load(?:_(\d+))?$")
BINARY = {
    "iadd": "+", "isub": "-", "imul": "*", "idiv": "/", "irem": "%",
    "fadd": "+", "fsub": "-", "fmul": "*", "fdiv": "/",
    "dadd": "+", "dsub": "-", "dmul": "*", "ddiv": "/",
    "ladd": "+", "lsub": "-", "lmul": "*", "ldiv": "/",
}
CAST = {"i2f", "i2d", "i2l", "f2i", "f2d", "d2f", "d2i", "l2i"}
RETURNS = {"ireturn", "freturn", "dreturn", "lreturn"}

class Unsupported(ValueError):
    pass

def _node(kind, **kwargs):
    return {"kind": kind, **kwargs}

def extract_method_instructions(text: str, method_fragment: str) -> list[tuple[int, str, str]]:
    """Select exactly one signature; never mix instructions from other methods."""
    selected = None
    active = False
    for line in text.splitlines():
        if METHOD.match(line) or line.startswith("  static {};"):
            if active:
                break
            active = METHOD.match(line) is not None and method_fragment in line
            if active:
                if selected is not None:
                    raise Unsupported("ambiguous duplicated method declaration")
                selected = []
            continue
        if not active:
            continue
        if line.strip() == "Exception table:":
            raise Unsupported("exception-table control flow")
        instr = INSTRUCTION.match(line)
        if instr:
            selected.append((int(instr.group(1)), instr.group(2), instr.group(3).strip()))
    if selected is None:
        raise Unsupported("exact signature missing")
    if not selected:
        raise Unsupported("no method instructions")
    if any(a[0] >= b[0] for a,b in zip(selected,selected[1:])):
        raise Unsupported("non-increasing bytecode offsets")
    return selected

def analyze(instructions: list[tuple[int,str,str]], expected_return: str) -> dict:
    """Symbolically execute straight-line scalar JVM code; unknown op => no formula."""
    stack = []
    traces = []
    final = None
    for index, op, rest in instructions:
        comment = rest.split("//",1)[1].strip() if "//" in rest else ""
        operand = rest.split("//",1)[0].strip()
        traces.append(op)
        if final is not None:
            raise Unsupported("instructions after return")
        m = LOAD.match(op)
        if m:
            slot = m.group(2) or (operand if operand.isdigit() else None)
            if slot is None:
                raise Unsupported("unresolved local index")
            # Selected methods are instance methods: local 0 is this, 1 is level, 2 is target.
            slot = int(slot)
            if slot not in {0,1,2}:
                raise Unsupported("unknown local slot")
            stack.append(_node("parameter",slot=slot))
        elif re.fullmatch(r"[ifdl]const_[m\d]+",op):
            v=op.split("_",1)[1]
            stack.append(_node("literal",value="-1" if v=="m1" else v))
        elif op in {"bipush","sipush"}:
            if not re.fullmatch(r"-?\d+",operand):
                raise Unsupported("unresolved immediate")
            stack.append(_node("literal",value=operand))
        elif op in {"ldc", "ldc_w", "ldc2_w"}:
            m=CONSTANT.match(comment)
            if m is None:
                raise Unsupported("non-numeric ldc")
            stack.append(_node("literal",value=m.group(1)))
        elif op in CAST:
            if not stack: raise Unsupported("stack underflow")
            stack.append(_node("cast",opcode=op,value=stack.pop()))
        elif op in BINARY:
            if len(stack)<2: raise Unsupported("stack underflow")
            right=stack.pop();left=stack.pop()
            stack.append(_node("binary",opcode=op,operator=BINARY[op],left=left,right=right))
        elif op == "invokestatic" and MATH_MAX.match(comment):
            if len(stack)<2: raise Unsupported("stack underflow")
            second=stack.pop();first=stack.pop()
            stack.append(_node("jdk_math_max_int",left=first,right=second))
        elif op == expected_return:
            if len(stack)!=1:
                raise Unsupported("invalid final stack height")
            final=stack.pop()
        else:
            raise Unsupported("unsupported opcode " + op)
    if final is None:
        raise Unsupported("missing declared scalar return")
    return {"state":"EXACT_STRAIGHT_LINE_EXPRESSION", "expression_ast":final,
            "instruction_count":len(traces),"assumptions":[
                "single straight-line method body with no inferred branches, writes or unknown calls",
                "arg slots refer to JVM locals and not gameplay units",
                "AST is compiled arithmetic provenance, not validated runtime scaling or a perk hook",
            ]}

def audit(jar: Path) -> dict:
    # Verify exact bytes and registered classes before any inspection.
    inventory=base.audit(jar)
    results={}
    for spell_id, rows in TARGETS.items():
        fqcn=base.BASE+base.ROSTER[spell_id]
        try:
            cp=subprocess.run(["javap","-c","-p","-classpath",str(jar),fqcn],
                              capture_output=True,text=True,timeout=20,check=True)
        except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
            raise base.AuditError("javap scalar inspection failed for " + fqcn) from exc
        spell_out={}
        for name,parameters,return_kind in rows:
            token=name+parameters+";"
            try:
                instructions=extract_method_instructions(cp.stdout,token)
                spell_out[name]=analyze(instructions,return_kind)
            except Unsupported as exc:
                spell_out[name]={"state":"UNRESOLVED", "reason":str(exc)}
        results[spell_id]=spell_out
    return {"result":"PASS_INVENTORY_ONLY", "sha1":inventory["sha1"],
            "provider":"wind_spellbooks", "release":"1.0.5",
            "method_count":sum(len(x) for x in results.values()), "methods":results,
            "limits":["method-local AST only; no original code or disassembly included",
                      "unsupported dataflow remains UNRESOLVED, not a formula",
                      "no runtime/Survival, config, mana, cooldown or RPG mutator validation",
                      "no authorization to reproduce or change provider implementation"]}

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    try:
        report=audit(args.jar)
        code=0
    except (base.AuditError,OSError,ValueError) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    data=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    print(data)
    return code

if __name__=="__main__":
    raise SystemExit(main())
