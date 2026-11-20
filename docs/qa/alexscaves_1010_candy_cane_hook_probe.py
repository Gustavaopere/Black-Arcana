#!/usr/bin/env python3
"""Exact-publisher binary capture of Candy Cane Hook item and typed consumers.

Discovery only; does not certify entity runtime or mutator boundaries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
CLASS_HASHES = {
    "CandyCaneHookItem": "d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44",
    "CandyCaneHookEntity": "e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8",
    "GumWormSegmentEntity": "b112e1b579368872a45464510902b2a6a728e38cdd8d320aa59bb9aa0013e09c",
    "ClientEvents": "52b53d87ec638fda2e0e39be41acec3e09da2c5ab3d327b1b4790bb97a87fbbc",
    "CandyCaneHookRenderer": "ce314d75ef0909c6b1e7f9a9803e271e3915b13b44480e8f4328c16b72376ad9",
    "ACItemPredicates": "ee5ea7be322641a29b49b3b08606928f38456f8ea3bb337a7624a897b379cc89",
    "ACCompat": None,
}

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def inspect(jar: Path, javap: str, output_dir: Path):
    raw = jar.read_bytes()
    if len(raw) != SIZE or hashlib.sha1(raw).hexdigest() != SHA1 or digest(raw) != SHA256:
        raise RuntimeError("FAIL-CLOSED: exact publisher artifact mismatch")
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(jar) as archive:
        roster = archive.namelist()
        classes = [name for name in roster if name.endswith(".class")]
        if len(roster) != 8898 or len(classes) != 1555 or len(roster) != len(set(roster)):
            raise RuntimeError("FAIL-CLOSED: exact archive roster mismatch")
        targets = {}
        for short_name, expected_hash in CLASS_HASHES.items():
            hits = [name for name in classes if name.endswith("/" + short_name + ".class")]
            if len(hits) != 1:
                raise RuntimeError("FAIL-CLOSED: target missing/ambiguous: " + short_name)
            path = hits[0]
            binary = archive.read(path)
            actual_hash = digest(binary)
            if expected_hash is not None and actual_hash != expected_hash:
                raise RuntimeError("FAIL-CLOSED: class changed: " + short_name)
            run = subprocess.run(
                [javap, "-classpath", str(jar), "-v", "-c", "-p", "-s", path[:-6].replace("/", ".")],
                capture_output=True, text=True, check=True,
            )
            if "    Code:" not in run.stdout:
                raise RuntimeError("FAIL-CLOSED: no method bodies for " + short_name)
            transcript = short_name + ".javap.txt"
            data = run.stdout.encode("utf-8")
            (output_dir / transcript).write_bytes(data)
            targets[short_name] = {
                "internal_name": path[:-6],
                "class_sha256": actual_hash,
                "class_size": len(binary),
                "javap_sha256": digest(data),
                "javap_lines": len(run.stdout.splitlines()),
                "transcript": transcript,
            }
    result = {
        "scope": "DISCOVERY_NOT_CERTIFIED",
        "version": "1.0.10",
        "jar_sha1": SHA1,
        "jar_sha256": SHA256,
        "jar_size": SIZE,
        "class_count": 1555,
        "targets": targets,
        "provider_universe_closed": False,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }
    out = output_dir / "report.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    inspect(args.jar, args.javap, args.output_dir)

if __name__ == "__main__":
    main()
