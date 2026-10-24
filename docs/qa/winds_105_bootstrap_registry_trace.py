#!/usr/bin/env python3
"""Exact Wind 1.0.5 compiled clinit/BootstrapMethods supplier edges, clean-room.

Bounded five-instruction stack provenance establishes a compiled registration
site, not that an effect fires, dispatches, or admits a perk mutation.
No provider instructions, class files, bytecode or JAR published.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

import winds_105_spell_metadata as binary
import winds_105_effect_registry_dispatch as stage
import winds_105_registry_dispatch_contract as evidence

TARGETS = {
    "ACROBATICS": {"key": "aeropic", "supplier_method": "lambda$static$0",
                  "effect": "net/raptorzizi/wind_spellbooks/effect/AeropicEffect"},
    "TAILWIND": {"key": "tailwind", "supplier_method": "lambda$static$1",
                 "effect": "net/raptorzizi/wind_spellbooks/effect/TailwindEffect"},
}
INSTR = re.compile(r"^\s*(\d+):\s+([a-z][\w]*)\b(.*)$")
BOOT_ENTRY = re.compile(r"^\s*(\d+):\s+#\d+\s+(REF_invokeStatic)\s+(\S+)")
BOOT_ARGUMENT = re.compile(r"^\s+#\d+\s+REF_invokeStatic\s+(\S+)")
BOOT_SITE = re.compile(r"InvokeDynamic\s+#(\d+):get:\(\)Ljava/util/function/Supplier;")
STRING = re.compile(r"^String\s+(\S+)$")
FIELD = re.compile(r"^Field\s+(\S+)$")
CALL = re.compile(r"^(?:Method|InterfaceMethod)\s+(\S+)$")
OWNER = "net/raptorzizi/wind_spellbooks/registries/ModMobEffectRegistry"
REGISTRY_REGISTER = (
    "net/neoforged/neoforge/registries/DeferredRegister.register:"
    "(Ljava/lang/String;Ljava/util/function/Supplier;)"
    "Lnet/neoforged/neoforge/registries/DeferredHolder;"
)

class TraceError(ValueError):
    pass

def method_instr(text: str) -> list[tuple[int, str, str]]:
    start = text.find("\n  static {};\n")
    if start < 0:
        raise TraceError("no single visible static initializer")
    after = text[start+len("\n  static {};\n"):].splitlines()
    found_code = False
    instructions = []
    for line in after:
        if line.strip() == "Code:":
            found_code = True
            continue
        if not found_code:
            continue
        if line.strip() == "}" or (line.startswith("  ") and not line.startswith("    ") and "(" in line):
            break
        m = INSTR.match(line)
        if m:
            offset, opcode, tail = m.groups()
            comment = tail.split("//",1)[1].strip() if "//" in tail else ""
            instructions.append((int(offset), opcode, comment))
    if not instructions or len(instructions)>400:
        raise TraceError("unbounded or missing clinit instructions")
    offsets=[o for o,_,_ in instructions]
    if offsets != sorted(set(offsets)):
        raise TraceError("duplicate or disordered offsets")
    return instructions

def bootstrap_invokers(text: str) -> dict[int,str]:
    """Resolve javap BootstrapMethods *method arguments*, not metafactory handle.

    The top-level bootstrap handle is LambdaMetafactory.metafactory. The
    implementation target of the Supplier is a REF_invokeStatic argument.
    """
    start=text.find("\nBootstrapMethods:\n")
    if start<0:
        raise TraceError("no BootstrapMethods attribute")
    tail=text[start+len("\nBootstrapMethods:\n"):].splitlines()
    entries={}
    current=None
    for line in tail:
        if line and not line.startswith(" ") and line.endswith(":"):
            break
        match=BOOT_ENTRY.match(line)
        if match:
            index,kind,metafactory=match.groups()
            current=int(index)
            if current in entries:
                raise TraceError("duplicate bootstrap index")
            if (kind!="REF_invokeStatic"
                or not metafactory.startswith("java/lang/invoke/LambdaMetafactory.metafactory:")):
                raise TraceError("unrecognized bootstrap metafactory")
            entries[current]=[]
            continue
        argument=BOOT_ARGUMENT.match(line)
        if argument and current is not None:
            target=argument.group(1)
            if target.startswith(OWNER+".lambda$static$"):
                entries[current].append(target)
    if not entries or len(entries)>128:
        raise TraceError("missing or unbounded bootstrap handles")
    targets={}
    for index,candidates in entries.items():
        if len(candidates)!=1:
            raise TraceError("ambiguous or absent Supplier method-handle argument")
        targets[index]=candidates[0]
    return targets

def trace(text: str, factory_methods: dict[str,dict]) -> dict:
    instructions=method_instr(text)
    boot=bootstrap_invokers(text)
    edges={}
    for field,required in TARGETS.items():
        sites=[i for i,(off,op,c) in enumerate(instructions)
               if op in {"ldc","ldc_w"} and STRING.match(c)
               and STRING.match(c).group(1)==required["key"]]
        if len(sites)!=1:
            raise TraceError("wrong compiled registration key population: "+field)
        i=sites[0]
        if i<1 or i+3>=len(instructions):
            raise TraceError("incomplete bounded stack window: "+field)
        receiver, key, invoked, registered, stored = instructions[i-1:i+4]
        # The exact instruction window is simple stack dataflow:
        # DeferredRegister receiver, String key, Supplier, register call, holder store.
        if receiver[1]!="getstatic" or not (m:=FIELD.match(receiver[2])):
            raise TraceError("missing registry receiver: "+field)
        reg_receiver=m.group(1)
        if not reg_receiver.endswith(":Lnet/neoforged/neoforge/registries/DeferredRegister;"):
            raise TraceError("unverified receiver type: "+field)
        if invoked[1]!="invokedynamic" or not (n:=BOOT_SITE.search(invoked[2])):
            raise TraceError("supplier callsite is not a recognized Supplier: "+field)
        boot_index=int(n.group(1))
        handle=boot.get(boot_index,"")
        if OWNER+"."+required["supplier_method"]+":" not in handle:
            raise TraceError("bootstrap target is not the declared factory: "+field)
        if registered[1] not in {"invokevirtual","invokeinterface"} or not (
            c:=CALL.match(registered[2])) or c.group(1)!=REGISTRY_REGISTER:
            raise TraceError("no exact DeferredRegister register call: "+field)
        if stored[1]!="putstatic" or not (v:=FIELD.match(stored[2])):
            raise TraceError("no deferred holder store: "+field)
        holder=v.group(1)
        if not (holder.startswith(field+":") or holder.startswith(OWNER+"."+field+":")):
            raise TraceError("holder and registration key disconnected: "+field)
        if not holder.endswith(":Lnet/neoforged/neoforge/registries/DeferredHolder;"):
            raise TraceError("holder has unexpected binary type: "+field)
        candidates=[v for decl,v in factory_methods.items()
                    if required["supplier_method"]+"(" in decl]
        if len(candidates)!=1 or required["effect"] not in candidates[0]["effect_constructor_candidates"]:
            raise TraceError("supplier factory has no exact effect construction: "+field)
        edges[field]={
            "registration_key": required["key"],
            "holder_field": field,
            "receiver_binary_type": "net.neoforged.neoforge.registries.DeferredRegister",
            "registration_call": REGISTRY_REGISTER,
            "supplier_bootstrap_site":boot_index,
            "supplier_target": required["supplier_method"],
            "factory_constructs_class":required["effect"].replace("/","."),
            "compiled_supplier_to_holder": "PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP",
            "runtime_instance_registration":"NOT_TESTED",
            "client_gameplay_effect":"NOT_TESTED",
            "safe_mutating_hook":"NOT_PROVEN",
        }
    if edges["ACROBATICS"]["supplier_bootstrap_site"]==edges["TAILWIND"]["supplier_bootstrap_site"]:
        raise TraceError("supplier sites alias unexpectedly")
    return {"result":"PASS_COMPILED_REGISTRATION_EDGES",
            "sha1":binary.EXPECTED_SHA1,
            "provider":"wind_spellbooks","release":"1.0.5",
            "scope":"EXACT_JAR_COMPILED_CLINIT_BOOTSTRAP_AND_FACTORY_ONLY",
            "registration_edges":edges,
            "runtime_cast_effect":"NOT_TESTED",
            "limits":["no runtime holder resolution, world client or physical QA",
                      "no host virtual receiver/dispatch resolution",
                      "no damage, jump strength, movement magnitude or perk hook approval"]}

def audit(jar:Path) -> dict:
    prior=stage.audit(jar)
    evidence.validate(prior)
    try:
        proc=subprocess.run(
            ["javap","-v","-c","-p","-classpath",str(jar),stage.REGISTRY],
            capture_output=True,text=True,timeout=30,check=True)
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        raise TraceError("exact registry javap -v failed") from exc
    result=trace(proc.stdout,prior["registry"]["candidate_methods"])
    return result

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        result=audit(args.jar)
        code=0
    except (TraceError,binary.AuditError,stage.AuditError,evidence.ContractError,
            OSError,ValueError,KeyError,TypeError) as exc:
        result={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    payload=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
