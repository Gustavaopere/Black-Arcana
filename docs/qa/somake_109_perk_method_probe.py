#!/usr/bin/env python3
"""Exact SHA-gated Somake 1.0.9 allowCrafting method references (clean-room)."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

MOD_ID = "somakespells"
VERSION = "1.0.9"
SHA1 = "171841ac9f802be9309ecc166c1d972ac6d404c0"
FILENAME = "somakespells-1.0.9-1.21.1.jar"
TARGETS = {
    "fragmented_requiem": "CONSTANT_FALSE",
    "rose_secret": "CONSTANT_FALSE",
    "comforting_lullaby": "CONSTANT_FALSE",
    "funeral_bloom": "NON_CONSTANT",
    "withered_rose_vortex": "NON_CONSTANT",
    "custodia_caeli": "NON_CONSTANT",
    "jingle_bell": "NON_CONSTANT",
}
INSTRUCTION = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)(?:\s+[^/\n]+)?(?:\s+//\s*(.*))?$")
DECL = re.compile(r"^  public boolean allowCrafting\(\);$")
BOUND = re.compile(r"^  (?:public|private|protected|static|final)\b")
TOKEN = re.compile(r"^[a-z][a-z0-9_]*$")
class GateError(Exception):
    pass

def key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())

def method_ops(disassembly: str) -> list[tuple[str, str]]:
    lines = disassembly.splitlines()
    starts = [i for i,line in enumerate(lines) if DECL.match(line)]
    if len(starts) != 1:
        raise GateError(f"allowCrafting declaration count {len(starts)}")
    start = starts[0]
    end = next((i for i in range(start+1, len(lines)) if BOUND.match(lines[i])), len(lines))
    body = lines[start+1:end]
    desc = [line.strip() for line in body if line.strip().startswith("descriptor:")]
    if desc and desc != ["descriptor: ()Z"]:
        raise GateError("unexpected JVM descriptor")
    ops = []
    for line in body:
        match = INSTRUCTION.match(line)
        if match:
            ops.append((match.group(1), (match.group(2) or "").strip()))
    if not ops or ops[-1][0] not in {"ireturn","athrow"}:
        raise GateError("no verified terminal bytecode path")
    return ops

def analyze(ops: list[tuple[str,str]]) -> dict:
    names = []
    for opcode, comment in ops:
        if opcode.startswith("invoke") or opcode in ("getfield","getstatic"):
            # Only symbolic member references; never retain implementation instructions.
            name = comment.replace("InterfaceMethod ", "").replace("Method ", "").replace("Field ", "")
            if name and name not in names:
                names.append(name[:220])
    if len(names) > 24:
        raise GateError("unbounded symbol count")
    false_only = [x[0] for x in ops] == ["iconst_0", "ireturn"]
    branch_count = sum(x[0].startswith(("if", "goto", "tableswitch", "lookupswitch")) for x in ops)
    return {
        "classification": "CONSTANT_FALSE" if false_only else "NON_CONSTANT",
        "instruction_count": len(ops),
        "branch_instructions": branch_count,
        "called_or_read_members": names,
        "has_explicit_calls": any(op.startswith("invoke") for op,_ in ops),
    }

def inspect(jar: Path, *, expected_sha1: str = SHA1) -> dict:
    if not jar.is_file() or jar.is_symlink() or jar.name != FILENAME:
        raise GateError("wrong physical artifact filename/type")
    if not 100 < jar.stat().st_size < 20_000_000:
        raise GateError("invalid artifact byte length")
    data = jar.read_bytes()
    digest = hashlib.sha1(data).hexdigest()
    if digest != expected_sha1:
        raise GateError(f"physical SHA mismatch: {digest}")
    with zipfile.ZipFile(jar) as zf:
        names = zf.namelist()
        if len(set(names)) != len(names):
            raise GateError("duplicate ZIP member")
        try:
            metadata = zf.read("META-INF/neoforge.mods.toml")
        except KeyError as e:
            raise GateError("NeoForge metadata missing") from e
        if len(metadata) > 250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]", metadata):
            raise GateError("mod metadata ID mismatch")
        targets = {}
        for member in names:
            if not member.startswith("com/somake/somakespells/spells/") or not member.endswith("Spell.class"):
                continue
            normalized = key(member.rsplit("/",1)[-1].removesuffix("Spell.class"))
            match = [id for id in TARGETS if key(id) == normalized]
            if match:
                if len(match) != 1 or match[0] in targets:
                    raise GateError("ambiguous concrete spell class")
                targets[match[0]] = member
        if set(targets) != set(TARGETS):
            raise GateError("concrete class matching failed: missing=" + repr(sorted(set(TARGETS)-set(targets))))
    rows = {}
    for spell_id,member in sorted(targets.items()):
        fqcn = member.removesuffix(".class").replace("/", ".")
        proc = subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),fqcn],
            capture_output=True,text=True,timeout=30,check=False)
        if proc.returncode or len(proc.stdout)>1_000_000:
            raise GateError("bounded javap unavailable for "+spell_id)
        observed = analyze(method_ops(proc.stdout))
        if observed["classification"] != TARGETS[spell_id]:
            raise GateError("classification differs from exact prior audit for "+spell_id)
        rows[spell_id] = {"class":fqcn,"descriptor":"()Z",**observed}
    if hashlib.sha1(jar.read_bytes()).hexdigest() != digest:
        raise GateError("artifact changed during inspection")
    return {
        "status":"PASS_STATIC_METHOD_SYMBOLS_NOT_RUNTIME",
        "evidence":"EXACT_SHA1_ALLOW_CRAFTING_SYMBOLIC_CALLSITE_ONLY",
        "mod_id":MOD_ID,"version":VERSION,"sha1":digest,
        "classes":len(rows),"constant_false":sum(x["classification"]=="CONSTANT_FALSE" for x in rows.values()),
        "nonconstant":sum(x["classification"]=="NON_CONSTANT" for x in rows.values()),
        "results":rows,
        "limits":["No method bodies, decompiled Java, strings, or proprietary assets exported.",
            "No proof of live crafting, effective configs, player eligibility, spell effects, or external hook mutability."]
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    for id,row in result["results"].items():
        print("SOMAKE_CRAFTING_METHOD",id,row["class"],row["classification"],
              "branches",row["branch_instructions"],"members",json.dumps(row["called_or_read_members"]))
    print("SOMAKE_109_EXACT_METHOD_GATE",result["status"],result["classes"],result["sha1"])

if __name__ == "__main__":
    main()
