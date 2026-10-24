#!/usr/bin/env python3
"""SHA-frozen clean-room boundary evidence for Wind 1.0.5 effect registry/dispatch.

Exports symbolic declarations, references and construction candidates only.
No source reproduction, class instructions, receiver proof or gameplay claims.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

import winds_105_spell_metadata as binary
import winds_105_cross_class_getter_calls as cross

REGISTRY = "net.raptorzizi.wind_spellbooks.registries.ModMobEffectRegistry"
CLASSES = {
    "aeropic_spell": binary.BASE + "AeropicSpell",
    "aeropic_effect": "net.raptorzizi.wind_spellbooks.effect.AeropicEffect",
    "tailwind_spell": binary.BASE + "TailwindSpell",
    "tailwind_effect": "net.raptorzizi.wind_spellbooks.effect.TailwindEffect",
    "registry": REGISTRY,
}
GET_RECAST = "(ILnet/minecraft/world/entity/LivingEntity;)I"
DECLARE = re.compile(r"^  (?:.+\([^;]*\)(?: throws .+)?;|static \{\};)$")
DESCRIPTOR = re.compile(r"^\s+descriptor:\s+(\S+)$")
HEADER = re.compile(r"^(?:public|protected|private|abstract|final|\s)+\s*(?:class|interface)\s+\S+.*\{$")
OP = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b(.*)$")
STRING = re.compile(r"^String (.+)$")
NEW_CLASS = re.compile(r"^class ([\w/$]+)$")
INVOKE = re.compile(r"^(?:Method|InterfaceMethod)\s+(\S+)$")
FIELD = re.compile(r"^Field (\S+)$")

class AuditError(ValueError):
    pass

def declaration_inventory(text: str) -> dict:
    lines = text.splitlines()
    headers = [line.strip() for line in lines if HEADER.match(line)]
    if len(headers) != 1:
        raise AuditError("missing or ambiguous class header")
    items = []
    for idx, line in enumerate(lines):
        if not DECLARE.match(line):
            continue
        declaration = line.strip()
        next_lines = lines[idx+1:idx+5]
        descriptor = next((m.group(1) for s in next_lines
                           if (m := DESCRIPTOR.match(s))), None)
        if descriptor is not None:
            items.append({"declaration": declaration, "descriptor": descriptor})
    if not items:
        raise AuditError("class has no methods or constructors with descriptors")
    parents = re.findall(r"\bextends\s+([\w.$]+)", headers[0])
    return {
        "class_declaration": headers[0],
        "immediate_superclass_token": parents[0] if parents else None,
        "recast_declarations": [row for row in items
                               if " getRecastCount(" in row["declaration"]],
        "method_signature_count": len(items),
        "semantics": "JAVAP_DECLARATIONS_ONLY",
    }

def registry_symbols(javap: str) -> dict:
    """Keep symbol names and method provenance; no operand-stack inference."""
    current = None
    inventory = {}
    for line in javap.splitlines():
        if DECLARE.match(line):
            current = line.strip()
            inventory.setdefault(current, {
                "relevant_string_constants": set(),
                "effect_constructor_candidates": set(),
                "invokedynamic_site_count": 0,
                "method_invokes": set(),
                "field_references": set(),
            })
            continue
        if current is None:
            continue
        m = OP.match(line)
        if not m:
            continue
        op, rest = m.groups()
        if op == "invokedynamic":
            inventory[current]["invokedynamic_site_count"] += 1
        if "// " not in rest:
            continue
        comment = rest.split("// ", 1)[1].strip()
        if op in {"ldc", "ldc_w"} and (s := STRING.match(comment)):
            if any(k in s.group(1).lower() for k in ("tailwind", "acrobat", "aeropic")):
                inventory[current]["relevant_string_constants"].add(s.group(1))
        if op == "new" and (s := NEW_CLASS.match(comment)):
            if any(k in s.group(1).lower() for k in ("tailwind", "acrobat", "aeropic")):
                inventory[current]["effect_constructor_candidates"].add(s.group(1))
        if op.startswith("invoke") and (s := INVOKE.match(comment)):
            if any(k in s.group(1).lower() for k in ("tailwind", "acrobat", "aeropic", "register")):
                inventory[current]["method_invokes"].add(s.group(1))
        if op in {"putstatic", "getstatic", "putfield", "getfield"} and (s := FIELD.match(comment)):
            if any(k in s.group(1).lower() for k in ("tailwind", "acrobat", "aeropic")):
                inventory[current]["field_references"].add(s.group(1))
    evidence = {}
    for decl, row in inventory.items():
        d = {k:(sorted(v) if isinstance(v,set) else v) for k,v in row.items()}
        if any(d[k] for k in ("relevant_string_constants",
                             "effect_constructor_candidates",
                             "method_invokes", "field_references")):
            evidence[decl] = d
    return {
        "candidate_methods": evidence,
        "registration_field_to_instance_binding": "NOT_PROVEN",
        "invokedynamic_bootstrap_resolution": "NOT_PROVEN",
        "semantics": "SYMBOLIC_JVM_REGISTRY_SITES_ONLY",
    }

def summarize(declarations: dict, registry_bytecode: str, effect_invoked_symbols: list[str]) -> dict:
    if set(declarations) != set(CLASSES):
        raise AuditError("incomplete class declaration set")
    aeropic = declarations["aeropic_spell"]
    rows = aeropic["recast_declarations"]
    if len(rows) != 1 or rows[0]["descriptor"] != GET_RECAST:
        raise AuditError("Aeropic override descriptor mismatch or absent")
    base = "io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:"+GET_RECAST
    if base not in effect_invoked_symbols:
        raise AuditError("Aeropic effect does not reference the known base method")
    reg = registry_symbols(registry_bytecode)
    # Do not pretend that 'new Effect' in a method proves the factory/field wiring.
    return {
        "result": "PASS_SHA_EXACT_REGISTRY_AND_DISPATCH_SYMBOLS",
        "sha1": binary.EXPECTED_SHA1,
        "provider": "wind_spellbooks",
        "release": "1.0.5",
        "class_declarations": declarations,
        "aeropic_virtual_recast": {
            "spell_declares_method_descriptor": GET_RECAST,
            "effect_invokes_owner": "io.redspace.ironsspellbooks.api.spells.AbstractSpell",
            "effect_invokes_method_descriptor": GET_RECAST,
            "signature_compatible": True,
            "runtime_dispatch_to_spell_override": "NOT_PROVEN",
            "receiver_instance": "NOT_PROVEN",
            "host_abstractspell_implementation": "NOT_INSPECTED",
        },
        "registry": reg,
        "limits": [
            "matched descriptors are static compatibility, not dispatch or receiver proof",
            "class header parents require exact host class hierarchy inspection",
            "registry names/new expressions without stack+bootstrap trace do not prove field factory binding",
            "no gameplay, client QA, perk hook, cast or recast ownership change",
        ],
    }

def audit(jar: Path) -> dict:
    proof = binary.audit(jar)
    classes = cross.class_names(jar)
    if not set(CLASSES.values()).issubset(classes):
        raise AuditError("missing exact named provider classes")
    if len(classes) != 64 or proof["sha1"] != binary.EXPECTED_SHA1:
        raise AuditError("frozen JAR class population or SHA drift")
    declarations = {}
    results = {}
    for short, fqcn in CLASSES.items():
        for flags, label in [(("-p","-s"),"signature"),(("-c","-p"),"bytecode")]:
            try:
                run = subprocess.run(["javap",*flags,"-classpath",str(jar),fqcn],
                    text=True,capture_output=True,timeout=20,check=True)
            except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
                raise AuditError("javap failed for "+short+" "+label) from exc
            results[(short,label)] = run.stdout
        declarations[short] = declaration_inventory(results[(short,"signature")])
    effect_methods = binary.summarize_disassembly(results[("aeropic_effect","bytecode")])
    symbols = sorted({symbol for row in effect_methods.values()
                      for symbol in row["invoked_symbols"]})
    report = summarize(declarations, results[("registry","bytecode")], symbols)
    report["classes_in_provider"] = len(classes)
    return report

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=audit(args.jar)
        result=0
    except (AuditError,binary.AuditError,cross.AuditError,
            ValueError,KeyError,OSError,TypeError) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        result=1
    data=json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    print(data)
    return result

if __name__=="__main__":
    raise SystemExit(main())
