#!/usr/bin/env python3
"""Exact-JAR clean-room discovery of Wind 1.0.5 effect/registry boundaries.

A method signature, field reference or callsite is a compilation fact, never
evidence that a gameplay modifier executes or a third-party hook is safe.
No third-party instructions, source code, class contents or bundled JAR output.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

import winds_105_spell_metadata as binary
import winds_105_cross_class_getter_calls as cross

EFFECT_NAME = re.compile(r"(?:tailwind|acrobat|effect)", re.IGNORECASE)
MAGIC_FIELDS = {"TAILWIND", "ACROBATICS"}
ENTRY_SPELLS = {"tailwind": "TAILWIND", "aeropic": "ACROBATICS"}
METHOD_FAMILIES = (
    "attribute", "speed", "movement", "jump", "fall", "tick", "effect",
    "hurt", "damage", "knockback", "impulse", "teleport", "apply",
    "remove", "add", "step", "gravity",
)
METHOD_LIMIT = 140

class EvidenceError(ValueError):
    pass

def _field_tags(fields: list[str]) -> list[str]:
    tags = set()
    for field in fields:
        for tag in MAGIC_FIELDS:
            if "." + tag + ":" in field:
                tags.add(tag)
    return sorted(tags)

def classify(class_name: str, methods: dict[str, dict]) -> dict | None:
    """Label candidate sources explicitly: names are not native API proof."""
    matched_name = bool(EFFECT_NAME.search(class_name.split(".")[-1]))
    reference_methods = {}
    role_methods = {}
    for declaration, row in methods.items():
        tagset = set(_field_tags(row.get("read_fields", []))) | set(
            _field_tags(row.get("written_fields", [])))
        if tagset:
            reference_methods[declaration] = sorted(tagset)
        method_name = declaration.split("(", 1)[0].rsplit(" ", 1)[-1]
        if matched_name and any(token in method_name.lower() for token in METHOD_FAMILIES):
            role_methods[declaration] = {
                "observed_invoked_symbols": row.get("invoked_symbols", []),
                "read_fields": row.get("read_fields", []),
                "written_fields": row.get("written_fields", []),
                "numeric_opcodes": row.get("numeric_opcodes", []),
                "branch_opcodes": row.get("branch_opcodes", []),
                "literal_candidates": row.get("literal_operands", []),
                "strength": "JVM_METHOD_SYMBOL_INVENTORY_NOT_ARGUMENT_FLOW",
            }
    if not matched_name and not reference_methods:
        return None
    if len(role_methods) > METHOD_LIMIT or len(reference_methods) > METHOD_LIMIT:
        raise EvidenceError("unbounded relevant method output for " + class_name)
    return {
        "class_name": class_name,
        "class_name_candidate": matched_name,
        "effect_registry_references": reference_methods,
        "candidate_methods": role_methods,
        "classification": "CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY",
        "runtime_effect_settlement": "NOT_PROVEN",
    }

def summarize(inventory: dict, class_data: dict[str, dict[str, dict]],
              universe: list[str]) -> dict:
    if inventory.get("result") != "PASS" or inventory.get("sha1") != binary.EXPECTED_SHA1:
        raise EvidenceError("physical release is not SHA-verified")
    if inventory.get("class_count") != 7 or inventory.get("provider") != "wind_spellbooks":
        raise EvidenceError("wrong primary spell roster")
    if len(universe) != len(set(universe)) or universe != sorted(universe):
        raise EvidenceError("non-canonical class universe")
    if set(class_data) != set(universe):
        raise EvidenceError("class coverage incomplete")
    if len(universe) < 7:
        raise EvidenceError("invalid provider class universe")
    entry_points = {}
    for spell, field in ENTRY_SPELLS.items():
        spells = inventory["spells"][spell]
        oncasts = [row for name, row in spells["methods"].items()
                   if " onCast(" in name]
        if len(oncasts) != 1 or field not in _field_tags(oncasts[0]["read_fields"]):
            raise EvidenceError(f"missing exact spell onCast reference to {field}")
        entry_points[spell] = {
            "referenced_provider_effect_registry_field": field,
            "proof": "EXACT_JVM_FIELD_READ_INSIDE_ONCAST_ONLY",
            "effect_class_or_instance_proven": False,
        }
    result = {}
    for class_name in universe:
        candidate = classify(class_name, class_data[class_name])
        if candidate is not None:
            result[class_name] = candidate
    if not result:
        raise EvidenceError("no candidate symbols in provider")
    return {
        "result": "PASS_SHA_EXACT_EFFECT_CANDIDATE_SYMBOL_AUDIT",
        "sha1": binary.EXPECTED_SHA1,
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "classes_inspected": len(universe),
        "candidate_class_count": len(result),
        "entry_spell_field_refs": entry_points,
        "candidate_classes": result,
        "limits": [
            "native effect class registration not proven by class name or spell field usage",
            "method names, literals and calls are symbols; no value flow or executed gameplay",
            "other providers, Iron's, IronSable, mixins, inherited behavior not in class universe",
            "no client/Survival QA; no mutating RPG perk or Black Arcana adapter",
        ],
    }

def audit(jar: Path) -> dict:
    source = binary.audit(jar)
    classes = cross.class_names(jar)
    collected = {}
    for name in classes:
        try:
            run = subprocess.run(
                ["javap", "-c", "-p", "-classpath", str(jar), name],
                capture_output=True, text=True, timeout=25, check=True,
            )
        except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
            raise EvidenceError("javap failed for effect-boundary class: " + name) from exc
        collected[name] = binary.summarize_disassembly(run.stdout)
    return summarize(source, collected, classes)

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    try:
        result=audit(args.jar)
        status=0
    except (EvidenceError,binary.AuditError,cross.AuditError,
            OSError,ValueError,KeyError,TypeError) as exc:
        result={"result":"FAIL_CLOSED","reason":str(exc)}
        status=1
    payload=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    print(payload)
    return status

if __name__=="__main__":
    raise SystemExit(main())
