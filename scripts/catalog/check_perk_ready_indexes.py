#!/usr/bin/env python3
"""Audit global and per-folder perk-ready INDEX.md ledgers.

The old ✅ folder prefix means inventory, not technically complete. The checked
scope is the filesystem snapshot of individually identifiable Markdown cards.
It is NOT a claim that all JAR/JSON/aggregated objects have been discovered.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROVIDERS = REPO / "wiki/modpack-catalog/providers"
LEDGER = REPO / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
IGNORED_PARTS = frozenset({
    "audits", "audit", "technical", "references", "reference", "meta",
    "docs", "evidence", "qa", "source", "tests", "test", "examples",
    "example", "registry", "registries", "checkpoints", "snapshots",
    "resources", "assets", "research",
})
IGNORED_NAME = re.compile(
    r"^(?:index|overview|technical|catalog|progress|verification|source|audit|"
    r"summary|evidence|readme|changelog|inventory|gate|policy|checkpoint|"
    r"integration|compatibility|perk-ready|baseline|migration|coverage|notes|"
    r"safety|status|registry|qa)[-_]", re.I
)
# Ace 1.2.7.2 registers 27 example items unconditionally in production,
# plus one distinct ArmorMaterial. Other providers' example folders remain ignored.
# This exact allowlist prevents tutorial/example documentation from silently
# becoming a perk-ready candidate when it is not a real provider object.
ACES_1272_PRODUCTION_EXAMPLE_CARDS = frozenset({
    "example_ap_magic_sword.md",
    "example_ap_sword.md",
    "example_armor_boots.md",
    "example_armor_chestplate.md",
    "example_armor_helmet.md",
    "example_armor_leggings.md",
    "example_armor_material.md",
    "example_chromatic_aberration.md",
    "example_curio.md",
    "example_dome.md",
    "example_gun.md",
    "example_imbue_curio.md",
    "example_imbue_staff.md",
    "example_impact_frame_blue.md",
    "example_impact_frame_green.md",
    "example_impact_frame_purple.md",
    "example_impact_frame_red.md",
    "example_impact_frame_white.md",
    "example_impact_frame_white_aberration.md",
    "example_loot_bag.md",
    "example_passive_ability_spellbook.md",
    "example_ribbon.md",
    "example_roar.md",
    "example_roar_ring.md",
    "example_sheath.md",
    "example_staff.md",
    "example_trail.md",
    "example_unqiue_ability_spellbook.md",
})

REQUIRED_EVIDENCE = frozenset({
    "identity", "behavior", "parameters", "targeting", "costs",
    "integration", "validation",
})
PER_FOLDER = re.compile(r"\*\*Homologadas para perks \(somente fichas detectadas\): (\d+)/(\d+)\.\*\*")
GLOBAL = re.compile(r"\*\*Mods com escopo integral certificado: (\d+)/(\d+)\.\*\*")
GLOBAL_OBJECTS = re.compile(r"\*\*Fichas com contrato técnico estático certificado: (\d+)/(\d+)\.\*\*")
CARD_ROW = re.compile(r"^\| (✅|⚠️) \| .*? \| \[.*?\]\(([^)]+\.md)\) \|$", re.M)
PROVIDER_ROW = re.compile(r"^\| (✅|⚠️) \| .*? \| (?:\d+|—) \| \d+ \| \[Ver fichas\]\(([^)]+)/INDEX\.md\) \|$", re.M)

class CatalogIndexError(ValueError):
    pass

def _unique_pairs(pairs):
    found = {}
    for k, v in pairs:
        if k in found:
            raise CatalogIndexError("duplicate JSON key: " + k)
        found[k] = v
    return found

def read_ledger(path=None):
    if path is None:
        path = LEDGER
    doc = json.loads(path.read_text(encoding="utf8"), object_pairs_hook=_unique_pairs)
    if not isinstance(doc, dict) or doc.get("schema_version") != 1:
        raise CatalogIndexError("missing completion ledger schema v1")
    objects = doc.get("objects")
    if not isinstance(objects, dict) or not isinstance(doc.get("providers"), dict):
        raise CatalogIndexError("missing certification dictionaries")
    for rel, item in objects.items():
        p = PROVIDERS / rel
        if not p.is_file() or not is_card(p):
            raise CatalogIndexError("certificate path is not an individual card: " + rel)
        if not isinstance(item, dict) or item.get("status") != "COMPLETE_PERK_READY":
            raise CatalogIndexError("unrecognized certification state: " + rel)
        # A ✅ covers the static catalog contract, not approval to mutate
        # provider-native runtime. Version and exact physical artifact provenance
        # are mandatory; source-only semantics are clearly scoped.
        if item.get("claim_scope") != "STATIC_TECHNICAL_CATALOG_ONLY":
            raise CatalogIndexError("certification scope must be explicit and limited: " + rel)
        # Familiar source audits must not claim the glyph+ritual 109-ID
        # binary identity proof. Physical JAR SHA is release provenance only.
        source_grades = {
            "PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY",
            "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY",
        }
        if item.get("evidence_grade") not in source_grades | {
                "SHA_EXACT_BINARY_BEHAVIOR"}:
            raise CatalogIndexError("unknown or missing evidence grade: " + rel)
        if (item["evidence_grade"] in source_grades
                and (not isinstance(item.get("source_revision"), str)
                     or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}",
                                         item["source_revision"]))):
            raise CatalogIndexError("missing exact pinned source revision: " + rel)
        if not isinstance(item.get("version"), str) or not item["version"].strip():
            raise CatalogIndexError("missing exact provider release: " + rel)
        if not isinstance(item.get("artifact_sha1"), str) or not re.fullmatch(
                r"[0-9a-f]{40}", item["artifact_sha1"]):
            raise CatalogIndexError("missing SHA-1 physical release evidence: " + rel)
        if item.get("mutating_hook") not in {"NOT_VERIFIED", "VERIFIED_CONTRACT"}:
            raise CatalogIndexError("unsafe/ambiguous mutating-hook state: " + rel)
        if item.get("physical_qa") not in {"NOT_TESTED", "PHYSICALLY_VERIFIED"}:
            raise CatalogIndexError("unsafe/ambiguous physical QA state: " + rel)
        evidence = item.get("evidence")
        if not isinstance(evidence, dict) or set(evidence) != REQUIRED_EVIDENCE:
            raise CatalogIndexError("missing required technical evidence: " + rel)
        for field in sorted(REQUIRED_EVIDENCE):
            proof = evidence[field]
            if not isinstance(proof, dict) or set(proof) != {"path", "reason"}:
                raise CatalogIndexError("evidence must have path + reason: " + rel + " " + field)
            cited = proof["path"]
            why = proof["reason"]
            if not isinstance(cited, str) or not isinstance(why, str) or len(why.strip()) < 18:
                raise CatalogIndexError("empty/weak evidence locator or rationale: " + rel + " " + field)
            # Reject URL, absolute and parent escape; CI must be able to inspect
            # the referenced artifact inside this very checkout.
            parts = Path(cited).parts
            if not cited.endswith(".md") or not parts or any(
                    p in {"..", ".", ""} for p in parts
                ) or Path(cited).is_absolute() or "://" in cited:
                raise CatalogIndexError("nonlocal or unsafe evidence path: " + rel + " " + field)
            resolved = REPO.joinpath(*parts).resolve()
            if not resolved.is_relative_to(REPO.resolve()) or not resolved.is_file():
                raise CatalogIndexError("missing referenced evidence file: " + rel + " " + field)
    for mod, item in doc["providers"].items():
        if not (PROVIDERS / mod).is_dir() or not isinstance(item, dict):
            raise CatalogIndexError("invalid provider certification: " + mod)
        if item.get("universe_closed"):
            if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
                raise CatalogIndexError("provider universe cannot close without evidence: " + mod)
    return doc

def is_card(path: Path) -> bool:
    rel = path.relative_to(PROVIDERS)
    if path.suffix != ".md" or len(rel.parts) < 2:
        return False
    name = path.name
    if name in {"README.md", "INDEX.md"} or not re.match(r"^[a-z]", name) or IGNORED_NAME.match(name):
        return False
    if (len(rel.parts) == 3
            and rel.parts[:2] == ("✅-aces-spell-utils", "examples")
            and name in ACES_1272_PRODUCTION_EXAMPLE_CARDS):
        return True
    return not any(
        segment in IGNORED_PARTS or re.match(r"^(?:source-|registry-|audit-|technical-|evidence-)", segment, re.I)
        for segment in rel.parts[1:-1]
    )

def inventory():
    dirs = sorted((p for p in PROVIDERS.rglob("*") if p.is_dir()))
    mods = sorted((p for p in PROVIDERS.iterdir() if p.is_dir()))
    cards = sorted((p for p in PROVIDERS.rglob("*.md") if is_card(p)))
    return dirs, mods, cards

def certified(card, ledger):
    return card.relative_to(PROVIDERS).as_posix() in ledger["objects"]

def mod_certified(mod, cards, ledger):
    these = [p for p in cards if mod in p.parents]
    info = ledger["providers"].get(mod.name, {})
    return bool(these and all(certified(p, ledger) for p in these)
                and info.get("universe_closed") is True and info.get("evidence"))

def check(repo=REPO):
    global REPO, PROVIDERS, LEDGER
    previous_repo, previous_providers, previous_ledger = REPO, PROVIDERS, LEDGER
    REPO = repo
    PROVIDERS = repo / "wiki/modpack-catalog/providers"
    LEDGER = repo / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
    try:
        ledger = read_ledger(LEDGER)
        dirs, mods, cards = inventory()
        problems = []
        for folder in dirs:
            path = folder / "INDEX.md"
            if not path.is_file():
                problems.append("missing subfolder index: " + str(path.relative_to(repo)))
                continue
            data = path.read_text(encoding="utf8")
            known = [p for p in cards if folder in p.parents]
            done = sum(certified(p, ledger) for p in known)
            matches = PER_FOLDER.findall(data)
            if len(matches) != 1 or tuple(map(int, matches[0])) != (done, len(known)):
                problems.append("stale completion numerator/denominator: " + str(path.relative_to(repo)))
            table = {link: symbol for symbol, link in CARD_ROW.findall(data)}
            if len(table) != len(known):
                problems.append("card table population drift: " + str(path.relative_to(repo)))
            for card in known:
                rel = card.relative_to(folder).as_posix()
                expected = "✅" if certified(card, ledger) else "⚠️"
                if table.get(rel) != expected:
                    problems.append("missing/wrong card status: " + str(path.relative_to(repo)) + " => " + rel)
            for link in table:
                if not (folder / link).is_file():
                    problems.append("broken card link: " + str(path.relative_to(repo)) + " => " + link)
            for child in (p for p in dirs if p.parent == folder):
                if ("(" + child.name + "/INDEX.md)") not in data:
                    problems.append("missing child-index navigation: " + str(child.relative_to(repo)))
        root = PROVIDERS / "INDEX.md"
        if not root.is_file():
            problems.append("missing global index")
        else:
            data = root.read_text(encoding="utf8")
            done = sum(mod_certified(mod, cards, ledger) for mod in mods)
            match = GLOBAL.findall(data)
            if len(match) != 1 or tuple(map(int, match[0])) != (done, len(mods)):
                problems.append("stale global provider numerator/denominator")
            object_pairs = GLOBAL_OBJECTS.findall(data)
            completed_objects = sum(certified(card, ledger) for card in cards)
            if len(object_pairs) != 1 or tuple(map(int, object_pairs[0])) != (
                    completed_objects, len(cards)):
                problems.append("stale global certified-object numerator/denominator")
            entries = PROVIDER_ROW.findall(data)
            if len(entries) != len(mods):
                problems.append("provider table population drift")
            rows = {name: mark for mark, name in entries}
            for mod in mods:
                expected = "✅" if mod_certified(mod, cards, ledger) else "⚠️"
                if rows.get(mod.name) != expected:
                    problems.append("missing/wrong provider status: " + mod.name)
                if not (mod / "INDEX.md").is_file():
                    problems.append("missing provider file: " + mod.name)
        return {"directories": len(dirs), "providers": len(mods),
                "candidate_cards": len(cards), "certified_cards": sum(certified(p, ledger) for p in cards),
                "certified_providers": sum(mod_certified(m, cards, ledger) for m in mods),
                "expected_indexes": 1 + len(dirs), "problems": problems}
    finally:
        REPO, PROVIDERS, LEDGER = previous_repo, previous_providers, previous_ledger

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=REPO)
    args = p.parse_args()
    result = check(args.root)
    print(json.dumps({k: (v[:12] if k == "problems" else v) for k, v in result.items()},
                     indent=2, ensure_ascii=False))
    if result["problems"]:
        print("ERROR: index drift detected; update the affected provider/subfolder indexes before merging")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
