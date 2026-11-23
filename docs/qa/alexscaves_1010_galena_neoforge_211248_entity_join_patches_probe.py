#!/usr/bin/env python3
"""Read-only official NeoForge 21.1.248 userdev entity-join PATCH discovery.

Reports patches, locations, line hashes, hunk indices and symbol tokens, not
third-party patch bodies. Does not reconstruct transformed Minecraft or prove
spawn acceptance, event timing, cancellation settlement, safe hooks or QA.
This is DISCOVERY ONLY until a separate version-exact report seal is checked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile

VERSION = "21.1.248"
ARTIFACT = f"neoforge-{VERSION}-userdev.jar"
ROOT = "patches/net/minecraft/"
TARGETS = {
    "ServerLevel": ROOT + "server/level/ServerLevel.java.patch",
    "PersistentEntitySectionManager": ROOT + "world/level/entity/PersistentEntitySectionManager.java.patch",
    "Level": ROOT + "world/level/Level.java.patch",
    "LevelWriter": ROOT + "world/level/LevelWriter.java.patch",
}
WORDS = (
    "EntityJoinLevelEvent", "addFreshEntity", "addNewEntity",
    "isCanceled", "EVENT_BUS", "PersistentEntitySectionManager", "LevelWriter",
)
PATTERN = re.compile(r"(?<![A-Za-z0-9_$])(?:" + "|".join(map(re.escape, WORDS)) +
                     r")(?![A-Za-z0-9_$])")


def need(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(record: dict) -> str:
    return json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def line_kind(line: str) -> str:
    if line.startswith("@@"):
        return "HUNK"
    if line.startswith(("+++", "---")):
        return "HEADER"
    return {"+": "ADD", "-": "DELETE", " ": "CONTEXT",
            "\\": "META"}.get(line[:1], "OTHER")


def scan_patch(path: str, content: bytes) -> dict:
    need(0 < len(content) <= 2_000_000, "patch size budget")
    lines = content.decode("utf-8", errors="strict").splitlines()
    need(lines and any(line.startswith("@@") for line in lines), "no patch hunks")
    hunk = 0
    findings = []
    for number, line in enumerate(lines, 1):
        kind = line_kind(line)
        if kind == "HUNK":
            hunk += 1
            continue
        if kind not in ("ADD", "DELETE", "CONTEXT"):
            continue
        tokens = sorted(set(PATTERN.findall(line[1:])))
        if tokens:
            findings.append({
                "patch_line": number, "hunk": hunk,
                "kind": kind, "tokens": tokens,
                "line_sha256": digest(line.encode("utf-8")),
                "line_bytes": len(line.encode("utf-8")),
            })
    need(0 < hunk <= 2000 and len(findings) <= 2000,
         "patch hunk or findings budget")
    return {
        "path": path, "present": True, "sha256": digest(content),
        "bytes": len(content), "total_lines": len(lines),
        "hunks": hunk, "matched_lines": findings,
        "counts_by_kind": {
            kind: sum(entry["kind"] == kind for entry in findings)
            for kind in ("ADD", "DELETE", "CONTEXT")
        },
        "retains_patch_source": False,
    }


def probe(userdev: Path, output: Path) -> dict:
    need(userdev.is_file() and userdev.name == ARTIFACT,
         "unexpected userdev filename")
    need(0 < userdev.stat().st_size <= 20_000_000, "userdev size budget")
    need(output.suffix == ".json" and not output.exists(),
         "report must be new JSON")
    raw = userdev.read_bytes()
    archive_sha = digest(raw)
    with ZipFile(userdev) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) and len(names) <= 20000,
             "duplicate or excessive ZIP entries")
        patches = sorted(n for n in names if n.startswith(ROOT) and
                         n.endswith(".java.patch"))
        need(len(patches) > 100, "unexpectedly small patch roster")
        targets = {}
        for name, path in TARGETS.items():
            targets[name] = (scan_patch(path, archive.read(path)) if path in names
                             else {"present": False, "path": path})
    result = {
        "schema": 1,
        "scope": "GALENA_NEOFORGE_211248_ENTITY_JOIN_PATCH_DISCOVERY_ONLY",
        "publisher": {
            "artifact": "net.neoforged:neoforge:21.1.248:userdev",
            "official_maven": (
                "https://maven.neoforged.net/releases/net/neoforged/"
                "neoforge/21.1.248/" + ARTIFACT),
            "filename": ARTIFACT, "sha256": archive_sha,
            "bytes": len(raw), "zip_entries": len(names),
            "patches": len(patches),
            "patch_roster_sha256": digest(("\n".join(patches) + "\n").encode()),
        },
        "targets": targets,
        "limitations": {
            "official_maven_sha256_verified_by_ci": True,
            "minecraft_transformed_runtime": "NOT_VERIFIED",
            "all_entity_join_callsites_exhausted": False,
            "event_firing_for_galena_weapon": "NOT_VERIFIED",
            "event_cancellation_settlement": "NOT_VERIFIED",
            "item_stack_rollback": "NOT_VERIFIED",
            "spawn_acceptance": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_contract": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_delta": 0,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(result), encoding="utf-8")
    return result


def selftest() -> None:
    patch = (
        "--- a/S.java\n+++ b/S.java\n@@ -1,2 +1,3 @@\n"
        " context\n-  addNewEntity(entity);\n"
        "+  if (EVENT_BUS.post(new EntityJoinLevelEvent(entity, level)).isCanceled()) return false;\n"
        "+  addFreshEntity(entity);\n"
    ).encode()
    scanned = scan_patch("S", patch)
    assert scanned["hunks"] == 1
    assert scanned["counts_by_kind"] == {
        "ADD": 2, "DELETE": 1, "CONTEXT": 0
    }
    assert len(scanned["matched_lines"]) == 3
    assert "EntityJoinLevelEvent" in scanned["matched_lines"][1]["tokens"]
    assert all("source" not in x for x in scanned["matched_lines"])
    try:
        scan_patch("invalid", b"--- a/S\n+++ b/S\nmissing hunk\n")
    except ValueError:
        pass
    else:
        raise AssertionError("accepted missing unified hunk")
    print("PASS: bounded parser, classified synthetic lines and malformed rejection")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--userdev", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return
    need(args.userdev is not None and args.output is not None,
         "expected --userdev and --output")
    result = probe(args.userdev, args.output)
    print("SCOPE", result["scope"])
    print("USERDEV", result["publisher"])
    for name, record in result["targets"].items():
        if not record["present"]:
            print("TARGET", name, "ABSENT_FROM_PATCH_ROSTER")
            continue
        print("TARGET", name, "SHA256", record["sha256"],
              "HUNKS", record["hunks"], "TOKENS",
              record["counts_by_kind"])
        for row in record["matched_lines"]:
            print("HIT", name, row["patch_line"], row["hunk"],
                  row["kind"], ",".join(row["tokens"]),
                  row["line_sha256"])
    print("REPORT_SHA256", digest(args.output.read_bytes()),
          "BYTES", args.output.stat().st_size)
    print("DISCOVERY_ONLY NO_MUTATION NO_GAMEPLAY_QA")


if __name__ == "__main__":
    main()
