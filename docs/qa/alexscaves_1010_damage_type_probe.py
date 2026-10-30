#!/usr/bin/env python3
"""Read-only 1.0.10 Alex's Caves damage-type resource probe, NOT a behavioral certificate."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE = 75279314
IDS = (
    "acid", "dark_arrow", "desolate_dagger", "forsaken_sonic_boom",
    "gumball", "intentional_game_design", "nuke", "radiation",
    "raygun", "spirit_dinosaur", "tremorzilla_beam",
)
PREFIX = "data/alexscaves/damage_type/"
TAG_RE = re.compile(r"data/([a-z0-9_.-]+)/tags/damage_type/([a-z0-9_./-]+)\.json\Z")


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def decode_resource(archive, name):
    info = archive.getinfo(name)
    if info.file_size > 16384:
        raise ValueError("oversized resource: " + name)
    data = archive.read(info)
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "json": json.loads(data.decode("utf-8"), object_pairs_hook=strict_pairs),
    }


def extract(archive):
    names = archive.namelist()
    if len(names) != len(set(names)):
        raise ValueError("duplicate ZIP members")
    actual = {
        name for name in names if name.startswith(PREFIX) and name.endswith(".json")
    }
    expected = {PREFIX + item + ".json" for item in IDS}
    if actual != expected:
        raise ValueError("damage type identity set differs: missing="
                         + str(sorted(expected - actual)) + " extra=" + str(sorted(actual - expected)))
    damage = {}
    for item in IDS:
        record = decode_resource(archive, PREFIX + item + ".json")
        if not isinstance(record["json"], dict):
            raise ValueError("damage type root is not an object: " + item)
        damage[item] = record
    tags = {}
    for name in sorted(names):
        match = TAG_RE.fullmatch(name)
        if not match:
            continue
        if len(tags) >= 500:
            raise ValueError("tag inventory limit exceeded")
        record = decode_resource(archive, name)
        value = record["json"]
        if not isinstance(value, dict) or not isinstance(value.get("values", []), list):
            raise ValueError("malformed damage type tag: " + name)
        tags[match.group(1) + ":" + match.group(2)] = {"path": name, **record}
    # Membership below records direct JSON entries only: tags can be overridden
    # by datapacks or point to other tags. No resolved runtime membership is inferred.
    direct = {item: [] for item in IDS}
    for tag, record in tags.items():
        for member in record["json"].get("values", []):
            value = member if isinstance(member, str) else (
                member.get("id") if isinstance(member, dict) else None)
            if not isinstance(value, str):
                continue
            for item in IDS:
                if value == "alexscaves:" + item:
                    direct[item].append(tag)
    return {
        "scope": "EXACT_ARTIFACT_RESOURCE_ONLY_NOT_CONSUMER_OR_RUNTIME",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "bytes": SIZE},
        "damage_types": damage,
        "damage_type_tags": tags,
        "direct_tag_entries": direct,
        "consumer_bytecode": "NOT_AUDITED",
        "mutating_hooks": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "provider_universe_closed": False,
    }


def audit(path):
    path = Path(path)
    sha1, sha256, size = hashlib.sha1(), hashlib.sha256(), 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            sha1.update(chunk)
            sha256.update(chunk)
            size += len(chunk)
    if (sha1.hexdigest(), sha256.hexdigest(), size) != (SHA1, SHA256, SIZE):
        raise ValueError("publisher artifact hash/size mismatch")
    with zipfile.ZipFile(path, "r") as archive:
        return extract(archive)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = audit(args.jar)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    # Delimit machine-readable evidence in CI logs for follow-up document authoring.
    print("ALEXSCAVES_DAMAGE_1010_BEGIN")
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    print("ALEXSCAVES_DAMAGE_1010_END")
    print("Exactly", len(result["damage_types"]), "damage type JSONs and",
          len(result["damage_type_tags"]), "damage-type tag JSONs inspected; no Java consumer claim.")


if __name__ == "__main__":
    main()
