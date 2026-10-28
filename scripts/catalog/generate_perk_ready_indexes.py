#!/usr/bin/env python3
"""Regenerate strict perk-ready indexes; never infer 100% from legacy ✅ folders.

The denominator is individual Markdown cards found under providers, not every
possible object in compiled registries or aggregate JSON/catalog documents.
Run without flags to update all INDEX.md, then --check to verify consistency.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_perk_ready_indexes as qa

ROOT = qa.PROVIDERS
TICK = chr(96)

def friendly(value: str) -> str:
    return value.removeprefix("✅-").replace("_", " ").replace("-", " ").title()

def bar(done: int, total: int) -> str:
    count = (20 * done // total) if total else 0
    return ("█" * count + "░" * (20 - count) +
            (f" {100 * done / total:.1f}%" if total else " — não determinado"))

def canonical_relative_posix(relative: object) -> bool:
    """Reject aliases so one source file cannot inflate an inspected-file count."""
    return (isinstance(relative, str) and bool(relative)
            and "\\" not in relative and "\x00" not in relative
            and ":" not in relative
            and all(part not in {"", ".", ".."} for part in relative.split("/")))


def provider_evidence(provider: str, relative: str, suffix: str) -> Path:
    """Resolve a local closure artifact without escaping its provider."""
    if (not canonical_relative_posix(relative)
            or not relative.startswith(provider + "/")
            or not relative.endswith(suffix)):
        raise ValueError("unsafe alphabetical evidence path")
    path = (ROOT / relative).resolve()
    if not path.is_relative_to((ROOT / provider).resolve()) or not path.is_file():
        raise ValueError("missing alphabetical evidence artifact")
    return path


def source_catalog_scope(item: dict, cards: list[Path]) -> None:
    """Check a frozen source catalog without certifying perks or a binary build."""
    provider = item["provider"]
    revision = item.get("source_revision")
    if (not isinstance(revision, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}", revision)
            or not isinstance(item.get("version"), str) or not item["version"].strip()
            or not isinstance(item.get("artifact_sha1"), str)
            or not re.fullmatch(r"[0-9a-f]{40}", item["artifact_sha1"])
            or item.get("physical_qa") != "NOT_TESTED"
            or item.get("mutating_hook") != "NOT_VERIFIED"):
        raise ValueError("source catalog closure lacks bounded identity or QA limits")
    evidence = provider_evidence(provider, item.get("evidence"), ".md")
    facts = set(evidence.read_text(encoding="utf8").splitlines())
    if not all(token in facts for token in (
            "CATALOG_SOURCE_SCOPE_ONLY", revision,
            "version=" + item["version"], "artifact_sha1=" + item["artifact_sha1"],
            "physical_qa=NOT_TESTED", "mutating_hook=NOT_VERIFIED")):
        raise ValueError("source catalog proof lacks explicit source-only limits")
    manifest = json.loads(provider_evidence(
        provider, item.get("catalog_manifest"), ".json").read_text(encoding="utf8"),
        object_pairs_hook=qa._unique_pairs)
    if (not isinstance(manifest, dict)
            or type(manifest.get("schema_version")) is not int
            or manifest["schema_version"] != 1
            or manifest.get("source_revision") != revision
            or manifest.get("version") != item["version"]
            or manifest.get("artifact_sha1") != item["artifact_sha1"]):
        raise ValueError("source catalog manifest identity mismatch")
    if (manifest.get("claim_scope") != "CATALOG_SOURCE_SCOPE_ONLY"
            or manifest.get("physical_qa") != "NOT_TESTED"
            or manifest.get("mutating_hook") != "NOT_VERIFIED"):
        raise ValueError("source catalog manifest lacks explicit source-only limits")
    hashes = manifest.get("cards")
    actual = {p.relative_to(ROOT).as_posix() for p in cards
              if ROOT / provider in p.parents}
    if not isinstance(hashes, dict) or not hashes or set(hashes) != actual:
        raise ValueError("source catalog closure does not cover exactly the detected cards")
    for relative, expected in hashes.items():
        path = provider_evidence(provider, relative, ".md")
        data = path.read_bytes()
        if (not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or hashlib.sha256(data).hexdigest() != expected):
            raise ValueError("source catalog card changed")
    objects = manifest.get("catalog_objects")
    aggregates = manifest.get("aggregates")
    if (not isinstance(objects, dict) or not objects
            or not all(isinstance(key, str) and key.strip() for key in objects)
            or not all(isinstance(value, str) for value in objects.values())
            or set(objects.values()) != actual
            or len(objects) != len(actual)
            or not isinstance(aggregates, dict)
            or not all(isinstance(key, str) and key.strip() for key in aggregates)
            or set(objects) & set(aggregates)):
        raise ValueError("source catalog object/aggregate crosswalk is incomplete")
    for aggregate in aggregates.values():
        if (not isinstance(aggregate, dict)
                or not isinstance(aggregate.get("reason"), str)
                or len(aggregate["reason"].strip()) < 18):
            raise ValueError("source catalog aggregate needs a bounded rationale")
        provider_evidence(provider, aggregate.get("evidence"), ".md")
    files = manifest.get("source_files")
    if (not isinstance(files, list) or not files
            or type(manifest.get("source_file_count")) is not int
            or manifest.get("source_file_count") != len(files)
            or type(manifest.get("java_file_count")) is not int
            or manifest.get("java_file_count") != sum(
                isinstance(source, dict) and isinstance(source.get("path"), str)
                and source["path"].endswith(".java")
                for source in files)):
        raise ValueError("source catalog inspected-file manifest is empty")
    seen = set()
    referenced = set()
    catalog_keys = objects.keys() | aggregates.keys()
    for source in files:
        relative = source.get("path") if isinstance(source, dict) else None
        refs = source.get("catalog_refs") if isinstance(source, dict) else None
        if (not canonical_relative_posix(relative)
                or relative in seen
                or not isinstance(source.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"])
                or not isinstance(refs, list) or not refs
                or not all(isinstance(ref, str) and ref in catalog_keys
                           for ref in refs)):
            raise ValueError("invalid or unmapped inspected source file")
        seen.add(relative)
        referenced.update(refs)
    if not objects.keys() <= referenced:
        raise ValueError("source catalog objects lack inspected source references")


def alphabetical_scope(mods: list[Path], cards: list[Path]) -> dict:
    """Verified alphabetical triage; never imply perk-ready from semantic closure."""
    path = ROOT.parent / "meta/ALPHABETICAL-CATALOG-STATUS.json"
    if not path.is_file():
        return {"completed_prefix": [], "next_provider": None}
    doc = json.loads(path.read_text(encoding="utf8"), object_pairs_hook=qa._unique_pairs)
    if (not isinstance(doc, dict) or type(doc.get("schema_version")) is not int
            or doc["schema_version"] != 1
            or doc.get("order") != "provider_directory_name_ascending"):
        raise ValueError("invalid alphabetical catalog ledger schema")
    entries = doc.get("completed_prefix")
    names = [p.name for p in mods]
    if (not isinstance(entries, list) or len(entries) > len(names)
            or not all(isinstance(item, dict) for item in entries)):
        raise ValueError("invalid completed alphabetical prefix")
    if [x.get("provider") for x in entries] != names[:len(entries)]:
        raise ValueError("alphabetical catalog entries must be a contiguous provider prefix")
    if doc.get("next_provider") != (names[len(entries)] if len(entries) < len(names) else None):
        raise ValueError("next provider is not the next alphabetical entry")
    for item in entries:
        if item.get("state") == "SOURCE_VERSION_CATALOG_CLOSED":
            source_catalog_scope(item, cards)
            continue
        mod = ROOT / item["provider"]
        evidence = item.get("evidence")
        if (item.get("state") != "NONMAGICAL_SCOPE_CLOSED"
                or type(item.get("owned_magic_actions")) is not int
                or item.get("owned_magic_actions") != 0
                or evidence != item["provider"] + "/README.md"
                or any(mod in card.parents for card in cards)):
            raise ValueError("nonmagical catalog closure has unsupported claims")
        source = ROOT / evidence
        if not source.is_file():
            raise ValueError("nonmagical scope lacks a local evidence document")
        facts = source.read_text(encoding="utf8")
        if not all(token in facts for token in (
                "Provider-owned spells: **0**",
                "Provider-owned rituals/rites: **0**",
                "Provider-owned equivalent discrete magical actions: **0**")):
            raise ValueError("nonmagical source fails closed on missing zero-action proof")
    return doc


def directory_index(folder: Path, dirs: list[Path], cards: list[Path],
                    ledger: dict, *, alphabetical: dict | None = None) -> str:
    parts = folder.relative_to(ROOT).parts
    mod = ROOT / parts[0]
    group = sorted(p for p in cards if folder in p.parents)
    complete = sum(qa.certified(p, ledger) for p in group)
    manifest_link = "../" * (len(parts) + 1) + "meta/PERK-READY-CERTIFICATIONS.json"
    rows = [
        "# Índice técnico para perks — " + " / ".join(friendly(x) for x in parts), "",
        "> Índice das fichas individuais identificadas por nome de arquivo. Uma ficha "
        "existente ou pasta antiga ✅ não certifica parâmetros, fluxo causal, "
        "integração ou testes.", "",
        f"**Homologadas para perks (somente fichas detectadas): {complete}/{len(group)}.**",
        f"**Barra do recorte documental:** {TICK}{bar(complete, len(group))}{TICK}",
        "**Denominador de todo o conteúdo integrável:** não verificado; o recorte "
        "não equivale ao progresso total do mod.", "",
    ]
    if folder == mod:
        alpha = (alphabetical if alphabetical is not None else
                 alphabetical_scope(sorted(p for p in ROOT.iterdir() if p.is_dir()), cards))
        closed = {item["provider"]: item for item in alpha["completed_prefix"]}
        if mod.name in closed:
            item = closed[mod.name]
            if item["state"] == "NONMAGICAL_SCOPE_CLOSED":
                rows += [
                    "**Catalogação semântica (independente da homologação de perks):** "
                    "✅ escopo encerrado: 0 feitiços, 0 rituais e 0 habilidades mágicas "
                    "próprias. Apenas apresentação visual; [evidência](README.md).", ""
                ]
            else:
                proof = Path(item["evidence"]).relative_to(mod.name).as_posix()
                rows += [
                    "**Catalogação da versão-fonte (independente da homologação de perks):** "
                    f"✅ {len(group)}/{len(group)} fichas do escopo documentado; "
                    f"versão {item['version']}. [Fechamento e limites]({proof}). "
                    "Hooks mutadores e QA físico continuam pendentes.",
                    f"**Barra do catálogo da versão-fonte:** {TICK}{bar(len(group), len(group))}{TICK}",
                    ""
                ]
        elif mod.name == alpha["next_provider"]:
            rows += [
                "**Fila alfabética:** 🟡 próximo provider a concluir. "
                "Não presumir 100% a partir de inventário agregado.", ""
            ]
        known = ledger.get("known_rosters", {}).get(mod.name)
        if known:
            rows += [
                f'**Registro específico confirmado:** {known["scope"]}: {known["total"]} '
                f'([fonte]({known["source"]})). Outros sistemas/objetos podem existir.', ""
            ]
        rows += [
            ("**Estado técnico global:** ✅ 100% certificado com escopo fechado."
             if qa.mod_certified(mod, cards, ledger) else
             "**Estado técnico global:** ⚠️ NÃO HOMOLOGADO como 100%; "
             "universo integral ainda depende de validação."), ""
        ]
    elif group and complete == len(group):
        rows += [
            "**Estado desta subpasta:** ✅ contratos técnicos estáticos de todas as "
            "fichas detectadas certificados; recorte documental, sem homologação "
            "de hooks mutadores, QA físico ou universo integral do provider.", ""
        ]
    else:
        rows += [
            "**Estado desta subpasta:** ⚠️ validação técnica individual pendente; "
            "status histórico de catálogo não é certificação.", ""
        ]
    if group:
        rows += ["| Estado | Objeto / habilidade identificada | Ficha |", "|---|---|---|"]
        for card in group:
            rel = card.relative_to(folder).as_posix()
            category = "/".join(card.relative_to(folder).parts[:-1]) or "ficha"
            symbol = "✅" if qa.certified(card, ledger) else "⚠️"
            rows.append(f"| {symbol} | {friendly(card.stem)} | "
                        f"[{category}/{card.name}]({rel}) |")
    else:
        rows += [
            "*Nenhuma ficha individual detectada nesta árvore pelas regras conservadoras.* "
            "Isso **não significa zero** magias/habilidades: podem existir inventários "
            "agregados, JSONs, classes ou registros ainda não desmembrados.", ""
        ]
    children = sorted(d for d in dirs if d.parent == folder)
    if children:
        rows += ["", "## Subpastas", "",
                 "| Subpasta | Fichas individuais detectadas | Índice |", "|---|---:|---|"]
        for child in children:
            count = sum(child in card.parents for card in cards)
            rows.append(f"| {friendly(child.name)} | {count} | "
                        f"[Abrir índice]({child.name}/INDEX.md) |")
    rows += [
        "", "## Critério do ✅", "",
        "Somente fichas individualmente auditadas no manifesto "
        f"[PERK-READY-CERTIFICATIONS.json]({manifest_link}) podem receber ✅, "
        "exigindo identidade, comportamento, parâmetros, targeting, custos, "
        "boundary de integração e validação documentados. Hook inseguro ou "
        "desconhecido nunca é presumido.", "",
        "Arquivos técnicos de apoio e inventários agregados continuam relevantes, "
        "mas não são contabilizados como objetos concluídos. O algoritmo deve "
        "ser revisado por provider antes de declarar universo fechado.", ""
    ]
    return "\n".join(rows)

def global_index(mods: list[Path], cards: list[Path], ledger: dict, *,
                 alphabetical: dict | None = None) -> str:
    alpha = alphabetical if alphabetical is not None else alphabetical_scope(mods, cards)
    closed = {item["provider"]: item for item in alpha["completed_prefix"]}
    nonmagical = sum(item["state"] == "NONMAGICAL_SCOPE_CLOSED" for item in closed.values())
    source_closed = len(closed) - nonmagical
    next_mod = alpha["next_provider"]
    done = sum(qa.mod_certified(mod, cards, ledger) for mod in mods)
    object_done = sum(qa.certified(card, ledger) for card in cards)
    rows = [
        "# Índice geral — certificação 100% para perks", "",
        "> Os prefixos ✅ antigos significam inventário histórico, não 100% técnico "
        "para perks.", "",
        f"**Mods com escopo integral certificado: {done}/{len(mods)}.**",
        f"**Fichas com contrato técnico estático certificado: {object_done}/{len(cards)}.**",
        f"**Barra das fichas estáticas observadas:** {TICK}{bar(object_done, len(cards))}{TICK}",
        f"**Progresso global confirmado:** {TICK}{bar(done, len(mods))}{TICK}",
        "**Escopo:** pastas atuais de providers; a modlist pode conter outros "
        "mods/sistemas ainda não representados. Objetos ausentes do catálogo "
        "não são presumidos inexistentes.", "",
        f"**Revisão alfabética do catálogo semântico:** {len(closed)}/{len(mods)} "
        "providers com escopo explicitamente encerrado: "
        f"{nonmagical} sem ações mágicas próprias e {source_closed} com catálogo "
        "da versão-fonte documentado. "
        "Esse contador NÃO equivale a providers perk-ready.",
        f"**Barra da revisão alfabética:** {TICK}{bar(len(closed), len(mods))}{TICK}",
        f"**Próximo na fila alfabética:** {friendly(next_mod) if next_mod else 'Nenhum'}.", "",
        "| Estado 100% | Mod/provider | Fichas individuais candidatas | "
        "Fichas 100% certificadas | Índice |", "|---|---|---:|---:|---|",
    ]
    for mod in mods:
        selected = [p for p in cards if mod in p.parents]
        certified = sum(qa.certified(p, ledger) for p in selected)
        state = "✅" if qa.mod_certified(mod, cards, ledger) else "⚠️"
        display = friendly(mod.name)
        if mod.name in closed:
            display += (" — ✅ escopo semântico encerrado (0 ações mágicas)"
                        if closed[mod.name]["state"] == "NONMAGICAL_SCOPE_CLOSED" else
                        " — ✅ catálogo da versão-fonte documentado")
        elif mod.name == next_mod:
            display += " — 🟡 próximo na fila"
        rows.append(f"| {state} | {display} | "
                    f"{len(selected) if selected else '—'} | {certified} | "
                    f"[Ver fichas]({mod.name}/INDEX.md) |")
    rows += [
        "", "**Legenda:** ✅ 100% certificado; ⚠️ parcial/condicionado ou ainda não "
        "homologado; ❌ não catalogado após auditoria específica; 🟡 em implementação; "
        "⛔ bloqueado por contrato. Ausência de ficha detectada não prova que "
        "não exista conteúdo.", "",
        "**Atenção:** as fichas candidatas são um recorte documental, NÃO o "
        "universo total de feitiços e sistemas. A barra de fichas estáticas observadas "
        "usa certificados/fichas detectadas. A barra Progresso global confirmado "
        "usa providers com escopo integral certificado.", ""
    ]
    return "\n".join(rows)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="verify current committed indexes without modifications")
    args = p.parse_args()
    if args.check:
        result = qa.check()
        ledger = qa.read_ledger(qa.LEDGER)
        dirs, mods, cards = qa.inventory()
        alpha = alphabetical_scope(mods, cards)
        # Verify the generated alphabetical ledger text as well as the numeric
        # index contract, so catalog status cannot be silently hand-edited.
        expected = global_index(mods, cards, ledger, alphabetical=alpha)
        if (ROOT / "INDEX.md").read_text(encoding="utf8") != expected:
            result["problems"].append("global alphabetical catalog status drift")
        watched = {item["provider"] for item in alpha["completed_prefix"]}
        if alpha["next_provider"]:
            watched.add(alpha["next_provider"])
        for name in watched:
            folder = ROOT / name
            expected_mod = directory_index(folder, dirs, cards, ledger, alphabetical=alpha)
            if (folder / "INDEX.md").read_text(encoding="utf8") != expected_mod:
                result["problems"].append("provider alphabetical catalog status drift: " + name)
        print(f"INDEX CHECK: {result['expected_indexes']} indexes, "
              f"{result['candidate_cards']} candidate cards, "
              f"{len(result['problems'])} errors")
        return int(bool(result["problems"]))
    ledger = qa.read_ledger(qa.LEDGER)
    dirs, mods, cards = qa.inventory()
    # Freeze validation for this invocation only: rendering changes INDEX.md,
    # while a subsequent invocation must recheck every proof and card hash.
    alpha = alphabetical_scope(mods, cards)
    changed = 0
    for folder in dirs:
        dest = folder / "INDEX.md"
        data = directory_index(folder, dirs, cards, ledger, alphabetical=alpha)
        if not dest.is_file() or dest.read_text(encoding="utf8") != data:
            dest.write_text(data, encoding="utf8")
            changed += 1
    dest = ROOT / "INDEX.md"
    data = global_index(mods, cards, ledger, alphabetical=alpha)
    if not dest.is_file() or dest.read_text(encoding="utf8") != data:
        dest.write_text(data, encoding="utf8")
        changed += 1
    print(f"Generated {len(dirs) + 1} indexes; changed={changed}; "
          f"providers={len(mods)} cards={len(cards)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
