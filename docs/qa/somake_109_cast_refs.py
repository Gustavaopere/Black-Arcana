#!/usr/bin/env python3
"""Somake 1.0.9 SHA-exact compiled class method and call-reference discovery.

Clean-room static catalog evidence. Does not execute Minecraft or export
third-party method bodies, classfiles, constants, strings, or assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError

CLASSES = {
    "fragmented_requiem": "com.somake.somakespells.spells.blood.FragmentedRequiemSpell",
    "rose_secret": "com.somake.somakespells.spells.blood.RoseSecretSpell",
    "comforting_lullaby": "com.somake.somakespells.spells.sound.ComfortingLullabySpell",
    "funeral_bloom": "com.somake.somakespells.spells.blood.FuneralBloomSpell",
    "withered_rose_vortex": "com.somake.somakespells.spells.blood.WitheredRoseVortexSpell",
    "custodia_caeli": "com.somake.somakespells.spells.holy.CustodiaCaeliSpell",
    "jingle_bell": "com.somake.somakespells.spells.sound.JingleBellSpell",
}
DECL = re.compile(r"^  (?:public|protected|private) (?!class\s|interface\s).*\([^;]*\);$")
DESC = re.compile(r"^\s*descriptor:\s*(\([^)]*\).+)$")
OP = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b")
SYMBOL = re.compile(r"^(Method|InterfaceMethod|Field)\s+(.+)$")
FOCUS = re.compile(r"^(?:on[A-Z]|get[A-Z]|check[A-Z]|can[A-Z]|is[A-Z]|"
                   r"set[A-Z]|should[A-Z]|lambda\$|cast|tick|summon|apply|"
                   r"hurt|damage|heal|spawn|create|perform)", re.I)

def parse_javap(data: str, simple: str, *, focus_pattern: re.Pattern | None = None) -> dict:
    focus_pattern = focus_pattern or FOCUS
    if not isinstance(data, str) or len(data) > 1_000_000:
        raise GateError("disassembly missing or unbounded")
    lines = data.splitlines()
    positions = [i for i, line in enumerate(lines) if DECL.match(line)]
    if not positions or len(positions) > 150:
        raise GateError("unbounded/absent method declarations")
    seen = set()
    records = []
    for index, pos in enumerate(positions):
        declaration = lines[pos].strip()
        desc_match = next((m for line in lines[pos+1:positions[index+1] if index+1 < len(positions) else len(lines)]
                           if (m := DESC.match(line))), None)
        if not desc_match:
            raise GateError("method descriptor missing")
        desc = desc_match.group(1)
        name = declaration.split("(", 1)[0].rsplit(" ", 1)[-1]
        if name == simple or name.endswith("." + simple):
            continue
        if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
            raise GateError("unrecognized method name")
        identity = (name, desc)
        if identity in seen:
            raise GateError("duplicate method signature")
        seen.add(identity)
        body = lines[pos+1:positions[index+1] if index+1 < len(positions) else len(lines)]
        members = []
        invoke_count = 0
        branch_count = 0
        for line in body:
            before, separator, after = line.partition("//")
            m = OP.match(before)
            if not m:
                continue
            opcode, comment = m.group(1), after.strip() if separator else ""
            if opcode.startswith(("if", "goto")) or opcode in ("tableswitch", "lookupswitch"):
                branch_count += 1
            if not focus_pattern.match(name):
                continue
            if opcode.startswith("invoke") or opcode in ("getfield", "getstatic", "putfield", "putstatic"):
                match = SYMBOL.match(comment)
                if not match:
                    # These comments may be absent in newer javap output; never infer calls.
                    continue
                kind, reference = match.groups()
                if opcode.startswith("invoke"):
                    invoke_count += 1
                normalized = kind + " " + reference
                if len(normalized) > 2048:
                    raise GateError("unbounded JVM symbol")
                if normalized not in members:
                    members.append(normalized)
                if len(members) > 90:
                    raise GateError("too many member references")
        records.append({"method": name, "descriptor": desc, "is_focus": bool(focus_pattern.match(name)),
                        "branches": branch_count if focus_pattern.match(name) else None,
                        "invokes": invoke_count if focus_pattern.match(name) else None,
                        "members": members if focus_pattern.match(name) else []})
    if not records:
        raise GateError("no real methods")
    focus = [x for x in records if x["is_focus"]]
    if not focus:
        raise GateError("no discoverable magic-method candidate")
    return {
        "declared_methods": len(records),
        "focused_methods": len(focus),
        "methods": focus,
        "other_declared": [{"method": x["method"], "descriptor": x["descriptor"]}
                           for x in records if not x["is_focus"]],
    }

def inspect(jar: Path) -> dict:
    if jar.name != FILENAME or not jar.is_file() or jar.is_symlink():
        raise GateError("invalid publisher file path")
    size = jar.stat().st_size
    if not 100 < size < 20_000_000:
        raise GateError("invalid publisher byte count")
    blob = jar.read_bytes()
    observed = hashlib.sha1(blob).hexdigest()
    if observed != SHA1:
        raise GateError("publisher SHA-1 differs from physical pack")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise GateError("duplicate ZIP members")
        for namespace, name in CLASSES.items():
            path = name.replace(".", "/") + ".class"
            if path not in names:
                raise GateError("previously verified class missing: " + namespace)
    rows = {}
    for namespace, class_name in CLASSES.items():
        p = subprocess.run(["javap", "-p", "-s", "-c", "-classpath", str(jar.resolve()), class_name],
                           capture_output=True, text=True, timeout=35, check=False)
        if p.returncode:
            raise GateError("javap failed on " + namespace)
        row = parse_javap(p.stdout, class_name.rsplit(".", 1)[-1])
        rows[namespace] = {"fqcn": class_name, **row}
        print("SOMAKE_CAST_DISCOVERY", namespace, "methods", row["declared_methods"],
              "focused", row["focused_methods"],
              "names", ",".join(x["method"] for x in row["methods"]))
        for method in row["methods"]:
            if method["members"]:
                print("SOMAKE_CAST_REFS", namespace, method["method"], json.dumps(method["members"]))
    if hashlib.sha1(jar.read_bytes()).hexdigest() != observed:
        raise GateError("JAR changed after audit")
    return {
        "status": "PASS_STATIC_METHOD_REFERENCES_ONLY",
        "scope": "7 preexisting Somake 1.0.9 spell identities",
        "physical_sha1": observed,
        "provider_version": "1.0.9",
        "audited_classes": len(rows),
        "results": rows,
        "limits": [
            "Signature/member reference presence does not prove reachability, branch predicates, dataflow, or runtime behavior.",
            "No per-player hook, range setter, damage formula, target/area geometry, or cooldown is approved solely by this report.",
            "No JAR, source implementation body, animation, localization prose, or game asset is exported.",
        ],
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = inspect(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SOMAKE_CAST_GATE", result["status"], result["audited_classes"], result["physical_sha1"])

if __name__ == "__main__":
    main()
