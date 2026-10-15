#!/usr/bin/env python3
"""SHA-gated static proof of compiled Artifacts owner→factory→Relics ability identity.

Reads the official installed-hash JAR with Java21 javap. Does not assert that
Mixin has successfully injected against the installed Artifacts/Relics runtime.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess

import reliquified_artifacts_108_binary_audit as base

AuditError = base.AuditError

def load_source_owner_classes(inventory: str) -> dict[str,str]:
    triples, by_class, owners = base.expected_inventory(inventory)
    source = {}
    for owner, ability, clazz in triples:
        if owner in source and source[owner] != clazz:
            raise AuditError("catalog maps one artifact owner to multiple implementation classes")
        source[owner] = clazz
    if len(source) != 48 or len(set(source.values())) != 47 or len(owners) != 48:
        raise AuditError("48-owner/47-class source mapping has drifted")
    return source

def decode_instructions(code: str) -> list[tuple[int,str,str,str]]:
    found=[]
    for m in re.finditer(r'^\s*(\d+):\s+([a-z][\w]*)\b([^\n]*)$',code,re.M):
        raw=m.group(3)
        operand=raw.split('//',1)[0].strip()
        comment=raw.split('//',1)[1].strip() if '//' in raw else ''
        found.append((int(m.group(1)),m.group(2),operand,comment))
    return found

def code_of_method(text: str, name: str) -> str:
    header=re.search(r'^  (?:private|public|protected|static) [^\n]*\b'+re.escape(name)+r'\([^\n]*\);$',text,re.M)
    if not header: raise AuditError("compiled Mixin method absent: "+name)
    after=text[header.end():]
    start=re.search(r'^    Code:$',after,re.M)
    if not start: raise AuditError("compiled method Code absent: "+name)
    code=after[start.end():]
    end=re.search(r'^      (?:LineNumberTable|LocalVariableTable|StackMapTable):',code,re.M)
    if not end: raise AuditError("compiled method Code footer unavailable: "+name)
    return code[:end.start()]

def int_opcode(op: str, operand: str, comment: str) -> int:
    if op == 'iconst_m1': return -1
    if re.fullmatch(r'iconst_[0-5]',op): return int(op[-1])
    if op in ('bipush','sipush') and re.fullmatch(r'-?\d+',operand): return int(operand)
    if op in ('ldc','ldc_w') and re.fullmatch(r'int -?\d+',comment): return int(comment[4:])
    raise AuditError("switch discriminator assignment not a direct integer constant")

def bootstrap_ctors(text: str) -> dict[int,str]:
    match=re.search(r'^BootstrapMethods:\s*$',text,re.M)
    if not match: raise AuditError("LambdaMetafactory BootstrapMethods absent")
    out={}
    number=None
    metafactory=False
    for line in text[match.end():].splitlines():
        entry=re.match(r'^  (\d+):\s+(.+)$',line)
        if entry:
            number=int(entry.group(1))
            metafactory='LambdaMetafactory.metafactory' in entry.group(2)
            continue
        if line.startswith(('InnerClasses:','NestMembers:')):
            break
        if number is not None and 'REF_newInvokeSpecial ' in line:
            if not metafactory: raise AuditError("constructor handle outside LambdaMetafactory")
            matched=re.search(r'REF_newInvokeSpecial\s+([\w/$]+)\."<init>":\(\)V',line)
            if not matched: raise AuditError("unexpected compiled factory method handle signature")
            if number in out: raise AuditError("ambiguous LambdaMetafactory constructor")
            out[number]=matched.group(1)
    return out

def switch_mapping(text: str, name: str, constructors: dict[int,str],
                   expected_owners: set[str] | None = None) -> dict[str,str]:
    code=code_of_method(text,name)
    ins=decode_instructions(code)
    by_offset={off:i for i,(off,_,_,_) in enumerate(ins)}
    if len(by_offset)!=len(ins): raise AuditError("duplicate compiled offsets in "+name)
    assignments={}
    for i,(offset,op,operand,comment) in enumerate(ins):
        if op not in ('ldc','ldc_w') or not comment.startswith('String '): continue
        owner=comment[7:]
        if not re.fullmatch(r'[a-z][a-z0-9_]*',owner) or i+4>=len(ins): continue
        equal,branch,push,store=ins[i+1:i+5]
        if not (equal[1]=='invokevirtual' and 'java/lang/String.equals:' in equal[3]
                and branch[1]=='ifeq' and store[1].startswith('istore')):
            continue
        if owner in assignments: raise AuditError("duplicate owner discriminator: "+owner)
        assignments[owner]=int_opcode(push[1],push[2],push[3])
    if expected_owners is not None and set(assignments)!=set(expected_owners):
        raise AuditError("compiled case owner names differ from pinned inventory")
    # Javac sometimes emits a hashcode tableswitch before its case-index dispatch.
    # Select the switch whose labels exactly match String.equals discriminants.
    matches=list(re.finditer(r'^\s*\d+:\s+tableswitch\s+\{[^\n]*\n(.*?)^\s*\}',code,re.M|re.S))
    if not matches: raise AuditError('no compiled tableswitch: '+name)
    candidates=[]
    for match in matches:
        table={}
        default=None
        for line in match.group(1).splitlines():
            label=re.match(r'^\s*(default|-?\d+):\s*(\d+)\s*$',line)
            if not label: raise AuditError('unrecognized compiled switch entry')
            target=int(label.group(2))
            if label.group(1)=='default':
                if default is not None: raise AuditError('duplicate compiled default')
                default=target
            else:
                n=int(label.group(1))
                if n in table: raise AuditError('duplicate compiled switch label')
                table[n]=target
        if default is not None and set(table)==set(assignments.values()):
            candidates.append((table,default))
    if len(candidates)!=1: raise AuditError('ambiguous compiled case-index dispatch')
    table,default=candidates[0]
    if default not in by_offset:
        raise AuditError("default case not aligned with bytecode")
    # The Java language fallback must retain the original Supplier/Consumer.
    tail=[]
    for step in ins[by_offset[default]:]:
        tail.append(step)
        if step[1] in ('goto','goto_w','areturn','return','athrow'):break
    fallback = 'wearableItem:' if name=='redirectWearableItem' else 'register:'
    if (len([x for x in tail if x[1]=='invokestatic' and fallback in x[3]])!=1
            or not any(x[1]=='aload_1' for x in tail)
            or any(x[1]=='invokedynamic' for x in tail)):
        raise AuditError("compiled default fallback does not preserve original provider factory")
    resolved={}
    for owner,label in assignments.items():
        target=table[label]
        if target not in by_offset:
            raise AuditError("compiled case points to non-instruction address: "+owner)
        steps=[]
        for step in ins[by_offset[target]:]:
            steps.append(step)
            if step[1] in ('goto','goto_w','areturn','return','athrow'):break
        dyn=[x for x in steps if x[1]=='invokedynamic']
        calls=[x for x in steps if x[1]=='invokestatic' and 'register:' in x[3]]
        if len(dyn)!=1 or len(calls)!=1 or dyn[0][0]>=calls[0][0]:
            raise AuditError("owner branch lacks single lambda Supplier→register flow: "+owner)
        handle=re.search(r'InvokeDynamic\s+#(\d+):',dyn[0][3])
        if not handle:
            raise AuditError("LambdaMetafactory bootstrap index missing: "+owner)
        ctor=constructors.get(int(handle.group(1)))
        if ctor is None or not ctor.endswith('Item'):
            raise AuditError("compiled bootstrap not an item constructor: "+owner)
        resolved[owner]=re.split(r'[/\$]',ctor)[-1]
    if len(resolved)!=len(assignments):
        raise AuditError("incomplete compiled constructor graph")
    return resolved

def require_exact_owner_classes(actual: dict[str,str], expected: dict[str,str]):
    missing=sorted(set(expected)-set(actual))
    unexpected=sorted(set(actual)-set(expected))
    wrong={key:{"expected":expected[key],"observed":actual[key]}
           for key in sorted(set(expected)&set(actual)) if expected[key]!=actual[key]}
    if missing or unexpected or wrong:
        raise AuditError("compiled artifact owner→class mismatch: "+json.dumps(
            {"missing":missing,"unexpected":unexpected,"wrong":wrong},sort_keys=True))
    return True

def full_compiled_owner_mapping(disassembly: str, expected: dict[str,str]):
    ctors=bootstrap_ctors(disassembly)
    wear=switch_mapping(disassembly,"redirectWearableItem",ctors)
    direct=switch_mapping(disassembly,"redirectRegister",ctors)
    if (set(wear)&set(direct)) or (len(wear),len(direct))!=(45,3):
        raise AuditError("compiled ownership routing is not 45 wearable + 3 direct")
    actual={**wear,**direct}
    require_exact_owner_classes(actual,expected)
    return actual

def run_javap_verbose(jar: Path, classname: str) -> str:
    try:
        result=subprocess.run(["javap","-c","-p","-v","-classpath",str(jar),classname],
                              capture_output=True,text=True,timeout=50,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("compiled Mixin verbose javap unavailable") from exc
    if result.returncode or not 0<len(result.stdout)<5_000_000:
        raise AuditError("compiled Mixin bytecode not available or oversized")
    return result.stdout

def audit_owner_links(jar: Path, inventory: str):
    physical=base.audit(jar,inventory)
    if physical["result"]!="PASS": raise AuditError("base physical SHA+ability proof not PASS")
    expected=load_source_owner_classes(inventory)
    javap=run_javap_verbose(jar.resolve(),base.MIXIN)
    observed=full_compiled_owner_mapping(javap,expected)
    return {
        "result":"PASS",
        "evidence_class":"SHA1_MATCHED_COMPILED_OWNER_SWITCH_TO_LAMBDA_CONSTRUCTOR_TO_ABILITY_TEMPLATES_ONLY",
        "publisher_sha1":base.SHA1,
        "publisher_sha256":physical["sha256"],
        "compiled_owner_to_constructor":dict(sorted(observed.items())),
        "owner_root_count":52,
        "owner_count":48,
        "class_count":47,
        "class_template_roots":physical["class_level_ability_roots"],
        "wearable_redirect_cases":45,
        "direct_redirect_cases":3,
        "deviations":{},
        "not_proven":[
          "Mixin applied to deployed Artifacts 13.2.5 registry",
          "Relics 0.12.8 loaded ability template and ranks",
          "Curios equip/unequip and actual Survival ability proc",
          "XP/cooldowns/owner state, world save/restart and multiplayer",
          "Sophisticated Backpacks pickup idempotence",
          "RPG Skill Tree contractual bridge"
        ]
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--inventory",type=Path,default=base.INVENTORY)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    try:
        payload=audit_owner_links(args.jar,args.inventory.read_text(encoding="utf8"))
        result=0
    except (AuditError,OSError,ValueError,UnicodeError) as exc:
        payload={"result":"FAIL_CLOSED","reason":str(exc)}
        result=1
    encoded=json.dumps(payload,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(encoded,encoding="utf8")
    print(encoded)
    return result

if __name__=="__main__":
    raise SystemExit(main())
