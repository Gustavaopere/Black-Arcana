#!/usr/bin/env python3
"""SHA-exact, bounded clean-room producer-reference audit for NuclearExplosionEntity.

Finds candidate classes by exact constant-pool UTF-8 tokens and verifies
relevant bytecode instructions. This is NOT a full call graph, constructor
execution proof, mutating integration contract, or runtime acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import (
    GumballStateProbeError, name_of, strict_pairs,
)
from alexscaves_1010_nuclear_envelope_probe import CLASS, CLASS_SHA

TOKENS = (
    b"NuclearExplosionEntity",
    b"NUCLEAR_EXPLOSION",
)
SYMBOL_TOKENS = ("NuclearExplosionEntity", "ACEntityRegistry.NUCLEAR_EXPLOSION")
CONTEXT = 9
MAX_CANDIDATES = 65
MAX_METHODS_PER_CLASS = 300
MAX_METHOD_INSNS = 4500
MAX_SITES = 110
MAX_SELECTED_METHODS = 75


def relevant_method(method):
    ins = method["instructions"]
    if len(ins) > MAX_METHOD_INSNS:
        raise GumballStateProbeError("candidate producer method budget")
    offsets = [x["offset"] for x in ins]
    if len(offsets) != len(set(offsets)):
        raise GumballStateProbeError("duplicate producer bytecode offset")
    positions = [j for j, x in enumerate(ins)
                 if any(t in x["symbol"] for t in SYMBOL_TOKENS)]
    if len(positions) > MAX_SITES:
        raise GumballStateProbeError("producer reference site budget")
    if not positions:
        return None
    def compact(x):
        return {k: x[k] for k in ("offset", "opcode", "operand", "symbol")}
    windows = []
    for j in positions:
        windows.append({
            "at": ins[j]["offset"], "anchor": compact(ins[j]),
            "ins": [compact(v) for v in ins[max(0, j - CONTEXT):j + CONTEXT + 1]],
        })
    digest = hashlib.sha256(json.dumps(
        method, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf8")).hexdigest()
    return {
        "name": name_of(method), "header": method["header"],
        "descriptor": method["descriptor"],
        "instruction_count": len(ins), "parsed_method_sha256": digest,
        "sites": windows,
    }


def collect(jar: Path, javap_bin: str):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("publisher 1.0.10 jar identity drift")
    candidates = []
    with zipfile.ZipFile(jar) as archive:
        members = archive.namelist()
        if len(set(members)) != len(members):
            raise GumballStateProbeError("duplicate publisher JAR entries")
        for name in members:
            if not name.startswith(BASE) or not name.endswith(".class"):
                continue
            data = archive.read(name)
            matched = [x.decode("ascii") for x in TOKENS if x in data]
            if matched:
                candidates.append({
                    "class_path": name, "class_sha256": hashlib.sha256(data).hexdigest(),
                    "token_matches": matched,
                })
        if len(candidates) > MAX_CANDIDATES:
            raise GumballStateProbeError("publisher producer candidate budget exceeded")
    if not candidates or CLASS not in {x["class_path"] for x in candidates}:
        raise GumballStateProbeError("missing own nuclear class in constant-pool scan")
    own = next(x for x in candidates if x["class_path"] == CLASS)
    if own["class_sha256"] != CLASS_SHA:
        raise GumballStateProbeError("NuclearExplosionEntity SHA drift")
    matched_classes = []
    for candidate in candidates:
        cls = candidate["class_path"]
        methods = parse_methods(javap(javap_bin, jar, cls[:-6].replace("/", ".")))
        if len(methods) > MAX_METHODS_PER_CLASS:
            raise GumballStateProbeError("producer class method population budget")
        refs = [v for m in methods if (v := relevant_method(m))]
        if refs:
            matched_classes.append({
                **candidate, "selected_methods": refs,
            })
    selected_count = sum(len(c["selected_methods"]) for c in matched_classes)
    if selected_count > MAX_SELECTED_METHODS:
        raise GumballStateProbeError("producer reference method budget exceeded")
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_NUCLEAR_PRODUCER_REFERENCE_CANDIDATES_NOT_CALL_GRAPH",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "scan": {
            "domain": "provider .class entries only",
            "evidence": "UTF8 candidate token presence + javap selected method reference windows",
            "candidate_tokens": [x.decode("ascii") for x in TOKENS],
            "symbol_tokens": list(SYMBOL_TOKENS),
            "limitations": {
                "bytecode_static_initializer": "EXCLUDED_BY_PARSER",
                "indirect_registry_calls": "POSSIBLY_MISSED",
                "reflection_and_mixin": "NOT_PROVEN",
                "candidate_tokens_are_constructor_proof": False,
                "runtime_owner_and_sender": "NOT_PROVEN",
                "network_state_and_save_reload": "NOT_PROVEN",
                "world_griefing_policy": "NOT_VERIFIED",
                "mutating_hook": "NOT_VERIFIED",
                "physical_qa": "NOT_TESTED",
                "provider_universe_closed": False,
            },
        },
        "candidate_classes": candidates,
        "classes_with_bytecode_references": matched_classes,
    }


def sealed(evidence):
    # Snapshot excludes free-form context windows but binds every relevant
    # parsed method hash, exact JVM descriptor, site anchor, and class hash.
    refs = []
    for cls in evidence["classes_with_bytecode_references"]:
        methods = []
        for m in cls["selected_methods"]:
            anchors = [x["anchor"] for x in m["sites"]]
            if len({x["offset"] for x in anchors}) != len(anchors):
                raise GumballStateProbeError("duplicate producer site offset")
            methods.append({
                "name": m["name"], "descriptor": m["descriptor"],
                "parsed_method_sha256": m["parsed_method_sha256"],
                "instruction_count": m["instruction_count"],
                "site_anchors": anchors,
            })
        refs.append({
            "class_path": cls["class_path"],
            "class_sha256": cls["class_sha256"],
            "selected_methods": methods,
        })
    return {
        "schema_version": evidence["schema_version"],
        "scope": evidence["scope"], "artifact": evidence["artifact"],
        "scan": {
            "candidate_tokens": evidence["scan"]["candidate_tokens"],
            "symbol_tokens": evidence["scan"]["symbol_tokens"],
        },
        "candidate_classes": evidence["candidate_classes"],
        "classes_with_bytecode_references": refs,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--snapshot")
    args = p.parse_args()
    data = collect(Path(args.jar), args.javap)
    minimal = sealed(data)
    if args.snapshot:
        frozen = json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                            object_pairs_hook=strict_pairs)
        if frozen != minimal:
            raise GumballStateProbeError("nuclear producer reference snapshot drift")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2,
                              sort_keys=True) + "\n", encoding="utf8")
    print("NUCLEAR_PRODUCERS_1010_BEGIN")
    print(json.dumps(minimal, ensure_ascii=False,
                     separators=(",", ":"), sort_keys=True))
    print("NUCLEAR_PRODUCERS_1010_END")
    print("NO_RUNTIME_OR_MUTATING_HOOK_CERTIFICATION")


if __name__ == "__main__":
    main()
