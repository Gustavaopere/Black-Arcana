#!/usr/bin/env python3
"""Read-only exact-JAR inventory of Alex's Caves DamageSource factories/callsites.

Does NOT certify effective gameplay, mutating hooks, total hit counts or runtime
damage. The 1.0.10 compiled artifact, not public 1.1.1 source, is authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
BASE = "com/github/alexmodguy/alexscaves/"
OWNER = BASE + "server/misc/ACDamageTypes"
IDS = (
    "acid", "dark_arrow", "desolate_dagger", "forsaken_sonic_boom",
    "gumball", "intentional_game_design", "nuke", "radiation",
    "raygun", "spirit_dinosaur", "tremorzilla_beam",
)
METHOD_LINE = re.compile(r"^  ([^ \n].*?)(?:\s*)\;$")
DESCRIPTOR_LINE = re.compile(r"^\s*descriptor:\s*(\S+)")
CODE_LINE = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\s*(.*?)\s*(?://\s*(.*))?$")
SOURCE_SYMBOL = re.compile(
    r"(?:Method|InterfaceMethod)\s+"
    r"(?:(?P<owner>[a-zA-Z0-9_/$]+)\.)?"
    r"(?P<method>[a-zA-Z0-9_$<>]+):(?P<descriptor>\S+)")
FIELD_SYMBOL = re.compile(
    r"Field (?:(?P<owner>[a-zA-Z0-9_/$]+)\.)?(?P<field>[A-Z0-9_]+):(?P<descriptor>\S+)")


def sha_file(path):
    h1, h256, size = hashlib.sha1(), hashlib.sha256(), 0
    with Path(path).open("rb") as stream:
        while part := stream.read(1024 * 1024):
            h1.update(part)
            h256.update(part)
            size += len(part)
    return h1.hexdigest(), h256.hexdigest(), size


def parse_methods(raw):
    """Parse javap -c -p -s with one descriptor per declared method."""
    methods = []
    current = None
    for line in raw.splitlines():
        decl = METHOD_LINE.match(line)
        if decl and "(" in decl.group(1) and not decl.group(1).startswith(("descriptor:", "Compiled from")):
            current = {"header": decl.group(1).strip(), "descriptor": None, "instructions": []}
            methods.append(current)
            continue
        if current is None:
            continue
        desc = DESCRIPTOR_LINE.match(line)
        if desc:
            current["descriptor"] = desc.group(1)
            continue
        if "Code:" in line:
            continue
        code = CODE_LINE.match(line)
        if code:
            offset, opcode, operand, symbol = code.groups()
            current["instructions"].append({
                "offset": int(offset), "opcode": opcode,
                "operand": operand.strip(), "symbol": (symbol or "").strip()
            })
    return [method for method in methods if method["descriptor"] is not None]


def callsites(methods, *, owner):
    out = []
    for method in methods:
        if method["descriptor"] is None:
            continue
        for i in method["instructions"]:
            if not i["opcode"].startswith("invoke"):
                continue
            match = SOURCE_SYMBOL.search(i["symbol"])
            if not match:
                continue
            target_owner = match.group("owner") or owner
            if target_owner != OWNER or not match.group("method").startswith("cause"):
                continue
            out.append({
                "caller_header": method["header"],
                "caller_descriptor": method["descriptor"],
                "bytecode_offset": i["offset"],
                "opcode": i["opcode"],
                "factory_name": match.group("method"),
                "factory_descriptor": match.group("descriptor")
            })
    return out


def factories(methods):
    out = []
    for m in methods:
        name_match = re.search(r"\b(cause[A-Za-z0-9_$]+)\(", m["header"])
        if not name_match:
            continue
        getstatic = []
        constructors = []
        damage_calls = []
        for i in m["instructions"]:
            field = FIELD_SYMBOL.search(i["symbol"])
            if i["opcode"] == "getstatic" and field:
                owning = field.group("owner")
                if owning in (None, OWNER):
                    getstatic.append({"field": field.group("field"), "offset": i["offset"]})
            if i["opcode"] == "invokespecial" and "DamageSourceRandomMessages" in i["symbol"]:
                constructors.append({"offset": i["offset"], "symbol": i["symbol"]})
            if i["opcode"].startswith("invoke") and "DamageSource" in i["symbol"]:
                damage_calls.append({"offset": i["offset"], "symbol": i["symbol"]})
        out.append({
            "method": name_match.group(1), "descriptor": m["descriptor"],
            "header": m["header"], "damage_type_fields": getstatic,
            "damage_source_constructor_sites": constructors,
            "damage_source_calls": damage_calls,
            "method_bytecode_instructions": len(m["instructions"])
        })
    return out


def javap(javap_bin, root, dotted, timeout=45):
    result = subprocess.run(
        [str(javap_bin), "-classpath", str(root), "-c", "-p", "-s", dotted],
        capture_output=True, text=True, timeout=timeout, check=False
    )
    if result.returncode or not result.stdout or len(result.stdout) > 3_500_000:
        raise ValueError("javap failure/oversize for " + dotted + ": " + result.stderr[:300])
    return result.stdout


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise ValueError("exact physical publisher artifact hash/size mismatch")
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate ZIP members")
        members = sorted(p for p in names if p.startswith(BASE) and p.endswith(".class"))
        if OWNER + ".class" not in members or not 100 <= len(members) <= 2500:
            raise ValueError("provider class layout/ACDamageTypes identity mismatch")
        candidates = [(p, arc.read(p)) for p in members
                      if p == OWNER + ".class" or b"ACDamageTypes" in arc.read(p)]
        if len(candidates) > 100:
            raise ValueError("candidate owner population too large")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Each javap invocation requires just the target class, with no
            # provider dependencies executed or loaded into the game runtime.
            for path, content in candidates:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            owner_methods = parse_methods(javap(javap_bin, root, OWNER.replace("/", ".")))
            factory_rows = factories(owner_methods)
            if not factory_rows or len(factory_rows) > 32:
                raise ValueError("no bounded compiled factory set")
            selected = []
            for path, data in candidates:
                if path == OWNER + ".class":
                    continue
                dotted = path[:-6].replace("/", ".")
                method_rows = parse_methods(javap(javap_bin, root, dotted))
                uses = callsites(method_rows, owner=path[:-6])
                if uses:
                    selected.append({
                        "class": path, "sha256": hashlib.sha256(data).hexdigest(),
                        "direct_factory_calls": uses
                    })
    return {
        "schema_version": 1,
        "scope": "EXACT_1_0_10_BYTECODE_DIRECT_CALLSITES_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "owner": {"path": OWNER + ".class", "sha256": hashlib.sha256(
            next(data for path, data in candidates if path == OWNER + ".class")
        ).hexdigest(), "factory_methods": factory_rows},
        "candidate_class_count": len(candidates),
        "direct_calling_classes": selected,
        "damage_type_resource_ids": list(IDS),
        "limits": {
            "static_only": True, "reflection_mixin_datapack_dispatch": "NOT_COVERED",
            "factory_runtime_reachability": "NOT_VERIFIED",
            "effective_damage_attribution": "NOT_VERIFIED",
            "mutating_hooks": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--snapshot", default=None)
    args = parser.parse_args()
    result = audit(args.jar, args.javap)
    if args.snapshot is not None:
        previous = json.loads(Path(args.snapshot).read_text(encoding="utf8"))
        if previous != result:
            raise ValueError("committed consumer bytecode snapshot diverges from exact 1.0.10 JAR")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf8")
    print("ALEXSCAVES_CONSUMERS_1010_BEGIN")
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=False, sort_keys=True))
    print("ALEXSCAVES_CONSUMERS_1010_END")
    print("factories=" + str(len(result["owner"]["factory_methods"]))
          + " callsite_classes=" + str(len(result["direct_calling_classes"]))
          + " class_candidates=" + str(result["candidate_class_count"])
          + "; NO RUNTIME CLAIMS")


if __name__ == "__main__":
    main()
