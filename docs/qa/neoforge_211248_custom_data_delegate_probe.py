#!/usr/bin/env python3
"""Read-only discovery of delegated CustomData/NBT stream boundaries.

Authority: the exact NeoForge 21.1.248 *distributed* server JAR, not the
fully ModLauncher-transformed installed modpack. No security conclusion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import parse_methods
from alexscaves_1010_raygun_receiver_probe import method_name
from alexscaves_1010_raygun_receiver_identity_probe import digest_method
from neoforge_211248_itemstack_server_codec_probe import (
    PINNED_SERVER_JAR_SHA256, sha256_file,
)

EXPECTED_SERVER_BYTES = 5675624
PINNED_SRG_JAR_SHA256 = "26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71"
MAX_CLASS_BYTES = 750000
MAX_JAVAP_BYTES = 3000000
MAX_METHODS = 850
MAX_SELECTED_METHODS = 24
MAX_REFS_PER_METHOD = 50
MAX_TOTAL_REFS = 160
MAX_REPORT_BYTES = 125000
CLASS_PATHS = {
    "custom_data": "net/minecraft/world/item/component/CustomData.class",
    "data_components": "net/minecraft/core/component/DataComponents.class",
    "byte_buf_codecs": "net/minecraft/network/codec/ByteBufCodecs.class",
}
CUES = (
    "CUSTOM_DATA", "custom_data", "CustomData", "COMPOUND_TAG",
    "CompoundTag", "readNbt", "writeNbt", "NbtAccounter",
    "readAnySizeNbt", "readNbt", "NBT", "unbounded", "limit",
)
REFERENCE_OPS = {
    "getstatic", "putstatic", "getfield", "putfield", "new",
    "ldc", "ldc_w", "bipush", "sipush", "checkcast",
}

class DelegatedCodecProbeError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise DelegatedCodecProbeError(message)


def interesting_instruction(i):
    """Keep only the selected JVM symbolic boundary; no full bytecode export."""
    return (
        i["opcode"].startswith("invoke")
        or i["opcode"] in REFERENCE_OPS
    ) and any(term.lower() in i["symbol"].lower() for term in CUES)


def selected_method(m):
    instructions = m["instructions"]
    selected_offsets = {
        i["offset"] for i in instructions if interesting_instruction(i)
    }
    # Collect the nearby literal operands passed to NbtAccounter.create(J).
    # This documents compiled arguments, never a validated packet limit.
    for index, i in enumerate(instructions):
        if "NbtAccounter.create:" in i["symbol"]:
            for prior in instructions[max(0, index-3):index]:
                selected_offsets.add(prior["offset"])
    refs = [
        {"offset": i["offset"], "opcode": i["opcode"],
         "operand": i["operand"][:55], "symbol": i["symbol"][:280]}
        for i in instructions if i["offset"] in selected_offsets
    ]
    require(len(refs) <= MAX_REFS_PER_METHOD,
            "delegated method reference budget exceeded")
    require(len({i["offset"] for i in m["instructions"]})
            == len(m["instructions"]), "duplicate JVM offset")
    return {
        "name": method_name(m), "descriptor": m["descriptor"],
        "method_sha256": digest_method(m),
        "instruction_count": len(m["instructions"]),
        "matching_references": refs,
    }


def snapshot_limits():
    return {
        "actual_delegated_nbt_byte_limit": "NOT_VERIFIED",
        "actual_delegated_nbt_depth_limit": "NOT_VERIFIED",
        "custom_data_value_sanitization": "NOT_VERIFIED",
        "raygun_entity_authorization": "NOT_VERIFIED",
        "actual_modlauncher_transformed_class": "NOT_OBSERVED",
        "physical_qa": "NOT_TESTED",
        "mutating_hook": "NOT_VERIFIED",
        "static_perk_certification": "NOT_CERTIFIED",
        "mutation": "NO_MUTATION",
    }


def verify_safe_report(report):
    require(report.get("scope")
            == "NEOFORGE_211248_DISTRIBUTED_CUSTOM_DATA_DELEGATE_DISCOVERY_ONLY",
            "discovery authority scope changed")
    require(report.get("limits") == snapshot_limits(),
            "unsupported delegated limit or security promotion")
    require(report.get("artifact") == {
        "server_jar_sha256": PINNED_SERVER_JAR_SHA256,
        "server_jar_bytes": EXPECTED_SERVER_BYTES,
        "server_srg_jar_sha256": PINNED_SRG_JAR_SHA256,
    }, "distribution identity drift")
    require(set(report.get("classes", {})) == set(CLASS_PATHS),
            "delegated class inventory incomplete")
    return True



def choose_archive(path, overlay_names, srg_names):
    """Patched NeoForge overlay takes precedence over the exact SRG library."""
    if path in overlay_names:
        return "NEOFORGE_OVERLAY"
    if path in srg_names:
        return "INSTALLED_MINECRAFT_SRG"
    return "NOT_FOUND_IN_BOTH_INSTALLED_ARCHIVES"


def audit(jar: Path, javap_bin: str, srg_jar: Path | None = None):
    digest, size = sha256_file(jar)
    require(digest == PINNED_SERVER_JAR_SHA256
            and size == EXPECTED_SERVER_BYTES,
            "official NeoForge server distribution SHA/size drift")
    require(srg_jar is not None, "exact server SRG jar required")
    srg_digest, srg_size = sha256_file(srg_jar)
    require(srg_digest == PINNED_SRG_JAR_SHA256 and srg_size > 0,
            "official installed SRG library SHA drift")
    class_binaries = {}
    sources = {}
    with zipfile.ZipFile(jar) as overlay, zipfile.ZipFile(srg_jar) as srg:
        overlay_names = overlay.namelist()
        srg_names = srg.namelist()
        require(len(overlay_names) == len(set(overlay_names))
                and len(srg_names) == len(set(srg_names)),
                "duplicate class archive member")
        for key, path in CLASS_PATHS.items():
            source = choose_archive(path, overlay_names, srg_names)
            sources[key] = source
            if source == "NEOFORGE_OVERLAY":
                blob = overlay.read(path)
            elif source == "INSTALLED_MINECRAFT_SRG":
                blob = srg.read(path)
            else:
                blob = None
            if blob is not None:
                require(8 <= len(blob) <= MAX_CLASS_BYTES
                        and blob[:4] == b"\xca\xfe\xba\xbe"
                        and int.from_bytes(blob[6:8], "big") == 65,
                        "untrusted delegated classfile: " + path)
            class_binaries[key] = blob

    classes = {}
    for key, path in CLASS_PATHS.items():
        if class_binaries[key] is None:
            classes[key] = {
                "class_path": path, "source_archive": sources[key],
                "class_sha256": None, "method_count": 0,
                "matching_method_count": 0, "matching_methods": [],
            }
            continue
        owner = path[:-6].replace("/", ".")
        classpath = str(jar) + ":" + str(srg_jar)
        run = subprocess.run(
            [str(javap_bin), "-classpath", classpath, "-c", "-p", "-s", owner],
            capture_output=True, text=True, timeout=65, check=False,
        )
        require(run.returncode == 0
                and 100 < len(run.stdout) <= MAX_JAVAP_BYTES,
                "bounded installed-class javap failed: " + path)
        methods = parse_methods(run.stdout)
        require(1 <= len(methods) <= MAX_METHODS,
                "delegated class method budget exceeded: " + path)
        signatures = [(method_name(m), m["descriptor"]) for m in methods]
        require(len(set(signatures)) == len(signatures),
                "duplicate delegated JVM signature: " + path)
        matching = []
        for m in methods:
            if any(interesting_instruction(i) for i in m["instructions"]):
                matching.append(selected_method(m))
        require(len(matching) <= MAX_SELECTED_METHODS,
                "delegated matching-method budget exceeded: " + path)
        classes[key] = {
            "class_path": path,
            "source_archive": sources[key],
            "class_sha256": hashlib.sha256(class_binaries[key]).hexdigest(),
            "method_count": len(methods),
            "matching_method_count": len(matching),
            "matching_methods": matching,
        }

    require(sum(len(m["matching_references"])
                for c in classes.values()
                for m in c["matching_methods"]) <= MAX_TOTAL_REFS,
            "total delegated symbolic references budget exceeded")
    report = {
        "schema_version": 1,
        "scope": "NEOFORGE_211248_DISTRIBUTED_CUSTOM_DATA_DELEGATE_DISCOVERY_ONLY",
        "artifact": {
            "server_jar_sha256": digest,
            "server_jar_bytes": size,
            "server_srg_jar_sha256": srg_digest,
        },
        "classes": classes,
        "limits": snapshot_limits(),
    }
    verify_safe_report(report)
    require(len(json.dumps(report, sort_keys=True).encode()) <= MAX_REPORT_BYTES,
            "delegated discovery report size exceeded")
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--srg-jar", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.jar, args.javap, args.srg_jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf8",
    )
    for label, entry in report["classes"].items():
        print("DELEGATED_CLASS=" + label + " SOURCE=" + entry["source_archive"]
              + " SHA256=" + (entry["class_sha256"] or "NOT_PRESENT")
              + " METHODS=" + str(entry["method_count"])
              + " MATCHED=" + str(entry["matching_method_count"]))
        for method in entry["matching_methods"]:
            print("DELEGATED_METHOD=" + label + " " + method["name"]
                  + " " + method["descriptor"] + " SHA256="
                  + method["method_sha256"])
            for ref in method["matching_references"]:
                print("DELEGATED_SYMBOL=" + label + " "
                      + json.dumps(ref, sort_keys=True))
    print("DISTRIBUTION_ONLY; DELEGATED_LIMITS_NOT_CERTIFIED; NO_MUTATION")


if __name__ == "__main__":
    main()
