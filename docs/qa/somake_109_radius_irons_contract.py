#!/usr/bin/env python3
"""Read-only exact Somake 1.0.9 radius CFG and Iron's 3.16.3 API contract probe.

Only method signatures, bounded symbolic call references and branch graph metadata
are retained; no third-party method bodies, bytecode or assets are exported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from somake_109_perk_method_probe import FILENAME, SHA1, GateError
from somake_109_cast_refs import DECL, DESC
from somake_109_funeral_bud_probe import isolate_named_methods
from somake_109_numeric_fingerprint import CODE, fingerprint

SOMAKE_CLASS="com.somake.somakespells.spells.blood.FuneralBloomSpell"
IRON_CLASS="io.redspace.ironsspellbooks.api.spells.AbstractSpell"
SOMAKE_GETTER_DESC="(ILnet/minecraft/world/entity/LivingEntity;)F"
POWER_DESC="(ILnet/minecraft/world/entity/Entity;)F"
IRON_VERSION="1.21.1-3.16.3"
IRON_API_FILENAME="irons_spellbooks-1.21.1-3.16.3-api.jar"
MAX_IRON_BYTES=5_000_000
MAX_JAVAP_BYTES=1_500_000
MAX_METHOD_INSTRUCTIONS=300
MAX_METHOD_DECLARATIONS=240

def sections(raw:str)->list[tuple[str,str,list[str]]]:
    if not raw or len(raw)>MAX_JAVAP_BYTES:
        raise GateError("missing or oversized javap output")
    lines=isolate_named_methods(raw).splitlines()
    positions=[n for n,line in enumerate(lines) if DECL.match(line)]
    if not 1<=len(positions)<=MAX_METHOD_DECLARATIONS:
        raise GateError("invalid method declaration count")
    result=[]
    for i,start in enumerate(positions):
        end=positions[i+1] if i+1<len(positions) else len(lines)
        header=lines[start].strip()
        name=header.split("(",1)[0].rsplit(" ",1)[-1]
        descriptors=[m.group(1) for line in lines[start+1:end] if (m:=DESC.match(line))]
        if len(descriptors)!=1:
            raise GateError("ambiguous JVM signature for "+name)
        result.append((name,descriptors[0],lines[start+1:end]))
    return result

def opcode_rows(body:list[str])->list[tuple[int,str,str,str]]:
    rows=[]
    for line in body:
        before,sep,after=line.partition("//")
        m=re.match(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(.+))?",before)
        if m:
            rows.append((int(m.group(1)),m.group(2),(m.group(3) or "").strip(),
                         after.strip() if sep else ""))
    if not 1<=len(rows)<=MAX_METHOD_INSTRUCTIONS:
        raise GateError("missing or oversized opcode cohort")
    offsets=[x[0] for x in rows]
    if len(set(offsets))!=len(offsets) or offsets!=sorted(offsets):
        raise GateError("duplicate or unordered instruction offsets")
    return rows

def radius_cfg(body:list[str])->dict:
    rows=opcode_rows(body)
    offsets={x[0] for x in rows}
    edges=[]
    branches=[]
    for i,(pc,op,operand,comment) in enumerate(rows):
        nextpc=rows[i+1][0] if i+1<len(rows) else None
        if op in ("tableswitch","lookupswitch","jsr","ret","jsr_w","wide"):
            raise GateError("unsupported control-flow opcode "+op)
        if op.startswith("if") or op.startswith("goto"):
            target_word=operand.split(" ",1)[0]
            if not re.fullmatch(r"\d+",target_word):
                raise GateError("unrecognized branch target")
            target=int(target_word)
            if target not in offsets:
                raise GateError("branch target outside bounded method")
            edges.append((pc,target))
            if op.startswith("if"):
                if nextpc is None:raise GateError("conditional without fallthrough")
                edges.append((pc,nextpc))
            branches.append({"opcode":op,"back_edge":target<pc,
                             "has_fallthrough":op.startswith("if")})
        elif op.endswith("return") or op=="athrow":
            pass
        elif nextpc is not None:
            edges.append((pc,nextpc))
        else:
            raise GateError("unterminated last instruction")
    reachable={rows[0][0]};pending=[rows[0][0]]
    graph={}
    for start,end in edges:graph.setdefault(start,[]).append(end)
    while pending:
        pc=pending.pop()
        for dst in graph.get(pc,[]):
            if dst not in reachable:reachable.add(dst);pending.append(dst)
    if any(x[0] not in reachable for x in rows):
        raise GateError("unreachable code needs separate guarded analysis")
    outgoing={}
    for a,b in edges:outgoing[a]=outgoing.get(a,0)+1
    return {
        "instruction_count":len(rows),
        "conditional_branches":sum(x["opcode"].startswith("if") for x in branches),
        "unconditional_branches":len(branches)-sum(x["opcode"].startswith("if") for x in branches),
        "branch_predicates":[x["opcode"] for x in branches if x["opcode"].startswith("if")],
        "back_edges":sum(x["back_edge"] for x in branches),
        "terminal_returns":sum(op.endswith("return") for _,op,_,_ in rows),
        "reachable_instruction_count":len(reachable),
        "control_flow_edges":len(edges),
        "join_points":sum(1 for pc in reachable if sum(b==pc for a,b in edges)>1),
        "method_calls":sorted(set(c for _,op,_,c in rows if op.startswith("invoke") and c)),
        "claim":"CFG topology + JVM symbols only, no formula, branch truth values or game radius."
    }

def callsite_descriptors(body:list[str],member:str)->list[str]:
    result=[]
    for _,opcode,_,comment in opcode_rows(body):
        if opcode.startswith("invoke") and re.search(r"\b"+re.escape(member)+r"\b",comment):
            matched=re.search(re.escape(member)+r":(\([^)]*\)[A-Za-z0-9_/\[;$]+)",comment)
            if not matched:raise GateError("missing callsite method descriptor "+member)
            result.append(matched.group(1))
    return result

def javap(jar:Path,clazz:str)->str:
    p=subprocess.run(["javap","-p","-c","-s","-classpath",str(jar.resolve()),clazz],
                     capture_output=True,text=True,timeout=50,check=False)
    if p.returncode or not p.stdout or len(p.stdout)>MAX_JAVAP_BYTES:
        raise GateError("javap failed for "+clazz)
    return p.stdout

def validate_irons_api(jar:Path)->str:
    if jar.is_symlink() or not jar.is_file() or jar.name!=IRON_API_FILENAME:
        raise GateError("wrong Iron's API artifact filename")
    if not 500<jar.stat().st_size<MAX_IRON_BYTES:
        raise GateError("unexpected Iron's API JAR length")
    with zipfile.ZipFile(jar) as zf:
        names=zf.namelist()
        if len(names)!=len(set(names)):
            raise GateError("duplicate Iron's API archive members")
        if IRON_CLASS.replace(".","/")+".class" not in names:
            raise GateError("expected AbstractSpell API class absent")
    return hashlib.sha256(jar.read_bytes()).hexdigest()

def inspect(somake:Path,iron:Path,expected_api_sha256:str|None)->dict:
    if somake.is_symlink() or not somake.is_file() or somake.name!=FILENAME:
        raise GateError("wrong installed Somake physical file")
    if hashlib.sha1(somake.read_bytes()).hexdigest()!=SHA1:
        raise GateError("installed Somake SHA-1 mismatch")
    with zipfile.ZipFile(somake) as zf:
        names=zf.namelist()
        if len(names)!=len(set(names)):raise GateError("duplicate Somake archive members")
        meta=zf.read("META-INF/neoforge.mods.toml")
        if len(meta)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError("Somake mod ID mismatch")
        if SOMAKE_CLASS.replace(".","/")+".class" not in names:
            raise GateError("Somake spell class missing")
    api_hash=validate_irons_api(iron)
    if expected_api_sha256 is not None and api_hash!=expected_api_sha256:
        raise GateError("Iron's official API SHA-256 mismatch")
    spell=sections(javap(somake,SOMAKE_CLASS))
    matches={}
    for name,desc,body in spell:
        if name in ("getRadius","getImpactDamage"):
            if name in matches:raise GateError("duplicated spell method")
            if desc!=SOMAKE_GETTER_DESC:raise GateError("unexpected Somake spell descriptor")
            matches[name]=(desc,body)
    if set(matches)!={"getRadius","getImpactDamage"}:
        raise GateError("missing required Somake methods")
    radius=radius_cfg(matches["getRadius"][1])
    numeric=fingerprint(matches["getRadius"][1])
    if radius["conditional_branches"]+radius["unconditional_branches"]!=2:
        raise GateError("Somake exact radius branch count changed")
    if not any("SchoolType.getPowerFor:" in c for c in radius["method_calls"]):
        raise GateError("radius no longer references SchoolType.getPowerFor")
    power_calls=callsite_descriptors(matches["getImpactDamage"][1],"getSpellPower")
    if power_calls!=[POWER_DESC]:
        raise GateError("Somake getSpellPower call descriptor mismatch: "+repr(power_calls))
    parsed_api=sections(javap(iron,IRON_CLASS))
    matching=[(name,desc,body) for name,desc,body in parsed_api if name=="getSpellPower" and desc==POWER_DESC]
    if len(matching)!=1:
        raise GateError("exact Iron's public API getSpellPower descriptor unavailable/ambiguous")
    api_refs=sorted(set(c for _,op,_,c in opcode_rows(matching[0][2]) if op.startswith("invoke") and c))
    if len(api_refs)>40:raise GateError("Iron's method reference budget exceeded")
    # A method descriptor match verifies binary linkage, not override/behavior.
    if hashlib.sha1(somake.read_bytes()).hexdigest()!=SHA1 or hashlib.sha256(iron.read_bytes()).hexdigest()!=api_hash:
        raise GateError("JAR changed during inspection")
    return {
        "status":"PASS_STATIC_RADIUS_CFG_AND_IRONS_API_SIGNATURE",
        "somake":{"sha1":SHA1,"fqcn":SOMAKE_CLASS,"radius":{
                    **{k:v for k,v in radius.items() if k!="method_calls"},
                    "symbolic_invocations":radius["method_calls"][:30],
                    "clamp_operand_proofs":numeric["direct_trailing_clamp_literals"]},
                  "impact_damage":{"descriptor":SOMAKE_GETTER_DESC,
                                   "getSpellPower_invocation_descriptors":power_calls}},
        "irons_api":{"version":IRON_VERSION,"sha256":api_hash,"fqcn":IRON_CLASS,
                     "getSpellPower_descriptor":POWER_DESC,"method_calls":api_refs},
        "limits":["Static symbol linkage does not establish active class loading, gameplay values or a safe per-player perk mutator.",
                  "No runtime player, config, Survival, PvP or multiplayer tests.",
                  "JARs, source bodies, disassembly and provider assets are not exported."]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--somake",required=True,type=Path)
    p.add_argument("--irons-api",required=True,type=Path)
    p.add_argument("--expected-api-sha256",default=None)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    data=inspect(a.somake,a.irons_api,a.expected_api_sha256)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    print("SOMAKE_RADIUS_CFG",json.dumps(data["somake"]["radius"],sort_keys=True))
    print("SOMAKE_IRONS_API",json.dumps(data["irons_api"],sort_keys=True))
    print("SOMAKE_RADIUS_GATE",data["status"],data["somake"]["sha1"],data["irons_api"]["sha256"])
if __name__=="__main__":
    main()
