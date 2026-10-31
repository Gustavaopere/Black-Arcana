#!/usr/bin/env python3
"""Seal a bounded Alex's Caves contract family against one exact JAR; no runtime claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

SHA1 = "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE_BYTES = 75279314
ACTIONS = frozenset("actions/" + name + ".md" for name in (
    "sea-staff-water-bolt", "sugar-staff-peppermint-cast", "sugar-staff-hex-cast",
    "magic-conch-summon-deep-ones", "totem-possession-remote-control",
    "occult-gem-beholder-observation", "cloak-darkness-incarnate",
    "conversion-crucible-biome-conversion"))
EFFECTS = frozenset("effects/" + name + ".md" for name in (
    "irradiated", "magnetizing", "rage", "stunned", "bubbled", "deepsight",
    "darkness-incarnate", "sugar-rush"))
DREADBOW = frozenset(("equipment/dreadbow.md", "damage-types/dark-arrow.md"))
ACID = frozenset(("damage-types/acid.md",))
DESOLATE_DAGGER = frozenset(("equipment/desolate-dagger.md", "damage-types/desolate-dagger.md"))
FORSAKEN = frozenset(("damage-types/forsaken-sonic-boom.md",))
SCOPE = {"schema_version": 1, "version": "1.0.10",
         "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
         "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR", "mutating_hook": "NOT_VERIFIED",
         "physical_qa": "NOT_TESTED", "provider_universe_closed": False,
         "semantic_magic_roots": 8, "artifact_sha1": SHA1,
         "artifact_sha256": SHA256, "artifact_size_bytes": SIZE_BYTES}
EFFECT_SCOPE = {**SCOPE, "catalog_family": "MOB_EFFECTS"}
DREADBOW_SCOPE = {**SCOPE, "catalog_family": "DREADBOW_AND_DARK_ARROW"}
ACID_SCOPE = {**SCOPE, "catalog_family": "ACID_DAMAGE_CONTRACT"}
DESOLATE_DAGGER_SCOPE = {**SCOPE, "catalog_family": "DESOLATE_DAGGER_CONTRACTS"}
FORSAKEN_SCOPE = {**SCOPE, "catalog_family": "FORSAKEN_SONIC_CONTRACT"}
ADJACENT_SOURCE = {"repository": "Codx-org/AlexsCavesContinued",
                   "revision": "523308608422ab8e31974befa7111ecdf495dd37",
                   "declared_version": "1.1.1",
                   "role": "CORROBORATION_ONLY_NOT_INSTALLED_PARAMETERS"}


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def profile_spec(profile):
    """Select a literal family without changing the existing action contract."""
    require(profile in ("actions", "effects", "dreadbow", "acid", "desolate_dagger", "forsaken"), "unknown catalog profile")
    if profile == "effects":
        return EFFECT_SCOPE, EFFECTS, "effect_evidence"
    if profile == "dreadbow":
        return DREADBOW_SCOPE, DREADBOW, "contract_evidence"
    if profile == "acid":
        return ACID_SCOPE, ACID, "contract_evidence"
    if profile == "desolate_dagger":
        return DESOLATE_DAGGER_SCOPE, DESOLATE_DAGGER, "contract_evidence"
    if profile == "forsaken":
        return FORSAKEN_SCOPE, FORSAKEN, "contract_evidence"
    return SCOPE, ACTIONS, "action_evidence"


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_manifest(path):
    require(Path(path).stat().st_size <= 2_000_000, "manifest exceeds size limit")
    return json.loads(Path(path).read_text(encoding="utf8"), object_pairs_hook=unique_pairs)


def canonical(path):
    return (isinstance(path, str) and bool(path) and not any(c in path for c in "\\\x00:")
            and all(part not in {"", ".", ".."} for part in path.split("/")))


def digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def descriptor(value):
    return isinstance(value, str) and re.fullmatch(
        r"\((?:\[*(?:[BCDFIJSZ]|L[^.;\[()]+;))*\)(?:V|\[*(?:[BCDFIJSZ]|L[^.;\[()]+;))", value) is not None


def parse_javap(raw, owner):
    """Parse instructions only; numeric switch-case rows are not instructions."""
    owner = owner.removesuffix(".class").replace("/", ".")
    declarations = re.findall(
        r"^[ \t]*(?:(?:public|protected|private|abstract|final|static|strictfp|sealed|non-sealed)[ \t]+)*"
        r"(?:class|interface|enum|record)[ \t]+([^ \t<({]+)[^\r\n]*\{[ \t]*$", raw, re.M)
    require(declarations == [owner], "javap declaration owner mismatch: " + owner)
    methods, pending, current = {}, None, None
    for line in raw.splitlines():
        header = line.strip()
        if line.startswith("  ") and not line.startswith("    "):
            if header == "static {};":
                pending, current = "<clinit>", None
            elif "(" in header and header.endswith(";"):
                name = header.split("(", 1)[0].rsplit(" ", 1)[-1]
                pending = "<init>" if name in {owner, owner.rsplit(".", 1)[-1]} else name
                current = None
            elif header and not header.startswith("descriptor:"):
                pending, current = None, None
        if header.startswith("descriptor:") and pending is not None:
            current = (pending, header.split(":", 1)[1].strip())
            require(current not in methods, "duplicate method descriptor: " + str(current))
            require(descriptor(current[1]), "invalid method descriptor: " + current[1])
            methods[current], pending = {}, None
        instruction = re.fullmatch(r"\s+(\d+):\s+([a-z][a-z0-9_]*)\b(?:\s+(.*))?", line)
        if instruction and current is not None:
            offset, opcode, tail = instruction.groups()
            operand, separator, symbol = (tail or "").partition("//")
            offset = int(offset)
            require(offset not in methods[current], "duplicate instruction offset: " + str(offset))
            methods[current][offset] = (opcode, " ".join(operand.split()), symbol.strip() if separator else "")
    return methods


def validate_structure(manifest, *, profile="actions"):
    scope, roster, evidence_key = profile_spec(profile)
    require(isinstance(manifest, dict), "manifest must be an object")
    require(set(manifest) == set(scope) | {"adjacent_source", "cards", evidence_key, "classes", "resources"},
            "unexpected or missing manifest fields")
    for key, value in scope.items():
        require(type(manifest[key]) is type(value) and manifest[key] == value, "scope/identity mismatch: " + key)
    require(manifest["adjacent_source"] == ADJACENT_SOURCE, "adjacent source is not the declared corroboration snapshot")
    cards, evidence, classes, resources = (manifest[key] for key in ("cards", evidence_key, "classes", "resources"))
    require(isinstance(cards, dict) and set(cards) == roster and all(digest(h) for h in cards.values()),
            "cards must seal exactly the " + str(len(roster)) + " literal " + profile + " paths")
    require(isinstance(evidence, dict) and set(evidence) == roster,
            "evidence must cover exactly the " + str(len(roster)) + " " + profile + " cards")
    require(isinstance(classes, dict) and len(roster) <= len(classes) <= 128
            and isinstance(resources, dict) and len(resources) <= 256,
            "invalid class/resource mapping limits")
    method_classes, total_anchors = set(), 0
    for path, entry in classes.items():
        require(canonical(path) and path.startswith("com/github/alexmodguy/alexscaves/") and path.endswith(".class"),
                "noncanonical provider class path")
        require(isinstance(entry, dict) and set(entry) == {"sha256", "methods"} and digest(entry["sha256"])
                and isinstance(entry["methods"], list) and len(entry["methods"]) <= 128, "invalid class record")
        seen = set()
        for method in entry["methods"]:
            require(isinstance(method, dict) and set(method) == {"name", "descriptor", "anchors"}, "invalid method record")
            name, desc, anchors = (method[key] for key in ("name", "descriptor", "anchors"))
            require(isinstance(name, str) and re.fullmatch(r"(?:[\w$]+|<init>|<clinit>)", name)
                    and descriptor(desc), "invalid method name/descriptor")
            require((name, desc) not in seen, "duplicate method record")
            seen.add((name, desc))
            require(isinstance(anchors, list) and 1 <= len(anchors) <= 256, "method needs bounded anchors")
            offsets = set()
            for anchor in anchors:
                require(isinstance(anchor, dict) and set(anchor) == {"offset", "opcode", "operand", "symbol"}, "invalid anchor")
                offset = anchor["offset"]
                require(type(offset) is int and 0 <= offset <= 65535 and offset not in offsets, "invalid/duplicate anchor offset")
                require(isinstance(anchor["opcode"], str) and re.fullmatch(r"[a-z][a-z0-9_]*", anchor["opcode"])
                        and all(isinstance(anchor[key], str) and len(anchor[key]) <= 4096 for key in ("operand", "symbol")),
                        "invalid anchor operation")
                offsets.add(offset)
            method_classes.add(path)
            total_anchors += len(anchors)
    require(len(method_classes) >= len(roster) and total_anchors <= 8192,
            "need at least " + str(len(roster)) + " critical classes within anchor limit")
    require(all(canonical(path) and not path.endswith(("/", ".class")) and digest(h) for path, h in resources.items()),
            "invalid resource paths/hashes")
    referenced_classes, referenced_resources = set(), set()
    for card, record in evidence.items():
        require(isinstance(record, dict) and set(record) == {"classes", "resources"}, "invalid card evidence")
        for key, mapping, referenced in (("classes", classes, referenced_classes), ("resources", resources, referenced_resources)):
            paths = record[key]
            require(isinstance(paths, list) and all(isinstance(path, str) for path in paths)
                    and len(paths) == len(set(paths)) and all(path in mapping for path in paths), "unknown/duplicate evidence paths")
            referenced.update(paths)
        require(set(record["classes"]) & method_classes, "card lacks an anchored class: " + card)
    require(referenced_classes == set(classes) and referenced_resources == set(resources), "unreferenced class/resource evidence")


def validate_cards(manifest, providerroot, *, profile="actions"):
    _, roster, _ = profile_spec(profile)
    root = Path(providerroot).resolve(strict=True)
    for relative, expected in manifest["cards"].items():
        require(relative in roster and canonical(relative), "invalid card path")
        card = (root / relative).resolve(strict=True)
        require(card.is_relative_to(root) and card.is_file(), "card escapes provider root: " + relative)
        require(hashlib.sha256(card.read_bytes()).hexdigest() == expected, "stale card seal: " + relative)


def pinned_identity():
    return {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE_BYTES}


def artifact_identity(path):
    sha1, sha256, size = hashlib.sha1(), hashlib.sha256(), 0
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha1.update(chunk)
            sha256.update(chunk)
            size += len(chunk)
    return {"sha1": sha1.hexdigest(), "sha256": sha256.hexdigest(), "size_bytes": size}


def audit(jar, manifest, providerroot, javap, *, expected_identity=None, profile="actions"):
    """expected_identity is a zero-argument synthetic-test seam, never a CLI option."""
    scope, roster, _ = profile_spec(profile)
    validate_structure(manifest, profile=profile)
    validate_cards(manifest, providerroot, profile=profile)
    jar = Path(jar).resolve(strict=True)
    observed = artifact_identity(jar)
    require(observed == (expected_identity or pinned_identity)(), "exact publisher artifact identity mismatch")
    initial_stat = jar.stat()
    checked_methods = checked_anchors = 0
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member names")
        for path, expected in manifest["resources"].items():
            require(path in names, "missing resource: " + path)
            require(hashlib.sha256(archive.read(path)).hexdigest() == expected, "resource hash mismatch: " + path)
        for path, entry in manifest["classes"].items():
            require(path in names, "missing class: " + path)
            raw = archive.read(path)
            require(len(raw) >= 8 and raw[:4] == b"\xca\xfe\xba\xbe" and int.from_bytes(raw[6:8], "big") == 65,
                    "class is not Java 21 major 65: " + path)
            require(hashlib.sha256(raw).hexdigest() == entry["sha256"], "class hash mismatch: " + path)
            if not entry["methods"]:
                continue
            owner = path.removesuffix(".class").replace("/", ".")
            result = subprocess.run([str(javap), "-p", "-c", "-s", "-classpath", str(jar), owner],
                                    capture_output=True, text=True, check=False, timeout=60)
            require(result.returncode == 0, "javap failed for " + owner)
            parsed = parse_javap(result.stdout, owner)
            for method in entry["methods"]:
                key = (method["name"], method["descriptor"])
                require(key in parsed, "method ABI missing: " + owner + "." + str(key))
                for anchor in method["anchors"]:
                    expected = (anchor["opcode"], anchor["operand"], anchor["symbol"])
                    require(parsed[key].get(anchor["offset"]) == expected,
                            "instruction anchor mismatch: " + owner + "." + method["name"] + "@" + str(anchor["offset"]))
                    checked_anchors += 1
                checked_methods += 1
    final_stat = jar.stat()
    require(all(getattr(initial_stat, field) == getattr(final_stat, field)
                for field in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns"))
            and artifact_identity(jar) == observed, "artifact changed during audit")
    validate_cards(manifest, providerroot, profile=profile)
    report = {"status": "PASS", "version": "1.0.10", "artifact": observed,
            "claim_scope": scope["claim_scope"], "evidence_grade": scope["evidence_grade"],
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED", "provider_universe_closed": False,
            "semantic_magic_roots": 8, "cards_checked": len(roster), "classes_checked": len(manifest["classes"]),
            "resources_checked": len(manifest["resources"]), "methods_checked": checked_methods,
            "instruction_anchors_checked": checked_anchors}
    if "catalog_family" in scope:
        report["catalog_family"] = scope["catalog_family"]
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("jar", "manifest", "provider-root", "javap"):
        parser.add_argument("--" + flag, required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--profile", choices=("actions", "effects", "dreadbow", "acid", "desolate_dagger", "forsaken"), default="actions")
    args = parser.parse_args(argv)
    try:
        report = audit(args.jar, load_manifest(args.manifest), args.provider_root, args.javap,
                       profile=args.profile)
    except (AuditError, OSError, zipfile.BadZipFile, subprocess.SubprocessError, json.JSONDecodeError) as error:
        parser.exit(1, "audit failed: " + str(error) + "\n")
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
