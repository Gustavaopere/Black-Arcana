#!/usr/bin/env python3
"""Regenerate catalog indexes with independent static-contract and runtime states.

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

if __package__:
    from . import check_perk_ready_indexes as qa
else:
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
    catalog_manifest_contents(provider, manifest, cards, files_key="source_files",
                              file_count_key="source_file_count",
                              class_count_key="java_file_count",
                              class_suffix=".java", label="source")


def catalog_manifest_contents(provider: str, manifest: dict, cards: list[Path], *,
                              files_key: str, file_count_key: str,
                              class_count_key: str, class_suffix: str,
                              label: str) -> None:
    """Validate a frozen card/member crosswalk without inferring gameplay QA."""
    hashes = manifest.get("cards")
    actual = {p.relative_to(ROOT).as_posix() for p in cards
              if p.is_relative_to(ROOT / provider)}
    if not isinstance(hashes, dict) or not hashes or set(hashes) != actual:
        raise ValueError(label + " catalog closure does not cover exactly the detected cards")
    for relative, expected in hashes.items():
        path = provider_evidence(provider, relative, ".md")
        data = path.read_bytes()
        if (not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or hashlib.sha256(data).hexdigest() != expected):
            raise ValueError(label + " catalog card changed")
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
        raise ValueError(label + " catalog object/aggregate crosswalk is incomplete")
    for aggregate in aggregates.values():
        if (not isinstance(aggregate, dict)
                or not isinstance(aggregate.get("reason"), str)
                or len(aggregate["reason"].strip()) < 18):
            raise ValueError(label + " catalog aggregate needs a bounded rationale")
        provider_evidence(provider, aggregate.get("evidence"), ".md")
    files = manifest.get(files_key)
    if (not isinstance(files, list) or not files
            or type(manifest.get(file_count_key)) is not int
            or manifest.get(file_count_key) != len(files)
            or type(manifest.get(class_count_key)) is not int
            or manifest.get(class_count_key) != sum(
                isinstance(source, dict) and isinstance(source.get("path"), str)
                and source["path"].endswith(class_suffix)
                for source in files)):
        raise ValueError(label + " catalog inspected-file manifest is empty")
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
            raise ValueError("invalid or unmapped inspected file file")
        if files_key == "artifact_files" and (type(source.get("bytes")) is not int
                or source["bytes"] < 0):
            raise ValueError("invalid artifact member byte count")
        seen.add(relative)
        referenced.update(refs)
    if not objects.keys() <= referenced:
        raise ValueError(label + " catalog objects lack inspected " + label + " references")


def artifact_catalog_scope(item: dict, cards: list[Path]) -> None:
    """Close a publisher artifact catalog without claiming source or installed parity."""
    provider = item["provider"]
    limits = {"installed_artifact_identity": "NOT_VERIFIED",
              "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED"}
    if (not isinstance(item.get("version"), str) or not item["version"].strip()
            or not isinstance(item.get("artifact_sha1"), str)
            or not re.fullmatch(r"[0-9a-f]{40}", item["artifact_sha1"])
            or not isinstance(item.get("artifact_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", item["artifact_sha256"])
            or type(item.get("artifact_size_bytes")) is not int
            or item["artifact_size_bytes"] <= 0
            or "source_revision" in item
            or any(item.get(key) != value for key, value in limits.items())):
        raise ValueError("publisher catalog lacks bounded identity or QA limits")
    facts = [line.strip() for line in provider_evidence(provider, item.get("evidence"), ".md")
             .read_text(encoding="utf8").splitlines()]
    identity = {key: item[key] for key in (
        "version", "artifact_sha1", "artifact_sha256", "artifact_size_bytes")}
    if ([line for line in facts if line.startswith("CATALOG_")]
            != ["CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY"]
            or any(line.startswith("source_revision=") for line in facts)
            or not all([line for line in facts if line.startswith(key + "=")]
                       == [f"{key}={value}"] for key, value in (identity | limits).items())):
        raise ValueError("publisher catalog proof lacks explicit artifact-only limits")
    manifest = json.loads(provider_evidence(provider, item.get("catalog_manifest"), ".json")
                          .read_text(encoding="utf8"), object_pairs_hook=qa._unique_pairs)
    if (not isinstance(manifest, dict)
            or type(manifest.get("schema_version")) is not int
            or manifest["schema_version"] != 1
            or type(manifest.get("artifact_size_bytes")) is not int
            or any(manifest.get(key) != value for key, value in identity.items())):
        raise ValueError("publisher catalog manifest identity mismatch")
    if (manifest.get("claim_scope") != "CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY"
            or "source_revision" in manifest
            or any(manifest.get(key) != value for key, value in limits.items())):
        raise ValueError("publisher catalog manifest lacks explicit artifact-only limits")
    catalog_manifest_contents(provider, manifest, cards, files_key="artifact_files",
                              file_count_key="artifact_file_count",
                              class_count_key="class_file_count",
                              class_suffix=".class", label="publisher")


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
        if item.get("state") == "PUBLISHER_ARTIFACT_CATALOG_CLOSED":
            artifact_catalog_scope(item, cards)
            continue
        if item.get("state") == "SOURCE_VERSION_CATALOG_CLOSED":
            source_catalog_scope(item, cards)
            continue
        mod = ROOT / item["provider"]
        evidence = item.get("evidence")
        if (item.get("state") != "NONMAGICAL_SCOPE_CLOSED"
                or type(item.get("owned_magic_actions")) is not int
                or item.get("owned_magic_actions") != 0
                or evidence != item["provider"] + "/README.md"
                or any(card.is_relative_to(mod) for card in cards)):
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
    alpha = (alphabetical if alphabetical is not None else
             alphabetical_scope(sorted(p for p in ROOT.iterdir() if p.is_dir()), cards))
    closed = {item["provider"]: item for item in alpha["completed_prefix"]}
    parts = folder.relative_to(ROOT).parts
    mod = ROOT / parts[0]
    group = sorted(p for p in cards if p.is_relative_to(folder))
    complete = sum(qa.certified(p, ledger) for p in group)
    documented = sum(qa.cataloged(p, ledger, closed) for p in group)
    catalog_complete = qa.folder_cataloged(folder, cards, ledger, closed)
    manifest_link = "../" * (len(parts) + 1) + "meta/PERK-READY-CERTIFICATIONS.json"
    catalog_bar = bar(documented, len(group)) if group else (
        "████████████████████ 100.0% — escopo fechado sem fichas" if catalog_complete
        else bar(0, 0))
    rows = [
        "# Índice do catálogo — " + " / ".join(friendly(x) for x in parts), "",
        "> Catálogo documentado, contrato técnico estático, hooks mutadores e QA "
        "físico têm estados independentes. Uma pasta antiga ✅ não constitui prova.", "",
        "**Catálogo desta árvore:** " + ("✅ documentado no escopo indicado abaixo."
            if catalog_complete else "⚠️ conclusão do escopo ainda não comprovada."), "",
        f"**Fichas catalogadas (somente fichas detectadas): {documented}/{len(group)}.**", "",
        f"**Barra das fichas catalogadas:** {TICK}{catalog_bar}{TICK}", "",
    ]
    item = closed.get(mod.name)
    if item:
        proof = "../" * (len(parts) - 1) + Path(item["evidence"]).relative_to(mod.name).as_posix()
        if item["state"] == "NONMAGICAL_SCOPE_CLOSED":
            rows += [
                "**Catalogação semântica (independente da homologação de perks):** "
                "✅ escopo encerrado: 0 feitiços, 0 rituais e 0 habilidades mágicas "
                f"próprias. Apenas apresentação visual; [evidência]({proof}).", ""
            ]
        else:
            qualifier = ("da versão-fonte" if item["state"] == "SOURCE_VERSION_CATALOG_CLOSED"
                         else "do artefato publisher")
            boundary = ("A prova cobre a versão-fonte fixada; identidade do binário instalado "
                        "não é inferida." if item["state"] == "SOURCE_VERSION_CATALOG_CLOSED" else
                        "A prova cobre o artefato publisher; paridade de fonte e identidade "
                        "do artefato instalado não são inferidas.")
            rows += [
                f"**Catalogação {qualifier} (independente da homologação de perks):** "
                f"✅ {len(group)}/{len(group)} fichas do escopo documentado; "
                f"versão {item['version']}. [Fechamento e limites]({proof}). "
                "Hooks mutadores e QA físico continuam pendentes.", "",
                f"**Barra do catálogo {qualifier}:** {TICK}{catalog_bar}{TICK}", "",
                "**Limite da prova do catálogo:** " + boundary, ""
            ]
    else:
        rows += [
            "**Limite da prova do catálogo:** apenas fichas com contratos técnicos estáticos "
            "certificados sustentam ✅ individual. O universo integral do provider "
            "continua não verificado; contagens observadas não encerram esse escopo.", ""
        ]
        if folder == mod and mod.name == alpha["next_provider"]:
            rows += [
                "**Fila alfabética:** 🟡 próximo provider a concluir. "
                "Não presumir 100% a partir de inventário agregado.", ""
            ]
    rows += [
        f"**Homologadas para perks (somente fichas detectadas): {complete}/{len(group)}.**", "",
        f"**Barra dos contratos técnicos estáticos:** {TICK}{bar(complete, len(group))}{TICK}", "",
        "**Limite da homologação:** os certificados acima cobrem contratos técnicos estáticos; "
        "catálogo concluído não promove hooks mutadores nem QA físico.", ""
    ]
    if folder == mod:
        known = ledger.get("known_rosters", {}).get(mod.name)
        if known:
            rows += [
                f'**Registro específico confirmado:** {known["scope"]}: {known["total"]} '
                f'([fonte]({known["source"]})). Outros sistemas/objetos podem existir.', ""
            ]
        rows += [
            ("**Homologação integral para perks:** ✅ 100% certificado com escopo fechado."
             if qa.mod_certified(mod, cards, ledger) else
             "**Homologação integral para perks:** ⚠️ NÃO HOMOLOGADO como 100%; "
             "universo integral ainda depende de validação."), ""
        ]
    elif group and complete == len(group):
        rows += [
            "**Contratos desta subpasta:** ✅ contratos técnicos estáticos de todas as "
            "fichas detectadas certificados; recorte documental, sem homologação "
            "de hooks mutadores, QA físico ou universo integral do provider.", ""
        ]
    else:
        rows += ["**Contratos desta subpasta:** ⚠️ validação técnica individual pendente.", ""]
    if group:
        rows += ["| Catálogo | Objeto / habilidade identificada | Ficha | Contrato estático | Hooks mutadores | QA físico |",
                 "|---|---|---|---|---|---|"]
        for card in group:
            rel = card.relative_to(folder).as_posix()
            category = "/".join(card.relative_to(folder).parts[:-1]) or "ficha"
            catalog, static, hook, physical = qa.card_states(card, ledger, closed)
            rows.append(f"| {catalog} | {friendly(card.stem)} | "
                        f"[{category}/{card.name}]({rel}) | {static} | {hook} | {physical} |")
    else:
        rows += [
            "*Nenhuma ficha individual detectada nesta árvore pelas regras conservadoras.* "
            + ("O fechamento acima documenta o escopo sem ações mágicas próprias."
               if item and item["state"] == "NONMAGICAL_SCOPE_CLOSED" else
               "Isso **não significa zero** magias/habilidades: podem existir inventários "
               "agregados, JSONs, classes ou registros ainda não desmembrados."), ""
        ]
    children = sorted(d for d in dirs if d.parent == folder)
    if children:
        rows += ["", "## Subpastas", "",
                 "| Catálogo | Subpasta | Fichas catalogadas / observadas | Contratos estáticos | Índice |",
                 "|---|---|---:|---:|---|"]
        for child in children:
            selected = [card for card in cards if card.is_relative_to(child)]
            mark = "✅" if qa.folder_cataloged(child, cards, ledger, closed) else "⚠️"
            static = sum(qa.certified(card, ledger) for card in selected)
            rows.append(f"| {mark} | {friendly(child.name)} | "
                        f"{qa.observed_catalog_count(selected, ledger, closed)} | {static} | "
                        f"[Abrir índice]({child.name}/INDEX.md) |")
    rows += [
        "", "## Critério do ✅", "",
        "**Catálogo:** fichas cobertas por fechamento validado de fonte/artefato no "
        "manifesto alfabético, ou por certificado técnico individual. O ✅ de uma "
        "subpasta cobre apenas seu recorte; o provider exige prova de escopo fechado.", "",
        "**Contrato estático:** somente fichas individualmente auditadas no manifesto "
        f"[PERK-READY-CERTIFICATIONS.json]({manifest_link}) recebem ✅ nessa coluna, "
        "exigindo identidade, comportamento, parâmetros, targeting, custos, "
        "boundary de integração e validação documentados. Hook inseguro ou "
        "desconhecido nunca é presumido. Hooks e QA exigem seus próprios estados "
        "verificados no certificado, sem promoção a partir do catálogo.", "",
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
    source_closed = sum(item["state"] == "SOURCE_VERSION_CATALOG_CLOSED"
                        for item in closed.values())
    artifact_closed = sum(item["state"] == "PUBLISHER_ARTIFACT_CATALOG_CLOSED"
                          for item in closed.values())
    next_mod = alpha["next_provider"]
    catalog_done = sum(qa.mod_cataloged(mod, cards, ledger, closed) for mod in mods)
    documented = sum(qa.cataloged(card, ledger, closed) for card in cards)
    done = sum(qa.mod_certified(mod, cards, ledger) for mod in mods)
    object_done = sum(qa.certified(card, ledger) for card in cards)
    rows = [
        "# Índice geral — catálogo documentado", "",
        "> ✅ na coluna Catálogo indica documentação comprovada no escopo informado. "
        "Contratos estáticos, hooks mutadores e QA físico têm estados separados; "
        "prefixos ✅ antigos não constituem prova.", "",
        f"**Providers com catálogo concluído: {catalog_done}/{len(mods)}.**", "",
        f"**Barra dos providers catalogados:** {TICK}{bar(catalog_done, len(mods))}{TICK}", "",
        f"**Fichas catalogadas (somente fichas detectadas): {documented}/{len(cards)}.**", "",
        f"**Barra das fichas catalogadas:** {TICK}{bar(documented, len(cards))}{TICK}", "",
        "**Escopo:** pastas atuais de providers; a modlist pode conter outros "
        "mods/sistemas ainda não representados. Objetos ausentes do catálogo "
        "não são presumidos inexistentes.", "",
        f"**Revisão alfabética do catálogo semântico:** {len(closed)}/{len(mods)} "
        "providers com escopo explicitamente encerrado: "
        f"{nonmagical} sem ações mágicas próprias e {source_closed} com catálogo "
        "da versão-fonte documentado"
        + (f" e {artifact_closed} com catálogo do artefato publisher documentado"
           if artifact_closed else "") + ". "
        "Esse contador NÃO equivale a providers perk-ready.", "",
        f"**Barra da revisão alfabética:** {TICK}{bar(len(closed), len(mods))}{TICK}", "",
        f"**Próximo na fila alfabética:** {friendly(next_mod) if next_mod else 'Nenhum'}.", "",
        f"**Fichas com contrato técnico estático certificado: {object_done}/{len(cards)}.**", "",
        f"**Barra das fichas estáticas observadas:** {TICK}{bar(object_done, len(cards))}{TICK}", "",
        f"**Mods com escopo integral certificado: {done}/{len(mods)}.**", "",
        f"**Progresso global confirmado (homologação integral para perks):** {TICK}{bar(done, len(mods))}{TICK}", "",
        "**Limite da homologação:** catálogo concluído não certifica contratos de perks, "
        "hooks mutadores nem QA físico. Os contadores técnicos acima continuam independentes.", "",
        "| Catálogo | Mod/provider | Fichas catalogadas / observadas | Contratos estáticos | "
        "Homologação integral para perks | Hooks mutadores | QA físico | Índice |",
        "|---|---|---:|---:|---|---|---|---|",
    ]
    for mod in mods:
        selected = [p for p in cards if p.is_relative_to(mod)]
        certified = sum(qa.certified(p, ledger) for p in selected)
        strict = qa.mod_certified(mod, cards, ledger)
        state = "✅" if qa.mod_cataloged(mod, cards, ledger, closed) else "⚠️"
        display = friendly(mod.name)
        if mod.name in closed:
            display += (" — ✅ escopo semântico encerrado (0 ações mágicas)"
                        if closed[mod.name]["state"] == "NONMAGICAL_SCOPE_CLOSED" else
                        " — ✅ catálogo da versão-fonte documentado"
                        if closed[mod.name]["state"] == "SOURCE_VERSION_CATALOG_CLOSED" else
                        " — ✅ catálogo do artefato publisher documentado")
        elif mod.name == next_mod:
            display += " — 🟡 próximo na fila"
        hook = qa.runtime_summary(selected, ledger, "mutating_hook", universe_closed=strict)
        physical = qa.runtime_summary(selected, ledger, "physical_qa", universe_closed=strict)
        rows.append(f"| {state} | {display} | "
                    f"{qa.observed_catalog_count(selected, ledger, closed)} | {certified} | "
                    f"{'✅' if strict else '⚠️'} | {hook} | {physical} | "
                    f"[Ver fichas]({mod.name}/INDEX.md) |")
    rows += [
        "", "**Legenda:** ✅ na coluna Catálogo = documentação comprovada no escopo "
        "indicado; ✅ nas colunas técnicas = prova específica daquela coluna; "
        "⚠️ = pendente ou escopo ainda não fechado; 🟡 = próximo na fila. "
        "Ausência de ficha detectada não prova que não exista conteúdo.", "",
        "**Limite dos percentuais:** fichas catalogadas / observadas mede apenas o recorte "
        "documental detectado. Mesmo 100% nessa coluna não fecha o universo de um provider "
        "sem evidência própria. A barra dos providers catalogados usa fechamentos de catálogo; "
        "a barra de homologação integral usa somente providers certificados para perks.", ""
    ]
    return "\n".join(rows)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="verify current committed indexes without modifications")
    args = p.parse_args()
    if args.check:
        result = qa.check()
        # The checker validates every index using one fresh, shared catalog proof
        # snapshot. Do not reread/hash closure manifests per folder or a second time.
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
