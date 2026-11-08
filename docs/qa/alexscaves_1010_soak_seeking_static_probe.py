#!/usr/bin/env python3
"""Read-only SHA-exact discovery of Alex's Caves 1.0.10 Soak Seeking.

Individual enchantment evidence, reusing the certified Sea Staff/Water Bolt
bytecode as an independently checked baseline. No mutation, no gameplay QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

CATALOG = Path("wiki/modpack-catalog/providers/✅-alexs-caves-continued")
BASELINE = CATALOG / "EXACT-TECHNICAL-CONTRACTS-1.0.10.json"
ENCH = "data/alexscaves/enchantment/soak_seeking.json"
TAG = "data/alexscaves/tags/item/enchantable/sea_staff.json"
EN = "assets/alexscaves/lang/en_us.json"
PT = "assets/alexscaves/lang/pt_br.json"
OWNER = BASE + "server/item/SeaStaffItem.class"
BOLT = BASE + "server/entity/item/WaterBoltEntity.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
CONSUMERS = {OWNER: ("use",), BOLT: ("tick", "onRicochetHit", "damageMobs")}
SCAN = (
    "SOAK_SEEKING", "enchantLevel", "seekAmount", "setArcingTowards",
    "getArcingTowards", "tickCount", "dieIn", "ricochet", "setDeltaMovement",
    "getDeltaMovement", "getOwner", "hurtAndBreak", "addFreshEntity",
    "Float", "double 0.3d", "float 0.3f", "float 0.2f",
    "float 0.85f", "float 3.0f", "getTarget", "distanceTo",
)
MAX_BYTES = 80000


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_anchors(method: dict, reference: dict) -> int:
    """All previously certified anchors must survive verbatim in exact JVM."""
    require(method["descriptor"] == reference["descriptor"], "descriptor drift")
    rows = {r["offset"]: r for r in method["instructions"]}
    anchors = reference["anchors"]
    require(bool(anchors), "missing independent anchors")
    for anchor in anchors:
        row = rows.get(anchor["offset"])
        require(row is not None, "missing anchor offset")
        require(row["opcode"] == anchor["opcode"], "anchor opcode drift")
        require(" ".join(row["operand"].split()) ==
                " ".join(anchor["operand"].split()), "anchor operand drift")
        require(row["symbol"] == anchor["symbol"], "anchor symbol drift")
    return len(anchors)


def choose_instructions(method: dict) -> list[dict]:
    rows = method["instructions"]
    require(1 <= len(rows) <= 2000, "invalid method length")
    positions = [i for i, r in enumerate(rows)
                 if any(token in r["symbol"] for token in SCAN)]
    chosen = set(range(min(5, len(rows))))
    chosen.update(range(max(0, len(rows) - 5), len(rows)))
    for i in positions[:45]:
        chosen.update(range(max(0, i - 3), min(len(rows), i + 4)))
    # Bytecode slices only: no third-party implementations reproduced.
    require(len(chosen) <= 350, "bounded JVM extract exceeded")
    return [{k: rows[i][k] for k in ("offset", "opcode", "operand", "symbol")}
            for i in sorted(chosen)]


def discover(jar: Path, javap_bin: str, prior: Path = BASELINE) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "wrong JAR: physical publisher SHA/size mismatch")
    baseline_raw = prior.read_bytes()
    baseline = json.loads(baseline_raw)
    require((baseline["artifact_sha1"], baseline["artifact_sha256"],
             baseline["artifact_size_bytes"]) == (SHA1, SHA256, SIZE),
            "existing Sea Staff baseline does not match physical JAR")
    require(baseline["version"] == "1.0.10", "baseline version drift")
    require(baseline["resources"][ENCH] ==
            "cfec967d084e9dc3870b90bc05d62375524af447ae280aa7fea63458e644b66b",
            "preexisting Soak Seeking resource SHA drift")
    with zipfile.ZipFile(jar) as z:
        all_names = z.namelist()
        require(len(all_names) == len(set(all_names)), "duplicate ZIP entry")
        require(all(p in all_names for p in
                    (ENCH, TAG, EN, PT, OWNER, BOLT, REG)), "missing JAR material")
        classes = [p for p in all_names if
                   p.startswith(BASE) and p.endswith(".class")]
        require(100 <= len(classes) <= 3000, "provider class census out of scope")
        direct = sorted(p for p in classes if b"SOAK_SEEKING" in z.read(p))
        require(OWNER in direct and REG in direct and len(direct) <= 12,
                "unexpected direct SOAK_SEEKING class consumers")
        resources = {p: {"size_bytes": len(z.read(p)),
                         "sha256": sha256(z.read(p))}
                     for p in (ENCH, TAG, EN, PT)}
        require(resources[ENCH]["sha256"] == baseline["resources"][ENCH],
                "installed enchantment resource drift")
        require(resources[TAG]["sha256"] == baseline["resources"][TAG],
                "installed Sea Staff tag drift")
        enchant = json.loads(z.read(ENCH))
        item_tag = json.loads(z.read(TAG))
        translations = {}
        for language, filename in (("en_us", EN), ("pt_br", PT)):
            language_data = json.loads(z.read(filename))
            translations[language] = {
                k: v for k, v in language_data.items()
                if k.startswith("enchantment.alexscaves.soak_seeking")
            }
        require(enchant["max_level"] == 3, "unexpected maximum level")
        require(enchant["supported_items"] == "#alexscaves:enchantable/sea_staff",
                "Soak Seeking supported item tag drift")
        require("alexscaves:sea_staff" in item_tag.get("values", []),
                "tag no longer contains the Sea Staff")
        hashes = {path: sha256(z.read(path)) for path in (OWNER, BOLT, REG)}
        for path in (OWNER, BOLT):
            require(hashes[path] == baseline["classes"][path]["sha256"],
                    "prior static class fingerprint drift: " + path)
    methods = {}
    for class_path, names in CONSUMERS.items():
        parsed = parse_methods(javap(javap_bin, jar,
                                     class_path[:-6].replace("/", ".")))
        prior_methods = baseline["classes"][class_path]["methods"]
        for method_name in names:
            matches = [m for m in parsed if name_of(m) == method_name]
            require(len(matches) == 1, "method missing/overloaded: " + method_name)
            method = matches[0]
            refs = [r for r in prior_methods if
                    r["name"] == method_name and
                    r["descriptor"] == method["descriptor"]]
            require(len(refs) == 1, "missing uniquely matched prior contract")
            anchor_count = verify_anchors(method, refs[0])
            symbols = [r["symbol"] for r in method["instructions"]]
            if class_path == OWNER:
                require(any("SOAK_SEEKING" in s for s in symbols),
                        "Sea Staff no longer reads Soak Seeking")
                require(any("seekAmount" in s for s in symbols),
                        "Sea Staff no longer assigns homing factor")
            if class_path == BOLT and method_name == "tick":
                require(any("seekAmount" in s for s in symbols),
                        "Water Bolt no longer consumes the homing factor")
            methods[class_path + "#" + method_name] = {
                "descriptor": method["descriptor"],
                "instructions_total": len(method["instructions"]),
                "method_sha256": digest_method(method),
                "independent_anchors_checked": anchor_count,
                "bounded_instructions": choose_instructions(method),
            }
    report = {
        "schema_version": 1,
        "scope": "SOAK_SEEKING_SHA_EXACT_READONLY_DISCOVERY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "prior_evidence_sha256": sha256(baseline_raw),
        "class_census": {"scanned": len(classes), "direct_token_hits": direct},
        "class_sha256": hashes,
        "resources": resources,
        "enchantment_json": enchant,
        "tag_json": item_tag,
        "translations": translations,
        "methods": methods,
        "limits": {"mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
                   "mutation": "NO_MUTATION", "provider_closed": False,
                   "engine_final_results": "NOT_VERIFIED",
                   "loaded_datapacks": "NOT_VERIFIED"},
    }
    require(len(json.dumps(report).encode("utf-8")) <= MAX_BYTES,
            "discovery exceeds clean-room size budget")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--prior", type=Path, default=BASELINE)
    parser.add_argument("--seal", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = discover(args.jar, args.javap, args.prior)
    # Keep a reviewable single-line artifact in workflow logs for handoff.
    print("SOAK_SEEKING_DISCOVERY_JSON=" +
          json.dumps(report, separators=(",", ":"), ensure_ascii=False))
    if args.seal:
        require(json.loads(args.seal.read_text(encoding="utf-8")) == report,
                "individual publisher seal drift")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
    print("SOAK_SEEKING_STATUS=READONLY_NO_MUTATION")


if __name__ == "__main__":
    main()
