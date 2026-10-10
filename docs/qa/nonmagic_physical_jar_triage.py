#!/usr/bin/env python3
"""Read-only candidate-path/cryptographic triage for all 489 non-Magic JARs.

The manifest comes from the pinned 587-row physical modlist, with 97 Magic
entries and one NeoForge loader entry excluded. ZIP member *names* are hints,
not proof of mod ownership, runtime registration, survival acquisition,
absence of magic, code behavior, or publisher/source equivalence.
No archive member body is extracted, copied or decompiled.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import re
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/qa/nonmagic_physical_manifest_2026-10-08.json"
MAX_JAR_BYTES = 1_073_741_824
MAX_ARCHIVE_MEMBERS = 100_000
MAX_MEMBER_NAME = 256
MAX_CANDIDATE_NAMES = 16
SIGNALS = re.compile(
    r"spell|ritual|glyph|magic|arcane|arcanum|sorcer|wizard|incant|"
    r"enchant|altar|summon|necrom|hex|curse|spirit|soul|ability|"
    r"power|channel|beam|transmut|portal|teleport",
    re.IGNORECASE,
)


def manifest_entries(manifest: Path = MANIFEST) -> list[dict]:
    obj = json.loads(manifest.read_text(encoding="utf-8"))
    if (
        obj.get("schema") != "black_arcana_nonmagic_jar_manifest_v1"
        or obj.get("source_commit") != "de80b186357cad20ba5b81892a8682777e96e35a"
        or obj.get("nonmagic_rows_including_loader") != 490
        or obj.get("nonmagic_mod_jars") != 489
        or obj.get("loader", {}).get("physical_number") != 1
    ):
        raise ValueError("unrecognized or drifted physical modlist snapshot")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 489:
        raise ValueError("expected 489 non-Magic JAR rows, excluding the modloader")
    ids: set[int] = set()
    filenames: set[str] = set()
    for item in rows:
        number, filename = item["physical_number"], item["filename"]
        if (
            not isinstance(number, int) or number <= 1 or number > 587
            or number in ids
            or not isinstance(filename, str)
            or len(filename) > MAX_MEMBER_NAME
            or not filename.endswith(".jar")
            or filename in filenames
            or filename in (".", "..")
            or "/" in filename or "\\" in filename
            or any(ord(ch) < 32 for ch in filename)
        ):
            raise ValueError(f"invalid or duplicate physical JAR identity: #{number}")
        if item.get("triage_group") not in (
            "LEXICAL_NAME", "RPG_GEAR_MOBS_DIMENSIONS", "OTHER"
        ):
            raise ValueError(f"unrecognized triage group: #{number}")
        ids.add(number)
        filenames.add(filename)
    return rows


def inspect_zip_name_signals(archive: zipfile.ZipFile) -> tuple[str, int, int, list[str]]:
    members = archive.infolist()
    if len(members) > MAX_ARCHIVE_MEMBERS:
        return ("TOO_MANY_MEMBERS", len(members), 0, [])
    hits = 0
    examples: list[str] = []
    for member in members:
        name = member.filename
        if (
            not member.is_dir()
            and len(name) <= MAX_MEMBER_NAME
            and ".." not in name.split("/")
            and SIGNALS.search(name)
        ):
            hits += 1
            if len(examples) < MAX_CANDIDATE_NAMES:
                examples.append(name)
    return ("FINGERPRINTED", len(members), hits, examples)


def scan(mods: Path, rows: list[dict]) -> dict:
    if not mods.is_dir() or mods.is_symlink():
        raise ValueError("mods must be an existing non-symlink directory")
    root = mods.resolve()
    results = []
    for item in rows:
        path = mods / item["filename"]
        row = {
            "physical_number": item["physical_number"],
            "name": item["name"],
            "filename": item["filename"],
            "triage_group": item["triage_group"],
        }
        try:
            if path.is_symlink():
                row["status"] = "UNSAFE_SYMLINK"
            elif not path.is_file():
                row["status"] = "MISSING"
            elif not path.resolve().is_relative_to(root):
                row["status"] = "UNSAFE_OUT_OF_ROOT"
            else:
                # Bind ZIP hints and hashes to a single open descriptor. Otherwise
                # a replaced pathname could pair artifact A's names with B's digest.
                flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                with os.fdopen(os.open(path, flags), "rb") as artifact:
                    first = os.fstat(artifact.fileno())
                    if not stat.S_ISREG(first.st_mode):
                        row["status"] = "UNREADABLE"
                    elif first.st_size > MAX_JAR_BYTES:
                        row["status"] = "OVERSIZED"
                    else:
                        with zipfile.ZipFile(artifact) as archive:
                            outcome, member_count, hits, examples = inspect_zip_name_signals(archive)
                        if outcome == "TOO_MANY_MEMBERS":
                            row.update(status=outcome, archive_member_count=member_count)
                        else:
                            sha256 = hashlib.sha256()
                            sha1 = hashlib.sha1()
                            artifact.seek(0)
                            for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
                                sha256.update(chunk)
                                sha1.update(chunk)
                            final = os.fstat(artifact.fileno())
                            current_path = os.stat(path, follow_symlinks=False)

                            def fingerprint(st: os.stat_result) -> tuple[int, int, int, int, int]:
                                return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)

                            if fingerprint(first) != fingerprint(final) or fingerprint(first) != fingerprint(current_path):
                                row["status"] = "CHANGED_DURING_SCAN"
                            else:
                                row.update(
                                    status=outcome,
                                    sha1=sha1.hexdigest(),
                                    sha256=sha256.hexdigest(),
                                    bytes=final.st_size,
                                    archive_member_count=member_count,
                                    lexical_hint_member_count=hits,
                                    lexical_hint_examples=examples,
                                )
        except zipfile.BadZipFile:
            row["status"] = "INVALID_ZIP_JAR"
        except (OSError, RuntimeError, ValueError, EOFError):
            row["status"] = "UNREADABLE"
        results.append(row)
    counts = dict(sorted(Counter(x["status"] for x in results).items()))
    return {
        "schema": "black_arcana_nonmagic_jar_triage_v1",
        "evidence": "ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF",
        "source_commit": "de80b186357cad20ba5b81892a8682777e96e35a",
        "attempted": len(rows),
        "statuses": counts,
        "rows": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument(
        "--physical-numbers", type=str, default="",
        help="Comma-separated subset of physical numbers; default scans all 489",
    )
    args = parser.parse_args()
    rows = manifest_entries()
    if args.physical_numbers:
        try:
            subset = set(int(token) for token in args.physical_numbers.split(","))
        except ValueError as exc:
            parser.error(f"physical numbers must be comma-separated integers: {exc}")
        known = {row["physical_number"] for row in rows}
        if not subset or not subset.issubset(known):
            parser.error("physical number not present in the pinned non-Magic JAR manifest")
        rows = [row for row in rows if row["physical_number"] in subset]
    report = scan(args.instance / "mods", rows)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
