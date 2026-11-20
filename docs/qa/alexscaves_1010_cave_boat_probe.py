#!/usr/bin/env python3
"""Read-only, SHA-exact publisher JAR inspection of CaveBoatItem and native boat entities.

Discovery output is *not* certification of game effects, hooks, or physical QA.
No third-party class bytes or code are committed to the repository.
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
CLASS_COUNT = 1555
ROSTER_COUNT = 8898
TARGETS = {
    "CaveBoatItem": "com/github/alexmodguy/alexscaves/server/item/CaveBoatItem",
    "AlexsCavesBoatEntity": "com/github/alexmodguy/alexscaves/server/entity/item/AlexsCavesBoatEntity",
    "AlexsCavesChestBoatEntity": "com/github/alexmodguy/alexscaves/server/entity/item/AlexsCavesChestBoatEntity",
    "AlexsCavesBoat_Type": "com/github/alexmodguy/alexscaves/server/entity/util/AlexsCavesBoat$Type",
    "ACCompat": "com/github/alexmodguy/alexscaves/server/misc/ACCompat",
}
EXPECTED_ITEM_SHA256 = "92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run(jar: Path, javap: str, output: Path) -> dict:
    jar_bytes = jar.read_bytes()
    if (len(jar_bytes) != SIZE or sha(jar_bytes) != SHA256
            or hashlib.sha1(jar_bytes).hexdigest() != SHA1):
        raise RuntimeError("FAIL-CLOSED: unexpected publisher JAR identity")
    output.mkdir(parents=True, exist_ok=True)
    result = {}
    with zipfile.ZipFile(jar) as z:
        roster = z.namelist()
        classes = [n for n in roster if n.endswith(".class")]
        if (len(roster) != ROSTER_COUNT or len(classes) != CLASS_COUNT
                or len(set(roster)) != len(roster)):
            raise RuntimeError("FAIL-CLOSED: unexpected archive roster")
        related = sorted(n for n in classes if "Boat" in n and n.startswith(
            "com/github/alexmodguy/alexscaves/"))
        for label, internal_name in TARGETS.items():
            path = internal_name + ".class"
            if roster.count(path) != 1:
                raise RuntimeError("FAIL-CLOSED: absent or duplicate " + path)
            bytecode = z.read(path)
            class_hash = sha(bytecode)
            if label == "CaveBoatItem" and class_hash != EXPECTED_ITEM_SHA256:
                raise RuntimeError("FAIL-CLOSED: item class mismatch")
            command = [javap, "-v", "-c", "-p", "-s", "-classpath",
                       str(jar), internal_name.replace("/", ".")]
            cp = subprocess.run(command, capture_output=True, text=True, check=True)
            if not cp.stdout.strip() or "Code:" not in cp.stdout:
                raise RuntimeError("FAIL-CLOSED: missing bytecode " + label)
            name = label + ".javap.txt"
            data = cp.stdout.encode("utf-8")
            (output / name).write_bytes(data)
            result[label] = {
                "class_path": path,
                "class_sha256": class_hash,
                "class_bytes": len(bytecode),
                "javap_sha256": sha(data),
                "javap_lines": len(cp.stdout.splitlines()),
                "transcript": name,
            }
    report = {
        "scope": "DISCOVERY_NOT_CERTIFIED",
        "publisher_version": "1.0.10",
        "publisher_sha1": SHA1,
        "publisher_sha256": SHA256,
        "publisher_size": SIZE,
        "class_count": CLASS_COUNT,
        "related_boat_class_paths": related,
        "targets": result,
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "provider_universe_closed": False,
        "mutation": "NO_MUTATION",
    }
    (output / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run(args.jar, args.javap, args.output_dir)

if __name__ == "__main__":
    main()
