#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 Spell Lasting -> Sugar Staff Hex static probe.

Clean-room interoperability evidence: resource/class hashes, prior-JVM anchor
checks, selected method digests and bounded call-site witnesses only.
No provider code is distributed; no hooks, effective runtime, or QA certified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, sha_file, javap, parse_methods,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

CATALOG = Path("wiki/modpack-catalog/providers/✅-alexs-caves-continued")
PRIOR = CATALOG / "EXACT-TECHNICAL-CONTRACTS-1.0.10.json"
ENCH = "data/alexscaves/enchantment/spell_lasting.json"
TAG = "data/alexscaves/tags/item/enchantable/sugar_staff.json"
LANG_EN = "assets/alexscaves/lang/en_us.json"
LANG_PT = "assets/alexscaves/lang/pt_br.json"
ITEM = BASE + "server/item/SugarStaffItem.class"
HEX = BASE + "server/entity/item/SugarStaffHexEntity.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
SHA_ITEM = "d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f"
SHA_HEX = "39f8d11595654ccebcb78540a2772106f0ae30507490570ac6b2cbe28de8e89c"
SHA_ENCH = "839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc"
SHA_TAG = "eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc"
FOCUS = {
    ITEM: {"use", "isEnchantable", "getEnchantmentValue"},
    HEX: {"<init>", "defineSynchedData", "tick", "hurtEntities",
          "getLifespan", "setLifespan", "getDespawnsIn",
          "setDespawnsIn", "getOwner", "getDimensions",
          "addAdditionalSaveData", "readAdditionalSaveData"},
}
PIVOTS = {
    ITEM: ("SPELL_LASTING", "setLifespan", "HUMUNGOUS_HEX",
           "addCooldown", "hurtAndBreakUsedHand", "isShiftKeyDown",
           "addFreshEntity", "float 0.25f"),
    HEX: ("Lifespan", "DespawnsIn", "Owner", "getLifespan",
          "setLifespan", "getOwner", "discard", "hurtEntities",
          "indirectMagic", "getEntitiesOfClass", "isClientSide",
          "setHexScale", "getHexScale", "getDimensions", "noPhysics"),
}
MAX_JVM_ROWS = 215
MAX_REPORT_BYTES = 95000


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relevant_windows(method: dict, cls: str) -> list[dict]:
    ins = method["instructions"]
    require(0 < len(ins) <= 1800, "empty or unbounded method")
    offsets = [r["offset"] for r in ins]
    require(offsets == sorted(set(offsets)), "duplicate/unsorted JVM offsets")
    found = [(index, x) for index, x in enumerate(ins)
             if any(symbol in x["symbol"] for symbol in PIVOTS[cls])]
    # The enchantment owner method is long: a small window around every
    # meaningful use/lifespan/side-effect anchor suffices for interoperability.
    limit = 14 if cls == ITEM else 16
    windows = []
    for idx, hit in found[:limit]:
        start = max(0, idx - 5)
        stop = min(len(ins), idx + 9)
        selected = [{k: row[k] for k in ("offset", "opcode", "operand", "symbol")}
                    for row in ins[start:stop]]
        windows.append({"pivot": hit["offset"], "symbol": hit["symbol"],
                        "instructions": selected})
    require(sum(len(w["instructions"]) for w in windows) <= MAX_JVM_ROWS,
            "bounded clean-room JVM window budget exceeded")
    return windows


def method_report(method: dict, cls: str, prior_class: dict) -> dict:
    identity = (name_of(method), method["descriptor"])
    previous = [m for m in prior_class["methods"]
                if (m["name"], m["descriptor"]) == identity]
    require(len(previous) <= 1, "ambiguous previous JVM method")
    verified = 0
    if previous:
        rows = {r["offset"]: r for r in method["instructions"]}
        for anchor in previous[0]["anchors"]:
            current = rows.get(anchor["offset"])
            require(current is not None and
                    all(current[k] == anchor[k]
                        for k in ("opcode", "operand", "symbol")),
                    "exact previous contract anchor mismatch: " + identity[0])
            verified += 1
    return {
        "name": identity[0], "descriptor": identity[1],
        "instructions_total": len(method["instructions"]),
        "parsed_method_sha256": digest_method(method),
        "prior_exact_anchors_verified": verified,
        "windows": relevant_windows(method, cls),
    }


def discover(jar: Path, javap_bin: str, prior_path: Path = PRIOR) -> dict:
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "installed/publisher physical JAR SHA mismatch")
    prior_raw = prior_path.read_bytes()
    prior = json.loads(prior_raw)
    require(prior["artifact_sha256"] == SHA256 and
            prior["artifact_sha1"] == SHA1,
            "prior artifact identity drift")
    require(prior["classes"][ITEM]["sha256"] == SHA_ITEM and
            prior["classes"][HEX]["sha256"] == SHA_HEX and
            prior["resources"][ENCH] == SHA_ENCH,
            "prior Sugar Staff/Spell Lasting identity drift")
    with zipfile.ZipFile(jar) as z:
        members = z.namelist()
        require(len(members) == len(set(members)), "duplicate archive members")
        relevant = (ENCH, TAG, LANG_EN, LANG_PT, ITEM, HEX, REG)
        require(all(p in members for p in relevant), "missing resource/class")
        hashes = {p: sha(z.read(p)) for p in relevant}
        require(hashes[ITEM] == SHA_ITEM and hashes[HEX] == SHA_HEX and
                hashes[ENCH] == SHA_ENCH and hashes[TAG] == SHA_TAG,
                "publisher method owner or resource SHA drift")
        ench = json.loads(z.read(ENCH))
        tag = json.loads(z.read(TAG))
        require(ench.get("description", {}).get("translate") ==
                "enchantment.alexscaves.spell_lasting", "wrong enchantment")
        require(ench.get("supported_items") ==
                "#alexscaves:enchantable/sugar_staff", "wrong supported tag")
        require("alexscaves:sugar_staff" in tag.get("values", []),
                "Sugar Staff tag membership drift")
        translations = {}
        for lang, path in (("en_us", LANG_EN), ("pt_br", LANG_PT)):
            locales = json.loads(z.read(path))
            translations[lang] = {k: v for k, v in locales.items()
                                  if k.startswith("enchantment.alexscaves.spell_lasting")}
        classes = [p for p in members
                   if p.startswith(BASE) and p.endswith(".class")]
        require(100 <= len(classes) <= 3000, "unbounded provider class census")
        direct = sorted(p for p in classes if b"SPELL_LASTING" in z.read(p))
        require(ITEM in direct and REG in direct and len(direct) <= 10,
                "unexpected direct SPELL_LASTING class census")
    methods = {}
    method_counts = {}
    for cls in (ITEM, HEX):
        parsed = parse_methods(javap(javap_bin, jar, cls[:-6].replace("/", ".")))
        require(8 <= len(parsed) <= 100, "unexpected method population: " + cls)
        method_counts[cls] = len(parsed)
        chosen = [m for m in parsed if name_of(m) in FOCUS[cls]]
        require(len(chosen) == len({(name_of(m), m["descriptor"]) for m in chosen}),
                "ambiguous JVM method identity")
        methods[cls] = [method_report(m, cls, prior["classes"][cls])
                        for m in chosen if m["instructions"]]
    owner = [m for m in methods[ITEM] if m["name"] == "use"]
    require(len(owner) == 1, "must have exactly one Sugar Staff use")
    require(any("SPELL_LASTING" in w["symbol"] for w in owner[0]["windows"]),
            "no exact Spell Lasting owner callsite")
    require(owner[0]["prior_exact_anchors_verified"] >= 25,
            "missing previously proven Sugar Staff guards")
    require(any(m["name"] == "tick" and
                m["prior_exact_anchors_verified"] >= 7
                for m in methods[HEX]), "missing Hex tick lifecycle anchors")
    require(any(m["name"] == "readAdditionalSaveData" and
                m["prior_exact_anchors_verified"] >= 4
                for m in methods[HEX]), "missing Hex persisted state anchors")
    output = {
        "schema_version": 1,
        "scope": "SPELL_LASTING_1010_SHA_EXACT_STATIC_HEX_LIFESPAN",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "prior_contract_sha256": sha(prior_raw),
        "resources": {p: {"sha256": hashes[p],
                          "bytes": None if p in (ITEM, HEX, REG) else None}
                      for p in relevant},
        "enchantment": ench, "supported_tag": tag, "translations": translations,
        "class_census": {"classes_scanned": len(classes), "direct_token_hits": direct},
        "class_sha256": {p: hashes[p] for p in (ITEM, HEX, REG)},
        "method_counts": method_counts, "methods": methods,
        "limits": {"claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
                   "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
                   "mutation": "NO_MUTATION", "provider_universe_closed": False,
                   "gameplay_timing": "NOT_TESTED",
                   "effective_spawns": "NOT_VERIFIED",
                   "save_reload_owner_resolution": "NOT_TESTED"},
    }
    require(len(json.dumps(output).encode("utf-8")) < MAX_REPORT_BYTES,
            "clean-room report size exceeded")
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", type=Path, required=True)
    ap.add_argument("--javap", default="javap")
    ap.add_argument("--prior", type=Path, default=PRIOR)
    ap.add_argument("--seal", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    report = discover(args.jar, args.javap, args.prior)
    print("SPELL_LASTING_REPORT=" +
          json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    if args.seal:
        require(json.loads(args.seal.read_text(encoding="utf-8")) == report,
                "individual Spell Lasting manifest drift")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    print("SPELL_LASTING_PROBE=READONLY_NO_MUTATION")


if __name__ == "__main__":
    main()
