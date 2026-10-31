#!/usr/bin/env python3
"""SHA-exact read-only search for Gumball producers and parameter callsites.

Publishes only bounded JVM symbolic/constant/branch windows and class/method
digests. No full method body, decompilation, runtime test or hook claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file

PROJECTILE = BASE + "server/entity/item/GumballEntity.class"
SERVER = BASE + "server/"
MAX_CANDIDATES = 125
MAX_SELECTED_CLASSES = 50
MAX_SELECTED_METHODS = 125
MAX_INSNS = 3200
MAX_HITS_PER_METHOD = 30
MAX_WINDOW_ITEMS = 23
METHOD_PATTERN = re.compile(r"([A-Za-z0-9_$<>]+)\(")
REF_PATTERN = re.compile(r"(?:GumballEntity|ACEntityRegistry\.GUMBALL:|\bGUMBALL\b)")
CONSTANT_PATTERN = re.compile(r"^(?:[ifld]const_|bipush$|sipush$|ldc(?:_w|2_w)?$)")
SUPPORT_REGISTRIES = {
    SERVER + "entity/ACEntityRegistry.class",
    SERVER + "item/ACItemRegistry.class",
}
HIT_SOURCE_FIELDS = ("offset", "opcode", "operand", "symbol")


class ProducerProbeError(ValueError):
    pass


def method_name(method):
    m = METHOD_PATTERN.search(method["header"])
    return m.group(1) if m else ""


def compact(instruction):
    return {k: instruction[k] for k in HIT_SOURCE_FIELDS}


def callsite_windows(method):
    instructions = method["instructions"]
    if not 1 <= len(instructions) <= MAX_INSNS:
        raise ProducerProbeError("unsafe selected method instruction population")
    positions = [i for i, inst in enumerate(instructions) if REF_PATTERN.search(inst["symbol"])]
    if len(positions) > MAX_HITS_PER_METHOD:
        raise ProducerProbeError("selected callsite count exceeded")
    windows = []
    for pos in positions:
        seq = instructions[max(0, pos - 10):pos + 11]
        if len(seq) > MAX_WINDOW_ITEMS:
            raise ProducerProbeError("oversize instruction window")
        windows.append({
            "at": instructions[pos]["offset"],
            "reference": compact(instructions[pos]),
            "window": [compact(x) for x in seq],
        })
    return windows


def method_row(method):
    windows = callsite_windows(method)
    if not windows:
        return None
    insns = method["instructions"]
    return {
        "name": method_name(method),
        "header": method["header"],
        "descriptor": method["descriptor"],
        "instruction_count": len(insns),
        "parsed_method_sha256": hashlib.sha256(
            json.dumps(method, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf8")
        ).hexdigest(),
        "reference_windows": windows,
        "effective_parameter_flow": "NOT_PROVEN",
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise ProducerProbeError("publisher artifact identity mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ProducerProbeError("duplicate ZIP members")
        candidates = []
        for p in names:
            if not p.startswith(SERVER) or not p.endswith(".class") or p == PROJECTILE:
                continue
            body = archive.read(p)
            if b"GumballEntity" in body or b"GUMBALL" in body:
                candidates.append((p, hashlib.sha256(body).hexdigest()))
    if not 1 <= len(candidates) <= MAX_CANDIDATES:
        raise ProducerProbeError("candidate population unbounded or missing")
    observed = []
    registry_support = []
    unselected = []
    method_total = 0
    for path, digest in sorted(candidates):
        if path in SUPPORT_REGISTRIES:
            registry_support.append({"class_path": path, "class_sha256": digest, "role": "REGISTRY_SUPPORT_NOT_PRODUCER_PROOF"})
            continue
        methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
        selected = []
        for m in methods:
            if not m["descriptor"]:
                continue
            if any(REF_PATTERN.search(i["symbol"]) for i in m["instructions"]):
                row = method_row(m)
                if row:
                    selected.append(row)
                    method_total += 1
        if selected:
            observed.append({"class_path": path, "class_sha256": digest, "methods": selected})
        else:
            unselected.append({"class_path": path, "class_sha256": digest, "disposition": "NO_EXPLICIT_TARGET_SYMBOLIC_CALLSITE"})
    if len(observed) > MAX_SELECTED_CLASSES or method_total > MAX_SELECTED_METHODS:
        raise ProducerProbeError("selected surface exceeded method/class bounds")
    if not observed:
        raise ProducerProbeError("no exact Gumball symbolic candidates identified")
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_GUMBALL_DIRECT_PRODUCER_REFERENCE_INVENTORY_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "projectile_class": PROJECTILE,
        "candidate_class_count": len(candidates),
        "selected_class_count": len(observed),
        "selected_method_count": method_total,
        "selected_classes": observed,
        "registry_support": registry_support,
        "no_selected_symbols": unselected,
        "limits": {
            "indirect_callers_reflection_mixins": "NOT_COVERED",
            "class_candidates_only": True,
            "full_bytecode_body_exported": False,
            "runtime_producers_and_initial_values": "NOT_CERTIFIED",
            "ownership_and_spawns": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False,
        },
    }



# A deliberately narrow contract: class/method digests and selected direct refs.
# Neither upstream source code nor runtime reachability is inferred.
PRODUCER_SNAPSHOT_SITES = {
    SERVER + "entity/living/GumbeeperEntity.class": {
        "tick": (385, 542, 560, 579),
        "shootGumball": (80, 265, 289, 307, 326),
    },
    SERVER + "item/ShotGumItem.class": {
        "acInventoryTick": (316, 434, 441, 448, 480, 487, 495),
    },
    SERVER + "misc/ACDamageTypes.class": {
        "causeGumballDamage": (19,),
    },
}


def strict_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ProducerProbeError("duplicate snapshot key: " + key)
        out[key] = value
    return out


def snapshot_view(observed):
    classes = []
    seen = set()
    for cls in observed["selected_classes"]:
        class_path = cls["class_path"]
        if class_path in seen:
            raise ProducerProbeError("duplicate producer class")
        seen.add(class_path)
        expected = PRODUCER_SNAPSHOT_SITES.get(class_path)
        if expected is None:
            raise ProducerProbeError("unmapped producer class")
        selected = []
        for m in cls["methods"]:
            sites = expected.get(m["name"])
            if sites is None:
                raise ProducerProbeError("unmapped producer method: " + m["name"])
            refs = []
            for at in sites:
                matches = [w["reference"] for w in m["reference_windows"] if w["at"] == at]
                if len(matches) != 1:
                    raise ProducerProbeError("missing/duplicate producer anchor: " + m["name"] + ":" + str(at))
                refs.append(matches[0])
            selected.append({
                **{k: m[k] for k in ("name", "descriptor", "instruction_count", "parsed_method_sha256")},
                "anchors": refs,
            })
        if set(m["name"] for m in cls["methods"]) != set(expected):
            raise ProducerProbeError("unexpected or missing selected methods")
        classes.append({"class_path": class_path, "class_sha256": cls["class_sha256"], "methods": selected})
    if set(PRODUCER_SNAPSHOT_SITES) != seen:
        raise ProducerProbeError("unexpected or missing selected classes")
    return {
        **{k: observed[k] for k in (
            "schema_version", "scope", "artifact", "projectile_class",
            "candidate_class_count", "selected_class_count", "selected_method_count",
            "registry_support", "no_selected_symbols"
        )},
        "selected_classes": classes,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--snapshot")
    args = parser.parse_args()
    output = audit(args.jar, args.javap)
    if args.snapshot:
        expected = json.loads(Path(args.snapshot).read_text(encoding="utf8"), object_pairs_hook=strict_pairs)
        if snapshot_view(output) != expected:
            raise ProducerProbeError("SHA-exact Gumball producer evidence drift")
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf8")
    print("GUMBALL_PRODUCERS_1010_BEGIN")
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    print("GUMBALL_PRODUCERS_1010_END")
    print("selected_classes=" + str(output["selected_class_count"]) +
          " selected_methods=" + str(output["selected_method_count"]) +
          " STATIC_INVENTORY_ONLY")


if __name__ == "__main__":
    main()
