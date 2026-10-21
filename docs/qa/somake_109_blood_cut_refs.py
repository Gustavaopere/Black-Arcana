#!/usr/bin/env python3
"""Clean-room, exact-SHA method reference discovery for Somake Blood Cut 1.0.9.

A class-name candidate is not a verified class until the exact JAR check passes.
No method bodies, classfiles, constants, strings or proprietary assets are exported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

from somake_109_cast_refs import GateError, parse_javap
from somake_109_perk_method_probe import FILENAME, SHA1

TARGET_ID = "somakespells:blood_cut"
CLASS_SUFFIX = "/BloodCutSpell.class"
PREFIX = "com/somake/somakespells/spells/"


def discover_member(names: list[str]) -> str:
    if len(names) != len(set(names)):
        raise GateError("duplicate ZIP member")
    matches = [
        n for n in names
        if n.startswith(PREFIX) and n.endswith(CLASS_SUFFIX)
        and re.fullmatch(r"[A-Za-z0-9_/$.-]+", n)
        and ".." not in n
    ]
    if len(matches) != 1:
        raise GateError(f"unverified/ambiguous Blood Cut class: {len(matches)}")
    return matches[0]


def inspect(jar: Path) -> dict:
    if jar.name != FILENAME or not jar.is_file() or jar.is_symlink():
        raise GateError("invalid Somake artifact")
    if not 100 < jar.stat().st_size < 20_000_000:
        raise GateError("unbounded/invalid jar length")
    source_bytes = jar.read_bytes()
    digest = hashlib.sha1(source_bytes).hexdigest()
    if digest != SHA1:
        raise GateError("JAR differs from exact physical SHA-1")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        member = discover_member(names)
        mods_toml = archive.read("META-INF/neoforge.mods.toml")
        if len(mods_toml) > 250_000 or not re.search(
            rb"\bmodId\s*=\s*['\"]somakespells['\"]", mods_toml
        ):
            raise GateError("mod ID is not somakespells")
    fqcn = member.removesuffix(".class").replace("/", ".")
    process = subprocess.run(
        ["javap", "-p", "-s", "-c", "-classpath", str(jar.resolve()), fqcn],
        capture_output=True, text=True, timeout=35, check=False
    )
    if process.returncode:
        raise GateError("javap could not inspect exact class")
    methods = parse_javap(process.stdout, fqcn.rsplit(".", 1)[-1])
    # These facts are local to a class. No registry relation or runtime result
    # is inferred from a name-match. Only non-body method/member references.
    if hashlib.sha1(jar.read_bytes()).hexdigest() != digest:
        raise GateError("artifact changed during inspection")
    return {
        "status": "PASS_EXACT_SHA_STATIC_CLASS_METHOD_REFERENCES",
        "spell_id": TARGET_ID,
        "version": "1.0.9",
        "sha1": digest,
        "class_candidate_verified_in_jar": fqcn,
        "methods": methods,
        "limits": [
            "Registry identity is sourced independently from the 83-ID exact registry audit.",
            "Declared method, bytecode symbol and branch counts do not establish runtime targeting, damage, duration, LOS or casting reachability.",
            "No mutating hook for RPG Skill Tree or Black Arcana has been verified.",
            "No proprietary classfile, method body, source code, assets or text is exported."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print("SOMAKE_BLOOD_CUT", result["status"], result["sha1"],
          result["class_candidate_verified_in_jar"],
          result["methods"]["declared_methods"],
          result["methods"]["focused_methods"])
    for method in result["methods"]["methods"]:
        print("SOMAKE_BLOOD_CUT_METHOD", method["method"], method["descriptor"],
              "branches", method["branches"], "members",
              json.dumps(method["members"], ensure_ascii=False))


if __name__ == "__main__":
    main()
