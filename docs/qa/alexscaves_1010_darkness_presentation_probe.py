#!/usr/bin/env python3
"""SHA-exact read-only discovery: presentation boundaries and Darkness equipment.

Never promotes a mutating hook, semantic magic root, or physical QA state.
Does not commit third-party bytecode, decompiled code, assets, or UI text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_armor_material_audit import ClassReader, digest, require, verify_artifact

PUBLISHER = "alexscaves-1.0.10-neoforge+1.21.1.jar"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
ROOT = "com/github/alexmodguy/alexscaves/"
INTERFACES = ("CustomArmorPostRender", "CustomTabBehavior")
CANDIDATE_TERMS = ("Darkness", "Dark", "Apple", "Cloak", "Hood", "CustomArmorPostRender", "CustomTabBehavior")
RESOURCE_TERMS = ("darkness", "dark_", "apple", "hood", "cloak")
MAX_TRANSCRIPTS = 38

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def inspect(jar: Path, javap: str, output: Path) -> dict:
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as zipf:
        paths = zipf.namelist()
        classes = [p for p in paths if p.endswith(".class")]
        require(len(classes) == 1555 and len(paths) == 8898
                and len(paths) == len(set(paths)), "JAR roster drift")
        raw = {path: zipf.read(path) for path in classes}
        readers = {}
        for path, data in raw.items():
            rd = ClassReader(data)
            require(rd.name + ".class" == path and rd.major == 65, "class identity mismatch")
            readers[rd.name] = rd
        interface_owners = {}
        for label in INTERFACES:
            hits = [owner for owner in readers if owner.endswith("/" + label)]
            require(len(hits) == 1, "missing or ambiguous interface " + label)
            interface_owners[label] = hits[0]
        typed = {}
        for label, owner in interface_owners.items():
            uses = {}
            for class_owner, rd in readers.items():
                refs = rd.typed_refs(owner)
                if refs or owner in rd.interfaces:
                    uses[class_owner] = {
                        "direct_implementer": owner in rd.interfaces,
                        "typed_refs": refs,
                    }
            typed[label] = uses
        matching = sorted(owner for owner in readers
                          if any(term in owner.rsplit("/", 1)[-1] for term in CANDIDATE_TERMS))
        candidates = {}
        for owner in matching:
            rd = readers[owner]
            candidates[owner] = {
                "sha256": sha(raw[owner + ".class"]),
                "parent": rd.parent,
                "interfaces": rd.interfaces,
                "fields": rd.fields,
                "method_declarations": rd.methods,
            }
        selected = set(interface_owners.values())
        for owner in matching:
            short = owner.rsplit("/", 1)[-1]
            if any(t in short for t in ("Darkness", "Apple", "Cloak", "Hood")):
                selected.add(owner)
        for uses in typed.values():
            selected.update(uses.keys())
        for owner in readers:
            if owner.endswith(("/ACItemRegistry", "/ACServerConfig", "/ACEffectRegistry", "/ACArmorMaterial")):
                selected.add(owner)
        score = {}
        for owner in selected:
            base = owner.rsplit("/", 1)[-1]
            score[owner] = (10000 if owner in interface_owners.values() else 0)
            score[owner] += (1200 if "Darkness" in base else 0)
            score[owner] += (900 if any(w in base for w in ("Apple", "Cloak", "Hood")) else 0)
            score[owner] += (600 if "Armor" in base else 0)
        selected = sorted(selected, key=lambda o: (-score[o], o))
        require(len(selected) <= MAX_TRANSCRIPTS, "transcript budget exceeded; audit selection")
        transcript = {}
        for owner in selected:
            result = subprocess.run(
                [javap, "-classpath", str(jar), "-p", "-c", "-v", "-s",
                 owner.replace("/", ".")],
                check=True, capture_output=True, text=True,
            )
            require("Classfile" in result.stdout and result.stdout.strip(), "javap missing")
            data = result.stdout.encode("utf-8")
            filename = owner.replace("/", "_").replace("$", "_") + ".javap.txt"
            (output / filename).write_bytes(data)
            transcript[owner] = {
                "file": filename,
                "class_sha256": sha(raw[owner + ".class"]),
                "javap_sha256": sha(data),
                "javap_lines": len(result.stdout.splitlines()),
            }
        resources = {}
        for path in sorted(paths):
            if not path.endswith(".json") or not any(term in path.lower() for term in RESOURCE_TERMS):
                continue
            blob = zipf.read(path)
            try:
                doc = json.loads(blob)
            except (ValueError, UnicodeError) as exc:
                raise RuntimeError("Invalid publisher JSON: " + path) from exc
            meta = {"sha256": sha(blob), "bytes": len(blob)}
            if isinstance(doc, dict):
                meta["top_level_keys"] = sorted(doc)
                if "/recipe/" in path or "/recipes/" in path:
                    meta["type"] = doc.get("type")
                    meta["result"] = doc.get("result")
                    meta["ingredients"] = doc.get("ingredients")
                    meta["key"] = doc.get("key")
                elif "/advancement/" in path:
                    meta["triggers"] = {
                        k: v.get("trigger") for k, v in doc.get("criteria", {}).items()
                        if isinstance(v, dict)}
            resources[path] = meta
        report = {
            "scope": "EXACT_NATIVE_DISCOVERY_NOT_CERTIFIED",
            "artifact": {
                "filename": PUBLISHER,
                "sha256": SHA256,
                "size_bytes": jar.stat().st_size,
                "class_count": len(classes), "jar_entries": len(paths),
            },
            "interface_owners": interface_owners,
            "typed_consumer_census": typed,
            "class_candidate_inventory": candidates,
            "candidate_count": len(candidates),
            "transcript_count": len(transcript),
            "transcripts": transcript,
            "resource_count": len(resources),
            "filename_matched_resources": resources,
            "mutation": "NO_MUTATION",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False,
            "semantic_magic_roots_certified": 0,
        }
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({
        "artifact_sha256": SHA256,
        "status": report["scope"],
        "interfaces": interface_owners,
        "direct_implementers": {
            label: [owner for owner, row in typed[label].items() if row["direct_implementer"]]
            for label in INTERFACES},
        "candidates": len(candidates), "transcripts": len(transcript),
        "resources": len(resources),
    }, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    inspect(args.jar, args.javap, args.output_dir)
