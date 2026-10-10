#!/usr/bin/env python3
"""Read-only, bounded NeoForge metadata check for the source-blocked #272 JAR.

Only META-INF/neoforge.mods.toml is read. This does not run mod code, read
spell payloads, certify registries, or prove acquisition in Survival.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import re
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/qa/nonmagic_physical_manifest_2026-10-08.json"
PROVENANCE = ROOT / "docs/qa/nonmagic_missing_dossier_272_2026-10-09.json"
SOURCE_COMMIT = "de80b186357cad20ba5b81892a8682777e96e35a"
METADATA_PATH = "META-INF/neoforge.mods.toml"
MAX_JAR_BYTES = 1_073_741_824
MAX_METADATA_BYTES = 65_536
MAX_ARCHIVE_MEMBERS = 100_000
MOD_ID = re.compile(r"^[a-z][a-z0-9_]{1,63}$")


def inspect_272_metadata(jar: Path, expected_mod_id: str) -> dict:
    """Read only the bounded NeoForge metadata entry, never registry payloads."""
    result = {
        "schema": "black_arcana_nonmagic_272_metadata_probe_v1",
        "evidence": "EMBEDDED_MOD_ID_ONLY_NOT_SPELL_REGISTRY_OR_RUNTIME_PROOF",
        "expected_mod_id": expected_mod_id,
        "status": "UNREADABLE",
        "registry_entries_verified": False,
        "survival_acquisition_verified": False,
        "spell_count": None,
    }

    def blocked(reason: str) -> dict:
        result["status"] = reason
        return result

    if not MOD_ID.fullmatch(expected_mod_id):
        raise ValueError("invalid source-attested mod ID")
    if jar.is_symlink():
        return blocked("UNSAFE_SYMLINK")
    if not jar.is_file():
        return blocked("MISSING_JAR")
    try:
        # Bind ZIP metadata, SHA-256 and final identity to one open descriptor.
        # Reopening the path could mix the metadata from artifact A with
        # the hash of a replacement artifact B.
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(jar, flags), "rb") as artifact:
            initial = os.fstat(artifact.fileno())
            if not stat.S_ISREG(initial.st_mode):
                return blocked("UNREADABLE")
            if initial.st_size > MAX_JAR_BYTES:
                return blocked("OVERSIZED_JAR")
            with zipfile.ZipFile(artifact) as z:
                entries = z.infolist()
                if len(entries) > MAX_ARCHIVE_MEMBERS:
                    return blocked("TOO_MANY_MEMBERS")
                metadata = [x for x in entries if x.filename == METADATA_PATH and not x.is_dir()]
                if not metadata:
                    return blocked("MISSING_NEOFORGE_METADATA")
                if len(metadata) != 1:
                    return blocked("AMBIGUOUS_NEOFORGE_METADATA")
                info = metadata[0]
                if info.file_size > MAX_METADATA_BYTES:
                    return blocked("METADATA_OVERSIZED")
                with z.open(info, "r") as stream:
                    contents = stream.read(MAX_METADATA_BYTES + 1)
                if len(contents) > MAX_METADATA_BYTES:
                    return blocked("METADATA_OVERSIZED")
            try:
                parsed = tomllib.loads(contents.decode("utf-8"))
            except (UnicodeError, tomllib.TOMLDecodeError):
                return blocked("INVALID_NEOFORGE_METADATA")
            mods = parsed.get("mods")
            if not isinstance(mods, list) or not mods:
                return blocked("INVALID_NEOFORGE_METADATA")
            ids = [item.get("modId") for item in mods if isinstance(item, dict)]
            if (len(ids) != len(mods) or not all(isinstance(x, str) and MOD_ID.fullmatch(x) for x in ids)
                    or len(set(ids)) != len(ids)):
                return blocked("INVALID_NEOFORGE_METADATA")
            sha = hashlib.sha256()
            artifact.seek(0)
            for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
                sha.update(chunk)
            completed = os.fstat(artifact.fileno())
            current_path = os.stat(jar, follow_symlinks=False)

            def fingerprint(st: os.stat_result) -> tuple[int, int, int, int, int]:
                return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)

            if fingerprint(initial) != fingerprint(completed) or fingerprint(initial) != fingerprint(current_path):
                return blocked("CHANGED_DURING_SCAN")
        result["sha256"] = sha.hexdigest()
        result["embedded_mod_ids"] = ids
        result["status"] = (
            "MATCHED_EMBEDDED_MOD_ID" if expected_mod_id in ids else "MOD_ID_MISMATCH"
        )
        return result
    except zipfile.BadZipFile:
        return blocked("INVALID_JAR")
    except (OSError, RuntimeError, ValueError, EOFError):
        return blocked("UNREADABLE")


def probe_instance(instance: Path, manifest: Path = MANIFEST, provenance: Path = PROVENANCE) -> dict:
    """Fail closed unless #272 identity matches both pinned documentary records."""
    source = json.loads(manifest.read_text(encoding="utf-8"))
    evidence = json.loads(provenance.read_text(encoding="utf-8"))
    row = next((x for x in source["rows"] if x["physical_number"] == 272), None)
    attested = evidence["observed_from_pinned_sibling"]
    if (
        source["source_commit"] != SOURCE_COMMIT
        or evidence["snapshot"]["commit"] != SOURCE_COMMIT
        or evidence["physical_number"] != 272
        or row is None
        or row["triage_group"] != "OTHER"
        or row["filename"] != attested["jar_filename"]
        or row["version"] != attested["version"]
        or attested["dossier_available"] is not False
    ):
        raise ValueError("#272 documentary provenance mismatch; refusing metadata claim")
    filename = row["filename"]
    if filename != "factory_construction_registry_probe-0.1.0.jar":
        raise ValueError("#272 physical filename drift; require new authority")
    mods = instance / "mods"
    if mods.is_symlink() or not mods.is_dir():
        raise ValueError("mods must be an existing non-symlink directory")
    result = inspect_272_metadata(mods / filename, attested["declared_mod_id"])
    result.update(physical_number=272, filename=filename, source_commit=SOURCE_COMMIT)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = probe_instance(args.instance)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "MATCHED_EMBEDDED_MOD_ID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
