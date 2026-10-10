#!/usr/bin/env python3
"""Read-only physical-JAR fingerprints for the 69 installed counted-ledger providers.

The source is the SHA-pinned canonical physical ledger crosswalk. This program
does NOT prove registry cardinality, loaded config, survival reachability,
class authenticity, binary/publisher equality, or runtime acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CROSSWALK = (
    ROOT / "wiki/modpack-catalog/meta"
    / "PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md"
)
MAX_JAR_BYTES = 1024 * 1024 * 1024
LINE = re.compile(
    r"^\| (?P<provider>[^|]+) \| #\d{3} \| "
    r"(?P<quote>.)"
    r"(?P<jar>[^|]+\.jar)"
    r"(?P=quote) \|"
)


def load_manifest(path: Path = CROSSWALK) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    section = text.split("## Exact-current physical crosswalk", 1)[1].split(
        "## Historical catalogs excluded", 1
    )[0]
    result: dict[str, str] = {}
    filenames: set[str] = set()
    for line in section.splitlines():
        match = LINE.match(line)
        if not match:
            continue
        provider = match.group("provider").strip()
        filename = match.group("jar").strip()
        if "/" in filename or "\\" in filename or filename in filenames:
            raise ValueError(f"unsafe or duplicate manifest filename: {filename}")
        if provider in result:
            raise ValueError(f"duplicate provider identity: {provider}")
        result[provider] = filename
        filenames.add(filename)
    if len(result) != 69:
        raise ValueError(f"unexpected physical manifest count: {len(result)}")
    return result


def fingerprint_instance(mods_dir: Path, manifest: dict[str, str]) -> dict:
    if mods_dir.is_symlink() or not mods_dir.is_dir():
        raise ValueError("mods path must be a real existing directory, not a symlink")
    counts = {
        "FINGERPRINTED": 0, "MISSING": 0, "UNSAFE": 0,
        "OVERSIZED": 0, "INVALID_JAR": 0, "UNREADABLE": 0,
        "CHANGED_DURING_SCAN": 0,
    }
    entries = []
    for provider, filename in sorted(manifest.items()):
        path = mods_dir / filename
        item = {"provider": provider, "filename": filename}
        if path.is_symlink():
            item["status"] = "UNSAFE"
        elif not path.is_file():
            item["status"] = "MISSING"
        else:
            try:
                # ZIP validation and both digests must refer to one open JAR.
                # A second pathname open could hash an entirely different JAR.
                flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                with os.fdopen(os.open(path, flags), "rb") as stream:
                    initial = os.fstat(stream.fileno())
                    if not stat.S_ISREG(initial.st_mode):
                        item["status"] = "UNSAFE"
                    elif initial.st_size > MAX_JAR_BYTES:
                        item["status"] = "OVERSIZED"
                    else:
                        with zipfile.ZipFile(stream):
                            pass
                        sha1 = hashlib.sha1()
                        sha256 = hashlib.sha256()
                        stream.seek(0)
                        for block in iter(lambda: stream.read(1024 * 1024), b""):
                            sha1.update(block)
                            sha256.update(block)
                        final = os.fstat(stream.fileno())
                        current_path = os.stat(path, follow_symlinks=False)

                        def identity(st: os.stat_result) -> tuple[int, int, int, int, int]:
                            return (
                                st.st_dev, st.st_ino, st.st_size,
                                st.st_mtime_ns, st.st_ctime_ns,
                            )

                        if identity(initial) != identity(final) or identity(initial) != identity(current_path):
                            item["status"] = "CHANGED_DURING_SCAN"
                        else:
                            item.update(
                                status="FINGERPRINTED",
                                size_bytes=final.st_size,
                                sha1=sha1.hexdigest(),
                                sha256=sha256.hexdigest(),
                            )
            except zipfile.BadZipFile:
                item["status"] = "INVALID_JAR"
            except (OSError, RuntimeError, ValueError, EOFError):
                item["status"] = "UNREADABLE"
        counts[item["status"]] += 1
        entries.append(item)
    return {
        "source": "PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md",
        "evidence_class": "READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF",
        "expected": len(manifest),
        "counts": counts,
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--instance", type=Path, required=True,
        help="Minecraft instance root with a mods/ directory (read-only)",
    )
    args = parser.parse_args()
    report = fingerprint_instance(args.instance / "mods", load_manifest())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
