#!/usr/bin/env python3
"""Read-only SHA-gated Malum 1.8.2 compiled Spirit Rite registry audit.
Identity proof only, NOT loaded registry, ritual effects, or Survival.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

FILENAME="malum-1.21.1-1.8.2.jar"
INSTALLED_SHA1="7bea3f874f186a17ad3e271df145c179e81c2a1d"
CLASS="com.sammy.malum.registry.common.magic.rite.MalumSpiritRiteTypes"
# Factual public release-bounded names/holder identities, never upstream implementation.
RITES={
 "undirected_rite":"UNDIRECTED_RITE","unchained_rite":"UNCHAINED_RITE",
 "rite_of_healing":"RITE_OF_HEALING","rite_of_nourishment":"RITE_OF_NOURISHMENT",
 "rite_of_nurturing":"RITE_OF_NURTURING","rite_of_lust":"RITE_OF_LUST",
 "rite_of_harming":"RITE_OF_HARMING","rite_of_empowerment":"RITE_OF_EMPOWERMENT",
 "rite_of_culling":"RITE_OF_CULLING","rite_of_rending":"RITE_OF_RAISING",
 "rite_of_the_howling_gale":"RITE_OF_THE_HOWLING_GALE",
 "rite_of_the_sky_tether":"RITE_OF_THE_SKY_TETHER",
 "rite_of_gravity":"RITE_OF_GRAVITY","rite_of_ascension":"RITE_OF_ASCENSION",
 "rite_of_the_flowing_grasp":"RITE_OF_THE_FLOWING_GRASP",
 "rite_of_the_good_tides":"RITE_OF_THE_GOOD_TIDES",
 "rite_of_soaking":"RITE_OF_SOAKING","rite_of_sapping":"RITE_OF_SAPPING",
 "rite_of_the_stone_ward":"RITE_OF_THE_STONE_WARD",
 "rite_of_the_oaken_might":"RITE_OF_THE_OAKEN_MIGHT",
 "rite_of_creation":"RITE_OF_CREATION","rite_of_destruction":"RITE_OF_DESTRUCTION",
 "rite_of_the_burning_fervor":"RITE_OF_THE_BURNING_FERVOR",
 "rite_of_the_fiery_embrace":"RITE_OF_THE_FIERY_EMBRACE",
 "rite_of_smelting":"RITE_OF_SMELTING","rite_of_quickening":"RITE_OF_QUICKENING"
}
class AuditError(ValueError): pass

def validate_manifest():
    if len(RITES)!=26 or len(set(RITES.values()))!=26:
        raise AuditError("requires 26 unique source-pinned rite names/holders")
    for name,holder in RITES.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*",name) or not re.fullmatch(r"[A-Z][A-Z0-9_]*",holder):
            raise AuditError("invalid rite manifest identity")

def instructions(text):
    result=[]
    for m in re.finditer(r"^\s*(\d+):\s+([a-z][\w]*)\b([^\n]*)$",text,re.M):
        rest=m.group(3)
        result.append((int(m.group(1)),m.group(2),
                       rest.split("//",1)[0].strip(),
                       rest.split("//",1)[1].strip() if "//" in rest else ""))
    return result

def static_initializer(disassembly):
    match=re.search(r"^  static \{\};$",disassembly,re.M)
    if not match: raise AuditError("compiled class initializer missing")
    remainder=disassembly[match.end():]
    start=re.search(r"^    Code:$",remainder,re.M)
    if not start: raise AuditError("compiled initializer Code absent")
    block=remainder[start.end():]
    end=re.search(r"^      (?:LineNumberTable|LocalVariableTable|StackMapTable):",block,re.M)
    if not end: raise AuditError("no reliable compiled initializer boundary")
    return instructions(block[:end.start()])

def bootstrap_lambdas(disassembly):
    start=re.search(r"^BootstrapMethods:\s*$",disassembly,re.M)
    if not start: raise AuditError("no LambdaMetafactory bootstrap section")
    found={}
    index=None
    permitted=False
    for line in disassembly[start.end():].splitlines():
        head=re.match(r"^  (\d+):\s+(.+)$",line)
        if head:
            index=int(head.group(1))
            permitted="LambdaMetafactory.metafactory:" in head.group(2)
            continue
        if line.startswith(("InnerClasses:","NestMembers:","Signature:","SourceFile:")): break
        if index is not None and permitted and "REF_invokeStatic " in line:
            match=re.search(r"REF_invokeStatic\s+([\w/$]+)\.(lambda\$static\$\d+):",line)
            if not match: continue
            if index in found: raise AuditError("two factory lambdas share bootstrap")
            found[index]=match.group(1).replace("/",".")+"."+match.group(2)
    return found

def parse_registry(disassembly,expected=RITES,owner=CLASS):
    validate_manifest()
    code=static_initializer(disassembly)
    if not any(op=="invokestatic" and "DeferredRiteTypes.create:" in comment
               for _,op,_,comment in code): raise AuditError("deferred rites factory absent")
    if not any(op in ("invokevirtual","invokestatic") and "makeRegistry:" in comment
               for _,op,_,comment in code): raise AuditError("rite registry declaration absent")
    factories=bootstrap_lambdas(disassembly)
    found={}
    for i,(_,op,_,comment) in enumerate(code):
        if op not in ("invokevirtual","invokeinterface") or "DeferredRiteTypes.register:" not in comment:
            continue
        if i<3 or i+1>=len(code): raise AuditError("truncated register block")
        registry,literal,supplier=code[i-3:i]
        field=code[i+1]
        if not(registry[1]=="getstatic" and "Field RITE_TYPES:" in registry[3]
               and literal[1] in ("ldc","ldc_w") and literal[3].startswith("String ")
               and supplier[1]=="invokedynamic" and field[1]=="putstatic" and "Field " in field[3]):
            raise AuditError("no direct RITE_TYPES → ID → lambda → holder")
        name=literal[3][7:]
        holder=re.search(r"Field ([A-Z][A-Z0-9_]*):",field[3])
        reference=re.search(r"InvokeDynamic #(\d+):",supplier[3])
        if not holder or not reference: raise AuditError("unresolved literal supplier or holder")
        factory=factories.get(int(reference.group(1)))
        if not factory or not factory.startswith(owner+".lambda$static$"):
            raise AuditError("lambda does not belong to rite registry: "+name)
        if name in found: raise AuditError("duplicate registered rite name "+name)
        found[name]={"holder":holder.group(1),"factory_lambda":factory.rsplit(".",1)[-1]}
    if len(found)!=len(expected) or set(found)!=set(expected):
        raise AuditError("compiled identities differ: "+json.dumps({
          "missing":sorted(set(expected)-set(found)),
          "extra":sorted(set(found)-set(expected)),"count":len(found)}))
    mismatches={name:{"expected":expected[name],"observed":item["holder"]}
                for name,item in found.items() if item["holder"]!=expected[name]}
    if mismatches: raise AuditError("holder mismatch: "+json.dumps(mismatches))
    if len({item["factory_lambda"] for item in found.values()})!=len(expected):
        raise AuditError("two rites share one supplier lambda unexpectedly")
    return found

def javap(jar):
    try:
        p=subprocess.run(["javap","-c","-p","-v","-classpath",str(jar),CLASS],
                         capture_output=True,text=True,timeout=70,check=False)
    except (OSError,subprocess.TimeoutExpired) as err:
        raise AuditError("Java21 javap failed or timed out") from err
    if p.returncode or not 0<len(p.stdout)<5_000_000:
        raise AuditError("compiled Spirit Rite class unavailable")
    return p.stdout

def audit(path):
    validate_manifest()
    if path.name!=FILENAME or path.is_symlink() or not path.is_file():
        raise AuditError("wrong or unsafe publisher artifact")
    before=path.stat()
    mark=lambda s:(s.st_dev,s.st_ino,s.st_ctime_ns,s.st_mtime_ns,s.st_size)
    if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<50_000_000:
        raise AuditError("publisher outside safe size/type bounds")
    raw=path.read_bytes()
    if mark(before)!=mark(path.stat()): raise AuditError("JAR changed during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=INSTALLED_SHA1: raise AuditError("official publisher not physically SHA1-equal")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        paths=z.namelist()
        if len(paths)!=len(set(paths)): raise AuditError("duplicate JAR entries")
        if CLASS.replace(".","/")+".class" not in paths:
            raise AuditError("compiled Spirit Rite registry absent")
        try: meta=z.read("META-INF/neoforge.mods.toml")
        except KeyError as e: raise AuditError("NeoForge mod metadata missing") from e
        if len(meta)>250000 or not re.search(rb'\bmodId\s*=\s*["\x27]malum["\x27]',meta):
            raise AuditError("publisher compiled mod ID mismatch")
    result=parse_registry(javap(path.resolve()))
    if mark(before)!=mark(path.stat()) or hashlib.sha256(path.read_bytes()).hexdigest()!=sha256:
        raise AuditError("publisher changed during audit")
    return {"result":"PASS",
      "evidence_class":"SHA_MATCHED_COMPILED_26_MALUM_RITE_ID_HOLDER_FACTORY_LAMBDA_NOT_RUNTIME",
      "filename":FILENAME,"mod_id":"malum","version":"1.8.2",
      "installed_sha1":sha1,"publisher_sha256":sha256,"size_bytes":len(raw),
      "registered_rites":len(result),"spirit_rite_identities":dict(sorted(result.items())),
      "semantic_roots_existing":26,"deviations":{},
      "not_additive":"RiteEffects, Geas, typed spirits, addon Gaze rites",
      "not_proven":["loaded registry or rite effects","totem activation and recipe inputs",
       "typed spirit costs, Rite Locus lifetime and world mutators",
       "dedicated modpack Survival/multiplayer and Gaze/Lodestone interop",
       "source implementation API permissions due unresolved license conflict"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=audit(args.jar)
        status=0
    except (AuditError,OSError,ValueError,zipfile.BadZipFile) as err:
        report={"result":"FAIL_CLOSED","reason":str(err)}
        status=1
    blob=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(blob,encoding="utf8")
    print(blob)
    return status

if __name__=="__main__":
    raise SystemExit(main())
