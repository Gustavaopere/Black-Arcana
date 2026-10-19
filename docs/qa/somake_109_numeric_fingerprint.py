#!/usr/bin/env python3
"""SHA-exact Somake 1.0.9 numeric-operand fingerprints for perk research.

Clean-room output is a bounded inventory of numeric literal occurrences,
arithmetic opcode counts and API callsites. It does NOT reconstruct or export
publisher method bodies, disassembly, source, constant tables or JARs.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_cast_refs import DECL, DESC
from somake_109_funeral_bud_probe import isolate_named_methods

TARGETS = {
    "funeral_bloom_spell": {
        "fqcn": "com.somake.somakespells.spells.blood.FuneralBloomSpell",
        "methods": ("getRadius", "getImpactDamage", "getMaxTargets", "getDuration",
                    "getWaveInterval", "getTelegraphTicks", "getWitherDuration",
                    "getWitherAmplifier"),
    },
    "funeral_bloom_controller": {
        "fqcn": "com.somake.somakespells.entity.FuneralBloomControllerEntity",
        "methods": ("tick", "launchWave", "isValidTarget"),
    },
    "funeral_bloom_bud": {
        "fqcn": "com.somake.somakespells.entity.FuneralBloomBudEntity",
        "methods": ("tick", "impact", "updatePrediction"),
    },
    "funeral_bloom_impact": {
        "fqcn": "com.somake.somakespells.entity.FuneralBloomImpactEntity",
        "methods": ("setScale", "getOpenProgress", "tick"),
    },
}
CODE = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)(?:\s+(.+))?$")
NUMBER = re.compile(r"^(int|float|long|double)\s+([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?[fFdDlL]?)$")
ARITH = re.compile(r"^[idfl](?:add|sub|mul|div|rem|neg)$")
MAX_JAR = 20_000_000
MAX_TOTAL_LITERALS = 450
MAX_METHOD_LITERALS = 110
MAX_UNIQUE_LITERALS = 45
MAX_METHOD_LINES = 3500
MAX_DISASM = 1_000_000
MAX_METHOD_COUNT = 150
CALL_FILTER = ("Mth.clamp:", "Math.", "SchoolType.getPowerFor:",
               "getSpellPower:", "getRadius:", "getImpactDamage:",
               "getDuration:", "getMaxTargets:", "getWaveInterval:",
               "getTelegraphTicks:", "getScale:", "smoothstep:",
               "DamageSources.applyDamage:", "SpellHealEvent")

def decode_numeric(opcode: str, args: str, comment: str) -> tuple[str, str] | None:
    """Return only literals proved numeric by the actual JVM opcode/comment."""
    for p,typ in (("iconst_", "int"), ("fconst_", "float"),
                  ("dconst_", "double"), ("lconst_", "long")):
        if opcode.startswith(p):
            num = opcode[len(p):]
            if num == "m1":
                num = "-1"
            if not re.fullmatch(r"-?\d+", num):
                raise GateError("invalid constant opcode")
            return (typ, num)
    if opcode in ("bipush", "sipush"):
        raw = args.split()[0] if args else ""
        if not re.fullmatch(r"-?\d+", raw):
            raise GateError("noninteger immediate")
        return ("int", raw)
    if opcode in ("ldc", "ldc_w", "ldc2_w"):
        m = NUMBER.fullmatch(comment.strip())
        if not m:
            return None  # strings, class references, dynamic constants not numeric
        return (m.group(1), m.group(2).lower().rstrip("fdl"))
    return None

def immediate_clamp_literals(body: list[str]) -> list[dict]:
    """Only certify the two literal-producing instructions immediately before clamp.

    This is a narrowly scoped operand-position proof, not a complete dataflow
    model; methods with conversions, loads or calculations between producers
    and callsite remain unclassified.
    """
    instructions=[]
    for line in body:
        before, divider, after=line.partition("//")
        match=CODE.match(before)
        if match:
            instructions.append((match.group(1),(match.group(2) or "").strip(),
                                 after.strip() if divider else ""))
    found=[]
    for index,(opcode,_,comment) in enumerate(instructions):
        if opcode!="invokestatic" or index<2:
            continue
        descriptor_match=re.search(r"Mth\.clamp:\((FFF|III|DDD)\)(F|I|D)(?:\s|$)",comment)
        if not descriptor_match:
            continue
        expected={"FFF":"float","III":"int","DDD":"double"}[descriptor_match.group(1)]
        trailing=[decode_numeric(*item) for item in instructions[index-2:index]]
        if any(value is None or value[0]!=expected for value in trailing):
            continue
        found.append({
            "call":"Mth.clamp",
            "descriptor":f"({descriptor_match.group(1)}){descriptor_match.group(2)}",
            "second_argument_literal":trailing[0][1],
            "third_argument_literal":trailing[1][1],
            "argument_type":expected,
            "claim":"Only the direct two operand pushes are proved; no gameplay scaling or mutability inferred."
        })
    if len(found)>12:
        raise GateError("excessive direct clamp callsites")
    return found


STRAIGHT_LINE_GETTERS = {"getMaxTargets", "getDuration", "getWaveInterval", "getWitherDuration", "getTelegraphTicks"}

def prove_straight_line_integer_expression(body: list[str], descriptor: str) -> dict:
    """Prove an integer expression only for branchless, wholly supported JVM opcodes.

    This deliberately cannot derive target/hit/cast runtime behavior. Integer
    operators retain JVM int overflow/division semantics; do not substitute
    real-valued arithmetic or reinterpret an expression as an attribute setter.
    """
    fail=lambda reason: {"status":"NOT_PROVED","reason":reason}
    if descriptor != "(I)I":
        return fail("descriptor_not_integer_getter")
    instructions=[]
    for line in body:
        before,divider,after=line.partition("//")
        m=CODE.match(before)
        if m:
            instructions.append((m.group(1),(m.group(2) or "").strip(),
                                 after.strip() if divider else ""))
    if not 2 <= len(instructions) <= 90:
        return fail("instruction_budget")
    stack=[]
    for i,(op,args,comment) in enumerate(instructions):
        if op.startswith(("if","goto")) or op in ("tableswitch","lookupswitch","athrow"):
            return fail("branch_or_throw")
        literal=decode_numeric(op,args,comment)
        if literal is not None:
            if literal[0]!="int":
                return fail("noninteger_literal")
            stack.append(literal[1])
        elif op.startswith("iload_") and op[6:].isdigit():
            index=int(op[6:])
            if index!=1:
                return fail("non_parameter_int_load")
            stack.append("level")
        elif op=="iload" and args=="1":
            stack.append("level")
        elif op in {"iadd","isub","imul","idiv","irem"}:
            if len(stack)<2:
                return fail("arithmetic_stack_underflow")
            rhs=stack.pop();lhs=stack.pop()
            operator={"iadd":"+","isub":"-","imul":"*","idiv":"idiv","irem":"irem"}[op]
            stack.append(f"jvm_{operator}({lhs},{rhs})" if op in {"idiv","irem"}
                         else f"({lhs}{operator}{rhs})")
        elif op=="ineg":
            if not stack:return fail("neg_stack_underflow")
            stack.append(f"(-{stack.pop()})")
        elif op=="invokestatic":
            if "Mth.clamp:(III)I" in comment:
                name="clamp"
            elif "Math.max:(II)I" in comment:
                name="max"
            elif "Math.min:(II)I" in comment:
                name="min"
            else:
                return fail("unsupported_invocation")
            arity=3 if name=="clamp" else 2
            if len(stack)<arity:
                return fail("invocation_stack_underflow")
            args_expr=stack[-arity:]
            del stack[-arity:]
            stack.append(f"{name}({','.join(args_expr)})")
        elif op=="ireturn":
            if i!=len(instructions)-1 or len(stack)!=1:
                return fail("return_not_single_terminal")
            expression=stack.pop()
            if len(expression)>1200:
                return fail("expression_budget")
            return {"status":"PROVED_STRAIGHT_LINE_JVM_INT_EXPRESSION",
                    "expression":expression,
                    "parameter":"level (int input, not necessarily actual player spell level)",
                    "limits":"Algebraic JVM int dataflow only; not verified live duration, distance, target count, client sync or perk mutability."}
        else:
            return fail("unsupported_opcode_"+op)
        if len(stack)>30:
            return fail("stack_budget")
    return fail("no_integer_return")


def fingerprint(body: list[str]) -> dict:
    if not 0 < len(body) <= MAX_METHOD_LINES:
        raise GateError("method body length outside guard")
    seen = Counter()
    arithmetic = Counter()
    branches = 0
    calls = Counter()
    instructions = 0
    for line in body:
        before, divider, after = line.partition("//")
        match = CODE.match(before)
        if not match:
            continue
        instructions += 1
        opcode = match.group(1)
        args = (match.group(2) or "").strip()
        comment = after.strip() if divider else ""
        number = decode_numeric(opcode,args,comment)
        if number is not None:
            seen[number] += 1
            if sum(seen.values()) > MAX_METHOD_LITERALS or len(seen)>MAX_UNIQUE_LITERALS:
                raise GateError("method exceeds literal budget")
        if ARITH.fullmatch(opcode) or opcode == "iinc":
            arithmetic[opcode] += 1
        if opcode.startswith(("if", "goto")) or opcode in ("tableswitch", "lookupswitch"):
            branches += 1
        if opcode.startswith("invoke"):
            for wanted in CALL_FILTER:
                if wanted in comment:
                    calls[wanted] += 1
                    break
    if not instructions:
        raise GateError("no bytecode decoded")
    return {
        "bytecode_instruction_count":instructions,
        "numeric_literal_occurrences":sum(seen.values()),
        "numeric_literals":[{"type":t,"literal":n,"occurrences":count}
                            for (t,n),count in sorted(seen.items())],
        "arithmetic_opcode_counts":dict(sorted(arithmetic.items())),
        "direct_trailing_clamp_literals":immediate_clamp_literals(body),
        "branch_instruction_count":branches,
        "bounded_callsite_counts":dict(sorted(calls.items())),
        "contract":"Literal inventory is NOT a formula, unit, clamp bound, or runtime setting.",
    }

def parse_selected_javap(text: str, names: tuple[str, ...]) -> dict:
    if not isinstance(text,str) or len(text)>MAX_DISASM:
        raise GateError("missing or oversized disassembly")
    lines = isolate_named_methods(text).splitlines()
    positions = [i for i,l in enumerate(lines) if DECL.match(l)]
    if not 1 <= len(positions) <= MAX_METHOD_COUNT:
        raise GateError("invalid JVM method cohort")
    discovered = {}
    for index,start in enumerate(positions):
        end=positions[index+1] if index+1<len(positions) else len(lines)
        name = lines[start].strip().split("(",1)[0].rsplit(" ",1)[-1]
        if name not in names:
            continue
        descriptors=[m.group(1) for line in lines[start+1:end] if (m:=DESC.match(line))]
        if len(descriptors)!=1 or name in discovered:
            raise GateError("missing/ambiguous method descriptor: "+name)
        descriptor=descriptors[0]
        if not re.fullmatch(r"\([^)]*\)[A-Za-z0-9/\[;$]+",descriptor):
            raise GateError("invalid JVM method descriptor")
        record={"descriptor":descriptor,**fingerprint(lines[start+1:end])}
        if name in STRAIGHT_LINE_GETTERS:
            record["straight_line_integer_expression"]=prove_straight_line_integer_expression(lines[start+1:end],descriptor)
        discovered[name]=record
    if set(discovered)!=set(names):
        raise GateError("missing exact selected methods: "+repr(sorted(set(names)-set(discovered))))
    return {name:discovered[name] for name in names}

def inspect(jar: Path)->dict:
    if jar.is_symlink() or not jar.is_file() or jar.name!=FILENAME:
        raise GateError("invalid physical JAR path")
    if not 100 < jar.stat().st_size < MAX_JAR:
        raise GateError("invalid JAR length")
    digest=hashlib.sha1(jar.read_bytes()).hexdigest()
    if digest!=SHA1:
        raise GateError("JAR SHA-1 does not match installed release")
    with zipfile.ZipFile(jar) as zf:
        members=zf.namelist()
        if len(members)!=len(set(members)):
            raise GateError("duplicate members")
        meta=zf.read("META-INF/neoforge.mods.toml")
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("publisher mod ID mismatch")
        for spec in TARGETS.values():
            if spec["fqcn"].replace(".","/")+".class" not in members:
                raise GateError("expected compiled class missing")
    rows={}
    total=0
    for label,spec in TARGETS.items():
        result=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),spec["fqcn"]],
                              text=True,capture_output=True,timeout=45,check=False)
        if result.returncode or not result.stdout or len(result.stdout)>MAX_DISASM:
            raise GateError("javap failed/oversized on "+label)
        data=parse_selected_javap(result.stdout,spec["methods"])
        total+=sum(x["numeric_literal_occurrences"] for x in data.values())
        if total>MAX_TOTAL_LITERALS:
            raise GateError("cohort literal budget exceeded")
        rows[label]={"fqcn":spec["fqcn"],"methods":data}
        for method,info in data.items():
            print("SOMAKE_NUMERIC_METHOD",label,method,info["descriptor"],
                  "literals",json.dumps(info["numeric_literals"]),
                  "arithmetic",json.dumps(info["arithmetic_opcode_counts"]),
                  "branches",info["branch_instruction_count"],
                  "calls",json.dumps(info["bounded_callsite_counts"]),
                  "direct_clamp",json.dumps(info["direct_trailing_clamp_literals"]),
                  "int_expression",json.dumps(info.get("straight_line_integer_expression")))
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=digest:
        raise GateError("artifact changed during inspection")
    return {
        "status":"PASS_STATIC_NUMERIC_FINGERPRINTS_NOT_FORMULAS",
        "evidence":"SHA_EXACT_SOMAKE_109_FUNERAL_BLOOM_NUMERIC_METHODS",
        "provider_version":"1.0.9",
        "mod_id":"somakespells",
        "sha1":digest,
        "classes":len(rows),
        "methods":sum(len(x["methods"]) for x in rows.values()),
        "numeric_literal_occurrences":total,
        "results":rows,
        "limits":[
            "Numeric constants are bounded per method, but their role, units and runtime truth values are not inferred.",
            "A nearby constant does not prove a clamp boundary; only explicit dataflow and branch validation could.",
            "No third-party implementation code, disassembly, JAR, animation, assets or source is exported.",
            "No per-player mutator, provider-loaded gameplay, PvP, Survival or client test conducted.",
        ]
    }

def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=inspect(a.jar)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("SOMAKE_NUMERIC_GATE",result["status"],result["classes"],result["methods"],result["sha1"])

if __name__=="__main__":
    main()
