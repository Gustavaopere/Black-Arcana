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
MAX_REPORT_BYTES = 32000


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




def named_vanilla_classes(mappings_text, obfuscated_names):
    """Resolve exact class symbols from the same official Mojang mapping input."""
    target = set(obfuscated_names)
    found = {}
    for line in mappings_text.splitlines():
        match = CLASS_MAPPING.match(line)
        if match and match.group(2) in target:
            require(match.group(2) not in found,
                    "ambiguous Mojang obfuscated class mapping")
            found[match.group(2)] = match.group(1)
    require(set(found) == target, "missing Mojang mapped bytecode class")
    return found


def codec_class_from_initializer(initializer):
    """Bounded JVM constructor nearest the pinned codec field assignment."""
    items = initializer["selected_preassignment_abi"]
    offset = initializer["optional_codec_putstatic_offset"]
    created = [
        row for row in items
        if row["opcode"] == "new" and
        0 < offset - row["offset"] <= 18 and
        re.fullmatch(r"class [A-Za-z0-9_/$]+", row["symbol"])
    ]
    require(len(created) == 1, "unresolved/ambiguous vanilla optional codec implementation")
    return created[0]["symbol"].split(" ", 1)[1]


def inspect_codec_class(client, javap_bin, outer_owner, codec_owner):
    """Selected ABI of the assigned codec class; no full method reproduction."""
    require(codec_owner.startswith(outer_owner + "$"),
            "assigned vanilla codec class is not an ItemStack inner class")
    with zipfile.ZipFile(client) as jar:
        data = jar.read(codec_owner + ".class")
        require(len(data) >= 8 and data[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(data[6:8], "big") == 65,
                "codec inner classfile version drift")
    cmd = [str(javap_bin), "-classpath", str(client), "-c", "-p", "-s",
           codec_owner.replace("/", ".")]
    result = subprocess.run(cmd, capture_output=True, text=True,
                            timeout=45, check=False)
    require(result.returncode == 0 and result.stdout and
            len(result.stdout) <= MAX_JAVAP_BYTES,
            "cannot inspect bounded vanilla anonymous codec implementation")
    # Existing parser exports bytecode offsets, method signatures and symbols only.
    from alexscaves_1010_damage_consumer_probe import parse_methods
    from alexscaves_1010_raygun_receiver_probe import method_name
    methods = parse_methods(result.stdout)
    require(2 <= len(methods) <= 12,
            "unbounded/missing optional codec implementation method roster")
    out = []
    for m in methods:
        ins = m["instructions"]
        require(0 <= len(ins) <= 350, "codec method instruction budget exceeded")
        selected = [
            {"offset": x["offset"], "opcode": x["opcode"],
             "operand": x["operand"][:40] if x["opcode"].startswith(("if", "goto")) else "",
             "symbol": x["symbol"][:300]}
            for x in ins if x["opcode"].startswith(("invoke", "if", "goto")) or
            x["opcode"] in ("getstatic", "putstatic", "getfield", "putfield",
                            "new", "instanceof", "checkcast", "bipush", "sipush")
        ]
        require(len(selected) <= 80, "codec selected method reference budget exceeded")
        out.append({
            "name": method_name(m), "descriptor": m["descriptor"],
            "instruction_count": len(ins),
            "selected_refs": selected
        })
    return {
        "class_path": codec_owner + ".class",
        "class_sha256": hashlib.sha256(data).hexdigest(),
        "declared_methods": len(methods),
        "methods": out
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
    official_mappings_text = Path(mappings).read_text(encoding="utf-8")
    mapped = map_itemstack(official_mappings_text)
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
    codec_owner = codec_class_from_initializer(selected)
    codec = inspect_codec_class(client, javap_bin, dotted.replace(".", "/"),
                                codec_owner)
    class_map = named_vanilla_classes(official_mappings_text, ("wk", "jm", "kn"))
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
        "assigned_codec_implementation": codec,
        "selected_obfuscated_class_names": class_map,
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



OFFICIAL_ITEMSTACK_SHA256 = "a34b9141828bd62fa74ad6a5d3b9b47a81df18b4a86866827c8f73d3ab97f901"
OFFICIAL_OPTIONAL_CODEC_SHA256 = "b67408499e6a5f8edd5120e1bffa67c6e0c50f68658d5d098c4813beebbadfc2"
OFFICIAL_MAPPING_SHA1 = "2244b6f072256667bcd9a73df124d6c58de77992"
EXPECTED_OWNER_MAP = {
    "jm": "net.minecraft.core.Holder",
    "kn": "net.minecraft.core.component.DataComponentPatch",
    "wk": "net.minecraft.network.RegistryFriendlyByteBuf"
}
EXPECTED_CODEC_METHODS = (
    ("cuq$1", "()V"),
    ("a", "(Lwk;)Lcuq;"),
    ("a", "(Lwk;Lcuq;)V"),
    ("encode", "(Ljava/lang/Object;Ljava/lang/Object;)V"),
    ("decode", "(Ljava/lang/Object;)Ljava/lang/Object;")
)
CORE_CODEC_ABI = (
    ("a", "(Lwk;)Lcuq;", 1, "invokevirtual", "wk.l:()I", ""),
    ("a", "(Lwk;)Lcuq;", 6, "ifgt", "", "13"),
    ("a", "(Lwk;)Lcuq;", 9, "getstatic", "Field cuq.l:", ""),
    ("a", "(Lwk;)Lcuq;", 17, "invokeinterface", "yx.decode:", ""),
    ("a", "(Lwk;)Lcuq;", 26, "getstatic", "Field kn.c:", ""),
    ("a", "(Lwk;)Lcuq;", 30, "invokeinterface", "yx.decode:", ""),
    ("a", "(Lwk;Lcuq;)V", 4, "ifeq", "", "14"),
    ("a", "(Lwk;Lcuq;)V", 9, "invokevirtual", "wk.c:(I)", ""),
    ("a", "(Lwk;Lcuq;)V", 19, "invokevirtual", "wk.c:(I)", ""),
    ("a", "(Lwk;Lcuq;)V", 23, "getstatic", "Field a:Lyx;", ""),
    ("a", "(Lwk;Lcuq;)V", 31, "invokeinterface", "yx.encode:", ""),
    ("a", "(Lwk;Lcuq;)V", 36, "getstatic", "Field kn.c:", ""),
    ("a", "(Lwk;Lcuq;)V", 47, "invokeinterface", "yx.encode:", "")
)
EXPECTED_STATUS = {
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


def snapshot_projection(report):
    """Pin exact Mojang vanilla artifact and selected codec semantics; not NeoForge."""
    require(report["scope"] ==
            "OFFICIAL_MOJANG_VANILLA_1211_ITEMSTACK_STATIC_ABI_CORROBORATION_ONLY",
            "changed runtime authority scope")
    require(report["official_client_sha1"] == CLIENT_SHA1 and
            report["official_mapping_sha1"] == OFFICIAL_MAPPING_SHA1,
            "official vanilla artifact or mappings drift")
    require(report["class_path"] == "cuq.class" and
            report["class_sha256"] == OFFICIAL_ITEMSTACK_SHA256 and
            report["mapped_field"] == MOJANG_FIELD and
            report["obfuscated_field"] == "h",
            "official vanilla ItemStack identity/field drift")
    initializer = report["static_initializer"]
    require(initializer["optional_codec_putstatic_offset"] == 127,
            "vanilla optional codec assignment drift")
    symbols = initializer["selected_preassignment_abi"]
    for off, opcode, fragment in (
        (120, "new", "class cuq$1"),
        (124, "invokespecial", "cuq$1"),
        (127, "putstatic", "Field h:"),
    ):
        matches = [x for x in symbols if x["offset"] == off]
        require(len(matches) == 1 and matches[0]["opcode"] == opcode and
                fragment in matches[0]["symbol"],
                "vanilla optional codec initializer ABI drift")
    require(report["selected_obfuscated_class_names"] == EXPECTED_OWNER_MAP,
            "official Mojang mapped component/buffer owners drift")
    impl = report["assigned_codec_implementation"]
    require(impl["class_path"] == "cuq$1.class" and
            impl["class_sha256"] == OFFICIAL_OPTIONAL_CODEC_SHA256,
            "official anonymous ItemStack codec SHA drift")
    methods = impl["methods"]
    require(tuple((m["name"], m["descriptor"]) for m in methods) ==
            EXPECTED_CODEC_METHODS, "vanilla codec method signatures/order drift")
    anchors = []
    for method_name, descriptor, offset, opcode, fragment, operand in CORE_CODEC_ABI:
        m = next(x for x in methods
                 if x["name"] == method_name and x["descriptor"] == descriptor)
        hits = [x for x in m["selected_refs"] if x["offset"] == offset]
        require(len(hits) == 1 and hits[0]["opcode"] == opcode
                and fragment in hits[0]["symbol"] and
                hits[0]["operand"] == operand,
                "vanilla codec branch or delegate ABI drift")
        anchors.append({
            "method": method_name, "descriptor": descriptor, **hits[0]
        })
    require(report["limits"] == EXPECTED_STATUS,
            "vanilla codec falsely promoted NeoForge or Raygun status")
    return {
        **{k: report[k] for k in (
            "schema_version", "scope", "version", "official_client_sha1",
            "official_client_size", "official_mapping_sha1",
            "official_mapping_size", "class_path", "class_sha256",
            "mapped_field", "obfuscated_field", "mapped_field_type")},
        "codec_class_path": impl["class_path"],
        "codec_class_sha256": impl["class_sha256"],
        "codec_method_signatures": [
            {"name": m["name"], "descriptor": m["descriptor"]}
            for m in methods
        ],
        "codec_initializer_putstatic_offset":
            initializer["optional_codec_putstatic_offset"],
        "selected_obfuscated_class_names": report["selected_obfuscated_class_names"],
        "selected_vanilla_codec_abi": anchors,
        "limits": report["limits"]
    }


def verify_snapshot(report, snapshot):
    require(snapshot_projection(report) == snapshot,
            "sealed Mojang vanilla optional codec evidence drift")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--client", type=Path, required=True)
    p.add_argument("--mappings", type=Path, required=True)
    p.add_argument("--metadata", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--snapshot", type=Path)
    args = p.parse_args()
    report = audit(args.client, args.mappings,
                   json.loads(args.metadata.read_text(encoding="utf8")), args.javap)
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
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
    impl = report["assigned_codec_implementation"]
    print("OPTIONAL_STREAM_CODEC_CLASS=" + impl["class_path"])
    print("OPTIONAL_STREAM_CODEC_CLASS_SHA256=" + impl["class_sha256"])
    for obf, named in report["selected_obfuscated_class_names"].items():
        print("OPTIONAL_STREAM_CODEC_MAPPED_CLASS=" + obf + " -> " + named)
    for method in impl["methods"]:
        print("OPTIONAL_STREAM_CODEC_METHOD=" + method["name"] + " " + method["descriptor"])
        for ref in method["selected_refs"]:
            print("OPTIONAL_STREAM_CODEC_METHOD_REF=" + method["name"] + " " +
                  json.dumps(ref, sort_keys=True))
    print("VANILLA_ONLY; NEOFORGE_RUNTIME_NOT_INSPECTED; NO_MUTATION")


if __name__ == "__main__":
    main()
