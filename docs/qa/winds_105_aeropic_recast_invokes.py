#!/usr/bin/env python3
"""SHA-verified AeropicEffect -> Iron's AbstractSpell recast opcode audit.

Method-level clean-room provenance only. Invocation opcode/owner can be
observed; the object on the operand stack and runtime dispatch are NOT proven.
No bytecode/JAR or source is emitted.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import winds_105_spell_metadata as physical
import winds_105_effect_contract as effect_contract
import winds_105_effect_boundaries as effects
import winds_105_registry_dispatch_contract as abi_contract
import winds_105_effect_registry_dispatch as abi

EFFECT = "net.raptorzizi.wind_spellbooks.effect.AeropicEffect"
RECAST = (
    "io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:"
    "(ILnet/minecraft/world/entity/LivingEntity;)I"
)
EXPECTED_CALLER_METHODS = ("applyEffectTick", "onEffectAdded")
RECAST_RELATED = (
    "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.",
    "io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.",
)
DECL = re.compile(r"^  (?:public|protected|private) [^\n]*\([^;]*\);$")
INS = re.compile(r"^\s*\d+:\s+(invokevirtual|invokeinterface|invokespecial|invokestatic)\b.*?\s+//\s+(?:Method|InterfaceMethod)\s+(\S+)")

class EvidenceError(ValueError):
    pass

def scan(javap: str) -> dict:
    """Report exact symbolic invocations from methods; never infer receiver."""
    method = None
    matches: dict[str, dict] = {}
    declarations: set[str] = set()
    for line in javap.splitlines():
        if DECL.match(line):
            declaration = line.strip()
            method = declaration.split("(",1)[0].rsplit(" ",1)[-1]
            if method in EXPECTED_CALLER_METHODS:
                if method in declarations:
                    raise EvidenceError("duplicate/overloaded recast caller " + method)
                declarations.add(method)
                matches[method] = {
                    "method_declaration": declaration,
                    "recast_opcodes": [],
                    "recast_related_calls_same_method": set(),
                }
            continue
        if line.startswith("  static {};"):
            method=None
            continue
        m = INS.match(line)
        if m is None or method not in matches:
            continue
        opcode, ref = m.groups()
        if ref == RECAST:
            matches[method]["recast_opcodes"].append(opcode)
        elif ref.startswith(RECAST_RELATED):
            matches[method]["recast_related_calls_same_method"].add(ref)
    if declarations != set(EXPECTED_CALLER_METHODS):
        raise EvidenceError("missing exact Aeropic effect caller method")
    result={}
    for name in EXPECTED_CALLER_METHODS:
        x=matches[name]
        if len(x["recast_opcodes"]) != 1:
            raise EvidenceError(f"expected one explicit AbstractSpell recast invoke in {name}")
        result[name]={
            "method_declaration":x["method_declaration"],
            "invocation_opcode":x["recast_opcodes"][0],
            "invoked_owner":"io.redspace.ironsspellbooks.api.spells.AbstractSpell",
            "invoked_name":"getRecastCount",
            "invoked_descriptor":"(ILnet/minecraft/world/entity/LivingEntity;)I",
            "related_call_symbols_in_same_method":sorted(x["recast_related_calls_same_method"]),
            "dynamic_receiver_type":"NOT_PROVEN",
            "virtual_target_resolution":"NOT_PROVEN",
            "return_value_consumer":"NOT_PROVEN",
            "execution_in_runtime":"NOT_TESTED",
        }
    return result

def verify(sha: str, calls:dict) -> dict:
    if sha != physical.EXPECTED_SHA1 or set(calls)!=set(EXPECTED_CALLER_METHODS):
        raise EvidenceError("non-frozen provider identity or call population")
    return {
        "result":"PASS_EXACT_AEROPIC_RECAST_CALLSITE_OPCODE_INVENTORY",
        "sha1":sha,"release":"1.0.5","provider":"wind_spellbooks",
        "effect_class":EFFECT,
        "recast_owner_ref":RECAST,
        "call_sites":calls,
        "call_site_total":sum(1 for _ in calls),
        "host_release":"3.16.3_FROM_INSTALLED_MODLIST_NOT_AUDITED_HERE",
        "host_JAR_abi":"NOT_VERIFIED",
        "runtime_override_dispatch":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN",
        "limits":[
            "invoke owner and opcode are method-level binary facts, not the stack receiver",
            "matched local AeropicSpell ABI does not establish runtime receiver",
            "no host JAR inspected, no runtime effect, no integration hook or physical QA",
        ],
    }

def audit(jar:Path) -> dict:
    # Reuse existing frozen identity + symbol/ABI guards before narrowing scope.
    record=effects.audit(jar)
    effect_contract.validate(record)
    signature=abi.audit(jar)
    abi_contract.validate(signature)
    try:
        p=subprocess.run(["javap","-c","-p","-classpath",str(jar),EFFECT],
                         capture_output=True,text=True,check=True,timeout=25)
    except (OSError,subprocess.TimeoutExpired,subprocess.CalledProcessError) as exc:
        raise EvidenceError("javap exact Aeropic effect inspection failed") from exc
    return verify(record["sha1"],scan(p.stdout))

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        data=audit(args.jar)
        code=0
    except (EvidenceError,physical.AuditError,effects.EvidenceError,
            abi.AuditError,effect_contract.ContractError,
            abi_contract.ContractError,OSError,ValueError,TypeError,KeyError) as exc:
        data={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    result=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding="utf-8")
    print(result)
    return code

if __name__=="__main__":
    raise SystemExit(main())
