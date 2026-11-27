#!/usr/bin/env python3
"""Read-only NeoForge 21.1.250 ABI discovery for Galena spawn interoperability.

This observes the *upstream API*, not Minecraft's transformed implementation,
the provider call outcome, a safe mutation hook or physical gameplay.
No source text, bytecode or assets are stored in the report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile

VERSION = "21.1.250"
CLASSES = (
    "net/neoforged/neoforge/event/entity/EntityJoinLevelEvent",
    "net/neoforged/neoforge/event/entity/EntityEvent",
    "net/neoforged/neoforge/event/EventHooks",
    "net/neoforged/bus/api/ICancellableEvent",
)
SOURCE_PATH = "net/neoforged/neoforge/event/entity/EntityJoinLevelEvent.java"


def need(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect_zip(path: Path, *, maximum: int) -> dict:
    need(path.is_file(), "missing artifact: " + str(path))
    need(0 < path.stat().st_size < maximum, "artifact size outside bound")
    raw_sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            raw_sha.update(chunk)
    with ZipFile(path) as z:
        names = z.namelist()
        need(len(names) == len(set(names)), "duplicate ZIP entries")
        need(len(names) > 0, "empty archive")
        return {
            "filename": path.name, "bytes": path.stat().st_size,
            "sha256": raw_sha.hexdigest(), "members": len(names),
        }


def declaration_summary(javap: str, jar: Path, owner: str) -> dict:
    run = subprocess.run(
        [javap, "-classpath", str(jar), "-p", "-s", owner.replace("/", ".")],
        text=True, capture_output=True, check=False, timeout=40,
    )
    need(run.returncode == 0, "javap failed: " + owner + " " + run.stderr[:300])
    output = run.stdout
    headers = [s.strip() for s in output.splitlines()
               if " class " in s or " interface " in s]
    need(len(headers) == 1, "ambiguous ABI class header " + owner)
    # Retain only declarations and JVM descriptors, never method bodies.
    rows = []
    unresolved = []
    lines = output.splitlines()
    for i, line in enumerate(lines):
        signature = line.strip()
        if (signature.startswith("descriptor:") or
                "(" not in signature or not signature.endswith(";")):
            continue
        if i + 1 >= len(lines) or not lines[i + 1].strip().startswith("descriptor:"):
            unresolved.append(signature)
            continue
        rows.append({"declaration": signature,
                     "descriptor": lines[i + 1].strip()[11:].strip()})
    need(bool(rows), "no methods found " + owner)
    need(not unresolved, "unresolved method signatures " + owner)
    # Match the method's identifier rather than the package names of arguments.
    def selected(row: dict) -> bool:
        name = row["declaration"].split("(", 1)[0].split()[-1].lower()
        return "join" in name or "entity" in name
    return {"owner": owner, "declaration": headers[0],
            "method_count": len(rows), "unresolved_signatures": unresolved,
            "methods": rows if owner.endswith("/EntityJoinLevelEvent")
            else [r for r in rows if selected(r)]}


def probe(universal: Path, sources: Path, javap: str, output: Path) -> dict:
    need(output.suffix == ".json" and not output.exists(), "write-once JSON only")
    universal_info = inspect_zip(universal, maximum=50_000_000)
    sources_info = inspect_zip(sources, maximum=50_000_000)
    need(universal_info["sha256"] ==
         "1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956",
         "universal publisher SHA-256 drift")
    need(sources_info["sha256"] ==
         "a2811d794544ec67dc3fa43b900158f058ea534881ba1c160373554384311a0d",
         "sources publisher SHA-256 drift")
    with ZipFile(universal) as jar:
        names = set(jar.namelist())
        # Event's own class and event-hook owner must be in this exact binary.
        required = CLASSES[:3]
        need(all(c + ".class" in names for c in required), "required NeoForge class absent")
        class_hashes = {c: sha256(jar.read(c + ".class")) for c in required}
        optional = CLASSES[3]
        if optional + ".class" in names:
            class_hashes[optional] = sha256(jar.read(optional + ".class"))
    with ZipFile(sources) as jar:
        need(SOURCE_PATH in jar.namelist(), "exact event source path absent")
        source_sha = sha256(jar.read(SOURCE_PATH))
    declarations = {
        owner: declaration_summary(javap, universal, owner)
        for owner in CLASSES[:3]
    }
    event = declarations[CLASSES[0]]
    hooks = declarations[CLASSES[2]]
    need("EntityJoinLevelEvent" in event["declaration"], "event identity drift")
    # Report candidates even when not found, rather than asserting a hook.
    event_methods = [m["declaration"] for m in event["methods"]]
    hook_methods = [m["declaration"] for m in hooks["methods"]]
    result = {
        "schema_version": 1,
        "scope": "GALENA_NEOFORGE_211250_ENTITY_JOIN_ABI_DISCOVERY_ONLY",
        "upstream": {"group": "net.neoforged", "artifact": "neoforge",
                     "version": VERSION, "universal": universal_info,
                     "sources": sources_info,
                     "event_source_sha256": source_sha,
                     "class_sha256": class_hashes},
        "api": declarations,
        "candidate": {
            "event_declares_cancellable_interface":
                "ICancellableEvent" in event["declaration"],
            "event_constructor_or_accessor_declarations": event_methods,
            "event_hook_method_declarations": hook_methods,
        },
        "limitations": {
            "jar_installed_parity": "NOT_VERIFIED",
            "event_firing_from_transformed_minecraft": "NOT_VERIFIED",
            "provider_item_consumption_and_spawn_atomicity": "NOT_VERIFIED",
            "event_order_and_spawn_result_acceptance": "NOT_VERIFIED",
            "authoritative_post_spawn_observation": "NOT_VERIFIED",
            "safe_mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
        },
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                 sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--universal", type=Path, required=True)
    p.add_argument("--sources", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = probe(a.universal, a.sources, a.javap, a.output)
    print("scope:", report["scope"])
    print("neoforge:", report["upstream"]["version"])
    for name, entry in report["api"].items():
        print(name, "declared methods:", entry["method_count"],
              "unresolved count:", len(entry["unresolved_signatures"]))
    print("cancellable interface in event class declaration:",
          report["candidate"]["event_declares_cancellable_interface"])
    print("candidate EventHooks declarations:",
          report["candidate"]["event_hook_method_declarations"])
    print("event ABI exact declarations:",
          report["api"][CLASSES[0]]["methods"])
    print("EntityEvent ABI exact declarations:",
          report["api"][CLASSES[1]]["methods"])
    print("class SHA-256:", report["upstream"]["class_sha256"])
    print("event source SHA-256:", report["upstream"]["event_source_sha256"])
    print("upstream artifact archive info:",
          report["upstream"]["universal"], report["upstream"]["sources"])
    print("report SHA-256:", sha256(a.output.read_bytes()))
    print("report size:", a.output.stat().st_size)


if __name__ == "__main__":
    main()
