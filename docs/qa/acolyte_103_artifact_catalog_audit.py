#!/usr/bin/env python3
"""Verify a pinned Acolyte publisher ZIP/catalog; never infer installed or gameplay QA."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import zipfile

PINNED_IDENTITY = (
    "ad0abc821f3f8a6573ac19a50970fc1bc46b4275",
    "73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256",
    621837,
)
LIMITS = {"claim_scope": "CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY",
          "installed_artifact_identity": "NOT_VERIFIED",
          "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED"}


class AuditError(ValueError):
    pass


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuditError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_manifest(path):
    return json.loads(path.read_text(encoding="utf8"), object_pairs_hook=unique_pairs)


def canonical(path):
    return (isinstance(path, str) and bool(path) and "\\" not in path
            and "\x00" not in path and ":" not in path
            and all(part not in {"", ".", ".."} for part in path.split("/")))


def validate_archive(blob, doc, *, expected_identity=PINNED_IDENTITY):
    """The optional identity is for synthetic tests; the CLI always uses the pin."""
    sha1, sha256, size = expected_identity
    if (len(blob) != size or hashlib.sha1(blob).hexdigest() != sha1
            or hashlib.sha256(blob).hexdigest() != sha256):
        raise AuditError("publisher artifact identity mismatch")
    if (not isinstance(doc, dict) or type(doc.get("schema_version")) is not int
            or doc["schema_version"] != 1 or doc.get("version") != "1.0.3"
            or doc.get("artifact_sha1") != sha1 or doc.get("artifact_sha256") != sha256
            or type(doc.get("artifact_size_bytes")) is not int
            or doc["artifact_size_bytes"] != size or "source_revision" in doc
            or any(doc.get(key) != value for key, value in LIMITS.items())):
        raise AuditError("manifest identity or publisher-only scope mismatch")
    files = doc.get("artifact_files")
    if not isinstance(files, list) or not files:
        raise AuditError("missing artifact members")
    members = {}
    for entry in files:
        if (not isinstance(entry, dict) or not canonical(entry.get("path"))
                or entry["path"] in members or type(entry.get("bytes")) is not int
                or entry["bytes"] < 0 or not isinstance(entry.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
            raise AuditError("invalid or duplicate manifest file")
        members[entry["path"]] = entry
    directories = doc.get("artifact_directories")
    if (not isinstance(directories, list)
            or not all(isinstance(path, str) and path.endswith("/")
                       and canonical(path[:-1]) for path in directories)
            or len(set(directories)) != len(directories)):
        raise AuditError("invalid or duplicate manifest directory")
    objects, cards, aggregates = (doc.get(key) for key in
                                  ("catalog_objects", "cards", "aggregates"))
    if (not isinstance(objects, dict) or not objects or not isinstance(cards, dict)
            or not isinstance(aggregates, dict) or set(objects) & set(aggregates)
            or not all(isinstance(value, str) for value in objects.values())
            or len(objects) != len(cards) or set(objects.values()) != set(cards)
            or not all(canonical(path) and path.startswith("✅-acolyte/")
                       and path.endswith(".md") and isinstance(digest, str)
                       and re.fullmatch(r"[0-9a-f]{64}", digest)
                       for path, digest in cards.items())):
        raise AuditError("invalid card/object crosswalk")
    referenced = set()
    for entry in files:
        refs = entry.get("catalog_refs")
        if (not isinstance(refs, list) or not refs
                or not all(isinstance(ref, str) and ref in objects.keys() | aggregates.keys()
                           for ref in refs)):
            raise AuditError("unmapped artifact member")
        referenced.update(refs)
    if not objects.keys() <= referenced:
        raise AuditError("unreferenced catalog object")
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            infos = archive.infolist()
            if any(count != 1 for count in Counter(info.filename for info in infos).values()):
                raise AuditError("duplicate archive path")
            regular, actual_dirs = {}, set()
            for info in infos:
                if info.is_dir():
                    if not canonical(info.filename[:-1]):
                        raise AuditError("noncanonical archive directory")
                    actual_dirs.add(info.filename)
                else:
                    if not canonical(info.filename):
                        raise AuditError("noncanonical archive file")
                    regular[info.filename] = info
            if set(regular) != set(members) or actual_dirs != set(directories):
                raise AuditError("archive/manifest path mismatch")
            class_count = 0
            for path, info in regular.items():
                data = archive.read(info)
                entry = members[path]
                if (len(data) != entry["bytes"]
                        or hashlib.sha256(data).hexdigest() != entry["sha256"]):
                    raise AuditError("archive/manifest member bytes mismatch: " + path)
                if path.endswith(".class"):
                    class_count += 1
                    if (len(data) < 8 or data[:4] != b"\xca\xfe\xba\xbe"
                            or struct.unpack(">H", data[6:8])[0] != 65):
                        raise AuditError("expected Java 21 classfile header: " + path)
                    if ("class_major_version" in entry
                            and (type(entry["class_major_version"]) is not int
                                 or entry["class_major_version"] != 65)):
                        raise AuditError("manifest classfile major mismatch")
    except (zipfile.BadZipFile, RuntimeError, OSError) as error:
        raise AuditError("invalid archive data: " + str(error)) from error
    counts = {"archive_entry_count": len(infos), "artifact_file_count": len(regular),
              "artifact_directory_count": len(actual_dirs), "class_file_count": class_count}
    if any(type(doc.get(key)) is not int or doc[key] != value for key, value in counts.items()):
        raise AuditError("archive/manifest count mismatch")
    if expected_identity == PINNED_IDENTITY and tuple(counts.values()) != (469, 359, 110, 93):
        raise AuditError("pinned release inventory mismatch")
    return {"version": "1.0.3", **LIMITS, "artifact_sha1": sha1,
            "artifact_sha256": sha256, "artifact_size_bytes": size, **counts,
            "catalog_cards": len(cards), "result": "PASS_PUBLISHER_ZIP_CROSSWALK_ONLY"}


def validate_card_files(doc, providers):
    for relative, digest in doc["cards"].items():
        path = (providers / relative).resolve()
        if (not path.is_relative_to((providers / "✅-acolyte").resolve())
                or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
            raise AuditError("card hash mismatch: " + relative)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    doc = load_manifest(args.manifest)
    # No CLI override of the publisher pin or source/installed/runtime claim scope.
    result = validate_archive(args.jar.read_bytes(), doc)
    validate_card_files(doc, args.manifest.resolve().parent.parent)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
