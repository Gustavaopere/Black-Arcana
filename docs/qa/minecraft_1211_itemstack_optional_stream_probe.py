#!/usr/bin/env python3
"""Read-only Minecraft 1.21.1 vanilla ItemStack stream-codec ABI probe.

This examines Mojang's *vanilla client* bytecode and official mapping.
NeoForge 21.1.248 runtime bytecode is NOT inferred from this artifact.
Never export provider/Mojang source or full class disassembly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

VERSION = "1.21.1"
CLIENT_SHA1 = "30c73b1c5da787909b2f73340419fdf13b9def88"
MOJANG_CLASS = "net.minecraft.world.item.ItemStack"
MOJANG_FIELD = "OPTIONAL_STREAM_CODEC"
CLASS_MAPPING = re.compile(r"^([^ \t:#].*?) -> ([\w.$]+):$")
FIELD_MAPPING = re.compile(r"^\s+(.+?)\s+([A-Za-z_$][A-Za-z0-9_$]*) -> ([A-Za-z_$][A-Za-z0-9_$]*)$")
BYTECODE_LINE = re.compile(r"^\s+(\d+):\s+([a-z][a-z0-9_]*)\s*(.*?)(?:\s+//\s+(.*))?$")
MAX_JAVAP_BYTES = 2_300_000
MAX_WINDOW = 34
MAX_REPORT_BYTES = 16000


class MojangBoundaryError(ValueError):
    pass


def require(ok, detail):
    if not ok:
        raise MojangBoundaryError(detail)


def sha1_file(path):
    digest = hashlib.sha1()
    size = 0
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def map_itemstack(mapping_text):
    """Extract only named field and owner from the official Mojang mappings."""
    owner = None
    candidates = []
    for line in mapping_text.splitlines():
        match = CLASS_MAPPING.match(line)
        if match:
            owner = match.group(1)
            obfuscated_class = match.group(2)
            if owner == MOJANG_CLASS:
                candidates.append({"class": obfuscated_class, "field": None,
                                   "named_field_type": None})
            continue
        if owner != MOJANG_CLASS:
            continue
        match = FIELD_MAPPING.match(line)
        if match and match.group(2) == MOJANG_FIELD:
            require(len(candidates) == 1, "ambiguous official ItemStack owner")
            require(candidates[0]["field"] is None, "duplicated optional field mapping")
            candidates[0]["field"] = match.group(3)
            candidates[0]["named_field_type"] = match.group(1)
    require(len(candidates) == 1 and candidates[0]["field"] is not None,
            "official mapping did not resolve ItemStack.OPTIONAL_STREAM_CODEC")
    require("StreamCodec" in candidates[0]["named_field_type"],
            "mapped OPTIONAL_STREAM_CODEC field type drift")
    return candidates[0]


def parse_initializer(javap_output, expected_field):
    """Find just selected references surrounding one putstatic in <clinit>."""
    require(0 < len(javap_output) <= MAX_JAVAP_BYTES, "oversized/empty javap output")
    lines = javap_output.splitlines()
    starts = [i for i, l in enumerate(lines) if l.strip() == "static {};"]
    require(len(starts) == 1, "missing or duplicate static initializer")
    entries = []
    for line in lines[starts[0] + 1:]:
        if line.startswith("}"):
            break
        match = BYTECODE_LINE.match(line)
        if match:
            off, opcode, operand, symbol = match.groups()
            entries.append({"offset": int(off), "opcode": opcode,
                            "symbol": (symbol or "")[:400]})
    require(5 <= len(entries) <= 1200, "unbounded/absent static initializer bytecode")
    require(len({x["offset"] for x in entries}) == len(entries),
            "duplicate JVM bytecode offsets")
    anchors = [
        i for i, x in enumerate(entries)
        if x["opcode"] == "putstatic" and
        re.search(r"\bField (?:[\w/$]+\.)?" +
                  re.escape(expected_field) + r":", x["symbol"])
    ]
    require(len(anchors) == 1, "mapped OPTIONAL_STREAM_CODEC static assignment not unique")
    center = anchors[0]
    window = entries[max(0,center - MAX_WINDOW):center + 1]
    selected = [
        x for x in window
        if x["opcode"].startswith("invoke") or
        x["opcode"] in ("getstatic", "putstatic", "new", "checkcast", "ldc", "ldc_w")
    ]
    require(1 <= len(selected) <= MAX_WINDOW, "bounded initializer symbolic refs exceeded")
    return {
        "initializer_instruction_count": len(entries),
        "optional_codec_putstatic_offset": entries[center]["offset"],
        "selected_preassignment_abi": selected
    }


def audit(client, mappings, metadata, javap_bin):
    require(metadata.get("id") == VERSION and metadata.get("type") == "release",
            "incorrect official version metadata")
    downloads = metadata.get("downloads", {})
    expected_client = downloads.get("client", {})
    expected_mapping = downloads.get("client_mappings", {})
    require(expected_client.get("sha1") == CLIENT_SHA1,
            "official client artifact SHA disagreement")
    require(isinstance(expected_mapping.get("sha1"), str) and
            re.fullmatch(r"[a-f0-9]{40}", expected_mapping["sha1"]),
            "official mapping hash missing")
    client_sha, client_size = sha1_file(client)
    require(client_sha == CLIENT_SHA1 and client_size == expected_client.get("size"),
            "downloaded vanilla 1.21.1 client JAR identity mismatch")
    mapping_sha, mapping_size = sha1_file(mappings)
    require(mapping_sha == expected_mapping["sha1"] and
            mapping_size == expected_mapping.get("size"),
            "downloaded official Mojang class mapping identity mismatch")
    mapped = map_itemstack(Path(mappings).read_text(encoding="utf-8"))
    dotted = mapped["class"]
    class_path = dotted.replace(".", "/") + ".class"
    with zipfile.ZipFile(client) as jar:
        names = jar.namelist()
        require(len(names) == len(set(names)), "duplicate client JAR member")
        require(class_path in names, "ItemStack obfuscated class missing from official JAR")
        raw = jar.read(class_path)
        require(len(raw) >= 8 and raw[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(raw[6:8], "big") == 65,
                "unexpected 1.21.1 official classfile major")
    command = [str(javap_bin), "-classpath", str(client), "-c", "-p", "-s", dotted]
    result = subprocess.run(command, capture_output=True, text=True,
                            timeout=45, check=False)
    require(result.returncode == 0 and result.stdout,
            "JDK21 javap cannot inspect official ItemStack binary")
    selected = parse_initializer(result.stdout, mapped["field"])
    report = {
        "schema_version": 1,
        "scope": "OFFICIAL_MOJANG_VANILLA_1211_ITEMSTACK_STATIC_ABI_CORROBORATION_ONLY",
        "version": VERSION,
        "official_client_sha1": client_sha,
        "official_client_size": client_size,
        "official_mapping_sha1": mapping_sha,
        "official_mapping_size": mapping_size,
        "class_path": class_path,
        "class_sha256": hashlib.sha256(raw).hexdigest(),
        "mapped_field": MOJANG_FIELD,
        "obfuscated_field": mapped["field"],
        "mapped_field_type": mapped["named_field_type"],
        "static_initializer": selected,
        "limits": {
            "neoforge_21_1_248_merged_runtime": "NOT_INSPECTED",
            "itemstack_stream_decode_method": "NOT_TRACED",
            "data_component_patch_bounds": "NOT_TRACED",
            "network_packet_size_limits": "NOT_VERIFIED",
            "nbt_depth_and_byte_limits": "NOT_VERIFIED",
            "raygun_tag_authority": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_perk_certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf8")) < MAX_REPORT_BYTES,
            "bounded Mojang evidence report size exceeded")
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--client", type=Path, required=True)
    p.add_argument("--mappings", type=Path, required=True)
    p.add_argument("--metadata", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.client, args.mappings,
                   json.loads(args.metadata.read_text(encoding="utf8")), args.javap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True,
                                      ensure_ascii=False) + "\n", encoding="utf8")
    print("OFFICIAL_CLIENT_SHA1=" + report["official_client_sha1"])
    print("OFFICIAL_MAPPING_SHA1=" + report["official_mapping_sha1"])
    print("ITEMSTACK_OBF_CLASS=" + report["class_path"])
    print("ITEMSTACK_CLASS_SHA256=" + report["class_sha256"])
    print("OPTIONAL_STREAM_CODEC_OBF_FIELD=" + report["obfuscated_field"])
    print("OPTIONAL_STREAM_CODEC_PUTSTATIC=" +
          str(report["static_initializer"]["optional_codec_putstatic_offset"]))
    for ref in report["static_initializer"]["selected_preassignment_abi"]:
        print("OPTIONAL_STREAM_CODEC_ABI_REF=" + json.dumps(ref, sort_keys=True))
    print("VANILLA_ONLY; NEOFORGE_RUNTIME_NOT_INSPECTED; NO_MUTATION")


if __name__ == "__main__":
    main()
