#!/usr/bin/env python3
"""SHA-1 gated read-only binary audit. No runtime/Survival claims."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

JAR_NAME = "reliquified_artifacts-1.21.1-1.0.8.jar"
SHA1 = "00ad43d5a1aa287fd0084bc3b48546821494ff80"
MOD_ID = "reliquified_artifacts"
PACKAGE = "it/hurts/shatterbyte/reliquified_artifacts/items/"
MIXIN = "it.hurts.shatterbyte.reliquified_artifacts.mixin.init.ModItemsMixin"
INVENTORY = Path("wiki/modpack-catalog/providers/✅-reliquified-artifacts/ABILITY-INVENTORY-1.0.8.md")
ROW = re.compile(r"^\| \d+ \| \x60artifacts:([a-z0-9_]+)\x60 \| \x60([a-z0-9_]+)\x60 \| \x60([A-Za-z0-9]+Item)\x60 \|$", re.M)
INS = re.compile(r"^\s*\d+:\s+(\w+)(?:\s+[^/\n]*)?(?:\s*//\s*(.*))?$", re.M)

class AuditError(ValueError):
    pass

def expected_inventory(markdown):
    triples=ROW.findall(markdown)
    if len(triples)!=52 or len({(owner,ability) for owner,ability,_ in triples})!=52:
        raise AuditError("catalog must have 52 unique owner-scoped abilities")
    by_class=defaultdict(set)
    owners=defaultdict(set)
    for owner,ability,clazz in triples:
        by_class[clazz].add(ability)
        owners[owner].add(clazz)
    if (len(owners),len(by_class),sum(map(len,by_class.values())))!=(48,47,51):
        raise AuditError("source 48 owner / 47 class / 51 class-ability invariant violated")
    if owners.get("plastic_drinking_hat")!={"DrinkingHatItem"} or owners.get("novelty_drinking_hat")!={"DrinkingHatItem"}:
        raise AuditError("shared drinking hat identity changed")
    return triples,dict(by_class),set(owners)

def instructions(text):
    return [(x.group(1),(x.group(2) or "").strip()) for x in INS.finditer(text)]

def template_roots(disassembly):
    match=re.search(r"^  public [^\n]+ constructDefaultRelicTemplate\(\);$",disassembly,re.M)
    if not match:
        raise AuditError("class has no direct constructDefaultRelicTemplate")
    body=re.split(r"(?=^  (?:public|private|protected|static) )",disassembly[match.end():],maxsplit=1,flags=re.M)[0]
    code=instructions(body)
    roots=[]
    for i,(op,comment) in enumerate(code):
        if "AbilityTemplate.builder:" not in comment:
            continue
        if op!="invokestatic" or i==0 or code[i-1][0] not in ("ldc","ldc_w") or not code[i-1][1].startswith("String "):
            raise AuditError("nonliteral or non-static Relics ability builder")
        value=code[i-1][1][7:]
        if not re.fullmatch(r"[a-z][a-z0-9_]*",value):
            raise AuditError("invalid compiled ability ID")
        roots.append(value)
    if not roots or len(roots)!=len(set(roots)):
        raise AuditError("missing or duplicate compiled ability ID")
    return set(roots)

def run_javap(jar,clazz):
    try:
        out=subprocess.run(["javap","-c","-p","-classpath",str(jar),clazz],text=True,capture_output=True,timeout=40,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("javap unavailable or timed out") from exc
    if out.returncode or not 0<len(out.stdout)<5_000_000:
        raise AuditError("javap failed for "+clazz)
    return out.stdout

def mixin_literals(text):
    return set(re.findall(r"// String ([a-z][a-z0-9_]+)\s*$",text,re.M))

def audit(jar,inventory):
    triples,by_class,owners=expected_inventory(inventory)
    if jar.name!=JAR_NAME or jar.is_symlink() or not jar.is_file():
        raise AuditError("wrong or unsafe JAR path")
    before=jar.stat()
    if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<16_000_000:
        raise AuditError("publisher JAR size or type invalid")
    raw=jar.read_bytes()
    stamp=lambda s:(s.st_dev,s.st_ino,s.st_mtime_ns,s.st_ctime_ns,s.st_size)
    if stamp(before)!=stamp(jar.stat()):
        raise AuditError("JAR changed while reading")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1:
        raise AuditError("publisher bytes do not match sibling physical SHA1")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):
            raise AuditError("duplicate publisher JAR entries")
        try:
            meta=z.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:
            raise AuditError("NeoForge mod metadata missing") from exc
        if len(meta)>250_000 or not re.search(rb'\bmodId\s*=\s*["\x27]reliquified_artifacts["\x27]',meta):
            raise AuditError("mod ID absent or changed")
        classes={}
        for name in by_class:
            hit=[p for p in names if p.startswith(PACKAGE) and p.endswith("/"+name+".class")]
            if len(hit)!=1:
                raise AuditError("compiled artifact class missing/ambiguous: "+name)
            classes[name]=hit[0][:-6].replace("/",".")
        if MIXIN.replace(".","/")+".class" not in names or "reliquified_artifacts.mixins.json" not in names:
            raise AuditError("provider item-replacement Mixin class/config missing")
        config=json.loads(z.read("reliquified_artifacts.mixins.json"))
        if "init.ModItemsMixin" not in config.get("mixins",[]):
            raise AuditError("provider item-replacement Mixin not configured")
    observed={name:sorted(template_roots(run_javap(jar.resolve(),cl))) for name,cl in sorted(classes.items())}
    disagreements={name:{"catalog":sorted(by_class[name]),"compiled":roots} for name,roots in observed.items() if set(roots)!=by_class[name]}
    mixin=mixin_literals(run_javap(jar.resolve(),MIXIN))
    deviations={
       "builder_identity_mismatch":disagreements,
       "mixin_owner_missing":sorted(owners-mixin),
       "mixin_owner_extra":sorted(mixin-owners),
       "class_builder_count_mismatch":sum(map(len,observed.values()))!=51,
    }
    if stamp(before)!=stamp(jar.stat()) or hashlib.sha256(jar.read_bytes()).hexdigest()!=sha256:
        raise AuditError("publisher JAR mutated during audit")
    return {
      "result":"PASS" if not any(deviations.values()) else "UNPROVEN_OR_MISMATCH",
      "evidence_class":"PHYSICAL_SHA_MATCHED_STATIC_ABILITY_BUILDERS_AND_MIXIN_CASE_LITERALS_NOT_RUNTIME",
      "jar":JAR_NAME,"mod_id":MOD_ID,"version":"1.0.8",
      "sha1":sha1,"sha256":sha256,"size_bytes":len(raw),
      "owner_literals":len(owners),"implementation_classes":len(classes),
      "class_level_ability_roots":sum(map(len,observed.values())),
      "owner_scoped_semantic_roots":len(triples),"deviations":deviations,
      "not_proven":["executed Mixin injection or correct class per owner","actual loaded Relics templates",
                    "current Artifacts 13.2.5 runtime compat","config/loot/reachability","Survival",
                    "rank/XP persistence, effect settlement, equipment and Curios",
                    "pickup idempotence with Sophisticated Backpacks","RPG Skill Tree adapter"]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--inventory",type=Path,default=INVENTORY)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        if args.inventory.stat().st_size>150000: raise AuditError("inventory oversized")
        report=audit(args.jar,args.inventory.read_text(encoding="utf8"))
        status=0 if report["result"]=="PASS" else 1
    except (AuditError,OSError,UnicodeError,ValueError,zipfile.BadZipFile) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        status=1
    output=json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf8")
    print(output)
    return status

if __name__=="__main__":
    raise SystemExit(main())
