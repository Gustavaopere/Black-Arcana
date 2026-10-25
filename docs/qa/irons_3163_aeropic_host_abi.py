#!/usr/bin/env python3
"""Clean-room ABI check for the precise published Iron's Spellbooks 1.21.1-3.16.3 JAR.

The Modrinth project/version/file identity and its published SHA512 are checked
before inspecting any class. Report signatures only, NEVER bytecode, third-party
implementation, dynamic receiver or actual runtime behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

HOST_NAME = "irons_spellbooks-1.21.1-3.16.3.jar"
HOST_VERSION = "1.21.1-3.16.3"
PROJECT_ID = "s4OWxYQQ"
VERSION_ID = "slKLosTb"
OFFICIAL_URL = ("https://cdn.modrinth.com/data/s4OWxYQQ/versions/slKLosTb/"
                + HOST_NAME)
EXPECTED_BYTES = 13_890_046  # cross-checked publisher release file listing
NEEDED = {
    "abstract_spell": "io.redspace.ironsspellbooks.api.spells.AbstractSpell",
    "player_recasts": "io.redspace.ironsspellbooks.capabilities.magic.PlayerRecasts",
    "recast_instance": "io.redspace.ironsspellbooks.capabilities.magic.RecastInstance",
    "magic_data": "io.redspace.ironsspellbooks.api.magic.MagicData",
}
METHODS = {
    "abstract_spell": {
        ("getRecastCount", "(ILnet/minecraft/world/entity/LivingEntity;)I")
    },
    "player_recasts": {
        ("addRecast", "(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z"),
        ("hasRecastForSpell", "(Ljava/lang/String;)Z"),
        ("decrementRecastCount", "(Ljava/lang/String;)V"),
    },
    "recast_instance": {
        ("<init>", "(Ljava/lang/String;IIILio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/spells/ICastDataSerializable;)V")
    },
}
DECL = re.compile(r"^  (?:public|protected|private) .+\([^;]*\)(?: throws [^;]*)?;$")
DESCRIPTOR = re.compile(r"^\s+descriptor:\s+(\S+)$")
HEX_SHA1 = re.compile(r"^[a-f0-9]{40}$")
HEX_SHA512 = re.compile(r"^[a-f0-9]{128}$")

class EvidenceError(ValueError):
    pass

def validate_publisher_metadata(record: dict) -> dict:
    """Trust only signed-by-content publisher digest, pinned release identity."""
    if (not isinstance(record, dict)
        or record.get("id") != VERSION_ID
        or record.get("project_id") != PROJECT_ID
        or record.get("version_number") != HOST_VERSION
        or "1.21.1" not in record.get("game_versions", [])
        or "neoforge" not in record.get("loaders", [])):
        raise EvidenceError("official release/project identity mismatch")
    files = record.get("files")
    if not isinstance(files, list):
        raise EvidenceError("official version has no file list")
    matches = [x for x in files if x.get("filename")==HOST_NAME]
    if len(matches)!=1:
        raise EvidenceError("not exactly one exact installed host filename")
    file=matches[0]
    if file.get("url")!=OFFICIAL_URL or file.get("size")!=EXPECTED_BYTES:
        raise EvidenceError("host publisher URL or exact size mismatch: published URL="+str(file.get("url"))+"; size="+str(file.get("size"))+"; expected="+OFFICIAL_URL+" / "+str(EXPECTED_BYTES))
    hashes=file.get("hashes")
    if (not isinstance(hashes, dict)
        or not HEX_SHA1.fullmatch(str(hashes.get("sha1", "")))
        or not HEX_SHA512.fullmatch(str(hashes.get("sha512", "")))):
        raise EvidenceError("no complete publisher SHA-1 and SHA-512")
    return {"sha1": hashes["sha1"], "sha512": hashes["sha512"],
            "source": "OFFICIAL_MODRINTH_VERSION_METADATA_MATCHED_SHA512",
            "publisher_version_id": VERSION_ID}

def verify_jar(jar: Path, identity: dict) -> dict:
    if jar.name!=HOST_NAME or not jar.is_file() or jar.is_symlink():
        raise EvidenceError("invalid host JAR physical filename or file kind")
    info=jar.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size!=EXPECTED_BYTES:
        raise EvidenceError("host JAR physical size drift")
    hashes={"sha1":hashlib.sha1(), "sha512":hashlib.sha512()}
    with jar.open("rb") as stream:
        while True:
            data=stream.read(1024*1024)
            if not data:
                break
            for digest in hashes.values():
                digest.update(data)
    observed={k:h.hexdigest() for k,h in hashes.items()}
    if observed != {k:identity[k] for k in observed}:
        raise EvidenceError("physical JAR digest differs from publisher digest")
    with zipfile.ZipFile(jar) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):
            raise EvidenceError("duplicate ZIP entries in published host")
        if archive.testzip() is not None:
            raise EvidenceError("corrupt host ZIP member")
        for name in NEEDED.values():
            if name.replace(".","/")+".class" not in names:
                raise EvidenceError("host class absent: "+name)
    return observed

def declarations(javap: str, class_short: str) -> dict[str,dict]:
    """Extract JVM ABI descriptors; reject ambiguous selected overloads."""
    output={}
    lines=javap.splitlines()
    for idx,line in enumerate(lines):
        if not DECL.match(line):
            continue
        name=line.strip().split("(",1)[0].rsplit(" ",1)[-1]
        if name in {NEEDED[class_short].rsplit(".",1)[-1], NEEDED[class_short]}:
            name="<init>"
        if name not in {n for n,_ in METHODS.get(class_short,set())}:
            continue
        if idx+1>=len(lines):
            raise EvidenceError("truncated javap declaration")
        dm=DESCRIPTOR.match(lines[idx+1])
        if dm is None:
            raise EvidenceError("missing declaration descriptor")
        descriptor=dm.group(1)
        if name in output:
            raise EvidenceError("ambiguous overload in selected host ABI "+name)
        output[name]={
            "declaration":line.strip(),
            "descriptor":descriptor,
            "is_static": bool(re.search(r"\bstatic\b",line)),
            "is_abstract": bool(re.search(r"\babstract\b",line)),
        }
    required=METHODS.get(class_short, set())
    for method,signature in required:
        row=output.get(method)
        if row is None or row["descriptor"]!=signature:
            raise EvidenceError("host method ABI absent or incompatible: "+class_short+"."+method)
        if method!="<init>" and (row["is_static"] or row["is_abstract"]):
            raise EvidenceError("unexpected static/abstract host method: "+method)
    return output

def inspect(jar:Path, metadata:dict) -> dict:
    identity=validate_publisher_metadata(metadata)
    digests=verify_jar(jar,identity)
    classes={}
    for short,fullname in NEEDED.items():
        try:
            proc=subprocess.run(["javap","-s","-p","-classpath",str(jar),fullname],
                capture_output=True,text=True,timeout=30,check=True)
        except (OSError,subprocess.TimeoutExpired,subprocess.CalledProcessError) as exc:
            raise EvidenceError("javap host failed: "+short) from exc
        classes[short]={"class_name":fullname,
                        "checked_signatures":declarations(proc.stdout,short),
                        "classification":"EXACT_PUBLISHED_JVM_DECLARATIONS_ONLY"}
    return {
        "result":"PASS_EXACT_HOST_3163_RECAST_ABI",
        "host_jar":HOST_NAME,"host_mod_version":HOST_VERSION,
        "sha1":digests["sha1"],"sha512":digests["sha512"],
        "file_size":EXPECTED_BYTES,
        "provenance":identity["source"],
        "host_classes":classes,
        "wind_provider":"wind_spellbooks-1.0.5; sha1 8744886899bc245ae147a44baa2b183689cec7da",
        "host_abi_compatible_with_Wind_calls":True,
        "aeropic_effect_receiver":"NOT_PROVEN",
        "aeropic_override_execution":"NOT_PROVEN",
        "recast_flow_to_host_state":"NOT_PROVEN",
        "safe_black_arcana_or_rpg_mutator":"NOT_PROVEN",
        "gameplay_validation":"NOT_TESTED",
        "scope":"EXACT_PUBLISHED_COMPILED_HOST_ABI_NOT_RUNTIME",
    }

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--publisher-json",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=inspect(args.jar,json.loads(args.publisher_json.read_text(encoding="utf8")))
        status=0
    except (EvidenceError,zipfile.BadZipFile,ValueError,TypeError,KeyError,OSError) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        status=1
    payload=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf8")
    print(payload)
    return status

if __name__=="__main__":
    raise SystemExit(main())
