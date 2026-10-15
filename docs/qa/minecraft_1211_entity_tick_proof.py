#!/usr/bin/env python3
"""Fail-closed audit of tickCount provenance in Mojang's official 1.21.1 server.

No Minecraft code, mappings or binaries are distributed in resulting report.
Not a NeoForge/GameTest or installed modpack proof.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from zipfile import ZipFile

VERSION = "1.21.1"
MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
HOSTS = {"piston-meta.mojang.com", "piston-data.mojang.com",
         "launchermeta.mojang.com"}


def download(url, sha1=None, size=None):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in HOSTS:
        raise ValueError("Expected official Mojang HTTPS origin")
    with urllib.request.urlopen(url, timeout=120) as result:
        data = result.read()
    digest = hashlib.sha1(data).hexdigest()
    if sha1 and sha1 != digest:
        raise ValueError("Mojang manifest SHA1 mismatch")
    if size and len(data) != size:
        raise ValueError("Mojang manifest size mismatch")
    return data, digest


def mapping_section(mappings, original):
    hit = re.search("^" + re.escape(original) + r" -> ([\w.$]+):$", mappings, re.M)
    if not hit:
        raise ValueError("Missing official class mapping: " + original)
    tail = mappings[hit.end():]
    next_class = re.search(r"^[^\s].+ -> [\w.$]+:$", tail, re.M)
    return hit.group(1), tail[:next_class.start() if next_class else len(tail)]


def member_name(section, phrase):
    entries = [line.split(" -> ")[-1].strip() for line in section.splitlines()
               if phrase in line and " -> " in line]
    if not entries or len(set(entries)) != 1:
        raise ValueError("Ambiguous official member mapping: " + phrase)
    return entries[0]


def extract_method(javap, name, descriptor):
    lines = javap.splitlines()
    hits = []
    for i, line in enumerate(lines[:-2]):
        if (line.startswith("  ") and not line.startswith("    ")
                and re.search(r"\b" + re.escape(name) + r"\([^)]*\);$", line)
                and lines[i + 1].strip() == "descriptor: " + descriptor):
            end = i + 2
            while end < len(lines) and not (
                    lines[end].startswith("  ") and not lines[end].startswith("    ")
                    and re.search(r"[;{}]$", lines[end])):
                end += 1
            hits.append("\n".join(lines[i:end]))
    if len(hits) != 1:
        raise ValueError("Expected exactly one method with official descriptor")
    return hits[0]


def analyze(mappings, javap):
    _, level = mapping_section(mappings, "net.minecraft.server.level.ServerLevel")
    entity_type, entity = mapping_section(mappings, "net.minecraft.world.entity.Entity")
    field = member_name(entity, "int tickCount ->")
    tick = member_name(entity, "void tick() ->")
    method = member_name(level, "void tickNonPassenger(net.minecraft.world.entity.Entity) ->")
    block = extract_method(javap, method, "(L" + entity_type.replace(".", "/") + ";)V")
    lines = block.splitlines()
    field_match = re.compile(r"// Field (?:(?:" + re.escape(entity_type) + r"|"
                             + re.escape(entity_type.replace(".", "/")) + r")\.)?"
                             + re.escape(field) + r":I")
    reads = [i for i, line in enumerate(lines)
             if "getfield" in line and field_match.search(line)]
    writes = [i for i, line in enumerate(lines)
              if "putfield" in line and field_match.search(line)]
    ticks = [i for i, line in enumerate(lines)
             if ("invokevirtual" in line or "invokeinterface" in line)
             and re.search(r"\." + re.escape(tick) + r":\(\)V", line)]
    proven = bool(writes and ticks and min(writes) < min(ticks))
    return {
        "minecraft": VERSION,
        "evidence_class": "MOJANG_VANILLA_SERVER_BYTECODE_STATIC",
        "tick_non_passenger_resolved": True,
        "reads_entity_tickCount": bool(reads),
        "writes_entity_tickCount": bool(writes),
        "calls_entity_tick": bool(ticks),
        "tickCount_written_before_entity_tick": proven,
        "result": ("WORLD_TICK_INCREMENTS_ENTITY_AGE" if proven
                   else "NOT_PROVEN_BY_SELECTED_METHOD"),
        "limits": ["Vanilla server: not NeoForge transformed code",
                   "No live game or Iron's ArrowVolleyEntity GameTest",
                   "No installed modpack binary fingerprint"],
    }


def self_test():
    mapping = ("net.minecraft.server.level.ServerLevel -> aa:\n"
               "    1:5:void tickNonPassenger(net.minecraft.world.entity.Entity) -> m\n"
               "net.minecraft.world.entity.Entity -> bb:\n"
               "    int tickCount -> n\n"
               "    void tick() -> t\n")
    code = ("  private void m(bb);\n"
            "    descriptor: (Lbb;)V\n"
            "    Code:\n"
            "       0: aload_1\n"
            "       1: getfield #3 // Field bb.n:I\n"
            "       2: iconst_1\n"
            "       3: iadd\n"
            "       4: putfield #3 // Field bb.n:I\n"
            "       5: invokevirtual #4 // Method bb.t:()V\n"
            "  private void z();\n"
            "    descriptor: ()V\n")
    assert analyze(mapping, code)["result"] == "WORLD_TICK_INCREMENTS_ENTITY_AGE"
    assert not analyze(mapping, code.replace("putfield", "getfield"))["writes_entity_tickCount"]
    try:
        extract_method(code, "m", "(Lcc;)V")
        raise AssertionError("Descriptor mismatch must fail closed")
    except ValueError:
        pass


def run(output):
    manifest = json.loads(download(MANIFEST)[0])
    version_rows = [v for v in manifest["versions"]
                    if v["id"] == VERSION and v.get("type") == "release"]
    if len(version_rows) != 1:
        raise ValueError("Ambiguous official version")
    version_blob, version_hash = download(version_rows[0]["url"], version_rows[0]["sha1"])
    version = json.loads(version_blob)
    bundle_spec = version["downloads"]["server"]
    mapping_spec = version["downloads"]["server_mappings"]
    bundle, bundle_hash = download(bundle_spec["url"], bundle_spec["sha1"], bundle_spec["size"])
    mapped, mapped_hash = download(mapping_spec["url"], mapping_spec["sha1"], mapping_spec["size"])
    with ZipFile(io.BytesIO(bundle)) as z:
        files = [n for n in z.namelist() if n.endswith("/server-1.21.1.jar")]
        if len(files) != 1:
            raise ValueError("Bundler did not contain one official 1.21.1 inner JAR")
        inner = z.read(files[0])
    output.parent.mkdir(parents=True, exist_ok=True)
    local = output.parent / "official-minecraft-inner.jar"
    local.write_bytes(inner)
    mapping = mapped.decode("utf-8")
    level, _ = mapping_section(mapping, "net.minecraft.server.level.ServerLevel")
    args = ["javap", "-p", "-c", "-s", "-classpath", str(local), level]
    proc = subprocess.run(args, text=True, capture_output=True, timeout=45, check=False)
    if proc.returncode or "descriptor:" not in proc.stdout:
        raise ValueError("javap could not inspect official server binary")
    result = analyze(mapping, proc.stdout)
    result["artifacts"] = {
        "manifest_version_sha1": version_hash,
        "mojang_server_sha1": bundle_hash,
        "mojang_server_bytes": len(bundle),
        "mojang_mappings_sha1": mapped_hash,
        "embedded_server_sha256": hashlib.sha256(inner).hexdigest(),
    }
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("PASS: synthetic server method and mappings test")
        else:
            if args.output is None:
                parser.error("--output is required")
            run(args.output)
    except (KeyError, ValueError, OSError, AssertionError,
            subprocess.TimeoutExpired) as exc:
        print("FAIL_CLOSED:", exc, file=sys.stderr)
        raise SystemExit(1)
