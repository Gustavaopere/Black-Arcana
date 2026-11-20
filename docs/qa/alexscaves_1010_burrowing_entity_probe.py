#!/usr/bin/env python3
"""Bounded read-only javap capture of the exact 1.0.10 Burrowing Arrow pathways.

Discovery only. No behavior, provider universe, hook, or physical QA is certified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

EXPECTED_SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
EXPECTED_SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
EXPECTED_SIZE = 75279314
EXPECTED_ITEM_SHA256 = "be5e566fc89b01c311d70d8d2a0fbbe7387601c9b07e70417135bd668b51fded"
BASENAMES = ("BurrowingArrowItem", "BurrowingArrowEntity", "ACItemRegistry$6")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    raw = args.jar.read_bytes()
    if (len(raw) != EXPECTED_SIZE or sha256(raw) != EXPECTED_SHA256
            or hashlib.sha1(raw).hexdigest() != EXPECTED_SHA1):
        raise SystemExit("FAIL-CLOSED: publisher JAR identity mismatch")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    with zipfile.ZipFile(args.jar) as z:
        names = z.namelist()
        classes = [n for n in names if n.endswith(".class")]
        if len(names) != len(set(names)) or len(classes) != 1555:
            raise SystemExit("FAIL-CLOSED: exact JAR class roster mismatch")
        for basename in BASENAMES:
            matches = [n for n in classes if n.endswith("/" + basename + ".class")]
            if len(matches) != 1:
                raise SystemExit(f"FAIL-CLOSED: expected one {basename}, got {len(matches)}")
            internal = matches[0][:-6]
            class_bytes = z.read(matches[0])
            class_hash = sha256(class_bytes)
            if basename == "BurrowingArrowItem" and class_hash != EXPECTED_ITEM_SHA256:
                raise SystemExit("FAIL-CLOSED: item class mismatch")
            fqcn = internal.replace("/", ".")
            command = [args.javap, "-classpath", str(args.jar), "-c", "-p", "-s", "-v", fqcn]
            completed = subprocess.run(command, capture_output=True, text=True, check=True)
            if not completed.stdout.strip() or "Code:" not in completed.stdout:
                raise SystemExit(f"FAIL-CLOSED: missing bytecode for {fqcn}")
            destination = args.output_dir / (basename.replace("$", "_") + ".javap.txt")
            destination.write_text(completed.stdout, encoding="utf-8")
            results[basename] = {
                "class_path": matches[0],
                "class_sha256": class_hash,
                "class_size_bytes": len(class_bytes),
                "javap_sha256": sha256(completed.stdout.encode("utf-8")),
                "javap_lines": len(completed.stdout.splitlines()),
                "transcript": destination.name,
            }
    report = {
        "scope": "EXACT_NATIVE_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "version": "1.0.10",
            "sha1": EXPECTED_SHA1,
            "sha256": EXPECTED_SHA256,
            "size_bytes": EXPECTED_SIZE,
            "classes": 1555,
        },
        "targets": results,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
    }
    path = args.output_dir / "report.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
