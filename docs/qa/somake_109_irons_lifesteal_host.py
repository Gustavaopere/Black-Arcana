#!/usr/bin/env python3
"""Read-only exact Iron's 3.16.3 runtime JAR lifesteal symbol discovery.

Clean-room: derived class/method identities and symbolic JVM references only;
no binary, source, method body, javap dump, or upstream assets are persisted.
A static runtime class scan is not proof of provider-loaded gameplay.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from somake_109_perk_method_probe import GateError
from somake_109_radius_irons_contract import sections, opcode_rows

MAX_ARCHIVE_CLASSES=18000
MAX_SCAN_BYTES=80_000_000
MAX_CLASS_BYTES=500_000
MAX_CANDIDATES=100
MAX_JAVAP_BYTES=1_500_000
RUNTIME_FILENAME="irons_spellbooks-1.21.1-3.16.3.jar"
RUNTIME_SHA256="13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73" # official CurseForge File 8680204, Java 21 run 39619044180
OWNER="io.redspace.ironsspellbooks.damage.SpellDamageSource"
APPLY="io.redspace.ironsspellbooks.damage.DamageSources"


def find_lifesteal_class_names(entries):
    """Discover marker owners without interpreting JVM method execution."""
    seen=set()
    candidates=[]
    count=0
    total=0
    for name,contents in entries:
        count+=1
        if count>MAX_ARCHIVE_CLASSES:
            raise GateError("too many class members to inspect safely")
        if not isinstance(name,str) or not isinstance(contents,bytes):
            raise GateError("invalid class entry")
        if (not name.endswith(".class") or len(name)>300
                or ".." in name or not re.fullmatch(r"[A-Za-z0-9_/$.-]+",name)):
            raise GateError("unsafe or ambiguous binary class member")
        if name in seen:
            raise GateError("duplicate class member")
        seen.add(name)
        total+=len(contents)
        if len(contents)>MAX_CLASS_BYTES or total>MAX_SCAN_BYTES:
            raise GateError("unbounded API class scan")
        lower=contents.lower()
        if b"lifesteal" in lower or b"life_steal" in lower:
            candidates.append(name[:-6].replace("/","."))
            if len(candidates)>MAX_CANDIDATES:
                raise GateError("lifesteal class set exceeds audit budget")
    if not candidates:
        raise GateError("no exact lifesteal bytecode markers; cannot infer absence from API")
    return sorted(candidates)


def get_class_members(jar:Path):
    with zipfile.ZipFile(jar) as archive:
        items=archive.infolist()
        if len(items)>30000 or len({x.filename for x in items})!=len(items):
            raise GateError("invalid API ZIP membership")
        selected=[x for x in items if x.filename.endswith(".class")]
        if not 1<=len(selected)<=MAX_ARCHIVE_CLASSES:
            raise GateError("unexpected API class count")
        if sum(x.file_size for x in selected)>MAX_SCAN_BYTES:
            raise GateError("unbounded API uncompressed classes")
        entries=[]
        for info in selected:
            if info.file_size>MAX_CLASS_BYTES:
                raise GateError("oversized classfile")
            entries.append((info.filename,archive.read(info)))
    return entries


def probe_class(jar:Path,cls:str):
    result=subprocess.run(["javap","-p","-s","-c","-classpath",str(jar.resolve()),cls],
       capture_output=True,text=True,timeout=40,check=False)
    if result.returncode or not 100<len(result.stdout)<MAX_JAVAP_BYTES:
        raise GateError("exact API javap failed for "+cls)
    all_methods=sections(result.stdout)
    matches=[]
    for name,desc,body in all_methods:
        if len(matches)>35:
            raise GateError("too many referenced methods")
        if ("lifesteal" not in name.lower() and
              not any("lifesteal" in line.lower() or "life_steal" in line.lower() for line in body)):
            continue
        rows=opcode_rows(body)
        symbol_hits=[]
        context=[]
        for i,(_,op,_,comment) in enumerate(rows):
            if not (op.startswith("invoke") or op in ("getfield","getstatic","putfield","putstatic")):
                continue
            if not comment:
                continue
            if "lifesteal" in comment.lower() or "life_steal" in comment.lower():
                symbol_hits.append({"instruction_index":i,"opcode":op,
                                    "reference":comment[:220]})
            elif any(x in comment.lower() for x in
                     ("livingentity.heal:",".heal:","sethealth:","hasposthiteffects:",
                      "damagesources.applydamage:","getentity:")):
                context.append({"instruction_index":i,"opcode":op,
                                "reference":comment[:190]})
        if symbol_hits or "lifesteal" in name.lower():
            row={"method":name,"descriptor":desc,"instruction_count":len(rows),
                 "lifesteal_symbol_calls":symbol_hits[:20],
                 "related_method_calls":context[:14],
                 "limitation":"Symbol references and method identity only; no call-stack/branch/damage/cure proof."}
            if cls==APPLY and name=="postHitEffects":
                row["bounded_host_diagnostic"]={
                  "all_invoke_symbols":[{"index":i,"opcode":op,"reference":c[:220]}
                      for i,(_,op,_,c) in enumerate(rows)
                      if op.startswith("invoke") and c][:32],
                  "opcode_kinds_24_to_42":[op for _,op,_,_ in rows[24:43]],
                  "bounded_local_slot_facts":[{
                      "index":i,"opcode":rows[i][1],"local_operand":rows[i][2][:16]
                   } for i in (14,17,18,21,22,23,25,26,27,28,33,34,36)
                   if i<len(rows)],
                  "conditional_opcode_indices":[{"index":i,"opcode":op,
                                                  "target_program_counter":arg}
                      for i,(_,op,arg,_) in enumerate(rows)
                      if op.startswith("if")][:18],
                  "scope":"Diagnostic opcode kinds and typed callsites only; no verbatim method body."
                }
            matches.append(row)
    # A class marker need not be a callsite; discovery is deliberately conservative.
    return {"class":cls,"methods":matches[:35],
            "method_count":len(all_methods)}


def inspect(jar:Path):
    jar=Path(jar)
    if jar.is_symlink() or not jar.is_file() or jar.name!=RUNTIME_FILENAME:
        raise GateError("wrong official Iron's 3.16.3 runtime filename")
    if not 5_000_000<jar.stat().st_size<30_000_000:
        raise GateError("unexpected runtime size")
    digest=hashlib.sha256(jar.read_bytes()).hexdigest()
    if RUNTIME_SHA256 is not None and digest!=RUNTIME_SHA256:
        raise GateError("runtime SHA256 mismatch")
    with zipfile.ZipFile(jar) as archive:
        modmeta=archive.read("META-INF/neoforge.mods.toml")
        if len(modmeta)>250000 or not re.search(rb"\bmodId\s*=\s*['\"]irons_spellbooks['\"]",modmeta):
            raise GateError("Iron's runtime modId mismatch")
    entries=get_class_members(jar)
    candidates=find_lifesteal_class_names(entries)
    available={name[:-6].replace("/",".") for name,_ in entries}
    if OWNER not in available or APPLY not in available:
        raise GateError("expected Iron's API classes absent")
    focus=[name[:-6].replace("/",".") for name,data in entries
           if b"getlifestealpercent" in data.lower() or b"hasposthiteffects" in data.lower()]
    inspect_names=sorted(set(focus)|{OWNER,APPLY})
    if len(inspect_names)>MAX_CANDIDATES+2:
        raise GateError("symbol proof not bounded")
    results=[probe_class(jar,cls) for cls in inspect_names]
    if hashlib.sha256(jar.read_bytes()).hexdigest()!=digest:
        raise GateError("Iron's runtime mutated during inspection")
    return {
       "status":"PASS_SHA_EXACT_IRONS_3163_RUNTIME_LIFESTEAL_SYMBOL_SCOUT",
       "version":"1.21.1-3.16.3",
       "runtime_sha256":digest,
       "lifesteal_marked_class_count":len(candidates),
       "lifesteal_marked_classes":candidates,
       "runtime_class_count":len(entries),
       "method_symbol_surveys":results,
       "scope":"Runtime JAR static discovery on publisher file 8680204; SHA256 verified against pinned CurseForge file 8680204. No inference of actual healed life or perk mutator."
    }

def certify_post_hit_lifesteal(rows):
    """Fail closed until host healer and float operands are proven."""
    raise GateError("host post-hit lifesteal JVM stack provenance not certified")



def main():
    p=argparse.ArgumentParser()
    p.add_argument("--irons-runtime",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    report=inspect(a.irons_runtime)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("IRONS_3163_LIFESTEAL_SCOUT",report["status"],report["runtime_sha256"])
    print("IRONS_3163_LIFESTEAL_CLASSES",report["lifesteal_marked_classes"])
    print("IRONS_3163_LIFESTEAL_METHODS",json.dumps(report["method_symbol_surveys"],sort_keys=True))
if __name__=="__main__":
    main()
