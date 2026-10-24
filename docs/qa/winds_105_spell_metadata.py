#!/usr/bin/env python3
"""Clean-room, SHA-exact method/operand *inventory* for Wind's Spellbooks 1.0.5.

Records symbolic consumers and literal candidates, not copied code, runtime outcomes,
perks, numerical formulas, or evidence of config/Survival behavior.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

EXPECTED_SHA1 = "8744886899bc245ae147a44baa2b183689cec7da"
JAR_NAME = "wind_spellbooks-1.0.5.jar"
BASE = "net.raptorzizi.wind_spellbooks.spells.wind."
ROSTER = {
    "wind_jump": "WindJumpSpell",
    "tornado": "TornadoSpell",
    "iron_slash": "IronSlashSpell",
    "aeropic": "AeropicSpell",
    "almighty_push": "AlmightyPushSpell",
    "wind_blade": "WindBladeSpell",
    "tailwind": "TailwindSpell",
}
HEADER = re.compile(r"^  (?:public|protected|private) .+\([^;]*\);$")
OPCODE = re.compile(r"^\s*\d+:\s+([a-z][\w]*)\b(?:[^\n]*?)(?:\s+//\s+(.*))?$")
CALL = re.compile(r"^(?:InterfaceMethod|Method)\s+([^\s]+)")
CONSTANT = re.compile(r"^(?:Float|Double|int|long)\s+(.+)$")

class AuditError(ValueError):
    pass

def summarize_disassembly(disassembly: str) -> dict:
    """Collapse javap text to method-level factual symbols, without raw instructions."""
    sections: dict[str, dict] = {}
    current = None
    for line in disassembly.splitlines():
        if HEADER.match(line):
            current = line.strip()
            if current in sections:
                raise AuditError("ambiguous duplicate method declaration")
            sections[current] = {"invoked_symbols": set(), "literal_operands": set()}
            continue
        if line.startswith("  static {};"):
            current = "<clinit>"
            sections.setdefault(current, {"invoked_symbols": set(), "literal_operands": set()})
            continue
        if not current:
            continue
        match = OPCODE.match(line)
        if not match:
            continue
        op, comment = match.groups()
        comment = (comment or "").strip()
        if op.startswith("invoke"):
            ref = CALL.match(comment)
            if ref:
                sections[current]["invoked_symbols"].add(ref.group(1))
        if op.startswith(("ldc", "iconst_", "fconst_", "dconst_", "lconst_", "bipush", "sipush")):
            literal = CONSTANT.match(comment)
            if literal:
                sections[current]["literal_operands"].add(literal.group(1).rstrip("fdl"))
            elif op.startswith(("iconst_", "fconst_", "dconst_", "lconst_")):
                sections[current]["literal_operands"].add(op.split("_", 1)[1])
            elif op in {"bipush", "sipush"}:
                data = line.split("//", 1)[0]
                value = re.search(r"\b(?:bipush|sipush)\s+(-?\d+)\b", data)
                if value:
                    sections[current]["literal_operands"].add(value.group(1))
    if not sections or not any("(" in k for k in sections):
        raise AuditError("no verifiable method declarations in javap")
    return {name: {key: sorted(vals) for key, vals in item.items()}
            for name, item in sorted(sections.items())}

def audit(jar: Path) -> dict:
    if jar.name != JAR_NAME or not jar.is_file() or jar.is_symlink():
        raise AuditError("wrong or non-regular physical JAR")
    st = jar.stat()
    if not stat.S_ISREG(st.st_mode) or not 250_000 <= st.st_size <= 2_000_000:
        raise AuditError("invalid JAR size or file kind")
    content = jar.read_bytes()
    observed = hashlib.sha1(content).hexdigest()
    if observed != EXPECTED_SHA1:
        raise AuditError("publisher and physical SHA-1 differ")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise AuditError("duplicate ZIP entries")
        if archive.testzip() is not None:
            raise AuditError("corrupt ZIP member")
        for spell in ROSTER.values():
            if (BASE.replace(".", "/") + spell + ".class") not in names:
                raise AuditError("missing registered spell class: " + spell)
    results = {}
    for spell_id, class_name in ROSTER.items():
        fqcn = BASE + class_name
        try:
            javap = subprocess.run(["javap", "-c", "-p", "-classpath", str(jar), fqcn],
                                   capture_output=True, text=True, timeout=20, check=True)
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise AuditError("javap inspection failed for " + fqcn) from exc
        methods = summarize_disassembly(javap.stdout)
        results[spell_id] = {"class": fqcn, "method_count": len(methods), "methods": methods}
    if jar.stat().st_size != st.st_size or hashlib.sha1(jar.read_bytes()).hexdigest() != observed:
        raise AuditError("JAR modified during audit")
    return {
        "result": "PASS", "evidence_class": "SHA1_EXACT_JAVAP_METHOD_AND_LITERAL_INVENTORY_NOT_CAUSAL_PROOF",
        "jar": JAR_NAME, "sha1": observed, "provider": "wind_spellbooks", "class_count": len(results),
        "spells": results,
        "limits": ["method signatures and literal candidates only", "no formula/argument attribution",
                   "no host registry, config, combat, targeting or gameplay validation",
                   "no approved RPG Skill Tree adapter or Black Arcana mutation"],
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.jar)
        status = 0
    except (AuditError, OSError, zipfile.BadZipFile) as exc:
        report = {"result": "FAIL_CLOSED", "reason": str(exc)}
        status = 1
    data = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf8")
    print(data)
    return status

if __name__ == "__main__":
    raise SystemExit(main())
