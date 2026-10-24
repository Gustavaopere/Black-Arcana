#!/usr/bin/env python3
"""SHA-exact, clean-room cross-class direct JVM callsites for nine Wind 1.0.5 getters.

Only explicit invoke* Method/InterfaceMethod constant-pool comments count.
No negative claim about reflective, inherited, host, indirect, or invokedynamic use.
Exports symbolic callsites, never copied instructions, provider JAR, or sources.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import zipfile
from pathlib import Path

import winds_105_spell_metadata as binary
import winds_105_getter_consumer_edges as edges

ROOT = "net/raptorzizi/wind_spellbooks/"
HEADER = re.compile(r"^  (?:.+\([^)]*\)(?: throws .+)?;|static \{\};)$")
INVOKE = re.compile(
    r"^\s*\d+:\s+(invokevirtual|invokespecial|invokestatic|invokeinterface)\b"
    r".*?\s+//\s+(?:InterfaceMethod|Method)\s+(\S+)"
)
GETTER_SIGNATURES = {
    f"{binary.BASE.replace('.', '/')}{binary.ROSTER[spell]}.{getter}:{descriptor}":
    (spell, getter)
    for spell, methods in edges.GETTERS.items()
    for getter, descriptor in methods.items()
}
# Exactly nine getters in six of the seven registered spells.
assert len(GETTER_SIGNATURES) == 9

class AuditError(ValueError):
    pass

def class_names(jar: Path) -> list[str]:
    with zipfile.ZipFile(jar) as z:
        classes = sorted(
            p[:-6].replace("/", ".")
            for p in z.namelist()
            if p.startswith(ROOT) and p.endswith(".class")
            and not p.endswith(("module-info.class", "package-info.class"))
        )
    if len(classes) != len(set(classes)) or not 7 <= len(classes) <= 1200:
        raise AuditError("unbounded or duplicated provider class universe")
    required = set(binary.BASE + name for name in binary.ROSTER.values())
    if not required.issubset(classes):
        raise AuditError("missing one of the seven registered spell classes")
    return classes

def inspect_class(class_name: str, javap: str) -> list[dict]:
    """Resolve class-qualified and own-class shorthand calls conservatively."""
    actual_owner = class_name.replace(".", "/")
    current_method = None
    in_code = False
    results = []
    # Input is an isolated javap response per .class, never concatenated across classes.
    for line in javap.splitlines():
        if HEADER.match(line):
            current_method = line.strip()
            in_code = False
            continue
        if line.strip() == "Code:":
            if current_method is None:
                raise AuditError(f"bytecode has no method header: {class_name}")
            in_code = True
            continue
        if not in_code:
            continue
        match = INVOKE.match(line)
        if match is None:
            continue
        opcode, ref = match.groups()
        # A short 'getRange:(...)F' ref is only attributable to current owner.
        if ref.startswith(("get", "is")) and "." not in ref.split(":", 1)[0]:
            qualified = actual_owner + "." + ref
            attribution = "JAVAP_OWN_CLASS_SHORTHAND"
        else:
            qualified = ref
            attribution = "JAVAP_EXPLICIT_CLASS_OWNER"
        target = GETTER_SIGNATURES.get(qualified)
        if target is None:
            continue
        if not current_method:
            raise AuditError("caller method not identified")
        results.append({
            "caller_class": class_name,
            "caller_declaration": current_method,
            "invoke_opcode": opcode,
            "callee_spell": target[0],
            "callee_getter": target[1],
            "callee_jvm_ref": qualified,
            "owner_attribution": attribution,
            "evidence": "DIRECT_COMPILED_INVOKE_ONLY",
        })
    return results

def summarize(disassemblies: dict[str, str], universe: list[str]) -> dict:
    if universe != sorted(set(universe)) or set(disassemblies) != set(universe):
        raise AuditError("incomplete provider class set")
    raw = [edge for clazz in universe for edge in inspect_class(clazz, disassemblies[clazz])]
    # Every one of the nine selected getters has a known direct caller from PR #884.
    observed = {(row["callee_spell"], row["callee_getter"]) for row in raw}
    expected = {(spell, getter) for spell, methods in edges.GETTERS.items() for getter in methods}
    if observed != expected:
        raise AuditError("nine-getter reference population drift")
    # Re-confirm all approved same-class callsites without assuming global completeness.
    for spell, getters in edges.EXPECTED_CALLERS.items():
        class_name = binary.BASE + binary.ROSTER[spell]
        for getter, required_names in getters.items():
            method_names = [
                row["caller_declaration"].split("(", 1)[0].rsplit(" ", 1)[-1]
                for row in raw
                if row["caller_class"] == class_name and row["callee_spell"] == spell
                and row["callee_getter"] == getter
            ]
            if sorted(method_names) != sorted(required_names):
                raise AuditError(f"prior SHA-exact spell caller drift: {spell}.{getter}")
    raw.sort(key=lambda x:(x["callee_spell"],x["callee_getter"],x["caller_class"],
                           x["caller_declaration"],x["invoke_opcode"]))
    per_getter = {}
    for spell, methods in edges.GETTERS.items():
        per_getter[spell] = {}
        for getter in methods:
            matches = [row for row in raw
                       if row["callee_spell"] == spell and row["callee_getter"] == getter]
            owner = binary.BASE + binary.ROSTER[spell]
            per_getter[spell][getter] = {
                "direct_calls": matches,
                "calls_outside_declaring_spell_class": sum(
                    row["caller_class"] != owner for row in matches
                ),
                "runtime_getter_to_sink_flow": "NOT_PROVEN",
            }
    return {
        "result": "PASS_SHA_EXACT_CROSS_CLASS_DIRECT_CALL_INVENTORY",
        "sha1": binary.EXPECTED_SHA1,
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "classes_inspected": len(universe),
        "getters_scoped": 9,
        "explicit_invokes_found": len(raw),
        "out_of_declaring_spell_invokes": sum(
            row["caller_class"] != binary.BASE + binary.ROSTER[row["callee_spell"]]
            for row in raw
        ),
        "selected_getters": per_getter,
        "limits": [
            "all .class members under provider namespace in the exact JAR, not dependency jars",
            "javap explicit invoke symbols only; NOT a proof of no host/inherited/indirect calls",
            "no invokedynamic, reflection, method handles, events or virtual dispatch resolution",
            "callsite does not prove that returned value feeds a particular entity setter",
            "no client/Survival QA and no approved mutating perk or provider adapter",
        ],
    }

def audit(jar: Path) -> dict:
    # Previous validator verifies physical file shape, SHA-1, seven classes and integrity.
    binary.audit(jar)
    classes = class_names(jar)
    results = {}
    for class_name in classes:
        try:
            run = subprocess.run(
                ["javap","-c","-p","-classpath",str(jar),class_name],
                capture_output=True,text=True,check=True,timeout=25,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
            raise AuditError("failed to inspect provider class: " + class_name) from exc
        results[class_name] = run.stdout
    return summarize(results, classes)

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=audit(args.jar)
        code=0
    except (AuditError,binary.AuditError,OSError,ValueError,zipfile.BadZipFile) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    payload=json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
