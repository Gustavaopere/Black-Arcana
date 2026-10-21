#!/usr/bin/env python3
"""Monsters & Spellbooks 0.0.16.3 SHA-gated read-only spell registry identity probe.

Clean-room: inspect Java21 compiled bytecode only; no publisher classes/assets
are incorporated. Does not prove registry loaded, config, casting or Survival.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

JAR_NAME = "monstersspellbooks-0.0.16.3.jar"
MOD_ID = "monstersspellbooks"
SHA1 = "b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e"
REGISTER = "net.redreaper.monsterspellbooks.init.ModSpellRegistry"
REGISTRY_BINARY = "net/redreaper/monsterspellbooks/init/ModSpellRegistry"
MAX_BYTES = 20_000_000
INVENTORY = Path("wiki/modpack-catalog/providers/✅-monsters-spellbooks/SPELL-CATALOG.md")
ROW = re.compile(r'^\| (\d+) \| \x60([a-z]+)\x60 \| \x60([A-Z][A-Z0-9_]+)\x60 \| \x60([A-Za-z][A-Za-z0-9]*)\x60 \| \x60registered in ModSpellRegistry\x60 \|$', re.M)
FAMILY_COUNTS = {"blood":5,"ender":12,"evocation":3,"fire":10,"holy":4,"hydro":8,"ice":8,
                 "lightning":14,"nature":7,"necro":25,"technomancy":2}
FIELD = re.compile(r'^\s*public static final java\.util\.function\.Supplier<[^\n]*\s+([A-Z][A-Z0-9_]+);$',re.M)
INSTRUCTION = re.compile(r'^[ \t]*\d+:[ \t]+(\w+)(?:[ \t]+[^/\n]*)?(?:[ \t]*//[ \t]*(.*))?$',re.M)

class AuditError(ValueError): pass

def expected_inventory(text: str) -> dict[str, tuple[str,str]]:
    entries=ROW.findall(text)
    if len(entries)!=98 or sorted(int(v[0]) for v in entries)!=list(range(1,99)):
        raise AuditError("source catalog is not exactly 98 individually indexed spells")
    roster={}
    family=Counter()
    for _,fam,constant,classname in entries:
        if constant in roster: raise AuditError("duplicate source registry constant")
        roster[constant]=(fam,classname)
        family[fam]+=1
    if dict(family)!=FAMILY_COUNTS or len({x[1] for x in roster.values()})!=98:
        raise AuditError("98 source family counts / concrete class identities differ")
    return roster

def instructions(text: str) -> list[tuple[str,str]]:
    return [(x.group(1),(x.group(2) or "").strip()) for x in INSTRUCTION.finditer(text)]

def registry_pairs(disassembly: str) -> dict[str,str]:
    marker="  static {};"
    if disassembly.count(marker)!=1: raise AuditError("registry has no single static initializer")
    declarations,initializer=disassembly.split(marker,1)
    fields=FIELD.findall(declarations)
    if len(fields)!=98 or len(set(fields))!=98:
        raise AuditError("compiled registry must declare 98 unique Supplier fields")
    code=instructions(initializer)
    records={}
    register_calls=0
    for n,(op,comment) in enumerate(code):
        if op!="invokestatic" or "registerSpell:" not in comment: continue
        register_calls+=1
        if n<3 or n+1>=len(code): raise AuditError("registry contains orphaned registration")
        (newop,newcomment),(dupop,_),(ctorop,ctorcomment)=code[n-3:n]
        storeop,storecomment=code[n+1]
        if (newop,dupop,ctorop,storeop)!=("new","dup","invokespecial","putstatic"):
            raise AuditError("non-literal or conditional-looking spell construction")
        clazz=re.search(r'\bclass (net/redreaper/monsterspellbooks/[\w/$]+)$',newcomment)
        field=re.search(r'\bField ([A-Z][A-Z0-9_]*):',storecomment)
        if not clazz or not field or '"<init>"' not in ctorcomment:
            raise AuditError("compiled constructor/field registration ambiguous")
        key=field.group(1)
        if key in records: raise AuditError("duplicate compiled registration field")
        records[key]=clazz.group(1).replace("/",".")
    if register_calls!=98 or set(records)!=set(fields) or len(set(records.values()))!=98:
        raise AuditError("compiled registry field/call/class cardinality mismatch")
    return records

def spell_id(disassembly: str) -> str:
    if "getSpellResource();" not in disassembly:
        raise AuditError("spell class has no getSpellResource method")
    code=instructions(disassembly)
    found=[]
    for n,(op,comment) in enumerate(code):
        if op!="invokestatic" or "ResourceLocation.fromNamespaceAndPath:" not in comment:continue
        if n<2 or n+1>=len(code): continue
        nsop,nscomment=code[n-2]
        pathop,pathcomment=code[n-1]
        storeop,storecomment=code[n+1]
        if not ((nsop in ("ldc","ldc_w") and nscomment=="String monstersspellbooks") or
                (nsop=="getstatic" and "MonstersSpellbooks.MOD_ID:" in nscomment)):
            raise AuditError("spell resource constructor uses unexpected namespace")
        if (pathop not in ("ldc","ldc_w") or not pathcomment.startswith("String ")
            or storeop!="putfield" or not re.search(r'\bField spellId:',storecomment)):
            continue
        root=pathcomment[7:]
        if not re.fullmatch(r"[a-z][a-z0-9_]*",root):
            raise AuditError("malformed compiled spell resource path")
        found.append(root)
    if len(found)!=1:
        raise AuditError("spell class has no unique spellId assignment: "+str(found))
    getter=disassembly.split("getSpellResource();",1)[1].split("\n  public ",1)[0]
    if not re.search(r"getfield\s+[^\n]*// Field spellId:",getter) or not re.search(r"\bareturn\b",getter):
        raise AuditError("compiled spell resource getter does not return the spellId field")
    return found[0]

def run_javap(jar:Path,name:str)->str:
    try:
        res=subprocess.run(["javap","-c","-p","-classpath",str(jar),name],capture_output=True,text=True,check=False,timeout=45)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("Java21 classfile inspector failed or timed out") from exc
    if res.returncode or not 0<len(res.stdout)<4_000_000:
        raise AuditError("javap cannot inspect required published class "+name)
    return res.stdout

def audit(jar:Path, source:str)->dict:
    expected=expected_inventory(source)
    if jar.name!=JAR_NAME or jar.is_symlink() or not jar.is_file():
        raise AuditError("wrong or unsafe installed JAR")
    st=jar.stat()
    if not stat.S_ISREG(st.st_mode) or not 0<st.st_size<MAX_BYTES:raise AuditError("physical JAR bounds invalid")
    before=lambda x:(x.st_dev,x.st_ino,x.st_mtime_ns,x.st_ctime_ns,x.st_size)
    raw=jar.read_bytes()
    if before(st)!=before(jar.stat()):raise AuditError("publisher bytes changed during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1:raise AuditError("official publisher JAR SHA-1 does not match physical modlist")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        paths=z.namelist()
        if len(paths)!=len(set(paths)):raise AuditError("duplicate JAR entry paths")
        if REGISTER.replace(".","/")+".class" not in paths:raise AuditError("published registry class not found")
        try:meta=z.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:raise AuditError("NeoForge mod descriptor absent") from exc
        if len(meta)>256_000 or not re.search(rb'\bmodId\s*=\s*["\x27]monstersspellbooks["\x27]',meta):
            raise AuditError("wrong exact publisher mod ID")
    compiled=registry_pairs(run_javap(jar.resolve(),REGISTER))
    mismatched={}
    records=[]
    for field,clazz in sorted(compiled.items()):
        expected_family,expected_class=expected.get(field,("", ""))
        if clazz.split(".")[-1]!=expected_class:
            mismatched[field]={"source":expected_class,"compiled":clazz}
        if clazz.replace(".","/")+".class" not in paths:raise AuditError("registered spell class missing: "+clazz)
        root=spell_id(run_javap(jar.resolve(),clazz))
        records.append({"field":field,"clazz":clazz,"root":root,"source_family":expected_family})
    roots=[x["root"] for x in records]
    observed=Counter(roots)
    deviations={
       "source_registry_constant_class_mismatch":mismatched,
       "unexpected_field_constants":sorted(set(compiled)-set(expected)),
       "missing_field_constants":sorted(set(expected)-set(compiled)),
       "duplicate_spell_ids":sorted(x for x,y in observed.items() if y!=1),
       "expected_98_compiled_spells":len(records)!=98,
       "spell_resources_wrong_namespace":False,
    }
    if before(jar.stat())!=before(st) or hashlib.sha256(jar.read_bytes()).hexdigest()!=sha256:
        raise AuditError("JAR changed during bytecode analysis")
    return {
      "result":"PASS" if not any(deviations.values()) else "UNPROVEN_OR_MISMATCH",
      "evidence_class":"PHYSICAL_SHA1_MATCHED_COMPILED_STATIC_REGISTRY_AND_98_SPELL_RESOURCES_NOT_RUNTIME",
      "version":"0.0.16.3","jar":JAR_NAME,"mod_id":MOD_ID,"sha1":sha1,"sha256":sha256,"size_bytes":len(raw),
      "declared_source_roots":len(expected),"compiled_registered_spell_classes":len(compiled),
      "unique_compiled_spell_ids":len(observed),"deviations":deviations,
      "registered_spell_identities":records,
      "not_proven":["registry actually loaded / config or spell enabled","Aero SchoolType present or absent",
        "school registration and configured spells","Iron's casting, mana, cooldown, tiers or acquisition",
        "live client/server or Survival","RPG Skill Tree bridge"]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--inventory",type=Path,default=INVENTORY)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    try:
        if a.inventory.stat().st_size>250000:raise AuditError("source inventory exceeds bounds")
        report=audit(a.jar,a.inventory.read_text(encoding="utf8"))
        code=0 if report["result"]=="PASS" else 1
    except (AuditError,OSError,UnicodeError,ValueError,zipfile.BadZipFile) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    payload=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if a.output:
        a.output.parent.mkdir(exist_ok=True,parents=True)
        a.output.write_text(payload,encoding="utf8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
,re.M)

class AuditError(ValueError): pass

def expected_inventory(text: str) -> dict[str, tuple[str,str]]:
    entries=ROW.findall(text)
    if len(entries)!=98 or sorted(int(v[0]) for v in entries)!=list(range(1,99)):
        raise AuditError("source catalog is not exactly 98 individually indexed spells")
    roster={}
    family=Counter()
    for _,fam,constant,classname in entries:
        if constant in roster: raise AuditError("duplicate source registry constant")
        roster[constant]=(fam,classname)
        family[fam]+=1
    if dict(family)!=FAMILY_COUNTS or len({x[1] for x in roster.values()})!=98:
        raise AuditError("98 source family counts / concrete class identities differ")
    return roster

def instructions(text: str) -> list[tuple[str,str]]:
    return [(x.group(1),(x.group(2) or "").strip()) for x in INSTRUCTION.finditer(text)]

def registry_pairs(disassembly: str) -> dict[str,str]:
    marker="  static {};"
    if disassembly.count(marker)!=1: raise AuditError("registry has no single static initializer")
    declarations,initializer=disassembly.split(marker,1)
    fields=FIELD.findall(declarations)
    if len(fields)!=98 or len(set(fields))!=98:
        raise AuditError("compiled registry must declare 98 unique Supplier fields")
    code=instructions(initializer)
    records={}
    register_calls=0
    for n,(op,comment) in enumerate(code):
        if op!="invokestatic" or "registerSpell:" not in comment: continue
        register_calls+=1
        if n<3 or n+1>=len(code): raise AuditError("registry contains orphaned registration")
        (newop,newcomment),(dupop,_),(ctorop,ctorcomment)=code[n-3:n]
        storeop,storecomment=code[n+1]
        if (newop,dupop,ctorop,storeop)!=("new","dup","invokespecial","putstatic"):
            raise AuditError("non-literal or conditional-looking spell construction")
        clazz=re.search(r'\bclass (net/redreaper/monsterspellbooks/[\w/$]+)$',newcomment)
        field=re.search(r'\bField ([A-Z][A-Z0-9_]*):',storecomment)
        if not clazz or not field or '"<init>"' not in ctorcomment:
            raise AuditError("compiled constructor/field registration ambiguous")
        key=field.group(1)
        if key in records: raise AuditError("duplicate compiled registration field")
        records[key]=clazz.group(1).replace("/",".")
    if register_calls!=98 or set(records)!=set(fields) or len(set(records.values()))!=98:
        raise AuditError("compiled registry field/call/class cardinality mismatch")
    return records

def spell_id(disassembly: str) -> str:
    if "getSpellResource();" not in disassembly:
        raise AuditError("spell class has no getSpellResource method")
    code=instructions(disassembly)
    found=[]
    for n,(op,comment) in enumerate(code):
        if op!="invokestatic" or "ResourceLocation.fromNamespaceAndPath:" not in comment:continue
        if n<2 or n+1>=len(code): continue
        nsop,nscomment=code[n-2]
        pathop,pathcomment=code[n-1]
        storeop,storecomment=code[n+1]
        if not ((nsop in ("ldc","ldc_w") and nscomment=="String monstersspellbooks") or
                (nsop=="getstatic" and "MonstersSpellbooks.MOD_ID:" in nscomment)):
            raise AuditError("spell resource constructor uses unexpected namespace")
        if (pathop not in ("ldc","ldc_w") or not pathcomment.startswith("String ")
            or storeop!="putfield" or not re.search(r'\bField spellId:',storecomment)):
            continue
        root=pathcomment[7:]
        if not re.fullmatch(r"[a-z][a-z0-9_]*",root):
            raise AuditError("malformed compiled spell resource path")
        found.append(root)
    if len(found)!=1:
        raise AuditError("spell class has no unique spellId assignment: "+str(found))
    getter=disassembly.split("getSpellResource();",1)[1].split("\n  public ",1)[0]
    if not re.search(r"getfield\s+[^\n]*// Field spellId:",getter) or not re.search(r"\bareturn\b",getter):
        raise AuditError("compiled spell resource getter does not return the spellId field")
    return found[0]

def run_javap(jar:Path,name:str)->str:
    try:
        res=subprocess.run(["javap","-c","-p","-classpath",str(jar),name],capture_output=True,text=True,check=False,timeout=45)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("Java21 classfile inspector failed or timed out") from exc
    if res.returncode or not 0<len(res.stdout)<4_000_000:
        raise AuditError("javap cannot inspect required published class "+name)
    return res.stdout

def audit(jar:Path, source:str)->dict:
    expected=expected_inventory(source)
    if jar.name!=JAR_NAME or jar.is_symlink() or not jar.is_file():
        raise AuditError("wrong or unsafe installed JAR")
    st=jar.stat()
    if not stat.S_ISREG(st.st_mode) or not 0<st.st_size<MAX_BYTES:raise AuditError("physical JAR bounds invalid")
    before=lambda x:(x.st_dev,x.st_ino,x.st_mtime_ns,x.st_ctime_ns,x.st_size)
    raw=jar.read_bytes()
    if before(st)!=before(jar.stat()):raise AuditError("publisher bytes changed during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1:raise AuditError("official publisher JAR SHA-1 does not match physical modlist")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        paths=z.namelist()
        if len(paths)!=len(set(paths)):raise AuditError("duplicate JAR entry paths")
        if REGISTER.replace(".","/")+".class" not in paths:raise AuditError("published registry class not found")
        try:meta=z.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:raise AuditError("NeoForge mod descriptor absent") from exc
        if len(meta)>256_000 or not re.search(rb'\bmodId\s*=\s*["\x27]monstersspellbooks["\x27]',meta):
            raise AuditError("wrong exact publisher mod ID")
    compiled=registry_pairs(run_javap(jar.resolve(),REGISTER))
    mismatched={}
    records=[]
    for field,clazz in sorted(compiled.items()):
        expected_family,expected_class=expected.get(field,("", ""))
        if clazz.split(".")[-1]!=expected_class:
            mismatched[field]={"source":expected_class,"compiled":clazz}
        if clazz.replace(".","/")+".class" not in paths:raise AuditError("registered spell class missing: "+clazz)
        root=spell_id(run_javap(jar.resolve(),clazz))
        records.append({"field":field,"clazz":clazz,"root":root,"source_family":expected_family})
    roots=[x["root"] for x in records]
    observed=Counter(roots)
    deviations={
       "source_registry_constant_class_mismatch":mismatched,
       "unexpected_field_constants":sorted(set(compiled)-set(expected)),
       "missing_field_constants":sorted(set(expected)-set(compiled)),
       "duplicate_spell_ids":sorted(x for x,y in observed.items() if y!=1),
       "expected_98_compiled_spells":len(records)!=98,
       "spell_resources_wrong_namespace":False,
    }
    if before(jar.stat())!=before(st) or hashlib.sha256(jar.read_bytes()).hexdigest()!=sha256:
        raise AuditError("JAR changed during bytecode analysis")
    return {
      "result":"PASS" if not any(deviations.values()) else "UNPROVEN_OR_MISMATCH",
      "evidence_class":"PHYSICAL_SHA1_MATCHED_COMPILED_STATIC_REGISTRY_AND_98_SPELL_RESOURCES_NOT_RUNTIME",
      "version":"0.0.16.3","jar":JAR_NAME,"mod_id":MOD_ID,"sha1":sha1,"sha256":sha256,"size_bytes":len(raw),
      "declared_source_roots":len(expected),"compiled_registered_spell_classes":len(compiled),
      "unique_compiled_spell_ids":len(observed),"deviations":deviations,
      "registered_spell_identities":records,
      "not_proven":["registry actually loaded / config or spell enabled","Aero SchoolType present or absent",
        "school registration and configured spells","Iron's casting, mana, cooldown, tiers or acquisition",
        "live client/server or Survival","RPG Skill Tree bridge"]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--inventory",type=Path,default=INVENTORY)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    try:
        if a.inventory.stat().st_size>250000:raise AuditError("source inventory exceeds bounds")
        report=audit(a.jar,a.inventory.read_text(encoding="utf8"))
        code=0 if report["result"]=="PASS" else 1
    except (AuditError,OSError,UnicodeError,ValueError,zipfile.BadZipFile) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        code=1
    payload=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if a.output:
        a.output.parent.mkdir(exist_ok=True,parents=True)
        a.output.write_text(payload,encoding="utf8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
