#!/usr/bin/env python3
"""SHA-exact read-only ServerLevel.save(ProgressListener,boolean,boolean) JVM caller census.

Three official distributed NeoForge 21.1.248/Minecraft 1.21.1 server JARs
only; never interprets a constant pool reference as a runtime invocation.
No ModLauncher class transform, physical shutdown, or disk durability is observed.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNER = "net/minecraft/server/level/ServerLevel"
METHOD = "save"
SIGNATURE = "(Lnet/minecraft/util/ProgressListener;ZZ)V"
NEOFORGE_UNIVERSAL_SHA256 = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
TARGET = {"owner": OWNER, "name": METHOD, "descriptor": SIGNATURE}
SCOPE = "NEOFORGE_211248_SERVERLEVEL_SAVE_CALLSITE_CENSUS_DISTRIBUTED_ONLY"
TARGETS = {
    "serverlevel-save": {"target": TARGET, "scope": SCOPE},
    "saveallchunks": {"target": {"owner": "net/minecraft/server/MinecraftServer",
                                  "name": "saveAllChunks", "descriptor": "(ZZZ)Z"},
                      "scope": "NEOFORGE_211248_SAVEALLCHUNKS_CALLSITE_CENSUS_DISTRIBUTED_ONLY"},
}
MAX_CLASS_BYTES = 8_000_000
MAX_CLASSES = 35_000
MAX_CANDIDATES = 140
MAX_INSNS = 4_500
MAX_REPORT_BYTES = 510_000

def matching_methodref(reader, i, target):
    entry = reader.pool[i]
    if entry is None or entry[0] not in (10, 11):
        return False
    _, owner, signature = reader.resolve(i)
    return owner == target["owner"] and signature[1:] == [target["name"], target["descriptor"]]

def scan_archive(path: Path, label: str, javap: str, target: dict):
    with ZipFile(path) as z:
        all_names = z.namelist()
        require(len(all_names) == len(set(all_names)), "duplicate JAR member")
        classes = sorted(n for n in all_names if n.endswith(".class")
                         and not n.startswith("META-INF/versions/"))
        require(len(classes) <= MAX_CLASSES, "class scan exceeded configured bound")
        candidates = []
        for path_name in classes:
            raw = z.read(path_name)
            require(64 < len(raw) <= MAX_CLASS_BYTES and raw[:4] == b"\xca\xfe\xba\xbe",
                    "invalid or oversized official class: " + path_name)
            reader = ClassReader(raw)
            require(reader.name + ".class" == path_name, "class path mismatch: " + path_name)
            refs = [i for i in range(1, len(reader.pool)) if matching_methodref(reader, i, target)]
            handles = [i for i, entry in enumerate(reader.pool)
                       if entry and entry[0] == 15 and entry[1][1] in refs]
            if refs or handles:
                candidates.append({"owner":reader.name,"class_sha256":digest(raw),
                                   "methodref_indices":refs,"handle_indices":handles})
    require(len(candidates) <= MAX_CANDIDATES, "candidate budget exceeded")
    direct = []
    for c in candidates:
        owner = c["owner"]
        with ZipFile(path) as z:
            raw = z.read(owner + ".class")
        reader = ClassReader(raw)
        methods = disassemble(str(path), javap, owner)
        declared = {(m["name"],m["descriptor"]):m for m in reader.methods}
        require(set(methods) == set(declared), "method roster mismatch: "+owner)
        for key,body in sorted(methods.items()):
            calls = []
            for offset,(opcode,operand,symbol) in sorted(body.items()):
                if not opcode.startswith("invoke") or opcode=="invokedynamic":
                    continue
                match = re.match(r"#(\d+)(?:\s|$)",operand)
                if match and int(match.group(1)) in c["methodref_indices"]:
                    calls.append({"offset":offset,"opcode":opcode,"cp_index":int(match.group(1)),
                                  "symbol":symbol})
            if calls:
                require(len(body) <= MAX_INSNS, "callsite method exceeds bounded disassembly")
                direct.append({"archive":label,"owner":owner,"class_sha256":c["class_sha256"],
                               "method":summarize(reader,key,body),"callsites":calls})
    return {"archive":label,"jar_sha256":digest(path.read_bytes()),
            "jar_bytes":path.stat().st_size,"class_entries_scanned":len(classes),
            "class_roster_sha256":digest(("\n".join(classes)+"\n").encode("utf8")),
            "typed_candidates":candidates,"direct_invoke_sites":direct}

def audit(server: Path, srg: Path, universal: Path, javap: str, mode: str):
    dist=verify_distribution(server,srg)
    require(universal.stat().st_size==3551268 and
            digest(universal.read_bytes())==NEOFORGE_UNIVERSAL_SHA256,
            "unexpected official universal JAR identity")
    spec = TARGETS[mode]
    archives = [scan_archive(path,label,javap,spec["target"]) for label,path in (
        ("NEOFORGE_OVERLAY",server),("INSTALLED_MINECRAFT_SRG",srg),
        ("NEOFORGE_UNIVERSAL",universal))]
    return {"schema_version":1,"scope":spec["scope"],"target":spec["target"],
            "distribution":dist,"archives":archives,
            "scope_limit":"three exact official distributed JARs only; no ModLauncher transform or modpack-wide proof",
            "server_stop_arguments":"NOT_VERIFIED",
            "shutdown_path_execution":"NOT_TESTED",
            "async_write_completion":"NOT_TESTED",
            "disk_durability":"NOT_TESTED",
            "static_contract":"NOT_CERTIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "provider_universe_closed":False,
            "mutation":"NO_MUTATION",
            "semantic_magic_roots_delta":0}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ("server","srg","universal","output"):
        ap.add_argument("--"+name,type=Path,required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--mode", choices=sorted(TARGETS), default="serverlevel-save")
    a=ap.parse_args()
    require(a.output.suffix==".json" and not a.output.exists(),"new report path required")
    report=audit(a.server,a.srg,a.universal,a.javap,a.mode)
    raw=canonical(report).encode("utf8")
    require(0<len(raw)<=MAX_REPORT_BYTES,"bounded report size exceeded")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(raw)
    print("SAVE_CALLSITE_REPORT_SHA256",a.mode,hashlib.sha256(raw).hexdigest())
    print("SAVE_CALLSITE_REPORT_BYTES",a.mode,len(raw))
    for archive in report["archives"]:
        print("ARCHIVE",archive["archive"],archive["jar_sha256"],
              "class_entries",archive["class_entries_scanned"],
              "typed_candidates",len(archive["typed_candidates"]),
              "direct_invoke_methods",len(archive["direct_invoke_sites"]))
        for item in archive["direct_invoke_sites"]:
            m=item["method"]
            print("DIRECT",item["owner"],m["declaration"]["name"],
                  m["declaration"]["descriptor"],"class_sha",item["class_sha256"],
                  "code_sha",m["declaration"]["code_sha256"],
                  "instruction_sha",m["instruction_sha256"],
                  "insns",m["instruction_count"],"calls",item["callsites"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")
if __name__=="__main__":
    main()
